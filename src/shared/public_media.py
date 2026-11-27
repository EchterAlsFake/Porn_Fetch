"""Public playback rules shared by the GUI and CLI."""

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from base_api import is_resource_gone
from base_api.modules.errors import AccessDeniedError, RegionBlocked

from .media import VideoObject
from .provider_parsing import parse_length

RESTRICTED_HOSTS = frozenset({
    "pornhubpremium.com", "xvideos.red", "xhamsterpremium.com", "faphouse.com",
    "bellesaplus.co", "bellesaplus.com",
})
RESTRICTED_MESSAGE = "Porn Fetch downloads only publicly available media. This item is paid or restricted."
UNAVAILABLE_MESSAGE = (
    "The website did not provide a downloadable video while signed out. "
    "It may be paid, private, or no longer available."
)


class RestrictedMediaError(ValueError):
    def __init__(self) -> None:
        super().__init__(RESTRICTED_MESSAGE)


class PublicMediaUnavailableError(ValueError):
    def __init__(self) -> None:
        super().__init__(UNAVAILABLE_MESSAGE)


def restricted_host(url: str) -> bool:
    host = (urlsplit(url).hostname or "").casefold().rstrip(".")
    return any(host == domain or host.endswith("." + domain) for domain in RESTRICTED_HOSTS)


def restricted_url(url: str) -> bool:
    parsed = urlsplit(url)
    return parsed.username is not None or parsed.password is not None or restricted_host(url)


def check_public_host(url: str) -> None:
    if restricted_url(url):
        raise RestrictedMediaError()


def account_media(media) -> bool:
    return getattr(getattr(media, "core", None), "account_only", False) is True


def listed_value(media, name, default=None):
    """Read already loaded listing data without fetching authenticated details."""
    fields = getattr(type(media), "__dataclass_fields__", None)
    if fields is not None and name not in fields:
        return default
    check = getattr(type(media), "is_field_loaded", None)
    if check is not None and not check(media, name):
        return default
    value = getattr(media, name, default)
    return default if value is None else value


def restricted_media(media) -> bool:
    return (listed_value(media, "is_premium") is True or listed_value(media, "is_private") is True
            or (type(media).__module__.startswith("redgifs_api.") and listed_value(media, "published") is False)
            or any(restricted_url(url) for field in ("url", "resolved_url")
                   if isinstance(url := listed_value(media, field), str)))


def require_public_media(media) -> None:
    if account_media(media) or restricted_media(media):
        raise RestrictedMediaError()


def guest_account_url(url: str) -> str:
    """Keep the watch identifier while discarding account query data."""
    parts = urlsplit(url)
    host = parts.hostname or ""
    pornhub = any(host == domain or host.endswith("." + domain)
                  for domain in ("pornhub.com", "pornhubpremium.com"))
    query = urlencode([(key, val) for key, val in parse_qsl(parts.query) if key == "viewkey"]) if pornhub else ""
    return urlunsplit(("https", host, parts.path, query, ""))


def account_video_row(media, provider: str) -> VideoObject:
    url = guest_account_url(str(listed_value(media, "url", "")))
    video_id = str(listed_value(media, "video_id", ""))
    length = listed_value(media, "length_seconds") or listed_value(media, "duration") or listed_value(media, "length")
    return VideoObject(
        url=url, title=str(listed_value(media, "title", video_id or "Untitled video")),
        author=str(listed_value(media, "author_name", "")), length=parse_length(length, video_source=provider),
        tags=None, thumbnail_url="", video_id=video_id, publish_date=None, qualities=[], status="pending",
        is_from_account=True, provider_restricted=restricted_media(media),
    )


def rejected_public_media(error: BaseException) -> bool:
    seen = set()
    pending = [error]
    while pending:
        current = pending.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))
        if isinstance(current, (RestrictedMediaError, PublicMediaUnavailableError, AccessDeniedError, RegionBlocked)):
            return True
        if is_resource_gone(current):
            return True
        status = getattr(current, "status_code", None) or getattr(getattr(current, "response", None), "status_code", None)
        if status in {401, 403, 404, 410, 451}:
            return True
        pending.extend(item for item in (current.__cause__, current.__context__) if item is not None)
        original = getattr(current, "original_error", None)
        if isinstance(original, BaseException):
            pending.append(original)
        pending.extend(item for item in getattr(current, "errors", ()) or () if isinstance(item, BaseException))
    return False
