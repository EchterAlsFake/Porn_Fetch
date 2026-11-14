"""Porn.com adapters for the four domain types supported by Porn Fetch."""
from __future__ import annotations

from contextlib import aclosing
from typing import Any, AsyncIterator
from urllib.parse import urlsplit


async def resolve_container(client: Any, url: str, *, expected: str | None = None) -> Any:
    from porn_api import Collection
    from porn_api.api import get_html_content
    from porn_api.modules.consts import page_parser

    # Every entity uses /<slug>; its URL cannot distinguish a performer from a
    # studio or generic collection. Inspect the real page through the same core.
    page = page_parser(await get_html_content(client.core, url))
    body = page.css_first("body")
    classes = set(body.attributes.get("class", "").split()) if body else set()
    if "single-channel" in classes:
        kind = "profile"
        target = await client.get_channel(url, load_html=True)
    elif "single-pornstar" in classes:
        kind = "profile"
        target = await client.get_pornstar(url, load_html=True)
    elif "single-category" in classes:
        kind = "collection"
        # The app deliberately supports Collection itself, not the provider's
        # Category or Source discovery interfaces.
        target = Collection(url=url, core=client.core)
        await target.load_sources("html")
    else:
        raise ValueError("Enter an individual Porn.com collection, channel or pornstar URL")
    if expected is not None and kind != expected:
        raise ValueError(f"This Porn.com URL is a {kind}; use the matching input section")
    return target


async def available_qualities(video: Any) -> list[int]:
    from porn_api.modules.errors import VideoUnavailable

    await video.load_fields("is_playable", "unavailable_reason")
    if not video.is_playable:
        raise VideoUnavailable(video.unavailable_reason or "This scene is an external referral")
    return sorted({int(rendition.height) for rendition in await video.get_qualities()})


def author_name(video: Any) -> str:
    return video.author_name or ", ".join(video.pornstars_names or ()) or "N/A"


async def playable_videos(stream: AsyncIterator[Any]) -> AsyncIterator[Any]:
    """Exclude external referrals before the app applies its public preview."""
    from src.shared.provider_routing import unwrap_scrape_result

    async with aclosing(stream):
        async for result in stream:
            if hasattr(result, "succeeded") and not result.succeeded:
                yield result
                continue
            video = unwrap_scrape_result(result)
            # Outbound cards have no native player; avoid fetching every referral.
            if video.link_url and urlsplit(video.link_url).path.startswith("/out/"):
                continue
            await video.load_fields("is_playable")
            if video.is_playable:
                yield result
