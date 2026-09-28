"""Android history keeps completed downloads across app restarts."""
import asyncio
import tempfile
import unittest
from pathlib import Path

from src.database.android_tracker import AndroidTracker
from src.shared.media import VideoObject


class AndroidTrackerTest(unittest.IsolatedAsyncioTestCase):
    async def test_completed_download_survives_restart(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            video = VideoObject(
                url="https://example.test/video", title="Example", author="Author", length=10,
                tags=[], thumbnail_url="", video_id="video-1", publish_date=None,
                qualities=[720], status="completed", identifier="job-1",
                origin_iterator_url="https://example.test/model",
                origin_iterator_name="Example model",
            )
            first = AndroidTracker(Path(directory))
            first.schedule_startup()
            await asyncio.wait_for(first.save_video(video), timeout=5)
            self.assertEqual(first.get_dashboard_stats()["successful"], 1)
            await first.close()

            reopened = AndroidTracker(Path(directory))
            await reopened.schedule_startup()
            self.assertEqual(reopened.get_dashboard_stats()["successful"], 1)
            self.assertEqual(reopened.get_available_iterators()[0]["name"], "Example model")
            await reopened.close()
