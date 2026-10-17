"""Qt-free provider routing and discovery shared by GUI and CLI."""
from __future__ import annotations

import inspect
import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, AsyncIterator
from urllib.parse import parse_qs, urljoin, urlparse


class ContentKind(StrEnum):
    VIDEO = "video"
    PROFILE = "profile"
    COLLECTION = "collection"
    GALLERY = "gallery"


@dataclass(frozen=True, slots=True)
class Route:
    provider: str
    kind: ContentKind
    url: str
    profile_mode: str | None = None


PROVIDER_MODULES = {
    "pornhub": "pornhub_api", "eporner": "eporner_api", "xnxx": "xnxx_api",
    "xvideos": "xvideos_api", "xhamster": "xhamster_api",
    "spankbang": "spankbang_api", "youporn": "youporn_api", "beeg": "beeg_api",
    "porntrex": "porntrex_api", "xfreehd": "xfreehd_api", "redtube": "redtube_api",
    "thumbzilla": "thumbzilla_api", "tube8": "tube8_api",
    "empflix": "empflix_api", "tnaflix": "tnaflix_api",
}

HOST_PATTERNS = {
    "pornhub": r"(?:^|\.)pornhub(?:premium)?\.com$",
    "eporner": r"(?:^|\.)eporner\.com$",
    "xnxx": r"(?:^|\.)xnxx\d*\.com$",
    "xvideos": r"(?:^|\.)xvideos\d*\.com$",
    "xhamster": r"(?:^|\.)xhamster(?:\d*\.com|\.desi)$",
    "spankbang": r"(?:^|\.)spankbang\.com$",
    "youporn": r"(?:^|\.)youporn\.com$",
    "beeg": r"(?:^|\.)beeg\.com$",
    "porntrex": r"(?:^|\.)porntrex\.com$",
    "xfreehd": r"(?:^|\.)xfreehd\.com$",
    "redtube": r"(?:^|\.)redtube\.com$",
    "thumbzilla": r"(?:^|\.)thumbzilla\.com$",
    "tube8": r"(?:^|\.)tube8\.com$",
    "empflix": r"(?:^|\.)empflix\.com$",
    "tnaflix": r"(?:^|\.)tnaflix\.com$",
}

PROFILE_SEGMENTS = {
    "pornhub": {"pornstar", "model", "users", "user", "channels", "channel"},
    "eporner": {"pornstar", "pornostar", "channel", "channels"},
    "xnxx": {"profile", "user", "users", "pornstar"},
    "xvideos": {"pornstar", "pornstars", "model", "models", "profiles", "channels", "channel", "amateur-channels"},
    "xhamster": {"pornstars", "pornstar", "creators", "creator", "users", "channels", "channel"},
    "spankbang": {"pornstar", "profile", "creator", "channel"},
    "youporn": {"pornstar", "channel"},
    "porntrex": {"model", "models", "channel", "channels"},
    "redtube": {"pornstar", "channel", "channels", "amateur", "users", "user"},
    "thumbzilla": {"pornstar", "channel", "amateur"},
    "tube8": {"pornstar", "channel", "amateur", "user", "users"},
    "empflix": {"profile", "pornstar", "pornstars"},
    "tnaflix": {"profile", "pornstar", "pornstars", "channel", "channels"},
}

COLLECTION_SEGMENTS = {
    "pornhub": {"playlist"}, "xvideos": {"playlist", "favorite"},
    "youporn": {"collections", "collection"}, "redtube": {"playlist"},
    "thumbzilla": {"playlist"},
}


def _content_section(provider: str, parts: list[str]) -> str:
    section = parts[0] if parts else ""
    # SpankBang puts an ID or locale before the profile type.
    if provider == "spankbang" and section not in PROFILE_SEGMENTS[provider]:
        if len(parts) >= 3 and parts[1] in PROFILE_SEGMENTS[provider]:
            return parts[1]
    return section


