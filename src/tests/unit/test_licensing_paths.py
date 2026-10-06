"""Preserve installation identity when moving GUI users to the shared service."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.shared.paths import shared_data_dir


class LicensingPathTests(unittest.TestCase):
    def test_existing_linux_gui_database_is_reused_in_place(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            legacy = base / "EchterAlsFake/Porn Fetch"
            legacy.mkdir(parents=True)
            (legacy / "licensing.sqlite3").touch()
            with patch.dict("os.environ", {"XDG_DATA_HOME": directory}), patch("src.shared.paths.sys_platform", return_value="linux"):
                self.assertEqual(shared_data_dir(), legacy)
                preferred = base / "Porn Fetch"
                preferred.mkdir()
                (preferred / "licensing.sqlite3").touch()
                self.assertEqual(shared_data_dir(), preferred)
