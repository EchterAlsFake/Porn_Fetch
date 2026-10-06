import asyncio
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone
from pathlib import Path

from curl_cffi import Response
from PySide6.QtCore import QCoreApplication, QFile, QIODevice, QObject, Signal

from src.backend import clients
from src.backend.helper_functions import get_original_executable_path
from src.backend.shared_functions import configure_app_logging
from src.shared.paths import shared_data_dir
from src.shared.release import ROOT_FILE, update_eligibility, verify_repository_manifest
from src.shared.version import BUILD_VERSION as __version__

logger = configure_app_logging(logger_name="PornFetch - [Update]")

DEFAULT_UPDATE_URL = "https://api.pornfetch.to/update"
UPDATE_URL_ENVIRONMENT_VARIABLE = "PORNFETCH_UPDATE_URL"
DEFAULT_REPO_BASE_URL = "https://api.pornfetch.to/repo"


def get_update_url() -> str:
    """Return the production endpoint unless a development override is set."""
    return os.environ.get(UPDATE_URL_ENVIRONMENT_VARIABLE, DEFAULT_UPDATE_URL)


def find_maintenance_tool() -> Path | None:
    """Locate the Qt Installer Framework maintenancetool binary in the installed application directory."""
    if env_path := os.environ.get("PORNFETCH_MAINTENANCETOOL_PATH"):
        p = Path(env_path).expanduser().resolve()
        if p.is_file() and (sys.platform == "win32" or os.access(p, os.X_OK)):
            return p

    orig = get_original_executable_path()
    if orig is None:
        return None

    name = "maintenancetool.exe" if sys.platform == "win32" else "maintenancetool"
    candidates = [
        orig.parent / name,
        orig.parent.parent / name,
        orig.parent.parent.parent.parent / "maintenancetool.app" / "Contents" / "MacOS" / "maintenancetool",
    ]
    for candidate in candidates:
        if candidate.is_file() and (sys.platform == "win32" or os.access(candidate, os.X_OK)):
            return candidate.resolve()
    return None


