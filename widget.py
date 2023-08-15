__author__ = "EchterAlsFake : Johannes Habel"
__version__ = "2.2"
__source__ = "https://github.com/EchterAlsFake/Porn_Fetch"
__license__ = "GPL 3"

credits_lol = """
Porn Fetch is created and maintained by EchterAlsFake | Johannes Habel.
EchterAlsFake is the internet pseudonym for Johannes Habel.

Porn Fetch comes 'AS IS' without any warranty or liability. 
You are responsible for your actions, but you get a few rights in exchange:

You are free to copy, modify, distribute and sell this software.
The software is licensed under the GPL 3.

The official Source code is available on GitHub:

https://github.com/EchterAlsFake/Porn_Fetch

This software uses some external libraries that are out of my control.

These are:

tqdm
pyside6
phub
colorama
sentry sdk
requests
wget
bs4 # Used by PHUB
js2py # Used by PHUB

Graphics:
Checkmark Icon: https://www.iconsdb.com/barbie-pink-icons/checkmark-icon.html

A special thanks to Egsagon for creating PHUB.
This project would not be possible without his great API and I have big respect for him!

2.2 - 2023
"""

import sys
import argparse
import sentry_sdk
import os
import requests

from configparser import ConfigParser
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTreeWidgetItem, QInputDialog, QLineEdit, QButtonGroup
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
            config_file.close() # I know, I don't have to close it manually, but I got some i/o errors, when not doing it.

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
        self.video.download(callback=self.callback, quality=self.quality, path=self.output_path)


