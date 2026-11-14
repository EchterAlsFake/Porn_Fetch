"""Qt-free adapters for YouJizz Video, Collection, Pornstar and User only."""
from __future__ import annotations

import re
from typing import Any
from urllib.parse import parse_qs, unquote, urlsplit

COLLECTIONS = {
    "most-popular": "Popular", "newest-clips": "Newest", "top-rated": "Top rated",
    "top-rated-week": "Top rated this week", "top-rated-month": "Top rated this month",
    "trending": "Trending", "highdefinition": "HD",
}


def search_identity(path: str) -> str:
    match = re.fullmatch(r"/search/(.+)-[1-9][0-9]*\.html", path)
    if not match:
        raise ValueError("An individual YouJizz pornstar link is required")
    slug = re.sub(r"^(?:recent|views|rating|length)_", "", match[1])
    return unquote(slug).replace("-", " ").casefold()


async def resolve_container(client: Any, route: Any) -> Any:
    from selectolax.lexbor import LexborHTMLParser
    from youjizz_api import Collection, Pornstar
    from youjizz_api.modules.consts import document

    parsed = urlsplit(route.url)
    if parsed.path.startswith("/profile/user/"):
        return await client.get_user(route.url, load_api=True)
    if parsed.path.startswith("/search/"):
        # Directory links themselves use /search/<name>-1.html. Validate the
        # identity without exposing keyword search or the directory as a feature.
        identity = search_identity(parsed.path)
        letter = identity[:1].upper()
        if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or not letter:
            raise ValueError("An individual YouJizz pornstar link is required")
        text = await client.core.fetch_text(f"https://{parsed.netloc}/pornstars/name/{letter}")
        parser: LexborHTMLParser = document(text)
        for node in parser.css('.tags-wrapper .tags li'):
            anchor = node.css_first('a[href^="/search/"]')
            if anchor and search_identity(urlsplit(anchor.attributes['href']).path) == identity:
                count = node.css_first('.tag-count')
                return Pornstar(url=route.url, core=client.core, name=anchor.text(strip=True),
                                video_count=int(re.sub(r"\D", "", count.text())) if count else None)
        raise ValueError("This URL is not a YouJizz pornstar directory entry; keyword search is unavailable")
    section = parsed.path.strip('/').split('/')[0]
    return Collection(url=route.url, core=client.core, name=COLLECTIONS[section])


def container_stream(container: Any, *, pages: int | str, iterator_config: Any = None):
    from youjizz_api import User

    parsed = urlsplit(container.url)
    options = {"pages": pages, "iterator_config": iterator_config}
    if isinstance(container, User):
        query = parse_qs(parsed.query)
        options['start_page'] = int(query.get('page', ['1'])[0])
        options['sort'] = query.get('order', ['recent'])[0]
    else:
        page = re.search(r'(?:/|-)([1-9][0-9]*)\.html$', parsed.path)
        options['start_page'] = int(page[1]) if page else 1
    return container.videos(**options)


async def rendition_labels(video: Any) -> dict[int, int]:
    """Map measured HLS quality tiers to the site's encoding labels.

    Inspect each real master: Auto omits legacy 288p/368p variants, and a
    portrait encoding labelled 1920 can measure 1080x1920 (a 1080p tier).
    """
    from youjizz_api.modules.errors import VideoUnavailable

    await video.load_fields('hls_urls')
    labels = {}
    for label, url in (video.hls_urls or {}).items():
        qualities = await video.core.list_available_qualities(url)
        if not qualities:
            raise VideoUnavailable("A YouJizz HLS rendition has no measurable video quality")
        for quality in qualities:
            labels[int(quality)] = int(label)
    if not labels:
        raise VideoUnavailable("This YouJizz video has no public HLS renditions")
    return labels


async def available_qualities(video: Any) -> list[int]:
    return sorted(await rendition_labels(video))


async def quality_label(video: Any, quality: str | int) -> int:
    from base_api.modules.static_functions import choose_quality_from_list

    labels = await rendition_labels(video)
    return labels[choose_quality_from_list(labels, quality)]
