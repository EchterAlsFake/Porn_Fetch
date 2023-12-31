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
__build__ = "desktop"  # android or desktop
__author__ = "Johannes Habel"


import requests
import re
import sys
import os.path
import argparse
import markdown
import time
import traceback
import src.frontend.resources

from requests.exceptions import SSLError
from pathlib import Path
from hqporner_api.api import Client as hq_Client, Quality as hq_Quality, Video as hq_Video
from hqporner_api.modules.locals import *
from phub import Quality, Client, errors, download, Video
from src.backend.shared_functions import *


from src.frontend.ui_form_desktop import Ui_Porn_Fetch_Widget
from src.frontend.License import Ui_License
from PySide6.QtCore import (QFile, QTextStream, Signal, QRunnable, QThreadPool, QObject, QSemaphore, Qt, QLocale,
                            QTranslator, QCoreApplication)
from PySide6.QtWidgets import (QWidget, QApplication, QMessageBox, QInputDialog, QCheckBox,
                               QTreeWidgetItem, QButtonGroup)
from PySide6.QtGui import QIcon, QFont


total_segments = 0
downloaded_segments = 0
send_error_logs = False  # Only enabled when developing the application.


def send_error_log(message):
    """A function to debug Porn Fetch on my local android development device"""
    url = "http://192.168.2.103:8000/error-log/"
    data = {"message": message}
    requests.post(url, json=data)


def get_output_path(path="/storage/emulated/0/Download"):
    """
    This will "brute" force the output path. I can't ask for runtime permissions due to some
    issues in Qt's QFileDialog and the general build process not allowing me to use pyjnius / Kivy

    This function will basically check some generic paths for storing the video files. If None was found, the user
    will be prompted to enter one.
    """
    if send_error_logs:
        send_error_log(f"Checking path: {path}")
    if not str(path).endswith("/"):
        path += "/"
        if send_error_logs:
            send_error_log(f"Appended /, now: {path}")

    if os.path.exists(path):
        if send_error_logs:
            send_error_log(f"Path: {path} Exists")
        if os.path.isfile(f"{path}test.txt"):
            if send_error_logs:
                send_error_log("File already exists")

            return True

        else:
            try:
                with open(f"{path}test.txt", "w") as text:
                    if send_error_logs:
                        send_error_log(f"Trying to write: {path}text.txt")
                    text.write("""
                    This is a test for the Porn Fetch application to check if Porn Fetch has permissions to write into
                    the download directory.""")
                    send_error_log("Written test.txt")
                    return True

            except Exception as e:
                if send_error_logs:
                    send_error_log(f"Nope: {e}")
                logger_error(e)
                return False

    else:
        if send_error_logs:
            send_error_log("Returning False")
        return False


