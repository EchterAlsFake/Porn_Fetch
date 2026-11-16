"""Exercise the real creator QML with session-only fixtures and no app services."""
import os
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QUICK_BACKEND", "software")
os.environ["QML_DISABLE_DISK_CACHE"] = "1"

import shiboken6
from PySide6.QtCore import QObject, QPoint, Qt, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent, QQmlExpression
from PySide6.QtQuick import QQuickWindow  # noqa: F401 - register the concrete QML window wrapper
from PySide6.QtTest import QTest

_app = QGuiApplication.instance() or QGuiApplication([])
UI = Path(__file__).resolve().parents[2] / "frontend/UI"


class CreatorsPreviewTests(unittest.TestCase):
    def setUp(self):
        self.engine = QQmlApplicationEngine()
        self.warnings = []
        self.engine.warnings.connect(lambda errors: self.warnings.extend(e.toString() for e in errors))
        component = QQmlComponent(self.engine)
        component.setData(b'''import QtQuick
QtObject {
 property bool dark_mode: true; property bool high_contrast: false
 property string accent_color: "#a69bff"; property int font_size: 12
 property bool anonymous_mode: false; property bool reduced_motion: true
}''', QUrl())
        self.settings = component.create()
        self.engine.rootContext().setContextProperty("appSettings", self.settings)
        self.engine.load(QUrl.fromLocalFile(str(UI / "CreatorsPreview.qml")))
        self.assertTrue(self.engine.rootObjects(), self.warnings)
        self.window = self.engine.rootObjects()[0]
        self.page = self.window.findChild(QObject, "creatorsPage")
        self.dialog = self.page.findChild(QObject, "creatorSubscriptionDialog")
        QTest.qWait(30)

    def tearDown(self):
        self.window.close()
        shiboken6.delete(self.engine)
        shiboken6.delete(self.settings)

    def evaluate(self, code, scope=None):
        expression = QQmlExpression(self.engine.contextForObject(scope or self.page), scope or self.page, code)
        result = expression.evaluate()
        self.assertFalse(expression.hasError(), expression.error().toString())
        return result[0]

    def control(self, name):
        control = self.window.findChild(QObject, name)
        if control is None:
            control = self.evaluate(f'findControl(contentItem, "{name}")')
        self.assertIsNotNone(control, name)
        return control

    def click(self, control):
        control.forceActiveFocus(Qt.TabFocusReason)
        _app.processEvents()
        QTest.qWait(20)
        position = control.mapToScene(control.boundingRect().center())
        QTest.mouseClick(self.window, Qt.LeftButton, Qt.NoModifier, QPoint(round(position.x()), round(position.y())))
        _app.processEvents()

    def test_add_edit_duplicate_and_modal_focus(self):
        self.click(self.control("creatorAddButton"))
        self.assertTrue(self.dialog.property("opened"))
        self.assertEqual(self.window.activeFocusItem().objectName(), "creatorUrlInput")
        self.evaluate("save()", self.dialog)
        self.assertTrue(self.dialog.property("errorText"))
        self.control("creatorUrlInput").setProperty("text", "https://www.bellesa.co/performers/sample")
        self.control("creatorNameInput").setProperty("text", "Sample performer")
        self.click(self.control("creatorSaveButton"))
        self.assertEqual(self.evaluate("previewModel.sources.length"), 5)
        self.assertFalse(self.dialog.property("opened"))
        self.assertEqual(self.window.activeFocusItem().objectName(), "creatorAddButton")
        self.click(self.control("creatorAddButton"))
        self.control("creatorUrlInput").setProperty("text", "https://www.bellesa.co/performers/sample")
        self.control("creatorNameInput").setProperty("text", "Duplicate")
        self.click(self.control("creatorSaveButton"))
        self.assertTrue(self.dialog.property("opened"))
        self.assertEqual(self.evaluate("previewModel.sources.length"), 5)
        QTest.keyClick(self.window, Qt.Key_Escape)
        self.assertFalse(self.dialog.property("opened"))
        self.evaluate('present("s10", null)', self.dialog)
        self.control("creatorNameInput").setProperty("text", "Updated performer")
        self.click(self.control("creatorSaveButton"))
        self.assertEqual(self.evaluate('previewModel.source("s10").name'), "Updated performer")
        self.assertEqual(self.warnings, [])

    def test_detail_scan_download_and_filter_bindings(self):
        self.evaluate('openSource("s1", null)')
        _app.processEvents()
        self.assertTrue(self.page.property("detailOpen"))
        self.assertEqual(self.page.property("pageCount"), 12)
        self.click(self.control("creatorDownloadButton"))
        self.assertEqual(self.evaluate("selectedCounts.downloading"), 1)
        self.control("creatorVideoAction-v0").forceActiveFocus(Qt.TabFocusReason)
        QTest.qWait(850)
        _app.processEvents()  # Settle deferred focus restoration after replacing preview rows.
        self.assertEqual(self.window.activeFocusItem().objectName(), "creatorVideoAction-v0")
        self.assertGreater(self.evaluate('selectedSource.videos.find(v => v.status === "downloading").progress'), 12)
        self.evaluate('previewModel.bulk(selectedId, "pause")')
        self.assertEqual(self.evaluate("selectedCounts.downloading"), 0)
        self.click(self.control("creatorScanButton"))
        self.assertEqual(self.evaluate("selectedSource.scan"), "scanning")
        self.evaluate("previewModel.finishScan(selectedId)")
        self.assertEqual(self.evaluate("selectedCounts.total"), 139)
        self.page.setProperty("videoFilter", 6)
        _app.processEvents()
        self.assertEqual(self.evaluate("filteredVideos.length"), 1)
        self.evaluate('previewModel.bulk(selectedId, "retry")')
        self.assertEqual(self.evaluate("filteredVideos.length"), 0)
        self.click(self.control("creatorBackButton"))
        self.assertFalse(self.page.property("detailOpen"))
        self.assertEqual(self.warnings, [])

    def test_recent_scans_toggle_and_timestamps(self):
        self.evaluate('openSource("s1", null)')
        _app.processEvents()
        button = self.control("creatorScanHistoryButton")
        button.forceActiveFocus(Qt.TabFocusReason)
        QTest.keyClick(self.window, Qt.Key_Return)
        self.assertTrue(self.page.property("historyOpen"))
        self.assertEqual(self.control("creatorLastCompleteValue").property("text"), "Not yet")
        self.assertEqual(self.control("creatorQualityValue").property("text"), "1080p")
        self.assertTrue(self.evaluate('dateText("2026-11-15T09:42:00Z").length > 0'))
        QTest.keyClick(self.window, Qt.Key_Return)
        self.assertFalse(self.page.property("historyOpen"))
        self.assertEqual(self.warnings, [])

    def test_trial_notice_and_detail_cards_explain_the_free_limits(self):
        self.evaluate('previewModel.premium = false; openSource("s1", null)')
        _app.processEvents()
        self.assertIn("Premium", self.control("creatorPremiumNotice").property("text"))
        self.assertEqual(self.control("creatorDownloadButton").property("text"), "Resume free preview")
        self.assertEqual(self.control("creatorQualityValue").property("text"), "1080p")
        self.assertTrue(self.control("creatorDestinationValue").property("text"))
        self.assertNotEqual(self.control("creatorLastAttemptValue").property("color"), self.control("creatorLastCompleteValue").property("color"))
        self.assertGreaterEqual(self.control("creatorDownloadButton").property("implicitHeight"), 48)
        self.assertEqual(self.warnings, [])

    def test_phone_dialog_dpad_and_empty_state(self):
        self.window.setWidth(390)
        self.window.setHeight(844)
        self.evaluate("focusInitial()")
        QTest.keyClick(self.window, Qt.Key_Down)
        self.assertNotEqual(self.window.activeFocusItem().objectName(), "creatorAddButton")
        self.evaluate("focusInitial()")
        QTest.keyClick(self.window, Qt.Key_Return)
        self.assertTrue(self.dialog.property("opened"))
        QTest.keyClick(self.window, Qt.Key_Tab)
        self.assertEqual(self.window.activeFocusItem().objectName(), "creatorNameInput")
        QTest.keyClick(self.window, Qt.Key_Escape)
        self.evaluate("previewModel.sources = []")
        _app.processEvents()
        self.assertEqual(self.evaluate("visibleSources.length"), 0)
        self.click(self.control("creatorAddButton"))
        self.assertTrue(self.dialog.property("opened"))
        self.assertEqual(self.warnings, [])


if __name__ == "__main__":
    unittest.main()
