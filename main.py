try:
    from av import open as av_open  # Don't ask
    from av.audio.resampler import AudioResampler  # Don't ask
    FORCE_DISABLE_AV = False

except Exception:
    FORCE_DISABLE_AV = True

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget, QTextBrowser, QVBoxLayout, QPushButton

app_path = Path(sys.argv[0]).resolve()
if str(app_path).startswith("/Volume"):
    class Notification(QWidget):
        def __init__(self):
            super().__init__()
            self.setGeometry(0, 0, 600, 600)
            self.setStyleSheet("""
QWidget: {
color: #ECECEC;  /* Brightened for better contrast */
background-color: #262626; /* Darkened for better contrast */
border: none}
""")
            self.layout = QVBoxLayout()
            self.close_button = QPushButton("Close")
            self.close_button.setMinimumHeight(30)
            self.msg_box = QTextBrowser(self)
            self.msg_box.setText("""
Please move Porn Fetch into your applications folder. You can do that by opening 'Finder' and dragging the Porn Fetch
executable you just clicked on, into the 'Applications' folder that you'll see in Finder. After that, you can open 'Launchpad'
and type 'Porn Fetch'. You'll find it there and can run it easily from Launchpad and also add it to your application bar at
the bottom.

This is an intended behaviour from macOS and all applications follow this scheme. 
Thank you for your patience :)
""")
            self.msg_box.setObjectName("reader")
            self.msg_box.setStyleSheet("""
/* Apply to a QTextBrowser with objectName "reader" */
#reader {
  background: #0b1220;            /* near-black with a hint of blue */
  color: #e5e7eb;                 /* gray-200 */
  border: 1px solid #1f2937;      /* slate-800 */
  border-radius: 12px;
  padding: 12px;
  selection-background-color: rgba(96, 165, 250, 0.28); /* soft blue */
  selection-color: #0b1220;
  font-family: Inter, Segoe UI, Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 14px;
  line-height: 1.35;
}

#reader img, #reader table {
  margin: 6px;
}

/* Vertical scrollbar */
#reader QScrollBar:vertical {
  width: 10px;
  margin: 8px 4px 8px 0;
  background: transparent;
  border: none;
}
#reader QScrollBar::handle:vertical {
  min-height: 24px;
  background: #374151;            /* gray-700 */
  border-radius: 8px;
}
#reader QScrollBar::handle:vertical:hover {
  background: #4b5563;            /* gray-600 */
}
#reader QScrollBar::add-line:vertical,
#reader QScrollBar::sub-line:vertical { height: 0; }
#reader QScrollBar::add-page:vertical,
#reader QScrollBar::sub-page:vertical { background: transparent; }

/* Horizontal scrollbar */
#reader QScrollBar:horizontal {
  height: 10px;
  margin: 0 8px 4px 8px;
  background: transparent;
  border: none;
}
#reader QScrollBar::handle:horizontal {
  min-width: 24px;
  background: #374151;
  border-radius: 8px;
}
#reader QScrollBar::handle:horizontal:hover {
  background: #4b5563;
}
#reader QScrollBar::add-line:horizontal,
#reader QScrollBar::sub-line:horizontal { width: 0; }
#reader QScrollBar::add-page:horizontal,
#reader QScrollBar::sub-page:horizontal { background: transparent; }

#reader:focus {
  border: 1px solid #60a5fa;      /* blue-400 */
}
""")
            self.layout.addWidget(self.msg_box)
            self.layout.addWidget(self.close_button)
            self.setLayout(self.layout)
            self.close_button.setStyleSheet("""
QPushButton {
    background-color: #7B1FA2; /* Purple */
    color: white;
    border-radius: 8px;
}

QPushButton:hover {
    background-color: #9575CD; /* Lighter violet */
}

QPushButton:pressed {
    background-color: #6A1B9A; /* Dark purple */
}

""")
            self.close_button.clicked.connect(self.close)
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.setContentsMargins(0, 0, 0, 0)

    app = QApplication(sys.argv)
    w = Notification()
    w.show()
    sys.exit(app.exec())

try:
    import time
    import uuid
    import random
    import shutil
    import os.path
    import argparse
    import markdown
    import traceback
    import requests # Imported, although not used, because this triggers the certifi cacert.pem include workflow
    import src.backend.shared_functions as shared_functions
    import src.frontend.UI.resources  # Your IDE may tell you that this is an unused import statement, but that is WRONG!
    from threading import Event, Lock
    from io import TextIOWrapper
    from itertools import islice, chain

    from src.backend.shared_gui import *
    from src.backend.class_help import *
    from src.frontend.UI.ui_form_main_window import Ui_MainWindow
    from src.frontend.UI.ui_form_android import Ui_PornFetchAndroid
    from src.backend.one_time_functions import *
    from src.backend.config import __version__, __build__
    from src.backend.donation_nag import DonationNag
    from src.backend.license import License, Disclaimer
    from src.backend.config import shared_config
    from hqporner_api.api import Sort as hq_Sort

    from PySide6.QtCore import (QFile, QTextStream, Signal, QRunnable, QThreadPool, QObject, QSemaphore, Qt, QLocale,
                                QTranslator, QCoreApplication, QSize, QEvent, QRectF)
    from PySide6.QtWidgets import (QApplication, QTreeWidgetItem, QButtonGroup, QFileDialog, QHeaderView, \
        QInputDialog, QMainWindow, QLabel, QProgressBar, QGraphicsPixmapItem, QDialog, QVBoxLayout,
                                   QGraphicsScene, QGraphicsView, QPushButton, QHBoxLayout)
    from PySide6.QtGui import QIcon, QFont, QFontDatabase, QPixmap, QShortcut, QKeySequence, QPainter

except Exception as e:
    import traceback
    error = traceback.format_exc()
    from PySide6.QtWidgets import QWidget, QApplication, QLabel

    class application(QWidget):
        def __init__(self):
            super().__init__()
            self.label = QLabel(self)
            self.label.setText(str(error))


    app = QApplication()
    w = application()
    w.show()
    app.exec()

# Possible errors from APIs
from base_api.modules.errors import ProxySSLError, InvalidProxy
from xnxx_api.modules.errors import InvalidResponse
from hqporner_api.modules.errors import (InvalidActress as InvalidActress_HQ, NoVideosFound,
                                         NotAvailable as NotAvailable_HQ, WeirdError as WeirdError_HQ)
from xvideos_api.modules.errors import (VideoUnavailable as VideoUnavailable_XV)
from eporner_api.modules.errors import NotAvailable as NotAvailable_EP, VideoDisabled as VideoDisabled_EP
from phub.errors import VideoError as VideoError_PH

_download_lock = Lock()
FORCE_PORTABLE_RUN = False


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


# For general information see /src/backend/config.py

total_segments = 0
downloaded_segments = 0
stop_flag = Event()

session_urls = []  # This list saves all URls used in the current session. Used for the URL export function
total_downloaded_videos = 0  # All videos that actually successfully downloaded
total_downloaded_videos_attempt = 0  # All videos the user tries to download
logger = setup_logger("Porn Fetch - [MAIN]", log_file="PornFetch.log", level=logging.DEBUG, http_ip=shared_functions.http_log_ip,
                      http_port=shared_functions.http_log_port)

conf = shared_config
core_conf = shared_functions.config


class VideoData:
    """
    This class stores the video objects and their loaded data across Porn Fetch.
    It allows for re-fetching data if needed, update data if needed and handles caching thanks to
    a dictionary.

    (Okay, I am overhyping it a bit, but yeah, let's put that away xD)
    """

    data_objects = {}
    consistent_data = {}  # This dictionary stores other important data which will be re-used for the entire
    # run of Porn Fetch

    """
    If a video object isn't used anymore e.g., the video finished downloading or the tree widget was loaded with other
    videos, than those videos will be cleaned up in the dictionary, to be as memory and performance efficient as
    possible.
    """

    def clean_dict(self, video_titles):
        if not isinstance(video_titles, list):  # In case we only have one video title to delete
            video_titles = [video_titles]

        for video_title in video_titles:
            del self.data_objects[video_title]  # Del is faster than pop :)

video_data = VideoData()

