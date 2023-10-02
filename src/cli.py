print("CLI")
import os.path
import random
import getpass
import sys
import threading
from configparser import ConfigParser

import phub.errors
from phub import Client, Quality, errors, locals
from tqdm import tqdm
from colorama import *
from hqporner_api import API

try:
    from src.setup import loggingl, setup_config_file

except ImportError:
    from setup import logging, setup_config_file


def note():
    input("""
Information:

The CLI version supports only the basic functions:

- Downloading + / from file
- Searching
- Model / User Accounts
- Metadata 
- Account
- Settings (persistent)

And that's it!

I mean if you want, you can a PR and implement that by yourself and I would really appreciate that, but I don't wanna
do this yk.


(Press ENTER)
""")


class CLI():
    def __int__(self):
        print("init")
        note()
        logging("Initialization...")
        setup_config_file()

        self.pbar = None
        self.api_language = "en"
        self.delay = False
        self.output_path = "./"
        self.quality = Quality.BEST
        self.threading = True
        self.load_user_settings()
        self.client = Client(language=self.api_language, delay=self.delay)
        self.main_menu()

    def callback(self, pos, total):
        self.pbar = tqdm(total=total, dynamic_ncols=True)
        self.pbar.update(pos - self.pbar.n)
        if pos == total:
            self.pbar.close()
            self.pbar = None

    def main_menu(self):
        options = input(f"""
1) Download Menu
2) Searching
3) Account
4) Metadata
5) Exit
----------------------=>:
""")

        if options == "1":
            self.download_menu()

        elif options == "2":
            self.searching_menu()

        elif options == "3":
            self.account_menu()

        elif options == "4":
            self.metadata_menu()

        elif options == "5":
            sys.exit(0)

    def download_menu(self):
        options = input(f"""
1) Download a video
2) Download from file
3) Download videos from model / channel
4) Back
----------------------=>:
""")


    def searching_menu(self):
        search_query = input(f"Enter search query --=>:")

    def account_menu(self):
        options = input(f"""
1) Login
2) Get likes videos
3) Get watched videos
4) Get recommended videos
5) Back
----------------------=>:
""")


    def metadata_menu(self):
        options = input(f"""
1) User metadata
2) Video metadata
3) Back
----------------------=>:""")

    def test_video(self, url):
        try:
            video_object = self.client.get(url)
            return video_object

        except phub.errors.URLError:
            logging(f"Invalid URL: {url}", level=1)
            return False

    def download_hqporner(self, url):

        if self.quality == Quality.BEST:
            quality = "highest"

        elif self.quality == Quality.HALF:
            quality = "720"

        elif self.quality == Quality.WORST:
            quality = "360"

        else:
            quality = "highest"

        API().download(url, output_path=self.output_path, quality=quality)

    def download_pornhub(self, url):

        video = self.test_video(url)
        video.download(path=self.output_path, quality=self.quality, downloader=phub.download.default,
                       display=self.callback)

    def download_raw(self, url):
        if url.endswith(".html"):
            if self.threading:
                thread = threading.Thread(target=self.download_hqporner, args=(url, ))
                thread.start()

            else:
                self.download_hqporner(url)

        else:
            if self.threading:
                thread = threading.Thread(target=self.download_pornhub, args=(url, ))
                thread.start()

            else:
                self.download_pornhub(url)

    def download_from_file(self):
        file = input(f"Please enter the file location --=>:")

        if os.path.exists(file):
            with open(file, "r") as url_file:
                content = url_file.read().splitlines()
                for url in content:
                    self.download_raw(url)

        else:
            logging("File doesn't exist...")
            self.download_from_file()

    def download_from_model_channel(self):
        model_url = input(f"Please enter the model url --=>:")
        model_object = self.client.get_user(model_url)

        videos = model_object.videos
        videos_raw = []
        titles = []

        for video in videos:
            videos_raw.append(video.url)
            titles.append(titles)

        for counter, selectable_video in titles:
            print(f"{counter}) {selectable_video}")

        choices_input = input(f"Please enter video you want to download (e.g., 1,2,5,14) -->: ")
        choices = choices_input.split(",")

        for choice in choices:
            self.download_pornhub(url=videos_raw[int(choice)])
















    def login(self):
        username = input(f"Enter your PornHub's Username --=>:")
        password = getpass.getpass("Enter your PornHub's Password: --=>:")

        try:
            self.client = Client(language=self.api_language, delay=self.delay, username=username, password=password)
            logging("Logged in successfully :)")

        except phub.errors.LoginFailed:
            logging("Login failed, probably an incorrect password. Please try again...")
            self.login()
            self.account_menu()





if __name__ == "__main__":
    CLI().__int__()