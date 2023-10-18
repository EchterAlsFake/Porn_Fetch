import os.path
import getpass
import sys
import threading

from configparser import ConfigParser
from phub import Client, Quality, errors, download, display
from colorama import *
from hqporner_api import API
from src.frontend.setup import logging, setup_config_file, strip_title
from hue_shift import return_color

colour = return_color()


class CLI:
    def __init__(self):
        logging("Initialization...")
        setup_config_file()
        self.conf = ConfigParser()
        self.conf.read("config.ini")

        self.z = f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET}"
        self.x = f"{Fore.LIGHTRED_EX}[~]{Fore.RESET}"
        self.pbar = None
        self.api_language = "en"
        self.delay = False
        self.output_path = "./"
        self.quality = Quality.BEST
        self.threading = True
        self.search_limit = 50
        self.load_user_settings()
        self.client = Client(language=self.api_language, delay=self.delay)
        while True:
            self.main_menu()

    def main_menu(self):
        options = input(f"""
{colour}1) Download Menu
{colour}2) Searching
{colour}3) Account
{colour}4) Metadata
{colour}5) Settings
{colour}6) Exit
{colour}----------------------=>:
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
            self.settings_menu()

        elif options == "6":
            sys.exit(0)

    def download_menu(self):
        options = input(f"""
{colour}1) Download a video
{colour}2) Download from file
{colour}3) Download videos from model / channel
{colour}4) Back
{colour}----------------------=>:
""")
        if options == "1":
            url = input(f"{colour}Enter video url --=>:")
            self.download_raw(url)

        elif options == "2":
            self.download_from_file()

        elif options == "3":
            self.download_from_model_channel()

        elif options == "4":
            self.main_menu()

    def searching_menu(self):
        search_query = input(f"{colour}Enter search query --=>:")
        search_object = self.client.search(search_query)
        videos = []
        for video in search_object[0:self.search_limit]:
            videos.append(video)

        self.iterator(videos)

    def account_menu(self):
        options = input(f"""
{colour}1) Login
{colour}2) Get liked videos
{colour}3) Get watched videos
{colour}4) Get recommended videos
{colour}5) Back
{colour}----------------------=>:
""")

        if options == "1":
            self.login()

        elif options == "2":
            self.get_liked_videos()

        elif options == "3":
            self.get_watched_videos()

        elif options == "4":
            self.get_recommended_videos()

        elif options == "5":
            self.main_menu()

    def metadata_menu(self):
        options = input(f"""
{colour}1) User metadata
{colour}2) Video metadata
{colour}3) Back
{colour}----------------------=>:""")

        if options == "1":
            self.metadata_user()

        elif options == "2":
            self.metadata_video()

        elif options == "3":
            self.main_menu()

    def test_video(self, url):
        try:
            video_object = self.client.get(url)
            return video_object

        except errors.URLError:
            logging(f"{colour}Invalid URL: {url}", level=1)
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
        title = video.title
        logging("Stripping title")
        title = strip_title(title)
        output_path = self.output_path + title + ".mp4"
        video.download(path=output_path, quality=self.quality, downloader=download.default,
                       display=display.progress(color=True))

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
        file = input(f"{colour}Please enter the file location --=>:")

        if os.path.exists(file):
            with open(file, "r") as url_file:
                content = url_file.read().splitlines()
                for url in content:
                    self.download_raw(url)

        else:
            logging(f"{colour}File doesn't exist...")
            self.download_from_file()

    def download_from_model_channel(self):
        model_url = input(f"{colour}Please enter the model url --=>:")
        model_object = self.client.get_user(model_url)

        videos = model_object.videos
        self.iterator(videos)

    def iterator(self, iterator_object):
        """
        Iterator object must be a list of video objects
        """
        logging("Starting iteration...")
        videos_raw = []
        titles = []

        for video in iterator_object:
            logging(video)
            videos_raw.append(video.url)
            titles.append(titles)

        for counter, selectable_video in enumerate(titles):
            logging(counter)
            print(f"{counter}) {selectable_video}")

        choices_input = input(f"{colour}Please enter video you want to download (e.g., 1,2,5,14) -->: ")
        choices = choices_input.split(",")

        for choice in choices:
            self.download_raw(url=videos_raw[int(choice)])

    def get_liked_videos(self):
        videos = self.client.account.liked
        logging("Got video object")
        self.iterator(videos)

    def get_watched_videos(self):
        videos = self.client.account.watched
        self.iterator(videos)

    def get_recommended_videos(self):
        videos = self.client.account.recommended
        self.iterator(videos)

    def metadata_video(self):
        url = input(f"{colour}Enter video url --=>:")
        video_object = self.test_video(url)

        tags_list = []

        tags = video_object.tags
        title = video_object.title
        image_url = video_object.image.url
        date = video_object.date
        views = video_object.views
        rating = video_object.like
        duration = video_object.duration
        author = video_object.author
        categories = video_object.categories

        for tag in tags:
            tags_list.append(tag.name)

        print(f"""
{colour}Title: {title}
{colour}Author: {author}
{colour}Pornstars: 
{colour}Date: {date}
{colour}Views: {views}
{colour}Rating: Likes: {rating.up} | Dislikes: {rating.down}
{colour}Duration: {duration}
{colour}Categories: {categories}
{colour}Image URL: {image_url}
{colour}Tags: {tags_list}
""")

    def metadata_user(self):
        url = input(f"{colour}Enter user url --=>:")
        user_object = self.client.get_user(url)
        info = user_object.info
        bio = user_object.bio
        avatar = user_object.avatar

        relationship = info.get("Relationship status")
        interested_in = info.get("Interested in")
        gender = info.get("Gender")
        height = info.get("Height")
        ethnicity = info.get("Ethnicity")
        hair_color = info.get("Hair Color")
        fake_breasts = info.get("Fake Boobs")
        tattoos = info.get("Tattoos")
        piercings = info.get("Piercings")
        hobbies = info.get("Interests and hobbie")
        turns_on = info.get("Turn Ons")
        video_views = info.get("Video Views")
        profile_views = info.get("Profile Views")
        videos_watched = info.get("Videos Watched")

        print(f"""
{colour}Gender: {gender}
{colour}Height: {height}
{colour}Ethnicity: {ethnicity}
{colour}Hair color: {hair_color}
{colour}Fake breasts: {fake_breasts}
{colour}Tattoos: {tattoos}
{colour}Piercings: {piercings}
{colour}Hobbies: {hobbies}
{colour}Turn ons: {turns_on}
{colour}Video views: {video_views}
{colour}Profile views: {profile_views}
{colour}Videos watched: {videos_watched}
{colour}Interested in: {interested_in}
{colour}Relationship: {relationship}

