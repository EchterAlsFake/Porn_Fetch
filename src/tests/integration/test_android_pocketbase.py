"""Opt-in host checks of the exact embedded Go runtime, with disposable app data."""
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.database.android import AndroidPocketBaseService
from src.database.creators import CreatorRepository, SCANS, SUBSCRIPTIONS, VIDEOS
from src.database.tracker import PocketBaseTracker
from src.shared.creator_library import CreatorLibrary
from src.shared.download_recovery import queue_record, read_queue, write_queue
from src.shared.media import VideoObject
from src.shared.provider_routing import route_url

LIBRARY = os.environ.get("PORN_FETCH_TEST_POCKETBASE_LIBRARY")
DESTINATION = "content://com.android.externalstorage.documents/tree/primary%3AMovies"


@unittest.skipUnless(LIBRARY, "Set PORN_FETCH_TEST_POCKETBASE_LIBRARY to a host-built embedded runtime")
class AndroidPocketBaseTests(unittest.IsolatedAsyncioTestCase):
    async def test_android_tracker_migrations_pause_and_reopen_keep_destination_and_checkpoints(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            service = AndroidPocketBaseService(directory / "database", library_path=LIBRARY)
            def native_service(*args, **kwargs):
                return service
            with patch("src.database.tracker.sys.platform", "android"), patch("src.database.android.AndroidPocketBaseService", side_effect=native_service):
                tracker = PocketBaseTracker(directory / "database", enabled=False)
                repository = CreatorRepository(await tracker.open_database())
            self.assertTrue(tracker.is_running)
            self.assertFalse(tracker.enabled)
            await repository.enable_batches()
            async def scan(source, premium):
                source["_progress"]["pages"] = 2
                for i in range(1, 27):
                    yield {"identity": f"bellesa:video:{i}", "provider": "bellesa", "url": f"https://bellesa.co/videos/{i}"}
            library = CreatorLibrary(repository, scan, mobile=True)
            async def resolve(url):
                return route_url(url), url, "Channel"
            try:
                id = await library.save("", {"name": "Android fixture", "url": "https://bellesa.co/channels/fixture",
                    "folder": DESTINATION, "quality": "480"}, resolve)
                await library.scan_tasks[id]
                source = await repository.get(SUBSCRIPTIONS, id)
                self.assertEqual(source["folder"], DESTINATION)
                self.assertEqual(source["scan_pages"], 2)
                self.assertTrue(source["baseline"])
                row = (await repository.page(VIDEOS))["items"][0]
                output = directory / "download-state/fixture.mp4"
                output.parent.mkdir()
                output.write_bytes(b"retained partial bytes")
                checkpoint = Path(f"{output}.raw-state.json")
                checkpoint.write_text('{"offset":22}')
                video = VideoObject(url=row["url"], title="Fixture", author="", length=0, tags=[], thumbnail_url="",
                    video_id="0", publish_date=None, qualities=[480], status="downloading", identifier="android-job",
                    output_path=output, selected_quality="480", export_destination=DESTINATION)
                snapshot = queue_record(video, 42)
                await repository.put(VIDEOS, row["id"], {"status":"downloading", "job": "android-job", "snapshot": snapshot})
                queue = directory / "download-state/download-queue.json"
                write_queue(queue, [snapshot])
                await library.close()
                await tracker.close()
                self.assertFalse(tracker.is_running)
                # A fresh service instance uses the same native library and private DB.
                restarted = AndroidPocketBaseService(directory / "database", library_path=LIBRARY)
                try:
                    repository = CreatorRepository(await restarted.start())
                    library = CreatorLibrary(repository, scan, mobile=True)
                    await library.recover()
                    saved = await repository.get(VIDEOS, row["id"])
                    self.assertEqual(saved["status"], "paused")
                    self.assertEqual(saved["snapshot"]["export_destination"], DESTINATION)
                    self.assertEqual(saved["snapshot"]["identifier"], "android-job")
                    restored, progress = read_queue(queue)[0]
                    self.assertEqual((restored.export_destination, progress), (DESTINATION, 42))
                    self.assertEqual(restored.output_path.read_bytes(), b"retained partial bytes")
                    self.assertTrue(checkpoint.is_file())
                    self.assertEqual((await repository.page(SCANS))["items"][0]["pages"], 2)
                finally:
                    await restarted.stop()
            finally:
                await library.close()
                await tracker.close()
