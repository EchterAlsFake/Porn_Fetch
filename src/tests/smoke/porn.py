"""Opt-in real Porn.com Video/Collection/Channel/Pornstar app integration.

Run: python -m src.tests.smoke.porn --gui --report /tmp/porn-fetch-integration.json
No network or media transfers are started by importing this module.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import tempfile
from contextlib import aclosing
from datetime import datetime, timezone
from html.parser import HTMLParser
from importlib.metadata import version
from pathlib import Path
from urllib.parse import urljoin

from base_api import update_url_query
from base_api.modules.config import RuntimeConfig
from base_api.modules.errors import HTTPStatusError

from src.cli.downloads import DownloadController, download_video
from src.cli.media import prepare_video
from src.cli.providers import ClientPool
from src.cli.settings import CliSettings
from src.shared.access import public_collection_items
from src.shared.media import VideoFilters
from src.shared.provider_routing import ContentKind, route_url
from src.tests.smoke.bellesa import probe


class LiveGrid(HTMLParser):
    """Independent enumeration of actual native scene links and all card IDs."""

    def __init__(self, text):
        super().__init__()
        self.depth = 0
        self.region = None
        self.card = None
        self.ids = []
        self.native = []
        self.next = None
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        classes = set(attrs.get("class", "").split())
        if tag == "div":
            self.depth += 1
            if "list-videos" in classes:
                self.region = self.depth
            elif self.region and self.depth == self.region + 1:
                self.card = attrs.get("data-itemid")
                if self.card:
                    self.ids.append(self.card)
        if tag == "a":
            href = attrs.get("href", "")
            if self.card and href.startswith("/scene/") and self.card not in self.native:
                self.native.append(self.card)
            if {"pagination__number", "next"} <= classes and href.startswith("https://"):
                self.next = href

    def handle_endtag(self, tag):
        if tag == "div":
            if self.depth == self.region:
                self.region = None
            if self.region and self.depth == self.region + 1:
                self.card = None
            self.depth -= 1


async def observed(core, url, *, all_pages=False):
    result, pages, seen = [], [], set()
    while url:
        assert url not in seen
        seen.add(url)
        try:
            text = await core.fetch_text(url)
        except HTTPStatusError as error:
            if pages and error.status_code == 404:
                break
            raise
        page = LiveGrid(text)
        if not page.ids:
            break
        result.extend(page.native)
        pages.append({"cards": len(page.ids), "native": len(page.native)})
        if not all_pages:
            break
        url = urljoin(text.url, page.next) if page.next else update_url_query(text.url, pg=len(pages) + 1)
    return result, pages


async def collect(stream):
    async with aclosing(stream):
        return [item async for item in stream]


async def run(args, workspace):
    from porn_api import Channel, Collection, Pornstar, Video
    from porn_api.modules.consts import HOSTS
    from porn_api.modules.errors import VideoUnavailable

    report = {"package": version("unofficial-api-for-porn"),
              "started_at_utc": datetime.now(timezone.utc).isoformat(),
              "hosts": [], "collections": [], "downloads": [], "gui": []}

    def save():
        args.report.write_text(json.dumps(report, indent=2) + "\n")

    runtime = RuntimeConfig()
    runtime.timeout = 25
    runtime.request_attempts = 2
    runtime.pages_concurrency = 1
    runtime.videos_concurrency = 2
    runtime.max_workers_download = 3
    settings = CliSettings(skip_existing=False, write_metadata=True, download_workers=3)
    async with ClientPool(runtime) as pool:
        for host in sorted(HOSTS):
            route, source = await pool.resolve(f"https://{host}/scene/208974141")
            assert route.provider == "porn" and isinstance(source, Video)
            media = await prepare_video(source, "porn")
            assert media.video_id == "208974141" and media.length == 6
            assert media.author == ", ".join(source.pornstars_names)
            assert media.qualities == [360, 480, 1080]
            assert media.tags and media.thumbnail_url and media.publish_date is None
            report["hosts"].append({"host": host, "language": source.language, "qualities": media.qualities})
            save()
        for slug, expected, kind, all_pages in (
            ("yoga-porn", Collection, ContentKind.COLLECTION, False),
            ("brazzers", Channel, ContentKind.PROFILE, True),
            ("mia-khalifa", Pornstar, ContentKind.PROFILE, True),
        ):
            url = f"https://www.porn.com/{slug}"
            route, target = await pool.resolve(url)
            assert type(target) is expected and route.kind == kind
            expected_ids, pages = await observed(target.core, url, all_pages=all_pages)
            actual = await collect(pool.media_stream(url, pages=30 if all_pages else 1))
            assert expected_ids and [v.video_id for v in actual] == expected_ids
            preview = await collect(public_collection_items(pool.media_stream(url, pages=30 if all_pages else 1), False))
            assert [v.video_id for v in preview] == expected_ids[:5]
            for source in preview:
                assert source.is_playable
                await prepare_video(source, "porn")
            report["collections"].append({"url": url, "class": expected.__name__, "pages": pages,
                                           "expected_native": len(expected_ids), "actual_native": len(actual),
                                           "free_preview": len(preview)})
            print("COLLECTION", slug, len(expected_ids), len(actual), flush=True)
            save()
        for url in ("https://www.porn.com/search?sq=test", "https://www.porn.com/categories",
                    "https://www.porn.com/sites", "https://www.porn.com/pornstars",
                    "https://www.porn.com/out/example", "https://www.porn.com/gay"):
            try:
                route_url(url)
            except ValueError:
                continue
            raise AssertionError(f"Unsupported feature route accepted: {url}")
        try:
            await pool.resolve("https://www.porn.com/xnxx")
        except ValueError:
            pass
        else:
            raise AssertionError("The excluded Source type was exposed")
        _, referral = await pool.resolve("https://www.porn.com/scene/186254188")
        try:
            await prepare_video(referral, "porn")
        except VideoUnavailable:
            pass
        else:
            raise AssertionError("An external referral became a downloadable row")
        _, source = await pool.resolve("https://www.porn.com/scene/208974141")
        media = await prepare_video(source, "porn")
        if not args.metadata_only:
            for request, premium, height in (("best", False, 480), ("best", True, 1080)):
                path = workspace / f"{height}.mp4"
                controller = DownloadController(url=source.url, target=path, provider="porn", state_directory=workspace / "state")
                outcome = await download_video(source, path, request, settings, has_premium=premium,
                                               available_qualities=None, metadata=media, controller=controller)
                assert outcome.status == "completed" and not outcome.missing_segments
                info = await asyncio.to_thread(probe, path)
                assert info["height"] == height and info["audio"] and abs(info["duration"] - source.duration) < 2
                assert info["tags"].get("title") == media.title and info["tags"].get("artist") == media.author
                report["downloads"].append({"premium": premium, **info})
                save()
    assert not pool.clients and not pool.cores
    if args.gui:
        from PySide6.QtGui import QGuiApplication

        from src.backend import clients
        from src.backend.application import stop_flag
        from src.backend.profile_diagnostics import diagnostic_settings, make_test_backend, test_profile_url

        app = QGuiApplication.instance() or QGuiApplication([])
        app.setQuitOnLastWindowClosed(False)
        try:
            gui_source = await clients.get_video("https://www.porn.com/scene/208974141")
            row = await clients.load_video_attributes(gui_source)
            assert row.length == 6 and row.qualities == [360, 480, 1080]
            assert row.author == media.author and row.publish_date is None
            for slug, factory in (("brazzers", "get_channel"), ("mia-khalifa", "get_pornstar")):
                stop_flag.clear()
                backend = make_test_backend()
                case = {"provider": "porn", "url": f"https://www.porn.com/{slug}", "expected_factory": factory}
                evidence = await test_profile_url(backend, backend._downloads_model, case, items=1)
                assert evidence["rows"] == 1
                report["gui"].append({"url": case["url"], **evidence})
                save()
            stop_flag.clear()
            backend = make_test_backend()
            with diagnostic_settings(items=2):
                await backend._process_playlist_url("https://www.porn.com/yoga-porn", "$index-$title", VideoFilters())
            assert backend._downloads_model.rowCount() == 2
            report["gui"].append({"url": "https://www.porn.com/yoga-porn", "profile": "Collection", "rows": 2})
            save()
        finally:
            stop_flag.clear()
            await clients.close_all_clients()
    report["passed"] = True
    report["metadata_only"] = args.metadata_only
    save()
    print("PASS Porn.com integration:", args.report, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=Path('/tmp/porn-fetch-integration.json'))
    parser.add_argument("--metadata-only", action="store_true")
    parser.add_argument("--gui", action="store_true")
    args = parser.parse_args()
    args.report = args.report.resolve()
    args.report.parent.mkdir(parents=True, exist_ok=True)
    logging.disable(logging.CRITICAL)
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ.setdefault("QT_QUICK_BACKEND", "software")
    with tempfile.TemporaryDirectory(prefix="porn-fetch-integration-") as directory:
        for kind in ("CONFIG", "CACHE", "DATA"):
            os.environ[f"XDG_{kind}_HOME"] = str(Path(directory) / kind.lower())
        asyncio.run(run(args, Path(directory)))


if __name__ == "__main__":
    main()
