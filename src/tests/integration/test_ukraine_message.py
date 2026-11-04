"""First-launch persistence and the shared desktop/mobile personal message."""
from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PySide6.QtCore import QCoreApplication, QEvent, QObject, QSettings, Qt, QUrl, Slot
from PySide6.QtGui import QDesktopServices
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtTest import QSignalSpy, QTest

from src.backend.config import SettingsManager
from src.tests.integration.settings_support import _app

UI_DIR = Path(__file__).resolve().parents[2] / "frontend/UI"


class UrlCapture(QObject):
    def __init__(self):
        super().__init__()
        self.urls = []

    @Slot(QUrl)
    def capture(self, url):
        self.urls.append(url.toString())


class UkraineMessageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = str(Path(self.temporary.name) / "settings.ini")
        self.settings = self.load_settings()
        self.engines = []
        self.addCleanup(self.close_windows)

    def load_settings(self):
        return SettingsManager(QSettings(self.path, QSettings.Format.IniFormat))

    def close_windows(self):
        for engine in self.engines:
            for window in engine.rootObjects():
                window.close()
            engine.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        _app.processEvents()
        self.engines.clear()

    def show_message(self, width=900, height=900):
        engine = QQmlApplicationEngine()
        self.engines.append(engine)
        engine.rootContext().setContextProperty("appSettings", self.settings)
        engine.loadData(f"""
            import QtQuick
            import QtQuick.Controls
            ApplicationWindow {{
                id: window
                width: {width}; height: {height}
                visible: true
                property bool startupWaiting: false
                property int continuedCount: 0
                UkraineMessageDialog {{
                    id: message
                    settings: appSettings
                    onDismissed: window.continuedCount += 1
                }}
                Component.onCompleted: startupWaiting = message.presentOnce()
            }}
        """.encode(), QUrl.fromLocalFile(str(UI_DIR / "UkraineMessageTest.qml")))
        self.assertTrue(engine.rootObjects())
        window = engine.rootObjects()[0]
        dialog = window.findChild(QObject, "ukraineMessageDialog")
        if window.property("startupWaiting") and not dialog.property("opened"):
            opened = QSignalSpy(dialog.opened)
            self.assertTrue(opened.wait(3000))
        return window, dialog

    def test_display_is_remembered_across_restart_update_and_settings_reset(self):
        self.assertFalse(self.settings.ukraine_message_seen)
        window, dialog = self.show_message()
        self.assertTrue(dialog.property("visible"))
        self.assertTrue(window.property("startupWaiting"))
        # Save on display, even if the app closes without pressing Continue.
        self.assertTrue(self.load_settings().ukraine_message_seen)
        self.close_windows()
        with patch("src.backend.config.__version__", "999.0"):
            self.settings = self.load_settings()
            self.settings.reset()
            self.assertTrue(self.load_settings().ukraine_message_seen)
            window, dialog = self.show_message()
            self.assertFalse(dialog.property("visible"))
            self.assertFalse(window.property("startupWaiting"))

    def test_inline_sources_and_aid_links_open_in_browser(self):
        capture = UrlCapture()
        QDesktopServices.setUrlHandler("https", capture, "capture")
        self.addCleanup(lambda: QDesktopServices.unsetUrlHandler("https"))
        window, dialog = self.show_message()
        items = {}
        pending = [window.contentItem()]
        while pending:
            item = pending.pop()
            items[item.objectName()] = item
            pending.extend(item.childItems())
        for index, domains in ((1, ("ukraine.ohchr.org", "www.icc-cpi.int")),
                               (3, ("www.unhcr.org", "www.unicef.org"))):
            paragraph = items.get(f"ukraineMessageParagraph{index}")
            self.assertIsNotNone(paragraph)
            urls = re.findall(r"\]\((https://[^)]+)\)", paragraph.property("text"))
            self.assertEqual([QUrl(url).host() for url in urls], list(domains))
            for url in urls:
                paragraph.linkActivated.emit(url)
                self.assertEqual(capture.urls[-1], url)
        self.assertTrue(dialog.property("visible"))

    def test_mobile_scroll_continue_and_discovery_link(self):
        capture = UrlCapture()
        QDesktopServices.setUrlHandler("https", capture, "capture")
        self.addCleanup(lambda: QDesktopServices.unsetUrlHandler("https"))
        window, dialog = self.show_message(360, 640)
        self.assertTrue(dialog.property("visible"))
        self.assertLessEqual(dialog.property("height"), 640)
        scroll = window.findChild(QObject, "ukraineMessageScroll")
        self.assertGreater(scroll.property("contentHeight"), scroll.property("height"))
        self.assertEqual(capture.urls, [])
        star = window.findChild(QObject, "ukraineDiscoveryButton")
        point = star.mapToScene(star.boundingRect().center()).toPoint()
        QTest.mouseClick(window, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, point)
        self.assertEqual(capture.urls, ["https://www.youtube.com/watch?v=lV9q901vS6o"])
        self.assertTrue(dialog.property("visible"))
        button = window.findChild(QObject, "ukraineMessageContinueButton")
        point = button.mapToScene(button.boundingRect().center()).toPoint()
        QTest.mouseClick(window, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, point)
        QTest.qWait(250)
        self.assertFalse(dialog.property("visible"))
        self.assertEqual(window.property("continuedCount"), 1)


if __name__ == "__main__":
    unittest.main()