class Widget(QWidget):
    """Main UI widget. Design is loaded from the ui_main_widget.py file. Feel free to change things if you want."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup()

        if not os.path.exists("graphics"):
            get_graphics()
        self.video = None
        self.api_language = "en"
        self.custom_language = False
        self.logging = None
        self.delay = True
        self.client = None
        self.download_thread = None
        self.threadpool = QThreadPool()

        self.ui = Ui_Porn_Fetch_Widget()
        self.ui.setupUi(self)
        self.button_group() # Needs to be called before load_user_settings!
        self.load_user_settings()  # Loads the user settings from config.ini to make settings persistent
        self.ui.stacked_main_account.setCurrentIndex(1)

        alpha_value = int((int(self.transparency) / 100) * 255) # Ignore type error, because the int type will be defined in self.load_user_settings().  If config file isn't corrupted, it should be no problem!
        color = QColor(0, 0, 0, alpha_value)
        self.setStyleSheet(f"background-color: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()});color: rgb(255,255,255);border: none;")


        self.ui.stackedWidget.setCurrentIndex(0)
        self.button_connectors()


    def button_connectors(self):
        self.ui.button_start.clicked.connect(self.start)
        self.ui.button_start_file.clicked.connect(self.start_file)
        self.ui.button_get_metadata.clicked.connect(self.get_metadata)
        self.ui.button_start_user_channel.clicked.connect(self.user_channel)
        self.ui.button_start_search.clicked.connect(self.search_videos)
        self.ui.button_download_search_query.clicked.connect(self.download_search)
        self.ui.button_settings_apply.clicked.connect(self.settings_tab)
        self.ui.button_settings_help.clicked.connect(self.help)
        self.ui.button_switch_to_account.clicked.connect(self.switch_to_account)
        self.ui.button_switch_main_page.clicked.connect(self.switch_to_main)
        self.ui.button_account_login.clicked.connect(self.login)
        self.ui.button_account_list_liked_videos.clicked.connect(self.get_liked_videos)
        self.ui.button_account_list_rec_videos.clicked.connect(self.get_recommended_videos)
        self.ui.button_account_list_watched_videos.clicked.connect(self.get_watched_videos)
        self.ui.button_account_download.clicked.connect(self.download_tree_widget)

    def button_group(self):
        """Separates the QRadioButtons from the different grid layouts"""

        button_group_quality = QButtonGroup()
        button_group_quality.addButton(self.ui.radio_highest)
        button_group_quality.addButton(self.ui.radio_lowest)
        button_group_quality.addButton(self.ui.radio_half)


        button_group_threading = QButtonGroup()
        button_group_threading.addButton(self.ui.radio_threading_multiple_2)
        button_group_threading.addButton(self.ui.radio_threading_single_2)

        button_group_api_language = QButtonGroup()
        button_group_api_language.addButton(self.ui.api_radio_es)
        button_group_api_language.addButton(self.ui.api_radio_fr)
        button_group_api_language.addButton(self.ui.api_radio_en)
        button_group_api_language.addButton(self.ui.api_radio_de)
        button_group_api_language.addButton(self.ui.api_radio_ru)

        button_group_ui_language = QButtonGroup()
        button_group_ui_language.addButton(self.ui.application_language_en)
        self.buttonGroups = button_group_ui_language, button_group_threading, button_group_quality, button_group_api_language

    def setup(self):
        self.conf = ConfigParser()
        self.conf.read("config.ini")

        if self.conf["Debug"]["sentry"] == "true":
            enable_error_handling()

        elif self.conf["Debug"]["sentry"] == "false":
            self.sentry_data_collection()

        logging(msg="Setup complete", level="0")

    def get_mode(self):

        if self.ui.radio_threading_single_2.isChecked():
            self.mode = "single"

        elif self.ui.radio_threading_multiple_2.isChecked():
            self.mode = "multiple"

        else:
            self.mode = "single"

    def sentry_data_collection(self):

        dlg = QMessageBox(self)
        dlg.setWindowTitle("I have a question!")
        dlg.setText("Do you enable automatic error collection by Sentry.io?  (Includes the name of your PC).  Sentry won't collect user / system specific information")
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
            return Quality.HALF # Changed to half, because the API changed the name in v3.1

        elif self.ui.radio_lowest.isChecked():
            return Quality.WORST

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
            self.client = Client(language=self.api_language, delay=True) # Fixes most API issues. Valid since PHUB 3.1
            self.video = self.client.get(url)
            return self.video


        except IndexError:
            print("API Error: Setting delay to 3 seconds.  Please wait a few seconds....")
            logging(msg="IndexError: Settings delay to 3 seconds....", level="1")
            self.delay = 3
            logging(msg="Retrying....", level="0")
            self.test_video(url)

        except Exception  as e:
            ui_popup(f"There was an error : {e} ")
            logging(msg=e, level="1")
            if self.sentry:
                sentry_sdk.capture_exception(e)


    def start(self):

        url = self.ui.lineedit_url.text()
        video = self.test_video(url)
        logging(msg=f"Downloading: {url}", level="0")
        self.download(video, progress_bar=self.ui.progressbar_download)

    def update_progressbar(self, pos, total, progress_bar):
        progress_bar.setMaximum(total)
        progress_bar.setValue(pos)

    def callback(self, pos, total):
        self.ui.progressbar_download.setMaximum(total)
        self.ui.progressbar_download.setValue(pos)

    def download(self, video, progress_bar):

        quality = self.get_quality()
        print(quality)
        self.get_mode()
        output_path = self.ui.lineedit_output.text()

        title = video.title
        title = strip_title(title) # Fixes OS Error on Windows
        output_path = output_path + title + ".mp4"

        try:
            if self.mode == "multiple":
                self.download_thread = DownloadThread(video, quality, output_path)
                self.download_thread.signals.progress.connect(lambda pos, total, pb=progress_bar: self.update_progressbar(pos, total, pb))
                self.threadpool.start(self.download_thread)

            elif self.mode == "single":
                self.video.download(callback=self.callback, quality=quality, path=output_path)

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

            for url in content:
                if self.test_video(url) is None:
                    ui_popup(f"The following URL is invalid: {url}  Please remove it from the file or correct it and try again.")

            for url in content:
                if not self.custom_language:
                    self.get_client_language()

                self.client = Client(language=self.api_language, delay=self.delay)
                video = self.client.get(url)

                try:
                    self.download(video=video, progress_bar=self.ui.progressbar_download)

                except Exception as e:
                    ui_popup(text=str(f"An unexpected error happened.  Exception: {e}"))

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
            image_url = video.image_url
            tags = video.tags

            self.ui.lineedit_likes.setText(likes)
            self.ui.lineedit_tags.setText(tags)
            self.ui.lineedit_image_url.setText(image_url)
            self.ui.lineedit_title.setText(title)
            self.ui.lineedit_author.setText(author)
            self.ui.lineedit_views.setText(views)
            self.ui.lineedit_date.setText(date)
            self.ui.lineedit_duration.setText(duration)
            self.ui.lineedit_hotspots.setText(hotspots)

    def user_channel(self):

        user = self.ui.lineedit_user_channel.text()
        try:
            user_object = self.client.get_user(url=user)
            logging(msg=user_object.name, level="0")

        except Exception as e:
            ui_popup(text=f"An unexpected error happened.  Exception: {e}  Note, the User must be a URL and NOT a name.")
            if self.sentry:
                sentry_sdk.capture_exception(e)
                ui_popup("Error was captured by Sentry.")

        else:
            videos = user_object.videos
            for video in videos:
                url = video.url
                url = f"https://www.pornhub.com/{url}"
                video = self.test_video(url)
                self.download(video, progress_bar=self.ui.progressbar_download)

    def search_videos(self):
        # Searches videos with query string and lets the user select them
        query = self.ui.lineedit_search_query.text()
        if not self.custom_language:
            self.get_client_language()

        self.client = Client(language=self.api_language, delay=self.delay)
        try:
            query_object = self.client.search(query)

        except requests.exceptions.ConnectionError:
            ui_popup("PornHub had an error. Increasing delay to 3 seconds.  Please don't overuse the search feature!.")
            self.delay = 3
            self.search_videos()

        for i, video in enumerate(query_object, start=1): # Limiting search results to 50
            item = QTreeWidgetItem(self.ui.treeWidget)
            item.setText(0, f"{i}) {video.title}")
            item.setData(0, QtCore.Qt.UserRole, video.url)
            item.setCheckState(0, QtCore.Qt.Unchecked)  # Adds a checkbox

    def download_search(self):
        # Downloads all selected videos with a for loop
        for i in range(self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(i)
            checkState = item.checkState(0)
            if checkState == QtCore.Qt.Checked:
                video_url = item.data(0, QtCore.Qt.UserRole)
                url = f"https://www.pornhub.com/{video_url}"
                video = self.test_video(url)
                self.download(video, progress_bar=self.ui.progressbar_download)

    def settings_tab(self):
        with open("config.ini", "w") as config_file:
            if self.ui.radio_highest.isChecked():
                self.conf.set("Porn_Fetch", "default_quality", "best")

            if self.ui.radio_half.isChecked():
                self.conf.set("Porn_Fetch", "default_quality", "middle")

            if self.ui.radio_lowest.isChecked():
                self.conf.set("Porn_Fetch", "default_quality", "worst")

            if self.ui.radio_threading_single_2.isChecked():
                self.conf.set("Porn_Fetch", "default_threading", "single")

            if self.ui.radio_threading_multiple_2.isChecked():
                self.conf.set("Porn_Fetch", "default_threading", "multiple")

            if self.ui.settings_checkbox_sentry.isChecked():
                self.conf.set("Debug", "sentry", "true")

            else:
                self.conf.set("Debug", "sentry", "false")

            if self.ui.settings_checkbox_logging.isChecked():
                self.conf.set("Debug", "logging", "true")

            else:
                self.conf.set("Debug", "logging", "false")

            if self.ui.api_radio_de.isChecked():
                self.conf.set("Porn_Fetch", "api_language", "de")

            elif self.ui.api_radio_fr.isChecked():
                self.conf.set("Porn_Fetch", "api_language", "fr")

            elif self.ui.api_radio_es.isChecked():
                self.conf.set("Porn_Fetch", "api_language", "es")

            elif self.ui.api_radio_ru.isChecked():
                self.conf.set("Porn_Fetch", "api_language", "ru")

            elif self.ui.api_radio_en.isChecked():
                self.conf.set("Porn_Fetch", "api_language", "en")

            if self.ui.application_language_en.isChecked():
                self.conf.set("UI", "language", "en")

            transparency = self.ui.horizontalSlider.value()
            self.conf.set("UI", "transparency", str(transparency)) # Needs to be a string!
            self.conf.write(config_file)

            ui_popup("Applied! (Please restart for changes to take effect)")

    def load_user_settings(self):

        if self.conf["Porn_Fetch"]["default_quality"] == "best":
            self.ui.radio_highest.setChecked(True)

        elif self.conf["Porn_Fetch"]["default_quality"] == "middle":
            self.ui.radio_half.setChecked(True)

        elif self.conf["Porn_Fetch"]["default_quality"] == "worst":
            self.ui.radio_lowest.setChecked(True)

        if self.conf["Porn_Fetch"]["default_threading"] == "multiple":
            self.ui.radio_threading_multiple_2.setChecked(True)

        elif self.conf["Porn_Fetch"]["default_threading"] == "single":
            self.ui.radio_threading_single_2.setChecked(True)

        if self.conf["Debug"]["sentry"] == "true":
            self.ui.settings_checkbox_sentry.setChecked(True)

        else:
            self.ui.settings_checkbox_sentry.setChecked(False)

        if self.conf["Debug"]["logging"] == "true":
            self.ui.settings_checkbox_logging.setChecked(True)
            self.logging = True

        else:
            self.ui.settings_checkbox_logging.setChecked(False)
            self.logging = False

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

    def login(self):

        username = self.ui.lineedit_account_username.text()
        password = self.ui.lineedit_account_password.text()
        self.ui.lineedit_account_status.setText("Logging in...")

        try:
            if not self.custom_language:
                self.get_client_language()

            self.client = Client(username=username, password=password, language=self.api_language, delay=self.delay)
            self.client.login()
            self.ui.lineedit_account_status.setText(f"Logged in as: {self.client.account.name}")

        except Exception as e:
            ui_popup(f"An error happened. This error will NOT be sent to sentry, to prevent leaking your account data! ERROR: {e}")

    def add_to_tree_widget(self, iterator, tree_widget):
        try:
            for i, video in enumerate(iterator, start=1): # Limiting search results to 50
                item = QTreeWidgetItem(tree_widget)
                item.setText(0, f"{i}) {video.title}")
                item.setData(0, QtCore.Qt.UserRole, video.url)
                item.setCheckState(0, QtCore.Qt.Unchecked)  # Adds a checkbox
        except Exception as e:
            ui_popup(f"An error happened. This error will NOT be sent to sentry, to prevent leaking your account data! ERROR: {e}")


    def get_liked_videos(self):
        try:
            videos = self.client.account.liked
            self.add_to_tree_widget(iterator=videos, tree_widget=self.ui.tree_widget_account)

        except Exception as e:
            ui_popup(f"An error happened. This error will NOT be sent to sentry, to prevent leaking your account data! ERROR: {e}")

    def get_watched_videos(self):
        try:
            videos = self.client.account.watched
            self.add_to_tree_widget(iterator=videos, tree_widget=self.ui.tree_widget_account)

        except Exception as e:
            ui_popup(f"An error happened. This error will NOT be sent to sentry, to prevent leaking your account data! ERROR: {e}")

    def get_recommended_videos(self):

        try:
            videos = self.client.account.recommended
            self.add_to_tree_widget(iterator=videos, tree_widget=self.ui.tree_widget_account)

        except Exception as e:
            ui_popup(f"An error happened. This error will NOT be sent to sentry, to prevent leaking your account data! ERROR: {e}")

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
            ui_popup(f"An error happened. This error will NOT be sent to sentry, to prevent leaking your account data! ERROR: {e}")


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

    def help(self):
        text = """

