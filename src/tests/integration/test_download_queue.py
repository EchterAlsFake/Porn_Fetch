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

from src.backend.application import Backend, OutputFolderError
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
                                  _download_stop_events={}, logger=Mock(), notifications=Mock())
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

    async def test_free_queue_stays_serial_even_with_an_old_larger_semaphore(self):
        for premium in (False, True):
            with self.subTest(premium=premium), tempfile.TemporaryDirectory() as directory:
                active = maximum = 0

                async def transfer(configuration):
                    nonlocal active, maximum
                    active += 1
                    maximum = max(maximum, active)
                    await asyncio.sleep(0.02)
                    active -= 1
                    return SimpleNamespace(status="completed")

                first, second = video("one"), video("two")
                backend = self.backend(first)
                backend._downloads_model.add_video(second, "720")
                backend.download_manager.add_video(second)
                backend._download_semaphore = asyncio.Semaphore(4)
                backend.has_premium_access = lambda: premium
                for item in (first, second):
                    item.output_path = Path(directory) / (item.identifier + ".mp4")
                    item.source_video = SimpleNamespace(download=AsyncMock(side_effect=transfer))
                settings = SimpleNamespace(processing_delay=0, skip_existing_files=False, write_metadata=False)
                with patch("src.backend.application.app_settings", settings), \
                     patch("src.backend.application.TEMP_DIRECTORY_STATES", Path(directory) / "states"), \
                     patch("src.backend.application.TEMP_DIRECTORY_SEGMENTS", Path(directory) / "segments"):
                    await asyncio.gather(*(Backend._download_video(backend, item.identifier, item, asyncio.Event(), False)
                                           for item in (first, second)))
                self.assertEqual(maximum, 2 if premium else 1)
                self.assertEqual(backend.notifications.download_completed.call_count, 2)

    async def test_stopped_download_stays_available_to_resume(self):
        item = video("job")
        backend = self.backend(item)
        stop = asyncio.Event()
        stop.set()
        await Backend._download_video(backend, "job", item, stop, False)
        self.assertEqual(backend._downloads_model.get_status("job"), "cancelled")
        self.assertIs(backend.download_manager.get_video("job"), item)

    async def test_output_folder_failure_keeps_row_and_original_without_completion_notice(self):
        with tempfile.TemporaryDirectory() as directory:
            item = video("job")
            item.output_path = Path(directory) / "output.mp4"
            item.output_path.write_bytes(b"completed private file")
            item.source_video = SimpleNamespace(download=AsyncMock(return_value=SimpleNamespace(status="completed")))
            backend = self.backend(item)
            backend.tr = lambda text: text
            backend._save_to_output_folder = AsyncMock(side_effect=OutputFolderError("folder denied"))
            settings = SimpleNamespace(processing_delay=0, skip_existing_files=False,
                                       write_metadata=False, enable_logging=False)
            with (patch("src.backend.application.app_settings", settings),
                  patch("src.backend.application.is_mobile", True),
                  patch("src.backend.application.report_exception", AsyncMock(return_value="output-error"))):
                await Backend._download_video(backend, "job", item, asyncio.Event(), False)
            self.assertEqual(backend._downloads_model.get_status("job"), "failed")
            self.assertTrue(item.output_path.is_file())
            backend.notifications.download_completed.assert_not_called()
            self.assertIn("output folder", backend.notifications.download_failed.call_args.args[1])

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
            self.assertIn("missing segments: [2]", backend._downloads_model.error_details("job"))

    async def test_provider_exception_details_keep_traceback_and_cause_without_reporting_consent(self):
        async def fail(_configuration):
            try:
                raise ConnectionError("provider refused the request")
            except ConnectionError as cause:
                raise RuntimeError("could not download video") from cause

        with tempfile.TemporaryDirectory() as directory:
            item = video("job")
            item.output_path = Path(directory) / "output.mp4"
            item.source_video = SimpleNamespace(download=fail)
            backend = self.backend(item)
            settings = SimpleNamespace(processing_delay=0, skip_existing_files=False,
                                       write_metadata=False, enable_logging=False, anonymous_mode=False)
            with patch("src.backend.application.app_settings", settings), \
                 patch("src.backend.application.report_exception", AsyncMock(return_value="local-error")) as report:
                await Backend._download_video(backend, "job", item, asyncio.Event(), False)
                details = Backend.download_error_details(backend, "job")
                self.assertIn("Traceback (most recent call last)", details)
                self.assertIn("ConnectionError: provider refused the request", details)
                self.assertIn("RuntimeError: could not download video", details)
                self.assertIn(item.url, details)
                self.assertFalse(report.call_args.kwargs["enabled"])
                settings.anonymous_mode = True
                backend.tr = lambda text: text
                self.assertNotIn("provider refused", Backend.download_error_details(backend, "job"))
            self.assertEqual(backend._downloads_model.get_status("job"), "failed")
            backend._downloads_model.set_error("job", "")
            self.assertEqual(backend._downloads_model.error_details("job"), "")

    async def test_clear_list_removes_every_row_and_keeps_completed_files(self):
        with tempfile.TemporaryDirectory() as directory:
            first, second = video("first"), video("second")
            first.output_path = Path(directory) / "completed.mp4"
            first.output_path.write_bytes(b"completed video")
            backend = self.backend(first)
            backend._downloads_model.add_video(second, "720")
            backend.download_manager.add_video(second)
            backend._is_shutting_down = False
            backend.busy = True
            backend.cancel_fetching = Mock()
            backend._clear_download_list = MethodType(Backend._clear_download_list, backend)
            Backend.clear_download_list(backend)
            backend.cancel_fetching.assert_called_once()
            self.assertEqual(backend._downloads_model.rowCount(), 0)
            self.assertIsNone(backend.download_manager.get_video("second"))
            self.assertEqual(first.output_path.read_bytes(), b"completed video")

    async def test_clear_active_list_waits_for_confirmation_then_stops_writers(self):
        first, pending = video("active"), video("pending")
        backend = self.backend(first)
        backend._downloads_model.add_video(pending, "720")
        backend.download_manager.add_video(pending)
        backend._is_shutting_down = False
        backend.busy = False
        backend.tr = lambda text: text
        backend._clear_download_list = MethodType(Backend._clear_download_list, backend)
        stop = asyncio.Event()
        task = asyncio.create_task(stop.wait())
        backend._download_stop_events["active"] = stop
        backend._download_tasks["active"] = task
        backend._downloads_model.set_status("active", "downloading")
        task.add_done_callback(lambda done: backend._download_task_finished("active", done))
        Backend.clear_download_list(backend)
        self.assertFalse(stop.is_set())
        self.assertEqual(backend._downloads_model.rowCount(), 2)
        self.assertEqual(backend.notifications.request_decision.call_args.args[0], "clear-download-list")
        Backend._accept_decision(backend, "clear-download-list")
        self.assertTrue(stop.is_set())
        self.assertIsNone(backend.download_manager.get_video("pending"))
        self.assertIsNotNone(backend.download_manager.get_video("active"))
        await task
        await asyncio.sleep(0)
        self.assertEqual(backend._downloads_model.rowCount(), 0)
        self.assertIsNone(backend.download_manager.get_video("active"))

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
