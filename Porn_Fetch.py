__author__ = "EchterAlsFake : Johannes Habel"
__version__ = "2.7"
__source__ = "https://github.com/EchterAlsFake/Porn_Fetch"
__license__ = "GPL 3"

import sys
import argparse
import phub.consts
import sentry_sdk
import os
import requests
import random
import wget

from configparser import ConfigParser
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTreeWidgetItem, QInputDialog, QLineEdit, \
    QButtonGroup
from PySide6.QtGui import QKeyEvent, QColor
from PySide6.QtCore import Signal, QThreadPool, QRunnable, QObject, Qt, QDir
from src.license_agreement import Ui_Widget_License
from phub import Client, Quality
from src.ui_main_widget import Ui_Porn_Fetch_Widget
from src.setup import enable_error_handling, setup_config_file, strip_title, logging, get_graphics
from src.cli import CLI


def ui_popup(text):
    """ A simple UI popup that will be used for small messages to the user."""
    qmsg_box = QMessageBox()
    qmsg_box.setText(text)
    qmsg_box.exec()


class License(QWidget):
    """ License class to display the GPL 3 License to the user."""

    def __init__(self, parent=None):
        super().__init__(parent)
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
            logging(msg="License was not accepted.", level="0")
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
        logging(msg="Starting Porn Fetch main widget", level="0")
        self.main_widget = Widget()
        self.main_widget.show()


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


def update_progressbar(pos, total, progress_bar):
    progress_bar.setMaximum(total)
    progress_bar.setValue(pos)

def help_ui_file():
    text = """
The URLs in the file needs to be separated with new lines.

e.g.

URL1
URL2
URL3

No comma or anything else. Just new lines.
"""
    ui_popup(text)

def help():
    text = """

API Language:

The API handles your requests to PornHub.com   If the API is in english language, then all the titles and video
attributes are also in english. If the API is for example in German language, then the video titles are (if automatically
translated by PornHub) also in German language.   Not all videos are supported! 

UI Language:

UI language defines the language in the application.

Quality:

Highest = Best Quality possible, Half = somewhere in the middle, Lowest = Least quality possible

Debug:

Sentry: Captures error logs, which helps me to fix issues faster, and you don't have to report them

UI Transparency: 

Defines the UI background transparency. Please note, that this feature doesn't work well on Hyprland!

Threading: 

Threading uses multiple cores of your CPU to download multiple videos simultaneously. This leads to a broken
progressbar, but can have a big speed impact if you have a really fast internet connection.

Delay:

The delay handles how fast the API requests are. By default you should definitely ENABLE this.
Without the delay, the API will spam the requests as fast as possible. Of course this has a big speed impact and 
videos will download 10x faster, but it can also lead to a lot more errors. If you just want to download
one video real quick, you can disable it, but if you plan to download more than that, please enable it!

(DO NOT REPORT ERRORS, IF YOU HAD DELAY DISABLED!) 

If you still have questions, let me know on GitHub in discussions.

Account:

You can log in to PornHub with your Account and fetch all videos you've liked, watched and that are recommended to you.
This can be useful for downloading more efficiently. Your Account data won't be exposed!
"""
    ui_popup(text)


