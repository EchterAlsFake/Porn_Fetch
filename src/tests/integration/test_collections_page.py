"""Production source controls validate input without requesting remote data."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CollectionControlContracts(unittest.TestCase):
    def test_source_validation_is_offline_and_restores_idle_controls(self):
        root = Path(__file__).resolve().parents[3]
        with tempfile.TemporaryDirectory(prefix="collection-contract-") as temporary:
            report = Path(temporary) / "result.json"
            result = subprocess.run(
                [sys.executable, "-m", "src.tests.smoke.collections_gui", "--offline-only", "--report", str(report)],
                cwd=root, env={**os.environ, "QT_QPA_PLATFORM": "offscreen"},
                capture_output=True, text=True, timeout=45,
            )
            self.assertEqual(result.returncode, 0, result.stdout[-2500:] + result.stderr[-3000:])
            data = json.loads(report.read_text())
        self.assertEqual(data["http_attempts"], 0)
        self.assertEqual(data["pass"], 10)
        self.assertEqual({row["id"] for row in data["results"]},
                         {kind + "." + case for kind in ("model", "playlist")
                          for case in ("empty", "unsupported", "single-video", "wrong-kind", "invalid-regex")})
