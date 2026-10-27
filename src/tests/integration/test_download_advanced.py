"""Actual advanced QML controls and explicit metadata fixtures without HTTP."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


class AdvancedControlContracts(unittest.TestCase):
    def test_validation_unusual_titles_templates_and_dialogs(self):
        root = Path(__file__).resolve().parents[3]
        with tempfile.TemporaryDirectory(prefix="advanced-contract-") as directory:
            report = Path(directory) / "result.json"
            result = subprocess.run(
                [sys.executable, "-m", "src.tests.smoke.download_advanced", "--offline-only", "--report", str(report)],
                cwd=root, env={**os.environ, "QT_QPA_PLATFORM": "offscreen"},
                capture_output=True, text=True, timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stdout[-3000:] + result.stderr[-2000:])
            data = json.loads(report.read_text())
        self.assertEqual(data["offline_http_attempts"], 0)
        self.assertEqual(data["pass"], 4)
        self.assertEqual(data["fail"], 0)
        self.assertEqual(data["pending"], 0)
        fixture = next(row for row in data["results"] if row["check"] == "unusual-title-fixtures")
        self.assertGreaterEqual(fixture["evidence"]["fixtures"], 20)
        self.assertEqual(fixture["evidence"]["data_kind"], "synthetic-metadata")


class OriginalTitleContracts(unittest.IsolatedAsyncioTestCase):
    async def test_provider_adapter_preserves_explicit_unusual_title_metadata(self):
        from src.backend import clients
        from src.tests.unit.test_download_options import TITLES

        class MetadataFixture(SimpleNamespace):
            pass

        with patch.object(clients, "ph_Video", MetadataFixture):
            for title in TITLES:
                source = MetadataFixture(loader_methods={}, title=title, url="https://fixture.invalid/title",
                                         author_information={"name": "作者 / Studio | A"}, duration=120,
                                         tags=["test"], publish_date="2026-10-27", thumbnail="", video_id="fixture",
                                         video_qualities=[240, 720])
                with self.subTest(title=title[:50]):
                    metadata = await clients.load_video_attributes(source)
                    self.assertEqual(metadata.title, title)
                    self.assertEqual(metadata.author, "作者 / Studio | A")
