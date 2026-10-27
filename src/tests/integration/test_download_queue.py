"""Offline queue lifecycle regressions, with no real provider requests or downloads."""
import asyncio
import os
import tempfile
import unittest
from pathlib import Path
from types import MethodType, SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ["PORN_FETCH_TEST_ENV"] = "1"

from src.backend.application import Backend
from src.backend.download_manager import DownloadListModel, DownloadManager
from src.shared.media import VideoObject


def video(identifier):
    return VideoObject(url="https://example.test/video", title="Example", author="Author",
                       length=2, tags=[], thumbnail_url="", video_id=identifier, publish_date=None,
                       qualities=[720], identifier=identifier, index=1, selected_quality="720", status="pending")


class QueueNumberingTests(unittest.TestCase):
    def test_numbering_and_job_lookup_follow_row_removal(self):
        model = DownloadListModel()
        for identifier in ("a", "b", "c"):
            model.add_video(video(identifier), "720")
        self.assertEqual([model.data(model.index(row, 0), model.TitleRole) for row in range(3)],
                         ["1) Example", "2) Example", "3) Example"])
        model.remove_video("b")
        self.assertEqual(model.rowCount(), 2)
        self.assertEqual(model.data(model.index(1, 0), model.TitleRole), "2) Example")
        model.set_selected("c", True)
        self.assertEqual(model.selected_job_ids(), ["c"])
        self.assertIsNone(model.get_video("b"))
        self.assertEqual(model.get_video("c").identifier, "c")


class QueueLifecycleTests(unittest.IsolatedAsyncioTestCase):
    def backend(self, item):
        model = DownloadListModel()
        manager = DownloadManager()
        model.add_video(item, "720")
        manager.add_video(item)
        backend = SimpleNamespace(_downloads_model=model, download_manager=manager,
                                  _download_semaphore=asyncio.Semaphore(1), _download_tasks={},
                                  _download_stop_events={}, logger=Mock())
        for method in ("remove_video", "stop_download", "_download_task_finished"):
            setattr(backend, method, MethodType(getattr(Backend, method), backend))
        return backend

    async def test_success_records_completion_then_clears_both_lists(self):
        with tempfile.TemporaryDirectory() as directory:
            item = video("job")
            item.output_path = Path(directory) / "output.mp4"
            item.source_video = SimpleNamespace(download=AsyncMock(return_value=SimpleNamespace(status="completed")))
            backend = self.backend(item)
            statuses = []
            backend.download_manager.video_updated.connect(lambda entry: statuses.append(entry.status))
            settings = SimpleNamespace(processing_delay=0, skip_existing_files=False, write_metadata=False)
            with (patch("src.backend.application.app_settings", settings),
                  patch("src.backend.application.TEMP_DIRECTORY_STATES", Path(directory) / "states"),
                  patch("src.backend.application.TEMP_DIRECTORY_SEGMENTS", Path(directory) / "segments")):
                await Backend._download_video(backend, "job", item, asyncio.Event(), False)
            self.assertEqual(statuses, ["completed"])
            self.assertEqual(backend._downloads_model.rowCount(), 0)
            self.assertIsNone(backend.download_manager.get_video("job"))

    async def test_stopped_download_stays_available_to_resume(self):
        item = video("job")
        backend = self.backend(item)
        stop = asyncio.Event()
        stop.set()
        await Backend._download_video(backend, "job", item, stop, False)
        self.assertEqual(backend._downloads_model.get_status("job"), "cancelled")
        self.assertIs(backend.download_manager.get_video("job"), item)

    async def test_failed_provider_report_keeps_the_row_available_to_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            item = video("job")
            item.output_path = Path(directory) / "output.mp4"
            item.source_video = SimpleNamespace(download=AsyncMock(
                return_value=SimpleNamespace(status="failed", missing=[2])))
            backend = self.backend(item)
            settings = SimpleNamespace(processing_delay=0, skip_existing_files=False,
                                       write_metadata=False, enable_logging=False, supress_errors=True)
            with (patch("src.backend.application.app_settings", settings),
                  patch("src.backend.application.TEMP_DIRECTORY_STATES", Path(directory) / "states"),
                  patch("src.backend.application.TEMP_DIRECTORY_SEGMENTS", Path(directory) / "segments"),
                  patch("src.backend.application.report_exception", AsyncMock(return_value="test"))):
                await Backend._download_video(backend, "job", item, asyncio.Event(), False)
            self.assertEqual(item.status, "failed")
            self.assertEqual(item.missing_segments, [2])
            self.assertEqual(backend._downloads_model.get_status("job"), "failed")
            self.assertIs(backend.download_manager.get_video("job"), item)

    async def test_removing_active_entry_stops_before_removing_it(self):
        item = video("job")
        backend = self.backend(item)
        stop = asyncio.Event()
        backend._download_stop_events["job"] = stop
        backend._downloads_model.set_status("job", "downloading")
        task = asyncio.create_task(stop.wait())
        backend._download_tasks["job"] = task
        task.add_done_callback(lambda done: backend._download_task_finished("job", done))
        backend.remove_video("job")
        self.assertTrue(stop.is_set())
        self.assertEqual(backend._downloads_model.get_status("job"), "stopping")
        await task
        await asyncio.sleep(0)
        self.assertEqual(backend._downloads_model.rowCount(), 0)
        self.assertIsNone(backend.download_manager.get_video("job"))
        self.assertEqual(backend._download_tasks, {})

    async def test_removing_queued_entry_does_not_wait_for_an_unrelated_active_download(self):
        for already_waiting in (False, True):
            with self.subTest(already_waiting=already_waiting):
                item = video("job")
                item.source_video = SimpleNamespace(download=AsyncMock())
                backend = self.backend(item)
                await backend._download_semaphore.acquire()
                stop = asyncio.Event()
                backend._download_stop_events["job"] = stop
                backend._downloads_model.set_status("job", "queued")
                task = asyncio.create_task(Backend._download_video(backend, "job", item, stop, False))
                backend._download_tasks["job"] = task
                task.add_done_callback(lambda done: backend._download_task_finished("job", done))
                try:
                    if already_waiting:
                        await asyncio.sleep(0)
                    backend.remove_video("job")
                    for _ in range(5):
                        await asyncio.sleep(0)
                    self.assertTrue(task.done(), "Queued cancellation waited for the semaphore")
                    self.assertEqual(backend._downloads_model.rowCount(), 0)
                    self.assertIsNone(backend.download_manager.get_video("job"))
                    self.assertEqual(backend._download_tasks, {})
                    item.source_video.download.assert_not_awaited()
                finally:
                    task.cancel()
                    await asyncio.gather(task, return_exceptions=True)


if __name__ == "__main__":
    unittest.main()
