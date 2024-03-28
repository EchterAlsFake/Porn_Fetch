import requests
import time
import sys
import os.path
import argparse
import markdown
import traceback
import src.frontend.resources

from threading import Event
from requests.exceptions import SSLError
from pathlib import Path
from hqporner_api.api import Sort as hq_Sort
from phub import download, consts
from src.backend.shared_functions import *
from itertools import islice
from base_api.modules import consts as bs_consts
from base_api.base import Core
from src.frontend.ui_form_desktop import Ui_Porn_Fetch_Widget
from src.frontend.License import Ui_License
from PySide6.QtCore import (QFile, QTextStream, Signal, QRunnable, QThreadPool, QObject, QSemaphore, Qt, QLocale,
                            QTranslator, QCoreApplication)
from PySide6.QtWidgets import (QWidget, QApplication, QMessageBox, QInputDialog, QTreeWidgetItem, QButtonGroup,
                               QFileDialog)
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
__version__ = "3.2"
__build__ = "desktop"  # android or desktop
__author__ = "Johannes Habel"
total_segments = 0
downloaded_segments = 0
last_index = 0
stop_flag = Event()
send_error_logs = False  # Only enabled when developing the application.
invalid_input_string = QCoreApplication.tr("Wrong Input, please verify the URL, category or actress!",
                                           disambiguation="")
ffmpeg_features = True
ffmpeg_path = None


class SomeFunctions:

    @classmethod
    def send_error_log(cls, message):
        """A function to debug Porn Fetch on my local android development device"""
        url = "http://192.168.2.103:8000/error-log/"
        data = {"message": message}
        requests.post(url, json=data)

    @classmethod
    def logger_error(cls, e):
        """Simple mechanism of printing error messages"""
        print(f"{datetime.now()} : {Fore.LIGHTRED_EX}[ERROR] : {reset()} : {e}")
        if send_error_logs:
            SomeFunctions().send_error_log(e)

    @classmethod
    def logger_debug(cls, e):
        """Simple mechanism of printing debug messages"""
        print(f"{datetime.now()} : {Fore.LIGHTCYAN_EX}[DEBUG] : {return_color()} : {e} {reset()}")
        if send_error_logs:
            SomeFunctions().send_error_log(e)

    @classmethod
    def get_output_path(cls, path="/storage/emulated/0/Download"):
        """
        Checks if the application can write to a specified directory by attempting to create a test file.
        If the directory does not exist or the file cannot be created, returns False.
        """
        path = path if path.endswith("/") else f"{path}/"
        test_file_path = f"{path}test.txt"

        try:
            if not os.path.exists(path):
                return False

            if os.path.isfile(test_file_path):
                logger_debug("Android output path tests successful")
                return True

            with open(test_file_path, "w") as test_file:
                test_file.write("Test content for permission check.")
            return True

        except Exception as e:
            logger_error(e)
            return False

    @classmethod
    def ui_popup(cls, text):
        """ A simple UI popup that will be used for small messages to the user."""
        qmsg_box = QMessageBox()
        qmsg_box.setText(text)
        qmsg_box.exec()


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

    # Metadata
    text_data = Signal(list)

    # Operations
    finished = Signal()
    clear_signal = Signal()
    get_total = Signal(str, str)


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
            SomeFunctions().logger_error("License was denied, closing Porn Fetch")
            self.close()
            sys.exit(0)  # exiting if user denied

    def show_main_window(self):
        """ If license was accepted, the License widget is closed and the main widget will be shown."""
        self.close()
        logger_debug("Startup: [2/5] License accepted")
        self.main_widget = Porn_Fetch()
        self.main_widget.show()


class AddToTreeWidget(QRunnable):
    def __init__(self, iterator, search_limit, data_mode, clickable, reverse, stop_flag, is_checked):
        super(AddToTreeWidget, self).__init__()
        self.signals = Signals()
        self.iterator = iterator
        self.search_limit = search_limit
        self.data_mode = data_mode
        self.clickable = clickable
        self.reverse = reverse
        self.stop_flag = stop_flag
        self.is_checked = is_checked

    def process_video(self, video, index):
        title = video.title
        disabled = QCoreApplication.tr("Disabled", disambiguation="It means, that the displaying of the"
                                                                  "author and duration in the tree widget is disabled")
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
            start = last_index + 1
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

                        text_data = self.process_video(video, i)

                        self.signals.progress.emit(self.search_limit, i)  # sends the current progress
                        self.signals.text_data.emit(text_data)  # sends the data to the main class
                        try_attempt = False  # Processing succeeded, move to the next video

                    except errors.NoResult:
                        try_attempt = False  # No result, move to the next video

                    except errors.RegexError as e:
                        SomeFunctions().logger_error("Warning: Rate limited by PornHub, trying again in 5 seconds...")
                        for j in range(5):
                            print(f"\r\033[K[Sleeping: [{j} / 10]", end='', flush=True)
                            time.sleep(1)

                    except ConnectionError:
                        SomeFunctions().logger_error(
                            "Client.call failed!, retrying...  If this error persists, set a delay in the settings")
                        SomeFunctions().logger_error(f"Video: {i} won't be processed.")
                        try_attempt = False  # Move to the next video after logging the error

                    except IndexError:
                        SomeFunctions().logger_error(
                            "You got blocked from PornHub. Please switch your IP or wait some minutes. (at least 5)")
                        SomeFunctions().ui_popup(QCoreApplication.tr(
                            "You got blocked from PornHub. Please switch your IP or wait some minutes. (at least 5)",
                            None))

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
                if current_time - self.last_update_time < 0.1:
                    # If not, do not update the progress and return immediately
                    return

            signal.emit(pos, total)
            # Update total progress only if the video source uses segments
            if video_source not in ['hqporner', 'eporner']:
                self.update_total_progress(ffmpeg)

        # Update the last update time to the current time
        self.last_update_time = current_time

    def update_ffmpeg_progress(self, pos, total):
        """Update progress for ffmpeg downloads."""
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
            SomeFunctions().logger_debug(f"Downloading Video to: {self.output_path}")
            if self.threading_mode == "FFMPEG" or self.threading_mode == download.FFMPEG:
                self.ffmpeg = True

            if isinstance(self.video, Video):  # Assuming 'Video' is the class for Pornhub
                self.threading_mode = self.resolve_threading_mode(self.threading_mode)
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
                SomeFunctions().logger_debug(f"FFMPEG PATH: {ffmpeg_path}")
                cmd = [ffmpeg_path, "-i", f"{self.output_path}_.tmp", "-c", "copy", self.output_path]
                ff = FfmpegProgress(cmd)
                for progress in ff.run_command_with_progress():
                    self.signals.ffmpeg_progress.emit(round(progress), 100)

                os.remove(f"{self.output_path}_.tmp")
                write_tags(path=self.output_path, video=self.video)
            else:
                SomeFunctions().logger_debug("FFMPEG features disabled, writing tags and converting the video won't be available!")


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
            SomeFunctions().logger_debug("Getting segments...")
            global total_segments, downloaded_segments
            total_segments = sum(
                [len(list(video.get_segments(quality=self.quality))) for video in video_objects if
                 hasattr(video, 'get_segments')])
            SomeFunctions().logger_debug("Got segments")
            # This basically looks how many segments exist in all videos together, so that we can calculate the total
            # progress

        else:
            SomeFunctions().logger_debug("Progress tracking: FFMPEG")
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
            SomeFunctions().logger_debug("Semaphore Acquired")
            self.signals.progress_video.emit(video)  # Now emits the video to the main class for further processing


