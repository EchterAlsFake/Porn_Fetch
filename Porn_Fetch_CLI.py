"""
Porn Fetch CLI

Licensed under GPL 3
Copyright (C) 2023 Johannes Habel (EchterAlsFake)

Version 3.0
"""
import os.path
import threading


from phub import *
from configparser import ConfigParser
from hqporner_api import API

from src.backend.shared_functions import (strip_title, check_video, check_if_video_exists, setup_config_file,
                                          logger_debug, logger_error, return_color, reset, correct_output_path)


downloaded_segments = 0
total_segments = 0

class CLI():
    def __init__(self):
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

        if self.license():
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

    def main_menu(self):
        options = input(f"""
1) Download a Video (PornHub / HQPorner)
2) Download videos from a Model / Channel / User
3) Search Users / Models / Channels
4) Download from a file with URLs
5) Metadata
6) Settings
7) Help
8) Credits / Information

-------------------------------=>:""")

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

    def download_video(self, video, output_path):

        if str(video).endswith(".html"):
            API().download(url=video, output_path=output_path, no_title=True, quality="highest")

        else:

            if self.threading_mode == "0":
                video.download()






    def pre_setup_video(self, url):

    def download_video_hqporner(self):

    def settings(self):

    def load_user_settings(self):
        self.api_language = self.conf["Video"]["language"]
        self.output_path = self.conf["Video"]["output_path"]
        self.search_limit = int(self.conf["Video"]["search_limit"])
        self.threading = self.conf["Performance"]["threading"]
        self.threading_mode = self.conf["Performance"]["threading_mode"]
        self.directory_system = self.conf["Video"]["directory_system"]

        if self.threading == "yes":
            self.threading = True

        if self.directory_system == "1":
            self.directory_system = True


    def save_user_settings(self):


    def help(self):

    def credits(self):










