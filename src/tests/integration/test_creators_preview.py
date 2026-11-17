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
        self.assertEqual(self.evaluate("filteredVideos.length"), 0)
        self.evaluate('previewModel.bulk(selectedId, "retry")')
        self.assertEqual(self.evaluate("filteredVideos.length"), 0)
        self.click(self.control("creatorBackButton"))
        self.assertFalse(self.page.property("detailOpen"))
        self.assertEqual(self.warnings, [])

    def test_download_all_uses_every_page_and_supports_keyboard(self):
        self.evaluate('openSource("s1", null)')
        _app.processEvents()
        completed = self.evaluate("selectedCounts.completed")
        ignored = self.evaluate("selectedCounts.ignored")
        button = self.control("creatorDownloadButton")
        self.assertEqual(button.property("text"), "Download all videos")
        self.assertGreater(self.page.property("pageCount"), 1)
        button.forceActiveFocus(Qt.TabFocusReason)
        QTest.keyClick(self.window, Qt.Key_Return)
        _app.processEvents()
        self.assertEqual(self.evaluate("selectedCounts.newCount + selectedCounts.paused + selectedCounts.failed"), 0)
        self.assertEqual(self.evaluate("selectedCounts.completed"), completed)
        self.assertEqual(self.evaluate("selectedCounts.ignored"), ignored)
        self.assertEqual(self.evaluate("selectedCounts.pending + selectedCounts.downloading"),
                         self.evaluate("selectedCounts.total") - completed - ignored)
        self.assertFalse(button.property("enabled"))
        self.assertEqual(self.window.activeFocusItem().objectName(), "creatorVideoFilter")
        self.assertEqual(self.warnings, [])

    def test_total_progress_counts_completed_videos_and_excludes_ignored(self):
        self.evaluate('openSource("s1", null)')
        _app.processEvents()
        progress = self.control("creatorTotalProgressBar")
        label = self.control("creatorTotalProgressLabel")
        self.assertEqual(label.property("text"), "130 of 138 videos downloaded")
        self.assertEqual(progress.property("value"), 130)
        self.assertEqual(progress.property("to"), 138)
        self.evaluate('previewModel.videoAction(selectedId, "v0", "ignored")')
        self.assertEqual(progress.property("to"), 137)
        self.evaluate('previewModel.videoAction(selectedId, "v1", "completed")')
        self.assertEqual(progress.property("value"), 131)
        self.assertEqual(label.property("text"), "131 of 137 videos downloaded")
        self.page.setProperty("videoFilter", 5)
        self.page.setProperty("videoPage", 1)
        self.assertEqual(label.property("text"), "131 of 137 videos downloaded")
        self.assertEqual(self.warnings, [])

    def test_storage_dialog_location_preview_import_choices_and_focus(self):
        dialog = self.control("libraryStorageDialog")
        self.evaluate("""storageBridge = Qt.createQmlObject('import QtQuick; QtObject { property bool transferBusy: false; property bool transferSupported: true; property real transferProgress: -1; property string transferStage: "Copying files"; property string chosen: ""; signal transferPreview(string kind, var details); signal transferFinished(string message); function cancelTransfer() {} function confirmTransfer(mode) { chosen = mode } function previewRelocation(oldFolder, newFolder, mode) { transferPreview("relocate", {videos: 3, folders: 1, mode: mode}) } }', this)""", dialog)
        self.evaluate('openSource("s1", null)')
        _app.processEvents()
        button = self.control("creatorMoveLocationButton")
        button.forceActiveFocus(Qt.TabFocusReason)
        QTest.keyClick(self.window, Qt.Key_Return)
        QTest.qWait(30)
        self.assertEqual(self.window.activeFocusItem().objectName(), "storageOldFolder")
        self.assertTrue(self.control("storageOldFolder").property("text"))
        self.assertFalse(self.control("storageMigrationSection").property("visible"))
        self.evaluate('storageBridge.transferBusy = true; storageBridge.transferProgress = 0.4', dialog)
        self.assertTrue(self.control("storageProgressBar").property("visible"))
        self.assertFalse(self.control("storageProgressBar").property("indeterminate"))
        self.assertAlmostEqual(self.control("storageProgressBar").property("value"), .4)
        self.assertIn("40%", self.control("storageProgressLabel").property("text"))
        self.evaluate('storageBridge.transferFinished("Move failed before copying")', dialog)
        self.evaluate('storageBridge.transferBusy = false', dialog)
        self.assertTrue(self.control("storageProgressBar").property("visible"))
        self.assertEqual(self.control("storageStatus").property("text"), "Move failed before copying")
        self.control("storageNewFolder").setProperty("text", "/new-library")
        self.control("storageMoveButton").forceActiveFocus(Qt.TabFocusReason)
        QTest.keyClick(self.window, Qt.Key_Return)
        QTest.qWait(30)
        self.assertTrue(self.control("storageConfirmDialog").property("opened"))
        self.assertEqual(self.window.activeFocusItem().objectName(), "storageConfirmCancel")
        QTest.keyClick(self.window, Qt.Key_Return)
        QTest.qWait(30)
        self.evaluate('storageBridge.transferPreview("import", {subscriptions: 4, videos: 30, existing: 2, history: 7})', dialog)
        QTest.qWait(30)
        self.assertTrue(self.control("storageConfirmMerge").property("visible"))
        self.assertTrue(self.control("storageConfirmReplace").property("visible"))
        self.control("storageConfirmMerge").forceActiveFocus(Qt.TabFocusReason)
        QTest.keyClick(self.window, Qt.Key_Return)
        self.assertEqual(self.evaluate("storageBridge.chosen", dialog), "merge")
        QTest.qWait(30)
        QTest.keyClick(self.window, Qt.Key_Escape)
        QTest.qWait(30)
        self.assertFalse(self.control("libraryStorageDialog").property("opened"))
        self.assertEqual(self.window.activeFocusItem().objectName(), "creatorMoveLocationButton")
        self.assertEqual(self.warnings, [])

    def test_import_and_export_share_the_header_actions_with_add_subscription(self):
        add = self.control("creatorAddButton")
        for width in (1200, 390):
            self.window.setWidth(width)
            QTest.qWait(30)
            for name in ("creatorImportButton", "creatorExportButton"):
                button = self.control(name)
                self.assertTrue(button.property("visible"))
                self.assertEqual(button.parentItem(), add.parentItem())
                position = button.mapToScene(button.boundingRect().topLeft())
                self.assertGreaterEqual(position.x(), 0)
                self.assertLessEqual(position.x() + button.width(), width)
        self.assertEqual(self.warnings, [])

    def test_library_file_picker_opens_alone_and_cancel_restores_header_focus(self):
        dialog = self.control("libraryStorageDialog")
        self.evaluate("""storageBridge = Qt.createQmlObject('import QtQuick; QtObject { property bool transferBusy: false; property bool transferSupported: true; property real transferProgress: -1; property string transferStage: "Preparing"; property string chosen: ""; signal transferPreview(string kind, var details); signal transferFinished(string message); function cancelTransfer() {} function exportLibrary(filename) { chosen = "export:" + filename; transferBusy = true } function previewImport(filename) { chosen = "import:" + filename; transferBusy = true } }', this)""", dialog)
        for action in ("import", "export"):
            button = self.control("creatorImportButton" if action == "import" else "creatorExportButton")
            button.forceActiveFocus(Qt.TabFocusReason)
            QTest.keyClick(self.window, Qt.Key_Return)
            QTest.qWait(30)
            picker = self.control("storageImportPicker" if action == "import" else "storageExportPicker")
            self.assertTrue(picker.property("visible"))
            self.assertFalse(dialog.property("opened"))
            self.evaluate("reject()", picker)
            QTest.qWait(30)
            self.assertFalse(dialog.property("opened"))
            self.assertEqual(self.window.activeFocusItem(), button)
        # Selecting a filename starts the operation and opens only progress/results.
        self.evaluate('startMigration("/tmp/library.zip")', dialog)
        _app.processEvents()
        self.assertTrue(dialog.property("opened"))
        self.assertEqual(self.evaluate("storageBridge.chosen", dialog), "export:/tmp/library.zip")
        self.assertTrue(self.control("storageProgressBar").property("visible"))
        self.assertIsNone(self.window.findChild(QObject, "storageExportButton"))
        self.assertIsNone(self.window.findChild(QObject, "storageImportButton"))
        self.evaluate('storageBridge.transferBusy = false; storageBridge.transferFinished("Export complete")', dialog)
        QTest.qWait(30)
        QTest.keyClick(self.window, Qt.Key_Escape)
        QTest.qWait(30)
        self.assertEqual(self.window.activeFocusItem().objectName(), "creatorExportButton")
        self.assertEqual(self.warnings, [])

    def test_integrity_progress_and_keyboard_recheck(self):
        self.evaluate('previewModel.integrityMessage = "Checking downloads"; previewModel.integrityBusy = true; previewModel.integrityTotal = 2; previewModel.integrityDone = 1')
        _app.processEvents()
        self.assertTrue(self.control("creatorIntegrityNotice").property("visible"))
        progress = self.control("creatorIntegrityProgress")
        self.assertTrue(progress.property("visible"))
        self.assertEqual(progress.property("value"), 1)
        self.assertEqual(progress.property("to"), 2)
        self.assertFalse(self.control("creatorCheckIntegrityButton").property("enabled"))
        self.evaluate('previewModel.integrityBusy = false; previewModel.integrityIssues = 1; previewModel.integrityMessage = "One file is missing"')
        button = self.control("creatorCheckIntegrityButton")
        button.forceActiveFocus(Qt.TabFocusReason)
        QTest.keyClick(self.window, Qt.Key_Return)
        self.assertIn("Sample integrity check", self.control("creatorIntegrityMessage").property("text"))
        full = self.control("creatorFullVerificationButton")
        full.forceActiveFocus(Qt.TabFocusReason)
        QTest.keyClick(self.window, Qt.Key_Return)
        self.assertIn("Sample full verification", self.control("creatorIntegrityMessage").property("text"))
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
