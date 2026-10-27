"""Full QML settings inventory in an isolated process; HTTP is explicitly blocked."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.tests.settings_cases import SETTINGS


class SettingsRuntimeContracts(unittest.TestCase):
    def test_all_settings_persist_reload_and_reach_the_real_runtime_consumers(self):
        root = Path(__file__).resolve().parents[3]
        with tempfile.TemporaryDirectory(prefix="settings-contract-report-") as directory:
            report = Path(directory) / "result.json"
            result = subprocess.run(
                [sys.executable, "-m", "src.tests.smoke.settings_gui", "--offline-only", "--report", str(report)],
                cwd=root, env={**os.environ, "QT_QPA_PLATFORM": "offscreen"},
                capture_output=True, text=True, timeout=90,
            )
            self.assertEqual(result.returncode, 0, result.stdout[-6000:] + result.stderr[-2000:])
            data = json.loads(report.read_text())
        self.assertEqual({row["setting"] for row in data["settings"]}, {setting.prop for setting in SETTINGS})
        self.assertEqual(data["persistence_passed"], len(SETTINGS))
        self.assertEqual(data["offline_http_attempts"], 0)
        self.assertTrue(all(row["active_configuration"] in {"PASS", "NOT_APPLICABLE"} for row in data["settings"]))
        self.assertEqual(data["auxiliary"]["status"], "PASS")
        self.assertFalse(data["effects"], "Offline discovery must not fabricate live-effect passes")
