"""Qt-free provider routing and discovery shared by GUI and CLI."""
from __future__ import annotations

import inspect
import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, AsyncIterator
from urllib.parse import urlparse


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


PROVIDER_MODULES = {
    "pornhub": "pornhub_api", "eporner": "eporner_api", "xnxx": "xnxx_api",
    "xvideos": "xvideos_api", "xhamster": "xhamster_api",
    "spankbang": "spankbang_api", "youporn": "youporn_api", "beeg": "beeg_api",
    "porntrex": "porntrex_api", "xfreehd": "xfreehd_api", "redtube": "redtube_api",
    "thumbzilla": "thumbzilla_api", "tube8": "tube8_api",
}

HOST_PATTERNS = {
    "pornhub": r"(?:^|\.)pornhub(?:premium)?\.com$",
    "eporner": r"(?:^|\.)eporner\.com$",
    "xnxx": r"(?:^|\.)xnxx\d*\.com$",
    "xvideos": r"(?:^|\.)xvideos\d*\.com$",
    "xhamster": r"(?:^|\.)xhamster\d*\.com$",
    "spankbang": r"(?:^|\.)spankbang\.com$",
    "youporn": r"(?:^|\.)youporn\.com$",
    "beeg": r"(?:^|\.)beeg\.com$",
    "porntrex": r"(?:^|\.)porntrex\.com$",
    "xfreehd": r"(?:^|\.)xfreehd\.com$",
    "redtube": r"(?:^|\.)redtube\.com$",
    "thumbzilla": r"(?:^|\.)thumbzilla\.com$",
    "tube8": r"(?:^|\.)tube8\.com$",
}

PROFILE_SEGMENTS = {
    "pornhub": {"pornstar", "model", "users", "user", "channels", "channel"},
    "eporner": {"pornstar", "profile", "channel", "channels"},
    "xnxx": {"profile", "user", "users", "pornstar"},
    "xvideos": {"pornstar", "pornstars", "model", "profiles", "channels", "channel"},
    "xhamster": {"pornstars", "pornstar", "creators", "creator", "users", "channels", "channel"},
    "spankbang": {"pornstar", "profile", "creator", "channel"},
    "youporn": {"pornstar", "channel"},
    "porntrex": {"model", "models", "channel", "channels"},
    "redtube": {"pornstar", "channel", "amateur", "users", "user"},
    "thumbzilla": {"pornstar", "channel", "amateur"},
    "tube8": {"pornstar", "channel", "amateur", "user", "users"},
}

COLLECTION_SEGMENTS = {
    "pornhub": {"playlist"}, "xvideos": {"playlist", "favorite"},
    "youporn": {"collections", "collection"}, "redtube": {"playlist"},
    "thumbzilla": {"playlist"},
}


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
    section = parts[0] if parts else ""
    if provider in {"xfreehd", "pornhub"} and section == "album":
        kind = ContentKind.GALLERY
    elif section in COLLECTION_SEGMENTS.get(provider, set()):
        kind = ContentKind.COLLECTION
    elif section in PROFILE_SEGMENTS.get(provider, set()):
        kind = ContentKind.PROFILE
    elif provider == "xvideos" and len(parts) == 1 and not parsed.query and not (
        section.startswith("video") or section in {"account", "history", "search", "new", "best", "tags"}
    ):
        kind = ContentKind.PROFILE
    else:
        kind = ContentKind.VIDEO
    return Route(provider, kind, url.strip())


async def _await_if_needed(value: Any) -> Any:
    return await value if inspect.isawaitable(value) else value


async def resolve_video(client: Any, route: Route, *, strict_language: bool | None = None) -> Any:
    path = urlparse(route.url).path.casefold()
    configuration = getattr(getattr(client, "core", None), "configuration", None)
    load_api = not (getattr(configuration, "strict_language", False) if strict_language is None else strict_language)
    if route.provider == "pornhub" and ("/short/" in path or "/shorties/" in path):
        return await _await_if_needed(client.get_short(route.url, load_html=True))
    if route.provider == "xhamster" and ("/moments/" in path or "/shorts/" in path):
        return await _await_if_needed(client.get_short(route.url, load_html=True))
    if route.provider == "eporner":
        return await _await_if_needed(client.get_video(
            route.url, load_html=True,
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
    section = urlparse(route.url).path.casefold().strip("/").split("/")[0]
    segments = {section}
    if route.provider == "pornhub":
        method = "get_channel" if segments & {"channel", "channels"} else (
            "get_model" if "model" in segments else (
                "get_user" if segments & {"user", "users"} else "get_pornstar"
            )
        )
    elif route.provider in {"redtube", "thumbzilla", "tube8"}:
        method = "get_amateur" if "amateur" in segments else (
            "get_channel" if "channel" in segments else (
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
        method = "get_pornstar" if segments & {"pornstar", "pornstars", "model", "profiles"} else "get_channel"
    elif route.provider == "xnxx":
        method = "get_user"
    elif route.provider == "eporner":
        method = "get_pornstar" if section == "pornstar" else "get_channel"
    else:
        method = "get_pornstar"
    return await _await_if_needed(getattr(client, method)(route.url, load_html=True))


def container_stream(
    container: Any, *, pages: int, provider: str, profile_mode: str = "videos",
    iterator_config: Any = None,
) -> AsyncIterator[Any]:
    if hasattr(container, "__aiter__"):
        return container
    if provider == "pornhub" and profile_mode in {"uploads", "both"} and hasattr(container, "get_uploads"):
        videos = _call_stream(container, "get_videos", pages) if profile_mode == "both" else None
        uploads = _call_stream(container, "get_uploads", pages)
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