class Widget(QWidget):
    """Main UI widget. Design is loaded from the ui_main_widget.py file. Feel free to change things if you want."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.sentry = None
        self.setup()

        if not os.path.exists("graphics"):
            get_graphics()

        self.video = None
        self.api_language = "en"
        self.custom_language = False
        self.logging = None
        self.delay = True
        self.client = None
        self.sort = None
        self.sort_time = None
        self.production = None
        self.hd = None
        self.category = False
        self.download_thread = None
        self.threadpool = QThreadPool()

        self.ui = Ui_Porn_Fetch_Widget()
        self.ui.setupUi(self)
        self.ui.groupBox_7.setDisabled(True)
        self.button_group()  # Needs to be called before load_user_settings!
        self.load_user_settings()  # Loads the user settings from config.ini to make settings persistent
        logging(f"Delay Set to: {self.delay}", level="0")
        logging(f"API Language is: {self.api_language}", level="0")
        self.ui.stacked_main_account.setCurrentIndex(1)
        alpha_value = int((int(self.transparency) / 100) * 255)
        color = QColor(0, 0, 0, alpha_value)
        self.setStyleSheet(
            f"background-color: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()});color: rgb(255,255,255);")

        self.ui.stackedWidget.setCurrentIndex(0)
        self.button_connectors()


    def button_connectors(self):
        self.ui.button_start.clicked.connect(self.start)
        self.ui.button_start_file.clicked.connect(self.start_file)
        self.ui.button_get_metadata.clicked.connect(self.get_metadata)
        self.ui.button_start_user_channel.clicked.connect(self.user_channel)
        self.ui.button_start_search.clicked.connect(self.search_videos)
        self.ui.button_download_search_query.clicked.connect(self.download_tree)
        self.ui.button_settings_apply.clicked.connect(self.settings_tab)
        self.ui.button_settings_help.clicked.connect(help)
        self.ui.button_switch_to_account.clicked.connect(self.switch_to_account)
        self.ui.button_switch_main_page.clicked.connect(self.switch_to_main)
        self.ui.button_switch_to_main_widget.clicked.connect(self.switch_to_main)
        self.ui.button_account_login.clicked.connect(self.login)
        self.ui.button_account_list_liked_videos.clicked.connect(self.get_liked_videos)
        self.ui.button_account_list_rec_videos.clicked.connect(self.get_recommended_videos)
        self.ui.button_account_list_watched_videos.clicked.connect(self.get_watched_videos)
        self.ui.button_account_download.clicked.connect(self.download_tree_widget)
        self.ui.button_switch_to_settings.clicked.connect(self.switch_to_settings)
        self.ui.button_download_thumbnail.clicked.connect(self.download_thumbnail)
        self.ui.button_file_help.clicked.connect(help_ui_file)

    def button_group(self):
        """Separates the QRadioButtons from the different grid layouts"""

        button_group_quality = QButtonGroup()
        button_group_quality.addButton(self.ui.radio_highest)
        button_group_quality.addButton(self.ui.radio_lowest)
        button_group_quality.addButton(self.ui.radio_half)

        button_group_threading = QButtonGroup()
        button_group_threading.addButton(self.ui.radio_threading_yes)
        button_group_threading.addButton(self.ui.radio_threading_no)

        button_group_api_language = QButtonGroup()
        button_group_api_language.addButton(self.ui.api_radio_es)
        button_group_api_language.addButton(self.ui.api_radio_fr)
        button_group_api_language.addButton(self.ui.api_radio_en)
        button_group_api_language.addButton(self.ui.api_radio_de)
        button_group_api_language.addButton(self.ui.api_radio_ru)

        button_group_sort = QButtonGroup()
        button_group_sort.addButton(self.ui.radio_most_recent)
        button_group_sort.addButton(self.ui.radio_most_relevant)
        button_group_sort.addButton(self.ui.radio_most_viewed)
        button_group_sort.addButton(self.ui.radio_longest)
        button_group_sort.addButton(self.ui.radio_nothing)

        button_group_sort_time = QButtonGroup()
        button_group_sort_time.addButton(self.ui.radio_day)
        button_group_sort_time.addButton(self.ui.radio_month)
        button_group_sort_time.addButton(self.ui.radio_year)
        button_group_sort_time.addButton(self.ui.radio_week)
        button_group_sort_time.addButton(self.ui.radio_nothing_2)

        button_group_hd = QButtonGroup()
        button_group_hd.addButton(self.ui.radio_hd_yes)
        button_group_hd.addButton(self.ui.radio_hd_no)

        button_group_ui_language = QButtonGroup()
        button_group_ui_language.addButton(self.ui.application_language_en)

        self.buttonGroups = button_group_ui_language, button_group_threading, button_group_quality, button_group_api_language, button_group_hd, button_group_sort_time, button_group_sort

    def setup(self):
        self.conf = ConfigParser()
        self.conf.read("config.ini")

        if self.conf["Debug"]["sentry"] == "true":
            enable_error_handling()
            self.sentry = True

        elif self.conf["Debug"]["sentry"] == "false":
            self.sentry_data_collection()

        logging(msg="Setup complete", level="0")

    def get_mode(self):

        if self.ui.radio_threading_no.isChecked():
            self.mode = False

        elif self.ui.radio_threading_yes.isChecked():
            self.mode = True

    def sentry_data_collection(self):

        dlg = QMessageBox(self)
        dlg.setWindowTitle("I have a question!")
        dlg.setText("""
