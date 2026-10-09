"""Own the terminal application's provider sessions."""
from __future__ import annotations

from importlib import import_module
from typing import Any, AsyncIterator, Callable, Mapping

from src.shared.provider_routing import (
    PROVIDER_MODULES as PROVIDER_MODULES,
)
from src.shared.provider_routing import (
    ContentKind as ContentKind,
)
from src.shared.provider_routing import (
    Route as Route,
)
from src.shared.provider_routing import (
    _await_if_needed,
    container_stream,
    resolve_container,
    resolve_video,
)
from src.shared.provider_routing import (
    route_url as route_url,
)
from src.shared.provider_routing import (
    unwrap_scrape_result as unwrap_scrape_result,
)


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

    async def resolve(self, url: str, *, pages: int = 5) -> tuple[Route, Any]:
        route = route_url(url)
        client = self.client(route.provider)
        if route.kind == ContentKind.VIDEO:
            return route, await resolve_video(client, route)
        if route.kind == ContentKind.GALLERY:
            return route, await _await_if_needed(client.get_album(url, load_html=True))
        return route, await resolve_container(client, route, pages=pages)

    async def media_stream(self, url: str, *, pages: int = 5) -> AsyncIterator[Any]:
        route, source = await self.resolve(url, pages=pages)
        if route.kind in {ContentKind.VIDEO, ContentKind.GALLERY}:
            yield source
            return
        stream = container_stream(
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
