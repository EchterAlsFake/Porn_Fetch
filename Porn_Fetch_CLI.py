"""
Porn Fetch CLI
Licensed under GPL 3
Copyright (C) 2023-2024 Johannes Habel (EchterAlsFake)

Version 3.0
"""
import getpass
import os.path
import re
import threading

from tqdm import tqdm
from hqporner_api.api import Client as hq_Client, Video as hq_Video, Quality as hq_Quality
from hqporner_api.modules.locals import *
from xnxx_api.xnxx_api import Client as xn_Client, Video as xn_Video
from eporner_api.eporner_api import Client as ep_Client, Video as ep_Video
from xvideos_api.xvideos_api import Client as xv_Client, Video as xv_Video
from threading import Semaphore
from rich import print as rprint
from rich.markdown import Markdown
from configparser import ConfigParser
from phub import Video, Client, errors, download, Quality

from src.backend.shared_functions import (strip_title, check_video, setup_config_file,
                                          logger_debug, logger_error, return_color, reset, correct_output_path)


class CLI:
    def __init__(self):
        setup_config_file()
        self.conf = ConfigParser()
        self.conf.read("config.ini")

        # Variable initialization
        self.semaphore_limit = None
        self.client = None
        self.directory_system = None
        self.threading = None
        self.threading_mode = None
        self.search_limit = None
        self.output_path = None
        self.api_language = None
        self.quality = None
        self.progress_bars = {}
        self.load_user_settings()

        if self.license():
            while True:
                self.main_menu()

    def license(self):
        license_accept = self.conf["License"]["accepted"]

        if license_accept != "true":
            license_text = """
GPL License Agreement for Porn Fetch
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
NO LIABILITY FOR END USER USE

Under no circumstances and under no legal theory, whether in tort, contract, or otherwise, shall the copyright holder or contributors be liable to You for any direct, indirect, special, incidental, consequential or exemplary damages of any character including, without limitation, damages for loss of goodwill, work stoppage, computer failure or malfunction, loss of data or any and all other commercial damages or losses, even if such party shall have been informed of the possibility of such damages.
This limitation of liability shall not apply to liability for death or personal injury resulting from such party’s negligence to the extent applicable law prohibits such limitation. Some jurisdictions do not allow the exclusion or limitation of incidental or consequential damages, so this exclusion and limitation may not apply to You.
This Agreement represents the complete agreement concerning the subject matter hereof.
"""

            x = input(f"""
{license_text}


Do you accept the License? [yes,no]""")

            if x.lower() == "yes":
                self.conf.set("License", "accepted", "true")
                with open("config.ini", "w") as config_file:
                    self.conf.write(config_file)
                    return True

            else:
                exit()

        else:
            return True

    def main_menu(self):
        options = input(f"""
{return_color()}1) Download a Video
{return_color()}2) Download videos from a Model / Channel / User
{return_color()}3) Search Users / Models / Channels
{return_color()}4) Download from a file with URLs
{return_color()}5) PornHub Account
{return_color()}6) HQPorner
{return_color()}7) Settings
{return_color()}8) Credits / Information
{return_color()}9) Exit

{return_color()}-------------------------------=>:{reset()}""")

        if options == "1":
            self.start_single_video()

        elif options == "2":
            self.start_model_user_channel()

        elif options == "3":
            self.search_options()

        elif options == "4":
            self.start_from_file()

        elif options == "5":
            self.account_options()

        elif options == "6":
            self.hqporner_options()

        elif options == "7":
            self.save_user_settings()

        elif options == "8":
            self.credits()

        elif options == "9":
            exit()

    def hqporner_options(self):
        options = input(f"""
1) Get Brazzers Videos
2) Get videos by category
3) Get videos by ranking (top)
4) Back
-------------->:""")

        if options == "1":
            self.download_brazzers_videos()

        elif options == "2":
            self.get_by_category()

        elif options == "3":
            self.download_top_porn()

        elif options == "4":
            self.main_menu()

        else:
            self.hqporner_options()

    def download_brazzers_videos(self):
        pages = input(f"How many pages do you want to iterate through? One page contains 46 videos -->:")
        videos = hq_Client().get_brazzers_videos(int(pages))
        self.start_generator(videos)

    def download_top_porn(self):
        sorting = input(f"""
Sorting:

1) Sort by top week
2) Sort by top month
3) Sort by all time
-------->:""")
        pages = input(f"How many pages do you want to iterate through? One page contains 46 videos -->:")

        if sorting == "1":
            sort = Sort.WEEK

        elif sorting == "2":
            sort = Sort.MONTH

        elif sorting == "3":
            sort = Sort.ALL_TIME

        else:
            print("Wrong input. Please enter in range 1 - 3")
            self.download_top_porn()

        videos = hq_Client().get_top_porn(pages=int(pages), sort_by=sort)
        self.start_generator(videos)

    def get_by_category(self):
        pages = input(f"How many pages do you want to iterate through? One page contains 46 videos -->:")
        category = input(f"Please enter the category name. Press C to get all categories -->:")

        if category.lower() == "c":
            categories = ",".join(hq_Client().get_all_categories())
            print(categories)

        elif not category.lower() == "c":
            videos = hq_Client().get_videos_by_category(pages=int(pages), category=category)
            self.start_generator(videos)

    def start_single_video(self):
        url = input(f"{return_color()}Enter PornHub / HQPorner URL --=>:{reset()}")
        self.pre_setup_video(url)

    def start_model_user_channel(self):
        url = input(f"""{reset()}
Please enter the URL to the PornHub User / Model / Channel account.
Or enter the name of an HQPorner actress e.g anissa-kate

Hint: You can select the videos to be downloaded later!

{return_color()}----------------------------=>:{reset()}""")

        actress_pattern = re.compile(r"https://hqporner.com/actress/(.+)")
        match = actress_pattern.match(url)

        if match:
            actress_id = match.group(1)
            video = hq_Client().get_videos_by_actress(actress_id)

        else:
            client = Client(language=self.api_language)
            model = client.get_user(url)
            video = model.videos

        self.start_generator(video)

    def start_from_file(self):
        file = input(f"""{reset()}
Enter the (exact) location of the file.

Hint: URLs from either PornHub or HQPorner need to be separated with new lines!

{return_color()}---------------------------------=>:{reset()}""")

        if os.path.exists(file):
            with open(file, "r") as url_file:
                content = url_file.read().splitlines()
                for url in content:
                    self.pre_setup_video(url)

        else:
            logger_error("File doesn't exist! Please try again.")
            self.start_from_file()

    def pre_setup_video(self, video):
        self.semaphore.acquire()
        language = self.api_language
        quality = self.quality
        if isinstance(video, str):
            video = check_video(language=language, url=video)

        if isinstance(video, hq_Video):
            title = video.title
            author = video.pornstars[0]

        elif isinstance(video, Video):
            title = video.title
            author = video.author.name

        else:
            title = video.title
            author = video.author

        title = strip_title(title)
        output_path = self.output_path
        if not output_path.endswith(os.sep):
            output_path = f"{output_path}{os.sep}"

        if self.directory_system:
            if not os.path.exists(f"{output_path}{author}"):
                os.mkdir(f"{output_path}{author}")

            output_path = f"{output_path}{author}{os.sep}{title}"

        else:
            output_path = f"{output_path}{title}"

        if not output_path.endswith(".mp4"):
            output_path += ".mp4"

        if not os.path.exists(output_path):
            if isinstance(video, hq_Video):
                hqporner_thread = threading.Thread(target=self.download_video_hqporner, args=(video, output_path, quality))
                hqporner_thread.start()

            elif isinstance(video, Video):
                pornhub_thread = threading.Thread(target=self.download_video_pornhub,
                                                  args=(video, output_path, quality))
                pornhub_thread.start()

            elif isinstance(video, xn_Video):
                xn_thread = threading.Thread(target=self.download_video_xnxx, args=(video, output_path, quality))
                xn_thread.start()

            elif isinstance(video, ep_Video):
                ep_thread = threading.Thread(target=self.download_video_eporner, args=(video, output_path, quality))
                ep_thread.start()
            
            elif isinstance(video, xv_Video):
                xv_thread = threading.Thread(target=self.download_video_xvideos, args=(video, output_path, quality))
                xv_thread.start()

    def download_callback(self, pos, total):
        """
        Callback function for the video download progress.
        It updates or creates a tqdm progress bar for each download and updates the total progress.
        """
        # Get the thread ID to uniquely identify each download
        thread_id = threading.get_ident()

        # If this is the first time this thread calls the callback, create a new progress bar
        if thread_id not in self.progress_bars:
            self.progress_bars[thread_id] = tqdm(total=total, desc=f"Download {thread_id}",
                                                 bar_format="{l_bar}{bar:20}{r_bar}{bar:-20b}",
                                                 colour='blue')

        # Update the individual progress bar
        self.progress_bars[thread_id].n = pos
        self.progress_bars[thread_id].refresh()

    def download_video_pornhub(self, video, output_path, quality):

        if self.threading_mode == "threaded":
            threading_X = download.threaded()

        elif self.threading_mode == "FFMPEG":
            threading_X = download.FFMPEG

        elif self.threading_mode == "default":
            threading_X = download.default

        video.download(downloader=threading_X, quality=quality, path=output_path, display=self.download_callback)
        logger_debug("Download Complete, releasing semaphore")
        self.semaphore.release()

    def download_video_xvideos(self, video, output_path, quality):
        logger_debug("Starting XVideos Download!")
        video.download(output_path=output_path, quality=quality, callback=self.download_callback, downloader=self.threading_mode)
        logger_debug("Download Complete, releasing semaphore")
        self.semaphore.release()

    def download_video_hqporner(self, video, output_path, quality):
        logger_debug("Starting HQPorner Download!")
        video.download(no_title=True, output_path=output_path, quality=quality, callback=self.download_callback)
        logger_debug("Download Complete, releasing semaphore")
        self.semaphore.release()

    def download_video_xnxx(self, video, output_path, quality):
        logger_debug("Starting XNXX Download!")
        video.download(output_path=output_path, quality=quality, callback=self.download_callback, downloader=self.threading_mode)
        logger_debug("Download Complete!, releasing semaphore")
        self.semaphore.release()

    def download_video_eporner(self, video, output_path, quality):
        logger_debug("Starting EPorner Download!")
        video.download_video(output_path=output_path, quality=quality, callback=self.download_callback)
        logger_debug("Download Complete!, releasing semaphore")
        self.semaphore.release()

    def load_user_settings(self):
        self.api_language = self.conf["Video"]["language"]
        self.output_path = self.conf["Video"]["output_path"]
        self.search_limit = int(self.conf["Video"]["search_limit"])
        self.threading_mode = self.conf["Performance"]["threading_mode"]
        self.directory_system = self.conf["Video"]["directory_system"]
        self.semaphore_limit = int(self.conf["Performance"]["semaphore"])
        self.semaphore = Semaphore(self.semaphore_limit)
        self.quality = self.conf["Video"]["quality"]

        if self.directory_system == "1":
            self.directory_system = True

    def save_user_settings(self):
        while True:
            if self.directory_system == "1":
                directory_system_ext = "Yes"

            elif self.directory_system == "0":
                directory_system_ext = "No"

            options = input(f"""
{reset()}--------------{return_color()}QUALITY{reset()}-------------|
{return_color()}|>  Current: {self.quality}
{return_color()}|>  1) Best
{return_color()}|>  2) Half
{return_color()}|>  3) Worst
{reset()}|-------------{return_color()}Threading{reset()}-----------|
{return_color()}|>  Current: {self.threading_mode}
{return_color()}|>  4) High Performance
{return_color()}|>  5) FFMPEG (needs ffmpeg installed on your system)
{return_color()}|>  6) Default
{return_color()}|>  7) Change Semaphore Limit (Current: {self.semaphore_limit})
{reset()}|--------------{return_color()}API Language{reset()}--------|
{return_color()}|>  Current: {self.api_language}
{return_color()}|>  8) English
{return_color()}|>  9) German
{return_color()}|>  10) French
{return_color()}|>  11) Chinese
{return_color()}|>  12) Russian
{return_color()}|>  13) Dutch
{return_color()}|>  14) Spanish
{return_color()}|>  15) Italian
{return_color()}|>  16) Portuguese
{return_color()}|>  17) Czech
{return_color()}|>  18) Japanese
{reset()}|--------------{return_color()}Output Path{reset()}----------|
{return_color()}|>  Current: {self.output_path}
{return_color()}|>  19) Change Output Path
{reset()}|--------------{return_color()}Directory System{reset()}-----|
{return_color()}|>  Current: {directory_system_ext}
{return_color()}|>  20) Enable
{return_color()}|>  21) Disable
{return_color()}|---------{return_color()}PRESS 99 TO STOP{reset()}----------|
{return_color()}|--------------------------=>:{reset()}""")
            if options == "1":
                self.conf.set("Video", "quality", "best")

            elif options == "2":
                self.conf.set("Video", "quality", "half")

            elif options == "3":
                self.conf.set("Video", "quality", "worst")

            elif options == "4":
                self.conf.set("Performance", "threading_mode", "threaded")

            elif options == "5":
                self.conf.set("Performance", "threading_mode", "FFMPEG")

            elif options == "6":
                self.conf.set("Performance", "threading_mode", "default")

            elif options == "7":
                limit = input(f"{return_color()}Enter the new Semaphore Limit between 1-6 -->:{reset()}")
                self.conf.set("Performance", "semaphore", options)

            elif options == "8":
                self.conf.set("Video", "language", "en")

            elif options == "9":
                self.conf.set("Video", "language", "de")

            elif options == "10":
                self.conf.set("Video", "language", "fr")

            elif options == "11":
                self.conf.set("Video", "language", "zh")

            elif options == "12":
                self.conf.set("Video", "language", "rt")

            elif options == "13":
                self.conf.set("Video", "language", "nl")

            elif options == "14":
                self.conf.set("Video", "language", "es")

            elif options == "15":
                self.conf.set("Video", "language", "it")

            elif options == "16":
                self.conf.set("Video", "language", "pt")

            elif options == "17":
                self.conf.set("Video", "language", "cz")

            elif options == "18":
                self.conf.set("Video", "language", "jp")

            elif options == "19":
                output_path = input(f"""
{return_color()}Please enter the new output path -->:{reset()}""")
                if not os.path.exists(output_path):
                    logger_error("The specified output path doesn't exist!")

                else:
                    output_path = correct_output_path(output_path)

                self.conf.set("Video", "output_path", output_path)

            elif options == "20":
                self.conf.set("Video", "directory_system", "1")

            elif options == "21":
                self.conf.set("Video", "directory_system", "0")

            elif options == "99":
                self.main_menu()

            with open("config.ini", "w") as config_file:
                self.conf.write(config_file)

            logger_debug("Applied new settings!")
            self.load_user_settings()
            logger_debug("Reloaded User settings. You may continue now :) ")

    def get_metadat_options(self):
        options = input(f"""
{return_color()}1) Get Video metadata
{return_color()}2) Get User metadata
{return_color()}3) Back
{return_color()}------------------=>:{reset()}""")
        if options == "1":
            self.get_video_metadata()

        elif options == "2":
            self.get_user_metadata()

        elif options == "3":
            self.main_menu()

    def search_options(self):
        options = input(f"""
{return_color()}1) Search for Videos (PornHub, HQPorner)
{return_color()}2) Search for Users  (PornHub)
{return_color()}3) Back

{return_color()}------------------=>:{reset()}""")

        if options == "1":
            self.search_videos()

        elif options == "2":
            self.search_users()

        elif options == "3":
            self.main_menu()

    def search_videos(self):
        query = input(f"""
{return_color()}Please enter your search query ---=>:{reset()}""")
        platform = input(f"""
{return_color()}Please enter your platform: [1]: PornHub, [2]: HQPorner""")

        if platform == "1":
            if not isinstance(self.client, Client):
                language = self.api_language
                self.client = Client(language=language)

            generator = self.client.search(query)

        elif platform == "2":
            generator = hq_Client.search_videos(query, pages=2)

        else:
            logger_debug("Wrong Platform. Choose between 1-2")

        self.start_generator(generator)

    def search_users(self):
        query = input(f"""
{return_color()}Enter a query to search for users --=>:{reset()}""")

        if not isinstance(self.client, Client):
            language = self.api_language
            self.client = Client(language=language)

        generator = self.client.search_user(query)
        for user in generator:
            print(user.name)

    def start_generator(self, generator):
        video_objects = []

        for idx, video in enumerate(generator):
            try:
                print(f"{idx}) {video.title}")

            except AttributeError:
                print(f"{idx}) {video.video_title}")

            video_objects.append(video)

        index = input(f"""{reset()}
Please enter the number for the videos you want to download. Separate with a comma
e.g 1,6,92 

! Enter 'ALL' to download all videos
{return_color()}-----------------------=>:{reset()}""")

        if index.lower() == "all":
            for video in video_objects:
                self.pre_setup_video(video)

        else:
            chosen_videos = index.split(",")
            for idx in chosen_videos:
                video = video_objects[int(idx)]
                self.pre_setup_video(video)

    def get_video_metadata(self):
        language = self.api_language
        url = input(f"""
{return_color()}Please enter the video url (PornHub) --=>:{reset()}""")

        video = check_video(url, language=language)

        author = video.author.name
        duration = video.duration.seconds
        duration = duration / 60
        duration = round(duration, 2)
        title = strip_title(video.title)
        date = video.date
        views = video.views
        pornstar_list = [pornstar.name for pornstar in video.pornstars]
        hotspots_list = [str(hotspots) for hotspots in video.hotspots]

        tags_list = [tag.name for tag in video.tags]
        tags = ", ".join(tags_list)
        hotspots = ", ".join(hotspots_list)
        pornstars = "".join(pornstar_list)
        rating = f"Likes: {video.likes.up} | Dislikes: {video.likes.down}"

        input(f"""
{return_color()}Title: {title}
{return_color()}Author: {author}
{return_color()}Duration: {duration} min
{return_color()}Date: {date}
{return_color()}Views: {views}
{return_color()}Pornstars: {pornstars}
{return_color()}Rating: {rating}
{return_color()}Tags: {tags}
{return_color()}Hotspots: {hotspots}
{reset()}
Press ENTER to continue""")
        self.main_menu()

    def get_user_metadata(self):
        api_language = self.api_language
        url = input(f"""
{return_color()}Enter the User URL (PornHub) --=>:{reset()}""")

        if not isinstance(self.client, Client):
            self.client = Client(language=api_language)

        user = self.client.get_user(url)
        info = user.info
        name = user.name
        type = user.type

        relationship_status = "Relationship status"
        interested_in = info.get("Interested in")
        city_and_country = info.get("City and Country")
        gender = info.get("Gender")
        birth_place = info.get("Birth Place")
        height = info.get("Height")
        weight = info.get("Weight")
        ethnicity = info.get("Ethnicity")
        hair_color = info.get("Hair Color")
        fake_boobs = info.get("Fake Boobs")
        tattoos = info.get("Tattoos")
        piercings = info.get("Piercings")
        hometown = info.get("Hometown")
        interests_and_hobbies = info.get("Interests and hobbie")
        turn_ons = info.get("Turn Ons")
        turn_offs = info.get("Turn Offs")
        video_views = info.get("Video Views")
        profile_views = info.get("Profile Views")
        videos_watched = info.get("Videos Watched")

        input(f"""
{return_color()}Name: {reset()}{name}
{return_color()}Type: {reset()}{type}

{return_color()}Relationship Status: {reset()}{relationship_status}
{return_color()}Interested In: {reset()}{interested_in}
{return_color()}City and Country: {reset()}{city_and_country}
{return_color()}Gender: {reset()}{gender}
{return_color()}Birth Place: {reset()}{birth_place}
{return_color()}Height: {reset()}{height}
{return_color()}Weight: {reset()}{weight}
{return_color()}Ethnicity: {reset()}{ethnicity}
{return_color()}Hair Color: {reset()}{hair_color}
{return_color()}Fake Boobs: {reset()}{fake_boobs}
{return_color()}Tattoos: {reset()}{tattoos}
{return_color()}Piercings: {reset()}{piercings}
{return_color()}Hometown: {reset()}{hometown}
{return_color()}Interests and Hobbies: {reset()}{interests_and_hobbies}
{return_color()}Turn Ons: {reset()}{turn_ons}
{return_color()}Turn Offs: {reset()}{turn_offs}
{return_color()}Video Views: {reset()}{video_views}
{return_color()}Profile views: {reset()}{profile_views}
{return_color()}Videos Watched: {reset()}{videos_watched}

Press ENTER to continue...""")
        self.main_menu()

    def account_options(self):
        options = input(f"""
{return_color()}1) Login
{return_color()}2) Get watched videos
{return_color()}3) Get liked videos
{return_color()}4) Get recommended videos
{return_color()}5) Back
{return_color()}---------------------------=>:{reset()}
""")

        if options == "1":
            self.login()
            self.account_options()

        elif options == "2":
            self.get_watched_videos()
            self.account_options()

        elif options == "3":
            self.get_liked_videos()
            self.account_options()

        elif options == "4":
            self.get_recommended_videos()
            self.account_options()

        elif options == "5":
            self.main_menu()
            self.account_options()

        else:
            self.account_options()

    def login(self):
        username = input(f"{return_color()}Please enter your PornHub Username --=>:{reset()}")
        password = getpass.getpass("Please enter your PornHub Password --=>:")
        self.client = Client(username=username, password=password, language=self.api_language)
        return True

    def check_login(self):
        if not self.client.logged:
            self.login()

        else:
            return True

    def get_watched_videos(self):
        self.check_login()
        iterator = self.client.account.watched
        self.start_generator(iterator)

    def get_liked_videos(self):
        self.check_login()
        iterator = self.client.account.liked
        self.start_generator(iterator)

    def get_recommended_videos(self):
        self.check_login()
        iterator = self.client.account.recommended
        self.start_generator(iterator)

    def credits(self):
        text_markdown = f"""
# Porn Fetch V3

Copyright (C) 2023-2024 Johannes Habel (EchterAlsFake)


### This Project is only possible thanks to Egsagon's [PHUB](https://github.com/EchterAlsFake/PHUB) API

## Please check out his project and give it a star!

# Development

- Language: [Python](https://www.python.org/)
- IDE: Jetbrains [PyCharm Professional](https://www.jetbrains.com/pycharm/)
- Platform: [GitHub](https://github.com)
- Graphical User Interface: [PySide6](https://doc.qt.io/qtforpython-6/)
- Framework: [Qt](https://qt.io)


# Graphics

- <a href="https://iconscout.com/icons/list" class="text-underline font-size-sm" target="_blank">List</a> by <a href="https://iconscout.com/contributors/iyikon" class="text-underline font-size-sm" target="_blank">Iyikon ...</a>
- <a href="https://iconscout.com/icons/information" class="text-underline font-size-sm" target="_blank">Information</a> by <a href="https://iconscout.com/contributors/petai-jantrapoon" class="text-underline font-size-sm">Petai Jantrapoon</a> on <a href="https://iconscout.com" class="text-underline font-size-sm">IconScout</a>
- <a href="https://iconscout.com/icons/unread" class="text-underline font-size-sm" target="_blank">unread</a> by <a href="https://iconscout.com/contributors/bharat-icons" class="text-underline font-size-sm">Bharat Design</a> on <a href="https://iconscout.com" class="text-underline font-size-sm">IconScout</a>
- <a href="https://iconscout.com/icons/top-arrow" class="text-underline font-size-sm" target="_blank">Top Arrow</a> by <a href="https://iconscout.com/contributors/creative-studio" class="text-underline font-size-sm" target="_blank">Mian Saab</a>
- <a href="https://iconscout.com/icons/down-arrow" class="text-underline font-size-sm" target="_blank">Down Arrow</a> by <a href="https://iconscout.com/contributors/adamicons" class="text-underline font-size-sm">Adam Dicons</a> on <a href="https://iconscout.com" class="text-underline font-size-sm">IconScout</a>
- <a href="https://iconscout.com/icons/tick" class="text-underline font-size-sm" target="_blank">Tick</a> by <a href="https://iconscout.com/contributors/kolo-design" class="text-underline font-size-sm" target="_blank">Kalash</a>
- <a href="https://iconscout.com/icons/account" class="text-underline font-size-sm" target="_blank">account</a> by <a href="https://iconscout.com/contributors/anggaraputra" class="text-underline font-size-sm">Anggara Putra</a> on <a href="https://iconscout.com" class="text-underline font-size-sm">IconScout</a>
- Download Icon by [Tutukof](https://iconscout.com/contributors/fersusart)
- Free [Settings Icon](https://iconscout.com/free-icon/settings-2856913) in Gradient Style
By [Haca Studio](https://iconscout.com/contributors/boosticon)

Logo was generated by DALL-E (ChatGPT)

## Contributors (as in V3 and before)

- [Egsagon](https://github.com/Egsagon)
- [RSDCFGVHBJNKML](https://github.com/RSDCFGVHBJNKML) : Enhancement [#11](https://github.com/EchterAlsFake/Porn_Fetch/issues/11)
- Chinese (3.0) Thanks to: [Joshua-auhsoj](https://github.com/Joshua-auhsoj) & Enhancement [#17](https://github.com/EchterAlsFake/Porn_Fetch/issues/17)

# Libraries

- [PHUB](https://github.com/EchterAlsFake/PHUB)
- [requests](https://github.com/psf/requests)
- [hqporner_api](https://github.com/EchterAlsFake/hqporner_api)
- [hue_shift](https://github.com/EchterAlsFake/hue_shift)
- [PySide6](https://doc.qt.io/qtforpython-6/)
- [pymediainfo](https://github.com/sbraz/pymediainfo)
- [colorama](https://github.com/tartley/colorama)
- [markdown](https://github.com/Python-Markdown/markdown)
- [rich](https://github.com/Textualize/rich)
- [tqdm](https://github.com/tqdm/tqdm)
- [EPorner API](https://github.com/EchterAlsFake/eporner_api)
- [XNXX API](https://github.com/EchterAlsFake/xnxx_api)
<br>ANDROID:
- [Buildozer](https://github.com/kivy/buildozer)
- [Cython](https://github.com/cython/cython)

** All other libraries are built in to Python.

"""
        md = Markdown(text_markdown)
        rprint(md)


CLI()