class Signals(QObject):
    """Signals for the Download class"""
    # Progress Signal
    total_progress = Signal(int) # Sets the current value for the progressbar
    total_progress_range = Signal(int) # Sets the maximum for the total progressbar
    progress_add_to_tree_widget = Signal(int, int)  # Tracks the number of videos
    # loaded and processed into the tree widget

    progress_video = Signal(int, int, int)
    progress_video_range = Signal(int, int)
    progress_video_converting = Signal(int, int)

    error_signal = Signal(object)

    # Animations
    start_undefined_range = Signal()  # Starts the loading animation progressbar
    stop_undefined_range = Signal()  # Stops the loading animation progressbar

    # Operations / Reportings
    install_finished = Signal(object)  # Reports if the Porn Fetch installation was finished
    internet_check = Signal(object)  # Reports if the internet checks were successful
    update_check = Signal(bool, dict)
    result = Signal(dict)  # Reports the result of the internet checks if something went wrong
    clear_tree_widget_signal = Signal()  # A signal to clear the tree widget
    text_data_to_tree_widget = Signal(int)  # Sends the text data in the form of a dictionary to the main class
    download_completed = Signal(object)  # Reports a successfully downloaded video
    progress_send_video = Signal(object,
                                 object)  # Sends the selected video objects from the tree widget to the main class
    tree_widget_finished = Signal()
    # to download them
    url_iterators = Signal(object, object)  # Sends the processed URLs from the file to Porn Fetch


