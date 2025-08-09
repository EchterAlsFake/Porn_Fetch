"""
This file contains functions which are needed for the Graphical User Interface, as well as the CLI.
If you know what you do, you can change a few things here :)
"""

import os
import re
import logging

from hqporner_api.modules.errors import WeirdError

from src.backend.config import *
from urllib.parse import urlsplit
from mutagen.mp4 import MP4, MP4Cover
from base_api.base import BaseCore, setup_logger
from base_api.modules.config import RuntimeConfig
from phub import Client as ph_Client, errors, Video as ph_Video, consts as phub_consts
from hqporner_api import Client as hq_Client, Video as hq_Video
from xnxx_api import Client as xn_Client, Video as xn_Video
from xvideos_api import Client as xv_Client, Video as xv_Video
from eporner_api import Client as ep_Client, Video as ep_Video, Category as ep_Category # Used in the main file
from missav_api.missav_api import Video as mv_Video, Client as mv_Client
from xhamster_api import Client as xh_Client, Video as xh_Video
from spankbang_api import Client as sp_Client, Video as sp_Video
from base_api.modules.config import config # This is the global configuration instance of base core config
# which is also affecting all other APIs when the refresh_clients function is called
# Initialize clients globally, so that we can override them later with a new configuration from BaseCore if needed
mv_client = mv_Client()
ep_client = ep_Client()
ph_client = ph_Client()
xv_client = xv_Client()
xh_client = xh_Client()
sp_client = sp_Client()
hq_client = hq_Client()
xn_client = xn_Client()
core = BaseCore() # We need that sometimes in Porn Fetch's main class e.g., thumbnail fetching
core_ph = None
core_internet_checks = BaseCore(config=config, auto_init=True)

def refresh_clients(enable_kill_switch=False):
    global mv_client, ep_client, ph_client, xv_client, xh_client, sp_client, hq_client, xn_client, core, core_ph

    # One BaseCore per site, with its own RuntimeConfig (isolated headers/cookies)
    core_common = BaseCore(config=config, auto_init=True)   # if you want a “generic” core
    core_hq    = BaseCore(config=config, auto_init=True)
    core_mv    = BaseCore(config=config, auto_init=True)
    core_ep    = BaseCore(config=config, auto_init=True)
    core_ph    = BaseCore(config=config, auto_init=True)
    core_xv    = BaseCore(config=config, auto_init=True)
    core_xh    = BaseCore(config=config, auto_init=True)
    core_xn    = BaseCore(config=config, auto_init=True)
    core_sp    = BaseCore(config=config, auto_init=True)

    if enable_kill_switch:
        core_common.enable_kill_switch()
        core_hq.enable_kill_switch()
        core_mv.enable_kill_switch()
        core_ep.enable_kill_switch()
        core_ph.enable_kill_switch()
        core_xv.enable_kill_switch()
        core_xh.enable_kill_switch()
        core_xn.enable_kill_switch()

    # Instantiate clients with their site-specific cores
    mv_client = mv_Client(core=core_mv)
    ep_client = ep_Client(core=core_ep)
    ph_client = ph_Client(core=core_ph, use_webmaster_api=True)
    xv_client = xv_Client(core=core_xv)
    xh_client = xh_Client(core=core_xh)
    sp_client = sp_Client(core=core_sp)
    hq_client = hq_Client(core=core_hq)
    xn_client = xn_Client(core=core_xn)

    core = core_common

def origin(url: str) -> str:
    p = urlsplit(url)
    return f"{p.scheme}://{p.netloc}/"

def enable_logging(level=logging.DEBUG, log_file="APIs.log", log_ip=http_log_ip, log_port=http_log_port):
    global mv_client, ep_client, ph_client, xv_client, xh_client, sp_client, hq_client, xn_client
    pass # Need to implement that later lol

logger = setup_logger(name="Porn Fetch - [shared_functions]", log_file="PornFetch.log", level=logging.DEBUG, http_ip=http_log_ip, http_port=http_log_port)


"""
The following are the sections and options for the configuration file. Please don't change anything here, 
as they are indeed needed for the main applications!
"""

