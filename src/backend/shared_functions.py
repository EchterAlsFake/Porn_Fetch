"""
This file contains functions which are needed for the Graphical User Interface, as well as the CLI.
If you know what you do, you can change a few things here :)
"""

import os
import re
import json
import logging
import http.client

from mutagen.mp4 import MP4, MP4Cover
from configparser import ConfigParser
from phub import Client, errors, Video, consts as phub_consts
from phub.modules import download as download
from ffmpeg_progress_yield import FfmpegProgress
from src.backend.config import shared_config
conf = shared_config

from base_api.base import BaseCore, setup_logger
from base_api.modules import consts as bs_consts
from hqporner_api import Client as hq_Client, Video as hq_Video
from xnxx_api import Client as xn_Client, Video as xn_Video
from xvideos_api import Client as xv_Client, Video as xv_Video
from eporner_api import Client as ep_Client, Video as ep_Video, Category as ep_Category # Used in the main file
from missav_api import Client as mv_Client, Video as mv_Video
from xhamster_api import Client as xh_Client, Video as xh_Video

# Initialize clients globally
client = Client()
hq_client = hq_Client()
ep_client = ep_Client()
xn_client = xn_Client()
xv_client = xv_Client()
mv_client = mv_Client()
xh_client = xh_Client()

logger = setup_logger(name="Porn Fetch - [shared_functions]", log_file="PornFetch.log", level=logging.DEBUG)


def refresh_clients():
    """
    Reinitializes all API clients with updated BaseCore settings.
    Call this after modifying consts.PROXY.
    """
    global hq_client, ep_client, xn_client, xv_client, client, xh_client, mv_client

    # Refresh BaseCore first
    BaseCore().initialize_session()

    import hqporner_api
    import xnxx_api
    import eporner_api
    import xvideos_api
    import xhamster_api
    import missav_api

    hqporner_api.api.refresh_core(enable_logging=True, log_file="hqporner_api.log", level=logging.DEBUG)
    xnxx_api.xnxx_api.refresh_core(enable_logging=True, log_file="xnxx_api.log", level=logging.DEBUG)
    eporner_api.refresh_core(enable_logging=True, log_file="eporner_api.log", log_level=logging.DEBUG)
    xvideos_api.xvideos_api.refresh_core(enable_logging=True, log_file="xvideos_api.log", level=logging.DEBUG)
    missav_api.missav_api.refresh_core(enable_logging=True, log_file="missav_api.log", level=logging.DEBUG)
    xhamster_api.xhamster_api.refresh_core(enable_logging=True, log_file="xhamster_api.log", level=logging.DEBUG)

    # Reinitialize all clients so they get a fresh BaseCore instance
    hq_client = hqporner_api.Client()
    ep_client = eporner_api.Client()
    xn_client = xnxx_api.Client()
    xv_client = xvideos_api.Client()
    xh_client = xhamster_api.Client()
    mv_client = missav_api.Client()

    hq_client.enable_logging(log_file="hqporner_api.log", level=logging.DEBUG)
    ep_client.enable_logging(log_file="eporner_api.log", level=logging.DEBUG)
    xv_client.enable_logging(log_file="xvideos_api.log", level=logging.DEBUG)

    client = Client()
    client.reset()
    logger.info(f"Initialized new sessions with Proxy value: {bs_consts.PROXY} | {phub_consts.PROXY}")


"""
The following are the sections and options for the configuration file. Please don't change anything here, 
as they are indeed needed for the main applications!
"""

# TODO: Implement logging
sections = ["Setup", "Performance", "PostProcessing", "Video", "UI", "Sponsoring", "Android"]

options_setup = ["license_accepted", "install", "update_checks", "internet_checks", "anonymous_mode", "disclaimer_shown"]
options_performance = ["semaphore", "threading_mode", "workers", "timeout", "retries", "ffmpeg_warning"]
options_post_processing = ["convert", "format", "write_metadata"]
options_video = ["quality", "output_path", "directory_system", "search_limit", "delay", "skip_existing_files", "model_videos"]
options_ui = ["language", "custom_font"]
options_sponsoring = ["downloaded_videos", "notice_shown"]
options_android = ["warning_shown"]


pornhub_pattern = re.compile(r'(.*?)pornhub(.*)') # can also be .org
hqporner_pattern = re.compile(r'(.*?)hqporner.com(.*)')
xnxx_pattern = re.compile(r'(.*?)xnxx.com(.*)')
xvideos_pattern = re.compile(r'(.*?)xvideos.com(.*)')
eporner_pattern = re.compile(r'(.*?)eporner.com(.*)')
missav_pattern = re.compile(r'(.*?)missav(.*?)')
xhamster_pattern = re.compile(r'(.*?)xhamster(.*?)')


