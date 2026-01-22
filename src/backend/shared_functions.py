"""
This file contains functions which are needed for the Graphical User Interface, as well as the CLI.
If you know what you do, you can change a few things here :)
"""

import os
import re
import sys
import json
import httpx
import sqlite3
import logging
import platform
import datetime
import traceback

from typing import Literal
from src.backend.config import __version__, http_log_ip, http_log_port, ConfigParser, __next_release__
from urllib.parse import urlsplit
from mutagen.mp4 import MP4, MP4Cover, MP4Tags
from base_api.base import BaseCore, setup_logger
from hqporner_api.modules.errors import WeirdError
from phub import Client as ph_Client, errors, Video as ph_Video, consts as phub_consts
from hqporner_api import Client as hq_Client, Video as hq_Video
from xnxx_api import Client as xn_Client, Video as xn_Video
from xvideos_api import Client as xv_Client, Video as xv_Video
from eporner_api import Client as ep_Client, Video as ep_Video, Category as ep_Category # Used in the main file
from missav_api.missav_api import Video as mv_Video, Client as mv_Client
from xhamster_api import Client as xh_Client, Video as xh_Video
from spankbang_api import Client as sp_Client, Video as sp_Video
from youporn_api.youporn_api import Client as yp_Client, Video as yp_Video
from porntrex_api.porntrex_api import Client as pt_Client, Video as pt_Video
from xfreehd_api.xfreehd_api import Client as xf_Client, Video as xf_Video
from beeg_api.beeg_api import Client as bg_Client, Video as bg_Video
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
yp_client = yp_Client()
bg_client = bg_Client()
pt_client = pt_Client()
xf_client = xf_Client()
core = BaseCore() # We need that sometimes in Porn Fetch's main class e.g., thumbnail fetching
core_update_checks = BaseCore()
core_ph = None
core_internet_checks = BaseCore(config=config)

core_update_checks.config.max_retries = 1
core_update_checks.config.use_http2 = False
core_update_checks.config.timeout = 10


def normalized_arch() -> str:
    m = platform.machine().lower()
    if m in ("x86_64", "amd64"):
        return "x86_64"
    if m in ("arm64", "aarch64"):
        return "arm64"

    else:
        logger.warning(f"Couldn't normalize platform: {m}, please report this")
        return m

class VideoData:
    """
    This class stores the video objects and their loaded data across Porn Fetch.
    It allows for re-fetching data if needed, update data if needed and handles caching thanks to
    a dictionary.

    (Okay, I am overhyping it a bit, but yeah, let's put that away xD)
    """

    data_objects = {}
    consistent_data = {}  # This dictionary stores other important data which will be re-used for the entire
    # run of Porn Fetch

    """
    If a video object isn't used anymore e.g., the video finished downloading or the tree widget was loaded with other
    videos, than those videos will be cleaned up in the dictionary, to be as memory and performance efficient as
    possible.
    """

    def clean_dict(self, video_titles):
        if not isinstance(video_titles, list):  # In case we only have one video title to delete
            video_titles = [video_titles]

        for video_title in video_titles:
            del self.data_objects[video_title]  # Del is faster than pop :)


def send_to_server(message: dict):
    try:
        response = httpx.post(
            url="https://echteralsfake.me/report",
            json=message,
            timeout=20)

        if response.status_code == 200:
            return(f"The error / feedback was successfully reported! Thanks :)")

        elif response.status_code == 500:
            return("An internal server error occurred. I am probably already fixing this.")

    except Exception:
        error = traceback.format_exc()
        return(f"Couldn't report to server due to error -->: {error}")


def handle_error_gracefully(self, data: dict, error_message: str | dict, needs_network_log: bool= False, is_feedback=False):
    if is_feedback:
        send_to_server(message=error_message)
        return

    self.logger.error(error_message)
    if not data.get("supress_errors") is True:
        self.signals.error_signal.emit(error_message)

    if needs_network_log:
        if data.get("activate_logging"):
            self.logger.info(f"Logging Error: {error_message} to network server...")
            message = f"""
            An error occurred in Porn Fetch!
            Time: {datetime.datetime.now()}
            Version: {__version__}
            System: {sys.platform}
            Error message: {error_message}
            """
            payload = {"message": message}
            send_to_server(message=payload)

        else:
            self.logger.info("Logging is disabled. Error will NOT be reported!")


