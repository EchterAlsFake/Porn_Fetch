"""
Copyright (C) 2023-2026 Johannes Habel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact:

E-Mail: EchterAlsFake@proton.me
Discord: echteralsfake (faster response)
"""
# macOS Setup...
import sys

if sys.platform == "darwin":
    from src.backend.macos_setup import macos_setup, SparkleUpdater
    macos_setup()


# General imports
import time
import os.path
import argparse
import markdown
import tempfile
import webbrowser
import subprocess
import src.frontend.UI.resources

from typing import Callable
from collections import deque
from threading import Event, Lock
from itertools import islice, chain


# Backend imports
from src.backend import clients # Singleton instance for the client objects (really important)
from src.backend.database import *
from src.backend.shared_gui import *
from src.backend.shared_functions import *
from src.backend.helper_functions import *
from src.backend.check_license import LicenseManager
import src.backend.shared_functions as shared_functions
from src.backend.config import __version__, PUBLIC_KEY_B64, shared_config, IS_SOURCE_RUN, TEMP_DIRECTORY, TEMP_DIRECTORY_STATES, TEMP_DIRECTORY_SEGMENTS

# Frontend imports
from src.frontend.UI.theme import *
from src.frontend.UI.ssl_warning import *
from src.frontend.UI.license import License, Disclaimer
from src.frontend.UI.ui_form_main_window import Ui_MainWindow
from src.frontend.UI.pornfetch_info_dialog import PornFetchInfoWidget
from src.frontend.UI.custom_combo_box import ComboPopupFitter, make_quality_combobox

# Qt / PySide6 related imports
from PySide6.QtGui import QIcon, QFontDatabase, QPixmap, QShortcut, QKeySequence
from PySide6.QtCore import (QTextStream, QRunnable, QThreadPool, QSemaphore, Qt, QLocale, QSize,
                            QTranslator, QCoreApplication, QStandardPaths, QSettings, Slot)
from PySide6.QtWidgets import (QApplication, QTreeWidgetItem, QButtonGroup, QFileDialog, QHeaderView, QComboBox, QLabel,
                               QInputDialog, QMainWindow, QProgressBar, QVBoxLayout, QSizePolicy, QLayout)

# Errors from different APIs
from phub import errors as ph_errors
from xnxx_api.modules.errors import InvalidResponse
from phub.errors import VideoError as VideoError_PH
from base_api.modules.errors import ProxySSLError, InvalidProxy
from xvideos_api.modules.errors import (VideoUnavailable as VideoUnavailable_XV)
from eporner_api.modules.errors import NotAvailable as NotAvailable_EP, VideoDisabled as VideoDisabled_EP
from youporn_api.modules.errors import VideoUnavailable as VideoUnavailable_YP, RegionBlocked as RegionBlocked_YP
from hqporner_api.modules.errors import InvalidActress as InvalidActress_HQ, NoVideosFound, NotAvailable as NotAvailable_HQ, WeirdError as WeirdError_HQ

# Other
from hqporner_api.api import Sort as hq_Sort
from eporner_api.modules.locals import Category as ep_Category

try:
    from av import open as av_open  # Don't ask
    from av.audio.resampler import AudioResampler  # Don't ask
    FORCE_DISABLE_AV = False

except Exception:
    FORCE_DISABLE_AV = True


FORCE_PORTABLE_RUN = False # Holds a value for argparse later (see main function)
total_segments = 0 # Total segments kept in a queue (for total progress tracking)
downloaded_segments = 0 # Amount of segments that have been downloaded (for total progress tracking)
total_downloaded_videos = 0  # All videos that actually successfully downloaded
session_urls = []  # This list saves all URls used in the current session. Used for the URL export function (CTRL + E)
conf = shared_config # Holds the configuration instance (converted to QSettings INI format)
stop_flag = Event() # Stops loading videos into the tree widget (does not stop any downloads)
_download_lock = Lock() # I actually don't really know why this is here
video_data = clients.VideoData() # Stores general video data as long as the data for each loaded video
settings: QSettings = QSettings() # Global instance of the settings used in Porn Fetch
logger = shared_functions.setup_logger("Porn Fetch - [MAIN]", log_file="PornFetch.log", level=logging.DEBUG)
license_storage_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation), "pornfetch.license")
x = False # Don't ask (this is a secret ;)


def _resolve_config_path(portable: bool, portable_dir: str | None = None) -> Path:
    """
    Portable  -> ./config.ini (portable_dir or CWD)
    Installed -> config.ini in AppConfigLocation (per-user standard location)
    """
    if portable:
        base = Path(portable_dir) if portable_dir else Path.cwd()
        return base / "config.ini"

    cfg_dir = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation))
    QDir().mkpath(str(cfg_dir))
    return cfg_dir / "config.ini"
    # We need this, because the configuration path is different whether used portably or if installed.


def make_settings(portable: bool, portable_dir: str | None = None) -> QSettings:
    """
    Returns QSettings bound to a real INI file (portable or installed).
    Also ensures the INI exists and contains merged defaults (no overwriting user values).

    This is needed, because the CLI can't use QSettings, but I want to use it in the GUI, so we keep both
    compatible.
    """
    ini_path = _resolve_config_path(portable, portable_dir)
    ensure_config_file(ini_path)

    return QSettings(str(ini_path), QSettings.Format.IniFormat)
    # This ensures the configuration fil exists, will get the current path and convert the ini format
    # Into an actual QSettings object that I can work with.
    # I wouldn't really need to use QSettings here, but if Qt provides a method, why not use it


class LicenseWidget(QWidget):
    """
    This is the License Widget which will let a user import the actual license and see if it's valid
    Still in experimental / beta mode, will be improved in v3.9 # TODO
    """
    def __init__(self, setup_restrictions: Callable, parent=None):
        super().__init__(parent)
        self.setup_restrictions = setup_restrictions # A function that basically creates the restrictions

        self.lic = LicenseManager(
            public_key_b64=PUBLIC_KEY_B64, # Public License to check the generated key
            storage_path=default_license_path(), # Storage path for the license
            expected_product="porn-fetch", # Yeah this is just an identifier, doesn't really matter
        )

        self.status = QLabel()
        self.btn_import = QPushButton("Import license…")
        self.btn_import.clicked.connect(self.import_license)

        layout = QVBoxLayout(self)
        layout.addWidget(self.status)
        layout.addWidget(self.btn_import)

        self.refresh_status()

    def refresh_status(self):
        res = self.lic.load_installed() # Checks if a license has already been installed before
        self.status.setText(f"License status: {'✅ Valid' if res.valid else '❌ Not valid'}\n{res.reason}")
        self.setup_restrictions() # Enforces the restrictions

    def import_license(self):
        # Opens a Dialog for importing the actual license
        path, _ = QFileDialog.getOpenFileName(self, "Select license file", "", "License (*.license);;All files (*)")
        if not path:
            return # User aborted (probably)
        res = self.lic.install_from_file(Path(path))
        QMessageBox.information(self, "License", res.reason)
        self.refresh_status()


class InstallThread(QRunnable):
    def __init__(self, app_name: str, app_id: str = "pornfetch", org_name: str = "EchterAlsFake",
                 portable_config_path: str | None = None):
        super().__init__()
        """
        This function installs Porn Fetch for Windows and Linux based systems.
        macOS has its own method and is not handled here.
        
        The installation works as simple as we take the install directory from a Qt provided default path, on 
        Linux typically somewhere in the user directory, and on Windows in the APPDATA directory.
        We will take the main executable of Porn Fetch + settings, write those into the new directory
        and write a desktop entry file / Shortcut with the executable path + Logo, 
        so that the user can run Porn Fetch from their start menu.
        """

        global settings
        settings = make_settings(portable=False) # At the first run, I assume the user goes for a portable install-type, however if the installation is called we need to switch that behaviour

        self.app_name = app_name # Custom app name, otherwise 'Porn Fetch'
        self.app_id = app_id  # used for desktop file name, etc.
        self.org_name = org_name # All handled in config.py
        self.portable_config_path = portable_config_path
        self.signals = Signals() # Signals for error / progress reporting

        # keep your logger setup if you want; using basic logging here
        self.logger = setup_logger(name="Porn Fetch - [InstallThread]", level=logging.DEBUG)

    def run(self):
        settings.setValue("Misc/app_name", self.app_name) # Sets app name, because we need that later in PF

        try:
            self.signals.start_undefined_range.emit() # Starts a loading animation until we have more information

            # These matter for QSettings() “installed” mode:
            QCoreApplication.setOrganizationName(self.org_name)
            QCoreApplication.setApplicationName(self.app_name)

            if sys.platform.startswith("linux"):
                self._install_linux_user() # Starts Linux install
            elif sys.platform == "win32":
                self._install_windows_user() # Starts Windows install
            else:
                raise RuntimeError(f"Unsupported platform: {sys.platform}") # lol

        except Exception: # Some error happened during installation
            error = traceback.format_exc()
            self.logger.error(error) # Log the error
            self.signals.install_finished.emit([False, error]) # Report the error (shows GUI message)
            self.signals.stop_undefined_range.emit() # Stop loading animation
            return

        self.signals.stop_undefined_range.emit() # Stop loading animation
        self.signals.install_finished.emit([True, ""]) # Successful install :)

    def _migrate_portable_settings(self, install_dir: str):
        """
        Copy current portable config.ini into the installed working directory
        so the installed run keeps user settings.
        """
        try:
            src = self.portable_config_path
            if not src:
                src = str(_resolve_config_path(portable=True, portable_dir=os.getcwd()))
            dst = str(_resolve_config_path(portable=True, portable_dir=install_dir))

            if src and os.path.exists(src):
                copy_overwrite_atomic(src, dst)
                self.logger.info(f"Migrated settings: {src} -> {dst}")
            else:
                self.logger.warning(f"No portable config found at {src}; creating defaults at {dst}")

            ensure_config_file(Path(dst))
            s = QSettings(dst, QSettings.Format.IniFormat)
            s.setValue("Misc/install_type", "installed")
            s.setValue("Misc/app_name", self.app_name)
            s.sync()
        except Exception as e:
            self.logger.warning(f"Settings migration failed: {e}")

    # ----------------------------
    # Linux (user-local install)
    # ----------------------------
    def _install_linux_user(self):
        filename = "PornFetch_Linux_GUI_x64.bin" # Typical filename, but needs to be improved # TODO

        # Install “payload” (binary + assets) into local app data:
        install_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)
        mkpath(install_dir)
        # We use the provided path by Qt as this is the most stable option for this

        apps_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ApplicationsLocation)
        if not apps_dir:
            # Rare, but some environments can return empty; keep a safe fallback.
            apps_dir = os.path.expanduser("~/.local/share/applications")
        mkpath(apps_dir)

        src_exe = get_original_executable_path() # Gets source executable path
        dst_exe = os.path.join(install_dir, filename) # Creates the final path for the destination executable
        try:
            copy_overwrite_atomic(src=src_exe, dst=dst_exe) # Copies the actual file

        except RuntimeError:
            self.signals.error_signal.emit(f"""
A Runtime error occurred during the installation process. This typically occurs, because I couldn't
find the real path of the extracted file from the main application.

In short: You can't fix that, please report this!""")

        chmod_755(dst_exe) # Grant execute permission (should be something like chmod +x I guess)
        icon_dst = os.path.join(install_dir, "logo.png") # Creates the destination for the logo
        if not QFile.exists(icon_dst):
            QFile.copy(":/images/graphics/logo.png", icon_dst) # We get the logo directly from the embedded resources
            # On Linux .png files are typically fine, on Windows this is handled differently

        self._migrate_portable_settings(install_dir)

        # Write desktop file atomically
        desktop_path = os.path.join(apps_dir, f"{self.app_id}.desktop")
        entry = f"""[Desktop Entry]
Version={__version__}
Type=Application
Name={self.app_name}
Exec="{dst_exe}" %F
Icon={icon_dst}
Path={install_dir}
Terminal=false
Categories=Utility;
StartupNotify=true
"""
        write_text_atomic(desktop_path, entry) # Creates the desktop entry for running PF from start menu

        # Store “installed” flag using Qt settings
        settings = make_settings(portable=False)
        settings.setValue("Misc/install_type", "installed")
        settings.sync()

        self.logger.info(f"Installed to {install_dir}, desktop entry {desktop_path}")

    # ----------------------------
    # Windows (user-local install)
    # ----------------------------
    def _install_windows_user(self):
        import win32com.client  # pywin32; Only available on Windows systems

        filename = "PornFetch_Windows_GUI_x64.exe" # Needs to be improved # TODO

        if os.path.exists("PornFetch_Windows_GUI_arm64.bin"):
            filename = "PornFetch_Windows_GUI_arm64.bin" # For ARM based CPUs

        # Every comment that hasn't been done here, see Linux install as it's the same
        install_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)
        mkpath(install_dir)

        src_exe = filename
        if not os.path.exists(src_exe):
            raise RuntimeError(f"Missing installer payload: {src_exe}")

        dst_exe = os.path.join(install_dir, filename)
        move_or_copy(src_exe, dst_exe)

        self._migrate_portable_settings(install_dir)

        # Settings flag
        settings = make_settings(portable=False)
        settings.setValue("Misc/install_type", "installed")
        settings.sync()

        # Start Menu Programs folder via Qt
        start_menu_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ApplicationsLocation)
        if not start_menu_dir:
            # Fallback (usually not needed)
            start_menu_dir = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs")
        mkpath(start_menu_dir)

        shortcut_path = os.path.join(start_menu_dir, f"{self.app_name}.lnk")

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = dst_exe
        shortcut.WorkingDirectory = install_dir
        shortcut.IconLocation = dst_exe
        shortcut.Save()

        self.logger.info(f"Installed to {install_dir}, shortcut {shortcut_path}")


