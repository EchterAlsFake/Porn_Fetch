import sys
import time
import threading

import sentry_sdk
from colorama import *
from phub import *
from tqdm import tqdm
try:
    from src.setup import internet_test, ask_for_sentry_cli, clear, check_path, strip_title

except ImportError:
    from setup import internet_test, ask_for_sentry_cli, clear, check_path, strip_title

__license__ = "GPL 3"
credits_lol = f"""
Porn Fetch is created and maintained by EchterAlsFake | Johannes Habel.
EchterAlsFake is the internet pseudonym for Johannes Habel.

Porn Fetch comes 'AS IS' without any warranty or liability. 
You are responsible for your actions, but you get a few rights in exchange:

You are free to copy, modify, distribute and sell this software.
The software is licensed under the GPL 3.

The official Source code is available on GitHub:

https://github.com/EchterAlsFake/Porn_Fetch

This software uses some external libraries that are out of my control.

These are:

tqdm
pyside6
phub
colorama
sentry sdk

Graphics:

Download Icon : https://icons8.com/icon/104149/herunterladen
Search Icon : https://icons8.com/icon/aROEUCBo74Il/suche
Settings Icon : https://icons8.com/icon/52146/einstellungen
C Icon : https://icons8.com/icon/Uehg4gyVyrUo/copyright
M Icon By Unicons Font on Icon Scout : https://iconscout.com/icons/medium : https://iconscout.com/contributors/unicons
: https://iconscout.com
Checkmark Icon : https://www.iconsdb.com/barbie-pink-icons/checkmark-icon.html

A special thanks to Egsagon for creating PHUB.
This project would not be possible without his great API and I have much respect for him!

1.9 - 2023
"""

