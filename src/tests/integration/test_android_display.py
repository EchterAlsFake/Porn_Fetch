"""Private outline transport updates after native atomic replacements."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PySide6.QtCore import QCoreApplication, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtTest import QTest

from src.backend.android_display import AndroidDisplay


class AndroidDisplayTests(unittest.TestCase):
    def test_atomic_outline_update_and_desktop_fallback(self):
        self.app = QCoreApplication.instance() or QCoreApplication([])
        self.assertEqual(AndroidDisplay().outline, {})
        self.assertTrue(AndroidDisplay().keyboardNavigation)
        with tempfile.TemporaryDirectory() as directory:
            bridge = AndroidDisplay(directory)
            self.assertFalse(bridge.keyboardNavigation)
            geometry = dict(keyboardNavigation=True, width=1200, height=2500, corners=[
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
            self.assertTrue(bridge.keyboardNavigation)
            bridge.refresh()
            self.assertEqual(len(changes), 1)

    def test_touch_device_keeps_keyboard_navigation_disabled(self):
        self.app = QCoreApplication.instance() or QCoreApplication([])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "display-outline.json"
            path.write_text(json.dumps(dict(width=400, height=800, keyboardNavigation=False,
                corners=[dict(x=0, y=0, radius=0)] * 4)))
            self.assertFalse(AndroidDisplay(directory).keyboardNavigation)

    def test_tv_policy_and_browser_free_web_links(self):
        self.app = QCoreApplication.instance() or QCoreApplication([])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "display-outline.json"
            path.write_text(json.dumps(dict(width=1920, height=1080, keyboardNavigation=True,
                television=True, corners=[dict(x=0, y=0, radius=0)] * 4)))
            bridge = AndroidDisplay(directory)
            self.assertTrue(bridge.television)
            links = []
            bridge.webLinkRequested.connect(links.append)
            with patch("src.backend.android_display.QDesktopServices.openUrl") as browser:
                bridge.open_web_link(QUrl("https://pornfetch.to/"))
                browser.assert_not_called()
            self.assertEqual(links, ["https://pornfetch.to/"])
            bridge.install_url_handlers()
            try:
                self.assertTrue(QDesktopServices.openUrl(QUrl("https://pornfetch.to/download")))
                self.assertEqual(links[-1], "https://pornfetch.to/download")
            finally:
                bridge.close()
            with patch("src.backend.android_display.QDesktopServices.openUrl") as browser:
                AndroidDisplay().open_web_link(QUrl("https://pornfetch.to/"))
                browser.assert_called_once()

    def test_vehicle_state_arrives_before_geometry_and_switches_controller_policy(self):
        self.app = QCoreApplication.instance() or QCoreApplication([])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "automotive-state.json"
            state = dict(automotive=True, carMode=True, systemNavigation=True,
                         controllerNavigation=True, foreground=True, restricted=True, restrictionsKnown=True)
            path.write_text(json.dumps(state))
            bridge = AndroidDisplay(directory)
            self.assertTrue(bridge.automotive)
            self.assertTrue(bridge.carMode)
            self.assertTrue(bridge.systemNavigation)
            self.assertTrue(bridge.interactionBlocked)
            self.assertTrue(bridge.keyboardNavigation)
            links = []
            bridge.webLinkRequested.connect(links.append)
            bridge.open_web_link(QUrl("https://pornfetch.to/"))
            self.assertEqual(links, [])
            state.update(restricted=False, controllerNavigation=False, foreground=False)
            temporary = path.with_suffix(".tmp")
            temporary.write_text(json.dumps(state))
            temporary.replace(path)
            QTest.qWait(60)
            self.assertFalse(bridge.interactionBlocked)
            self.assertFalse(bridge.keyboardNavigation)
            self.assertFalse(bridge.foreground)
            bridge.open_web_link(QUrl("https://pornfetch.to/"))
            self.assertEqual(links, ["https://pornfetch.to/"])

    def test_manual_car_layout_does_not_claim_vehicle_restriction_support(self):
        self.app = QCoreApplication.instance() or QCoreApplication([])
        bridge = AndroidDisplay()
        bridge.setCarControls(True)
        self.assertTrue(bridge.carMode)
        self.assertFalse(bridge.automotive)
        self.assertFalse(bridge.interactionBlocked)
        self.assertFalse(bridge.systemNavigation)
        bridge.setCarControls(False)
        self.assertFalse(bridge.carMode)
