import os.path
import sys
import threading
import sentry_sdk
from colorama import *
from phub import *
from tqdm import tqdm
from configparser import ConfigParser
import getpass

o = '\033[33m'

try:
    from src.setup import internet_test, ask_for_sentry_cli, clear, check_path, strip_title, logging, setup_config_file

except ImportError:
    from setup import internet_test, ask_for_sentry_cli, clear, check_path, strip_title, logging, setup_config_file

__license__ = "GPL 3"

license_agreement = f"""
{Fore.RESET}GPL License Agreement for Porn Fetch
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
NO LIABILITY FOR END USER USE
Under no circumstances and under no legal theory, whether in tort, contract, or otherwise, shall the copyright holder or contributors be liable to You for any direct, indirect, special, incidental, consequential or exemplary damages of any character including, without limitation, damages for loss of goodwill, work stoppage, computer failure or malfunction, loss of data or any and all other commercial damages or losses, even if such party shall have been informed of the possibility of such damages.
This limitation of liability shall not apply to liability for death or personal injury resulting from such party’s negligence to the extent applicable law prohibits such limitation. Some jurisdictions do not allow the exclusion or limitation of incidental or consequential damages, so this exclusion and limitation may not apply to You.
This Agreement represents the complete agreement concerning the subject matter hereof.

1) Accept
2) Deny
--------------=>:"""
setup_config_file()

