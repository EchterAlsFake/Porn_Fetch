import asyncio
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections.abc import Awaitable, Callable
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QObject, Signal
from curl_cffi import Response

from src.backend import clients
from src.backend.config import __version__
from src.backend.helper_functions import get_original_executable_path
from src.backend.shared_functions import configure_app_logging, get_os_and_arch

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
        # Check via installed Qt IFW maintenance tool first if present
        if tool_update := await CheckUpdates.check_via_maintenancetool():
            return tool_update

        # Fallback to HTTP update check endpoint
        return await CheckUpdates.check_via_http()

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
    ) -> None:
        super().__init__(parent)
        self.before_update = before_update

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
            [str(tool), "--updater"],
            cwd=str(tool.parent),
            creationflags=creationflags,
            start_new_session=(sys.platform != "win32"),
        )

        self.statusReport.emit("Updater launched. Closing Porn Fetch...")
        await asyncio.sleep(0.5)
        QCoreApplication.quit()
