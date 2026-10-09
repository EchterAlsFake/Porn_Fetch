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


try:
    from src.backend.handle_ssl import build_ssl_context

except (ModuleNotFoundError, ImportError):
    from handle_ssl import build_ssl_context

from src.shared.errors import InvalidInput
from src.backend.config import app_settings
from urllib.parse import urlparse
from base_api.modules.config import config # This is the global configuration instance of base core config
from typing import Any, List, TypeAlias, Dict
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
from xhamster_api.api import Short as xh_Short
from redtube_api import Client as rt_Client, Video as rt_Video
from spankbang_api import Client as sp_Client, Video as sp_Video
from youporn_api import Client as yp_Client, Video as yp_Video
from base_api import BaseCore, ScrapeResult, Cache
from src.shared.errors import SomethingStupidHappened
from src.shared.provider_routing import ContentKind, resolve_video, route_url
from base_api.modules.logger import configure_app_logging
from src.shared.media import VideoObject
from src.shared.provider_parsing import parse_length, parse_publish_date
from base_api.modules.static_functions import normalize_quality, choose_quality_from_list, strip_title, \
    normalize_quality_value
from curl_cffi.const import CurlOpt

# Note, the Video instances are mostly used in `shared_functions.py`
AllowedVideoType: TypeAlias = (
    ph_Video | xn_Video | xv_Video | yp_Video | tu_Video | ph_Short |
    xh_Video | xh_Short | sp_Video | bg_Video | rt_Video | th_Video
    # Those are all HLS streams
)

AllowedVideoType_Legacy: TypeAlias = (
    xf_Video | ep_Video | pt_Video
    # Those are all non HLS streams for now
)

AnyVideoClass: TypeAlias = AllowedVideoType | AllowedVideoType_Legacy

_NOT_AVAILABLE_RE = re.compile(r"^\s*(not\s+available|n/?a|none|null)?\s*$", re.IGNORECASE)
DOH_BOOTSTRAP_RESOLVES: list[bytes] = [
    b"dns.mullvad.net:443:194.242.2.2,194.242.2.3,194.242.2.4",
    b"dns.quad9.net:443:9.9.9.9,149.112.112.112",
    b"cloudflare-dns.com:443:1.1.1.1,1.0.0.1",
    b"dns.google:443:8.8.8.8,8.8.4.4",
]

_orig_basecore_init_session = BaseCore.initialize_session

def _bootstrap_basecore_init_session(self) -> None:
    _orig_basecore_init_session(self)
    if getattr(self, "session", None) is not None and hasattr(CurlOpt, "RESOLVE"):
        self.session.curl_options[CurlOpt.RESOLVE] = list(DOH_BOOTSTRAP_RESOLVES)

