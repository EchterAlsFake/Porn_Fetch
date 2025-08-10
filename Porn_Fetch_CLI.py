import time
import queue
import logging
import os.path
import argparse
import threading
import traceback
import itertools

from colorama import *
from io import TextIOWrapper
from rich import print as rprint
from hue_shift import return_color
from rich.markdown import Markdown
from base_api.modules.progress_bars import *
from base_api.base import BaseCore, setup_logger
from base_api.modules.config import RuntimeConfig
from src.backend.CLI_model_feature_addon import *
import src.backend.shared_functions as shared_functions
from base_api.modules.errors import (InvalidProxy, ProxySSLError)
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn, TimeElapsedColumn, TimeRemainingColumn

try:
    import av
    remux = True

except (ModuleNotFoundError, ImportError):
    print(f"""Couldn't import pyav. Videos will not be remuxed, this is NOT an error if you are running on macOS / Termux""")
    remux = False


proxy_one_time_config_stuff_please_dont_ask_thank_you_very_mushhh = RuntimeConfig()
STATE_FILE = "model_database.json"

logger = setup_logger(name="Porn Fetch - [CLI]", log_file="PornFetch_CLI_LOG.log", level=logging.ERROR)
logger_model_feature = setup_logger(name="Porn Fetch - [ModelBatchDownload]", log_file="PornFetch___ModelDownload___.log", level=logging.INFO)
init(autoreset=True)
conf = shared_functions.shared_config
logging.disable(level=logging.DEBUG)


class CLI:
    def __init__(self):
        self._progress_stop = threading.Event()
        self.downloaded_segments = 0
        self.total_segments = 0
        self.to_be_downloaded = 0
        self.finished_downloading = 0
        self.progress_queue = queue.Queue()
        self.skip_existing_files = None
        self.threading_mode = None
        self.result_limit = None
        self.speed_limit = None
        self.directory_system = None
        self.output_path = None
        self.progress_thread = None
        self.quality = None
        self.semaphore = None
        self.retries = None
        self.timeout = None
        self.workers = None
        self.delay = None
        self.language = None
        self.ffmpeg_features = True
        self.ffmpeg_path = None
        shared_functions.refresh_clients()

        # Setup the progress display (tasks added later)
        self.progress = Progress(
            TextColumn("[progress.description]{task.description}", style="bold cyan"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%", style="bold cyan"),
            BarColumn(bar_width=20, finished_style="bold green"),
            TextColumn("[bold green]{task.completed}[/] / {task.total}", style="bold yellow"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            SpinnerColumn(spinner_name="dots"),
        )
        self.task_total_progress = None

    def init(self):
        shared_functions.setup_config_file()
        conf.read("config.ini")
        self.license()
        self.load_user_settings()
        conf.read("config.ini")

        if conf.get("Setup", "first_run_cli") == "true":
            self.first_run_cli()

        while True:
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
{return_color()}5) Search a file for Video URLs (only Videos)
{return_color()}6) Settings
{return_color()}7) Model update / database feature (experimental)
 
{return_color()}1337) Enable Proxy (experimental)
{return_color()}1338) Enable Proxy Kill Switch (very experimental)

{Fore.LIGHTWHITE_EX}98) Credits
{Fore.LIGHTRED_EX}99) Exit
{return_color()}------------------>:""")

        if options == "1":
            url = input(f"{return_color()}Please the enter video URL -->: {return_color()}")
            video = [shared_functions.check_video(url)]
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

        elif options == "7":
            self.experimental_model_download()

        elif options == "1337":
            self.set_proxy()

        elif options == "1338":
            shared_functions.refresh_clients(enable_kill_switch=True)
            print("Refreshed Clients with Kill Switch enabled!")

        elif options == "98":
            self.credits()
            self.menu()

        elif options == "99":
            sys.exit(0)

    def experimental_model_download(self, path: str = STATE_FILE):
        """
        Interactive menu for managing the automatic model downloader.
        `fetch_generator_fn` must accept a model_url and return an iterable of Video objects.
        """
        while True:
            choice = input("""
What do you want to do?

1) Show help
2) Add new Models
3) Fetch pending URLs for all models
4) Delete Models
5) Show statistics
6) Exit

99) Start Downloading / Updating Models

