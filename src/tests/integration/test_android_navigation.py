"""Offline touch and Back navigation checks with unrelated services stubbed out."""
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QUICK_BACKEND", "software")
os.environ["QML_DISABLE_DISK_CACHE"] = "1"

from PySide6.QtCore import QMetaObject, QObject, QPoint, Qt, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent
from PySide6.QtQuick import QQuickItem
from PySide6.QtTest import QTest

from src.frontend.UI import resources  # noqa: F401

_app = QGuiApplication.instance() or QGuiApplication([])
UI = Path(__file__).resolve().parents[2] / "frontend/UI"


class AndroidNavigationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="android-navigation-")
        root = Path(self.directory.name)
        for name in ("AndroidMain.qml", "BackSwipeArea.qml", "RemoteNavigation.qml"):
            (root / name).write_text((UI / name).read_text())
        (root / "qmldir").write_text("singleton Theme 1.0 Theme.qml\n")
        (root / "Theme.qml").write_text('''pragma Singleton
import QtQuick
QtObject {
 property color background: "white"; property color ink: "black"
 property color surface: "white"; property color muted: "gray"
 property color accent: "blue"; property color selectionInk: "white"
 property color outline: "gray"; property color disabledInk: "gray"
}''')
        stubs = {
            "ServiceTorFailureDialog": "property bool presentationBlocked: false",
            "ActivityEdge": '''property var outline; property bool active: false
                property color accentColor; property bool animationAllowed: false''',
            "FirstRunSetup": '''property var settings; property string licenseText
                property string reportDisclosure; property bool fullScreen; property bool requireOutputFolder
                property bool active: false; property bool keyboardNavigation; signal finished(); signal quitRequested()
                function begin() { return false }''',
            "NotificationPanel": "property bool blocked; function openActivity() {}",
            "AndroidDownloadsPage": "signal openManager()",
            "AndroidAccountPage": '''Flickable {
                objectName: "accountScroll"; anchors.fill: parent; contentHeight: 1600
                Rectangle { width: parent.width; height: 1600; color: "white" }
                Button { objectName: "accountButton"; x: 40; y: 200; text: "Account action" }
            }''',
            "AndroidSettingsPage": '''property bool tablet: false; property int section: -1
                property var titles: ["Downloads", "Performance"]
                function goBack() { section = -1 }''',
            "AndroidInfoPage": "",
            "SupportedWebsitesPage": "property bool showBackButton: true; signal backRequested()",
            "AndroidMorePage": "signal openActivity(); signal openPage(int index)",
            "DownloadManagerPage": "",
            "CreatorsPage": 'objectName: "creatorsPage"; property bool showBackButton: true; property bool detailOpen: false; function goBack() { if (!detailOpen) return false; detailOpen = false; return true }',
        }
        for name, body in stubs.items():
            (root / f"{name}.qml").write_text("import QtQuick\nimport QtQuick.Controls\nItem { " + body + " }")
        (root / "AppButton.qml").write_text("import QtQuick.Controls\nButton {}")
        (root / "ContrastPopupBackground.qml").write_text("import QtQuick\nItem { property var popup }")
        self.engine = QQmlApplicationEngine()
        self.warnings = []
        self.engine.warnings.connect(lambda errors: self.warnings.extend(e.toString() for e in errors))
        self.context_objects = []
        definitions = {
            "appSettings": '''property int font_size: 12; property bool dark_mode: false
                property string accent_color: "blue"; property bool activity_glow_enabled: false
                property bool reduced_motion: false; property bool anonymous_mode: false
                signal anonymousModeChanged()
                property bool smoke_test: true; property bool setup_completed: true
                property bool update_checks: false; property bool update_prompts: true
                property string service_transport: "direct"''',
            "backend": '''property bool activityActive: false; property string errorReportDisclosure: ""
                signal shutdown_complete(); signal updateAvailable(var details)
                signal updateStatus(string status); signal updateProgress(real current, real total)
                signal updateCheckStarted(); signal updateFinished()
                function initiate_shutdown() {}''',
            "androidDisplay": '''property var outline: []; property bool keyboardNavigation: true
                property bool television: false; property bool carMode: false
                property bool systemNavigation: false; property bool interactionBlocked: false
                property bool restrictionsKnown: true; property bool foreground: true
                property int pauseGeneration: 0
                signal webLinkRequested(string address); signal carStateChanged()''',
            "torStatus": "property string text: ''",
        }
        for name, body in definitions.items():
            component = QQmlComponent(self.engine)
            component.setData(("import QtQuick\nQtObject { " + body + " }").encode(), QUrl())
            obj = component.create()
            self.assertIsNotNone(obj, component.errors())
            obj.setParent(self.engine)
            self.context_objects.append(obj)
            self.engine.rootContext().setContextProperty(name, obj)
        self.engine.rootContext().setContextProperty("applicationLicenseText", "test")
        self.engine.load(QUrl.fromLocalFile(str(root / "AndroidMain.qml")))
        self.assertTrue(self.engine.rootObjects(), self.warnings)
        self.window = self.engine.rootObjects()[0]
        QTest.qWait(50)
        self.device = QTest.createTouchDevice()

    def tearDown(self):
        self.window.setProperty("safeToClose", True)
        self.window.close()
        self.engine.deleteLater()
        _app.processEvents()
        self.directory.cleanup()

    def visual_item(self, name):
        def find(item):
            if item.objectName() == name:
                return item
            for child in item.childItems():
                found = find(child)
                if found is not None:
                    return found
            return None
        return find(self.window.contentItem())

    def back(self):
        QMetaObject.invokeMethod(self.window, "goBack")
        QTest.qWait(10)

    def swipe(self, start, end):
        QTest.touchEvent(self.window, self.device).press(0, QPoint(*start), self.window).commit()
        for part in (.2, .5, .8, 1):
            point = QPoint(round(start[0] + (end[0] - start[0]) * part),
                           round(start[1] + (end[1] - start[1]) * part))
            QTest.touchEvent(self.window, self.device).move(0, point, self.window).commit()
            QTest.qWait(10)
        QTest.touchEvent(self.window, self.device).release(0, QPoint(*end), self.window).commit()
        QTest.qWait(10)

    def test_creator_detail_returns_to_library_before_leaving_page(self):
        self.window.setProperty("pageIndex", 7)
        page = self.window.findChild(QObject, "creatorsPage")
        page.setProperty("detailOpen", True)
        self.back()
        self.assertEqual(self.window.property("pageIndex"), 7)
        self.assertFalse(page.property("detailOpen"))
        self.back()
        self.assertEqual(self.window.property("pageIndex"), 0)

    def test_tv_sidebar_and_web_link_dialog_use_remote_controls(self):
        self.context_objects[2].setProperty("television", True)
        self.window.resize(1280, 720)
        QTest.qWait(60)
        sidebar = self.visual_item("sidebarNavigation-0")
        sidebar.forceActiveFocus(Qt.TabFocusReason)
        QTest.keyClick(self.window, Qt.Key_Down)
        account = self.visual_item("sidebarNavigation-1")
        self.assertTrue(account.hasActiveFocus())
        QTest.keyClick(self.window, Qt.Key_Select)
        QTest.qWait(30)
        self.assertEqual(self.window.property("pageIndex"), 1)
        button = self.window.findChild(QQuickItem, "accountButton")
        self.assertTrue(button.hasActiveFocus())
        self.context_objects[2].webLinkRequested.emit("https://pornfetch.to/")
        QTest.qWait(100)
        dialog = self.window.findChild(QObject, "tvWebLinkDialog")
        self.assertTrue(dialog.property("visible"))
        self.assertEqual(dialog.property("address"), "https://pornfetch.to/")
        QTest.keyClick(self.window, Qt.Key_Back)
        QTest.qWait(350)
        self.assertFalse(dialog.property("visible"))
        self.assertTrue(button.hasActiveFocus())
        self.assertEqual(self.window.property("pageIndex"), 1)
        self.assertEqual(self.warnings, [])

    def test_car_layout_provides_exit_and_defers_to_system_navigation(self):
        display = self.context_objects[2]
        display.setProperty("carMode", True)
        self.window.resize(1080, 600)
        QTest.qWait(50)
        close = self.window.findChild(QQuickItem, "androidCloseButton")
        self.assertTrue(close.isVisible())
        self.window.setProperty("pageIndex", 1)
        QTest.qWait(30)
        back = self.window.findChild(QQuickItem, "androidBackButton")
        self.assertTrue(back.isVisible())
        display.setProperty("systemNavigation", True)
        QTest.qWait(30)
        self.assertFalse(back.isVisible())
        self.assertFalse(close.isVisible())
        self.assertEqual(self.warnings, [])

    def test_vehicle_restrictions_block_the_current_page_and_preserve_history(self):
        display = self.context_objects[2]
        display.setProperty("carMode", True)
        self.window.setProperty("pageIndex", 1)
        QTest.qWait(50)
        button = self.window.findChild(QQuickItem, "accountButton")
        button.forceActiveFocus(Qt.TabFocusReason)
        display.setProperty("interactionBlocked", True)
        display.carStateChanged.emit()
        QTest.qWait(100)
        dialog = self.window.findChild(QObject, "vehicleRestrictionDialog")
        self.assertTrue(dialog.property("visible"))
        self.assertFalse(button.isEnabled())
        QTest.keyClick(self.window, Qt.Key_Back)
        self.assertEqual(self.window.property("pageIndex"), 1)
        self.assertTrue(dialog.property("visible"))
        display.setProperty("interactionBlocked", False)
        display.carStateChanged.emit()
        QTest.qWait(350)
        self.assertFalse(dialog.property("visible"))
        self.assertTrue(button.isEnabled())
        self.assertTrue(button.hasActiveFocus())
        navigator = next(item for item in self.window.findChildren(QObject)
                         if item.metaObject().className().startswith("RemoteNavigation"))
        navigator.setProperty("editingItem", button)
        display.setProperty("pauseGeneration", 1)
        display.carStateChanged.emit()
        self.assertIsNone(navigator.property("editingItem"))
        self.assertEqual(self.warnings, [])

    def test_back_retraces_pages_and_settings_detail(self):
        self.window.setProperty("pageIndex", 1)
        QTest.qWait(10)
        button = self.window.findChild(QQuickItem, "accountButton")
        button.forceActiveFocus()
        self.window.setProperty("pageIndex", 2)
        settings = self.window.findChild(QQuickItem, "androidSettingsPage")
        settings.setProperty("section", 1)
        self.back()
        self.assertEqual(settings.property("section"), -1)
        self.assertEqual(self.window.property("pageIndex"), 2)
        self.back()
        self.assertEqual(self.window.property("pageIndex"), 1)
        self.assertTrue(button.hasActiveFocus())
        back_button = self.window.findChild(QQuickItem, "androidBackButton")
        back_button.forceActiveFocus()
        QTest.keyClick(self.window, Qt.Key_Return)
        self.assertEqual(self.window.property("pageIndex"), 0)
        self.assertFalse(self.window.property("canGoBack"))
        self.assertEqual(self.warnings, [])

    def test_edge_swipes_and_escape_share_back_history(self):
        self.window.setProperty("pageIndex", 1)
        self.window.setProperty("pageIndex", 2)
        self.swipe((390, 400), (240, 400))
        self.assertEqual(self.window.property("pageIndex"), 1)
        self.swipe((10, 400), (160, 400))
        self.assertEqual(self.window.property("pageIndex"), 0)
        self.window.setProperty("pageIndex", 1)
        QTest.keyClick(self.window, Qt.Key_Escape)
        self.assertEqual(self.window.property("pageIndex"), 0)
        self.window.setProperty("pageIndex", 1)
        QTest.keyClick(self.window, Qt.Key_Back)
        self.assertEqual(self.window.property("pageIndex"), 0)
        self.assertEqual(self.warnings, [])

    def test_touch_navigation_does_not_force_control_focus(self):
        self.context_objects[2].setProperty("keyboardNavigation", False)
        self.window.setProperty("pageIndex", 1)
        QTest.qWait(20)
        button = self.window.findChild(QQuickItem, "accountButton")
        self.assertFalse(button.hasActiveFocus())
        back_button = self.window.findChild(QQuickItem, "androidBackButton")
        back_button.forceActiveFocus()
        QTest.keyClick(self.window, Qt.Key_Down)
        self.assertTrue(button.hasActiveFocus())
        self.assertEqual(self.warnings, [])

    def test_short_vertical_and_modal_swipes_do_not_navigate(self):
        self.window.setProperty("pageIndex", 1)
        self.swipe((390, 550), (390, 250))
        scroll = self.window.findChild(QQuickItem, "accountScroll")
        self.assertGreater(scroll.property("contentY"), 0)
        self.assertEqual(self.window.property("pageIndex"), 1)
        self.window.setProperty("pageIndex", 2)
        for start, end in [((390, 400), (350, 400)), ((390, 400), (250, 650)),
                           ((200, 400), (50, 400))]:
            self.swipe(start, end)
            self.assertEqual(self.window.property("pageIndex"), 2)
        dialog = self.window.findChild(QObject, "updateDialog")
        QMetaObject.invokeMethod(dialog, "open")
        QTest.qWait(100)
        self.swipe((390, 400), (240, 400))
        self.assertEqual(self.window.property("pageIndex"), 2)
        self.assertEqual(self.warnings, [])
