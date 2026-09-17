from __future__ import annotations

import asyncio
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from src.backend.media import quality_requires_premium, select_allowed_quality
from src.cli.downloads import download_gallery, download_video, progress_percentage
from src.cli.model_store import ModelStore
from src.cli.providers import ClientPool, ContentKind, route_url, unwrap_scrape_result
from src.cli.settings import CliSettings, SettingsStore


class ProviderRoutingTests(unittest.TestCase):
    def test_capability_matrix_routes(self):
        cases = {
            "https://pornhub.com/short/1": ("pornhub", ContentKind.VIDEO),
            "https://pornhub.com/model/name": ("pornhub", ContentKind.PROFILE),
            "https://pornhub.com/playlist/12": ("pornhub", ContentKind.COLLECTION),
            "https://eporner.com/pornstar/name/": ("eporner", ContentKind.PROFILE),
            "https://xnxx.com/profile/name": ("xnxx", ContentKind.PROFILE),
            "https://xvideos.com/pornstars/name": ("xvideos", ContentKind.PROFILE),
            "https://xvideos.com/playlist/12/name": ("xvideos", ContentKind.COLLECTION),
            "https://xhamster.com/creators/name": ("xhamster", ContentKind.PROFILE),
            "https://spankbang.com/pornstar/name": ("spankbang", ContentKind.PROFILE),
            "https://youporn.com/collections/12/name": ("youporn", ContentKind.COLLECTION),
            "https://porntrex.com/model/name/": ("porntrex", ContentKind.PROFILE),
            "https://xfreehd.com/album/12/name": ("xfreehd", ContentKind.GALLERY),
            "https://redtube.com/playlist?playlist_id=1": ("redtube", ContentKind.COLLECTION),
            "https://thumbzilla.com/playlist/1": ("thumbzilla", ContentKind.COLLECTION),
            "https://tube8.com/pornstar/name/": ("tube8", ContentKind.PROFILE),
            "https://beeg.com/-123": ("beeg", ContentKind.VIDEO),
        }
        for url, expected in cases.items():
            route = route_url(url)
            self.assertEqual((route.provider, route.kind), expected)

    def test_quality_gate(self):
        self.assertTrue(quality_requires_premium("best"))
        self.assertTrue(quality_requires_premium(1080))
        self.assertFalse(quality_requires_premium(720))
        self.assertEqual(select_allowed_quality("best", [360, 720, 1080], False), "720")


class _Core:
    def __init__(self, configuration):
        self.configuration = configuration
        self.closed = False

    async def close(self):
        self.closed = True


class ClientPoolTests(unittest.IsolatedAsyncioTestCase):
    async def test_pool_cleanup_and_result_unwrap(self):
        class Client:
            def __init__(self, core):
                self.core = core

        pool = ClientPool(object(), client_factories={"pornhub": Client}, core_factory=_Core)
        client = pool.client("pornhub")
        await pool.close()
        self.assertTrue(client.core.closed)

        marker = object()
        success = type("Result", (), {"succeeded": True, "unwrap": lambda self: marker})()
        self.assertIs(unwrap_scrape_result(success), marker)
        failure = type("Result", (), {"succeeded": False, "error": ValueError("no")})()
        with self.assertRaises(ValueError):
            unwrap_scrape_result(failure)