# TODO: Implement logging
sections = ["Setup", "Performance", "Video", "UI", "Sponsoring", "Android"]

options_setup = ["license_accepted", "install", "update_checks", "internet_checks", "anonymous_mode", "disclaimer_shown", "activate_logging", "first_run_cli"]
options_performance = ["semaphore", "threading_mode", "workers", "timeout", "retries", "speed_limit", "processing_delay"]
options_video = ["quality", "output_path", "directory_system", "result_limit", "delay", "skip_existing_files", "model_videos", "supress_errors",
                 "video_id_as_filename", "direct_download", "write_metadata"]
options_ui = ["language", "custom_font", "font_size"]
options_sponsoring = ["downloaded_videos", "notice_shown"]
options_android = ["warning_shown"]


pornhub_pattern = re.compile(r'(.*?)pornhub(.*)') # can also be .org
hqporner_pattern = re.compile(r'(.*?)hqporner.com(.*)')
xnxx_pattern = re.compile(r'(.*?)xnxx.com(.*)')
xvideos_pattern = re.compile(r'(.*?)xvideos.com(.*)')
eporner_pattern = re.compile(r'(.*?)eporner.com(.*)')
missav_pattern = re.compile(r'(.*?)missav(.*?)')
xhamster_pattern = re.compile(r'(.*?)xhamster(.*?)')
spankbang_pattern = re.compile(r'(.*?)spankbang(.*?)')


default_configuration = f"""[Setup]
license_accepted = false
install = unknown
update_checks = true
internet_checks = true
anonymous_mode = false
disclaimer_shown = false
activate_logging = not_set
first_run_cli = true

[Performance]
threading_mode = threaded
semaphore = 2
workers = 20
timeout = 10
retries = 4
speed_limit = 0
processing_delay = 0

[Video]
quality = best
output_path = ./
directory_system = false
result_limit = 50
delay = 0
skip_existing_files = true
model_videos = both
supress_errors = false
video_id_as_filename = false
direct_download = false
write_metadata = true

[UI]
language = system
custom_font = true
font_size = 14

[Sponsoring]
downloaded_videos = 0
notice_shown = false

[Android]
warning_shown = false
"""


def check_video(url, is_url=True):
    if is_url:
        if hqporner_pattern.search(str(url)) and not isinstance(url, hq_Video):
            print("Returning HQPorner Video! ")
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

        elif spankbang_pattern.search(str(url)) and not isinstance(url, sp_Video):
            return sp_client.get_video(url)

        if isinstance(url, ph_Video):
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

        elif isinstance(url, sp_Video):
            return url

        elif isinstance(url, str) and not str(url).endswith(".html"):
            video = ph_client.get(url) # PornHub client
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
                for option in options_video:
                    if not config.has_option(section, option):
                        print(f"Config mismatch: {section} | {option}")
                        setup_config_file(force=True)
                        print("ISSUE 4")

            if idx == 3:
                for option in options_ui:
                    if not config.has_option(section, option):
                        setup_config_file(force=True)
                        print("ISSUE 5")

            if idx == 4:
                for option in options_sponsoring:
                    if not config.has_option(section, option):
                        setup_config_file(force=True)
                        print("ISSUE 6")

            if idx == 5:
                for option in options_android:
                    if not config.has_option(section, option):
                        print(f"ISSUE 7, {section} {option}")
                        setup_config_file(force=True)



def load_video_attributes(video):
    title = video.title

    if isinstance(video, ph_Video):
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
        author = video.author.name
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
        print("In loading stuff")
        try:
            author = video.pornstars[0]
        except Exception:
            author = "No pornstars / author"  # This can sometimes happen. Very rarely, but can happen...

        length = video.length
        tags = ",".join([category for category in video.tags])
        publish_date = video.publish_date
        try:
            thumbnail = video.get_thumbnails()[0]

        except (TypeError, WeirdError):
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

    elif isinstance(video, sp_Video):
        author = video.author
        length = video.length
        tags = ",".join(video.tags)
        thumbnail = video.thumbnail
        publish_date = video.publish_date

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
