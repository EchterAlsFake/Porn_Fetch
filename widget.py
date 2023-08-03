__author__ = "EchterAlsFake : Johannes Habel"
__version__ = "1.8"
__source__ = "https://github.com/EchterAlsFake/Porn_Fetch"
__license__ = "GPL 3"

sentry = False
credits_lol = f"""
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

1.8 - 2023
"""

import sys
import argparse
import sentry_sdk
import time
import requests
import os.path

from configparser import ConfigParser
from PySide6 import QtCore
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTreeWidgetItem
from PySide6.QtCore import Signal, QThreadPool, QRunnable, QObject, QSize
from src.license_agreement import Ui_Widget_License
from phub import Client, Quality
from src.ui_main_widget import Ui_Widget
from src.setup import enable_error_handling, get_graphics, setup_config_file
from src.cli import CLI

def ui_popup(text):
    qmsg_box = QMessageBox()
    qmsg_box.setText(str(text))
    qmsg_box.exec()


class License(QWidget):
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
            print("License accepted. Continuing...")
            self.show_main_window()
        else:
            print("License was not accepted. Prompting user...")
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
            sys.exit(0)

    def show_main_window(self):
        self.close()
        self.main_widget = Widget()
        self.main_widget.show()


class DownloadProgressSignal(QObject):
    progress = Signal(int, int)


class DownloadThread(QRunnable):

    def __init__(self, video, quality, output_path, parent=None):
        super().__init__()
        self.video = video
        self.quality = quality
        self.output_path = output_path
        self.signals = DownloadProgressSignal()

    def callback(self, **kwargs):
        def _update_progress(pos, total):
            self.signals.progress.emit(pos, total)

        return _update_progress

    def run(self):
        self.video.download(callback=self.callback, quality=self.quality, path=self.output_path)


