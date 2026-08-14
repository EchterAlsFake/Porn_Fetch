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

from src.backend.errors import InvalidInput
from src.backend.config import app_settings
from urllib.parse import urlparse
from base_api.modules.config import config # This is the global configuration instance of base core config
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, timezone
from typing import Any, List, TypeAlias, Optional, Dict
from pornhub_api import Client as ph_Client, Video as ph_Video, Short as ph_Short
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
from base_api import BaseCore, ScrapeResult, Cache
from src.backend.errors import SomethingStupidHappened, MetadataWriteError
from base_api.modules.logger import configure_app_logging
from src.backend.download_manager import VideoObject
from base_api.modules.static_functions import normalize_quality, choose_quality_from_list, strip_title, \
    normalize_quality_value

# Note, the Video instances are mostly used in `shared_functions.py`
AllowedVideoType: TypeAlias = (
    ph_Video | xn_Video | xv_Video | yp_Video | tu_Video | ph_Short |
    xh_Video | sp_Video | bg_Video | rt_Video | th_Video
    # Those are all HLS streams
)

AllowedVideoType_Legacy: TypeAlias = (
    xf_Video | ep_Video | pt_Video | pt_Video
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

DEFAULT_CONTENT_LOCALE = "en-US"
SUPPORTED_CONTENT_LOCALES: Dict[str, str] = {
    "cs-CZ": "cs",
    "de-DE": "de",
    "en-US": "en",
    "es-ES": "es",
    "fil-PH": "fil",
    "fr-FR": "fr",
    "it-IT": "it",
    "nl-NL": "nl",
    "ja-JP": "ja",
    "pl-PL": "pl",
    "pt-PT": "pt",
    "ru-RU": "ru",
    "uk-UA": "uk",
    "zh-CN": "zh",
}


def generate_locale_headers_and_cookies(
    locale: str | None = None,
) -> tuple[Dict[str, str], Dict[str, str]]:
    """Build curl-cffi-ready headers and cookies for a content locale.

    ``locale`` may be one of the full locale tags used by the settings menu or
    its short language code (for example, ``"de-DE"`` or ``"de"``). Unknown
    and empty values safely fall back to English.

    Example::

        headers, cookies = generate_locale_headers_and_cookies("de-DE")
        session.headers.update(headers)
        session.cookies.update(cookies)
    """
    requested_locale = locale if locale is not None else app_settings.locale
    normalized_locale = str(requested_locale).strip().replace("_", "-").casefold()

    locale_lookup = {
        alias.casefold(): canonical_locale
        for canonical_locale, language_code in SUPPORTED_CONTENT_LOCALES.items()
        for alias in (canonical_locale, language_code)
    }
    canonical_locale = locale_lookup.get(normalized_locale, DEFAULT_CONTENT_LOCALE)
    language_code = SUPPORTED_CONTENT_LOCALES[canonical_locale]

    if language_code == "en":
        accept_language = f"{canonical_locale},en;q=0.9"
    else:
        accept_language = (
            f"{canonical_locale},{language_code};q=0.9,"
            "en-US;q=0.8,en;q=0.7"
        )

    headers = {"Accept-Language": accept_language}
    cookies = {
        "lang": language_code,
        "language": language_code,
        "locale": canonical_locale,
    }
    return headers, cookies


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
           rt_Video, th_Video, tu_Video, ph_Short]

for _core in cores:
    _core.initialize_session()

logger.debug("Successfully initialized all clients and!")


