"""GUI feature boundaries; no license-service lifecycle or real HTTP requests."""
import asyncio
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from PySide6.QtCore import QObject, QSettings

from src.backend.application import Backend
from src.backend.config import SettingsManager
from src.backend.video_processor import ProcessVideos
from src.shared.access import public_collection_items
from src.shared.media import VideoFilters


async def source():
    for index in range(12):
        yield index


class GuiPremiumFeatures(unittest.IsolatedAsyncioTestCase):
    async def test_live_download_fixture_uses_the_same_entitlement_in_qml_and_backend(self):
        from PySide6.QtGui import QGuiApplication

        from src.tests.smoke.download_gui import DownloadWindow

        app = QGuiApplication.instance() or QGuiApplication([])
        for premium in (False, True):
            gui = DownloadWindow(5, premium=premium)
            try:
                self.assertEqual(gui.backend.has_premium_access(), premium)
                self.assertFalse(gui.backend._license_bridge.busy)
                await gui.backend._license_bridge.close()
                self.assertEqual(gui.window.property("bridge").property("isPremium"), premium)
            finally:
                await gui.shutdown()
        app.processEvents()

    async def test_public_profiles_and_playlists_are_capped_but_account_lists_are_not(self):
        from src.shared.provider_routing import ContentKind

        for premium in (False, True):
            fetched = []

            async def process(**options):
                fetched.extend([item async for item in options["iterator"]])

            backend = SimpleNamespace(has_premium_access=lambda: premium, notifications=Mock(),
                                      tr=lambda text: text, process_videos=process, showMessage=Mock(),
                                      _iterator_display_name=lambda *args: "source", logger=Mock(),
                                      accountFetchStateChanged=Mock(), _account_fetch_in_progress=False)
            for kind, method in ((ContentKind.PROFILE, Backend._process_model_url),
                                 (ContentKind.COLLECTION, Backend._process_playlist_url)):
                fetched.clear()
                with patch("src.backend.application.route_url", return_value=SimpleNamespace(kind=kind, provider="pornhub", profile_mode=None)), \
                     patch("src.backend.application.resolve_container", AsyncMock(return_value=object())), \
                     patch("src.backend.application.container_stream", side_effect=lambda *a, **kw: source()), \
                     patch("src.backend.application.clients.client_for", return_value=object()):
                    await method(backend, "https://example.test/collection", "", VideoFilters())
                self.assertEqual(fetched, list(range(12 if premium else 5)))
            fetched.clear()
            with patch("src.backend.application.get_account_video_iterator", return_value=(source(), "Account playlist")):
                await Backend._run_fetch_account_videos(backend, "PornHub", "playlist", "account-playlist")
            self.assertEqual(fetched, list(range(12)))

    async def test_previously_loaded_public_rows_beyond_preview_cannot_start_for_free(self):
        from src.tests.integration.test_download_queue import video

        item = video("old-public-row")
        item.origin_iterator_url = "https://example.test/channel"
        item.index = 6
        backend = SimpleNamespace(_is_shutting_down=False, _download_tasks={},
                                  _downloads_model=Mock(get_video=Mock(return_value=item)),
                                  has_premium_access=lambda: False, notifications=Mock(),
                                  tr=lambda text: text, _spawn=Mock())
        Backend.download_video(backend, item.identifier)
        backend._spawn.assert_not_called()
        self.assertEqual(backend.notifications.publish.call_args.kwargs["key"], "bulk-preview")

    async def test_range_cannot_skip_past_free_preview(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = SimpleNamespace(retries=1, output_path=directory, result_limit=100,
                                       log_level=1, log_level_map={1: "INFO"}, processing_delay=0)
            with patch("src.backend.video_processor.app_settings", settings):
                manager = Mock()
                processor = ProcessVideos(public_collection_items(source(), False), "$title",
                                          VideoFilters(start_index=6), manager, False, asyncio.Event())
                processor.process_single_video = AsyncMock()
                await processor.start_processing()
                processor.process_single_video.assert_not_awaited()
                manager.add_video.assert_not_called()

    async def test_parallel_setting_and_runtime_limit_follow_entitlement(self):
        with tempfile.TemporaryDirectory() as directory:
            settings = SettingsManager(QSettings(str(Path(directory) / "settings.ini"), QSettings.IniFormat))
            backend = Backend.__new__(Backend)
            QObject.__init__(backend)
            backend._license_bridge = SimpleNamespace(isPremium=False)
            backend._download_tasks = {}
            backend.notifications = Mock()
            with patch("src.backend.application.app_settings", settings):
                settings.parallel_downloads = 4
                backend.update_parallel_downloads(4)
                self.assertEqual(settings.parallel_downloads, 1)
                self.assertEqual(backend._download_semaphore._value, 1)
                backend.set_parallel_downloads(2)
                self.assertEqual(settings.parallel_downloads, 1)
                backend._license_bridge.isPremium = True
                backend.set_parallel_downloads(3)
                backend.update_parallel_downloads(3)
                self.assertEqual(settings.parallel_downloads, 3)
                self.assertEqual(backend._download_semaphore._value, 3)
                backend._license_bridge.isPremium = False
                backend._enforce_parallel_access()
                self.assertEqual(settings.parallel_downloads, 1)
