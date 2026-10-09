"""Offline regressions for provider integration fixes and documented API contracts."""
from __future__ import annotations

import inspect
import io
import tempfile
import unittest
from contextlib import redirect_stderr
from importlib import import_module
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

from src.cli.batch import build_parser
from src.cli.downloads import download_gallery
from src.cli.media import available_qualities, prepare_video
from src.cli.providers import ClientPool
from src.shared import provider_routing
from src.shared.media import xfreehd_quality
from src.shared.provider_accounts import connect_pornhub_cookies
from src.shared.provider_routing import (
    PROVIDER_MODULES,
    ContentKind,
    container_stream,
    resolve_container,
    resolve_video,
    route_url,
)


async def items(*values):
    for value in values:
        yield value


class RoutingTests(unittest.IsolatedAsyncioTestCase):
    async def test_correct_profile_handler(self):
        cases = {
            "https://pornhub.com/model/example": "get_model",
            "https://pornhub.com/users/example": "get_user",
            "https://eporner.com/channel/example": "get_channel",
            "https://eporner.com/profile/example": "get_channel",
            "https://xhamster.com/users/example": "get_creator",
            "https://xhamster.com/creator/example": "get_creator",
            "https://spankbang.com/profile/example": "get_creator",
            "https://porntrex.com/channels/example": "get_channel",
            "https://xvideos.com/example": "get_channel",
            "https://redtube.com/amateur/example": "get_amateur",
            "https://thumbzilla.com/channel/example": "get_channel",
            "https://tube8.com/user/example": "get_user",
        }
        for url, method in cases.items():
            with self.subTest(url=url):
                route = route_url(url)
                self.assertEqual(route.kind, ContentKind.PROFILE)
                client = SimpleNamespace(**{method: AsyncMock(return_value="profile")})
                self.assertEqual(await resolve_container(client, route), "profile")
                getattr(client, method).assert_awaited_once_with(url, load_html=True)
                api_method = getattr(import_module(PROVIDER_MODULES[route.provider]).Client, method)
                inspect.signature(api_method).bind(client, url, load_html=True)

    async def test_xvideos_playlist_is_consumed_without_awaiting_generator(self):
        client = SimpleNamespace(get_playlist=Mock(side_effect=lambda url, pages: items("one", "two")))
        route = route_url("https://xvideos.com/playlist/123/example")
        stream = await resolve_container(client, route, pages=7)
        self.assertEqual([item async for item in container_stream(stream, pages=7, provider="xvideos")],
                         ["one", "two"])
        client.get_playlist.assert_called_once_with(route.url, pages=7)

    async def test_short_aliases_use_short_api(self):
        for url in ("https://pornhub.com/shorties/example", "https://xhamster.com/shorts/example"):
            client = SimpleNamespace(get_short=AsyncMock(return_value="short"))
            self.assertEqual(await resolve_video(client, route_url(url)), "short")
            client.get_short.assert_awaited_once_with(url, load_html=True)

    async def test_pornhub_uploads_featured_modes(self):
        profile = SimpleNamespace(get_uploads=lambda pages: items("uploaded"),
                                  get_videos=lambda pages: items("featured"))
        for mode, expected in (("uploads", ["uploaded"]), ("videos", ["featured"]),
                               ("both", ["featured", "uploaded"])):
            stream = container_stream(profile, pages=5, provider="pornhub", profile_mode=mode)
            self.assertEqual([item async for item in stream], expected)

    def test_url_titles_do_not_change_content_kind_or_provider(self):
        self.assertEqual(route_url("https://xvideos.com/video123/profile").kind, ContentKind.VIDEO)
        self.assertEqual(route_url("https://beeg.com/playlist123").kind, ContentKind.VIDEO)
        with self.assertRaises(ValueError):
            route_url("https://example.com/?url=https://pornhub.com/model/example")


class SearchRestrictionTests(unittest.TestCase):
    def test_application_adapters_do_not_expose_upstream_search(self):
        self.assertFalse(hasattr(ClientPool, "search"))
        self.assertFalse(hasattr(provider_routing, "search_stream"))
        self.assertFalse(hasattr(provider_routing, "SEARCH_METHODS"))
        self.assertNotIn("search", {kind.value for kind in ContentKind})

    def test_batch_rejects_search_flags(self):
        parser = build_parser()
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            parser.parse_args(["--search", "example", "--provider", "eporner"])
        self.assertEqual(error.exception.code, 2)
        self.assertNotIn("--search", parser.format_help())
        self.assertNotIn("--provider", parser.format_help())


class MediaTests(unittest.IsolatedAsyncioTestCase):
    async def test_raw_youporn_is_not_parsed_as_hls(self):
        core = SimpleNamespace(list_available_qualities=AsyncMock())
        video = SimpleNamespace(is_hls=False, m3u8_base_url="https://media.test/video.mp4", core=core)
        self.assertEqual(await available_qualities(video), [])
        core.list_available_qualities.assert_not_awaited()

    async def test_dates_tags_and_short_duration_are_preserved(self):
        video = SimpleNamespace(loader_methods={}, title="Example", url="https://example.test/video",
                                duration=24, action_tags=["example"], created_timestamp=1700000000)
        media = await prepare_video(video, "redtube")
        self.assertEqual(media.tags, ["example"])
        self.assertEqual(media.length, 1)
        self.assertEqual(media.publish_date.year, 2023)

    def test_xfreehd_quality_names(self):
        self.assertEqual(xfreehd_quality("720"), "hd")
        self.assertEqual(xfreehd_quality(480), "sd")
        self.assertEqual(xfreehd_quality("worst"), "sd")

    async def test_pornhub_gallery_uses_all_album_pages(self):
        calls = []
        async def photos(pages):
            calls.append(pages)
            for index in range(pages):
                yield {"download_url": f"https://images.test/{index}.jpg"}
        album = SimpleNamespace(loader_methods={}, title="Example album", total_pages=2,
                                get_photos=photos, core=SimpleNamespace(fetch_bytes=AsyncMock(return_value=b"image")))
        with tempfile.TemporaryDirectory() as directory:
            outcome = await download_gallery(album, directory)
            self.assertEqual(outcome.status, "completed")
            self.assertEqual(calls, [2])
            self.assertEqual(len(list(Path(outcome.path).glob("*.jpg"))), 2)

    async def test_pornhub_browser_login_initializes_account_username(self):
        client = SimpleNamespace(core=SimpleNamespace(session=SimpleNamespace(cookies={})),
                                 account=SimpleNamespace(name=None), logged=False,
                                 get_user=AsyncMock(return_value="user"))
        self.assertTrue(await connect_pornhub_cookies(client, {"session": "cookie"}, "example"))
        self.assertEqual(client.account.name, "example")
        self.assertEqual(client.account.user, "user")
        self.assertTrue(client.logged)
        with self.assertRaises(ValueError):
            await connect_pornhub_cookies(client, {"session": "cookie"}, "")


if __name__ == "__main__":
    unittest.main()