Do you enable automatic error collection by sentry.io?

This collects the following:

- The Python error
- The lines of code in which the error happened
- may also include your PC name

All other information is stripped out from the reports.

See setup.py : before_send()


Thanks :) 
""")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()

        if button == QMessageBox.Yes:
            enable_error_handling()
            self.conf.set("Debug", "sentry", "true")
            with open("config.ini", "w") as config_file:
                self.conf.write(config_file)
                config_file.close()

            self.sentry = True

        else:
            self.sentry = False

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
        if self.ui.radio_highest.isChecked():
            return Quality.BEST

        elif self.ui.radio_half.isChecked():
            return Quality.HALF

        elif self.ui.radio_lowest.isChecked():
            return Quality.WORST

        else:
            return Quality.BEST

    def stack_widget_search(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def stack_widget_metadata(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def stack_widget_credits(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def test_video(self, url):

        if not self.custom_language:
            self.get_client_language()

        try:
            self.client = Client(language=self.api_language, delay=self.delay)
            self.video = self.client.get(url)
            return self.video


        except phub.errors.ParsingError:
            ui_popup("Parsing error. Please try again in a few minutes")

    def start(self):

        url = self.ui.lineedit_url.text()
        video = self.test_video(url)
        logging(msg=f"Downloading: {url}", level="0")
        self.download(video, progress_bar=self.ui.progressbar_download)

    def callback(self, pos, total):
        self.ui.progressbar_download.setMaximum(total)
        self.ui.progressbar_download.setValue(pos)

    def download(self, video, progress_bar, os_error_handle=False):

        quality = self.get_quality()
        logging(msg=f"Quality: {quality}", level="0")
        self.get_mode()
        output_path = self.ui.lineedit_output.text()
        logging(msg=f"Output path: {output_path}", level="0")

        title = video.title
        if os_error_handle:
            title = random.randint(0, 10000)

        title = strip_title(title)  # Fixes OS Error on Windows
        output_path = output_path + title + ".mp4"

        try:
            if self.mode:
                self.download_thread = DownloadThread(video, quality, output_path)
                self.download_thread.signals.progress.connect(
                    lambda pos, total, pb=progress_bar: update_progressbar(pos, total, pb))
                self.threadpool.start(self.download_thread)
                logging(msg="Started download thread...", level="0")

            elif not self.mode:
                logging(msg="Running in main thread...", level="0")
                self.video.download(callback=self.callback, quality=quality, path=output_path)

        except OSError:
            logging(msg="OS Error: The file name is invalid for your system. Recreating a random int name...",
                    level="0")
            self.download(video, progress_bar, os_error_handle=True)

        except Exception as e:
            ui_popup(text=f"An unexpected error happened.  Exception: {e}")
            logging(msg=e, level="1")
            if self.sentry:
                sentry_sdk.capture_exception(e)

    def start_file(self):

        file_path = self.ui.lineedit_url_file.text()

        if not os.path.isfile(file_path):
            ui_popup(f"File does not exist. Please check again!  PATH: {file_path}")

        else:
            self.get_mode()
            with open(file_path, "r") as file:
                content = file.read().splitlines()

            valid_urls = []
            for url in content:
                if self.test_video(url) is None:
                    ui_popup(
                        f"The following URL is invalid: {url} Please remove it from the file or correct it and try again.")

                else:
                    valid_urls.append(url)

            video_objects = []

            for url in valid_urls:
                video_object = self.test_video(url)
                video_objects.append(video_object)

            self.add_to_download_tree(video_objects)
            self.download_tree()

    def get_metadata(self):

        url = self.ui.lineedit_url.text()
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

        video.refresh()

    def user_channel(self):
        if not self.custom_language:
            self.get_client_language()

        self.client = Client(language=self.api_language, delay=self.delay)
        user = self.ui.lineedit_user_channel.text()
        logging(msg=f"USER: {user}", level="0")
        videos = self.client.get_user(user)

        total_videos = videos.videos
        user_objects = []

        try:

            for video in total_videos:
                video_object = self.test_video(video.url)
                user_objects.append(video_object)
        except IndexError:
            pass

        self.add_to_tree_widget(user_objects, tree_widget=self.ui.treeWidget)

    def download_thumbnail(self):
        url = self.ui.lineedit_image_url.text()
        title = self.ui.lineedit_title.text()
        name = f"{title}.jpg"

        try:
            wget.download(url, out=name)
            logging(msg=f"Downloaded Thumbnail for: {name} Location: {name}", level="0")
            ui_popup("Download complete")

        except Exception as e:
            logging(msg=f"Error download thumbnail: {e}", level="1")
            ui_popup(e)
            if self.sentry:
                sentry_sdk.capture_exception(e)

    def search_videos(self):
        # Searches videos with query string and lets the user select them
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
        with open("config.ini", "w") as config_file:

            # Define the mappings between UI states and configurations
            mappings = {
                "hd": [("radio_hd_yes", "true"), ("radio_hd_no", "false")],
                "sort_time": [("radio_day", "day"), ("radio_week", "week"), ("radio_year", "year"),
                              ("radio_month", "month"), ("radio_nothing_2", "none")],
                "sort": [("radio_most_recent", "most_recent"), ("radio_most_viewed", "most_viewed"),
                         ("radio_most_relevant", "most_relevant"), ("radio_top_rated", "top_rated"),
                         ("radio_nothing", "none"), ("radio_longest", "longest")],
                "production": [("checkbox_homemade", "homemade"), ("checkbox_professional", "professional")],
                "default_quality": [("radio_highest", "best"), ("radio_half", "half"), ("radio_lowest", "worst")],
                "default_threading": [("radio_threading_no", "no"), ("radio_threading_yes", "yes")],
                "sentry": [("settings_checkbox_sentry", "true")],
                "api_language": [("api_radio_de", "de"), ("api_radio_fr", "fr"), ("api_radio_es", "es"),
                                 ("api_radio_ru", "ru"), ("api_radio_en", "en")],
                "UI_language": [("application_language_en", "en")]
            }
            if not self.ui.settings_checkbox_delay.isChecked():
                self.conf.set("Porn_Fetch", "delay", "false")
                logging("Delay disabled!", level="0")

            elif self.ui.settings_checkbox_delay.isChecked():
                logging("Delay Enabled!", level="0")
                self.conf.set("Porn_Fetch", "delay", "true")

            for config_key, options in mappings.items():
                for ui_elem, value in options:
                    if getattr(self.ui, ui_elem).isChecked():
                        self.conf.set("Porn_Fetch", config_key, value)
                        break
                else:
                    self.conf.set("Porn_Fetch", config_key, "none")

            transparency = self.ui.horizontalSlider.value()
            self.conf.set("UI", "transparency", str(transparency))  # Needs to be a string!
            self.conf.write(config_file)
            ui_popup("Applied! (Please restart for changes to take effect)")

    def load_user_settings(self):
        self.conf.read('config.ini')

        if self.conf["Debug"]["sentry"] == "true":
            self.sentry = True

        elif self.conf["Debug"]["sentry"] == "false":
            self.sentry = False

        if self.conf["Porn_Fetch"]["delay"] == "true":
            self.ui.settings_checkbox_delay.setChecked(True)
            self.delay = True

        elif self.conf["Porn_Fetch"]["delay"] == "false":
            self.ui.settings_checkbox_delay.setChecked(False)
            self.delay = False

        if self.conf["Porn_Fetch"]["sort"] == "most viewed":
            self.ui.radio_most_viewed.setChecked(True)
            self.sort = "most viewed"

        elif self.conf["Porn_Fetch"]["sort"] == "most relevant":
            self.ui.radio_most_relevant.setChecked(True)
            self.sort = "most relevant"

        elif self.conf["Porn_Fetch"]["sort"] == "top rated":
            self.ui.radio_top_rated.setChecked(True)
            self.sort = "top rated"

        elif self.conf["Porn_Fetch"]["sort"] == "longest":
            self.ui.radio_longest.setChecked(True)
            self.sort = "longest"

        elif self.conf["Porn_Fetch"]["sort"] == "most recent":
            self.ui.radio_most_recent.setChecked(True)
            self.sort = "most recent"

        elif self.conf["Porn_Fetch"]["sort"] == "false":
            self.sort = None

        if self.conf["Porn_Fetch"]["sort_time"] == "day":
            self.ui.radio_day.setChecked(True)
            self.sort_time = "day"

        elif self.conf["Porn_Fetch"]["sort_time"] == "week":
            self.ui.radio_week.setChecked(True)
            self.sort_time = "week"

        elif self.conf["Porn_Fetch"]["sort_time"] == "month":
            self.ui.radio_month.setChecked(True)
            self.sort_time = "month"

        elif self.conf["Porn_Fetch"]["sort_time"] == "year":
            self.ui.radio_year.setChecked(True)
            self.sort_time = "year"

        elif self.conf["Porn_Fetch"]["sort_time"] == "none":
            self.sort_time = None

        if self.conf["Porn_Fetch"]["production"] == "homemade":
            self.ui.checkbox_homemade.setChecked(True)
            self.production = "homemade"

        elif self.conf["Porn_Fetch"]["production"] == "professional":
            self.ui.checkbox_professional.setChecked(True)
            self.production = "professional"

        if self.conf["Porn_Fetch"]["hd"] == "true":
            self.ui.radio_hd_yes.setChecked(True)
            self.hd = True

        elif self.conf["Porn_Fetch"]["hd"] == "false":
            self.ui.radio_hd_no.setChecked(True)
            self.hd = False

        if self.conf["Porn_Fetch"]["default_quality"] == "best":
            self.ui.radio_highest.setChecked(True)

        elif self.conf["Porn_Fetch"]["default_quality"] == "half":
            self.ui.radio_half.setChecked(True)

        elif self.conf["Porn_Fetch"]["default_quality"] == "worst":
            self.ui.radio_lowest.setChecked(True)

        if self.conf["Porn_Fetch"]["default_threading"] == "multiple":
            self.ui.radio_threading_yes.setChecked(True)

        elif self.conf["Porn_Fetch"]["default_threading"] == "single":
            self.ui.radio_threading_no.setChecked(True)

        if self.conf["Debug"]["sentry"] == "true":
            self.ui.settings_checkbox_sentry.setChecked(True)

        else:
            self.ui.settings_checkbox_sentry.setChecked(False)

        if self.conf["Porn_Fetch"]["api_language"] == "en":
            self.ui.api_radio_en.setChecked(True)
            self.api_language = "en"

        elif self.conf["Porn_Fetch"]["api_language"] == "ru":
            self.ui.api_radio_ru.setChecked(True)
            self.api_language = "ru"

        elif self.conf["Porn_Fetch"]["api_language"] == "fr":
            self.ui.api_radio_fr.setChecked(True)
            self.api_language = "fr"

        elif self.conf["Porn_Fetch"]["api_language"] == "es":
            self.ui.api_radio_es.setChecked(True)
            self.api_language = "es"

        elif self.conf["Porn_Fetch"]["api_language"] == "de":
            self.ui.api_radio_de.setChecked(True)
            self.api_language = "de"

        if self.conf["UI"]["language"] == "en":
            self.ui.application_language_en.setChecked(True)
            self.application_language = "en"

        self.transparency = self.conf["UI"]["transparency"]
        self.ui.horizontalSlider.setValue(int(self.transparency))
    def switch_to_account(self):
        self.ui.stacked_main_account.setCurrentIndex(0)

    def switch_to_main(self):
        self.ui.stacked_main_account.setCurrentIndex(1)

    def switch_to_settings(self):
        self.ui.stacked_main_account.setCurrentIndex(2)

    def login(self):

        username = self.ui.lineedit_account_username.text()
        password = self.ui.lineedit_account_password.text()
        self.ui.lineedit_account_status.setText("Logging in...")

        try:
            if not self.custom_language:
                self.get_client_language()

            self.client = Client(username=username, password=password, language=self.api_language, delay=self.delay)
            self.ui.lineedit_account_status.setText(f"Logged in as: {self.client.account.name}")
            self.ui.groupBox_7.setEnabled(True)

        except phub.errors.LoginFailed:
            logging(msg="Login Failed. Check credentials!", level="1")
            ui_popup("Login Failed. Check credentials!")

    def add_to_tree_widget(self, iterator, tree_widget):
        tree_widget.clear()
        try:
            for i, video in enumerate(iterator, start=1):  # Limiting search results to 50
                item = QTreeWidgetItem(tree_widget)
                item.setText(0, f"{i}) {video.title}")
                item.setData(0, QtCore.Qt.UserRole, video.url)
                item.setCheckState(0, QtCore.Qt.Unchecked)  # Adds a checkbox
        except Exception as e:
            ui_popup(
                f"An error happened. This error will NOT be sent to sentry, to prevent leaking your account data! ERROR: {e}")

    def get_liked_videos(self):

        videos = self.client.account.liked
        if len(videos) == 0:
            ui_popup("No videos found. If you are sure that this is an error, it's PornHub's fault ;) ")

        else:
            self.add_to_tree_widget(iterator=videos, tree_widget=self.ui.tree_widget_account)

    def get_watched_videos(self):
        videos = self.client.account.watched
        if len(videos) == 0:
            ui_popup("No videos found. If you are sure that this is an error, it's PornHub's fault ;) ")

        else:
            self.add_to_tree_widget(iterator=videos, tree_widget=self.ui.tree_widget_account)

    def get_recommended_videos(self):
        videos = self.client.account.recommended
        if len(videos) == 0:
            ui_popup("No videos found. If you are sure that this is an error, it's PornHub's fault ;) ")

        else:
            self.add_to_tree_widget(iterator=videos, tree_widget=self.ui.tree_widget_account)

    def download_tree_widget(self):
        # Downloads all selected videos with a for loop
        try:
            for i in range(self.ui.tree_widget_account.topLevelItemCount()):
                item = self.ui.tree_widget_account.topLevelItem(i)
                checkState = item.checkState(0)
                if checkState == QtCore.Qt.Checked:
                    video_url = item.data(0, QtCore.Qt.UserRole)
                    url = f"https://www.pornhub.com/{video_url}"
                    video = self.test_video(url)
                    self.download(video, progress_bar=self.ui.account_progressbar)

        except Exception as e:
            ui_popup(
                f"An error happened. This error will NOT be sent to sentry, to prevent leaking your account data! ERROR: {e}")

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key.Key_W and event.modifiers() == Qt.ControlModifier:
            logging(msg="Closing Porn Fetch.  Bye :) ", level="0")
            self.close()

        if event.key() == Qt.Key.Key_M and event.modifiers() == Qt.ControlModifier:
            self.stack_widget_metadata()
            logging(msg="Loaded Metadata page from QStackedWidget", level="0")

        if event.key() == Qt.Key.Key_S and event.modifiers() == Qt.ControlModifier:
            self.stack_widget_search()
            logging(msg="Loaded Search page from QStackedWidget", level="0")

        if event.key() == Qt.Key.Key_C and event.modifiers() == Qt.ControlModifier:
            self.stack_widget_credits()
            logging(msg="Loaded Credits page from QStackedWidget", level="0")

        if event.key() == Qt.Key.Key_R and event.modifiers() == Qt.ControlModifier:
            setup_config_file(force=True)
            logging(msg="Configuration was reset successfully", level="0")

        if event.key() == Qt.Key.Key_L and event.modifiers() == Qt.ControlModifier:
            text, ok = QInputDialog.getText(self, "QInputDialog.getText()",
                                            "Language Code (e.g: de, en, es):", QLineEdit.Normal,
                                            QDir.home().dirName())
            if ok and text:
                self.api_language = text
                self.custom_language = True

        if event.key() == Qt.Key.Key_1 and event.modifiers() == Qt.ControlModifier:
            self.switch_to_account()

        if event.key() == Qt.Key.Key_2 and event.modifiers() == Qt.ControlModifier:
            self.switch_to_main()

        if event.key() == Qt.Key.Key_3 and event.modifiers() == Qt.ControlModifier:
            self.switch_to_settings()


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
        try:
            main()

        except requests.exceptions.ConnectionError:
            ui_popup("Connection Error. This error belongs to PornHub. I can't do anything about it.")
