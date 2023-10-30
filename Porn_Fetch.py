__author__ = "EchterAlsFake : Johannes Habel"
__version__ = "3.0"
__source__ = "https://github.com/EchterAlsFake/Porn_Fetch"
__license__ = "GPL 3"

import argparse
import math
import os
import random
import sys
import src.frontend.resource
from configparser import ConfigParser  # See: https://github.com/python/cpython/blob/main/Lib/configparser.py

import requests  # See: https://github.com/psf/requests
from PySide6 import QtCore  # See: https://pypi.org/project/PySide6/
from PySide6.QtCore import Signal, QThreadPool, QRunnable, QObject, Slot, QTranslator, QLocale, QSemaphore, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QWidget, QMessageBox, QTreeWidgetItem, QButtonGroup,
                               QVBoxLayout, QHBoxLayout, QRadioButton, QCheckBox, QPushButton, QScrollArea, QGroupBox)
from hqporner_api import API  # See: https://github.com/EchterAlsFake/hqporner_api
from phub import Client, Quality, locals, errors  # See https://github.com/Egsagon/PHUB
from phub.modules.download import threaded

from Porn_Fetch_CLI import CLI
from src.frontend.Porn_Fetch_v3 import Ui_Porn_Fetch_widget
from src.frontend.license_agreement import Ui_License_Widget
from src.frontend.setup import setup_config_file, strip_title, logging, check_if_video_exists

categories = [attr for attr in dir(locals.Category) if
              not callable(getattr(locals.Category, attr)) and not attr.startswith("__")]


class License(QWidget):
    """ License class to display the GPL 3 License to the user."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_widget = None
        self.conf = ConfigParser()
        self.conf.read("config.ini")

        self.ui = Ui_License_Widget()
        self.ui.setupUi(self)
        self.ui.button_accept.clicked.connect(self.accept)
        self.ui.button_deny.clicked.connect(self.denied)

    def check_license_and_proceed(self):
        if self.conf["License"]["accept"] == "true":
            self.show_main_window()

        else:
            logging(msg="License was not accepted.")
            self.show()  # Show the license widget

    def accept(self):
        self.conf.set("License", "accept", "true")
        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)
            config_file.close()

        self.show_main_window()

    def denied(self):
        self.conf.set("License", "accept", "false")
        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)
            config_file.close()
            self.close()
            sys.exit(0)

    def show_main_window(self):
        """ If license was accepted, the License widget is closed and the main widget will be shown."""
        self.close()
        logging(msg="Starting Porn Fetch main widget")
        self.main_widget = Widget()
        self.main_widget.show()


class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super(CustomTitleBar, self).__init__(parent)
        self._parent = parent

        self.setAutoFillBackground(True)

        self.close_btn = QPushButton("X", self)
        self.close_btn.clicked.connect(self._parent.close)

        self.minimize_btn = QPushButton("-", self)
        self.minimize_btn.clicked.connect(self._parent.showMinimized)

        self.fullscreen_btn = QPushButton("[ ]", self)
        self.fullscreen_btn.clicked.connect(self.toggle_maximize_restore)

        layout = QHBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(self.minimize_btn)
        layout.addWidget(self.fullscreen_btn)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)
        self.setFixedHeight(30)  # or whatever height you want

    def toggle_maximize_restore(self):
        if self._parent.isMaximized():
            self._parent.showNormal()
        else:
            self._parent.showMaximized()





def ui_popup(text):
    """ A simple UI popup that will be used for small messages to the user."""
    qmsg_box = QMessageBox()
    qmsg_box.setText(text)
    qmsg_box.exec()


def update_progressbar(pos, total, progress_bar):
    progress_bar.setMaximum(total)
    progress_bar.setValue(pos)


def help_speed():
    text = """
Speed (or Delay) is the requests limit per second.

If speed is set to 'usual' then the Delay will be 0.5 which means, that you will download
1 Segment of a video every 0.5 seconds. A video download can take like 2 minutes (also depends on your internet
connection). 

I recommend setting speed to 'high' in most use cases, but if you download a lot of videos and with that I mean like 10+
you should definitely set speed to 'usual' to prevent errors and increase stability."""
    ui_popup(text)


def help_threading():
    text = """
Threading means, that multiple cores of your CPU will be used to download multiple videos at once.
If you have a really fast internet connection, this can save you a lot of time. 

