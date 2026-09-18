"""Provider routing and common async source adapters."""
from __future__ import annotations

import inspect
import re
from dataclasses import dataclass
from enum import StrEnum
from importlib import import_module
from typing import Any, AsyncIterator, Callable, Mapping
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
    "eporner": {"pornstar", "profile", "channel"},
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
    segments = {segment for segment in parsed.path.casefold().split("/") if segment}
    if provider == "xfreehd" and "album" in segments:
        kind = ContentKind.GALLERY
    elif (
        segments & COLLECTION_SEGMENTS.get(provider, set())
        or any(s.startswith("playlist") for s in segments)
    ):
        kind = ContentKind.COLLECTION
    elif segments & PROFILE_SEGMENTS.get(provider, set()):
        kind = ContentKind.PROFILE
    else:
        kind = ContentKind.VIDEO
    return Route(provider, kind, url.strip())


class ClientPool:
    """Own one isolated BaseCore and API client for each supported provider."""

    def __init__(
        self,
        runtime_config: Any,
        *,
        client_factories: Mapping[str, Callable[..., Any]] | None = None,
        core_factory: Callable[..., Any] | None = None,
    ) -> None:
        self.runtime_config = runtime_config
        self._factories = dict(client_factories or {})
        self._core_factory = core_factory
        self.clients: dict[str, Any] = {}
        self.cores: dict[str, Any] = {}
        self._closed = False

    def _make_core(self) -> Any:
        if self._core_factory:
            return self._core_factory(self.runtime_config)
        from base_api import BaseCore
        return BaseCore(configuration=self.runtime_config)

    def client(self, provider: str) -> Any:
        if self._closed:
            raise RuntimeError("client pool is closed")
        if provider not in PROVIDER_MODULES:
            raise ValueError(f"unsupported provider: {provider}")
        if provider not in self.clients:
            core = self._make_core()
            factory = self._factories.get(provider)
            if factory is None:
                factory = import_module(PROVIDER_MODULES[provider]).Client
            try:
                client = factory(core=core)
            except TypeError:
                client = factory(core)
            self.cores[provider] = core
            self.clients[provider] = client
        return self.clients[provider]

    async def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        unique = list(dict.fromkeys(self.cores.values()))
        await _close_all(unique)
        self.clients.clear()
        self.cores.clear()

    async def __aenter__(self) -> "ClientPool":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    async def resolve(self, url: str) -> tuple[Route, Any]:
        route = route_url(url)
        client = self.client(route.provider)
        if route.kind == ContentKind.VIDEO:
            return route, await _get_video(client, route)
        if route.kind == ContentKind.GALLERY:
            return route, await _await_if_needed(client.get_album(url, load_html=True))
        return route, await _get_container(client, route)

    async def media_stream(self, url: str, *, pages: int = 5) -> AsyncIterator[Any]:
        route, source = await self.resolve(url)
        if route.kind in {ContentKind.VIDEO, ContentKind.GALLERY}:
            yield source
            return
        stream = _container_stream(
            source, pages=pages, provider=route.provider,
            profile_mode=getattr(self.runtime_config, "profile_video_mode", "videos"),
        )
        try:
            async for item in stream:
                yield unwrap_scrape_result(item)
        finally:
            close = getattr(stream, "aclose", None)
            if close:
                await close()


async def _close_all(items: list[Any]) -> None:
    import asyncio
    await asyncio.gather(*(
        _await_if_needed(item.close()) for item in items if hasattr(item, "close")
    ), return_exceptions=True)


async def _await_if_needed(value: Any) -> Any:
    return await value if inspect.isawaitable(value) else value


async def _get_video(client: Any, route: Route) -> Any:
    path = urlparse(route.url).path.casefold()
    configuration = getattr(getattr(client, "core", None), "configuration", None)
    load_api = not getattr(configuration, "strict_language", False)
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
    try:
        return await _await_if_needed(client.get_video(route.url, load_html=True))
    except TypeError:
        return await _await_if_needed(client.get_video(route.url))


async def _get_container(client: Any, route: Route) -> Any:
    if route.kind == ContentKind.COLLECTION:
        if route.provider == "xvideos":
            return client.get_playlist(route.url)
        name = {
            "youporn": "get_collection",
        }.get(route.provider, "get_playlist")
        return await _await_if_needed(getattr(client, name)(route.url, load_html=True))

    segments = {part for part in urlparse(route.url).path.casefold().split("/") if part}
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
        method = "get_creator" if "creator" in segments or "creators" in segments else (
            "get_channel" if "channel" in segments or "channels" in segments else "get_pornstar"
        )
    elif route.provider == "porntrex":
        method = "get_channel" if "channel" in segments else "get_model"
    elif route.provider in {"xvideos", "youporn"}:
        method = "get_channel" if "channel" in segments or "channels" in segments else "get_pornstar"
    elif route.provider == "xnxx":
        method = "get_user"
    else:
        method = "get_pornstar"
    return await _await_if_needed(getattr(client, method)(route.url, load_html=True))


def _container_stream(
    container: Any, *, pages: int, provider: str, profile_mode: str = "videos",
) -> AsyncIterator[Any]:
    if hasattr(container, "__aiter__"):
        return container
    if provider == "pornhub" and profile_mode in {"uploads", "both"} and hasattr(container, "get_uploads"):
        videos = _call_stream(container, "get_videos", pages) if profile_mode == "both" else None
        uploads = _call_stream(container, "get_uploads", pages)
        return _chain_streams(*(stream for stream in (videos, uploads) if stream is not None))
    for name in ("get_videos", "videos"):
        if getattr(container, name, None):
            return _call_stream(container, name, pages)
    raise ValueError(f"{provider} source does not expose a video stream")


def _call_stream(container: Any, name: str, pages: int) -> AsyncIterator[Any]:
    method = getattr(container, name)
    try:
        return method(pages=pages)
    except TypeError:
        return method()


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