Enter choice: """)
            if choice == '1':
                show_help()

            elif choice == '2':
                urls = input("Enter model URLs to add (comma-separated): ").split(',')
                for url in [u.strip() for u in urls if u.strip()]:
                    add_model_url(url, path=path)

            elif choice == '3':
                # requires a function fetch_generator_fn(url)
                update_pending_for_all_models(self.process_model, path=path)

            elif choice == '4':
                urls = input("Enter model URLs to delete (comma-separated): ").split(',')
                for url in [u.strip() for u in urls if u.strip()]:
                    remove_model_url(url, path=path)

            elif choice == '5':
                show_stats(path)

            elif choice == '6':
                self.menu()

            elif choice == "99":
                self.update_models()

            else:
                print("Invalid choice, please enter 1-6.")

    def update_models(self):
        models = get_all_saved_models(STATE_FILE)
        idx = 0
        for model in models:
            model_url, data = model

            idx += 1
            print(f"Processing: [{idx}|{len(models)}] -->: {model_url}")
            pending_videos = data.get("pending")

            if len(pending_videos) >= 1:
                print(f"Model has pending videos! Downloading: {len(pending_videos)}")
                for idx, url in enumerate(pending_videos):
                    print(f"[{idx}|{len(pending_videos)}] Downloading -->: {url}")
                    videos = [shared_functions.check_video(url)]
                    try:
                        self.iterate_generator(generator=videos, batch=True, auto=True, remove_total_bar=True)
                        record_download(model_url=model_url, video_url=url, path=STATE_FILE)

                    except Exception:
                        error = traceback.format_exc()
                        logger_model_feature.error(f"""
        Model: {model_url}
        Video URL: {url}
        Error: {error}
        Index: {idx}""")

                logger_model_feature.info(f"""
        Model: {model_url}
        STATUS: Finished!
        """)

            else:
                print(f"Model has no pending videos, continuing with the next one!")
                continue

    def set_proxy(self):
        proxy = input(f"""
{Fore.LIGHTWHITE_EX}Please enter your proxy in the format like this:
<protocol><ip>:<port>
You can find free socks proxies here: https://spys.one/en/socks-proxy-list/
Or http[s] proxies here: https://proxyscrape.com/free-proxy-list
Example:

1) {Fore.LIGHTMAGENTA_EX}socks5://13.37.4.20:1337 {Fore.LIGHTGREEN_EX}(Socks5 is recommended)
2) {Fore.LIGHTCYAN_EX}https://54.224.25.185:69
{Fore.LIGHTMAGENTA_EX}
Disclaimer:
The Proxy feature was well tested, however there's no guarantee for it to perfectly function and never leaking your IP.
Also, free proxies are very unreliable in general. Consider using a paid / your own proxy. 

{Fore.LIGHTYELLOW_EX}Your Proxy -->:{Fore.LIGHTWHITE_EX}""")
        print(f"Testing your Proxy: {proxy}")

        import httpx
        ip_unmasked = httpx.Client().get("https://httpbin.org/ip").json()["origin"]
        try:
            proxy_one_time_config_stuff_please_dont_ask_thank_you_very_mushhh.proxy = proxy
            proxy_core = BaseCore(proxy_one_time_config_stuff_please_dont_ask_thank_you_very_mushhh)
            ip_masked = BaseCore(config=proxy_one_time_config_stuff_please_dont_ask_thank_you_very_mushhh).fetch("https://httpbin.org/ip", get_response=True).json()["origin"]

        except InvalidProxy:
            print("Your Proxy in invalid. Try again!")
            self.set_proxy()

        except ProxySSLError:
            ssl_verification = input(f"""
        {Fore.LIGHTYELLOW_EX}WARNING

{Fore.LIGHTRED_EX}Your Proxy does NOT support proper TLS / SSL verfification. It may use a self-signed certificate or 
no certificate at all. You can disable SSL verification to get around this, however, this makes you vulnerable to
man in the middle attacks. Everyone in your network will be able to inject malicious downloads on the fly, intercept 
your connection, and read all your traffic.