BaseCore.initialize_session = _bootstrap_basecore_init_session
logger = configure_app_logging(logger_name="Porn Fetch - [Clients]", level=logging.DEBUG, log_file="PornFetch.log")
_retired_sessions: list[Any] = []
_session_cleanup_tasks: set[asyncio.Task[None]] = set()

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
    ("pornhub", re.compile(r"(?:^|\.)pornhub(?:premium)?\.com$", re.IGNORECASE)),
    ("xnxx", re.compile(r"(?:^|\.)xnxx\d*\.com$", re.IGNORECASE)),
    ("xvideos", re.compile(r"(?:^|\.)xvideos\d*\.com$", re.IGNORECASE)),
    ("eporner", re.compile(r"(?:^|\.)eporner\.com$", re.IGNORECASE)),
    ("xhamster", re.compile(r"(?:^|\.)xhamster\d*\.com$", re.IGNORECASE)),
    ("spankbang", re.compile(r"(?:^|\.)spankbang\.com$", re.IGNORECASE)),
    ("youporn", re.compile(r"(?:^|\.)youporn\.com$", re.IGNORECASE)),
    ("beeg", re.compile(r"(?:^|\.)beeg\.com$", re.IGNORECASE)),
    ("redtube", re.compile(r"(?:^|\.)redtube\.com$", re.IGNORECASE)),
    ("thumbzilla", re.compile(r"(?:^|\.)thumbzilla\.com$", re.IGNORECASE)),
    ("tube8", re.compile(r"(?:^|\.)tube8\.com$", re.IGNORECASE)),
    ("xfreehd", re.compile(r"(?:^|\.)xfreehd\.com$", re.IGNORECASE)),
    ("porntrex", re.compile(r"(?:^|\.)porntrex\.com$", re.IGNORECASE)),
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
           rt_Video, th_Video, tu_Video, ph_Short, xh_Short]

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
    active_sni_proxy = getattr(app_settings, "active_sni_proxy_url", None)
    config.proxy = active_sni_proxy or app_settings.proxy or None
    # Both SNI proxy implementations are TCP-only. Never allow HTTP/3/QUIC to
    # silently bypass the local proxy when obfuscation is enabled.
    config.http_version = "v2" if active_sni_proxy else app_settings.http_version
    config.dns_over_https = app_settings.dns_server if app_settings.dns_over_https else None
    config.impersonation = app_settings.impersonation
    config.custom_ja3 = app_settings.custom_ja3 if app_settings.custom_ja3 else None
    config.verify_ssl = app_settings.proxy_ssl_verification
    config.trust_env = app_settings.trust_environment
    config.max_workers_download = app_settings.download_workers
    config.videos_concurrency = app_settings.videos_concurrency
    config.pages_concurrency = app_settings.pages_concurrency
    # With the local proxy enabled curl connects to loopback. The proxy manager
    # applies the selected interface/source address to its Internet-facing socket.
    config.interface = None if active_sni_proxy else (app_settings.interface or None)
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
        c.session = None
        c.cache = Cache(c.configuration)
        c.default_headers.update(locale_headers)
        c.initialize_session()

        if old_session is not None and c.session is not None:
            try:
                c.session.cookies.update(old_session.cookies)
                c.session.headers.update(old_session.headers)
            except Exception as e:
                logger.warning(f"Couldn't copy cookies/headers during session refresh: {e}")
            _retired_sessions.append(old_session)

        # Language preferences must win over values copied from the old session.
        if c.session is not None:
            c.session.headers.update(locale_headers)
            for cookie_name in locale_cookies:
                c.session.cookies.delete(cookie_name)
            c.session.cookies.update(locale_cookies)
            if hasattr(CurlOpt, "ECH"):
                c.session.curl_options[CurlOpt.ECH] = (
                    b"true" if app_settings.encrypted_ch else b"false"
                )
            if hasattr(CurlOpt, "RESOLVE"):
                c.session.curl_options[CurlOpt.RESOLVE] = list(DOH_BOOTSTRAP_RESOLVES)

    logger.debug("Applied in-place clients!")
    schedule_retired_session_cleanup()


async def close_retired_sessions() -> None:
    """Close sessions replaced by :func:`refresh_clients`."""

    sessions = list(dict.fromkeys(_retired_sessions))
    _retired_sessions.clear()
    for session in sessions:
        try:
            await session.close()
        except Exception:
            logger.exception("Could not close a retired network session")


def schedule_retired_session_cleanup() -> asyncio.Task[None] | None:
    """Schedule cleanup when a Qt/asyncio loop is currently running."""

    if not _retired_sessions:
        return None
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return None
    task = loop.create_task(close_retired_sessions(), name="close-retired-network-sessions")
    _session_cleanup_tasks.add(task)
    task.add_done_callback(_session_cleanup_tasks.discard)
    return task


async def close_all_clients() -> None:
    """Close current and replaced sessions during application shutdown."""

    if _session_cleanup_tasks:
        await asyncio.gather(*tuple(_session_cleanup_tasks), return_exceptions=True)
    await close_retired_sessions()
    unique_cores = set(cores)
    unique_cores.add(core)
    for client in (
        ep_client, ph_client, xv_client, xh_client, sp_client, xn_client,
        yp_client, bg_client, pt_client, xf_client, rt_client, th_client, tu_client,
    ):
        unique_cores.add(client.core)
    await asyncio.gather(*(item.close() for item in unique_cores), return_exceptions=True)


async def get_video(url: str | AnyVideoClass) -> AnyVideoClass:
    """
    This function check the URL and generates the corresponding video object with the correct client.
    If the url is already a video object, the function will simply return it.
    """
    if isinstance(url, ScrapeResult): # When the video comes from an iterator
        if not url.succeeded:
            if url.error is not None:
                raise url.error

            raise RuntimeError(f"Scraping failed without an exception: {url.url}")

        video = url.item
        if video is None:
            raise RuntimeError(f"Successful scrape does not contain a video: {url.url}")

        if not isinstance(video, tuple(video_objects)):
            raise InvalidInput
        return video

    if isinstance(url, tuple(video_objects)):
        return url

    if not isinstance(url, str):
        raise InvalidInput

    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    if parsed_url.scheme.casefold() not in {"http", "https"} or not hostname:
        raise InvalidInput

    final_website = None
    for website, pattern in SITE_PATTERNS:
        if pattern.search(hostname):
            final_website = website
            break

    if not final_website:
        raise InvalidInput

    route = route_url(url)
    if route.kind != ContentKind.VIDEO:
        raise InvalidInput
    return await resolve_video(client_for(final_website), route,
                               strict_language=app_settings.strict_enforcement)


