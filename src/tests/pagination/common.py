"""Live requests and explicit result unwrapping; no response replay."""

import importlib
import json
import logging
import pathlib
from contextlib import aclosing

from base_api import BaseCore, ErrorMode, IteratorConfig, ResultOrder
from base_api.modules.config import RuntimeConfig

logging.disable(logging.CRITICAL)
import os

OUTPUT = pathlib.Path(os.environ.get("PAGINATION_LIVE_OUTPUT", "/tmp/pornfetch-pagination-live"))
OUTPUT.mkdir(parents=True, exist_ok=True)
cases = [
    ("eporner", "Pornstar", "https://www.eporner.com/pornstar/riley-reid/", "videos"),
    ("empflix", "Profile", "https://www.empflix.com/profile/dani-daniels", "videos"),
    ("tnaflix", "Channel", "https://www.tnaflix.com/channel/team-skeet", "videos"),
    ("pornhub", "Model", "https://www.pornhub.com/model/teddy-tarantino", "get_videos"),
    ("porntrex", "Model", "https://www.porntrex.com/models/rose/", "videos"),
    ("redtube", "Channel", "https://de.redtube.com/channels/freeuse", "get_videos"),
    ("thumbzilla", "Channel", "https://www.thumbzilla.com/channel/brazzers/", "get_videos"),
    ("tube8", "Channel", "https://www.tube8.com/channel/teamskeet/", "get_videos"),
    ("xhamster", "Creator", "https://xhamster.com/creators/comatozze", "videos"),
    ("xnxx", "User", "https://www.xnxx.com/pornstar/cory-chase", "videos"),
    ("xvideos", "Channel", "https://de.xvideos.com/teddy_tarantino", "videos"),
    ("youporn", "Channel", "https://www.youporn.com/channel/mia-khalifa/", "videos"),
    ("bellesa", "Channel", "https://www.bellesa.co/channels/zero-to-hero", "videos"),
    ("porndoe", "Pornstar", "https://porndoe.com/pornstars-profile/eva-elfie", "videos"),
    ("pornhat", "Model", "https://www.pornhat.com/models/armani-black/", "videos"),
    ("porn", "Collection", "https://www.porn.com/yoga-porn", "videos"),
    ("youjizz", "Pornstar", "https://www.youjizz.com/search/Abby-Marie-1.html", "videos"),
    ("spankbang", "Creator", "https://spankbang.com/kxrn/creator/yvonna/", "videos"),
    ("redgifs", "User", "https://www.redgifs.com/users/nickiipeach", "videos"),
]
search = {
    "eporner": "search_videos",
    "xhamster": "search_videos",
    "xnxx": "search_videos",
    "youporn": "search_videos",
    "youjizz": "search_videos",
    "pornhub": "search_videos",
}
config = IteratorConfig(
    order=ResultOrder.ORIGINAL,
    load_specific_sources=(),
    page_error_mode=ErrorMode.RAISE,
    item_error_mode=ErrorMode.RAISE,
)


class ObservedCore(BaseCore):
    async def fetch_text(self, url, **kwargs):
        content = await super().fetch_text(url, **kwargs)
        self.observed = getattr(self, "observed", []) + [(url, getattr(content, "url", None), str(content))]
        return content


async def collect(stream):
    async with aclosing(stream):
        return [str(r.unwrap().url).rstrip("/") async for r in stream]


async def run(site, cls, url, method):
    runtime = RuntimeConfig()
    runtime.request_attempts = 3
    runtime.pages_concurrency = 1
    runtime.videos_concurrency = 3
    async with ObservedCore(configuration=runtime) as core:
        module = importlib.import_module(site + "_api.api")
        obj = getattr(module, cls)(
            core=core,
            url=url,
            **(
                {"username": url.split("/users/")[1].split("/")[0], "collection_id": url.rstrip("/").rsplit("/", 1)[-1]}
                if site == "redgifs" and cls == "Collection"
                else {}
            ),
            **({"name": "Abby Marie"} if site == "youjizz" and cls == "Pornstar" else {}),
        )
        fn = getattr(obj, method)
        first = await collect(fn(pages=1, start_page=1, iterator_config=config))
        second = await collect(fn(pages=1, start_page=2, iterator_config=config))
        both = await collect(fn(pages=2, start_page=1, iterator_config=config))
        if not first:
            raise AssertionError("EMPTY_UNVERIFIED: selected listing is empty")
        if both != first + second:
            (OUTPUT / (site + "-diff.json")).write_text(
                json.dumps(
                    {"first": first, "second": second, "both": both, "requests": [(a, b) for a, b, c in core.observed]},
                    indent=2,
                )
            )
            raise AssertionError(f"page slicing mismatch {len(first)}/{len(second)}/{len(both)}")
        assert not second or first != second, "page2 repeated page1"
        return {
            "provider": site,
            "kind": cls + "." + method,
            "url": url,
            "status": "PASS",
            "counts": [len(first), len(second), len(both)],
        }


