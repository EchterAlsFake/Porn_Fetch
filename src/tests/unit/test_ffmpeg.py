"""Offline media checks, explicitly enabled for freshly built FFmpeg executables."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from src.shared.ffmpeg import remux_ts_to_mp4, write_metadata_tags

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures/ffmpeg"
TEST_BINARY = os.environ.get("PORN_FETCH_TEST_FFMPEG")


@unittest.skipUnless(TEST_BINARY, "Set PORN_FETCH_TEST_FFMPEG to check a freshly built executable")
class MinimalFFmpegTests(unittest.TestCase):
    def setUp(self):
        self.binary = Path(TEST_BINARY).resolve()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "video.mp4"
        remux_ts_to_mp4(FIXTURES / "sample.ts", self.output, self.binary)

    def inspect(self):
        result = subprocess.run([str(self.binary), "-hide_banner", "-i", str(self.output)],
                                capture_output=True, text=True)
        return result.stderr

    def test_ts_remux_preserves_audio_and_video_with_faststart(self):
        description = self.inspect()
        self.assertIn("Video: h264", description)
        self.assertIn("Audio: aac", description)
        data = self.output.read_bytes()
        self.assertLess(data.index(b"moov"), data.index(b"mdat"))

    def test_metadata_and_jpeg_png_covers(self):
        for name in ("cover.jpg", "cover.png"):
            with self.subTest(cover=name), patch.dict(os.environ, {"PORN_FETCH_FFMPEG_BINARY": str(self.binary)}):
                metadata = SimpleNamespace(title="Tiny remux sample", author="Test artist",
                                           thumbnail_data=(FIXTURES / name).read_bytes())
                self.assertTrue(write_metadata_tags(self.output, metadata))
                description = self.inspect()
                self.assertIn("Tiny remux sample", description)
                self.assertIn("Test artist", description)
                self.assertIn("attached pic", description)
                self.assertIn("Audio: aac", description)

    def test_single_pass_ts_remux_with_metadata_and_covers(self):
        for name in ("cover.jpg", "cover.png"):
            with self.subTest(cover=name):
                single_pass_out = Path(self.temp.name) / f"single_{name}.mp4"
                metadata = SimpleNamespace(
                    title="Single-pass HLS remux",
                    author="Test artist",
                    tags=["hls", "single-pass"],
                    publish_date="2026-10-16",
                    url="https://example.com/v/42",
                    thumbnail_data=(FIXTURES / name).read_bytes(),
                )
                metadata_written = remux_ts_to_mp4(
                    FIXTURES / "sample.ts",
                    single_pass_out,
                    self.binary,
                    metadata=metadata,
                )
                self.assertTrue(metadata_written)
                result = subprocess.run(
                    [str(self.binary), "-hide_banner", "-i", str(single_pass_out)],
                    capture_output=True,
                    text=True,
                )
                description = result.stderr
                self.assertIn("Single-pass HLS remux", description)
                self.assertIn("Test artist", description)
                self.assertIn("attached pic", description)
                self.assertIn("Video: h264", description)
                self.assertIn("Audio: aac", description)
                data = single_pass_out.read_bytes()
                self.assertLess(data.index(b"moov"), data.index(b"mdat"))


if __name__ == "__main__":
    unittest.main()

