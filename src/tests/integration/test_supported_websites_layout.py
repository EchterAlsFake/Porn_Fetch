"""The catalog's size hint must not depend on its responsive layout width."""
import os
import subprocess
import sys
import unittest
from pathlib import Path


class SupportedWebsitesLayoutTests(unittest.TestCase):
    def test_responsive_page_has_stable_size_hint_across_desktop_styles(self):
        script = r'''
import sys
from pathlib import Path
from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QQmlPropertyMap
from PySide6.QtQuick import QQuickItem
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtTest import QTest
from src.backend.qml_lifecycle import destroy_qml_engine
from src.shared.supported_websites import supported_websites

QQuickStyle.setStyle(sys.argv[1])
app = QGuiApplication([])
engine = QQmlApplicationEngine()
warnings = []
engine.warnings.connect(lambda errors: warnings.extend(e.toString() for e in errors))
settings, backend = QQmlPropertyMap(), QQmlPropertyMap()
settings.insert('font_size', 12)
backend.insert('supportedWebsites', supported_websites())
engine.rootContext().setContextProperty('appSettings', settings)
engine.rootContext().setContextProperty('backend', backend)
ui = Path('src/frontend/UI').resolve()
engine.loadData(b"""import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
ApplicationWindow {
    visible: true; width: 1280; height: 800
    StackLayout {
        anchors.fill: parent
        currentIndex: 0
        Item {}
        SupportedWebsitesPage {}
    }
}""", QUrl.fromLocalFile(str(ui / 'SupportedWebsitesLayoutTest.qml')))
assert engine.rootObjects(), warnings
window = engine.rootObjects()[0]
page = window.findChild(QQuickItem, 'supportedWebsitesPage')
hint = page.implicitWidth()
def visual_items(item):
    yield item
    for child in item.childItems():
        yield from visual_items(child)
try:
    for font_size in (12, 20):
        settings.insert('font_size', font_size)
        for width in (320, 599, 600, 1280):
            window.resize(width, 800)
            page.parentItem().setProperty('currentIndex', 1)
            QTest.qWait(30)
            assert page.width() == width, (page.width(), width)
            assert page.implicitWidth() == hint, (hint, page.implicitWidth(), width)
            assert any(item.objectName() == 'websiteCard-pornhub' for item in visual_items(page))
            page.parentItem().setProperty('currentIndex', 0)
    assert not warnings, warnings
finally:
    window.close()
    destroy_qml_engine(engine)
'''
        root = Path(__file__).resolve().parents[3]
        env = dict(os.environ, QT_QPA_PLATFORM="offscreen", QT_QUICK_BACKEND="software",
                   QML_DISABLE_DISK_CACHE="1")
        for style in ("Material", "Fusion", "Universal"):
            with self.subTest(style=style):
                result = subprocess.run([sys.executable, "-c", script, style], cwd=root, env=env,
                                        capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