def route_url(url: str) -> Route:
    parsed = urlparse(url.strip())
    if parsed.scheme.casefold() not in {"http", "https"} or not parsed.hostname:
        raise ValueError("a complete HTTP(S) URL is required")
    host = parsed.hostname.casefold()
    provider = next(
        (name for name, pattern in HOST_PATTERNS.items() if re.search(pattern, host, re.I)),
        None,
    )
    if provider is None:
        raise ValueError(f"unsupported provider host: {host}")
    parts = [segment for segment in parsed.path.casefold().split("/") if segment]
    section = _content_section(provider, parts)
    query = parse_qs(parsed.query)
    mode = None
    if provider == "xvideos" and parsed.fragment.startswith("quickies/"):
        raise ValueError("XVideos Quickies links are not supported")
    if provider in {"xfreehd", "pornhub"} and section == "album" and len(parts) >= 2:
        kind = ContentKind.GALLERY
    elif section in COLLECTION_SEGMENTS.get(provider, set()):
        has_id = len(parts) >= 2 or bool(query.get("playlist_id") or query.get("id"))
        if provider == "youporn":
            has_id = len(parts) >= 3 and parts[1] == "videos" and parts[2].isdigit()
        if not has_id:
            raise ValueError("An individual playlist or collection URL is required")
        kind = ContentKind.COLLECTION
    elif section in PROFILE_SEGMENTS.get(provider, set()):
        offset = 1 if provider == "spankbang" and parts[0] != section else 0
        if len(parts) < offset + 2:
            raise ValueError("An individual profile or channel URL is required")
        name = parts[offset + 1]
        if ((provider == "xhamster" and name in {"all", "contest", "videos"})
                or (provider == "pornhub" and section in {"user", "users"} and name in {"search", "discover"})):
            raise ValueError("Profile directories are not supported")
        suffix = parts[offset + 2:]
        if any(part in {"shorts", "moments", "albums", "photos", "gifs", "favorites"} for part in suffix):
            raise ValueError("This profile tab is not supported for video fetching")
        if provider == "pornhub" and suffix[:1] == ["videos"]:
            mode = "uploads" if suffix[1:2] == ["upload"] else "videos"
        kind = ContentKind.PROFILE
    elif provider == "xvideos" and parts and not section.startswith("video") and section not in {
        "account", "history", "search", "new", "best", "tags", "lang", "c", "pornstars",
        "channels", "models", "profiles", "amateur-channels", "watch-later", "videos-i-like",
    } and (len(parts) == 1 or parts[1:3] == ["videos", "best"]):
        kind = ContentKind.PROFILE
    elif _is_video_url(provider, parsed.path, query):
        kind = ContentKind.VIDEO
    else:
        raise ValueError(f"Unsupported {provider} URL type; enter an individual supported media URL")
    return Route(provider, kind, url.strip(), profile_mode=mode)


def _is_video_url(provider: str, path: str, query: dict[str, list[str]]) -> bool:
    patterns = {
        "eporner": r"^/(?:video-[a-z0-9]+|(?:hd-porn|embed|porno-video)/[a-z0-9]+)(?:/|$)",
        "xnxx": r"^/video-?[a-z0-9]+(?:/|$)",
        "xvideos": r"^/(?:video\.?[a-z0-9]+|embedframe/[a-z0-9]+)(?:/|$)",
        "xhamster": r"^/(?:videos|movies|moments|shorts)/[^/]+",
        "spankbang": r"^/[a-z0-9]+/(?:video|play|embed)(?:/|$)|^/[a-z0-9]+-[a-z0-9]+/playlist/[^/]+",
        "youporn": r"^/(?:watch|embed)/[0-9]+(?:/|$)",
        "beeg": r"^/(?:video/)?-?[0-9]+/?$",
        "porntrex": r"^/video/[0-9]+(?:/|$)",
        "xfreehd": r"^/video/[0-9]+(?:/|$)",
        "redtube": r"^/[0-9]+/?$",
        "thumbzilla": r"^/watch/[0-9]+(?:/|$)",
        "tube8": r"^/(?:porn-video|video)/[0-9]+(?:/|$)",
        "empflix": r"^/(?:(?:[^/]+/)+video[0-9]+|video[0-9]+|videos?/[0-9]+|videos?/[^/]+-[0-9]+\.html)(?:/|$)",
        "tnaflix": r"^/(?:(?:[^/]+/)+video[0-9]+|video[0-9]+|videos?/[0-9]+|videos?/[^/]+-[0-9]+\.html)(?:/|$)",
    }
    if provider == "pornhub":
        return (path in {"/view_video.php", "/video/show"} and bool(query.get("viewkey"))) or bool(
            re.match(r"^/(?:embed|short|shorties)/[a-z0-9]+(?:/|$)", path, re.I)
        )
    return bool(re.match(patterns[provider], path, re.I))


