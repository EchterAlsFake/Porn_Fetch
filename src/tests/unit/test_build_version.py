"""CI embeds the same release identity in binaries and publishing jobs."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.tests.unit.test_cli_self_update import load_script

writer = load_script("write_build_version")
signer = load_script("sign_desktop_release")


class BuildVersionTests(unittest.TestCase):
    def test_workflow_version_and_timestamp_are_stable_on_rerun(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "version.py"
            source.write_text('__version__ = "3.9"\nBUILD_VERSION = "3.9.0"\nRELEASE_TIMESTAMP = 1791244800\n')
            writer.write_build_version("3.9.66", 1792264598, source)
            first_build = source.read_text()
            writer.write_build_version("3.9.66", 1792264598, source)
            self.assertEqual(source.read_text(), first_build)
            values = {}
            exec(first_build, values)
            self.assertEqual(values["__version__"], "3.9.66")
            self.assertEqual(values["BUILD_VERSION"], "3.9.66")
            self.assertEqual(values["RELEASE_TIMESTAMP"], 1792264598)

    def test_current_release_notes_come_from_the_separate_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            changelog = Path(temporary) / "CHANGELOG_STATIC.md"
            changelog.write_text("# Current beta\n\n### Fixes\n- Current changes\n")
            self.assertEqual(signer.release_notes(changelog), "# Current beta\n\n### Fixes\n- Current changes")

    def test_release_version_must_be_numeric(self):
        with self.assertRaisesRegex(ValueError, "dot-separated numbers"):
            writer.write_build_version("3.9.beta", 1792264598)
