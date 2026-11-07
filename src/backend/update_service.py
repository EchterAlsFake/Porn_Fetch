import asyncio
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import xml.etree.ElementTree as ET
from collections.abc import Awaitable, Callable
from pathlib import Path
from urllib.parse import quote

from curl_cffi import Response
from PySide6.QtCore import QCoreApplication, QFile, QIODevice, QObject, Signal
from tuf.api.serialization import DeserializationError

from src.backend import clients
from src.backend.helper_functions import get_original_executable_path
from src.shared.logging_setup import configure_app_logging
from src.shared.paths import shared_data_dir
from src.shared.release import ROOT_FILE, validate_ifw_packages, verify_repository_manifest
from src.shared.service_transport import ServiceCore
from src.shared.version import BUILD_VERSION as __version__

logger = configure_app_logging(logger_name="PornFetch - [Update]")

DEFAULT_UPDATE_URL = "https://api.pornfetch.to/update"
UPDATE_URL_ENVIRONMENT_VARIABLE = "PORNFETCH_UPDATE_URL"
DEFAULT_REPO_BASE_URL = "https://api.pornfetch.to/repo"
service_core = ServiceCore(clients.app_settings)


def _metadata_error(message):
    if service_core.tor_enabled:
        return service_core.policy.failed("metadata", detail=message)
    return ValueError(message)


def get_update_url() -> str:
    """Return the production endpoint unless a development override is set."""
    return os.environ.get(UPDATE_URL_ENVIRONMENT_VARIABLE, DEFAULT_UPDATE_URL)


def find_maintenance_tool() -> Path | None:
    """Locate the Qt Installer Framework maintenancetool binary in the installed application directory."""
    if env_path := os.environ.get("PORNFETCH_MAINTENANCETOOL_PATH"):
        p = Path(env_path).expanduser().resolve()
        if p.is_file() and (sys.platform == "win32" or os.access(p, os.X_OK)):
            return p

    try:
        orig = get_original_executable_path()
    except FileNotFoundError:
        return None
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


def launch_maintenance_tool(tool: Path, mode: str, *, repository: Path | None = None) -> None:
    """Keep IFW on local files; the app owns all repository network traffic."""
    flags = {"update": "--updater", "components": "--start-package-manager", "uninstall": "--start-uninstaller"}
    flag = flags[mode]
    if repository is None:
        if mode != "uninstall":
            raise ValueError("A verified local repository is required")
        cache = shared_data_dir() / "verified-updates"
        cache.mkdir(parents=True, exist_ok=True, mode=0o700)
        repository = Path(tempfile.mkdtemp(prefix="uninstall-", dir=cache))
        # Removal needs no remote packages, including if the user switches modes.
        (repository / "Updates.xml").write_text("<Updates/>\n", encoding="utf-8")
    subprocess.Popen(
        [str(tool), flag, "--set-temp-repository", repository.as_uri(), "--no-proxy"],
        cwd=str(tool.parent),
        creationflags=subprocess.DETACHED_PROCESS if sys.platform == "win32" else 0,
        start_new_session=sys.platform != "win32",
    )