class MetadataVideos(QRunnable):
    """Threading class for the video metadata"""

    def __init__(self, video):
        super(MetadataVideos, self).__init__()
        self.signals = Signals()
        self.video = video

    def run(self):
        """
        Loads all metadata for videos. Since we don't have all variables on every website, I cna load them if they are
        available, which is why I always check with the hasattribute method.
        """
        self.signals.start_undefined_range.emit()  # This btw starts the undefined range in the total bar. (Loading animation)

        like_string = QCoreApplication.tr("Likes", disambiguation="The Likes of the video")
        dislike_string = QCoreApplication.tr("Dislikes", disambiguation="The dislikes of the video")
        duration_string = QCoreApplication.tr("minutes", disambiguation="The duration of the video")

        title = self.video.title
        views = self.video.views if hasattr(self.video, 'views') else "Unknown"
        duration = self.video.length
        orientation = self.video.orientation if hasattr(self.video, 'orientation') else "Unknown"
        pornstars = ",".join(self.video.pornstars if hasattr(self.video, 'pornstars') else "Unknown")
        tags = ",".join(self.video.tags if hasattr(self.video, 'tags') else self.video.categories)
        hotspots_x = ",".join(self.video.hotspots if hasattr(self.video, 'hotspots') else "unknown")

        likes = self.video.likes if hasattr(self.video, 'likes') else "Unknown"
        dislikes = self.video.dislikes if hasattr(self.video, 'dislikes') else "Unknown"

        rating = f"{like_string}: {likes} | {dislike_string}: {dislikes}"
        try:
            duration = f"{round(duration / 60)} {duration_string}"

        except (ValueError, TypeError):
            duration = str(duration)

        data = [title, views, duration, orientation, pornstars, tags, rating, hotspots_x]
        SomeFunctions().logger_debug("Successfully loaded video metadata")
        self.signals.data.emit(data)  # Send the data to the main class, so that they can be applied to the lineedits


class MetadataUser(QRunnable):
    """Threading class for the user metadata"""

    def __init__(self, user):
        super(MetadataUser, self).__init__()
        self.user = user
        self.signals = Signals()

    def run(self):
        self.signals.start_undefined_range.emit()
        info = self.user.info

        interested_in = info.get("Interested in")
        relationship_status = info.get("Relationship status")
        city_country = info.get("City and Country")
        gender = info.get("Gender")
        birth_place = info.get("Birth Place")
        height = info.get("Height")
        weight = info.get("Weight")
        ethnicity = info.get("Ethnicity")
        hair_color = info.get("Hair Color")
        fake_boobs = info.get("Fake Boobs")
        tattoos = info.get("Tattoos")
        piercings = info.get("Piercings")
        hometown = info.get("Hometown")
        interests_hobbies = info.get("Interests and hobbie")
        turn_ons = info.get("Turn Ons")
        turn_offs = info.get("Turn Offs")
        video_views = info.get("Video Views")
        profile_views = info.get("Profile Views")
        videos_watched = info.get("Videos Watched")
        type = self.user.type
        name = self.user.name

        data = [interested_in, relationship_status, city_country, gender, birth_place, height, weight, ethnicity,
                hair_color, fake_boobs, tattoos, piercings, hometown, interests_hobbies, turn_ons, turn_offs,
                video_views, profile_views, videos_watched, type, name]

        self.signals.data.emit(data)


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
                SomeFunctions().ui_popup(invalid_input_string)

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
                stripped_title = Core().strip_title(title)  # Strip the title, so that videos with special chars can be saved
                # on windows. Would raise an OSError otherwise

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