If threading is disabled, the Graphical User Interface won't respond to any actions, during a download.
That's why it's enabled by default.
"""
    ui_popup(text)


def add_to_tree_widget(iterator, tree_widget, search_limit=False):
    tree_widget.clear()
    try:
        if not search_limit:
            for i, video in enumerate(iterator, start=1):
                item = QTreeWidgetItem(tree_widget)
                item.setText(0, f"{i}) {video.title}")
                item.setData(0, QtCore.Qt.UserRole, video.url)
                item.setCheckState(0, QtCore.Qt.Unchecked)  # Adds a checkbox

        else:
            logging(f"Search Limit: {search_limit}")
            for i, video in enumerate(iterator[0:search_limit], start=1):
                item = QTreeWidgetItem(tree_widget)
                item.setText(0, f"{i}) {video.title}")
                item.setData(0, QtCore.Qt.UserRole, video.url)
                item.setCheckState(0, QtCore.Qt.Unchecked)  # Adds a checkbox

    except Exception as e:
        ui_popup(f"An error happened. ERROR: {e}")


def create_button_group(buttons):
    """Creates a QButtonGroup and adds the given buttons to it."""
    button_group = QButtonGroup()
    for button in buttons:
        button_group.addButton(button)
    return button_group


class WorkerSignals(QObject):
    progress = Signal(int)
    completed = Signal()


class DownloadWorker(QRunnable):
    def __init__(self, video, quality, output_path):
        super(DownloadWorker, self).__init__()
        self.video = video
        self.quality = quality
        self.output_path = output_path
        self.signals = WorkerSignals()

    def run(self):
        urls = API().get_final_urls(self.video)
        url = f"http:{urls[self.quality]}"
        title = API().extract_title(self.video)
        title = strip_title(title)
        final_path = os.path.join(self.output_path, title + ".mp4")
        response = requests.get(url, stream=True)
        file_size = int(response.headers.get('content-length', 0))

        if not os.path.exists(final_path):
            with open(final_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
                    progress = math.ceil((file.tell() / file_size) * 100)
                    self.signals.progress.emit(progress)

        self.signals.completed.emit()
        # Thanks to ChatGPT for programming this function. I am just too stupid for math calculations ^^


class DownloadProgressSignal(QObject):
    """Sends the current download progress to the main UI to update the progressbar."""
    progress = Signal(int, int)


class DownloadThread(QRunnable):
    """
    Uses threading to download the videos without interfering with the main UI
    Will be used when the 'Yes' Box is checked in the main UI.
    """

    def __init__(self, video, quality, output_path, semaphore):
        super().__init__()
        self.video = video
        self.quality = quality
        self.output_path = output_path
        self.signals = DownloadProgressSignal()
        self.signals_completed = WorkerSignals()
        self.semaphore = semaphore

    def callback(self, pos, total):
        self.signals.progress.emit(pos, total)

    def run(self):
        try:
            self.video.download(display=self.callback, quality=self.quality, path=self.output_path,
                                downloader=threaded())

        except OSError:
            logging("OS Error in Download Thread!", level=1)
            self.video.download(display=self.callback, quality=self.quality, path="os_error_fixed_title.mp4",
                                downloader=threaded())

        self.signals_completed.completed.emit()


class CategoryFilterWindow(QWidget):
    # Entirely coded by ChatGPT.
    def __init__(self):
        super().__init__()
        self.radio_buttons = {}
        self.checkboxes = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        left_layout = QVBoxLayout()
        left_group = QGroupBox("Select Category")

        for category in categories:
            radio_button = QRadioButton(category)
            left_layout.addWidget(radio_button)
            self.radio_buttons[category] = radio_button

        left_group.setLayout(left_layout)

        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setWidget(left_group)

        right_layout = QVBoxLayout()
        right_group = QGroupBox("Exclude Categories")

        for category in categories:
            checkbox = QCheckBox(category)
            right_layout.addWidget(checkbox)
            self.checkboxes[category] = checkbox

        right_group.setLayout(right_layout)

        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setWidget(right_group)

        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.on_apply)

        hlayout = QHBoxLayout()
        hlayout.addWidget(left_scroll)
        hlayout.addWidget(right_scroll)

        layout.addLayout(hlayout)
        layout.addWidget(apply_button)
        self.setLayout(layout)

    def on_apply(self):
        selected_category = None
        excluded_categories = []

        for category, radio_button in self.radio_buttons.items():
            if radio_button.isChecked():
                selected_category = category

        for category, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                excluded_categories.append(category)

        self.conf = ConfigParser()
        self.conf.read("config.ini")

        if selected_category is not None:
            self.conf.set("Porn_Fetch", "categories", selected_category)

        if excluded_categories:
            excluded_categories_str = ','.join(excluded_categories)
            self.conf.set("Porn_Fetch", "excluded_categories", excluded_categories_str)

        with open('config.ini', 'w') as configfile:
            self.conf.write(configfile)


class Widget(QWidget):
    """Main UI widget. Design is loaded from the ui_main_widget.py file. Feel free to change things if you want."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.conf = ConfigParser()
        self.conf.read("config.ini")

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.title_bar = CustomTitleBar(self)


        self.video = None
        self.api_language = "en"
        self.custom_language = False
        self.delay = True
        self.client = None
        self.sort = None
        self.sort_time = None
        self.production = None
        self.mode = None
        self.hd = None
        self.buttonGroups = None
        self.download_thread = None
        self.path = None
        self.search_limit = 50
        self.excluded_categories_filter = None
        self.excluded_categories = None
        self.excluded_categories_str = None
        self.selected_category_value = None
        self.selected_category = None
        self.videos_total = 0
        self.videos_downloaded = 0
        self.threadpool = QThreadPool.globalInstance()
        self.semaphore = QSemaphore(1)

        self.ui = Ui_Porn_Fetch_widget()
        self.ui.setupUi(self)
        self.ui.button_video.setIcon(QIcon(":/graphics/graphics/download.svg"))
        self.ui.button_account.setIcon(QIcon(":/graphics/graphics/account.svg"))
        self.ui.button_settings.setIcon(QIcon(":/graphics/graphics/settings.svg"))
        self.setWindowIcon(QIcon(":/graphics/graphics/logo.png"))
        logging("Loaded Icons")
        self.ui.groupBox_3.setDisabled(True)
        self.button_group()  # Needs to be called before load_user_settings!
        self.load_user_settings()  # Loads the user settings from config.ini to make settings persistent
        self.load_search_filters()  # Must be called before load_user_settings!
        logging(f"Delay Set to: {self.delay}")
        logging(f"API Language is: {self.api_language}")
        logging(f"Threading: {self.mode}")
        self.client = Client(language=self.api_language, delay=self.delay)
        self.ui.stackedWidget_3.setCurrentIndex(0)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.button_connectors()

    def button_connectors(self):
        self.ui.button_video_url_start.clicked.connect(self.start)
        self.ui.button_file_start.clicked.connect(self.start_file)
        self.ui.button_get_metadata.clicked.connect(self.get_metadata)
        self.ui.button_model_url_start.clicked.connect(self.user_channel)
        self.ui.button_search_start.clicked.connect(self.search_videos)
        self.ui.button_download_tree_widget.clicked.connect(self.download_tree)
        self.ui.button_settings_apply.clicked.connect(self.settings_tab)
        self.ui.button_login.clicked.connect(self.login)
        self.ui.button_get_liked.clicked.connect(self.get_liked_videos)
        self.ui.button_get_recommended.clicked.connect(self.get_recommended_videos)
        self.ui.button_get_watched.clicked.connect(self.get_watched_videos)
        self.ui.button_download_thumbnail.clicked.connect(self.download_thumbnail)
        self.ui.button_video.clicked.connect(self.switch_video_page)
        self.ui.button_account.clicked.connect(self.switch_account_page)
        self.ui.button_settings.clicked.connect(self.switch_to_settings)
        self.ui.button_miscellaneus.clicked.connect(self.switch_to_miscellaneous)
        self.ui.button_credits.clicked.connect(self.switch_to_credits)
        self.ui.button_category_filters.clicked.connect(self.set_category_filters)
        self.ui.button_speed_help.clicked.connect(help_speed)
        self.ui.button_threading_help.clicked.connect(help_threading)
        self.ui.button_user_information.clicked.connect(self.get_user_information)
        self.ui.button_user_biography.clicked.connect(self.get_user_bio)
        self.ui.button_switch_user_metadata.clicked.connect(self.switch_to_user_metadata)
        self.ui.button_switch_video_metadata.clicked.connect(self.switch_to_video_metadata)
        self.ui.button_select_all.clicked.connect(self.select_all_items)
        self.ui.button_unselect_all.clicked.connect(self.unselect_all_items)
        self.ui.button_custom_api.clicked.connect(self.custom_api_language)
        self.ui.button_download_avatar.clicked.connect(self.download_avatar)

    def switch_video_page(self):
        self.ui.stackedWidget_3.setCurrentIndex(0)
        self.ui.stackedWidget.setCurrentIndex(0)

    def switch_account_page(self):
        self.ui.stackedWidget_3.setCurrentIndex(0)
        self.ui.stackedWidget.setCurrentIndex(1)

    def switch_to_settings(self):
        self.ui.stackedWidget_3.setCurrentIndex(1)

    def switch_to_miscellaneous(self):
        self.ui.stackedWidget_3.setCurrentIndex(2)

    def switch_to_credits(self):
        self.ui.stackedWidget_3.setCurrentIndex(3)

    def switch_to_video_metadata(self):
        self.ui.stacked_widget_metadata.setCurrentIndex(0)

    def switch_to_user_metadata(self):
        self.ui.stacked_widget_metadata.setCurrentIndex(1)

    def download_completed(self):
        self.videos_downloaded += 1
        logging("Download Completed!")
        text = f"Downloaded: {self.videos_downloaded} / {self.videos_total}"
        logging(text)
        self.ui.lineedit_total.setText(str(text))
        self.semaphore.release()

    def set_category_filters(self):
        """
        Starts the external Class for the Category Filters
        """

        self.window = CategoryFilterWindow()
        self.window.show()
        logging("Displaying Category Window Widget")

    def button_group(self):
        """Separates the QRadioButtons from the different grid layouts"""

        button_groups = {
            "quality": [self.ui.radio_quality_best, self.ui.radio_quality_worst, self.ui.radio_quality_middle],
            "threading": [self.ui.radio_threading_yes, self.ui.radio_threading_no],
            "api_language": [self.ui.api_radio_es, self.ui.api_radio_fr, self.ui.api_radio_en, self.ui.api_radio_de,
                             self.ui.api_radio_ru, self.ui.radio_api_custom],
            "sort": [self.ui.radio_most_recent, self.ui.radio_most_relevant, self.ui.radio_most_viewed,
                     self.ui.radio_longest, self.ui.radio_top_rated, self.ui.radio_sort_ignore],
            "sort_time": [self.ui.radio_day, self.ui.radio_month, self.ui.radio_year, self.ui.radio_week,
                          self.ui.radio_time_sort_ignore],
            "production": [self.ui.radio_production_ignore, self.ui.radio_homemade, self.ui.radio_professional],
            "ui_language": []
        }
        self.buttonGroups = tuple(create_button_group(buttons) for buttons in button_groups.values())

    def get_client_language(self):
        """Checks the radio button for the language used for the API client"""

        if self.ui.api_radio_de.isChecked():
            self.api_language = "de"

        elif self.ui.api_radio_en.isChecked():
            self.api_language = "en"

        elif self.ui.api_radio_fr.isChecked():
            self.api_language = "fr"

        elif self.ui.api_radio_ru.isChecked():
            self.api_language = "ru"

        elif self.ui.api_radio_es.isChecked():
            self.api_language = "es"

        else:
            self.api_language = "en"

    def get_quality(self):
        """Checks the radio button for the quality used for the video object"""

        if self.ui.radio_quality_best.isChecked():
            return Quality.BEST

        elif self.ui.radio_quality_middle.isChecked():
            return Quality.HALF

        elif self.ui.radio_quality_worst.isChecked():
            return Quality.WORST

        else:
            return Quality.BEST

    def unselect_all_items(self):
        root = self.ui.treeWidget.invisibleRootItem()
        item_count = root.childCount()
        for i in range(item_count):
            item = root.child(i)
            item.setCheckState(0, QtCore.Qt.Unchecked)

    def select_all_items(self):
        root = self.ui.treeWidget.invisibleRootItem()
        item_count = root.childCount()
        for i in range(item_count):
            item = root.child(i)
            item.setCheckState(0, QtCore.Qt.Checked)

    def download_raw(self, video, output_path):
        self.semaphore.acquire()
        quality = 0  # Default to low quality
        if self.ui.radio_quality_middle.isChecked():
            quality = 1
        elif self.ui.radio_quality_best.isChecked():
            quality = -1

        worker = DownloadWorker(video, quality, output_path)
        worker.signals.progress.connect(self.update_progressbar)
        worker.signals.completed.connect(self.download_completed)
        # Start the worker in a new thread
        self.threadpool.start(worker)

    @Slot(int)
    def update_progressbar(self, value):
        self.ui.progressbar_download.setValue(value)

    def test_video(self, url):
        if not self.custom_language:
            self.get_client_language()

        try:
            self.client = Client(language=self.api_language, delay=self.delay)
            self.video = self.client.get(url)
            return self.video

        except errors.ParsingError:
            ui_popup("Parsing error. Please try again in a few minutes")

    def start(self):
        url = self.ui.lineedit_video_url.text()
        self.videos_total += 1
        if url.endswith(".html"):
            self.download_raw(url, output_path=self.path)

        else:
            video = self.test_video(url)
            logging(msg=f"Downloading: {url}", level="0")
            self.download(video, progress_bar=self.ui.progressbar_download)

    def callback(self, pos, total):
        self.ui.progressbar_download.setMaximum(total)
        self.ui.progressbar_download.setValue(pos)

    def download(self, video, progress_bar, os_error_handle=False):
        quality = self.get_quality()
        logging(msg=f"Quality: {quality}")
        output_path = self.path
        logging(msg=f"Output path: {output_path}")

        title = video.title
        if os_error_handle:
            title = random.randint(0, 10000)

        title = strip_title(title)  # Fixes OS Error on Windows
        logging(f"Stripped title: {title}")
        output_path = f"{output_path}{title}.mp4"

        logging("Checking if video already exists...")
        text = f"Downloaded {self.videos_downloaded} / {self.videos_total} total videos"
        self.ui.lineedit_total.setText(str(text))

        if check_if_video_exists(video, output_path):
            self.videos_downloaded += 1
            self.ui.lineedit_total.setText(str(text))

        else:
            try:
                self.ui.lineedit_total.setText(str(text))
                logging(f"Mode: {self.mode}")
                if self.mode:
                    self.download_thread = DownloadThread(video, quality, output_path, self.semaphore)
                    self.download_thread.signals.progress.connect(
                        lambda pos, total, pb=progress_bar: update_progressbar(pos, total, pb))
                    self.download_thread.signals_completed.completed.connect(self.download_completed)
                    self.threadpool.start(self.download_thread)
                    logging(msg="Started download thread...")

                elif not self.mode:
                    logging(msg="Running in main thread...")
                    self.video.download(downloader=threaded(), display=self.callback, quality=quality, path=output_path)

            except OSError:
                logging(msg="OS Error: The file name is invalid for your system. Recreating a random int name...",
                        level=1)
                self.download(video, progress_bar, os_error_handle=True)

            except Exception as e:
                ui_popup(text=f"An unexpected error happened.  Exception: {e}")
                logging(msg=e, level=1)

    def custom_api_language(self):
        api_language = self.ui.lineedit_custom_api_language.text()

        self.conf.set("Porn_Fetch", "api_language", api_language)
        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)

        ui_popup("Applied, please restart Porn Fetch")

    def start_file(self):
        file_path = self.ui.lineedit_file.text()
        with open(file_path, "r") as file:
            content = file.read().splitlines()
            self.videos_total += len(content)

            for url in content:
                self.semaphore.acquire()
                if url.endswith(".html"):
                    logging(f"Downloading HQPorner.com: {url}")
                    self.download_raw(url, output_path=self.path)

                else:
                    logging(f"Downloading PornHub.com: {url}")
                    self.download(progress_bar=self.ui.progressbar_download, video=self.test_video(url))

    def get_metadata(self):
        url = self.ui.lineedit_metadata_url.text()

        if url.endswith(".html"):
            publish_date = API().get_publish_date(url)
            title = API().extract_title(url)
            length = API().get_video_length(url)
            categories = API().get_categories(url)
            actress = API().extract_actress(url)
            logging("Got metadata for HQPorner")
            self.ui.lineedit_actress.setText(str(actress))
            self.ui.lineedit_duration.setText(str(length))
            self.ui.lineedit_tags.setText(str(categories))
            self.ui.lineedit_title.setText(str(title))
            self.ui.lineedit_date.setText(str(publish_date))

        else:
            video = self.test_video(url)
            title = video.title
            author = video.author.name
            views = video.views
            date = video.date
            duration = video.duration.seconds
            duration = duration / 60
            duration = f"{round(duration)}m"
            likes_up = video.like.up
            likes_down = video.like.down
            likes = f"Likes: {likes_up} - Dislikes: {likes_down}"
            image_url = video.image.url
            tags = video.tags
            tag_names = []
            for tag in tags:
                tag_names.append(tag.name)

            tag_names = str(tag_names).strip("[").strip("]")
            logging("Got metadata for PornHub")
            self.ui.lineedit_likes.setText(str(likes))
            self.ui.lineedit_tags.setText(str(tag_names))
            self.ui.lineedit_image_url.setText(str(image_url))
            self.ui.lineedit_title.setText(str(title))
            self.ui.lineedit_author.setText(str(author))
            self.ui.lineedit_views.setText(str(views))
            self.ui.lineedit_date.setText(str(date))
            self.ui.lineedit_duration.setText(str(duration))

    def user_channel(self):
        if not self.custom_language:
            self.get_client_language()

        self.client = Client(language=self.api_language, delay=self.delay)
        user = self.ui.lineedit_model_url.text()
        user_object = self.client.get_user(user)
        logging("Got user object")
        logging(msg=f"User: {str(user_object.name)}")

        total_videos = user_object.videos
        user_objects = []

        try:
            for video in total_videos:
                video_object = self.test_video(video.url)
                user_objects.append(video_object)

        except IndexError:
            pass
        add_to_tree_widget(user_objects, tree_widget=self.ui.treeWidget)

    def download_thumbnail(self):
        url = self.ui.lineedit_metadata_url.text()
        video = self.test_video(url)
        image = video.image
        image.download(path="./")
        ui_popup(f"Downloaded Thumbnail for: {url}")

    def download_avatar(self):
        user_url = self.ui.lineedit_user_url.text()
        object = self.client.get_user(user_url)
        avatar = object.avatar
        name = object.name
        location = self.path + name + ".jpg"
        try:
            avatar.download(path=location)
            ui_popup(f"Downloaded Avatar for: {name} to: {location}")

        except Exception as e:
            ui_popup("Error downloading avatar: " + str(e))


    def get_user_information(self):
        user = self.ui.lineedit_user_url.text()
        user_object = self.client.get_user(user)
        logging("Loaded user object")
        info = user_object.info
        logging("Loaded user information object... Processing...")

        relationship = info.get("Relationship status")
        interested_in = info.get("Interested in")
        gender = info.get("Gender")
        height = info.get("Height")
        ethnicity = info.get("Ethnicity")
        hair_color = info.get("Hair Color")
        fake_breasts = info.get("Fake Boobs")
        tattoos = info.get("Tattoos")
        piercings = info.get("Piercings")
        hobbies = info.get("Interests and hobbie")
        turns_on = info.get("Turn Ons")
        video_views = info.get("Video Views")
        profile_views = info.get("Profile Views")
        videos_watched = info.get("Videos Watched")

        avatar_url = user_object.avatar.url

        self.ui.lineedit_user_name.setText(str(user_object.name))
        self.ui.lineedit_user_url.setText(str(user_object.url))
        self.ui.lineedit_user_fake_breasts.setText(str(fake_breasts))
        self.ui.lineedit_user_avatar.setText(str(avatar_url))
        self.ui.lineedit_user_gender.setText(str(gender))
        self.ui.lineedit_user_ethnicity.setText(str(ethnicity))
        self.ui.lineedit_user_hair_color.setText(str(hair_color))
        self.ui.lineedit_user_height.setText(str(height))
        self.ui.lineedit_user_hobbies.setText(str(hobbies))
        self.ui.lineedit_user_interested.setText(str(interested_in))
        self.ui.lineedit_user_piercings.setText(str(piercings))
        self.ui.lineedit_user_profile_views.setText(str(profile_views))
        self.ui.lineedit_user_video_views.setText(str(video_views))
        self.ui.lineedit_user_videos_watched.setText(str(videos_watched))
        self.ui.lineedit_user_relationship.setText(str(relationship))
        self.ui.lineedit_user_turn_ons.setText(str(turns_on))
        self.ui.lineedit_user_tattoos.setText(str(tattoos))
        logging("Loaded User information")

    def get_user_bio(self):
        name = self.ui.lineedit_user_url.text()
        user_object = self.client.get_user(name)

        bio = user_object.bio
        ui_popup(bio)

    def search_videos(self):
        include_filters = []
        exclude_filters = []

        filter_objects = {
            'include': [self.selected_category, self.production, self.sort, self.sort_time],
            'exclude': [self.excluded_categories_filter]
        }

        for action, filters in filter_objects.items():
            for filter_object in filters:
                if isinstance(filter_object, locals.Param):
                    if action == 'include':
                        include_filters.append(filter_object)
                    elif action == 'exclude':
                        exclude_filters.append(filter_object)
                else:
                    logging(f"Invalid filter: {filter_object}")

        if include_filters:
            combined_include_filter = include_filters[0]
            for filter_object in include_filters[1:]:
                combined_include_filter |= filter_object
        else:
            combined_include_filter = None

        if exclude_filters:
            combined_exclude_filter = exclude_filters[0]
            for filter_object in exclude_filters[1:]:
                combined_exclude_filter -= filter_object
        else:
            combined_exclude_filter = None

        query = self.ui.lineedit_search_query.text()

        if combined_include_filter and combined_exclude_filter:
            final_filter = combined_include_filter - combined_exclude_filter
            query_object = self.client.search(query, final_filter)
        elif combined_include_filter:
            query_object = self.client.search(query, combined_include_filter)
        elif combined_exclude_filter:
            query_object = self.client.search(query, -combined_exclude_filter)
        else:
            query_object = self.client.search(query)

        logging("Got query object")
        add_to_tree_widget(tree_widget=self.ui.treeWidget, iterator=query_object, search_limit=int(self.search_limit))

    def download_tree(self):
        video_objects = []
        for i in range(self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(i)
            checkState = item.checkState(0)
            if checkState == QtCore.Qt.Checked:
                video_url = item.data(0, QtCore.Qt.UserRole)
                video_objects.append(self.test_video(video_url))

        self.videos_total += len(video_objects)
        for video_object in video_objects:
            self.download(video_object, progress_bar=self.ui.progressbar_download)

    def settings_tab(self):
        quality_options = {
            "radio_quality_best": "best",
            "radio_quality_middle": "half",
            "radio_quality_worst": "worst",
        }
        threading_options = {
            "radio_threading_yes": "yes",
            "radio_threading_no": "no",
        }
        speed_options = {
            "radio_speed_high": "false",
            "radio_speed_usual": "true",
        }
        language_options = {
            "api_radio_de": "de",
            "api_radio_en": "en",
            "api_radio_fr": "fr",
            "api_radio_ru": "ru",
            "api_radio_es": "es",
        }
        time_sort_options = {
            "radio_day": "day",
            "radio_week": "week",
            "radio_month": "month",
            "radio_year": "year",
            "radio_time_sort_ignore": "false",
        }
        sort_options = {
            "radio_most_relevant": "relevant",
            "radio_most_viewed": "most viewed",
            "radio_longest": "longest",
            "radio_most_recent": "most recent",
            "radio_top_rated": "top rated",
            "radio_sort_ignore": "false",
        }
        production_options = {
            "radio_homemade": "homemade",
            "radio_professional": "professional",
            "radio_production_ignore": "false",
        }

        options_mapping = {
            "default_quality": quality_options,
            "default_threading": threading_options,
            "api_language": language_options,
            "delay": speed_options,
            "sort": sort_options,
            "sort_time": time_sort_options,
            "production": production_options,
        }

        for setting, options in options_mapping.items():
            for attribute, value in options.items():
                if getattr(self.ui, attribute).isChecked():
                    self.conf.set("Porn_Fetch", setting, value)
                    break

        tree_widget_limit = self.ui.horizontalSlider.value()
        self.conf.set("Porn_Fetch", "search_limit", str(tree_widget_limit))
        self.conf.set("Porn_Fetch", "semaphore_limit", str(self.ui.slider_simultaneous_downloads.value()))
        output_path = self.ui.lineedit_default_output_path.text()
        if not output_path.endswith(os.sep):
            output_path += os.sep

        if os.path.exists(output_path):
            self.conf.set("Porn_Fetch", "default_path", output_path)

        else:
            ui_popup("The output path doesn't exist! It won't be applied.")

        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)
        ui_popup("Applied, please restart!")
        logging("Applied settings")

    def load_user_settings(self):
        settings_mapping = {
            "sort": {
                "most viewed": self.ui.radio_most_viewed,
                "most relevant": self.ui.radio_most_relevant,
                "top rated": self.ui.radio_top_rated,
                "longest": self.ui.radio_longest,
                "most recent": self.ui.radio_most_recent,
                "false": self.ui.radio_sort_ignore,
            },
            "sort_time": {
                "day": self.ui.radio_day,
                "week": self.ui.radio_week,
                "month": self.ui.radio_month,
                "year": self.ui.radio_year,
                "false": self.ui.radio_time_sort_ignore,
            },
            "production": {
                "homemade": self.ui.radio_homemade,
                "professional": self.ui.radio_professional,
                "false": self.ui.radio_production_ignore,
            },
            "default_quality": {
                "best": self.ui.radio_quality_best,
                "half": self.ui.radio_quality_middle,
                "worst": self.ui.radio_quality_worst,
            },
            "api_language": {
                "en": self.ui.api_radio_en,
                "ru": self.ui.api_radio_ru,
                "fr": self.ui.api_radio_fr,
                "es": self.ui.api_radio_es,
                "de": self.ui.api_radio_de,
            },
        }

        for setting, options in settings_mapping.items():
            value = self.conf["Porn_Fetch"][setting]
            if value in options:
                options[value].setChecked(True)
                setattr(self, setting, value if value != "false" else None)
        language_codes = ["ru", "de", "fr", "es", "en"]
        if not self.conf["Porn_Fetch"]["api_language"] in language_codes:
            self.ui.radio_api_custom.setChecked(True)
            logging("Applied custom language")

        if self.conf["Porn_Fetch"]["delay"] == "true":
            self.ui.radio_speed_usual.setChecked(True)
            self.delay = True

        elif self.conf["Porn_Fetch"]["delay"] == "false":
            self.ui.radio_speed_high.setChecked(True)
            self.delay = False

        if self.conf["Porn_Fetch"]["default_threading"] == "yes":
            self.ui.radio_threading_yes.setChecked(True)
            self.mode = True

        elif self.conf["Porn_Fetch"]["default_threading"] == "no":
            self.ui.radio_threading_no.setChecked(False)
            self.mode = False

        else:
            self.ui.radio_threading_yes.setChecked(True)
            self.mode = True

        self.search_limit = self.conf["Porn_Fetch"]["search_limit"]
        self.semaphore = QSemaphore(int(self.conf["Porn_Fetch"]["semaphore_limit"]))
        self.ui.slider_simultaneous_downloads.setValue(int(self.conf["Porn_Fetch"]["semaphore_limit"]))
        self.ui.horizontalSlider.setValue(int(self.search_limit))
        self.path = self.conf["Porn_Fetch"]["default_path"]
        self.ui.lineedit_default_output_path.setText(self.path)
        logging("Loaded user settings")

    def load_search_filters(self):
        production_mapping = {
            "professional": locals.Production.PROFESSIONAL,
            "homemade": locals.Production.HOMEMADE
        }

        sort_mapping = {
            "most recent": locals.Sort.VIDEO_MOST_RECENT,
            "most viewed": locals.Sort.VIDEO_MOST_VIEWS,
            "top rated": locals.Sort.VIDEO_TOP_RATED,
            "longest": locals.Sort.VIDEO_LONGUEST
        }

        sort_time_mapping = {
            "day": locals.Sort.DAYLY,
            "week": locals.Sort.WEEKLY,
            "month": locals.Sort.MONTHLY,
            "year": locals.Sort.YEARLY
        }

        self.production = production_mapping.get(self.production, self.production)
        self.sort = sort_mapping.get(self.sort, self.sort)
        self.sort_time = sort_time_mapping.get(self.sort_time, self.sort_time)

        self.selected_category_value = self.conf.get('Porn_Fetch', 'categories', fallback=None)
        self.excluded_categories_str = self.conf.get('Porn_Fetch', 'excluded_categories', fallback=None)
        self.excluded_categories = self.excluded_categories_str.split(',') if self.excluded_categories_str else []
        self.excluded_categories_filter = []

        try:
            self.selected_category = getattr(locals.Category, self.selected_category_value)

        except AttributeError:
            self.selected_category = False

        try:
            for category in self.excluded_categories:
                self.excluded_categories.append(getattr(locals.Category, category))

        except AttributeError:
            self.excluded_categories_filter = False

        logging("Loaded search filters")

    def login(self):
        username = self.ui.lineedit_username.text()
        password = self.ui.lineedit_password.text()
        self.ui.lineedit_status.setText("Logging in...")

        try:
            if not self.custom_language:
                self.get_client_language()

            self.client = Client(username=username, password=password, language=self.api_language, delay=self.delay)
            logging("Login Successful")
            self.ui.lineedit_status.setText(f"Logged in as: {self.client.account.name}")
            self.ui.groupBox_3.setEnabled(True)

        except errors.LoginFailed:
            logging(msg="Login Failed. Check credentials!", level=1)
            ui_popup("Login Failed. Check credentials!")

    def get_liked_videos(self):
        try:
            videos = self.client.account.liked
            logging("Fetched videos")
            add_to_tree_widget(iterator=videos, tree_widget=self.ui.treeWidget)
            logging("Added videos to tree widget")

        except AttributeError:
            self.login()
            self.get_liked_videos()

    def get_watched_videos(self):
        try:
            videos = self.client.account.watched
            logging("Fetched videos")
            add_to_tree_widget(iterator=videos, tree_widget=self.ui.treeWidget)
            logging("Added videos to tree widget")

        except AttributeError:
            self.login()
            self.get_watched_videos()

    def get_recommended_videos(self):
        try:
            videos = self.client.account.recommended
            logging("Fetched videos")
            add_to_tree_widget(iterator=videos, tree_widget=self.ui.treeWidget)
            logging("Added videos to tree widget")

        except AttributeError:
            self.login()  # Sometimes the Account Session times out. In that case a simple re-initialization is best :)
            self.get_recommended_videos()


