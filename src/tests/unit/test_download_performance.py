"""Offline regressions for bounded download work and persistence."""
import asyncio
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from src.cli.concurrency import bounded_map
from src.cli.downloads import DownloadOutcome, download_gallery
from src.cli.model_store import ModelStore
from src.cli.settings import CliSettings
from src.cli.tracker import record_cli_download


class DownloadPerformanceTests(unittest.IsolatedAsyncioTestCase):
    async def test_gallery_failure_awaits_other_workers_and_closes_source(self):
        started = asyncio.Event()
        cancelled = asyncio.Event()
        closed = asyncio.Event()

        class Album:
            title = "album"
            loader_methods = {}

            async def get_photos(self, pages):
                try:
                    for name in ["slow", "fail", *range(100)]:
                        yield {"download_url": f"https://images.test/{name}.jpg"}
                finally:
                    closed.set()

            async def fetch_bytes(self, url):
                if url.endswith('/fail.jpg'):
                    await started.wait()
                    raise OSError("simulated failure")
                started.set()
                try:
                    await asyncio.Event().wait()
                finally:
                    cancelled.set()

        album = Album()
        album.core = album
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(OSError, "simulated failure"):
                await download_gallery(album, directory, concurrency=2)
            self.assertTrue(cancelled.is_set())
            self.assertTrue(closed.is_set())
            self.assertEqual(list(Path(directory).rglob('*.jpg')), [])

    async def test_gallery_streams_with_bounded_prefetch(self):
        produced = 0
        first_fetch_at = None

        class Album:
            title = "album"
            loader_methods = {}

            async def get_photos(self, pages):
                nonlocal produced
                for index in range(40):
                    produced += 1
                    yield {"download_url": f"https://images.test/{index}.jpg"}

            async def fetch_bytes(self, url):
                nonlocal first_fetch_at
                if first_fetch_at is None:
                    first_fetch_at = produced
                await asyncio.sleep(0)
                return b'image'

        album = Album()
        album.core = album
        with tempfile.TemporaryDirectory() as directory:
            result = await download_gallery(album, directory, concurrency=2)
            self.assertLessEqual(first_fetch_at, 5)
            self.assertEqual(len(list(result.path.glob('*.jpg'))), 40)

    async def test_batch_bounds_tasks_and_preserves_order(self):
        baseline = len(asyncio.all_tasks())
        peak = baseline

        async def operation(value):
            nonlocal peak
            peak = max(peak, len(asyncio.all_tasks()))
            await asyncio.sleep(0)
            return value * 2

        self.assertEqual(await bounded_map(list(range(100)), operation, 3), list(range(0, 200, 2)))
        self.assertLessEqual(peak - baseline, 4)

    async def test_batch_cancellation_stops_handlers_that_save_pause_state(self):
        started = asyncio.Event()
        calls = []

        async def operation(value):
            calls.append(value)
            started.set()
            try:
                await asyncio.Event().wait()
            except asyncio.CancelledError:
                return False

        task = asyncio.create_task(bounded_map(list(range(100)), operation, 2))
        await started.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await asyncio.wait_for(task, timeout=1)
        self.assertLessEqual(len(calls), 2)

    async def test_gallery_tracking_prefers_actual_download_path(self):
        tracker = SimpleNamespace(save_video=AsyncMock(return_value={}))
        video = SimpleNamespace(url='https://example.test/album', title='album')
        with patch('src.cli.tracker.ensure_cli_tracker', AsyncMock(return_value=tracker)):
            await record_cli_download(
                CliSettings(track_videos=True), video,
                DownloadOutcome('completed', Path('/downloads/album')),
                target=Path('/downloads'),
            )
        self.assertEqual(tracker.save_video.call_args.args[0].output_path, Path('/downloads/album'))


class ModelBatchTests(unittest.TestCase):
    def test_batch_updates_once_preserving_order(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ModelStore(Path(directory) / 'models.json', legacy_paths=[])
            store.update_pending('model', ['a', 'b', 'c', 'd'])
            store.mark_downloaded('model', 'a')
            with patch.object(store, '_write', wraps=store._write) as write:
                store.mark_downloaded_many('model', ['c', 'b', 'c', 'a'])
                write.assert_called_once()
            self.assertEqual(store.models(), [('model', {'downloaded': ['a', 'c', 'b'], 'pending': ['d']})])
