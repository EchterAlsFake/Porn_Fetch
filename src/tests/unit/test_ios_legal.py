"""Check that the pinned iOS media extension ships its corresponding source materials."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

from src.tests.unit.test_cli_self_update import load_script
from src.tests.unit.test_collect_legal import collect_legal

ios_legal = load_script("prepare_ios_legal")
ROOT = Path(__file__).resolve().parents[3]


class IOSLegalTests(unittest.TestCase):
    def test_native_build_materials_reach_the_release_legal_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            device = root / "device"
            native = device / "native/packages"
            legal = native / "ffmpeg-legal"
            legal.mkdir(parents=True)
            for name in ("COPYING.LGPLv2.1", "LICENSE.md", "config.h", "config_components.h", "configuration.txt"):
                (legal / name).write_text(f"Actual build: {name}")
            binary = native / "_ios_ffmpeg.cpython-315-iphoneos.so"
            binary.write_bytes(b"pinned native extension")
            archive = root / "ffmpeg-9.0.2.tar.xz"
            archive.write_bytes(b"complete source archive")
            provenance = json.loads((ROOT / "ios-lab/device/BUILD-REVISIONS.json").read_text())["ffmpeg"]
            provenance.update(source_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
                              native_extension_sha256=hashlib.sha256(binary.read_bytes()).hexdigest())
            original_loads = json.loads

            def load_provenance(text):
                value = original_loads(text)
                return {**value, "ffmpeg": provenance}

            with patch.object(ios_legal.json, "loads", side_effect=load_provenance):
                result = ios_legal.prepare(device, archive)
                binary.write_bytes(b"unrecorded replacement")
                with self.assertRaisesRegex(ValueError, "extension does not match"):
                    ios_legal.prepare(device, archive)
            with patch.object(collect_legal, "distributions", return_value=[]):
                bundle = collect_legal.collect_legal(root / "LEGAL", offline=True, ffmpeg_legal=[result])
            with ZipFile(bundle) as contents:
                self.assertEqual(contents.read("ffmpeg/0/ffmpeg-9.0.2.tar.xz"), archive.read_bytes())
                self.assertEqual(contents.read("ffmpeg/0/bridge.c"), (ROOT / "ios-lab/device/ffmpeg/bridge.c").read_bytes())
                for name in ("apple-probe.m", "config.h", "configuration.txt", "build-ffmpeg.py", "REBUILD.md", "build.json"):
                    self.assertIn("ffmpeg/0/" + name, contents.namelist())

    def test_ci_passes_the_native_legal_directory_to_the_collector(self):
        workflow = (ROOT / ".github/workflows/build_all.yml").read_text()
        self.assertIn('--ffmpeg-legal "$IOS_WORK_ROOT/lab/device/native/packages/ffmpeg-legal"', workflow)

