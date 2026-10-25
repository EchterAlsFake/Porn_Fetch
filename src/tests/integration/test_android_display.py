"""Private outline transport updates after native atomic replacements."""
import json
import tempfile
import unittest
from pathlib import Path

from PySide6.QtCore import QCoreApplication
from PySide6.QtTest import QTest

from src.backend.android_display import AndroidDisplay


class AndroidDisplayTests(unittest.TestCase):
    def test_atomic_outline_update_and_desktop_fallback(self):
        self.app = QCoreApplication.instance() or QCoreApplication([])
        self.assertEqual(AndroidDisplay().outline, {})
        with tempfile.TemporaryDirectory() as directory:
            bridge = AndroidDisplay(directory)
            geometry = dict(width=1200, height=2500, corners=[
                dict(x=134, y=50, radius=134), dict(x=1066, y=50, radius=134),
                dict(x=1066, y=2450, radius=134), dict(x=134, y=2450, radius=134)])
            changes = []
            bridge.outlineChanged.connect(lambda: changes.append(bridge.outline))
            temporary = Path(directory) / "outline.tmp"
            temporary.write_text(json.dumps(geometry))
            temporary.replace(Path(directory) / "display-outline.json")
            QTest.qWait(100)
            self.assertEqual(bridge.outline, geometry)
            self.assertEqual(len(changes), 1)
            bridge.refresh()
            self.assertEqual(len(changes), 1)
