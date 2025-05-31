import configparser
import os.path
import shutil
import threading
import argparse
import phub.consts
import traceback
import itertools

import queue
from io import TextIOWrapper
from src.backend.shared_functions import *
from base_api.modules.progress_bars import *
from base_api.base import BaseCore, setup_logger
from rich import print as rprint
from rich.markdown import Markdown
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn, TimeElapsedColumn, TimeRemainingColumn
from colorama import *
from hue_shift import return_color


logger = setup_logger(name="Porn Fetch - [CLI]", log_file=None, level=logging.INFO)
init(autoreset=True)



class CLI:
    def __init__(self):
        self.downloaded_segments = 0
        self.total_segments = 0 # Used for total progress tracking
        self.to_be_downloaded = 0
        self.finished_downloading = 0
        self.progress_queue = queue.Queue()
        self.skip_existing_files = None
        self.threading_mode = None
        self.result_limit = None
        self.directory_system = None
        self.output_path = None
        self.progress_thread = None
        self.quality = None
        self.semaphore = None
        self.retries = None
        conf = None
        self.timeout = None
        self.workers = None
        self.delay = None
        self.language = None
        self.ffmpeg_features = True
        self.ffmpeg_path = None
        self.progress = Progress(
            TextColumn("[progress.description]{task.description}", style="bold cyan"),  # Display task description here
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%", style="bold cyan"),
            BarColumn(bar_width=20, finished_style="bold green"),
            TextColumn("[bold green]{task.completed}[/] / {task.total}", style="bold yellow"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            SpinnerColumn(spinner_name="dots")
        )
        self.task_total_progres = self.progress.add_task("[progress.description]{task.description}", total=self.total_segments)
        # Please just don't ask, thank you :)

    def init(self):
        while True:
            setup_config_file()
            conf = ConfigParser()
            conf.read("config.ini")
            self.license()
            self.ffmpeg_recommendation()
            self.load_user_settings()
            self.menu()

    def license(self):
        if not conf["Setup"]["license_accepted"] == "true":
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
                conf.set("Setup", "license_accepted", "true")
                with open("config.ini", "w") as config_file: #type: TextIOWrapper
                    conf.write(config_file)

            else:
                conf.set("Setup", "license_accepted", "false")
                with open("config.ini", "w") as config_file: #type: TextIOWrapper
                    conf.write(config_file)

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
            url = input(f"{return_color()}Please the enter video URL -->: {return_color()}")
            video = [check_video(url)]
            self.iterate_generator(auto=True, generator=video)

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
                conf.set("Performance", "threading_mode", "FFMPEG")
                with open("config.ini", "w") as config_file: #type: TextIOWrapper
                    conf.write(config_file)
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTYELLOW_EX}Done!")

    def load_user_settings(self):
        self.delay = int(conf.get("Video", "delay"))
        self.workers = int(conf.get("Performance", "workers"))
        self.timeout = int(conf.get("Performance", "timeout"))
        self.retries = int(conf.get("Performance", "retries"))
        self.semaphore = threading.Semaphore(int(conf.get("Performance", "semaphore")))
        self.quality = conf.get("Video", "quality")
        self.output_path = conf.get("Video", "output_path")
        self.directory_system = True if conf.get("Video", "directory_system") == "1" else False
        self.skip_existing_files = True if conf.get("Video", "skip_existing_files") == "true" else False
        self.result_limit = int(conf.get("Video", "search_limit"))
        self.threading_mode = conf.get("Performance", "threading_mode")

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
                bs_consts.FFMPEG_PATH = self.ffmpeg_path
                self.ffmpeg_features = True

    def save_user_settings(self):
        while True:
            quality_color = {  # Highlight the current quality option in yellow
                "Best": Fore.LIGHTYELLOW_EX if self.quality == "best" else Fore.LIGHTWHITE_EX,
                "Half": Fore.LIGHTYELLOW_EX if self.quality == "half" else Fore.LIGHTWHITE_EX,
                "Worst": Fore.LIGHTYELLOW_EX if self.quality == "worst" else Fore.LIGHTWHITE_EX
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
                    conf.set("Video", "quality", "best")

                elif settings_options == "2":
                    conf.set("Video", "quality", "half")

                elif settings_options == "3":
                    conf.set("Video", "quality", "worst")

                elif settings_options == "4":
                    limit = input(f"Enter a new Semaphore limit -->:")
                    conf.set("Performance", "semaphore", limit)

                elif settings_options == "5":
                    limit = input(f"Enter a new delay (seconds) -->:")
                    conf.set("Video", "delay", limit)

                elif settings_options == "6":
                    limit = input(f"Enter a new value for max workers -->:")
                    conf.set("Performance", "workers", limit)

                elif settings_options == "7":
                    limit = input(f"Enter a new value for max retries -->:")
                    conf.set("Performance", "retries", limit)

                elif settings_options == "8":
                    limit = input(f"Enter a new value for the max timeout -->:")
                    conf.set("Performance", "timeout", limit)

                elif settings_options == "9":
                    if self.directory_system:
                        conf.set("Video", "directory_system", "0")

                    else:
                        conf.set("Video", "directory_system", "1")

                elif settings_options == "10":
                    limit = input(f"Enter a new result limit -->:")
                    conf.set("Video", "search_limit", limit)

                elif settings_options == "11":
                    path = input(f"Enter a new output path -->:")
                    if not os.path.exists(path):
                        raise "The specified output path doesn't exist!"

                    conf.set("Video", "output_path", path)

                elif settings_options == "12":
                    conf.set("Performance", "threading_mode", "threaded")

                elif settings_options == "13":
                    conf.set("Performance", "threading_mode", "FFMPEG")

                elif settings_options == "14":
                    conf.set("Performance", "threading_mode", "default")

                elif settings_options == "99":
                    self.menu()

            finally:
                with open("config.ini", "w") as config_file: #type: TextIOWrapper
                    conf.write(config_file)

    def process_video(self, url=None, batch=False):
        self.semaphore.acquire()

        if url is None:
            url = input(f"{return_color()}Please enter the Video URL -->:")

        video = check_video(url=url)
        data = load_video_attributes(video)
        author = data.get("author")
        title = data.get("title")

        output_path = self.output_path

        if self.directory_system:
            path_author = os.path.join(output_path, author)
            if not os.path.exists(path_author):
                os.makedirs(path_author, exist_ok=True) # doesn't make sense ik

            output_path = os.path.join(str(path_author), title + ".mp4")

        else:
            output_path = os.path.join(output_path, title + ".mp4")

        if os.path.exists(output_path):
            logger.debug(f"{return_color()}File: {output_path} already exists, skipping...")
            print(f"{return_color()}File: {output_path} already exists, skipping...")
            self.semaphore.release()
            return

        # Create the progress task
        task = self.progress.add_task(description=f"[bold cyan]Downloading: {video.title}[/bold cyan]", total=100)

        # Start the download thread
        self.progress.start()
        self.download_thread = threading.Thread(target=self.download, args=(video, output_path, task))
        self.download_thread.start()

        self.progress_thread = threading.Thread(target=self._update_progress)
        self.progress_thread.start()


        if batch:
            self.download_thread.join()

    def process_video_with_error_handling(self, video, batch, ignore_errors):
        try:
            print(f"Processing video: {video.title}")
            self.process_video(video, batch=batch)
        except Exception as e:
            if ignore_errors:
                print(f"{Fore.LIGHTRED_EX}[~]{Fore.RED}Ignoring Error: {e}")
            else:
                raise f"{Fore.LIGHTRED_EX}[~]{Fore.RED}Error: {e}, please report the full traceback --: {traceback.print_exc()}"

    def iterate_generator(self, generator, auto=False, ignore_errors=False, batch=False):
        videos = []

        for idx, video in enumerate(generator):
            print(f"{idx}) - {video.title}")
            videos.append(video)

            if idx >= self.result_limit:
                break

        print(f"Videos loaded: {len(videos)}")

        if not auto:
            vids = input(f"""
    {return_color()}Please enter the numbers of videos you want to download with a comma separated.
    for example: 1,5,94,3{Fore.WHITE}

    Enter 'all' to download all videos

    {return_color()}------------------------>:{Fore.WHITE}""")
        else:
            vids = "all"

        if vids == "all" or auto:
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTYELLOW_EX}Calculating the total progress... This may take some time!")

            self.total_segments = sum(
                [len(list(video.get_segments(quality=self.quality))) for video in videos if
                 hasattr(video, 'get_segments')])
            logger.debug(f"Got segments: {self.total_segments}")

            self.to_be_downloaded = len(videos)

            for video in videos:
                self.process_video_with_error_handling(video, batch, ignore_errors)
        else:
            selected_videos = vids.split(",")
            videos_ = []
            for number in selected_videos:
                videos_.append(videos[int(number)])

            self.total_segments = sum(
                [len(list(video.get_segments(quality=self.quality))) for video in videos_ if
                 hasattr(video, 'get_segments')])

            self.to_be_downloaded = len(selected_videos)
            for number in selected_videos:
                video = videos[int(number)]
                self.process_video_with_error_handling(video, batch, ignore_errors)


    def process_model(self, url=None, do_return=False, auto=False, ignore_errors=False, batch=False):
        if url is None:
            model = input(f"{return_color()}Enter the model URL -->:")

        else:
            model = url

        if eporner_pattern.search(model):
            model = ep_Client().get_pornstar(model, enable_html_scraping=True).videos(pages=10)

        elif xnxx_pattern.match(model):
            model = xn_Client().get_user(model).videos

        elif pornhub_pattern.match(model):
            model = itertools.chain(Client().get_user(model).videos, Client().get_user(model).uploads)

        elif hqporner_pattern.match(model):
            model = hq_Client().get_videos_by_actress(model)

        elif xvideos_pattern.match(model):
            model = xv_Client().get_pornstar(model).videos

        if do_return:
            return model

        self.iterate_generator(model, auto=auto, ignore_errors=ignore_errors, batch=batch)

    def process_playlist(self, url=None, auto=False, ignore_errors=False, batch=False):
        if url is None:
            url = input(f"{return_color()}Enter the (PornHub) playlist URL -->:")
        playlist = Client().get_playlist(url)
        print(f"{return_color()}Processing: {playlist.title}")
        self.iterate_generator(playlist.sample(), auto=auto, ignore_errors=ignore_errors, batch=batch)

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
            objects.append(check_video(video))

        for video in models:
            objects.append(video)

        logger.debug(f"{return_color()}Done!")
        self.iterate_generator(objects)

    def download(self, video, output_path, task):
        try:
            def callback_wrapper(pos, total):
                self.progress_queue.put((task, pos, total))
                self.downloaded_segments += 1

            if isinstance(video, Video):
                video.download(path=output_path, quality=self.quality, downloader=self.threading_mode,
                               display=callback_wrapper)

            elif isinstance(video, ep_Video) or isinstance(video, hq_Video):
                video.download(path=output_path, quality=self.quality, no_title=True,
                               callback=Callback.text_progress_bar)

            else:
                video.download(downloader=self.threading_mode, path=output_path, no_title=True, quality=self.quality,
                               callback=callback_wrapper)

        finally:
            logger.debug(f"{return_color()}Finished downloading for: {video.title}")

            # Handle FFMPEG processing
            if self.ffmpeg_features:
                os.rename(f"{output_path}", f"{output_path}_.tmp")
                cmd = [self.ffmpeg_path, "-i", f"{output_path}_.tmp", "-c", "copy", output_path, '-hide_banner',
                       '-loglevel', 'error']
                ff = FfmpegProgress(cmd)
                for progress in ff.run_command_with_progress():
                    logger.debug(f"Converting progress: {progress}")

                os.remove(f"{output_path}_.tmp")
                write_tags(path=output_path, data=load_video_attributes(video))
            else:
                logger.debug("FFMPEG features disabled, writing tags and converting the video won't be available!")

            # Mark task as completed
            self.progress.update(task, completed=self.progress.tasks[task].total)
            self.progress_queue.put(None)  # This signals _update_progress to stop when all tasks are done
            self.finished_downloading += 1
            self.semaphore.release()
            print(f"{Fore.LIGHTGREEN_EX}[+] {Fore.LIGHTYELLOW_EX}Video download finished!, you can continue navigating through the menu :)")


    def _update_progress(self):
        while True:
            try:
                task_data = self.progress_queue.get()
                if task_data is None:
                    break  # Stop when all tasks are done

                task, pos, total = task_data

                # Ensure we only update when progress changes
                progress_diff = pos - self.progress.tasks[task].completed
                if progress_diff > 0:
                    self.progress.update(task, advance=progress_diff, total=total)

                total_progress_diff = self.downloaded_segments - self.progress.tasks[self.task_total_progres].completed
                if total_progress_diff > 0:
                    self.progress.update(self.task_total_progres, advance=total_progress_diff,
                                         total=self.total_segments,
                                         description=f"Total progress | Downloaded: {self.finished_downloading}/{self.to_be_downloaded} videos")

                self.progress.refresh()

            except TypeError:
                break

        self.progress.stop()  # Ensure the progress disappears when done

    @staticmethod
    def credits():
        content = BaseCore().fetch("https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/README/CREDITS.md")
        md = Markdown(content)
        rprint(md)