class CLI():

    def __init__(self):
        self.z = f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET}"
        self.x = f"{Fore.LIGHTRED_EX}[~]{Fore.RESET}"
        self.quality = Quality.BEST
        self.output_path = None
        self.threading_mode = None
        self.api_language = None
        self.custom_language = False
        self.login_status = f"{Fore.LIGHTRED_EX}Not logged in{Fore.RESET}"
        self.pbar = None
        self.delay = True
        self.conf = ConfigParser()
        self.conf.read("../config.ini")
        try:
            self.load_user_settings() # Needs to be initialized after the variables
        except KeyError:
            self.conf = ConfigParser()
            self.conf.read("config.ini")
            self.load_user_settings()

        self.client = Client(language=self.api_language, delay=self.delay)

        self.sentry = ask_for_sentry_cli()


        if internet_test():
            while True:
                self.menu()

    def callback(self, pos, total):
        self.pbar = tqdm(total=total, dynamic_ncols=True)
        self.pbar.update(pos - self.pbar.n)
        if pos == total:
            self.pbar.close()
            self.pbar = None

    def load_user_settings(self):

        if not self.conf["License"]["accept"] == "true":
            _ = input(license_agreement)

            with open("config.ini", "w") as config_file:

                if _ == "1":
                    self.conf.set("License", "accept", "true")
                    self.conf.write(config_file)

                elif _ == "2":
                    self.conf.set("License", "accept", "false")
                    self.conf.write(config_file)
                    exit(0)

                else:
                    logging(msg="License not accepted...", level="1")
                    exit(0)

        if self.conf["Porn_Fetch"]["default_quality"] == "best":
            self.quality = Quality.BEST

        elif self.conf["Porn_Fetch"]["default_quality"] == "half":
            self.quality = Quality.HALF

        elif self.conf["Porn_Fetch"]["default_quality"] == "Worst":
            self.quality = Quality.WORST

        if self.conf["Porn_Fetch"]["delay"] == "False":
            self.delay = False

        if self.conf["Porn_Fetch"]["hd"] == "true":
            self.hd = True

        elif self.conf["Porn_Fetch"]["hd"] == "false":
            self.hd = False

        self.production = self.conf["Porn_Fetch"]["production"]
        self.sort_time = self.conf["Porn_Fetch"]["sort_time"]
        self.sort = self.conf["Porn_Fetch"]["sort"]
        self.api_language = self.conf["Porn_Fetch"]["api_language"]
        self.threading_mode = self.conf["Porn_Fetch"]["default_threading"]
        self.output_path = self.conf["Porn_Fetch"]["default_path"]


    def check_video(self, url):
        try:
            self.client = Client(language=self.api_language, delay=self.delay)
            return self.client.get(url)

        except Exception as e:
            print(logging(msg=e, level="1"))
            if self.sentry:
                sentry_sdk.capture_exception(e)

    def settings(self):

        options = input(f"""
{Fore.LIGHTCYAN_EX}1) Change API Language
{Fore.LIGHTMAGENTA_EX}2) Change default output path
{Fore.LIGHTYELLOW_EX}3) Change default Quality
{Fore.LIGHTGREEN_EX}4) Change default Threading mode
{Fore.LIGHTMAGENTA_EX}5) Change API delay
{Fore.LIGHTCYAN_EX}6) Change search filters
{Fore.LIGHTWHITE_EX}7) Back
---------------------=>:""")

        with open("config.ini", "w") as config_file:

            if options == "1":

                option = input(f"""
Please enter your API language:     {Fore.LIGHTYELLOW_EX} !!! RESTART FOR CHANGES TO TAKE EFFECT !!!
{Fore.LIGHTGREEN_EX}de | {Fore.LIGHTBLUE_EX}Ge{Fore.LIGHTRED_EX}rm{Fore.LIGHTYELLOW_EX}n
{Fore.LIGHTCYAN_EX}en | English
{Fore.LIGHTYELLOW_EX}es | Spanish
{Fore.LIGHTMAGENTA_EX}ru | Russian
{Fore.LIGHTBLUE_EX}fr | French
{Fore.LIGHTGREEN_EX}1) set a custom language (may not work)
{Fore.LIGHTRED_EX}2) Back
---------------------=>:""")
                if option == "de" or "en" or "es" or "ru" or "fr":
                    self.conf.set("Porn_Fetch", "api_language", option)
                    self.conf.write(config_file)

                elif option == "1":
                    api_language = input(f"""
{self.z}{Fore.LIGHTCYAN_EX}Enter the language code --=>:""")
                    self.conf.set("Porn_Fetch", "api_language", api_language)


                elif option == "2":
                    self.settings()

                else:
                    print(f"{self.x}{Fore.LIGHTMAGENTA_EX}Wrong input. Please select the language code!")

            elif options == "2":
                output_path = input(f"{self.z}{Fore.LIGHTBLUE_EX}Please enter the new output path --=>:")
                if os.path.exists(output_path):
                    self.conf.set("Porn_Fetch", "default_path", output_path)
                    self.conf.write(config_file)

                else:
                    print(f"{self.x}{Fore.RESET}Invalid path.")

                self.settings()

            elif options == "3":
                option = f"""
{Fore.LIGHTGREEN_EX}1) Best
{o}2) Half
{Fore.LIGHTRED_EX}3) Worst
{Fore.LIGHTWHITE_EX}4) back
--------------------=>:"""

                if option == "1":
                    self.conf.set("Porn_Fetch", "default_quality", "best")
                    self.conf.write(config_file)

                elif option == "2":
                    self.conf.set("Porn_Fetch", "default_quality", "middle")
                    self.conf.write(config_file)

                elif option == "3":
                    self.conf.set("Porn_Fetch", "default_quality", "worst")
                    self.conf.write(config_file)

                elif option == "4":
                    self.settings()

                else:
                    print(f"{self.x}{Fore.RESET}Invalid input. Select in range 1 - 3")

            elif options == "4":
                option = input(f"""
{Fore.LIGHTGREEN_EX}1) Yes
{Fore.LIGHTRED_EX}2) No
{Fore.LIGHTWHITE_EX}3) back""")

                if option == "1":
                    self.conf.set("Porn_Fetch", "default_threading", "multiple")
                    self.conf.write(config_file)

                elif option == "2":
                    self.conf.set("Porn_Fetch", "default_threading", "single")
                    self.conf.write(config_file)

                elif option == "3":
                    self.settings()

                else:
                    print(f"{self.x}{Fore.RESET}Invalid input!")
                    self.settings()

            elif options == "5":

                option = input(f"""
{Fore.LIGHTRED_EX}1) Disable delay  : Can lead to more errors!
{Fore.LIGHTGREEN_EX}2) Set new delay (Default is 0.5 seconds)
{Fore.LIGHTYELLOW_EX}3) Back
{Fore.LIGHTWHITE_EX}-------------=>:""")

            elif options == "6":
                search_filter_menu = input(f"""
1) Change HD filter
2) Change production filter
3) Change time sort
4) Change general sort
5) Back
---------------------=>:
""")

                if search_filter_menu == "1":
                    hd_filter_options = input(f"""
1) Enable HD sorting
2) Disable HD sorting
3) Back
---------------------=>:""")

                    if hd_filter_options == "1":
                        self.conf.set("Porn_Fetch", "hd", "true")
                        self.conf.write(config_file)

                    elif hd_filter_options == "2":
                        self.conf.set("Porn_Fetch", "hd", "false")
                        self.conf.write(config_file)

                    elif hd_filter_options == "3":
                        self.settings()


                    else:
                        print(f"{self.x}{Fore.RESET}Invalid input. Select in range 1 - 3")


                elif search_filter_menu == "2":
                    production_filter_options = input(f"""
1) Enable professional sorting
2) Enable homemade sorting
3) Back
---------------------=>:""")

                    if production_filter_options == "1":
                        self.conf.set("Porn_Fetch", "production", "professional")
                        self.conf.write(config_file)

                    elif production_filter_options == "2":
                        self.conf.set("Porn_Fetch", "production", "homemade")
                        self.conf.write(config_file)

                    elif production_filter_options == "3":
                        self.settings()

                    else:
                        print(f"{self.x}{Fore.RESET}Invalid input. Select in range 1 - 3")


                elif search_filter_menu == "3":
                    time_options = input("""
1) Sort by Day
2) Sort by Week
3) Sort by Month
4) Sort by Year
5) Back
-------------------------=>:""")

                    if time_options == "1":
                        self.conf.set("Porn_Fetch", "sort_time", "day")
                        self.conf.write(config_file)

                    elif time_options == "2":
                        self.conf.set("Porn_Fetch", "sort_time", "week")
                        self.conf.write(config_file)

                    elif time_options == "3":
                        self.conf.set("Porn_Fetch", "sort_time", "month")
                        self.conf.write(config_file)

                    elif time_options == "4":
                        self.conf.set("Porn_Fetch", "sort_time", "year")
                        self.conf.write(config_file)

                    elif time_options == "5":
                        self.settings()

                    else:
                        print(f"{self.x}{Fore.RESET}Invalid input. Select in range 1 - 5")


                elif options == "4":
                    general_sort_options = input(f"""
1) Most relevant
2) Most recent
3) Most viewed
4) Top rated
5) longest
6) Back
----------------------=>:""")

                    if general_sort_options == "1":
                        self.conf.set("Porn_Fetch", "sort", "most relevant")
                        self.conf.write(config_file)

                    elif general_sort_options == "2":
                        self.conf.set("Porn_Fetch", "sort", "most recent")
                        self.conf.write(config_file)

                    elif general_sort_options == "3":
                        self.conf.set("Porn_Fetch", "sort", "most viewed")
                        self.conf.write(config_file)

                    elif general_sort_options == "4":
                        self.conf.set("Porn_Fetch", "sort", "top rated")
                        self.conf.write(config_file)

                    elif general_sort_options == "5":
                        self.conf.set("Porn_Fetch", "sort", "longest")
                        self.conf.write(config_file)

                    elif general_sort_options == "6":
                        self.settings()

                    else:
                        print(f"{self.x}{Fore.RESET}Invalid input. Select in range 1 - 6")

                elif options == "5":
                    self.settings()




            elif options == "7":
                self.menu()


    def menu(self):

        options = input(f"""
                SETTINGS    
{Fore.RESET}|---------------------------------------|
|   {Fore.LIGHTCYAN_EX}Threading{Fore.RESET}  : {self.threading_mode}  
|   {Fore.LIGHTGREEN_EX}Quality{Fore.RESET}    : {self.quality}        
|   {Fore.LIGHTMAGENTA_EX}API Delay{Fore.RESET}  : {self.delay}           
|   {Fore.LIGHTBLUE_EX}API Lang{Fore.RESET}   : {self.api_language}    
|   {Fore.LIGHTGREEN_EX}Output Path:{Fore.RESET} {self.output_path}     
|---------------------------------------|


{Fore.LIGHTCYAN_EX}1) Download a single Video
{Fore.LIGHTMAGENTA_EX}2) Download videos from a file
{Fore.LIGHTYELLOW_EX}3) Download all videos from a User / Channel
{Fore.LIGHTBLUE_EX}4) Get metadata from Videos
{Fore.LIGHTMAGENTA_EX}5) Search for videos and download them
{o}6) Account page
{Fore.LIGHTWHITE_EX}7) Settings
{Fore.LIGHTRED_EX}8) Credits
{Fore.LIGHTBLUE_EX}9) Exit
{Fore.RESET}-------------------->:{Fore.RESET} """)



        if options == "1":
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
            self.account_menu()

        elif options == "7":
            self.settings()

        elif options == "8":
            sys.exit(0)

    def raw_download(self, video):

        title = video.title
        title = strip_title(title)
        print(f"{self.z}{Fore.LIGHTMAGENTA_EX}Downloading: {Fore.RESET}{title}")

        try:
            video.download(path=self.output_path, callback=self.callback, quality=self.quality)
            print(f"{self.z}{Fore.LIGHTBLUE_EX}Download finished :) ")

        except Exception as e:
            logging(e, level="1")
            if self.sentry:
                sentry_sdk.capture_exception(e)

    def download_video(self, url):

        mode = self.threading_mode
        video = self.check_video(url)

        if mode == "single":
            self.raw_download(video)

        elif mode == "multiple":
            t = threading.Thread(target=self.raw_download, args=(video, ))
            print(f"{self.z}{Fore.RESET}Running Thread: {t.name}")
            t.start()

    def download_from_file(self):
        file = input(f"""
{self.z}{Fore.LIGHTYELLOW_EX}Path to URL file -->:""")

        with open(file, "r") as url_file:
            content = url_file.read().encode("utf-8").splitlines()

            total_urls = len(content)
            valid_urls = []
            titles = []

            print(f"{self.z}{Fore.LIGHTCYAN_EX}Found: {total_urls}")
            print(f"{self.z}{Fore.LIGHTMAGENTA_EX}Verifying URLs...")


            for url in tqdm(content):
                try:
                    video = self.check_video(url)
                    titles.append(video.title)
                    valid_urls.append(url)

                except Exception as e:
                    print(f"{self.x}{Fore.RESET}URL: {url} is invalid.")

            for counter, title in enumerate(titles, start=1):
                print(f"{counter}) {title}")

            chosen_titles = input(f"""
{self.z}{Fore.RESET}Enter the numbers you want to download (eg 1,2,3,4) --=>:""")
            chosen_titles = str(chosen_titles).split(",")

            chosen_urls = []

            for url_ in chosen_titles:
                url = valid_urls[int(url_)]
                chosen_urls.append(url)

            for _url in chosen_urls:
                self.download_video(_url)

    def download_channel_user(self):

        user = input(f"""
{self.z}{Fore.LIGHTMAGENTA_EX}Please enter the URL to the User / Model / Channel Account -->:""")

        user_object = self.client.get_user(user)

        videos = user_object.videos
        url_list = []
        titles = []

        for counter, title in enumerate(titles, start=1):
            print(f"{counter}) {title}")

        chosen_titles = input(f"""
        {self.z}{Fore.RESET}Enter the numbers you want to download (eg 1,2,3,4) --=>:""")
        chosen_titles = str(chosen_titles).split(",")

        chosen_urls = []

        for url_ in chosen_titles:
            url = url_list[int(url_)]
            chosen_urls.append(url)


        for _url in chosen_urls:
            self.download_video(_url)

    def get_metadata(self):

        url = input(f"""
{self.z}{Fore.LIGHTBLUE_EX}Please enter the URL of the video:""")

        print(f"{self.z}{Fore.LIGHTMAGENTA_EX}Getting metadata....")
        video = self.check_video(url)
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

        input(f"{Fore.RESET}Press ENTER to continue...")

    def search_ext_2(self, search):

        urls = []
        for count, video in enumerate(search):
            print(f"{count}) {video.title}")
            urls.append(video.url)

        downloads = input(Fore.RESET + "Enter the number of videos you want to download. Separate by comma e.g 1,7,12-->:")
        videos = downloads.split(",")

        for number in videos:
            base_url = "https://www.pornhub.com/"
            additional_url = urls[int(number)]
            url = base_url + additional_url
            self.download_video(url)

    def search_ext(self, search_query):

        try:
            search = self.client.search(search_query, production=self.production, time=self.sort_time, sort=self.sort, hd=self.hd)
            return search

        except ConnectionError:
            pass  # This is an issue from PornHub and not from my Application. I can not fix it anyway

    def search_videos(self):


        search_query = input(f"""
{self.z}{Fore.RESET}Please enter your search query -->:""")

        print(self.z + Fore.LIGHTMAGENTA_EX + "Searching....")
        search = self.search_ext(search_query)

        if len(search) == 0:
            print(f"{self.x}{Fore.LIGHTWHITE_EX}PornHub didn't return data. Trying automatic resolve.  Please higher the API delay in settings")
            print(f"{self.z}{Fore.LIGHTWHITE_EX}Trying a new initialization to the Client Object...")
            self.client = Client(language=self.api_language, delay=self.delay)

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

    def account_menu(self):

        options = input(f"""
{Fore.LIGHTGREEN_EX}1) Login   :                [ Status: {self.login_status} ]
{Fore.LIGHTYELLOW_EX}2) Get liked videos
{Fore.LIGHTCYAN_EX}3) Get watched videos
{o}4) Get recommendations
{Fore.LIGHTRED_EX}5) Back
---------------------------=>:""")

        if options == "1":
            self.login()

        elif options == "2":
            self.get_liked_videos()

        elif options == "3":
            self.get_watched_videos()

        elif options == "4":
            self.get_recommended_videos()

        elif options == "5":
            self.menu()

        else:
            print(f"{self.x}{Fore.RESET}Wrong input. Select in range 1 - 5 ")

    def login(self):

        username = input(f"""
{self.z}{Fore.RESET}Please enter your PornHub username --=>:""")
        password = getpass.getpass(f"""
{self.z}{Fore.RESET}Please enter your password --=>:""")

        try:
            self.client = Client(username=username, password=password, delay=self.delay, language=self.api_language)
            name = self.client.account.name
            self.login_status = f"{Fore.LIGHTGREEN_EX}Logged in as: {name}"
            print(f"{self.z}{Fore.LIGHTCYAN_EX}[SUCCESS]")
            self.account_menu()

        except Exception as e:
            if str(e) == "LogginFailed":
                logging(msg="Login failed. Check your credentials!", level="1")
                self.login()

            else:
                logging(msg=e, level="1")
                if self.sentry:
                    sentry_sdk.capture_exception(e)

    def get_liked_videos(self):

        liked_videos = self.client.account.liked
        video_list_url = []
        video_list_title = []

        for video in liked_videos:
            video_list_title.append(video.title)
            video_list_url.append(video.url)

        for counter, title in enumerate(video_list_title):
            print(f"{counter}) {title}")

        chosen_titles = input(f"""
{self.z}{Fore.RESET}Enter the videos you want to download (eg 1,2,3,4) --=>:""")

        _ = str(chosen_titles).split(",")

        for index in _:
            url = video_list_url[int(index)]
            self.download_video(url)

    def get_watched_videos(self):

        watched_videos = self.client.account.watched
        video_list_url = []
        video_list_title = []

        for video in watched_videos:
            video_list_title.append(video.title)
            video_list_url.append(video.url)

        for counter, title in enumerate(video_list_title):
            print(f"{counter}) {title}")

        chosen_titles = input(f"""
        {self.z}{Fore.RESET}Enter the videos you want to download (eg 1,2,3,4) --=>:""")

        _ = str(chosen_titles).split(",")

        for index in _:
            url = video_list_url[int(index)]
            self.download_video(url)

    def get_recommended_videos(self):

        recommended = self.client.account.recommended
        video_list_url = []
        video_list_title = []

        for video in recommended:
            video_list_title.append(video.title)
            video_list_url.append(video.url)

        for counter, title in enumerate(video_list_title):
            print(f"{counter}) {title}")

        chosen_titles = input(f"""
        {self.z}{Fore.RESET}Enter the videos you want to download (eg 1,2,3,4) --=>:""")

        _ = str(chosen_titles).split(",")

        for index in _:
            url = video_list_url[int(index)]
            self.download_video(url)

if __name__ == "__main__":
    CLI()
