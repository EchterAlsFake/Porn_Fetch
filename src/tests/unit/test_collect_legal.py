"""Focused checks for legal notice downloads."""

import tempfile
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.error import URLError
from zipfile import ZipFile

module_spec = spec_from_file_location("collect_legal", Path(__file__).resolve().parents[3] / "packaging" / "collect_legal.py")
assert module_spec and module_spec.loader
collect_legal = module_from_spec(module_spec)
module_spec.loader.exec_module(collect_legal)


class CollectLegalTests(unittest.TestCase):
    def test_ffmpeg_source_and_build_details_are_included_in_legal_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "ffmpeg-legal"
            source.mkdir()
            (source / "source.tar.xz").write_bytes(b"source archive")
            (source / "configuration.txt").write_text("--disable-gpl --disable-nonfree")
            with patch.object(collect_legal, "distributions", return_value=[]):
                archive = collect_legal.collect_legal(base / "legal", offline=True, ffmpeg_legal=[source])
            with ZipFile(archive) as bundle:
                self.assertEqual(bundle.read("ffmpeg/0/source.tar.xz"), b"source archive")
                self.assertIn(b"--disable-gpl", bundle.read("ffmpeg/0/configuration.txt"))

    def test_download_retries_after_connection_timeout(self):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = b"GNU LESSER GENERAL PUBLIC LICENSE"
        with patch.object(collect_legal, "urlopen", side_effect=[URLError("timed out"), response]) as open_url:
            with patch.object(collect_legal.time, "sleep") as sleep:
                self.assertEqual(collect_legal.download_lgpl_text(), b"GNU LESSER GENERAL PUBLIC LICENSE")

        self.assertEqual(open_url.call_count, 2)
        sleep.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
