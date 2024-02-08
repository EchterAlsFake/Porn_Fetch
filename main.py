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
__version__ = "3.0"
__build__ = "android"  # android or desktop
__author__ = "Johannes Habel"
total_segments = 0
downloaded_segments = 0

send_error_logs = True  # Only enabled when developing the application.

import shutil
import tarfile
import requests

import sys
import os.path
import argparse
import markdown
import traceback
import zipfile
import src.frontend.resources

from requests.exceptions import SSLError
from pathlib import Path
from hqporner_api.api import Sort as hq_Sort, Video as hq_Video
from phub import Quality, download, consts
from src.backend.shared_functions import *
from itertools import islice

from src.frontend.ui_form_desktop import Ui_Porn_Fetch_Widget
from src.frontend.License import Ui_License
from PySide6.QtCore import (QFile, QTextStream, Signal, QRunnable, QThreadPool, QObject, QSemaphore, Qt, QLocale,
                            QTranslator, QCoreApplication)
from PySide6.QtWidgets import (QWidget, QApplication, QMessageBox, QInputDialog, QLabel,
                               QTreeWidgetItem, QButtonGroup, QFileDialog)
from PySide6.QtGui import QIcon, QFont


def send_error_log(message):
    """A function to debug Porn Fetch on my local android development device"""
    url = "http://192.168.2.103:8000/error-log/"
    data = {"message": message}
    requests.post(url, json=data)


def logger_error(e):
    print(f"{datetime.now()} : {Fore.LIGHTRED_EX}[ERROR] : {reset()} : {e}")
    if send_error_logs:
        send_error_log(e)


def logger_debug(e):
    print(f"{datetime.now()} : {Fore.LIGHTCYAN_EX}[DEBUG] : {return_color()} : {e} {reset()}")
    if send_error_logs:
        send_error_log(e)


def get_output_path(path="/storage/emulated/0/Download"):
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
            return True

        with open(test_file_path, "w") as test_file:
            test_file.write("Test content for permission check.")
        return True

    except Exception as e:
        logger_error(e)
        return False


def ui_popup(text):
    """ A simple UI popup that will be used for small messages to the user."""
    qmsg_box = QMessageBox()
    qmsg_box.setText(text)
    qmsg_box.exec()


class WorkerSignals(QObject):
    progress = Signal(int)
    completed = Signal()


class DownloadProgressSignal(QObject):
    """Sends the current download progress to the main UI to update the progressbar."""

    # ADAPTION
    progress = Signal(int, int)
    progress_hqporner = Signal(int, int)
    progress_eporner = Signal(int, int)
    progress_xnxx = Signal(int, int)
    progress_xvideos = Signal(int, int)
    total_progress = Signal(int, int)


class QTreeWidgetSignal(QObject):
    """Signals needed across the QTreeWidget"""
    progress = Signal(object)
    get_total = Signal(str, Quality)
    start_undefined_range = Signal()
    stop_undefined_range = Signal()


class MetadataSignals(QObject):
    """Signals needed to emit data from the metadata class"""
    data = Signal(list)
    start_undefined = Signal()


class TreeWidgetSignals(QObject):
    """Signals to send data to the tree Widget"""
    clear_signal = Signal()
    text_data = Signal(list)
    progress = Signal(int, int)
    finished = Signal()


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
            self.close()
            sys.exit(0)

    def show_main_window(self):
        """ If license was accepted, the License widget is closed and the main widget will be shown."""
        self.close()
        self.main_widget = Porn_Fetch()
        self.main_widget.show()


class AddToTreeWidget(QRunnable):
    def __init__(self, iterator, search_limit, data_mode, clickable, reverse):
        super(AddToTreeWidget, self).__init__()
        self.signals = TreeWidgetSignals()
        self.iterator = iterator
        self.search_limit = search_limit
        self.data_mode = data_mode
        self.clickable = clickable
        self.reverse = reverse

    def process_video(self, video, index):
        title = video.title
        disabled = QCoreApplication.tr("Disabled", disambiguation="It means, that the displaying of the"
                                                                  "author and duration in the tree widget is disabled")
        duration = disabled
        author = disabled

        if self.data_mode == 1:
            if isinstance(video, (hq_Video, xn_Video, xv_Video)):
                duration = str(video.length)

                if hasattr(video, 'pornstars'):
                    author = video.pornstars[0] if video.pornstars else "author_not_found"

                else:
                    author = video.author if hasattr(video, 'author') and video.author else "unknown_author"

            elif isinstance(video, Video):
                duration = round(video.duration.seconds / 60)
                author = video.author.name

            elif isinstance(video, ep_Video):
                duration = round(int(video.length) / 60)
                author = video.author

        # Handling exceptions for missing author in xn_Video
        if isinstance(video, xn_Video) and not hasattr(video, 'pornstars'):
            author = "no_pornstars_found"

        return [str(title), str(author), str(duration), str(index), video]

    def run(self):
        self.signals.clear_signal.emit()

        try:
            logger_debug(f"Search Limit: {str(self.search_limit)}")

            if self.reverse:
                # Use islice to limit the number of items fetched from the iterator
                videos = list(islice(self.iterator, self.search_limit))
                videos.reverse()  # Reverse the list

            else:
                videos = islice(self.iterator, self.search_limit)

                for i, video in enumerate(videos, start=1):
                    if i == self.search_limit + 1:
                        break

                    text_data = self.process_video(video, i)

                    self.signals.progress.emit(self.search_limit, i)
                    self.signals.text_data.emit(text_data)

        except errors.NoResult:
            pass

        finally:
            self.signals.finished.emit()


