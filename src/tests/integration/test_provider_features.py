"""Offline checks of GUI dispatch through the shared provider adapters."""
from __future__ import annotations

import asyncio
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from src.backend.application import Backend
from src.shared.media import VideoFilters, VideoObject


async def items(*values):
    for value in values:
        yield value


class GuiProviderTests(unittest.IsolatedAsyncioTestCase):
    def test_gui_does_not_expose_keyword_search(self):
        self.assertFalse(hasattr(Backend, "process_search"))
        self.assertFalse(hasattr(Backend, "_process_search"))
        ui = Path(__file__).resolve().parents[2] / "frontend/UI"
        for filename in ("DownloadsPage.qml", "AndroidDownloadsPage.qml"):
            source = (ui / filename).read_text(encoding="utf-8")
            self.assertNotIn("process_search", source)
            self.assertNotIn("searchProvider", source)

    def backend(self):
        return SimpleNamespace(
            process_videos=AsyncMock(), showMessage=Mock(),
            _iterator_display_name=lambda target, url, fallback: fallback,
        )

    async def test_gui_pornhub_uploaded_mode_and_user_profiles(self):
        backend = self.backend()
        profile = SimpleNamespace(get_uploads=lambda pages: items("uploaded"),
                                  get_videos=lambda pages: items("featured"))
        client = SimpleNamespace(get_model=AsyncMock(return_value=profile),
                                 get_user=AsyncMock(return_value=profile))
        settings = SimpleNamespace(model_videos=1, strict_enforcement=False)
        with patch("src.backend.application.clients.client_for", return_value=client), \
                patch("src.backend.application.app_settings", settings):
            await Backend._process_model_url(backend, "https://pornhub.com/model/example", "", VideoFilters())
            stream = backend.process_videos.call_args.kwargs["iterator"]
            self.assertEqual([item async for item in stream], ["uploaded"])
            await Backend._process_model_url(backend, "https://pornhub.com/users/example", "", VideoFilters())
            client.get_user.assert_awaited_once()

    async def test_gui_xvideos_playlists_and_redtube_profiles(self):
        backend = self.backend()
        client = SimpleNamespace(get_playlist=Mock(side_effect=lambda url, pages: items("video")),
                                 get_channel=AsyncMock(return_value=SimpleNamespace(videos=lambda pages: items("video"))))
        with patch("src.backend.application.clients.client_for", return_value=client):
            await Backend._process_playlist_url(backend, "https://xvideos.com/playlist/123", "", VideoFilters())
            stream = backend.process_videos.call_args.kwargs["iterator"]
            self.assertEqual([item async for item in stream], ["video"])
            await Backend._process_model_url(backend, "https://redtube.com/channel/example", "", VideoFilters())
            client.get_channel.assert_awaited_once()
        backend.showMessage.emit.assert_not_called()

    async def test_gui_xfreehd_hd_quality_and_metadata(self):
        class Video:
            def __init__(self):
                self.download = AsyncMock(return_value=True)
        source = Video()
        settings = SimpleNamespace(processing_delay=0, skip_existing_files=False, download_workers=1,
                                   timeout=30, retries=1, write_metadata=True)
        backend = SimpleNamespace(_download_semaphore=asyncio.Semaphore(1), _downloads_model=Mock(),
                                  download_manager=Mock(), logger=Mock())
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "video.mp4"
            output.write_bytes(b"downloaded")
            video = VideoObject(url="https://xfreehd.com/video/1", title="Example", author="Example",
                                length=1, tags=[], thumbnail_url="", video_id="1", publish_date=None,
                                qualities=[480, 720], status="pending", selected_quality="720",
                                output_path=output, source_video=source)
            with patch("src.backend.application.clients.xf_Video", Video), \
                    patch("src.backend.application.app_settings", settings), \
                    patch("src.backend.application.FORCE_DISABLE_AV", False), \
                    patch("src.backend.application.asyncio.to_thread", new_callable=AsyncMock,
                          side_effect=lambda function, *args: function(*args)), \
                    patch("src.backend.application.write_tags", return_value=True) as writer:
                await Backend._download_video(backend, "job", video, asyncio.Event(), False)
            self.assertEqual(source.download.call_args.args[0].quality, "hd")
            self.assertEqual(video.status, "completed")
            writer.assert_called_once_with(str(output), video)

    def test_unknown_youporn_mp4_is_available_only_with_entitlement(self):
        class Video:
            is_hls = False
        def spawn(coroutine, **options):
            coroutine.close()
            return Mock()
        media = SimpleNamespace(source_video=Video(), qualities=[], selected_quality=None)
        for premium in (False, True):
            backend = SimpleNamespace(
                _download_tasks={}, _download_stop_events={},
                _downloads_model=Mock(get_video=Mock(return_value=media)),
                has_premium_access=lambda: premium, logger=Mock(), showMessage=Mock(),
                tr=lambda message: message,
                _spawn=Mock(side_effect=spawn), _download_video=AsyncMock(),
            )
            with patch("src.backend.application.clients.yp_Video", Video):
                Backend.download_video(backend, "job")
            self.assertEqual(backend._spawn.call_count, int(premium))
        self.assertEqual(media.selected_quality, "best")


if __name__ == "__main__":
    unittest.main()
