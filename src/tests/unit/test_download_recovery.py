"""Queue persistence contains recoverable metadata, never native sessions."""
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from src.shared.download_recovery import discard_changed_hls_quality, queue_record, read_queue, write_queue
from src.shared.media import VideoObject


class QueueRecoveryTests(unittest.TestCase):
    def test_changed_quality_discards_incompatible_segments_but_matching_quality_reuses_them(self):
        with tempfile.TemporaryDirectory() as directory:
            checkpoint = Path(directory) / "checkpoint"
            checkpoint.write_text(json.dumps({"quality": "1080"}))
            segments = Path(directory) / "segments"
            segments.mkdir()
            (segments / "0.ts").write_bytes(b"explicit checkpoint fixture")
            self.assertFalse(discard_changed_hls_quality(checkpoint, segments, "1080"))
            self.assertTrue(checkpoint.is_file())
            self.assertTrue(discard_changed_hls_quality(checkpoint, segments, "720"))
            self.assertFalse(checkpoint.exists())
            self.assertFalse(segments.exists())

    def video(self, path):
        return VideoObject(url="https://www.pornhub.com/view_video.php?viewkey=abc123", title="日本語 / title | name",
                           author="Author", length=2, tags=["test"], thumbnail_url="https://images.invalid/private",
                           video_id="abc123", publish_date=datetime(2026, 10, 27, tzinfo=timezone.utc),
                           qualities=[240, 720], status="downloading", identifier="a" * 32, output_path=path,
                           selected_quality="240", source_video=object(), thumbnail_data=b"private")

    def test_round_trip_keeps_job_and_path_but_restores_paused_without_a_session(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "queue.json"
            video = self.video(Path(directory) / "movie.mp4")
            write_queue(path, [queue_record(video, 42)])
            restored, progress = read_queue(path)[0]
            self.assertEqual(restored.identifier, video.identifier)
            self.assertEqual(restored.output_path, video.output_path)
            self.assertEqual(restored.publish_date, video.publish_date)
            self.assertEqual(restored.title, video.title)
            self.assertEqual(restored.selected_quality, "240")
            self.assertEqual(restored.status, "cancelled")
            self.assertEqual(progress, 42)
            self.assertIsNone(restored.source_video)
            self.assertIsNone(restored.thumbnail_data)
            self.assertNotIn("private", path.read_text())
            self.assertEqual(list(Path(directory).glob(".queue-*")), [])
            write_queue(path, [])
            self.assertEqual(read_queue(path), [])

    def test_corrupt_or_unsafe_identifiers_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "queue.json"
            record = queue_record(self.video(Path(directory) / "movie.mp4"))
            for rows in ([record | {"identifier": "../outside"}], [record, record]):
                write_queue(path, rows)
                with self.assertRaises(ValueError):
                    read_queue(path)
            path.write_text("{broken")
            with self.assertRaises(json.JSONDecodeError):
                read_queue(path)
            path.write_text("[]")
            with self.assertRaises(ValueError):
                read_queue(path)