class Porn_Fetch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Variable initialization:
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
        self.conf = ConfigParser()
        self.conf.read("config.ini")
        self.threadpool = QThreadPool()
        self.ui = Ui_Porn_Fetch_Widget()
        self.ui.setupUi(self)
        self.button_connectors()
        self.button_groups()
        self.load_style()
        SomeFunctions().logger_debug("Startup: [3/5] Initialized the User Interface")
        self.language_strings()
        self.settings_maps_initialization()
        self.load_user_settings()
        SomeFunctions().logger_debug("Startup: [4/5] Loaded the user settings")
        self.switch_to_home()
        self.check_for_updates()
        SomeFunctions().logger_debug("Startup: [5/5] ✔")

        if __build__ == "android":
            self.setup_android()

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
            self.ui.button_switch_metadata: "list.svg",
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
        self.ui.button_tree_select_all.setStyleSheet(stylesheets["button_green"])
        self.ui.button_output_path_select.setStyleSheet(stylesheets["button_blue"])
        self.ui.button_login.setStyleSheet(stylesheets["button_blue"])
        self.ui.button_settings_apply.setStyleSheet(stylesheets["button_blue"])
        self.ui.button_user_get_bio.setStyleSheet(stylesheets["button_orange"])
        self.ui.button_get_random_videos.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_get_brazzers_videos.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_metadata_user_start.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_list_categories.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_open_file.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_switch_supported_websites.setStyleSheet(stylesheets["button_blue"])
        self.ui.button_user_download_avatar.setStyleSheet(stylesheets["button_orange"])
        self.ui.button_video_thumbnail_download.setStyleSheet(stylesheets["button_orange"])
        self.ui.button_metadata_video_start.setStyleSheet(stylesheets["button_purple"])
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
        self.ui.button_stop.setStyleSheet(stylesheets["button_reset"])
        self.ui.button_export_video_urls.setStyleSheet(stylesheets["button_purple"])
        self.ui.button_timeout_maximal_retries_help.setStyleSheet(stylesheets["button_green"])
        self.ui.button_help_file.setStyleSheet(stylesheets["button_green"])

    def language_strings(self):
        """Contains the language strings. Needed for translation"""
        self.get_output_path_string_ui_popup = QCoreApplication.tr("""The specified output path doesn't exist.
        If you think, this is an error, please report it!""", disambiguation=None)

        self.save_user_settings_language_string = QCoreApplication.tr("Saved User Settings, please restart Porn Fetch!",
                                                                      disambiguation=None)
        self.open_file_language_string = QCoreApplication.tr("Select URL file", disambiguation=None)
        self.language_string_login_failed = QCoreApplication.tr("Login Failed, please check your credentials and try "
                                                                "again!", disambiguation=None)

        self.language_string_login_successful = QCoreApplication.tr("Login Successful!", disambiguation=None)
        self.get_user_avatar_language_string = QCoreApplication.tr("User Avatar saved in current directory...",
                                                                   disambiguation=None)
        self.get_video_thumbnail_language_string = QCoreApplication.tr("Video thumbnail saved in current directory",
                                                                       disambiguation=None)

    @classmethod
    def check_for_updates(cls):
        if requests.get("https://github.com/EchterAlsFake/Porn_Fetch/releases/tag/3.3").status_code == 200:
            SomeFunctions().logger_debug("Next release v3.3 found!")
            SomeFunctions().ui_popup(QCoreApplication.tr("Information: A new version of Porn Fetch (v3.3) is out. "
                                                         "I recommend you to update Porn Fetch. Go to: "
                                                         "https://github.com/EchterAlsFake/Porn_Fetch/releases/tag/3.3",
                                                         None))

        else:
            SomeFunctions().logger_debug("No updates found...")

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
        SomeFunctions().logger_debug(f"Running on Android: {sys.platform}")
        if not SomeFunctions().get_output_path():
            self.handle_no_output_path()
            return  # Early return to avoid setting up UI components again at the end.

        self.configure_ui_for_android("/storage/emulated/0/Download/")

    def handle_no_output_path(self):
        SomeFunctions().ui_popup(
            QCoreApplication.tr("The output path does not exist or is not writable.", disambiguation=""))
        text, ok = QInputDialog.getText(self, "Enter custom Path",
                                        QCoreApplication.tr("Enter custom Path:", disambiguation=""))
        if ok and SomeFunctions().get_output_path(text):
            SomeFunctions().ui_popup(
                QCoreApplication.tr(f"Success: {text} will be used for this session!", disambiguation=""))
            self.configure_ui_for_android(text)
        else:
            SomeFunctions().ui_popup(
                QCoreApplication.tr("Invalid path. The application will now exit.", disambiguation=""))
            sys.exit()

    def configure_ui_for_android(self, path):
        """Disables some things on Android which just don't work yet"""
        self.output_path = path
        self.ui.lineedit_output_path.setText(self.output_path)
        self.ui.lineedit_output_path.setReadOnly(True)
        self.ui.button_open_file.setDisabled(True)
        self.ui.lineedit_file.setText(QCoreApplication.tr("Not supported on Android", disambiguation=""))
        self.ui.radio_threading_mode_ffmpeg.setDisabled(True)  # Assume ffmpeg is too much for Android in this context.
        self.warn_about_high_performance_threading()

    def warn_about_high_performance_threading(self):
        if self.ui.radio_threading_mode_high_performance.isChecked():
            SomeFunctions().ui_popup(
                QCoreApplication.tr("High Performance threading may cause issues on Android devices.",
                                    disambiguation=""))

    @staticmethod
    def reset_pornfetch():
        SomeFunctions().ui_popup(
            QCoreApplication.tr("Porn Fetch will now reset to its default settings...", disambiguation=None))
        setup_config_file(force=True)
        SomeFunctions().ui_popup(QCoreApplication.tr("Done! Please restart.", disambiguation=None))

    "These functions are used to switch to different widgets. Basically this is the sidebar at the left"

    def switch_to_account(self):
        self.ui.stacked_widget_top.setCurrentIndex(1)
        self.ui.stacked_widget_main.setCurrentIndex(0)
        self.ui.stacked_widget_top.setMinimumHeight(150)
        self.ui.scrollarea_stacked_top.setMaximumHeight(150)

    def switch_to_home(self):
        self.ui.stacked_widget_main.setCurrentIndex(0)
        self.ui.stacked_widget_top.setCurrentIndex(0)
        self.ui.stacked_widget_top.setMinimumHeight(220)
        self.ui.scrollarea_stacked_top.setMaximumHeight(220)

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

    def switch_to_all_progress_bars(self):
        self.ui.stacked_widget_top.setCurrentIndex(2)

    def switch_stop_state(self):
        stop_flag.set()
        time.sleep(1)
        self.switch_stop_state_2()

    @classmethod
    def switch_stop_state_2(self):
        global stop_flag
        stop_flag = Event()

    def button_connectors(self):
        """a function to link the buttons to their functions"""
        # Menu Bar Switch Button Connections
        self.ui.button_switch_home.clicked.connect(self.switch_to_home)
        self.ui.button_switch_settings.clicked.connect(self.switch_to_settings)
        self.ui.button_switch_credits.clicked.connect(self.switch_to_credits)
        self.ui.button_switch_metadata.clicked.connect(self.switch_to_metadata)
        self.ui.button_switch_account.clicked.connect(self.switch_to_account)
        self.ui.button_switch_supported_websites.clicked.connect(self.switch_to_supported_websites)
        self.ui.button_view_all_progress_bars.clicked.connect(self.switch_to_all_progress_bars)

        # Video Download Button Connections
        self.ui.button_download.clicked.connect(self.start_single_video)
        self.ui.button_model.clicked.connect(self.start_model)
        self.ui.button_tree_download.clicked.connect(self.download_tree_widget)
        self.ui.button_tree_select_all.clicked.connect(self.select_all_items)
        self.ui.button_tree_unselect_all.clicked.connect(self.unselect_all_items)
        self.ui.button_playlist_get_videos.clicked.connect(self.start_playlist)

        # Help Buttons Connections
        self.ui.button_semaphore_help.clicked.connect(self.button_semaphore_help)
        self.ui.button_threading_mode_help.clicked.connect(self.button_threading_mode_help)
        self.ui.button_directory_system_help.clicked.connect(self.button_directory_system_help)
        self.ui.button_workers_help.clicked.connect(self.maximal_workers_help)
        self.ui.button_timeout_help.clicked.connect(self.timeout_help)
        self.ui.button_pornhub_delay_help.clicked.connect(self.pornhub_delay_help)
        self.ui.button_result_limit_help.clicked.connect(self.result_limit_help)
        self.ui.button_help_file.clicked.connect(self.open_file_help)
        self.ui.button_timeout_maximal_retries_help.clicked.connect(self.max_retries_help)

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

        # Metadata
        self.ui.button_metadata_video_start.clicked.connect(self.get_metadata_video)
        self.ui.button_metadata_user_start.clicked.connect(self.get_metadata_user)
        self.ui.button_user_get_bio.clicked.connect(self.get_user_bio)
        self.ui.button_user_download_avatar.clicked.connect(self.get_user_avatar)
        self.ui.button_video_thumbnail_download.clicked.connect(self.get_video_thumbnail)

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
        self.ui.button_stop.clicked.connect(self.switch_stop_state)
        self.ui.button_export_video_urls.clicked.connect(self.export_urls)

    def switch_login_button_state(self):
        """If the user is logged in, I'll change the stylesheets of the buttons"""
        file = QFile(":/style/stylesheets/stylesheet_switch_buttons_login_state.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        stylesheet = stream.readAll()

        self.ui.button_get_liked_videos.setStyleSheet(stylesheet)
        self.ui.button_get_watched_videos.setStyleSheet(stylesheet)
        self.ui.button_get_recommended_videos.setStyleSheet(stylesheet)

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

    def load_user_settings(self):
        """Loads the user settings from the configuration file and applies them."""

        # Apply settings
        self.quality_map.get(self.conf.get("Video", "quality")).setChecked(True)
        self.threading_mode_map.get(self.conf.get("Performance", "threading_mode")).setChecked(True)
        self.directory_system_map.get(self.conf.get("Video", "directory_system")).setChecked(True)
        self.language_map.get(self.conf.get("Video", "language")).setChecked(True)
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

        if self.gui_language == "en":
            self.ui.radio_ui_language_english.setChecked(True)

        elif self.gui_language == "de_DE":
            self.ui.radio_ui_language_german.setChecked(True)

        elif self.gui_language == "fr":
            self.ui.radio_ui_language_french.setChecked(True)

        elif self.gui_language == "zh_CN":
            self.ui.radio_ui_language_chinese_simplified.setChecked(True)

        elif self.gui_language == "system":
            self.ui.radio_ui_language_system_default.setChecked(True)

        if self.conf["Video"]["directory_system"] == "1":
            self.directory_system = True
            self.ui.radio_directory_system_yes.setChecked(True)

        elif self.conf["Video"]["directory_system"] == "0":
            self.directory_system = False
            self.ui.radio_directory_system_no.setChecked(True)

        global ffmpeg_path

        if os.path.isfile("ffmpeg"):
            ffmpeg_path = "ffmpeg"

        elif os.path.isfile("ffmpeg.exe"):
            ffmpeg_path = "ffmpeg.exe"

        else:
            SomeFunctions().logger_error("FFMPEG wasn't found... Have you extracted it from the .zip file?")
            SomeFunctions().logger_error("FFMPEG Features won't be available!")

            global ffmpeg_features
            ffmpeg_features = False

            self.ui.radio_threading_mode_ffmpeg.setChecked(False)
            self.ui.radio_threading_mode_ffmpeg.setDisabled(False)
            self.ui.radio_threading_mode_ffmpeg.setToolTip("FFMPEG is not installed, therefore this feature is NOT available.")

        self.ui.spinbox_maximal_timeout.setValue(int(self.timeout))
        self.ui.spinbox_maximal_workers.setValue(int(self.workers))
        self.ui.spinbox_pornhub_delay.setValue(int(self.delay))
        consts.MAX_CALL_RETRIES = self.max_retries
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

        # Save other settings
        self.conf.set("Performance", "semaphore", str(self.ui.spinbox_semaphore.value()))
        self.conf.set("Video", "search_limit", str(self.ui.spinbox_treewidget_limit.value()))
        self.conf.set("Video", "output_path", self.ui.lineedit_output_path.text())

        if self.ui.radio_ui_language_french.isChecked():
            self.conf.set("UI", "language", "fr")

        elif self.ui.radio_ui_language_german.isChecked():
            self.conf.set("UI", "language", "de_DE")

        elif self.ui.radio_ui_language_english.isChecked():
            self.conf.set("UI", "language", "en_DE")

        elif self.ui.radio_ui_language_chinese_simplified.isChecked():
            self.conf.set("UI", "language", "zh_CN")

        elif self.ui.radio_ui_language_system_default.isChecked():
            self.conf.set("UI", "language", "system")

        self.conf.set("Performance", "timeout", str(self.ui.spinbox_maximal_timeout.value()))
        self.conf.set("Performance", "workers", str(self.ui.spinbox_maximal_workers.value()))
        self.conf.set("Video", "delay", str(self.ui.spinbox_pornhub_delay.value()))
        self.conf.set("Performance", "retries", str(self.ui.spinbox_maximal_retries.value()))

        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)

        SomeFunctions().ui_popup(self.save_user_settings_language_string)
        SomeFunctions().logger_debug("Saved User Settings, please restart Porn Fetch.")

    """
    The following functions are related to the tree widget    
    """

    def add_to_tree_widget_thread(self, iterator, search_limit, clickable=False):
        if clickable:
            # If a Pornstar has uploads, I want to add a button to download their videos. This is gonna be implemented in
            # v3.2
            for user_object in iterator:
                uploads = user_object.uploads
                if uploads:
                    pass  # Implemented in v3.2

        if self.ui.radio_tree_show_title.isChecked():
            data_mode = 0

        elif self.ui.radio_tree_show_all.isChecked():
            data_mode = 1

        else:
            data_mode = 0

        if self.ui.checkbox_show_videos_reversed.isChecked():
            reverse = True

        else:
            reverse = False

        is_checked = self.ui.checkbox_do_not_clear_videos.isChecked()

        self.thread = AddToTreeWidget(iterator, search_limit, data_mode, clickable, reverse, is_checked=is_checked,
                                      stop_flag=stop_flag)
        self.thread.signals.text_data.connect(self.add_to_tree_widget_signal)
        self.thread.signals.progress.connect(self.progress_tree_widget)
        self.thread.signals.clear_signal.connect(self.clear_tree_widget)
        self.thread.signals.start_undefined_range.connect(self.start_undefined_range)
        self.thread.signals.stop_undefined_range.connect(self.stop_undefined_range)
        self.thread.signals.finished.connect(self.stop_undefined_range)
        self.threadpool.start(self.thread)

    def clear_tree_widget(self):
        """
        This (like the name says) clears the tree widget. I try to improve this in the future, to allow the user
        the adding of multiple videos, so that the tree widget doesn't get cleared instantly.
        """
        if not self.ui.checkbox_do_not_clear_videos.isChecked():
            self.ui.treeWidget.clear()

    def export_urls(self):
        video_urls = []

        for i in range(self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(i)
            video_object = item.data(0, Qt.UserRole)
            video_urls.append(video_object.url)

        if len(video_urls) == 0:
            SomeFunctions().ui_popup(
                QCoreApplication.tr("No video URLs found. Are there videos in the tree widget?", ""))
            return

        file, mode = QFileDialog().getSaveFileName(self)

        try:
            with open(file, "a") as file:
                for url in video_urls:
                    file.write(f"{url}\n")

        except PermissionError:
            SomeFunctions().ui_popup(QCoreApplication.tr(f"Permission Error, please select a file from your user space,"
                                                         f"or run Porn Fetch with admin permissions (not recommended!)",
                                                         None))

    def progress_tree_widget(self, total, current):
        """This tracks the progress of the tree widget data"""
        self.ui.progressbar_total.setMaximum(total)
        self.ui.progressbar_total.setValue(current)

    def add_to_tree_widget_signal(self, data):
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
        Starts the thread for downloading the tree widget
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

    """
    The following functions are used for the help messages
    """

    @classmethod
    def result_limit_help(cls):
        text = QCoreApplication.tr(f"""
The result limit defines how many videos will be returned when performing a search or doing other operations which
involves loading multiple videos. This also affects models / channels and your liked videos. The result limit is
basically the number of videos which can be loaded into the tree widget (this thing where videos are displayed).
""", disambiguation=None)
        SomeFunctions().ui_popup(text)

    @classmethod
    def pornhub_delay_help(cls):
        text = QCoreApplication.tr(f"""
You can set a delay between requests from you to PornHub. If you are downloading a lot of videos or experiencing 
'client.call' errors, you should enable a delay. By default the delay is turned off with the value 0

A good starting point is between 0.5 - 1.5

The longer the delay is, the longer it will take to download videos, load videos and generally do stuff.
This does NOT affect other sites!
""", disambiguation=None)
        SomeFunctions().ui_popup(text)

    @classmethod
    def maximal_workers_help(cls):
        text = QCoreApplication.tr(f"""
The maximal workers define the amount of maximal threads which can be started when using the threaded download mode.
One thread handles downloading one segment, so (in theory) 20 threads can download 20 segments at the same time.
This can of course be helpful when you have a very fast internet connection, but when you have a poor PC or running on
Android, you should set this to a lower value.

I recommend '3' for Android and 5 for low bandwidth connections < 15000 bit/s
""", disambiguation=None)
        SomeFunctions().ui_popup(text)

    @classmethod
    def timeout_help(cls):
        text = QCoreApplication.tr(f"""
The timeout handles the timeout for retrieving segments when using the treaded download mode. If you have a poor 
internet connection you can set this higher than 10. But this isn't required for most users!
""", disambiguation=None)
        SomeFunctions().ui_popup(text)

    @classmethod
    def button_semaphore_help(cls):
        text = QCoreApplication.tr(f"""
The Semaphore is a tool to limit the number of simultaneous actions / downloads.

For example: If the semaphore is set to 1, only 1 video will be downloaded at the same time.
If the semaphore is set to 4, 4 videos will be downloaded at the same time. Changing this is only useful, if
you have a really good internet connection and a good system.
""", disambiguation=None)
        SomeFunctions().ui_popup(text)

    @classmethod
    def button_threading_mode_help(cls):
        text = QCoreApplication.tr("""
The different threading modes are used for different scenarios. 

1) High Performance:  Uses a class of workers to download multiple video segments at a time. Can be really fast if you
have a very strong internet connection. Maybe not great for low end systems.

2) FFMPEG:  ffmpeg is a tool for converting media files. ffmpeg will download every video segment and merge it directly
into the video file. This removes an extra step from the default method and is therefore a lot faster, but still not as 
good as high performance.

3) Default:  The default download mode will just download one video segment after the next one. If you get a lot of 
timeouts this can really slow down the process, as we need to wait for PornHub to return the video segments.
With the High Performance method, we can just download other segments while waiting which makes it so fast.
""", disambiguation=None)
        SomeFunctions().ui_popup(text)

    @classmethod
    def button_directory_system_help(cls):
        text = QCoreApplication.tr("""
The directory system will save videos in an intelligent way. If you download 3 videos form one Pornstar and 5 videos 
from another, Porn Fetch will automatically make folders for it and move the 3 videos into that one folder and the other
5 into the other. (This will still apply with your selected output path)

This can be helpful for organizing stuff, but is a more advanced feature, so the majority of users won't use it probably.
""", disambiguation=None)

        SomeFunctions().ui_popup(text)

    @classmethod
    def open_file_help(cls):
        text = QCoreApplication.tr("""
Create a .txt file and add URLs like this:

url1
url2
url3
...

Split them with new lines. No comma, not multiple URLs in the same line!
You can also add model URLs like this:

model#MODEL_URL

An example for a file would be:

https://de.pornhub.com/view_video.php?viewkey=ph5be76343323ff
https://de.pornhub.com/view_video.php?viewkey=ph5946e5f19585a
model#https://de.pornhub.com/pornstar/nancy-a
""", None)
        SomeFunctions().ui_popup(text)

    @classmethod
    def max_retries_help(cls):
        text = QCoreApplication.tr("""
The maximal retries defines how much attempts will be used for a network request. For example if an API calls
a URL for a website there will be <AMOUNT> of attempts until an error is thrown.
""", None)
        SomeFunctions().ui_popup(text)

    def start_single_video(self):
        """
        Starts the download of a single video.
        This still uses the tree widget, because this makes it easier to track the total progress, as I've already
        implemented this feature into the tree widget and I don't want to write code 2 times
        """
        url = self.ui.lineedit_url.text()
        api_language = self.api_language
        one_time_iterator = []

        video = check_video(url=url, language=api_language, delay=self.delay)
        if video is False:  # If a video url is invalid, check_video will return it as False
            SomeFunctions().ui_popup(invalid_input_string)

        else:
            one_time_iterator.append(video)
            self.add_to_tree_widget_thread(iterator=one_time_iterator, search_limit=self.search_limit)

    def start_model(self, url=None):
        """Starts the model downloads"""
        if type(url) is str:
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
        SomeFunctions().logger_debug(f"Error loading video: {error_message}")
        SomeFunctions().ui_popup(
            QCoreApplication.tr(f"Some error occurred in loading a video. Please report this: {error_message}",
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
        SomeFunctions().logger_debug("Started Download Thread!")

    """
    The following functions are used to connect data between Threads and the Main UI
    """

    def update_total_progressbar(self, value, maximum):
        """This updates the total progressbar"""
        try:
            self.ui.progressbar_total.setMaximum(maximum)
            self.ui.progressbar_total.setValue(value)

        except OverflowError:
            value = value / 1024 / 1024
            maximum = maximum / 1024 / 1024
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
        scaling_factor = 1024 * 1024
        scaled_value = int(value / scaling_factor)
        scaled_maximum = int(maximum / scaling_factor)
        self.ui.progressbar_hqporner.setMaximum(scaled_maximum)
        self.ui.progressbar_hqporner.setValue(scaled_value)

    def update_progressbar_eporner(self, value, maximum):
        """This updates the eporner progressbar"""
        scaling_factor = 1024 * 1024
        scaled_value = int(value / scaling_factor)
        scaled_maximum = int(maximum / scaling_factor)
        self.ui.progressbar_eporner.setMaximum(scaled_maximum)
        self.ui.progressbar_eporner.setValue(scaled_value)

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
        SomeFunctions().logger_debug("Download Completed!")
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
        """This opens and processes urls in a the file"""
        dialog = QFileDialog()
        file, types = dialog.getOpenFileName()
        self.ui.lineedit_file.setText(file)
        iterator = []
        model_iterators = []

        with (open(file, "r") as url_file):
            content = url_file.read().splitlines()
            for idx, url in enumerate(content):
                if len(url) == 0:
                    continue

                self.ui.progressbar_total.setMaximum(len(content))
                self.ui.progressbar_total.setValue(idx)
                if url.startswith("model#"):
                    url = url.split("#")
                    url = url[1]
                    model_iterators.append(url)

                else:
                    video = check_video(url, language=self.api_language, delay=self.delay)

                    if video is not False:
                        iterator.append(video)

                    else:
                        SomeFunctions().ui_popup(invalid_input_string)

            SomeFunctions().logger_debug("Adding URLs to the tree widget...")
            self.add_to_tree_widget_thread(iterator, search_limit=self.search_limit)
            SomeFunctions().logger_debug("Adding Model videos to the tree widget...")
            for url in model_iterators:
                SomeFunctions().logger_debug(f"Loading videos for model URL: {url}")
                self.start_model(url)

    """
    The following functions are related to the User's account
    """

    def login(self):
        """
        This handles logging in into the users PornHub accounts
        I need to update this to support more websites
        """
        # TODO

        username = self.ui.lineedit_username.text()
        password = self.ui.lineedit_password.text()
        if len(username) <= 2 or len(password) <= 2:
            SomeFunctions().ui_popup(
                QCoreApplication.tr("Those credentials don't seem to be valid...", disambiguation=None))
            return

        try:
            self.client = Client(username, password, language=self.api_language, delay=self.delay)
            SomeFunctions().logger_debug("Login Successful!")
            SomeFunctions().ui_popup(self.language_string_login_successful)
            self.switch_login_button_state()

        except errors.LoginFailed:
            SomeFunctions().ui_popup(self.language_string_login_failed)

        except errors.ClientAlreadyLogged:
            SomeFunctions().ui_popup(QCoreApplication.tr("You are already logged in!", disambiguation=""))

    def check_login(self):
        """Checks if the user is logged in, so that no errors are threw if not"""
        if self.client.logged:
            return True

        elif not self.client.logged:
            self.login()
            if not self.client.logged:
                text = QCoreApplication.tr("There's a problem with the login. Please make sure you login first "
                                           "and then you try to get videos based on your account.", disambiguation="")
                SomeFunctions().ui_popup(text)
                return False

            else:
                return True

    def get_watched_videos(self):
        """Returns the videos watched by the user"""
        if self.check_login():
            watched = self.client.account.watched
            self.add_to_tree_widget_thread(watched, search_limit=500)

    def get_liked_videos(self):
        """Returns the videos liked by the user"""
        if self.check_login():
            liked = self.client.account.liked
            self.add_to_tree_widget_thread(liked, search_limit=500)

    def get_recommended_videos(self):
        """Returns the videos recommended for the user"""
        if self.check_login():
            recommended = self.client.account.recommended
            self.add_to_tree_widget_thread(recommended, search_limit=500)

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
            pages = round(search_limit / 48)
            videos = xv_Client.search(query, pages=pages)

        elif self.ui.radio_search_website_hqporner.isChecked():
            pages = round(search_limit / 46)
            videos = hq_Client.search_videos(query, pages=pages)
            search_limit = 3 * 46

        elif self.ui.radio_search_website_eporner.isChecked():
            videos = ep_Client().search_videos(query, sorting_gay="", sorting_order="", sorting_low_quality="", page=1,
                                               per_page=search_limit, enable_html_scraping=True)

        elif self.ui.radio_search_website_xnxx.isChecked():
            videos = xn_Client().search(query).videos

        self.add_to_tree_widget_thread(videos, search_limit=search_limit)

    def get_metadata_video(self):
        """This starts the metadata thread for videos"""
        api_language = self.api_language
        video = self.ui.lineedit_metadata_video_url.text()
        video = check_video(url=video, language=api_language, delay=self.delay)

        if video is False:
            SomeFunctions().ui_popup(invalid_input_string)

        else:
            self.metadata_thread = MetadataVideos(video)
            self.metadata_thread.signals.start_undefined_range.connect(self.start_undefined_range)
            self.metadata_thread.signals.data.connect(self.apply_metadata_video)
            self.threadpool.start(self.metadata_thread)

    def apply_metadata_video(self, data):  # TODO
        """
        This applies the metadata to the actual lineedits. I need to improve this mechanism, so that
        I can do that for more websites
            """
        title = data[0]
        views = data[1]
        duration = data[2]
        orientation = data[3]
        pornstars = data[4]
        tags = data[5]
        rating = data[6]
        hotspots = data[7]

        self.ui.lineedit_video_title.setText(title)
        self.ui.lineedit_video_views.setText(str(views))
        self.ui.lineedit_video_duration.setText(str(duration))
        self.ui.lineedit_video_orientation.setText(orientation)
        self.ui.lineedit_video_pornstars.setText(pornstars)
        self.ui.lineedit_video_tags.setText(tags)
        self.ui.lineedit_video_rating.setText(rating)
        self.ui.lineedit_video_hotspots.setText(str(hotspots))
        self.stop_undefined_range()

    def get_metadata_user(self):
        """
        This gets metadata for PornHub users. I try to add support for other sites, but depends on the APIs
        and the information provided by the website
        """
        api_language = self.api_language  # TODO
        user = self.ui.lineedit_metadata_user_url.text()
        user_object = self.client.get_user(user)

        self.user_metadata_thread = MetadataUser(user_object)
        self.user_metadata_thread.signals.start_undefined_range.connect(self.start_undefined_range)
        self.user_metadata_thread.signals.data.connect(self.apply_metadata_user)
        self.threadpool.start(self.user_metadata_thread)

    def apply_metadata_user(self, data):
        """This applies the metadata, and as you can see, this is the magic of the index filtering :) """  # TODO
        interested_in = get_element_safe(data, 0)
        relationship = get_element_safe(data, 1)
        city_and_country = get_element_safe(data, 2)
        gender = get_element_safe(data, 3)
        birth_place = get_element_safe(data, 4)
        height = get_element_safe(data, 5)
        weight = get_element_safe(data, 6)
        ethnicity = get_element_safe(data, 7)
        hair_color = get_element_safe(data, 8)
        fake_boobs = get_element_safe(data, 9)
        tattoos = get_element_safe(data, 10)
        piercings = get_element_safe(data, 11)
        hometown = get_element_safe(data, 12)
        interests_and_hobbies = get_element_safe(data, 13)
        turn_ons = get_element_safe(data, 14)
        turn_offs = get_element_safe(data, 15)
        video_views = get_element_safe(data, 16)
        profile_views = get_element_safe(data, 17)
        videos_watched = get_element_safe(data, 18)
        type = get_element_safe(data, 19)
        name = get_element_safe(data, 20)

        self.ui.lineedit_user_interested_in.setText(str(interested_in))
        self.ui.lineedit_user_relationship.setText(str(relationship))
        self.ui.lineedit_user_city_country.setText(str(city_and_country))
        self.ui.lineedit_user_gender.setText(str(gender))
        self.ui.lineedit_user_birth_place.setText(str(birth_place))
        self.ui.lineedit_user_height.setText(str(height))
        self.ui.lineedit_user_weight.setText(str(weight))
        self.ui.lineedit_user_ethnicity.setText(str(ethnicity))
        self.ui.lineedit_user_hair_color.setText(str(hair_color))
        self.ui.lineedit_user_fake_boobs.setText(str(fake_boobs))
        self.ui.lineedit_user_tattoos.setText(str(tattoos))
        self.ui.lineedit_user_piercings.setText(str(piercings))
        self.ui.lineedit_user_home_town.setText(str(hometown))
        self.ui.lineedit_user_interests_hobbies.setText(str(interests_and_hobbies))
        self.ui.lineedit_user_turn_ons.setText(str(turn_ons))
        self.ui.lineedit_user_turn_offs.setText(str(turn_offs))
        self.ui.lineedit_user_video_views.setText(str(video_views))
        self.ui.lineedit_user_profile_views.setText(str(profile_views))
        self.ui.lineedit_user_videos_watched.setText(str(videos_watched))
        self.ui.lineedit_user_type.setText(str(type))
        self.ui.lineedit_user_name.setText(str(name))

        self.stop_undefined_range()

    def get_user_bio(self):
        """Returns the user bio in a string format"""
        url = self.ui.lineedit_metadata_user_url.text()
        user = self.client.get_user(url)
        bio = user.bio
        SomeFunctions().ui_popup(bio)

    def get_user_avatar(self):
        """Downloads the users avatar image to the specified output path"""
        url = self.ui.lineedit_metadata_user_url.text()
        user = self.client.get_user(url)
        avatar = user.avatar
        avatar.download(Path(self.output_path))
        user_string = self.get_user_avatar_language_string
        SomeFunctions().ui_popup(user_string)

    def get_video_thumbnail(self):
        """Returns the video thumbnail. I need to add support for more websites here"""  # TODO
        api_language = self.api_language
        url = self.ui.lineedit_metadata_video_url.text()
        video = check_video(url=url, language=api_language, delay=self.delay)

        if video is False or not isinstance(video, Video):
            SomeFunctions().ui_popup(invalid_input_string)

        else:
            video.image.download(Path(self.output_path))
            user_string = self.get_video_thumbnail_language_string
            SomeFunctions().ui_popup(user_string)

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
            "Invalid Category. Press 'list categories' to see all possible ones.",
            disambiguation="")
        category_name = self.ui.lineedit_hqporner_category.text()
        all_categories = hq_Client().get_all_categories()
        search_limit = self.search_limit
        pages = round(search_limit / 46)

        if not category_name in all_categories:
            SomeFunctions().ui_popup(self.list_all_categories_string)

        else:
            videos = hq_Client().get_videos_by_category(category=category_name, pages=pages)
            self.add_to_tree_widget_thread(videos, search_limit)

    def get_by_category_eporner(self):
        """Returns video by category from EPorner"""
        search_limit = self.search_limit
        pages = round(search_limit / 63)
        category_name = self.ui.lineedit_videos_by_category_eporner.text()

        if not category_name in self.all_cateogories_eporner:
            SomeFunctions().ui_popup(self.list_all_categories_string)

        else:
            videos = ep_Client().get_videos_by_category(category=category_name, pages=pages, enable_html_scraping=True)
            self.add_to_tree_widget_thread(iterator=videos, search_limit=search_limit)

    def list_categories_eporner(self):
        """Lists all video categories from EPorner"""
        all_categories = ",".join([getattr(ep_Category, category) for category in dir(ep_Category) if
                                   not callable(getattr(ep_Category, category)) and not category.startswith("__")])

        self.all_cateogories_eporner = all_categories  # Need this list to verify the category later
        SomeFunctions().ui_popup(all_categories)

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
        SomeFunctions().ui_popup(categories)

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
        print(language_code)
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

    try:
        if args.version:
            print(__version__)

        else:
            setup_config_file()
            main()

    except PermissionError as e:
        SomeFunctions().ui_popup(
            QCoreApplication.tr("Insufficient Permissions to access something. Please run Porn Fetch as root / admin",
                                disambiguation=""))
        SomeFunctions().logger_error(e)

    except ConnectionResetError as e:
        SomeFunctions().ui_popup(
            QCoreApplication.tr("Connection was reset. Are you connected to a public wifi or a university's wifi? ",
                                disambiguation=""))
        SomeFunctions().logger_error(e)

    except ConnectionError as e:
        SomeFunctions().ui_popup(
            QCoreApplication.tr("Connection Error, please make sure you have a stable internet connection",
                                disambiguation=""))
        SomeFunctions().logger_error(e)

    except KeyboardInterrupt:
        sys.exit(0)

    except SSLError as e:
        SomeFunctions().ui_popup(QCoreApplication.tr(
            "SSLError: Your connection is blocked by your ISP / IT administrator (Firewall). If you are in a "
            "University or at school, please connect to a VPN / Proxy", disambiguation=""))
        SomeFunctions().logger_error(e)

    except TypeError:
        pass

    except OSError as e:
        SomeFunctions().ui_popup(QCoreApplication.tr(
            f"This error shouldn't happen. If you still see it it's REALLY important that you report the "
            f"following: {e}", disambiguation=""))
        SomeFunctions().logger_error(e)

    except ZeroDivisionError:
        SomeFunctions().ui_popup(QCoreApplication.tr(f"Zero Division Error. This shouldn't really happen...", None))

    except Exception as e:
        error_message = "An error occurred: " + str(e) + "\n" + traceback.format_exc()
        SomeFunctions().logger_error(error_message)
        if send_error_logs:
            SomeFunctions().send_error_log(error_message)
