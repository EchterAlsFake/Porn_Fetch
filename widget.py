__author__ = "EchterAlsFake : Johannes Habel"
__version__ = "1.6"
__source__ = "https://github.com/EchterAlsFake/Porn_Fetch"
__license__ = "LGPLv3"

import time

"""
INFORMATION

This program comes AS IS without any warranty of any kind.
You are free to copy, modify, redistribute, and/or sell it.


The Source Code can be found on GitHub : https://github.com/EchterAlsFake/Porn_Fetch

Author: Johannes Habel | EchterAlsFake
Co Author: ChatGPT by OpenAI
"""

credits = f"""

Developer / Maintainer : EchterAlsFake | Johannes Habel
Official contact E-Mail: EchterAlsFake@proton.me

Credits:

API: PHUB by Egsagon.  This project would not be possible without it.
Author: EchterAlsFake
License: LGPLv3

Plugins: Tabnine, Material Theme Icons, Sourcery
IDE: PyCharm Professional
Libraries: colorama, tqdm, PySide6, PHUB

Graphical User Interface was created with Qt - PySide6
Version: {__version__}"""

import sys
import threading
import os
import argparse
import webbrowser
import logging
from datetime import datetime

from PySide6 import QtCore
from colorama import *
from tqdm import tqdm
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTreeWidgetItem
from PySide6.QtCore import Signal, QThreadPool, QRunnable, QObject
from ui_form import Ui_Widget
from phub import Client, Quality

log_file = ".porn_fetch_LOG"

def logger_debug(function, message):
    date = datetime.now()
    logger = logging.getLogger(f"Date : {date} : Porn Fetch : {function}")
    logger.debug(f"DEBUG: {message}")

def logger_error(function, message):
    date = datetime.now()
    logger = logging.getLogger(f"Date : {date} : Porn Fetch : {function}")
    logger.error(f"DEBUG: {message}")

def ui_popup(text):
    qmsg_box = QMessageBox()
    qmsg_box.setText(str(text))
    qmsg_box.exec()

def clear():
    os.system("cls")
    os.system("clear")

def check_path(path):
    return True if os.path.exists(path) else False


