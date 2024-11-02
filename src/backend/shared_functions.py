"""
This file contains functions which are needed for the Graphical User Interface, as well as the CLI.
If you know what you do, you can change a few things here :)
"""

import os
import re
import logging
import http.client
import json

import requests
from mutagen.mp4 import MP4, MP4Cover
from phub import Client, errors, Video
from phub.modules import download as download
from colorama import Fore
from hue_shift import return_color, reset
from datetime import datetime
from configparser import ConfigParser
from hqporner_api import Client as hq_Client, Video as hq_Video
from eporner_api import Client as ep_Client, Video as ep_Video
from eporner_api.modules.locals import Category as ep_Category
from xnxx_api import Client as xn_Client, Video as xn_Video
from xvideos_api import Client as xv_Client, Video as xv_Video
from spankbang_api import Client as sp_Client, Video as sp_Video
from base_api import FFMPEG as bs_ffmpeg, default as bs_default, threaded as bs_threaded
from base_api.modules import consts
from base_api.modules.quality import Quality as bs_Quality
from ffmpeg_progress_yield import FfmpegProgress

"""
The following are the sections and options for the configuration file. Please don't change anything here, 
as they are indeed needed for the main applications!
"""

sections = ["Performance", "License", "Video", "UI"]
options_performance = ["semaphore", "threading_mode", "workers", "timeout", "retries", "ffmpeg_warning"]
options_video = ["quality", "output_path", "directory_system", "search_limit", "delay", "skip_existing_files",
                 "model_videos"]
options_license = ["accepted"]
options_ui = ["language", "design"]

pornhub_pattern = re.compile(r'(.*?)pornhub(.*)') # can also be .org
hqporner_pattern = re.compile(r'(.*?)hqporner.com(.*)')
xnxx_pattern = re.compile(r'(.*?)xnxx.com(.*)')
xvideos_pattern = re.compile(r'(.*?)xvideos.com(.*)')
eporner_pattern = re.compile(r'(.*?)eporner.com(.*)')
spankbang_pattern = re.compile(r'(.*?)spankbang.com(.*)')

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
ffmpeg_warning = true

[Video]
quality = best
output_path = ./
directory_system = 0
search_limit = 50
delay = 0
skip_existing_files = true
model_videos = both

