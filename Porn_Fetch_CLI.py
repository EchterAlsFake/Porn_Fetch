import sys
import pathlib
import threading

from src.backend.shared_functions import *
from phub import download as ph_download
from base_api.modules.download import *
from base_api.modules.progress_bars import *



class CLI():
    def __init__(self):
        self.threading_mode = None
        self.result_limit = None
        self.directory_system = None
        self.output_path = None
        self.quality = None
        self.semaphore = None
        self.retries = None
        self.timeout = None
        self.workers = None
        self.delay = None
        self.language = None
        while True:
            setup_config_file()
            self.conf = ConfigParser()
            self.conf.read("config.ini")
            self.load_user_settings()
            self.menu()


    def license(self):
        if not self.conf["License"]["accepted"] == "true":
            license = input(f"""
GPL License Agreement for Porn Fetch
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
NO LIABILITY FOR END USER USE
Under no circumstances and under no legal theory, whether in tort, contract, or otherwise, shall the copyright holder or contributors be liable to You for any direct, indirect, special, incidental, consequential or exemplary damages of any character including, without limitation, damages for loss of goodwill, work stoppage, computer failure or malfunction, loss of data or any and all other commercial damages or losses, even if such party shall have been informed of the possibility of such damages.
This limitation of liability shall not apply to liability for death or personal injury resulting from such party’s negligence to the extent applicable law prohibits such limitation. Some jurisdictions do not allow the exclusion or limitation of incidental or consequential damages, so this exclusion and limitation may not apply to You.
This Agreement represents the complete agreement concerning the subject matter hereof.

Disclaimer:
Porn Fetch is NOT associated with any of the websites. Using this tool is against the ToS of every website. Usage of Porn Fetch is at your own risk. I (the developer) am not liable for any of your actions. This tool is not meant to be used for mass downloading content from websites or downloading copyright protected material.


Do you accept the license?  [yes,no]
---------------------------------->:""")

            if license == "yes":
                self.conf.set("License", "accepted", "true")

                with open("config.ini", "w") as config_file:
                    self.conf.write(config_file)

            else:
                self.conf.set("License", "accepted", "false")

                with open("config.ini", "w") as config_file:
                    self.conf.write(config_file)

                sys.exit()

    def menu(self):
        options = input(f"""
1) Download a Video
2) Get videos from a model
3) Get videos from a PornHub playlist
4) Search for videos
5) Search a file for URLs and Model URLs
6) Settings

98) Credits
99) Exit

------------------>:""")

        if options == "1":
            self.process_video()

    def load_user_settings(self):
        self.language = self.conf.get("Video", "language")
        self.delay = int(self.conf.get("Video", "delay"))
        self.workers = int(self.conf.get("Performance", "workers"))
        self.timeout = int(self.conf.get("Performance", "timeout"))
        self.retries = int(self.conf.get("Performance", "retries"))
        self.semaphore = threading.Semaphore(int(self.conf.get("Performance", "semaphore")))
        self.quality = self.conf.get("Video", "quality")
        self.output_path = correct_output_path(output_path=self.conf.get("Video", "output_path"))
        self.directory_system = True if self.conf.get("Video", "directory_system") == "1" else False
        self.result_limit = int(self.conf.get("Video", "search_limit"))
        self.threading_mode = self.conf.get("Performance", "threading_mode")

    def save_user_settings(self):
        languages = """
de: German
en: English
fr: French
zh: Chinese
rt: Russian
nl: Dutch
es: Spanish
it: Italian
pt: Portuguese
cz: Czech
jp: Japanese
"""
        while True:
            settings_options = input(f"""
--------- Quality ----------
1) Best
2) Half
3) Worst
-------- Performance --------
4) Change Semaphore
5) Change Delay
6) Change Workers
7) Change Retries
8) Change Timeout
-------- Directory System ---
9) Enable / Disable directory system
-------- Result Limit -------
10) Change result limit
-------- Language (Video titles for PornHub)
11) Change Language
-------- Output Path --------
12) Change output path

99) Exit
------------->:
""")

            try:
                if settings_options == "1":
                    self.conf.set("Video", "quality", "best")
    
                elif settings_options == "2":
                    self.conf.set("Video", "quality", "half")
    
                elif settings_options == "3":
                    self.conf.set("Video", "quality", "worst")
                
                elif settings_options == "4":
                    limit = input(f"Enter a new Semaphore limit -->:")    
                    self.conf.set("Performance", "semaphore", limit)
                
                elif settings_options == "5":
                    limit = input(f"Enter a new delay (seconds) -->:")
                    self.conf.set("Video", "delay", limit)
                
                elif settings_options == "6":
                    limit = input(f"Enter a new value for max workers -->:")
                    self.conf.set("Performance", "workers", limit)
    
                elif settings_options == "7":
                    limit = input(f"Enter a new value for max retries -->:")
                    self.conf.set("Performance", "retries", limit)
                
                elif settings_options == "8":
                    limit = input(f"Enter a new value for the max timeout -->:", limit)
                
                elif settings_options == "9":
                    if self.directory_system:
                        self.conf.set("Video", "directory_system", "0")
                    
                    else:
                        self.conf.set("Video", "directory_system", "1")
                    
                elif settings_options == "10":
                    limit = input(f"Enter a new result limit -->:")
                    self.conf.set("Video", "search_limit", limit)
                
                elif settings_options == "11":
                    print("Please enter a language code from the list below:")
                    print(languages)
                    language = input(f"Enter the new language code -->:")
                    self.conf.set("Video", "language", language)
                
                elif settings_options == "12":
                    path = input(f"Enter a new output path -->:")
                    if not os.path.exists(path):
                        raise FileNotFoundError("The specified output path doesn't exist!")
                    
                    self.conf.set("Video", "output_path", path)                
            
                
                elif settings_options == "99":
                    self.menu()
            
            finally:
                with open("config.ini", "w") as config_file:
                    self.conf.write(config_file)
                    
    def process_video(self, url=None):
        if url is None:
            url = input(f"Please enter the Video URL -->:")

        video = check_video(url=url, language=self.language, delay=self.delay)
        title = video.title

        if isinstance(video, Video):
            author = video.author.name

        else:
            author = video.author

        output_path = self.output_path

        if self.directory_system:
            output_path = pathlib.Path(output_path + title + author + ".mp4")

        else:
            output_path = pathlib.Path(output_path + title + ".mp4")

        if os.path.exists(output_path):
            logger_debug(f"File: {output_path} already exists, skipping...")
            return

        logger_debug("Trying to acquire the semaphore...")
        self.semaphore.acquire()
        self.thread = threading.Thread(target=self.download, args=(video, output_path, ))
        self.thread.start()

    def iterate_generator(self, generator):
        videos = []

        for idx, video in enumerate(generator):
            print(f"{idx}) - {video.title}")
            videos.append(video)

        vids = input(f"""
Please enter the numbers of videos you want to download with a comma separated.
for example: 1,5,94,3

------------------------>:""")

        selected_videos = vids.split(",")
        for number in selected_videos:
            video = videos[int(number)]
            self.process_video(video)

    def process_model(self, url=None, do_return=False):
        if url is None:
            model = input(f"Enter the model URL -->:")

        else:
            model = url

        if eporner_pattern.search(model):
            model = ep_Client().get_pornstar(model, enable_html_scraping=True).videos(pages=10)

        elif xnxx_pattern.match(model):
            model = xn_Client().get_user(model).videos

        elif pornhub_pattern.match(model):
            model = Client().get_user(model).videos

        elif hqporner_pattern.match(model):
            model = hq_Client().get_videos_by_actress(model)

        elif xvideos_pattern.match(model):
            print("XVideos isn't supported yet, sorry.")
            return

        if do_return:
            return model

        self.iterate_generator(model)

    def process_playlist(self):
        url = input("Enter the (PornHub) playlist URL -->:")
        playlist = Client().get_playlist(url)
        print(f"Processing: {playlist.title}")
        self.iterate_generator(playlist.videos)

    def search_videos(self):
        website = input(f"""
Please select the website to search on:

1) PornHub
2) HQPorner
3) XVideos
4) XNXX
5) Eporner
----------->:""")
        query = input(f"Please enter the search query -->:")

        if website == "1":
            self.iterate_generator(Client().search(query))

        elif website == "2":
            self.iterate_generator(hq_Client().search_videos(query=query, pages=10))

        elif website == "3":
            self.iterate_generator(xv_Client().search(query))

        elif website == "4":
            self.iterate_generator(xn_Client().search(query))

        elif website == "5":
            self.iterate_generator(ep_Client().search_videos(query, page=1, per_page=self.result_limit, sorting_order="", sorting_gay="", sorting_low_quality=""))

    def process_file(self):
        videos = []
        models = []
        objects = []
        file = input(f"Please enter the file path -->:")

        with open(file, "r") as file:
            content = file.read()
            content = content.splitlines()

        for line in content:
            if line.startswith("model#"):
                line = line.split("#")[1]
                models.append(self.process_model(url=line, do_return=True))

            else:
                videos.append(line)

        logger_debug("Processing Models / Videos...")
        for video in videos:
            objects.append(check_video(video, language=self.language, delay=self.delay))

        for video in models:
            objects.append(video)

        logger_debug("Done!")
        self.iterate_generator(objects)

    def download(self, video, output_path):

        try:
            if self.threading_mode == "threaded" and isinstance(video, Video):
                self.threading_mode = ph_download.threaded(max_workers=self.workers, timeout=self.timeout)

            elif self.threading_mode == "threaded" and not isinstance(video, Video):
                self.threading_mode = threaded(max_workers=self.workers, timeout=self.timeout, retries=self.retries)

            if isinstance(video, Video):
                video.download(path=output_path, quality=self.quality, downloader=self.threading_mode, display=Callback.text_progress_bar)

            else:
                video.download(path=output_path, quality=self.quality, downloader=self.threading_mode, callback=Callback.text_progress_bar)

        finally:
            logger_debug(f"Finished downloading for: {video.title}")



CLI()



