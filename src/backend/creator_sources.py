"""Provider sessions for creator listings, using the existing media transport."""
from contextlib import aclosing, asynccontextmanager
from copy import copy
from dataclasses import replace

from base_api.modules.config import config

from src.backend import clients
from src.backend.config import app_settings
from src.shared.creator_library import listing_item, loaded, source_url
from src.shared.creator_scans import discover, listing_config
from src.shared.provider_routing import ContentKind, provider_client_class, resolve_container, route_url
from src.shared.tor_transport import MediaCore


@asynccontextmanager
async def session(provider):
    settings = copy(config)
    settings.response_cache_ttl = 0
    settings.response_cache_size_bytes = 0
    async with MediaCore(configuration=settings, settings=app_settings) as core:
        original = clients.client_for(provider).core
        core.default_headers.update(original.default_headers)
        client = provider_client_class(provider)(core=core)
        yield client


async def resolve(client, url, mode=None):
    route = route_url(source_url(url))
    target = await resolve_container(client, route, pages="all", iterator_config=listing_config())
    if route.provider == "porn":
        from porn_api import Channel, Pornstar
        route = replace(route, kind=ContentKind.PROFILE if isinstance(target, (Channel, Pornstar)) else ContentKind.COLLECTION)
    if mode:
        route = replace(route, profile_mode=mode)
    elif route.provider == "pornhub" and hasattr(target, "get_uploads"):
        route = replace(route, profile_mode=route.profile_mode or "uploads")
    return route, target


async def resolve_subscription(url):
    provider = route_url(url).provider
    async with session(provider) as client:
        route, target = await resolve(client, url)
        try:
            resolved = loaded(target, "resolved_url") or loaded(target, "url") or url
            # Iterator-only sources retain their validated subscription URL.
            canonical = source_url(resolved)
            kind = type(target).__name__
            label = kind if kind in {"Channel", "Performer", "Playlist", "Collection"} else "Collection" if route.kind == ContentKind.COLLECTION else "Creator"
            return route, canonical, label
        finally:
            if hasattr(target, "aclose"):
                await target.aclose()


async def scan_subscription(source, premium):
    async with session(source["provider"]) as client:
        route, target = await resolve(client, source["url"], source.get("mode"))
        stream = discover(target, route, progress=source.get("_progress"))
        count = 0
        async with aclosing(stream):
            async for _, video in stream:
                yield listing_item(route, video)
                count += 1
                if not premium and count >= 5:
                    return
