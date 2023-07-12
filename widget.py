"""
IMPORTANT INFORMATION

THIS PROJECT IS LICENSED UNDER THE LGPLv3 License
You should have received a copy of the license along with this program.

The Source code of this program can be found here: https://github.com/EchterAlsFake/Porn_Fetch

API by Egsagon: https://github.com/Egsagon/PHUB



Author: EchterAlsFake - Johannes Habel

Version: 1.4
2023
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QListWidget, QListWidgetItem, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import QThread, Signal
from ui_form import Ui_Widget
from phub import Client, Quality
import os
from PySide6 import QtCore
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


class DownloadThread(QThread):

    download_progress = Signal(int, int)

    def __init__(self, video, quality, output_path, parent=None):
        QThread.__init__(self, parent)
        self.video = video
        self.quality = quality
        self.output_path = output_path

    def callback(self, **kwargs):
        def _update_progress(pos, total):
            self.download_progress.emit(pos, total)

        return _update_progress

    def run(self):

        self.video.download(callback=self.callback, quality=self.quality, path=self.output_path)



class Widget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.video = None
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.conf = ConfigParser()
        self.conf.read("config.ini")
        self.client = Client(language="en")
        self.download_thread = None
        self.mode = "single"

        self.ui.button_start.clicked.connect(self.start)
        self.ui.button_start_file.clicked.connect(self.start_file)
        self.ui.button_get_metadata.clicked.connect(self.get_metadata)
        self.ui.button_start_user_channel.clicked.connect(self.user_channel)
        self.ui.button_start_search.clicked.connect(self.search_videos)
        self.ui.button_download_search_query.clicked.connect(self.download_search)

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

    def test_video(self, url):

        try:

            self.video = self.client.get(url)
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
        debug(f"Quality: {quality}")
        self.get_mode()
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
                    if self.mode == "multiple":

                        self.download_thread = DownloadThread(video, quality, output_path)
                        self.download_thread.download_progress.connect(self.update_progressbar)
                        self.download_thread.start()


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
                    print(url)
                    if self.test_video(url) != False:
                        ""

                    else:

                        ui_popup(f"The following URL is invalid: {url}  Please remove it from the file or correct it and try again.")

                for url in content:

                    video = self.client.get(str(url))
                    try:

                        self.download(video=video, mode=self.mode)

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

    def get_mode(self):

        if self.ui.radio_threading_single.isChecked():
            self.mode = "single"

        elif self.ui.radio_threading_multiple.isChecked():
            self.mode = "multiple"

        else:
            self.mode = "single"

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
                self.download(video, mode=self.mode)
                counter += 1
                try:
                    self.ui.lineedit_status.setText(f"Downloaded: {counter}/{length}")

                except IndexError as e:
                    ui_popup(text=str(f"Index Error.  (Just ignore this exception.  The download should still be finished)  Exception: {e}"))

    def search_videos(self):

        query = self.ui.lineedit_search_query.text()
        query_object = self.client.search(query)
        length = len(query_object)
        self.ui.lineedit_total_videos.setText(str(length))

        for i, video in enumerate(query_object, start=1):
            item = QTreeWidgetItem(self.ui.treeWidget_search_query)
            item.setText(0, f"{i}) {video.title}")
            item.setData(0, QtCore.Qt.UserRole, video.url)
            item.setCheckState(0, QtCore.Qt.Unchecked)  # Adds a checkbox
    def download_search(self):

        for i in range(self.ui.treeWidget_search_query.topLevelItemCount()):
            item = self.ui.treeWidget_search_query.topLevelItem(i)
            checkState = item.checkState(0)
            if checkState == QtCore.Qt.Checked:
                video_url = item.data(0, QtCore.Qt.UserRole)
                url = "https://www.pornhub.com/" + video_url
                video = self.test_video(url)
                self.download(video)


    def qmsg_box(self, text):
        message_box = QMessageBox()
        message_box.setText(str(text))
        message_box.exec()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())