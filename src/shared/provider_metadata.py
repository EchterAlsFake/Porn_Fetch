"""Explicit metadata mappings for the audited providers; never load another source."""
from __future__ import annotations

import hashlib
import html
import inspect
import re
from datetime import datetime
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit, urlunsplit

from base_api.modules.errors import DataNotLoadedError

from .library_metadata import Credit, LibraryMetadata
from .provider_routing import PROVIDER_MODULES

# Fields refer to the native video, not VideoObject.author (whose role varies).
PROVIDER_FIELDS = {
    "beeg": (None, "duration", "publish_date", "author", "tags", None, "thumbnail"),
    "bellesa": ("description", "duration", "publish_date", None, "tags", "categories", "thumbnail_url"),
    "empflix": ("description", "duration", "publish_date", "author_name", "tags", "categories", "thumbnail_url"),
    "eporner": ("description", "length_seconds", "publish_date", "uploader", "tags", "categories", "thumbnail"),
    "porn": (None, "duration", None, None, "tags", None, "thumbnail_url"),
    "porndoe": ("description", "duration", "publish_date", None, "tags", "categories", "thumbnail_url"),
    "pornhat": ("description", "duration", "publish_date", None, "tags", None, "thumbnail_url"),
    "pornhub": ("description", "duration", "publish_date", "author_name", "tags", "categories", "thumbnail"),
    "porntrex": ("description", "duration", "publish_date", "author", "tags", "categories", "thumbnail"),
    "redgifs": ("description", "duration", "publish_date", "author", "tags", None, "thumbnail_url"),
    "redtube": (None, "duration", "publish_date", "author_name", "tags", "categories", "thumbnail"),
    "spankbang": ("description", "length", None, "author", "tags", None, "thumbnail"),
    "thumbzilla": ("description", "duration", "publish_date", "author_name", None, None, "thumbnail"),
    "tnaflix": ("description", "duration", "publish_date", "author_name", "tags", "categories", "thumbnail_url"),
    "tube8": ("description", "duration", "publish_date", "author_name", None, None, "thumbnail"),
    "xfreehd": (None, "length", "publish_date", "author", "tags", "categories", "thumbnail"),
    "xhamster": ("description", "duration", "created_timestamp", "uploader_name", "tags", "categories", "thumbnail"),
    "xnxx": ("description", "length", "publish_date", "author", "tags", None, "thumbnail"),
    "xvideos": ("description", "length", "publish_date", "author_name", "tags", None, "thumbnail_url"),
    "youporn": (None, "length", "publish_date", "uploader_name", "tags", "categories", "thumbnail"),
    "youjizz": ("description", "duration", "publish_date", "author_name", "tags", None, "thumbnail_url"),
}
CAST_FIELDS = {
    "bellesa": "pornstars", "empflix": "pornstars", "porn": "pornstars_names",
    "porndoe": "pornstars", "pornhat": "pornstars", "pornhub": "pornstars",
    "redtube": "pornstars_names", "tnaflix": "pornstars", "xhamster": "pornstars",
    "eporner": "performers", "xvideos": "performers", "youporn": "performers",
}


def value(source, name):
    if not name:
        return None
    try:
        # Some APIs expose async properties. Inspect first to avoid creating an
        # unawaited coroutine or interpreting a generator as descriptive data.
        descriptor = inspect.getattr_static(source, name, None)
        if isinstance(descriptor, property) and inspect.iscoroutinefunction(descriptor.fget):
            return None
        result = getattr(source, name, None)
    except (AttributeError, RuntimeError, DataNotLoadedError):
        return None
    if inspect.iscoroutine(result):
        result.close()
        return None
    return None if callable(result) or inspect.isawaitable(result) else result


def text(raw) -> str | None:
    if not isinstance(raw, str):
        return None
    result = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    result = " ".join(result.split())
    return None if result.casefold() in {"", "n/a", "none", "null", "not available"} else result


def public_url(raw, base="") -> str | None:
    if not isinstance(raw, str) or not raw:
        return None
    url = urlsplit(urljoin(base, raw))
    if url.scheme not in {"http", "https"} or not url.netloc or url.username or url.password:
        return None
    # Public page identities need viewkey on Pornhub; other query values may
    # include account/session/tracking tokens and are not portable metadata.
    query = parse_qs(url.query)
    kept = {"viewkey": query["viewkey"][0]} if "viewkey" in query and "pornhub" in url.hostname else {}
    return urlunsplit((url.scheme, url.netloc, url.path, urlencode(kept), ""))


