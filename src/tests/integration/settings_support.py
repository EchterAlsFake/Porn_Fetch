from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["PORN_FETCH_TEST_ENV"] = "1"

from PySide6.QtCore import Property, QObject, QSettings, QUrl, Signal, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent
from PySide6.QtQuickControls2 import QQuickStyle

from src.backend.config import SettingsManager
from src.frontend.UI import resources

resources.qInitResources()
QQuickStyle.setStyle("Material")

# Ensure singleton QGuiApplication exists
_app = QGuiApplication.instance() or QGuiApplication([])


class _TestBackend(QObject):
    proxyTestSucceeded = Signal(str, dict)
    proxyTestFailed = Signal(str, str)
    proxySslError = Signal(str, str)

    def __init__(self, settings_manager: SettingsManager, bridge: _TestBridge | None = None) -> None:
        super().__init__()
        self.settings = settings_manager
        self.bridge = bridge

    @Property(str, constant=True)
    def errorReportDisclosure(self) -> str:
        return "Test Disclosure"

    @Slot(int)
    def set_default_quality(self, index: int) -> None:
        quality = self.settings.mappings_quality.get(index)
        if quality is None:
            return
        requires_license = index in (0, 1, 3, 4, 5)
        if requires_license and not (self.bridge and self.bridge.isPremium):
            return
        self.settings.quality = index

    @Slot(str, bool)
    def testProxy(self, proxy_url: str, verify_ssl: bool) -> None:
        pass

    @Slot(str, bool)
    def applyProxy(self, proxy_url: str, verify_ssl: bool) -> None:
        self.settings.apply_proxy_settings(proxy_url, verify_ssl)

    @Slot()
    def reset_pornfetch(self) -> None:
        self.settings.reset()

    @Slot()
    def clear_temporary_files(self) -> None:
        pass


class _TestBridge(QObject):
    def __init__(self, premium: bool = True) -> None:
        super().__init__()
        self._is_premium = premium

    @Property(bool, constant=True)
    def isPremium(self) -> bool:
        return self._is_premium

    def set_premium(self, premium: bool) -> None:
        self._is_premium = premium


class SettingsGUITestBase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.ini_path = Path(self.temp_dir.name) / "test_settings.ini"
        self.qsettings = QSettings(str(self.ini_path), QSettings.Format.IniFormat)
        self.settings_manager = SettingsManager(self.qsettings)
        self.bridge = _TestBridge(premium=True)
        self.backend = _TestBackend(self.settings_manager, self.bridge)

        self.engine = QQmlApplicationEngine()
        self.engine.rootContext().setContextProperty("appSettings", self.settings_manager)
        self.engine.rootContext().setContextProperty("backend", self.backend)
        self.engine.rootContext().setContextProperty("bridge", self.bridge)

        ui_dir = Path("src/frontend/UI").resolve()
        self.engine.addImportPath(str(ui_dir))

        qml_path = ui_dir / "SettingsPage.qml"
        self.component = QQmlComponent(self.engine, QUrl.fromLocalFile(str(qml_path)))
        if self.component.isError():
            errors = "\n".join(e.toString() for e in self.component.errors())
            self.fail(f"Failed to load SettingsPage.qml:\n{errors}")

        self.root = self.component.create()
        self.assertIsNotNone(self.root, "SettingsPage root item should not be None")

    def tearDown(self) -> None:
        del self.root
        del self.component
        del self.engine
        del self.backend
        del self.bridge
        del self.settings_manager
        del self.qsettings
        self.temp_dir.cleanup()

    # --- Simulation helpers ---

    def find_control(self, name: str) -> QObject:
        item = self.root.findChild(QObject, name)
        self.assertIsNotNone(item, f"Control with objectName '{name}' not found")
        return item

    def simulate_combobox(self, name: str, index: int) -> None:
        combo = self.find_control(name)
        combo.setProperty("currentIndex", index)
        combo.activated.emit(index)

    def simulate_checkbox(self, name: str, checked: bool) -> None:
        cb = self.find_control(name)
        cb.setProperty("checked", checked)
        cb.toggled.emit()

    def simulate_switch(self, name: str, checked: bool) -> None:
        sw = self.find_control(name)
        sw.setProperty("checked", checked)
        sw.toggled.emit()

    def simulate_spinbox(self, name: str, value: int) -> None:
        sb = self.find_control(name)
        sb.setProperty("value", value)
        sb.valueModified.emit()

    def simulate_decimal_spinbox(self, name: str, value: float) -> None:
        dsb = self.find_control(name)
        factor = float(dsb.property("factor") or 100.0)
        dsb.setProperty("value", int(round(value * factor)))
        dsb.valueModified.emit()

    def simulate_textfield(self, name: str, text: str) -> None:
        tf = self.find_control(name)
        tf.setProperty("text", text)
        tf.editingFinished.emit()

    def simulate_radio(self, name: str) -> None:
        radio = self.find_control(name)
        radio.clicked.emit()

    def simulate_folder_dialog(self, name: str, folder_path: str) -> None:
        dlg = self.find_control(name)
        folder_url = QUrl.fromLocalFile(folder_path)
        dlg.setProperty("currentFolder", folder_url)
        dlg.setProperty("selectedFolder", folder_url)
        dlg.accepted.emit()

    def simulate_proxy_acceptance(self, proxy_url: str, verify_ssl: bool) -> None:
        pw = self.find_control("proxyWindow")
        pw.proxyAccepted.emit(proxy_url, verify_ssl)

    def simulate_reset_button(self) -> None:
        btn = self.find_control("resetSettingsButton")
        btn.clicked.emit()

    def read_fresh_settings(self) -> QSettings:
        self.settings_manager.sync()
        return QSettings(str(self.ini_path), QSettings.Format.IniFormat)

    def assert_file_value(self, key: str, expected_value: object) -> None:
        fresh = self.read_fresh_settings()
        val = fresh.value(key)
        if isinstance(expected_value, bool):
            if isinstance(val, str):
                actual_bool = val.lower() == "true"
            else:
                actual_bool = bool(val)
            self.assertEqual(actual_bool, expected_value, f"File key '{key}' was {val!r}, expected {expected_value!r}")
        elif isinstance(expected_value, int):
            self.assertEqual(int(val), expected_value, f"File key '{key}' was {val!r}, expected {expected_value!r}")
        elif isinstance(expected_value, float):
            self.assertAlmostEqual(float(val), expected_value, places=2, msg=f"File key '{key}' was {val!r}, expected {expected_value!r}")
        else:
            self.assertEqual(str(val), str(expected_value), f"File key '{key}' was {val!r}, expected {expected_value!r}")


