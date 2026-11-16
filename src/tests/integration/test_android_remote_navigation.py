"""Remote-only navigation through real download controls and representative Qt popups."""
import os
from pathlib import Path
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QUICK_BACKEND", "software")
os.environ["QML_DISABLE_DISK_CACHE"] = "1"

from PySide6.QtCore import QObject, QMetaObject, Qt, QUrl
from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent
from PySide6.QtQuick import QQuickItem
from PySide6.QtTest import QTest
from src.tests.integration import test_android_download_layout as downloads
from src.backend.android_display import AndroidDisplay

UI = Path(__file__).resolve().parents[2] / "frontend/UI"


class CarControlLayoutTests(unittest.TestCase):
    def test_shared_controls_have_large_car_touch_targets(self):
        engine = QQmlApplicationEngine()
        warnings = []
        engine.warnings.connect(lambda errors: warnings.extend(str(error) for error in errors))
        component = QQmlComponent(engine)
        component.setData(b'import QtQuick\nQtObject { property bool carMode: true }', QUrl())
        display = component.create()
        self.assertIsNotNone(display)
        display.setParent(engine)
        engine.rootContext().setContextProperty("androidDisplay", display)
        engine.loadData(b'''import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
ApplicationWindow {
 visible:true; width:600; height:900
 ColumnLayout {
  anchors.fill:parent; anchors.margins:24
  AppButton { objectName:"button"; text:"Action"; Layout.fillWidth:true }
  AppTextField { objectName:"field"; Layout.fillWidth:true }
  AppComboBox { objectName:"combo"; model:["One","Two"]; Layout.fillWidth:true }
  AppSpinBox { objectName:"number"; Layout.fillWidth:true }
  Item { Layout.fillHeight:true }
 }
}''', QUrl.fromLocalFile(str(UI / "CarControlLayoutTest.qml")))
        self.assertTrue(engine.rootObjects(), warnings)
        window = engine.rootObjects()[0]
        try:
            for width, height in [(600, 900), (1920, 480)]:
                window.resize(width, height)
                QTest.qWait(50)
                for name in ("button", "field", "combo", "number"):
                    control = window.findChild(QQuickItem, name)
                    self.assertGreaterEqual(control.height(), 64, name)
                    self.assertLessEqual(control.width(), width - 48, name)
            self.assertEqual(warnings, [])
        finally:
            window.close()
            engine.deleteLater()
            downloads._app.processEvents()


class DownloadRemoteTests(downloads.AndroidDownloadLayoutTests):
    def setUp(self):
        original = downloads.HARNESS
        downloads.HARNESS = original.replace("ApplicationWindow {", """ApplicationWindow {
 id: remoteWindow
 readonly property var remoteNavigation: navigator
 RemoteNavigation { id: navigator; targetWindow: remoteWindow; automaticFocus: true }
""")
        try:
            super().setUp()
        finally:
            downloads.HARNESS = original
        QTest.qWait(60)

    def key(self, key):
        QTest.keyClick(self.window, key)
        QTest.qWait(30)

    def test_toolbar_drawer_and_back_restore_focus(self):
        manager = self.window.findChild(QQuickItem, "openDownloadManagerButton")
        manager.forceActiveFocus(Qt.TabFocusReason)
        self.key(Qt.Key_Right)
        opener = self.window.activeFocusItem()
        self.assertEqual(opener.property("text"), "Add videos")
        self.key(Qt.Key_Enter)
        drawer = self.window.findChild(QObject, "mobileAddSheet")
        self.assertTrue(drawer.property("visible"))
        first = self.window.activeFocusItem()
        self.assertIsNot(first, opener)
        for _ in range(6):
            self.key(Qt.Key_Down)
            self.assertIsNot(self.window.activeFocusItem(), manager)
            self.assertIsNot(self.window.activeFocusItem(), opener)
        self.key(Qt.Key_Back)
        QTest.qWait(350)
        self.assertFalse(drawer.property("visible"))
        self.assertTrue(opener.hasActiveFocus())
        self.assertEqual(self.warnings, [])

    def test_queue_actions_receive_directional_focus_and_scroll(self):
        manager = self.window.findChild(QQuickItem, "openDownloadManagerButton")
        manager.forceActiveFocus(Qt.TabFocusReason)
        for _ in range(20):
            self.key(Qt.Key_Down)
        self.assertGreater(self.queue.property("contentY"), 0)
        focused = self.window.activeFocusItem()
        self.assertTrue(focused.property("activeFocusOnTab"))
        outline = next((item for item in downloads.visual_items(focused) if item.objectName() == "remoteFocusOutline"), None)
        self.assertIsNotNone(outline)
        self.assertTrue(outline.isVisible())
        self.assertEqual(self.warnings, [])

    def test_title_format_center_edits_and_back_finishes_before_closing_drawer(self):
        opener = next(item for item in downloads.visual_items(self.page) if item.property("text") == "Add videos")
        opener.forceActiveFocus(Qt.TabFocusReason)
        self.key(Qt.Key_Enter)
        self.page.setProperty("showFilters", True)
        QTest.qWait(30)
        drawer = self.window.findChild(QObject, "mobileAddSheet")
        # Drawers live in the window overlay, outside the page's visual children.
        field = next(item for item in downloads.visual_items(self.window.contentItem())
                     if item.property("placeholderText") == "$title")
        field.forceActiveFocus(Qt.TabFocusReason)
        self.key(Qt.Key_Enter)
        self.key(Qt.Key_A)
        self.assertIn("a", field.property("text"))
        self.key(Qt.Key_Back)
        self.assertTrue(drawer.property("visible"))
        self.key(Qt.Key_Back)
        QTest.qWait(350)
        self.assertFalse(drawer.property("visible"))
        self.assertEqual(self.warnings, [])