def labels(raw) -> list[str]:
    if isinstance(raw, str):
        raw = raw.split(",")
    if isinstance(raw, dict):
        raw = list(raw)
    if not isinstance(raw, (tuple, list)):
        return []
    return list(dict.fromkeys(label for item in raw if (label := text(item.get("name") if isinstance(item, dict) else item))))


def credits(raw, urls=(), base="") -> list[Credit]:
    if not isinstance(raw, (list, tuple)):
        raw = [raw] if raw else []
    result = []
    for index, item in enumerate(raw):
        name = text(item.get("name") if isinstance(item, dict) else item)
        url = item.get("url") if isinstance(item, dict) else urls[index] if index < len(urls) else None
        if name and name not in [credit.name for credit in result]:
            result.append(Credit(name, public_url(url, base)))
    return result


def duration_seconds(raw, *, minutes=False) -> float | None:
    if raw is None or isinstance(raw, bool):
        return None
    string = str(raw).strip()
    try:
        number = float(string)
        return number * (60 if minutes else 1) if 0 < number < 864000 else None
    except ValueError:
        pass
    if re.fullmatch(r"\d+(?::\d{1,2}){1,2}", string):
        return sum(float(part) * 60 ** index for index, part in enumerate(reversed(string.split(":"))))
    iso = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?", string, re.I)
    if iso and any(iso.groups()):
        return sum(float(part or 0) * factor for part, factor in zip(iso.groups(), (3600, 60, 1)))
    # A minute-only display does not establish precise seconds.
    return None