class DownloadThread(QRunnable):
    """Threading class to download videos."""

    """
    I know that this function is horribly optimized, but I (and ChatGPT) don't know how to do it better.
    If you find a way, to keep both progress bars, handle ffmpeg progress and keep the total progress available:
    
    Make a PR and I'll underline your name at the top of my Readme lmao
    """

    signal = Signal()

    def __init__(self, video, quality, output_path, threading_mode):
        super(DownloadThread, self).__init__()

        self.video = video
        self.quality = quality
        self.output_path = output_path
        self.threading_mode = threading_mode
        self.signals = DownloadProgressSignal()
        self.signals_completed = WorkerSignals()
        self.video_progress = {}

        if isinstance(self.video, Video):
            if self.threading_mode == "threaded":
                self.threading_mode = download.threaded()

            elif self.threading_mode == "FFMPEG":
                self.threading_mode = download.FFMPEG

            elif self.threading_mode == "default":
                self.threading_mode = download.default

    def callback(self, pos, total, ffmpeg=False):
        self.signals.progress.emit(pos, total)

        if ffmpeg is False:
            global downloaded_segments
            downloaded_segments += 1  # Assuming each call represents one segment
            self.signals.total_progress.emit(downloaded_segments, total_segments)

    def callback_hqporner(self, pos, total, ffmpeg=False):
        # Choose a divisor that reduces the values sufficiently
        # 1024 converts bytes to kilobytes, for example
        # Fixes the OverflowError
        divisor = 1024
        pos_reduced = pos // divisor
        total_reduced = total // divisor

        # Emit the signal with the reduced values
        self.signals.progress_hqporner.emit(pos_reduced, total_reduced)

    def callback_eporner(self, pos, total, ffmpeg=False):
        self.signals.progress_eporner.emit(pos, total)

    def callback_xnxx(self, pos, total, ffmpeg=False):
        self.signals.progress_xnxx.emit(pos, total)

        if ffmpeg is False:
            global downloaded_segments
            downloaded_segments += 1
            self.signals.total_progress.emit(downloaded_segments, total_segments)

    def callback_xvideos(self, pos, total, ffmpeg=True):
        self.signals.progress_xvideos.emit(pos, total)

        global downloaded_segments
        downloaded_segments += 1
        self.signals.total_progress.emit(downloaded_segments, total_segments)

    def callback_ffmpeg(self, pos, total):
        video_title = self.video.title
        self.video_progress[video_title] = pos / total * 100

        total_progress = sum(self.video_progress.values()) / len(self.video_progress)
        self.signals.total_progress.emit(total_progress, 100)

    def wrapper_ffmpeg_pornhub(self, pos, total):
        self.callback_ffmpeg(pos, total)
        self.callback(pos, total, ffmpeg=True)

    def wrapper_ffmpeg_xvideos(self, pos, total):
        self.callback_ffmpeg(pos, total)
        self.callback_xvideos(pos, total, ffmpeg=True)

    def wrapper_ffmpeg_xnxx(self, pos, total):
        self.callback_ffmpeg(pos, total)
        self.callback_xnxx(pos, total, ffmpeg=True)

    # ADAPTION

    def run(self):
        try:
            logger_debug(f"Downloading Video to: {self.output_path}")

            if self.threading_mode == "FFMPEG" or self.threading_mode == download.FFMPEG:

                if isinstance(self.video, Video):
                    self.video.download(downloader=self.threading_mode, path=self.output_path, quality=self.quality,
                                        display=self.wrapper_ffmpeg_pornhub)

                elif isinstance(self.video, hq_Video):
                    self.video.download(quality=self.quality, output_path=self.output_path,
                                        callback=self.callback_hqporner, no_title=True)

                elif isinstance(self.video, ep_Video):
                    self.video.download_video(quality=self.quality, output_path=self.output_path,
                                              callback=self.callback_eporner, no_title=True)

                elif isinstance(self.video, xn_Video):
                    self.video.download(downloader=self.threading_mode, output_path=self.output_path,
                                        quality=self.quality,
                                        callback=self.wrapper_ffmpeg_xnxx)

                elif isinstance(self.video, xv_Video):
                    self.video.download(downloader=self.threading_mode, output_path=self.output_path,
                                        quality=self.quality,
                                        callback=self.wrapper_ffmpeg_xvideos)

            else:
                if isinstance(self.video, Video):
                    self.video.download(downloader=self.threading_mode, path=self.output_path, quality=self.quality,
                                        display=self.callback)

                elif isinstance(self.video, hq_Video):
                    self.video.download(quality=self.quality, output_path=self.output_path,
                                        callback=self.callback_hqporner, no_title=True)

                elif isinstance(self.video, ep_Video):
                    self.video.download_video(quality=self.quality, output_path=self.output_path,
                                              callback=self.callback_eporner, no_title=True)

                elif isinstance(self.video, xn_Video):
                    self.video.download(downloader=self.threading_mode, output_path=self.output_path,
                                        quality=self.quality,
                                        callback=self.callback_xnxx)

                elif isinstance(self.video, xv_Video):
                    self.video.download(downloader=self.threading_mode, output_path=self.output_path,
                                        quality=self.quality,
                                        callback=self.callback_xvideos)

            # ADAPTION

        finally:
            self.signals_completed.completed.emit()