def refresh_clients(enable_kill_switch=False):
    global mv_client, ep_client, ph_client, xv_client, xh_client, sp_client, \
        hq_client, xn_client, core, core_ph, yp_client, bg_client, pt_client, xf_client

    # One BaseCore per site, with its own RuntimeConfig (isolated headers/cookies)
    core_common = BaseCore(config=config)   # if you want a “generic” core
    core_hq    = BaseCore(config=config)
    core_mv    = BaseCore(config=config)
    core_ep    = BaseCore(config=config)
    core_ph    = BaseCore(config=config)
    core_xv    = BaseCore(config=config)
    core_xh    = BaseCore(config=config)
    core_xn    = BaseCore(config=config)
    core_sp    = BaseCore(config=config)
    core_yp    = BaseCore(config=config)
    core_bg    = BaseCore(config=config)
    core_pt    = BaseCore(config=config)
    core_xf    = BaseCore(config=config)

    if enable_kill_switch:
        core_common.enable_kill_switch()
        core_hq.enable_kill_switch()
        core_mv.enable_kill_switch()
        core_ep.enable_kill_switch()
        core_ph.enable_kill_switch()
        core_xv.enable_kill_switch()
        core_xh.enable_kill_switch()
        core_xn.enable_kill_switch()
        core_yp.enable_kill_switch()
        core_bg.enable_kill_switch()
        core_pt.enable_kill_switch()
        core_xf.enable_kill_switch()

    # Instantiate clients with their site-specific cores
    mv_client = mv_Client(core=core_mv)
    ep_client = ep_Client(core=core_ep)
    ph_client = ph_Client(core=core_ph, use_webmaster_api=True)
    xv_client = xv_Client(core=core_xv)
    xh_client = xh_Client(core=core_xh)
    sp_client = sp_Client(core=core_sp)
    hq_client = hq_Client(core=core_hq)
    xn_client = xn_Client(core=core_xn)
    yp_client = yp_Client(core=core_yp)
    bg_client = bg_Client(core=core_bg)
    pt_client = pt_Client(core=core_pt)
    xf_client = xf_Client(core=core_xf)

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
sections = [ "Misc", "Performance", "Video", "UI"]

options_misc = ["app_name", "debug_mode", "first_run_gui", "license_accepted", "install_type", "update_checks", "internet_checks", "anonymous_mode", "disclaimer_shown",
                "network_logging", "first_run_cli", "downloaded_videos", "notice_shown", "android_warning_shown", "supress_errors"]
options_performance = ["download_mode", "semaphore", "videos_concurrency", "pages_concurrency", "download_workers",
                       "timeout", "retries", "speed_limit", "processing_delay", "network_delay"]
options_video = ["quality", "model_videos", "result_limit", "output_path", "video_id_as_filename", "write_metadata",
                 "skip_existing_files", "track_videos", "database_path", "directory_system"]
options_ui = ["language", "font_size", "theme"]


default_configuration = f"""
[Misc]
app_name = none
debug_mode = false
first_run_gui = true
license_accepted = false
install_type = unknown
update_checks = true
internet_checks = true
anonymous_mode = false
disclaimer_shown = false
network_logging = false
first_run_cli = true
downloaded_videos = 0
notice_shown = false
android_warning_shown = false
supress_errors = false

[Performance]
download_mode = 0
semaphore = 1
videos_concurrency = 10
pages_concurrency = 2
download_workers = 20
timeout = 10
retries = 4
speed_limit = 0
processing_delay = 0
network_delay = 0

[Video]
quality = 6
model_videos = 0
result_limit = 50
output_path = ./
video_id_as_filename = false
write_metadata = true
skip_existing_files = true
track_videos = false
database_path = ./downloads.db
directory_system = false

[UI]
language = 0
font_size = 10
theme = 0
"""

