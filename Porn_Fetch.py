__author__ = "EchterAlsFake : Johannes Habel"
__version__ = "2.8"
__source__ = "https://github.com/EchterAlsFake/Porn_Fetch"
__license__ = "GPL 3"

import sys
import argparse
import os
import re
import random

import phub.errors
import requests
import math
import src.resources_rc  # It's used in Runtime for the icons. Do not remove this requirement!

from phub import Client, Quality, locals, errors
from bs4 import BeautifulSoup
from configparser import ConfigParser
from PySide6 import QtCore
from PySide6.QtCore import QSemaphore
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTreeWidgetItem, QButtonGroup
from PySide6.QtCore import Signal, QThreadPool, QRunnable, QObject, Slot
from PySide6.QtGui import QIcon
from src.license_agreement import Ui_Widget_License
from src.Porn_Fetch_v3 import Ui_Porn_Fetch_widget
from src.setup import setup_config_file, strip_title, logging
from src.cli import CLI

headers = {
        "Referer": "https://hqporner.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    }  # Use this to prevent detection mechanisms...


def extract_title(url):
    html = requests.get(url, headers=headers).content
    beautifulsoup = BeautifulSoup(html, "lxml")
    return beautifulsoup.find("title").text


def extract_text_after_double_slash(url):
    """
    HQPorner uses an external CDN (Content Delivery Network) to load the videos dynamically. Luckily for us, the video
    locations are saved in the JS code, and we can just extract them
    """
    html = requests.get(url, headers=headers).content
    beautifulsoup = BeautifulSoup(html, "lxml")
    url_pattern = re.compile(r"url: '/blocks/altplayer\.php\?i=//(.*?)',")  # This is the URL for the redirection link
    match = url_pattern.search(str(beautifulsoup))

    if match:
        url_path = match.group(1)
        return url_path


def get_final_urls(url):
    """
    This will extract the .mp4 source urls from the CDN Network. Please note, that these are temporary URLs.
    They change from time to time.
    """
    base_url = extract_text_after_double_slash(url)
    final_content = requests.get("https://" + base_url).content
    soup = BeautifulSoup(final_content, "lxml")
    for script in soup.find_all('script'):
        if 'do_pl()' in script.text:
            script_content = script.text
            break

    video_urls = re.findall(r'//[^\'"]+\.mp4', script_content)  # Direct Download link from the CDN network
    urls = []
    for url in video_urls:
        urls.append(url) if not url in urls else ""

    return urls


def ui_popup(text):
    """ A simple UI popup that will be used for small messages to the user."""
    qmsg_box = QMessageBox()
    qmsg_box.setText(text)
    qmsg_box.exec()


def update_progressbar(pos, total, progress_bar):
    progress_bar.setMaximum(total)
    progress_bar.setValue(pos)


def add_to_tree_widget(iterator, tree_widget):
    tree_widget.clear()
    try:
        for i, video in enumerate(iterator, start=1):
            item = QTreeWidgetItem(tree_widget)
            item.setText(0, f"{i}) {video.title}")
            item.setData(0, QtCore.Qt.UserRole, video.url)
            item.setCheckState(0, QtCore.Qt.Unchecked)  # Adds a checkbox
    except Exception as e:
        ui_popup(
            f"An error happened. ERROR: {e}")


def create_button_group(buttons):
    """Creates a QButtonGroup and adds the given buttons to it."""
    button_group = QButtonGroup()
    for button in buttons:
        button_group.addButton(button)
    return button_group


class DownloadWorker(QRunnable):
    def __init__(self, video, quality, output_path):
        super(DownloadWorker, self).__init__()
        self.video = video
        self.quality = quality
        self.output_path = output_path
        self.signals = WorkerSignals()

    def run(self):
        urls = get_final_urls(self.video)
        url = f"http:{urls[self.quality]}"
        title = extract_title(self.video)
        final_path = os.path.join(self.output_path, title + ".mp4")
        response = requests.get(url, stream=True)
        file_size = int(response.headers.get('content-length', 0))

        if not os.path.exists(final_path):
            with open(final_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
                    # emit progress signal here
                    progress = math.ceil((file.tell() / file_size) * 100)
                    self.signals.progress.emit(progress)

        # emit completed signal here
        self.signals.completed.emit()
        # Thanks to ChatGPT for programming this function. I am just too stupid for math calculations ^^


class License(QWidget):
    """ License class to display the GPL 3 License to the user."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_widget = None
        self.conf = ConfigParser()
        self.conf.read("config.ini")

        self.ui = Ui_Widget_License()
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


class WorkerSignals(QObject):
    progress = Signal(int)
    completed = Signal()


class DownloadProgressSignal(QObject):
    """Sends the current download progress to the main UI to update the progressbar."""
    progress = Signal(int, int)


class DownloadThread(QRunnable):
    """
    Uses threading to download the videos without interfering with the main UI
    Will be used when the 'Yes' Box is checked in the main UI.
    """

    def __init__(self, video, quality, output_path):
        super().__init__()
        self.video = video
        self.quality = quality
        self.output_path = output_path
        self.signals = DownloadProgressSignal()

    def callback(self, pos, total):
        self.signals.progress.emit(pos, total)

    def run(self):
        self.video.download(display=self.callback, quality=self.quality, path=self.output_path)


class Widget(QWidget):
    """Main UI widget. Design is loaded from the ui_main_widget.py file. Feel free to change things if you want."""

    def __init__(self, parent=None):
        super().__init__(parent)
        setup_config_file()
        self.conf = ConfigParser()
        self.conf.read("config.ini")

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
        self.threadpool = QThreadPool()
        self.semaphore = QSemaphore(1)

        self.ui = Ui_Porn_Fetch_widget()
        self.ui.setupUi(self)
        self.ui.button_video.setIcon(QIcon(":/icons/download.svg"))
        self.ui.button_account.setIcon(QIcon(":/icons/account.svg"))
        self.ui.button_settings.setIcon(QIcon(":/icons/settings.svg"))
        logging("Loaded Icons")
        self.ui.groupBox_3.setDisabled(True)
        self.button_group()  # Needs to be called before load_user_settings!
        self.load_user_settings()  # Loads the user settings from config.ini to make settings persistent
        self.load_search_filters()  # Must be called before load_user_settings!
        logging(f"Delay Set to: {self.delay}")
        logging(f"API Language is: {self.api_language}")
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

    def button_group(self):
        """Separates the QRadioButtons from the different grid layouts"""

        button_groups = {
            "quality": [self.ui.radio_quality_best, self.ui.radio_quality_worst, self.ui.radio_quality_middle],
            "threading": [self.ui.radio_threading_yes, self.ui.radio_threading_no],
            "api_language": [self.ui.api_radio_es, self.ui.api_radio_fr, self.ui.api_radio_en, self.ui.api_radio_de,
                             self.ui.api_radio_ru],
            "sort": [self.ui.radio_most_recent, self.ui.radio_most_relevant, self.ui.radio_most_viewed,
                     self.ui.radio_longest, self.ui.radio_top_rated, self.ui.radio_sort_ignore],
            "sort_time": [self.ui.radio_day, self.ui.radio_month, self.ui.radio_year, self.ui.radio_week,
                          self.ui.radio_time_sort_ignore],
            "hd": [self.ui.radio_hd_yes, self.ui.radio_hd_no, self.ui.radio_hd_ignore],
            "production": [self.ui.radio_production_ignore, self.ui.radio_homemade, self.ui.radio_professional],
            "ui_language": []
        }
        self.buttonGroups = tuple(create_button_group(buttons) for buttons in button_groups.values())

    def get_mode(self):

        if self.ui.radio_threading_no.isChecked():
            self.mode = False

        elif self.ui.radio_threading_yes.isChecked():
            self.mode = True

        else:
            self.mode = True

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

    def download_raw(self, video, output_path):
        self.semaphore.acquire()
        # Determine quality based on user selection
        quality = 0  # Default to low quality
        if self.ui.radio_quality_middle.isChecked():
            quality = 1
        elif self.ui.radio_quality_best.isChecked():
            quality = -1


        # Create worker and connect signals
        worker = DownloadWorker(video, quality, output_path)
        worker.signals.progress.connect(self.update_progressbar)
        worker.signals.completed.connect(self.download_completed_slot)

        # Start the worker in a new thread
        self.threadpool.start(worker)

    @Slot(int)
    def update_progressbar(self, value):
        self.ui.progressbar_download.setValue(value)

    @Slot()
    def download_completed(self):
        # Handle completion, e.g., show a message to the user
        logging("Download Completed!")

    def download_completed_slot(self):
        self.download_completed()  # Call your original download_completed logic if any
        self.semaphore.release()  # Release the semaphore once download is complete

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
        self.get_mode()
        output_path = self.path
        logging(msg=f"Output path: {output_path}")

        title = video.title
        if os_error_handle:
            title = random.randint(0, 10000)

        title = strip_title(title)  # Fixes OS Error on Windows
        output_path = f"{output_path}{title}.mp4"

        try:
            if self.mode:
                self.download_thread = DownloadThread(video, quality, output_path)
                self.download_thread.signals.progress.connect(
                    lambda pos, total, pb=progress_bar: update_progressbar(pos, total, pb))
                self.threadpool.start(self.download_thread)
                logging(msg="Started download thread...")

            elif not self.mode:
                logging(msg="Running in main thread...")
                self.video.download(display=self.callback, quality=quality, path=output_path)

        except OSError:
            logging(msg="OS Error: The file name is invalid for your system. Recreating a random int name...", level=1)
            self.download(video, progress_bar, os_error_handle=True)

        except Exception as e:
            ui_popup(text=f"An unexpected error happened.  Exception: {e}")
            logging(msg=e, level=1)

    def start_file(self):
        file_path = self.ui.lineedit_file.text()
        with open(file_path, "r") as file:
            content = file.read().splitlines()
            counter = 0
            length = len(content)
            text = f"Downloaded {counter} / {length} total videos"
            self.ui.lineedit_toal.setText(str(text))

            for url in content:
                self.semaphore = QSemaphore(1)
                if url.endswith(".html"):
                    self.download_raw(url, output_path=self.path)
                    counter += 1
                    self.ui.lineedit_toal.setText(str(text))

                else:
                    self.get_mode()
                    self.download(progress_bar=self.ui.progressbar_download, video=self.test_video(url))

    def download_completed_slot(self):
        self.download_completed()  # Call your original download_completed logic if any
        self.semaphore.release()  # Release the semaphore once download is complete

    def get_metadata(self):
        url = self.ui.lineedit_metadata_url.text()
        video = self.test_video(url)

        if video != False:
            title = video.title
            author = video.author.name
            views = video.views
            date = video.date
            duration = video.duration.seconds
            duration = duration / 60
            duration = f"{duration}m"
            hotspots = video.hotspots
            likes_up = video.like.up
            likes_down = video.like.down
            likes = f"Likes: {likes_up} - Dislikes: {likes_down}"
            image_url = video.image.url
            tags = video.tags

            self.ui.lineedit_likes.setText(str(likes))
            self.ui.lineedit_tags.setText(str(tags))
            self.ui.lineedit_image_url.setText(str(image_url))
            self.ui.lineedit_title.setText(str(title))
            self.ui.lineedit_author.setText(str(author))
            self.ui.lineedit_views.setText(str(views))
            self.ui.lineedit_date.setText(str(date))
            self.ui.lineedit_duration.setText(str(duration))
            self.ui.lineedit_hotspots.setText(str(hotspots))

    def user_channel(self):
        if not self.custom_language:
            self.get_client_language()

        self.client = Client(language=self.api_language, delay=self.delay)
        user = self.ui.lineedit_model_url.text()
        user_object = self.client.get_user(user)
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

    def search_videos(self):
        query = self.ui.lineedit_search_query.text()
        if not self.custom_language:
            self.get_client_language()

        self.client = Client(language=self.api_language, delay=self.delay)
        query_object = self.client.search(query)

        self.add_to_download_tree(query_object)
        self.download_tree()

    def add_to_download_tree(self, data):
        self.ui.treeWidget.clear()
        for i, video in enumerate(data, start=1):
            item = QTreeWidgetItem(self.ui.treeWidget)
            item.setText(0, f"{i}) {video.title}")
            item.setData(0, QtCore.Qt.UserRole, video.url)
            item.setCheckState(0, QtCore.Qt.Unchecked)  # Adds a checkbox

    def download_tree(self):
        for i in range(self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(i)
            checkState = item.checkState(0)
            if checkState == QtCore.Qt.Checked:
                video_url = item.data(0, QtCore.Qt.UserRole)
                video = self.test_video(video_url)
                self.download(video, progress_bar=self.ui.progressbar_download)

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
        hd_options = {
            "radio_hd_yes": "yes",
            "radio_hd_no": "no",
            "radio_hd_ignore": "false",
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
            "hd": hd_options,
            "sort": sort_options,
            "sort_time": time_sort_options,
            "production": production_options,
        }

        for setting, options in options_mapping.items():
            for attribute, value in options.items():
                if getattr(self.ui, attribute).isChecked():
                    self.conf.set("Porn_Fetch", setting, value)
                    break

        output_path = self.ui.lineedit_default_output_path.text()
        if os.path.exists(output_path):
            self.conf.set("Porn_Fetch", "default_path", output_path)

        else:
            ui_popup("The output path doesn't exist! It won't be applied.")

        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)
        ui_popup("Applied, please restart!")

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
            "hd": {
                "true": self.ui.radio_hd_yes,
                "false": self.ui.radio_hd_no,
            },
            "default_quality": {
                "best": self.ui.radio_quality_best,
                "half": self.ui.radio_quality_middle,
                "worst": self.ui.radio_quality_worst,
            },
            "default_threading": {
                "yes": self.ui.radio_threading_yes,
                "no": self.ui.radio_threading_no,
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

        if self.conf["Porn_Fetch"]["delay"] == "true":
            self.ui.radio_speed_usual.setChecked(True)
            self.delay = True

        elif self.conf["Porn_Fetch"]["delay"] == "false":
            self.ui.radio_speed_high.setChecked(True)
            self.delay = False

        self.path = self.conf["Porn_Fetch"]["default_path"]
        self.ui.lineedit_default_output_path.setText(self.path)

    def load_search_filters(self):
        if self.production == "professional":
            self.production = locals.Production.PROFESSIONAL

        elif self.production == "homemade":
            self.production = locals.Production.HOMEMADE

    def login(self):
        username = self.ui.lineedit_username.text()
        password = self.ui.lineedit_password.text()
        self.ui.lineedit_status.setText("Logging in...")

        try:
            if not self.custom_language:
                self.get_client_language()

            self.client = Client(username=username, password=password, language=self.api_language, delay=self.delay)
            self.ui.lineedit_status.setText(f"Logged in as: {self.client.account.name}")
            self.ui.groupBox_3.setEnabled(True)

        except errors.LoginFailed:
            logging(msg="Login Failed. Check credentials!", level=1)
            ui_popup("Login Failed. Check credentials!")

    def get_liked_videos(self):
        try:
            videos = self.client.account.liked

        except AttributeError:
            self.login()
            self.get_liked_videos()

        if len(videos) == 0:
            ui_popup("No videos found. If you are sure that this is an error, it's PornHub's fault ;) ")

        else:
            add_to_tree_widget(iterator=videos, tree_widget=self.ui.treeWidget)

    def get_watched_videos(self):
        try:
            videos = self.client.account.watched

        except AttributeError:
            self.login()
            self.get_watched_videos()

        if len(videos) == 0:
            ui_popup("No videos found. If you are sure that this is an error, it's PornHub's fault ;) ")

        else:
            add_to_tree_widget(iterator=videos, tree_widget=self.ui.treeWidget)

    def get_recommended_videos(self):
        try:
            videos = self.client.account.recommended

        except AttributeError:
            self.login()  # Sometimes the Account Session times out. In that case a simple re-initialization is best :)
            self.get_recommended_videos()

        if len(videos) == 0:
            ui_popup("No videos found. If you are sure that this is an error, it's PornHub's fault ;) ")

        else:
            add_to_tree_widget(iterator=videos, tree_widget=self.ui.treeWidget)


def main():
    app = QApplication(sys.argv)
    setup_config_file()

    widget = License()
    widget.check_license_and_proceed()
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
