import sys, pathlib, asyncio, json, logging, importlib
from urllib.parse import urljoin, urlsplit
from contextlib import aclosing
from .common import *
from base_api import BaseCore, IteratorConfig, ResultOrder, ErrorMode
from base_api.modules.config import RuntimeConfig
from selectolax.lexbor import LexborHTMLParser

logging.disable(logging.CRITICAL)
ic = IteratorConfig(order=ResultOrder.ORIGINAL, page_error_mode=ErrorMode.RAISE, item_error_mode=ErrorMode.RAISE)
cases = [
    ("eporner", "Pornstar", "https://www.eporner.com/pornstar/riley-reid/"),
    ("porndoe", "Pornstar", "https://porndoe.com/pornstars-profile/eva-elfie"),
    ("pornhat", "Model", "https://www.pornhat.com/models/armani-black/"),
    ("empflix", "Profile", "https://www.empflix.com/profile/dani-daniels"),
    ("youjizz", "Pornstar", "https://www.youjizz.com/search/Abby-Marie-1.html"),
]


class ObserveCore(BaseCore):
    async def fetch_text(self, url, **kwargs):
        text = await super().fetch_text(url, **kwargs)
        if getattr(self, "record", False):
            self.received.append(text)
        return text


async def main():
    out = []
    for site, cls, url in cases:
        cfg = RuntimeConfig()
        cfg.request_attempts = 3
        try:
            async with ObserveCore(configuration=cfg) as core:
                expected = []
                counts = []
                current = url
                visited = set()
                while current:
                    assert current not in visited, "independent navigation loop"
                    visited.add(current)
                    content = await core.fetch_text(current)
                    tree = LexborHTMLParser(content)
                    selector = {
                        "eporner": "#vidresults div.mb p.mbtit a[href]",
                        "porndoe": ".video-item .video-item-link[href]",
                        "pornhat": '#custom_list_videos_common_videos_list_items .thumb-video > a[href*="/video/"]',
                        "empflix": "div[data-vid] a.video-thumb[href], div[data-vid] a.thumb[href]",
                        "youjizz": "a.frame[data-video-id]:not(.related-thumb)",
                    }[site]
                    rows = list(
                        dict.fromkeys(
                            urljoin(content.url, n.attributes["href"]).rstrip("/") for n in tree.css(selector)
                        )
                    )
                    expected.extend(rows)
                    counts.append(len(rows))
                    if site == "porndoe":
                        node = tree.css_first(".pager-next[href]")
                    elif site == "youjizz":
                        node = tree.css_first("a.pagination-next[href]")
                    else:
                        candidates = [a for a in tree.css("a[href]") if a.text(strip=True).casefold() == "next"]
                        node = candidates[0] if candidates else None
                    current = urljoin(content.url, node.attributes["href"]) if node and rows else None
                module = importlib.import_module(site + "_api.api")
                obj = getattr(module, cls)(core=core, url=url, **({"name": "Abby Marie"} if site == "youjizz" else {}))
                core.received = []
                core.record = True
                stream = obj.videos(pages="all", iterator_config=ic)
                async with aclosing(stream):
                    actual = [r.unwrap().url.rstrip("/") async for r in stream]
                core.record = False
                assert expected, "independent listing unexpectedly empty"
                changed_order = False
                if expected != actual and len(expected) == len(actual) and set(expected) == set(actual):
                    received = []
                    for text in core.received:
                        tree = LexborHTMLParser(text)
                        received.extend(
                            list(
                                dict.fromkeys(
                                    urljoin(text.url, n.attributes["href"]).rstrip("/") for n in tree.css(selector)
                                )
                            )
                        )
                    assert received == actual, "API order differs from the live responses it actually consumed"
                    changed_order = True
                    expected = received
                assert actual == expected, (
                    f"ID/order mismatch expected={len(expected)} actual={len(actual)} missing={len(set(expected) - set(actual))} unexpected={len(set(actual) - set(expected))}"
                )
                # Verify the advertised beyond-final start and tail count using real requests.
                tail = obj.videos(pages="all", start_page=len(counts), iterator_config=ic)
                async with aclosing(tail):
                    last = [r.unwrap().url.rstrip("/") async for r in tail]
                final_rows = expected[-counts[-1] :] if counts[-1] else []
                assert last == final_rows, "final-page offset mismatch"
                beyond = obj.videos(pages="all", start_page=len(counts) + 1, iterator_config=ic)
                async with aclosing(beyond):
                    extra = [r.unwrap().url async for r in beyond]
                assert not extra, "beyond-final returned entries"
                row = {
                    "provider": site,
                    "kind": cls,
                    "status": "PASS",
                    "independent_pages": counts,
                    "expected": len(expected),
                    "actual": len(actual),
                    "ordered_match": True,
                    "final_and_beyond": True,
                    "separate_observation_order_changed": changed_order,
                }
        except Exception as e:
            row = {"provider": site, "kind": cls, "status": "FAIL", "error": type(e).__name__ + ": " + str(e)}
        out.append(row)
        print(json.dumps(row), flush=True)
    (OUTPUT / "full.json").write_text(json.dumps(out, indent=2))
    if any(row["status"] != "PASS" for row in out):
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