[UI]
language = system
design = native
"""

logger = logging.getLogger(__name__)
do_not_log = False

def send_error_log(message):
    """
    This function is made for the Android development of Porn Fetch and is used for debugging.
    You can of course change or remove it, but I wouldn't recommend it.
    """

    if do_not_log is False:
        url = "192.168.0.19:8000"
        endpoint = "/error-log/"
        data = json.dumps({"message": message})
        headers = {"Content-type": "application/json"}

        conn = http.client.HTTPConnection(url)

        try:
            conn.request("POST", endpoint, data, headers)
            response = conn.getresponse()

            if response.status == 200:
                print("Error log sent successfully")
            else:
                print(f"Failed to send error log: Status {response.status}, Reason: {response.reason}")

            conn.close()
        except Exception as e:
            print(f"Request failed: {e}")

def check_video(url, is_url=True, delay=False):
    if is_url:

        if hqporner_pattern.search(str(url)):
            return hq_Client().get_video(url)

        elif eporner_pattern.search(str(url)):
            return ep_Client().get_video(url, enable_html_scraping=True)

        elif xnxx_pattern.search(str(url)):
            return xn_Client().get_video(url)

        elif xvideos_pattern.search(str(url)):
            return xv_Client().get_video(url)

        elif spankbang_pattern.search(str(url)):
            return sp_Client().get_video(url)

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

        elif isinstance(url, sp_Video):
            return url

        elif isinstance(url, str) and not str(url).endswith(".html"):
            try:
                video = Client(delay=delay).get(url)
                video.fetch("page@")
                return video

            except Exception:
                return False

        else:
            return False

    else:
        pass

        # TODO


def setup_config_file(force=False):
    if os.path.isfile("config.ini") is False or force:
        logger.warning("Configuration file is broken / not found. Automatically creating a new one with default "
                     "configuration")

        try:
            with open("config.ini", "w") as config_file:
                config_file.write(default_configuration)

        except PermissionError:
            logger.error("Can't write to config.ini due to permission issues.")
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


def load_video_attributes(video):
    title = video.title

    if isinstance(video, xn_Video):
        author = video.author
        length = video.length
        tags = video.tags
        publish_date = video.publish_date
        thumbnail = video.thumbnail_url[0]

    elif isinstance(video, xv_Video):
        author = video.author
        length = video.length
        tags = video.tags
        publish_date = video.publish_date
        thumbnail = video.thumbnail_url

    elif isinstance(video, Video):
        try:
            author = video.author.name

        except Exception:
            author = video.pornstars[0]

        length = video.duration.seconds / 60
        tags = ",".join([tag.name for tag in video.tags])
        publish_date = video.date
        video.refresh()  # Throws an error otherwise. I have no idea why.
        thumbnail = video.image.url

    elif isinstance(video, ep_Video):
        author = video.author
        length = video.length_minutes
        tags = ",".join([tag for tag in video.tags])
        publish_date = video.publish_date
        thumbnail = video.thumbnail

    elif isinstance(video, hq_Video):
        try:
            author = video.pornstars[0]
        except Exception:
            author = "No pornstars / author"  # This can sometimes happen. Very rarely, but can happen...

        length = video.length
        tags = ",".join([category for category in video.categories])
        publish_date = video.publish_date
        thumbnail = video.get_thumbnails()[0]

    elif isinstance(video, sp_Video):
        author = video.author
        _length = video.length.split(":")
        length_minutes = _length[0] + "m"
        length_seconds = _length[1] + "s"
        length = length_minutes + " " + length_seconds
        tags = ",".join([tag for tag in video.tags])
        publish_date = video.publish_date
        thumbnail = video.thumbnail

    data = [title, author, length, tags, publish_date, thumbnail]
    return data


def write_tags(path, video):
    data = load_video_attributes(video)
    comment = "Downloaded with Porn Fetch (GPLv3)"
    genre = "Porn"

    title = data[0]
    artist = data[1]
    date = data[3]
    thumbnail = data[5]
    logging.debug("Tags [1/3]")

    audio = MP4(path)
    audio.tags["\xa9nam"] = title
    audio.tags["\xa9ART"] = artist
    audio.tags["\xa9cmt"] = comment
    audio.tags["\xa9gen"] = genre
    audio.tags["\xa9day"] = date

    logging.debug("Tags: [2/3] - Writing Thumbnail")
    content = requests.get(thumbnail).content
    cover = MP4Cover(content, imageformat=MP4Cover.FORMAT_JPEG)
    audio.tags["covr"] = [cover]
    audio.save()
    logging.debug("Tags: [3/3] ✔")


def parse_length(length):
    try:
        # Check if length is a valid integer string representing minutes
        if isinstance(length, int) or (isinstance(length, str) and length.isdigit()):
            return int(length)

        # Check for decimal format like "9.3333334" which represents minutes and fractions of minutes
        if isinstance(length, float) or (isinstance(length, str) and '.' in length):
            try:
                return int(round(length))
            except ValueError:
                pass

        # Initialize a dictionary for time units conversion
        time_units = {'s': 1 / 60, 'm': 1, 'h': 60}
        total_minutes = 0

        # Split the length string by spaces
        parts = length.split()
        for part in parts:
            # Extract the numeric value and the time unit
            value = int(part[:-1])
            unit = part[-1]

            # Convert the value to minutes if the unit is valid
            if unit in time_units:
                total_minutes += value * time_units[unit]

        # If a valid time conversion was found, return the total minutes
        if total_minutes > 0:
            return total_minutes

        # Check for format ending with 'min'
        if length.endswith('min'):
            return int(length[:-3])

        # Check for format like '24 seconds'
        if length.endswith('seconds'):
            value = int(length.split()[0])
            return value / 60  # Convert seconds to minutes

        return None

    except Exception:
        return 0


def resolve_threading_mode(video, mode, workers, timeout):
    """Resolve the appropriate threading mode based on input."""
    if isinstance(video, Video):
        return {
            "threaded": download.threaded(max_workers=workers, timeout=timeout),
            "FFMPEG": download.FFMPEG,
            "default": download.default
        }.get(mode, download.default)

    else:
        return {
            "threaded": bs_threaded(max_workers=workers, timeout=timeout, retries=5),
            "FFMPEG": bs_ffmpeg,
            "default": bs_default
        }.get(mode, download.default)
