"""Actual window-close/loop-exit contracts in two isolated, HTTP-blocked processes."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ApplicationRecoveryContracts(unittest.TestCase):
    def test_idle_window_closes_once_reaps_tasks_and_reopens_without_http(self):
        root = Path(__file__).resolve().parents[3]
        with tempfile.TemporaryDirectory(prefix="recovery-contract-") as directory:
            report = Path(directory) / "result.json"
            result = subprocess.run(
                [sys.executable, "-m", "src.tests.smoke.application_recovery", "--offline-only", "--report", str(report)],
                cwd=root, env={**os.environ, "QT_QPA_PLATFORM": "offscreen"}, capture_output=True, text=True, timeout=75,
            )
            self.assertEqual(result.returncode, 0, result.stdout[-2000:] + result.stderr[-2000:])
            data = json.loads(report.read_text())
        self.assertEqual(data["passed"], 1)
        self.assertEqual(data["failed"], 0)
        for phase in data["results"][0]["phases"]:
            self.assertTrue(phase["shutdown_once"])
            self.assertTrue(phase["queue_restored_without_provider_requests"])
            self.assertTrue(phase["network_closed"])
            self.assertFalse(phase["remaining_tasks"])
            self.assertEqual(phase["requests"], [])
