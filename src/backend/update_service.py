import os
import re
import sys
import asyncio
import ctypes
import shutil
import tempfile
import subprocess

from pathlib import Path
from base_api.modules.config import DownloadConfigRAW
from src.backend.helper_functions import get_original_executable_path
from src.backend import clients as clients

from src.backend.config import __version__
from curl_cffi import Response
from PySide6.QtCore import Slot, QObject, QCoreApplication, Signal
from src.backend.shared_functions import configure_app_logging, get_os_and_arch


logger = configure_app_logging(logger_name="PornFetch - [Update]")

DEFAULT_UPDATE_URL = "https://echteralsfake.me/update"
UPDATE_URL_ENVIRONMENT_VARIABLE = "PORNFETCH_UPDATE_URL"


def get_update_url() -> str:
    """Return the production endpoint unless a development override is set."""
    return os.environ.get(UPDATE_URL_ENVIRONMENT_VARIABLE, DEFAULT_UPDATE_URL)


class SparkleUpdater(QObject):
    def __init__(self):
        super().__init__()

        macos_dir = os.path.dirname(
            os.path.realpath(sys.executable)
        )

        frameworks_dir = os.path.realpath(
            os.path.join(macos_dir, "..", "Frameworks")
        )

        dylib_path = os.path.join(
            frameworks_dir,
            "sparkle_bridge.dylib",
        )

        logger.info("Loading Sparkle bridge: %s", dylib_path)

        self._lib = ctypes.CDLL(dylib_path)

        self._lib.sparkle_start_updater.argtypes = []
        self._lib.sparkle_start_updater.restype = None

        self._lib.sparkle_check_for_updates.argtypes = []
        self._lib.sparkle_check_for_updates.restype = None

        self._lib.sparkle_can_check_for_updates.argtypes = []
        self._lib.sparkle_can_check_for_updates.restype = ctypes.c_int

        self._lib.sparkle_start_updater()

    @Slot()
    def check_for_updates(self):
        logger.info("Checking for updates...")
        self._lib.sparkle_check_for_updates()

    def can_check_for_updates(self) -> bool:
        return bool(
            self._lib.sparkle_can_check_for_updates()
        )


class CheckUpdates:
    """
    This function checks for updates using my own server:
    https://echteralsfake.me/update
    (No data is transmitted while checking for updates, your IP is not logged.)
    See: https://echteralsfake.me/privacy_policy for more information
    """

    @staticmethod
    async def check() -> dict | None:
        url = get_update_url()
        try:
            response: Response = await clients.core.request(url=url)
            if response.status_code == 200:
                update = response.json()
                version = str(update["version"]).removeprefix("latest - ").strip()

                if CheckUpdates._version_parts(version) > CheckUpdates._version_parts(__version__):
                    logger.info(f"A new update is available -->: {version}")
                    return update

                else:
                    logger.info(f"Checked for updates... You are on the latest version :)")

            elif response.status_code == 404:
                logger.error("Temporary error reaching the server")
                return

            elif response.status_code == 500:
                logger.error("Internal Server error, probably already fixing it :) ")
                return

            elif response.status_code == 530 or response.status_code == 502:
                logger.error("Server is currently offline. Probably already fixing it :)")

        except (ConnectionError, ConnectionResetError, ConnectionRefusedError, TimeoutError) as error:
            logger.warning("Could not check for updates: %s", error)
        except (KeyError, TypeError, ValueError) as error:
            logger.error("The update server returned invalid data: %s", error)
        except Exception as error:
            # Update checks are deliberately silent: a temporary outage should
            # never prevent the application from starting.
            logger.warning("Could not check for updates: %s", error)

        return None

    @staticmethod
    def _version_parts(version: str) -> tuple[int, ...]:
        """Return numeric version components without relying on float parsing."""
        parts = [int(part) for part in re.findall(r"\d+", version)]
        while len(parts) > 1 and parts[-1] == 0:
            parts.pop()
        return tuple(parts) or (0,)


class AutoUpdater(QObject):
    statusReport = Signal(str)
    updateProgress = Signal(int, int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.assets: dict = {}

    async def run(self) -> None:
        try:
            await self._run()
        except asyncio.CancelledError:
            raise
        except Exception as error:
            logger.exception("Update failed")
            self.statusReport.emit(f"Update failed: {error}")

    async def _run(self) -> None:
        logger.info("Fetching release information...")
        url = get_update_url()
        self.statusReport.emit("Fetching release information...")
        response: Response = await clients.core.request(url=url)

        if response.status_code == 200:
            self.assets = response.json()
            logger.info(f"Got Update Information for: {self.assets["version"]}")

        else:
            logger.error("Update server returned HTTP %s", response.status_code)
            self.statusReport.emit(
                "Update failed: The server is currently unable to return update information. "
                "Please try again later."
            )
            return

        logger.info("Starting auto-update process...")
        os_arch = get_os_and_arch()
        download_url = self.assets.get(f"download_{os_arch}")

        if not download_url:
            logger.error(f"No download URL found for {os_arch}")
            self.statusReport.emit(f"Update failed: No download available for your system ({os_arch}).")
            return

        logger.info(f"Downloading update from: {download_url}")
        self.statusReport.emit("Downloading update...")

        temp_dir = tempfile.gettempdir()
        filename = download_url.split("/")[-1]
        download_path = Path(temp_dir).joinpath(filename)

        configuration = DownloadConfigRAW(
            quality="best",
            path=download_path,
            callback=self.update_progress,
        )
        await clients.core.legacy_download(
            url=download_url,
            configuration=configuration,
        )
        logger.info("Download complete. Replacing binary.")
        self.statusReport.emit("Download complete. Installing update...")
        self.replace_binary(download_path)
        logger.info("Update successful. Please restart the application.")
        self.statusReport.emit("Update successful! Please restart the application.")

    def update_progress(self, current: int, total: int) -> None:
        self.updateProgress.emit(current, total)

    def replace_binary(self, new_binary_path: Path) -> None:
        current_binary_path = get_original_executable_path()
        if not current_binary_path:
            raise RuntimeError("Could not determine the path of the current executable.")

        # On Windows, you can't replace a running executable.
        # A common strategy is to use a helper script.
        if sys.platform == "win32":
            self.create_windows_updater(current_binary_path, new_binary_path)
        else:
            # On Linux/macOS, you can often replace the binary directly.
            os.chmod(new_binary_path, 0o755)
            shutil.move(new_binary_path, current_binary_path)

    @staticmethod
    def create_windows_updater(current_path: Path, new_path: Path) -> None:
        updater_script_path = os.path.join(tempfile.gettempdir(), "updater.bat")
        with open(updater_script_path, "w") as f:
            f.write(f"""
@echo off
echo Waiting for application to close...
taskkill /F /IM {os.path.basename(current_path)}
timeout /t 2 /nobreak
echo Replacing application file...
move /Y "{new_path}" "{current_path}"
echo Starting new version...
start "" "{current_path}"
del "%~f0"
            """)
        subprocess.Popen([updater_script_path], creationflags=subprocess.CREATE_NO_WINDOW)
        QCoreApplication.quit()