Do you accept the risk? 
-------[Yes|No]--->:
""")

            if ssl_verification.lower() == "yes":
                print("Disabling SSL verficiation...")
                shared_functions.config.verify_ssl = False
                ip_masked = httpx.Client(proxy=proxy, verify=False).get("https://httpbin.org/ip").json()["origin"]

            else:
                print("Alright, going back to main menu....")
                self.menu()

        if ip_unmasked == ip_masked:
            print(f"{Fore.LIGHTRED_EX}Your Proxy IP is equal to your normal IP! Your Proxy is not working, check your input!{Fore.LIGHTWHITE_EX}")
            self.set_proxy()

        else:
            print(f"{return_color()}SUCCESS! {Fore.LIGHTWHITE_EX}Your Proxy IP is: {Fore.LIGHTYELLOW_EX}{ip_masked}. {Fore.LIGHTWHITE_EX}Using your Proxy for this session :)")
            shared_functions.config.proxy = proxy
            shared_functions.refresh_clients()
            print("Refreshed Clients!")

    def first_run_cli(self):
        input(f"""
Hello, thank you for using Porn Fetch. Please read through this real quick, to get a better understanding how everything 
works.

Notice: The CLI is for advanced users and has a different / uncompleted feature set compared to the GUI!

# Regarding Video Progress:
Progressbar for EPorner and HQPorner videos is in MB, for all others it's in segments. 

# Video post processing:
Videos are post-processed using pyav by default. Pyav ships the binaries for ffmpeg, and I use that to remux videos. 
Videos that use HLS streaming are wrapped in an MPEG-TS container. Some video players fail to play that and I can't
tag metadata to these videos. That's why we remux them. Pyav is NOT available on Termux (See down below).

# Termux
If you want to use the CLI on Termux, you definitely can. However, to actually save videos, you need to setup termux storage.
You can do so by typing: 'termux-setup-storage' in your terminal. This will request storage permissions and you should
see a folder called 'storage' in your home directory. From there you should be able to access your internal phone storage
and save videos to that path.

Pyav does not work on Termux, because you'd need to cross-compile ffmpeg for aarch64 / armv7. I don't do that, and trust
me you also don't want to do that XD. Porn Fetch's code is automatically made in a way that it handles this automatically.
So please don't be upset if the videos aren't true mp4. Most Android media players should play those files just fine. 

Thank you very much for using Porn Fetch. Have a great time.
Bugs can be reported at: https://github.com/EchterAlsFake/Porn_Fetch/issues/