def main():
    app = QApplication(sys.argv)
    setup_config_file()

    try:
        """
        I had many problems with coding in general where something didn't work but the translations are the hardest
        thing I've ever done. Now where I've understand it it makes sense but the Qt documentation is a piece of shit...
        """

        # Obtain the system's locale
        locale = QLocale.system()
        # Get the language code (e.g., "de" for German)
        language_code = locale.name().split('_')[0]
        # Construct the path to the translation file
        path = f":/translations/translations/{language_code}.qm"

        translator = QTranslator(app)
        if translator.load(path):
            logging(f"{language_code} translation loaded")
            app.installTranslator(translator)
        else:
            logging(f"Failed to load {language_code} translation")

        widget = License()  # Starts License widget and checks if license was accepted.
        widget.check_license_and_proceed()

    except PermissionError:
        ui_popup("Insufficient Permissions to access something. Please run Porn Fetch as root / admin")

    except ConnectionResetError:
        ui_popup("Connection was reset. Are you connected to a public wifi or a university's wifi? ")
    except ConnectionError:
        ui_popup("Connection Error, please make sure you have a stable internet connection")

    except KeyboardInterrupt:
        sys.exit(0)

    except requests.exceptions.SSLError:
        ui_popup("SSL Error.  Please connect to a VPN!")

    except TypeError:
        pass

    except OSError as e:
        ui_popup(f"This error shouldn't happen. If you still see it it's REALLY important that you report the "
                 f"following: {e}")

    except ZeroDivisionError:
        pass

    sys.exit(app.exec())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cli",
                        help="CLI Terminal Version. Intended for advanced users or systems without a Graphical "
                             "Environment",
                        action="store_true")
    parser.add_argument("-v", "--version", help="Shows version information", action="store_true")
    parser.add_argument("-s", "--source", help="Shows the Source of this project", action="store_true")
    parser.add_argument("-l", "--license", help="Shows License information", action="store_true")
    args = parser.parse_args()

    if args.cli:
        CLI()

    elif args.version:
        print(__version__)

    elif args.source:
        print(__source__)

    elif args.license:
        print(__license__)

    else:
        main()
