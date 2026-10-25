"""Offline layout checks with representative queue states; no provider requests."""
import os
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ["QML_DISABLE_DISK_CACHE"] = "1"

from PySide6.QtCore import QAbstractListModel, QMetaObject, QModelIndex, Qt, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickItem
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtTest import QTest

QQuickStyle.setStyle("Material")
_app = QGuiApplication.instance() or QGuiApplication([])


class QueueModel(QAbstractListModel):
    names = ["jobId", "title", "author", "duration", "availableQualities",
             "selectedQuality", "progress", "selected", "status"]
    states = ["pending", "downloading", "completed", "failed", "queued", "stopping", "cancelled"]

    def roleNames(self):
        return {Qt.UserRole + i: name.encode() for i, name in enumerate(self.names)}

    def rowCount(self, parent=QModelIndex()):
        return len(self.states)

    def data(self, index, role):
        values = [f"job{index.row()}", "A longer example video title to verify wrapping on small screens",
                  "Example creator", "12 min 30 sec", ["480", "720", "1080"], "720", 42, False,
                  self.states[index.row()]]
        offset = role - Qt.UserRole
        return values[offset] if 0 <= offset < len(values) else None


def visual_items(item):
    yield item
    for child in item.childItems():
        yield from visual_items(child)


HARNESS = r'''
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Material
ApplicationWindow {
 visible: true; width: 400; height: 800
 Material.accent: "#6366f1"
 Material.primary: "#6366f1"
 property QtObject appSettings: QtObject {
 property bool dark_mode: false
 property string android_output_folder: ""
 property bool anonymous_mode: false
 property string core_style: "Material"
 }
 property QtObject bridge: QtObject { property bool isPremium: false }
 property QtObject backend: QtObject {
 property bool busy: false
 property var downloads: sampleModel
 }

 AndroidDownloadsPage { id: page; objectName: "page"; anchors.fill: parent }
}
'''

class AndroidDownloadLayoutTests(unittest.TestCase):
    def setUp(self):
        self.engine = QQmlApplicationEngine()
        self.model = QueueModel()
        self.engine.rootContext().setContextProperty("sampleModel", self.model)
        self.warnings = []
        self.engine.warnings.connect(lambda errors: self.warnings.extend(e.toString() for e in errors))
        location = Path(__file__).resolve().parents[2] / "frontend/UI/MobileLayoutTest.qml"
        self.engine.loadData(HARNESS.encode(), QUrl.fromLocalFile(str(location)))
        self.assertTrue(self.engine.rootObjects())
        self.window = self.engine.rootObjects()[0]
        self.page = self.window.findChild(QQuickItem, "page")
        self.queue = next(item for item in visual_items(self.page)
                          if item.objectName() == "mobileDownloadList")

    def tearDown(self):
        self.window.close()
        self.engine.deleteLater()
        _app.processEvents()

    def test_queue_uses_available_space_and_details_expand(self):
        for width, height in [(320, 640), (400, 800), (800, 400), (600, 960), (1280, 800)]:
            with self.subTest(width=width, height=height):
                self.window.resize(width, height)
                QTest.qWait(50)
                self.assertLessEqual(self.queue.width(), width)
                self.assertGreater(self.queue.height(), height * .5)
                self.assertEqual(self.queue.property("count"), 7)
        self.window.resize(320, 640)
        self.page.setProperty("expandedJob", "job0")
        self.page.setProperty("selectionMode", True)
        QTest.qWait(50)
        combos = [item for item in visual_items(self.page) if item.property("currentText") == "720"]
        self.assertTrue(combos, "Expanded details preserve the selected quality")
        self.assertGreater(self.queue.height(), 200)
        self.assertEqual(self.warnings, [])

    def test_add_sheet_opens_and_filters_remain_available(self):
        button = next(item for item in visual_items(self.page) if item.property("text") == "Add videos")
        QMetaObject.invokeMethod(button, "clicked")
        QTest.qWait(100)
        sheet = self.window.findChild(object, "mobileAddSheet")
        self.assertTrue(sheet.property("visible"))
        self.page.setProperty("showFilters", True)
        QTest.qWait(50)
        self.assertEqual(self.warnings, [])


if __name__ == "__main__":
    unittest.main()