async def _await_if_needed(value: Any) -> Any:
    return await value if inspect.isawaitable(value) else value


def eporner_video_id(url: str) -> str | None:
    """Retain the case-sensitive ID in canonical and localized video paths."""
    match = re.match(r"^/(?:video-|(?:hd-porn|embed|porno-video)/)([a-z0-9]+)(?:/|$)",
                     urlparse(url).path, re.I)
    return match.group(1) if match else None


async def resolve_video(client: Any, route: Route, *, strict_language: bool | None = None) -> Any:
    path = urlparse(route.url).path.casefold()
    configuration = getattr(getattr(client, "core", None), "configuration", None)
    load_api = not (getattr(configuration, "strict_language", False) if strict_language is None else strict_language)
    if route.provider == "pornhub" and re.match(r"^/(?:short|shorties)/", path):
        return await _await_if_needed(client.get_short(route.url, load_html=True))
    if route.provider == "xhamster" and re.match(r"^/(?:moments|shorts)/", path):
        return await _await_if_needed(client.get_short(route.url, load_html=True))
    if route.provider == "eporner":
        url = route.url
        if path.startswith("/porno-video/") and (video_id := eporner_video_id(url)):
            url = urlparse(url)._replace(path=f"/video-{video_id}/").geturl()
        return await _await_if_needed(client.get_video(
            url, load_html=True,
            load_api=load_api,
        ))
    if route.provider == "pornhub":
        return await _await_if_needed(client.get_video(
            route.url, load_html=True,
            load_api=load_api,
        ))
    if route.provider == "beeg":
        return await _await_if_needed(client.get_video(route.url, load_api=True))
    return await _await_if_needed(client.get_video(route.url, load_html=True))


