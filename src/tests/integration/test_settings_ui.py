from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PySide6.QtCore import QSettings

from src.backend.config import SettingsManager
from src.tests.integration.settings_support import SettingsGUITestBase


class TestUITabGUI(SettingsGUITestBase):
    """Verifies that every change made on the UI settings tab modifies the actual settings file."""

    def test_gui_language_combobox(self) -> None:
        # Index 2: "German"
        self.simulate_combobox("guiLanguageComboBox", 2)
        self.assertEqual(self.settings_manager.language, 2)
        self.assert_file_value("UI/language", 2)

        # Index 4: "French"
        self.simulate_combobox("guiLanguageComboBox", 4)
        self.assertEqual(self.settings_manager.language, 4)
        self.assert_file_value("UI/language", 4)

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


class TestRestartDialogUX(unittest.TestCase):
    """Verifies the UX requirement: the restart-required dialog must only be shown once per session."""

    def test_backend_setting_requires_restart_shown_only_once(self) -> None:
        from main import Backend

        backend = Backend()
        self.assertFalse(backend._restart_warning_shown)

        with patch("src.backend.application.ui_popup") as mock_popup:
            backend.setting_requires_restart()
            self.assertEqual(mock_popup.call_count, 1)
            self.assertTrue(backend._restart_warning_shown)

            # Second trigger in the same session
            backend.setting_requires_restart()
            self.assertEqual(mock_popup.call_count, 1)

            # Third trigger in the same session
            backend.setting_requires_restart()
            self.assertEqual(mock_popup.call_count, 1)

    def test_restart_dialog_triggered_by_multiple_setting_changes_only_once(self) -> None:
        from main import Backend

        with tempfile.TemporaryDirectory() as tmpdir:
            ini_path = Path(tmpdir) / "test_restart.ini"
            qs = QSettings(str(ini_path), QSettings.Format.IniFormat)
            mgr = SettingsManager(qs)

            backend = Backend()
            # Connect manager to backend's slot
            mgr.restartRequired.connect(backend.setting_requires_restart)

        with patch("src.backend.application.ui_popup") as mock_popup:
                # 1st change that requires restart: track_videos
                mgr.track_videos = True
                self.assertEqual(mock_popup.call_count, 1)

                # 2nd change in same session: enable_tor
                mgr.enable_tor = True
                self.assertEqual(mock_popup.call_count, 1)

                # 3rd change in same session: pocketbase_data_path
                mgr.pocketbase_data_path = "/new/pb/dir"
                self.assertEqual(mock_popup.call_count, 1)

                # 4th change in same session: core_style
                mgr.core_style = "Fusion"
                self.assertEqual(mock_popup.call_count, 1)

                # 5th change in same session: set_sni_obfuscation_mode
                mgr.set_sni_obfuscation_mode("strict")
                self.assertEqual(mock_popup.call_count, 1)

