"""Own the terminal application's provider sessions."""
from __future__ import annotations

from copy import copy
from dataclasses import replace
from typing import Any, AsyncIterator, Callable, Mapping

from src.shared.account_capabilities import ACCOUNT_PROVIDERS
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
    provider_client_class,
    resolve_container,
    resolve_video,
)
from src.shared.provider_routing import (
    route_url as route_url,
)
from src.shared.provider_routing import (
    unwrap_scrape_result as unwrap_scrape_result,
)
from src.shared.public_media import (
    PublicMediaUnavailableError,
    RestrictedMediaError,
    check_public_host,
    rejected_public_media,
    require_public_media,
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
        self._accounts: dict[str, Any] = {}
        self._account_cores: dict[str, Any] = {}
        self._closed = False

    def _make_core(self, account: bool) -> Any:
        configuration = copy(self.runtime_config)
        if hasattr(configuration, "cookies"):
            configuration.cookies = dict(configuration.cookies or {}) if account else None
        if self._core_factory:
            core = self._core_factory(configuration)
            core.account_only = account
            return core
        from src.shared.tor_transport import MediaCore
        return MediaCore(configuration=configuration, account_only=account)

    def client(self, provider: str) -> Any:
        return self._client(provider, self.clients, self.cores, account=False)

    def account_client(self, provider: str) -> Any:
        if provider not in ACCOUNT_PROVIDERS:
            raise ValueError(f"accounts are not supported for {provider}")
        return self._client(provider, self._accounts, self._account_cores, account=True)

    def _client(self, provider: str, clients: dict, cores: dict, *, account: bool) -> Any:
        if self._closed:
            raise RuntimeError("client pool is closed")
        if provider not in PROVIDER_MODULES:
            raise ValueError(f"unsupported provider: {provider}")
        if provider not in clients:
            core = self._make_core(account)
            factory = self._factories.get(provider)
            if factory is None:
                factory = provider_client_class(provider)
            try:
                client = factory(core=core)
            except TypeError:
                client = factory(core)
            cores[provider] = core
            clients[provider] = client
        return clients[provider]

    async def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        unique = list(dict.fromkeys([*self.cores.values(), *self._account_cores.values()]))
        await _close_all(unique)
        self.clients.clear()
        self.cores.clear()
        self._accounts.clear()
        self._account_cores.clear()

    async def __aenter__(self) -> "ClientPool":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    async def resolve(self, url: str, *, pages: int | str = 5) -> tuple[Route, Any]:
        check_public_host(url)
        route = route_url(url)
        client = self.client(route.provider)
        if route.kind == ContentKind.VIDEO:
            try:
                return route, await resolve_video(client, route)
            except RestrictedMediaError:
                raise
            except Exception as error:
                if rejected_public_media(error):
                    raise PublicMediaUnavailableError() from error
                raise
        if route.kind == ContentKind.GALLERY:
            album = await _await_if_needed(client.get_album(url, load_html=True))
            require_public_media(album)
            return route, album
        target = await resolve_container(client, route, pages=pages)
        if route.provider == "porn":
            from porn_api import Channel, Pornstar
            kind = ContentKind.PROFILE if isinstance(target, (Channel, Pornstar)) else ContentKind.COLLECTION
            route = replace(route, kind=kind, profile_mode=None)
        return route, target

    async def media_stream(self, url: str, *, pages: int | str = 5) -> AsyncIterator[Any]:
        route, source = await self.resolve(url, pages=pages)
        if route.kind in {ContentKind.VIDEO, ContentKind.GALLERY}:
            yield source
            return
        stream = container_stream(
            source, pages=pages, provider=route.provider,
            profile_mode=route.profile_mode or getattr(self.runtime_config, "profile_video_mode", "videos"),
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