class PersistenceTests(unittest.TestCase):
    def test_settings_migration_and_atomic_save(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            legacy = root / "config.ini"
            legacy.write_text("[Video]\nquality=6\noutput_path=/tmp/out\nresult_limit=7\n[Performance]\ntimeout=25\nspeed_limit=0\n", encoding="utf-8")
            store = SettingsStore(root / "settings.json")
            settings = store.load([legacy])
            self.assertEqual(settings.quality, "720")
            self.assertEqual(settings.result_limit, 7)
            self.assertEqual(settings.timeout, 25)
            store.save(settings.overridden(quality="720"))
            self.assertEqual(store.load().quality, "720")
            self.assertTrue(legacy.exists())

    def test_runtime_config_translation(self):
        settings = CliSettings(
            response_cache_mb=3, segment_cache_mb=4, bandwidth_limit_mb=0,
            proxy="", custom_ja3="", ip_preference="ipv6", locale="de-DE",
        )
        runtime = settings.to_runtime_config()
        self.assertEqual(runtime.response_cache_size_bytes, 3 * 1024 * 1024)
        self.assertEqual(runtime.segment_cache_size_bytes, 4 * 1024 * 1024)
        self.assertIsNone(runtime.max_bandwidth_mb)
        self.assertIsNone(runtime.proxy)
        self.assertEqual(runtime.ip_resolve, 2)
        self.assertIn("de-DE", runtime.locale)
        self.assertEqual(runtime.cookies["lang"], "de")

    def test_model_store_only_marks_successes(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ModelStore(Path(directory) / "models.json", legacy_paths=[])
            store.add("https://example.test/model")
            self.assertEqual(store.update_pending("https://example.test/model", ["v2", "v1", "v2"]), 2)
            store.mark_downloaded("https://example.test/model", "v1")
            downloaded, pending = store.counts("https://example.test/model")
            self.assertEqual((downloaded, pending), (1, 1))


class DownloadTests(unittest.IsolatedAsyncioTestCase):
    async def test_progress_skip_and_raw_hls_dispatch(self):
        self.assertIsNone(progress_percentage(1, 0))
        self.assertEqual(progress_percentage(11, 10), 100)
        with tempfile.TemporaryDirectory() as directory:
            settings = CliSettings(output_path=directory, skip_existing=True, write_metadata=False)
            existing = Path(directory) / "done.mp4"
            existing.write_bytes(b"x")
            skipped = await download_video(object(), existing, "720", settings, has_premium=False)
            self.assertTrue(skipped.skipped)

            raw_type = type("RawVideo", (), {"__module__": "eporner_api.api"})
            raw = raw_type()
            raw_progress = []
            async def raw_download(configuration, mode=None):
                raw.configuration = configuration
                raw.mode = mode
                configuration.callback(1024, 2048)
                return True
            raw.download = raw_download
            result = await download_video(
                raw, Path(directory) / "raw.mp4", "best", settings,
                has_premium=False, available_qualities=[720, 1080],
                progress=lambda completed, total, unit: raw_progress.append((completed, total, unit)),
            )
            await asyncio.sleep(0)
            self.assertEqual(result.status, "completed")
            self.assertEqual(str(raw.configuration.quality), "720")
            self.assertEqual(raw.mode, "h264")
            self.assertIn((1024, 2048, "bytes"), raw_progress)

            hls_type = type("HlsVideo", (), {"__module__": "pornhub_api.api"})
            hls = hls_type()
            hls_progress = []
            async def hls_download(configuration):
                hls.configuration = configuration
                configuration.callback(4, 10)
                return type("Report", (), {"status": "missing", "missing": [2, 3]})()
            hls.download = hls_download
            with patch("src.cli.downloads.data_dir", return_value=Path(directory) / "state"):
                result = await download_video(
                    hls, Path(directory) / "hls.mp4", 720, settings,
                    has_premium=False, available_qualities=[720],
                    progress=lambda completed, total, unit: hls_progress.append((completed, total, unit)),
                )
            await asyncio.sleep(0)
            self.assertEqual(result.status, "failed")
            self.assertEqual(result.missing_segments, (2, 3))
            self.assertIn((4, 10, "segments"), hls_progress)

    async def test_gallery_names_and_progress(self):
        class Core:
            async def fetch_bytes(self, url):
                return url.encode()
        class Album:
            title = "An / Album"
            loader_methods = {}
            core = Core()
            async def get_all_images(self):
                return ["https://img.test/a.png", "https://img.test/no-extension"]
        progress = []
        with tempfile.TemporaryDirectory() as directory:
            result = await download_gallery(Album(), directory, progress=progress.append)
            self.assertEqual(result.status, "completed")
            self.assertTrue((result.path / "0001.png").exists())
            self.assertTrue((result.path / "0002.jpg").exists())
            self.assertEqual(progress[-1], 100)


from src.cli.media import _author, prepare_video


class MediaPreparationTests(unittest.IsolatedAsyncioTestCase):
    async def test_author_async_property_without_warning(self):
        class VideoWithAsyncAuthorProperty:
            author_information = {"name": "InfoAuthor"}

            @property
            async def author(self):
                return "SlowAuthor"

        author = await _author(VideoWithAsyncAuthorProperty(), "pornhub")
        self.assertEqual(author, "InfoAuthor")

    async def test_author_awaited_when_only_async_property(self):
        class VideoWithOnlyAsyncAuthor:
            @property
            async def author(self):
                return "OnlyAsyncAuthor"

        author = await _author(VideoWithOnlyAsyncAuthor(), "test")
        self.assertEqual(author, "OnlyAsyncAuthor")

    async def test_author_async_callable_and_getter(self):
        class AuthorObj:
            name = "ObjectAuthor"

        class VideoWithAsyncMethod:
            async def author(self):
                return AuthorObj()

        author = await _author(VideoWithAsyncMethod(), "youporn")
        self.assertEqual(author, "ObjectAuthor")

        class VideoWithGetAuthor:
            async def get_author(self):
                return AuthorObj()

        author = await _author(VideoWithGetAuthor(), "xvideos")
        self.assertEqual(author, "ObjectAuthor")


class TextualPilotTests(unittest.IsolatedAsyncioTestCase):
    async def test_navigation_submission_selection_queue_and_settings(self):
        try:
            from textual.widgets import Button, DataTable, Input
            from src.cli.app import DownloadsScreen, PornFetchApp, ResultsScreen
        except ImportError:
            self.skipTest("Textual is not installed")

        video_type = type("Video", (), {"__module__": "pornhub_api.api"})

        class FakePool:
            async def media_stream(self, url, pages=5):
                video = video_type()
                video.url = url
                video.title = "Pilot Video"
                video.author = "Pilot"
                video.duration = 120
                video.thumbnail = ""
                video.video_id = "pilot"
                video.publish_date = None
                video.tags = []
                video.video_qualities = [360, 720]
                video.loader_methods = {}

                async def download(configuration):
                    return True

                video.download = download
                yield video

            async def close(self):
                return None

        with tempfile.TemporaryDirectory() as directory, patch.dict(
            "os.environ",
            {"XDG_CONFIG_HOME": f"{directory}/config", "XDG_DATA_HOME": f"{directory}/data"},
        ):
            app = PornFetchApp()
            async with app.run_test(size=(140, 45)) as pilot:
                await pilot.pause()
                app.pool = FakePool()
                app.screen.query_one("#url-input", Input).value = "https://pornhub.com/view_video.php?viewkey=pilot"
                app.screen.query_one("#submit-url", Button).press()
                await pilot.pause()
                await pilot.pause()
                self.assertIsInstance(app.screen, ResultsScreen)
                self.assertEqual(app.screen.query_one("#results-table", DataTable).row_count, 1)
                app.screen.query_one("#toggle-result", Button).press()
                await pilot.pause()
                app.screen.query_one("#queue-selected", Button).press()
                await pilot.pause()
                await pilot.pause()
                self.assertIsInstance(app.screen, DownloadsScreen)
                self.assertEqual(app.screen.query_one("#downloads-table", DataTable).row_count, 1)
                await pilot.click("#nav-settings")
                await pilot.pause()
                app.screen.query_one("#save-settings", Button).press()
                await pilot.pause()
                self.assertIn("Saved", str(app.screen.query_one("#settings-status").render()))


if __name__ == "__main__":
    unittest.main()