def refresh_clients() -> None:
    # Apply Settings
    debug_mode = app_settings.debug_mode

    config.response_cache_size_bytes = app_settings.response_cache_size * 1024 * 1024
    config.response_cache_ttl = app_settings.response_cache_ttl
    config.segment_cache_size_bytes = app_settings.segment_cache_size * 1024 * 1024
    config.segment_cache_ttl = app_settings.segment_cache_ttl
    config.request_attempts = app_settings.retries
    config.request_retry_initial_delay = app_settings.request_initial_retry_delay
    config.request_retry_max_delay = app_settings.request_retry_max_delay
    config.request_multiplier = app_settings.request_retry_multiplier
    config.request_retry_jitter = app_settings.request_retry_jitter
    config.request_delay = app_settings.network_delay
    config.timeout = app_settings.timeout
    config.max_bandwidth_mb = app_settings.speed_limit
    config.proxy = getattr(app_settings, 'active_sni_proxy_url', None) or app_settings.proxy or None
    config.http_version = app_settings.http_version
    config.dns_over_https = app_settings.dns_server if app_settings.dns_over_https else None
    config.impersonation = app_settings.impersonation
    config.custom_ja3 = app_settings.custom_ja3 if app_settings.custom_ja3 else None
    config.verify_ssl = app_settings.proxy_ssl_verification
    config.trust_env = app_settings.trust_environment
    config.max_workers_download = app_settings.download_workers
    config.videos_concurrency = app_settings.videos_concurrency
    config.pages_concurrency = app_settings.pages_concurrency
    config.interface = app_settings.interface if app_settings.interface else None
    locale_headers, locale_cookies = generate_locale_headers_and_cookies()
    config.locale = locale_headers["Accept-Language"]
    config.cookies = locale_cookies.copy()

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
        c.cache = Cache(c.configuration)
        c.default_headers.update(locale_headers)
        c.initialize_session()

        if old_session is not None and c.session is not None:
            try:
                c.session.cookies.update(old_session.cookies)
                c.session.headers.update(old_session.headers)
            except Exception as e:
                logger.warning(f"Couldn't copy cookies/headers during session refresh: {e}")

        # Language preferences must win over values copied from the old session.
        if c.session is not None:
            c.session.headers.update(locale_headers)
            for cookie_name in locale_cookies:
                c.session.cookies.delete(cookie_name)
            c.session.cookies.update(locale_cookies)

    logger.debug("Applied in-place clients!")


async def get_video(url: str | AnyVideoClass) -> AnyVideoClass:
    """
    This function check the URL and generates the corresponding video object with the correct client.
    If the url is already a video object, the function will simply return it.
    """
    if isinstance(url, ScrapeResult):
        if not url.succeeded:
            if url.error is not None:
                raise url.error

            raise RuntimeError(f"Scraping failed without an exception: {url.url}")

        video = url.item
        if video is None:
            raise RuntimeError(f"Succesful scrpa does not contain a video (how tf did you do that? {url.url}")

        return video

    if isinstance(url, tuple(video_objects)):
        return url

    if not isinstance(url, str):
        print(f"Video Type: {url}")
        print(type(url))

        raise SomethingStupidHappened

    if not url.startswith("http"):
        raise InvalidInput

    final_website = None
    hostname = urlparse(url).hostname
    for website, pattern in SITE_PATTERNS:
        if pattern.search(hostname):
            final_website = website

    if not final_website:
        raise InvalidInput

    load_api_sources = not app_settings.strict_enforcement

    # 2. Call ONLY the specific client for that website
    if final_website == "pornhub":
        return await ph_client.get_video(url=url, load_html=True, load_api=load_api_sources)
    elif final_website == "eporner":
        return await ep_client.get_video(url=url, load_html=True, load_api=load_api_sources)
    elif final_website == "xnxx":
        return await xn_client.get_video(url=url, load_html=True)
    elif final_website == "xvideos":
        return await xv_client.get_video(url=url, load_html=True)
    elif final_website == "xhamster":
        return await xh_client.get_video(url=url, load_html=True)
    elif final_website == "xhamter_short":
        return await xh_client.get_short(url=url, load_html=True)
    elif final_website == "spankbang":
        return await sp_client.get_video(url=url, load_html=True)
    elif final_website == "youporn":
        return await yp_client.get_video(url=url, load_html=True)
    elif final_website == "beeg":
        return await bg_client.get_video(url=url, load_api=load_api_sources)
    elif final_website == "porntrex":
        return await pt_client.get_video(url=url)
    elif final_website == "xfreehd":
        return await xf_client.get_video(url=url)
    elif final_website == "redtube":
        return await rt_client.get_video(url=url)
    elif final_website == "thumbzilla":
        return await th_client.get_video(url=url)
    elif final_website == "tube8":
        return await tu_client.get_video(url=url)
    else:
        raise InvalidInput