def check_video(url):
    objects = [hq_Video, ep_Video, xn_Video, xv_Video, mv_Video, xh_Video, sp_Video, yp_Video, bg_Video, pt_Video, xf_Video]

    if isinstance(url, tuple(objects)):
        return url

    else:
        if isinstance(url, str) and len(url) > 0 and url.startswith("http"):
            if "pornhub" in url:
                return ph_client.get(url)

            if "hqporner" in url:
                return hq_client.get_video(url)

            elif "eporner" in url:
                return ep_client.get_video(url, enable_html_scraping=True)

            elif "xnxx" in url:
                return xn_client.get_video(url)

            elif "xvideos" in url:
                return xv_client.get_video(url)

            elif "missav" in url:
                return mv_client.get_video(url)

            elif "xhamster" in str(url) and "moments" in str(url) and not isinstance(url, xh_Video):
                return xh_client.get_short(url)

            elif "xhamster" in url:
                return xh_client.get_video(url)

            elif "spankbang" in url:
                return sp_client.get_video(url)

            elif "youporn" in url:
                return yp_client.get_video(url)

            elif "beeg.com" in str(url):
                return bg_client.get_video(url)

            elif "porntrex" in str(url):
                return pt_client.get_video(url)

            elif "xfreehd" in str(url):
                return xf_client.get_video(url)

            else:
                return False


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
                for option in options_misc:
                    if not config.has_option(section, option):
                        print(f"Configuration mismatch: {section} -> {option}")
                        setup_config_file(force=True)

            if idx == 1:
                for option in options_performance:
                    if not config.has_option(section, option):
                        print(f"Configuration mismatch: {section} -> {option}")
                        setup_config_file(force=True)

            if idx == 2:
                for option in options_video:
                    if not config.has_option(section, option):
                        print(f"Configuration mismatch: {section} -> {option}")
                        setup_config_file(force=True)


            if idx == 3:
                for option in options_ui:
                    if not config.has_option(section, option):
                        print(f"Configuration mismatch: {section} -> {option}")
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
        video_id = video.id

    elif isinstance(video, xn_Video):
        author = video.author
        length = video.length
        tags = video.tags
        publish_date = video.publish_date
        thumbnail = video.thumbnail_url[0]
        video_id = video.title

    elif isinstance(video, xv_Video):
        author = video.author.name
        length = video.length
        tags = video.tags
        publish_date = video.publish_date
        thumbnail = video.thumbnail_url
        video_id = video.title

    elif isinstance(video, ep_Video):
        author = video.author
        length = video.length_minutes
        tags = ",".join([tag for tag in video.tags])
        publish_date = video.publish_date
        thumbnail = video.thumbnail
        video_id = video.video_id

    elif isinstance(video, hq_Video):
        try:
            author = video.pornstars[0]
        except Exception:
            author = "No pornstars / author"  # This can sometimes happen. Very rarely, but can happen...

        length = video.length
        tags = ",".join([category for category in video.tags])
        publish_date = video.publish_date
        video_id = video.title
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
        video_id = video.video_code

    elif isinstance(video, yp_Video):
        author = video.author.name
        length = round(int(video.length) // 60)
        tags = ",".join(video.categories)
        thumbnail = video.thumbnail
        publish_date = video.publish_date
        video_id = video.title

    elif isinstance(video, xh_Video):
        author = ",".join(video.pornstars)
        length = "Not available"
        tags = "Not available"
        thumbnail = video.thumbnail
        publish_date = "Not available"
        video_id = video.title

    elif isinstance(video, sp_Video):
        author = video.author
        length = round(int(video.length) // 60)
        tags = ",".join(video.tags)
        thumbnail = video.thumbnail
        publish_date = "Not available"
        video_id = video.title

    elif isinstance(video, bg_Video):
        author = "Not available"
        length = round(int(video.duration // 60))
        tags = "Not available"
        thumbnail = "Not available"
        publish_date = "Not available"
        video_id = video.video_id

    elif isinstance(video, pt_Video):
        author = video.author
        length = video.duration
        tags = video.tags
        thumbnail = video.thumbnail
        publish_date = video.publish_date
        video_id = video.video_id

    elif isinstance(video, xf_Video):
        author = video.author
        length = video.length
        tags = video.tags
        thumbnail = video.thumbnail
        publish_date = video.publish_date
        video_id = video.title

    else:
        raise "Instance Error! Please report this immediately on GitHub!"

    data_bytes = None

    try:
        logger.info(f"Fetching Thumbnail for: {title}")
        if not thumbnail == "Not available":
            if "hqporner" in thumbnail:
                core.session.headers["Referer"] = "https://www.hqporner.com/"
            data_bytes = core.fetch(thumbnail, get_bytes=True)  # <- returns bytes

    except:
        error = traceback.format_exc()
        logger.error(f"An error occurred when fetching Thumbnail for: {title}: {error}")
        data_bytes = None

    finally:
        # remove header if present (no KeyError)
        try:
            core.session.headers.pop("Referer", None)

        except AttributeError:
            pass

    data = {
        "title": title,
        "author": author,
        "length": parse_length(length), # Make sure the video duration is not something like 6.7777777779
        "tags": tags,
        "publish_date": publish_date,
        "thumbnail": thumbnail,
        "url": video.url,
        "thumbnail_data": data_bytes,
        "video_id": video_id
    }
    logger.debug(f"Successfully loaded video data for: {title}")

    return data

def save_video_metadata(video_id, data, database_path: str):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO videos (video_id, url, title, author, length, tags, publish_date, thumbnail)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        video_id,
        data.get("url"),
        data.get("title"),
        data.get("author"),
        data.get("length"),
        json.dumps(data.get("tags")),  # store tags list as JSON
        data.get("publish_date"),
        data.get("thumbnail")
    ))
    conn.commit()
    conn.close()

def init_db(database_path: str):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT UNIQUE,
            url TEXT,
            title TEXT,
            author TEXT,
            length INTEGER,
            tags TEXT,
            publish_date TEXT,
            thumbnail TEXT,
            downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def write_tags(path, data: dict):
    comment   = "Downloaded with Porn Fetch (GPLv3)"
    genre     = "Porn"
    title     = data.get("title")
    artist    = data.get("author")
    date      = data.get("publish_date")  # e.g. "2025-10-26" or "2025"
    thumbnail = data.get("thumbnail_data")

    logging.debug("Tags [1/3]")

    audio = MP4(path)

    # Ensure an 'ilst' tag container exists
    if audio.tags is None:
        try:
            audio.add_tags()          # preferred; creates empty MP4Tags
        except Exception:
            pass
    if audio.tags is None:
        audio.tags = MP4Tags()        # fallback for older/env-specific builds

    # Write basic text tags (skip Nones)
    if title  is not None:  audio.tags["\xa9nam"] = str(title)
    if artist is not None:  audio.tags["\xa9ART"] = str(artist)
    if comment is not None: audio.tags["\xa9cmt"] = str(comment)
    if genre  is not None:  audio.tags["\xa9gen"] = str(genre)
    if date   is not None:  audio.tags["\xa9day"] = str(date)

    logging.debug("Tags: [2/3] - Writing Thumbnail")

    # Optional: embed cover art if it's JPEG/PNG
    if thumbnail:
        try:
            # Heuristically choose cover format
            if thumbnail.startswith(b"\x89PNG\r\n\x1a\n"):
                fmt = MP4Cover.FORMAT_PNG
            else:
                # JPEG has many possible headers; default to JPEG if not PNG
                fmt = MP4Cover.FORMAT_JPEG

            cover = MP4Cover(thumbnail, imageformat=fmt)
            audio.tags["covr"] = [cover]  # must be a list
        except Exception as e:
            logging.error(
                "Could not embed thumbnail: %s - Image URL: %s", e, thumbnail
            )

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
        s_lower = s.lower()

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
        # NEW Case 4a: "<value>min <value>sec/seconds" (e.g. "247min 02sec")
        # Supports: min|mins|minute|minutes and sec|secs|second|seconds (any case), spaces optional.
        m = re.search(
            r'(?i)\b(\d+(?:\.\d+)?)\s*(?:min|mins|minute|minutes)\s*(\d+(?:\.\d+)?)\s*(?:sec|secs|second|seconds)\b',
            s
        )
        if m:
            minutes = float(m.group(1))
            seconds = float(m.group(2))
            total = minutes + seconds / 60.0
            result = round(total)
            if result == 0 and total > 0:
                result = 1
            return result

        # -------------------------------
        # Case 4: Contains "min" (e.g. "9 Min")
        if "min" in s_lower:
            # Extract only the first contiguous number near 'min' to avoid picking up trailing seconds.
            # This keeps existing behavior for strings like "17 min".
            # If seconds are present, the regex case above will have returned already.
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
        # (Extended to accept long-form units too.)
        time_units = {
            's': 1 / 60, 'sec': 1 / 60, 'secs': 1 / 60, 'second': 1 / 60, 'seconds': 1 / 60,
            'm': 1, 'min': 1, 'mins': 1, 'minute': 1, 'minutes': 1,
            'h': 60, 'hr': 60, 'hrs': 60, 'hour': 60, 'hours': 60
        }
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
        if s_lower.endswith("second") or s_lower.endswith("seconds") or s_lower.endswith("sec") or s_lower.endswith(
                "secs"):
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
        if s_lower.endswith("min") or s_lower.endswith("mins") or s_lower.endswith("minute") or s_lower.endswith(
                "minutes"):
            # Pull the leading number(s)
            m_only = re.search(r'(\d+(?:\.\d+)?)', s)
            if m_only:
                val = float(m_only.group(1))
                result = round(val)
                if result == 0 and val > 0:
                    result = 1
                return result

        # If nothing matches, return None.
        return None

    except Exception:
        return 0