default_configuration = f"""[Setup]
license_accepted = false
install = unknown
update_checks = true
internet_checks = true
anonymous_mode = false
disclaimer_shown = false

[Performance]
threading_mode = threaded
semaphore = 2
workers = 20
timeout = 10
retries = 4
ffmpeg_warning = true

[PostProcessing]
convert = true
format = mp4
write_metadata = true

[Video]
quality = best
output_path = ./
directory_system = false
search_limit = 50
delay = 0
skip_existing_files = true
model_videos = both

[UI]
language = system
custom_font = true

[Sponsoring]
downloaded_videos = 0
notice_shown = false

[Android]
warning_shown = false
"""

def send_error_log(message):
    """
    This function is made for the Android development of Porn Fetch and is used for debugging.
    You can, of course, change or remove it, but I wouldn't recommend it.
    """
    return
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

def check_video(url, is_url=True):
    if is_url:
        if hqporner_pattern.search(str(url)) and not isinstance(url, hq_Video):
            return hq_client.get_video(url)

        elif eporner_pattern.search(str(url)) and not isinstance(url, ep_Video):
            return ep_client.get_video(url, enable_html_scraping=True)

        elif xnxx_pattern.search(str(url)) and not isinstance(url, xn_Video):
            return xn_client.get_video(url)

        elif xvideos_pattern.search(str(url)) and not isinstance(url, xv_Video):
            return xv_client.get_video(url)

        elif missav_pattern.search(str(url)) and not isinstance(url, mv_Video):
            return mv_client.get_video(url)

        elif xhamster_pattern.search(str(url)) and not isinstance(url, xh_Video):
            return xh_client.get_video(url)

        if isinstance(url, Video):
            url.fetch("page@") # If url is a PornHub Video object it does have the `fetch` method
            return url

        elif isinstance(url, hq_Video):
            return url

        elif isinstance(url, ep_Video):
            return url

        elif isinstance(url, xn_Video):
            return url

        elif isinstance(url, xv_Video):
            return url

        elif isinstance(url, xh_Video):
            return url

        elif isinstance(url, mv_Video):
            return url


        elif isinstance(url, str) and not str(url).endswith(".html"):
            video = Client().get(url)
            video.fetch("page@")
            return video


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
            if idx == 0:
                for option in options_setup:
                    if not config.has_option(section, option):
                        setup_config_file(force=True)
                        print("ISSUE 1")

            if idx == 1:
                for option in options_performance:
                    if not config.has_option(section, option):
                        setup_config_file(force=True)
                        print("ISSUE 2")
            if idx == 2:
                for option in options_post_processing:
                    if not config.has_option(section, option):
                        setup_config_file(force=True)
                        print("ISSUE 3")

            if idx == 3:
                for option in options_video:
                    if not config.has_option(section, option):
                        setup_config_file(force=True)
                        print("ISSUE 4")

            if idx == 4:
                for option in options_ui:
                    if not config.has_option(section, option):
                        setup_config_file(force=True)
                        print("ISSUE 5")

            if idx == 5:
                for option in options_sponsoring:
                    if not config.has_option(section, option):
                        setup_config_file(force=True)
                        print("ISSUE 6")

            if idx == 6:
                for option in options_android:
                    if not config.has_option(section, option):
                        print(f"ISSUE 7, {section} {option}")
                        setup_config_file(force=True)



def load_video_attributes(video):
    title = video.title

    if isinstance(video, Video):
        try:
            author = video.author.name

        except Exception:
            author = video.pornstars[0]

        length = video.duration.seconds / 60
        tags = ",".join([tag.name for tag in video.tags])
        publish_date = video.date
        video.refresh()  # Throws an error otherwise. I have no idea why.
        thumbnail = video.image.url

    elif isinstance(video, xn_Video):
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
        tags = ",".join([category for category in video.tags])
        publish_date = video.publish_date
        try:
            thumbnail = video.get_thumbnails()[0]

        except TypeError:
            thumbnail = "Not available" # Expected, it's an error on HQPorners end.

    elif isinstance(video, mv_Video):
        author = "Not available"
        length = "Not available"
        tags = "Not available"
        thumbnail = video.thumbnail
        publish_date = video.publish_date

    elif isinstance(video, xh_Video):
        author = ",".join(video.pornstars)
        length = "Not available"
        tags = "Not available"
        thumbnail = video.thumbnail
        publish_date = "Not available"

    else:
        raise "Instance Error! Please report this immediately on GitHub!"

    data = {
        "title": title,
        "author": author,
        "length": parse_length(length), # Make sure the video duration is not something like 6.7777777779
        "tags": tags,
        "publish_date": publish_date,
        "thumbnail": thumbnail,
    }
    logger.debug(f"Loaded video data: {data}")

    return data


