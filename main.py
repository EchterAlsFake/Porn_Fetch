import time
import sys
import os.path
import argparse
import markdown
import zipfile
import shutil
import tarfile
import src.frontend.resources

from itertools import islice
from threading import Event
from pathlib import Path
from pypresence import Presence, exceptions

from hqporner_api.api import Sort as hq_Sort
from phub import consts
from base_api.modules import consts as bs_consts
from base_api.base import Core

from src.backend.shared_functions import *
from src.backend.shared_gui import *
from src.backend.class_help import *
from src.frontend.ui_form_desktop import Ui_Porn_Fetch_Widget
from src.frontend.License import Ui_License
from src.frontend.range_selector import Ui_Form

from PySide6.QtCore import (QFile, QTextStream, Signal, QRunnable, QThreadPool, QObject, QSemaphore, Qt, QLocale,
                            QTranslator, QCoreApplication)
from PySide6.QtWidgets import (QWidget, QApplication, QInputDialog, QTreeWidgetItem, QButtonGroup, QFileDialog,
                               QPushButton)
from PySide6.QtGui import QIcon, QFont

"""
Copyright (C) 2023-2024 Johannes Habel

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

__license__ = "GPL 3"
__version__ = "3.3"
__build__ = "desktop"  # android or desktop
__author__ = "Johannes Habel"
__next_release__ = "3.4"
discord_id = "1224629014032023563"  # Used for rich presence
discord_image = "logo_transparent"
total_segments = 0
downloaded_segments = 0
last_index = 0
stop_flag = Event()
invalid_input_string = QCoreApplication.tr("Wrong Input, please verify the URL, category or actress!", None)
ffmpeg_features = True
ffmpeg_path = None
urls = ["https://www.pornhub.com", "https://www.eporner.com", "https://www.hqporner.com", "https://www.xnxx.com",
        "https://www.xvideos.com"]

url_linux = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
url_windows = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
ffmpeg_linux = "ffmpeg-7.0-essentials_build"
ffmpeg_windows = "ffmpeg-6.1-amd64-static"


class Signals(QObject):
    """Signals for the Download class"""
    # Progress Signals
    progress_single = Signal(int)
    completed = Signal()
    progress = Signal(int, int)
    progress_hqporner = Signal(int, int)
    progress_eporner = Signal(int, int)
    progress_xnxx = Signal(int, int)
    progress_xvideos = Signal(int, int)
    total_progress = Signal(int, int)
    progress_video = Signal(object)
    ffmpeg_progress = Signal(int, int)

    # Ranges
    start_undefined_range = Signal()
    stop_undefined_range = Signal()
    data = Signal(list)

    # Other (I don't remember)
    text_data = Signal(list)

    # URL Thread
    url_iterators = Signal(list, list, list)

    # Operations
    finished = Signal()
    clear_signal = Signal()
    get_total = Signal(str, str)
    result = Signal(bool)

    # Errors
    error_signal = Signal(str)


class License(QWidget):
    """License class to display the GPL 3 License to the user."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_widget = None
        self.conf = ConfigParser()
        self.conf.read("config.ini")

        self.ui = Ui_License()
        self.ui.setupUi(self)
        self.ui.button_accept.clicked.connect(self.accept)
        self.ui.button_deny.clicked.connect(self.denied)

    def check_license_and_proceed(self):
        if self.conf["License"]["accepted"] == "true":
            self.show_main_window()

        else:
            self.show()  # Show the license widget

    def accept(self):
        self.conf.set("License", "accepted", "true")
        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)
            config_file.close()

        self.show_main_window()

    def denied(self):
        self.conf.set("License", "accepted", "false")
        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)
            config_file.close()
            logger_error("License was denied, closing Porn Fetch")
            self.close()
            sys.exit(0)  # exiting if user denied

    def show_main_window(self):
        """ If license was accepted, the License widget is closed and the main widget will be shown."""
        self.close()
        logger_debug("Startup: [2/5] License accepted")
        self.main_widget = Porn_Fetch()
        self.main_widget.show()


class CheckUpdates(QRunnable):
    def __init__(self):
        super(CheckUpdates, self).__init__()
        self.signals = Signals()

    def run(self):
        url = f"https://github.com/EchterAlsFake/Porn_Fetch/releases/tag/{__next_release__}"
        if requests.get(url).status_code == 200:
            self.signals.result.emit(True)

        else:
            self.signals.result.emit(False)


class CheckInternet(QRunnable):
    def __init__(self):
        super(CheckInternet, self).__init__()
        self.signals = Signals()

    def run(self):
        try:
            for url in urls:
                if not requests.get(url).status_code == 200:
                    self.signals.result.emit(False)
                    return

        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError, ConnectionResetError,
                ConnectionError, requests.exceptions.HTTPError):
            self.signals.result.emit(False)

        else:
            self.signals.result.emit(True)


class AddToTreeWidget(QRunnable):
    def __init__(self, iterator, search_limit, data_mode, reverse, stop_flag, is_checked):
        super(AddToTreeWidget, self).__init__()
        self.signals = Signals()
        self.iterator = iterator
        self.search_limit = search_limit
        self.data_mode = data_mode
        self.reverse = reverse
        self.stop_flag = stop_flag
        self.is_checked = is_checked

    def process_video(self, video, index):
        title = video.title
        disabled = QCoreApplication.tr("Disabled", None)
        duration = disabled
        author = disabled

        # Checks which mode is selected by the user and loads the video attributes
        if self.data_mode == 1:
            if isinstance(video, (hq_Video, xn_Video, xv_Video)):
                duration = str(video.length)

                if hasattr(video, 'pornstars'):
                    author = video.pornstars[0] if video.pornstars else "unknown"

                else:
                    author = video.author if hasattr(video, 'author') and video.author else "unknown"

            elif isinstance(video, Video):
                duration = round(video.duration.seconds / 60)
                author = video.author.name

            elif isinstance(video, ep_Video):
                duration = round(int(video.length) / 60)
                author = video.author

        # Handling exceptions for missing author in xn_Video
        if isinstance(video, xn_Video) and not hasattr(video, 'pornstars'):
            author = "unknown"

        print(
            f"\r\033[K[{Fore.LIGHTCYAN_EX}{index}/{self.search_limit}]{Fore.RESET}{str(title)} Successfully processed!",
            end='', flush=True)
        return [str(title), str(author), str(duration), str(index), video]

    def run(self):
        self.signals.clear_signal.emit()
        self.signals.start_undefined_range.emit()
        global last_index

        if self.is_checked:
            start = last_index + 1  # Videos won't be cleared from tree widget, so we need to set the last known index
            self.search_limit += last_index + 1

        else:
            start = 1

        try:
            logger_debug(f"Result Limit: {str(self.search_limit)}")

            if self.reverse:
                logger_debug("Reversing Videos. This may take some time...")

                # Use islice to limit the number of items fetched from the iterator
                videos = list(islice(self.iterator, self.search_limit))
                videos.reverse()  # Reverse the list (to show videos in reverse order)

            else:
                videos = islice(self.iterator, self.search_limit)

            self.signals.stop_undefined_range.emit()

            for i, video in enumerate(videos, start=start):
                if self.stop_flag.is_set():
                    return

                last_index += 1
                try_attempt = True
                while try_attempt:
                    try:
                        if i == self.search_limit + 1:
                            break  # The search limit prevents an infinite loop

                        try:
                            text_data = self.process_video(video, i)
                        except errors.RegexError as e:
                            logger_error(f"Warning: a Regex Error occurred. This must not be an error, but could be one!"
                                         f" -->: {e}")

                            text_data = [str(video.title), str("Unknown"), str("Unknown"), str(i), video]

                        self.signals.progress.emit(self.search_limit, i)  # sends the current progress
                        self.signals.text_data.emit(text_data)  # sends the data to the main class
                        try_attempt = False  # Processing succeeded, move to the next video

                    except errors.NoResult:
                        try_attempt = False  # No result, move to the next video

                    except (errors.MaxRetriesExceeded, IndexError, ConnectionError) as e:
                        logger_error(f"""
Rate limited by PornHub, waiting for 5 seconds...

Note: If this error persists, please close the application and report the following error.

Error: {e}""")

                    except (ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError):
                        self.signals.error_signal("""
There's a problem with your internet access... Are certain Porn sites blocked by a firewall or your ISP?""")
                        break

        finally:
            self.signals.finished.emit()


