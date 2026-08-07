import os
import sys
import ctypes
import shutil
import tempfile
import subprocess

from pathlib import Path
from backend.helper_functions import get_original_executable_path
from src.backend import clients as clients

from src.backend.config import __version__
from curl_cffi import Response
from PySide6.QtCore import Slot, QObject, QCoreApplication, Signal
from src.backend.shared_functions import configure_app_logging, handle_error_gracefully, get_os_and_arch


logger = configure_app_logging(logger_name="PornFetch - [Update]")


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
    async def check():
        url = f"https://echteralsfake.me/update"
        try:
            response: Response = await clients.core.fetch(url=url, get_response=True)
            if response.status_code == 200:
                json_stuff = response.json()
                version = str(json_stuff["version"]).strip("latest - ")

                if float(version) > float(__version__):
                    logger.info(f"A new update is available -->: {version}")

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

        except (ConnectionError, ConnectionResetError, ConnectionRefusedError, TimeoutError):
            raise CheckUpdates


class AutoUpdater:
    statusReport = Signal(str)
    updateProgress = Signal(int, int)

    def __init__(self) -> None:
        self.assets: dict = {}

    def run(self):
        logger.info("Fetching release information...")
        url = "https://echteralsfake.me/update"
        response: Response = clients.core.fetch(url=url, get_response=True)

        if response.status_code == 200:
            self.assets = response.json()
            logger.info(f"Got Update Information for: {self.assets["version"]}")

        elif response.status_code == 502 or response.status_code == 530 or response.status_code == 500:
            logger.error("Server is currently unable to return the update information. Please try again later...")
            self.statusReport.emit("Server is currently unable to return the update information. Please try again later...")
            return


        logger.info("Starting auto-update process...")
        os_arch = get_os_and_arch()
        download_url = self.assets.get(f"download_{os_arch}")

        if not download_url:
            logger.error(f"No download URL found for {os_arch}")
            self.statusReport.emit(f"Update failed: No download available for your system ({os_arch}).")
            return

        logger.info(f"Downloading update from: {download_url}")

        temp_dir = tempfile.gettempdir()
        filename = download_url.split("/")[-1]
        download_path = Path(temp_dir).joinpath(filename)

        try:
            clients.core.legacy_download(
                url=download_url,
                path=download_path,
                callback=self.update_progress
            )
            logger.info("Download complete. Replacing binary.")
            self.replace_binary(download_path)
            logger.info("Update successful. Please restart the application.")
            self.statusReport.error_signal.emit("Update successful! Please restart the application.")
        except Exception as e:
            logger.error(f"Update failed: {e}")
            self.statusReport.emit(f"Update failed: {e}")

    def update_progress(self, current: int, total: int) -> None:
        self.updateProgress.emit(current)
        self.updateProgress.emit(total)

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

