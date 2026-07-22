"""
This file will handle all network clients and allow for refreshing and creating session objects.
This is important, because Porn Fetch will dynamically need to update the different website APIs
for example if you apply a proxy.

If I only use one specific file that handles everything, it's easier to manage it, because I have more control
where I import stuff from.

I know this might seem a bit confusing if you read this the first time, but if you look at the `eaf_base_api` module
and the other Porn APIs and how they are working together, then you will definitely understand why this matters.
"""
"""
Current APIs:

1) PHUB           -> https://pornhub.com (ph_client, ph_video)
2) xnxx           -> https://xnxx.com (xn_client, xn_video)
3) xvideos        -> https://xvideos.com (xv_client, xv_video)
4) eporner        -> https://eporner.com (ep_client, ep_video)
5) xhamster       -> https://xhamster.com (xh_client, xh_video)
6) spankbang      -> https://spankbang.com (sp_client, sp_video)
7) youporn        -> https://youporn.com (yp_client, yp_video)
8) beeg           -> https://beeg.com (bg_client, bg_video)
9) redtube        -> https://redtube.com (rt_client, rt_video)
10) thumbzilla    -> https://thumbzilla.com (th_client, th_video)
11) tube8         -> https://tube8.com (tu_client, tu_video)
12) xfreehd       -> https://xfreehd.com (xf_client, xv_video)
13) porntrex      -> https://porntrex.com (pt_client, pt_video)
"""

import os
import re
import logging
import asyncio
import inspect
import tempfile
import traceback


try:
    from src.backend.handle_ssl import build_ssl_context

except (ModuleNotFoundError, ImportError):
    from handle_ssl import build_ssl_context

from errors import InvalidInput
from urllib.parse import urlparse
from dataclasses import dataclass
from base_api.modules.config import config # This is the global configuration instance of base core config
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, timezone
from typing import Any, List, TypeAlias, Optional, Dict
from pornhub_api import Client as ph_Client, Video as ph_Video
from xnxx_api import Client as xn_Client, Video as xn_Video
from beeg_api import Client as bg_Client, Video as bg_Video
from xvideos_api import Client as xv_Client, Video as xv_Video
from xfreehd_api import Client as xf_Client, Video as xf_Video
from eporner_api import Client as ep_Client, Video as ep_Video
from porntrex_api import Client as pt_Client, Video as pt_Video
from tube8_api import Client as tu_Client, Video as tu_Video
from thumbzilla_api import Client as th_Client, Video as th_Video
from xhamster_api import Client as xh_Client, Video as xh_Video
from redtube_api import Client as rt_Client, Video as rt_Video
from spankbang_api import Client as sp_Client, Video as sp_Video
from youporn_api import Client as yp_Client, Video as yp_Video
from base_api import BaseCore
from src.backend.errors import SomethingStupidHappened
from base_api.modules.logger import configure_app_logging
from base_api.modules.static_functions import normalize_quality_value, choose_quality_from_list, strip_title
# Note, the Video instances are mostly used in `shared_functions.py`
AllowedVideoType: TypeAlias = (
    type[ph_Video] | type[xn_Video] | type[xv_Video] | type[yp_Video] | type[tu_Video] |
    type[xh_Video] | type[sp_Video] | type[bg_Video] | type[rt_Video] | type[th_Video]
    # Those are all HLS streams
)

AllowedVideoType_Legacy: TypeAlias = (
    type[xf_Video] | type[ep_Video] | type[pt_Video] | type[pt_Video]
    # Those are all non HLS streams for now
)

AnyVideoClass: TypeAlias = AllowedVideoType | AllowedVideoType_Legacy

_RELATIVE_RE = re.compile(
    r"^\s*(?P<num>\d+)\s*(?P<unit>second|minute|hour|day|week|month|year)s?\s+ago\s*$",
    re.IGNORECASE,
)

_PUBLISHED_ON_RE = re.compile(
    r"^\s*published\s+on\s+(?P<date>.+?)\s*$",
    re.IGNORECASE,
)

_TEMPLATE_RE = re.compile(r"\$(\w+)|\$\{([^}]+)}")

_NOT_AVAILABLE_RE = re.compile(r"^\s*(not\s+available|n/?a|none|null)?\s*$", re.IGNORECASE)
logger = configure_app_logging(logger_name="Porn Fetch - [Clients]", level=logging.DEBUG, log_file="PornFetch.log")