async def load_video_attributes(video: AnyVideoClass) -> VideoObject:
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
        thumbnail = video.thumbnail
        video_id = video.title

    elif isinstance(video, xv_Video):
        author = await video.get_author
        author = author.name
        length = video.length
        tags = video.tags
        publish_date = video.publish_date
        thumbnail = video.thumbnail_url
        video_id = video.title

    elif isinstance(video, ep_Video):
        _authors = []
        authors = video.get_authors()
        async for author in authors:
            _authors.append(author.name)
            print(f"Received: {author.name}")

        author = "".join(_authors)
        print(f"Author: {author}")

        if not author:
            author = video.uploader

        length = video.length_minutes
        tags = ",".join(video.tags)
        publish_date = video.publish_date
        thumbnail = video.thumbnail
        video_id = video.video_id

    elif isinstance(video, yp_Video):
        stuff = await video.author(load_html=True)
        author = stuff.name
        length = video.length
        tags = ",".join(video.categories)
        thumbnail = video.thumbnail
        publish_date = video.publish_date
        video_id = video.title

    elif isinstance(video, xh_Video):
        author = ",".join(video.pornstars)
        length = video.duration
        tags = video.tags
        thumbnail = video.thumbnail
        publish_date = "Not available"
        video_id = video.title

    elif isinstance(video, sp_Video):
        author = video.author
        length = video.length
        tags = ",".join(video.tags)
        thumbnail = video.thumbnail
        publish_date = video.length
        video_id = video.title

    elif isinstance(video, bg_Video):
        author = "Not available"
        length = video.duration
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
        publish_date = video.publish_date

    else:
        raise SomethingStupidHappened

    length = parse_length(length)
    qualities = await get_available_qualities(video)  # [144, 240, 360, ...]
    print(f"Received Qualities: {qualities}")
    print(f"Putting: {qualities[0]} in function")
    print(f"Got: {normalize_quality_value(qualities[0])}")


    qualities = [normalize_quality(quality) for quality in qualities]
    print(qualities)

    # Normalize publish date into UTC datetime (optional extra field)
    publish_dt_utc = parse_publish_date(publish_date)
    title = strip_title(title)
    video_object = VideoObject(
        url=video.url,
        thumbnail_url=thumbnail,
        video_id=video_id,
        length=length,
        author=author,
        title=title,
        publish_date=publish_dt_utc,
        status="Pending",
        qualities=qualities,
        tags=tags
    )

    return video_object


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
        # TODO
        return video.get_direct_download_urls(quality=quality, mode="h264") # Pls don't download AV1, thank you
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
    if isinstance(video, (ep_Video, xf_Video)):
        quals = video.video_qualities()
        print(f"Qualities: {quals}")
        return quals

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


def write_tags(path: str, data: VideoObject) -> bool:
    """
    Writes the tags of the video into the file using PyAV.
    """
    try:
        import av

    except (ModuleNotFoundError, ImportError):
        return None # Handled in code, don't worry :)

    genre = "XXX"
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
        raise MetadataWriteError(str(e))