class CheckUpdates:
    """Checks for available updates via Qt IFW maintenancetool or the remote update server."""

    @staticmethod
    async def check() -> dict | None:
        from src.shared.android_updates import check, is_android_device
        if is_android_device():
            return await asyncio.to_thread(check, clients.app_settings, __version__)
        try:
            return await CheckUpdates.check_signed_repository()
        except Exception:
            if service_core.tor_enabled:
                raise
            logger.warning("Signed release metadata is unavailable. Falling back to informational update discovery; automatic installation remains disabled.")
            # Legacy discovery is informational only; installation requires a signed repository.
            update = await CheckUpdates.check_via_http()
            if update:
                update.update(install_allowed=False, entitlement_message="Release metadata could not be authenticated. Automatic installation is unavailable.")
            return update

    @staticmethod
    async def check_signed_repository(*, include_current: bool = False) -> dict | None:
        tag = platform.system().lower() + "_" + {"x86_64": "amd64", "x64": "amd64", "aarch64": "arm64"}.get(platform.machine().lower(), platform.machine().lower())
        url = DEFAULT_REPO_BASE_URL + "/" + tag + "/"
        response = await service_core.request(url=url + "release.json", allow_redirects=False)
        if response.status_code != 200:
            raise _metadata_error(f"The update metadata request returned HTTP {response.status_code}; expected HTTP 200.")
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
        try:
            metadata, release = verify_repository_manifest(response.content, root_bytes, tag)
        except DeserializationError as error:
            content_type = response.headers.get("Content-Type", "unspecified")
            logger.error("Unreadable signed update metadata from %s (HTTP %s, Content-Type %s)",
                         url + "release.json", response.status_code, content_type)
            raise _metadata_error("The update server returned a response that could not be read as signed JSON metadata.") from error
        published = CheckUpdates._version_parts(release["version"])
        installed = CheckUpdates._version_parts(__version__)
        if include_current and published < installed:
            raise ValueError("The published component repository is older than this installation. Try again after its release repository is published.")
        if published < installed or (published == installed and not include_current):
            return None
        if changelog_path := release.get("changelog_path"):
            try:
                notes = await service_core.fetch_bytes(
                    url + quote(changelog_path, safe="/"), allow_redirects=False,
                )
                metadata.signed.targets[changelog_path].verify_length_and_hashes(notes)
                release = {**release, "changelog": notes.decode("utf-8"), "changelog_format": "markdown"}
            except Exception:
                logger.warning("Could not fetch the verified release changelog; using the signed manifest's notes.")
        return {**release, "metadata": metadata, "repository_url": url, "source": "signed_repository"}

    @staticmethod
    async def check_via_maintenancetool() -> dict | None:
        if service_core.tor_enabled:
            return await CheckUpdates.check_signed_repository()
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
            response: Response = await service_core.request(url=url)
            if response.status_code == 200:
                update = response.json()
                version = str(update.get("version", "")).removeprefix("latest - ").strip()
                if CheckUpdates._version_parts(version) > CheckUpdates._version_parts(__version__):
                    logger.info("A new update is available: %s", version)
                    return update
                logger.info("Legacy update discovery reports no newer version (%s); this does not authenticate the signed release repository.", __version__)
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
    updateProgress = Signal(float, float)
    finished = Signal()
    outcome = Signal(str, str)

    def __init__(
        self,
        parent: QObject | None = None,
        before_update: Callable[[], Awaitable[None]] | None = None,
        request_shutdown: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(parent)
        self.before_update = before_update
        self.request_shutdown = request_shutdown
        self._android_cancel = threading.Event()

    async def run(self, mode: str = "update") -> None:
        try:
            await self._run(mode)
        except asyncio.CancelledError:
            self._android_cancel.set()
            self.outcome.emit("info", self.tr("Update cancelled."))
            raise
        except Exception as error:
            logger.exception("Update launch failed")
            message = self.tr("Could not prepare the update: %s: %s") % (type(error).__name__, error)
            self.statusReport.emit(message)
            self.outcome.emit("error", message)
        finally:
            self.finished.emit()

    async def _run(self, mode: str = "update") -> None:
        if mode not in {"update", "components"}:
            raise ValueError(f"Unsupported maintenance mode: {mode}")
        from src.shared.android_updates import download_and_request_install, is_android_device
        if is_android_device():
            self.statusReport.emit(self.tr("Downloading and verifying the Android update…"))
            self._android_cancel.clear()
            downloaded = 0
            def progress(size):
                nonlocal downloaded
                downloaded += size
                self.updateProgress.emit(downloaded, 0)
            await asyncio.to_thread(download_and_request_install, clients.app_settings, __version__,
                                    progress, self._android_cancel)
            message = self.tr("APK verified. Waiting for Android's installation confirmation…")
            self.statusReport.emit(message)
            self.outcome.emit("info", message)
            return
        tool = find_maintenance_tool()
        if not tool:
            message = self.tr("Automatic updates require the Qt Maintenance Tool. Download the latest build from the website instead.")
            self.statusReport.emit(message)
            self.outcome.emit("warning", message)
            return

        update = (await CheckUpdates.check_signed_repository(include_current=True)
                  if mode == "components" else await CheckUpdates.check_signed_repository())
        if update is None:
            message = self.tr("No update available.")
            self.statusReport.emit(message)
            self.outcome.emit("info", message)
            return
        repository = await self._stage_repository(update)

        self.statusReport.emit(self.tr("Preparing the verified update…"))

        # Gracefully stop PocketBase and close sessions so binaries are not locked on Windows
        if self.before_update:
            try:
                await self.before_update()
            except Exception as exc:
                logger.warning("Error during pre-update cleanup: %s", exc)

        self.statusReport.emit("Launching Qt Maintenance Tool...")
        logger.info("Launching maintenancetool: %s (%s, verified local repository)", tool, mode)
        launch_maintenance_tool(tool, mode, repository=repository)

        self.statusReport.emit("Updater launched. Closing Porn Fetch...")
        if self.request_shutdown:
            # Use the same cooperative download/recovery teardown as a normal
            # window close. Only start it after the installer was opened.
            self.request_shutdown()
        else:
            QCoreApplication.quit()

    async def _stage_repository(self, update):
        """Pin ALL IFW metadata and payload bytes before handing control to IFW."""
        cache = shared_data_dir() / "verified-updates"
        cache.mkdir(parents=True, exist_ok=True, mode=0o700)
        stage = Path(tempfile.mkdtemp(prefix="repository-", dir=cache))
        try:
            metadata = update["metadata"]
            total = sum(target.length for target in metadata.signed.targets.values())
            completed = 0
            self.statusReport.emit(self.tr("Downloading and verifying the update…"))
            self.updateProgress.emit(0, total)
            for name, target in metadata.signed.targets.items():
                path = stage / name
                path.parent.mkdir(parents=True, exist_ok=True)
                await service_core.download_verified(
                    update["repository_url"] + quote(name, safe="/"), target, path,
                    on_progress=lambda size: self.updateProgress.emit(completed + size, total),
                )
                completed += target.length
            xml = ET.parse(stage / "Updates.xml")
            validate_ifw_packages(xml, update["version"], update["release_timestamp"])
            # All content is local and hash checked; remote repository substitutions are forbidden.
            if any(el.tag in {"DownloadableArchives", "UpdateFile"} and "://" in (el.text or "") for el in xml.iter()):
                raise ValueError("External update content is not permitted")
            return stage
        except BaseException:
            shutil.rmtree(stage)
            raise