SITE_PATTERNS = [
    ("pornhub", re.compile(r"(?:^|\.)pornhub(?:premium)?\.[a-z.]{2,}$", re.IGNORECASE)),
    ("xnxx", re.compile(r"(?:^|\.)xnxx\d*\.[a-z.]{2,}$", re.IGNORECASE)),
    ("xvideos", re.compile(r"(?:^|\.)xvideos\d*\.[a-z.]{2,}$", re.IGNORECASE)),
    ("eporner", re.compile(r"(?:^|\.)eporner\.[a-z.]{2,}$", re.IGNORECASE)),
    ("xhamster", re.compile(r"(?:^|\.)xhamster(?:live)?\d*\.[a-z.]{2,}$", re.IGNORECASE)),
    ("spankbang", re.compile(r"(?:^|\.)spankbang\.[a-z.]{2,}$", re.IGNORECASE)),
    ("youporn", re.compile(r"(?:^|\.)youporn\.[a-z.]{2,}$", re.IGNORECASE)),
    ("beeg", re.compile(r"(?:^|\.)beeg\.[a-z.]{2,}$", re.IGNORECASE)),
    ("redtube", re.compile(r"(?:^|\.)redtube\.[a-z.]{2,}$", re.IGNORECASE)),
    ("thumbzilla", re.compile(r"(?:^|\.)thumbzilla\.[a-z.]{2,}$", re.IGNORECASE)),
    ("tube8", re.compile(r"(?:^|\.)tube8\.[a-z.]{2,}$", re.IGNORECASE)),
    ("xfreehd", re.compile(r"(?:^|\.)xfreehd\.[a-z.]{2,}$", re.IGNORECASE)),
    ("porntrex", re.compile(r"(?:^|\.)porntrex\.[a-z.]{2,}$", re.IGNORECASE)),
    ("xhamster_shorts", re.compile(r"(?=.*xhamster)(?=.*moments)", re.IGNORECASE))
]

# which is also affecting all other APIs when the refresh_clients function is called
# Initialize clients globally, so that we can override them later with a new configuration from BaseCore if needed
core = BaseCore(configuration=config)
core_ep = BaseCore(configuration=config)
core_ph = BaseCore(configuration=config)
core_xv = BaseCore(configuration=config)
core_xh = BaseCore(configuration=config)
core_xn = BaseCore(configuration=config)
core_sp = BaseCore(configuration=config)
core_yp = BaseCore(configuration=config)
core_bg = BaseCore(configuration=config)
core_pt = BaseCore(configuration=config)
core_xf = BaseCore(configuration=config)
core_rt = BaseCore(configuration=config)
core_th = BaseCore(configuration=config)
core_tu = BaseCore(configuration=config)

ep_client = ep_Client(core=core_ep)
xv_client = xv_Client(core=core_xv)
xh_client = xh_Client(core=core_xh)
sp_client = sp_Client(core=core_sp)
xn_client = xn_Client(core=core_xn)
yp_client = yp_Client(core=core_yp)
bg_client = bg_Client(core=core_bg)
pt_client = pt_Client(core=core_pt)
xf_client = xf_Client(core=core_xf)
ph_client = ph_Client(core=core_ph)
rt_client = rt_Client(core=core_rt)
th_client = th_Client(core=core_th)
tu_client = tu_Client(core=core_tu)

cores = [
    core_ep, core_ph, core_xv, core_xh, core_xn, core_sp, core_yp, core_bg, core_pt, core_xf, core_rt, core_th,
    core_tu,
]

video_objects = [ep_Video, xv_Video, xh_Video, sp_Video, xn_Video, yp_Video, bg_Video, pt_Video, xf_Video, ph_Video,
           rt_Video, th_Video, tu_Video]

for _core in cores:
    _core.initialize_session()

logger.debug("Successfully initialized all clients and!")


