"""Offline regression checks for the account, download table and credit layouts."""
import os
import unittest
from itertools import combinations
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ["QML_DISABLE_DISK_CACHE"] = "1"

from PySide6.QtCore import QMetaObject, QPointF, QUrl
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickItem
from PySide6.QtTest import QTest

from src.frontend.UI import resources  # Register bundled icons.
from src.tests.integration.test_android_download_layout import QueueModel, _app, visual_items

resources.qInitResources()

UI = Path(__file__).resolve().parents[2] / "frontend/UI"
HARNESS = '''
import QtQuick
import QtQuick.Controls
ApplicationWindow {
    visible: true; width: 1100; height: 800
    font.pixelSize: 16
    property string applicationLicenseText: "License"
    property string thirdPartyNoticesText: "Notices"
    property QtObject appSettings: QtObject {
        property bool dark_mode: true
        property bool anonymous_mode: false
        property string core_style: "Material"
    }
    property QtObject bridge: QtObject { property bool isPremium: false }
    property QtObject backend: QtObject {
        property bool busy: false
        property bool loginInProgress: false
        property bool accountFetchInProgress: false
        property var accountLoginStatus: ({"PornHub": true})
        property var downloads: sampleModel
    }
    PAGE
}
'''


class DesignLayoutTests(unittest.TestCase):
    def load(self, page):
        self.engine = QQmlApplicationEngine()
        self.model = QueueModel()
        self.engine.rootContext().setContextProperty("sampleModel", self.model)
        self.warnings = []
        self.engine.warnings.connect(lambda errors: self.warnings.extend(e.toString() for e in errors))
        self.engine.loadData(HARNESS.replace("PAGE", page).encode(), QUrl.fromLocalFile(str(UI / "DesignTest.qml")))
        self.assertTrue(self.engine.rootObjects(), self.warnings)
        self.window = self.engine.rootObjects()[0]
        self.page = self.window.findChild(QQuickItem, "page")
        self.addCleanup(self.cleanup_window)
        QTest.qWait(80)

    def cleanup_window(self):
        self.window.close()
        self.engine.deleteLater()
        _app.processEvents()

    def items(self, text):
        return [item for item in visual_items(self.page) if item.property("text") == text]

    def test_download_headers_do_not_overlap_and_options_open(self):
        self.load('DownloadsPage { objectName: "page"; anchors.fill: parent }')
        viewport = self.window.findChild(QQuickItem, "downloadTableViewport")
        for width in (760, 1600):
            self.window.resize(width, 800)
            QTest.qWait(50)
            stop = self.items("Stop / Resume")[0]
            progress = self.items("Progress")[0]
            self.assertLessEqual(stop.mapToItem(self.page, QPointF(stop.width(), 0)).x(),
                                 progress.mapToItem(self.page, QPointF()).x())
            self.assertGreaterEqual(viewport.property("contentWidth"), viewport.width())
        QMetaObject.invokeMethod(self.items("Advanced Configuration")[0], "clicked")
        QTest.qWait(50)
        QMetaObject.invokeMethod(self.items("Options")[0], "clicked")
        QTest.qWait(80)
        messages = [item for item in visual_items(self.window.contentItem())
                    if item.objectName() == "messageLabel" and item.isVisible()]
        self.assertTrue(any("$output_path" in item.property("text") for item in messages))
        self.assertEqual(self.warnings, [])

    def test_account_collections_share_a_row_below_full_width_login(self):
        self.load('AccountPage { objectName: "page"; anchors.fill: parent; backendController: backend }')
        login = self.items("Login")[0]
        buttons = [self.items(text)[0] for text in ("Get Watch History", "Get Recommended Videos",
                                                   "Get Subscription Feed", "Get Favorite Videos")]
        for width in (900, 1280):
            self.window.resize(width, 800)
            QTest.qWait(50)
            positions = [button.mapToItem(self.page, QPointF()) for button in buttons]
            self.assertLess(max(p.y() for p in positions) - min(p.y() for p in positions), 1)
            self.assertGreater(login.width(), self.page.width() - 40)
            for button, pos in zip(buttons, positions):
                self.assertLessEqual(pos.x() + button.width(), self.page.width())
            browser = self.items("Login with Browser Cookies")[0]
            self.assertGreater(browser.mapToItem(self.page, QPointF()).y(), positions[0].y())
        QMetaObject.invokeMethod(self.items("How to login")[0], "clicked")
        QTest.qWait(50)
        self.assertEqual(self.warnings, [])

    def test_credit_cards_and_their_text_do_not_overlap_after_resizing(self):
        self.load('InfoPage { objectName: "page"; anchors.fill: parent }')
        cards = [item for item in visual_items(self.page) if item.objectName() == "creditCard"]
        self.assertEqual(len(cards), 9)
        applications = next(card for card in cards if card.property("title") == "Applications")
        # A taller card must move the next row rather than cover it.
        applications.setProperty("content", "Media processing details that wrap over several lines. " * 12)
        for width in (1500, 420, 900, 1500):
            with self.subTest(width=width):
                self.window.resize(width, 800)
                QTest.qWait(60)
                bounds = []
                for card in cards:
                    pos = card.mapToItem(self.page, QPointF())
                    self.assertGreaterEqual(pos.x(), 0)
                    self.assertLessEqual(pos.x() + card.width(), self.page.width())
                    self.assertGreater(card.height(), 0)
                    bounds.append((pos.x(), pos.y(), pos.x() + card.width(), pos.y() + card.height()))
                    for text in visual_items(card):
                        if text.property("text"):
                            origin = text.mapToItem(card, QPointF())
                            self.assertGreaterEqual(origin.x(), 0)
                            self.assertGreaterEqual(origin.y(), 0)
                            self.assertLessEqual(origin.x() + text.width(), card.width() + 0.5)
                            self.assertLessEqual(origin.y() + text.height(), card.height() + 0.5)
                for a, b in combinations(bounds, 2):
                    self.assertTrue(a[2] <= b[0] + 0.5 or b[2] <= a[0] + 0.5
                                    or a[3] <= b[1] + 0.5 or b[3] <= a[1] + 0.5,
                                    f"Credit cards overlap: {a}, {b}")
        self.assertEqual(self.warnings, [])


if __name__ == "__main__":
    unittest.main()
