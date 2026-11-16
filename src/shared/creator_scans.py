"""Strict, listing-only traversal of the providers' unified pagination API."""
from contextlib import aclosing
from dataclasses import replace
from urllib.parse import parse_qs, urlsplit

from base_api import ErrorMode, ResultOrder, make_iterator_config
from src.shared.provider_routing import unwrap_scrape_result
from src.shared.creator_library import identity, loaded


def listing_config(config=None):
    config = config or make_iterator_config(load_specific_sources=())
    return replace(config, order=ResultOrder.ORIGINAL, load_specific_sources=(), load_specific_fields=(),
                   page_error_mode=ErrorMode.RAISE, item_error_mode=ErrorMode.RAISE,
                   page_error_handler=None, item_error_handler=None)


async def discover(target, route, *, iterator_config=None, progress=None):
    """Traverse from page one once, without loading every video's player page.

    Native PaginatedStreams expose a terminal summary. Provider async-generator
    facades use the strict all-pages contract: errors must raise/yield and ordinary
    exhaustion is successful. No finite page limit or custom skip handler is used.
    """
    config = listing_config(iterator_config)
    options = dict(pages="all", start_page=1, iterator_config=config)
    streams = []
    if hasattr(target, "__aiter__"):
        streams.append(target)  # XVideos constructs its playlist stream in the resolver.
    elif route.provider == "pornhub" and route.profile_mode in {"both", "uploads"} and hasattr(target, "get_uploads"):
        if route.profile_mode == "both":
            streams.append(target.get_videos(**options))
        streams.append(target.get_uploads(**options))
    else:
        name = "items" if route.provider == "redgifs" and hasattr(target, "collection_id") else next(
            (n for n in ("get_videos", "videos") if callable(getattr(target, n, None))), None)
        if name is None:
            raise ValueError("This source does not expose a video listing.")
        if route.provider == "youjizz" and "/profile/user/" in route.url:
            options["sort"] = parse_qs(urlsplit(route.url).query).get("order", ["recent"])[0]
        streams.append(getattr(target, name)(**options))
    seen = set()
    completed_pages = 0
    progress = progress if progress is not None else {}
    try:
        for stream in streams:
            async with aclosing(stream):
                async for result in stream:
                    page_index = getattr(result, "page_index", None)
                    if isinstance(page_index, int):
                        progress["pages"] = max(progress.get("pages", 0), completed_pages + page_index + 1)
                    video = unwrap_scrape_result(result)
                    if route.provider == "redgifs":
                        from redgifs_api import Image
                        if isinstance(video, Image):
                            continue
                    if route.provider == "porn" and urlsplit(loaded(video, "link_url", "")).path.startswith("/out/"):
                        continue
                    key = identity(route.provider, video.url, loaded(video, "video_id"))
                    if key in seen:
                        continue
                    seen.add(key)
                    yield key, video
            summary = getattr(stream, "summary", None)
            if summary is not None:
                progress["pages"] = max(progress.get("pages", 0), completed_pages + getattr(summary, "pages", 0))
            completed_pages = progress.get("pages", completed_pages)
            if summary is not None and not summary.exhausted:
                raise ValueError(f"Source traversal is {summary.status}; the listing is incomplete.")
    finally:
        for stream in streams:
            await stream.aclose()