def client_for(provider: str) -> Any:
    """Look up the current GUI client, including after a session refresh."""
    return {
        "pornhub": ph_client, "eporner": ep_client, "xnxx": xn_client,
        "xvideos": xv_client, "xhamster": xh_client, "spankbang": sp_client,
        "youporn": yp_client, "beeg": bg_client, "porntrex": pt_client,
        "xfreehd": xf_client, "redtube": rt_client, "thumbzilla": th_client,
        "tube8": tu_client,
    }[provider]


async def load_video_attributes(video: AnyVideoClass) -> VideoObject:
    # Iterator results may be lazy. Load the provider's page source before
    # reading fields; Beeg is the one supported provider with only an API source.
    source = "api" if isinstance(video, bg_Video) else "html"
    if source in video.loader_methods:
        await video.load_sources(source)
    if isinstance(video, ep_Video) and not app_settings.strict_enforcement:
        await video.load_sources("api")

    title = _safe_getattr(video, "title")
    video_source = ""

    if isinstance(video, ph_Video):
        video_source = "pornhub"
        author_information = video.author_information or {}
        author = author_information.get("name") or "N/A"

        length = video.duration
        tags = video.tags
        publish_date = video.publish_date
        thumbnail = video.thumbnail
        video_id = video.video_id

    elif isinstance(video, ph_Short):
        video_source = "pornhub"
        author = video.author_name or "N/A"
        length = None
        tags = None
        publish_date = None
        thumbnail = video.thumbnail
        video_id = video.video_id

    elif isinstance(video, xn_Video):
        video_source = "xnxx"
        author = video.author
        length = video.length
        tags = video.tags
        publish_date = video.publish_date
        thumbnail = video.thumbnail
        video_id = video.title

    elif isinstance(video, xv_Video):
        video_source = "xvideos"
        author_object = await video.get_author
        author = getattr(author_object, "name", None) or "N/A"
        length = video.length
        tags = video.tags
        publish_date = video.publish_date
        thumbnail = video.thumbnail_url
        video_id = video.title

    elif isinstance(video, ep_Video):
        video_source = "eporner"
        author = video.uploader or "N/A"
        # These fields are API-backed and intentionally remain unresolved when
        # content-language strict mode requests HTML only.
        length = _safe_getattr(video, "length_seconds")
        tags = video.tags
        publish_date = _safe_getattr(video, "publish_date")
        thumbnail = _safe_getattr(video, "thumbnail")
        video_id = video.video_id

    elif isinstance(video, yp_Video):
        video_source = "youporn"
        if video.author_link:
            stuff = await video.author(load_html=True)
            author = getattr(stuff, "name", None) or video.uploader_name or "N/A"
        else:
            author = video.uploader_name or "N/A"
        length = video.length
        tags = video.categories
        thumbnail = video.thumbnail
        publish_date = video.publish_date
        video_id = video.title

    elif isinstance(video, xh_Video):
        video_source = "xhamster"
        author = ",".join(video.pornstars or ())
        if not author:
            author = video.uploader_name or "N/A"
        length = video.duration
        tags = video.tags
        thumbnail = video.thumbnail
        publish_date = video.date_ago or video.created_timestamp
        video_id = video.title

    elif isinstance(video, xh_Short):
        video_source = "xhamster"
        author = video.author or "N/A"
        length = video.duration
        tags = video.tags
        thumbnail = video.thumbnail or video.poster_url
        publish_date = video.created_at
        video_id = video.video_id

    elif isinstance(video, sp_Video):
        video_source = "spankbang"
        author = video.author
        length = video.length
        tags = video.tags
        thumbnail = video.thumbnail
        publish_date = None
        video_id = video.title

    elif isinstance(video, bg_Video):
        video_source = "beeg"
        author = "Not available"
        length = video.duration
        tags = "Not available"
        thumbnail = "Not available"
        publish_date = "Not available"
        video_id = video.video_id

    elif isinstance(video, pt_Video):
        video_source = "porntrex"
        author = video.author
        length = video.duration
        tags = video.tags
        thumbnail = video.thumbnail
        publish_date = video.publish_date
        video_id = video.video_id

    elif isinstance(video, xf_Video):
        video_source = "xfreehd"
        author = video.author
        length = video.length
        tags = video.tags
        thumbnail = video.thumbnail
        publish_date = video.publish_date
        video_id = video.title

    elif isinstance(video, (rt_Video, tu_Video, th_Video)):
        video_source = "redtube" if isinstance(video, rt_Video) else (
            "tube8" if isinstance(video, tu_Video) else "thumbzilla"
        )
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

    length = parse_length(length, video_source=video_source)
    qualities = await get_available_qualities(video)  # [144, 240, 360, ...]
    normalized_qualities = []
    for quality in qualities:
        try:
            normalized_qualities.append(normalize_quality(quality))
        except (TypeError, ValueError):
            logger.warning("Ignoring invalid video quality: %r", quality)

    if isinstance(tags, dict):
        normalized_tags = [str(tag) for tag in tags]
    elif isinstance(tags, str):
        normalized_tags = [
            tag.strip() for tag in tags.split(",")
            if tag.strip() and not _NOT_AVAILABLE_RE.match(tag)
        ]
    else:
        normalized_tags = [str(tag) for tag in (tags or ())]

    # Normalize publish date into UTC datetime (optional extra field)
    publish_dt_utc = parse_publish_date(publish_date)
    title = strip_title(title)
    video_object = VideoObject(
        url=video.url,
        thumbnail_url=thumbnail or "",
        video_id=str(video_id or video.url),
        length=length,
        author=author or "N/A",
        title=title,
        publish_date=publish_dt_utc,
        status="Pending",
        qualities=normalized_qualities,
        tags=normalized_tags
    )

    return video_object


