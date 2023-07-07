"""
IMPORTANT INFORMATION

THIS PROJECT IS LICENSED UNDER THE LGPLv3 License
You should have received a copy of the license along with this program.

The Source code of this program can be found here: https://github.com/EchterAlsFake/Porn_Fetch

API by Egsagon: https://github.com/Egsagon/PHUB



Author: EchterAlsFake - Johannes Habel

Version: 1.1
2023
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from ui_form import Ui_Widget
from phub import Client, Quality
import os
from configparser import ConfigParser
from colorama import *

def ui_popup(text):
    qmsg_box = QMessageBox()
    qmsg_box.setText(str(text))
    qmsg_box.exec()

def debug(text):
    print(f"{Fore.LIGHTCYAN_EX}[DEBUG]{Fore.RESET}{text}")

def test_path(path):

    if os.path.exists(path) == False:

        ui_popup(text="Path does not exist.  You need to put a / at the end of the path.")

    else:
        return path


class Widget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.video = None
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.conf = ConfigParser()
        self.conf.read("config.ini")
        self.client = Client(language="en")

        self.ui.button_start.clicked.connect(self.start)
        self.ui.button_start_file.clicked.connect(self.start_file)
        self.ui.button_get_metadata.clicked.connect(self.get_metadata)
        self.ui.button_start_user_channel.clicked.connect(self.user_channel)

    def get_quality(self):

        if self.ui.radio_highest.isChecked():
            return Quality.BEST

        elif self.ui.radio_middle.isChecked():
            return Quality.MIDDLE

        elif self.ui.radio_lowest.isChecked():
            return Quality.WORST

        else:
            qmsg_box = QMessageBox()
            qmsg_box.setText("Please select a quality option, before starting with the download.")
            qmsg_box.exec()
            return False

    def callback(self, **kwargs):
        def _update_progress(pos, total):
            self.ui.progressbar_download.setMaximum(total)
            self.ui.progressbar_download.setValue(pos)

        return _update_progress
    def test_video(self, url):

        try:

            self.video = self.client.get(url)
            title = self.video.title
            return self.video

        except Exception as e:
            ui_popup(text=str(f"The Video URL is invalid.  Exception: {e}"))
            return False

    def start(self):

        url = self.ui.lineedit_url.text()
        video = self.test_video(url)

        if video != False:
            debug(f"URL: {url}")
            self.download(video)

    def download(self, video):

        quality = self.get_quality()
        debug(f"Quality: {quality}")
        if quality != False:

            output_path = self.ui.lineedit_output.text()
            output_path = test_path(output_path)

            if output_path != False:

                debug(f"Output path: {output_path}")
                title = video.title
                debug(f"Title: {title}")
                output_path = str(output_path) + str(title)

                try:
                    self.ui.lineedit_status.setText(f"Downloading: {title}")
                    debug("Downloading...")
                    video.download(callback=self.callback, quality=quality, path=output_path)

                except Exception as e:
                    ui_popup(text=str(f"An unexpected error happened.  Exception: {e}"))

    def start_file(self):

        file_path = self.ui.lineedit_url_file.text()

        try:
            with open(file_path, "r") as file:
                content = file.read().splitlines()


                for url in content:
                    print(url)
                    if self.test_video(url) != False:
                        ""

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
            duration = f"{str(video.duration)}m"
            hotspots = str(video.hotspots)

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
                    self.ui.lineedit_status.setText(f"Downloaded: {counter}/{length}")

                except IndexError as e:
                    ui_popup(text=str(f"Index Error.  (Just ignore this exception.  The download should still be finished)  Exception: {e}"))

    def qmsg_box(self, text):
        message_box = QMessageBox()
        message_box.setText(str(text))
        message_box.exec()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