class QTreeWidgetDownloadThread(QRunnable):
    """Threading class for the QTreeWidget (sends objects to the download class defined above)"""

    def __init__(self, treeWidget, semaphore, quality, threading_mode):
        super(QTreeWidgetDownloadThread, self).__init__()
        self.treeWidget = treeWidget
        self.semaphore = semaphore
        self.signals = QTreeWidgetSignal()
        self.quality = quality
        self.threading_mode = threading_mode

    def run(self):
        self.signals.start_undefined_range.emit()
        video_objects_hqporner = []
        video_objects_pornhub = []
        video_objects_eporner = []
        video_objects_xnxx = []
        video_objects_xvideos = []
        # ADAPTION

        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)
            checkState = item.checkState(0)
            if checkState == Qt.Checked:
                object_ = item.data(0, Qt.UserRole)
                if isinstance(object_, hq_Video):
                    video_objects_hqporner.append(object_)

                elif isinstance(object_, Video):
                    video_objects_pornhub.append(object_)

                elif isinstance(object_, ep_Video):
                    video_objects_eporner.append(object_)

                elif isinstance(object_, xn_Video):
                    video_objects_xnxx.append(object_)

                elif isinstance(object_, xv_Video):
                    video_objects_xvideos.append(object_)
                # ADAPTION

        if not self.threading_mode == "FFMPEG":
            global total_segments, downloaded_segments
            total_segments = sum(
                [len(list(video.get_segments(quality=self.quality))) for video in video_objects_pornhub +
                 video_objects_xnxx + video_objects_xvideos])  # ADAPTION

        else:
            counter = 0
            for _ in video_objects_pornhub + video_objects_xnxx + video_objects_xvideos:
                counter += 100

            total_segments = counter

        downloaded_segments = 0

        self.signals.stop_undefined_range.emit()
        videos = (video_objects_pornhub + video_objects_hqporner + video_objects_eporner + video_objects_xnxx +
                  video_objects_xvideos)  # ADAPTION
        for video in videos:
            self.semaphore.acquire()
            logger_debug("Semaphore Acquired")
            self.signals.progress.emit(video)


class MetadataVideos(QRunnable):
    """Threading class for the video metadata"""

    def __init__(self, video):
        super(MetadataVideos, self).__init__()
        self.signals = MetadataSignals()
        self.video = video

    def run(self):
        """
        I know this can be handled better, I'll refactor it in v3.1
        """

        self.signals.start_undefined.emit()

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

        self.signals.data.emit(data)


class MetadataUser(QRunnable):
    """Threading class for the user metadata"""

    def __init__(self, user):
        super(MetadataUser, self).__init__()
        self.user = user
        self.signals = MetadataSignals()

    def run(self):
        self.signals.start_undefined.emit()
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


class FFMPEGSignals(QObject):
    progress_signal = Signal(int, int)


class FFMPEGDownload(QRunnable):
    def __init__(self, url, extract_path, mode):
        super().__init__()
        self.url = url
        self.extract_path = extract_path
        self.mode = mode
        self.signals = FFMPEGSignals()

    def run(self):
        # Download the file
        with requests.get(self.url, stream=True) as r:
            r.raise_for_status()
            total_length = int(r.headers.get('content-length'))
            self.signals.progress_signal.emit(0, total_length)  # Initialize progress bar
            dl = 0
            filename = self.url.split('/')[-1]
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        dl += len(chunk)
                        self.signals.progress_signal.emit(dl, total_length)

        # Extract the file based on OS mode
        if self.mode == "linux" and filename.endswith(".tar.xz"):
            with tarfile.open(filename, "r:xz") as tar:
                total_members = len(tar.getmembers())

                for idx, member in enumerate(tar.getmembers()):
                    if 'ffmpeg' in member.name and (member.name.endswith('ffmpeg')):
                        tar.extract(member, self.extract_path)
                        extracted_path = os.path.join(self.extract_path, member.path)
                        shutil.move(extracted_path, "./")

                    self.signals.progress_signal.emit(idx, total_members)

        elif self.mode == "windows" and filename.endswith(".zip"):
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                total = len(zip_ref.namelist())

                for idx, member in enumerate(zip_ref.namelist()):
                    if 'ffmpeg.exe' in member:
                        zip_ref.extract(member, self.extract_path)
                        extracted_path = os.path.join(self.extract_path, member)
                        shutil.move(extracted_path, ".")

                    self.signals.progress_signal.emit(idx, total)

        # Finalize
        self.signals.progress_signal.emit(total_length, total_length)  # Ensure progress bar reaches 100%
        os.remove(filename)  # Clean up downloaded archive

        if sys.platform == "linux":
            os.removedirs("ffmpeg-6.1-amd64-static")

        elif sys.platform == "win32":
            os.removedirs("ffmpeg-6.1.1-essentials_build")