class InstallThread(QRunnable):
    def __init__(self, app_name):
        super(InstallThread, self).__init__()
        self.app_name = app_name
        self.signals = Signals()
        self.logger = setup_logger(name="Porn Fetch - [InstallThread]", log_file="PornFetch.log", level=logging.DEBUG,
                                   http_ip=shared_functions.http_log_ip, http_port=shared_functions.http_log_port)

    def run(self):
        try:
            self.signals.start_undefined_range.emit()

            if sys.platform == "linux":
                self.logger.info("Running installation for Platform: Linux")
                filename = "PornFetch_Linux_GUI_x64.bin"
                destination_path_tmp = os.path.expanduser("~/.local/share/")
                destination_path_final = os.path.expanduser("~/.local/share/pornfetch/")
                destination_install = os.path.expanduser("~/.local/share/applications/")
                shortcut_path = os.path.join(destination_install, "pornfetch.desktop")

                if not os.path.exists(destination_path_tmp):
                    self.logger.warning("The needed installation path doesn't exist?!")
                    text = QCoreApplication.translate("main", """The path ~/.local/share/ does not exist. This path is typically used for installing applications and their settings
in a users local account. Since you don't have that, you can't install it. Probably because your Linux does not follow
the XDG Desktop Portal specifications. It's your own decision and I don't create the directory for you, or force you to
do that. If you still wish to install Porn Fetch, look Online how to setup XDK-Desktop-Portal on your Linux distribution,
head over to the setting and down there you will be able to try the installation again. Otherwise, you can just keep
using the portable version, which will work just fine.

If you believe, that this is a mistake, please report it on GitHub, so that I can fix it :)""", disambiguation=None)
                    ui_popup(text)

                os.makedirs(destination_path_final, exist_ok=True)
                pornfetch_exe = os.path.join(destination_path_final, filename)
                if os.path.exists(pornfetch_exe):
                    os.remove(pornfetch_exe)

                shutil.move("PornFetch_Linux_GUI_x64.bin", dst=destination_path_final)
                self.logger.info(f"Moved the PornFetch binary to: {destination_path_final}")
                shared_functions.shared_config.set("Setup", "install", "installed")
                with open("config.ini", "w") as configuration:
                    shared_config.write(configuration)

                shutil.move("config.ini", dst=destination_path_final)
                self.logger.info("Moved configuration file")
                self.logger.info(f"Downloading additional asset: icon")

                if not os.path.exists(os.path.join(destination_path_final, "Logo.png")):
                    img = shared_functions.core.fetch(
                        "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/refs/heads/master/src/frontend/graphics/android_app_icon.png",
                        get_bytes=True)
                    self.logger.debug("Got Porn Fetch logo, saving...")
                    with open("Logo.png", "wb") as logo:
                        logo.write(img)
                        shutil.move("Logo.png", dst=destination_path_final)

                entry_content = f"""[Desktop Entry]
Name={self.app_name}
Exec={destination_path_final}PornFetch_Linux_GUI_x64.bin %F
Icon={destination_path_final}Logo.png
Type=Application
Terminal=false
Categories=Utility;"""
                if os.path.exists(shortcut_path):
                    os.remove(shortcut_path)

                with open("pornfetch.desktop", "w") as entry_file:
                    entry_file.write(entry_content)

                shutil.move("pornfetch.desktop", shortcut_path)
                self.logger.info("Successfully installed Porn Fetch!")
                os.chmod(mode=0o755,
                         path=destination_path_final + "PornFetch_Linux_GUI_x64.bin")  # Setting executable permission

            elif sys.platform == "win32":
                import win32com.client  # Only available on Windows

                filename = "PornFetch_Windows_GUI_x64.exe"
                target_dir = os.path.join(os.getenv("LOCALAPPDATA"), "pornfetch")
                os.makedirs(target_dir, exist_ok=True)
                self.logger.info(f"Created path at: {target_dir}")
                if os.path.exists(os.path.join(target_dir, filename)):
                    self.logger.info("Removed old Porn Fetch executable")
                    os.remove(os.path.join(target_dir, filename))

                # Move the executable to the target directory
                shutil.move(filename, target_dir)
                self.logger.info(f"Moved current Porn Fetch executable to: {target_dir}")

                try:
                    shared_functions.shared_config.set("Setup", "install", "installed")
                    with open("config.ini", "w") as configuration:
                        shared_config.write(configuration)

                    print("Written new values to config")
                    os.remove(os.path.join(target_dir, "config.ini"))

                except Exception:
                    "Don't care"
                    pass

                shutil.move("config.ini", target_dir)
                print(f"Moved config.ini to {target_dir}")
                # Define paths for the shortcut creation
                app_name = self.app_name
                app_exe_path = os.path.join(target_dir, filename)  # Full path to the executable
                start_menu_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs")
                shortcut_path = os.path.join(start_menu_path, f"{app_name}.lnk")

                # Create the shortcut
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortcut(shortcut_path)
                shortcut.TargetPath = app_exe_path  # Path to the executable
                shortcut.WorkingDirectory = target_dir  # Set working directory to the target directory
                shortcut.IconLocation = app_exe_path
                shortcut.Save()
                self.logger.info(f"Created shortcut in -->: {shortcut_path}")

        except Exception:
            error = traceback.format_exc()
            self.logger.error(error)
            self.signals.install_finished.emit([False, error])
            self.signals.stop_undefined_range.emit()
            return

        self.signals.stop_undefined_range.emit()
        self.signals.install_finished.emit([True, ""])
        # Porn Fetch installation is finished


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
            "https://www.spankbang.com"
            # Append new URLs here
        ]

        self.website_results = {}
        self.signals = Signals()
        self.logger = setup_logger(name="Porn Fetch - [InternetCheck]", log_file="PornFetch.log", level=logging.DEBUG,
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
        self.logger = setup_logger(name="Porn Fetch - [CheckUpdates]", log_file="PornFetch.log", level=logging.DEBUG,
                                   http_port=shared_functions.http_log_port, http_ip=shared_functions.http_log_ip)

    def run(self):
        url = f"https://echteralsfake.duckdns.org:443/update"

        try:
            response = shared_functions.core.fetch(url=url, get_response=True)
            if response.status_code == 200:
                json_stuff = response.json()
                if float(json_stuff["version"]) > float(__version__):
                    self.logger.info(f"A new update is available -->: {json_stuff['version']}")
                    self.signals.update_check.emit(True, json_stuff)

                else:
                    self.logger.info(f"Checked for updates... You are on the latest versioin :)")
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
    def __init__(self, iterator, is_reverse, is_checked, last_index):
        super(AddToTreeWidget, self).__init__()
        self.signals = Signals()  # Processing signals for progress and information
        self.iterator = iterator  # The video iterator (Search or model object yk)
        self.reverse = is_reverse  # If the user wants to display the videos in reverse
        self.stop_flag = stop_flag  # If the user pressed the stop process button
        self.is_checked = is_checked  # If the "do not clear videos" checkbox is checked
        self.last_index = last_index  # The last index (video) of the tree widget to maintain a correct order of numbers
        self.consistent_data = video_data.consistent_data
        self.output_path = self.consistent_data.get("output_path")
        self.result_limit = self.consistent_data.get("result_limit")
        self.supress_errors = self.consistent_data.get("supress_errors")
        self.activate_logging = self.consistent_data.get("activate_logging")
        self.logger = setup_logger(name="Porn Fetch - [AddToTreeWidget]", log_file="PornFetch.log", level=logging.DEBUG,
                                   http_port=shared_functions.http_log_port, http_ip=shared_functions.http_log_ip)

    def process_video(self, video, index):
        if not isinstance(video, str):
            self.logger.debug(f"Requesting video processing of: {video.url}")

        else:
            self.logger.debug(f"Requesting video processing of: {video}")

        for attempt in range(0, 5):
            try:
                video_id = random.randint(0, 99999999) # Creates a random ID for each video
                if isinstance(video, str):
                    video = shared_functions.check_video(url=video, is_url=True)

                self.logger.debug(f"Created ID: {video_id} for: {video.url}")
                data = shared_functions.load_video_attributes(video)
                session_urls.append(video.url)
                self.logger.debug("Loaded video attributes")
                stripped_title = shared_functions.core.strip_title(
                    data.get("title"))  # Strip the title so that videos with special chars can be
                                        # saved on windows. it would raise an OSError otherwise

                if self.consistent_data.get("video_id_as_filename"):
                    stripped_title = str(video_id)

                if self.consistent_data.get(
                        "directory_system"):  # If the directory system is enabled, this will create an additional folder
                    author_path = os.path.join(self.output_path, data.get("author"))
                    os.makedirs(author_path, exist_ok=True)
                    output_path = os.path.join(str(author_path), stripped_title + ".mp4")

                else:
                    output_path = os.path.join(self.output_path, stripped_title + ".mp4")

                stripped_title = shared_functions.core.strip_title(title=data.get("title"))
                # Emit the loaded signal with all the required information

                data.update(
                    {
                        "title": stripped_title,
                        "output_path": output_path,
                        "index": index,
                        "video": video
                    })

                video_data.data_objects.update({video_id: data})
                return video_id

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

            except Exception:
                error = traceback.format_exc()
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"Unexpected error occurred: {error}", needs_network_log=True)
                return False

        return None

    def run(self):
        self.signals.start_undefined_range.emit()  # Starts the progressbar, but with a loading animation
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


        if self.reverse:
            self.logger.info("Reversing Videos. This may take some time...")

            # Use islice to limit the number of items fetched from the iterator
            videos = list(islice(self.iterator, self.result_limit))  # Can take A LOT of time (like really)
            videos.reverse()  # Reverse the list (to show videos in reverse order)

        else:
            videos = islice(self.iterator, self.result_limit)

        self.signals.total_progress_range.emit(self.result_limit)
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
        self.logger = setup_logger(name="Porn Fetch - [DownloadThread]", log_file="PornFetch.log", level=logging.DEBUG,
                                   http_ip=shared_functions.http_log_ip, http_port=shared_functions.http_log_port)

        self.threading_mode = self.consistent_data.get("threading_mode")
        self.signals = Signals()
        self.stop_flag = stop_flag
        self.skip_existing_files = self.consistent_data.get("skip_existing_files")
        self.workers = int(self.consistent_data.get("workers"))
        self.timeout = int(self.consistent_data.get("timeout"))
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
            if isinstance(self.video, shared_functions.hq_Video) or isinstance(self.video, shared_functions.ep_Video):
                video_source = "raw"
                try:
                    self.video.download(quality=self.quality, path=self.output_path, no_title=True,
                                    callback=lambda pos, total: self.generic_callback(pos, total, video_source))

                except Exception:
                    error = traceback.format_exc()
                    handle_error_gracefully(data=self.consistent_data, self=self, error_message=f"An error happened while downloading a video from HQPorner / EPorner: {error}", needs_network_log=True)

            elif isinstance(self.video, shared_functions.ph_Video):  # Assuming 'Video' is the class for Pornhub
                video_source = "general"
                self.logger.debug("Starting the Download!")
                self.video.download(downloader=str(self.threading_mode), path=self.output_path, quality=self.quality, remux=remux, display_remux=self.callback_remux,
                                    display=lambda pos, total: self.generic_callback(pos, total))

            else:
                self.video.download(downloader=str(self.threading_mode), path=self.output_path, callback_remux=self.callback_remux, no_title=True,
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
        self.threading_mode = self.consistent_data.get("threading_mode")
        self.quality = self.consistent_data.get("quality")
        self.semaphore = semaphore
        self.logger = setup_logger(name="Porn Fetch - [QTreeWidgetDownloadThread]", log_file="PornFetch.log",
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


class AddUrls(QRunnable):
    """
    This class is used to add the URLs from the 'open file' function, because the UI doesn't respond until
    all URLs / Models / Search terms have been processed. This is why I made this threading class
    """

    def __init__(self, file):
        super(AddUrls, self).__init__()
        self.signals = Signals()
        self.file = file
        self.logger = setup_logger(name="Porn Fetch - [AddUrls (Batch Processing)]", log_file="PornFetch.log", level=logging.DEBUG,
                                   http_port=shared_functions.http_log_port, http_ip=shared_functions.http_log_ip)

    def run(self):
        iterator = []
        model_iterators = []

        self.signals.start_undefined_range.emit()
        self.logger.info(f"Trying to read URL (Batch) file: {self.file}")
        with open(self.file, "r") as url_file:
            content = url_file.read().splitlines()

        self.logger.info(f"Found: {len(content)} lines of iterables")
        for idx, line in enumerate(content):
            if len(line) == 0:
                continue

            self.signals.stop_undefined_range.emit()
            total = len(content)
            self.signals.total_progress_range.emit(total)
            """
            Template:
            
            model#<url>
            video#<url>
            """

            if line.startswith("model#"):
                model_url = line.split("#")[1]
                model_iterators.append(model_url)
                self.logger.debug(f"Found Model URL ->: {model_url}")

            elif line.startswith("video#"):
                video_url = line.split("#")[1]
                video = shared_functions.check_video(video_url)

                if video is not False:
                    self.logger.debug("Found Video object!")
                    iterator.append(video)

            else:
                self.logger.warning(f"Line: {idx} - {line} contains invalid formatting!, skipping...")

            self.signals.total_progress.emit(idx)

        self.signals.url_iterators.emit(iterator, model_iterators)

class SSLWarningDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SSL Verification Warning")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        warning_text = (
            "<b>Your proxy does not support proper SSL verification.</b><br><br>"
            "The only way to bypass this is to <b>disable SSL certificate verification</b> completely.<br><br>"
            "<b>⚠ This is a serious security risk.</b><br>"
            "Disabling SSL verification may expose your connection to man-in-the-middle (MITM) attacks, "
            "data interception, or spoofed websites.<br><br>"
            "Do you want to proceed and disable SSL verification?"
        )

        label = QLabel(warning_text)
        label.setWordWrap(True)
        label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(label)

        # Button layout
        button_layout = QHBoxLayout()
        self.accept_btn = QPushButton("Accept (Disable SSL Verification)")
        self.cancel_btn = QPushButton("Cancel")

        button_layout.addStretch()
        button_layout.addWidget(self.accept_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

        self.accept_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

class PornFetch(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_update_time = time.time()
        self.last_thumbnail_change = time.time()
        self.stylesheets = None
        self._pixmap_item = None
        self._scene = None
        self.use_video_id_as_filename = None
        self.processing_delay = None
        self.activate_logging = None
        self.supress_errors = None
        self.direct_download = None
        self._full_pixmap = None
        if __build__ == "desktop":
            self.ui = Ui_MainWindow()

        elif __build__ == "android":
            self.ui = Ui_PornFetchAndroid()

        self.ui.setupUi(self)

        # Threads
        self.install_thread = None
        self.internet_check_thread = None
        self.update_thread = None
        self.url_thread = None
        self.download_thread = None
        self.video_loader_thread = None
        self.download_tree_thread = None
        self.add_to_tree_widget_thread_ = None

        # Button groups
        self.group_threading_mode = None
        self.group_quality = None
        self.group_radio_tree_data_mode = None
        self.group_ui_language = None
        self.group_directory_system = None
        self.group_radio_hqporner = None
        self.group_radio_model_videos = None
        self.group_radio_skip_existing_files = None

        # UI Stuff
        self.header = None
        self.widget = None
        self.range_ui = None
        self.keyboard_widget = None
        self.keyboard_widget_ = None
        self.all_categories_eporner = None

        # Settings mappings
        self.map_quality = None
        self.map_model_videos = None
        self.map_gui_language = None
        self.map_threading_mode = None

        self.internet_checks = None
        self.update_checks = None
        self._anonymous_mode = None
        self.write_metadata = None
        self.semaphore_limit = None
        self.result_limit = None
        self.output_path = None
        self.gui_language = None
        self.quality = None
        self.threading_mode = None
        self.semaphore = None
        self.delay = None
        self.timeout = None
        self.workers = None
        self.max_retries = None
        self.skip_existing_files = None
        self.model_videos_type = None
        self.kill_switch = False
        self.proxy = None
        self.downloader = None
        self.speed_limit_mb = None
        self.directory_system = None
        self.logger = setup_logger(name="Porn Fetch - [PornFetch]", log_file="PornFetch.log", level=logging.DEBUG,
                                   http_ip=shared_functions.http_log_ip, http_port=shared_functions.http_log_port)

        self.last_index = 0  # Keeps track of the last index of videos added to the tree widget
        self.threadpool = QThreadPool()

        self.load_style()
        self.donation_nag = DonationNag(self.ui, self.initialize_pornfetch)
        self.license = License(self.ui, self.initialize_pornfetch)
        self.disclaimer = Disclaimer(self.ui, self.initialize_pornfetch)

        """
                             ! INDEX LIST !

        0) Main application (downloading, login, tree widget etc.)
        :: Index list for main application ::
        - 0: Download
        - 1: Login
        - 2: Progress Bars
        - 3: Tools

        1) Settings
        2) Credits
        3) License
        4) Range Selector (for automatically selecting videos in the tree widget)
        5) Keyboard Shortcuts
        6) Install Dialog
        7) Supported websites
        8) Donation Nag        
        9) Disclaimer text
        This may look a little bit confusing, but once you understand it, it makes sense, trust me :)
        """

        self.default_max_height = self.ui.main_stacked_widget_top.maximumHeight()
        self.button_connections()  # Connects the buttons to their functions
        self.button_groups()  # Groups the buttons, so that the Radio buttons are split from themselves (hard to explain)
        self.shortcuts()  # Activates the keyboard shortcuts
        self.logger.debug("Startup: [3/5] Initialized the User Interface")
        self.settings_maps_initialization()
        self.load_user_settings()  # Loads the user settings and applies selected values to the UI
        self.logger.debug("Startup: [4/5] Loaded the user settings")
        self.progress_widgets = {}  # video_id -> {'label': QLabel, 'progressbar': QProgressBar}

        if self.internet_checks:
            self.logger.info("Running internet checks")
            self.check_internet()

        if self.update_checks:
            self.logger.info("Running update checks")
            self.check_for_updates()

        if self._anonymous_mode:
            self.logger.info("Enabling anonymous mode")
            self.anonymous_mode()

        # IMPORTANT
        video_data.consistent_data.update({
            "output_path": self.output_path,
            "threading_mode": self.threading_mode,
            "quality": self.quality,
            "timeout": self.timeout,
            "workers": self.workers,
            "directory_system": self.directory_system,
            "write_metadata": self.write_metadata,
            "result_limit": self.result_limit,
            "skip_existing_files": self.skip_existing_files,
            "supress_errors": self.supress_errors,
            "activate_logging": self.activate_logging,
            "video_id_as_filename": self.use_video_id_as_filename,
            "processing_delay": self.processing_delay,
        })
        self.logger.debug("Startup: [5/5] OK")
        self.initialize_pornfetch()

    def disable_logging(self):
        conf["Setup"]["activate_logging"] = "false"
        with open("config.ini", "w") as configuration:
            conf.write(configuration)

        self.initialize_pornfetch()

    def enable_logging(self):
        conf["Setup"]["activate_logging"] = "true"
        with open("config.ini", "w") as configuration:
            conf.write(configuration)

        self.initialize_pornfetch()

    """
    The following functions just switch the Stacked Widget to the different widgets
    """

    def switch_to_main(self):
        self.ui.CentralStackedWidget.setCurrentIndex(0)

    def switch_to_settings(self):
        self.ui.CentralStackedWidget.setCurrentIndex(1)

    def switch_to_credits(self):
        self.show_credits()
        self.ui.CentralStackedWidget.setCurrentIndex(2)

    def switch_to_license(self):
        self.ui.CentralStackedWidget.setCurrentIndex(3)

    def switch_to_range_selector(self):
        self.ui.CentralStackedWidget.setCurrentIndex(4)

    def switch_to_keyboard_shortcuts(self):
        self.ui.CentralStackedWidget.setCurrentIndex(5)

    def switch_to_install_dialog(self):
        self.ui.CentralStackedWidget.setCurrentIndex(7)

    def switch_to_supported_sites(self):
        self.ui.CentralStackedWidget.setCurrentIndex(8)

    def switch_to_donation_nag(self):
        self.ui.CentralStackedWidget.setCurrentIndex(9)

    def switch_to_download(self):
        self.ui.scroll_area_top_stacked.setMinimumHeight(110)
        self.ui.scroll_area_top_stacked.setMaximumHeight(240)
        self.ui.main_stacked_widget_top.setMaximumHeight(230)
        self.ui.main_stacked_widget_top.setMinimumHeight(220)
        self.ui.main_stacked_widget_top.setCurrentIndex(0)
        self.switch_to_main()

    def switch_to_login(self):
        self.ui.scroll_area_top_stacked.setMinimumHeight(110)
        self.ui.scroll_area_top_stacked.setMaximumHeight(160)
        self.ui.main_stacked_widget_top.setMinimumHeight(160)
        self.ui.main_stacked_widget_top.setMaximumHeight(160)
        self.ui.main_stacked_widget_top.setCurrentIndex(1)
        self.switch_to_main()

    def switch_to_progressbars(self):
        self.ui.scroll_area_top_stacked.setMinimumHeight(80)
        self.ui.scroll_area_top_stacked.setMaximumHeight(200)
        self.ui.main_stacked_widget_top.setMinimumHeight(200)
        self.ui.main_stacked_widget_top.setMaximumHeight(200)
        self.ui.main_stacked_widget_top.setCurrentIndex(2)
        self.switch_to_main()

    def switch_to_tools(self):
        self.ui.scroll_area_top_stacked.setMinimumHeight(120)
        self.ui.scroll_area_top_stacked.setMaximumHeight(250)
        self.ui.main_stacked_widget_top.setMinimumHeight(250)
        self.ui.main_stacked_widget_top.setMaximumHeight(250)
        self.ui.main_stacked_widget_top.setCurrentIndex(3)
        self.switch_to_main()

    def switch_to_disclaimer(self):
        self.ui.CentralStackedWidget.setCurrentIndex(10)

    def switch_to_logging(self):
        self.ui.CentralStackedWidget.setCurrentIndex(11)

    def load_style(self):
        icons = {
            # Menu Bar Icons
            self.ui.main_button_switch_home: "download.svg",
            self.ui.main_button_switch_settings: "settings.svg",
            self.ui.main_button_switch_credits: "information.svg",
            self.ui.main_button_switch_account: "account.svg",
            self.ui.main_button_switch_tools: "tools.svg",
            self.ui.main_button_view_progress_bars: "progressbars.svg",
        }
        """Refactored function to load icons and stylesheets."""
        # Setting icons with a loop if applicable
        self.setGeometry(0, 0, 1054, 829)
        for button, icon_name in icons.items():
            if icon_name == "settings.svg" or icon_name == "tools.svg":
                button.setIconSize(QSize(24, 24))

            button.setIcon(QIcon(f":/images/graphics/{icon_name}"))

        self.setWindowIcon(QIcon(":/images/graphics/logo_transparent.ico"))
        # Stylesheets
        stylesheet_paths = {
            "stylesheet_menu_button_download": ":/style/stylesheets/menu_button_download.qss",
            "stylesheet_menu_button_account": ":/style/stylesheets/menu_button_account.qss",
            "stylesheet_menu_button_tools": ":/style/stylesheets/menu_button_tools.qss",
            "stylesheet_menu_button_credits": ":/style/stylesheets/menu_button_credits.qss",
            "stylesheet_menu_button_progress": ":/style/stylesheets/menu_button_progress.qss",
            "progressbar_pornhub": ":/style/stylesheets/progressbar_pornhub.qss",
            "progressbar_hqporner": ":/style/stylesheets/progressbar_hqporner.qss",
            "progressbar_eporner": ":/style/stylesheets/progressbar_eporner.qss",
            "progressbar_total": ":/style/stylesheets/progressbar_total.qss",
            "progressbar_xnxx": ":/style/stylesheets/progressbar_xnxx.qss",
            "progressbar_missav": ":/style/stylesheets/progressbar_missav.qss",
            "progressbar_xhamster": ":/style/stylesheets/progressbar_xhamster.qss",
            "progressbar_xvideos": ":/style/stylesheets/progressbar_xvideos.qss",
            "progressbar_spankbang": ":/style/stylesheets/progressbar_spankbang.qss",
            "progressbar_converting": ":/style/stylesheets/progressbar_converting.qss",
            "button_blue": ":/style/stylesheets/stylesheet_button_blue.qss",
            "button_orange": ":/style/stylesheets/stylesheet_button_orange.qss",
            "button_purple": ":/style/stylesheets/stylesheet_button_purple.qss",
            "button_green": ":/style/stylesheets/stylesheet_button_green.qss",
            "buttons_login": ":/style/stylesheets/stylesheet_buttons_login.qss",
            "button_reset": ":/style/stylesheets/stylesheet_button_reset.qss"
        }

        self.stylesheets = {key: load_stylesheet(path) for key, path in stylesheet_paths.items()}
        stylesheets = self.stylesheets # Please don't ask
        # Applying stylesheets to specific buttons
        # Simplify this part based on actual UI structure and naming

        from PySide6.QtWidgets import QWidget
        for child in self.findChildren(QWidget):
            if isinstance(child, QPushButton) and "button_help" in child.objectName():
                child.setStyleSheet(stylesheets["button_green"])
                child.setIcon(QIcon(f":/images/graphics/faq.svg"))

        # Applying top buttons
        self.ui.login_button_login.setStyleSheet(stylesheets["button_green"])
        self.ui.main_progressbar_total.setStyleSheet(stylesheets["progressbar_total"])
        self.ui.main_progressbar_converting.setStyleSheet(stylesheets["progressbar_converting"])
        self.ui.download_button_model.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_search.setStyleSheet(stylesheets["button_purple"])
        self.ui.download_button_download.setStyleSheet(stylesheets["button_purple"])
        self.ui.main_button_tree_download.setStyleSheet(stylesheets["button_orange"])
        self.ui.settings_button_videos_open_output_path.setStyleSheet(stylesheets["button_blue"])
        self.ui.login_button_login.setStyleSheet(stylesheets["button_blue"])
        self.ui.settings_button_apply.setStyleSheet(stylesheets["button_blue"])
        self.ui.tools_button_get_random_videos.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_update_acknowledged.setStyleSheet(stylesheets["button_green"])
        self.ui.tools_button_get_brazzers_videos.setStyleSheet(stylesheets["button_purple"])
        self.ui.tools_button_list_categories.setStyleSheet(stylesheets["button_purple"])

        if __build__ == "desktop":
            self.ui.download_button_open_file.setStyleSheet(stylesheets["button_purple"])

        self.ui.main_button_switch_supported_websites.setStyleSheet(stylesheets["button_blue"])
        self.ui.tools_button_hqporner_category_get_videos.setStyleSheet(stylesheets["button_purple"])
        self.ui.tools_button_top_porn_get_videos.setStyleSheet(stylesheets["button_purple"])
        self.ui.login_button_get_watched_videos.setStyleSheet(stylesheets["buttons_login"])
        self.ui.login_button_get_liked_videos.setStyleSheet(stylesheets["buttons_login"])
        self.ui.login_button_get_recommended_videos.setStyleSheet(stylesheets["buttons_login"])
        self.ui.settings_button_reset.setStyleSheet(stylesheets["button_reset"])
        self.ui.download_button_playlist_get_videos.setStyleSheet(stylesheets["button_purple"])
        self.ui.main_button_tree_stop.setStyleSheet(stylesheets["button_reset"])
        self.ui.tools_button_eporner_category_get_videos.setStyleSheet(stylesheets["button_purple"])

        self.ui.tools_button_list_categories_eporner.setStyleSheet(stylesheets["button_purple"])
        self.ui.settings_button_system_install_pornfetch.setStyleSheet(stylesheets["button_green"])
        self.ui.main_button_tree_automated_selection.setStyleSheet(stylesheets["button_purple"])
        self.ui.main_button_tree_keyboard_shortcuts.setStyleSheet(stylesheets["button_blue"])

        self.ui.main_button_switch_home.setStyleSheet(stylesheets["stylesheet_menu_button_download"])
        self.ui.main_button_switch_account.setStyleSheet(stylesheets["stylesheet_menu_button_account"])
        self.ui.main_button_switch_tools.setStyleSheet(stylesheets["stylesheet_menu_button_tools"])
        self.ui.main_button_switch_credits.setStyleSheet(stylesheets["stylesheet_menu_button_credits"])
        self.ui.main_button_view_progress_bars.setStyleSheet(stylesheets["stylesheet_menu_button_progress"])

        self.header = self.ui.treeWidget.header()
        self.header.resizeSection(0, 300)
        self.header.resizeSection(1, 150)
        self.header.resizeSection(2, 50)
        self.header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.ui.treeWidget.setColumnWidth(3, 150)
        self.ui.treeWidget.itemClicked.connect(self.set_thumbnail)
        self.ui.treeWidget.currentItemChanged.connect(self.set_thumbnail)
        self.setWindowTitle(f"Porn Fetch v{__version__} Copyright (C) Johannes Habel 2023-2025")

        font = QFont()
        if conf["UI"]["custom_font"] == "true":
            font_id = QFontDatabase.addApplicationFont(":/fonts/graphics/JetBrainsMono-Regular.ttf")
            if font_id == -1:
                print("Failed to load font, please report")
            else:
                # Get the family name of the loaded font
                font.setFamily(QFontDatabase.applicationFontFamilies(font_id)[0])

        else:
            font.setFamily("Arial")

        font.setPixelSize(int(conf["UI"]["font_size"]))
        from PySide6.QtWidgets import QWidget
        for w in self.findChildren(QWidget):
            w.setFont(font)

        self.ui.treeWidget.sortByColumn(2, Qt.SortOrder.AscendingOrder)
        self.ui.progress_gridlayout_progressbar.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ChatGPT really cooked here
        if __build__ == "desktop":
            gv = self.ui.graphicsView # Geschlechtsverkehr Hihihi
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

        self.switch_to_download()

    def install_pornfetch(self):
        app_name = self.ui.lineedit_custom_app_name.text()
        if app_name == "" or app_name is None:
            self.logger.info("You did not provide a custom App name. Using 'Porn Fetch' for the installation.")
            app_name = "Porn Fetch"

        self.install_thread = InstallThread(app_name=app_name)
        self.install_thread.signals.start_undefined_range.connect(self.start_undefined_range)
        self.install_thread.signals.stop_undefined_range.connect(self.stop_undefined_range)
        self.install_thread.signals.install_finished.connect(self.install_pornfetch_result)
        self.threadpool.start(self.install_thread)

    def install_porn_fetch_portable(self):
        conf["Setup"]["install"] = "portable"
        with open("config.ini", "w") as config: # type: TextIOWrapper
            conf.write(config)

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
        self.ui.settings_groupbox_system_pornfetch.setWindowTitle("System")
        self.ui.main_textbrowser_supported_websites.setText(
            "Running in anonymous mode, please deactivate to display...")
        self.ui.download_lineedit_playlist_url.setPlaceholderText("Enter playlist URL")
        self.ui.download_radio_search_website_eporner.setText("4")
        self.ui.download_radio_search_website_hqporner.setText("2")
        self.ui.download_radio_search_website_pornhub.setText("1")
        self.ui.download_radio_search_website_xvideos.setText("3")
        self.ui.download_radio_search_website_xnxx.setText("5")
        self._anonymous_mode = True  # Makes sense, trust
        self.logger.info("Enabled anonymous mode!")

    def button_groups(self):
        """
        The button groups are needed to tell the radio button which of them are in a group.
        If I don't do this, then you could check all redio buttons at the same time lol"""
        self.group_threading_mode = QButtonGroup()
        self.group_threading_mode.addButton(self.ui.settings_radio_performance_download_mode_performance)
        self.group_threading_mode.addButton(self.ui.settings_radio_performance_download_mode_default)

        self.group_quality = QButtonGroup()
        self.group_quality.addButton(self.ui.settings_radio_videos_quality_worst)
        self.group_quality.addButton(self.ui.settings_radio_videos_quality_half)
        self.group_quality.addButton(self.ui.settings_radio_videos_quality_best)

        self.group_ui_language = QButtonGroup()
        self.group_ui_language.addButton(self.ui.settings_radio_ui_language_english)
        self.group_ui_language.addButton(self.ui.settings_radio_ui_language_german)
        self.group_ui_language.addButton(self.ui.settings_radio_ui_language_french)
        self.group_ui_language.addButton(self.ui.settings_radio_ui_language_system_default)
        self.group_ui_language.addButton(self.ui.settings_radio_ui_language_chinese_simplified)

        self.group_radio_hqporner = QButtonGroup()
        self.group_radio_hqporner.addButton(self.ui.tools_radio_top_porn_week)
        self.group_radio_hqporner.addButton(self.ui.tools_radio_top_porn_month)
        self.group_radio_hqporner.addButton(self.ui.tools_radio_top_porn_all_time)

        self.group_radio_model_videos = QButtonGroup()
        self.group_radio_model_videos.addButton(self.ui.settings_radio_videos_model_type_both)
        self.group_radio_model_videos.addButton(self.ui.settings_radio_videos_model_type_user_uploads)
        self.group_radio_model_videos.addButton(self.ui.settings_radio_videos_model_type_featured)

    def button_connections(self):
        """a function to link the buttons to their functions"""
        # Menu Bar Switch Button Connections
        self.ui.main_button_switch_home.clicked.connect(self.switch_to_download)
        self.ui.main_button_switch_settings.clicked.connect(self.switch_to_settings)
        self.ui.main_button_switch_credits.clicked.connect(self.switch_to_credits)
        self.ui.main_button_switch_account.clicked.connect(self.switch_to_login)
        self.ui.main_button_switch_supported_websites.clicked.connect(self.switch_to_supported_sites)
        self.ui.main_button_view_progress_bars.clicked.connect(self.switch_to_progressbars)

        # Video Download Button Connections
        self.ui.main_button_tree_download.clicked.connect(self.download_tree_widget)
        self.ui.download_button_download.clicked.connect(self.start_single_video)
        self.ui.download_button_model.clicked.connect(self.start_model)
        self.ui.download_button_playlist_get_videos.clicked.connect(self.start_playlist)

        # Help Buttons Connections
        self.ui.settings_button_help_performance_simultaneous_downloads.clicked.connect(button_help_simultaneous_downloads)
        self.ui.settings_button_help_performance_download_mode.clicked.connect(button_help_download_mode)
        self.ui.settings_button_help_performance_maximal_workers.clicked.connect(button_help_maximal_workers)
        self.ui.settings_button_help_performance_maximal_timeout.clicked.connect(button_help_timeout)
        self.ui.settings_button_help_performance_network_delay.clicked.connect(button_help_network_delay)
        self.ui.settings_button_help_performance_maximal_retries.clicked.connect(button_help_max_retries)
        self.ui.settings_button_help_performance_processing_delay.clicked.connect(button_help_processing_delay)
        self.ui.settings_button_help_performance_speed_limit.clicked.connect(button_help_speed_limit)
        self.ui.settings_button_help_videos_use_directory_system.clicked.connect(button_help_directory_system)
        self.ui.settings_button_help_videos_result_limit.clicked.connect(button_help_result_limit)
        self.ui.settings_button_help_videos_skip_existing_files.clicked.connect(button_help_skip_existing_files)
        self.ui.settings_button_help_videos_model_videos_type.clicked.connect(button_help_model_videos)
        self.ui.settings_button_help_videos_write_metadata.clicked.connect(button_help_write_metadata)
        self.ui.settings_button_help_videos_direct_download.clicked.connect(button_help_direct_download)
        self.ui.settings_button_help_system_anonymous_mode.clicked.connect(button_help_anonymous_mode)
        self.ui.settings_button_help_system_supress_errors.clicked.connect(button_help_supress_errors)
        self.ui.settings_button_help_system_enable_network_logging.clicked.connect(button_help_network_logging)
        self.ui.settings_button_help_system_proxy_kill_switch.clicked.connect(button_help_proxy_kill_switch)
        if __build__ == "desktop":
            self.ui.download_button_help_file.clicked.connect(open_file_help)
        # Settings
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
        if __build__ == "desktop":
            self.ui.download_button_open_file.clicked.connect(self.open_file_dialog)

        # Other stuff IDK
        self.ui.main_button_tree_stop.clicked.connect(switch_stop_state)
        self.ui.main_button_tree_keyboard_shortcuts.clicked.connect(self.switch_to_keyboard_shortcuts)
        self.ui.main_button_tree_automated_selection.clicked.connect(self.select_range_of_items)
        self.ui.settings_checkbox_system_proxy_kill_switch.toggled.connect(self.toggle_killswitch)

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

    def settings_maps_initialization(self):
        # Maps for settings and corresponding UI elements
        self.map_quality = {
            "best": self.ui.settings_radio_videos_quality_best,
            "half": self.ui.settings_radio_videos_quality_half,
            "worst": self.ui.settings_radio_videos_quality_worst
        }

        self.map_threading_mode = {
            "threaded": self.ui.settings_radio_performance_download_mode_performance,
            "default": self.ui.settings_radio_performance_download_mode_default
        }

        self.map_gui_language = {
            "en": self.ui.settings_radio_ui_language_english,
            "de_DE": self.ui.settings_radio_ui_language_german,
            "fr": self.ui.settings_radio_ui_language_french,
            "zh_CN": self.ui.settings_radio_ui_language_chinese_simplified,
            "system": self.ui.settings_radio_ui_language_system_default
        }

        self.map_model_videos = {
            "both": self.ui.settings_radio_videos_model_type_both,
            "uploads": self.ui.settings_radio_videos_model_type_user_uploads,
            "featured": self.ui.settings_radio_videos_model_type_featured
        }

    def load_user_settings(self):
        """Loads the user settings from the configuration file and applies them."""
        conf.read("config.ini")
        # Apply settings
        self.map_quality.get(conf.get("Video", "quality")).setChecked(True)
        self.map_threading_mode.get(conf.get("Performance", "threading_mode")).setChecked(True)
        self.map_gui_language.get(conf.get("UI", "language")).setChecked(True)
        self.map_model_videos.get(conf.get("Video", "model_videos")).setChecked(True)
        self.ui.settings_spinbox_performance_simultaneous_downloads.setValue(int(conf.get("Performance", "semaphore")))
        self.ui.settings_spinbox_videos_result_limit.setValue(int(conf.get("Video", "result_limit")))
        self.ui.settings_lineedit_videos_output_path.setText(conf.get("Video", "output_path"))
        self.ui.settings_spinbox_ui_font_size.setValue(int(conf.get("UI", "font_size")))
        self.internet_checks = conf.get("Setup", "internet_checks") == "true"
        self.ui.settings_checkbox_system_internet_checks.setChecked(self.internet_checks)

        self.update_checks = conf.get("Setup", "update_checks") == "true"
        self.ui.settings_checkbox_system_update_checks.setChecked(self.update_checks)

        self._anonymous_mode = conf.get("Setup", "anonymous_mode") == "true"
        self.ui.settings_checkbox_system_enable_anonymous_mode.setChecked(self._anonymous_mode)

        self.use_video_id_as_filename = conf.get("Video", "video_id_as_filename") == "true"
        self.ui.settings_checkbox_videos_use_video_id_as_filename.setChecked(self.use_video_id_as_filename)

        self.skip_existing_files = conf.get("Video", "skip_existing_files") == "true"
        self.ui.settings_checkbox_videos_skip_existing_files.setChecked(self.skip_existing_files)

        self.direct_download = conf.get("Video", "direct_download") == "true"
        self.ui.settings_checkbox_videos_direct_download.setChecked(self.direct_download)

        self.directory_system = conf.get("Video", "directory_system") == "true"
        self.ui.settings_checkbox_videos_use_directory_system.setChecked(self.directory_system)

        self.supress_errors = conf.get("Video", "supress_errors") == "true"
        self.ui.settings_checkbox_system_supress_errors.setChecked(self.supress_errors)

        self.activate_logging = conf.get("Setup", "activate_logging") == "true"
        self.ui.settings_checkbox_system_enable_network_logging.setChecked(self.activate_logging)

        self.ui.settings_checkbox_ui_custom_font.setChecked(True if conf.get("UI", "custom_font") == "true" else False)

        self.write_metadata = conf.get("Video", "write_metadata") == "true"
        self.ui.settings_checkbox_videos_write_metadata.setChecked(self.write_metadata)

        self.semaphore_limit = conf.get("Performance", "semaphore")
        self.result_limit = int(conf.get("Video", "result_limit"))
        self.output_path = conf.get("Video", "output_path")

        self.gui_language = conf.get("UI", "language")
        self.quality = conf["Video"]["quality"]
        self.threading_mode = conf["Performance"]["threading_mode"]
        self.semaphore = QSemaphore(int(self.semaphore_limit))
        self.delay = int(conf["Video"]["delay"])
        self.timeout = int(conf["Performance"]["timeout"])
        self.workers = int(conf["Performance"]["workers"])
        self.max_retries = int(conf["Performance"]["retries"])
        self.speed_limit_mb = float(conf["Performance"]["speed_limit"])
        self.model_videos_type = conf["Video"]["model_videos"]
        self.processing_delay = conf["Performance"]["processing_delay"]
        self.ui.settings_spinbox_performance_processing_delay.setValue(int(self.processing_delay))
        self.ui.settings_spinbox_performance_maximal_timeout.setValue(int(self.timeout))
        self.ui.settings_spinbox_performance_maximal_workers.setValue(int(self.workers))
        self.ui.settings_spinbox_performance_maximal_retries.setValue(int(self.max_retries))
        self.ui.settings_doublespinbox_performance_speed_limit.setValue(self.speed_limit_mb)
        self.ui.settings_spinbox_performance_network_delay.setValue(int(self.delay))

        # Apply stuff to eaf_base_api and refresh cores
        shared_functions.config.timeout = self.timeout
        shared_functions.config.request_delay = self.delay
        shared_functions.config.max_bandwidth_mb = self.speed_limit_mb
        shared_functions.config.max_retries = self.max_retries
        shared_functions.refresh_clients()
        shared_functions.enable_logging()


    def save_user_settings(self):
        """Saves the user settings to the configuration file based on the UI state."""
        # Save quality setting
        conf.read("config.ini")
        for quality, radio_button in self.map_quality.items():
            if radio_button.isChecked():
                conf.set("Video", "quality", quality)

        # Save threading mode
        for mode, radio_button in self.map_threading_mode.items():
            if radio_button.isChecked():
                conf.set("Performance", "threading_mode", mode)

        for language, radio_button in self.map_gui_language.items():
            if radio_button.isChecked():
                conf.set("UI", "language", language)

        for model_video_type, radio_button in self.map_model_videos.items():
            if radio_button.isChecked():
                conf.set("Video", "model_videos", model_video_type)

        # Save other settings
        conf.set("Performance", "semaphore", str(self.ui.settings_spinbox_performance_simultaneous_downloads.value()))
        conf.set("Performance", "speed_limit", str(self.ui.settings_doublespinbox_performance_speed_limit.value()))
        conf.set("Video", "result_limit", str(self.ui.settings_spinbox_videos_result_limit.value()))
        conf.set("Video", "output_path", self.ui.settings_lineedit_videos_output_path.text())
        conf.set("Performance", "timeout", str(self.ui.settings_spinbox_performance_maximal_timeout.value()))
        conf.set("Performance", "workers", str(self.ui.settings_spinbox_performance_maximal_workers.value()))
        conf.set("Video", "delay", str(self.ui.settings_spinbox_performance_network_delay.value()))
        conf.set("Performance", "retries", str(self.ui.settings_spinbox_performance_maximal_retries.value()))
        conf.set("Setup", "update_checks",
                 "true" if self.ui.settings_checkbox_system_update_checks.isChecked() else "false")
        conf.set("Setup", "internet_checks",
                 "true" if self.ui.settings_checkbox_system_internet_checks.isChecked() else "false")
        conf.set("Setup", "anonymous_mode",
                 "true" if self.ui.settings_checkbox_system_enable_anonymous_mode.isChecked() else "false")
        conf.set("Video", "write_metadata",
                 "true" if self.ui.settings_checkbox_videos_write_metadata.isChecked() else "false")
        conf.set("Video", "skip_existing_files",
                 "true" if self.ui.settings_checkbox_videos_skip_existing_files.isChecked() else "false")
        conf.set("Video", "directory_system",
                 "true" if self.ui.settings_checkbox_videos_use_directory_system.isChecked() else "false")
        conf.set("UI", "custom_font",
                 "true" if self.ui.settings_checkbox_ui_custom_font.isChecked() else "false")
        conf.set("UI", "font_size", str(self.ui.settings_spinbox_ui_font_size.value()))
        conf.set("Video", "video_id_as_filename", "true" if self.ui.settings_checkbox_videos_use_video_id_as_filename.isChecked() else "false")
        conf.set("Video", "supress_errors", "true" if self.ui.settings_checkbox_system_supress_errors.isChecked() else "false")
        conf.set("Performance", "processing_delay", str(self.ui.settings_spinbox_performance_processing_delay.value()))
        conf.set("Video", "direct_download", "true" if self.ui.settings_checkbox_videos_direct_download.isChecked() else "false")
        conf.set("Setup", "activate_logging", "true" if self.ui.settings_checkbox_system_enable_network_logging.isChecked() else "false")

        with open("config.ini", "w") as config_file:  # type: TextIOWrapper
            conf.write(config_file)

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
        global FORCE_PORTABLE_RUN
        if not self.license.check_license():
            self.switch_to_license()
            return

        if not self.disclaimer.check_disclaimer():
            self.switch_to_disclaimer()
            return

        if not self.donation_nag.check_donation_nag():
            self.switch_to_donation_nag()
            return

        if conf["Setup"]["activate_logging"] == "not_set":
            self.handle_network_logging()
            return

        if not FORCE_PORTABLE_RUN:
            if sys.platform == "darwin":
                self.ui.CentralStackedWidget.setCurrentIndex(0)
                return

            if conf["Setup"]["install"] == "unknown":
                self.switch_to_install_dialog()
                return

        self.ui.CentralStackedWidget.setCurrentIndex(0)

    def handle_network_logging(self):
        self.switch_to_logging()
        self.ui.button_server_enable_logging.setStyleSheet(self.stylesheets["button_green"])
        self.ui.button_server_disable_logging.setStyleSheet(self.stylesheets["button_reset"])
        self.ui.button_server_enable_logging.clicked.connect(self.enable_logging)
        self.ui.button_server_disable_logging.clicked.connect(self.disable_logging)

    def start_single_video(self):
        """
        Starts the download of a single video.
        This still uses the tree widget because this makes it easier to track the total progress, as I've already
        implemented this feature into the tree widget and I don't want to write code 2 times
        """
        url = self.ui.download_lineedit_url.text()
        self.logger.info(f"Starting a single shot download for -->: {url}")
        self.add_to_tree_widget_thread(iterator=url)

    def start_model(self, url=None):
        """Starts the model downloads"""
        if isinstance(url, str):
            model = url

        else:
            model = self.ui.download_lineedit_model_url.text()

        self.logger.info(f"Checking model: {url}")
        if shared_functions.pornhub_pattern.match(model):
            model_object = shared_functions.ph_client.get_user(model)
            videos = model_object.videos
            uploads = model_object.uploads

            if self.model_videos_type == "both":
                videos = chain(uploads, videos)

            elif self.model_videos_type == "featured":
                videos = videos

            elif self.model_videos_type == "uploads":
                videos = uploads

        elif shared_functions.hqporner_pattern.match(model):
            try:
                videos = shared_functions.hq_client.get_videos_by_actress(name=model)

            except InvalidActress_HQ:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message="Invalid Actress URL!")
                return

            except NoVideosFound:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message="No videos found. This is probably an error and will be reported.", needs_network_log=True)
                return

        elif shared_functions.eporner_pattern.match(model):
            videos = shared_functions.ep_client.get_pornstar(url=model, enable_html_scraping=True).videos()

        elif shared_functions.xnxx_pattern.match(model):
            videos = shared_functions.xn_client.get_user(url=model).videos

        elif "xvideos" and "model" or "pornstar" in str(model):
            videos = shared_functions.xv_client.get_pornstar(url=model).videos

        elif "xvideos" and "channel" in str(model):
            videos = shared_functions.xv_client.get_channel(url=model).videos

        else:
            videos = None
            ui_popup(self.tr("The model URL you entered seems to be invalid. Please check your input",
                             disambiguation=None))

        self.add_to_tree_widget_thread(videos)

    def start_playlist(self):
        url = self.ui.download_lineedit_playlist_url.text()
        self.logger.info(f"Requesting playlist videos for -->: {url}")
        playlist = shared_functions.ph_client.get_playlist(url)
        videos = playlist.sample()
        self.logger.debug("Got playlist videos!")
        self.add_to_tree_widget_thread(iterator=videos)

    def open_file_dialog(self):
        """This opens and processes urls in the file"""
        dialog = QFileDialog()
        file, types = dialog.getOpenFileName()
        self.logger.info(f"Iterating over: {file}")
        self.ui.download_lineedit_file.setText(file)
        self.start_file_processing()

    def start_file_processing(self):
        file = self.ui.download_lineedit_file.text()
        self.url_thread = AddUrls(file)
        self.url_thread.signals.total_progress.connect(self.update_total_progressbar)
        self.url_thread.signals.stop_undefined_range.connect(self.stop_undefined_range)
        self.url_thread.signals.start_undefined_range.connect(self.start_undefined_range)
        self.url_thread.signals.url_iterators.connect(self.receive_url_result)
        self.threadpool.start(self.url_thread)

    def receive_url_result(self, iterator, model_iterator):
        self.logger.debug(f"Received Video Iterator ({len(iterator)} videos)")
        self.logger.debug(f"Received Model Iterator ({len(model_iterator)} urls)")
        direct_download = self.direct_download
        self.direct_download = False # Makes sense, trust me
        self.logger.debug("Processing Videos...")
        self.add_to_tree_widget_thread(iterator)
        self.logger.debug("Processing Models...")
        for url in model_iterator:
            self.start_model(url)

        if direct_download:
            self.download_tree_widget()

    def search(self):
        """Does a simple search for videos without filters on selected website"""
        query = self.ui.download_lineedit_search_query.text()
        self.logger.debug(f"Searching with query: {query}")
        if self.ui.download_radio_search_website_pornhub.isChecked():
            videos = shared_functions.ph_client.search(query)

        elif self.ui.download_radio_search_website_xvideos.isChecked():
            videos = shared_functions.xv_client.search(query)

        elif self.ui.download_radio_search_website_hqporner.isChecked():
            try:
                videos = shared_functions.hq_client.search_videos(query)

            except NoVideosFound:
                handle_error_gracefully(self, data=video_data.consistent_data, error_message=f"No videos found for query: {query}")
                return


        elif self.ui.download_radio_search_website_eporner.isChecked():
            videos = shared_functions.ep_client.search_videos(query, sorting_gay="", sorting_order="", sorting_low_quality="",
                                                              page=1,
                                                              per_page=self.result_limit, enable_html_scraping=True)

        elif self.ui.download_radio_search_website_xnxx.isChecked():
            videos = shared_functions.xn_client.search(query).videos

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
        is_reverse = self.ui.main_checkbox_tree_show_videos_reversed.isChecked()
        is_checked = self.ui.main_checkbox_tree_do_not_clear_videos.isChecked()
        self.add_to_tree_widget_thread_ = AddToTreeWidget(iterator=iterator, is_reverse=is_reverse,
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

    def tree_widget_finished(self):
        if self.direct_download:
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
        # ADAPTION
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
        video_data.clean_dict(video_id)
        self.semaphore.release()
        widgets = self.progress_widgets.pop(video_id, None)
        if widgets:
            for widget in widgets.values():
                self.ui.progress_gridlayout_progressbar.removeWidget(widget)
                widget.deleteLater()

        downloaded_videos = int(conf.get("Sponsoring", "downloaded_videos"))
        downloaded_videos += 1
        conf.set("Sponsoring", "downloaded_videos", str(downloaded_videos))
        with open("config.ini", "w") as config_file:  # type:TextIOWrapper
            conf.write(config_file)

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
        self.range_ui.spinbox_range_end.setMaximum(item_count)
        self.range_ui.button_range_apply_index.clicked.connect(self.process_range_of_items_selection_index)
        self.range_ui.button_range_apply_time.clicked.connect(self.process_range_of_items_selection_time)
        self.range_ui.button_range_apply_author.clicked.connect(self.process_range_of_items_author)

    def select_all_items(self):
        """Selects all items from the tree widget"""
        self.logger.info("Selected all items")
        root = self.ui.treeWidget.invisibleRootItem()
        item_count = root.childCount()
        for i in range(item_count):
            item = root.child(i)
            item.setCheckState(0, Qt.CheckState.Checked)

    def process_range_of_items_selection_index(self):
        start = self.range_ui.spinbox_range_start.value()
        end = self.range_ui.spinbox_range_end.value()
        root = self.ui.treeWidget.invisibleRootItem()

        # Adjust start and end indices to match tree widget indexing
        start -= 1
        end -= 1

        for i in range(start, end + 1):  # Adjust the range to be inclusive of the end
            item = root.child(i)
            item.setCheckState(0, Qt.CheckState.Checked)

    def process_range_of_items_selection_time(self):
        start_time = int(self.range_ui.lineedit_range_start.text())
        end_time = int(self.range_ui.lineedit_range_end.text())
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
        name = str(self.range_ui.lineedit_range_author.text())
        root = self.ui.treeWidget.invisibleRootItem()

        for i in range(root.childCount()):
            item = root.child(i)
            author = str(item.data(1, Qt.ItemDataRole.UserRole))
            if str(author).lower() == str(name).lower():
                item.setCheckState(0, Qt.CheckState.Checked)

    def set_thumbnail(self, item_current, item_previous=None): # Won's use the previous item
        """Replace your QLabel code with this, feeding the graphicsView."""
        if time.time() - self.last_thumbnail_change < 0.5: # Bypasses a bug
            return

        self.last_thumbnail_change = time.time()
        if __build__ == "android":
            return

        item = item_current
        gv = self.ui.graphicsView

        # clear if nothing to show
        if item is None or self._anonymous_mode:
            self._pixmap_item.setPixmap(QPixmap())
            return

        thumbnail = item.data(3, Qt.ItemDataRole.UserRole)
        if not "http" in thumbnail:
            self.logger.warning("Thumbnail not available for. This is not an error.")
            return

        if not thumbnail:
            self._pixmap_item.setPixmap(QPixmap())
            return

        try:
            pixmap = QPixmap()
            # your custom referer logic…
            if "hqporner" in thumbnail:
                shared_functions.core.session.headers["Referer"] = "https://hqporner.com"

            pixmap.loadFromData(shared_functions.core.fetch(thumbnail, get_bytes=True))
            if "hqporner" in thumbnail:
                del shared_functions.core.session.headers['Referer']

            self.logger.info("Fetched thumbnail!")

            # 1) stash the full-res copy
            self._full_pixmap = pixmap

            # 2) show it in the scene
            self._pixmap_item.setPixmap(pixmap)
            self._scene.setSceneRect(QRectF(pixmap.rect()))
            # 3) initial fit/fill
            gv.fitInView(self._scene.sceneRect(),
                         Qt.AspectRatioMode.KeepAspectRatioByExpanding)

        except Exception:
            self.logger.error("Failed to load thumbnail", exc_info=True)
            self._pixmap_item.setPixmap(QPixmap())

    """
    The following functions are used to connect data between Threads and the Main UI
    """

    def create_video_progressbar(self, video_id, title):
        progressbar_themes = [
            "progressbar_eporner", "progressbar_pornhub", "progressbar_missav", "progressbar_hqporner", "progressbar_xhamster",
            "progressbar_xnxx", "progressbar_xvideos", "progressbar_eporner"
        ]
        truncated_title = (title[:30] + '...') if len(title) > 30 else title
        label = QLabel(truncated_title)
        progressbar = QProgressBar()
        progressbar.setStyleSheet(self.stylesheets[random.choice(progressbar_themes)])
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
            switch_login_button_state(self)

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
        if self.ui.tools_radio_top_porn_week.isChecked():
            sort = hq_Sort.WEEK

        elif self.ui.tools_radio_top_porn_month.isChecked():
            sort = hq_Sort.MONTH

        elif self.ui.tools_radio_top_porn_all_time:
            sort = hq_Sort.ALL_TIME

        else:
            sort = None

        try:
            videos = shared_functions.hq_client.get_top_porn(sort_by=sort)

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
        if self.activate_logging is False:
            self.logger.info("You have disabled IPv6 connection to my server. Won't check for updates...")
            return

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

    if language == "system":
        # Get the system's locale
        locale = QLocale.system()
        language_code = locale.name()

    else:
        language_code = language
    # Try loading the specific regional translation

    path = f":/translations/translations/{language_code}.qm"
    translator = QTranslator(app)
    if translator.load(path):
        logger.debug(f"Startup: [1/5] {language_code} translation loaded")
    else:
        # Try loading a more general translation if specific one fails
        general_language_code = language_code.split('_')[0]
        path = f":/translations/translations/{general_language_code}.qm"
        if translator.load(path):
            logger.debug(f"{general_language_code} translation loaded as fallback")
        else:
            logger.debug(f"Failed to load {language_code} translation")

    app.installTranslator(translator)
    app.setStyleSheet(load_stylesheet(":/style/stylesheets/stylesheet.qss"))
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
            file, type_ = QFileDialog().getOpenFileName()
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