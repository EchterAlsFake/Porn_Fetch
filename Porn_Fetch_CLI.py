"""
Porn Fetch CLI

Licensed under GPL 3
Copyright (C) 2023 Johannes Habel (EchterAlsFake)

Version 3.0
"""
import getpass
import os.path
import threading
import markdown

from phub import Video, Client, errors, download, display, Quality
from configparser import ConfigParser
from hqporner_api import API
from rich import print as rprint
from rich.markdown import Markdown
from tqdm import tqdm

from src.backend.shared_functions import (strip_title, check_video, check_if_video_exists, setup_config_file,
                                          logger_debug, logger_error, return_color, reset, correct_output_path)


downloaded_segments = 0
total_segments = 0


class CLI():
    def __init__(self):
        self.client = None
        setup_config_file()
        self.conf = ConfigParser()
        self.conf.read("config.ini")

        # Variable initialization
        self.directory_system = None
        self.threading = None
        self.threading_mode = None
        self.search_limit = None
        self.output_path = None
        self.api_language = None
        self.quality = None

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
1) Download a Video (PornHub / HQPorner)
2) Download videos from a Model / Channel / User
3) Search Users / Models / Channels
4) Download from a file with URLs
5) Account
6) Metadata
7) Settings
8) Credits / Information

-------------------------------=>:""")

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
            self.get_metadat_options()

        elif options == "7":
            self.save_user_settings()

        elif options == "8":
            self.credits()

    def start_single_video(self):
        url = input(f"""Enter PornHub / HQPorner URL --=>: """)
        self.pre_setup_video(url)

    def start_model_user_channel(self):
        url = input(f"""
Please enter the URL to the PornHub User / Model / Channel account.

Hint: You can select the videos to be downloaded later!

----------------------------=>:""")

        client = Client(language=self.api_language)
        model = client.get_user(url)
        videos = model.videos

        videos_list = []

        for idx, video in enumerate(videos, start=0):
            print(f"{idx}) {video.title}")
            videos_list.append(video)

        to_be_downloaded = input(f"""
Enter the numbers of videos you want to download (separate with comma)

e.g. 1,5,20,6,7 

Hint: Enter ALL to download all videos

------------------------=>:

""")
        if to_be_downloaded.lower() == "all":
            for video in videos_list:
                self.pre_setup_video(video)

        else:
            split = to_be_downloaded.split(",")
            for index in split:
                video = videos_list[int(index)]
                self.pre_setup_video(video)

    def start_from_file(self):
        file = input(f"""
Enter the (exact) location of the file.

Hint: URLs from either PornHub or HQPorner need to be separated with new lines!

---------------------------------=>:""")

        if os.path.exists(file):
            with open(file, "r") as url_file:
                content = url_file.read().splitlines()
                for url in content:
                    self.pre_setup_video(url)

        else:
            logger_error("File doesn't exist! Please try again.")
            self.start_from_file()

    def pre_setup_video(self, url):
        if str(url).endswith(".html"):
            title = API().extract_title(url)
            author = API().extract_actress(url)
            video = str(url)

        else:
            language = self.api_language
            video = check_video(url, language)
            title = video.title
            author = video.author.name
            quality = self.quality

        title = strip_title(title)
        output_path = self.output_path
        if not output_path.endswith(os.sep):
            output_path = f"{output_path}{os.sep}"

        if self.directory_system:
            output_path = f"{output_path}{author}{os.sep}{title}"

        else:
            output_path = f"{output_path}{title}"

        if not check_if_video_exists(video=video, output_path=output_path):
            if isinstance(video, str):
                if self.threading:
                    hqporner_thread = threading.Thread(target=self.download_video_hqporner, args=(url, output_path))
                    hqporner_thread.start()

                else:
                    self.download_video_hqporner(url=url, output_path=output_path)

            elif isinstance(video, Video):
                if self.threading:
                    pornhub_thread = threading.Thread(target=self.download_video_pornhub,
                                                      args=(video, output_path, quality))
                    pornhub_thread.start()

                else:
                    self.download_video_pornhub(video=video, output_path=output_path, quality=quality)

    def download_video_pornhub(self, video, output_path, quality):

        if self.threading_mode == "2":
            threading_X = download.threaded()

        elif self.threading_mode == "1":
            threading_X = download.FFMPEG

        elif self.threading_mode == "0":
            threading_X = download.default

        video.download(downloader=threading_X, quality=quality, path=output_path, display=display.progress())

    def download_video_hqporner(self, url, output_path):
        API().download(url=url, no_title=True, output_path=output_path, quality="highest")

    def load_user_settings(self):
        self.api_language = self.conf["Video"]["language"]
        self.output_path = self.conf["Video"]["output_path"]
        self.search_limit = int(self.conf["Video"]["search_limit"])
        self.threading = self.conf["Performance"]["threading"]
        self.threading_mode = self.conf["Performance"]["threading_mode"]
        self.directory_system = self.conf["Video"]["directory_system"]
        quality = self.conf["Video"]["quality"]

        if quality == "best":
            self.quality = Quality.BEST

        elif quality == "half":
            self.quality = Quality.HALF

        elif quality == "worst":
            self.quality = Quality.WORST

        if self.threading == "yes":
            self.threading = True

        if self.directory_system == "1":
            self.directory_system = True
        ""

    def save_user_settings(self):
        quality_ext = self.quality
        threading_ext = self.threading_mode
        api_language_ext = self.api_language
        output_path_ext = self.output_path
        directory_system_ext = self.directory_system

        options = input(f"""