class Widget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        print("Checking graphics...")

        if not os.path.exists("graphics"):
            print("Downloading assets...")
            get_graphics()
            print("Done")

        self.conf = ConfigParser()
        self.conf.read("config.ini")

        if self.conf["Debug"]["sentry"] == "true":
            enable_error_handling()

        elif self.conf["Debug"]["sentry"] == "false":
            self.sentry_data_collection()

        self.video = None
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        # Set correct image path
        icon_download = QIcon()
        icon_download.addFile(u"graphics/download.ico", QSize(), QIcon.Normal, QIcon.Off)
        icon_search = QIcon()
        icon_search.addFile(u"graphics/search.ico", QSize(), QIcon.Normal, QIcon.Off)
        icon_metadata = QIcon()
        icon_metadata.addFile(u"graphics/medium.ico", QSize(), QIcon.Normal, QIcon.Off)
        icon_settings = QIcon()
        icon_settings.addFile(u"graphics/settings-colorful.ico", QSize(), QIcon.Normal, QIcon.Off)
        icon_c = QIcon()
        icon_c.addFile(u"graphics/c.ico", QSize(), QIcon.Normal, QIcon.Off)

        self.ui.button_download_tab.setIcon(icon_download)
        self.ui.button_settings_tab.setIcon(icon_settings)
        self.ui.button_search_tab.setIcon(icon_search)
        self.ui.button_metadata_tab.setIcon(icon_metadata)
        self.ui.button_credits_tab.setIcon(icon_c)



        
        self.client = Client(language="en")
        self.download_thread = None
        self.mode = "single"
        self.threadpool = QThreadPool()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.load_user_settings()

        self.ui.button_start.clicked.connect(self.start)
        self.ui.button_start_file.clicked.connect(self.start_file)
        self.ui.button_get_metadata.clicked.connect(self.get_metadata)
        self.ui.button_start_user_channel.clicked.connect(self.user_channel)
        self.ui.button_start_search.clicked.connect(self.search_videos)
        self.ui.button_download_search_query.clicked.connect(self.download_search)

        self.ui.button_credits_tab.clicked.connect(self.do_1)
        self.ui.button_download_tab.clicked.connect(self.do_2)
        self.ui.button_metadata_tab.clicked.connect(self.do_3)
        self.ui.button_search_tab.clicked.connect(self.do_4)
        self.ui.button_settings_tab.clicked.connect(self.do_5)
        self.ui.button_settings_apply.clicked.connect(self.settings_tab)

    def do_1(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def do_2(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def do_3(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def do_4(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def do_5(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def get_mode(self):

        if self.ui.radio_threading_single.isChecked():
            self.mode = "single"

        elif self.ui.radio_threading_multiple.isChecked():
            self.mode = "multiple"

        else:
            self.mode = "single"

    def sentry_data_collection(self):

        dlg = QMessageBox(self)
        dlg.setWindowTitle("I have a question!")
        dlg.setText("Do you enable automatic error collection by Sentry.io?  This won't include system or user specific information.")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()

        if button == QMessageBox.Yes:
            enable_error_handling()
            self.conf.set("Debug", "sentry", "true")
            with open("config.ini", "w") as config_file:
                self.conf.write(config_file)
                config_file.close()
            sentry = True

        else:
            sentry = False

    def get_quality(self):

        if self.ui.radio_highest.isChecked():
            return Quality.BEST

        elif self.ui.radio_middle.isChecked():
            return Quality.MIDDLE

        elif self.ui.radio_lowest.isChecked():
            return Quality.WORST

    def test_video(self, url):

        try:
            self.video = self.client.get(url)
            return self.video

        except IndexError:
            ui_popup("Video object didn't return any data. You probably got blocked by PornHub. I am trying to automatically fix the situation. Please wait a few seconds....")
            self.client = Client(language="en")
            time.sleep(3)
            try:
                self.test_video(url)

            except IndexError:
                ui_popup("Sorry, that didn't work. Please wait a few minutes or change your IP address. I can not do anything about it.")


        except Exception as e:
            ui_popup(text=f"There was an error with the URL.  Here is a detailed error: {e}  Please report it on GitHub :)")
            if sentry:
                sentry_sdk.capture_exception(e)
                ui_popup("Error was captured by Sentry. I'll review it soon.")

    def start(self):

        url = self.ui.lineedit_url.text()
        video = self.test_video(url)

        if video is not None:
            self.download(video)

        else:
            ui_popup("There was a really weird error. Please tell me exactly what you did to trigger this.")

    def update_progressbar(self, pos, total):
        self.ui.progressbar_download.setMaximum(total)
        self.ui.progressbar_download.setValue(pos)

    def callback(self, **kwargs):
        def _update_progress(pos, total):
            self.ui.progressbar_download.setMaximum(total)
            self.ui.progressbar_download.setValue(pos)

        return _update_progress

    def download(self, video):

        quality = self.get_quality()
        self.get_mode()
        output_path = self.ui.lineedit_output.text()

        title = video.title
        output_path = str(output_path) + str(title)

        try:
            self.ui.label_search_query_progress.setText(f"Downloading: {title}")
            if self.mode == "multiple":

                if self.mode == "multiple":
                    self.download_thread = DownloadThread(video, quality, output_path)
                    self.download_thread.signals.progress.connect(self.update_progressbar)
                    self.threadpool.start(self.download_thread)

            elif self.mode == "single":

                self.video.download(callback=self.callback, quality=quality, path=output_path)

        except Exception as e:
            ui_popup(text=str(f"An unexpected error happened.  Exception: {e}"))

    def start_file(self):

        file_path = self.ui.lineedit_url_file.text()
        self.get_mode()
        try:
            with open(file_path, "r") as file:
                content = file.read().splitlines()


                for url in content:
                    if self.test_video(url) is not None:
                        pass

                    else:
                        ui_popup(f"The following URL is invalid: {url}  Please remove it from the file or correct it and try again.")

                for url in content:
                    video = self.client.get(str(url))

                    try:
                        self.download(video=video)

                    except Exception as e:
                        ui_popup(text=str(f"An unexpected error happened.  Exception: {e}"))



        except PermissionError as e:
            ui_popup(text=str(f"Permission denied. Please make sure, I can access and read the file... Exception: {e}"))

        except FileNotFoundError as e:
            ui_popup(text=str(f"The file does not exist.  Exception: {e}"))

    def get_metadata(self):

        url = self.ui.lineedit_url.text()
        video = self.test_video(url)

        if video != False:

            title = str(video.title)
            author = str(video.author.name)
            views = str(video.views)
            date = str(video.date)
            duration = video.duration.seconds
            duration = duration / 60
            duration = str(f"{duration}m")
            hotspots = str(video.hotspots)
            likes_up = str(video.like.up)
            likes_down = str(video.like.down)
            likes = str(f"Likes: {likes_up} - Dislikes: {likes_down}")
            image_url = str(video.image_url)
            tags = str(video.tags)

            self.ui.lineedit_likes.setText(likes)
            self.ui.lineedit_tags.setText(tags)
            self.ui.lineedit_image_url.setText(image_url)
            self.ui.lineedit_title.setText(title)
            self.ui.lineedit_author.setText(author)
            self.ui.lineedit_views.setText(views)
            self.ui.lineedit_date.setText(date)
            self.ui.lineedit_duration.setText(duration)
            self.ui.lineedit_hotspots.setText(hotspots)

        else:
            ui_popup(text=str(f"The Video URL is invalid."))

    def user_channel(self):

        user = self.ui.lineedit_user_channel.text()
        try:
            user_object = self.client.get_user(url=user)
            print(user_object.name)

        except Exception as e:
            ui_popup(text=str(f"An unexpected error happened.  Exception: {e}  Note, the User must be a URL and NOT a name."))
            if sentry:
                sentry_sdk.capture_exception(e)
                ui_popup("Error was captured by Sentry.")

        else:

            videos = user_object.videos
            counter = 0
            length = len(videos)
            for video in videos:

                url = video.url
                print(url)
                url = "https://www.pornhub.com/" + url
                print(url)
                video = self.test_video(url)
                self.download(video)
                counter += 1
                try:
                    self.ui.label_search_query_progress.setText(f"Downloaded: {counter}/{length}")

                except IndexError as e:
                    ui_popup("You got blocked by PornHub. I try to fix this, but the best solution is to wait or change IP address")
                    self.client = Client(language="en")

                except Exception as e:
                    ui_popup(f"Unexpected Error: {e}")

                    if sentry:
                        sentry_sdk.capture_exception(e)

    def search_videos(self):
        # Searches videos with query string and lets the user select them
        query = self.ui.lineedit_search_query.text()
        query_object = self.client.search(query)
        length = len(query_object)
        self.ui.lineedit_total_videos.setText(str(length))

        for i, video in enumerate(query_object, start=1):
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
                url = "https://www.pornhub.com/" + video_url
                video = self.test_video(url)
                self.download(video)

    def settings_tab(self):
        with open("config.ini", "w") as config_file:
            if self.ui.settings_radio_best.isChecked():
                self.conf.set("Porn_Fetch", "default_quality", "best")

            if self.ui.settings_radio_middle.isChecked():
                self.conf.set("Porn_Fetch", "default_quality", "middle")

            if self.ui.settings_radio_worst.isChecked():
                self.conf.set("Porn_Fetch", "default_quality", "worst")

            if self.ui.settings_radio_single.isChecked():
                self.conf.set("Porn_Fetch", "default_threading", "single")

            if self.ui.settings_radio_multiple.isChecked():
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
            self.ui.settings_radio_best.setChecked(True)

        if self.conf["Porn_Fetch"]["default_quality"] == "middle":
            self.ui.radio_middle.setChecked(True)
            self.ui.settings_radio_middle.setChecked(True)

        if self.conf["Porn_Fetch"]["default_quality"] == "worst":
            self.ui.radio_lowest.setChecked(True)
            self.ui.settings_radio_worst.setChecked(True)

        if self.conf["Porn_Fetch"]["default_threading"] == "multiple":
            self.ui.radio_threading_multiple.setChecked(True)
            self.ui.settings_radio_multiple.setChecked(True)

        if self.conf["Porn_Fetch"]["default_threading"] == "single":
            self.ui.radio_threading_single.setChecked(True)
            self.ui.settings_radio_single.setChecked(True)

        if self.conf["Debug"]["sentry"] == "true":
            self.ui.settings_checkbox_sentry.setChecked(True)

        elif self.conf["Debug"]["sentry"] == "false":
            self.ui.settings_checkbox_sentry.setChecked(False)

def main():
    print("Checking configuration...")
    setup_config_file()

    app = QApplication(sys.argv)
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