class Porn_Fetch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        print(sys.platform)
        # Variable initialization:
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
        self.language_strings()
        self.settings_maps_initialization()
        self.load_user_settings()
        self.check_ffmpeg()

        if __build__ == "android":
            self.setup_android()

    def load_style(self):
        """a simple function to load the icons for the buttons"""
        self.ui.button_switch_home.setIcon(QIcon(":/images/graphics/download.svg"))
        self.ui.button_switch_settings.setIcon(QIcon(":/images/graphics/settings.svg"))
        self.ui.button_switch_credits.setIcon(QIcon(":/images/graphics/information.svg"))
        self.ui.button_switch_metadata.setIcon(QIcon(":/images/graphics/list.svg"))
        self.ui.button_switch_account.setIcon(QIcon(":/images/graphics/account.svg"))
        self.setWindowIcon(QIcon(":/images/graphics/logo_transparent.ico"))

        file_progress_pornhub = QFile(":/style/stylesheets/progressbar_pornhub.qss")
        file_progress_pornhub.open(QFile.ReadOnly | QFile.Text)
        stream_progress_pornhub = QTextStream(file_progress_pornhub)

        file_progress_hqporner = QFile(":/style/stylesheets/progressbar_hqporner.qss")
        file_progress_hqporner.open(QFile.ReadOnly | QFile.Text)
        stream_progress_hqporner = QTextStream(file_progress_hqporner)

        file_progress_eqporner = QFile(":/style/stylesheets/progressbar_eporner.qss")
        file_progress_eqporner.open(QFile.ReadOnly | QFile.Text)
        stream_progress_eporner = QTextStream(file_progress_eqporner)

        file_progressbar_total = QFile(":/style/stylesheets/progressbar_total.qss")
        file_progressbar_total.open(QFile.ReadOnly | QFile.Text)
        stream_progress_total = QTextStream(file_progressbar_total)

        file_progressbar_xnxx = QFile(":/style/stylesheets/progressbar_xnxx.qss")
        file_progressbar_xnxx.open(QFile.ReadOnly | QFile.Text)
        stream_progress_xnxx = QTextStream(file_progressbar_xnxx)

        file_progressbar_xvideos = QFile(":/style/stylesheets/progressbar_xvideos.qss")
        file_progressbar_xvideos.open(QFile.ReadOnly | QFile.Text)
        stream_progress_xvideos = QTextStream(file_progressbar_xvideos)

        file_stylesheet_button_blue = QFile(":/style/stylesheets/stylesheet_button_blue.qss")
        file_stylesheet_button_orange = QFile(":/style/stylesheets/stylesheet_button_orange.qss")
        file_stylesheet_button_purple = QFile(":/style/stylesheets/stylesheet_button_purple.qss")
        file_stylesheet_button_login = QFile(":/style/stylesheets/stylesheet_button_login.qss")
        file_stylesheet_button_logins = QFile(":/style/stylesheets/stylesheet_buttons_login.qss")

        file_stylesheet_button_blue.open(QFile.ReadOnly | QFile.Text)
        stream_button_blue = QTextStream(file_stylesheet_button_blue)
        file_stylesheet_button_logins.open(QFile.ReadOnly | QFile.Text)
        stream_button_logins = QTextStream(file_stylesheet_button_logins)
        file_stylesheet_button_login.open(QFile.ReadOnly | QFile.Text)
        stream_button_login = QTextStream(file_stylesheet_button_login)
        file_stylesheet_button_orange.open(QFile.ReadOnly | QFile.Text)
        stream_button_orange = QTextStream(file_stylesheet_button_orange)
        file_stylesheet_button_purple.open(QFile.ReadOnly | QFile.Text)
        stream_button_purple = QTextStream(file_stylesheet_button_purple)

        blue = stream_button_blue.readAll()
        orange = stream_button_orange.readAll()
        purple = stream_button_purple.readAll()
        login = stream_button_login.readAll()
        logins = stream_button_logins.readAll()

        self.ui.button_login.setStyleSheet(login)
        self.ui.button_get_watched_videos.setStyleSheet(logins)
        self.ui.button_get_liked_videos.setStyleSheet(logins)
        self.ui.button_get_recommended_videos.setStyleSheet(logins)
        self.ui.button_download.setStyleSheet(purple)
        self.ui.button_model.setStyleSheet(purple)
        self.ui.button_open_file.setStyleSheet(purple)
        self.ui.button_tree_download.setStyleSheet(purple)
        self.ui.button_metadata_user_start.setStyleSheet(purple)
        self.ui.button_metadata_video_start.setStyleSheet(purple)
        self.ui.button_user_download_avatar.setStyleSheet(purple)
        self.ui.button_user_get_bio.setStyleSheet(purple)
        self.ui.button_video_thumbnail_download.setStyleSheet(purple)
        self.ui.button_tree_select_all.setStyleSheet(orange)
        self.ui.button_tree_unselect_all.setStyleSheet(blue)
        self.ui.button_help_pages.setStyleSheet(login)
        self.ui.button_semaphore_help.setStyleSheet(login)
        self.ui.button_threading_mode_help.setStyleSheet(login)
        self.ui.button_directory_system_help.setStyleSheet(login)
        self.ui.button_output_path_select.setStyleSheet(login)
        self.ui.button_settings_apply.setStyleSheet(login)
        self.ui.button_search.setStyleSheet(purple)
        self.ui.button_hqporner_category_get_videos.setStyleSheet(purple)
        self.ui.button_get_random_videos.setStyleSheet(purple)
        self.ui.button_get_brazzers_videos.setStyleSheet(purple)
        self.ui.button_list_categories.setStyleSheet(purple)
        self.ui.button_top_porn_get_videos.setStyleSheet(purple)
        self.ui.button_switch_supported_websites.setStyleSheet(login)

        self.ui.progressbar_pornhub.setStyleSheet(stream_progress_pornhub.readAll())
        self.ui.progressbar_hqporner.setStyleSheet(stream_progress_hqporner.readAll())
        self.ui.progressbar_total.setStyleSheet(stream_progress_total.readAll())
        self.ui.progressbar_eporner.setStyleSheet(stream_progress_eporner.readAll())
        self.ui.progressbar_xnxx.setStyleSheet(stream_progress_xnxx.readAll())
        self.ui.progressbar_xvideos.setStyleSheet(stream_progress_xvideos.readAll())
        logger_debug("Loaded Icons!")

    def language_strings(self):
        """Contains the language strings. Needed for translation"""
        self.get_api_language_string_dialog = QCoreApplication.tr("Please enter the language code for your "
                                                                  "language.  Example: en, de, fr, ru --=>:",
                                                                  disambiguation=None)

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

    def button_groups(self):
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
        logger_debug(f"Running on Android: {sys.platform}")
        if not get_output_path():
            self.handle_no_output_path()
            return  # Early return to avoid setting up UI components again at the end.

        self.configure_ui_for_android("/storage/emulated/0/Download/")

    def handle_no_output_path(self):
        ui_popup(QCoreApplication.tr("The output path does not exist or is not writable.", disambiguation=""))
        text, ok = QInputDialog.getText(self, "Enter custom Path",
                                        QCoreApplication.tr("Enter custom Path:", disambiguation=""))
        if ok and get_output_path(text):
            ui_popup(QCoreApplication.tr(f"Success: {text} will be used for this session!", disambiguation=""))
            self.configure_ui_for_android(text)
        else:
            ui_popup(QCoreApplication.tr("Invalid path. The application will now exit.", disambiguation=""))
            exit()

    def configure_ui_for_android(self, path):
        self.output_path = path
        self.ui.lineedit_output_path.setText(self.output_path)
        self.ui.lineedit_output_path.setReadOnly(True)
        self.ui.button_open_file.setDisabled(True)
        self.ui.lineedit_file.setText(QCoreApplication.tr("Not supported on Android", disambiguation=""))
        self.ui.radio_threading_mode_ffmpeg.setDisabled(True)  # Assume ffmpeg is too much for Android in this context.
        self.warn_about_high_performance_threading()

    def warn_about_high_performance_threading(self):
        if self.ui.radio_threading_mode_high_performance.isChecked():
            ui_popup(QCoreApplication.tr("High Performance threading may cause issues on Android devices.",
                                         disambiguation=""))

    def check_ffmpeg(self):
        if self.ui.radio_threading_mode_ffmpeg.isChecked() or self.conf["Performance"]["threading_mode"] == "ffmpeg":
            if sys.platform == "linux":
                if not os.path.isfile("ffmpeg"):
                    url_linux = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
                    ui_popup("FFMPEG isn't installed on your system. I'll do this now for you.")
                    self.downloader = FFMPEGDownload(url=url_linux, extract_path=".", mode="linux")
                    self.downloader.signals.progress_signal.connect(self.update_total_progressbar)
                    self.threadpool.start(self.downloader)

                consts.FFMPEG_EXECUTABLE = "ffmpeg"

            elif sys.platform == "win32":
                if not os.path.isfile("ffmpeg.exe"):
                    url_windows = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
                    ui_popup("FFMPEG isn't installed on your system. I'll do this now for you.")
                    self.downloader = FFMPEGDownload(url=url_windows, extract_path=".", mode="windows")
                    self.downloader.signals.progress_signal.connect(self.update_total_progressbar)
                    self.threadpool.start(self.downloader)

                consts.FFMPEG_EXECUTABLE = "ffmpeg.exe"

    def switch_to_account(self):
        self.ui.stacked_widget_top.setCurrentIndex(1)
        self.ui.stacked_widget_main.setCurrentIndex(0)
        self.layout().update()

    def switch_to_home(self):
        self.ui.stacked_widget_main.setCurrentIndex(0)
        self.ui.stacked_widget_top.setCurrentIndex(0)
        self.layout().update()

    def switch_to_hqporner(self):
        self.ui.stacked_widget_main.setCurrentIndex(0)
        self.ui.stacked_widget_top.setCurrentIndex(3)

    def switch_to_settings(self):
        self.ui.stacked_widget_main.setCurrentIndex(1)

    def switch_to_metadata(self):
        self.ui.stacked_widget_main.setCurrentIndex(3)

    def switch_to_credits(self):
        self.ui.stacked_widget_main.setCurrentIndex(2)
        self.show_credits()

    def switch_to_supported_websites(self):
        self.ui.stacked_widget_main.setCurrentIndex(4)

    def button_connectors(self):
        """a function to link the buttons to their functions"""

        # Menu Bar Switch Button Connections
        self.ui.button_switch_home.clicked.connect(self.switch_to_home)
        self.ui.button_switch_settings.clicked.connect(self.switch_to_settings)
        self.ui.button_switch_credits.clicked.connect(self.switch_to_credits)
        self.ui.button_switch_metadata.clicked.connect(self.switch_to_metadata)
        self.ui.button_switch_account.clicked.connect(self.switch_to_account)
        self.ui.button_switch_supported_websites.clicked.connect(self.switch_to_supported_websites)

        # Video Download Button Connections
        self.ui.button_download.clicked.connect(self.start_single_video)
        self.ui.button_model.clicked.connect(self.start_model)
        self.ui.button_tree_download.clicked.connect(self.download_tree_widget)
        self.ui.button_tree_select_all.clicked.connect(self.select_all_items)
        self.ui.button_tree_unselect_all.clicked.connect(self.unselect_all_items)

        # Help Buttons Connections
        self.ui.button_semaphore_help.clicked.connect(self.button_semaphore_help)
        self.ui.button_threading_mode_help.clicked.connect(self.button_threading_mode_help)
        self.ui.button_directory_system_help.clicked.connect(self.button_directory_system_help)
        self.ui.button_help_pages.clicked.connect(self.hqporner_pages_help)

        # Settings
        self.ui.button_settings_apply.clicked.connect(self.save_user_settings)

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
        self.ui.button_switch_hqporner.clicked.connect(self.switch_to_hqporner)
        self.ui.button_get_random_videos.clicked.connect(self.get_random_video)

        # File Dialog
        self.ui.button_output_path_select.clicked.connect(self.open_output_path_dialog)
        self.ui.button_open_file.clicked.connect(self.open_file_dialog)
        logger_debug("Connected Buttons!")

    def switch_login_button_state(self):
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

        logger_debug(f"Video Language: {self.api_language}")
        logger_debug("Loaded User Settings!")

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

        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)

        ui_popup(self.save_user_settings_language_string)
        logger_debug("Saved User Settings, please restart Porn Fetch.")

    """
    The following functions are related to the tree widget    
    """

    def add_to_tree_widget_thread(self, iterator, search_limit, clickable=False):
        if clickable:
            for user_object in iterator:
                uploads = user_object.uploads
                if uploads:
                    pass  # Implemented in v3.1

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

        self.thread = AddToTreeWidget(iterator, search_limit, data_mode, clickable, reverse)
        self.thread.signals.text_data.connect(self.add_to_tree_widget_signal)
        self.thread.signals.progress.connect(self.progress_tree_widget)
        self.thread.signals.clear_signal.connect(self.clear_tree_widget)
        self.thread.signals.finished.connect(self.stop_undefined_range)
        self.threadpool.start(self.thread)

    def clear_tree_widget(self):
        self.ui.treeWidget.clear()

    def progress_tree_widget(self, total, current):
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
        semaphore = self.semaphore
        treeWidget = self.ui.treeWidget
        quality = self.quality
        download_tree_thread = QTreeWidgetDownloadThread(treeWidget=treeWidget, semaphore=semaphore,
                                                         quality=quality, threading_mode=self.threading_mode)
        download_tree_thread.signals.progress.connect(self.tree_widget_completed)
        download_tree_thread.signals.start_undefined_range.connect(self.start_undefined_range)
        download_tree_thread.signals.stop_undefined_range.connect(self.stop_undefined_range)
        self.threadpool.start(download_tree_thread)

    def tree_widget_completed(self, video):
        self.load_video(video)

    def unselect_all_items(self):
        root = self.ui.treeWidget.invisibleRootItem()
        item_count = root.childCount()
        for i in range(item_count):
            item = root.child(i)
            item.setCheckState(0, Qt.Unchecked)

    def select_all_items(self):
        root = self.ui.treeWidget.invisibleRootItem()
        item_count = root.childCount()
        for i in range(item_count):
            item = root.child(i)
            item.setCheckState(0, Qt.Checked)

    """
    The following functions are used for the help messages
    """

    def button_semaphore_help(self):
        text = QCoreApplication.tr(f"""
The Semaphore is a tool to limit the number of simultaneous actions / downloads.

For example: If the semaphore is set to 1, only 1 video will be downloaded at the same time.
If the semaphore is set to 4, 4 videos will be downloaded at the same time. Changing this is only useful, if
you have a really good internet connection and a good system.
""", disambiguation=None)
        ui_popup(text)

    def button_threading_mode_help(self):
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
        ui_popup(text)

    def button_directory_system_help(self):
        text = QCoreApplication.tr("""
The directory system will save videos in an intelligent way. If you download 3 videos form one Pornstar and 5 videos 
from another, Porn Fetch will automatically make folders for it and move the 3 videos into that one folder and the other
5 into the other. (This will still apply with your selected output path)

This can be helpful for organizing stuff, but is a more advanced feature, so the majority of users won't use it probably.
""", disambiguation=None)

        ui_popup(text)

    def hqporner_pages_help(self):
        ui_popup(QCoreApplication.tr("""
Videos are split into pages on HQPorner. One page contains 46 videos.
If you specify 2 pages 92 videos will therefore be loaded.

If no more videos are found it will break the loop and the received videos can be used.""", disambiguation=""))

    """
    Starting video download processes
    """

    def start_single_video(self):
        url = self.ui.lineedit_url.text()
        api_language = self.api_language
        one_time_iterator = []
        one_time_iterator.append(check_video(url=url, language=api_language))
        self.add_to_tree_widget_thread(iterator=one_time_iterator, search_limit=self.search_limit)

    def start_model(self):
        search_limit = self.search_limit
        model = self.ui.lineedit_model_url.text()
        pornhub_pattern = re.compile(r"(.*?)pornhub(.*?)")

        if pornhub_pattern.match(model):
            api_language = self.api_language
            if not isinstance(self.client, Client):
                client = Client(language=api_language)

            else:
                client = self.client

            model_object = client.get_user(model)
            videos = model_object.videos

        else:
            videos = hq_Client().get_videos_by_actress(model)

        self.add_to_tree_widget_thread(videos, search_limit=search_limit)

    def load_video(self, url):
        output_path = self.output_path
        api_language = self.api_language
        threading_mode = self.threading_mode
        directory_system = self.directory_system
        quality = self.quality

        video = check_video(url, language=api_language)
        title = video.title

        if isinstance(video, Video):
            author = video.author.name

        elif isinstance(video, hq_Video):
            pornstars = video.pornstars
            if len(pornstars) == 0:
                author = "no_author_found"

            else:
                author = pornstars[0]

        else:
            author = video.author

        output_path = Path(output_path)

        stripped_title = strip_title(title)
        logger_debug(f"Loading Video: {stripped_title}")

        if directory_system:
            author_path = output_path / author  # Use the '/' operator for joining paths
            author_path.mkdir(parents=True, exist_ok=True)  # Creates the directory if it does not exist
            output_file_path = author_path / f"{stripped_title}.mp4"
        else:
            output_file_path = output_path / f"{stripped_title}.mp4"

        if not output_file_path.exists():
            logger_debug("Processing Thread")
            self.process_video_thread(output_path=output_file_path, video=video, threading_mode=threading_mode,
                                      quality=quality)
        else:
            self.semaphore.release()
            if not isinstance(video, hq_Video):
                global downloaded_segments
                downloaded_segments += len(list(video.get_segments(quality=quality)))

    def return_client(self):
        if isinstance(self.client, Client):
            return self.client

        else:
            return Client(language=self.api_language)

    def process_video_thread(self, output_path, video, threading_mode, quality):
        """Checks which of the three types of threading the user selected and handles them."""
        self.download_thread = DownloadThread(video=video, output_path=output_path, quality=quality,
                                              threading_mode=threading_mode)
        self.download_thread.signals.progress.connect(self.update_progressbar)
        self.download_thread.signals.total_progress.connect(self.update_total_progressbar)
        self.download_thread.signals.progress_hqporner.connect(self.update_progressbar_hqporner)
        self.download_thread.signals.progress_eporner.connect(self.update_progressbar_eporner)
        self.download_thread.signals.progress_xnxx.connect(self.update_progressbar_xnxx)
        self.download_thread.signals.progress_xvideos.connect(self.update_progressbar_xvideos)
        # ADAPTION
        self.download_thread.signals_completed.completed.connect(self.download_completed)
        self.threadpool.start(self.download_thread)
        logger_debug("Started Download Thread!")

    """
    The following functions are used to connect data between Threads and the Main UI
    """

    def update_total_progressbar(self, value, maximum):
        self.ui.progressbar_total.setMaximum(maximum)
        self.ui.progressbar_total.setValue(value)

    def update_progressbar(self, value, maximum):
        self.ui.progressbar_pornhub.setMaximum(maximum)
        self.ui.progressbar_pornhub.setValue(value)

    def update_progressbar_hqporner(self, value, maximum):
        self.ui.progressbar_hqporner.setMaximum(maximum)
        self.ui.progressbar_hqporner.setValue(value)

    def update_progressbar_eporner(self, value, maximum):
        self.ui.progressbar_eporner.setMaximum(maximum)
        self.ui.progressbar_eporner.setValue(value)

    def update_progressbar_xnxx(self, value, maximum):
        self.ui.progressbar_xnxx.setMaximum(maximum)
        self.ui.progressbar_xnxx.setValue(value)

    def update_progressbar_xvideos(self, value, maximum):
        self.ui.progressbar_xvideos.setMaximum(maximum)
        self.ui.progressbar_xvideos.setValue(value)

    # ADAPTION
    def download_completed(self):
        logger_debug("Download Completed!")
        self.semaphore.release()

    def start_undefined_range(self):
        self.ui.progressbar_total.setRange(0, 0)

    def stop_undefined_range(self):
        self.ui.progressbar_total.setRange(0, 1)

    """
    The following functions are used for opening files / directories with the QFileDialog
    """

    def open_output_path_dialog(self):
        dialog = QFileDialog()
        path = dialog.getExistingDirectory()
        self.ui.lineedit_output_path.setText(str(path))
        self.output_path = path
        self.save_user_settings()

    def open_file_dialog(self):
        dialog = QFileDialog()
        file, types = dialog.getOpenFileName()
        self.ui.lineedit_file.setText(file)
        iterator = []

        with open(file, "r") as url_file:
            content = url_file.read().splitlines()

            for url in content:
                print(url)
                video = check_video(url, language=self.api_language)
                iterator.append(video)

            self.add_to_tree_widget_thread(iterator, search_limit=self.search_limit)

    """
    The following functions are related to the User's account
    """

    def login(self):
        username = self.ui.lineedit_username.text()
        password = self.ui.lineedit_password.text()

        try:
            self.client = Client(username, password, language=self.api_language)
            logger_debug("Login Successful!")
            ui_popup(self.language_string_login_successful)
            self.switch_login_button_state()

        except errors.LoginFailed:
            ui_popup(self.language_string_login_failed)

        except errors.ClientAlreadyLogged:
            ui_popup(QCoreApplication.tr("You are already logged in!", disambiguation=""))

    def check_login(self):
        if self.client.logged:
            return True

        elif not self.client.logged:
            self.login()
            if not self.client.logged:
                text = QCoreApplication.tr("There's a problem with the login. Please make sure you login first "
                                           "and then you try to get videos based on your account.", disambiguation="")
                ui_popup(text)
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
        query = self.ui.lineedit_search_query.text()

        if self.ui.radio_search_website_pornhub.isChecked():
            videos = Client().search(query, use_hubtraffic=True)
            search_limit = 100

        elif self.ui.radio_search_website_xvideos.isChecked():
            videos = xv_Client.search(query, pages=3)
            search_limit = 3 * 27

        elif self.ui.radio_search_website_hqporner.isChecked():
            videos = hq_Client.search_videos(query, pages=3)
            search_limit = 3 * 46

        self.add_to_tree_widget_thread(videos, search_limit=search_limit)

    def get_metadata_video(self):
        api_language = self.api_language
        video = self.ui.lineedit_metadata_video_url.text()
        video = check_video(url=video, language=api_language)

        if not video is False:
            self.metadata_thread = MetadataVideos(video)
            self.metadata_thread.signals.start_undefined.connect(self.start_undefined_range)
            self.metadata_thread.signals.data.connect(self.apply_metadata_video)
            self.threadpool.start(self.metadata_thread)

    def apply_metadata_video(self, data):
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
        api_language = self.api_language
        user = self.ui.lineedit_metadata_user_url.text()
        client = Client(language=api_language)
        user_object = client.get_user(user)

        self.user_metadata_thread = MetadataUser(user_object)
        self.user_metadata_thread.signals.start_undefined.connect(self.start_undefined_range)
        self.user_metadata_thread.signals.data.connect(self.apply_metadata_user)
        self.threadpool.start(self.user_metadata_thread)

    def apply_metadata_user(self, data):
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
        url = self.ui.lineedit_metadata_user_url.text()
        client = self.return_client()
        user = client.get_user(url)
        bio = user.bio
        ui_popup(bio)

    def get_user_avatar(self):
        url = self.ui.lineedit_metadata_user_url.text()
        client = self.return_client()
        user = client.get_user(url)
        avatar = user.avatar
        avatar.download(Path(self.output_path))
        user_string = self.get_user_avatar_language_string
        ui_popup(user_string)

    def get_video_thumbnail(self):
        api_language = self.api_language
        url = self.ui.lineedit_metadata_video_url.text()
        video = check_video(url=url, language=api_language)
        video.image.download(Path(self.output_path))
        user_string = self.get_video_thumbnail_language_string
        ui_popup(user_string)

    def get_top_porn_hqporner(self):
        if self.ui.radio_top_porn_week.isChecked():
            sort = hq_Sort.WEEK

        elif self.ui.radio_top_porn_month.isChecked():
            sort = hq_Sort.MONTH

        elif self.ui.radio_top_porn_all_time:
            sort = hq_Sort.ALL_TIME

        else:
            sort = None

        pages = self.ui.spinbox_pages.value()
        videos = hq_Client().get_top_porn(sort_by=sort, pages=pages)
        search_limit = pages * 46
        self.add_to_tree_widget_thread(iterator=videos, search_limit=search_limit)

    def get_by_category_hqporner(self):
        category_name = self.ui.lineedit_hqporner_category.text()
        pages = self.ui.spinbox_pages.value()
        all_categories = hq_Client().get_all_categories()

        if not category_name in all_categories:
            ui_popup(QCoreApplication.tr("Invalid Category. Press 'list categories' to see all possible ones.",
                                         disambiguation=""))

        else:
            videos = hq_Client().get_videos_by_category(name=category_name, pages=pages)
            search_limit = pages * 46
            self.add_to_tree_widget_thread(videos, search_limit)

    def get_brazzers_videos(self):
        pages = self.ui.spinbox_pages.value()
        search_limit = pages * 46
        videos = hq_Client().get_brazzers_videos(pages)
        self.add_to_tree_widget_thread(videos, search_limit)

    @classmethod
    def list_categories_hqporner(cls):
        categories_ = hq_Client().get_all_categories()
        categories = ",".join(categories_)
        ui_popup(categories)

    def get_random_video(self):
        list_object = []
        video = hq_Client().get_random_video()
        list_object.append(video)
        self.add_to_tree_widget_thread(list_object, search_limit=2)

    def show_credits(self):
        self.ui.textBrowser.setOpenExternalLinks(True)
        file = QFile(":/credits/README/CREDITS.md")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        self.ui.textBrowser.setHtml(markdown.markdown(stream.readAll()))