class UninstallThread(QRunnable):
    """
    Uninstalls the *user-local installed* version:
      - Linux: removes ~/.local/share/applications/<app_id>.desktop
               removes AppLocalDataLocation payload folder (binary/icon)
      - Windows: removes Start Menu shortcut
                 removes AppLocalDataLocation payload folder
                 uses a .bat helper to delete after app exit (because Windows locks running exe)
    """

    def __init__(self, app_id: str = "pornfetch", org_name: str = "EchterAlsFake"):
        super().__init__()
        global settings
        settings = make_settings(portable=False)
        self.app_name = settings.value("Misc/app_name")

        self.app_id = app_id
        self.org_name = org_name
        self.signals = Signals()

        self.logger = logging.getLogger("UninstallThread")

    def run(self):
        try:
            self.signals.start_undefined_range.emit()

            # Match the settings identity of installed mode
            QCoreApplication.setOrganizationName(self.org_name)
            QCoreApplication.setApplicationName(self.app_name)
            # This is the reason why we need to save the app name in config, so that we later know
            # where it's actually installed

            if sys.platform.startswith("linux"):
                self._uninstall_linux_user() # Linux uninstall
            elif sys.platform == "win32":
                self._uninstall_windows_user() # Windows uninstall
            else:
                raise RuntimeError(f"Unsupported platform: {sys.platform}")

        except Exception:
            error = traceback.format_exc()
            self.logger.error(error)

            # You can reuse install_finished if you want, but it's nicer to add uninstall_finished
            if hasattr(self.signals, "uninstall_finished"):
                self.signals.uninstall_finished.emit([False, error])
            else:
                self.signals.install_finished.emit([False, error])

            self.signals.stop_undefined_range.emit()
            return

        self.signals.stop_undefined_range.emit()

        if hasattr(self.signals, "uninstall_finished"):
            self.signals.uninstall_finished.emit([True, ""])
        else:
            self.signals.install_finished.emit([True, ""])

    # ----------------------------
    # Linux (user-local uninstall)
    # ----------------------------
    def _uninstall_linux_user(self):
        install_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)
        # The directory where stuff is currently installed to

        apps_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ApplicationsLocation)
        if not apps_dir:
            apps_dir = os.path.expanduser("~/.local/share/applications")

        desktop_path = os.path.join(apps_dir, f"{self.app_id}.desktop")

        # Remove desktop entry
        safe_unlink(desktop_path)

        # Remove payload files (best effort)
        if install_dir and os.path.isdir(install_dir):
            safe_rmtree(install_dir) # Delete the entire directory

        # Clear settings keys / file
        self._clear_qt_settings()
        self.logger.info(f"Uninstalled (Linux). Removed: {desktop_path} and {install_dir}")

    # ----------------------------
    # Windows (user-local uninstall)
    # ----------------------------
    def _uninstall_windows_user(self):
        install_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)

        # Start Menu Programs folder via Qt
        start_menu_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ApplicationsLocation)
        if not start_menu_dir:
            start_menu_dir = os.path.join(os.getenv("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs")

        shortcut_path = os.path.join(start_menu_dir, f"{self.app_name}.lnk")

        # Remove shortcut now (usually possible even while app runs)
        safe_unlink(shortcut_path)

        # Clear settings first
        self._clear_qt_settings()

        # Now remove install_dir.
        # On Windows you typically cannot delete the running exe, so we spawn a helper bat
        # that waits for this process to exit, then deletes the folder.
        if install_dir and os.path.isdir(install_dir):
            self._spawn_windows_cleanup_bat(
                pid=os.getpid(),
                install_dir=install_dir,
                shortcut_path=shortcut_path,
            )

        self.logger.info(f"Uninstall scheduled (Windows). Shortcut removed: {shortcut_path}, install_dir: {install_dir}")

    def _clear_qt_settings(self):
        """
        Clear the app's Qt settings.
        Works for INI-based settings and registry-based ones.
        """
        try:
            s = make_settings(portable=False)
            s.clear()
            s.sync()

            # If this is an ini file, you can also delete it for a "clean uninstall"
            fname = ""
            try:
                fname = s.fileName()
            except Exception:
                fname = "config.ini" # What could go wrong?

            if fname and os.path.exists(fname):
                safe_unlink(fname)

        except Exception as e:
            # Don't fail uninstall if settings cleanup fails
            self.logger.warning(f"Settings cleanup failed: {e}")

    def _spawn_windows_cleanup_bat(self, pid: int, install_dir: str, shortcut_path: str):
        """
        Creates and runs a .bat that waits until PID exits, then deletes install_dir.
        The .bat deletes itself at the end.
        """
        bat_path = os.path.join(tempfile.gettempdir(), f"{self.app_id}_uninstall_cleanup.bat")

        # Use rmdir /s /q for full folder wipe
        # Hopefully this doesn't delete your PC LMAO
        # "tasklist /FI" loop waits until PID is gone
        script = rf"""@echo off
setlocal ENABLEDELAYEDEXPANSION

REM Wait for the app process to exit
:loop
tasklist /FI "PID eq {pid}" 2>NUL | find /I "{pid}" >NUL
if "%ERRORLEVEL%"=="0" (
    timeout /t 1 /nobreak >NUL
    goto loop
)

REM Remove shortcut (best effort)
del /f /q "{shortcut_path}" >NUL 2>&1

REM Remove install folder
rmdir /s /q "{install_dir}" >NUL 2>&1

REM Self-delete
del /f /q "%~f0" >NUL 2>&1
endlocal
"""

        with open(bat_path, "w", encoding="utf-8") as f:
            f.write(script)

        # Launch hidden
        creationflags = 0
        try:
            creationflags = subprocess.CREATE_NO_WINDOW
        except Exception:
            creationflags = 0

        subprocess.Popen(
            ["cmd.exe", "/c", bat_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags,
            close_fds=True,
        )


class AutoUpdatingThread(QRunnable):
    def __init__(self, asset_path):
        super(AutoUpdatingThread, self).__init__()
        self.asset_path = asset_path
        self.signals = Signals()

    def run(self):
        ""



class CheckUpdates(QRunnable):
    def __init__(self):
        super(CheckUpdates, self).__init__()
        self.signals = Signals()
        self.logger = shared_functions.setup_logger(name="Porn Fetch - [CheckUpdates]", log_file="PornFetch.log", level=logging.DEBUG,)

    def run(self):
        url = f"https://echteralsfake.me/update"
        try:
            response = clients.core.fetch(url=url, get_response=True)
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

        except (ConnectionError, ConnectionResetError, ConnectionRefusedError, TimeoutError):
            handle_error_gracefully(self, data=video_data.consistent_data, error_message="I could NOT check for updates. The server is either not reachable, or you don't have an IPv6 connection.")


class AddToTreeWidget(QRunnable):
    def __init__(self, iterator, is_checked, last_index):
        super(AddToTreeWidget, self).__init__()
        self.signals = Signals()  # Processing signals for progress and information
        self.iterator = iterator  # The video iterator (Search or model object yk)
        self.stop_flag = stop_flag  # If the user pressed the stop process button
        self.is_checked = is_checked  # If the "do not clear videos" checkbox is checked
        self.last_index = last_index  # The last index (video) of the tree widget to maintain a correct order of numbers
        self.consistent_data = video_data.consistent_data
        self.output_path = self.consistent_data.get("output_path")
        self.result_limit = self.consistent_data.get("result_limit")
        self.supress_errors = self.consistent_data.get("supress_errors")
        self.activate_logging = self.consistent_data.get("activate_logging")
        self.logger = shared_functions.setup_logger(name="Porn Fetch - [AddToTreeWidget]", log_file="PornFetch.log", level=logging.DEBUG)

    def process_video(self, video, index):
        if isinstance(video, str):
            report = video

        else:
            try:
                report = video.url

            except: # Don't ask
                report = "If you can read this, then you know I fucked up badly. Please call ChatGPT and ask it to fix this code"

        if not isinstance(video, str):
            self.logger.debug(f"Requesting video processing of: {video.url}")

        else:
            self.logger.debug(f"Requesting video processing of: {video}")

        for attempt in range(0, 5):
            try:
                video_identifier = random.randint(0, 99999999) # Creates a random ID for each video
                if isinstance(video, str):
                    video = clients.check_video(url=video)

                self.logger.info(f"[Download (3/10) - Video ID] -->: {video_identifier}")
                data = clients.load_video_attributes(video)
                self.logger.debug("[Download (4/10) - Fetched Attributes")
                session_urls.append(video.url)
                title = data.get("title")
                video_id = data.get("video_id")
                stripped_title_1 = clients.core.strip_title(title) # Clears special characters
                stripped_title_2 = clients.core.strip_title(title)

                if self.consistent_data.get("video_id_as_filename"):
                    stripped_title_1 = video_id # Only PornHub / EPorner / MissAV

                if self.consistent_data.get(
                        "directory_system"):  # If the directory system is enabled, this will create an additional folder
                    author_path = os.path.join(self.output_path, data.get("author"))
                    os.makedirs(author_path, exist_ok=True)
                    output_path = os.path.join(str(author_path), stripped_title_1 + ".mp4")

                else:
                    output_path = os.path.join(self.output_path, stripped_title_1 + ".mp4")

                # Emit the loaded signal with all the required information
                data.update(
                    {
                        "title": stripped_title_2,
                        "output_path": output_path,
                        "index": index,
                        "video": video
                    })

                video_data.data_objects.update({video_identifier: data})
                self.logger.info(f"[Download (5/10) - Finished Processing]")
                return video_identifier

            except (ph_errors.PremiumVideo, IndexError):
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"Premium-only video skipped: {report}")
                return False

            except ph_errors.RegionBlocked:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"Region-blocked video skipped: {report}")
                return False

            except ph_errors.VideoDisabled:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"Warning: The video {report} is disabled. It will be skipped")

            except ph_errors.RegexError:
                message = f"""
                A regex error occurred. This is always a 50/50 chance if it's my or PornHub's fault. If this happens again on
                the same video, please consider reporting it. If you have logging enabled, this issue will automatically be reported.
                
                Current Index: {index}
                Additional Info: URL: {report}
                """
                self.logger.error("Regex error occurred, sleeping one second...")
                time.sleep(1)

                if attempt == 4:
                    self.logger.info("Nevermind, didn't work lmao")
                    handle_error_gracefully(self, data=video_data.consistent_data, error_message=message, needs_network_log=True)
                    return False

            except ph_errors.VideoPendingReview:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"Warning: The video {report} is pending review. It will be skipped")
                return False

            except InvalidResponse:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"Warning: The video: {report} returned an empty response when trying"
                                             f"to fetch its content. There is nothing I can do. It will be skipped")
                return False

            except NotAvailable_HQ:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"The video: {report} is not available, because the CDN network has an issue. "
                                              f"This is not my fault, please do NOT report this error, thank you :)")
                return False


            except WeirdError_HQ:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"An error happened with: {report} this is a weird error i have no fix for yet,"
                                              f" however this will be reported, to help me fixing it :) ", needs_network_log=True)
                return False

            except VideoUnavailable_XV:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message= f"The video {report} is not available. Do not report this error... Not my fault :)")
                return False

            except NotAvailable_EP:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"The video: {report} is not available on HQPorner. This is not my fault, skipping...")
                return False

            except VideoDisabled_EP:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"The video: {report} has been disabled by EPorner itself. It will be skippled...")
                return False

            except VideoError_PH:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"The video: {report} has an error. However, in this case it's PornHub's fault. It will be skipped!")
                return False

            except RegionBlocked_YP:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"The video: {report} is region locked. It will be skipped...")

            except VideoUnavailable_YP:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"The video: {report} is unavailable on YouPorn. It will be skipped...")

            except ProxySSLError:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"SSL Error, are you are you using  a public network?")

            except Exception:
                error = traceback.format_exc()
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"Unexpected error occurred: {error}", needs_network_log=True)
                return False

        return None

    def run(self):
        self.signals.start_undefined_range.emit()  # Starts the progressbar, but with a loading animation
        is_first = True # see down below for an explanation

        if isinstance(self.iterator, str):
            self.iterator = [self.iterator]

        if not self.is_checked:
            self.signals.clear_tree_widget_signal.emit()  # Clears the tree widget

        if self.is_checked:
            start = self.last_index
            self.result_limit += start

        else:
            start = 1
            self.logger.debug(f"Result Limit: {str(self.result_limit)}")

        videos = islice(self.iterator, self.result_limit)

        for i, video in enumerate(videos, start=start):
            if self.stop_flag.is_set():
                self.signals.tree_widget_finished.emit()
                return  # Stop processing if user pressed the stop button

            if i >= self.result_limit + 1:
                break  # Respect search limit

            video_id = self.process_video(video, i)  # Passes video and index object / int

            if video_id is False:
                self.logger.warning(f"Skipping Video: {video}")
                continue

            if is_first:
                self.signals.total_progress_range.emit(self.result_limit)
                is_first = False # Otherwise the total would be sent every time which creates overhead
                
            self.signals.total_progress.emit(i)
            self.signals.text_data_to_tree_widget.emit(video_id)

        self.logger.debug("Finished Iterating")
        self.signals.tree_widget_finished.emit()