async def resolve_container(client: Any, route: Route, *, pages: int = 5) -> Any:
    if route.kind == ContentKind.COLLECTION:
        if route.provider not in COLLECTION_SEGMENTS:
            raise ValueError(f"public playlists are not supported for {route.provider}")
        if route.provider == "xvideos":
            return client.get_playlist(route.url, pages=pages)
        name = {
            "youporn": "get_collection",
        }.get(route.provider, "get_playlist")
        return await _await_if_needed(getattr(client, name)(route.url, load_html=True))

    if route.kind != ContentKind.PROFILE or route.provider not in PROFILE_SEGMENTS:
        raise ValueError(f"profiles are not supported for {route.provider}")
    parsed = urlparse(route.url)
    original_parts = [segment for segment in parsed.path.split("/") if segment]
    parts = [segment.casefold() for segment in original_parts]
    section = _content_section(route.provider, parts)
    segments = {section}
    if route.provider == "pornhub":
        method = "get_channel" if segments & {"channel", "channels"} else (
            "get_model" if "model" in segments else (
                "get_user" if segments & {"user", "users"} else "get_pornstar"
            )
        )
    elif route.provider in {"redtube", "thumbzilla", "tube8"}:
        method = "get_amateur" if "amateur" in segments else (
            "get_channel" if segments & {"channel", "channels"} else (
                "get_user" if segments & {"user", "users"} else "get_pornstar"
            )
        )
    elif route.provider in {"xhamster", "spankbang"}:
        method = "get_creator" if segments & {"creator", "creators", "users", "profile"} else (
            "get_channel" if "channel" in segments or "channels" in segments else "get_pornstar"
        )
    elif route.provider == "porntrex":
        method = "get_channel" if segments & {"channel", "channels"} else "get_model"
    elif route.provider in {"xvideos", "youporn"}:
        method = "get_pornstar" if segments & {"pornstar", "pornstars", "model", "models", "profiles"} else "get_channel"
    elif route.provider == "xnxx":
        method = "get_user"
    elif route.provider == "eporner":
        method = "get_pornstar" if section in {"pornstar", "pornostar"} else "get_channel"
    elif route.provider == "tnaflix":
        method = "get_channel" if segments & {"channel", "channels"} else (
            "get_pornstar" if segments & {"pornstar", "pornstars"} else "get_profile"
        )
    elif route.provider == "empflix":
        method = "get_pornstar" if segments & {"pornstar", "pornstars"} else "get_profile"
    else:
        method = "get_pornstar"
    # AJAX/video tabs can return JSON or omit the profile header. Load identity
    # from the base profile before creating its listing stream. Keep spelling,
    # filters and the requested upload mode (already recorded on Route).
    target_url = route.url
    if route.provider in {"pornhub", "xnxx", "xvideos"}:
        depth = 1 if route.provider == "xvideos" and section not in PROFILE_SEGMENTS["xvideos"] else 2
        if parts[depth:depth + 1] == ["videos"]:
            target_url = parsed._replace(path="/" + "/".join(original_parts[:depth]), fragment="").geturl()
    target = await _await_if_needed(getattr(client, method)(target_url, load_html=True))
    if route.provider == "xhamster" and section == "users" and hasattr(client, "core"):
        # User pages can link their public Creator identity in the personal-info
        # block. Their own root is not the Creator's video listing.
        from selectolax.lexbor import LexborHTMLParser

        html = await client.core.fetch_text(target_url)
        parser = LexborHTMLParser(html)
        for anchor in parser.css(".personal-info-block .user-details a[href]"):
            linked = urljoin(target_url, anchor.attributes["href"])
            parsed_link = urlparse(linked)
            if (parsed_link.path.startswith("/creators/") and parsed_link.hostname
                    and re.search(HOST_PATTERNS["xhamster"], parsed_link.hostname, re.I)):
                target = await _await_if_needed(client.get_creator(linked, load_html=True))
                break
    resolved = getattr(target, "resolved_url", None)
    if route.provider == "xvideos" and section == "profiles" and isinstance(resolved, str):
        resolved_section = urlparse(resolved).path.strip("/").split("/")[0]
        if resolved_section in {"channel", "channels", "amateur-channels"}:
            target = await _await_if_needed(client.get_channel(resolved, load_html=True))
    return target


def container_stream(
    container: Any, *, pages: int, provider: str, profile_mode: str = "videos",
    iterator_config: Any = None,
) -> AsyncIterator[Any]:
    if hasattr(container, "__aiter__"):
        return container
    if provider == "pornhub" and profile_mode in {"uploads", "both"} and hasattr(container, "get_uploads"):
        videos = _call_stream(container, "get_videos", pages, iterator_config) if profile_mode == "both" else None
        uploads = _call_stream(container, "get_uploads", pages, iterator_config)
        return _chain_streams(*(stream for stream in (videos, uploads) if stream is not None))
    for name in ("get_videos", "videos"):
        if getattr(container, name, None):
            return _call_stream(container, name, pages, iterator_config)
    raise ValueError(f"{provider} source does not expose a video stream")


def _call_stream(container: Any, name: str, pages: int, iterator_config: Any = None) -> AsyncIterator[Any]:
    method = getattr(container, name)
    options: dict[str, Any] = {"pages": pages}
    if iterator_config is not None:
        options["iterator_config"] = iterator_config
    return method(**options)


async def _chain_streams(*streams: AsyncIterator[Any]) -> AsyncIterator[Any]:
    for stream in streams:
        try:
            async for item in stream:
                yield item
        finally:
            close = getattr(stream, "aclose", None)
            if close:
                await close()


def unwrap_scrape_result(result: Any) -> Any:
    """Accept plain media objects and Base API ScrapeResult values."""
    if not hasattr(result, "succeeded"):
        return result
    if not result.succeeded:
        error = getattr(result, "error", None)
        if error is not None:
            raise error
        raise RuntimeError("provider returned an unsuccessful scrape result")
    unwrap = getattr(result, "unwrap", None)
    if unwrap:
        return unwrap()
    item = getattr(result, "item", None)
    if item is None:
        raise RuntimeError("successful scrape result contains no media")
    return item