def search_source_keys(site, requested, resolved, content):
    """Independent IDs from actual responses; production extractors are not used."""
    from urllib.parse import urljoin

    from selectolax.lexbor import LexborHTMLParser

    from .complete_profiles import identity, source_rows

    base = resolved or requested
    if site in {"eporner", "bellesa", "redgifs"}:
        data = json.loads(content)
        if site == "eporner":
            urls = [row["url"] for row in data["videos"]]
        elif site == "bellesa":
            urls = ["https://www.bellesa.co/videos/" + str(row["id"]) for row in data]
        else:
            assert all(row["type"] == 1 for row in data["gifs"]), "Search returned the wrong media type"
            urls = ["https://www.redgifs.com/watch/" + row["id"].lower() for row in data["gifs"]]
    elif site in {"xvideos", "xnxx"}:
        tree = LexborHTMLParser(content)
        return [
            node.attributes["id"].removeprefix("video_")
            for node in tree.css('#content div[id^="video_"]')
            if "thumb-block-profile" not in node.attributes.get("class", "")
        ]
    elif site == "xfreehd":
        tree = LexborHTMLParser(content)
        urls = list(dict.fromkeys(urljoin(base, node.attributes["href"]) for node in tree.css("a.video-link[href]")))
    elif site == "pornhat":
        tree = LexborHTMLParser(content)
        root = tree.css_first("#custom_list_videos_videos_list_search_result_items")
        assert root is not None, "Search response omitted its intended KVS region"
        urls = [urljoin(base, node.attributes["href"]) for node in root.css('.thumb-video > a[href*="/video/"]')]
    elif site == "pornhub":
        tree = LexborHTMLParser(content)
        root = tree.css_first("#videoSearchResult")
        assert root is not None, "Search response omitted its intended listing"
        urls = list(
            dict.fromkeys(
                urljoin(base, node.attributes["href"]) for node in root.css('a[href*="view_video"][href*="viewkey="]')
            )
        )
    else:
        observed = source_rows(site, base, content)
        assert observed is not None, "Search response omitted its source listing"
        urls = observed[0]
    return [identity(site, url) for url in urls]


async def runsearch(site):
    from selectolax.lexbor import LexborHTMLParser

    from .complete_profiles import identity

    runtime = RuntimeConfig()
    runtime.request_attempts = 3
    async with ObservedCore(configuration=runtime) as core:
        module = importlib.import_module(site + "_api.api")
        client = module.Client(core=core)
        fn = getattr(client, search.get(site, "search"))
        samples = []
        tracked_urls = []
        for pages, start in [(1, 1), (1, 2), (2, 1)]:
            begin = len(getattr(core, "observed", []))
            actual_urls = await collect(fn("massage", pages=pages, start_page=start, iterator_config=config))
            responses = core.observed[begin:]
            # Each known search fixture has at least two nonempty pages.
            # Offset validation / route resolution may precede the real pages.
            assert len(responses) >= pages, "Search ended before its known source pages"
            consumed = responses[-pages:]
            expected_pages = [
                search_source_keys(site, request, resolved, content) for request, resolved, content in consumed
            ]
            assert all(expected_pages), "Known search page is unexpectedly empty"
            expected = [key for page in expected_pages for key in page]
            actual = [identity(site, url) for url in actual_urls]
            assert actual == expected, "Search differs from the exact live source responses it consumed"
            if pages == 2:
                assert expected_pages[0] != expected_pages[1], "Second source page repeated the first"
            samples.append(actual)
            if site in {"xvideos", "xnxx"}:
                tracked_urls.extend(url for url in actual_urls if url.endswith("/video"))
        if tracked_urls:
            watch = await core.fetch_text(tracked_urls[0])
            assert identity(site, watch.url) == identity(site, tracked_urls[0]), (
                "Tracked card resolved to another video"
            )
            assert LexborHTMLParser(watch).css_first("#html5video") is not None, "Tracked card route omitted its player"
        return {
            "provider": site,
            "kind": "search",
            "status": "PASS",
            "counts": [len(values) for values in samples],
            "independent_same_response_match": True,
            "volatile_ranking": samples[0] + samples[1] != samples[2],
            "tracked_watch_route_verified": bool(tracked_urls),
        }


ic = config
