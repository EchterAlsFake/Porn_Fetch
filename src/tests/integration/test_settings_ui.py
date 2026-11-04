from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtTest import QSignalSpy

from src.backend.config import SettingsManager
from src.tests.integration.settings_support import SettingsGUITestBase


class TestUITabGUI(SettingsGUITestBase):
    """Verifies that every change made on the UI settings tab modifies the actual settings file."""

    def test_gui_language_is_english_only(self) -> None:
        control = self.find_control("guiLanguageComboBox")
        self.assertFalse(control.property("enabled"))
        self.assertEqual(control.property("currentText"), "English")

    def test_font_size_spinbox(self) -> None:
        self.simulate_spinbox("fontSizeSpinBox", 16)
        self.assertEqual(self.settings_manager.font_size, 16)
        self.assert_file_value("UI/font_size", 16)

    def test_core_style_combobox(self) -> None:
        # Index 1: "Fusion"
        self.simulate_combobox("coreStyleComboBox", 1)
        self.assertEqual(self.settings_manager.core_style, "Fusion")
        self.assert_file_value("UI/core_style", "Fusion")

        # Index 2: "Universal"
        self.simulate_combobox("coreStyleComboBox", 2)
        self.assertEqual(self.settings_manager.core_style, "Universal")
        self.assert_file_value("UI/core_style", "Universal")

    def test_dark_mode_switch(self) -> None:
        self.simulate_switch("darkModeSwitch", False)
        self.assertFalse(self.settings_manager.dark_mode)
        self.assert_file_value("UI/dark_mode", False)

        self.simulate_switch("darkModeSwitch", True)
        self.assertTrue(self.settings_manager.dark_mode)
        self.assert_file_value("UI/dark_mode", True)

    def test_activity_glow_switch_persists(self) -> None:
        self.assertTrue(self.settings_manager.activity_glow_enabled)
        self.simulate_switch("activityGlowSwitch", False)
        self.assertFalse(self.settings_manager.activity_glow_enabled)
        self.assert_file_value("UI/activity_glow_enabled", False)
        restored = SettingsManager(self.read_fresh_settings())
        self.assertFalse(restored.activity_glow_enabled)

        self.simulate_switch("activityGlowSwitch", True)
        self.assertTrue(self.settings_manager.activity_glow_enabled)
        self.assert_file_value("UI/activity_glow_enabled", True)

    def test_accent_color_combobox(self) -> None:
        # Index 1: "#f44336" (Red)
        self.simulate_combobox("accentColorComboBox", 1)
        self.assertEqual(self.settings_manager.accent_color, "#f44336")
        self.assert_file_value("UI/accent_color", "#f44336")

        # Index 2: "#4caf50" (Green)
        self.simulate_combobox("accentColorComboBox", 2)
        self.assertEqual(self.settings_manager.accent_color, "#4caf50")
        self.assert_file_value("UI/accent_color", "#4caf50")


class TestResetSettingsGUI(SettingsGUITestBase):
    """Verifies that clicking the Reset button clears and resets settings back to defaults."""

    def test_reset_settings_button(self) -> None:
        # Change multiple settings
        self.simulate_spinbox("fontSizeSpinBox", 22)
        self.simulate_spinbox("resultLimitSpinBox", 999)
        self.simulate_textfield("httpVersionInput", "v3")

        self.assert_file_value("UI/font_size", 22)
        self.assert_file_value("Video/result_limit", 999)
        self.assert_file_value("Misc/http_version", "v3")

        # Click reset button
        self.simulate_reset_button()

        # Check that settings manager and file reverted to defaults
        fresh = self.read_fresh_settings()
        self.assertEqual(fresh.allKeys(), [])
        self.assertEqual(self.settings_manager.font_size, 12)
        self.assertEqual(self.settings_manager.result_limit, 50)
        self.assertEqual(self.settings_manager.http_version, "v2")


class TestRestartNotificationUX(unittest.TestCase):
    """Restart feedback stays visible and is announced only once per session."""

    def test_backend_setting_requires_restart_shown_only_once(self) -> None:
        from main import Backend

        backend = Backend()
        announcements = QSignalSpy(backend.notifications.announced)
        self.assertFalse(backend.notifications.restartRequired)

        for _ in range(3):
            backend.setting_requires_restart()
            self.assertTrue(backend.notifications.restartRequired)
            self.assertEqual(announcements.count(), 1)

    def test_restart_notification_from_multiple_setting_changes_only_once(self) -> None:
        from main import Backend

        with tempfile.TemporaryDirectory() as tmpdir:
            ini_path = Path(tmpdir) / "test_restart.ini"
            qs = QSettings(str(ini_path), QSettings.Format.IniFormat)
            mgr = SettingsManager(qs)
            backend = Backend()
            announcements = QSignalSpy(backend.notifications.announced)
            mgr.restartRequired.connect(backend.setting_requires_restart)

            mgr.track_videos = True
            self.assertTrue(backend.notifications.restartRequired)
            self.assertEqual(announcements.count(), 1)

            mgr.enable_tor = True
            mgr.pocketbase_data_path = "/new/pb/dir"
            mgr.core_style = "Fusion"
            mgr.set_sni_obfuscation_mode("strict")
            self.assertTrue(backend.notifications.restartRequired)
            self.assertEqual(announcements.count(), 1)
            qs.sync()