class DownloadThread(QRunnable):
    """Refactored threading class to download videos with improved performance and logic."""

    def __init__(self, video, quality, output_path, threading_mode, workers, timeout, stop_flag):
        super().__init__()
        self.video = video
        self.ffmpeg = None
        self.quality = quality
        self.output_path = output_path
        self.threading_mode = threading_mode
        self.signals = Signals()
        self.stop_flag = stop_flag
        self.workers = int(workers)
        self.timeout = int(timeout)
        self.video_progress = {}
        self.last_update_time = 0
        self.progress_signals = {
            'pornhub': self.signals.progress,
            'hqporner': self.signals.progress_hqporner,
            'eporner': self.signals.progress_eporner,
            'xnxx': self.signals.progress_xnxx,
            'xvideos': self.signals.progress_xvideos,
        }

    def generic_callback(self, pos, total, signal, video_source, ffmpeg=False):
        """Generic callback function to emit progress signals with rate limiting."""
        current_time = time.time()
        if self.stop_flag.is_set():
            return

        if ffmpeg:
            self.update_ffmpeg_progress(pos, total)
            signal.emit(pos, total)

        else:
            # Emit signal for individual progress
            if video_source == "hqporner" or video_source == "eporner":

                # Check if the current time is at least 0.5 seconds greater than the last update time
                if current_time - self.last_update_time < 0.5:
                    # If not, do not update the progress and return immediately
                    return

                scaling_factor = 1024 * 1024
                pos = int(pos / scaling_factor)
                total = int(total / scaling_factor)

            signal.emit(pos, total)
            # Update total progress only if the video source uses segments
            if video_source not in ['hqporner', 'eporner']:
                self.update_total_progress(ffmpeg)

        # Update the last update time to the current time
        self.last_update_time = current_time

    def update_ffmpeg_progress(self, pos, total):
        """Update progress for ffmpeg downloads."""
        print(f"\r\033[KProgress: [{pos} / 100]", end='', flush=True)  # I don't know why, but this fixes the progress.
        video_title = self.video.title
        self.video_progress[
            video_title] = pos / total * 100  # video title as video id, to keep track which video has how many progress done
        total_progress = sum(self.video_progress.values()) / len(self.video_progress)
        self.signals.total_progress.emit(total_progress, 100)

    def update_total_progress(self, ffmpeg):
        """Update total download progress."""
        if not ffmpeg:
            global downloaded_segments
            downloaded_segments += 1
            self.signals.total_progress.emit(downloaded_segments, total_segments)

    def run(self):
        """Run the download in a thread, optimizing for different video sources and modes."""

        try:
            logger_debug(f"Downloading Video to: {self.output_path}")
            if self.threading_mode == "FFMPEG" or self.threading_mode == download.FFMPEG:
                self.ffmpeg = True

            if isinstance(self.video, Video):  # Assuming 'Video' is the class for Pornhub
                self.threading_mode = resolve_threading_mode(workers=self.workers, timeout=
                self.timeout, mode=self.threading_mode, video=self.video)
                video_source = "pornhub"
                path = self.output_path
                logger_debug("Starting the Download!")
                try:
                    self.video.download(downloader=self.threading_mode, path=path, quality=self.quality,
                                        display=lambda pos, total: self.generic_callback(pos, total,
                                                                                         self.signals.progress,
                                                                                         video_source, self.ffmpeg))

                except TypeError:
                    self.video.download(downloader=self.threading_mode, path=path, quality=self.quality,
                                        display=lambda pos, total: self.generic_callback(pos, total,
                                                                                         self.signals.progress,
                                                                                         video_source, self.ffmpeg))

            # We need to specify the sources, so that it knows which individual progressbar to use
            elif isinstance(self.video, hq_Video):
                video_source = "hqporner"
                self.video.download(quality=self.quality, path=self.output_path,
                                    callback=lambda pos, total: self.generic_callback(pos, total,
                                                                                      self.signals.progress_hqporner,
                                                                                      video_source, self.ffmpeg))

            elif isinstance(self.video, ep_Video):
                video_source = "eporner"
                self.video.download(quality=self.quality, path=self.output_path,
                                    callback=lambda pos, total: self.generic_callback(pos, total,
                                                                                      self.signals.progress_eporner,
                                                                                      video_source, self.ffmpeg))

            elif isinstance(self.video, xn_Video):
                video_source = "xnxx"
                self.video.download(downloader=self.threading_mode, path=self.output_path,
                                    quality=self.quality,
                                    callback=lambda pos, total: self.generic_callback(pos, total,
                                                                                      self.signals.progress_xnxx,
                                                                                      video_source, self.ffmpeg))

            elif isinstance(self.video, xv_Video):
                video_source = "xvideos"
                self.video.download(downloader=self.threading_mode, path=self.output_path,
                                    quality=self.quality,
                                    callback=lambda pos, total: self.generic_callback(pos, total,
                                                                                      self.signals.progress_xvideos,
                                                                                      video_source, self.ffmpeg))

                # ... other video types ...

            # Emit the completed signal when done
            self.signals.completed.emit()

        finally:
            if ffmpeg_features:
                os.rename(f"{self.output_path}", f"{self.output_path}_.tmp")
                logger_debug(f"FFMPEG PATH: {ffmpeg_path}")
                cmd = [ffmpeg_path, "-i", f"{self.output_path}_.tmp", "-c", "copy", self.output_path]
                ff = FfmpegProgress(cmd)
                for progress in ff.run_command_with_progress():
                    self.signals.ffmpeg_progress.emit(round(progress), 100)

                os.remove(f"{self.output_path}_.tmp")
                write_tags(path=self.output_path, video=self.video, ffmpeg_path=ffmpeg_path)
            else:
                logger_debug("FFMPEG features disabled, writing tags and converting the video won't be available!")


class QTreeWidgetDownloadThread(QRunnable):
    """Threading class for the QTreeWidget (sends objects to the download class defined above)"""

    def __init__(self, treeWidget, semaphore, quality, threading_mode, stop_flag):
        super(QTreeWidgetDownloadThread, self).__init__()
        self.treeWidget = treeWidget
        self.semaphore = semaphore
        self.signals = Signals()
        self.quality = quality
        self.threading_mode = threading_mode
        self.stop_flag = stop_flag

    def run(self):
        self.signals.start_undefined_range.emit()
        video_objects = []

        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)
            checkState = item.checkState(0)
            if checkState == Qt.Checked:
                video_objects.append(item.data(0, Qt.UserRole))

        if not self.threading_mode == "FFMPEG":
            logger_debug("Getting segments...")
            global total_segments, downloaded_segments
            total_segments = sum(
                [len(list(video.get_segments(quality=self.quality))) for video in video_objects if
                 hasattr(video, 'get_segments')])
            logger_debug("Got segments")
            # This basically looks how many segments exist in all videos together, so that we can calculate the total
            # progress

        else:
            logger_debug("Progress tracking: FFMPEG")
            # FFMPEG has always 0-100 as progress callback, that is why I specify 100 for each video instead of the
            # total segments
            counter = 0
            for _ in video_objects:
                counter += 100

            total_segments = counter

        downloaded_segments = 0
        self.signals.stop_undefined_range.emit()

        for video in video_objects:
            self.semaphore.acquire()  # Trying to start the download if the thread isn't locked
            if stop_flag.is_set():
                return
            logger_debug("Semaphore Acquired")
            self.signals.progress_video.emit(video)  # Now emits the video to the main class for further processing


class VideoLoaderSignals(QObject):
    """Signals for the Video Loader class to handle the loading of videos"""
    loaded = Signal(object, str, str, object, str, bool, str)
    error = Signal(str)


class VideoLoader(QRunnable):
    def __init__(self, url, output_path, api_language, threading_mode, directory_system, quality, delay):
        super(VideoLoader, self).__init__()
        self.url = url
        self.output_path = output_path
        self.api_language = api_language
        self.threading_mode = threading_mode
        self.directory_system = directory_system
        self.quality = quality
        self.signals = VideoLoaderSignals()
        self.delay = delay

    def run(self):
        try:
            video = check_video(self.url, language=self.api_language, delay=self.delay)

            if video is False:
                ui_popup(invalid_input_string)

            else:
                title = video.title

                if isinstance(video, Video):
                    author = video.author.name

                elif isinstance(video, hq_Video):
                    pornstars = video.pornstars
                    author = pornstars[0] if pornstars else "no_author_found"
                else:
                    author = video.author

                output_path = Path(self.output_path)
                stripped_title = Core().strip_title(title)  # Strip the title so that videos with special chars can be
                # saved on windows. It would raise an OSError otherwise

                if self.directory_system:  # If the directory system is enabled, this will create an additional folder
                    author_path = output_path / author
                    author_path.mkdir(parents=True, exist_ok=True)
                    output_file_path = author_path / f"{stripped_title}.mp4"

                else:
                    output_file_path = output_path / f"{stripped_title}.mp4"

                # Emit the loaded signal with all the required information
                self.signals.loaded.emit(video, author, stripped_title, output_file_path, self.threading_mode,
                                         self.directory_system, self.quality)

        except Exception as e:
            self.signals.error.emit(str(e))