def refresh_clients(debug_mode: bool = False) -> None:
    logger.info("Refreshing all clients!")
    level = logging.DEBUG if debug_mode else logging.INFO
    core.enable_logging(level=level, log_file="BaseCore.log" if debug_mode else None)
    core_ep.enable_logging(level=level, log_file="BaseCore_EP.log" if debug_mode else None)
    core_ph.enable_logging(level=level, log_file="BaseCore_PH.log" if debug_mode else None)
    core_xv.enable_logging(level=level, log_file="BaseCore_XV.log" if debug_mode else None)
    core_xh.enable_logging(level=level, log_file="BaseCore_XH.log" if debug_mode else None)
    core_xn.enable_logging(level=level, log_file="BaseCore_XN.log" if debug_mode else None)
    core_sp.enable_logging(level=level, log_file="BaseCore_SP.log" if debug_mode else None)
    core_yp.enable_logging(level=level, log_file="BaseCore_YP.log" if debug_mode else None)
    core_bg.enable_logging(level=level, log_file="BaseCore_BG.log" if debug_mode else None)
    core_pt.enable_logging(level=level, log_file="BaseCore_PT.log" if debug_mode else None)
    core_xf.enable_logging(level=level, log_file="BaseCore_XF.log" if debug_mode else None)
    core_rt.enable_logging(level=level, log_file="BaseCore_RT.log" if debug_mode else None)
    core_tu.enable_logging(level=level, log_file="BaseCore_Tu.log" if debug_mode else None)
    core_th.enable_logging(level=level, log_file="BaseCore_TH.log" if debug_mode else None)

    cores_to_update = {
        core, core_ep, core_ph, core_xv, core_xh, core_xn, core_sp,
        core_yp, core_bg, core_pt, core_xf, core_rt, core_th, core_tu
    }

    clients_list = [
        ep_client, ph_client, xv_client, xh_client, sp_client, xn_client,
        yp_client, bg_client, pt_client, xf_client, rt_client, th_client, tu_client
    ]

    for client in clients_list:
        cores_to_update.add(client.core)

    for c in cores_to_update:
        old_session = c.session
        c.initialize_session()
        if old_session is not None and c.session is not None:
            try:
                c.session.cookies.update(old_session.cookies)

            except Exception as e:
                logger.warning(f"Couldn't copy cookies during session refresh: {e}")

    logger.debug("Applied in-place clients!")


async def get_video(url: str | AnyVideoClass) -> AnyVideoClass:
    """
    This function check the URL and generates the corresponding video object with the correct client.
    If the url is already a video object, the function will simply return it.
    """
    if isinstance(url, tuple(video_objects)):
        return url

    if not isinstance(url, str):
        raise SomethingStupidHappened

    if not url.startswith("http"):
        raise InvalidInput

    mapping = {
        "pornhub": await ph_client.get_video(url=url, load_html=True, load_api=True),
        "eporner": await ep_client.get_video(url=url, load_html=True, load_api=True),
        "xnxx": await xn_client.get_video(url=url, load_html=True),
        "xvideos": await xv_client.get_video(url=url, load_html=True),
        "xhamster": await xh_client.get_video(url=url, load_html=True),
        "xhamter_short": await xh_client.get_short(url=url, load_html=True),
        "spankbang": await sp_client.get_video(url=url, load_html=True),
        "youporn": await yp_client.get_video(url=url, load_html=True),
        "beeg": await bg_client.get_video(url=url),
        "porntrex": await pt_client.get_video(url=url),
        "xfreehd": await xf_client.get_video(url=url),
        "redtube": await rt_client.get_video(url=url),
        "thumbzilla": await th_client.get_video(url=url),
        "tube8": await tu_client.get_video(url=url),
    }

    final_website = None
    hostname = urlparse(url).hostname
    for website, pattern in SITE_PATTERNS:
        if pattern.search(hostname):
            final_website = website

    if not final_website:
        raise InvalidInput

    return mapping[final_website]


async def load_video_attributes(video: AnyVideoClass) -> dict:
    title = video.title

    if isinstance(video, ph_Video):
        stuff = await video.author
        author = stuff.name
        length = video.duration
        tags = video.tags
        publish_date = video.publish_date
        thumbnail = video.thumbnail
        video_id = video.video_id

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

    elif isinstance(video, yp_Video):
        stuff = await video.author(load_html=True)
        author = stuff.name
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

    elif isinstance(video, (rt_Video, tu_Video, th_Video)):
        author = video.author_name
        length = video.duration
        try:
            tags = video.action_tags

        except AttributeError:
            tags = "Not Available"
        thumbnail = video.thumbnail
        video_id = video.video_id
        publish_date = "Unknown"

    else:
        raise SomethingStupidHappened

    qualities = await get_available_qualities(video)  # [144, 240, 360, ...]

    # Normalize publish date into UTC datetime (optional extra field)
    publish_dt_utc = parse_publish_date(publish_date)
    title = strip_title(title)

    return {
        "title": title,
        "author": author,
        "length": length,
        "tags": tags,
        "thumbnail": thumbnail,
        "video_id": video_id,
        "publish_date": publish_dt_utc,
        "qualities": qualities
    }