def ui_popup(text):
    """ A simple UI popup that will be used for small messages to the user."""
    file = QFile(":/style/stylesheets/stylesheet_ui_popup.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)

    qmsg_box = QMessageBox()
    qmsg_box.setStyleSheet(stream.readAll())
    qmsg_box.setText(text)
    qmsg_box.exec()


class WorkerSignals(QObject):
    progress = Signal(int)
    completed = Signal()


class DownloadProgressSignal(QObject):
    """Sends the current download progress to the main UI to update the progressbar."""
    progress = Signal(int, int)
    progress_hqporner = Signal(int, int)
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
    def __init__(self, iterator, search_limit, data_mode, clickable):
        super(AddToTreeWidget, self).__init__()
        self.signals = TreeWidgetSignals()
        self.iterator = iterator
        self.search_limit = search_limit
        self.data_mode = data_mode
        self.clickable = clickable

    def run(self):
        self.signals.clear_signal.emit()
        disabled = QCoreApplication.tr("Disabled", disambiguation="It means, that the displaying of the"
                                                                  "author and duration in the tree widget is disabled")

        try:
            logger_debug(f"Search Limit: {str(self.search_limit)}")
            try:
                total = len(self.iterator)

            except Exception:
                logger_debug("Can't get length of the iterator. Progress won't be available!")
                total = None

            for i, video in enumerate(self.iterator, start=1):

                if i == self.search_limit + 1:
                    break

                if isinstance(video, hq_Video):
                    title = video.video_title
                    if self.data_mode == 1:
                        duration = int(video.video_length) / 60
                        pornstars = video.pornstars
                        if len(pornstars) == 0:
                            author = "author_not_found"

                        else:
                            author = pornstars[0]

                    else:
                        duration = disabled
                        author = disabled

                    text_data = [str(title), str(author), str(duration), str(i), video]

                else:
                    title = video.title
                    if self.data_mode == 1:
                        duration = round(video.duration.seconds / 60)
                        author = video.author.name

                    else:
                        duration = disabled
                        author = disabled

                    text_data = [str(title), str(author), str(duration), str(i), video]

                self.signals.progress.emit(total, i)
                self.signals.text_data.emit(text_data)

        except errors.NoResult:
            pass

        finally:
            self.signals.finished.emit()


class DownloadThread(QRunnable):
    """Threading class to download videos."""
    signal = Signal()

    def __init__(self, video, quality, output_path, threading_mode):
        super(DownloadThread, self).__init__()

        self.video = video
        self.quality = quality
        self.output_path = output_path
        self.threading_mode = threading_mode
        self.downloader = None
        self.signals = DownloadProgressSignal()
        self.signals_completed = WorkerSignals()

    def callback(self, pos, total):
        self.signals.progress.emit(pos, total)

        global downloaded_segments
        downloaded_segments += 1  # Assuming each call represents one segment
        self.signals.total_progress.emit(downloaded_segments, total_segments)

    def callback_hqporner(self, pos, total):
        self.signals.progress_hqporner.emit(pos, total)

    def run(self):
        try:
            if isinstance(self.video, Video):
                if self.threading_mode == 2:
                    self.downloader = download.threaded(max_workers=20, timeout=5)

                elif self.threading_mode == 1:
                    self.downloader = download.FFMPEG

                elif self.threading_mode == 0:
                    self.downloader = download.default

                self.video.download(downloader=self.downloader, path=self.output_path, quality=self.quality,
                                    display=self.callback)

            else:
                self.video.download(quality=hq_Quality.BEST, output_path=self.output_path,
                                    callback=self.callback_hqporner, no_title=True)

        finally:
            self.signals_completed.completed.emit()


class QTreeWidgetDownloadThread(QRunnable):
    """Threading class for the QTreeWidget (sends objects to the download class defined above)"""

    def __init__(self, treeWidget, semaphore, quality):
        super(QTreeWidgetDownloadThread, self).__init__()
        self.treeWidget = treeWidget
        self.semaphore = semaphore
        self.signals = QTreeWidgetSignal()
        self.quality = quality

    def run(self):
        self.signals.start_undefined_range.emit()
        video_objects_hqporner = []
        video_objects_pornhub = []

        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)
            checkState = item.checkState(0)
            if checkState == Qt.Checked:
                object_ = item.data(0, Qt.UserRole)
                if isinstance(object_, hq_Video):
                    video_objects_hqporner.append(object_)

                elif isinstance(object_, Video):
                    video_objects_pornhub.append(object_)

        global total_segments, downloaded_segments
        total_segments = sum(
            [len(list(video.get_segments(quality=self.quality))) for video in video_objects_pornhub])

        downloaded_segments = 0

        self.signals.stop_undefined_range.emit()
        videos = video_objects_pornhub + video_objects_hqporner
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
        self.signals.start_undefined.emit()

        like_string = QCoreApplication.tr("Likes", disambiguation="The Likes of the video")
        dislike_string = QCoreApplication.tr("Dislikes", disambiguation="The dislikes of the video")
        duration_string = QCoreApplication.tr("minutes", disambiguation="The duration of the video")

        title = self.video.title
        views = self.video.views
        duration = round(self.video.duration.seconds / 60, 2)
        duration = f"{duration} {duration_string}"
        pornstar_generator = self.video.pornstars
        tags_generator = self.video.tags
        rating = self.video.like
        orientation = self.video.orientation
        hotspots = self.video.hotspots

        pornstar_list = [pornstar.name for pornstar in pornstar_generator]
        tags_list = [tag.name for tag in tags_generator]
        hotspots_list = [str(hotspot) for hotspot in hotspots]

        pornstars = ", ".join(pornstar_list)
        tags = ", ".join(tags_list)
        hotspots_x = ", ".join(hotspots_list)
        rating = f"{like_string}: {rating.up} | {dislike_string}: {rating.down}"

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