class FFMPEGDownload(QRunnable):
    """Downloads ffmpeg into the execution path of Porn Fetch"""

    def __init__(self, url, extract_path, mode):
        super().__init__()
        self.url = url
        self.extract_path = extract_path
        self.mode = mode
        self.signals = Signals()

    def run(self):
        # Download the file
        logger_debug(f"Downloading: {self.url}")
        logger_debug("FFMPEG: [1/4] Starting the download")
        with requests.get(self.url, stream=True) as r:
            r.raise_for_status()
            total_length = int(r.headers.get('content-length'))
            self.signals.total_progress.emit(0, total_length)  # Initialize progress bar
            dl = 0
            filename = self.url.split('/')[-1]
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        dl += len(chunk)
                        self.signals.total_progress.emit(dl, total_length)

        logger_debug("FFMPEG: [2/4] Starting file extraction")
        # Extract the file based on OS mode
        if self.mode == "linux" and filename.endswith(".tar.xz"):
            with tarfile.open(filename, "r:xz") as tar:
                total_members = len(tar.getmembers())

                for idx, member in enumerate(tar.getmembers()):
                    if 'ffmpeg' in member.name and (member.name.endswith('ffmpeg')):
                        tar.extract(member, self.extract_path)
                        extracted_path = os.path.join(self.extract_path, member.path)
                        shutil.move(extracted_path, "./")

                    self.signals.total_progress.emit(idx, total_members)

        elif self.mode == "windows" and filename.endswith(".zip"):
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                total = len(zip_ref.namelist())

                for idx, member in enumerate(zip_ref.namelist()):
                    if 'ffmpeg.exe' in member:
                        zip_ref.extract(member, self.extract_path)
                        extracted_path = os.path.join(self.extract_path, member)
                        shutil.move(extracted_path, ".")

                    self.signals.total_progress.emit(idx, total)
        logger_debug("FFMPEG: [3/4] Finished Extraction")
        # Finalize
        self.signals.total_progress.emit(total_length, total_length)  # Ensure progress bar reaches 100%
        os.remove(filename)  # Clean up downloaded archive

        if sys.platform == "linux":
            shutil.rmtree(ffmpeg_linux)

        elif sys.platform == "win32":
            shutil.rmtree(ffmpeg_windows)

        logger_debug("FFMPEG: [4/4] Cleaned Up")
        self.signals.finished.emit()


class Discord(QRunnable):
    """
    The Discord class handles the Pypresence, which is a feature that allows to show your current activity in Discord.
    If enabled, discord will show on your profile, that you are 'playing' Porn Fetch.
    """

    def __init__(self):
        super(Discord, self).__init__()

    def run(self):
        while True:
            try:
                presence = Presence(discord_id)
                presence.connect()
                presence.update(details=f"Porn Fetch (v{__version__})", large_image=discord_image, buttons=
                [{"label": "Visit Project", "url": "https://github.com/EchterAlsFake/Porn_Fetch"}])
                time.sleep(60)  # Delay of 60 seconds, so that the Discord API doesn't get spammed

            except exceptions.DiscordNotFound:
                logger_error("Discord was not found... Pypresence won't be started!")

            except exceptions.InvalidID:
                logger_error("Invalid Discord Application ID. Please report this error, as it shouldn't happen!")

            except exceptions.PyPresenceException as e:
                logger_error(f"Pypresence exception... {e}")


class AddUrls(QRunnable):
    """
    This class is used to add the URLs from the 'open file' function, because the UI doesn't respond until
    all URLs / Models / Search terms have been processed. This is why I made this threading class
    """

    def __init__(self, file, api_language, delay):
        super(AddUrls, self).__init__()
        self.signals = Signals()
        self.file = file
        self.api_language = api_language
        self.delay = delay

    def run(self):
        iterator = []
        model_iterators = []
        search_iterators = []

        with open(self.file, "r") as url_file:
            content = url_file.read().splitlines()

        for idx, line in enumerate(content):
            if len(line) == 0:
                continue

            total = len(content)
            self.signals.total_progress.emit(0, total)

            if line.startswith("model#"):
                line = line.split("#")[1]
                model_iterators.append(line)
                search_iterators.append(line)

            elif line.startswith("search#"):
                query = line.split("#")[1]
                site = line.split("#")[2]
                search_iterators.append({"website" : site,
                                         "query": query})

            else:
                video = check_video(line, language=self.api_language, delay=self.delay)

                if video is not False:
                    iterator.append(video)

                else:
                    ui_popup(invalid_input_string)

            self.signals.total_progress.emit(idx, total)

            self.signals.url_iterators.emit(iterator, model_iterators, search_iterators)