class RemoteControlTests(unittest.TestCase):
    def setUp(self):
        self.engine = QQmlApplicationEngine()
        self.warnings = []
        self.engine.warnings.connect(lambda errors: self.warnings.extend(e.toString() for e in errors))
        self.engine.loadData(b'''import QtQuick
import QtQuick.Controls
ApplicationWindow {
 id: win; width: 900; height: 640; visible: true
 readonly property var remoteNavigation: navigator
 readonly property bool choicesOpen: choices.popup.visible
 RemoteNavigation { id: navigator; targetWindow: win; automaticFocus: true }
 Button { objectName: "opener"; x:20; y:20; text:"Open"; onClicked: dialog.open() }
 Button { objectName: "disabled"; x:140; y:20; text:"Disabled"; enabled:false }
 Button { objectName: "hidden"; x:240; y:20; text:"Hidden"; visible:false }
 CheckBox { objectName: "check"; x:340; y:20; text:"Check" }
 AppTextField { objectName: "editor"; x:20; y:80; width:250; text:"abc" }
 AppComboBox { id: choices; objectName: "choices"; x:20; y:140; width:250; model:["A","B","C"] }
 Button { objectName: "afterChoices"; x:20; y:200; text:"After choices" }
 TextArea { objectName:"multiline"; x:20; y:260; width:280; height:70; text:"Editable text" }
 ScrollView {
  x:20; y:350; width:280; height:250; contentWidth:availableWidth
  TextArea { objectName:"reader"; readOnly:true; text:"A long document\\n".repeat(100); wrapMode:TextEdit.Wrap }
 }
 AppSpinBox { objectName:"number"; x:760; y:100; width:120; editable:true; from:0; to:100; value:10 }
 Slider { objectName:"slider"; x:760; y:200; width:120; from:0; to:100; stepSize:1; value:50 }
 Button { objectName:"afterSlider"; x:760; y:280; text:"After slider" }
 ListView {
  objectName:"longList"; x:340; y:100; width:400; height:420; clip:true
  model:80; spacing:4; keyNavigationEnabled:false
  delegate: Button {
   required property int index
   objectName:"row" + index; text: "Row " + index; width:380; height:50
  }
 }
 Dialog {
  id:dialog; objectName:"dialog"; parent:Overlay.overlay
  x:100; y:100; width:500; height:400; modal:true; focus:true
  standardButtons:Dialog.Close
  contentItem: Column {
   Button { objectName:"nestedOpener"; text:"Nested"; onClicked:nested.open() }
   Button { objectName:"dialogAction"; text:"Action" }
  }
  Dialog {
   id:nested; objectName:"nested"; parent:Overlay.overlay
   x:200;y:150;width:300;height:200;modal:true;focus:true
   standardButtons: Dialog.Close
  }
 }
}''', QUrl.fromLocalFile(str(UI / "RemoteControlTest.qml")))
        self.assertTrue(self.engine.rootObjects(), self.warnings)
        self.window = self.engine.rootObjects()[0]
        self.key_dispatcher = AndroidDisplay()
        navigator = next(item for item in self.window.findChildren(QObject)
                         if item.metaObject().className().startswith("RemoteNavigation"))
        navigator.navigationKeyRequested.connect(lambda key: self.key_dispatcher.sendNavigationKey(self.window, key))
        QTest.qWait(60)

    def tearDown(self):
        self.window.close()
        self.engine.deleteLater()
        downloads._app.processEvents()

    def item(self, name):
        return next((item for item in downloads.visual_items(self.window.contentItem()) if item.objectName() == name), None)

    def key(self, key):
        QTest.keyClick(self.window, key)
        QTest.qWait(30)

    def test_disabled_controls_skipped_and_center_toggles_once(self):
        self.item("opener").forceActiveFocus(Qt.TabFocusReason)
        self.key(Qt.Key_Right)
        self.assertTrue(self.item("check").hasActiveFocus())
        self.key(Qt.Key_Select)
        self.assertTrue(self.item("check").property("checked"))
        self.key(Qt.Key_Return)
        self.assertFalse(self.item("check").property("checked"))
        self.assertEqual(self.warnings, [])

    def test_text_editing_and_closed_combo_navigation(self):
        editor = self.item("editor")
        editor.forceActiveFocus(Qt.TabFocusReason)
        editor.setProperty("cursorPosition", 3)
        self.key(Qt.Key_Select)
        self.key(Qt.Key_Left)
        self.assertTrue(editor.hasActiveFocus())
        self.assertEqual(editor.property("cursorPosition"), 2)
        self.key(Qt.Key_Back)
        self.key(Qt.Key_Down)
        self.assertTrue(self.item("choices").hasActiveFocus())
        self.key(Qt.Key_Down)
        self.assertTrue(self.item("afterChoices").hasActiveFocus())
        self.assertEqual(self.item("choices").property("currentIndex"), 0)
        self.assertEqual(self.warnings, [])

    def test_combo_popup_selection_and_back(self):
        combo = self.item("choices")
        combo.forceActiveFocus(Qt.TabFocusReason)
        self.key(Qt.Key_Select)
        self.assertTrue(self.window.property("choicesOpen"))
        self.key(Qt.Key_Down)
        self.key(Qt.Key_Enter)
        self.assertEqual(combo.property("currentIndex"), 1)
        self.key(Qt.Key_Select)
        self.key(Qt.Key_Back)
        QTest.qWait(350)
        self.assertFalse(self.window.property("choicesOpen"))
        self.assertTrue(combo.hasActiveFocus())
        self.assertEqual(combo.property("currentIndex"), 1)
        self.assertEqual(self.warnings, [])

    def test_multiline_field_and_document_reader_do_not_trap_focus(self):
        field = self.item("multiline")
        field.forceActiveFocus(Qt.TabFocusReason)
        self.key(Qt.Key_Down)
        reader = self.item("reader")
        self.assertTrue(reader.hasActiveFocus())
        scroll = reader.parentItem()
        while scroll is not None and scroll.property("contentY") is None:
            scroll = scroll.parentItem()
        self.assertIsNotNone(scroll)
        before = scroll.property("contentY")
        self.key(Qt.Key_Down)
        self.assertGreater(scroll.property("contentY"), before)
        self.assertTrue(reader.hasActiveFocus())
        self.key(Qt.Key_Right)
        self.assertFalse(reader.hasActiveFocus())
        self.assertEqual(self.warnings, [])

    def test_spinbox_and_slider_adjust_only_after_center_activation(self):
        number = self.item("number")
        slider = self.item("slider")
        number.forceActiveFocus(Qt.TabFocusReason)
        self.key(Qt.Key_Select)
        self.key(Qt.Key_Up)
        self.assertEqual(number.property("value"), 11)
        self.key(Qt.Key_Back)
        self.key(Qt.Key_Down)
        self.assertTrue(slider.hasActiveFocus())
        self.key(Qt.Key_Select)
        self.key(Qt.Key_Right)
        self.assertEqual(slider.property("value"), 51)
        self.key(Qt.Key_Back)
        self.key(Qt.Key_Down)
        self.assertTrue(self.item("afterSlider").hasActiveFocus())
        self.assertEqual(self.warnings, [])

    def test_rotary_commands_traverse_controls_and_adjust_values(self):
        self.item("opener").forceActiveFocus(Qt.TabFocusReason)
        self.key(Qt.Key_F11)
        self.assertTrue(self.item("check").hasActiveFocus())
        self.key(Qt.Key_F12)
        self.assertTrue(self.item("opener").hasActiveFocus())
        slider = self.item("slider")
        slider.forceActiveFocus(Qt.TabFocusReason)
        self.key(Qt.Key_Select)
        self.key(Qt.Key_F11)
        self.assertEqual(slider.property("value"), 51)
        self.key(Qt.Key_F12)
        self.assertEqual(slider.property("value"), 50)
        self.key(Qt.Key_Back)
        self.key(Qt.Key_F11)
        self.assertTrue(self.item("afterSlider").hasActiveFocus())
        self.assertEqual(self.warnings, [])

    def test_rotary_selects_choices_without_leaving_the_open_popup(self):
        combo = self.item("choices")
        combo.forceActiveFocus(Qt.TabFocusReason)
        self.key(Qt.Key_Select)
        self.assertTrue(self.window.property("choicesOpen"))
        self.key(Qt.Key_F11)
        self.assertTrue(self.window.property("choicesOpen"))
        self.assertFalse(self.item("afterChoices").hasActiveFocus())
        self.key(Qt.Key_Enter)
        self.assertEqual(combo.property("currentIndex"), 1)
        self.assertEqual(self.warnings, [])

    def test_rotary_commands_scroll_lazy_rows_without_leaving_the_list(self):
        self.item("row0").forceActiveFocus(Qt.TabFocusReason)
        for _ in range(20):
            self.key(Qt.Key_F11)
        self.assertTrue(self.window.activeFocusItem().objectName().startswith("row"))
        self.assertGreater(self.item("longList").property("contentY"), 0)
        self.assertEqual(self.warnings, [])

    def test_nested_popups_trap_arrows_and_restore_each_opener(self):
        self.item("opener").forceActiveFocus(Qt.TabFocusReason)
        self.key(Qt.Key_Return)
        dialog = self.window.findChild(QObject, "dialog")
        self.assertTrue(dialog.property("visible"))
        opener = self.item("nestedOpener")
        opener.forceActiveFocus(Qt.TabFocusReason)
        self.key(Qt.Key_Enter)
        nested = self.window.findChild(QObject, "nested")
        self.assertTrue(nested.property("visible"))
        for key in (Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right):
            self.key(key)
            self.assertFalse(self.item("check").hasActiveFocus())
        self.key(Qt.Key_Back)
        QTest.qWait(350)
        self.assertFalse(nested.property("visible"))
        self.assertTrue(opener.hasActiveFocus())
        self.key(Qt.Key_Back)
        QTest.qWait(350)
        self.assertFalse(dialog.property("visible"))
        self.assertTrue(self.item("opener").hasActiveFocus())
        self.assertEqual(self.warnings, [])

    def test_lazy_list_reaches_last_row_and_scrolls_back(self):
        first = self.item("row0")
        self.assertIsNotNone(first)
        first.forceActiveFocus(Qt.TabFocusReason)
        for _ in range(85):
            self.key(Qt.Key_Down)
        self.assertEqual(self.window.activeFocusItem().objectName(), "row79")
        listing = self.item("longList")
        focused = self.window.activeFocusItem()
        point = focused.mapToItem(listing, 0, 0)
        self.assertGreaterEqual(point.y(), 0)
        self.assertLessEqual(point.y() + focused.height(), listing.height())
        for _ in range(79):
            self.key(Qt.Key_Up)
        self.assertEqual(self.window.activeFocusItem().objectName(), "row0")
        self.assertEqual(self.warnings, [])
