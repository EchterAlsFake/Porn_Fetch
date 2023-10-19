import os.path
import getpass
import sys
import threading

from configparser import ConfigParser
from phub import Client, Quality, errors, download, display
from colorama import *
from hqporner_api import API
from src.frontend.setup import logging, setup_config_file, strip_title, check_if_video_exists
from hue_shift import return_color


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
{return_color()}1) Download Menu
{return_color()}2) Searching
{return_color()}3) Account
{return_color()}4) Metadata
{return_color()}5) Settings
{return_color()}6) Exit
{return_color()}----------------------=>:
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
{return_color()}1) Download a video
{return_color()}2) Download from file
{return_color()}3) Download videos from model / channel
{return_color()}4) Back
{return_color()}----------------------=>:
""")
        if options == "1":
            url = input(f"{return_color()}Enter video url --=>:")
            self.download_raw(url)

        elif options == "2":
            self.download_from_file()

        elif options == "3":
            self.download_from_model_channel()

        elif options == "4":
            self.main_menu()

    def searching_menu(self):
        search_query = input(f"{return_color()}Enter search query --=>:")
        search_object = self.client.search(search_query)
        videos = []
        for video in search_object[0:self.search_limit]:
            videos.append(video)

        self.iterator(videos)

    def account_menu(self):
        options = input(f"""
{return_color()}1) Login
{return_color()}2) Get liked videos
{return_color()}3) Get watched videos
{return_color()}4) Get recommended videos
{return_color()}5) Back
{return_color()}----------------------=>:
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
{return_color()}1) User metadata
{return_color()}2) Video metadata
{return_color()}3) Back
{return_color()}----------------------=>:""")

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
            logging(f"{return_color()}Invalid URL: {url}", level=1)
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

        if not check_if_video_exists(video, output_path):
            video.download(path=output_path, quality=self.quality,
                           display=display.progress(color=True), downloader=download.threaded())

    def download_raw(self, url):
        if url.endswith(".html"):
            if self.threading:
                thread = threading.Thread(target=self.download_hqporner, args=(url,))
                thread.start()

            else:
                self.download_hqporner(url)

        else:
            if self.threading:
                thread = threading.Thread(target=self.download_pornhub, args=(url,))
                thread.start()

            else:
                self.download_pornhub(url)

    def download_from_file(self):
        file = input(f"{return_color()}Please enter the file location --=>:")

        if os.path.exists(file):
            with open(file, "r") as url_file:
                content = url_file.read().splitlines()
                for url in content:
                    self.download_raw(url)

        else:
            logging(f"{return_color()}File doesn't exist...")
            self.download_from_file()

    def download_from_model_channel(self):
        model_url = input(f"{return_color()}Please enter the model url --=>:")
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

        choices_input = input(f"{return_color()}Please enter video you want to download (e.g., 1,2,5,14) -->: ")
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
        url = input(f"{return_color()}Enter video url --=>:")
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
{return_color()}Title: {title}
{return_color()}Author: {author}
{return_color()}Pornstars: 
{return_color()}Date: {date}
{return_color()}Views: {views}
{return_color()}Rating: Likes: {rating.up} | Dislikes: {rating.down}
{return_color()}Duration: {duration}
{return_color()}Categories: {categories}
{return_color()}Image URL: {image_url}
{return_color()}Tags: {tags_list}
""")

    def metadata_user(self):
        url = input(f"{return_color()}Enter user url --=>:")
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
{return_color()}Gender: {gender}
{return_color()}Height: {height}
{return_color()}Ethnicity: {ethnicity}
{return_color()}Hair color: {hair_color}
{return_color()}Fake breasts: {fake_breasts}
{return_color()}Tattoos: {tattoos}
{return_color()}Piercings: {piercings}
{return_color()}Hobbies: {hobbies}
{return_color()}Turn ons: {turns_on}
{return_color()}Video views: {video_views}
{return_color()}Profile views: {profile_views}
{return_color()}Videos watched: {videos_watched}
{return_color()}Interested in: {interested_in}
{return_color()}Relationship: {relationship}

{return_color()}Bio: {bio}

{return_color()}Avatar: {avatar.url}

""")

    def login(self):
        username = input(f"{return_color()}Enter your PornHub's Username --=>:")
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
{return_color()}------| Quality |------
    {return_color()}Current Value: {self.quality}
    
    1{return_color()}) Change to BEST
    {return_color()}2) Change to HALF
    {return_color()}3) Change to WORST

{return_color()}------| Threading |------
    {return_color()}Current Value: {self.threading}
    
    {return_color()}4) Enable
    {return_color()}5) Disable

{return_color()}------| Output path |------
    {return_color()}Current Path: {self.output_path}
    
    {return_color()}6) Change path

{return_color()}------| Search result limit |------
    {return_color()}Current Value: {self.search_limit}
    
    {return_color()}7) Change Limit

{return_color()}------| Change Delay (Speed) |-------
    {return_color()}Current Value: {self.delay}
    
    {return_color()}8) Enable Delay
    {return_color()}9) Disable Delay

{return_color()}------| Reset |------
        
    {return_color()}99) reset configuration
        
{return_color()}B) Back
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
            new_path = input(f"{return_color()}Enter new output path --=>:")
            if os.path.exists(new_path):
                self.conf.set("Porn_Fetch", "default_path", new_path)

            else:
                logging("Invalid path...", level=1)
                self.settings_menu()

        elif options == "7":
            limit = input(f"{return_color()}Enter result limit (int) -->:")
            if type(limit) == "int":
                self.conf.set("Porn_Fetch", "search_limit", limit)

            else:
                logging("Limit needs to be an integer (1,2,3 or 50 but not 30.3 or a string)")

        elif options == "8":
            self.conf.set("Porn_Fetch", "delay", "true")

        elif options == "9":
            self.conf.set("Porn_Fetch", "delay", "false")

        elif options == "99":
            confirmation = input(f"{return_color()}Are you sure? (y/n): ")
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