API Language:

The API handles your requests to PornHub.com   If the API is in english language, then all the titles and video
attributes are also in english. If the API is for example in German language, then the video titles are (if automatically
translated by PornHub) also in German language.   Not all videos are supported! 

UI Language:

UI language defined the language in the application. See contribution on GitHub how to port it into your language

Quality:

Highest = Best Quality possible, Half = somewhere in the middle, Lowest = Least quality possible

Debug:

Sentry: Captures error logs, which helps me to fix issues faster, and you don't have to report them
Logging: Creates a log.log file, which may helps to diagnose issues.

UI Transparency: 

Defines the UI background transparency. Please note, that this feature doesn't work well on Hyprland!

Threading: 

Threading uses multiple cores of your CPU to download multiple videos simultaneously. This leads to a broken
progressbar, but can have a big speed impact if you have a really fast internet connection.


If you still have questions, let me know on GitHub in discussions.
"""
        ui_popup(text)




def main():
    print("Checking configuration...")

    app = QApplication(sys.argv)
    setup_config_file()

    widget = License()
    widget.check_license_and_proceed()
    sys.exit(app.exec())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cli", help="CLI Terminal Version. Intended for advanced users or systems without a Graphical Environment", action="store_true")
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

            # Some common exceptions...
        except requests.exceptions.SSLError:
            ui_popup("Couldn't establish a secure connection to PornHub. This mostly happens, because your router / ISP / firewall blocks PornHub. Are you currently at a hotel or a university?")

        except requests.exceptions.ConnectionError:
            ui_popup("There was a connection error. This mostly happens, because PornHub blocks you, or your connection is unstable. Please wait, or change IP and try again")

        except KeyboardInterrupt:
            print("Bye")
            sys.exit()

        except PermissionError:
            ui_popup("You don't have permissions to write / access something. Please give Porn Fetch the appropriate permissions and try again.")



# EOF
