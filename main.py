"""
Copyright (C) 2023-2025 Johannes Habel

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
import webbrowser

if sys.platform == "darwin":
    from src.backend.macos_setup import macos_setup
    macos_setup()

try:
    from av import open as av_open  # Don't ask
    from av.audio.resampler import AudioResampler  # Don't ask
    FORCE_DISABLE_AV = False

except Exception:
    FORCE_DISABLE_AV = True


import time
import os.path
import logging
import pathlib
import argparse
import markdown
import truststore
import src.frontend.UI.resources
import src.backend.shared_functions as shared_functions

from io import TextIOWrapper
from threading import Event, Lock
from itertools import islice, chain
from src.backend.shared_gui import *
from src.frontend.UI.ssl_warning import *
from src.frontend.UI.ui_form_main_window import Ui_MainWindow
from src.frontend.UI.theme import *
from src.backend.config import __version__, __build__
from src.frontend.UI.pornfetch_info_dialog import PornFetchInfoWidget
from src.backend.check_license import LicenseManager
from src.frontend.UI.license import License, Disclaimer
from src.backend.config import shared_config
from src.backend.shared_functions import *

from hqporner_api.api import Sort as hq_Sort
from pathlib import Path

from PySide6.QtCore import (QFile, QTextStream, QRunnable, QThreadPool, QSemaphore, Qt, QLocale,
                            QTranslator, QCoreApplication, QSize, QEvent, QRectF, QByteArray, QStandardPaths,
                            QDir, QIODevice, QFileDevice, QSettings, QSaveFile)
from PySide6.QtWidgets import (QApplication, QTreeWidgetItem, QButtonGroup, QFileDialog, QHeaderView, \
                               QInputDialog, QMainWindow, QLabel, QProgressBar, QGraphicsPixmapItem, QDialog, QVBoxLayout,
                               QGraphicsScene, QGraphicsView, QComboBox)
from PySide6.QtGui import QIcon, QFontDatabase, QPixmap, QShortcut, QKeySequence, QPainter

# Possible errors from APIs
from base_api.modules.errors import ProxySSLError, InvalidProxy
from xnxx_api.modules.errors import InvalidResponse
from hqporner_api.modules.errors import (InvalidActress as InvalidActress_HQ, NoVideosFound,
                                         NotAvailable as NotAvailable_HQ, WeirdError as WeirdError_HQ)
from xvideos_api.modules.errors import (VideoUnavailable as VideoUnavailable_XV)
from eporner_api.modules.errors import NotAvailable as NotAvailable_EP, VideoDisabled as VideoDisabled_EP
from youporn_api.modules.errors import VideoUnavailable as VideoUnavailable_YP, RegionBlocked as RegionBlocked_YP
from phub.errors import VideoError as VideoError_PH
from eporner_api.modules.locals import Category as ep_Category
from typing import Callable

truststore.inject_into_ssl() # Uses System CAs instead of ceritfi's cacert.pem

FORCE_PORTABLE_RUN = False
total_segments = 0
downloaded_segments = 0
total_downloaded_videos = 0  # All videos that actually successfully downloaded
total_downloaded_videos_attempt = 0  # All videos the user tries to download
session_urls = []  # This list saves all URls used in the current session. Used for the URL export function
conf = shared_config
core_conf = shared_functions.config
stop_flag = Event()
_download_lock = Lock()
video_data = VideoData()
settings: QSettings = QSettings()
logger = shared_functions.setup_logger("Porn Fetch - [MAIN]", log_file="PornFetch.log", level=logging.DEBUG, http_ip=shared_functions.http_log_ip,
                      http_port=shared_functions.http_log_port)


PUBLIC_KEY_B64 = 'zGUmG8Z5InvoYIwnIokQi+SysjEodvfP8kLoCur3KjM=' # This is the public key lol
license_storage_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation), "pornfetch.license")


def _mkpath(path: str) -> None:
    if not path:
        raise RuntimeError("Got empty path from QStandardPaths.")
    if not QDir().mkpath(path):
        raise RuntimeError(f"Failed to create directory: {path}")


def _move_or_copy(src: str, dst: str) -> None:
    # Prefer atomic-ish rename, but fall back to copy+remove (cross-device, etc.)
    if QFile.exists(dst):
        QFile.remove(dst)

    if QFile.rename(src, dst):
        return

    if not QFile.copy(src, dst):
        raise RuntimeError(f"Could not move/copy '{src}' -> '{dst}'")

    # Only remove original after successful copy
    QFile.remove(src)


def _write_text_atomic(path: str, text: str) -> None:
    f = QSaveFile(path)
    if not f.open(QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Text):
        raise RuntimeError(f"Could not open for writing: {path}")
    f.write(text.encode("utf-8"))
    if not f.commit():
        raise RuntimeError(f"Could not commit: {path}")


def _chmod_755(path: str) -> None:
    perms = (
        QFileDevice.Permission.ReadOwner | QFileDevice.Permission.WriteOwner | QFileDevice.Permission.ExeOwner |
        QFileDevice.Permission.ReadGroup | QFileDevice.Permission.ExeGroup |
        QFileDevice.Permission.ReadOther | QFileDevice.Permission.ExeOther
    )
    QFile.setPermissions(path, perms)


def _default_license_path() -> Path:
    cfg = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation)
    return Path(cfg) / "porn_fetch.license"


def make_settings(portable: bool, portable_dir: str | None = None) -> QSettings:
    """
    One clean place to decide where settings go.
    - Portable: INI next to the portable app folder
    - Installed: native backend (registry/plist/ini in standard locations) OR INI in AppConfigLocation
    """
    if portable:
        if not portable_dir:
            portable_dir = os.getcwd()
        ini_path = os.path.join(portable_dir, "config.ini")
        return QSettings(ini_path, QSettings.Format.IniFormat)

    # Installed:
    return QSettings()  # uses org/app + platform standard location/backend


def get_settings(*, portable: bool, portable_dir: str | None = None) -> QSettings:
    """
    Portable  -> ./config.ini (next to app / CWD or portable_dir)
    Installed -> config.ini in AppConfigLocation (per-user standard location)
    """
    QSettings.setDefaultFormat(QSettings.Format.IniFormat)

    if portable:
        base = portable_dir or os.getcwd()
        return QSettings(os.path.join(base, "config.ini"), QSettings.Format.IniFormat)

    cfg_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation)
    QDir().mkpath(cfg_dir)
    return QSettings(os.path.join(cfg_dir, "config.ini"), QSettings.Format.IniFormat)


class LicenseWidget(QWidget):
    def __init__(self, setup_restrictions: Callable, parent=None):
        super().__init__(parent)
        self.setup_restrictions = setup_restrictions

        self.lic = LicenseManager(
            public_key_b64=PUBLIC_KEY_B64,
            storage_path=_default_license_path(),
            expected_product="porn-fetch",
        )

        self.status = QLabel()
        self.btn_import = QPushButton("Import license…")
        self.btn_import.clicked.connect(self.import_license)

        layout = QVBoxLayout(self)
        layout.addWidget(self.status)
        layout.addWidget(self.btn_import)

        self.refresh_status()

    def refresh_status(self):
        res = self.lic.load_installed()
        self.status.setText(f"License status: {'✅ Valid' if res.valid else '❌ Not valid'}\n{res.reason}")
        self.setup_restrictions()

    def import_license(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select license file", "", "License (*.license);;All files (*)")
        if not path:
            return
        res = self.lic.install_from_file(Path(path))
        QMessageBox.information(self, "License", res.reason)
        self.refresh_status()


class InstallThread(QRunnable):
    def __init__(self, app_name: str, app_id: str = "pornfetch", org_name: str = "EchterAlsFake"):
        super().__init__()
        global settings
        settings = get_settings(portable=False) # At the first run, I assume the user goes for a portable install-type, however if the installation is called we need to switch that behaviour

        self.app_name = app_name
        self.app_id = app_id  # used for desktop file name, etc.
        self.org_name = org_name
        self.signals = Signals()

        # keep your logger setup if you want; using basic logging here
        self.logger = logging.getLogger("InstallThread")

    def run(self):
        try:
            self.signals.start_undefined_range.emit()

            # These matter for QSettings() “installed” mode:
            QCoreApplication.setOrganizationName(self.org_name)
            QCoreApplication.setApplicationName(self.app_name)

            if sys.platform.startswith("linux"):
                self._install_linux_user()
            elif sys.platform == "win32":
                self._install_windows_user()
            else:
                raise RuntimeError(f"Unsupported platform: {sys.platform}")

        except Exception:
            error = traceback.format_exc()
            self.logger.error(error)
            self.signals.install_finished.emit([False, error])
            self.signals.stop_undefined_range.emit()
            return

        self.signals.stop_undefined_range.emit()
        self.signals.install_finished.emit([True, ""])

    # ----------------------------
    # Linux (user-local install)
    # ----------------------------
    def _install_linux_user(self):
        filename = "PornFetch_Linux_GUI_x64.bin"

        # Install “payload” (binary + assets) into local app data:
        install_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)
        _mkpath(install_dir)


        apps_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ApplicationsLocation)
        if not apps_dir:
            # Rare, but some environments can return empty; keep a safe fallback.
            apps_dir = os.path.expanduser("~/.local/share/applications")
        _mkpath(apps_dir)

        src_exe = QCoreApplication.applicationFilePath()
        dst_exe = os.path.join(install_dir, filename)
        _move_or_copy(src_exe, dst_exe)
        _chmod_755(dst_exe)

        icon_dst = os.path.join(install_dir, "logo.png")
        if not QFile.exists(icon_dst):
            QFile.copy(":/images/graphics/logo.png", icon_dst)

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
        _write_text_atomic(desktop_path, entry)

        # Store “installed” flag using Qt settings
        settings = make_settings(portable=False)
        settings.setValue("Misc/install_type", "installed")
        settings.sync()

        self.logger.info(f"Installed to {install_dir}, desktop entry {desktop_path}")

    # ----------------------------
    # Windows (user-local install)
    # ----------------------------
    def _install_windows_user(self):
        import win32com.client  # pywin32

        filename = "PornFetch_Windows_GUI_x64.exe"

        if os.path.exists("PornFetch_Windows_GUI_arm64.bin"):
            filename = "PornFetch_Windows_GUI_arm64.bin"

        install_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)
        _mkpath(install_dir)

        src_exe = filename
        if not os.path.exists(src_exe):
            raise RuntimeError(f"Missing installer payload: {src_exe}")

        dst_exe = os.path.join(install_dir, filename)
        _move_or_copy(src_exe, dst_exe)

        # Settings flag
        settings = make_settings(portable=False)
        settings.setValue("Misc/install_type", "installed")
        settings.sync()

        # Start Menu Programs folder via Qt
        start_menu_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ApplicationsLocation)
        if not start_menu_dir:
            # Fallback (usually not needed)
            start_menu_dir = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs")
        _mkpath(start_menu_dir)

        shortcut_path = os.path.join(start_menu_dir, f"{self.app_name}.lnk")

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = dst_exe
        shortcut.WorkingDirectory = install_dir
        shortcut.IconLocation = dst_exe
        shortcut.Save()

        self.logger.info(f"Installed to {install_dir}, shortcut {shortcut_path}")


class InternetCheck(QRunnable):
    def __init__(self):
        super(InternetCheck, self).__init__()
        self.websites = [
            "https://www.pornhub.com",
            "https://www.hqporner.com",
            "https://www.xvideos.com",
            "https://www.xnxx.com",
            "https://www.missav.ws",
            "https://www.xhamster.com",
            "https://www.spankbang.com",
            "https://www.youporn.com",
            "https://www.beeg.com",
            "https://www.porntrex.com",
            "https://www.xfreehd.com"
            # Append new URLs here
        ]

        self.website_results = {}
        self.signals = Signals()
        self.logger = shared_functions.setup_logger(name="Porn Fetch - [InternetCheck]", log_file="PornFetch.log", level=logging.DEBUG,
                                   http_ip=shared_functions.http_log_ip, http_port=shared_functions.http_log_port)

    def run(self):
        for idx, website in enumerate(self.websites, start=1):
            try:
                ref = shared_functions.origin(website)

                # DUMMY FIX: rebuild session with per-site headers
                shared_functions.core_internet_checks.initialize_session(headers={
                    "Referer": ref,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/139.0.0.0 Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                })

                # Try HEAD first (lighter); some sites disallow HEAD -> fallback to GET
                resp = shared_functions.core_internet_checks.session.head(website, timeout=10)
                if resp.status_code in (405, 501):  # method not allowed / not implemented
                    resp = shared_functions.core_internet_checks.session.get(website, timeout=10)

                if resp.status_code == 200:
                    self.logger.debug(f"Internet Check: {website} : OK")
                    self.website_results[website] = "OK"
                elif resp.status_code == 404 and website != "https://www.missav.ws":
                    self.website_results[website] = "Failed, website doesn't exist? Please report this error"

            except Exception:
                # swallow per your current behavior
                pass

        self.signals.internet_check.emit(self.website_results)


class CheckUpdates(QRunnable):
    def __init__(self):
        super(CheckUpdates, self).__init__()
        self.signals = Signals()
        self.logger = shared_functions.setup_logger(name="Porn Fetch - [CheckUpdates]", log_file="PornFetch.log", level=logging.DEBUG,
                                   http_port=shared_functions.http_log_port, http_ip=shared_functions.http_log_ip)

    def run(self):
        url = f"https://echteralsfake.me/update"

        try:
            response = shared_functions.core_update_checks.fetch(url=url, get_response=True)
            if response.status_code == 200:
                json_stuff = response.json()
                if float(json_stuff["version"]) > float(__version__):
                    self.logger.info(f"A new update is available -->: {json_stuff['version']}")
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
        self.logger = shared_functions.setup_logger(name="Porn Fetch - [AddToTreeWidget]", log_file="PornFetch.log", level=logging.DEBUG,
                                   http_port=shared_functions.http_log_port, http_ip=shared_functions.http_log_ip)

    def process_video(self, video, index):
        if not isinstance(video, str):
            self.logger.debug(f"Requesting video processing of: {video.url}")

        else:
            self.logger.debug(f"Requesting video processing of: {video}")

        for attempt in range(0, 5):
            try:
                video_identifier = random.randint(0, 99999999) # Creates a random ID for each video
                if isinstance(video, str):
                    video = shared_functions.check_video(url=video)

                self.logger.debug(f"Created ID: {video_identifier} for: {video.url}")
                data = shared_functions.load_video_attributes(video)
                self.logger.debug("Loaded video attributes")
                session_urls.append(video.url)
                title = data.get("title")
                video_id = data.get("video_id")
                stripped_title_1 = shared_functions.core.strip_title(title) # Clears special characters
                stripped_title_2 = shared_functions.core.strip_title(title)

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
                return video_identifier

            except (shared_functions.errors.PremiumVideo, IndexError):
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"Premium-only video skipped: {video.url}")
                return False

            except shared_functions.errors.RegionBlocked:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"Region-blocked video skipped: {video.url}")
                return False

            except shared_functions.errors.VideoDisabled:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"Warning: The video {video.url} is disabled. It will be skipped")

            except shared_functions.errors.RegexError:
                message = f"""
                A regex error occurred. This is always a 50/50 chance if it's my or PornHub's fault. If this happens again on
                the same video, please consider reporting it. If you have logging enabled, this issue will automatically be reported.
                
                Current Index: {index}
                Additional Info: URL: {video.url}
                """
                self.logger.error("Regex error occurred, sleeping one second...")
                time.sleep(1)

                if attempt == 4:
                    self.logger.info("Nevermind, didn't work lmao")
                    handle_error_gracefully(self, data=video_data.consistent_data, error_message=message, needs_network_log=True)
                    return False

            except shared_functions.errors.VideoPendingReview:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"Warning: The video {video.url} is pending review. It will be skipped")
                return False

            except InvalidResponse:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"Warning: The video: {video.url} returned an empty response when trying"
                                             f"to fetch its content. There is nothing I can do. It will be skipped")
                return False

            except NotAvailable_HQ:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"The video: {video.url} is not available, because the CDN network has an issue. "
                                              f"This is not my fault, please do NOT report this error, thank you :)")
                return False


            except WeirdError_HQ:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"An error happened with: {video.url} this is a weird error i have no fix for yet,"
                                              f" however this will be reported, to help me fixing it :) ", needs_network_log=True)
                return False

            except VideoUnavailable_XV:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message= f"The video {video.url} is not available. Do not report this error... Not my fault :)")
                return False

            except NotAvailable_EP:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"The video: {video.url} is not available on HQPorner. This is not my fault, skipping...")
                return False

            except VideoDisabled_EP:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"The video: {video.url} has been disabled by EPorner itself. It will be skippled...")
                return False

            except VideoError_PH:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"The video: {video.url} has an error. However, in this case it's PornHub's fault. It will be skipped!")
                return False

            except RegionBlocked_YP:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"The video: {video.url} is region locked. It will be skipped...")

            except VideoUnavailable_YP:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"The video: {video.url} is unavailable on YouPorn. It will be skipped...")

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


class DownloadThread(QRunnable):
    """Refactored threading class to download videos with improved performance and logic."""
    def __init__(self, video, video_id):
        super().__init__()
        self.video = video
        self.video_id = video_id
        self.consistent_data = video_data.consistent_data
        self.quality = self.consistent_data.get("quality")
        data_object: dict = video_data.data_objects[self.video_id]
        self.output_path = data_object.get("output_path")
        self.logger = shared_functions.setup_logger(name="Porn Fetch - [DownloadThread]", log_file="PornFetch.log", level=logging.DEBUG,
                                   http_ip=shared_functions.http_log_ip, http_port=shared_functions.http_log_port)

        self.download_mode = self.consistent_data.get("download_mode")
        self.signals = Signals()
        self.stop_flag = stop_flag
        self.skip_existing_files = self.consistent_data.get("skip_existing_files")
        self.video_progress = {}
        self.last_update_time = 0
        self._range_emitted = False

    def callback_remux(self, pos, total):
        self.signals.progress_video_converting.emit(pos, total)

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

    def run(self):
        """Run the download in a thread, optimizing for different video sources and modes."""
        try:
            if os.path.isfile(self.output_path):
                if self.skip_existing_files:
                    self.logger.debug("The file already exists, skipping...")
                    self.signals.download_completed.emit(True)
                    return

                else:
                    self.logger.debug("The file already exists, appending random number...")
                    path = str(self.output_path).split(".")
                    path = path[0] + str(random.randint(0, 1000)) + ".mp4"
                    self.output_path = path

            if int(self.consistent_data.get("processing_delay")) != 0:
                time.sleep(int(self.consistent_data.get("processing_delay")))
            self.logger.debug(f"Downloading Video to: {self.output_path}")
            self.signals.total_progress_range.emit(total_segments)
            global FORCE_DISABLE_AV
            if not FORCE_DISABLE_AV:
                remux = True

            else:
                remux = False


            # We need to specify the sources, so that it knows which individual progressbar to use
            instances_legacy = [shared_functions.hq_Video, shared_functions.ep_Video, shared_functions.pt_Video,
                                shared_functions.xf_Video]

            if isinstance(self.video, tuple(instances_legacy)):
                video_source = "raw"
                try:
                    self.logger.debug("Starting the Download!")
                    self.video.download(quality=self.quality, path=self.output_path, no_title=True,
                                    callback=lambda pos, total: self.generic_callback(pos, total, video_source))

                except Exception:
                    error = traceback.format_exc()
                    handle_error_gracefully(data=self.consistent_data, self=self, error_message=f"An error happened while downloading a video from HQPorner / EPorner: {error}", needs_network_log=True)

            elif isinstance(self.video, shared_functions.ph_Video):  # Assuming 'Video' is the class for Pornhub
                video_source = "general"
                self.logger.debug("Starting the Download!")
                self.video.download(downloader=str(self.download_mode), path=self.output_path,
                                    quality=self.quality, remux=remux, display_remux=self.callback_remux,
                                    display=lambda pos, total: self.generic_callback(pos, total),
                                    )

            else:
                self.video.download(downloader=str(self.download_mode), path=self.output_path, callback_remux=self.callback_remux, no_title=True,
                                    quality=self.quality, remux=remux, callback=lambda pos, total: self.generic_callback(pos, total))

        except Exception:
            error = traceback.format_exc()
            error = f"An error occurred when trying to download video: {error}. This will be reported!"
            handle_error_gracefully(self, data=video_data.consistent_data, error_message=error, needs_network_log=True)

        finally:
            if self.consistent_data.get("write_metadata"):
                try:
                    if not FORCE_DISABLE_AV:
                        shared_functions.write_tags(path=self.output_path, data=video_data.data_objects.get(self.video_id))

                except Exception:
                    error = traceback.format_exc()
                    error = f"An error occurred when trying to write metadata: {error}. This will be reported!"
                    handle_error_gracefully(self, data=video_data.consistent_data, error_message=error, needs_network_log=True)

            self.signals.download_completed.emit(self.video_id)


class QTreeWidgetDownloadThread(QRunnable):
    """Threading class for the QTreeWidget (sends objects to the download class defined above)"""

    def __init__(self, tree_widget, semaphore):
        super(QTreeWidgetDownloadThread, self).__init__()
        self.treeWidget = tree_widget
        self.signals = Signals()
        self.consistent_data = video_data.consistent_data
        self.download_mode = self.consistent_data.get("download_mode")
        self.quality = self.consistent_data.get("quality")
        self.semaphore = semaphore
        self.logger = shared_functions.setup_logger(name="Porn Fetch - [QTreeWidgetDownloadThread]", log_file="PornFetch.log",
                                   level=logging.DEBUG, http_ip=shared_functions.http_log_ip, http_port=shared_functions.http_log_port)

    def run(self):
        self.signals.start_undefined_range.emit()
        video_objects = []
        data_objects = []
        global total_segments, downloaded_segments

        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)
            check_state = item.checkState(0)
            if check_state == Qt.CheckState.Checked:
                video_objects.append(item.data(0, Qt.ItemDataRole.UserRole))
                data_objects.append(item.data(1, Qt.ItemDataRole.UserRole))


        self.logger.debug("Retrieving total length of video segments to calculate total progress...")

        video_objects_with_hls = []
        for video in video_objects:
            if hasattr(video, "get_segments"):
                video_objects_with_hls.append(video)

        self.signals.total_progress_range.emit(len(video_objects_with_hls))
        for idx, video in enumerate(video_objects_with_hls):
            total_segments += len(video.get_segments(quality=self.quality))
            self.signals.total_progress.emit(idx)

        self.logger.debug(f"Got {total_segments} segments...")
        # This basically looks how many segments exist in all videos together, so that we can calculate the total
        # progress

        downloaded_segments = 0
        self.signals.stop_undefined_range.emit()

        for idx, video in enumerate(video_objects):
            self.semaphore.acquire()  # Trying to start the download if the thread isn't locked
            self.logger.debug("Semaphore Acquired")
            self.signals.progress_send_video.emit(video, data_objects[
                idx])  # Now emits the video to the main class for further processing


class PornFetch(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_update_time = time.time()
        self.last_thumbnail_change = time.time()
        self.signals = Signals()
        self.signals.error_signal.connect(ui_popup)

        global settings
        settings = get_settings(portable=True, portable_dir=os.getcwd())

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.logger = shared_functions.setup_logger(name="Porn Fetch - [PornFetch]", log_file="PornFetch.log", level=logging.DEBUG,
                                   http_ip=shared_functions.http_log_ip, http_port=shared_functions.http_log_port)

        self.last_index = 0  # Keeps track of the last index of videos added to the tree widget
        self.kill_switch = False
        self.threadpool = QThreadPool()
        self.maps()
        self.load_style()
        self.license = License(self.ui, self.initialize_pornfetch)
        self.disclaimer = Disclaimer(self.ui, self.initialize_pornfetch)
        self.ui.vbox_info.addWidget(PornFetchInfoWidget())
        self.license_manager = LicenseManager(storage_path=_default_license_path(), public_key_b64=PUBLIC_KEY_B64)
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
        self.progress_widgets = {}  # video_id -> {'label': QLabel, 'progressbar': QProgressBar}

        if video_data.consistent_data.get("internet_checks"):
            self.logger.info("Running internet checks")
            self.check_internet()

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

    def switch_to_batch(self):
        self.ui.CentralStackedWidget.setCurrentIndex(10)

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

    def switch_to_progressbars(self):
        self.ui.main_stacked_widget_top.setCurrentIndex(3)
        self.switch_to_main()

    def switch_to_range_selector(self):
        self.ui.main_stacked_widget_top.setCurrentIndex(4)
        self.switch_to_main()

    def load_style(self):
        #self.ui.CentralStackedWidget.insertWidget(12, Batch())
        icons = {
            self.ui.main_button_switch_home: "download.svg",
            self.ui.main_button_switch_settings: "settings.svg",
            self.ui.main_button_switch_credits: "information.svg",
            self.ui.main_button_switch_account: "account.svg",
            self.ui.main_button_switch_tools: "tools.svg",
            self.ui.main_button_view_progress_bars: "progressbars.svg",
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
            #self.ui.main_button_switch_batch, (Not implemented yet)
            self.ui.main_button_view_progress_bars,
        ]
        group_menu_bar = QButtonGroup(self)
        group_menu_bar.setExclusive(True)
        for b in nav:
            b.setCheckable(True)
            group_menu_bar.addButton(b)
            mark(b, seg=True)  # <- gives the segmented style
        self.ui.main_button_switch_home.setChecked(True)

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
        mark(self.ui.main_button_tree_download, intent="primary")
        mark(self.ui.login_button_login, intent="primary")
        mark(self.ui.settings_button_apply, intent="primary")

        mark(self.ui.main_button_tree_stop, intent="danger")
        mark(self.ui.settings_button_reset, intent="danger")

        mark(self.ui.main_progressbar_total, role="total")
        mark(self.ui.main_progressbar_converting, role="convert")

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
        mark(self.ui.main_progressbar_converting, role="convert")

        # --- tree header sizing / behavior ---
        hdr = self.ui.treeWidget.header()
        hdr.setStretchLastSection(False)
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Title
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Author
        hdr.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Length
        hdr.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # Actions/Status
        self.ui.treeWidget.setColumnWidth(3, 150)
        self.ui.treeWidget.setAlternatingRowColors(True)

        # --- misc you already had ---
        self.ui.treeWidget.sortByColumn(2, Qt.SortOrder.AscendingOrder)
        self.ui.progress_gridlayout_progressbar.setAlignment(Qt.AlignmentFlag.AlignTop)

        if __build__ == "desktop":
            gv = self.ui.graphicsView
            gv.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            gv.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            gv.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self._scene = QGraphicsScene(self)
            gv.setScene(self._scene)
            self._pixmap_item = QGraphicsPixmapItem()
            self._scene.addItem(self._pixmap_item)
            self._full_pixmap = QPixmap()
            gv.installEventFilter(self)
            gv.viewport().installEventFilter(self)

        self.header = self.ui.treeWidget.header()
        self.header.resizeSection(0, 300)
        self.header.resizeSection(1, 150)
        self.header.resizeSection(2, 50)
        self.header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.ui.treeWidget.setColumnWidth(3, 150)
        self.ui.treeWidget.itemClicked.connect(self.set_thumbnail)
        self.ui.treeWidget.currentItemChanged.connect(self.set_thumbnail)
        self.setWindowTitle(f"Porn Fetch v{__version__} Copyright (C) Johannes Habel 2023-2025")
        self.ui.treeWidget.sortByColumn(2, Qt.SortOrder.AscendingOrder)
        self.ui.progress_gridlayout_progressbar.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.ui.settings_stacked_widget_main.setCurrentIndex(0)

        install_focus_outline(self)

        stylesheet_license_buttons = QFile(":/style/UI/stylesheet_license_button.qss")
        stylesheet_license_buttons.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text)
        stream = QTextStream(stylesheet_license_buttons)
        style = stream.readAll()

        self.ui.settings_button_buy_license.setProperty("variant", "primary")
        self.ui.settings_button_buy_license.setStyleSheet(style)

        self.ui.settings_button_import_license.setProperty("variant", "danger")
        self.ui.settings_button_import_license.setStyleSheet(style)

        self.switch_to_download()

    def install_pornfetch(self):
        app_name = self.ui.lineedit_custom_app_name.text() or self.ui.settings_lineedit_system_custom_app_name.text()
        if app_name == "" or app_name is None:
            self.logger.info("You did not provide a custom App name. Using 'Porn Fetch' for the installation.")
            app_name = "Porn Fetch"

        self.install_thread = InstallThread(app_name=app_name)
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
        self.ui.main_textbrowser_supported_websites.setText(
            "Running in anonymous mode, please deactivate to display...")
        self.ui.download_lineedit_playlist_url.setPlaceholderText("Enter playlist URL")
        self._anonymous_mode = True  # Makes sense, trust
        self.logger.info("Enabled anonymous mode!")

    def button_connections(self):
        """a function to link the buttons to their functions"""
        # Menu Bar Switch Button Connections
        self.ui.main_button_switch_home.clicked.connect(self.switch_to_download)
        self.ui.main_button_switch_settings.clicked.connect(self.switch_to_settings)
        self.ui.main_button_switch_credits.clicked.connect(self.switch_to_credits)
        self.ui.main_button_switch_account.clicked.connect(self.switch_to_login)
        self.ui.main_button_switch_supported_websites.clicked.connect(self.switch_to_supported_sites)
        self.ui.main_button_view_progress_bars.clicked.connect(self.switch_to_progressbars)
        #self.ui.main_button_switch_batch.clicked.connect(self.switch_to_batch) (Not implemented yet)

        # Video Download Button Connections
        self.ui.main_button_tree_download.clicked.connect(self.download_tree_widget)
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
        self.ui.main_button_tree_automated_selection.clicked.connect(self.select_range_of_items)
        self.ui.settings_checkbox_system_proxy_kill_switch.toggled.connect(self.toggle_killswitch)

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

        download_tree_widget = QShortcut(QKeySequence("Ctrl+T"), self)
        download_tree_widget.activated.connect(self.download_tree_widget)

        enable_anonymous_mode = QShortcut(QKeySequence("Ctrl+A"), self)
        enable_anonymous_mode.activated.connect(self.anonymous_mode)

        save_settings = QShortcut(QKeySequence("Ctrl+S"), self)
        save_settings.activated.connect(self.save_user_settings)

        select_all_items = QShortcut(QKeySequence("Ctrl+X"), self)
        select_all_items.activated.connect(self.select_all_items)

        unselect_all_items = QShortcut(QKeySequence("Ctrl+Z"), self)
        unselect_all_items.activated.connect(self.unselect_all_items)

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
        self.mappings_download_mode = {
            0: "threaded",
            1: "ffmpeg",
            2: "default"
        }

    def load_user_settings(self):
        settings.sync()
        # --- Video ---
        _quality = settings.value("Video/quality", 0, int)
        if _quality <= 5 and not self.license_manager.has_feature("full_unlock"):
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
        _download_mode = settings.value("Performance/download_mode", 0, int)
        video_data.consistent_data.update({"download_mode": self.mappings_download_mode.get(_download_mode)})
        self.ui.settings_performance_combobox_download_mode.setCurrentIndex(_download_mode)

        simultaneous_downloads = settings.value("Performance/semaphore", 2, int)

        if int(simultaneous_downloads) > 1 and not self.license_manager.has_feature("full_unlock"):
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

        internet_checks = settings.value("Misc/internet_checks", True, bool)
        video_data.consistent_data.update({"internet_checks": internet_checks})
        self.ui.settings_checkbox_system_internet_checks.setChecked(internet_checks)

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

        # --- UI ---
        ui_language_idx = settings.value("UI/language", 0, int)
        self.ui.settings_ui_combobox_language.setCurrentIndex(ui_language_idx)

        font_size = settings.value("UI/font_size", 10, int)
        self.ui.settings_spinbox_ui_font_size.setValue(font_size)

        ui_theme_idx = settings.value("UI/theme", 0, int)
        self.ui.settings_combobox_ui_theme.setCurrentIndex(ui_theme_idx)

        # Apply to your core_conf
        core_conf.timeout = timeout
        core_conf.max_retries = retries
        core_conf.max_bandwidth_mb = speed_limit
        core_conf.raise_bot_protection = False
        core_conf.request_delay = network_delay
        core_conf.videos_concurrency = videos_concurrency
        core_conf.pages_concurrency = pages_concurrency
        core_conf.max_workers_download = download_workers

        shared_functions.refresh_clients()
        shared_functions.enable_logging()

    def save_user_settings(self):
        print(f"In settings....")
        print(id(settings))
        print(settings.fileName())

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
        settings.setValue("download_mode", self.ui.settings_performance_combobox_download_mode.currentIndex())
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
        settings.setValue("internet_checks", self.ui.settings_checkbox_system_internet_checks.isChecked())
        settings.setValue("anonymous_mode", self.ui.settings_checkbox_system_enable_anonymous_mode.isChecked())
        settings.setValue("supress_errors", self.ui.settings_checkbox_system_supress_errors.isChecked())
        settings.setValue("network_logging", self.ui.settings_checkbox_system_enable_network_logging.isChecked())
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
            ip = shared_functions.core.fetch(url="https://httpbin.org/ip", get_response=True).json()["origin"]
            self.logger.info("Applying Proxy to all session objects...")
            shared_functions.config.proxy = proxy_input
            shared_functions.refresh_clients()
            self.logger.info(f"Unmasked IP is -->: {ip}")
            try:
                ip_masked = shared_functions.core.fetch(url="https://httpbin.org/ip", get_response=True).json()["origin"]

            except ProxySSLError:
                dialog = SSLWarningDialog()
                if dialog.exec():
                    self.logger.warning("Disabling SSL Verification")
                    shared_functions.config.verify_ssl = False
                    shared_functions.refresh_clients()
                    ip_masked = shared_functions.core.fetch(url="https://httpbin.org/ip", get_response=True).json()[
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
            shared_functions.refresh_clients(enable_kill_switch=False)
            return None

        else:
            if self.proxy is None:
                ui_popup(self.tr("Can not enable Kill Switch if you haven't applied a proxy yet!", disambiguation=None))
                self.ui.settings_checkbox_system_proxy_kill_switch.setChecked(False)
                return None

            self.logger.info(f"Enabling Kill Switch for -->: {self.proxy}")
            shared_functions.refresh_clients(enable_kill_switch=True)
            return None

    """
    These are the core functions of Porn Fetch outside of the UI stuff. They are used to process user input.
    """

    def initialize_pornfetch(self):
        """
        After all stylesheets and icons are loaded, this function will initiate the process for checking
        if the License was shown and accepted, if the disclaimer text was shown, if the user downloaded the amount
        of videos to show the sponsoring dialog and after all that switch to the main widget.
        """

        print(id(settings))
        print(settings.fileName())

        global FORCE_PORTABLE_RUN
        settings.sync()
        if not self.license.check_license():
            self.switch_to_license()
            return

        if not self.disclaimer.check_disclaimer():
            self.switch_to_disclaimer()
            return

        v = settings.value("Misc/first_run_gui")
        print(v, type(v))

        first = settings.value("Misc/first_run_gui", True, type=bool)
        if first:
            print(f"It's true lol ")
            settings.setValue("Misc/first_run_gui", False)
            settings.sync()
            self.switch_to_one_time_setup()
            return

        if not FORCE_PORTABLE_RUN:
            if sys.platform == "darwin":
                self.ui.CentralStackedWidget.setCurrentIndex(0)
                return

            if settings.value("Misc/install_type") == "unknown":
                self.switch_to_install_dialog()
                return

        self.ui.CentralStackedWidget.setCurrentIndex(0)

    def start_single_video(self):
        """
        Starts the download of a single video.
        This still uses the tree widget because this makes it easier to track the total progress, as I've already
        implemented this feature into the tree widget and I don't want to write code 2 times
        """
        url = self.ui.download_lineedit_url.text()
        self.logger.info(f"Starting a single shot download for -->: {url}")
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
            model_object = shared_functions.ph_client.get_user(model)
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
                videos = shared_functions.hq_client.get_videos_by_actress(name=model)

            except InvalidActress_HQ:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message="Invalid Actress URL!")
                return

            except NoVideosFound:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message="No videos found. This is probably an error and will be reported.", needs_network_log=True)
                return

        elif "eporner" in str(model):
            videos = shared_functions.ep_client.get_pornstar(url=model, enable_html_scraping=True).videos()

        elif "xnxx" in str(model):
            videos = shared_functions.xn_client.get_user(url=model).videos

        elif "youporn" in str(model) and "channel" in model:
            videos = shared_functions.yp_client.get_channel(url=model).videos()

        elif "youporn" in str(model):
            videos = shared_functions.yp_client.get_pornstar(url=model).videos()

        elif "xvideos" in str(model) and ("model" or "pornstar") in str(model):
            videos = shared_functions.xv_client.get_pornstar(url=model).videos()

        elif "xvideos" in str(model) and "channel" in str(model):
            videos = shared_functions.xv_client.get_channel(url=model).videos()

        elif "xvideos" in str(model):
            videos = shared_functions.xv_client.get_channel(url=model).videos()

        elif "spankbang" in str(model) and "pornstar" in str(model):
            videos = shared_functions.sp_client.get_pornstar(url=model).videos()

        elif "spankbang" in str(model) and "creator" in str(model):
            videos = shared_functions.sp_client.get_creator(url=model).videos()

        elif "spankbang" in str(model) and "channel" in str(model):
            videos = shared_functions.sp_client.get_channel(url=model).videos()

        elif "xhamster" in str(model) and "pornstars" in str(model):
            videos = shared_functions.xh_client.get_pornstar(url=model).videos()

        elif "xhamster" in str(model) and "creators" in str(model):
            videos = shared_functions.xh_client.get_creator(url=model).videos()

        elif "xhamster" in str(model) and "channels" in str(model):
            videos = shared_functions.xh_client.get_channel(url=model).videos()

        elif "youporn" in str(model) and "pornstar" in str(model):
            videos = shared_functions.yp_client.get_pornstar(url=model).videos()

        elif "youporn" in str(model) and "channel" in str(model):
            videos = shared_functions.yp_client.get_channel(url=model).videos()

        elif "porntrex" in str(model) and "channel" in str(model):
            videos = shared_functions.pt_client.get_channel(url=model).videos()

        elif "porntrex" in str(model) and "model" in str(model):
            videos = shared_functions.pt_client.get_model(url=model).videos()

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
            playlist = shared_functions.ph_client.get_playlist(url)
            videos = playlist.sample()

        elif "xvideos" in url:
            videos = shared_functions.xv_client.get_playlist(url=url, pages=400)

        elif "youporn" in str(url) and "collection" in str(url):
            videos = shared_functions.yp_client.get_collection(url).videos()

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
            videos = shared_functions.hq_client.search_videos(query, pages=500)

        elif self.ui.download_website_combobox.currentIndex() == 1:
            videos = shared_functions.ph_client.search(query)

        elif self.ui.download_website_combobox.currentIndex() == 2:
            videos = shared_functions.ep_client.search_videos(query, sorting_gay="", sorting_order="",
                                                              sorting_low_quality="", page=20, per_page=200)
        elif self.ui.download_website_combobox.currentIndex() == 3:
            videos = shared_functions.xv_client.search(query, pages=500)

        elif self.ui.download_website_combobox.currentIndex() == 4:
            videos = shared_functions.xh_client.search_videos(query=query, pages=500)

        elif self.ui.download_website_combobox.currentIndex() == 5:
            videos = shared_functions.xn_client.search(query).videos(pages=500)

        elif self.ui.download_website_combobox.currentIndex() == 6:
            videos = shared_functions.sp_client.search(query=query, pages=500)

        elif self.ui.download_website_combobox.currentIndex() == 7:
            videos = shared_functions.mv_client.search(query=query, video_count=500)

        elif self.ui.download_website_combobox.currentIndex() == 8:
            videos = shared_functions.yp_client.search_videos(query=query, pages=500)

        elif self.ui.download_website_combobox.currentIndex() == 9:
            videos = shared_functions.pt_client.search(query=query, pages=500)

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
        self.add_to_tree_widget_thread_.signals.error_signal.connect(self.show_error)
        self.add_to_tree_widget_thread_.signals.clear_tree_widget_signal.connect(self.clear_tree_widget)
        self.add_to_tree_widget_thread_.signals.start_undefined_range.connect(self.start_undefined_range)
        self.add_to_tree_widget_thread_.signals.stop_undefined_range.connect(self.stop_undefined_range)
        self.add_to_tree_widget_thread_.signals.tree_widget_finished.connect(self.tree_widget_finished)
        self.add_to_tree_widget_thread_.signals.total_progress_range.connect(self.update_total_progressbar_range)
        self.add_to_tree_widget_thread_.signals.total_progress.connect(self.update_total_progressbar)
        self.threadpool.start(self.add_to_tree_widget_thread_)
        self.logger.debug("Started the thread for adding videos...")

    def add_to_tree_widget_signal(self, identifier: int):
        """
        Receives video data (by identifier) and applies it to the GUI tree widget.

        The video length is parsed using parse_length(), which now handles multiple formats:
          - "mm:ss" (e.g. "16:19")
          - Digits-only strings that are interpreted based on video source (xnxx vs. eporner/phub)
          - Decimal, mixed-unit, and other formats.

        A display string and a zero-padded sorting key are then generated.
        """
        self.logger.info(f"Applying video data for ID -->: {identifier}")
        self.last_index += 1
        data = video_data.data_objects.get(identifier)
        title = data.get("title")
        author = data.get("author")
        raw_length = data.get("length")  # Raw length from the data source.
        index = data.get("index")
        video = data.get("video")  # e.g. a URL or identifier that may contain "xnxx", "eporner", etc.
        thumbnail = data.get("thumbnail")
        thumbnail_data = data.get("thumbnail_data")

        # Parse the raw length, passing video as a hint for the source.
        parsed_length = shared_functions.parse_length(raw_length, video)

        item = QTreeWidgetItem(self.ui.treeWidget)

        # If in anonymous mode, set tooltips and redact title/author.
        if self._anonymous_mode:
            item.setToolTip(0, title)
            item.setToolTip(1, author)
            title = "[redacted]"
            author = "[redacted]"

        item.setText(0, f"{index}) {title}")
        item.setText(1, author)

        # Prepare display and sort keys for the duration.
        if parsed_length == "Not available" or parsed_length is None:
            display_duration = "Not available"
            formatted_duration = "000000000"
        else:
            # Use the parsed_length (which should be an integer representing minutes).
            display_duration = str(parsed_length)
            formatted_duration = f"{parsed_length:05d}"

        item.setCheckState(0, Qt.CheckState.Unchecked)
        item.setData(0, Qt.ItemDataRole.UserRole, video)
        item.setData(1, Qt.ItemDataRole.UserRole, identifier)
        item.setText(2, display_duration)  # What the user sees.
        item.setData(2, Qt.ItemDataRole.UserRole, formatted_duration)  # Hidden sort key.
        item.setData(3, Qt.ItemDataRole.UserRole, str(thumbnail))
        item.setData(4, Qt.ItemDataRole.UserRole, str(author))
        item.setData(5, Qt.ItemDataRole.UserRole, thumbnail_data) # Thumbnail in bytes form

    def tree_widget_finished(self):
        if self.ui.main_checkbox_direct_download.isChecked():
            self.logger.info("Automatically downloading all videos in the tree widget!")
            self.select_all_items()
            self.download_tree_widget()

        self.update_total_progressbar_range(1)
        self.update_total_progressbar(1)

    def show_error(self, message):
        ui_popup(text=message, title="Error")

    def download_tree_widget(self):
        """
        Starts the thread for downloading the tree widget (All selected videos)
        """
        tree_widget = self.ui.treeWidget
        self.download_tree_thread = QTreeWidgetDownloadThread(tree_widget=tree_widget, semaphore=self.semaphore)
        self.download_tree_thread.signals.total_progress_range.connect(self.update_total_progressbar_range)
        self.download_tree_thread.signals.total_progress.connect(self.update_total_progressbar)
        self.download_tree_thread.signals.start_undefined_range.connect(self.start_undefined_range)
        self.download_tree_thread.signals.stop_undefined_range.connect(self.stop_undefined_range)
        self.download_tree_thread.signals.progress_send_video.connect(self.process_video_thread)
        self.threadpool.start(self.download_tree_thread)

    def process_video_thread(self, video, video_id):
        """Checks which of the three types of threading the user selected and handles them."""
        self.create_video_progressbar(video_id=video_id, title=video.title)
        self.download_thread = DownloadThread(video=video, video_id=video_id)
        self.download_thread.signals.progress_video_converting.connect(self.progress_video_remuxing)
        self.download_thread.signals.progress_video.connect(self.update_video_progressbar)
        self.download_thread.signals.progress_video_range.connect(self.set_video_progress_range)
        self.download_thread.signals.total_progress_range.connect(self.update_total_progressbar_range)
        self.download_thread.signals.total_progress.connect(self.update_total_progressbar)
        self.download_thread.signals.download_completed.connect(self.download_completed)
        self.threadpool.start(self.download_thread)
        self.logger.debug("Started Download Thread!")

    def download_completed(self, video_id):
        """If a video is downloaded, the semaphore is released"""
        self.logger.debug("Download Completed!")
        global total_downloaded_videos
        total_downloaded_videos += 1
        self.ui.progress_lineedit_download_info.setText(
            f"Downloaded: {total_downloaded_videos} video(s) this session.")
        self.ui.main_progressbar_total.setMaximum(100)
        self.ui.main_progressbar_total.setValue(0)
        self.ui.main_progressbar_converting.setMaximum(100)
        self.ui.main_progressbar_converting.setValue(0)
        widgets = self.progress_widgets.pop(video_id, None)
        if widgets:
            for widget in widgets.values():
                self.ui.progress_gridlayout_progressbar.removeWidget(widget)
                widget.deleteLater()

        downloaded_videos = int(settings.value("Misc/downloaded_videos"))
        downloaded_videos += 1
        settings.setValue("Misc/downloaded_videos", str(downloaded_videos))
        settings.sync()

        if video_data.consistent_data.get("track_videos"):
            self.logger.info(f"Tracking video: {video_id}")
            shared_functions.init_db(video_data.consistent_data.get("database_path"))
            data = video_data.data_objects.get(video_id)
            shared_functions.save_video_metadata(video_id, data, video_data.consistent_data.get("database_path"))

        try:
            video_data.clean_dict(video_id)

        except KeyError:
            pass # Doesn't matter

        self.semaphore.release()

    def clear_tree_widget(self):
        """
        This (like the name says) clears the tree widget.
        """
        self.logger.debug("Cleared the tree widget")
        if not self.ui.main_checkbox_tree_do_not_clear_videos.isChecked():
            self.ui.treeWidget.clear()

    """These functions are related to selecting video items within the tree widget"""

    def unselect_all_items(self):
        """Unselects all items from the tree widget"""
        self.logger.info("Unselected all items")
        root = self.ui.treeWidget.invisibleRootItem()
        item_count = root.childCount()
        for i in range(item_count):
            item = root.child(i)
            item.setCheckState(0, Qt.CheckState.Unchecked)

    def select_range_of_items(self):
        # Create an instance of the UI form widget
        self.switch_to_range_selector()
        root = self.ui.treeWidget.invisibleRootItem()
        item_count = root.childCount()
        self.ui.spinbox_range_end.setMaximum(item_count)
        self.ui.button_range_apply_index.clicked.connect(self.process_range_of_items_selection_index)
        self.ui.button_range_apply_time.clicked.connect(self.process_range_of_items_selection_time)
        self.ui.button_range_apply_author.clicked.connect(self.process_range_of_items_author)
        self.ui.button_range_select_all.clicked.connect(self.select_all_items)
        self.ui.button_range_unselect_all.clicked.connect(self.unselect_all_items)

    def select_all_items(self):
        """Selects all items from the tree widget"""
        self.logger.info("Selected all items")
        root = self.ui.treeWidget.invisibleRootItem()
        item_count = root.childCount()
        for i in range(item_count):
            item = root.child(i)
            item.setCheckState(0, Qt.CheckState.Checked)

    def process_range_of_items_selection_index(self):
        start = self.ui.spinbox_range_start.value()
        end = self.ui.spinbox_range_end.value()
        root = self.ui.treeWidget.invisibleRootItem()

        # Adjust start and end indices to match tree widget indexing
        start -= 1
        end -= 1

        for i in range(start, end + 1):  # Adjust the range to be inclusive of the end
            item = root.child(i)
            item.setCheckState(0, Qt.CheckState.Checked)

    def process_range_of_items_selection_time(self):
        start_time = int(self.ui.lineedit_range_start.text())
        end_time = int(self.ui.lineedit_range_end.text())
        root = self.ui.treeWidget.invisibleRootItem()

        # Loop through all items in the QTreeWidget
        for i in range(root.childCount()):
            item = root.child(i)

            # Retrieve the duration from the item, assuming it's stored as an integer in UserRole
            duration = int(item.data(2, Qt.ItemDataRole.UserRole))

            # Check if the duration is within the specified start and end times
            if start_time <= duration <= end_time:
                item.setCheckState(0, Qt.CheckState.Checked)

    def process_range_of_items_author(self):
        name = str(self.ui.lineedit_range_author.text())
        root = self.ui.treeWidget.invisibleRootItem()

        for i in range(root.childCount()):
            item = root.child(i)
            author = str(item.data(4, Qt.ItemDataRole.UserRole))
            if str(author).lower() == str(name).lower():
                item.setCheckState(0, Qt.CheckState.Checked)

    def set_thumbnail(self, item_current: QTreeWidgetItem, item_previous=None): # Won's use the previous item
        """Replace your QLabel code with this, feeding the graphicsView."""

        if __build__ == "android":
            return

        if time.time() - self.last_thumbnail_change < 0.1: # Bypasses a bug where the function would be called 2 times always
            return

        data = item_current.data(5, Qt.ItemDataRole.UserRole)
        self.last_thumbnail_change = time.time()
        item = item_current

        # clear if nothing to show
        if item is None or self._anonymous_mode:
            self._pixmap_item.setPixmap(QPixmap())
            return

        pixmap = QPixmap()

        if not data:
            self._pixmap_item.setPixmap(QPixmap())
            return

        if isinstance(data, (bytes, bytearray, memoryview)):
            ok = pixmap.loadFromData(bytes(data))
        elif isinstance(data, QByteArray):
            ok = pixmap.loadFromData(data)
        elif isinstance(data, QPixmap):
            pixmap = data
            ok = True
        else:
            self.logger.warning("Unexpected thumbnail_data type: %r", type(data))
            ok = False

        if not ok:
            self.logger.warning("Failed to load pixmap from thumbnail data")
            self._pixmap_item.setPixmap(QPixmap())
            return

        self._full_pixmap = pixmap
        self._pixmap_item.setPixmap(pixmap)
        self._scene.setSceneRect(QRectF(pixmap.rect()))
        self.ui.graphicsView.fitInView(self._scene.sceneRect(),
                                       Qt.AspectRatioMode.KeepAspectRatioByExpanding)


    """
    The following functions are used to connect data between Threads and the Main UI
    """

    def create_video_progressbar(self, video_id, title):
        truncated_title = (title[:30] + '...') if len(title) > 30 else title
        label = QLabel(truncated_title)
        progressbar = QProgressBar()
        progressbar.setStyleSheet(generate_random_progressbar_qss())
        progressbar.setMaximum(100)
        progressbar.setValue(0)

        row = self.ui.progress_gridlayout_progressbar.rowCount()
        self.ui.progress_gridlayout_progressbar.addWidget(label, row, 0)
        self.ui.progress_gridlayout_progressbar.addWidget(progressbar, row, 1)

        self.progress_widgets[video_id] = {'label': label, 'progressbar': progressbar}

    def set_video_progress_range(self, video_id, maximum):
        """Called once per video to set up [0.maximum] on the bar."""
        widget_set = self.progress_widgets.get(video_id)
        if not widget_set:
            return
        bar = widget_set['progressbar']
        bar.setRange(0, maximum)
        # optional: reset to zero if you like
        bar.setValue(0)

    def progress_video_remuxing(self, pos, total):
        """Updates the progress when the video gets remuxed"""
        if time.time() - self.last_thumbnail_change < 0.3:
            return

        self.ui.main_progressbar_converting.setMaximum(total)
        self.ui.main_progressbar_converting.setValue(pos)
        self.last_update_time = time.time()

    def update_video_progressbar(self, video_id, pos, maximum):
        """Fired repeatedly—only updates the current value."""
        widget_set = self.progress_widgets.get(video_id)
        if not widget_set:
            return
        bar = widget_set['progressbar']
        bar.setValue(pos)

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
            shared_functions.ph_client = shared_functions.ph_Client(email=username, password=password, core=shared_functions.core_ph)
            self.logger.debug("Login Successful!")
            ui_popup(self.tr("Login Successful!", None))
            # TODO

        except shared_functions.errors.LoginFailed:
            self.logger.error("Login Failed, because of invalid credentials")
            ui_popup(self.tr("Login Failed, please check your credentials and try again!", None))

        except shared_functions.errors.ClientAlreadyLogged:
            self.logger.warning("Client already logged in?!! wait what??")
            ui_popup(self.tr("You are already logged in!", None))

    def check_login(self):
        """Checks if the user is logged in, so that no errors are threw if not"""
        if shared_functions.ph_client.logged:
            return True

        elif not shared_functions.ph_client.logged:
            self.login()
            if not shared_functions.ph_client.logged:
                text = self.tr("There's a problem with the login. Please make sure you login first and then "
                               "you try to get videos based on your account.", None)
                ui_popup(text)
                return False

            else:
                return True

    def get_watched_videos(self):
        """Returns the videos watched by the user"""
        if self.check_login():
            watched = shared_functions.ph_client.account.watched
            self.add_to_tree_widget_thread(watched)

    def get_liked_videos(self):
        """Returns the videos liked by the user"""
        if self.check_login():
            liked = shared_functions.ph_client.account.liked
            self.add_to_tree_widget_thread(liked)

    def get_recommended_videos(self):
        """Returns the videos recommended for the user"""
        if self.check_login():
            recommended = shared_functions.ph_client.account.recommended
            self.add_to_tree_widget_thread(recommended)

    """
    The following functions are related to the search functionality
    """


    def get_top_porn_hqporner(self):
        try:
            videos = shared_functions.hq_client.get_top_porn(sort_by=self.mappings_hqporner_tools[self.ui.tools_combobox_hqporner_top_porn.currentIndex()])

        except NoVideosFound:
            handle_error_gracefully(self, data=video_data.consistent_data, error_message="No videos found. This is likely an issue and will be reported", needs_network_log=True)
            return

        self.add_to_tree_widget_thread(iterator=videos)

    def get_by_category_hqporner(self):
        """Returns video by category from HQPorner."""
        category_name = self.ui.tools_lineedit_hqporner_category.text()
        all_categories = shared_functions.hq_client.get_all_categories()

        if not category_name in all_categories:
            ui_popup(self.tr("Invalid Category. Press 'list categories' to see all "
                             "possible ones.", None))

        else:
            videos = shared_functions.hq_client.get_videos_by_category(category=category_name)
            self.add_to_tree_widget_thread(videos)

    def list_categories_hqporner(self):
        """Get all available categories. I want to also extend that for EPorner (and maybe even more sites)"""
        categories_ = shared_functions.hq_client.get_all_categories()
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
            videos = shared_functions.ep_client.get_videos_by_category(category=category_name, enable_html_scraping=True)
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
            videos = shared_functions.hq_client.get_brazzers_videos()

        except NoVideosFound:
            handle_error_gracefully(self, data=video_data.consistent_data, error_message="No videos found. This is likely an issue and will be reported", needs_network_log=True)
            return

        self.add_to_tree_widget_thread(videos)

    def get_random_video(self):
        """Gets a random video from HQPorner"""
        try:
            video = shared_functions.hq_client.get_random_video()
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
        if self.ui.settings_checkbox_system_enable_anonymous_mode.isChecked():
            self.ui.main_textbrowser_credits.setText("Running in anonymous mode...")

        else:
            self.ui.main_textbrowser_credits.setOpenExternalLinks(True)
            file = QFile(":/credits/README/CREDITS.md")
            file.open(QFile.OpenModeFlag.ReadOnly)
            stream = QTextStream(file)
            self.ui.main_textbrowser_credits.setHtml(markdown.markdown(stream.readAll()))

    def check_for_updates(self):
        """Checks for updates in a thread, so that the main UI isn't blocked, until update checks are done"""
        self.update_thread = CheckUpdates()
        self.update_thread.signals.update_check.connect(self.check_for_updates_result)
        self.threadpool.start(self.update_thread)

    def eventFilter(self, source, event):
        gv = self.ui.graphicsView

        # ——————————————————————————————
        # A) On the view resizing → re-fit & fill
        if source is gv and event.type() == QEvent.Type.Resize:
            rect = self._scene.sceneRect()
            if not rect.isNull():
                gv.fitInView(rect, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
            return False  # let the usual painting happen too

        # ——————————————————————————————
        # B) On double-click in the viewport → popup
        if source is gv.viewport() and event.type() == QEvent.Type.MouseButtonDblClick:
            if not self._full_pixmap.isNull():
                self._show_full_thumbnail()
                return True  # swallow the event
            return False

        return super().eventFilter(source, event)

    def _show_full_thumbnail(self):
        """Open a fixed 1280×720 preview, aspect-fill + center-crop."""
        # Made by ChatGPT :)
        if self._full_pixmap.isNull():
            return

        # 1) Scale up so it at least covers 1280×720, preserving aspect
        scaled = self._full_pixmap.scaled(
            1280, 720,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )

        # 2) Center-crop the scaled pixmap to exactly 1280×720
        w, h = scaled.width(), scaled.height()
        x = max(0, (w - 1280) // 2)
        y = max(0, (h - 720) // 2)
        final_pix = scaled.copy(x, y, 1280, 720)

        # 3) Build a simple scene/view that will show that pixmap 1:1
        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("Full Thumbnail"))

        scene = QGraphicsScene(dialog)
        item = QGraphicsPixmapItem(final_pix)
        scene.addItem(item)
        scene.setSceneRect(item.boundingRect())

        view = QGraphicsView(dialog)
        view.setScene(scene)
        view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        # no scrollbars — we’ve already cropped exactly
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # 4) Layout + force the dialog itself to 1280×720
        layout = QVBoxLayout(dialog)
        layout.addWidget(view)
        dialog.setFixedSize(1280, 720)
        dialog.exec()

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
        has_license = self.license_manager.has_feature("full_unlock")
        self.apply_license_state(combo = self.ui.settings_video_combobox_quality, has_license=has_license)

    def check_internet(self):
        """Checks if the porn sites are accessible"""
        self.internet_check_thread = InternetCheck()
        self.internet_check_thread.signals.internet_check.connect(self.internet_check_result)
        self.threadpool.start(self.internet_check_thread)

    def internet_check_result(self, results: dict):
        show = False
        formatted_results = ""

        for website, status in results.items():
            if status != "OK":
                formatted_results += f"{website} -->: {status}\n\n"
                show = True

        if show:
            ui_popup(self.tr(f"""
! Warning !
Some websites couldn't be accessed. Here's a detailed report:
------------------------------------------------------------
{formatted_results}"""))


def main():
    setup_config_file()
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

    if args.version:
        print(__version__)


    if args.portable:
        FORCE_PORTABLE_RUN = True

    main()