"""
This file contains functions which are needed for the Graphical User Interface, as well as the CLI.
If you know what you do, you can change a few things here :)
"""

import os
import re
from mutagen.mp4 import MP4

from phub import Client, errors, Video
from phub.modules import download as ph_download
from colorama import Fore
from hue_shift import return_color, reset
from datetime import datetime
from configparser import ConfigParser
from hqporner_api.api import Client as hq_Client, Video as hq_Video
from eporner_api.eporner_api import Client as ep_Client, Video as ep_Video
from eporner_api.modules.locals import Category as ep_Category
from xnxx_api.xnxx_api import Client as xn_Client, Video as xn_Video
from xvideos_api.xvideos_api import Client as xv_Client, Video as xv_Video
from base_api.modules.download import FFMPEG as bs_ffmpeg, default as bs_default, threaded as bs_threaded
from base_api.modules.quality import Quality as bs_Quality
from ffmpeg_progress_yield import FfmpegProgress

"""
The following are the sections and options for the configuration file. Please don't change anything here, 
as they are indeed needed for the main applications!
"""

sections = ["Performance", "License", "Video", "UI"]
options_performance = ["semaphore", "threading_mode", "workers", "timeout", "retries"]
options_video = ["quality", "language", "output_path", "directory_system", "search_limit", "delay"]
options_license = ["accepted"]
options_ui = ["language"]

"""
Explanation:

Directory System:

1 = Yes
0 = No

Semaphore:

Integer value.

If you set it to 3, three videos will be downloaded at the same time (You get the point)

"""

default_configuration = f"""
[License]
accepted = no

[Performance]
threading_mode = threaded
semaphore = 2
workers = 20
timeout = 10
retries = 4

[Video]
quality = best
language = en
output_path = ./
directory_system = 0
search_limit = 50
delay = 0

[UI]
language = system
"""


def logger_error(e):
    print(f"{datetime.now()} : {Fore.LIGHTRED_EX}[ERROR] : {reset()} : {e}")


def logger_debug(e):
    print(f"{datetime.now()} : {Fore.LIGHTCYAN_EX}[DEBUG] : {return_color()} : {e} {reset()}")


def check_video(url, language, is_url=True, delay=False):

    if is_url:
        regex_eporner_url = re.compile(r"eporner.com/(.*?)")
        regex_xnxx_url = re.compile(r"xnxx.com(.*?)")
        regex_xvideos_url = re.compile(r'xvideos.com(.*?)')
        regex_hqporner_url = re.compile(r'hqporner.com/(.*?)')

        if regex_hqporner_url.search(str(url)):
            return hq_Client().get_video(url)

        elif regex_eporner_url.search(str(url)):
            return ep_Client().get_video(url, enable_html_scraping=True)

        elif regex_xnxx_url.search(str(url)):
            return xn_Client().get_video(url)

        elif regex_xvideos_url.search(str(url)):
            return xv_Client().get_video(url)

        if isinstance(url, Video):
            url.fetch("page@")
            return url

        elif isinstance(url, hq_Video):
            return url

        elif isinstance(url, ep_Video):
            return url

        elif isinstance(url, xn_Video):
            return url

        elif isinstance(url, xv_Video):
            return url

        elif isinstance(url, str) and not str(url).endswith(".html"):
            try:
                video = Client(language=language, delay=delay).get(url)
                video.fetch("page@")
                return video

            except Exception:
                return False

        else:
            return False

    else:
        pass

        # TODO


def strip_title(title):
    print(title)
    # Characters not allowed in Windows filenames
    illegal_chars = '<>:"/\\|?*'

    # Keep characters that are not in the list of illegal characters
    cleaned_title = ''.join(char for char in title if char not in illegal_chars)

    return cleaned_title


def setup_config_file(force=False):
    if os.path.isfile("config.ini") is False or force:
        logger_error("Configuration file is broken / not found. Automatically creating a new one with default "
                     "configuration")

        try:
            with open("config.ini", "w") as config_file:
                config_file.write(default_configuration)

        except PermissionError:
            logger_error("Can't write to config.ini due to permission issues.")
            exit(1)

    else:
        config = ConfigParser()
        config.read("config.ini")

        for idx, section in enumerate(sections):
            section_processed = False
            if config.has_section(section) and idx == 0:
                for option in options_performance:
                    if config.has_option(section=section, option=option):
                        pass

                    else:
                        setup_config_file(force=True)
                        break

                else:
                    section_processed = True

            if config.has_section(section) and idx == 1:
                for option in options_license:
                    if config.has_option(section=section, option=option):
                        pass

                    else:
                        setup_config_file(force=True)
                        break

                else:
                    section_processed = True

            if config.has_section(section) and idx == 2:
                for option in options_video:
                    if config.has_option(section=section, option=option):
                        pass

                    else:
                        setup_config_file(force=True)
                        break

                else:
                    section_processed = True

            if config.has_section(section) and idx == 3:
                for option in options_ui:
                    if config.has_option(section=section, option=option):
                        pass

                    else:
                        setup_config_file(force=True)
                        break

                else:
                    section_processed = True


def correct_output_path(output_path):
    if not str(output_path).endswith(os.sep):
        output_path += os.sep
        return output_path

    else:
        return output_path


def get_element_safe(list, index):
    """
    I need this for the metadata functions, because not always are all values in the actual list, which need to be
    extracted.
    """
    if 0 <= index < len(list):
        return list[index]
    else:
        return ""


def write_tags(path, video):
    title = video.title
    comment = "Downloaded with Porn Fetch (GPLv3)"
    genre = "Porn"
    if hasattr(video.author, "name"):
        artist = video.author.name

    else:
        artist = video.author if not isinstance(video.author, list) else video.author[0]

    if artist == "":
        artist = "Unknown"

    if hasattr(video, "date"):
        date = video.date.strftime("%Y/%m/%d")

    elif hasattr(video, "publish_date"):
        date = video.publish_date

    else:
        date = "Unknown"

    logger_debug("Tags [1/3]")

    audio = MP4(path)
    audio.tags["\xa9nam"] = title
    audio.tags["\xa9ART"] = artist
    audio.tags["\xa9cmt"] = comment
    audio.tags["\xa9gen"] = genre
    audio.tags["\xa9day"] = date

    logger_debug("Tags: [2/3]")
    audio.save()
    logger_debug("Tags: [3/3] ✔")


pornhub_pattern = re.compile(r'(.*?)pornhub.com(.*)')
hqporner_pattern = re.compile(r'(.*?)hqporner.com(.*)')
xnxx_pattern = re.compile(r'(.*?)xnxx.com(.*)')
xvideos_pattern = re.compile(r'(.*?)xvideos.com(.*)')
eporner_pattern = re.compile(r'(.*?)eporner.com(.*)')
