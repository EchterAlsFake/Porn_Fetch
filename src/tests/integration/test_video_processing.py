"""Offline checks for download numbering and GUI fetch lifecycle."""
from __future__ import annotations

import asyncio
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from PySide6.QtCore import QObject

from src.backend.application import Backend, stop_flag
from src.backend.download_manager import DownloadListModel
from src.backend.video_processor import ProcessVideos
from src.shared.media import VideoFilters, VideoObject


class VideoProcessingTests(unittest.IsolatedAsyncioTestCase):
    async def test_numbering_and_filenames_start_at_one_with_result_limit(self):
        async def videos():
            for index in range(3):
                yield str(index)

        async def prepare(url):
            return object(), VideoObject(
                url=url, title="Example", author="Author", length=60, tags=[],
                thumbnail_url="", video_id=url, publish_date=None,
                qualities=[720], status="pending",
            )

        with tempfile.TemporaryDirectory() as directory:
            settings = SimpleNamespace(
                retries=1, output_path=directory, result_limit=2,
                quality=2, mappings_quality={2: "720"},
            )
            manager = Mock()
            with patch("src.backend.video_processor.app_settings", settings):
                processor = ProcessVideos(
                    videos(), "$index-$title", VideoFilters(), manager, False, asyncio.Event(),
                )
                processor.process_single_video = AsyncMock(side_effect=prepare)
                await processor.start_processing()

            prepared = [call.args[0] for call in manager.add_video.call_args_list]
            self.assertEqual([video.index for video in prepared], [1, 2])
            self.assertEqual([video.output_path for video in prepared], [
                Path(directory) / "01-Example", Path(directory) / "02-Example",
            ])
            model = DownloadListModel()
            for video in prepared:
                model.add_video(video, "720")
            self.assertEqual(model.data(model.index(0, 0), model.TitleRole), "1) Example")
            self.assertEqual(model.data(model.index(1, 0), model.TitleRole), "2) Example")

    def backend(self):
        backend = Backend.__new__(Backend)
        QObject.__init__(backend)
        backend._video_fetch_task = None
        backend._account_fetch_task = None
        backend._account_fetch_in_progress = False
        backend._spawn = lambda coroutine, **kwargs: asyncio.create_task(coroutine)
        self.addCleanup(stop_flag.clear)
        return backend

    async def test_busy_clears_after_completion_and_failure(self):
        backend = self.backend()
        changes = []
        backend.busyChanged.connect(lambda: changes.append(backend.busy))

        async def fetch(fail):
            await asyncio.sleep(0)
            if fail:
                raise ValueError("fetch failed")

        for fail in (False, True):
            task = backend._start_video_fetch(fetch(fail), name="test-fetch")
            self.assertTrue(backend.busy)
            await asyncio.gather(task, return_exceptions=True)
            self.assertFalse(backend.busy)
        self.assertEqual(changes, [True, False, True, False])

    async def test_cancel_fetch_then_start_again(self):
        backend = self.backend()
        started = asyncio.Event()

        async def fetch():
            started.set()
            await asyncio.Event().wait()

        task = backend._start_video_fetch(fetch(), name="test-fetch")
        await started.wait()
        backend.cancel_fetching()
        await asyncio.gather(task, return_exceptions=True)
        self.assertTrue(task.cancelled())
        self.assertFalse(backend.busy)

        task = backend._start_video_fetch(asyncio.sleep(0), name="next-fetch")
        self.assertFalse(stop_flag.is_set())
        await task
        self.assertFalse(backend.busy)
