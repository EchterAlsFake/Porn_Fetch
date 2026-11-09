"""Mobile dialog geometry and the Android output-folder setup, without device I/O."""
import tempfile
import unittest
from pathlib import Path

from PySide6.QtCore import Property, QMetaObject, QObject, QSettings, QUrl, Slot
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtTest import QTest

from src.backend.config import SettingsManager
from src.backend.qml_lifecycle import destroy_qml_engine
from src.tests.integration.settings_support import _app  # noqa: F401

UI = Path(__file__).resolve().parents[2] / "frontend/UI"


class FolderBackend(QObject):
    android_shared_downloads_available = Property(bool, lambda self: self.shared_downloads, constant=True)

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.selections = []
        self.shared_downloads = False

    @Slot()
    def use_android_shared_downloads(self):
        if self.shared_downloads:
            self.settings.android_output_folder = "mediastore:Download/Porn Fetch"

    @Slot(str)
    def set_android_output_folder(self, folder):
        self.selections.append(folder)
        self.settings.android_output_folder = (QUrl.fromLocalFile(folder).toString()
                                               if folder.startswith("/") else folder)


class MobileOnboardingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = str(Path(self.temporary.name) / "settings.ini")
        self.settings = SettingsManager(QSettings(self.path, QSettings.IniFormat))
        self.backend = FolderBackend(self.settings)
        self.engine = QQmlApplicationEngine()
        self.addCleanup(lambda: destroy_qml_engine(self.engine))
        self.engine.rootContext().setContextProperty("appSettings", self.settings)
        self.engine.rootContext().setContextProperty("backend", self.backend)
        self.warnings = []
        self.engine.warnings.connect(lambda errors: self.warnings.extend(e.toString() for e in errors))

    def load(self, component):
        self.engine.loadData(f"""
            import QtQuick
            import QtQuick.Controls
            ApplicationWindow {{
                width: 360; height: 640; visible: true
                {component}
                Component.onCompleted: dialog.open()
            }}
        """.encode(), QUrl.fromLocalFile(str(UI / "MobileOnboardingFixture.qml")))
        self.assertTrue(self.engine.rootObjects(), self.warnings)
        QTest.qWait(250)
        return self.engine.rootObjects()[0]

    def test_mobile_message_fills_window_in_both_orientations(self):
        window = self.load("UkraineMessageDialog { id: dialog; settings: appSettings; fullScreen: true }")
        dialog = window.findChild(QObject, "ukraineMessageDialog")
        for width, height in ((360, 640), (640, 360)):
            window.resize(width, height)
            QTest.qWait(50)
            self.assertEqual(dialog.property("width"), width)
            self.assertEqual(dialog.property("height"), height)
            self.assertEqual(dialog.property("x"), 0)
            self.assertEqual(dialog.property("y"), 0)
            self.assertEqual(dialog.property("background").property("radius"), 0)
        self.assertEqual(self.warnings, [])

    def test_folder_setup_survives_cancellation_and_saves_selection(self):
        window = self.load("AndroidOutputSetupDialog { id: dialog; settings: appSettings }")
        dialog = window.findChild(QObject, "androidOutputSetupDialog")
        picker = window.findChild(QObject, "androidSetupFolderPicker")
        QMetaObject.invokeMethod(picker, "open")
        QTest.qWait(100)
        QMetaObject.invokeMethod(picker, "reject")
        self.assertTrue(dialog.property("visible"))
        self.assertEqual(self.backend.selections, [])
        self.assertEqual(self.settings.android_output_folder, "")
        folder = QUrl.fromLocalFile(self.temporary.name)
        QMetaObject.invokeMethod(picker, "open")
        QTest.qWait(100)
        picker.setProperty("currentFolder", folder)
        picker.setProperty("selectedFolder", folder)
        picker.accepted.emit()
        QMetaObject.invokeMethod(picker, "close")
        QTest.qWait(250)
        self.assertFalse(dialog.property("visible"))
        saved = SettingsManager(QSettings(self.path, QSettings.IniFormat))
        self.assertEqual(QUrl(saved.android_output_folder), folder)
        self.assertEqual(len(self.backend.selections), 1)
        self.assertEqual(self.warnings, [])
