"""Integration checks for the Qt adapter around the database core."""

import unittest

from src.database.bridge import DatabaseBridge
from src.database.core import PocketBaseTracker


class DatabaseBridgeTests(unittest.TestCase):
    def test_database_bridge_wraps_tracker(self):
        tracker = PocketBaseTracker(enabled=False)
        bridge = DatabaseBridge(tracker=tracker)

        self.assertFalse(bridge._enabled)
        self.assertEqual(bridge.getDashboardStats()["total"], 0)
        self.assertEqual(bridge.getAvailableIterators(), [])
        self.assertEqual(bridge.getFailedVideosForIterator("https://test"), [])
        self.assertEqual(bridge._status_bucket("completed"), "successful")


if __name__ == "__main__":
    unittest.main()