(Press enter when you've finished reading)
""")
        with open("config.ini", "w") as config:
            shared_functions.shared_config.set("Setup", "first_run_cli", "false")
            shared_functions.shared_config.write(config)

    def load_user_settings(self):
        self.delay = int(conf.get("Video", "delay"))
        self.workers = int(conf.get("Performance", "workers"))
        self.timeout = int(conf.get("Performance", "timeout"))
        self.retries = int(conf.get("Performance", "retries"))
        self.speed_limit = float(conf.get("Performance", "speed_limit"))
        self.semaphore = threading.Semaphore(int(conf.get("Performance", "semaphore")))
        self.quality = conf.get("Video", "quality")
        self.output_path = conf.get("Video", "output_path")
        self.directory_system = True if conf.get("Video", "directory_system") == "1" else False
        self.skip_existing_files = True if conf.get("Video", "skip_existing_files") == "true" else False
        self.result_limit = int(conf.get("Video", "result_limit"))
        self.threading_mode = conf.get("Performance", "threading_mode")
        shared_functions.config.request_delay = self.delay # Lmao in all versions past 3.6 these things were never actually applied to the backend LOOOOL
        shared_functions.config.timeout = self.timeout
        shared_functions.config.max_retries = self.retries
        shared_functions.config.max_bandwidth_mb = self.speed_limit
        shared_functions.refresh_clients()
        logger.info("Refreshed Clients with user settings being applied!")


    def save_user_settings(self):
        while True:
            quality_color = {  # Highlight the current quality option in yellow
                "Best": Fore.LIGHTYELLOW_EX if self.quality == "best" else Fore.LIGHTWHITE_EX,
                "Half": Fore.LIGHTYELLOW_EX if self.quality == "half" else Fore.LIGHTWHITE_EX,
                "Worst": Fore.LIGHTYELLOW_EX if self.quality == "worst" else Fore.LIGHTWHITE_EX
            }
            threading_mode_color = {  # Highlight the current threading mode in yellow
                "threaded": Fore.LIGHTYELLOW_EX if self.threading_mode == "threaded" else Fore.LIGHTWHITE_EX,
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
20) Set a Speed Limit {Fore.LIGHTYELLOW_EX}(Current: {self.speed_limit}){Fore.LIGHTWHITE_EX}
-------- {Fore.LIGHTYELLOW_EX}Directory System {Fore.LIGHTWHITE_EX}---
9) Enable / Disable directory system {Fore.LIGHTYELLOW_EX}(current: {"Enabled" if self.directory_system else "Disabled"}){Fore.LIGHTWHITE_EX}
{Fore.LIGHTWHITE_EX}-------- {Fore.LIGHTGREEN_EX}Result Limit {Fore.LIGHTWHITE_EX}-------
10) Change result limit {Fore.LIGHTYELLOW_EX}(current: {self.result_limit}){Fore.LIGHTWHITE_EX}
{Fore.LIGHTWHITE_EX}-------- {Fore.LIGHTBLUE_EX}Output Path {Fore.LIGHTWHITE_EX}--------
11) Change output path {Fore.LIGHTYELLOW_EX}(current: {self.output_path}){Fore.LIGHTWHITE_EX}
{Fore.LIGHTWHITE_EX}---------{Fore.LIGHTMAGENTA_EX}Threading Mode {Fore.LIGHTWHITE_EX}---------
12) {threading_mode_color["threaded"]}Change to threaded (Not recommended on Android!){Fore.LIGHTWHITE_EX}
13) {threading_mode_color["default"]}Change to default (really slow){Fore.LIGHTWHITE_EX}
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
                    conf.set("Video", "result_limit", limit)

                elif settings_options == "11":
                    path = input(f"Enter a new output path -->:")
                    if not os.path.exists(path):
                        raise "The specified output path doesn't exist!"

                    conf.set("Video", "output_path", path)

                elif settings_options == "12":
                    conf.set("Performance", "threading_mode", "threaded")

                elif settings_options == "13":
                    conf.set("Performance", "threading_mode", "default")

                elif settings_options == "20":
                    speed_limit = input(f"Please enter the limit in MB/s (example: 2.5) -->:")
                    conf.set("Performance", "speed_limit", speed_limit)

                elif settings_options == "99":
                    self.menu()

            finally:
                with open("config.ini", "w") as config_file: #type: TextIOWrapper
                    conf.write(config_file)

    def process_video(self, url=None, video=None, batch=False, remove_total_bar=False):
        self.semaphore.acquire()
        if video is None:
            url = url or input("Enter Video URL: ")
            video = shared_functions.check_video(url=url)

        attrs = shared_functions.load_video_attributes(video)
        author = attrs.get('author', '')
        title = attrs.get('title', 'video')

        # Determine output path
        out_dir = self.output_path or os.getcwd()
        if self.directory_system:
            author_dir = os.path.join(out_dir, author)
            os.makedirs(author_dir, exist_ok=True)
            out_file = os.path.join(author_dir, f"{title}.mp4")
        else:
            out_file = os.path.join(out_dir, f"{title}.mp4")

        if os.path.exists(out_file):
            logger.debug(f"File exists, skipping: {out_file}")
            print(f"Skipping existing file: {out_file}")
            self.semaphore.release()
            self.menu()

        # Create per-video task
        task_id = self.progress.add_task(
            description=f"Downloading: {title}",
            total=None,
        )

        dl_thread = threading.Thread(
            target=self.download,
            args=(video, out_file, task_id, remove_total_bar),
            daemon=True,
        )
        dl_thread.start()
        if batch:
            dl_thread.join()

    def process_video_with_error_handling(self, video, batch, ignore_errors, remove_total_bar):
        try:
            print(f"Processing video: {video.title}")
            self.process_video(video, batch=batch, remove_total_bar=remove_total_bar)
        except Exception as e:
            if ignore_errors:
                print(f"{Fore.LIGHTRED_EX}[~]{Fore.RED}Ignoring Error: {e}")
            else:
                raise f"{Fore.LIGHTRED_EX}[~]{Fore.RED}Error: {e}, please report the full traceback --: {traceback.print_exc()}"

    def iterate_generator(self, generator, auto=False, ignore_errors=False, batch=False, remove_total_bar=False):
        videos = []
        for idx, video in enumerate(generator):
            print(f"{idx}) - {video.title}")
            videos.append(video)
            if idx + 1 >= self.result_limit:
                break

        selection = "all" if auto else input(
            "\nPlease enter the numbers of videos to download (comma-separated) or 'all' to download all:\n"
        )
        to_download = videos if selection.strip().lower() == "all" else [videos[i] for i in
                                                                         map(int, selection.split(","))]

        # (your existing segment counting + optional total bar creation here)

        # reset per-run counters and start refresh thread
        self.finished_downloading = 0
        self.to_be_downloaded = len(to_download)
        self._progress_stop.clear()

        self.progress.start()
        self.progress_thread = threading.Thread(target=self._update_progress, daemon=True)
        self.progress_thread.start()

        # kick off downloads
        for video in to_download:
            try:
                self.process_video_with_error_handling(video=video, batch=batch, remove_total_bar=remove_total_bar,
                                                       ignore_errors=ignore_errors)
            except Exception as e:
                if ignore_errors:
                    print(f"{Fore.LIGHTRED_EX}[~]{Fore.RED} Ignoring Error: {e}")
                else:
                    raise

        # wait until all downloads finished (set in download() finally)
        while self.finished_downloading < self.to_be_downloaded:
            time.sleep(0.1)

        # stop refresher cleanly and close progress
        self._progress_stop.set()
        self.progress_thread.join()

        # optional tidy-up of total bar if you want the line gone:
        if self.task_total_progress is not None:
            try:
                self.progress.remove_task(self.task_total_progress)
            except ValueError:
                pass

        self.progress.stop()


    def process_model(self, url=None, do_return=False, auto=False, ignore_errors=False, batch=False):
        if url is None:
            model = input(f"{return_color()}Enter the model URL -->:")

        else:
            model = url

        if shared_functions.eporner_pattern.search(model):
            model = shared_functions.ep_client.get_pornstar(model, enable_html_scraping=True).videos(pages=10)

        elif shared_functions.xnxx_pattern.match(model):
            model = shared_functions.xn_client.get_user(model).videos

        elif shared_functions.pornhub_pattern.match(model):
            model = itertools.chain(shared_functions.ph_client.get_user(model).videos, shared_functions.ph_client.get_user(model).uploads)

        elif shared_functions.hqporner_pattern.match(model):
            model = shared_functions.hq_client.get_videos_by_actress(model)

        elif shared_functions.xvideos_pattern.match(model):
            if "/model" in model or "/pornstar" in model:
                model = shared_functions.xv_client.get_pornstar(model).videos

            else:
                logger.info("Model URL does not contain expected /model or /pornstar. Assuming it's a channel instead...")
                model = shared_functions.xv_client.get_channel(model).videos

        if do_return:
            return model

        self.iterate_generator(model, auto=auto, ignore_errors=ignore_errors, batch=batch)

    def process_playlist(self, url=None, auto=False, ignore_errors=False, batch=False):
        if url is None:
            url = input(f"{return_color()}Enter the (PornHub) playlist URL -->:")
        playlist = shared_functions.ph_client.get_playlist(url)
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
            self.iterate_generator(shared_functions.ph_client.search(query))

        elif website == "2":
            self.iterate_generator(shared_functions.hq_client.search_videos(query=query))

        elif website == "3":
            self.iterate_generator(shared_functions.xv_client.search(query))

        elif website == "4":
            self.iterate_generator(shared_functions.xn_client.search(query).videos)

        elif website == "5":
            self.iterate_generator(shared_functions.ep_client.search_videos(query, per_page=50,
                                                             sorting_order="", sorting_gay="", sorting_low_quality="",
                                                             enable_html_scraping=True, page=20))

    def process_file(self):
        videos = []
        file = input(f"{return_color()}Please enter the file path -->:")

        with open(file, "r") as file:
            content = file.read()
            content = content.splitlines()

        for line in content:
            if line.startswith("video#"):
                line = line.split("#")[1]
                try:
                    videos.append(shared_functions.check_video(is_url=True, url=line))

                except:
                    error = traceback.format_exc()
                    logger.error(f"Error in processing video: {line}, {error}")
                    print(f"Error in processing video: {line}, {error}")
                    continue

        logger.debug(f"{return_color()}Done!")
        self.iterate_generator(videos)

    def download(self, video, output_path, task_id, remove_total_bar=False):
        try:
            # Detect whether this is a byte-based download
            is_byte_download = (
                isinstance(video, shared_functions.hq_Video)
                or isinstance(video, shared_functions.ep_Video)
            )

            def callback_wrapper(pos, total):
                if is_byte_download:
                    tot_mb = (total / (1024 ** 2)) if total and total > 0 else None
                    comp_mb = (pos / (1024 ** 2))
                    if tot_mb is not None:
                        # avoid accidental 'finished' due to float/rounding
                        if comp_mb >= tot_mb:
                            comp_mb = tot_mb - 1e-6

                        self.progress.update(task_id, total=round(tot_mb), completed=round(comp_mb))
                    else:
                        # keep task indeterminate until we know total size
                        self.progress.update(task_id)
                else:
                    self.progress.update(task_id, total=total, completed=pos)
                    if self.task_total_progress is not None:
                        self.progress.update(self.task_total_progress, advance=1)

            # Kick off the right download call
            if isinstance(video, shared_functions.ph_Video):
                video.download(path=output_path,
                    quality=self.quality,
                    downloader=self.threading_mode,
                    display=callback_wrapper,
                    remux=remux)
            elif is_byte_download:
                # HQPorner / Eporner
                video.download(
                    path=output_path,
                    quality=self.quality,
                    callback=callback_wrapper,
                    no_title=True,
                )
            else:
                # other types (e.g. ep_Video/hq_Video fall through here if needed)
                video.download(
                    path=output_path,
                    quality=self.quality,
                    downloader=self.threading_mode,
                    callback=callback_wrapper,
                    remux=remux,
                    no_title=True,
                )

        finally:
            logger.debug(f"Finished download: {video.title}")
            if conf["Video"]["write_metadata"] == "true":
                if remux:
                    shared_functions.write_tags(
                        path=output_path,
                        data=shared_functions.load_video_attributes(video))


            # Release semaphore and log
            t = next((t for t in self.progress.tasks if t.id == task_id), None)
            if t and t.total is not None:
                self.progress.update(task_id, completed=t.total)
            self.finished_downloading += 1
            self.semaphore.release()
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTYELLOW_EX} Download finished: {video.title}")

            # Clean up the per-video bar; leave total bar intact for segments
            try:
                self.progress.remove_task(task_id)
                if remove_total_bar and not is_byte_download:
                    self.progress.remove_task(self.task_total_progress)
            except ValueError:
                pass

    def _update_progress(self):
        # Exit once every task is finished (no live tasks left).
        while not self._progress_stop.is_set():
            self.progress.refresh()
            time.sleep(0.1)


    @staticmethod
    def credits():
        content = BaseCore().fetch("https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/README/CREDITS.md")
        md = Markdown(content)
        rprint(md)



class Batch(CLI):
    def __init__(self):
        super().__init__()
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
            parser.add_argument("--add-model-to-database", help="A model URL that should be added to the database")
            parser.add_argument("--remove-model-from-database", help="A model URL that should be removed from the database")
            parser.add_argument("--update-models", help="Runs the model update function", action="store_true")
            parser.add_argument("--update-pending-urls", help="Updates the videos that need to be fetched from a model", action="store_true")

            args = parser.parse_args()

            if args.info:
                print(description)
                exit(0)

            if args.add_model_to_database:
                model_url = args.add_model_to_database
                add_model_url(model_url, path=STATE_FILE)
                exit(0)

            if args.remove_model_from_database:
                model_url = args.remove_model_from_database
                remove_model_url(model_url, path=STATE_FILE)
                exit(0)

            if args.update_pending_urls:
                update_pending_for_all_models(self.process_model, STATE_FILE)
                exit(0)

            if args.update_models:
                cli = CLI()
                cli.load_user_settings()
                cli.update_models()
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
                conf.read("config.ini")
                self.load_user_settings()

            except Exception as e:
                print(f"Error in loading configuration..., creating a new configuration file... Error:")
                logger.error(e)
                shared_functions.setup_config_file(force=True)
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