async def get_direct_url_legacy(video: AllowedVideoType_Legacy, quality: str | int):
    """
    Since the non HLS downloads now support resuming by getting the current filesize
    and appending missing bytes, we need a way in Porn Fetch to actually see if a file is incomplete.

    If we don't do this, the skip existing files feature wouldn't work or I would need to find another
    more complex implementation for this.

    This helper function basically just gets the direct download URL for a given quality based on each API
    that uses mp4 streams.
    """

    if isinstance(video, xf_Video):
        if quality > "480p" or quality > 480 or quality == "best" or quality == "half": # Bro pls don't ask :rose:
            try:
                return video.cdn_urls[1]

            except IndexError:
                return video.cdn_urls[0]

        return video.cdn_urls[0]

    elif isinstance(video, pt_Video):
        qn = normalize_quality_value(quality)
        chosen_height = choose_quality_from_list(video.video_qualities, qn)

        result = video.direct_download_urls
        if inspect.iscoroutine(result):
            direct_urls = await result

        else:
            direct_urls = result

        quality_url_map = {int(re.search(r'(\d{3,4})', q).group(1)): url for q, url in zip(await video.video_qualities, direct_urls)}
        download_url = f"https://{quality_url_map[chosen_height]}"
        return download_url # Uhhh

    elif isinstance(video, ep_Video):
        return video.direct_download_link(quality=quality, mode="h264") # Pls don't download AV1, thank you
        # NO I won't spend half on hour to handle this edge case where one video on this whole platform might not have
        # A h264 stream bro

    return "MakesNoSense"


async def get_available_qualities(video: Any) -> List[int]:
    """
    Returns sorted unique qualities worst->best as ints.
    Works for:
      - HLS videos: video.m3u8_base_url + video.core.list_available_qualities()
      - Legacy videos: video.video_qualities (e.g. ["360", "480", "720"])
    """
    # ---- HLS (m3u8) ----
    m3u8_url = getattr(video, "m3u8_base_url", None)
    if m3u8_url:
        try:
            if hasattr(video, "core"):
                heights = await video.core.list_available_qualities(m3u8_url)  # your existing function

            else:
                heights = await video.client.core.list_available_qualities(m3u8_url)

            return sorted({int(h) for h in heights if h is not None})
        except Exception:
            error = traceback.format_exc()
            print(error)
            return []

    # ---- Legacy ----
    # Your legacy wrapper already exposes `video_qualities` as list[str]
    if isinstance(video, ep_Video):
        quals = video.video_qualities()

    else:
        quals = getattr(video, "video_qualities", None)

    if quals:
        try:
            return sorted({int(q) for q in quals})
        except Exception:
            return []

    return []

def _safe_getattr(obj: Any, attr: str) -> Any:
    try:
        return getattr(obj, attr)
    except Exception:
        return None

def resolve_path(context: Dict[str, Any], path: str) -> Any:
    """
    Resolve 'title' or 'author.name' or 'video.some_attr' from context.
    """
    cur: Any = context
    for part in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            cur = _safe_getattr(cur, part)
        if cur is None:
            return None
    return cur


