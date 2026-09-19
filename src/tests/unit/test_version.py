"""Ensure installed metadata uses the Python version constant."""
import unittest
from importlib.metadata import version

from src.shared.version import __version__


class VersionMetadataTests(unittest.TestCase):
    def test_installed_metadata_matches_python_version(self) -> None:
        self.assertEqual(version("Porn_Fetch"), __version__)


if __name__ == "__main__":
    unittest.main()