class DownloadScheduler(QObject):
    worker_started = Signal(int, object)  # video_id, worker

    def __init__(self, threadpool, max_concurrent: int, parent=None):
        super().__init__(parent)
        self.pool = threadpool # Threadpool from the GUI (QThreadPool)
        self.sem = QSemaphore(max_concurrent) # Creates a semaphore that limits the maximum number of concurrent downloads
        self.queue = deque() # This is a queue, that keeps track of all vidos that are currently being downloaded

    def enqueue(self, video_obj, video_id: int, quality, stop_event, segment_dir: str, segment_state_path: str):
        self.queue.append((video_obj, video_id, quality, stop_event, segment_dir, segment_state_path)) # Appends a video to the queue
        # Video OBJ ->: This is the actual video object
        # Video ID -->: Unique ID of the video generated by AddToTreWidget class, so that we can access its data
        # Quality -->: The selected download quality from the quality box
        # Stop Event -->: This is associated with the stop button. If pressed the event
        # will raise an internal exception in the download process of eaf_base_api which gracefully stops the download
        # and all network requests
        self._try_start()

    def _try_start(self):
        while self.queue and self.sem.tryAcquire(1): # Tries to start the download
            video_obj, video_id, quality, stop_event, segment_dir, segment_state_path = self.queue.popleft()
            # Deletes the video from the queue, gets the data and then starts the download
            worker = DownloadThread(video=video_obj, video_id=video_id, quality=quality, stop_event=stop_event, segment_dir=segment_dir, segment_state_path=segment_state_path)
            # Creates the actual download object
            worker.signals.download_completed.connect(self._on_done)
            # Connects the completed signal to the UI
            self.worker_started.emit(video_id, worker) # Does something idk???
            self.pool.start(worker) # Starts the actual download
            logger.info(f"[Download (9/10) - Started Download]")

    @Slot(int)
    def _on_done(self, video_id: int):
        self.sem.release(1)
        self._try_start()
        # Releases the semaphore, so that the next video can be downloaded


class DownloadThread(QRunnable):
    """Refactored threading class to download videos with improved performance and logic."""
    def __init__(self, video, video_id, quality, stop_event, segment_state_path, segment_dir):
        super().__init__()
        self.video: clients.AllowedVideoType = video
        self.video_id = video_id
        self.consistent_data = video_data.consistent_data
        self.quality = quality
        self.segment_state_path = segment_state_path
        self.segment_dir = segment_dir
        self.stop_event = stop_event
        data_object: dict = video_data.data_objects[self.video_id]
        self.output_path = data_object.get("output_path")
        self.logger = shared_functions.setup_logger(name="Porn Fetch - [DownloadThread]", log_file="PornFetch.log", level=logging.DEBUG)
        self.signals = Signals()
        self.stop_flag = stop_event
        self.skip_existing_files = self.consistent_data.get("skip_existing_files")
        self.video_progress = {}
        self.last_update_time = 0
        self._range_emitted = False

    def callback_remux(self, pos, total):
        self.signals.progress_remux.emit(self.video_id, pos, total)

    def generic_callback(self, pos, total,  video_source="general"):
        """Generic callback function to emit progress signals with rate limiting."""
        current_time = time.time()
        if self.stop_flag.is_set():
            return
        # Emit signal for individual progress
        if video_source == "raw":

            # Check if the current time is at least 0.5 seconds greater than the last update time
            if current_time - self.last_update_time < 0.5:
                # If not, do not update the progress and return immediately
                return

            scaling_factor = 1024 * 1024
            pos = int(pos / scaling_factor)
            total = int(total / scaling_factor)

        if not self._range_emitted:
            # tell UI: "for video_id, this is the maximum"
            self.signals.progress_video_range.emit(self.video_id, total)
            self._range_emitted = True

        self.signals.progress_video.emit(self.video_id, pos, total) # Although we don't use total, we need to accept it
        # Update total progress only if the video source uses segments
        if video_source == "general":
            self.update_total_progress()

        # Update the last update time to the current time
        self.last_update_time = current_time

    def update_total_progress(self):
        """Update total download progress."""
        global downloaded_segments
        with _download_lock:
            downloaded_segments += 1
            self.signals.total_progress.emit(downloaded_segments)

    def _add_total_segments(self):
        """Fetch segment count off the UI thread and update total progress range."""
        global total_segments
        if self.stop_flag.is_set() or self.stop_event.is_set():
            return
        if not hasattr(self.video, "get_segments"):
            return
        try:
            segments = self.video.get_segments(quality=self.quality)
        except Exception:
            self.logger.debug("Failed to get segments for total progress", exc_info=True)
            return

        try:
            count = len(segments)
        except TypeError:
            count = sum(1 for _ in segments)

        if count <= 0:
            return

        with _download_lock:
            total_segments += count
            current_total = total_segments
        self.signals.total_progress_range.emit(current_total)

    def run(self):
        """Run the download in a thread, optimizing for different video sources and modes."""
        report = None  # Needed for HLS downloads

        # We need to specify the sources, so that it knows which individual progressbar to use
        instances_legacy = [clients.hq_Video, clients.ep_Video, clients.pt_Video,
                            clients.xf_Video]

        try:
            do_not_skip = False
            if os.path.isfile(self.output_path) and isinstance(self.video, tuple(instances_legacy)):
                self.logger.info("File already exists, checking integrity...")
                clients.core.session.headers.update({"Accept-Encoding": "identity"}) # Chad told me to do this idk
                direct_download_url = clients.get_direct_url_legacy(video=self.video, quality=self.quality)
                response = clients.core.fetch(method="HEAD", url=direct_download_url, get_response=True)
                size = int(response.headers.get("Content-Length"))
                do_not_skip = True
                size_of_file = os.path.getsize(self.output_path)
                if size != size_of_file:
                    self.logger.info("File seems to be incomplete, appending the rest of bytes, please wait...")

                else:
                    self.logger.info("Checked Integrity -->: 100% :)")
                    return

                if self.skip_existing_files and not do_not_skip:
                    self.logger.debug("The file already exists, skipping...")
                    self.signals.download_completed.emit(True)
                    return

                else:
                    if not do_not_skip:
                        self.logger.debug("The file already exists, appending random number...")
                        path = str(self.output_path).split(".")
                        path = path[0] + str(random.randint(0, 1000)) + ".mp4"
                        self.output_path = path

            self._add_total_segments()
            if int(self.consistent_data.get("processing_delay")) != 0:
                time.sleep(int(self.consistent_data.get("processing_delay")))
            self.logger.debug(f"Downloading Video to: {self.output_path}")
            global FORCE_DISABLE_AV
            if not FORCE_DISABLE_AV:
                remux = True

            else:
                remux = False

            if isinstance(self.video, tuple(instances_legacy)):
                video_source = "raw"
                try:
                    self.logger.debug("Starting the Download!")
                    self.video.download(quality=self.quality, path=self.output_path, no_title=True,
                                    callback=lambda pos, total: self.generic_callback(pos, total, video_source), stop_event=self.stop_event)

                except Exception:
                    error = traceback.format_exc()
                    handle_error_gracefully(data=self.consistent_data, self=self, error_message=f"An error happened while downloading a video from HQPorner / EPorner: {error}", needs_network_log=True)

            else:
                report = self.video.download(path=self.output_path, callback_remux=self.callback_remux, no_title=True,
                                    quality=self.quality, remux=remux, stop_event=self.stop_event,
                                    callback=lambda pos, total: self.generic_callback(pos, total),
                                             return_report=True, segment_state_path=self.segment_state_path,
                                             keep_segment_dir=True, cleanup_on_stop=True, segment_dir=self.segment_dir
                                             )
                print(f"Got Report from downloading: {report}")

        except Exception:
            error = traceback.format_exc()
            error = f"An error occurred when trying to download video: {error}. This will be reported!"
            handle_error_gracefully(self, data=video_data.consistent_data, error_message=error, needs_network_log=True)

        finally:
            self.logger.info(f"[Download (10/10) - Download Completed!]")
            if self.consistent_data.get("write_metadata") and not self.stop_flag.is_set():
                try:
                    if not FORCE_DISABLE_AV:
                        clients.write_tags(path=self.output_path, data=video_data.data_objects.get(self.video_id))

                except Exception:
                    error = traceback.format_exc()
                    error = f"An error occurred when trying to write metadata: {error}. This will be reported!"
                    handle_error_gracefully(self, data=video_data.consistent_data, error_message=error, needs_network_log=True)

            self.signals.download_completed.emit(self.video_id, report)