class DownloadTreeWidget(QRunnable):
    def __init__(self, treeWidget, semaphore, quality):
        super(DownloadTreeWidget, self).__init__()
        self.treeWidget = treeWidget
        self.semaphore = semaphore
        self.quality = quality
        self.signals = QTreeWidgetSignal()

    def run(self):
        self.signals.start_undefined_range.emit()

        video_objects = []
        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)
            checkState = item.checkState(0)
            if checkState == Qt.Checked:
                video_objects.append(item.data(0, Qt.UserRole))

        global total_segments, downloaded_segments
        total_segments = sum(
            [len(list(video.get_segments(quality=self.quality))) for video in video_objects])

        downloaded_segments = 0

        self.signals.stop_undefined_range.emit()
        for video in video_objects:
            self.signals.progress.emit(video)


class Porn_Fetch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

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

        if __build__ == "android":
            self.setup_android()

        self.create_checkboxes()
        self.language_strings()
        self.settings_maps_initialization()
        self.load_user_settings()
        self.update_settings()

    def load_style(self):
        """a simple function to load the icons for the buttons"""
        self.ui.button_switch_search.setIcon(QIcon(":/images/graphics/search.svg"))
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

        file_progressbar_total = QFile(":/style/stylesheets/progressbar_total.qss")
        file_progressbar_total.open(QFile.ReadOnly | QFile.Text)
        stream_progress_total = QTextStream(file_progressbar_total)

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
        self.ui.button_search_videos.setStyleSheet(purple)
        self.ui.button_tree_download.setStyleSheet(purple)
        self.ui.button_metadata_user_start.setStyleSheet(purple)
        self.ui.button_metadata_video_start.setStyleSheet(purple)
        self.ui.button_user_download_avatar.setStyleSheet(purple)
        self.ui.button_user_get_bio.setStyleSheet(purple)
        self.ui.button_video_thumbnail_download.setStyleSheet(purple)
        self.ui.button_tree_select_all.setStyleSheet(orange)
        self.ui.button_tree_unselect_all.setStyleSheet(blue)
        self.ui.button_search_pornhub_filters.setStyleSheet(purple)
        self.ui.button_search_users.setStyleSheet(purple)
        self.ui.button_search_hqporner.setStyleSheet(purple)
        self.ui.button_help_pages.setStyleSheet(login)
        self.ui.button_semaphore_help.setStyleSheet(login)
        self.ui.button_threading_mode_help.setStyleSheet(login)
        self.ui.button_directory_system_help.setStyleSheet(login)
        self.ui.button_output_path_select.setStyleSheet(login)
        self.ui.button_settings_apply.setStyleSheet(login)

        self.ui.progressbar_pornhub.setStyleSheet(stream_progress_pornhub.readAll())
        self.ui.progressbar_hqporner.setStyleSheet(stream_progress_hqporner.readAll())
        self.ui.progressbar_total.setStyleSheet(stream_progress_total.readAll())
        logger_debug("Loaded Icons!")

    def language_strings(self):
        """Contains the language strings. Needed for translation"""
        self.get_api_language_string_dialog = QCoreApplication.tr("Please enter the language code for your "
                                                                  "language.  Example: en, de, fr, ru --=>:",
                                                                  disambiguation=None)

        self.get_output_path_string_ui_popup = QCoreApplication.tr("""The specified output path doesn't exist.
        If you think, this is an error, please report it!""", disambiguation=None)

        self.save_user_settings_language_string = QCoreApplication.tr("Saved User Settings!", disambiguation=None)
        self.open_file_language_string = QCoreApplication.tr("Select URL file", disambiguation=None)
        self.language_string_login_failed = QCoreApplication.tr("Login Failed, please check your credentials and try "
                                                                "again!", disambiguation=None)

        self.language_string_login_successful = QCoreApplication.tr("Login Successful!", disambiguation=None)
        self.get_user_avatar_language_string = QCoreApplication.tr("User Avatar saved in current directory...",
                                                                   disambiguation=None)
        self.get_video_thumbnail_language_string = QCoreApplication.tr("Video thumbnail saved in current directory",
                                                                       disambiguation=None)

    def button_groups(self):
        self.group_threading = QButtonGroup()
        self.group_threading.addButton(self.ui.radio_threading_no)
        self.group_threading.addButton(self.ui.radio_threading_yes)

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

        self.directory_system_group = QButtonGroup()
        self.directory_system_group.addButton(self.ui.radio_directory_system_no)
        self.directory_system_group.addButton(self.ui.radio_directory_system_yes)

        self.language_group = QButtonGroup()
        self.language_group.addButton(self.ui.radio_ui_language_english)
        self.language_group.addButton(self.ui.radio_ui_language_german)
        self.language_group.addButton(self.ui.radio_ui_language_french)

        self.radio_hqporner = QButtonGroup()
        self.radio_hqporner.addButton(self.ui.radio_top_porn_week)
        self.radio_hqporner.addButton(self.ui.radio_top_porn_month)
        self.radio_hqporner.addButton(self.ui.radio_top_porn_all_time)

    def create_checkboxes(self):
        self.checkboxes = {}
        member_attributes = [
            'IS_MODEL', 'IS_STAFF', 'IS_ONLINE', 'HAS_AVATAR', 'HAS_VIDEOS',
            'HAS_PHOTOS', 'HAS_PLAYLISTS', 'OFFER_FAN_CLUB', 'OFFER_CUSTOM_VIDEOS',
            'SINGLE', 'TAKEN', 'OPEN_RELATION', 'GENDER_MALE', 'GENDER_FEMALE',
            'GENDER_COUPLE', 'GENDER_TRANS_FEMALE', 'GENDER_FEMALE_COUPLE',
            'GENDER_TRANS_MALE', 'GENDER_NON_BINARY', 'GENDER_OTHER',
            'INTO_NONE', 'INTO_MALE', 'INTO_FEMALE', 'INTO_ALL'
        ]

        layout = self.ui.gridlayout_user_filter
        row, col = 0, 0
        for attr in member_attributes:
            checkbox = QCheckBox(attr.replace('_', ' ').title())
            checkbox.setObjectName(attr)
            self.checkboxes[attr] = checkbox
            layout.addWidget(checkbox, row, col)

            col += 1
            if col >= 3:  # Adjust the number of columns as needed
                col = 0
                row += 1

    def get_checked_filters(self):
        checked_filters = []
        for attr, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                checked_filters.append(f'Member.{attr}')

        return ' | '.join(checked_filters)

    def setup_android(self):
        if get_output_path():
            self.output_path = "/storage/emulated/0/Download/"

        else:
            ui_popup("""
The output path: /storage/emulated/0/Download does not exist.
The Permission System on Android is currently not working for me. 
If you know what you do, you can now enter a manual output path, which will be used!
If you don't know what /storage/ even is, please just close the App.

Sorry.""")

            text, ok = QInputDialog().getText(self, "Enter custom Path", "Enter custom Path:")
            if ok:
                if get_output_path(text):
                    ui_popup(f"Success: {text} will be used for this session!")
                    self.output_path = text

                else:
                    ui_popup("Sorry, but this path also doesn't exist, or I can't write to it. Sorry.")

        self.ui.lineedit_output_path.setDisabled(True)
        self.ui.button_open_file.setDisabled(True)
        scroll_area = QFile(":/style/stylesheets/stylesheet_scroll_area.qss")
        scroll_area.open(QFile.ReadOnly | QFile.Text)
        stream_scroll_area = QTextStream(scroll_area)
        stylesheet_scroll_area = stream_scroll_area.readAll()
        self.ui.scrollArea.setStyleSheet(stylesheet_scroll_area)
        self.ui.scrollArea_3.setStyleSheet(stylesheet_scroll_area)
        self.ui.button_switch_account.setIcon(QIcon(":/images/graphics/account.svg"))
        self.ui.button_switch_account.clicked.connect(self.switch_to_account)

    def switch_to_account(self):
        """Only needed for Android build"""
        self.ui.stacked_widget_top.setCurrentIndex(1)
        self.ui.stacked_widget_main.setCurrentIndex(0)
        self.layout().update()

    def switch_to_home(self):
        self.ui.stacked_widget_main.setCurrentIndex(0)
        self.ui.stacked_widget_top.setCurrentIndex(0)
        self.layout().update()

    def switch_to_search(self):
        self.ui.stacked_widget_main.setCurrentIndex(0)
        self.ui.stacked_widget_top.setCurrentIndex(2)
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
        time.sleep(0.3)
        self.show_credits()

    def button_connectors(self):
        """a function to link the buttons to their functions"""

        # Menu Bar Switch Button Connections
        self.ui.button_switch_home.clicked.connect(self.switch_to_home)
        self.ui.button_switch_search.clicked.connect(self.switch_to_search)
        self.ui.button_switch_settings.clicked.connect(self.switch_to_settings)
        self.ui.button_switch_credits.clicked.connect(self.switch_to_credits)
        self.ui.button_switch_metadata.clicked.connect(self.switch_to_metadata)

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
        self.ui.button_search_videos.clicked.connect(self.basic_search)
        # self.ui.button_search_users.clicked.connect(self.search_users)
        # self.ui.button_search_hqporner.clicked.connect(self.hqporner_search)

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


        logger_debug("Connected Buttons!")


    def switch_login_button_state(self):
        file = QFile(":/style/stylesheets/stylesheet_switch_buttons_login_state.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        stylesheet = stream.readAll()

        self.ui.button_get_liked_videos.setStyleSheet(stylesheet)
        self.ui.button_get_watched_videos.setStyleSheet(stylesheet)
        self.ui.button_get_recommended_videos.setStyleSheet(stylesheet)

    """
    The following are functions used by different other functions to handle data over different classes / threads.
    Mostly by using signals and slot connectors. I don't recommend anyone to change stuff here!
    (It's already complicated enough, even with the Documentation)
    """

    def get_quality(self):
        """Returns the quality selected by the user"""
        if self.ui.radio_quality_best.isChecked():
            self.quality = Quality.BEST

        elif self.ui.radio_quality_half.isChecked():
            self.quality = Quality.HALF

        elif self.ui.radio_quality_worst.isChecked():
            self.quality = Quality.WORST

    def get_semaphore_limit(self):
        """Returns the semaphore limit selected by the user"""
        value = self.ui.spinbox_semaphore.value()
        if value >= 1:
            self.semaphore_limit = value

    def get_threading_mode(self):
        """Returns the threading mode selected by the user"""
        if self.ui.radio_threading_mode_default.isChecked():
            self.threading_mode = 0

        elif self.ui.radio_threading_mode_ffmpeg.isChecked():
            self.threading_mode = 1

        elif self.ui.radio_threading_mode_high_performance.isChecked():
            self.threading_mode = 2

    def get_threading(self):
        """Checks if threading should be used or not"""
        if self.ui.radio_threading_yes.isChecked():
            self.threading = True

        elif self.ui.radio_threading_no.isChecked():
            self.threading = False

    def get_search_limit(self):
        """Returns the search limit selected by the user"""
        search_limit = self.ui.spinbox_searching.value() if self.ui.spinbox_searching.value() >= 1 else 50
        self.search_limit = search_limit

    def is_directory_system(self):
        """Checks if the directory system was enabled"""
        if self.ui.radio_directory_system_yes.isChecked():
            self.directory_system = True

        elif self.ui.radio_directory_system_no.isChecked():
            self.directory_system = False

    def update_settings(self):
        """Updates all settings, so that the cache gets reloaded."""
        self.get_threading()
        self.get_search_limit()
        self.get_threading_mode()
        self.get_quality()
        self.is_directory_system()
        self.get_semaphore_limit()

    def settings_maps_initialization(self):
        self.native_languages = ["en", "de", "fr", "ru", "zh"]

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
            "zh": self.ui.radio_api_language_chinese
        }

        self.threading_map = {
            "yes": self.ui.radio_threading_yes,
            "no": self.ui.radio_threading_no
        }

        self.threading_mode_map = {
            "2": self.ui.radio_threading_mode_high_performance,
            "1": self.ui.radio_threading_mode_ffmpeg,
            "0": self.ui.radio_threading_mode_default
        }

        self.directory_system_map = {
            "1": self.ui.radio_directory_system_yes,
            "0": self.ui.radio_directory_system_no
        }

    def load_user_settings(self):
        """Loads the user settings from the configuration file and applies them."""

        # Apply settings
        self.quality_map.get(self.conf.get("Video", "quality")).setChecked(True)
        self.language_map.get(self.conf.get("Video", "language")).setChecked(True)
        self.threading_map.get(self.conf.get("Performance", "threading")).setChecked(True)
        self.threading_mode_map.get(self.conf.get("Performance", "threading_mode")).setChecked(True)
        self.directory_system_map.get(self.conf.get("Video", "directory_system")).setChecked(True)

        self.ui.spinbox_semaphore.setValue(int(self.conf.get("Performance", "semaphore")))
        self.ui.spinbox_searching.setValue(int(self.conf.get("Video", "search_limit")))
        self.ui.lineedit_output_path.setText(self.conf.get("Video", "output_path"))

        self.semaphore_limit = self.conf.get("Performance", "semaphore")
        self.search_limit = self.conf.get("Video", "search_limit")
        self.output_path = self.conf.get("Video", "output_path")

        self.gui_language = self.conf.get("UI", "language")

        if self.gui_language == "en":
            self.ui.radio_ui_language_english.setChecked(True)

        elif self.gui_language == "de":
            self.ui.radio_ui_language_german.setChecked(True)

        elif self.gui_language == "fr":
            self.ui.radio_ui_language_french.setChecked(True)

        self.semaphore = QSemaphore(int(self.semaphore_limit))
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

        # Save threading setting
        for threading, radio_button in self.threading_map.items():
            if radio_button.isChecked():
                self.conf.set("Performance", "threading", threading)

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
        self.conf.set("Video", "search_limit", str(self.ui.spinbox_searching.value()))
        self.conf.set("Video", "output_path", self.ui.lineedit_output_path.text())

        if self.ui.radio_ui_language_french.isChecked():
            self.conf.set("UI", "language", "fr")

        elif self.ui.radio_ui_language_german.isChecked():
            self.conf.set("UI", "language", "de")

        elif self.ui.radio_ui_language_english.isChecked():
            self.conf.set("UI", "language", "en")

        self.update_settings()

        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)

        ui_popup(self.save_user_settings_language_string)
        logger_debug("Saved User Settings!")

    """
    The following functions are related to the tree widget    
    """

    def add_to_tree_widget_thread(self, iterator, search_limit, clickable=False):
        if clickable:
            for user_object in iterator:
                uploads = user_object.uploads
                if uploads:
                    print("User has uploaded videos")

        if self.ui.radio_tree_show_title.isChecked():
            data_mode = 0

        elif self.ui.radio_tree_show_all.isChecked():
            data_mode = 1

        else:
            data_mode = 0

        self.thread = AddToTreeWidget(iterator, search_limit, data_mode, clickable)
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
                                                         quality=quality)
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

    """
    Starting video download processes
    """

    def start_single_video(self):
        self.update_settings()
        url = self.ui.lineedit_url.text()
        api_language = self.api_language
        one_time_iterator = []
        if url.endswith(".html"):
            one_time_iterator.append(check_video(url=url, language=api_language))

        else:
            one_time_iterator.append(check_video(url=url, language=api_language))

        self.add_to_tree_widget_thread(iterator=one_time_iterator, search_limit=self.search_limit)

    def start_model(self):
        search_limit = self.search_limit
        model = self.ui.lineedit_model_url.text()

        actress_pattern = re.compile(r"https://hqporner\.com/actress/(.+)")
        pornhub_pattern = re.compile(r"(.*?)pornhub(.*?)")

        match = actress_pattern.match(model)
        if match:
            # Extract the actress name from the URL
            model = match.group(1)
            videos = hq_Client().get_videos_by_actress(name=model)

        elif pornhub_pattern.match(model):
            api_language = self.api_language
            if not isinstance(self.client, Client):
                client = Client(language=api_language)
            else:
                client = self.client

            model_object = client.get_user(model)
            videos = model_object.videos

        elif not model.startswith("https://"):
            videos = hq_Client().get_videos_by_actress(name=model)

        else:
            return

        self.add_to_tree_widget_thread(videos, search_limit=search_limit)

    def load_video(self, url):
        self.update_settings()
        output_path = self.output_path
        api_language = self.api_language
        threading_mode = self.threading_mode
        directory_system = self.directory_system
        quality = self.quality
        video = check_video(url, language=api_language)
        if isinstance(video, hq_Video):
            title = video.video_title
            pornstars = video.pornstars
            if len(pornstars) == 0:
                author = "no_author_found"

            else:
                author = pornstars[0]

        elif isinstance(video, Video):
            video = check_video(url, language=api_language)
            title = video.title
            author = video.author.name

        else:
            ui_popup(
                QCoreApplication.tr("There's something wrong with the video. Is the URL correct?", disambiguation=""))
            title = None
            author = None

        output_path = correct_output_path(output_path)
        stripped_title = strip_title(title)
        logger_debug(f"Loading Video: {stripped_title}")

        if directory_system:
            if not os.path.exists(f"{output_path}{author}"):
                os.mkdir(output_path + author)

            output_path = f"{output_path}{author}{os.sep}{stripped_title}.mp4"
            output_path.strip("'")

        else:
            output_path = f"{output_path}{stripped_title}.mp4"
            output_path.strip("'")

        if not check_if_video_exists(video, output_path):
            if self.threading:
                logger_debug("Processing Thread")
                self.process_video_thread(output_path=output_path, video=video, threading_mode=threading_mode,
                                          quality=quality)

            elif not self.threading:
                self.process_video_without_thread(output_path, video, quality)

        else:
            self.semaphore.release()
            if not isinstance(video, hq_Video):
                global downloaded_segments
                downloaded_segments += len(list(video.get_segments(quality=quality)))

    def return_client(self):
        if isinstance(self.client, Client):
            return self.client

        else:
            self.update_settings()
            api_language = self.api_language
            return Client(language=api_language)

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

    def download_completed(self):
        logger_debug("Download Completed!")
        self.semaphore.release()

    def start_undefined_range(self):
        self.ui.progressbar_total.setRange(0, 0)

    def stop_undefined_range(self):
        self.ui.progressbar_total.setRange(0, 1)

        """
        The following functions are related to the QFileDialog
        """

    def process_video_thread(self, output_path, video, threading_mode, quality):
        """Checks which of the three types of threading the user selected and handles them."""
        self.download_thread = DownloadThread(video=video, output_path=output_path, quality=quality,
                                              threading_mode=threading_mode)
        self.download_thread.signals.progress.connect(self.update_progressbar)
        self.download_thread.signals.total_progress.connect(self.update_total_progressbar)
        self.download_thread.signals.progress_hqporner.connect(self.update_progressbar_hqporner)
        self.download_thread.signals_completed.completed.connect(self.download_completed)
        self.threadpool.start(self.download_thread)
        logger_debug("Started Download Thread!")

    def process_video_without_thread(self, output_path, video, quality):
        """Downloads the video without any threading.  (NOT RECOMMENDED!)"""
        logger_debug("Downloading without threading! Note, the GUI will freeze until the video is downloaded!!!")
        video.download(path=output_path, quality=quality, downloader=download.default)
        logger_debug("Download Completed!")

    """
    The following functions are related to the User's account
    """

    def login(self):
        username = self.ui.lineedit_username.text()
        password = self.ui.lineedit_password.text()
        self.update_settings()

        try:
            self.client = Client(username, password, language=self.api_language)
            self.logger_debug("Login Successful!")
            ui_popup(self.language_string_login_successful)
            self.switch_login_button_state()

        except errors.LoginFailed:
            ui_popup(self.language_string_login_failed)

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
        self.update_settings()
        query = self.ui.lineedit_search_query.text()
        language = self.api_language
        search_limit = self.search_limit
        client = Client(language=language)
        search = client.search(query, use_hubtraffic=True)
        self.add_to_tree_widget_thread(search, search_limit=search_limit)

    def hqporner_search(self):
        query = self.ui.lineedit_search_hqporner.text()
        search_limit = self.search_limit
        search = hq_Client().get_videos_by_actress(query)
        self.add_to_tree_widget_thread(iterator=search, search_limit=search_limit)

    def search_users(self):
        query = self.ui.lineedit_search_users.text()
        search_limit = self.search_limit
        filters = self.get_checked_filters()
        search = Client().search_user(query, filters)
        logger_debug("Received Search Query")
        self.add_to_tree_widget_thread(iterator=search, search_limit=search_limit, clickable=True)

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
        interested_in = data[0]
        relationship = data[1]
        city_and_country = data[2]
        gender = data[3]
        birth_place = data[4]
        height = data[5]
        weight = data[6]
        ethnicity = data[7]
        hair_color = data[8]
        fake_boobs = data[9]
        tattoos = data[10]
        piercings = data[11]
        hometown = data[12]
        interests_and_hobbies = data[13]
        turn_ons = data[14]
        turn_offs = data[15]
        video_views = data[16]
        profile_views = data[17]
        videos_watched = data[18]
        type = data[19]
        name = data[20]

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
            sort = Sort.WEEK

        elif self.ui.radio_top_porn_month.isChecked():
            sort = Sort.MONTH

        elif self.ui.radio_top_porn_all_time:
            sort = Sort.ALL_TIME

        else:
            sort = None

        pages = self.ui.spinbox_pages.value()
        videos = hq_Client().get_top_porn(sort_by=sort, pages=pages)
        search_limit = self.search_limit
        self.add_to_tree_widget_thread(iterator=videos, search_limit=search_limit)

    def get_by_category_hqporner(self):
        category_name = self.ui.lineedit_hqporner_category.text()
        pages = self.ui.spinbox_pages.value()
        search_limit = self.search_limit
        all_categories = hq_Client().get_all_categories()

        if not category_name in all_categories:
            ui_popup("Invalid Category. Press 'list categories' to see all possible ones.")

        else:
            videos = hq_Client().get_videos_by_category(name=category_name, pages=pages)
            self.add_to_tree_widget_thread(videos, search_limit)

    def get_brazzers_videos(self):
        pages = self.ui.spinbox_pages.value()
        videos = hq_Client().get_brazzers_videos(pages)
        self.add_to_tree_widget_thread(videos, search_limit=False)

    def list_categories_hqporner(self):
        categories_ = hq_Client().get_all_categories()
        categories = ",".join(categories_)
        ui_popup(categories)

    def hqporner_pages_help(self):
        ui_popup("""
Videos are split into pages on HQPorner. One page contains 46 videos.
If you specify 2 pages 92 videos will therefore be loaded.

If no more videos are found it will break the loop and the received videos can be used.""")

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
            # Get the language code (e.g., "de" for German)
            language_code = locale.name().split('_')[0]
            # Construct the path to the translation file

        else:
            language_code = language
        path = f":/translations/translations/{language_code}.qm"

        translator = QTranslator(app)
        if translator.load(path):
            logger_debug(f"{language_code} translation loaded")
            app.installTranslator(translator)
        else:
            logger_debug(f"Failed to load {language_code} translation")

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

    except PermissionError:
        ui_popup(
            QCoreApplication.tr("Insufficient Permissions to access something. Please run Porn Fetch as root / admin",
                                disambiguation=""))

    except ConnectionResetError:
        ui_popup(
            QCoreApplication.tr("Connection was reset. Are you connected to a public wifi or a university's wifi? ",
                                disambiguation=""))

    except ConnectionError:
        ui_popup(QCoreApplication.tr("Connection Error, please make sure you have a stable internet connection",
                                     disambiguation=""))

    except KeyboardInterrupt:
        sys.exit(0)

    except SSLError:
        ui_popup(QCoreApplication.tr(
            "SSLError: Your connection is blocked by your ISP / IT administrator (Firewall). If you are in a "
            "University or at school, please connect to a VPN / Proxy", disambiguation=""))

    except TypeError:
        pass

    except OSError as e:
        ui_popup(QCoreApplication.tr(
            f"This error shouldn't happen. If you still see it it's REALLY important that you report the "
            f"following: {e}", disambiguation=""))

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
