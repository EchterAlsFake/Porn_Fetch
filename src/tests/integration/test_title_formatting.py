"""Exercise live filename highlighting through the real QML editor and backend slot."""

import os
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ["QML_DISABLE_DISK_CACHE"] = "1"

from PySide6.QtCore import QObject, Qt, QUrl, Slot
from PySide6.QtGui import QGuiApplication, QTextCharFormat
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickTextDocument  # noqa: F401
from PySide6.QtTest import QTest

from src.backend.application import Backend


class EditorBackend(QObject):
    def __init__(self):
        super().__init__()
        self._title_highlighters = {}

    @Slot(QObject, bool, bool)
    def highlight_title_format(self, document, dark, high_contrast):
        Backend.highlight_title_format(self, document, dark, high_contrast)


class TitleFormattingTests(unittest.TestCase):
    def test_typing_highlights_tokens_without_changing_the_template(self):
        app = QGuiApplication.instance() or QGuiApplication([])
        backend = EditorBackend()
        engine = QQmlApplicationEngine()
        engine.rootContext().setContextProperty("backend", backend)
        warnings = []
        engine.warnings.connect(lambda messages: warnings.extend(str(e) for e in messages))
        ui = Path(__file__).resolve().parents[2] / "frontend/UI/TitleFixture.qml"
        engine.loadData(b"""import QtQuick
import QtQuick.Controls
ApplicationWindow {
    visible: true; width: 500; height: 220
    TitleFormatField { objectName: "editor"; width: parent.width - 32; x: 16; y: 16 }
}""", QUrl.fromLocalFile(str(ui)))
        self.assertTrue(engine.rootObjects(), warnings)
        window = engine.rootObjects()[0]
        field = window.findChild(QObject, "editor")
        text = "\U0001f600 $title ${author} $$ $unknown $"
        field.setProperty("text", text)
        QTest.qWait(30)
        document = field.property("textDocument").textDocument()
        formats = document.firstBlock().layout().formats()
        self.assertEqual(document.toPlainText(), text)
        # The emoji occupies two UTF-16 units; the first token starts at 3.
        self.assertEqual(formats[0].start, 3)
        errors = [f for f in formats if f.format.underlineStyle() == QTextCharFormat.WaveUnderline]
        self.assertEqual(len(errors), 2)

        window.requestActivate()
        field.forceActiveFocus()
        QTest.keyClick(window, Qt.Key_A, Qt.ControlModifier)
        for character in "$video_id":
            QTest.keyClick(window, character)
        QTest.qWait(30)
        self.assertEqual(document.toPlainText(), "$video_id")
        formats = document.firstBlock().layout().formats()
        self.assertEqual(len(formats), 1)
        self.assertNotEqual(formats[0].format.underlineStyle(), QTextCharFormat.WaveUnderline)
        self.assertEqual(warnings, [])
        window.close()
        from src.backend.qml_lifecycle import destroy_qml_engine
        destroy_qml_engine(engine)
        self.assertFalse(backend._title_highlighters)
