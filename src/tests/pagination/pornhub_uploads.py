"""Opt-in live regression: python -m src.tests.pagination.pornhub_uploads."""
import asyncio
from contextlib import aclosing
from dataclasses import replace
from urllib.parse import urljoin

from base_api import BaseCore
from pornhub_api import Client
from selectolax.lexbor import LexborHTMLParser

from src.shared.creator_scans import discover, listing_config
from src.shared.provider_routing import container_stream, route_url


async def main():
    url = "https://www.pornhub.com/model/porn-force"
    async with BaseCore() as core:
        # Independently follow the actual page links and select only listing cards.
        expected, pages, visited = [], [], set()
        following = url + "/videos/upload?page=1"
        while following:
            assert following not in visited, "Source navigation looped"
            visited.add(following)
            tree = LexborHTMLParser(await core.fetch_text(following))
            listing = tree.css_first("#mostRecentVideosSection")
            assert listing is not None, "Missing source video listing"
            ids = [row.attributes["data-video-vkey"] for row in listing.css("li[data-video-vkey]")]
            assert ids, "Unexpected empty source page"
            pages.append(ids)
            expected.extend(ids)
            link = tree.css_first(".page_next:not(.disabled) a[href]")
            following = urljoin(following, link.attributes["href"]) if link else None

        assert len(pages) > 1 and len(expected) > 40
        target = await Client(core=core).get_model(url)
        options = dict(iterator_config=listing_config())
        # A stream is an async generator, closed explicitly on all paths.
        async with aclosing(target.get_uploads(pages="all", **options)) as stream:
            actual = [r.unwrap().video_id async for r in stream]
        assert actual == expected, "Upload stream differs from source pages"
        async with aclosing(target.get_uploads(pages=1, start_page=2, **options)) as stream:
            assert [r.unwrap().video_id async for r in stream] == pages[1]
        async with aclosing(target.get_uploads(pages=2, **options)) as stream:
            assert [r.unwrap().video_id async for r in stream] == pages[0] + pages[1]
        async with aclosing(target.get_uploads(pages=1, start_page=len(pages), **options)) as stream:
            assert [r.unwrap().video_id async for r in stream] == pages[-1]
        progress = {}
        async with aclosing(discover(target, replace(route_url(url), profile_mode="uploads"), progress=progress)) as stream:
            creator_ids = [v.video_id async for _, v in stream]
        assert creator_ids == list(dict.fromkeys(expected))
        assert progress["pages"] == len(pages)
        async with aclosing(container_stream(target, pages="all", provider="pornhub", profile_mode="uploads", **options)) as stream:
            assert [r.unwrap().video_id async for r in stream] == expected
        print(f"PASS: {len(actual)} videos across {len(pages)} pages; exact source order, page slicing, creator scan and shared routing.")


if __name__ == "__main__":
    asyncio.run(main())
