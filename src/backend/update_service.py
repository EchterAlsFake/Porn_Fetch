import os
import sys
import ctypes

from config import __version__
from curl_cffi import Response
from PySide6.QtCore import Slot, QObject
from shared_functions import configure_app_logging


logger = configure_app_logging(logger_name="PornFetch - [Update]")


class SparkleUpdater(QObject):
    """
    This interacts with the shared library `sparkle_bridge.dylib`, see `sparkle_bridge.m` for source reference.
    During build, I will place the shared lib into the frameworks folder of the packaged nuitka app.

    Sparkle will periodically check for updates using my own server URL.
    More information here: https://sparkle-project.org/
    See also: https://echteralsfake.me/appcast.xml
    """

    def __init__(self, feed_url: str | None = None):
        super().__init__()
        logger.info("Trying to interact with Sparkle!")

        # In a macOS .app:
        # sys.executable -> .../MyApp.app/Contents/MacOS/MyApp
        macos_dir = os.path.dirname(os.path.realpath(sys.executable))
        logger.debug(f"macOS Directory: {macos_dir}")
        frameworks_dir = os.path.realpath(os.path.join(macos_dir, "..", "Frameworks"))
        logger.debug(f"Sparkle Framework: {frameworks_dir}")
        dylib_path = os.path.join(frameworks_dir, "sparkle_bridge.dylib")
        logger.debug(f"dylib bridge for talking to native code: {dylib_path}")

        self._lib = ctypes.CDLL(dylib_path)
        logger.info("Loaded dylib bridge, trying to talk to sparkle now...")
        # Define signatures
        self._lib.sparkle_start_updater.argtypes = [ctypes.c_char_p]
        self._lib.sparkle_start_updater.restype = None

        self._lib.sparkle_check_for_updates.argtypes = []
        self._lib.sparkle_check_for_updates.restype = None

        self._lib.sparkle_check_for_updates_in_background.argtypes = []
        self._lib.sparkle_check_for_updates_in_background.restype = None

        self._lib.sparkle_can_check_for_updates.argtypes = []
        self._lib.sparkle_can_check_for_updates.restype = ctypes.c_int
        logger.debug("Defined the necessary structures")

        # Start Sparkle once (use Info.plist SUFeedURL if feed_url is None)
        if feed_url:
            self._lib.sparkle_start_updater(feed_url.encode("utf-8"))
        else:
            self._lib.sparkle_start_updater(None)

    @Slot()
    def check_for_updates(self):
        # Must be called from Qt main thread (your UI thread)
        logger.info("Checking for Updates...")
        self._lib.sparkle_check_for_updates()

    @Slot()
    def check_for_updates_in_background(self):
        logger.info("Checking for Updates (background)....")
        self._lib.sparkle_check_for_updates_in_background()

    def can_check_for_updates(self) -> bool:
        return bool(self._lib.sparkle_can_check_for_updates())


class CheckUpdates:
    """
    This function checks for updates using my own server:
    https://echteralsfake.me/update
    (No data is transmitted while checking for updates, your IP is not logged.)
    See: https://echteralsfake.me/privacy_policy for more information
    """

    async def check(self):
        url = f"https://echteralsfake.me/update"
        try:
            response: Response = await clients.core.fetch(url=url, get_response=True)
            if response.status_code == 200:
                json_stuff = response.json()
                version = str(json_stuff["version"]).strip("latest - ")

                if float(version) > float(__version__):
                    self.logger.info(f"A new update is available -->: {version}")
                    self.signals.update_check.emit(True, json_stuff)

                else:
                    self.logger.info(f"Checked for updates... You are on the latest version :)")
                    self.signals.update_check.emit(False, json_stuff)

            elif response.status_code == 404:
                self.logger.error("Temporary error reaching the server")
                return

            elif response.status_code == 500:
                self.logger.error("Internal Server error, probably already fixing it :) ")
                return

            elif response.status_code == 530 or response.status_code == 502:
                self.logger.error("Server is currently offline. Probably already fixing it :)")

        except (ConnectionError, ConnectionResetError, ConnectionRefusedError, TimeoutError):
            handle_error_gracefully(self, data=video_data.consistent_data, error_message="I could NOT check for updates. The server is either not reachable, or you don't have an IPv6 connection.")




class AutoUpdateThread(QRunnable):
    def __init__(self) -> None:
        super(AutoUpdateThread, self).__init__()
        self.signals: Signals = Signals()
        self.assets: dict = {}
        self.logger = configure_app_logging(logger_name="Porn Fetch - [AutoUpdateThread]", log_file="PornFetch.log", level=logging.DEBUG)

    def run(self):
        self.signals.start_undefined_range.emit()
        self.logger.info("Fetching release information...")
        url = "https://echteralsfake.me/update"
        response: Response = clients.core.fetch(url=url, get_response=True)

        if response.status_code == 200:
            self.assets = response.json()
            self.logger.info(f"Got Update Information for: {self.assets["version"]}")

        elif response.status_code == 502 or response.status_code == 530 or response.status_code == 500:
            self.logger.error("Server is currently unable to return the update information. Please try again later...")
            ui_popup("Server is currently unable to return the update information. Please try again later...")
            return


        self.logger.info("Starting auto-update process...")
        os_arch = get_os_and_arch()
        download_url = self.assets.get(f"download_{os_arch}")

        if not download_url:
            self.logger.error(f"No download URL found for {os_arch}")
            self.signals.error_signal.emit(f"Update failed: No download available for your system ({os_arch}).")
            return

        self.logger.info(f"Downloading update from: {download_url}")

        temp_dir = tempfile.gettempdir()
        filename = download_url.split("/")[-1]
        download_path = os.path.join(temp_dir, filename)

        try:
            clients.core.legacy_download(
                url=download_url,
                path=download_path,
                callback=self.update_progress
            )
            self.logger.info("Download complete. Replacing binary.")
            self.replace_binary(download_path)
            self.logger.info("Update successful. Please restart the application.")
            self.signals.error_signal.emit("Update successful! Please restart the application.")
        except Exception as e:
            self.logger.error(f"Update failed: {e}")
            self.signals.error_signal.emit(f"Update failed: {e}")

    def update_progress(self, current: int, total: int) -> None:
        self.signals.total_progress.emit(current)
        self.signals.total_progress_range.emit(total)

    def replace_binary(self, new_binary_path: str) -> None:
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

    def create_windows_updater(self, current_path: str, new_path: str) -> None:
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

