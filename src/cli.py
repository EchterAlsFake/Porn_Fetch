import os.path
import random
import getpass
import threading

from phub import Client, Quality, errors
from tqdm import tqdm
from configparser import ConfigParser
from colorama import *

try:
    from src.setup import logging, setup_config_file

except ImportError:
    from setup import logging, setup_config_file


class CLI():

    def __init__(self):
        self.z = f"{Fore.LIGHTCYAN_EX}[+]"
        self.client = None
        self.quality = None
        self.hd = None
        self.sort = None
        self.sort_time = None
        self.delay = None
        self.api_language = None
        self.production = None
        self.pbar = None
        self.threading = None
        self.output_path = None
        setup_config_file()
        self.conf = ConfigParser()
        self.conf.read("config.ini")
        self.load_variables()
        while True:
            self.main_menu()

    def main_menu(self):

        options = input(f"""
{Fore.LIGHTCYAN_EX}1) Download a video
{Fore.LIGHTGREEN_EX}2) Download from a file
{Fore.LIGHTMAGENTA_EX}3) Download a channel / model / user account
{Fore.LIGHTYELLOW_EX}4) Search for videos
{Fore.LIGHTRED_EX}5) Get metadata from video
{Fore.LIGHTCYAN_EX}6) Account page
{Fore.LIGHTGREEN_EX}7) Settings
{Fore.LIGHTMAGENTA_EX}8) Exit {Fore.RESET}
-------------------------=>:""")

        if options == "1":
            url = input(f"{self.z}{Fore.LIGHTCYAN_EX}Enter the video url --=>:{Fore.RESET}")
            self.download_prerequisites(url)

        elif options == "2":
            file = input(f"{self.z}{Fore.LIGHTGREEN_EX}Enter the video file --=>:{Fore.RESET}")
            self.download_from_file(file)

        elif options == "3":
            user = input(f"{self.z}{Fore.LIGHTMAGENTA_EX}Enter the URL for User / Channel / Model account --=>:{Fore.RESET}")
            self.download_from_channel(user)

        elif options == "4":
            query = input(f"{Fore.LIGHTYELLOW_EX}Enter the search query --=>:{Fore.RESET}")
            self.search(query)

        elif options == "5":
            url = input(f"{Fore.LIGHTRED_EX}Enter the video url --=>:{Fore.RESET}")
            self.get_metadata(url)

        elif options == "6":
            self.account_page()

        elif options == "7":
            self.settings()

        elif options == "8":
            exit(0)

        else:
            logging(msg="Invalid input. Select in range 1 - 8", level="1")

    def load_variables(self):
        self.sort_time = self.conf["Porn_Fetch"]["sort_time"]
        self.sort = self.conf["Porn_Fetch"]["sort"]
        self.production = self.conf["Porn_Fetch"]["production"]
        self.output_path = self.conf["Porn_Fetch"]["default_path"]

        if self.conf["Porn_Fetch"]["default_threading"] == "yes":
            self.threading = True

        else:
            self.threading = False

        if self.conf["Porn_Fetch"]["delay"] == "true":
            self.delay = True

        else:
            self.delay = False

        if self.conf["Porn_Fetch"]["hd"] == "true":
            self.hd = True

        else:
            self.hd = False

        if self.conf["Porn_Fetch"]["default_quality"] == "best":
            self.quality = Quality.BEST

        elif self.conf["Porn_Fetch"]["default_quality"] == "half":
            self.quality = Quality.HALF

        elif self.conf["Porn_Fetch"]["default_quality"] == "worst":
            self.quality = Quality.WORST

        else:
            self.quality = Quality.BEST

    def get_video(self, url):

        self.client = Client(language=self.api_language, delay=self.delay)
        return self.client.get(url)

    def callback(self, pos, total):
        self.pbar = tqdm(total=total, dynamic_ncols=True)
        self.pbar.update(pos - self.pbar.n)
        if pos == total:
            self.pbar.close()
            self.pbar = None

    def download_prerequisites(self, url):

        video = self.get_video(url)
        if os.path.exists(self.output_path):
            logging(msg="Started download...", level="0")
            if self.threading:
                download_thread = threading.Thread(target=self.download, args=(video, ))
                download_thread.start()

            else:
                self.download(video)
        else:
            logging(
                msg="Output path does not exist. Please change it in settings and make sure I have read / write access.",
                level="1")

    def download(self, video_object, os_error_handler=None):

        try:
            if not os_error_handler:
                logging(msg=f"Starting video download for: {video_object.title}", level="0")
                video_object.download(path=self.output_path, quality=self.quality, display=self.callback)
                logging(msg="Finished :) ", level="0")

            else:
                logging(msg="Got OSError. Using different integer title.", level="1")
                random_number = random.randint(0, 1000000)
                random_number = str(f"{random_number}.mp4")
                video_object.download(path=self.output_path + random_number, quality=self.quality,
                                      callback=self.callback)

        except PermissionError:
            logging(msg=f"Permission denied for: {video_object.title}", level="1")

        except OSError:
            self.download(video_object=video_object, os_error_handler=True)

    def download_from_file(self, file_path):

        video_objects = []
        video_urls = []

        with open(file_path, "r") as file:
            content = file.read()
            lines = content.splitlines()

            for line in lines:
                video_urls.append(line)

        for url in video_urls:

            try:
                video = self.get_video(url)
                video_objects.append(video)
                logging(msg=f"Verified: {video.title}", level="0")

            except Exception as e:
                logging(msg=f"Unexpected error: {e}", level="1")

        print("""
:-----------------------VIDEOS--------------------------:



""")
        for counter, video in enumerate(video_objects, start=0):
            print(f"{counter}) {video.title}")

        picked_indexes = input(
            "Enter the numbers of video you want to download. Separate with comma.  e.g 1,2,3,4 -=>:")
        numbers = picked_indexes.split(",")

        for number in numbers:
            video = video_objects[int(number)]
            video_id = video.url
            url_string = "https://www.pornhub.com/"
            url = f"{url_string}{video_id}"
            self.download_prerequisites(url)

        logging(msg="All videos finished :)", level="0")

    def download_from_channel(self, url):

        self.client = Client(language=self.api_language, delay=self.delay)
        videos = self.client.get_user(url).videos

        for counter, video in enumerate(videos):
            print(f"{counter}) {video.title}")

        picked_indexes = input(""""


Enter the numbers of video you want to download. Separate with comma.  e.g 1,2,3,4 -=>:""")
        numbers = picked_indexes.split(",")
        for number in numbers:
            video_id = videos[int(number)].url
            self.download_prerequisites(video_id)

        logging(msg="All videos finished :)", level="0")

    def search(self, query):

        self.client = Client(language=self.api_language, delay=self.delay)
        search_results = self.client.search(query)

        for counter, video in enumerate(search_results):
            print(f"{counter}) {video.title}")

        picked_indexes = input("""
        
        

Enter the numbers of video you want to download. Separate with comma. e.g 1,2,3,4 -=>:""")

        numbers = picked_indexes.split(",")
        for number in numbers:
            video_id = search_results[int(number)].url
            self.download_prerequisites(video_id)

        logging(msg="All videos finished :)", level="0")

    def get_metadata(self, url):

        video = self.get_video(url)

        title = video.title
        rating = f"""Likes: {video.like.up} Dislikes: {video.like.down}"""
        rating = str(rating)
        views = video.views
        views = str(views)
        duration = video.duration
        duration = str(duration)
        author = video.author
        date = video.date
        date = str(date)
        hotspots = video.hotspots
        hotspots = str(hotspots)
        is_vertical = video.is_vertical

        if is_vertical:
            is_vertical = "Yes"

        else:
            is_vertical = "No"

        image_url = video.image.url
        tags = video.tags

        print(f"""
{Fore.RESET}
Title: {title}
Rating: {rating}
Views: {views}
Duration: {duration}
Author: {author}
Date: {date}
Hotspots: {hotspots}
Is vertical: {is_vertical}
Image URL: {image_url}
Tags: {tags}

-- END -- """)

    def account_page(self):
        account_menu = input(f"""
{Fore.LIGHTGREEN_EX}1) Login
{Fore.LIGHTYELLOW_EX}2) Get liked videos
{Fore.LIGHTMAGENTA_EX}3) Get watched videos
{Fore.LIGHTCYAN_EX}4) Get recommended videos
{Fore.LIGHTRED_EX}5) Back {Fore.RESET}
-------------------------=>:""")

        if account_menu == "1":
            self.login()

        elif account_menu == "2":
            self.get_liked_videos()

        elif account_menu == "3":
            self.get_watched_videos()

        elif account_menu == "4":
            self.get_recommended_videos()

        elif account_menu == "5":
            self.main_menu()

        else:
            logging(msg="Please enter a valid number in range 1 - 5 ", level="1")

    def login(self):

        username = input(f"{self.z}{Fore.LIGHTCYAN_EX}Please enter your username --=>:{Fore.RESET}")
        password = getpass.getpass("Please enter your password --=>:")

        try:
            self.client = Client(language=self.api_language, delay=self.delay, username=username, password=password)
            logging(f"Logged in as: {self.client.account.name}", level="0")

        except errors.LoginFailed:
            logging("Login Failed, check your credentials", level="0")
            self.login()

    def get_liked_videos(self):
        liked_object = self.client.account.liked
        liked_videos = liked_object.videos
        self.iterate_and_download(liked_videos)

    def get_watched_videos(self):
        watched_object = self.client.account.watched
        watched_videos = watched_object.videos
        self.iterate_and_download(watched_videos)

    def get_recommended_videos(self):
        recommended_object = self.client.account.reccomended
        recommended_videos = recommended_object.videos
        self.iterate_and_download(recommended_videos)

    def iterate_and_download(self, iterator):

        urls = []

        for counter, video in enumerate(iterator):
            print(f"{counter}) {video.title}")
            urls.append(video.url)

        selected_indexes = input(
            f"{self.z}{Fore.LIGHTCYAN_EX}Enter the numbers of video you want to download. Separate with comma e.g 1,"
            f"2,3,4 -=>:{Fore.RESET}")

        numbers = selected_indexes.split(",")
        for number in numbers:
            self.download_prerequisites(url=urls[int(number)])

    def settings(self):
        settings_main_menu = input(f"""
{Fore.LIGHTCYAN_EX}1) Change API language
{Fore.LIGHTRED_EX}2) Change delay
{Fore.LIGHTGREEN_EX}3) Change quality
{Fore.LIGHTYELLOW_EX}4) Change output path
{Fore.LIGHTMAGENTA_EX}5) Define search filters
{Fore.LIGHTBLUE_EX}6) Back {Fore.RESET}
----------------------=>:""")

        if settings_main_menu == "1":
            self.settings_api_language()

        elif settings_main_menu == "2":
            self.settings_delay()

        elif settings_main_menu == "3":
            self.settings_quality()

        elif settings_main_menu == "4":
            self.settings_output_path()

        elif settings_main_menu == "5":
            self.settings_search_filters()

        elif settings_main_menu == "6":
            self.main_menu()

        else:
            logging(msg="Please enter a valid number in range 1 - 6", level="1")

    def settings_api_language(self):

        language = input("""
Please enter the language code.
You can see the supported list down below. You can also use a custom language code, but this may 
not work. Please also note, that many videos are only in English. PornHub needs to automatically translate them!

en  : English
de  : German
es  : Spanish
ru  : Russian
fr  : French

----------------------=>:""")

        with open("config.ini", "w") as config:
            self.conf.set("Porn_Fetch", "api_language", language)
            self.conf.write(config)
            self.settings()

    def settings_delay(self):

        delay = input(f"""
The default delay is 0.5 seconds per API request. Note: If disabling the delay, you will encounter a lot of errors.
Do NOT report any errors caused with deactivated delay!

Thanks.


{Fore.LIGHTRED_EX}1) Disable delay 
{Fore.LIGHTGREEN_EX}2) Enable delay {Fore.RESET}
----------------------------=>:""")

        with open("config.ini", "w") as config:

            if delay == "1":
                self.conf.set("Porn_Fetch", "delay", "false")
                self.conf.write(config)

            elif delay == "2":
                self.conf.set("Porn_Fetch", "delay", "true")
                self.conf.write(config)

            else:
                logging(msg="Please enter a valid number.", level="1")
                self.settings_delay()

            self.settings()

    def settings_quality(self):

        quality = input(f"""
{Fore.LIGHTGREEN_EX}1) Highest quality possible
{Fore.LIGHTMAGENTA_EX}2) Medium / half quality
{Fore.LIGHTRED_EX}3) Lowest quality {Fore.RESET}
-----------------------------=>:""")

        with open("config.ini", "w") as config:

            if quality == "1":
                self.conf.set("Porn_Fetch", "default_quality", "best")
                self.conf.write(config)

            elif quality == "2":
                self.conf.set("Porn_Fetch", "default_quality", "half")
                self.conf.write(config)

            elif quality == "3":
                self.conf.set("Porn_Fetch", "default_quality", "worst")
                self.conf.write(config)

            else:
                logging(msg="Please enter a valid number.", level="1")
                self.settings_quality()

    def settings_output_path(self):

        new_output_path = input(f"""
{self.z}{Fore.LIGHTWHITE_EX}Please enter the new output path (with a / or \\ at the end!) {Fore.RESET}

-----------------=>:""")

        if not os.path.exists(new_output_path):
            logging(msg=f"The path {new_output_path} does not exist.", level="1")
            self.settings_output_path()

        else:
            with open("config.ini", "w") as config:
                self.conf.set("Porn_Fetch", "default_path", new_output_path)
                self.conf.write(config)
                self.settings()

    def settings_search_filters(self):

        options_menu = input(f"""

{Fore.LIGHTCYAN_EX}1) Change production filter
{Fore.LIGHTMAGENTA_EX}2) Change time sort filter
{Fore.LIGHTYELLOW_EX}3) Change general sort filter
{Fore.LIGHTGREEN_EX}4) Change HD filtering {Fore.RESET}
-----------------------------=>:""")

        if options_menu == "1":
            menu = input(f"""

{Fore.LIGHTCYAN_EX}1) filter for only professional videos
{Fore.LIGHTMAGENTA_EX}2) filter for only homemade videos
{Fore.LIGHTRED_EX}3) disable filter {Fore.RESET}
-----------------------------=>:""")

            with open("config.ini", "w") as config:

                if menu == "1":
                    self.conf.set("Porn_Fetch", "production", "professional")
                    self.conf.write(config)

                elif menu == "2":
                    self.conf.set("Porn_Fetch", "production", "homemade")
                    self.conf.write(config)

                elif menu == "3":
                    self.conf.set("Porn_Fetch", "production", "none")
                    self.conf.write(config)


                else:
                    logging(msg="Please enter a valid number.", level="1")

                self.settings_search_filters()

        elif options_menu == "2":
            menu = input(f"""
{Fore.LIGHTCYAN_EX}1) Filter by Day
{Fore.LIGHTMAGENTA_EX}2) Filter by Week
{Fore.LIGHTYELLOW_EX}3) Filter by Month
{Fore.LIGHTGREEN_EX}4) Filter by Year
{Fore.LIGHTBLUE_EX}5) Disable filter {Fore.RESET}
-----------------------------=>:""")

            with open("config.ini", "w") as config:

                if menu == "1":
                    self.conf.set("Porn_Fetch", "sort_time", "day")
                    self.conf.write(config)

                elif menu == "2":
                    self.conf.set("Porn_Fetch", "sort_time", "week")
                    self.conf.write(config)

                elif menu == "3":
                    self.conf.set("Porn_Fetch", "sort_time", "month")
                    self.conf.write(config)

                elif menu == "4":
                    self.conf.set("Porn_Fetch", "sort_time", "year")
                    self.conf.write(config)

                elif menu == "5":
                    self.conf.set("Porn_Fetch", "sort_time", "none")
                    self.conf.write(config)

                else:
                    logging(msg="Please enter a valid number.", level="1")

                self.settings_search_filters()

        elif options_menu == "3":
            menu = input(f"""
{Fore.LIGHTCYAN_EX}1) most recent
{Fore.LIGHTMAGENTA_EX}2) most viewed
{Fore.LIGHTYELLOW_EX}3) top rated
{Fore.LIGHTGREEN_EX}4) most relevant
{Fore.LIGHTBLUE_EX}5) longest
{Fore.LIGHTRED_EX}6) disable filter
{Fore.LIGHTWHITE_EX}7) back {Fore.RESET}
-------------------------------------=>:
""")

            with open("config.ini", "w") as config:

                if menu == "1":
                    self.conf.set("Porn_Fetch", "sort", "most recent")
                    self.conf.write(config)

                elif menu == "2":
                    self.conf.set("Porn_Fetch", "sort", "most viewed")
                    self.conf.write(config)

                elif menu == "3":
                    self.conf.set("Porn_Fetch", "sort", "top rated")
                    self.conf.write(config)

                elif menu == "4":
                    self.conf.set("Porn_Fetch", "sort", "most relevant")
                    self.conf.write(config)

                elif menu == "5":
                    self.conf.set("Porn_Fetch", "sort", "longest")
                    self.conf.write(config)

                elif menu == "6":
                    self.conf.set("Porn_Fetch", "sort", "none")
                    self.conf.write(config)

                elif menu == "7":
                    self.settings_search_filters()

                else:
                    logging(msg="Please enter a valid number.", level="1")

                self.settings_search_filters()

        elif options_menu == "4":
            menu = input(f"""
HD = High quality. If enabled, HD videos will be shown first.

{Fore.LIGHTGREEN_EX}1) Enable HD filtering
{Fore.LIGHTRED_EX}2) Disable HD filtering {Fore.RESET}
-----------------------------=>:""")

            with open("config.ini", "w") as config:

                if menu == "1":
                    self.conf.set("Porn_Fetch", "hd", "true")
                    self.conf.write(config)

                elif menu == "2":
                    self.conf.set("Porn_Fetch", "hd", "false")
                    self.conf.write(config)

                else:
                    logging(msg="Please enter a valid number.", level="1")

                self.settings_search_filters()


if __name__ == "__main__":
    CLI()