class CLI():

    def __init__(self):
        self.z =f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET}"
        self.x = f"{Fore.LIGHTRED_EX}[~]{Fore.RESET}"
        self.quality = Quality.BEST
        self.output_path = "./"
        self.threading_mode = "multiple"
        self.client = Client(language="en")
        self.video = None
        self.pbar = None
        while True:
            self.menu()

    def callback(self, **kwargs):

        def _update_progress(pos, total):

            self.pbar = tqdm(total=total, dynamic_ncols=True)
            self.pbar.update(pos - self.pbar.n)
            if pos == total:
                self.pbar.close()
                self.pbar = None

        return _update_progress

    def check_video(self, url):

        try:
            self.video = self.client.get(url)
            return True

        except Exception as e:
            self.exception(e)

    def exception(self, e):
        print(f"{self.x}Unhandled Exception: {e}")

    def menu(self):

        if self.quality == Quality.BEST:
            quality_ext = f"{Fore.LIGHTCYAN_EX}Best"

        elif self.quality == Quality.MIDDLE:
            quality_ext = f"{Fore.LIGHTMAGENTA_EX}Middle"

        elif self.quality == Quality.WORST:
            quality_ext = f"{Fore.LIGHTRED_EX}Worst"

        options = input(f"""
{Fore.LIGHTYELLOW_EX}    Settings:
{Fore.LIGHTWHITE_EX}|----------------------|
{Fore.LIGHTCYAN_EX}|99) Change Quality     | {Fore.RESET}Currently set to: {quality_ext}
{Fore.LIGHTMAGENTA_EX}|98) Set output path    {Fore.RESET}| Currently set to: {self.output_path}
{Fore.LIGHTYELLOW_EX}|97) Set Threading mode | {Fore.RESET}Currently set to: {self.threading_mode}
{Fore.RESET}|----------------------|


{Fore.LIGHTCYAN_EX}1) Download a single Video
{Fore.LIGHTMAGENTA_EX}2) Download videos from a file
{Fore.LIGHTYELLOW_EX}3) Download all videos from a User / Channel
{Fore.LIGHTBLUE_EX}4) Get metadata from Videos
{Fore.LIGHTMAGENTA_EX}5) Search for videos and download them
{Fore.LIGHTWHITE_EX}6) Show credits
{Fore.LIGHTWHITE_EX}7) Submit Issue / Bug / Security vulnerabilities / Typos
{Fore.LIGHTRED_EX}8) Exit
{Fore.RESET}-------------------->:{Fore.RESET} """)


        if options == "99":
            self.change_quality()

        elif options == "98":
            self.set_output_path()

        elif options == "97":
            self.set_threading_mode()

        elif options == "1":
            url = input(f"""
{self.z}{Fore.LIGHTCYAN_EX}Please enter the video URL --->:""")
            self.download_video(url)

        elif options == "2":
            self.download_from_file()

        elif options == "3":
            self.download_channel_user()

        elif options == "4":
            self.get_metadata()

        elif options == "5":
            self.search_videos()

        elif options == "6":
            print(Fore.RESET + credits)

        elif options == "7":
            webbrowser.open("https://github.com/EchterAlsFake/Porn_Fetch/issues")

        elif options == "8":
            sys.exit(0)

    def change_quality(self):

        options = input(f"""
{Fore.LIGHTGREEN_EX}1) Change Quality to best
{Fore.LIGHTMAGENTA_EX}2) Change Quality to middle
{Fore.LIGHTRED_EX}3) Change Quality to worst
{Fore.LIGHTWHITE_EX}4) Go back
{Fore.LIGHTYELLOW_EX}----------->:{Fore.RESET}""")

        if options == "1":
            self.quality = Quality.BEST
            print(f"{self.z}✓")

        elif options == "2":
            self.quality = Quality.MIDDLE
            print(f"{self.z}✓")

        elif options == "3":
            self.quality = Quality.WORST
            print(f"{self.z}✓")

        elif options == "4":
            self.menu()

        else:
            print(f"{self.x}Wrong option. Please enter in range 1-4")
            self.change_quality()

    def set_output_path(self):
        output = input("""
Please enter the new output path.  Make sure to put a / at the end -->:""")
        self.output_path = output
        print(self.z + "✓")

    def set_threading_mode(self):
        options = input(f"""
{Fore.LIGHTMAGENTA_EX}1) Single threaded mode (downloads everything one by one)
{Fore.LIGHTCYAN_EX}2) Multiple threaded mode (downloads multiple videos at once)
{Fore.LIGHTWHITE_EX}3) Go back
{Fore.LIGHTYELLOW_EX}------------------------>:{Fore.RESET}""")

        try:
            if options == "1":
                self.threading_mode = "single"

            elif options == "2":
                self.threading_mode = "multiple"

            elif options == "3":
                    self.menu()

            else:
                print(f"{self.x}Wrong Input. Select in range 1-3")
                self.set_threading_mode()

        finally:
            clear()

    def raw_download(self, video):

        title = video.title
        print(f"{self.z}{Fore.LIGHTMAGENTA_EX}Downloading: {Fore.RESET}{title}")

        try:
            video.download(path=self.output_path, callback=self.callback, quality=self.quality)
            print(f"{self.z}{Fore.LIGHTBLUE_EX}Download finished :) ")

        except Exception as e:
            self.exception(e)

    def download_video(self, url):

        mode = self.threading_mode
        output_path = self.output_path
        time.sleep(2) # You can set it to 0 if you want.  Read further down for additional information
        self.check_video(url) # Video will be assigned in this function. You probably ask why, so here a little explanation:

        """
        The API from Egsagon is not very good optimized. Also he doesn't maintain it actively and PornHub is also a really bad
        platform for writing an API. So the API video objects are sometimes returning Index Errors, because some 
        data from PornHub is not returned as it should. The only way to get around this, is to initialize the client from 
        time to time and refresh the video object. This doesn't prevent the error, but it let's it happen less.
        If you don't want the delay, you can just remove it from the code. It won't break the program.
        In case, the API gets more stable, I will also remove it, but this is the only solution for now.
        """

        if not check_path(output_path):
            print(f"{self.x}{Fore.RESET}The Output path, you submitted is wrong. You will be redirected to change it!")
            self.set_output_path()


        else:
            video = self.video

            if mode == "single":
                self.raw_download(video)

            elif mode == "multiple":
                t = threading.Thread(target=self.raw_download, args=(video, ))
                print(f"{self.z}{Fore.RESET}Running Thread: {t.name}")
                t.start()

    def download_from_file(self):

        print(f"""
            {Fore.LIGHTCYAN_EX}INFORMATION

{Fore.LIGHTWHITE_EX}The file needs to be in the following format:

URL (After the URL, make a new line!
URL
URL etc....

Do NOT separate them with commas or anything else. Just with a new line. Should be easy enough :) 
""")

        file = input(f"""
{self.z}{Fore.LIGHTYELLOW_EX}Path to URL file -->:""")

        with open(file, "r") as url_file:
            content = url_file.read().encode("utf-8").splitlines()

            total_urls = len(content)
            valid_urls = []
            counter = 0

            print(f"{self.z}{Fore.LIGHTCYAN_EX}Found: {total_urls}")
            print(f"{self.z}{Fore.LIGHTMAGENTA_EX}Verifying URLs...")

            for url in tqdm(content):

                counter += 1
                self.check_video(url)
                valid_urls.append(url)


            print(self.z + Fore.LIGHTMAGENTA_EX + f"Downloading: {len(valid_urls)} Videos...")
            for url in valid_urls:
                self.download_video(url)

    def download_channel_user(self):

        user = input(f"""
{self.z}{Fore.LIGHTMAGENTA_EX}Please enter the URL to the User / Model / Channel Account -->:""")

        user_object = self.client.get_user(user)

        videos = user_object.videos
        url_list = []
        for video in videos:
            url_list.append(video.url)

        print(f"{self.z}{Fore.GREEN}Found: {len(url_list)} Videos.")
        x = input(f"{Fore.RESET}Hit enter to download them all or B to go back")

        if x == "B" or x == "b":
            self.menu()

        else:
            for url in url_list:
                self.download_video(url)

    def get_metadata(self):

        url = input(f"""
{self.z}{Fore.LIGHTBLUE_EX}Please enter the URL of the video:""")

        print(self.z + Fore.LIGHTMAGENTA_EX + "Getting metadata....")
        self.check_video(url)

        video = self.video
        title = video.title
        likes_up = video.like.up
        likes_down = video.like.down
        image_url = video.image_url
        tags = video.tags
        tag_list = []

        for tag in tags:
            tag_list.append(tag.name)

        author = video.author.name
        views = video.views
        date = video.date
        duration = video.duration
        hotspots = video.hotspots
        likes = f"Likes: {likes_up} | Dislikes: {likes_down}"

        print(f"""
{Fore.RESET}
Title: {title}
Rating: {likes}
Image URL: {image_url}
Tags: {str(tag_list).strip("[").strip("]")}
Author: {author}
Views: {views}
Date: {date}
Duration: {duration}
Hotspots: {hotspots}
-- END --""")

        input(f"{Fore.RESET}Hit enter to continue...")

    def search_ext_2(self, search):

        urls = []
        for count, video in enumerate(search):
            print(f"{count}) {video.title}")
            urls.append(video.url)

        downloads = input(
            Fore.RESET + "Enter the number of videos you want to download. Separate by comma e.g 1,7,12-->:")
        videos = downloads.split(",")

        for number in videos:
            base_url = "https://www.pornhub.com/"
            additional_url = urls[int(number)]
            url = base_url + additional_url
            self.download_video(url)

    def search_ext(self, search_query):

        try:
            search = self.client.search(search_query)
            return search

        except ConnectionError:
            pass  # This is an issue from PornHub and not from my Application. I can not fix it anyway

    def search_videos(self):


        search_query = input(f"""
{self.z}{Fore.RESET}Please enter your search query -->:""")

        print(self.z + Fore.LIGHTMAGENTA_EX + "Searching....")
        search = self.search_ext(search_query)

        if len(search) == 0:
            print(f"{self.x}{Fore.LIGHTWHITE_EX}You got limited by the API! Wait a few minutes or change your IP and try again")
            print(f"{self.z}{Fore.LIGHTWHITE_EX}Trying a new initialization to the Client Object...")
            self.client = Client(language="en")

            try:
                search = self.client.search(search_query)

            except ConnectionError:
                pass

            if len(search) == 0:
                print(f"{self.x}{Fore.LIGHTMAGENTA_EX}Failed.  Sorry, you need to wait or use a VPN.")
                self.menu()

            else:
                self.search_ext_2(search)

        else:
            self.search_ext_2(search)






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
        self.video = None
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.client = Client(language="en")
        self.download_thread = None
        self.mode = "single"
        self.threadpool = QThreadPool()
        self.ui.stackedWidget.setCurrentIndex(0)

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

    def do_1(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def do_2(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def do_3(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def do_4(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def get_mode(self):

        if self.ui.radio_threading_single.isChecked():
            self.mode = "single"

        elif self.ui.radio_threading_multiple.isChecked():
            self.mode = "multiple"

        else:
            self.mode = "single"

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
            ui_popup(text=f"There was an error with the URL.  Here is a detailed error: {e}  Please report it on GitHub :)")

    def start(self):

        url = self.ui.lineedit_url.text()
        video = self.test_video(url)

        if video != False:
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
        self.get_mode()
        if quality != False:

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
                    ui_popup(text=str(f"Index Error.  (Just ignore this exception.  The download should still be finished)  Exception: {e}"))

    def search_videos(self):

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

        for i in range(self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(i)
            checkState = item.checkState(0)
            if checkState == QtCore.Qt.Checked:
                video_url = item.data(0, QtCore.Qt.UserRole)
                url = "https://www.pornhub.com/" + video_url
                video = self.test_video(url)
                self.download(video)


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
        app = QApplication(sys.argv)
        widget = Widget()
        widget.show()
        sys.exit(app.exec())