class PornFetch(QMainWindow):
    COL_DOWNLOAD = 0
    COL_TITLE = 1
    COL_AUTHOR = 2
    COL_LENGTH = 3
    COL_QUALITY = 4
    COL_STOP = 5
    COL_PROGRESS = 6

    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_update_time = time.time()
        self.last_thumbnail_change = time.time()
        self.signals = Signals()
        self.signals.error_signal.connect(ui_popup)

        global settings
        settings = make_settings(portable=True, portable_dir=os.getcwd())

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.logger = shared_functions.setup_logger(name="Porn Fetch - [PornFetch]", log_file="PornFetch.log", level=logging.DEBUG)

        self.last_index = 0  # Keeps track of the last index of videos added to the tree widget
        self.kill_switch = False
        self.ensure_temp()
        self._row = {} # Video ID -> dict of widgets + state
        self.threadpool = QThreadPool()
        self.maps()
        self.load_style()
        self.license = License(self.ui, self.initialize_pornfetch)
        self.disclaimer = Disclaimer(self.ui, self.initialize_pornfetch)
        self.ui.vbox_info.addWidget(PornFetchInfoWidget())
        self.license_manager = LicenseManager(storage_path=default_license_path(), public_key_b64=PUBLIC_KEY_B64)
        self.setup_license_restrictions()

        """
                             ! INDEX LIST !

        0) Main application (downloading, login, tree widget etc.)
        :: Index list for main application ::
        - 0: Download
        - 1: Login
        - 2: Tools
        - 3: Progressbars
        - 4: Range selector
        
        1) Settings
        2) Credits
        3) License
        4) Keyboard Shortcuts
        5) Install Dialog
        6) Supported websites
        7) Donation Nag        
        8) Disclaimer text
        9) One-Time Information
        10) Batch Feature (Not implemented yet)
        This may look a little bit confusing, but once you understand it, it makes sense, trust me :)
        """

        self.default_max_height = self.ui.main_stacked_widget_top.maximumHeight()
        self.button_connections()  # Connects the buttons to their functions
        self.shortcuts()  # Activates the keyboard shortcuts
        self.logger.debug("Startup: [3/5] Initialized the User Interface")
        self.load_user_settings()  # Loads the user settings and applies selected values to the UI
        self.logger.debug("Startup: [4/5] Loaded the user settings")
        max_concurrent = int(video_data.consistent_data.get("semaphore", 1))
        self.download_scheduler = DownloadScheduler(self.threadpool, max_concurrent, self)
        self.download_scheduler.worker_started.connect(self._wire_worker_signals)
        self.progress_widgets = {}  # video_id -> {'label': QLabel, 'progressbar': QProgressBar}

        if video_data.consistent_data.get("update_checks"):
            self.logger.info("Running update checks")
            self.check_for_updates()

        if video_data.consistent_data.get("anonymous_mode"):
            self.logger.info("Enabling anonymous mode")
            self.anonymous_mode()

        self.semaphore = QSemaphore(video_data.consistent_data["semaphore"])
        self.logger.debug("Startup: [5/5] OK")
        self.initialize_pornfetch()


    """
    The following functions just switch the Stacked Widget to the different widgets
    """

    """Stacked Widget Main:"""

    def switch_to_main(self):
        self.ui.CentralStackedWidget.setCurrentIndex(0)

    def switch_to_settings(self):
        self.ui.CentralStackedWidget.setCurrentIndex(1)

    def switch_to_credits(self):
        self.show_credits()
        self.ui.CentralStackedWidget.setCurrentIndex(2)

    def switch_to_license(self):
        self.ui.CentralStackedWidget.setCurrentIndex(3)

    def switch_to_keyboard_shortcuts(self):
        self.ui.CentralStackedWidget.setCurrentIndex(4)

    def switch_to_install_dialog(self):
        self.ui.CentralStackedWidget.setCurrentIndex(5)

    def switch_to_supported_sites(self):
        self.ui.CentralStackedWidget.setCurrentIndex(6)

    def switch_to_disclaimer(self):
        self.ui.CentralStackedWidget.setCurrentIndex(7)

    def switch_to_one_time_setup(self):
        self.ui.CentralStackedWidget.setCurrentIndex(8)

    def switch_to_update_available(self):
        self.ui.CentralStackedWidget.setCurrentIndex(9)

    """Stacked Widget Top:"""

    def switch_to_download(self):
        self.ui.main_stacked_widget_top.setCurrentIndex(0)
        self.switch_to_main()

    def switch_to_login(self):
        self.ui.main_stacked_widget_top.setCurrentIndex(1)
        self.switch_to_main()

    def switch_to_tools(self):
        self.ui.main_stacked_widget_top.setCurrentIndex(2)
        self.switch_to_main()

    # Stacked Widget Tree
    def switch_to_treewidget_downloads(self):
        self.ui.stacked_widget_tree.setCurrentIndex(0)
        self.switch_to_main()

    def switch_to_treewidget_advanced_configuration(self):
        self.ui.stacked_widget_tree.setCurrentIndex(1)
        self.switch_to_main()

    def load_style(self):
        icons = {
            self.ui.main_button_switch_home: "download.svg",
            self.ui.main_button_switch_settings: "settings.svg",
            self.ui.main_button_switch_credits: "information.svg",
            self.ui.main_button_switch_account: "account.svg",
            self.ui.main_button_switch_tools: "tools.svg",
        }
        self.setWindowIcon(QIcon(":/images/graphics/logo_transparent.ico"))

        for btn, name in icons.items():
            btn.setIcon(QIcon(f":/images/graphics/{name}"))
            btn.setIconSize(QSize(24, 24))  # consistent size for all

        pixmap_tooltip = QPixmap(":/images/graphics/tooltip.svg")
        mark_help_buttons(ui=self.ui, pixmap=pixmap_tooltip)

        # --- top nav becomes segmented & exclusive ---
        nav = [
            self.ui.main_button_switch_home,
            self.ui.main_button_switch_account,
            self.ui.main_button_switch_tools,
            self.ui.main_button_switch_settings,
            self.ui.main_button_switch_credits,
        ]
        group_menu_bar = QButtonGroup(self)
        group_menu_bar.setExclusive(True)
        for b in nav:
            b.setCheckable(True)
            group_menu_bar.addButton(b)
            mark(b, seg=True)  # <- gives the segmented style
        self.ui.main_button_switch_home.setChecked(True)

        tree_nav = [
            self.ui.button_treewidget_downloads,
            self.ui.button_treewidget_advanced_configuration,
        ]

        group_tree_nav = QButtonGroup(self)
        group_tree_nav.setExclusive(True)
        for b in tree_nav:
            b.setCheckable(True)
            group_tree_nav.addButton(b)
            mark(b, seg=True)
        self.ui.button_treewidget_downloads.setChecked(True)


        settings_nav = [
            self.ui.settings_button_switch_video,
            self.ui.settings_button_switch_performance,
            self.ui.settings_button_switch_system,
            self.ui.settings_button_switch_ui
        ]
        group_settings_bar = QButtonGroup(self)
        group_settings_bar.setExclusive(True)
        for b in settings_nav:
            b.setCheckable(True)
            group_settings_bar.addButton(b)
            mark(b, seg=True)
        self.ui.settings_button_switch_video.setChecked(True)

        # --- intent & size instead of dozens of QSS files ---
        mark(self.ui.download_button_download, intent="primary", size="lg")
        mark(self.ui.login_button_login, intent="primary")
        mark(self.ui.settings_button_apply, intent="primary")

        mark(self.ui.main_button_tree_stop, intent="danger")
        mark(self.ui.settings_button_reset, intent="danger")

        mark(self.ui.main_progressbar_total, role="total")

        mark(self.ui.button_info_enable_all, intent="success")
        mark(self.ui.button_info_disable_all, intent="danger")
        mark(self.ui.button_info_enable_update, intent="primary")


        # most of these are secondary or flat so they don’t compete visually
        for b in [
            self.ui.main_button_switch_supported_websites,
            self.ui.main_button_tree_keyboard_shortcuts,
            self.ui.button_update_acknowledged,
        ]:
            mark(b, flat=True)

        # things that start/queue work but aren’t “the” CTA: make them secondary
        for b in [
            self.ui.download_button_playlist_get_videos,
            self.ui.download_button_model,
            self.ui.button_search,
            self.ui.tools_button_get_random_videos,
            self.ui.tools_button_get_brazzers_videos,
            self.ui.tools_button_list_categories,
            self.ui.tools_button_list_categories_eporner,
            self.ui.tools_button_eporner_category_get_videos,
            self.ui.tools_button_hqporner_category_get_videos,
            self.ui.settings_button_system_install_pornfetch,
        ]:
            mark(b)  # no intent ⇒ secondary

        for cb in self.findChildren(QComboBox):
            pretty_combo(cb)

        # --- progress bars: mark roles instead of separate QSS files ---
        mark(self.ui.main_progressbar_total, role="total")

        # --- tree header sizing / behavior ---

        self.ui.treeWidget.setColumnCount(7)
        self.ui.treeWidget.setHeaderLabels([
            "Download", "Title", "Author", "Length", "Quality", "Stop", "Progress"
        ])
        self.ui.treeWidget.setRootIsDecorated(False)  # looks more like a table
        self.ui.treeWidget.setAlternatingRowColors(True)
        self.ui.treeWidget.setSelectionBehavior(self.ui.treeWidget.SelectionBehavior.SelectRows)

        # Make it look reasonable
        self.ui.treeWidget.setColumnWidth(self.COL_DOWNLOAD, 110)
        self.ui.treeWidget.setColumnWidth(self.COL_TITLE, 120)
        self.ui.treeWidget.setColumnWidth(self.COL_AUTHOR, 180)
        self.ui.treeWidget.setColumnWidth(self.COL_LENGTH, 120)
        self.ui.treeWidget.setColumnWidth(self.COL_QUALITY, 120)
        self.ui.treeWidget.setColumnWidth(self.COL_PROGRESS, 220)
        self.ui.treeWidget.header().setSectionResizeMode(self.COL_DOWNLOAD, QHeaderView.ResizeMode.ResizeToContents)
        self.ui.treeWidget.header().setSectionResizeMode(self.COL_QUALITY, QHeaderView.ResizeMode.ResizeToContents)
        self.ui.treeWidget.header().setSectionResizeMode(self.COL_STOP, QHeaderView.ResizeMode.ResizeToContents)
        self.ui.treeWidget.header().setSectionResizeMode(self.COL_LENGTH, QHeaderView.ResizeMode.ResizeToContents)

        # Let the title take the free space
        self.ui.treeWidget.header().setSectionResizeMode(self.COL_TITLE, QHeaderView.ResizeMode.Stretch)

        # Progress is last: let it stretch too (it will consume remaining space)
        self.ui.treeWidget.header().setStretchLastSection(True)

        # --- misc you already had ---
        self.ui.treeWidget.sortByColumn(2, Qt.SortOrder.AscendingOrder)
        self.setWindowTitle(f"Porn Fetch v{__version__} Copyright (C) Johannes Habel 2023-2026")
        self.ui.treeWidget.sortByColumn(2, Qt.SortOrder.AscendingOrder)
        self.ui.settings_stacked_widget_main.setCurrentIndex(0)

        install_focus_outline(self)
        self.filter = ComboPopupFitter()
        self.ui.download_website_combobox.installEventFilter(self.filter)
        self.ui.settings_combobox_ui_theme.installEventFilter(self.filter)
        self.ui.settings_ui_combobox_language.installEventFilter(self.filter)
        self.ui.settings_video_combobox_quality.installEventFilter(self.filter)
        self.ui.tools_combobox_hqporner_top_porn.installEventFilter(self.filter)
        self.ui.settings_video_combobox_model_videos.installEventFilter(self.filter)


        stylesheet_license_buttons = QFile(":/style/UI/stylesheet_license_button.qss")
        stylesheet_license_buttons.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text)
        stream = QTextStream(stylesheet_license_buttons)
        style = stream.readAll()

        self.ui.settings_button_buy_license.setProperty("variant", "primary")
        self.ui.settings_button_buy_license.setStyleSheet(style)

        self.ui.settings_button_import_license.setProperty("variant", "danger")
        self.ui.settings_button_import_license.setStyleSheet(style)

        self.switch_to_download()
        self.switch_to_treewidget_downloads()

    def anonymous_mode(self):
        """
        This mode will hide that you are using Porn Fetch by hiding video title names, hiding author names,
        hiding the window title and removing all placeholders from lineedits. May not be the most efficient approach,
         but it works.
        """
        self.setWindowTitle("Running in Anonymous mode...")
        self.ui.download_lineedit_url.setPlaceholderText(" ")
        self.ui.login_lineedit_password.setPlaceholderText(" ")
        self.ui.login_lineedit_username.setPlaceholderText(" ")
        self.ui.settings_label_performance_network_delay.setText("Delay (0 = Disabled) in seconds:")
        self.ui.settings_label_videos_model_vdeos_type.setText("Actors video types:")
        self.ui.settings_button_system_install_pornfetch.setText("Install Program")
        self.ui.tools_label_get_top_porn.setText("Get 'Top' videos")
        self.ui.tools_button_get_brazzers_videos.setText("Get BRZ videos")
        self.ui.main_textbrowser_supported_websites.setText(
            "Running in anonymous mode, please deactivate to display...")
        self.ui.groupbox_tools_hqporner.setTitle("HQ")
        self.ui.groupbox_tools_eporner.setTitle("EP")
        self.ui.download_lineedit_playlist_url.setPlaceholderText("Enter playlist URL")
        self.ui.settings_button_reset.setText("Reset PF")
        self.ui.settings_button_uninstall_porn_fetch.setText("Uninstall PF")
        self._anonymous_mode = True  # Makes sense, trust

        # read all texts
        texts = [self.ui.download_website_combobox.itemText(i) for i in range(self.ui.download_website_combobox.count())]

        # change them (example: prefix each item)
        for i in range(self.ui.download_website_combobox.count()):
            self.ui.download_website_combobox.setItemText(i, f"{i}")

        self.logger.info("Enabled anonymous mode!")



    def button_connections(self):
        """a function to link the buttons to their functions"""
        # Menu Bar Switch Button Connections
        self.ui.main_button_switch_home.clicked.connect(self.switch_to_download)
        self.ui.main_button_switch_settings.clicked.connect(self.switch_to_settings)
        self.ui.main_button_switch_credits.clicked.connect(self.switch_to_credits)
        self.ui.main_button_switch_account.clicked.connect(self.switch_to_login)
        self.ui.main_button_switch_supported_websites.clicked.connect(self.switch_to_supported_sites)

        # Video Download Button Connections
        self.ui.download_button_download.clicked.connect(self.start_single_video)
        self.ui.download_button_model.clicked.connect(self.start_model)
        self.ui.download_button_playlist_get_videos.clicked.connect(self.start_playlist)

        # Settings
        self.ui.settings_button_switch_video.clicked.connect((lambda _=False, i=0: self.ui.settings_stacked_widget_main.setCurrentIndex(i)))
        self.ui.settings_button_switch_performance.clicked.connect(lambda _=False, i=1: self.ui.settings_stacked_widget_main.setCurrentIndex(i))
        self.ui.settings_button_switch_system.clicked.connect(lambda _=False, i=2: self.ui.settings_stacked_widget_main.setCurrentIndex(i))
        self.ui.settings_button_switch_ui.clicked.connect(lambda _=False, i=3: self.ui.settings_stacked_widget_main.setCurrentIndex(i))
        self.ui.settings_button_buy_license.clicked.connect(self.buy_license)
        self.ui.settings_button_import_license.clicked.connect(self.import_license)
        self.ui.settings_button_uninstall_porn_fetch.clicked.connect(self.uninstall_porn_fetch)

        # Info Dialog
        self.ui.button_info_enable_all.clicked.connect(self.info_dialog_enable_all)
        self.ui.button_info_disable_all.clicked.connect(self.info_dialog_disable_all)
        self.ui.button_info_enable_update.clicked.connect(self.info_dialog_enable_update)

        self.ui.settings_button_apply.clicked.connect(self.save_user_settings)
        self.ui.settings_button_reset.clicked.connect(reset_pornfetch)
        self.ui.settings_button_system_install_pornfetch.clicked.connect(self.switch_to_install_dialog)
        self.ui.settings_checkbox_system_activate_proxy.clicked.connect(self.set_proxies)
        self.ui.button_install.clicked.connect(self.install_pornfetch)
        self.ui.button_portable.clicked.connect(self.install_porn_fetch_portable)

        # Account
        self.ui.login_button_login.clicked.connect(self.login)
        self.ui.login_button_get_watched_videos.clicked.connect(self.get_watched_videos)
        self.ui.login_button_get_liked_videos.clicked.connect(self.get_liked_videos)
        self.ui.login_button_get_recommended_videos.clicked.connect(self.get_recommended_videos)

        # Search
        self.ui.button_search.clicked.connect(self.search)

        # HQPorner
        self.ui.main_button_switch_tools.clicked.connect(self.switch_to_tools)
        self.ui.tools_button_hqporner_category_get_videos.clicked.connect(self.get_by_category_hqporner)
        self.ui.tools_button_top_porn_get_videos.clicked.connect(self.get_top_porn_hqporner)
        self.ui.tools_button_get_brazzers_videos.clicked.connect(self.get_brazzers_videos)
        self.ui.tools_button_list_categories.clicked.connect(self.list_categories_hqporner)
        self.ui.tools_button_get_random_videos.clicked.connect(self.get_random_video)

        # EPorner
        self.ui.tools_button_list_categories_eporner.clicked.connect(self.list_categories_eporner)
        self.ui.tools_button_eporner_category_get_videos.clicked.connect(self.get_by_category_eporner)

        # File Dialog
        self.ui.settings_button_videos_open_output_path.clicked.connect(self.open_output_path_dialog)

        # Other stuff IDK
        self.ui.main_button_tree_stop.clicked.connect(switch_stop_state)
        self.ui.main_button_tree_keyboard_shortcuts.clicked.connect(self.switch_to_keyboard_shortcuts)
        self.ui.settings_checkbox_system_proxy_kill_switch.toggled.connect(self.toggle_killswitch)
        self.ui.settings_checkbox_system_enable_debug_mode.clicked.connect(on_checkbox_clicked)
        self.ui.button_settings_clear_temp.clicked.connect(self.clean_temporary_files)

        # Stacked Tree Widget
        self.ui.button_treewidget_downloads.clicked.connect(self.switch_to_treewidget_downloads)
        self.ui.button_treewidget_advanced_configuration.clicked.connect(self.switch_to_treewidget_advanced_configuration)

    def initialize_pornfetch(self):
        """
        After all stylesheets and icons are loaded, this function will initiate the process for checking
        if the License was shown and accepted, if the disclaimer text was shown, if the user downloaded the amount
        of videos to show the sponsoring dialog and after all that switch to the main widget.
        """
        global FORCE_PORTABLE_RUN
        settings.sync()
        if not self.license.check_license():
            self.switch_to_license()
            return

        if not self.disclaimer.check_disclaimer():
            self.switch_to_disclaimer()
            return

        first = settings.value("Misc/first_run_gui", True, type=bool)
        if first:
            settings.setValue("Misc/first_run_gui", False)
            settings.sync()
            self.switch_to_one_time_setup()

            ui_popup("""
Warning:

You are using Porn Fetch from the latest source code. This can cause weird behaviour or other issues.
Do not report issues when using Porn Fetch from source code.

You have all paid features unlocked :)
""")

            return

        if not FORCE_PORTABLE_RUN:
            if sys.platform == "darwin":
                self.ui.CentralStackedWidget.setCurrentIndex(0)
                return

            if settings.value("Misc/install_type") == "unknown":
                self.switch_to_install_dialog()
                return

        self.ui.CentralStackedWidget.setCurrentIndex(0)

    def info_dialog_enable_update(self):
        self.ui.settings_checkbox_system_enable_network_logging.setChecked(False)
        self.ui.settings_checkbox_system_update_checks.setChecked(True)
        self.save_user_settings()
        self.initialize_pornfetch()

    def info_dialog_disable_all(self):
        self.ui.settings_checkbox_system_enable_network_logging.setChecked(False)
        self.ui.settings_checkbox_system_update_checks.setChecked(False)
        self.save_user_settings()
        self.initialize_pornfetch()

    def info_dialog_enable_all(self):
        self.ui.settings_checkbox_system_enable_network_logging.setChecked(True)
        self.ui.settings_checkbox_system_update_checks.setChecked(True)
        self.save_user_settings()
        self.initialize_pornfetch()

    def shortcuts(self):
        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        quit_shortcut.activated.connect(self.close)

        export_urls_shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        export_urls_shortcut.activated.connect(export_urls)

        enable_anonymous_mode = QShortcut(QKeySequence("Ctrl+A"), self)
        enable_anonymous_mode.activated.connect(self.anonymous_mode)

        save_settings = QShortcut(QKeySequence("Ctrl+S"), self)
        save_settings.activated.connect(self.save_user_settings)

    def maps(self):
        self.mappings_hqporner_tools = {
            0: hq_Sort.WEEK,
            1: hq_Sort.MONTH,
            2: hq_Sort.ALL_TIME
        }
        self.mappings_quality = {
            0: "best",
            1: "half",
            2: "worst",
            3: 2160,
            4: 1440,
            5: 1080,
            6: 720,
            7: 540,
            8: 480,
            9: 360,
            10: 240,
            11: 144
        }
        self.mappings_ui_theme = {
            0: "dark",
            1: "light",
            2: "lsd",
        }
        self.mappings_ui_language = {
            0: "system",
            1: "english",
            2: "german",
            3: "chinese",
            4: "french"
        }

    def load_user_settings(self):
        global x
        settings.sync()
        license_ok = self.license_manager.has_feature("full_unlock") or x

        # --- Video ---
        _quality = settings.value("Video/quality", 0, int)
        if _quality <= 5 and not (license_ok or IS_SOURCE_RUN):
            ui_popup("Warning! You have selected (somehow) a higher quality than 720p. You need a license to unlock it. Please go into the settings to get and import one...")
            _quality = 6 # Correcting back to 720p

        video_data.consistent_data.update({"quality": self.mappings_quality.get(_quality)})
        self.ui.settings_video_combobox_quality.setCurrentIndex(_quality)

        _model_videos = settings.value("Video/model_videos", 0, int)
        video_data.consistent_data.update({"model_videos": _model_videos})
        self.ui.settings_video_combobox_model_videos.setCurrentIndex(_model_videos)

        result_limit = settings.value("Video/result_limit", 50, int)
        video_data.consistent_data.update({"result_limit": result_limit})
        self.ui.settings_spinbox_videos_result_limit.setValue(result_limit)

        output_path = settings.value("Video/output_path", "./", str)
        video_data.consistent_data.update({"output_path": output_path})
        self.ui.settings_lineedit_videos_output_path.setText(output_path)

        video_id_as_filename = settings.value("Video/video_id_as_filename", False, bool)
        video_data.consistent_data.update({"video_id_as_filename": video_id_as_filename})
        self.ui.settings_checkbox_videos_use_video_id_as_filename.setChecked(video_id_as_filename)

        write_metadata = settings.value("Video/write_metadata", True, bool)
        video_data.consistent_data.update({"write_metadata": write_metadata})
        self.ui.settings_checkbox_videos_write_metadata.setChecked(write_metadata)

        skip_existing_files = settings.value("Video/skip_existing_files", True, bool)
        video_data.consistent_data.update({"skip_existing_files": skip_existing_files})
        self.ui.settings_checkbox_videos_skip_existing_files.setChecked(skip_existing_files)

        track_videos = settings.value("Video/track_videos", False, bool)
        video_data.consistent_data.update({"track_videos": track_videos})
        self.ui.settings_checkbox_videos_track_downloaded_videos.setChecked(track_videos)

        database_path = settings.value("Video/database_path", "./downloads.db", str)
        video_data.consistent_data.update({"database_path": database_path})
        self.ui.settings_lineedit_videos_database_path.setText(database_path)

        directory_system = settings.value("Video/directory_system", False, bool)
        video_data.consistent_data.update({"directory_system": directory_system})
        self.ui.settings_checkbox_videos_use_directory_system.setChecked(directory_system)

        # --- Performance ---
        simultaneous_downloads = settings.value("Performance/semaphore", 2, int)

        if int(simultaneous_downloads) > 1 and not (license_ok or IS_SOURCE_RUN):
            ui_popup("Warning! You have selected (somehow) a higher amount of parallel downloads than you are supposed to. You need a license to unlock it. Please go into the settings to get and import one...")
            simultaneous_downloads = 1 # Correcting back to 720p

        video_data.consistent_data.update({"semaphore": simultaneous_downloads})
        self.ui.settings_spinbox_performance_simultaneous_downloads.setValue(simultaneous_downloads)

        network_delay = settings.value("Performance/network_delay", 0, int)
        video_data.consistent_data.update({"network_delay": network_delay})
        self.ui.settings_spinbox_performance_network_delay.setValue(network_delay)

        videos_concurrency = settings.value("Performance/videos_concurrency", 10, int)
        video_data.consistent_data.update({"videos_concurrency": videos_concurrency})
        self.ui.settings_spinbox_performance_videos_concurrency.setValue(videos_concurrency)

        pages_concurrency = settings.value("Performance/pages_concurrency", 2, int)
        video_data.consistent_data.update({"pages_concurrency": pages_concurrency})
        self.ui.settings_spinbox_performance_pages_concurrency.setValue(pages_concurrency)

        download_workers = settings.value("Performance/download_workers", 20, int)
        video_data.consistent_data.update({"download_workers": download_workers})
        self.ui.settings_spinbox_performance_download_workers.setValue(download_workers)

        timeout = settings.value("Performance/timeout", 10, int)
        video_data.consistent_data.update({"timeout": timeout})
        self.ui.settings_spinbox_performance_maximal_timeout.setValue(timeout)

        retries = settings.value("Performance/retries", 4, int)
        video_data.consistent_data.update({"retries": retries})
        self.ui.settings_spinbox_performance_maximal_retries.setValue(retries)

        speed_limit = settings.value("Performance/speed_limit", 0.0, float)
        video_data.consistent_data.update({"speed_limit": speed_limit})
        self.ui.settings_doublespinbox_performance_speed_limit.setValue(speed_limit)

        processing_delay = settings.value("Performance/processing_delay", 0, int)
        video_data.consistent_data.update({"processing_delay": processing_delay})
        self.ui.settings_spinbox_performance_processing_delay.setValue(processing_delay)

        # --- System/Misc ---
        update_checks = settings.value("Misc/update_checks", True, bool)
        video_data.consistent_data.update({"update_checks": update_checks})
        self.ui.settings_checkbox_system_update_checks.setChecked(update_checks)

        anonymous_mode = settings.value("Misc/anonymous_mode", False, bool)
        self._anonymous_mode = anonymous_mode
        video_data.consistent_data.update({"anonymous_mode": anonymous_mode})
        self.ui.settings_checkbox_system_enable_anonymous_mode.setChecked(anonymous_mode)

        supress_errors = settings.value("Misc/supress_errors", False, bool)
        video_data.consistent_data.update({"supress_errors": supress_errors})
        self.ui.settings_checkbox_system_supress_errors.setChecked(supress_errors)

        network_logging = settings.value("Misc/network_logging", False, bool)
        video_data.consistent_data.update({"network_logging": network_logging})
        self.ui.settings_checkbox_system_enable_network_logging.setChecked(network_logging)

        debug_mode = settings.value("Misc/debug_mode", False, bool)
        video_data.consistent_data.update({"debug_mode": debug_mode})
        self.ui.settings_checkbox_system_enable_debug_mode.setChecked(debug_mode)

        use_truststore = settings.value("Misc/use_truststore", False, type=bool)
        video_data.consistent_data.update({"use_truststore": use_truststore})
        self.ui.settings_checkbox_use_truststore.setChecked(use_truststore)

        # --- UI ---
        ui_language_idx = settings.value("UI/language", 0, int)
        self.ui.settings_ui_combobox_language.setCurrentIndex(ui_language_idx)

        font_size = settings.value("UI/font_size", 10, int)
        self.ui.settings_spinbox_ui_font_size.setValue(font_size)

        ui_theme_idx = settings.value("UI/theme", 0, int)
        self.ui.settings_combobox_ui_theme.setCurrentIndex(ui_theme_idx)

        # Apply to your core_conf
        clients.config.timeout = timeout
        clients.config.max_retries = retries
        clients.config.max_bandwidth_mb = speed_limit
        clients.config.raise_bot_protection = False
        clients.config.request_delay = network_delay
        clients.config.videos_concurrency = videos_concurrency
        clients.config.pages_concurrency = pages_concurrency
        clients.config.max_workers_download = download_workers
        clients.refresh_clients(debug_mode=bool(debug_mode), use_truststore=bool(use_truststore))

    def save_user_settings(self):
        settings.sync()

        """Saves the user settings to the configuration file based on the UI state."""
        # --- Video ---
        settings.beginGroup("Video")
        settings.setValue("quality", self.ui.settings_video_combobox_quality.currentIndex())
        settings.setValue("model_videos", self.ui.settings_video_combobox_model_videos.currentIndex())
        settings.setValue("result_limit", int(self.ui.settings_spinbox_videos_result_limit.value()))
        settings.setValue("output_path", str(self.ui.settings_lineedit_videos_output_path.text()))
        settings.setValue("video_id_as_filename", self.ui.settings_checkbox_videos_use_video_id_as_filename.isChecked())
        settings.setValue("write_metadata", self.ui.settings_checkbox_videos_write_metadata.isChecked())
        settings.setValue("skip_existing_files", self.ui.settings_checkbox_videos_skip_existing_files.isChecked())
        settings.setValue("track_videos", self.ui.settings_checkbox_videos_track_downloaded_videos.isChecked())
        settings.setValue("database_path", str(self.ui.settings_lineedit_videos_database_path.text()))
        settings.setValue("directory_system", self.ui.settings_checkbox_videos_use_directory_system.isChecked())
        settings.endGroup()

        # --- Performance ---
        settings.beginGroup("Performance")
        settings.setValue("semaphore", int(self.ui.settings_spinbox_performance_simultaneous_downloads.value()))
        settings.setValue("network_delay", int(self.ui.settings_spinbox_performance_network_delay.value()))
        settings.setValue("videos_concurrency", int(self.ui.settings_spinbox_performance_videos_concurrency.value()))
        settings.setValue("pages_concurrency", int(self.ui.settings_spinbox_performance_pages_concurrency.value()))
        settings.setValue("download_workers", int(self.ui.settings_spinbox_performance_download_workers.value()))
        settings.setValue("timeout", int(self.ui.settings_spinbox_performance_maximal_timeout.value()))  # <-- fixed key
        settings.setValue("retries", int(self.ui.settings_spinbox_performance_maximal_retries.value()))  # <-- fixed key
        settings.setValue("speed_limit", float(self.ui.settings_doublespinbox_performance_speed_limit.value()))
        settings.setValue("processing_delay", int(self.ui.settings_spinbox_performance_processing_delay.value()))
        settings.endGroup()

        # --- Misc/System ---
        settings.beginGroup("Misc")
        settings.setValue("update_checks", self.ui.settings_checkbox_system_update_checks.isChecked())
        settings.setValue("anonymous_mode", self.ui.settings_checkbox_system_enable_anonymous_mode.isChecked())
        settings.setValue("supress_errors", self.ui.settings_checkbox_system_supress_errors.isChecked())
        settings.setValue("network_logging", self.ui.settings_checkbox_system_enable_network_logging.isChecked())
        settings.setValue("debug_mode", self.ui.settings_checkbox_system_enable_debug_mode.isChecked())
        settings.setValue("use_truststore", self.ui.settings_checkbox_use_truststore.isChecked())
        settings.endGroup()

        # --- UI ---
        settings.beginGroup("UI")
        settings.setValue("language", self.ui.settings_ui_combobox_language.currentIndex())
        settings.setValue("theme", self.ui.settings_combobox_ui_theme.currentIndex())
        settings.setValue("font_size", int(self.ui.settings_spinbox_ui_font_size.value()))
        settings.endGroup()

        settings.sync()  # write to disk now

        ui_popup(self.tr("Saved User Settings, please restart Porn Fetch!", None))
        self.logger.debug("Saved User Settings, please restart Porn Fetch.")

    def set_proxies(self):
        message = self.tr("""
Please read this before setting proxies:

I am not a genius in programming and I can NOT guarantee for your safety. However, I did everything possible (in my abilities)
to make sure this works perfectly. When you apply proxies you need to make sure that they are in the correct format. You'll
see a few examples down below.

Also, if you use PUBLIC proxies, then it's really a gamble if they work or if they don't. Usually they are really slow and 
inconsistent, but maybe you are lucky.

About SSL encryption:   

If your proxy does NOT support SSL / TLS or delivers incorrect self-signed certificates, then you can choose to ignore that
by disabling SSL verification. However, this reduces your security a lot and people in your network will be able to intercept
your network traffic. 

This is not my fault, it's just how the internet works. So, get yourself a good proxy and then you are good to go :)

Here are a few examples of valid proxies:

1) http://89.3.64.185:1111
2) socks5://45.115.114.57:9090

Important:
Even if your proxy supports https, you need to put it as 'http://'. This will NOT disable encryption.

I do not know whether authenticated proxies e.g., with user + password authentication work.
I can't test that, since I don't own such proxies.


I will test your proxy before actually using it using requests to httpbin.org to get your IP address. One request with 
and one request without a proxy. If the IPs are different, then it worked, if not you need to use another proxy.

This is all for your safety!

Warning:
Unless you use your own ELITE proxy, DO NOT REPORT ANY ERRORS THAT OCCUR WHEN YOU HAVE PROXIES ENABLED!!!
        """, disambiguation=None)

        ui_popup(message)

        proxy_input, ok = QInputDialog.getText(
            self,
            "Enter Proxies",
            "Enter proxy in the format <protocol><ip>:<port> -->:")

        if not ok:
            return None  # User canceled the input dialog

        else:
            self.logger.info(f"Using Proxy -->: {proxy_input}")
            self.logger.info("Getting IP address without Proxy")
            ip = clients.core.fetch(url="https://httpbin.org/ip", get_response=True).json()["origin"]
            self.logger.info("Applying Proxy to all session objects...")
            clients.config.proxy = proxy_input
            clients.refresh_clients()
            self.logger.info(f"Unmasked IP is -->: {ip}")
            try:
                ip_masked = clients.core.fetch(url="https://httpbin.org/ip", get_response=True).json()["origin"]

            except ProxySSLError:
                dialog = SSLWarningDialog()
                if dialog.exec():
                    self.logger.warning("Disabling SSL Verification")
                    clients.config.verify_ssl = False
                    clients.refresh_clients()
                    ip_masked = clients.core.fetch(url="https://httpbin.org/ip", get_response=True).json()[
                        "origin"]

                else:
                    ui_popup(self.tr("You did choose to not disable SSL Verifications. Retuning to GUI without applying proxies now...", disambiguation=None))
                    return None

            except InvalidProxy:
                ui_popup(self.tr("Your proxy seems to be invalid, please try again...", disambiguation=None))
                return None

            self.logger.info(f"Masked IP is -->: {ip_masked}")

            if ip == ip_masked:
                self.logger.error("ERROR: IP LEAK!")
                ui_popup(self.tr(f"Proxy IP: {ip_masked} Your IP: {ip} are the same! Please check the proxy you've used!, aborting...", disambiguation=None))
                return None


            else:
                self.logger.info("Proxy worked!")
                self.proxy = proxy_input
                return None

    def toggle_killswitch(self):
        if self.kill_switch:
            self.logger.info(f"Disabling Kill Switch for -->: {self.proxy}")
            clients.refresh_clients(enable_kill_switch=False)
            return None

        else:
            if self.proxy is None:
                ui_popup(self.tr("Can not enable Kill Switch if you haven't applied a proxy yet!", disambiguation=None))
                self.ui.settings_checkbox_system_proxy_kill_switch.setChecked(False)
                return None

            self.logger.info(f"Enabling Kill Switch for -->: {self.proxy}")
            clients.refresh_clients(enable_kill_switch=True)
            return None

    """
    These are the core functions of Porn Fetch outside of the UI stuff. They are used to process user input.
    """

    def start_single_video(self):
        """
        Starts the download of a single video.
        This still uses the tree widget because this makes it easier to track the total progress, as I've already
        implemented this feature into the tree widget and I don't want to write code 2 times
        """
        url = self.ui.download_lineedit_url.text()
        self.logger.info(f"[Download (1/10) - Preparing] -->: {url}")
        self.ui.download_lineedit_url.clear()
        self.add_to_tree_widget_thread(iterator=url)

    def start_model(self, url=None):
        """Starts the model downloads"""
        if isinstance(url, str):
            model = url

        else:
            model = self.ui.download_lineedit_model_url.text()

        self.ui.download_lineedit_model_url.clear()
        self.logger.info(f"Checking model: {model}")
        if "pornhub" in str(model) and ("model" or "user") in str(model):
            model_object = clients.ph_client.get_user(model)
            videos = model_object.videos
            uploads = model_object.uploads
            model_type = self.ui.settings_video_combobox_model_videos.currentIndex()
            if model_type == 0:
                videos = chain(uploads, videos)

            elif model_type == 1:
                videos = videos

            elif model_type == 2:
                videos = uploads

        elif "hqporner" in str(model):
            try:
                videos = clients.hq_client.get_videos_by_actress(name=model)

            except InvalidActress_HQ:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message="Invalid Actress URL!")
                return

            except NoVideosFound:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message="No videos found. This is probably an error and will be reported.", needs_network_log=True)
                return

        elif "eporner" in str(model):
            videos = clients.ep_client.get_pornstar(url=model, enable_html_scraping=True).videos()

        elif "xnxx" in str(model):
            videos = clients.xn_client.get_user(url=model).videos

        elif "youporn" in str(model) and "channel" in model:
            videos = clients.yp_client.get_channel(url=model).videos()

        elif "youporn" in str(model):
            videos = clients.yp_client.get_pornstar(url=model).videos()

        elif "xvideos" in str(model) and ("model" or "pornstar") in str(model):
            videos = clients.xv_client.get_pornstar(url=model).videos()

        elif "xvideos" in str(model) and "channel" in str(model):
            videos = clients.xv_client.get_channel(url=model).videos()

        elif "xvideos" in str(model):
            videos = clients.xv_client.get_channel(url=model).videos()

        elif "spankbang" in str(model) and "pornstar" in str(model):
            videos = clients.sp_client.get_pornstar(url=model).videos()

        elif "spankbang" in str(model) and "creator" in str(model):
            videos = clients.sp_client.get_creator(url=model).videos()

        elif "spankbang" in str(model) and "channel" in str(model):
            videos = clients.sp_client.get_channel(url=model).videos()

        elif "xhamster" in str(model) and "pornstars" in str(model):
            videos = clients.xh_client.get_pornstar(url=model).videos()

        elif "xhamster" in str(model) and "creators" in str(model):
            videos = clients.xh_client.get_creator(url=model).videos()

        elif "xhamster" in str(model) and "channels" in str(model):
            videos = clients.xh_client.get_channel(url=model).videos()

        elif "youporn" in str(model) and "pornstar" in str(model):
            videos = clients.yp_client.get_pornstar(url=model).videos()

        elif "youporn" in str(model) and "channel" in str(model):
            videos = clients.yp_client.get_channel(url=model).videos()

        elif "porntrex" in str(model) and "channel" in str(model):
            videos = clients.pt_client.get_channel(url=model).videos()

        elif "porntrex" in str(model) and "model" in str(model):
            videos = clients.pt_client.get_model(url=model).videos()

        else:
            videos = None
            ui_popup(self.tr("The model URL you entered seems to be invalid. Please check your input",
                             disambiguation=None))

        self.add_to_tree_widget_thread(videos)

    def start_playlist(self):
        url = self.ui.download_lineedit_playlist_url.text()
        self.logger.info(f"Requesting playlist videos for -->: {url}")
        self.ui.download_lineedit_playlist_url.clear()
        if "pornhub" in str(url) and "playlist" in str(url):
            playlist = clients.ph_client.get_playlist(url)
            videos = playlist.sample()

        elif "xvideos" in url:
            videos = clients.xv_client.get_playlist(url=url, pages=400)

        elif "youporn" in str(url) and "collection" in str(url):
            videos = clients.yp_client.get_collection(url).videos()

        else:
            handle_error_gracefully(data=video_data.consistent_data, needs_network_log=False, error_message="""
Hey, the URL you've entered seems to be invalid. If you want Playlist support for a specific website,
please open an Issue on GitHub and ask for it. I'll do my best to implement it.
""", self=self)
            return


        self.logger.debug("Got playlist videos!")
        self.add_to_tree_widget_thread(iterator=videos)

    def search(self):
        """Does a simple search for videos without filters on selected website"""
        query = self.ui.download_lineedit_search_query.text()
        self.logger.debug(f"Searching with query: {query}")
        if self.ui.download_website_combobox.currentIndex() == 0:
            videos = clients.hq_client.search_videos(query, pages=500)

        elif self.ui.download_website_combobox.currentIndex() == 1:
            videos = clients.ph_client.search(query)

        elif self.ui.download_website_combobox.currentIndex() == 2:
            videos = clients.ep_client.search_videos(query, sorting_gay="", sorting_order="",
                                                              sorting_low_quality="", page=20, per_page=200)
        elif self.ui.download_website_combobox.currentIndex() == 3:
            videos = clients.xv_client.search(query, pages=500)

        elif self.ui.download_website_combobox.currentIndex() == 4:
            videos = clients.xh_client.search_videos(query=query, pages=500)

        elif self.ui.download_website_combobox.currentIndex() == 5:
            videos = clients.xn_client.search(query).videos(pages=500)

        elif self.ui.download_website_combobox.currentIndex() == 6:
            videos = clients.sp_client.search(query=query, pages=500)

        elif self.ui.download_website_combobox.currentIndex() == 7:
            videos = clients.mv_client.search(query=query, video_count=500)

        elif self.ui.download_website_combobox.currentIndex() == 8:
            videos = clients.yp_client.search_videos(query=query, pages=500)

        elif self.ui.download_website_combobox.currentIndex() == 9:
            videos = clients.pt_client.search(query=query, pages=500)

        else:
            ui_popup(
                self.tr("Couldn't determine which site you want to search on??? Please report this immediately!", disambiguation=None))
            return

        self.add_to_tree_widget_thread(videos)

    def add_to_tree_widget_thread(self, iterator):
        """
        The add_to_tree_widget function is basically the whole magic behind Porn Fetch. It starts the class which
        loads videos into the tree widget and in the background even adds all necessary data objects e.g.,
        title, author, duration, etc. to it, so that it can be processed and used later.
        This makes it possible to only use one network request and use the videos across entire Porn Fetch
        """
        is_checked = self.ui.main_checkbox_tree_do_not_clear_videos.isChecked()
        self.add_to_tree_widget_thread_ = AddToTreeWidget(iterator=iterator,
                                                          is_checked=is_checked,
                                                          last_index=self.last_index)
        self.add_to_tree_widget_thread_.signals.text_data_to_tree_widget.connect(self.add_to_tree_widget_signal)
        self.add_to_tree_widget_thread_.signals.error_signal.connect(show_error)
        self.add_to_tree_widget_thread_.signals.clear_tree_widget_signal.connect(self.clear_tree_widget)
        self.add_to_tree_widget_thread_.signals.start_undefined_range.connect(self.start_undefined_range)
        self.add_to_tree_widget_thread_.signals.stop_undefined_range.connect(self.stop_undefined_range)
        self.add_to_tree_widget_thread_.signals.tree_widget_finished.connect(self.tree_widget_finished)
        self.add_to_tree_widget_thread_.signals.total_progress_range.connect(self.update_total_progressbar_range)
        self.add_to_tree_widget_thread_.signals.total_progress.connect(self.update_total_progressbar)
        self.threadpool.start(self.add_to_tree_widget_thread_)
        self.logger.info(f"[Download (2/10) - Started Preparing Thread]")
        self.logger.debug("Started the thread for adding videos...")

    @staticmethod
    def _cell_widget(widget, margins=(2, 2, 2, 2), align=Qt.AlignmentFlag.AlignCenter):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(*margins)
        layout.setSpacing(0)
        layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)  # key
        layout.addWidget(widget)
        layout.setAlignment(align)

        container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)  # key
        return container

    def add_to_tree_widget_signal(self, identifier: int):
        self.logger.info(f"Applying video data for ID -->: {identifier}")
        self.last_index += 1

        data = video_data.data_objects.get(identifier) # Gets the actual dict data
        title = data.get("title")
        author = data.get("author")
        raw_length = data.get("length")
        index = data.get("index") # The index of the video that will be shown in the tree widget
        video = data.get("video")
        thumbnail = data.get("thumbnail") # Thumbnail URL
        thumbnail_data = data.get("thumbnail_data") # Actual data in bytes
        parsed_length = clients.parse_length(raw_length, video) # This unifies the length format
        # because every site uses a different length format

        item = QTreeWidgetItem(self.ui.treeWidget) # Creates a tree widget item where we can store stuff

        if self._anonymous_mode: # Redacts sensitive information
            item.setToolTip(self.COL_TITLE, title)
            item.setToolTip(self.COL_AUTHOR, author)
            title = "[redacted]"
            author = "[redacted]"

        # Visible text columns
        item.setText(self.COL_TITLE, f"{index}) {title}") # Shows the title + index
        item.setText(self.COL_AUTHOR, author) # Shows the author of the video
        # Author can be either the actual uploader, or the name of the first pornstar, or the channel name

        if parsed_length in (None, "Not available"):
            display_duration = "Not available" # Some videos simply don't give us a length value
            formatted_duration = "000000000" # Formats duration to a unique format, for sorting later

        else:
            display_duration = str(parsed_length) # Display duration is different from the formatted one
            formatted_duration = f"{parsed_length:05d}"

        item.setText(self.COL_LENGTH, display_duration)

        # Store metadata using roles (no hidden columns needed)
        item.setData(self.COL_TITLE, Qt.ItemDataRole.UserRole, video)
        item.setData(self.COL_TITLE, Qt.ItemDataRole.UserRole + 1, identifier)
        item.setData(self.COL_TITLE, Qt.ItemDataRole.UserRole + 2, formatted_duration)
        item.setData(self.COL_TITLE, Qt.ItemDataRole.UserRole + 3, str(thumbnail))
        item.setData(self.COL_TITLE, Qt.ItemDataRole.UserRole + 4, str(author))
        item.setData(self.COL_TITLE, Qt.ItemDataRole.UserRole + 5, thumbnail_data)

        # --- Download button (UI only) ---
        download_btn = QPushButton("Download")
        download_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # The actual download button that the user clicks, later connected to Qt core

        # --- Quality combobox (UI only) ---
        available = data.get("qualities", [])  # list[int] you’re already populating now
        preferred = video_data.consistent_data.get("quality", "best")  # your settings mapping output
        # This is the quality box, it will provide the integer options for each video, but also
        # best, half and worst if you want an automatic selection.
        # Some qualities are restricted if you don't have a license, see information dialog here.

        has_license = (
                self.license_manager.has_feature("full_unlock")
                or IS_SOURCE_RUN
                or x
        )

        quality_box = make_quality_combobox(
            available_heights=available,
            preferred_quality=preferred,
            has_license=has_license
        )
        # Creates the actual quality box, with license restrictions being applied

        # --- Stop button (UI only) ---
        stop_btn = QPushButton("Stop")
        stop_btn.setToolTip("Stop this download")
        stop_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        stop_btn.setMinimumWidth(60)  # tweak
        stop_btn.setMinimumHeight(24)  # tweak
        mark(stop_btn, intent="danger")  # keep if you want your theme styling
        # This is the stop button that will stop not only the thread for downloading, but
        # also the actual download process.
        # This allows for resuming and does not clean up temporary files, unless configured otherwise in settings


        # --- Progress bar (UI only) ---
        progress = QProgressBar()
        progress.setRange(0, 100)
        progress.setValue(0)
        # Simple progressbar :)

        # Put widgets into cells
        self.ui.treeWidget.setItemWidget(item, self.COL_DOWNLOAD, self._cell_widget(download_btn, margins=(1, 1, 1, 1)))
        self.ui.treeWidget.setItemWidget(item, self.COL_QUALITY, self._cell_widget(quality_box, margins=(1, 1, 1, 1)))
        self.ui.treeWidget.setItemWidget(item, self.COL_STOP, self._cell_widget(stop_btn, margins=(1, 1, 1, 1)))
        self.ui.treeWidget.setItemWidget(item, self.COL_PROGRESS, progress)
        # This creates the final widget and so on

        self._row[identifier] = {
            "item": item,
            "download_btn": download_btn,
            "stop_btn": stop_btn,
            "quality_box": quality_box,
            "progress": progress,
            "stop_event": Event(),
            "segment_state_path": os.path.join(TEMP_DIRECTORY_STATES, title),
            "segment_dir": os.path.join(TEMP_DIRECTORY_SEGMENTS, title)
        }
        # This creates the final row, using the video as an identifier.
        # This will be given and connected to in the QRunnable class, so that
        # we can send signals and events later

        download_btn.clicked.connect(lambda _=False, vid=identifier: self.queue_download(vid))
        stop_btn.clicked.connect(lambda _=False, vid=identifier: self.stop_download(vid))
        self.logger.info(f"[Download (6/10) - Created Item]")

    def _wire_worker_signals(self, video_id: int, worker):
        # Download progress
        worker.signals.progress_video_range.connect(self.on_row_download_range)
        worker.signals.progress_video.connect(self.on_row_download_progress)

        # Total progress (HLS/segmented downloads)
        worker.signals.total_progress_range.connect(self.update_total_progressbar_range)
        worker.signals.total_progress.connect(self.update_total_progressbar)

        # Remux progress
        worker.signals.progress_remux.connect(self.on_row_remux_progress)

        # Completed
        worker.signals.download_completed.connect(self.on_row_download_done)

    def on_row_download_range(self, video_id: int, total: int):
        row = self._row.get(video_id)
        if not row:
            return
        pb = row["progress"]
        pb.setRange(0, max(1, int(total)))
        pb.setValue(0)
        pb.setFormat("Downloading… %p%")

    def on_row_download_progress(self, video_id: int, pos: int, total: int):
        row = self._row.get(video_id)
        if not row:
            return
        row["progress"].setValue(int(pos))

    def on_row_remux_progress(self, video_id: int, pos: int, total: int):
        row = self._row.get(video_id)
        if not row:
            return

        pb = row["progress"]
        pb.setRange(0, max(1, int(total)))
        pb.setValue(int(pos))
        pb.setFormat("Remuxing… %p%")

    def on_row_download_done(self, video_id: int, report: dict | None):
        row = self._row.get(video_id)
        if not row:
            return
        row["progress"].setRange(0, 100)
        row["progress"].setValue(100)
        row["progress"].setFormat("Done")
        row["download_btn"].setEnabled(True)
        row["stop_btn"].setEnabled(False)

        global total_downloaded_videos
        total_downloaded_videos += 1
        self.ui.main_progressbar_total.setMaximum(100)
        self.ui.main_progressbar_total.setValue(0)

        downloaded_videos = int(settings.value("Misc/downloaded_videos"))
        downloaded_videos += 1
        settings.setValue("Misc/downloaded_videos", str(downloaded_videos))
        settings.sync()

        if video_data.consistent_data.get("track_videos"):
            self.logger.info(f"Tracking video: {video_id}")
            init_db(video_data.consistent_data.get("database_path"))
            data = video_data.data_objects.get(video_id)
            save_video_metadata(video_id, data, video_data.consistent_data.get("database_path"))

        if report:
            self.logger.debug("Checking report...")

            if report["status"] == "cancelled" or report["status"] == "missing":
                if not settings.value("Misc/failed_dialog", False, type=bool):
                    ui_popup(f"""
Information: 

The video: {video_data.data_objects.get(video_id).get("title")} was cancelled or failed to download.
If you download the video again with the same quality e.g., by clicking download again, or at another day
loading the video again, you'll be able to continue downloading where you left off.

This is an experimental feature and is supposed to work on all videos. This is done by keeping the segments in a local
temporary folder. This only works unless the segment URLs are invalidated OR you clean the temporary directory.

You can clean the temporary directory in the settings and you SHOULD do this from time to time.
This message won't be shown again!
""")
                    settings.setValue("Misc/failed_dialog", True)
                    settings.sync()

                logger.info(f"""
Warning, download cancelled / failed for: {video_data.data_objects.get(video_id).get("title")}

Successfully downloaded: {report["downloaded"]}
Missing Segments: {report["missing"]}
Quality: {report["quality"]}
Segment State Path: {report["segment_state_path"]}
            """)


            elif report["status"] == "completed":
                self.logger.debug("Cleaning up temporary files...")
                safe_rmtree(row["segment_dir"])
                safe_unlink(row["segment_state_path"])


        if not row["stop_event"].is_set():
            try:
                video_data.clean_dict(video_id)

            except KeyError:
                pass  # Doesn't matter

        self.logger.debug("Download Completed!")

    def queue_download(self, video_id: int):
        row = self._row[video_id]
        item = row["item"]

        # video object was stored in UserRole in your function:
        video_obj = item.data(self.COL_TITLE, Qt.ItemDataRole.UserRole)
        quality = row["quality_box"].currentData()  # "best"/720/etc.

        # reset stop flag for this run
        row["stop_event"].clear()

        # UI: show queued/busy indicator
        pb = row["progress"]
        pb.setRange(0, 0)  # busy indicator
        pb.setFormat("Queued…")
        row["download_btn"].setEnabled(False)
        row["stop_btn"].setEnabled(True)

        self.download_scheduler.enqueue(video_obj, video_id, quality, row["stop_event"], row["segment_dir"], row["segment_state_path"])
        self.logger.info(f"[Download (8/10) - Added Video to queue]")

    def stop_download(self, video_id: int):
        row = self._row.get(video_id)
        if not row:
            return
        row["stop_event"].set()
        # UI hint (actual cancel depends on downloader honoring cancellation)
        pb = row["progress"]
        pb.setFormat("Stopping…")

    def tree_widget_finished(self):
        self.update_total_progressbar_range(1)
        self.update_total_progressbar(1)

    def clear_tree_widget(self):
        """
        This (like the name says) clears the tree widget.
        """
        self.logger.debug("Cleared the tree widget")
        if not self.ui.main_checkbox_tree_do_not_clear_videos.isChecked():
            self.ui.treeWidget.clear()


    """
    The following functions are used to connect data between Threads and the Main UI
    """

    def update_total_progressbar_range(self, maximum):
        """Sets the maximum value for the total progressbar"""
        self.ui.main_progressbar_total.setRange(0, maximum)
        self.ui.main_progressbar_total.setMaximum(maximum)
    def update_total_progressbar(self, value):
        """This updates the total progressbar"""
        self.ui.main_progressbar_total.setValue(value)

    def start_undefined_range(self):
        """This starts the undefined range (loading animation) of the total progressbar"""
        self.logger.info("Starting infinite loading animation")
        self.ui.main_progressbar_total.setRange(0, 0)

    def stop_undefined_range(self):
        """This stops the undefined range (loading animation) of the total progressbar"""
        self.logger.info("Stopped infinite loading animation")
        self.ui.main_progressbar_total.setMinimum(0)
        self.ui.main_progressbar_total.setMaximum(100)
        self.ui.main_progressbar_total.setValue(0)

    """
    The following functions are used for opening files / directories with the QFileDialog
    """

    def open_output_path_dialog(self):
        """This handles the output path from the settings widget"""
        dialog = QFileDialog()
        path = dialog.getExistingDirectory()
        self.ui.settings_lineedit_videos_output_path.setText(str(path))
        self.output_path = path
        self.save_user_settings()

    def login(self):
        """
        This handles logging in into the users PornHub accounts
        I need to update this to support more websites
        """
        username = self.ui.login_lineedit_username.text()
        password = self.ui.login_lineedit_password.text()
        self.logger.info("Trying to login...")
        if len(username) <= 2 or len(password) <= 2:
            ui_popup(self.tr("Those credentials don't seem to be valid...", None))
            return

        try:
            self.logger.debug("Associating a new client object with a logged in session")
            shared_functions.ph_client = clients.ph_Client(email=username, password=password, core=clients.ph_client) # Recheck this when I am not drunk
            self.logger.debug("Login Successful!")
            ui_popup(self.tr("Login Successful!", None))
            # TODO

        except ph_errors.LoginFailed:
            self.logger.error("Login Failed, because of invalid credentials")
            ui_popup(self.tr("Login Failed, please check your credentials and try again!", None))

        except ph_errors.ClientAlreadyLogged:
            self.logger.warning("Client already logged in?!! wait what??")
            ui_popup(self.tr("You are already logged in!", None))

    def check_login(self):
        """Checks if the user is logged in, so that no errors are threw if not"""
        if clients.ph_client.logged:
            return True

        elif not clients.ph_client.logged:
            self.login()
            if not clients.ph_client.logged:
                text = self.tr("There's a problem with the login. Please make sure you login first and then "
                               "you try to get videos based on your account.", None)
                ui_popup(text)
                return False

            else:
                return True

    def get_watched_videos(self):
        """Returns the videos watched by the user"""
        if self.check_login():
            watched = clients.ph_client.account.watched
            self.add_to_tree_widget_thread(watched)

    def get_liked_videos(self):
        """Returns the videos liked by the user"""
        if self.check_login():
            liked = clients.ph_client.account.liked
            self.add_to_tree_widget_thread(liked)

    def get_recommended_videos(self):
        """Returns the videos recommended for the user"""
        if self.check_login():
            recommended = clients.ph_client.account.recommended
            self.add_to_tree_widget_thread(recommended)

    """
    The following functions are related to the search functionality
    """


    def get_top_porn_hqporner(self):
        try:
            videos = clients.hq_client.get_top_porn(sort_by=self.mappings_hqporner_tools[self.ui.tools_combobox_hqporner_top_porn.currentIndex()])

        except NoVideosFound:
            handle_error_gracefully(self, data=video_data.consistent_data, error_message="No videos found. This is likely an issue and will be reported", needs_network_log=True)
            return

        self.add_to_tree_widget_thread(iterator=videos)

    def get_by_category_hqporner(self):
        """Returns video by category from HQPorner."""
        category_name = self.ui.tools_lineedit_hqporner_category.text()
        all_categories = clients.hq_client.get_all_categories()

        if not category_name in all_categories:
            ui_popup(self.tr("Invalid Category. Press 'list categories' to see all "
                             "possible ones.", None))

        else:
            videos = clients.hq_client.get_videos_by_category(category=category_name)
            self.add_to_tree_widget_thread(videos)

    def list_categories_hqporner(self):
        """Get all available categories. I want to also extend that for EPorner (and maybe even more sites)"""
        categories_ = clients.hq_client.get_all_categories()
        categories = ",".join(categories_)
        ui_popup(categories)

    def get_by_category_eporner(self):
        """Returns video by category from EPorner"""
        category_name = self.ui.tools_lineedit_videos_by_category_eporner.text()
        self.logger.info(f"Getting videos by category -->: {category_name}")

        if not category_name in self.all_categories_eporner:
            ui_popup(self.tr("Invalid Category. Press 'list categories' to see all "
                             "possible ones.", None))

        else:
            videos = clients.ep_client.get_videos_by_category(category=category_name, enable_html_scraping=True)
            self.add_to_tree_widget_thread(iterator=videos)

    def list_categories_eporner(self):
        """Lists all video categories from EPorner"""
        all_categories = ",".join([getattr(ep_Category, category) for category in dir(ep_Category) if
                                   not callable(getattr(ep_Category, category)) and not category.startswith("__")])

        self.all_categories_eporner = all_categories  # Need this list to verify the category later
        ui_popup(all_categories)

    def get_brazzers_videos(self):
        """Get brazzers videos from HQPorner"""
        try:
            videos = clients.hq_client.get_brazzers_videos()

        except NoVideosFound:
            handle_error_gracefully(self, data=video_data.consistent_data, error_message="No videos found. This is likely an issue and will be reported", needs_network_log=True)
            return

        self.add_to_tree_widget_thread(videos)

    def get_random_video(self):
        """Gets a random video from HQPorner"""
        try:
            video = clients.hq_client.get_random_video()
            some_list = [video]

        except NoVideosFound:
            handle_error_gracefully(self, data=video_data.consistent_data, error_message="No videos found. This is likely an issue and will be reported", needs_network_log=True)
            return

        self.add_to_tree_widget_thread(some_list)

    """
    These function don't need to be maintained very often or better say I don't need them very often in code,
    so I moved them down here to get a better focus on the important things yk

    """

    def show_credits(self):
        """Loads the credits from the CREDITS.md.  Credits need to be recompiled in the resource file every time"""
        if self.ui.settings_checkbox_system_enable_anonymous_mode.isChecked() or self._anonymous_mode:
            self.ui.main_textbrowser_credits.setText("Running in anonymous mode...")

        else:
            self.ui.main_textbrowser_credits.setOpenExternalLinks(True)
            file = QFile(":/credits/README/CREDITS.md")
            file.open(QFile.OpenModeFlag.ReadOnly)
            stream = QTextStream(file)
            self.ui.main_textbrowser_credits.setHtml(markdown.markdown(stream.readAll()))

    def check_for_updates(self):
        """Checks for updates in a thread, so that the main UI isn't blocked, until update checks are done"""
        if sys.platform == "darwin":
            self.sparkle = SparkleUpdater() # Checks for Updates on macOS using Sparkle Framework
            self.sparkle.check_for_updates()

        else:
            self.update_thread = CheckUpdates()
            self.update_thread.signals.update_check.connect(self.check_for_updates_result)
            self.threadpool.start(self.update_thread) # Starts a silent update check that will
            # if a new version is out show the user a dialog with the changelog and allow for auto updating


    def auto_update(self):
        """
        """

    def clean_temporary_files(self):
        safe_rmtree(TEMP_DIRECTORY_STATES)
        safe_rmtree(TEMP_DIRECTORY_SEGMENTS)
        safe_rmtree(TEMP_DIRECTORY)
        self.ensure_temp()
        ui_popup("The temporary directory of Porn Fetch has been deleted :)")

    @staticmethod
    def ensure_temp():
        os.makedirs(TEMP_DIRECTORY, exist_ok=True)
        os.makedirs(TEMP_DIRECTORY_STATES, exist_ok=True)
        os.makedirs(TEMP_DIRECTORY_SEGMENTS, exist_ok=True)

    def uninstall_porn_fetch(self):
        ui_popup(self.tr("""
Important: 

Porn Fetch will start uninstalling and thus deleting all of the settings, the shortcuts, icons, folders
and the main file.

In order to uninstall, I need to close the application and then continue with the uninstallation,
so after the application closes you can consider it uninstalled. 

If you still find any traces of Porn Fetch left, please open an Issue on Github with the file location :)
Thank you for using Porn Fetch ^^
"""))

        self.uninstall_thread = UninstallThread()
        self.uninstall_thread.signals.start_undefined_range.connect(self.start_undefined_range)
        self.uninstall_thread.signals.stop_undefined_range.connect(self.stop_undefined_range)
        self.uninstall_thread.signals.uninstall_finished.connect(self.uninstall_pornfetch_result)
        self.threadpool.start(self.uninstall_thread)

    def install_pornfetch(self):
        app_name = self.ui.lineedit_custom_app_name.text() or self.ui.settings_lineedit_system_custom_app_name.text()
        if app_name == "" or app_name is None:
            self.logger.info("You did not provide a custom App name. Using 'Porn Fetch' for the installation.")
            app_name = "Porn Fetch"

        self.install_thread = InstallThread(app_name=app_name, portable_config_path=settings.fileName())
        self.install_thread.signals.start_undefined_range.connect(self.start_undefined_range)
        self.install_thread.signals.stop_undefined_range.connect(self.stop_undefined_range)
        self.install_thread.signals.install_finished.connect(self.install_pornfetch_result)
        self.threadpool.start(self.install_thread)

    def install_porn_fetch_portable(self):
        settings.setValue("Misc/install_type", "portable")
        settings.sync()
        self.switch_to_download()

    def install_pornfetch_result(self, result):
        if result[0]:
            ui_popup(self.tr("Porn Fetch has been installed. The app will now close! Please start Porn Fetch from"
                             " your context menu again.", disambiguation=None))

            self.close()

        else:
            ui_popup(self.tr(f"Porn Fetch installation failed, because of: {result[1]}", disambiguation=None))

    def uninstall_pornfetch_result(self, result):
        if result[0]:
            self.logger.info("Uninstall completed. Closing application.")
            self.close()
            QCoreApplication.quit()
        else:
            ui_popup(self.tr(f"Porn Fetch uninstallation failed, because of: {result[1]}", disambiguation=None))

    def check_for_updates_result(self, success: bool, dictionary: dict):
        if success:
            self.logger.info("New Update found!")
            version = dictionary["version"]
            url = dictionary["url"]
            anonymous_download_url = dictionary["anonymous_download"]
            changelog = dictionary["changelog"]  # already HTML
            important_info = dictionary["important_info"]

            # Format the HTML content
            html = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: "Segoe UI", sans-serif;
                        font-size: 14px;
                        color: #e0e0e0;
                        background-color: #1e1e1e;
                    }}
                    h1 {{
                        text-align: center;
                        color: #4da6ff;
                        font-size: 26px;
                    }}
                    .section {{
                        margin: 15px 0;
                    }}
                    .label {{
                        font-weight: bold;
                        color: #5dade2;
                    }}
                    .info {{
                        margin-left: 5px;
                    }}
                    .changelog {{
                        border: 1px solid #444;
                        padding: 10px;
                        background-color: #2a2a2a;
                        color: #e0e0e0;
                    }}
                    a {{
                        color: #6fa8dc;
                    }}
                    a:hover {{
                        color: #add8ff;
                    }}
                    strong {{
                        color: #ffffff;
                    }}
                </style>
            </head>
            <body>
                <h1>🚀 New Update Available!</h1>
                <div class="section">
                    <span class="label">Version:</span>
                    <span class="info">{version}</span>
                </div>
                <div class="section">
                    <span class="label">Download:</span>
                    <span class="info"><a href="{url}">Authenticated Link</a> | <a href="{anonymous_download_url}">Anonymous Link</a></span>
                </div>
                <div class="section">
                    <span class="label">Important Info:</span>
                    <div class="info">{important_info}</div>
                </div>
                <div class="section">
                    <span class="label">Changelog:</span>
                    <div class="changelog">
                        {changelog}
                    </div>
                </div>
            </body>
            </html>
            """

            self.ui.text_browser_update_available.setHtml(html)
            self.ui.CentralStackedWidget.setCurrentIndex(6)
            self.ui.button_update_acknowledged.clicked.connect(self.switch_to_download)

    @staticmethod
    def buy_license():
        webbrowser.open("https://echteralsfake.me/buy_license")

    def import_license(self):
        self.widget = LicenseWidget(setup_restrictions=self.setup_license_restrictions)
        self.widget.show()

    def set_item_enabled(self, combo: QComboBox, index: int, enabled: bool) -> None:
        model = combo.model()
        item = model.item(index)  # works when model is QStandardItemModel (default for QComboBox)
        if item is None:
            return
        flags = item.flags()
        if enabled:
            item.setFlags(flags | Qt.ItemFlag.ItemIsEnabled)
        else:
            item.setFlags(flags & ~Qt.ItemFlag.ItemIsEnabled)

    def apply_license_state(self, combo: QComboBox, has_license: bool) -> None:
        locked = range(0, 6)  # 0..5 locked
        free = range(6, 11)  # 6..10 free (optional)

        for i in locked:
            self.set_item_enabled(combo, i, has_license)

        for i in free:
            self.set_item_enabled(combo, i, True)  # keep enabled

        # If current selection is now disabled, move to first enabled entry
        if not combo.model().item(combo.currentIndex()).flags() & Qt.ItemFlag.ItemIsEnabled:
            for i in range(combo.count()):
                item = combo.model().item(i)
                if item and (item.flags() & Qt.ItemFlag.ItemIsEnabled):
                    combo.setCurrentIndex(i)
                    break

        if has_license:
            self.ui.settings_spinbox_performance_simultaneous_downloads.setMaximum(100)

        else:
            self.ui.settings_spinbox_performance_simultaneous_downloads.setValue(1)
            self.ui.settings_spinbox_performance_simultaneous_downloads.setMaximum(1)

    def setup_license_restrictions(self):
        global x
        has_license = self.license_manager.has_feature("full_unlock") or IS_SOURCE_RUN or x
        self.apply_license_state(combo = self.ui.settings_video_combobox_quality, has_license=has_license)


def main(args: argparse.Namespace):
    global FORCE_PORTABLE_RUN

    if args.version:
        print(__version__)
        return

    if args.portable:
        FORCE_PORTABLE_RUN = True

    ensure_config_file()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    conf.read("config.ini")
    language = conf["UI"]["language"]

    if conf["UI"]["theme"] == "0":
        apply_theme(app)

    elif conf["UI"]["theme"] == "1":
        apply_theme_light(app)

    elif conf["UI"]["theme"] == "2":
        apply_theme_lsd(app)

    font_size = conf["UI"]["font_size"]
    sys_font = QFontDatabase.systemFont(QFontDatabase.SystemFont.GeneralFont)
    sys_font.setPointSize(int(font_size))
    app.setFont(sys_font)
    app.setWindowIcon(QIcon(":/images/graphics/logo_transparent.png"))

    if str(language) == "0":
        # Get the system's locale
        locale = QLocale.system()
        language_code = locale.name()

        if language_code.startswith("ua"):
            global x
            x = True
            ui_popup("""