def parse_length(
    length: str | int | float | None,
    video_source: str | None = None,
) -> int | None | str:
    """
    Parse a video duration and return its length in rounded minutes.

    Supported examples:
        16:19
        123
        12.5
        9 Min
        247min 02sec
        59m 40s
        1h 2m 3s
        24 seconds
        PT00H11M42S
        PT11M42S
        PT2H
        PT42S

    Digits-only strings depend on `video_source`:
        - xnxx:    value is interpreted as minutes
        - eporner: value is interpreted as seconds
        - phub:    value is interpreted as seconds
        - other:   value is interpreted as minutes

    Returns:
        int:
            Rounded duration in minutes.
            Positive durations below 0.5 minutes are returned as 1.

        "Not available":
            If no duration was provided.

        None:
            If the duration format could not be parsed.
    """

    def rounded_minutes(minutes: float) -> int:
        """Round minutes, but keep any positive duration at at least 1 minute."""
        result = round(minutes)
        return max(1, result) if minutes > 0 else 0

    if length is None or length == "" or length == "Not available":
        return "Not available"

    # Already numeric -> assume minutes.
    if isinstance(length, (int, float)):
        return rounded_minutes(float(length))

    s = str(length).strip()
    s_lower = s.lower()

    if not s:
        return "Not available"

    # ---------------------------------------------------------
    # ISO 8601 duration:
    # PT00H11M42S
    # PT11M42S
    # PT2H
    # PT42S
    # PT1H2.5M
    iso_match = re.fullmatch(
        r"PT"
        r"(?:(?P<hours>\d+(?:\.\d+)?)H)?"
        r"(?:(?P<minutes>\d+(?:\.\d+)?)M)?"
        r"(?:(?P<seconds>\d+(?:\.\d+)?)S)?",
        s,
        flags=re.IGNORECASE,
    )

    if iso_match and any(iso_match.groupdict().values()):
        hours = float(iso_match.group("hours") or 0)
        minutes = float(iso_match.group("minutes") or 0)
        seconds = float(iso_match.group("seconds") or 0)

        total_minutes = (
            hours * 60
            + minutes
            + seconds / 60
        )

        return rounded_minutes(total_minutes)

    # ---------------------------------------------------------
    # Colon format:
    # 16:19 -> 16 minutes, 19 seconds
    #
    # Also handles:
    # 1:02:03 -> 1 hour, 2 minutes, 3 seconds
    parts = s.split(":")

    if len(parts) in (2, 3) and all(part.isdigit() for part in parts):
        if len(parts) == 2:
            minutes, seconds = map(int, parts)
            total_minutes = minutes + seconds / 60

        else:
            hours, minutes, seconds = map(int, parts)
            total_minutes = hours * 60 + minutes + seconds / 60

        return rounded_minutes(total_minutes)

    # ---------------------------------------------------------
    # Digits only.
    if s.isdigit():
        value = int(s)
        source = (video_source or "").lower()

        if "eporner" in source or "phub" in source:
            return rounded_minutes(value / 60)

        # xnxx and unknown sources are interpreted as minutes.
        return value

    # ---------------------------------------------------------
    # Plain decimal -> assume minutes.
    #
    # Examples:
    # 12.5
    # 0.25
    if re.fullmatch(r"\d+(?:\.\d+)?", s):
        return rounded_minutes(float(s))

    # ---------------------------------------------------------
    # Human-readable units.
    #
    # Examples:
    # 59m 40s
    # 1h 2m 3s
    # 247min 02sec
    # 24 seconds
    # 17 min
    # 1 hour 24 minutes
    unit_multipliers = {
        # Hours
        "h": 60,
        "hr": 60,
        "hrs": 60,
        "hour": 60,
        "hours": 60,

        # Minutes
        "m": 1,
        "min": 1,
        "mins": 1,
        "minute": 1,
        "minutes": 1,

        # Seconds
        "s": 1 / 60,
        "sec": 1 / 60,
        "secs": 1 / 60,
        "second": 1 / 60,
        "seconds": 1 / 60,
    }

    matches = re.findall(
        r"(\d+(?:\.\d+)?)\s*"
        r"(hours?|hrs?|h|minutes?|mins?|m|seconds?|secs?|s)\b",
        s_lower,
    )

    if matches:
        total_minutes = sum(
            float(value) * unit_multipliers[unit]
            for value, unit in matches
        )

        return rounded_minutes(total_minutes)

    return None