class CLI():

    def __init__(self):
        self.z =f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET}"
        self.x = f"{Fore.LIGHTRED_EX}[~]{Fore.RESET}"
        self.quality = Quality.BEST
        self.output_path = "./"
        self.threading_mode = "multiple"
        self.client = Client(language="en")
        self.video = None
        self.pbar = None
        self.sentry = ask_for_sentry_cli()


        if internet_test():
            while True:
                self.menu()

    def callback(self, **kwargs):

        def _update_progress(pos, total):

            self.pbar = tqdm(total=total, dynamic_ncols=True)
            self.pbar.update(pos - self.pbar.n)
            if pos == total:
                self.pbar.close()
                self.pbar = None

        return _update_progress

    def check_video(self, url):

        try:
            self.video = self.client.get(url)
            return True

        except IndexError:

            print(f"{self.x}{Fore.RESET}Video object returned no data. You got probably limited by PornHub. ")
            print(f"{self.z}{Fore.LIGHTCYAN_EX}Trying automatic reconnect...")

            self.client = Client("en")
            try:
                self.check_video(url)

            except IndexError:
                print(f"{self.x}{Fore.RESET}Didn't work.  Waiting 60 seconds before next attempt...")
                time.sleep(60)
                self.check_video(url)

        except Exception as e:
            self.exception(e)
            if self.sentry:
                sentry_sdk.capture_exception(e)
                print(f"{self.z}{Fore.LIGHTCYAN_EX}Sentry successfully captured the exception. I am working on it :) ")


    def exception(self, e):
        print(f"{self.x}Unhandled Exception: {e}")

    def menu(self):

        if self.quality == Quality.BEST:
            quality_ext = f"{Fore.LIGHTCYAN_EX}Best"

        elif self.quality == Quality.MIDDLE:
            quality_ext = f"{Fore.LIGHTMAGENTA_EX}Middle"

        elif self.quality == Quality.WORST:
            quality_ext = f"{Fore.LIGHTRED_EX}Worst"

        options = input(f"""
{Fore.LIGHTYELLOW_EX}    Settings:
{Fore.LIGHTWHITE_EX}|----------------------|
{Fore.LIGHTCYAN_EX}|99) Change Quality     | {Fore.RESET}Currently set to: {quality_ext}
{Fore.LIGHTMAGENTA_EX}|98) Set output path    {Fore.RESET}| Currently set to: {self.output_path}
{Fore.LIGHTYELLOW_EX}|97) Set Threading mode | {Fore.RESET}Currently set to: {self.threading_mode}
{Fore.RESET}|----------------------|


{Fore.LIGHTCYAN_EX}1) Download a single Video
{Fore.LIGHTMAGENTA_EX}2) Download videos from a file
{Fore.LIGHTYELLOW_EX}3) Download all videos from a User / Channel
{Fore.LIGHTBLUE_EX}4) Get metadata from Videos
{Fore.LIGHTMAGENTA_EX}5) Search for videos and download them
{Fore.LIGHTWHITE_EX}6) Show credits
{Fore.LIGHTRED_EX}7) Exit
{Fore.RESET}-------------------->:{Fore.RESET} """)


        if options == "99":
            self.change_quality()

        elif options == "98":
            self.set_output_path()

        elif options == "97":
            self.set_threading_mode()

        elif options == "1":
            url = input(f"""
{self.z}{Fore.LIGHTCYAN_EX}Please enter the video URL --->:""")
            self.download_video(url)

        elif options == "2":
            self.download_from_file()

        elif options == "3":
            self.download_channel_user()

        elif options == "4":
            self.get_metadata()

        elif options == "5":
            self.search_videos()

        elif options == "6":
            print(f"{Fore.RESET}{credits_lol}")

        elif options == "7":
            sys.exit(0)

    def change_quality(self):

        options = input(f"""
{Fore.LIGHTGREEN_EX}1) Change Quality to best
{Fore.LIGHTMAGENTA_EX}2) Change Quality to middle
{Fore.LIGHTRED_EX}3) Change Quality to worst
{Fore.LIGHTWHITE_EX}4) Go back
{Fore.LIGHTYELLOW_EX}----------->:{Fore.RESET}""")

        if options == "1":
            self.quality = Quality.BEST
            print(f"{self.z}✓")

        elif options == "2":
            self.quality = Quality.MIDDLE
            print(f"{self.z}✓")

        elif options == "3":
            self.quality = Quality.WORST
            print(f"{self.z}✓")

        elif options == "4":
            self.menu()

        else:
            print(f"{self.x}Wrong option. Please enter in range 1-4")
            self.change_quality()

    def set_output_path(self):
        output = input("""
Please enter the new output path.  Make sure to put a / at the end -->:""")
        self.output_path = output
        print(self.z + "✓")

    def set_threading_mode(self):
        options = input(f"""
{Fore.LIGHTMAGENTA_EX}1) Single threaded mode (downloads everything one by one)
{Fore.LIGHTCYAN_EX}2) Multiple threaded mode (downloads multiple videos at once)
{Fore.LIGHTWHITE_EX}3) Go back
{Fore.LIGHTYELLOW_EX}------------------------>:{Fore.RESET}""")

        try:
            if options == "1":
                self.threading_mode = "single"

            elif options == "2":
                self.threading_mode = "multiple"

            elif options == "3":
                    self.menu()

            else:
                print(f"{self.x}Wrong Input. Select in range 1-3")
                self.set_threading_mode()

        finally:
            clear()

    def raw_download(self, video):

        title = video.title
        title = strip_title(title)
        print(f"{self.z}{Fore.LIGHTMAGENTA_EX}Downloading: {Fore.RESET}{title}")

        try:
            video.download(path=self.output_path, callback=self.callback, quality=self.quality)
            print(f"{self.z}{Fore.LIGHTBLUE_EX}Download finished :) ")

        except Exception as e:
            self.exception(e)

    def download_video(self, url):

        mode = self.threading_mode
        output_path = self.output_path
        time.sleep(2) # You can set it to 0 if you want.  Read further down for additional information
        self.check_video(url) # Video will be assigned in this function. You probably ask why, so here a little explanation:

        """
        The API from Egsagon is not very good optimized. Also he doesn't maintain it actively and PornHub is also a really bad
        platform for writing an API. So the API video objects are sometimes returning Index Errors, because some 
        data from PornHub is not returned as it should. The only way to get around this, is to initialize the client from 
        time to time and refresh the video object. This doesn't prevent the error, but it let's it happen less.
        If you don't want the delay, you can just remove it from the code. It won't break the program.
        In case, the API gets more stable, I will also remove it, but this is the only solution for now.
        """

        if not check_path(output_path):
            print(f"{self.x}{Fore.RESET}The Output path, you submitted is wrong. You will be redirected to change it!")
            self.set_output_path()


        else:
            video = self.video

            if mode == "single":
                self.raw_download(video)

            elif mode == "multiple":
                t = threading.Thread(target=self.raw_download, args=(video, ))
                print(f"{self.z}{Fore.RESET}Running Thread: {t.name}")
                t.start()

    def download_from_file(self):

        print(f"""
            {Fore.LIGHTCYAN_EX}INFORMATION

{Fore.LIGHTWHITE_EX}The file needs to be in the following format:

URL (After the URL, make a new line!
URL
URL etc....

Do NOT separate them with commas or anything else. Just with a new line. Should be easy enough :) 
""")

        file = input(f"""
{self.z}{Fore.LIGHTYELLOW_EX}Path to URL file -->:""")

        with open(file, "r") as url_file:
            content = url_file.read().encode("utf-8").splitlines()

            total_urls = len(content)
            valid_urls = []
            counter = 0

            print(f"{self.z}{Fore.LIGHTCYAN_EX}Found: {total_urls}")
            print(f"{self.z}{Fore.LIGHTMAGENTA_EX}Verifying URLs...")

            for url in tqdm(content):

                counter += 1
                self.check_video(url)
                valid_urls.append(url)


            print(self.z + Fore.LIGHTMAGENTA_EX + f"Downloading: {len(valid_urls)} Videos...")
            for url in valid_urls:
                self.download_video(url)

    def download_channel_user(self):

        user = input(f"""
{self.z}{Fore.LIGHTMAGENTA_EX}Please enter the URL to the User / Model / Channel Account -->:""")

        user_object = self.client.get_user(user)

        videos = user_object.videos
        url_list = []
        for video in videos:
            url_list.append(video.url)

        print(f"{self.z}{Fore.GREEN}Found: {len(url_list)} Videos.")
        x = input(f"{Fore.RESET}Hit enter to download them all or B to go back")

        if x == "B" or x == "b":
            self.menu()

        else:
            for url in url_list:
                self.download_video(url)

    def get_metadata(self):

        url = input(f"""
{self.z}{Fore.LIGHTBLUE_EX}Please enter the URL of the video:""")

        print(self.z + Fore.LIGHTMAGENTA_EX + "Getting metadata....")
        self.check_video(url)

        video = self.video
        title = video.title
        likes_up = video.like.up
        likes_down = video.like.down
        image_url = video.image_url
        tags = video.tags
        tag_list = []

        for tag in tags:
            tag_list.append(tag.name)

        author = video.author.name
        views = video.views
        date = video.date
        duration = video.duration
        hotspots = video.hotspots
        likes = f"Likes: {likes_up} | Dislikes: {likes_down}"

        print(f"""
{Fore.RESET}
Title: {title}
Rating: {likes}
Image URL: {image_url}
Tags: {str(tag_list).strip("[").strip("]")}
Author: {author}
Views: {views}
Date: {date}
Duration: {duration}
Hotspots: {hotspots}
-- END --""")

        input(f"{Fore.RESET}Hit enter to continue...")

    def search_ext_2(self, search):

        urls = []
        for count, video in enumerate(search):
            print(f"{count}) {video.title}")
            urls.append(video.url)

        downloads = input(
            Fore.RESET + "Enter the number of videos you want to download. Separate by comma e.g 1,7,12-->:")
        videos = downloads.split(",")

        for number in videos:
            base_url = "https://www.pornhub.com/"
            additional_url = urls[int(number)]
            url = base_url + additional_url
            self.download_video(url)

    def search_ext(self, search_query):

        try:
            search = self.client.search(search_query)
            return search

        except ConnectionError:
            pass  # This is an issue from PornHub and not from my Application. I can not fix it anyway

    def search_videos(self):


        search_query = input(f"""
{self.z}{Fore.RESET}Please enter your search query -->:""")

        print(self.z + Fore.LIGHTMAGENTA_EX + "Searching....")
        search = self.search_ext(search_query)

        if len(search) == 0:
            print(f"{self.x}{Fore.LIGHTWHITE_EX}You got limited by the API! Wait a few minutes or change your IP and try again")
            print(f"{self.z}{Fore.LIGHTWHITE_EX}Trying a new initialization to the Client Object...")
            self.client = Client(language="en")

            try:
                search = self.client.search(search_query)

            except ConnectionError:
                pass

            if len(search) == 0:
                print(f"{self.x}{Fore.LIGHTMAGENTA_EX}Failed.  Sorry, you need to wait or use a VPN.")
                self.menu()

            else:
                self.search_ext_2(search)

        else:
            self.search_ext_2(search)

if __name__ == "__main__":
    try:
        CLI()

    except KeyboardInterrupt:
        print("Bye :)")