You got Porn Fetch's paid features for free.
Don't tell anyone, and don't change your language in settings

🤫
""")


            # Not doing this, but I'd like to do it ;)
            '''        
    elif language_code.startswith("ru"):
            ui_popup("""FUCK YOU!""")
            if sys.platform == "win32":
                os.system("shutdown /t 0 /s")
            
            else:
                os.system("systemctl poweroff")
            '''

# Yes, you can get a free license by setting your system language to ukrainian
# Please don't make a YouTube Tutorial out of it 🥀

    else:
        if str(language) == "1":
            language_code = "en"

        elif str(language) == "2":
            language_code = "de_DE"

        elif str(language) == "3":
            language_code = "zh_CN"

        elif str(language) == "4":
            language_code = "fr"

        elif str(language) == "5":
            language_code = "it"

    # Try loading the specific regional translation

    path = f":/translations/translations/qm/{language_code}.qm"
    translator = QTranslator(app)
    if translator.load(path):
        logger.debug(f"Startup: [1/5] {language_code} translation loaded")
    else:
        # Try loading a more general translation if specific one fails
        general_language_code = language_code.split('_')[0]
        path = f":/translations/translations/qm/{general_language_code}.qm"
        if translator.load(path):
            logger.debug(f"{general_language_code} translation loaded as fallback")
        else:
            logger.debug(f"Failed to load {language_code} translation")

    app.installTranslator(translator)
    w = PornFetch()  # This actually starts Porn Fetch
    w.show()  # This shows the main widget
    """
    The following exceptions are just general exceptions to handle some basic errors. They are not so relevant for
    most cases.
    """

    sys.exit(app.exec())


if __name__ == "__main__":
    """
    These functions are static functions which I won't need while coding.
    These just exist for some reason, but I don't want to scroll through endless lines of code,
    which is why I placed them here.
    """
    def switch_stop_state_2():
        global stop_flag
        stop_flag = Event()


    def switch_stop_state():
        stop_flag.set()
        time.sleep(1)
        switch_stop_state_2()


    def export_urls():
        if not len(session_urls) == 0:
            file, type_ = QFileDialog().getSaveFileName()
            with open(file, "w") as url_export_file:
                for url in session_urls:
                    url_export_file.write(f"{url}\n")

            ui_popup(QCoreApplication.translate("main", f"Success! Saved: {len(session_urls)} URLs", disambiguation=None))

        else:
            ui_popup(QCoreApplication.translate("main", "No URLs in the current session...", None))


    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="Shows the version information", action="store_true")
    parser.add_argument("-p", "--portable", help="Forces a portable run of Porn Fetch (skips install dialog)", action="store_true")
    args = parser.parse_args()
    main(args)

# EOF
