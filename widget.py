__author__ = "EchterAlsFake : Johannes Habel"
__version__ = "2.1"
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

Graphics:

Download Icon : https://icons8.com/icon/104149/herunterladen
Search Icon : https://icons8.com/icon/aROEUCBo74Il/suche
Settings Icon : https://icons8.com/icon/52146/einstellungen
C Icon : https://icons8.com/icon/Uehg4gyVyrUo/copyright
M Icon By Unicons Font on Icon Scout : https://iconscout.com/icons/medium : https://iconscout.com/contributors/unicons
: https://iconscout.com
Checkmark Icon: https://www.iconsdb.com/barbie-pink-icons/checkmark-icon.html

A special thanks to Egsagon for creating PHUB.
This project would not be possible without his great API and I have much respect for him!

2.1 - 2023
"""

import sys
import argparse
import sentry_sdk
import os
import requests

from configparser import ConfigParser
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTreeWidgetItem, QInputDialog, QLineEdit
from PySide6.QtGui import QKeyEvent, QColor
from PySide6.QtCore import Signal, QThreadPool, QRunnable, QObject, Qt, QDir
from src.license_agreement import Ui_Widget_License
from phub import Client, Quality
from src.ui_main_widget import Ui_Porn_Fetch_Widget
from src.setup import enable_error_handling, setup_config_file, strip_title, logging
from src.cli import CLI

def ui_popup(text):
    """ A simple UI popup that will be used for small messages to the user."""
    qmsg_box = QMessageBox()
    qmsg_box.setText(str(text))
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

    def callback(self, **kwargs):
        """The callback argument from PHUB needs to be extracted. This is the reason why I need to use two functions."""
        def _update_progress(pos, total):
            self.signals.progress.emit(pos, total)

        return _update_progress

    def run(self):
        self.video.download(callback=self.callback, quality=self.quality, path=self.output_path)


class Widget(QWidget):
    """Main UI widget. Design is loaded from the ui_main_widget.py file. Feel free to change things, if you want."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup()

        self.video = None
        self.api_language = "en"
        self.custom_language = False
        self.delay = True
        self.client = None
        self.ui = Ui_Porn_Fetch_Widget()
        self.ui.setupUi(self)

        transparency_percent = int(self.conf["UI"]["transparency"])
        alpha_value = int(transparency_percent // 100 * 255)
        color = QColor(0, 0, 0, alpha_value)
        self.setStyleSheet(f"background-color: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()});color: white;")

        self.download_thread = None
        self.threadpool = QThreadPool()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.load_user_settings() # Loads the user settings from config.ini to make settings persistent
        self.button_connectors()

    def button_connectors(self):
        self.ui.button_start.clicked.connect(self.start)
        self.ui.button_start_file.clicked.connect(self.start_file)
        self.ui.button_get_metadata.clicked.connect(self.get_metadata)
        self.ui.button_start_user_channel.clicked.connect(self.user_channel)
        self.ui.button_start_search.clicked.connect(self.search_videos)
        self.ui.button_download_search_query.clicked.connect(self.download_search)
        self.ui.button_settings_apply.clicked.connect(self.settings_tab)

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

        if self.ui.radio_highest.isChecked():
            return Quality.BEST

        elif self.ui.radio_middle.isChecked():
            return Quality.MIDDLE

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
        self.download(video)

    def update_progressbar(self, pos, total):
        self.ui.progressbar_download.setMaximum(total)
        self.ui.progressbar_download.setValue(pos)

    def callback(self, pos, total):
        self.ui.progressbar_download.setMaximum(total)
        self.ui.progressbar_download.setValue(pos)

    def download(self, video):

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
                self.download_thread.signals.progress.connect(self.update_progressbar)
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
                    self.download(video=video)

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
            ui_popup(text=str(f"An unexpected error happened.  Exception: {e}  Note, the User must be a URL and NOT a name."))
            if self.sentry:
                sentry_sdk.capture_exception(e)
                ui_popup("Error was captured by Sentry.")

        else:
            videos = user_object.videos
            for video in videos:
                url = video.url
                url = f"https://www.pornhub.com/{url}"
                video = self.test_video(url)
                self.download(video)

    def search_videos(self):
        # Searches videos with query string and lets the user select them
        query = self.ui.lineedit_search_query.text()
        if not self.custom_language:
            self.get_client_language()

        self.client = Client(language=self.api_language, delay=self.delay)
        try:
            query_object = self.client.search(query)

        except requests.exceptions.ConnectionError:
            ui_popup("You got blocked by PornHub. Some videos won't show up in the search results. The only option is to wait or change IP address. I can't do anything about it. You can still download the videos, that got returned by PornHub.")

        for i, video in enumerate(query_object[:50], start=1): # Limiting search results to 50
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
                self.download(video)

    def settings_tab(self):
        with open("config.ini", "w") as config_file:
            if self.ui.radio_highest.isChecked():
                self.conf.set("Porn_Fetch", "default_quality", "best")

            if self.ui.radio_middle.isChecked():
                self.conf.set("Porn_Fetch", "default_quality", "middle")

            if self.ui.radio_lowest.isChecked():
                self.conf.set("Porn_Fetch", "default_quality", "worst")

            if self.ui.radio_threading_single_2.isChecked():
                self.conf.set("Porn_Fetch", "default_threading", "single")

            if self.ui.radio_threading_multiple_2.isChecked():
                self.conf.set("Porn_Fetch", "default_threading", "multiple")

            if self.ui.settings_checkbox_sentry.isChecked():
                self.conf.set("Porn_Fetch", "sentry", "true")

            if not self.ui.settings_checkbox_sentry.isChecked():
                self.conf.set("Debug", "sentry", "false")

            self.conf.write(config_file)
            ui_popup("Applied!")

    def load_user_settings(self):

        if self.conf["Porn_Fetch"]["default_quality"] == "best":
            self.ui.radio_highest.setChecked(True)
            self.ui.radio_highest.setChecked(True)

        if self.conf["Porn_Fetch"]["default_quality"] == "middle":
            self.ui.radio_middle.setChecked(True)
            self.ui.radio_middle.setChecked(True)

        if self.conf["Porn_Fetch"]["default_quality"] == "worst":
            self.ui.radio_lowest.setChecked(True)
            self.ui.radio_lowest.setChecked(True)

        if self.conf["Porn_Fetch"]["default_threading"] == "multiple":
            self.ui.radio_threading_multiple_2.setChecked(True)
            self.ui.radio_threading_multiple_2.setChecked(True)

        if self.conf["Porn_Fetch"]["default_threading"] == "single":
            self.ui.radio_threading_single_2.setChecked(True)
            self.ui.radio_threading_single_2.setChecked(True)

        if self.conf["Debug"]["sentry"] == "true":
            self.ui.settings_checkbox_sentry.setChecked(True)

        elif self.conf["Debug"]["sentry"] == "false":
            self.ui.settings_checkbox_sentry.setChecked(False)

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