class Porn_Fetch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Variable initialization:
        self.gui_language_map = None
        self.discord_map = None
        self.max_retries = None
        self.workers = None
        self.timeout = None
        self.gui_language = None
        self.semaphore = None
        self.native_languages = None
        self.directory_system_map = None
        self.threading_mode_map = None
        self.threading_map = None
        self.language_map = None
        self.quality_map = None
        self.selected_category = None
        self.excluded_categories_filter = None
        self.client = None
        self.api_language = None
        self.delay = None
        self.search_limit = None
        self.semaphore_limit = None
        self.quality = None
        self.output_path = None
        self.threading_mode = None
        self.threading = None
        self.directory_system = None
        self.total_progress = 0
        self.threadpool = QThreadPool()

        self.conf = ConfigParser()
        self.conf.read("config.ini")

        self.ui = Ui_Porn_Fetch_Widget()
        self.ui.setupUi(self)
        self.button_connectors()  # Connects the buttons to their functions
        self.button_groups()  # Groups the buttons, so that the Radio buttons are split from themselves (hard to explain)
        self.load_style()  # Loads all the User Interface stylesheets
        logger_debug("Startup: [3/5] Initialized the User Interface")
        self.settings_maps_initialization()
        self.load_user_settings()  # Loads the user settings and applies selected values to the UI
        logger_debug("Startup: [4/5] Loaded the user settings")
        self.switch_to_home()  # Switches Porn Fetch to the home widget
        self.check_for_updates()  # Checks if a new version is out, by using the GitHub release tags
        self.check_internet()  # Checks if Porn Fetch can reach all websites
        self.check_ffmpeg()  # Checks and sets up FFmpeg
        self.discord_()  # Discord Rich Presence
        logger_debug("Startup: [5/5] ✔")

        if __build__ == "android":
            self.setup_android()  # Sets up Android, if build mode is Android (handles some UI stuff and things)

    @classmethod
    def load_stylesheet(cls, path):
        """Load stylesheet from a given path with explicit open and close."""
        file = QFile(path)
        if not file.open(QFile.ReadOnly | QFile.Text):
            logger_debug(f"Failed to open {path}")
            return ""
        stylesheet = QTextStream(file).readAll()
        file.close()
        return stylesheet

    def load_style(self):
        """Refactored function to load icons and stylesheets."""
        # Setting icons with a loop if applicable
        icons = {
            self.ui.button_switch_home: "download.svg",
            self.ui.button_switch_settings: "settings.svg",
            self.ui.button_switch_credits: "information.svg",
            self.ui.button_switch_account: "account.svg",
            self.ui.button_switch_tools: "tools.svg",
            self.ui.button_workers_help: "faq.svg",
            self.ui.button_pornhub_delay_help: "faq.svg",
            self.ui.button_threading_mode_help: "faq.svg",
            self.ui.button_semaphore_help: "faq.svg",
            self.ui.button_timeout_help: "faq.svg",
            self.ui.button_directory_system_help: "faq.svg",
            self.ui.button_result_limit_help: "faq.svg",
            self.ui.button_timeout_maximal_retries_help: "faq.svg",
            self.ui.button_help_file: "faq.svg",
            self.ui.discord_rich_presence_help: "faq.svg",
        }
        for button, icon_name in icons.items():
            button.setIcon(QIcon(f":/images/graphics/{icon_name}"))

        self.setWindowIcon(QIcon(":/images/graphics/logo_transparent.ico"))
        # Stylesheets
        stylesheet_paths = {
            "progressbar_pornhub": ":/style/stylesheets/progressbar_pornhub.qss",
            "progressbar_hqporner": ":/style/stylesheets/progressbar_hqporner.qss",
            "progressbar_eporner": ":/style/stylesheets/progressbar_eporner.qss",
            "progressbar_total": ":/style/stylesheets/progressbar_total.qss",
            "progressbar_xnxx": ":/style/stylesheets/progressbar_xnxx.qss",
            "progressbar_xvideos": ":/style/stylesheets/progressbar_xvideos.qss",
            "progressbar_converting": ":/style/stylesheets/progressbar_converting.qss",
            "button_blue": ":/style/stylesheets/stylesheet_button_blue.qss",
            "button_orange": ":/style/stylesheets/stylesheet_button_orange.qss",
            "button_purple": ":/style/stylesheets/stylesheet_button_purple.qss",
            "button_green": ":/style/stylesheets/stylesheet_button_green.qss",
            "buttons_login": ":/style/stylesheets/stylesheet_buttons_login.qss",
            "button_reset": ":/style/stylesheets/stylesheet_button_reset.qss"
        }

        stylesheets = {key: self.load_stylesheet(path) for key, path in stylesheet_paths.items()}

        # Applying stylesheets to specific buttons
        # Simplify this part based on actual UI structure and naming
        self.ui.button_login.setStyleSheet(stylesheets["button_green"])
        self.ui.progressbar_pornhub.setStyleSheet(stylesheets["progressbar_pornhub"])
        self.ui.progressbar_total.setStyleSheet(stylesheets["progressbar_total"])
        self.ui.progressbar_xnxx.setStyleSheet(stylesheets["progressbar_xnxx"])
        self.ui.progressbar_eporner.setStyleSheet(stylesheets["progressbar_eporner"])
        self.ui.progressbar_hqporner.setStyleSheet(stylesheets["progressbar_hqporner"])
        self.ui.progressbar_xvideos.setStyleSheet(stylesheets["progressbar_xvideos"])
        self.ui.progressbar_converting.setStyleSheet(stylesheets["progressbar_converting"])

        self.ui.button_model.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_search.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_download.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_threading_mode_help.setStyleSheet(stylesheets["button_green"])
        self.ui.button_directory_system_help.setStyleSheet(stylesheets["button_green"])
        self.ui.button_semaphore_help.setStyleSheet(stylesheets["button_green"])
        self.ui.button_tree_download.setStyleSheet(stylesheets["button_orange"])
        self.ui.button_tree_unselect_all.setStyleSheet(stylesheets["button_blue"])
        self.ui.button_tree_select_range.setStyleSheet(stylesheets["button_green"])
        self.ui.button_output_path_select.setStyleSheet(stylesheets["button_blue"])
        self.ui.button_login.setStyleSheet(stylesheets["button_blue"])
        self.ui.button_settings_apply.setStyleSheet(stylesheets["button_blue"])
        self.ui.button_get_random_videos.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_get_brazzers_videos.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_list_categories.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_open_file.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_switch_supported_websites.setStyleSheet(stylesheets["button_blue"])
        self.ui.button_hqporner_category_get_videos.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_top_porn_get_videos.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_get_watched_videos.setStyleSheet(stylesheets["buttons_login"])
        self.ui.button_get_liked_videos.setStyleSheet(stylesheets["buttons_login"])
        self.ui.button_get_recommended_videos.setStyleSheet(stylesheets["buttons_login"])
        self.ui.button_timeout_help.setStyleSheet(stylesheets["button_green"])
        self.ui.button_workers_help.setStyleSheet(stylesheets["button_green"])
        self.ui.button_pornhub_delay_help.setStyleSheet(stylesheets["button_green"])
        self.ui.button_result_limit_help.setStyleSheet(stylesheets["button_green"])
        self.ui.button_settings_reset.setStyleSheet(stylesheets["button_reset"])
        self.ui.button_playlist_get_videos.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_view_all_progress_bars.setStyleSheet(stylesheets["button_blue"])
        self.ui.button_tree_stop.setStyleSheet(stylesheets["button_reset"])
        self.ui.button_tree_export_video_urls.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_timeout_maximal_retries_help.setStyleSheet(stylesheets["button_green"])
        self.ui.button_help_file.setStyleSheet(stylesheets["button_green"])
        self.ui.button_download_ffmpeg.setStyleSheet(stylesheets["button_purple"])
        self.header = self.ui.treeWidget.header()
        self.header.resizeSection(0, 300)
        self.header.resizeSection(1, 150)
        self.header.resizeSection(2, 50)

    def check_for_updates(self):
        """Checks for updates in a thread, so that the main UI isn't blocked, until update checks are done"""
        self.update_thread = CheckUpdates()
        self.update_thread.signals.result.connect(self.check_for_updates_result)
        self.threadpool.start(self.update_thread)

    def check_for_updates_result(self, value):
        """Receives the Update result from the thread"""
        if value:
            logger_debug(f"Next release v{__next_release__} found!")
            ui_popup(QCoreApplication.tr(f"""
            Information: A new version of Porn Fetch (v{__next_release__}) is out. I recommend you to update Porn Fetch. 
            Go to: https://github.com/EchterAlsFake/Porn_Fetch/releases/tag/ {__next_release__}""", None))
            self.ui.lineedit_status_update.setText(f"✔, V{__next_release__} is out!")

        else:
            logger_debug("No updates found...")
            self.ui.lineedit_status_update.setText("❌")

    def check_internet(self):
        """Checks the internet access for all sites"""
        self.internet_thread = CheckInternet()
        self.internet_thread.signals.result.connect(self.check_internet_result)
        self.threadpool.start(self.internet_thread)

    def check_internet_result(self, value):
        if value:
            logger_debug("All Internet connection tests passed: ✔")
            self.ui.lineedit_status_internet.setText("✔")

        else:
            logger_error("""
Couldn't access one of the supported websites, make sure you have a stable internet connection and you are outside of 
a firewall. If you are at a public place or using your universities WiFi, your IT-Administrator may have forbidden 
access to specific sites. In this case you can use a VPN / Proxy.""")
            self.ui.lineedit_status_internet.setText("❌, please check your Internet connection!")

    def check_ffmpeg(self):
        # Check if ffmpeg is available in the system PATH
        global ffmpeg_path
        ffmpeg_path = shutil.which("ffmpeg")

        if ffmpeg_path is None:
            # If ffmpeg is not in PATH, check the current directory for ffmpeg binaries
            ffmpeg_binary = "ffmpeg.exe" if os.path.isfile("ffmpeg.exe") else "ffmpeg" if os.path.isfile(
                "ffmpeg") else None

            if ffmpeg_binary is None:
                # If ffmpeg binaries are not found in the current directory, display warning and disable features
                if self.conf.get("Performance", "ffmpeg_warning") == "true":
                    ffmpeg_warning_message = QCoreApplication.tr(
                        """
FFmpeg isn't installed on your system... Some features won't be available:

- The FFmpeg threading mode
- Converting videos into a valid .mp4 format
- Writing tags / metadata into the videos

These features aren't necessary for Porn Fetch, but can be useful for some people.

To automatically install ffmpeg, just head over to the settings and press the magical button, or install ffmpeg in your
local PATH (e.g, through your linux package manager, or through the Windows PATH)

This warning won't be shown again.
                        """, None)
                    ui_popup(ffmpeg_warning_message)
                    self.conf.set("Performance", "ffmpeg_warning", "false")
                    with open("config.ini", "w") as config_file:
                        self.conf.write(config_file)

                self.ui.radio_threading_mode_ffmpeg.setDisabled(True)
                global ffmpeg_features
                ffmpeg_features = False
                logger_error("FFMPEG features have been disabled, because ffmpeg wasn't found on your system.")
                self.ui.lineedit_status_ffmpeg.setText("❌, FFmpeg features won't be available!")
            else:
                # If ffmpeg binary is found in the current directory, set it as the ffmpeg path
                ffmpeg_path = os.path.abspath(ffmpeg_binary)
                self.ui.lineedit_status_ffmpeg.setText(f"✔ -->: {ffmpeg_path}")
        else:
            # If ffmpeg is found in system PATH, use it directly
            ffmpeg_path = shutil.which("ffmpeg")
            consts.FFMPEG_EXECUTABLE = ffmpeg_path
            bs_consts.FFMPEG_PATH = ffmpeg_path
            self.ui.lineedit_status_ffmpeg.setText(f"✔ -->: {ffmpeg_path}")
            logger_debug(f"FFMPEG: {ffmpeg_path}")

    def download_ffmpeg(self):
        if sys.platform == "linux":
            if not os.path.isfile("ffmpeg"):
                self.downloader = FFMPEGDownload(url=url_linux, extract_path=".", mode="linux")

        elif sys.platform == "win32":
            if not os.path.isfile("ffmpeg.exe"):
                self.downloader = FFMPEGDownload(url=url_windows, extract_path=".", mode="windows")

        self.downloader.signals.total_progress.connect(self.update_total_progressbar)
        self.downloader.signals.finished.connect(self.ffmpeg_finished)
        self.threadpool.start(self.downloader)

    @classmethod
    def ffmpeg_finished(cls):
        ui_popup(QCoreApplication.tr("FFmpeg has been installed. Please restart Porn Fetch :)"))

    def discord_(self):
        """
        I don't force anyone to use this. It's disabled by default :)
        """
        if self.discord:
            self.discord_thread = Discord()
            self.threadpool.start(self.discord_thread)
            logger_debug("Started Discord thread")

    def button_groups(self):
        """
        The button groups are needed to tell the radio button which of them are in a group.
        If I don't do this, then you could check all redio buttons at the same time lol"""
        self.group_threading_mode = QButtonGroup()
        self.group_threading_mode.addButton(self.ui.radio_threading_mode_ffmpeg)
        self.group_threading_mode.addButton(self.ui.radio_threading_mode_default)
        self.group_threading_mode.addButton(self.ui.radio_threading_mode_high_performance)

        self.group_quality = QButtonGroup()
        self.group_quality.addButton(self.ui.radio_quality_worst)
        self.group_quality.addButton(self.ui.radio_quality_half)
        self.group_quality.addButton(self.ui.radio_quality_best)

        self.group_api_language = QButtonGroup()
        self.group_api_language.addButton(self.ui.radio_api_language_chinese)
        self.group_api_language.addButton(self.ui.radio_api_language_german)
        self.group_api_language.addButton(self.ui.radio_api_language_french)
        self.group_api_language.addButton(self.ui.radio_api_language_english)
        self.group_api_language.addButton(self.ui.radio_api_language_russian)
        self.group_api_language.addButton(self.ui.radio_api_language_czech)
        self.group_api_language.addButton(self.ui.radio_api_language_italian)
        self.group_api_language.addButton(self.ui.radio_api_language_spanish)
        self.group_api_language.addButton(self.ui.radio_api_language_portuguese)
        self.group_api_language.addButton(self.ui.radio_api_language_dutch)
        self.group_api_language.addButton(self.ui.radio_api_language_japanese)

        self.directory_system_group = QButtonGroup()
        self.directory_system_group.addButton(self.ui.radio_directory_system_no)
        self.directory_system_group.addButton(self.ui.radio_directory_system_yes)

        self.language_group = QButtonGroup()
        self.language_group.addButton(self.ui.radio_ui_language_english)
        self.language_group.addButton(self.ui.radio_ui_language_german)
        self.language_group.addButton(self.ui.radio_ui_language_french)
        self.language_group.addButton(self.ui.radio_ui_language_system_default)
        self.language_group.addButton(self.ui.radio_ui_language_chinese_simplified)

        self.radio_hqporner = QButtonGroup()
        self.radio_hqporner.addButton(self.ui.radio_top_porn_week)
        self.radio_hqporner.addButton(self.ui.radio_top_porn_month)
        self.radio_hqporner.addButton(self.ui.radio_top_porn_all_time)

    def setup_android(self):
        """Sets up for Porn Fetch for Android devices"""
        logger_debug(f"Running on Android: {sys.platform}")
        if not get_output_path():
            self.handle_no_output_path()
            return  # Early return to avoid setting up UI components again at the end.

        self.configure_ui_for_android("/storage/emulated/0/Download/")

    def handle_no_output_path(self):
        ui_popup(
            QCoreApplication.tr("The output path does not exist or is not writable.", None))
        text, ok = QInputDialog.getText(self, "Enter custom Path",
                                        QCoreApplication.tr("Enter custom Path:", None))
        if ok and get_output_path(text):
            ui_popup(
                QCoreApplication.tr(f"Success: {text} will be used for this session!", None))
            self.configure_ui_for_android(text)
        else:
            ui_popup(
                QCoreApplication.tr("Invalid path. The application will now exit.", None))
            sys.exit()

    def configure_ui_for_android(self, path):
        """Disables some things on Android which just don't work yet"""
        self.output_path = path
        self.ui.lineedit_output_path.setText(self.output_path)
        self.ui.lineedit_output_path.setReadOnly(True)
        self.ui.button_open_file.setDisabled(True)
        self.ui.lineedit_file.setText(QCoreApplication.tr("Not supported on Android", None))
        self.ui.radio_threading_mode_ffmpeg.setDisabled(True)
        self.warn_about_high_performance_threading()

        self.ui.gridlayout_progressbar.addWidget(self.ui.label_progress_pornhub)
        self.ui.gridlayout_progressbar.addWidget(self.ui.progressbar_pornhub)
        self.ui.gridlayout_progressbar.addWidget(self.ui.label_total_progress)
        self.ui.gridlayout_progressbar.addWidget(self.ui.progressbar_total)
        self.ui.gridlayout_progressbar.addWidget(self.ui.label_progress_converting)
        self.ui.gridlayout_progressbar.addWidget(self.ui.progressbar_converting)

        self.progress_button = QPushButton("Show Progress")
        self.ui.verticallayout_sidebar.addWidget(self.progress_button)
        self.progress_button.clicked.connect(self.switch_to_all_progress_bars)
        self.ui.scrollarea_status.deleteLater()

    def warn_about_high_performance_threading(self):
        if self.ui.radio_threading_mode_high_performance.isChecked():
            ui_popup(
                QCoreApplication.tr("High Performance threading may cause issues on Android devices.", None))

    @staticmethod
    def reset_pornfetch():
        ui_popup(
            QCoreApplication.tr("Porn Fetch will now reset to its default settings...", None))
        setup_config_file(force=True)
        ui_popup(QCoreApplication.tr("Done! Please restart.", None))

    def toggle_sorting(self):
        if self.ui.checkbox_tree_allow_sorting.isChecked():
            logger_debug("Enabling sorting on the tree widget")
            self.ui.treeWidget.setSortingEnabled(True)

        else:
            logger_debug("Disabling sorting on the tree widget")
            self.ui.treeWidget.setSortingEnabled(False)

    def button_connectors(self):
        """a function to link the buttons to their functions"""
        # Menu Bar Switch Button Connections
        self.ui.button_switch_home.clicked.connect(self.switch_to_home)
        self.ui.button_switch_settings.clicked.connect(self.switch_to_settings)
        self.ui.button_switch_credits.clicked.connect(self.switch_to_credits)
        self.ui.button_switch_account.clicked.connect(self.switch_to_account)
        self.ui.button_switch_supported_websites.clicked.connect(self.switch_to_supported_websites)
        self.ui.button_view_all_progress_bars.clicked.connect(self.switch_to_all_progress_bars)

        # Video Download Button Connections
        self.ui.button_download.clicked.connect(self.start_single_video)
        self.ui.button_model.clicked.connect(self.start_model)
        self.ui.button_tree_download.clicked.connect(self.download_tree_widget)
        self.ui.button_tree_select_range.clicked.connect(self.select_all_items)
        self.ui.button_tree_unselect_all.clicked.connect(self.unselect_all_items)
        self.ui.button_playlist_get_videos.clicked.connect(self.start_playlist)

        # Help Buttons Connections
        self.ui.button_semaphore_help.clicked.connect(button_semaphore_help)
        self.ui.button_threading_mode_help.clicked.connect(button_threading_mode_help)
        self.ui.button_directory_system_help.clicked.connect(button_directory_system_help)
        self.ui.button_workers_help.clicked.connect(maximal_workers_help)
        self.ui.button_timeout_help.clicked.connect(timeout_help)
        self.ui.button_pornhub_delay_help.clicked.connect(pornhub_delay_help)
        self.ui.button_result_limit_help.clicked.connect(result_limit_help)
        self.ui.button_help_file.clicked.connect(open_file_help)
        self.ui.button_timeout_maximal_retries_help.clicked.connect(max_retries_help)
        self.ui.discord_rich_presence_help.clicked.connect(discord_rich_presence_help)

        # Settings
        self.ui.button_settings_apply.clicked.connect(self.save_user_settings)
        self.ui.button_settings_reset.clicked.connect(self.reset_pornfetch)

        # Account
        self.ui.button_login.clicked.connect(self.login)
        self.ui.button_get_watched_videos.clicked.connect(self.get_watched_videos)
        self.ui.button_get_liked_videos.clicked.connect(self.get_liked_videos)
        self.ui.button_get_recommended_videos.clicked.connect(self.get_recommended_videos)

        # Search
        self.ui.button_search.clicked.connect(self.basic_search)

        # HQPorner
        self.ui.button_hqporner_category_get_videos.clicked.connect(self.get_by_category_hqporner)
        self.ui.button_top_porn_get_videos.clicked.connect(self.get_top_porn_hqporner)
        self.ui.button_get_brazzers_videos.clicked.connect(self.get_brazzers_videos)
        self.ui.button_list_categories.clicked.connect(self.list_categories_hqporner)
        self.ui.button_switch_tools.clicked.connect(self.switch_to_hqporner)
        self.ui.button_get_random_videos.clicked.connect(self.get_random_video)

        # EPorner
        self.ui.button_list_categories_eporner.clicked.connect(self.list_categories_eporner)
        self.ui.button_eporner_category_get_videos.clicked.connect(self.get_by_category_eporner)

        # File Dialog
        self.ui.button_output_path_select.clicked.connect(self.open_output_path_dialog)
        self.ui.button_open_file.clicked.connect(self.open_file_dialog)

        # Other stuff idk
        self.ui.checkbox_tree_allow_sorting.checkStateChanged.connect(self.toggle_sorting)
        self.ui.button_tree_select_range.clicked.connect(self.select_range_of_items)
        self.ui.button_tree_stop.clicked.connect(self.switch_stop_state)
        self.ui.button_tree_export_video_urls.clicked.connect(self.export_urls)
        self.ui.button_download_ffmpeg.clicked.connect(self.download_ffmpeg)

    def switch_login_button_state(self):
        """If the user is logged in, I'll change the stylesheets of the buttons"""
        file = QFile(":/style/stylesheets/stylesheet_switch_buttons_login_state.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        stylesheet = stream.readAll()

        self.ui.button_get_liked_videos.setStyleSheet(stylesheet)
        self.ui.button_get_watched_videos.setStyleSheet(stylesheet)
        self.ui.button_get_recommended_videos.setStyleSheet(stylesheet)

    @classmethod
    def switch_stop_state_2(cls):
        global stop_flag
        stop_flag = Event()

    def switch_to_home(self):
        self.ui.stacked_widget_main.setCurrentIndex(0)
        self.ui.stacked_widget_top.setCurrentIndex(0)
        self.ui.stacked_widget_top.setMinimumHeight(220)
        self.ui.scrollarea_stacked_top.setMaximumHeight(220)

    def settings_maps_initialization(self):
        # Maps for settings and corresponding UI elements
        self.quality_map = {
            "best": self.ui.radio_quality_best,
            "half": self.ui.radio_quality_half,
            "worst": self.ui.radio_quality_worst
        }

        self.language_map = {
            "en": self.ui.radio_api_language_english,
            "fr": self.ui.radio_api_language_french,
            "de": self.ui.radio_api_language_german,
            "zh": self.ui.radio_api_language_chinese,
            "nl": self.ui.radio_api_language_dutch,
            "ru": self.ui.radio_api_language_russian,
            "jp": self.ui.radio_api_language_japanese,
            "pt": self.ui.radio_api_language_portuguese,
            "es": self.ui.radio_api_language_spanish,
            "cz": self.ui.radio_api_language_czech,
            "it": self.ui.radio_api_language_italian
        }

        self.threading_mode_map = {
            "threaded": self.ui.radio_threading_mode_high_performance,
            "FFMPEG": self.ui.radio_threading_mode_ffmpeg,
            "default": self.ui.radio_threading_mode_default
        }

        self.directory_system_map = {
            "1": self.ui.radio_directory_system_yes,
            "0": self.ui.radio_directory_system_no
        }

        self.discord_map = {
            "false": self.ui.radio_discord_no,
            "true": self.ui.radio_discord_yes
        }

        self.gui_language_map = {
            "en": self.ui.radio_ui_language_english,
            "de_DE": self.ui.radio_ui_language_german,
            "fr": self.ui.radio_ui_language_french,
            "zh_CN": self.ui.radio_ui_language_chinese_simplified,
            "system": self.ui.radio_ui_language_system_default
        }

    def load_user_settings(self):
        """Loads the user settings from the configuration file and applies them."""

        # Apply settings
        self.quality_map.get(self.conf.get("Video", "quality")).setChecked(True)
        self.threading_mode_map.get(self.conf.get("Performance", "threading_mode")).setChecked(True)
        self.directory_system_map.get(self.conf.get("Video", "directory_system")).setChecked(True)
        self.language_map.get(self.conf.get("Video", "language")).setChecked(True)
        self.discord_map.get(self.conf.get("UI", "discord")).setChecked(True)
        self.gui_language_map.get(self.conf.get("UI", "language")).setChecked(True)
        self.ui.spinbox_semaphore.setValue(int(self.conf.get("Performance", "semaphore")))
        self.ui.spinbox_treewidget_limit.setValue(int(self.conf.get("Video", "search_limit")))
        self.ui.lineedit_output_path.setText(self.conf.get("Video", "output_path"))

        self.semaphore_limit = self.conf.get("Performance", "semaphore")
        self.search_limit = int(self.conf.get("Video", "search_limit"))
        self.output_path = self.conf.get("Video", "output_path")

        self.gui_language = self.conf.get("UI", "language")
        self.quality = self.conf["Video"]["quality"]
        self.threading_mode = self.conf["Performance"]["threading_mode"]
        self.api_language = self.conf["Video"]["language"]
        self.semaphore = QSemaphore(int(self.semaphore_limit))
        self.delay = int(self.conf["Video"]["delay"])
        self.timeout = int(self.conf["Performance"]["timeout"])
        self.workers = int(self.conf["Performance"]["workers"])
        self.max_retries = int(self.conf["Performance"]["retries"])

        self.discord = True if self.conf["UI"]["discord"] == "yes" else False
        self.ui.spinbox_maximal_timeout.setValue(int(self.timeout))
        self.ui.spinbox_maximal_workers.setValue(int(self.workers))
        self.ui.spinbox_pornhub_delay.setValue(int(self.delay))
        consts.MAX_CALL_RETRIES = self.max_retries
        bs_consts.REQUEST_DELAY = self.delay
        bs_consts.MAX_RETRIES = self.max_retries
        consts.FFMPEG_EXECUTABLE = ffmpeg_path
        self.client = Client(delay=self.delay, language=self.api_language)

    def save_user_settings(self):
        """Saves the user settings to the configuration file based on the UI state."""
        # Save quality setting
        for quality, radio_button in self.quality_map.items():
            if radio_button.isChecked():
                self.conf.set("Video", "quality", quality)

        # Save language setting
        for language, radio_button in self.language_map.items():
            if radio_button.isChecked():
                self.conf.set("Video", "language", language)

        # Save threading mode
        for mode, radio_button in self.threading_mode_map.items():
            if radio_button.isChecked():
                self.conf.set("Performance", "threading_mode", mode)

        # Save directory system setting
        for system, radio_button in self.directory_system_map.items():
            if radio_button.isChecked():
                self.conf.set("Video", "directory_system", system)

        for language, radio_button in self.gui_language_map.items():
            if radio_button.isChecked():
                self.conf.set("UI", "language", language)

        for mode, radio_button in self.discord_map.items():
            if radio_button.isChecked():
                self.conf.set("UI", "discord", mode)

        # Save other settings
        self.conf.set("Performance", "semaphore", str(self.ui.spinbox_semaphore.value()))
        self.conf.set("Video", "search_limit", str(self.ui.spinbox_treewidget_limit.value()))
        self.conf.set("Video", "output_path", self.ui.lineedit_output_path.text())
        self.conf.set("Performance", "timeout", str(self.ui.spinbox_maximal_timeout.value()))
        self.conf.set("Performance", "workers", str(self.ui.spinbox_maximal_workers.value()))
        self.conf.set("Video", "delay", str(self.ui.spinbox_pornhub_delay.value()))
        self.conf.set("Performance", "retries", str(self.ui.spinbox_maximal_retries.value()))

        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)

        ui_popup(QCoreApplication.tr("Saved User Settings, please restart Porn Fetch!", None))
        logger_debug("Saved User Settings, please restart Porn Fetch.")

    """
    Switchers for the Stacked Widgets
    """

    def switch_to_account(self):
        self.ui.stacked_widget_top.setCurrentIndex(1)
        self.ui.stacked_widget_main.setCurrentIndex(0)
        self.ui.stacked_widget_top.setMinimumHeight(150)
        self.ui.scrollarea_stacked_top.setMaximumHeight(150)

    def switch_to_hqporner(self):
        self.ui.stacked_widget_main.setCurrentIndex(0)
        self.ui.stacked_widget_top.setCurrentIndex(3)
        self.ui.stacked_widget_top.setMinimumHeight(300)
        self.ui.scrollarea_stacked_top.setMaximumHeight(300)

    def switch_to_settings(self):
        self.ui.stacked_widget_main.setCurrentIndex(1)

    def switch_to_metadata(self):
        self.ui.stacked_widget_main.setCurrentIndex(3)

    def switch_to_credits(self):
        self.ui.stacked_widget_main.setCurrentIndex(2)
        self.show_credits()

    def switch_to_supported_websites(self):
        self.ui.stacked_widget_main.setCurrentIndex(4)
        self.ui.stackedWidget.setCurrentIndex(0)

    def switch_to_all_progress_bars(self):
        self.ui.stacked_widget_top.setCurrentIndex(2)

    def switch_stop_state(self):
        stop_flag.set()
        time.sleep(1)
        self.switch_stop_state_2()

    """
    The following functions are related to the tree widget    
    """

    def add_to_tree_widget_thread(self, iterator, search_limit):
        if self.ui.radio_tree_show_title.isChecked():
            data_mode = 0

        elif self.ui.radio_tree_show_all.isChecked():
            data_mode = 1

        if self.ui.checkbox_tree_show_videos_reversed.isChecked():
            reverse = True

        else:
            reverse = False

        is_checked = self.ui.checkbox_tree_do_not_clear_videos.isChecked()

        self.thread = AddToTreeWidget(iterator=iterator, search_limit=search_limit, data_mode=data_mode,
                                      reverse=reverse, is_checked=is_checked, stop_flag=stop_flag)
        self.thread.signals.text_data.connect(self.add_to_tree_widget_signal)
        self.thread.signals.progress.connect(self.progress_tree_widget)
        self.thread.signals.clear_signal.connect(self.clear_tree_widget)
        self.thread.signals.start_undefined_range.connect(self.start_undefined_range)
        self.thread.signals.stop_undefined_range.connect(self.stop_undefined_range)
        self.thread.signals.finished.connect(self.stop_undefined_range)
        self.threadpool.start(self.thread)

    def add_to_tree_widget_signal(self, data):
        """
        This is the signal for the Tree Widget thread. It receives the data and applies it to the GUI
        """
        title = data[0]
        author = data[1]
        duration = data[2]
        index = data[3]
        video = data[4]

        item = QTreeWidgetItem(self.ui.treeWidget)
        item.setText(0, f"{index}) {title}")
        item.setText(1, author)
        item.setText(2, str(duration))
        item.setData(0, Qt.UserRole, video)
        item.setCheckState(0, Qt.Unchecked)  # Adds a checkbox

    def download_tree_widget(self):
        """
        Starts the thread for downloading the tree widget (All selected videos)
        """
        semaphore = self.semaphore
        treeWidget = self.ui.treeWidget
        quality = self.quality
        download_tree_thread = QTreeWidgetDownloadThread(treeWidget=treeWidget, semaphore=semaphore,
                                                         quality=quality, threading_mode=self.threading_mode,
                                                         stop_flag=stop_flag)
        download_tree_thread.signals.progress_video.connect(self.tree_widget_completed)
        download_tree_thread.signals.start_undefined_range.connect(self.start_undefined_range)
        download_tree_thread.signals.stop_undefined_range.connect(self.stop_undefined_range)
        self.threadpool.start(download_tree_thread)
        self.threadpool.releaseThread()

    def clear_tree_widget(self):
        """
        This (like the name says) clears the tree widget. I try to improve this in the future, to allow the user
        the adding of multiple videos, so that the tree widget doesn't get cleared instantly.
        """
        if not self.ui.checkbox_tree_do_not_clear_videos.isChecked():
            self.ui.treeWidget.clear()

    def export_urls(self):
        video_urls = []

        for i in range(self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(i)
            video_object = item.data(0, Qt.UserRole)
            video_urls.append(video_object.url)

        if len(video_urls) == 0:
            ui_popup(QCoreApplication.tr("No video URLs found. Are there videos in the tree widget?", None))
            return

        file, mode = QFileDialog().getSaveFileName(self)

        try:
            with open(file, "a") as file:
                for url in video_urls:
                    file.write(f"{url}\n")

        except PermissionError:
            ui_popup(QCoreApplication.tr(f"Permission Error, please select a file from your user space,"
                                         f"or run Porn Fetch with admin permissions (not recommended!)",
                                         None))

    def progress_tree_widget(self, total, current):
        """This tracks the progress of the tree widget data"""
        self.ui.progressbar_total.setMaximum(total)
        self.ui.progressbar_total.setValue(current)

    def tree_widget_completed(self, video):
        """
        This emits the video. If the semaphore is released, this function is called, so that the next video can be
        downloaded.
        """
        self.load_video(video)

    def unselect_all_items(self):
        """Unselects all items from the tree widget"""
        root = self.ui.treeWidget.invisibleRootItem()
        item_count = root.childCount()
        for i in range(item_count):
            item = root.child(i)
            item.setCheckState(0, Qt.Unchecked)

    def select_all_items(self):
        """Selects all items from the tree widget"""
        root = self.ui.treeWidget.invisibleRootItem()
        item_count = root.childCount()
        for i in range(item_count):
            item = root.child(i)
            item.setCheckState(0, Qt.Checked)

    def select_range_of_items(self):
        self.widget = Ui_Form()
        self.widget.setupUi(self)
        root = self.ui.treeWidget.invisibleRootItem()
        item_count = root.childCount()
        self.widget.spinbox_range_end.setMaximum(item_count)
        self.widget.button_range_apply.clicked.connect(self.process_range_of_items_selection)

    def process_range_of_items_selection(self):
        start = self.widget.spinbox_range_start.value()
        end = self.widget.spinbox_range_end.value()

        root = self.ui.treeWidget.invisibleRootItem()
        item_count = root.childCount()
        for i in range(item_count):
            if i < start:
                pass

            if i > end:
                break

            else:
                item = root.child(i)
                item.setCheckState(0, Qt.Checked)

    def start_single_video(self):
        """
        Starts the download of a single video.
        This still uses the tree widget because this makes it easier to track the total progress, as I've already
        implemented this feature into the tree widget and I don't want to write code 2 times
        """
        url = self.ui.lineedit_url.text()
        api_language = self.api_language
        one_time_iterator = []

        video = check_video(url=url, language=api_language, delay=self.delay)
        if video is False:  # If a video url is invalid, check_video will return it as False
            ui_popup(invalid_input_string)

        else:
            one_time_iterator.append(video)
            self.add_to_tree_widget_thread(iterator=one_time_iterator, search_limit=self.search_limit)

    def start_model(self, url=None):
        """Starts the model downloads"""
        if isinstance(url, str):
            model = url

        else:
            model = self.ui.lineedit_model_url.text()

        search_limit = self.search_limit

        if pornhub_pattern.match(model):
            api_language = self.api_language
            if not isinstance(self.client, Client):
                client = Client(language=api_language, delay=self.delay)

            else:
                client = self.client

            model_object = client.get_user(model)
            videos = model_object.videos

        elif hqporner_pattern.match(model):
            pages = round(search_limit / 46)
            videos = hq_Client().get_videos_by_actress(name=model, pages=pages)

        elif eporner_pattern.match(model):
            pages = round(search_limit / 38)
            videos = ep_Client.get_pornstar(url=model, enable_html_scraping=True).videos(pages=pages)

        elif xnxx_pattern.match(model):
            videos = xn_Client.get_user(url=model).videos

        elif xvideos_pattern.match(model):
            videos = xv_Client().get_pornstar(url=model).videos

        self.add_to_tree_widget_thread(videos, search_limit=search_limit)

    def start_playlist(self):
        url = self.ui.lineedit_playlist_url.text()
        playlist = self.client.get_playlist(url)
        videos = playlist.videos
        self.add_to_tree_widget_thread(iterator=videos, search_limit=self.search_limit)

    def load_video(self, url):
        """This starts the thread to load a video"""
        video_loader = VideoLoader(url, self.output_path, self.api_language, self.threading_mode, self.directory_system,
                                   self.quality, delay=self.delay)

        # Connect signals to your slots
        video_loader.signals.loaded.connect(self.on_video_loaded)
        video_loader.signals.error.connect(self.on_video_load_error)

        # Start the thread
        QThreadPool.globalInstance().start(video_loader)

    def on_video_loaded(self, video, author, stripped_title, output_file_path, threading_mode, directory_system,
                        quality):
        # Handle the loaded video, possibly start download
        self.stop_undefined_range()
        self.process_video_thread(output_path=output_file_path, video=video, threading_mode=threading_mode,
                                  quality=quality)

    def on_video_load_error(self, error_message):
        # Handle errors, possibly show message to user
        logger_debug(f"Error loading video: {error_message}")
        ui_popup(QCoreApplication.tr(f"Some error occurred in loading a video. Please report this: {error_message}",
                                     None))

    def process_video_thread(self, output_path, video, threading_mode, quality):
        """Checks which of the three types of threading the user selected and handles them."""
        self.download_thread = DownloadThread(video=video, output_path=output_path, quality=quality,
                                              threading_mode=threading_mode, workers=self.workers, timeout=self.timeout,
                                              stop_flag=stop_flag)
        self.download_thread.signals.progress.connect(self.update_progressbar)
        self.download_thread.signals.total_progress.connect(self.update_total_progressbar)
        self.download_thread.signals.progress_hqporner.connect(self.update_progressbar_hqporner)
        self.download_thread.signals.progress_eporner.connect(self.update_progressbar_eporner)
        self.download_thread.signals.progress_xnxx.connect(self.update_progressbar_xnxx)
        self.download_thread.signals.progress_xvideos.connect(self.update_progressbar_xvideos)
        self.download_thread.signals.ffmpeg_progress.connect(self.update_converting)
        # ADAPTION
        self.download_thread.signals.completed.connect(self.download_completed)
        self.threadpool.start(self.download_thread)
        logger_debug("Started Download Thread!")

    """
    The following functions are used to connect data between Threads and the Main UI
    """

    def update_total_progressbar(self, value, maximum):
        """This updates the total progressbar"""
        self.ui.progressbar_total.setMaximum(maximum)
        self.ui.progressbar_total.setValue(value)

    def update_converting(self, value, maximum):
        """This updates the converting progressbar"""
        self.ui.progressbar_converting.setMaximum(maximum)
        self.ui.progressbar_converting.setValue(value)

    def update_progressbar(self, value, maximum):
        """This updates the PornHub progressbar"""
        self.ui.progressbar_pornhub.setMaximum(maximum)
        self.ui.progressbar_pornhub.setValue(value)

    def update_progressbar_hqporner(self, value, maximum):
        """This updates the HQPorner progressbar"""
        self.ui.progressbar_hqporner.setMaximum(maximum)
        self.ui.progressbar_hqporner.setValue(value)

    def update_progressbar_eporner(self, value, maximum):
        """This updates the eporner progressbar"""
        self.ui.progressbar_eporner.setMaximum(maximum)
        self.ui.progressbar_eporner.setValue(value)

    def update_progressbar_xnxx(self, value, maximum):
        """This updates the xnxx progressbar"""
        self.ui.progressbar_xnxx.setMaximum(maximum)
        self.ui.progressbar_xnxx.setValue(value)

    def update_progressbar_xvideos(self, value, maximum):
        """This updates the xvideos progressbar"""
        self.ui.progressbar_xvideos.setMaximum(maximum)
        self.ui.progressbar_xvideos.setValue(value)

    # ADAPTION
    def download_completed(self):
        """If a video is downloaded, the semaphore is released"""
        logger_debug("Download Completed!")
        self.semaphore.release()

    def start_undefined_range(self):
        """This starts the undefined range (loading animation) of the total progressbar"""
        self.ui.progressbar_total.setRange(0, 0)

    def stop_undefined_range(self):
        """This stops the undefined range (loading animation) of the total progressbar"""
        self.ui.progressbar_total.setRange(0, 1)

    """
    The following functions are used for opening files / directories with the QFileDialog
    """

    def open_output_path_dialog(self):
        """This handles the output path from the settings widget"""
        dialog = QFileDialog()
        path = dialog.getExistingDirectory()
        self.ui.lineedit_output_path.setText(str(path))
        self.output_path = path
        self.save_user_settings()

    def open_file_dialog(self):
        """This opens and processes urls in the file"""
        dialog = QFileDialog()
        file, types = dialog.getOpenFileName()
        self.ui.lineedit_file.setText(file)
        self.start_it()

    def start_it(self):
        file = self.ui.lineedit_file.text()
        self.url_thread = AddUrls(file, api_language=self.api_language, delay=self.delay)
        self.url_thread.signals.total_progress.connect(self.update_total_progressbar)
        self.url_thread.signals.url_iterators.connect(self.receive_url_result)
        self.threadpool.start(self.url_thread)

    def receive_url_result(self, iterator, model_iterator, search_iterator):
        logger_debug(f"Received Video Iterator ({len(iterator)} videos)")
        logger_debug(f"Received Model Iterator ({len(model_iterator)} urls)")
        logger_debug(f"Received Search Iterator ({len(search_iterator)} keywords)")

        logger_debug("Processing Videos...")
        self.add_to_tree_widget_thread(iterator, search_limit=self.search_limit)
        logger_debug("Processing Models...")
        for url in model_iterator:
            self.start_model(url)

        logger_debug("Processing Search queries....")
        for search in search_iterator:
            query = search.get("query")
            website = search.get("website")

            if website == "hqporner":
                self.ui.radio_search_website_hqporner.setChecked(True)

            elif website == "xvideos":
                self.ui.radio_search_website_xvideos.setChecked(True)

            elif website == "pornhub":
                self.ui.radio_search_website_pornhub.setChecked(True)

            elif website == "xnxx":
                self.ui.radio_search_website_xnxx.setChecked(True)

            elif website == "eporner":
                self.ui.radio_search_website_eporner.setChecked(True)

            else:
                ui_popup(f"Information: The Website {website} specified in the URL file isn't valid.")
                return

            self.ui.lineedit_search_query.setText(query)
            self.basic_search()

    def login(self):
        """
        This handles logging in into the users PornHub accounts
        I need to update this to support more websites
        """
        # TODO

        username = self.ui.lineedit_username.text()
        password = self.ui.lineedit_password.text()
        if len(username) <= 2 or len(password) <= 2:
            ui_popup(
                QCoreApplication.tr("Those credentials don't seem to be valid...", None))
            return

        try:
            self.client = Client(username, password, language=self.api_language, delay=self.delay)
            logger_debug("Login Successful!")
            ui_popup(QCoreApplication.tr("Login Successful!", None))
            self.switch_login_button_state()

        except errors.LoginFailed:
            ui_popup(QCoreApplication.tr("Login Failed, please check your credentials and try again!", None))

        except errors.ClientAlreadyLogged:
            ui_popup(QCoreApplication.tr("You are already logged in!", None))

    def check_login(self):
        """Checks if the user is logged in, so that no errors are threw if not"""
        if self.client.logged:
            return True

        elif not self.client.logged:
            self.login()
            if not self.client.logged:
                text = QCoreApplication.tr("There's a problem with the login. Please make sure you login first "
                                           "and then you try to get videos based on your account.", None)
                ui_popup(text)
                return False

            else:
                return True

    def get_watched_videos(self):
        """Returns the videos watched by the user"""
        if self.check_login():
            watched = self.client.account.watched
            self.add_to_tree_widget_thread(watched, search_limit=self.search_limit)

    def get_liked_videos(self):
        """Returns the videos liked by the user"""
        if self.check_login():
            liked = self.client.account.liked
            self.add_to_tree_widget_thread(liked, search_limit=self.search_limit)

    def get_recommended_videos(self):
        """Returns the videos recommended for the user"""
        if self.check_login():
            recommended = self.client.account.recommended
            self.add_to_tree_widget_thread(recommended, search_limit=self.search_limit)

    """
    The following functions are related to the search functionality
    """

    def basic_search(self):
        """Does a simple search for videos without filters on selected website"""
        query = self.ui.lineedit_search_query.text()
        search_limit = self.search_limit

        if self.ui.radio_search_website_pornhub.isChecked():
            videos = Client().search(query)

        elif self.ui.radio_search_website_xvideos.isChecked():
            videos = xv_Client.search(query, pages=99)

        elif self.ui.radio_search_website_hqporner.isChecked():
            videos = hq_Client.search_videos(query, pages=99)

        elif self.ui.radio_search_website_eporner.isChecked():
            videos = ep_Client().search_videos(query, sorting_gay="", sorting_order="", sorting_low_quality="", page=1,
                                               per_page=search_limit, enable_html_scraping=True)

        elif self.ui.radio_search_website_xnxx.isChecked():
            videos = xn_Client().search(query).videos

        self.add_to_tree_widget_thread(videos, search_limit=search_limit)

    def get_top_porn_hqporner(self):
        if self.ui.radio_top_porn_week.isChecked():
            sort = hq_Sort.WEEK

        elif self.ui.radio_top_porn_month.isChecked():
            sort = hq_Sort.MONTH

        elif self.ui.radio_top_porn_all_time:
            sort = hq_Sort.ALL_TIME

        else:
            sort = None

        search_limit = self.search_limit
        pages = round(search_limit / 46)
        videos = hq_Client().get_top_porn(sort_by=sort, pages=pages)
        self.add_to_tree_widget_thread(iterator=videos, search_limit=search_limit)

    def get_by_category_hqporner(self):
        """Returns video by category from HQPorner. I want to add support for EPorner"""  # TODO
        self.list_all_categories_string = QCoreApplication.tr(
            "Invalid Category. Press 'list categories' to see all possible ones.", None)
        category_name = self.ui.lineedit_hqporner_category.text()
        all_categories = hq_Client().get_all_categories()
        search_limit = self.search_limit
        pages = round(search_limit / 46)

        if not category_name in all_categories:
            ui_popup(self.list_all_categories_string)

        else:
            videos = hq_Client().get_videos_by_category(category=category_name, pages=pages)
            self.add_to_tree_widget_thread(videos, search_limit)

    def get_by_category_eporner(self):
        """Returns video by category from EPorner"""
        search_limit = self.search_limit
        pages = round(search_limit / 63)
        category_name = self.ui.lineedit_videos_by_category_eporner.text()

        if not category_name in self.all_cateogories_eporner:
            ui_popup(self.list_all_categories_string)

        else:
            videos = ep_Client().get_videos_by_category(category=category_name, pages=pages, enable_html_scraping=True)
            self.add_to_tree_widget_thread(iterator=videos, search_limit=search_limit)

    def list_categories_eporner(self):
        """Lists all video categories from EPorner"""
        all_categories = ",".join([getattr(ep_Category, category) for category in dir(ep_Category) if
                                   not callable(getattr(ep_Category, category)) and not category.startswith("__")])

        self.all_cateogories_eporner = all_categories  # Need this list to verify the category later
        ui_popup(all_categories)

    def get_brazzers_videos(self):
        """Get brazzers videos from HQPorner"""
        search_limit = self.search_limit
        pages = round(search_limit / 46)
        videos = hq_Client().get_brazzers_videos(pages)
        self.add_to_tree_widget_thread(videos, search_limit)

    @classmethod
    def list_categories_hqporner(cls):
        """Get all available categories. I want to also extend that for EPorner (and maybe even more sites)"""
        categories_ = hq_Client().get_all_categories()
        categories = ",".join(categories_)
        ui_popup(categories)

    def get_random_video(self):
        """Gets a random video from HQPorner"""
        list_object = []
        video = hq_Client().get_random_video()
        list_object.append(video)
        self.add_to_tree_widget_thread(list_object, search_limit=2)

    def show_credits(self):
        """Loads the credits from the CREDITS.md.  Credits need to be recompiled in qresource file every time"""
        self.ui.textBrowser.setOpenExternalLinks(True)
        file = QFile(":/credits/README/CREDITS.md")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        self.ui.textBrowser.setHtml(markdown.markdown(stream.readAll()))

        """
        The following functions are used for the help messages
        """


def main():
    setup_config_file()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    """
    I had many problems with coding in general where something didn't work but the translations are the hardest
    thing I've ever done. Now where I've understand it it makes sense but the Qt documentation is a piece of shit...
    """
    conf = ConfigParser()
    conf.read("config.ini")
    language = conf["UI"]["language"]

    if language == "system":
        # Obtain the system's locale
        locale = QLocale.system()
        # Get the full locale name (e.g., "zh_CN" for Simplified Chinese)
        language_code = locale.name()
        logger_debug(f"System Language: {language_code}")
    else:
        language_code = language

    # Try loading the specific regional translation
    path = f":/translations/translations/{language_code}.qm"
    translator = QTranslator(app)
    if translator.load(path):
        logger_debug(f"Startup: [1/5] {language_code} translation loaded")

    else:
        # Try loading a more general translation if specific one fails
        general_language_code = language_code.split('_')[0]
        path = f":/translations/translations/{general_language_code}.qm"
        if translator.load(path):
            logger_debug(f"{general_language_code} translation loaded as fallback")
        else:
            logger_debug(f"Failed to load {language_code} translation")

    app.installTranslator(translator)

    file = QFile(":/style/stylesheets/stylesheet.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    if __build__ == "android":
        font = QFont("arial", 12)
        app.setFont(font)

    widget = License()  # Starts License widget and checks if license was accepted.
    widget.check_license_and_proceed()

    """
    The following exceptions are just general exceptions to handle some basic errors. They are not so relevant for
    most cases.
    """

    sys.exit(app.exec())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="Shows the version information", action="store_true")
    args = parser.parse_args()

    if args.version:
        print(__version__)

    setup_config_file()
    try:
        main()

    except FileNotFoundError as e:
        ui_popup(f"a File Not Found Error occured. This shouldn't happenn. If you see this error, please report it: {e}")

    except PermissionError as e:
        ui_popup(f"Permission Error: {e}, please report this error.")

    except OverflowError:
        ui_popup("OverFlow Error, please report this immediately, as it's supposed to be fixed!")
