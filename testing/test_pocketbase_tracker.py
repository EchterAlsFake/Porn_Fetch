"""Unit tests for PocketBaseTracker, DatabaseBridge, and CLI tracking integration."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from rich.console import Console

from src.backend.database import (
    DatabaseBridge,
    PocketBaseClient,
    PocketBaseError,
    PocketBaseService,
    PocketBaseTracker,
    _format_date,
    _read_legacy_sqlite,
)
from src.backend.media import VideoObject
from src.cli.downloads import DownloadOutcome
from src.cli.settings import CliSettings
from src.cli.tracker import (
    close_cli_tracker,
    ensure_cli_tracker,
    get_cli_tracker,
    print_dashboard_stats,
    print_failed_downloads,
    print_origin_iterators,
    record_cli_download,
)


class PocketBaseStatusBucketTests(unittest.TestCase):
    def test_status_bucketing(self):
        successful_samples = [
            "completed", "Completed", "COMPLETED", "complete", "downloaded",
            "finished", "success", "successful", " SUCCESSFUL ",
        ]
        for s in successful_samples:
            self.assertEqual(
                PocketBaseTracker.status_bucket(s),
                "successful",
                f"Expected '{s}' to bucket into 'successful'",
            )

        failed_samples = [
            "failed", "Failed", "FAILED", "error", "failure",
            "Download failed with timeout", "Network failure",
        ]
        for s in failed_samples:
            self.assertEqual(
                PocketBaseTracker.status_bucket(s),
                "failed",
                f"Expected '{s}' to bucket into 'failed'",
            )

        other_samples = [
            "paused", "Paused", "cancelled", "Cancelled", "pending",
            "downloading", "", None, "in_progress",
        ]
        for s in other_samples:
            self.assertEqual(
                PocketBaseTracker.status_bucket(s),
                "other",
                f"Expected '{s}' to bucket into 'other'",
            )


class PocketBasePayloadTests(unittest.TestCase):
    def test_create_video_payload_single_file(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4") as tmp:
            tmp.write(b"x" * (2 * 1024 * 1024))  # 2 MB
            tmp.flush()

            video = VideoObject(
                url="https://example.com/video/123",
                title="Test Video 1",
                author="Alpha Creator",
                length=12,
                tags=["hd", "exclusive"],
                thumbnail_url="https://example.com/thumb.jpg",
                video_id="vid_123",
                publish_date=datetime(2026, 3, 10, 15, 30, tzinfo=timezone.utc),
                qualities=[720, 1080],
                status="completed",
                identifier="ident_123",
                output_path=Path(tmp.name),
                selected_quality="1080",
                origin_iterator_url="https://example.com/model/alpha",
                origin_iterator_name="Alpha",
                is_hls=True,
                missing_segments=[1, 2],
                is_from_account=True,
            )

            payload = PocketBaseTracker.create_video_payload(video, {"id": "orig_abc"})
            self.assertEqual(payload["url"], "https://example.com/video/123")
            self.assertEqual(payload["title"], "Test Video 1")
            self.assertEqual(payload["video_id"], "vid_123")
            self.assertEqual(payload["author"], "Alpha Creator")
            self.assertEqual(payload["length"], "12")
            self.assertEqual(payload["status"], "completed")
            self.assertEqual(payload["tags"], ["hd", "exclusive"])
            self.assertEqual(payload["qualities"], [720, 1080])
            self.assertEqual(payload["selected_quality"], "1080")
            self.assertEqual(payload["file_size_mb"], 2.0)
            self.assertEqual(payload["is_hls"], True)
            self.assertEqual(payload["missing_segments"], [1, 2])
            self.assertEqual(payload["is_from_account"], True)
            self.assertEqual(payload["origin_iterator_url"], "https://example.com/model/alpha")
            self.assertEqual(payload["origin_iterator"], "orig_abc")
            self.assertTrue("2026-03-10" in payload["publish_date"])

    def test_create_video_payload_directory(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            p = Path(tmp_dir)
            (p / "img1.jpg").write_bytes(b"x" * (1024 * 1024))
            (p / "img2.jpg").write_bytes(b"x" * (1024 * 1024))

            video = VideoObject(
                url="https://example.com/album/456",
                title="Test Gallery",
                author="Beta Creator",
                length=None,
                tags=[],
                thumbnail_url="",
                video_id="album_456",
                publish_date=None,
                qualities=[],
                status="completed",
                output_path=p,
            )
            payload = PocketBaseTracker.create_video_payload(video)
            self.assertEqual(payload["file_size_mb"], 2.0)
            self.assertEqual(payload["origin_iterator"], "")


class PocketBaseDashboardStatsTests(unittest.TestCase):
    def test_dashboard_stats_empty(self):
        tracker = PocketBaseTracker(enabled=False)
        stats = tracker.get_dashboard_stats()
        self.assertFalse(stats["enabled"])
        self.assertEqual(stats["total"], 0)
        self.assertEqual(stats["successful"], 0)
        self.assertEqual(stats["failed"], 0)
        self.assertEqual(stats["other"], 0)
        self.assertEqual(stats["successRate"], 0)
        self.assertEqual(stats["totalSizeMb"], 0.0)
        self.assertEqual(stats["sources"], [])

    def test_dashboard_stats_aggregation(self):
        tracker = PocketBaseTracker(enabled=True)
        tracker._iterators = {
            "https://origin.com/profile1": {"id": "orig_1", "name": "Model 1", "url": "https://origin.com/profile1"},
            "https://origin.com/profile2": {"id": "orig_2", "name": "Model 2", "url": "https://origin.com/profile2"},
        }
        tracker._videos = {
            "v1": {"url": "v1", "status": "completed", "file_size_mb": 100.0, "downloaded_at": "2026-09-01T10:00:00", "origin_iterator": "orig_1"},
            "v2": {"url": "v2", "status": "successful", "file_size_mb": 200.0, "downloaded_at": "2026-09-02T10:00:00", "origin_iterator": "orig_1"},
            "v3": {"url": "v3", "status": "failed", "file_size_mb": 0.0, "downloaded_at": "2026-09-03T10:00:00", "origin_iterator": "orig_1"},
            "v4": {"url": "v4", "status": "completed", "file_size_mb": 300.0, "downloaded_at": "2026-09-04T10:00:00", "origin_iterator": "orig_2"},
            "v5": {"url": "v5", "status": "paused", "file_size_mb": 50.0, "downloaded_at": "2026-09-05T10:00:00", "origin_iterator": ""},
        }

        stats = tracker.get_dashboard_stats()
        self.assertTrue(stats["enabled"])
        self.assertEqual(stats["total"], 5)
        self.assertEqual(stats["successful"], 3)
        self.assertEqual(stats["failed"], 1)
        self.assertEqual(stats["other"], 1)
        self.assertEqual(stats["successRate"], 75)
        self.assertEqual(stats["totalSizeMb"], 650.0)
        self.assertEqual(stats["lastDownloaded"], "2026-09-05T10:00:00")

        sources = {s["name"]: s for s in stats["sources"]}
        self.assertIn("Model 1", sources)
        self.assertEqual(sources["Model 1"]["total"], 3)
        self.assertEqual(sources["Model 1"]["successful"], 2)
        self.assertEqual(sources["Model 1"]["failed"], 1)

        self.assertIn("Model 2", sources)
        self.assertEqual(sources["Model 2"]["total"], 1)
        self.assertEqual(sources["Model 2"]["successful"], 1)

        self.assertIn("Direct downloads", sources)
        self.assertEqual(sources["Direct downloads"]["total"], 1)
        self.assertEqual(sources["Direct downloads"]["other"], 1)

    def test_get_failed_videos(self):
        tracker = PocketBaseTracker(enabled=True)
        tracker._videos = {
            "v1": {"title": "Vid 1", "url": "https://v1", "video_id": "1", "status": "failed", "origin_iterator_url": "https://orig1"},
            "v2": {"title": "Vid 2", "url": "https://v2", "video_id": "2", "status": "completed", "origin_iterator_url": "https://orig1"},
            "v3": {"title": "Vid 3", "url": "https://v3", "video_id": "3", "status": "failed", "origin_iterator_url": "https://orig2"},
        }
        all_failed = tracker.get_failed_videos()
        self.assertEqual(len(all_failed), 2)

        orig1_failed = tracker.get_failed_videos("https://orig1")
        self.assertEqual(len(orig1_failed), 1)
        self.assertEqual(orig1_failed[0]["video_id"], "1")


class LegacySQLiteReaderTests(unittest.TestCase):
    def test_read_legacy_sqlite(self):
        with tempfile.NamedTemporaryFile(suffix=".db") as tmp_db:
            with sqlite3.connect(tmp_db.name) as conn:
                conn.execute("CREATE TABLE originiterator (url TEXT PRIMARY KEY, name TEXT)")
                conn.execute(
                    "CREATE TABLE videorecord ("
                    "url TEXT PRIMARY KEY, title TEXT, video_id TEXT, author TEXT, "
                    "length TEXT, thumbnail_url TEXT, publish_date TEXT, status TEXT, "
                    "tags_json TEXT, qualities_json TEXT, identifier TEXT, output_path TEXT, "
                    "selected_quality TEXT, file_size_mb REAL, downloaded_at TEXT, "
                    "is_hls INTEGER, missing_segments TEXT, is_from_account INTEGER, "
                    "origin_iterator_url TEXT"
                    ")"
                )
                conn.execute("INSERT INTO originiterator VALUES ('https://origin.com', 'Source Alpha')")
                conn.execute(
                    "INSERT INTO videorecord VALUES ("
                    "'https://video.com/1', 'Title 1', 'vid1', 'Author A', '15', 'https://thumb', "
                    "'2026-01-01', 'completed', '[\"tag1\", \"tag2\"]', '[720, 1080]', 'ident1', "
                    "'/path/1.mp4', '1080', 123.4, '2026-01-01T12:00:00', 1, '[5]', 0, 'https://origin.com'"
                    ")"
                )
                conn.commit()

            origins, videos = _read_legacy_sqlite(Path(tmp_db.name))
            self.assertEqual(len(origins), 1)
            self.assertEqual(origins[0]["name"], "Source Alpha")
            self.assertEqual(origins[0]["url"], "https://origin.com")

            self.assertEqual(len(videos), 1)
            v = videos[0]
            self.assertEqual(v["title"], "Title 1")
            self.assertEqual(v["tags"], ["tag1", "tag2"])
            self.assertEqual(v["qualities"], [720, 1080])
            self.assertEqual(v["file_size_mb"], 123.4)
            self.assertEqual(v["missing_segments"], [5])
            self.assertTrue(v["is_hls"])


class PocketBaseServiceTests(unittest.TestCase):
    def test_find_binary_not_found(self):
        service = PocketBaseService("/tmp/nonexistent_data")
        with patch.dict("os.environ", {}, clear=True):
            with patch("shutil.which", return_value=None):
                with self.assertRaises(PocketBaseError):
                    service.find_binary(custom_path="/tmp/nonexistent_pocketbase_binary")

    def test_find_binary_custom_valid(self):
        with tempfile.NamedTemporaryFile(suffix=".exe" if sys.platform == "win32" else "") as tmp:
            if sys.platform != "win32":
                os.chmod(tmp.name, 0o755)
            service = PocketBaseService("/tmp/data", binary_path=tmp.name)
            found = service.find_binary()
            self.assertEqual(found, Path(tmp.name).resolve())


class CliTrackerIntegrationTests(unittest.IsolatedAsyncioTestCase):
    async def asyncTearDown(self):
        await close_cli_tracker()

    async def test_record_disabled_returns_none(self):
        settings = CliSettings(track_videos=False)
        video = VideoObject(
            url="https://example.com/vid", title="Vid", author="A",
            length=10, tags=[], thumbnail_url="", video_id="1",
            publish_date=None, qualities=[720], status="completed",
        )
        outcome = DownloadOutcome("completed", Path("/tmp/vid.mp4"))
        result = await record_cli_download(settings, video, outcome)
        self.assertIsNone(result)

    async def test_print_dashboard_stats(self):
        console = Console(record=True)
        stats = {
            "enabled": True,
            "total": 10,
            "successful": 8,
            "failed": 1,
            "other": 1,
            "successRate": 89,
            "totalSizeMb": 2048.0,
            "lastDownloaded": "2026-09-18T20:00:00",
            "sources": [
                {"name": "PornHub Model", "total": 6, "successful": 5, "failed": 1, "other": 0},
                {"name": "Direct downloads", "total": 4, "successful": 3, "failed": 0, "other": 1},
            ],
        }
        print_dashboard_stats(stats, console)
        output = console.export_text()
        self.assertIn("PocketBase Download Statistics", output)
        self.assertIn("89%", output)
        self.assertIn("2.00 GB", output)
        self.assertIn("PornHub Model", output)

    async def test_print_failed_downloads_empty_and_populated(self):
        console = Console(record=True)
        print_failed_downloads([], console)
        self.assertIn("No failed downloads recorded", console.export_text())

        console = Console(record=True)
        print_failed_downloads([
            {"title": "Broken Stream", "video_id": "123", "status": "failed", "url": "https://broken.com"},
        ], console)
        output = console.export_text()
        self.assertIn("Broken Stream", output)
        self.assertIn("123", output)

    async def test_print_origin_iterators(self):
        console = Console(record=True)
        print_origin_iterators([
            {"name": "Sweetie Fox", "url": "https://xvideos.com/sweetie-fox"},
        ], console)
        self.assertIn("Sweetie Fox", console.export_text())


class DatabaseBridgeTests(unittest.TestCase):
    def test_database_bridge_wraps_tracker(self):
        tracker = PocketBaseTracker(enabled=False)
        bridge = DatabaseBridge(tracker=tracker)
        self.assertEqual(bridge._enabled, False)
        self.assertEqual(bridge.getDashboardStats()["total"], 0)
        self.assertEqual(bridge.getAvailableIterators(), [])
        self.assertEqual(bridge.getFailedVideosForIterator("https://test"), [])
        self.assertEqual(bridge._status_bucket("completed"), "successful")


if __name__ == "__main__":
    unittest.main()