{colour}Bio: {bio}

{colour}Avatar: {avatar}

""")

    def login(self):
        username = input(f"{colour}Enter your PornHub's Username --=>:")
        password = getpass.getpass("Enter your PornHub's Password: --=>:")

        try:
            self.client = Client(language=self.api_language, delay=self.delay, username=username, password=password)
            logging("Logged in successfully :)")
            self.account_menu()

        except errors.LoginFailed:
            logging("Login failed, probably an incorrect password. Please try again...")
            self.login()

    def settings_menu(self):
        options = input(f"""
{colour}------| Quality |------
    {colour}Current Value: {self.quality}
    
    1{colour}) Change to BEST
    {colour}2) Change to HALF
    {colour}3) Change to WORST

{colour}------| Threading |------
    {colour}Current Value: {self.threading}
    
    {colour}4) Enable
    {colour}5) Disable

{colour}------| Output path |------
    {colour}Current Path: {self.output_path}
    
    {colour}6) Change path

{colour}------| Search result limit |------
    {colour}Current Value: {self.search_limit}
    
    {colour}7) Change Limit

{colour}------| Change Delay (Speed) |-------
    {colour}Current Value: {self.delay}
    
    {colour}8) Enable Delay
    {colour}9) Disable Delay

{colour}------| Reset |------
        
    {colour}99) reset configuration
        
{colour}B) Back
""")

        if options == "1":
            self.conf.set("Porn_Fetch", "default_quality", "best")

        elif options == "2":
            self.conf.set("Porn_Fetch", "default_quality", "half")

        elif options == "3":
            self.conf.set("Porn_Fetch", "default_quality", "worst")

        elif options == "4":
            self.conf.set("Porn_Fetch", "default_threading", "yes")

        elif options == "5":
            self.conf.set("Porn_Fetch", "default_threading", "no")

        elif options == "6":
            new_path = input(f"{colour}Enter new output path --=>:")
            if os.path.exists(new_path):
                self.conf.set("Porn_Fetch", "default_path", new_path)

            else:
                logging("Invalid path...", level=1)
                self.settings_menu()

        elif options == "7":
            limit = input(f"{colour}Enter result limit (int) -->:")
            if type(limit) == "int":
                self.conf.set("Porn_Fetch", "search_limit", limit)

            else:
                logging("Limit needs to be an integer (1,2,3 or 50 but not 30.3 or a string)")

        elif options == "8":
            self.conf.set("Porn_Fetch", "delay", "true")

        elif options == "9":
            self.conf.set("Porn_Fetch", "delay", "false")

        elif options == "99":
            confirmation = input(f"{colour}Are you sure? (y/n): ")
            if confirmation == "y":
                setup_config_file(force=True)

        elif options == "B":
            self.main_menu()

        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)
            logging("Applied new configuration, please restart!")

    def load_user_settings(self):
        self.output_path = self.conf["Porn_Fetch"]["default_path"]
        self.search_limit = int(self.conf["Porn_Fetch"]["search_limit"])

        if self.conf["Porn_Fetch"]["default_threading"] == "yes":
            self.threading = True

        elif self.conf["Porn_Fetch"]["default_threading"] == "no":
            self.threading = False

        if self.conf["Porn_Fetch"]["delay"] == "true":
            self.delay = True

        elif self.conf["Porn_Fetch"]["delay"] == "false":
            self.delay = False

        if self.conf["Porn_Fetch"]["default_quality"] == "best":
            self.quality = Quality.BEST

        elif self.conf["Porn_Fetch"]["default_quality"] == "half":
            self.quality = Quality.HALF

        elif self.conf["Porn_Fetch"]["default_quality"] == "worst":
            self.quality = Quality.WORST


if __name__ == "__main__":
    try:
        CLI()

    except errors.URLError:
        logging("Invalid URL", level=1)

    except errors.UserNotFound:
        logging("User not found", level=1)

    except errors.MaxRetriesExceeded:
        logging("Max retries exceeded", level=1)