--------------QUALITY-------------|
|>  Current: {quality_ext}
|>  1) Best
|>  2) Half
|>  3) Worst
|-------------Threading-----------|
|>  Current: {threading_ext}
|>  4) High Performance
|>  5) FFMPEG (needs ffmpeg installed on your system)
|>  6) Default
|>  7) Disable Threading for the whole application
|--------------API Language--------|
|>  Current: {api_language_ext}
|>  8) Enter custom language code... e.g. de for german or es for espanol
|--------------Output Path----------|
|>  Current: {output_path_ext}
|>  9) Change Output Path
|--------------Directory System-----|
|>  Current: {directory_system_ext}
|>  10) Enable
|>  11) Disable
|--------------------------=>:""")
        if options == "1":
            self.conf.set("Video", "quality", "best")

        elif options == "2":
            self.conf.set("Video", "quality", "half")

        elif options == "3":
            self.conf.set("Video", "quality", "worst")

        elif options == "4":
            self.conf.set("Performance", "threading_mode", "2")
            self.conf.set("Performance", "threading", "1")

        elif options == "5":
            self.conf.set("Performance", "threading_mode", "1")
            self.conf.set("Performance", "threading", "1")

        elif options == "6":
            self.conf.set("Performance", "threading_mode", "0")
            self.conf.set("Performance", "threading", "1")

        elif options == "7":
            self.conf.set("Performance", "threading", "0")

        elif options == "8":
            language_code = input(f"""
Please enter the language code -->:""")
            self.conf.set("Video", "language", language_code)

        elif options == "9":
            output_path = input(f"""
Please enter the new output path -->:""")
            if not os.path.exists(output_path):
                logger_error("The specified output path doesn't exist!")

            else:
                output_path = correct_output_path(output_path)

            self.conf.set("Video", "output_path", output_path)

        elif options == "10":
            self.conf.set("Video", "directory_system", "1")

        elif options == "11":
            self.conf.set("Video", "directory_system", "0")

        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)

        logger_debug("Applied new settings!")
        self.load_user_settings()
        logger_debug("Reloaded User settings. You may continue now :) ")

    def get_metadat_options(self):
        options = input(f"""
1) Get Video metadata
2) Get User metadata
3) Back
------------------=>:""")
        if options == "1":
            self.get_video_metadata()

        elif options == "2":
            self.get_user_metadata()

        elif options == "3":
            self.main_menu()

    def search_options(self):
        options = input(f"""
1) Search for Videos
2) Search for Users
3) Search for Pornstars
4) Back
! search filters aren't working yet. 

------------------=>:""")

        if options == "1":
            self.search_videos()

        elif options == "2":
            self.search_users()

        elif options == "3":
            self.search_pornstars()

        elif options == "4":
            self.main_menu()

    def search_videos(self):
        query = input(f"""
Please enter your search query ---=>:""")

        if not isinstance(self.client, Client):
            language = self.api_language
            self.client = Client(language=language)

        generator = self.client.search(query)
        self.start_generator(generator)

    def search_users(self):
        query = input(f"""
Enter a query to search for users --=>:""")

        if not isinstance(self.client, Client):
            language = self.api_language
            self.client = Client(language=language)

        generator = self.client.search_user(query)
        self.start_generator(generator)

    def search_pornstars(self):

        query = input(f"""
        Enter a query to search for Pornstars --=>:""")

        if not isinstance(self.client, Client):
            language = self.api_language
            self.client = Client(language=language)

        generator = self.client.search_pornstar(query)
        self.start_generator(generator)

    def start_generator(self, generator):
        video_objects = []

        for idx, video in enumerate(generator):
            print(f"{idx}) {video.title}")
            video_objects.append(video)

        index = input(f"""
        Please enter the number for the videos you want to download. Separate with a comma
        e.g 1,6,92 

        ! Enter 'ALL' to download all videos
        -----------------------=>:""")

        if index.lower() == "all":
            for video in video_objects:
                self.pre_setup_video(url=video)

        else:
            chosen_videos = index.split(",")
            for idx in chosen_videos:
                video = video_objects[int(idx)]
                self.pre_setup_video(url=video)

    def get_video_metadata(self):
        language = self.api_language
        url = input(f"""
