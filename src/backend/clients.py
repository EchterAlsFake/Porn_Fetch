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
2) hqporner       -> https://hqporner.com (hq_client, hq_video)
3) xnxx           -> https://xnxx.com (xn_client, xn_video)
4) xvideos        -> https://xvideos.com (xv_client, xv_video)
5) eporner        -> https://eporner.com (ep_client, ep_video)
6) missav         -> https://missav.ws   (mv_client, mv_video)
7) xhamster       -> https://xhamster.com (xh_client, xh_video)
8) spankbang      -> https://spankbang.com (sp_client, sp_video)
9) youporn        -> https://youporn.com (yp_client, yp_video)
10) porntrex      -> https://porntrex.com (pt_client, pt_video)
11) xfreehd       -> https://xfreehd.com  (xf_client, xf_video)
12) beeg          -> https://beeg.com (bg_client, bg_video)
"""

import re
import logging
import traceback


from dataclasses import dataclass
from base_api.modules.config import config # This is the global configuration instance of base core config
from mutagen.mp4 import MP4, MP4Cover, MP4Tags
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, timezone
from src.backend.handle_ssl import build_ssl_context
from typing import Any, List, TypeAlias, Optional, Dict
from phub import Client as ph_Client, Video as ph_Video
from xnxx_api import Client as xn_Client, Video as xn_Video
from beeg_api import Client as bg_Client, Video as bg_Video
from missav_api import Client as mv_Client, Video as mv_Video
from xvideos_api import Client as xv_Client, Video as xv_Video
from xfreehd_api import Client as xf_Client, Video as xf_Video
from eporner_api import Client as ep_Client, Video as ep_Video
from porntrex_api import Client as pt_Client, Video as pt_Video
from xhamster_api import Client as xh_Client, Video as xh_Video
from spankbang_api import Client as sp_Client, Video as sp_Video
from youporn_api.youporn_api import Client as yp_Client, Video as yp_Video
from hqporner_api import Client as hq_Client, Video as hq_Video, errors as hq_errors
from base_api.base import BaseCore, setup_logger, _normalize_quality_value, _choose_quality_from_list
# Note, the Video instances are mostly used in `shared_functions.py`
AllowedVideoType: TypeAlias = (
    type[ph_Video] | type[xn_Video] | type[xv_Video] | type[yp_Video] |
    type[xh_Video] | type[sp_Video] | type[bg_Video] | type[mv_Video]
    # Those are all HLS streams
)

AllowedVideoType_Legacy: TypeAlias = (
    type[hq_Video] | type[xf_Video] | type[ep_Video] | type[pt_Video]
    # Those are all non HLS streams for now
)

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
logger = setup_logger(name="Porn Fetch - [Clients]", level=logging.DEBUG)

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
logger.debug("Successfully initialized all clients!")


core = BaseCore() # We need that sometimes in Porn Fetch's main class e.g., thumbnail fetching
core.config.max_retries = 2 # Only use 2 retries to prevent blocking
core.config.use_http2 = False # Fallback to http 1 for critical operations
core.config.timeout = 10 # Medium to low timeout to prevent blocking
core.initialize_session()


def get_direct_url_legacy(video: AllowedVideoType_Legacy, quality: str | int):
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

    elif isinstance(video, hq_Video) or isinstance(video, pt_Video):
        qn = _normalize_quality_value(quality)
        chosen_height = _choose_quality_from_list(video.video_qualities, qn)

        quality_url_map = {int(re.search(r'(\d{3,4})', q).group(1)): url for q, url in zip(video.video_qualities, video.direct_download_urls())}
        download_url = f"https://{quality_url_map[chosen_height]}"
        return download_url # Uhhh

    elif isinstance(video, ep_Video):
        return video.direct_download_link(quality=quality, mode="h264") # Pls don't download AV1, thank you
        # NO I won't spend half on hour to handle this edge case where one video on this whole platform might not have
        # A h264 stream bro

    return "MakesNoSense"


def refresh_clients(enable_kill_switch: bool = False, debug_mode: bool = False, use_truststore: bool = True) -> None:
    logger.info(f"Refreshing clients!")
    config.ssl_context = build_ssl_context(use_truststore) # Decides whether to use truststore (OS CA's) or Certifi CA's

    global mv_client, ep_client, ph_client, xv_client, xh_client, sp_client, \
        hq_client, xn_client, core, yp_client, bg_client, pt_client, xf_client

    if debug_mode:
        level = logging.DEBUG

    else:
        level = logging.ERROR


    log_file_core = "BaseCore.log" if debug_mode else None
    log_file_core_hq = "BaseCore_HQ.log" if debug_mode else None
    log_file_core_mv = "BaseCore_MV.log" if debug_mode else None
    log_file_core_ep = "BaseCore_EP.log" if debug_mode else None
    log_file_core_ph = "BaseCore_PH.log" if debug_mode else None
    log_file_core_xv = "BaseCore_XV.log" if debug_mode else None
    log_file_core_xh = "BaseCore_XH.log" if debug_mode else None
    log_file_core_xn = "BaseCore_XN.log" if debug_mode else None
    log_file_core_sp = "BaseCore_SP.log" if debug_mode else None
    log_file_core_yp = "BaseCore_YP.log" if debug_mode else None
    log_file_core_bg = "BaseCore_BG.log" if debug_mode else None
    log_file_core_pt = "BaseCore_PT.log" if debug_mode else None
    log_file_core_xf = "BaseCore_XF.log" if debug_mode else None

    # One BaseCore per site, with its own RuntimeConfig (isolated headers/cookies)
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

    core.enable_logging(level=level, log_file=log_file_core)
    core_hq.enable_logging(level=level, log_file=log_file_core_hq)
    core_mv.enable_logging(level=level, log_file=log_file_core_mv)
    core_ep.enable_logging(level=level, log_file=log_file_core_ep)
    core_ph.enable_logging(level=level, log_file=log_file_core_ph)
    core_xv.enable_logging(level=level, log_file=log_file_core_xv)
    core_xh.enable_logging(level=level, log_file=log_file_core_xh)
    core_xn.enable_logging(level=level, log_file=log_file_core_xn)
    core_sp.enable_logging(level=level, log_file=log_file_core_sp)
    core_yp.enable_logging(level=level, log_file=log_file_core_yp)
    core_bg.enable_logging(level=level, log_file=log_file_core_bg)
    core_pt.enable_logging(level=level, log_file=log_file_core_pt)
    core_xf.enable_logging(level=level, log_file=log_file_core_xf)


    if enable_kill_switch:
        logger.warning("Warning: You have enabled the kill switch, refreshing clients with enabled kill switch")
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
        core.enable_kill_switch()

    # Instantiate clients with their site-specific cores
    mv_client = mv_Client(core=core_mv)
    ep_client = ep_Client(core=core_ep)
    xv_client = xv_Client(core=core_xv)
    xh_client = xh_Client(core=core_xh)
    sp_client = sp_Client(core=core_sp)
    hq_client = hq_Client(core=core_hq)
    xn_client = xn_Client(core=core_xn)
    yp_client = yp_Client(core=core_yp)
    bg_client = bg_Client(core=core_bg)
    pt_client = pt_Client(core=core_pt)
    xf_client = xf_Client(core=core_xf)
    ph_client = ph_Client(core=core_ph, use_webmaster_api=True)
    logger.debug("Applied new clients. Configurations should be overridden now e.g., if you have set a proxy.")


def check_video(url):
    """
    This function check the URL and generates the corresponding video object with the correct client.
    If the url is already a video object, the function will simply return it.
    """

    objects = [hq_Video, ep_Video, xn_Video, xv_Video, mv_Video, xh_Video, sp_Video, yp_Video, bg_Video, pt_Video,
               xf_Video]

    if isinstance(url, tuple(objects)):
        return url

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

        elif "xhamster" in url or "xhopen" in url:
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

    return False


def get_available_qualities(video: Any) -> List[int]:
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
                heights = video.core.list_available_qualities(m3u8_url)  # your existing function

            else:
                heights = video.client.core.list_available_qualities(m3u8_url)

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

def render_name_template(
    template: str,
    context: Dict[str, Any],
    *,
    missing: str = "",
) -> str:
    """
    Supports:
      $title
      ${author.name}
      ${publish_date:%Y-%m-%d}
      ${length:0.1f}  (uses Python's format())
    """
    def repl(m: re.Match) -> str:
        simple = m.group(1)
        braced = m.group(2)

        if simple:
            value = resolve_path(context, simple)
            return missing if value is None else str(value)

        expr = (braced or "").strip()

        # optional format: path:format_spec
        path, fmt = expr, None
        if ":" in expr:
            # split on first ':' (good enough for your use-case)
            path, fmt = expr.split(":", 1)
            path, fmt = path.strip(), fmt.strip()

        value = resolve_path(context, path)
        if value is None:
            return missing

        if fmt:
            if isinstance(value, datetime):
                return value.strftime(fmt)
            try:
                return format(value, fmt)
            except Exception:
                return str(value)

        return str(value)

    return _TEMPLATE_RE.sub(repl, template)

@dataclass
class VideoAttributes:
    title: str
    qualities: list[int]
    author: str
    length: Any
    tags: str
    publish_date: Any
    publish_dt_utc: Optional[datetime]
    thumbnail: str
    video_id: str
    # rendered output
    output_name: str

def _public_attr_snapshot(obj: Any) -> Dict[str, Any]:
    """
    Best-effort map of public attrs without calling methods.
    WARNING: some properties may still perform I/O when accessed.
    """
    out: Dict[str, Any] = {}
    for name in dir(obj):
        if name.startswith("_"):
            continue
        # skip obvious methods/iterables by type check after getattr
        val = _safe_getattr(obj, name)
        if callable(val):
            continue
        out[name] = val
    return out

def load_video_attributes(video, name_template: str, *, now: Optional[datetime] = None) -> VideoAttributes:
    title = video.title
    qualities = get_available_qualities(video)  # [144, 240, 360, ...]

    # --- your per-site extraction (unchanged logic) ---
    if isinstance(video, ph_Video):
        try:
            author = video.author.name
        except Exception:
            author = video.pornstars[0]

        length = video.duration.seconds / 60
        tags = ",".join([tag.name for tag in video.tags])
        publish_date = video.date
        video.refresh()  # as before
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
            author = "No pornstars / author"

        length = video.length
        tags = ",".join([category for category in video.tags])
        publish_date = video.publish_date
        video_id = video.title
        try:
            thumbnail = video.get_thumbnails()[0]
        except (TypeError, hq_errors.WeirdError):
            thumbnail = "Not available"

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
        # fallback if you ever add a new site and forget to implement it
        author = _safe_getattr(video, "author") or "Not available"
        length = _safe_getattr(video, "length") or "Not available"
        tags = _safe_getattr(video, "tags") or "Not available"
        publish_date = _safe_getattr(video, "publish_date") or "Not available"
        thumbnail = _safe_getattr(video, "thumbnail") or "Not available"
        video_id = _safe_getattr(video, "id") or title

    # Normalize publish date into UTC datetime (optional extra field)
    publish_dt_utc = parse_publish_date(publish_date, now=now)

    # Build template context:
    # - normalized keys (stable)
    # - "video" for deep access: ${video.some_attr}
    # - raw snapshot so users can also do $some_attr if it exists
    normalized = {
        "title": title,
        "qualities": qualities,
        "qualities_csv": ",".join(map(str, qualities)),
        "author": author,
        "length": length,
        "tags": tags,
        "publish_date": publish_date,         # original
        "publish_dt": publish_dt_utc,         # parsed datetime (UTC)
        "thumbnail": thumbnail,
        "video_id": video_id,
    }
    raw = _public_attr_snapshot(video)

    context: Dict[str, Any] = {}
    context.update(raw)        # allow $publish_date if the object has it, etc.
    context.update(normalized) # normalized wins if same name
    context["video"] = video   # allow ${video.author.name} etc.

    rendered = render_name_template(name_template, context, missing="")
    rendered = core.strip_title(rendered)

    return VideoAttributes(
        title=title,
        qualities=qualities,
        author=str(author),
        length=length,
        tags=str(tags),
        publish_date=publish_date,
        publish_dt_utc=publish_dt_utc,
        thumbnail=str(thumbnail),
        video_id=str(video_id),
        output_name=rendered,
    )



def parse_publish_date(value: str, *, now: Optional[datetime] = None) -> Optional[datetime]:
    """
    Parse a publish-date string from various sites and return a timezone-aware datetime in UTC.

    Parameters
    ----------
    value : str
        Raw publish date text.
    now : datetime | None
        Reference time for relative strings like "7 days ago".
        Defaults to current time in UTC.

    Returns
    -------
    datetime | None
        A timezone-aware datetime in UTC, or None if not parseable / not available.
    """
    if value is None:
        return None

    s = str(value).strip()
    if _NOT_AVAILABLE_RE.match(s):
        return None

    now_utc = (now or datetime.now(timezone.utc))
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


def download_android(url: str, quality="best", path="./", remux=False):
    """
    Downloads a video and reports progress back to Kotlin ProgressBridge.
    Note: This is intended to be used by the Android App, NOT the main gui in `main.py` nor the CLI!
    """
    video = check_video(url)
    if not video:
        return False

    from java import jclass
    ProgressBridge = jclass("me.echteralsfake.pornfetch.ProgressBridge")

    def cb(current, total):
        try:
            ProgressBridge.onProgress(int(current), int(total))
        except Exception:
            pass

    return video.download(
        quality=quality,
        path=path,
        callback=cb,
        remux=remux
    )


def write_tags(path: str, data: dict):
    """
    Writes the tags of the video into the file. This needs a correct MP4 header either from a remuxed mpeg-ts stream
    through PyAV or the stream is already an mp4 file e.g., from EPorner or HQPorner.
    """
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


# EOF