def write_tags(path, data: dict): # Using core from Porn Fetch to keep proxy support
    comment = "Downloaded with Porn Fetch (GPLv3)"
    genre = "Porn"

    title = data.get("title")
    artist = data.get("author")
    date = data.get("publish_date")
    thumbnail = data.get("thumbnail")
    logging.debug("Tags [1/3]")

    audio = MP4(path)
    audio.tags["\xa9nam"] = str(title)
    audio.tags["\xa9ART"] = str(artist)
    audio.tags["\xa9cmt"] = str(comment)
    audio.tags["\xa9gen"] = str(genre)
    audio.tags["\xa9day"] = str(date)

    logging.debug("Tags: [2/3] - Writing Thumbnail")

    try:
        content = BaseCore().fetch(url=thumbnail, get_bytes=True)
        cover = MP4Cover(content, imageformat=MP4Cover.FORMAT_JPEG)
        audio.tags["covr"] = [cover] # Yes, it needs to be in a list

    except Exception as e:
        logger.error("Could not download / write thumbnail into the metadata tags of the video. Please report the"
                     f"following error on GitHub: {e} - Image URL: {thumbnail}")

    audio.save()
    logging.debug("Tags: [3/3] ✔")


def parse_length(length, video_source=None):
    "Entirely written and copied from ChatGPT. My brain is not ready to fix that myself now, seriously..."
    """
    Parse a video length value and return its duration in minutes (rounded).

    Notes:
      - If length is already numeric (int/float), it is assumed to be in minutes.
      - If length is a string:
          * A string of the format "mm:ss" (e.g. "16:19") is parsed as minutes and seconds.
          * A digits-only string is treated based on the source:
              - If video_source contains "xnxx", then the value is already in minutes.
              - If video_source contains "eporner" or "phub", then the value is in seconds.
              - Otherwise, digits-only defaults to minutes.
          * A string with a decimal point is assumed to be a minute value.
          * If the string contains "min" (case-insensitive), the numeric part is extracted and used as minutes.
          * Otherwise, we try to extract components from mixed formats such as "59m 40s" or "24 seconds".
      - If no valid duration is found (or if the video source provides no length information),
        returns "Not available".

    In all conversions, if the computed minute value is > 0 but rounds to 0, returns 1 instead.
    """
    if length in (None, "", "Not available"):
        return "Not available"

    try:
        # If already numeric (non-string) assume minutes.
        if isinstance(length, (int, float)):
            # Ensure that a small positive value returns at least 1 minute.
            result = round(length)
            return result if result > 0 else (1 if length > 0 else 0)

        # Work with a stripped string.
        s = str(length).strip()

        # -------------------------------
        # Case 1: "mm:ss" format (e.g. "16:19")
        if ":" in s:
            parts = s.split(":")
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                minutes = int(parts[0])
                seconds = int(parts[1])
                total = minutes + seconds / 60.0
                result = round(total)
                if result == 0 and total > 0:
                    result = 1
                return result

        # -------------------------------
        # Case 2: Digits-only string.
        if s.isdigit():
            num = int(s)
            if video_source:
                src = str(video_source).lower()
                if "xnxx" in src:
                    # xnxx provides minutes directly.
                    return num
                elif "eporner" in src or "phub" in src:
                    # These sites give seconds; convert to minutes.
                    result = round(num / 60)
                    if result == 0 and num > 0:
                        result = 1
                    return result
                else:
                    # Default: assume minutes.
                    return num
            else:
                # Without a source hint, default to minutes.
                return num

        # -------------------------------
        # Case 3: Value with a decimal point (assumed to be minutes).
        if '.' in s:
            try:
                val = float(s)
                result = round(val)
                if result == 0 and val > 0:
                    result = 1
                return result
            except ValueError:
                pass

        # -------------------------------
        # Case 4: Contains "min" (e.g. "9 Min").
        if "min" in s.lower():
            num_str = ''.join(ch for ch in s if ch.isdigit() or ch == '.')
            if num_str:
                try:
                    val = float(num_str)
                    result = round(val)
                    if result == 0 and val > 0:
                        result = 1
                    return result
                except ValueError:
                    pass

        # -------------------------------
        # Case 5: Mixed time units such as "59m 40s" or "1h 2m 3s"
        time_units = {'s': 1 / 60, 'm': 1, 'h': 60}
        total_minutes = 0.0
        for part in s.split():
            # Extract numeric (or decimal) part and letter part.
            value_str = ''.join(ch for ch in part if ch.isdigit() or ch == '.')
            unit_str = ''.join(ch for ch in part if ch.isalpha()).lower()
            if value_str and unit_str in time_units:
                try:
                    total_minutes += float(value_str) * time_units[unit_str]
                except ValueError:
                    continue
        if total_minutes > 0:
            result = round(total_minutes)
            if result == 0 and total_minutes > 0:
                result = 1
            return result

        # -------------------------------
        # Case 6: Formats like "24 seconds"
        if s.endswith("seconds"):
            num_str = ''.join(ch for ch in s if ch.isdigit() or ch == '.')
            if num_str:
                try:
                    sec = float(num_str)
                    result = round(sec / 60)
                    if result == 0 and sec > 0:
                        result = 1
                    return result
                except ValueError:
                    pass

        # -------------------------------
        # Case 7: Formats ending with "min" (e.g. "17 min")
        if s.endswith("min"):
            num_part = s[:-3].strip()
            if num_part.isdigit():
                return int(num_part)

        # If nothing matches, return None.
        return None

    except Exception:
        return 0
