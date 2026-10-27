"""Offline disabled-history GUI contract; full live checks stay explicitly opt-in."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class StatisticsPageContracts(unittest.TestCase):
    def test_disabled_tracking_renders_without_starting_http_or_a_database(self):
        root = Path(__file__).resolve().parents[3]
        with tempfile.TemporaryDirectory(prefix="statistics-contract-") as directory:
            report = Path(directory) / "result.json"
            result = subprocess.run(
                [sys.executable, "-m", "src.tests.smoke.statistics_gui", "--offline-only", "--report", str(report)],
                cwd=root, env={**os.environ, "QT_QPA_PLATFORM": "offscreen"},
                capture_output=True, text=True, timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stdout[-3000:] + result.stderr[-2000:])
            data = json.loads(report.read_text())
        self.assertEqual(data["offline_http_attempts"], 0)
        self.assertEqual(data["pass"], 1)
        self.assertEqual(data["fail"], 0)
        self.assertEqual(data["results"][0]["check"], "tracking-disabled")
        self.assertTrue(data["results"][0]["evidence"]["no_database_or_saved_records"])
        self.assertFalse(data["results"][0]["evidence"]["real_preparation_checked"])