Please enter the video url (PornHub) --=>:""")

        video = check_video(url, language=language)

        author = video.author
        duration = video.duration.seconds
        duration = round(duration, 2) / 60
        title = strip_title(video.title)
        date = video.date
        views = video.views
        pornstar_list = [pornstar.name for pornstar in video.pornstars]
        hotspots_list = [str(hotspots) for hotspots in video.hotspots]

        tags_list = [tag.name for tag in video.tags]
        tags = ", ".join(tags_list)
        hotspots = ", ".join(hotspots_list)
        pornstars = "".join(pornstar_list)
        rating = f"Likes: {video.like.up} | Dislikes: {video.like.down}"

        input(f"""
Title: {title}
Author: {author}
Duration: {duration}
Date: {date}
Views: {views}
Pornstars: {pornstars}
Rating: {rating}
Tags: {tags}
Hotspots: {hotspots}

Press ENTER to continue""")
        self.main_menu()

    def get_user_metadata(self):
        api_language = self.api_language
        url = input(f"""
Enter the User URL (PornHub) --=>:""")

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
Name: {name}
Type: {type}

Relationship Status: {relationship_status}
Interested In: {interested_in}
City and Country: {city_and_country}
Gender: {gender}
Birth Place: {birth_place}
Height: {height}
Weight: {weight}
Ethnicity: {ethnicity}
Hair Color: {hair_color}
Fake Boobs: {fake_boobs}
Tattoos: {tattoos}
Piercings: {piercings}
Hometown: {hometown}
Interests and Hobbies: {interests_and_hobbies}
Turn Ons: {turn_ons}
Turn Offs: {turn_offs}
Video Views: {video_views}
Profile views: {profile_views}
Videos Watched: {videos_watched}

Press ENTER to continue...""")
        self.main_menu()

    def account_options(self):
        options = input(f"""
1) Login
2) Get watched videos
3) Get liked videos
4) Get recommended videos
5) Back
---------------------------=>:
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
        username = input(f"Please enter your PornHub Username --=>:")
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

    def progress(self, desc: str = 'Downloading'):
        '''
        Simple progress display using tqdm.

        Args:
            desc (str): Description to display.

        Returns:
            Callable: A wrapper to pass to a downloader.
        '''

        def wrapper(total: int) -> tqdm:
            """
            Initializes and returns a tqdm progress bar object.

            Args:
                total (int): The total number of iterations (e.g., the size of the file to be downloaded).

            Returns:
                tqdm: A tqdm progress bar object.
            """
            return tqdm(total=total, desc=desc, unit='i', ncols=100)

        return wrapper

    def credits(self):
        text_markdown = f"""
# Porn Fetch V3

Copyright (C) 2023 Johannes Habel (EchterAlsFake)


### This Project is only possible thanks to Egsagon's [PHUB](https://github.com/Egsagon/PHUB) API

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
- <a href="https://iconscout.com/icons/tick" class="text-underline font-size-sm" target="_blank">Tick</a> by <a href="https://iconscout.com/contributors/endesignz" class="text-underline font-size-sm">Jessiey Sahana</a> on <a href="https://iconscout.com" class="text-underline font-size-sm">IconScout</a>
- <a href="https://iconscout.com/icons/top-arrow" class="text-underline font-size-sm" target="_blank">Top Arrow</a> by <a href="https://iconscout.com/contributors/creative-studio" class="text-underline font-size-sm" target="_blank">Mian Saab</a>
- <a href="https://iconscout.com/icons/down-arrow" class="text-underline font-size-sm" target="_blank">Down Arrow</a> by <a href="https://iconscout.com/contributors/adamicons" class="text-underline font-size-sm">Adam Dicons</a> on <a href="https://iconscout.com" class="text-underline font-size-sm">IconScout</a>
- <a href="https://iconscout.com/icons/tick" class="text-underline font-size-sm" target="_blank">Tick</a> by <a href="https://iconscout.com/contributors/kolo-design" class="text-underline font-size-sm" target="_blank">Kalash</a>
- Download Icon by [Tutukof](https://iconscout.com/contributors/fersusart)
- Search Icon by [Kmg Design](https://iconscout.com/contributors/kmgdesignid)

Logo was generated by DALL-E (ChatGPT)

## Contributors (as in V3 and before)

- [Egsagon](https://github.com/Egsagon)
- [RSDCFGVHBJNKML](https://github.com/RSDCFGVHBJNKML) : Enhancement [#11](https://github.com/EchterAlsFake/Porn_Fetch/issues/11)

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
<br>ANDROID:
- [Kivy MD](https://github.com/kivymd/KivyMD)
- [Kivy](https://kivy.org/)
- [Buildozer](https://github.com/kivy/buildozer)
- [Cython](https://github.com/cython/cython)

** All other libraries are built in to Python.


"""
        md = Markdown(text_markdown)
        rprint(md)

CLI()





