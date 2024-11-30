import os.path
import pathlib
import shutil
import threading
from io import TextIOWrapper

import phub.consts

from src.backend.shared_functions import *
from src.backend.log_config import setup_logging
from base_api.modules.download import *
from base_api.modules.progress_bars import *
from base_api.base import Core
from colorama import init
from rich import print as rprint
from rich.markdown import Markdown

logger = setup_logging()
init(autoreset=True)


class CLI:
    def __init__(self):
        self.skip_existing_files = None
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
        self.ffmpeg_features = True
        self.ffmpeg_path = None
        while True:
            setup_config_file()
            self.conf = ConfigParser()
            self.conf.read("config.ini")
            self.license()
            self.ffmpeg_recommendation()
            self.load_user_settings()
            self.menu()

    def license(self):
        if not self.conf["Setup"]["license_accepted"] == "true":
            license_text = input(f"""{Fore.WHITE}
GPL License Agreement for Porn Fetch
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.
NO LIABILITY FOR END USER USE
Under no circumstances and under no legal theory, whether in tort, contract, or otherwise, shall the copyright holder or contributors be liable to You for any direct, indirect, special, incidental, consequential or exemplary damages of any character including, without limitation, damages for loss of goodwill, work stoppage, computer failure or malfunction, loss of data or any and all other commercial damages or losses, even if such party shall have been informed of the possibility of such damages.
This limitation of liability shall not apply to liability for death or personal injury resulting from such party’s negligence to the extent applicable law prohibits such limitation. Some jurisdictions do not allow the exclusion or limitation of incidental or consequential damages, so this exclusion and limitation may not apply to You.
This Agreement represents the complete agreement concerning the subject matter hereof.

Disclaimer:
Porn Fetch is NOT associated with any of the websites. Using this tool is against the ToS of every website. Usage of Porn Fetch is at your own risk. I (the developer) am not liable for any of your actions. This tool is not meant to be used for mass downloading content from websites or downloading copyright protected material.

Information:
Porn Fetch uses ffmpeg for video processing / converting. FFmpeg is free software licensed under the GPL license.
See more information on: https://FFmpeg.org


Do you accept the license?  [{Fore.LIGHTBLUE_EX}yes{Fore.RESET},{Fore.LIGHTRED_EX}no{Fore.RESET}]
---------------------------------->:""")

            if license_text == "yes":
                self.conf.set("Setup", "license_accepted", "true")
                with open("config.ini", "w") as config_file: #type: TextIOWrapper
                    self.conf.write(config_file)

            else:
                self.conf.set("Setup", "license_accepted", "false")
                with open("config.ini", "w") as config_file: #type: TextIOWrapper
                    self.conf.write(config_file)

                sys.exit()

    def menu(self):
        options = input(f"""
{return_color()}1) Download a Video
{return_color()}2) Get videos from a model
{return_color()}3) Get videos from a PornHub playlist
{return_color()}4) Search for videos
{return_color()}5) Search a file for URLs and Model URLs
{return_color()}6) Settings

{Fore.LIGHTWHITE_EX}98) Credits
{Fore.LIGHTRED_EX}99) Exit
{return_color()}------------------>:""")

        if options == "1":
            self.process_video()

        elif options == "2":
            self.process_model(None, False)

        elif options == "3":
            self.process_playlist()

        elif options == "4":
            self.search_videos()

        elif options == "5":
            self.process_file()

        elif options == "6":
            self.save_user_settings()

        elif options == "98":
            self.credits()

        elif options == "99":
            sys.exit(0)

    def ffmpeg_recommendation(self):
        if os.path.exists("/data/data/com.termux/files/home"):
            ffmpeg = input(f"""
Hey,

It seems like you are using Termux... I highly recommend you to use FFmpeg as your threading mode, because downloading
HLS segments is very slow on Android devices, because the processor and the system in general can't handle so many
threads at the same time.

You can install FFmpeg with: 'apt-get install ffmpeg'

If you accept, Porn Fetch will close and automatically set ffmpeg as your downloader.

Do you want to use FFmpeg? [yes,no]        
    """)

            if ffmpeg.lower() == "yes":
                self.conf.set("Performance", "threading_mode", "FFMPEG")
                with open("config.ini", "w") as config_file: #type: TextIOWrapper
                    self.conf.write(config_file)
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTYELLOW_EX}Done!")

    def load_user_settings(self):
        self.delay = int(self.conf.get("Video", "delay"))
        self.workers = int(self.conf.get("Performance", "workers"))
        self.timeout = int(self.conf.get("Performance", "timeout"))
        self.retries = int(self.conf.get("Performance", "retries"))
        self.semaphore = threading.Semaphore(int(self.conf.get("Performance", "semaphore")))
        self.quality = self.conf.get("Video", "quality")
        self.output_path = correct_output_path(output_path=self.conf.get("Video", "output_path"))
        self.directory_system = True if self.conf.get("Video", "directory_system") == "1" else False
        self.skip_existing_files = True if self.conf.get("Video", "skip_existing_files") == "true" else False
        self.result_limit = int(self.conf.get("Video", "search_limit"))
        self.threading_mode = self.conf.get("Performance", "threading_mode")

        try:
            if shutil.which("ffmpeg"):
                self.ffmpeg_path = shutil.which("ffmpeg")

            else:
                if os.path.isfile("ffmpeg"):
                    self.ffmpeg_path = "ffmpeg"

                elif os.path.isfile("ffmpeg.exe"):
                    self.ffmpeg_path = "ffmpeg.exe"

                else:
                    logger.warning("FFMPEG wasn't found... Have you extracted it from the .zip file?")
                    logger.warning("FFMPEG Features won't be available!")
                    self.ffmpeg_features = False
        finally:
            if not self.ffmpeg_path == "":
                phub.consts.FFMPEG_EXECUTABLE = self.ffmpeg_path
                consts.FFMPEG_PATH = self.ffmpeg_path
                self.ffmpeg_features = True

    def save_user_settings(self):
        while True:
            quality_color = {  # Highlight the current quality option in yellow
                "Best": Fore.LIGHTYELLOW_EX if self.quality == "best" else Fore.LIGHTWHITE_EX,
                "Half": Fore.LIGHTYELLOW_EX if self.quality == "balf" else Fore.LIGHTWHITE_EX,
                "Worst": Fore.LIGHTYELLOW_EX if self.quality == "borst" else Fore.LIGHTWHITE_EX
            }
            threading_mode_color = {  # Highlight the current threading mode in yellow
                "threaded": Fore.LIGHTYELLOW_EX if self.threading_mode == "threaded" else Fore.LIGHTWHITE_EX,
                "ffmpeg": Fore.LIGHTYELLOW_EX if self.threading_mode == "ffmpeg" else Fore.LIGHTWHITE_EX,
                "default": Fore.LIGHTYELLOW_EX if self.threading_mode == "default" else Fore.LIGHTWHITE_EX
            }

            settings_options = input(f"""
{Fore.LIGHTYELLOW_EX}YELLOW {Fore.LIGHTWHITE_EX} = Currently selected / Current value
            
{Fore.LIGHTWHITE_EX}--------- {Fore.LIGHTGREEN_EX}Quality {Fore.LIGHTWHITE_EX}----------
1) {quality_color["Best"]}Best{Fore.LIGHTWHITE_EX}
2) {quality_color["Half"]}Half{Fore.LIGHTWHITE_EX}
3) {quality_color["Worst"]}Worst{Fore.LIGHTWHITE_EX}
{Fore.LIGHTWHITE_EX}-------- {Fore.LIGHTCYAN_EX}Performance {Fore.LIGHTWHITE_EX}--------
4) Change Semaphore {Fore.LIGHTYELLOW_EX}(current: {self.semaphore._value}){Fore.LIGHTWHITE_EX}
5) Change Delay {Fore.LIGHTYELLOW_EX}(current: {self.delay}){Fore.LIGHTWHITE_EX}
6) Change Workers {Fore.LIGHTYELLOW_EX}(current: {self.workers}){Fore.LIGHTWHITE_EX}
7) Change Retries {Fore.LIGHTYELLOW_EX}(current: {self.retries}){Fore.LIGHTWHITE_EX}
8) Change Timeout {Fore.LIGHTYELLOW_EX}(current: {self.timeout}){Fore.LIGHTWHITE_EX}
-------- {Fore.LIGHTYELLOW_EX}Directory System {Fore.LIGHTWHITE_EX}---
9) Enable / Disable directory system {Fore.LIGHTYELLOW_EX}(current: {"Enabled" if self.directory_system else "Disabled"}){Fore.LIGHTWHITE_EX}
{Fore.LIGHTWHITE_EX}-------- {Fore.LIGHTGREEN_EX}Result Limit {Fore.LIGHTWHITE_EX}-------
10) Change result limit {Fore.LIGHTYELLOW_EX}(current: {self.result_limit}){Fore.LIGHTWHITE_EX}
{Fore.LIGHTWHITE_EX}-------- {Fore.LIGHTBLUE_EX}Output Path {Fore.LIGHTWHITE_EX}--------
11) Change output path {Fore.LIGHTYELLOW_EX}(current: {self.output_path}){Fore.LIGHTWHITE_EX}
{Fore.LIGHTWHITE_EX}---------{Fore.LIGHTMAGENTA_EX}Threading Mode {Fore.LIGHTWHITE_EX}---------
12) {threading_mode_color["threaded"]}Change to threaded (Not recommended on Android!){Fore.LIGHTWHITE_EX}
13) {threading_mode_color["ffmpeg"]}Change to FFmpeg (Recommended on Android){Fore.LIGHTWHITE_EX}
14) {threading_mode_color["default"]}Change to default (really slow){Fore.LIGHTWHITE_EX}
{Fore.LIGHTRED_EX}99) Exit
{Fore.WHITE}------------->:""")

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
                    limit = input(f"Enter a new value for the max timeout -->:")
                    self.conf.set("Performance", "timeout", limit)

                elif settings_options == "9":
                    if self.directory_system:
                        self.conf.set("Video", "directory_system", "0")

                    else:
                        self.conf.set("Video", "directory_system", "1")

                elif settings_options == "10":
                    limit = input(f"Enter a new result limit -->:")
                    self.conf.set("Video", "search_limit", limit)

                elif settings_options == "11":
                    path = input(f"Enter a new output path -->:")
                    if not os.path.exists(path):
                        raise "The specified output path doesn't exist!"

                    self.conf.set("Video", "output_path", path)

                elif settings_options == "12":
                    self.conf.set("Performance", "threading_mode", "threaded")

                elif settings_options == "13":
                    self.conf.set("Performance", "threading_mode", "FFMPEG")

                elif settings_options == "14":
                    self.conf.set("Performance", "threading_mode", "default")

                elif settings_options == "99":
                    self.menu()

            finally:
                with open("config.ini", "w") as config_file: #type: TextIOWrapper
                    self.conf.write(config_file)

    def process_video(self, url=None):
        if url is None:
            url = input(f"{return_color()}Please enter the Video URL -->:")

        video = check_video(url=url, delay=self.delay)
        title = Core().strip_title(video.title)

        if isinstance(video, Video):
            author = video.author.name

        elif isinstance(video, hq_Video):
            author = video.pornstars[0] if len(video.pornstars) > 0 else "Unknown"

        else:
            author = video.author

        output_path = self.output_path

        if self.directory_system:
            output_path = pathlib.Path(output_path + title + author + ".mp4")

        else:
            output_path = pathlib.Path(output_path + title + ".mp4")

        if os.path.exists(output_path):
            logger.debug(f"{return_color()}File: {output_path} already exists, skipping...")
            return

        logger.debug(f"{return_color()}Trying to acquire the semaphore...")
        self.semaphore.acquire()
        self.thread = threading.Thread(target=self.download, args=(video, output_path,))
        self.thread.start()

    def iterate_generator(self, generator):
        videos = []

        for idx, video in enumerate(generator):
            print(f"{idx}) - {video.title}")
            videos.append(video)

            if idx >= self.result_limit:
                break

        vids = input(f"""
{return_color()}Please enter the numbers of videos you want to download with a comma separated.
for example: 1,5,94,3{Fore.WHITE}

Enter 'all' to download all videos

{return_color()}------------------------>:{Fore.WHITE}""")

        if vids == "all":
            for video in videos:
                self.process_video(video)

        else:
            selected_videos = vids.split(",")

            for number in selected_videos:
                video = videos[int(number)]
                self.process_video(video)

    def process_model(self, url=None, do_return=False):
        if url is None:
            model = input(f"{return_color()}Enter the model URL -->:")

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
            model = xv_Client().get_pornstar(model).videosH

        if do_return:
            return model

        self.iterate_generator(model)

    def process_playlist(self):
        url = input(f"{return_color()}Enter the (PornHub) playlist URL -->:")
        playlist = Client().get_playlist(url)
        print(f"{return_color()}Processing: {playlist.title}")
        self.iterate_generator(playlist.sample())

    def search_videos(self):
        website = input(f"""
{return_color()}Please select the website to search on:

{return_color()}1) PornHub
{return_color()}2) HQPorner
{return_color()}3) XVideos
{return_color()}4) XNXX
{return_color()}5) Eporner
{return_color()}----------->:""")
        query = input(f"{return_color()}Please enter the search query -->:")

        if website == "1":
            self.iterate_generator(Client().search(query))

        elif website == "2":
            self.iterate_generator(hq_Client().search_videos(query=query))

        elif website == "3":
            self.iterate_generator(xv_Client().search(query))

        elif website == "4":
            self.iterate_generator(xn_Client().search(query).videos)

        elif website == "5":
            self.iterate_generator(ep_Client().search_videos(query, per_page=self.result_limit,
                                                             sorting_order="", sorting_gay="", sorting_low_quality="",
                                                             enable_html_scraping=True, page=1))

    def process_file(self):
        videos = []
        models = []
        objects = []
        file = input(f"{return_color()}Please enter the file path -->:")

        with open(file, "r") as file:
            content = file.read()
            content = content.splitlines()

        for line in content:
            if line.startswith("model#"):
                line = line.split("#")[1]
                models.append(self.process_model(url=line, do_return=True))

            else:
                videos.append(line)

        logger.debug(f"{return_color()}Processing Models / Videos...")
        for video in videos:
            objects.append(check_video(video, delay=self.delay))

        for video in models:
            objects.append(video)

        logger.debug(f"{return_color()}Done!")
        self.iterate_generator(objects)

    def download(self, video, output_path):
        try:
            if isinstance(video, Video):
                self.threading_mode = resolve_threading_mode(mode=self.threading_mode, video=video,
                                                             workers=self.workers, timeout=self.timeout)
                video.download(path=output_path, quality=self.quality, downloader=self.threading_mode,
                               display=self.callback_wrapper(video.title, Callback.text_progress_bar))

            elif isinstance(video, ep_Video) or isinstance(video, hq_Video):
                video.download(path=output_path, quality=self.quality, callback=self.callback_wrapper(video.title,
                                Callback.text_progress_bar))

            else:
                video.download(downloader=self.threading_mode, path=output_path, quality=self.quality,
                               callback=self.callback_wrapper(video.title, Callback.text_progress_bar))

        finally:
            logger.debug(f"{return_color()}Finished downloading for: {video.title}")
            self.semaphore.release()
            if self.ffmpeg_features:
                os.rename(f"{output_path}", f"{output_path}_.tmp")
                cmd = [self.ffmpeg_path, "-i", f"{output_path}_.tmp", "-c", "copy", output_path, '-hide_banner',
                       '-loglevel', 'error']
                ff = FfmpegProgress(cmd)
                for progress in ff.run_command_with_progress():
                    print(f"\r\033[K[Converting: {progress}/100", end='', flush=True)

                os.remove(f"{output_path}_.tmp")
                write_tags(path=output_path, video=video)
            else:
                logger.debug("FFMPEG features disabled, writing tags and converting the video won't be available!")

    @staticmethod
    def callback_wrapper(title, callback):
        def wrapped_callback(pos, total):
            callback(pos, total, title)

        return wrapped_callback

    @staticmethod
    def credits():
        content = (requests.get("https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/README/CREDITS.md")
                   .text)
        md = Markdown(content)
        rprint(md)


CLI()
