"""Explicit Brave-cookie checks; reports contain counts, never private identities."""

import asyncio
import importlib
import json
from contextlib import aclosing
from urllib.parse import urlsplit

import browser_cookie3
from base_api import BaseCore
from base_api.modules.config import RuntimeConfig
from selectolax.lexbor import LexborHTMLParser

from src.shared.provider_accounts import connect_pornhub_cookies, connect_xvideos_cookies, verify_account_session

from .common import OUTPUT, collect, config


class AccountCore(BaseCore):
    async def fetch_text(self, url, **kwargs):
        text = await super().fetch_text(url, **kwargs)
        if self.record:
            self.responses.append((url, text))
        return text


def expected_rows(provider, responses, kind):
    pages = {}
    for requested, text in responses:
        tree = LexborHTMLParser(text)
        path = urlsplit(requested).path
        if provider == "pornhub":
            if path == "/":
                continue
            if kind == "get_subscriptions":
                assert any(
                    phrase in str(text).casefold()
                    for phrase in ["not subscribed", "no subscriptions", "haven’t subscribed", "haven't subscribed"]
                ), "Subscription fixture changed; independently reconcile its user cards"
                pages[requested] = []
                continue
            root = tree.css_first("#moreData, #recommendations, .feedContent")
            if root is None:
                # Do not substitute header/recommended videos for an empty feed.
                rows = []
            else:
                rows = list(dict.fromkeys(n.attributes["href"] for n in root.css('a[href*="view_video.php?viewkey="]')))
            from urllib.parse import parse_qs

            rows = [parse_qs(urlsplit(u).query)["viewkey"][0] for u in rows]
        elif provider == "xvideos":
            rows = []
            for card in tree.css("#content .frame-block, #content .thumb-block"):
                if "thumb-block-profile" in card.attributes.get("class", ""):
                    continue
                anchor = card.css_first('a[href*="/video."]')
                if anchor:
                    rows.append(urlsplit(anchor.attributes["href"]).path.rstrip("/"))
            rows = list(dict.fromkeys(rows))
        else:
            script = tree.css_first("#initials-script")
            if not script or "window.initials=" not in script.text():
                continue
            data = json.loads(script.text().split("window.initials=", 1)[1].strip().rstrip(";"))
            values = data.get("layoutPage", {}).get("likedVideosListProps", {}).get("videoThumbProps")
            if values is None:
                values = data.get("favoritesVideoCollection")
            if values is None:
                values = data.get("singlePlaylistComponent", {}).get("playlist", {}).get("list")
            if values is None:
                continue
            rows = [urlsplit(row["pageURL"]).path.rstrip("/") for row in values if row.get("pageURL")]
            rows = list(dict.fromkeys(rows))
        pages[requested] = rows
    return [row for values in pages.values() for row in values], len(pages)


async def main():
    results = []
    for provider in ("xvideos", "xhamster", "pornhub"):
        try:
            jar = await asyncio.to_thread(browser_cookie3.brave, domain_name=provider + ".com")
            settings = RuntimeConfig()
            settings.request_attempts = 3
            async with AccountCore(configuration=settings) as core:
                core.responses = []
                core.record = False
                module = importlib.import_module(provider + "_api.api")
                client = module.Client(core=core)
                if provider == "pornhub":
                    await connect_pornhub_cookies(client, jar)
                    target = client.account
                    methods = ["get_history", "get_favorites", "get_recommended", "get_feed", "get_subscriptions"]
                elif provider == "xvideos":
                    await connect_xvideos_cookies(client, {c.name: c.value for c in jar}, browser_jar=jar)
                    target = client.account
                    methods = ["get_recommended_videos", "get_liked_videos", "get_watch_later_videos"]
                else:
                    core.session.cookies.update(jar)
                    await verify_account_session(client, provider)
                    target = module.Account(core=core)
                    methods = ["get_liked_videos"]
                    # Discover a real user-owned collection from the site's UI.
                    import re
                    from urllib.parse import urljoin

                    page = await core.fetch_text("https://xhamster.com/my/liked/videos")
                    tree = LexborHTMLParser(page)
                    private_urls = list(
                        dict.fromkeys(
                            urljoin(page.url, node.attributes["href"])
                            for node in tree.css("a[href]")
                            if re.fullmatch(
                                r"/my/(?:playlists|favorites/videos)/[^/]+/?", urlsplit(node.attributes["href"]).path
                            )
                        )
                    )
                    if not private_urls:
                        raise AssertionError("No authenticated account playlist fixture")
                    methods.append("get_account_playlist")
                for method in methods:
                    try:
                        core.responses = []
                        core.record = True
                        stream = getattr(target, method)(
                            *([private_urls[0]] if method == "get_account_playlist" else []),
                            pages="all",
                            iterator_config=config,
                        )
                        async with aclosing(stream):
                            objects = [result.unwrap() async for result in stream]
                        core.record = False
                        if provider == "pornhub":
                            from urllib.parse import parse_qs

                            actual = [parse_qs(urlsplit(obj.url).query)["viewkey"][0] for obj in objects]
                        else:
                            actual = [urlsplit(obj.url).path.rstrip("/") for obj in objects]
                        expected, pages = expected_rows(provider, core.responses, method)
                        assert actual == expected, (
                            f"Authenticated listing differs from its live source pages: expected={len(expected)} actual={len(actual)} pages={pages}"
                        )
                        if method == "get_account_playlist":
                            # The available private fixture is one source page.
                            assert await collect(
                                target.get_account_playlist(private_urls[0], pages=1, iterator_config=config)
                            )
                            assert not await collect(
                                target.get_account_playlist(
                                    private_urls[0], pages="all", start_page=2, iterator_config=config
                                )
                            ), "Private-playlist beyond-last request returned items"
                        row = {
                            "provider": provider,
                            "method": method,
                            "status": "PASS",
                            "source_pages": pages,
                            "expected": len(expected),
                            "actual": len(actual),
                            "empty_fixture": not actual,
                            "ordered_match": True,
                        }
                    except Exception as error:
                        row = {
                            "provider": provider,
                            "method": method,
                            "status": "FAIL",
                            "error_type": type(error).__name__,
                            "reason": str(error) if isinstance(error, AssertionError) else None,
                        }
                    print(json.dumps(row), flush=True)
                    results.append(row)
                    (OUTPUT / "account-complete.json").write_text(json.dumps(results, indent=2))
        except Exception as error:
            row = {"provider": provider, "status": "FAIL", "error_type": type(error).__name__}
            print(json.dumps(row), flush=True)
            results.append(row)
    (OUTPUT / "account-complete.json").write_text(json.dumps(results, indent=2))
    if any(row["status"] != "PASS" for row in results):
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
