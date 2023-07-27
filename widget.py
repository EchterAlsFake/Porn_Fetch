"""
IMPORTANT INFORMATION

THIS PROJECT IS LICENSED UNDER THE LGPLv3 License
You should have received a copy of the license along with this program.

The Source code of this program can be found here: https://github.com/EchterAlsFake/Porn_Fetch

API by Egsagon: https://github.com/Egsagon/PHUB



Author: EchterAlsFake - Johannes Habel

Version: 1.5
2023
"""

import sys
import threading
import os
import argparse

from PySide6 import QtCore
from configparser import ConfigParser
from colorama import *
from tqdm import tqdm
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QTreeWidgetItem
from PySide6.QtCore import Signal, QThreadPool, QRunnable, QObject
from ui_form import Ui_Widget
from phub import Client, Quality


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


class CLI():

    def __init__(self):

        self.z = Fore.LIGHTGREEN_EX + "[+]" + Fore.RESET
        self.x = Fore.LIGHTRED_EX + "[~]" + Fore.RESET
        self.pbar = None
        self.quality = Quality.BEST
        self.output_path = "./"
        self.threading_mode = "multiple"
        self.client = Client(language="en")
        self.menu()

    def callback(self, **kwargs):
        def _update_progress(pos, total):
            if self.pbar is None:
                self.pbar = tqdm(total=total, dynamic_ncols=True)
            self.pbar.update(pos - self.pbar.n)
            if pos == total:
                self.pbar.close()
                self.pbar = None

        return _update_progress

    def check_path(self, path):
        return True if os.path.exists(path) else False

    def check_video(self, url):

        try:
            video = self.client.get(url)
            return video

        except Exception as e:
            self.exception(e)

    def exception(self, e):
        print(self.z + f"Unhandled Exception: {e}")


    def menu(self):

        if self.quality == Quality.BEST:
            quality_ext = Fore.LIGHTCYAN_EX + "Best"

        elif self.quality == Quality.MIDDLE:
            quality_ext = Fore.LIGHTMAGENTA_EX + "Middle"

        elif self.quality == Quality.WORST:
            quality_ext = Fore.LIGHTRED_EX + "Worst"

        options = input(f"""
{Fore.LIGHTYELLOW_EX}    Settings:
{Fore.LIGHTWHITE_EX}|----------------------|
{Fore.LIGHTCYAN_EX}|99) Change Quality     | {Fore.RESET}Currently set to: {quality_ext}
{Fore.LIGHTMAGENTA_EX}|98) Set output path    {Fore.RESET}| Currently set to: {self.output_path}
{Fore.LIGHTYELLOW_EX}|97) Set Threading mode | {Fore.RESET}Currently set to: {self.threading_mode}
{Fore.RESET}|----------------------|


1) Download a single Video
2) Download videos from a file
3) Download all videos from a User / Channel
4) Get metadata from Videos
5) Search for videos and download them
6) Show credits
7) Exit

""")


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
            pass

        elif options == "7":
            exit(0)









    def change_quality(self):

        options = """
1) Change Quality to best
2) Change Quality to middle
3) Change Quality to worst
4) Go back

"""

        if options == "1":
            self.quality = Quality.BEST
            print(self.z + "✓")

        elif options == "2":
            self.quality = Quality.MIDDLE
            print(self.z + "✓")

        elif options == "3":
            self.quality = Quality.WORST
            print(self.z + "✓")

        elif options == "4":
            self.menu()

        else:
            print(self.x + "Wrong option. Please enter in range 1-4")
            self.change_quality()

    def set_output_path(self):
        output = input("""
Please enter the new output path.  Make sure to put a / at the end -->:""")
        self.output_path = output
        print(self.z + "✓")

    def set_threading_mode(self):
        options = input("""
1) Single threaded mode (downloads everything one by one)
2) Multiple threaded mode (downloads multiple videos at once)
3) Go back
------------------------>:""")

        if options == "1":
            self.threading_mode = "single"

        elif options == "2":
            self.threading_mode = "multiple"


        elif options == "3":
            self.menu()

    def raw_download(self, video):

        title = video.title
        print(self.z + Fore.LIGHTMAGENTA_EX + f"Downloading: {title}")

        try:
            video.download(path=self.output_path, callback=self.callback, quality=self.quality)
            print(self.z + Fore.LIGHTBLUE_EX + "Download finished :) ")

        except Exception as e:
            self.exception(e)

    def download_video(self, url):

        mode = self.threading_mode
        output_path = self.output_path
        video = self.check_video(url)

        if self.check_path(output_path):

            if mode == "single":
                self.raw_download(video)

            elif mode == "multiple":

                t = threading.Thread(target=self.raw_download, args=(video, ))
                t.start()

    def download_from_file(self):

        print(f"""
            {Fore.LIGHTCYAN_EX}INFORMATION

{Fore.LIGHTWHITE_EX}The file needs to be in the following format:

URL (After the URL, make a new line!
URL
URL etc....

Do NOT seperate them with commas or anything else. Just with a new line. Should be easy enough :) 
""")

        file = input(f"""
{self.z}{Fore.LIGHTYELLOW_EX}Path to URL file -->:""")


        with open(file, "r") as url_file:
            content = url_file.read().encode("utf-8").splitlines()
            total_urls = len(content)

            valid_urls = []

            print(f"{self.z}{Fore.LIGHTCYAN_EX}Found: {total_urls}")
            print(self.z + Fore.LIGHTMAGENTA_EX + "Verifying URLs...")

            counter = 0

            for url in tqdm(content):

                counter += 1
                try:
                    self.check_video(url)
                    valid_urls.append(url)

                except Exception as e:
                    print(self.x + Fore.RESET + f"URL: {url} is Invalid!")

            print(self.z + Fore.LIGHTMAGENTA_EX + f"Downloading: {len(valid_urls)} Videos...")


            for url in valid_urls:
                self.download_video(url)

    def download_channel_user(self):

        user = input(f"""
{self.z}{Fore.LIGHTMAGENTA_EX}Plese enter the URL to the User / Model / Channel Account -->:""")

        user_object = self.client.get_user(user)

        videos = user_object.videos
        url_list = []
        for video in videos:
            url_list.append(video.url)

        print(self.z + Fore.GREEN + f"Found: {len(url_list)} Videos.")
        x = input(Fore.RESET + "Hit enter to download them all or B to go back")

        if x == "B" or x == "b":
            self.menu()

        else:

            for url in url_list:
                self.download_video(url)

    def get_metadata(self):

        url = input(f"""
{self.z}{Fore.LIGHTBLUE_EX}Please enter the URL of the video:""")

        video = self.check_video(url)
        print(self.z + Fore.LIGHTMAGENTA_EX + "Getting metadata....")

        title = video.title
        likes_up = video.like.up
        likes_down = video.like.down
        image_url = video.image_url
        tags = video.tags
        author = video.author
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
Tags: {tags}
Author: {author}
Views: {views}
Date: {date}
Duration: {duration}
Hotspots: {hotspots}
-- END --
""")

    def search_videos(self):

        search_query = input(f"""
{self.z}{Fore.RESET}Please enter your search query -->:""")

        print(self.z + Fore.LIGHTMAGENTA_EX + "Searching....")

        search = self.client.search(search_query)
        urls = []

        try:

            for count, video in enumerate(search):
                print(f"{count}) {video.title}")
                urls.append(video.url)

        except ConnectionError:
            print("Got a connection error.  This is more a problem with PornHub, so you can ignore that. Restarting will fix it!")

        downloads = input(Fore.RESET + "Enter the number of videos you want to download. Separate by comma e.g 1,7,12-->:")
        videos = downloads.split(",")

        for number in videos:
            base_url = "https://www.pornhub.com/"
            additional_url = urls[int(number)]
            url = base_url + additional_url

            self.client = Client()
            self.download_video(url=url)








    def show_credits(self):
        pass
    def exit(self):

        print(Fore.LIGHTCYAN_EX + "Have a nice day :)")
        exit(0)


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
        self.conf = ConfigParser()
        self.conf.read("config.ini")
        self.client = Client(language="en")
        self.download_thread = None
        self.mode = "single"
        self.threadpool = QThreadPool()


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
            print(url)
            url = url.replace("www", "de")
            print(url)
            self.video = self.client.get(url)
            return self.video

        except Exception as e:
            ui_popup(text=f"There was an error with the URL.  Here is a detailed error: {e}  Please report it on GitHub :)")

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
                    self.ui.label_search_query_progress.setText(f"Downloading: {title}")
                    debug("Downloading...")
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
    args = parser.parse_args()

    if args.cli:
        CLI()


    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())