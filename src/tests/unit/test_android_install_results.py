"""Native installer failures must reach the visible update notification flow."""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PySide6.QtCore import QCoreApplication

from src.backend.tor_status import TorStatus


class AndroidInstallResultTests(unittest.TestCase):
    def test_permission_and_errors_reach_update_outcomes(self):
        app = QCoreApplication.instance() or QCoreApplication([])
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {"ANDROID_PRIVATE": directory}):
            status = TorStatus()
            outcomes = []
            status.installOutcome.connect(lambda severity, message: outcomes.append((severity, message)))
            for state, severity in (("permission", "info"), ("error", "error")):
                result = Path(directory) / "install-result.json"
                result.write_text(json.dumps({"state": state, "message": "Installer response"}))
                status._install_result()
                self.assertEqual(outcomes[-1], (severity, "Installer response"))
                self.assertFalse(result.exists())
            status.deleteLater()