def main():
    setup_config_file()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    try:
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
            logger_debug(f"{language_code} translation loaded")

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

    except PermissionError as e:
        ui_popup(
            QCoreApplication.tr("Insufficient Permissions to access something. Please run Porn Fetch as root / admin",
                                disambiguation=""))
        logger_error(e)

    except ConnectionResetError as e:
        ui_popup(
            QCoreApplication.tr("Connection was reset. Are you connected to a public wifi or a university's wifi? ",
                                disambiguation=""))
        logger_error(e)

    except ConnectionError as e:
        ui_popup(QCoreApplication.tr("Connection Error, please make sure you have a stable internet connection",
                                     disambiguation=""))
        logger_error(e)

    except KeyboardInterrupt:
        sys.exit(0)

    except SSLError as e:
        ui_popup(QCoreApplication.tr(
            "SSLError: Your connection is blocked by your ISP / IT administrator (Firewall). If you are in a "
            "University or at school, please connect to a VPN / Proxy", disambiguation=""))
        logger_error(e)

    except TypeError:
        pass

    except OSError as e:
        ui_popup(QCoreApplication.tr(
            f"This error shouldn't happen. If you still see it it's REALLY important that you report the "
            f"following: {e}", disambiguation=""))
        logger_error(e)

    except ZeroDivisionError:
        pass

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

    except Exception as e:
        error_message = "An error occurred: " + str(e) + "\n" + traceback.format_exc()
        logger_error(error_message)
        if send_error_logs:
            send_error_log(error_message)