class CheckUpdates:
    """Checks for available updates via Qt IFW maintenancetool or the remote update server."""

    @staticmethod
    async def check() -> dict | None:
        try:
            return await CheckUpdates.check_signed_repository()
        except Exception:
            # Legacy discovery is informational only; installation requires a signed repository.
            update = await CheckUpdates.check_via_http()
            if update:
                update.update(install_allowed=False, entitlement_message="Release metadata could not be authenticated. Automatic installation is unavailable.")
            return update

    @staticmethod
    async def check_signed_repository() -> dict | None:
        tag = platform.system().lower() + "_" + {"x86_64": "amd64", "x64": "amd64", "aarch64": "arm64"}.get(platform.machine().lower(), platform.machine().lower())
        url = DEFAULT_REPO_BASE_URL + "/" + tag + "/"
        response = await clients.core.request(url=url + "release.json", allow_redirects=False, timeout=20)
        resource = QFile(":/updates/root.json")
        if resource.exists():
            if not resource.open(QIODevice.OpenModeFlag.ReadOnly):
                raise ValueError("Cannot load update trust root")
            try:
                root_bytes = bytes(resource.readAll())
            finally:
                resource.close()
        else:
            root_bytes = ROOT_FILE.read_bytes()
        metadata, release = verify_repository_manifest(response.content, root_bytes, tag)
        if CheckUpdates._version_parts(release["version"]) <= CheckUpdates._version_parts(__version__):
            return None
        return {**release, "metadata": metadata, "repository_url": url, "source": "signed_repository"}

    @staticmethod
    async def check_via_maintenancetool() -> dict | None:
        tool = find_maintenance_tool()
        if not tool:
            return None

        logger.info("Checking for updates via Qt maintenancetool: %s", tool)
        try:
            creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            proc = await asyncio.create_subprocess_exec(
                str(tool),
                "check-updates",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(tool.parent),
                creationflags=creationflags,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
            output = stdout.decode("utf-8", errors="replace").strip()

            if "<updates>" in output and "<update " in output:
                root = ET.fromstring(output)
                update_el = root.find("update")
                if update_el is not None:
                    version = update_el.get("version", "latest")
                    name = update_el.get("name", "Porn Fetch")
                    logger.info("maintenancetool reports update available: %s v%s", name, version)
                    return {
                        "version": version,
                        "name": name,
                        "size": update_el.get("size", "0"),
                        "source": "maintenancetool",
                    }
        except (asyncio.TimeoutError, Exception) as exc:
            logger.warning("maintenancetool update check failed or timed out: %s", exc)

        return None

    @staticmethod
    async def check_via_http() -> dict | None:
        url = get_update_url()
        try:
            response: Response = await clients.core.request(url=url)
            if response.status_code == 200:
                update = response.json()
                version = str(update.get("version", "")).removeprefix("latest - ").strip()
                if CheckUpdates._version_parts(version) > CheckUpdates._version_parts(__version__):
                    logger.info("A new update is available: %s", version)
                    return update
                logger.info("Application is up to date (%s)", __version__)
            elif response.status_code == 404:
                logger.error("Update endpoint returned 404")
            elif response.status_code in {500, 502, 530}:
                logger.error("Update server is temporarily unavailable (status %s)", response.status_code)
        except Exception as error:
            logger.warning("Could not check for updates via HTTP: %s", error)

        return None

    @staticmethod
    def _version_parts(version: str) -> tuple[int, ...]:
        """Return numeric version components without relying on float parsing."""
        parts = [int(part) for part in re.findall(r"\d+", version)]
        while len(parts) > 1 and parts[-1] == 0:
            parts.pop()
        return tuple(parts) or (0,)


class AutoUpdater(QObject):
    """Orchestrates Qt Installer Framework maintenancetool to update the installed application."""

    statusReport = Signal(str)
    updateProgress = Signal(int, int)

    def __init__(
        self,
        parent: QObject | None = None,
        before_update: Callable[[], Awaitable[None]] | None = None,
        license_status: Callable[[], Awaitable] | None = None,
    ) -> None:
        super().__init__(parent)
        self.before_update = before_update
        self.license_status = license_status

    async def run(self) -> None:
        try:
            await self._run()
        except asyncio.CancelledError:
            raise
        except Exception as error:
            logger.exception("Update launch failed")
            self.statusReport.emit(f"Update failed: {error}")

    async def _run(self) -> None:
        tool = find_maintenance_tool()
        if not tool:
            self.statusReport.emit(
                "Automatic updates require an installation managed by the Qt Maintenance Tool.\n"
                "Please download the latest beta build from "
                "https://github.com/EchterAlsFake/Porn_Fetch/releases/"
            )
            return

        if self.license_status is None:
            self.statusReport.emit("Validate your production license before updating.")
            return
        update = await CheckUpdates.check_signed_repository()
        if update is None:
            self.statusReport.emit("No update available.")
            return
        status = await self.license_status()
        entitled, reason = update_eligibility(status, update["release_timestamp"])
        self.statusReport.emit(reason)
        if not entitled:
            return
        repository = await self._stage_repository(update)

        self.statusReport.emit("Preparing update: stopping background services...")

        # Gracefully stop PocketBase and close sessions so binaries are not locked on Windows
        if self.before_update:
            try:
                await self.before_update()
            except Exception as exc:
                logger.warning("Error during pre-update cleanup: %s", exc)

        self.statusReport.emit("Launching Qt Maintenance Tool...")
        logger.info("Launching maintenancetool: %s --updater", tool)

        creationflags = subprocess.DETACHED_PROCESS if sys.platform == "win32" else 0
        subprocess.Popen(
            [str(tool), "--updater", "--set-temp-repository", repository.as_uri()],
            cwd=str(tool.parent),
            creationflags=creationflags,
            start_new_session=(sys.platform != "win32"),
        )

        self.statusReport.emit("Updater launched. Closing Porn Fetch...")
        await asyncio.sleep(0.5)
        QCoreApplication.quit()

    async def _stage_repository(self, update):
        """Pin ALL IFW metadata and payload bytes before handing control to IFW."""
        cache = shared_data_dir() / "verified-updates"
        cache.mkdir(parents=True, exist_ok=True, mode=0o700)
        stage = Path(tempfile.mkdtemp(prefix="repository-", dir=cache))
        try:
            metadata = update["metadata"]
            for name, target in metadata.signed.targets.items():
                response = await clients.core.request(
                    url=update["repository_url"] + name, allow_redirects=False, timeout=120,
                )
                target.verify_length_and_hashes(response.content)
                path = stage / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(response.content)
            xml = ET.parse(stage / "Updates.xml")
            packages = xml.findall("PackageUpdate")
            release_date = datetime.fromtimestamp(update["release_timestamp"], timezone.utc).strftime("%Y-%m-%d")
            if (len(packages) != 1 or packages[0].findtext("Version") != update["version"]
                    or packages[0].findtext("ReleaseDate") != release_date
                    or xml.find("RepositoryUpdate") is not None):
                raise ValueError("Qt repository does not match the authenticated release")
            # All content is local and hash checked; remote repository substitutions are forbidden.
            if any(el.tag in {"DownloadableArchives", "UpdateFile"} and "://" in (el.text or "") for el in xml.iter()):
                raise ValueError("External update content is not permitted")
            return stage
        except BaseException:
            shutil.rmtree(stage)
            raise