async def get_direct_url_legacy(video: AllowedVideoType_Legacy, quality: str | int) -> str:
    """
    Since the non HLS downloads now support resuming by getting the current filesize
    and appending missing bytes, we need a way in Porn Fetch to actually see if a file is incomplete.

    If we don't do this, the skip existing files feature wouldn't work or I would need to find another
    more complex implementation for this.

    This helper function basically just gets the direct download URL for a given quality based on each API
    that uses mp4 streams.
    """

    if isinstance(video, xf_Video):
        await video.load_fields("cdn_urls")
        available = video.video_qualities()
        preference = {"hd": "best", "sd": "worst"}.get(
            str(quality).strip().casefold(), quality
        )
        chosen_height = choose_quality_from_list(available, preference)
        return dict(zip(available, video.cdn_urls))[chosen_height]

    elif isinstance(video, pt_Video):
        await video.load_fields("video_qualities", "direct_download_urls")
        qn = normalize_quality_value(quality)
        chosen_height = choose_quality_from_list(video.video_qualities, qn)

        quality_url_map = {
            normalize_quality(q): url
            for q, url in zip(video.video_qualities, video.direct_download_urls)
        }
        return quality_url_map[chosen_height]

    elif isinstance(video, ep_Video):
        await video.load_fields("parsed_urls")
        return video.get_url_by_quality(quality=quality, mode="h264")

    raise TypeError(f"Unsupported legacy video type: {type(video).__name__}")


async def get_available_qualities(video: Any) -> List[int]:
    """
    Returns sorted unique qualities worst->best as ints.
    Works for:
      - HLS videos: video.m3u8_base_url + video.core.list_available_qualities()
      - Legacy videos: video.video_qualities (e.g. ["360", "480", "720"])
    """
    if isinstance(video, yp_Video) and video.is_hls is False:
        # This provider exposes only its selected fallback MP4 URL in this case.
        return []

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
            logger.exception("Could not load HLS qualities for %s", getattr(video, "url", video))
            raise

    # ---- Legacy ----
    # Your legacy wrapper already exposes `video_qualities` as list[str]
    if isinstance(video, (ep_Video, xf_Video)):
        quals = video.video_qualities()
        return sorted({normalize_quality(q) for q in quals})

    else:
        quals = getattr(video, "video_qualities", None)

    if quals:
        normalized = set()
        for quality in quals:
            try:
                normalized.add(normalize_quality(quality))
            except (TypeError, ValueError):
                logger.warning("Ignoring invalid video quality: %r", quality)
        return sorted(normalized)

    return []

def _safe_getattr(obj: Any, attr: str) -> Any:
    try:
        return getattr(obj, attr)
    except Exception:
        return None