def publication(raw) -> str | None:
    if isinstance(raw, (int, float)):
        from datetime import UTC
        try:
            return datetime.fromtimestamp(raw, UTC).date().isoformat()
        except (ValueError, OSError, OverflowError):
            return None
    string = text(raw)
    if not string or re.search(r"\bago\b", string, re.I):
        return None
    string = re.sub(r"^Published\s+on\s+", "", string, flags=re.I)
    try:
        return datetime.fromisoformat(string.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        pass
    for fmt in ("%B %d, %Y", "%b %d, %Y", "%Y-%m-%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(string, fmt).date().isoformat()
        except ValueError:
            pass
    return None


def source_identity(provider: str, url: str, source=None) -> tuple[str, str]:
    parts = urlsplit(url)
    path = parts.path
    kind = "short" if type(source).__name__ == "Short" or re.search(r"/(?:shorties|short|moments|shorts)/", path) else "video"
    if provider == "beeg" and (key := value(source, "key")):
        return kind, str(key)
    if provider == "pornhat" and (identifier := value(source, "video_id")):
        return kind, str(identifier)
    if provider == "xhamster":
        token = path.rstrip("/").rsplit("/", 1)[-1]
        match = re.search(r"(?:^|-)(xh[A-Za-z0-9]+|\d+)$", token)
        if match:
            return kind, match.group(1)
    patterns = {
        "beeg": r"/(-?\d+)", "bellesa": r"/videos/(\d+)",
        "empflix": r"/video(\d+)", "eporner": r"/(?:video-|hd-porn/|porno-video/|embed/)([A-Za-z0-9]+)",
        "porn": r"/scene/(\d+)", "porndoe": r"/watch/([^/]+)",
        "pornhat": r"/video/([^/]+)", "pornhub": r"/(?:shorties|embed)/([^/]+)",
        "porntrex": r"/video/(\d+)", "redgifs": r"/(?:watch|ifr)/([^/]+)",
        "redtube": r"/(\d+)", "spankbang": r"/([^/]+)/(?:video|embed|play)",
        "thumbzilla": r"/(?:watch|video)/([^/]+)", "tnaflix": r"/video(\d+)",
        "tube8": r"/(?:porn-video|video)/(\d+)", "xfreehd": r"/(?:video|embed)/(\d+)",
        "xhamster": r"/(?:videos|moments)/([^/]+)", "xnxx": r"/video[.-]([^/]+)",
        "xvideos": r"/video[.-]([^/]+)", "youporn": r"/(?:watch|embed)/(\d+)",
        "youjizz": r"/videos/.*?-(\d+)\.html",
    }
    if provider == "pornhub" and kind == "video" and (key := parse_qs(parts.query).get("viewkey")):
        return kind, key[0]
    if match := re.search(patterns[provider], path, re.I):
        return kind, match.group(1).lstrip("-") if provider == "beeg" else match.group(1)
    identifier = value(source, "video_id") if source is not None else None
    if identifier and str(identifier) != str(value(source, "title")):
        return kind, str(identifier)
    return kind, "url-" + hashlib.sha256(url.encode()).hexdigest()[:24]


def collect_library_metadata(provider: str, source, prepared) -> LibraryMetadata:
    description, duration, date, author, tags, categories, image = PROVIDER_FIELDS[provider]
    url = public_url(prepared.url)
    if url is None:
        raise ValueError("Metadata needs a public video page URL without credentials")
    kind, identity = source_identity(provider, url, source)
    snapshot = LibraryMetadata(provider, kind, identity, url, prepared.title)
    snapshot.description = text(value(source, description))
    if snapshot.description == text(prepared.title):
        snapshot.description = None
    raw_duration = value(source, duration)
    snapshot.duration_seconds = (None if provider == "xnxx" and str(raw_duration).isdigit()
                                 else duration_seconds(raw_duration))
    raw = value(source, date)
    snapshot.publication_raw = str(raw) if raw is not None else None
    snapshot.publication_kind = "fact_created" if provider == "beeg" else "platform_created" if provider in {"redgifs", "xhamster"} else "platform_upload"
    if raw is None or (provider in {"xnxx", "xvideos"} and value(source, "publish_date_source") != "uploadDate"):
        snapshot.publication_kind = "unknown"
    # Older XVideos/XNXX parsers merge uploadDate with an unrelated page comment.
    if provider not in {"xnxx", "xvideos"} or value(source, "publish_date_source") == "uploadDate":
        snapshot.publication_date = publication(raw) if provider != "beeg" else None
    snapshot.tags, snapshot.categories = labels(value(source, tags)), labels(value(source, categories))
    image_url = value(source, image)
    if isinstance(image_url, list):
        image_url = next(iter(image_url), None)
    snapshot.image_url = urljoin(url, image_url) if isinstance(image_url, str) and image_url else None
    base = url
    author_links = {"xfreehd": "author_url", "redtube": "author_url", "redgifs": "author_link", "youporn": "author_link", "xvideos": "author_link", "pornhub": "author_link"}
    if names := credits(value(source, author), [value(source, author_links.get(provider))], base):
        snapshot.uploader = names[0]
    cast_urls = value(source, "authors_urls" if provider == "eporner" else "pornstars_urls") or []
    snapshot.performers = credits(value(source, CAST_FIELDS.get(provider)), cast_urls, base)
    snapshot.performer_urls = [url for item in cast_urls if (url := public_url(item, base))]
    if provider == "bellesa":
        snapshot.content_providers = credits(value(source, "content_providers"), base=base) or credits(value(source, "author"), [value(source, "author_link")], base)
    elif provider == "porndoe":
        snapshot.producers = credits(value(source, "producers"), base=base)
        snapshot.publishers = credits(value(source, "publishers"), base=base)
        if not snapshot.producers and not snapshot.publishers:
            snapshot.publishers = credits(value(source, "author_name"), [value(source, "author_link")], base)
    elif provider in {"porn", "pornhat"}:
        snapshot.channels = credits(value(source, "author_name"), [value(source, "author_link")], base)
    elif provider == "beeg":
        # The existing author can be either an owner or person tag.
        snapshot.uploader = None
    if kind == "short":
        snapshot.performers, snapshot.performer_urls = [], []
        snapshot.categories = []
        if provider == "pornhub":
            snapshot.description = text(value(source, "meta_description"))
            snapshot.publication_date = snapshot.publication_raw = None
            snapshot.categories = labels(value(source, "categories"))
        elif provider == "xhamster":
            snapshot.description = None
            snapshot.uploader = next(iter(credits(value(source, "author"), [value(source, "author_link")], base)), None)
            snapshot.publication_raw = str(value(source, "created_at") or "") or None
            snapshot.publication_date = publication(value(source, "created_at"))
            snapshot.publication_kind = "platform_created" if snapshot.publication_raw else "unknown"
    if snapshot.description == text(prepared.title):
        snapshot.description = None
    if raw_duration is not None and snapshot.duration_seconds is None:
        snapshot.extras["duration_display"] = str(raw_duration)
    extra_fields = {
        "views", "likes", "dislikes", "rating", "rating_percent", "rating_percentage",
        "rating_value", "rating_count", "rating_votes", "rate", "niche_ids", "action_tags",
        "is_vr", "has_audio", "width", "height", "primary_category", "owners", "people",
    }
    for name in extra_fields:
        item = value(source, name)
        if item is not None and isinstance(item, (str, int, float, bool, list, dict)):
            snapshot.extras[name] = item
    return snapshot


assert set(PROVIDER_FIELDS) == set(PROVIDER_MODULES)