class Batch(CLI):
    def __init__(self):
        super().__init__()
        conf = ConfigParser()
        conf.read("config.ini")
        self.main()

    def main(self):
            description = """
Porn Fetch CLI - Download Porn from your terminal / batch processing

Disclaimer:
I strictly forbid you to mass-scrape content from other sites. I do not encourage this in any way. If you use this tool
to redistribute copyright protected content, you are responsible for your actions. I am not liable for any damages caused!

CLI GUIDE (Please read this if it's your first time)

1.
All options like --url; --playlist; ... can be put together. Porn Fetch will process all of your inputs starting from 
a URL. a URL given with '--url' will download a single video. If you put a URL and a Playlist at the same time,
Porn Fetch will start downloading the single video from '--url' and then continue with the videos from the submitted
playlist. 

2. 
You can give a lot of options from the configuration file manually into the CLI. This allows for a lot of flexibility.
If you don't give any of the options Porn Fetch will attempt to read from an existing 'config.ini' file. 
If neither a configuration file is found nor you provided any options manually, Porn Fetch will create a 'config.ini' 
file which you can use in the next run. Please use this file to change your options accordingly. 
I do not want to implement all options as a command line option as it would be too much work for such a small thing. 
If you wanna implement it, feel free to PR lol


Here are the options:

OPTION            | TYPE  | DESCRIPTION
--url             | (str) | A video URL
--model           | (str) | A model URL
--playlist        | (str) | A playlist URL
--quality         | (str) | The quality of the videos [best, half, worst] > Default: best
--output          | (str) | The path to a folder where to save the downloaded videos. > Default: current directory (./) 
--threading_mode  | (str) | The threading mode (backend, how to download the videos) [threaded,ffmpeg,default]
                            Note: The threading mode 'ffmpeg' requires ffmpeg installed in your path!

--auto_process    | (bool) | Whether to automatically download all videos from playlists, files, models or ask you 
                             to select a range of videos


Note:
By using the CLI batch mode you automatically accept the GPLv3 License of Porn Fetch!
        """

            parser = argparse.ArgumentParser("Porn Fetch CLI - Batch processing")
            parser.add_argument("--info", help="A help message. READ THIS ON YOUR FIRST RUN!!!!!!!!!!!!!!!!!!!!!!!!",
                                action="store_true")
            parser.add_argument("--batch",
                                help="Whether to start the interactive CLI or batch processing (Read documentation)",
                                action="store_true")
            parser.add_argument("--url", help="a Video URL", type=str)
            parser.add_argument("--model", help="a model URL", type=str)
            parser.add_argument("--playlist", help="a Playlist URL", type=str)
            parser.add_argument("--output", help="the path to a folder where to save the downloaded videos",
                                type=str, default=os.getcwd())
            parser.add_argument("--quality", help="The quality of the videos", default="best",
                                choices=["best", "half", "worst"], type=str)
            parser.add_argument("--threading_mode", help="the threading mode", default="threaded",
                                choices=["threaded", "ffmpeg", "default"], type=str)
            parser.add_argument("--ignore_errors", help="Whether to ignore errors during downloads",
                                action="store_false")
            parser.add_argument("--auto_process", help="Whether to automatically download all videos from playlists,"
                                                       "files, models or ask you to select each videos individually",
                                action="store_true")

            args = parser.parse_args()

            if args.info:
                print(description)
                exit(0)

            if args.batch is False:
                CLI().init()

            url = args.url
            model = args.model
            playlist = args.playlist
            quality = args.quality
            threading_mode = args.threading_mode
            output = args.output
            ignore = args.ignore_errors
            auto_process = args.auto_process

            print("Checking and loading configuration...")
            try:
                conf = configparser.ConfigParser()
                conf.read("config.ini")
                self.load_user_settings()

            except Exception as e:
                print(f"Error in loading configuration..., creating a new configuration file... Error:")
                logger.error(e)
                setup_config_file(force=True)
                conf = configparser.ConfigParser()
                conf.read("config.ini")
                self.load_user_settings()

            # Overriding the values from configuration file with CLI values
            self.quality = quality
            self.threading_mode = threading_mode
            self.output_path = output

            if url:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTCYAN_EX}Downloading URL -->: {url}")
                self.process_video(url=url, batch=True)

            if model:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTYELLOW_EX}Processing model -->: {model}")
                if auto_process:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTMAGENTA_EX}! Using auto processing !")

                self.process_model(url=model, auto=auto_process, ignore_errors=ignore, batch=True)

            if playlist:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTBLUE_EX}Processing Playlist -->: {playlist}")
                if auto_process:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTMAGENTA_EX}! Using auto processing !")

                self.process_playlist(url=playlist, auto=auto_process, ignore_errors=ignore, batch=True)




if __name__ == '__main__':
    Batch()