def parse_publish_date(value: str) -> Optional[datetime]:
    if value is None:
        return None

    s = str(value).strip()
    if _NOT_AVAILABLE_RE.match(s):
        return None

    now_utc = datetime.now(timezone.utc)
    if now_utc.tzinfo is None:
        now_utc = now_utc.replace(tzinfo=timezone.utc)
    else:
        now_utc = now_utc.astimezone(timezone.utc)

    # 1) Relative: "7 days ago", "4 months ago", etc.
    m = _RELATIVE_RE.match(s)
    if m:
        num = int(m.group("num"))
        unit = m.group("unit").lower()

        if unit in ("second", "minute", "hour", "day", "week"):
            seconds = {
                "second": 1,
                "minute": 60,
                "hour": 3600,
                "day": 86400,
                "week": 7 * 86400,
            }[unit]
            return now_utc - timedelta(seconds=num * seconds)

        # month/year need calendar arithmetic
        if relativedelta is None:
            raise ImportError(
                "Parsing 'months ago'/'years ago' requires python-dateutil. "
                "Install with: pip install python-dateutil"
            )

        if unit == "month":
            return now_utc - relativedelta(months=num)
        if unit == "year":
            return now_utc - relativedelta(years=num)

    # 2) "Published on September 17, 2024"
    m = _PUBLISHED_ON_RE.match(s)
    if m:
        s = m.group("date").strip()

    # 3) Try ISO 8601 (handles "2025-10-17T22:56:30+00:00")
    # datetime.fromisoformat also accepts "YYYY-MM-DD" and "YYYY-MM-DD HH:MM:SS" in many cases.
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            # Assume naive timestamps are UTC. Change this if you prefer local time.
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        pass

    # 4) Try common long-form date (after stripping "Published on")
    # Example: "September 17, 2024"
    for fmt in ("%B %d, %Y", "%b %d, %Y"):
        try:
            dt = datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue

    return None


def write_tags(path: str, data: VideoAttributes):
    """
    Writes the tags of the video into the file using PyAV.
    """
    try:
        import av

    except (ModuleNotFoundError, ImportError):
        return None # Handled in code, don't worry :)

    genre = "Porn"
    title = data.title
    artist = data.author
    date = data.publish_date  # e.g. "2025-10-26" or "2025"
    thumbnail = data.thumbnail_data

    logging.debug("Tags [1/3] - Preparing containers")

    # FFmpeg/PyAV cannot update headers safely in-place.
    # We write to a temporary file in the same directory and perform an atomic swap.
    temp_dir = os.path.dirname(path)
    with tempfile.NamedTemporaryFile(dir=temp_dir, delete=False, suffix=".mp4") as tmp:
        tmp_path = tmp.name

    try:
        with av.open(path) as in_container, av.open(tmp_path, mode='w', format='mp4') as out_container:

            # 1. Setup stream mapping (remux existing video/audio without re-encoding)
            stream_mapping = {}
            for stream in in_container.streams:
                # Skip any existing thumbnail streams so we don't duplicate them
                if stream.type == 'video' and getattr(stream.disposition, 'attached_pic', False):
                    continue

                # Clone the stream configuration exactly
                out_stream = out_container.add_stream(template=stream)
                stream_mapping[stream] = out_stream

            # 2. Write basic text tags
            # FFmpeg automatically maps these standard keys to the correct MP4 boxes (\xa9nam, \xa9ART, etc.)
            meta = {}
            if title is not None:    meta['title'] = str(title)
            if artist is not None:   meta['artist'] = str(artist)
            if genre is not None:    meta['genre'] = str(genre)
            if date is not None:     meta['date'] = str(date)
            out_container.metadata.update(meta)

            # 3. Setup Thumbnail Stream (MP4 stores cover art as an attached picture video stream)
            logging.debug("Tags: [2/3] - Processing Thumbnail")
            thumb_stream = None
            if thumbnail:
                # Heuristically choose cover codec format
                codec_name = 'png' if thumbnail.startswith(b"\x89PNG\r\n\x1a\n") else 'mjpeg'
                try:
                    thumb_stream = out_container.add_stream(codec_name, rate=1)
                    thumb_stream.disposition.attached_pic = True
                except Exception as e:
                    logging.error("Could not initialize thumbnail stream: %s", e)
                    thumb_stream = None

            # 4. Remux packets (Read from original file, write to temp file)
            for packet in in_container.demux():
                if packet.stream not in stream_mapping:
                    continue
                packet.stream = stream_mapping[packet.stream]
                out_container.mux(packet)

            # 5. Inject the thumbnail packet at the end
            if thumbnail and thumb_stream:
                try:
                    thumb_packet = av.Packet(thumbnail)
                    thumb_packet.stream = thumb_stream
                    out_container.mux(thumb_packet)
                except Exception as e:
                    logging.error("Could not embed thumbnail data: %s", e)

        # Replace the original file with the newly tagged file atomically
        os.replace(tmp_path, path)
        logging.debug("Tags: [3/3] ✔")

    except Exception as e:
        logging.error("Failed to write tags: %s", e)
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise e


def parse_length(length: str | int, video_source: str | None = None) -> int | None | str:
    # DO NOT TOUCH THIS!!!!!!!!!!!!!!!!!!!!!!

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


