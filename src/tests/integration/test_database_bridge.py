"""Integration checks for the Qt adapter around the database core."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from src.database.bridge import DatabaseBridge
from src.database.core import PocketBaseTracker


class DatabaseBridgeTests(unittest.IsolatedAsyncioTestCase):
    def test_database_bridge_wraps_tracker(self):
        tracker = PocketBaseTracker(enabled=False)
        bridge = DatabaseBridge(tracker=tracker)

        self.assertFalse(bridge._enabled)
        self.assertEqual(bridge.getDashboardStats()["total"], 0)
        self.assertEqual(bridge.getAvailableIterators(), [])
        self.assertEqual(bridge.getFailedVideosForIterator("https://test"), [])
        self.assertEqual(bridge._status_bucket("completed"), "successful")

    async def test_android_and_mobile_preview_do_not_start_or_save_tracking(self):
        for android, supported in ((True, True), (False, False)):
            with self.subTest(android=android, tracking_supported=supported), tempfile.TemporaryDirectory() as directory:
                data_path = Path(directory) / "history"
                with patch("src.database.bridge.IS_ANDROID", android), patch("src.database.bridge.app_settings") as settings:
                    # A persisted setting from an older installation must not re-enable tracking.
                    settings.track_videos = True
                    settings.pocketbase_data_path = str(data_path)
                    settings.legacy_database_path = str(Path(directory) / "legacy.sqlite3")
                    with patch("src.database.tracker.PocketBaseService") as service:
                        bridge = DatabaseBridge(tracking_supported=supported)
                        bridge.start()
                        bridge.on_video_updated(Mock())
                        await bridge.close()
                        service.assert_not_called()

                self.assertFalse(bridge._enabled)
                self.assertIsNone(bridge._service)
                self.assertIsNone(bridge.tracker._startup_task)
                self.assertEqual(bridge.tracker._tasks, set())
                self.assertFalse(bridge.getDashboardStats()["enabled"])
                self.assertEqual(bridge.getDashboardStats()["total"], 0)
                self.assertEqual(bridge.getAvailableIterators(), [])
                self.assertFalse(data_path.exists())

    def test_desktop_keeps_pocketbase_tracking_setting(self):
        with tempfile.TemporaryDirectory() as directory:
            for enabled in (True, False):
                with self.subTest(enabled=enabled), patch("src.database.bridge.IS_ANDROID", False):
                    with patch("src.database.bridge.app_settings") as settings:
                        settings.track_videos = enabled
                        settings.pocketbase_data_path = directory
                        settings.legacy_database_path = str(Path(directory) / "legacy.sqlite3")
                        with patch("src.database.tracker.PocketBaseService") as service:
                            bridge = DatabaseBridge()
                            self.assertEqual(bridge._enabled, enabled)
                            self.assertEqual(service.called, enabled)


if __name__ == "__main__":
    unittest.main()
