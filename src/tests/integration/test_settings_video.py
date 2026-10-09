from __future__ import annotations

from PySide6.QtCore import QObject

from src.tests.integration.settings_support import SettingsGUITestBase


class TestVideoTabGUI(SettingsGUITestBase):
    """Verifies that every change made on the Video settings tab modifies the actual settings file."""

    def test_quality_combobox_licensed(self) -> None:
        # Index 0 is 'best' (requires license)
        self.simulate_combobox("defaultQualityCombo", 0)
        self.assertEqual(self.settings_manager.quality, 0)
        self.assert_file_value("Video/quality", 0)

        # Index 6 is '720p'
        self.simulate_combobox("defaultQualityCombo", 6)
        self.assertEqual(self.settings_manager.quality, 6)
        self.assert_file_value("Video/quality", 6)

    def test_quality_combobox_unlicensed_enforcement(self) -> None:
        # Unlicensed user attempting premium quality (index 0 'best')
        self.bridge.set_premium(False)
        self.settings_manager.quality = 6
        self.simulate_combobox("defaultQualityCombo", 0)
        # Should stay 6 because premium quality is rejected for unlicensed users
        self.assertEqual(self.settings_manager.quality, 6)
        self.assert_file_value("Video/quality", 6)

        # Unlicensed user selecting non-premium quality (index 8 '480p')
        self.simulate_combobox("defaultQualityCombo", 8)
        self.assertEqual(self.settings_manager.quality, 8)
        self.assert_file_value("Video/quality", 8)

    def test_model_videos_combobox(self) -> None:
        # Index 1: "Uploaded Videos"
        self.simulate_combobox("modelVideosCombo", 1)
        self.assertEqual(self.settings_manager.model_videos, 1)
        self.assert_file_value("Video/model_videos", 1)

        # Index 2: "Featured Videos"
        self.simulate_combobox("modelVideosCombo", 2)
        self.assertEqual(self.settings_manager.model_videos, 2)
        self.assert_file_value("Video/model_videos", 2)

    def test_content_language_combobox(self) -> None:
        # Index 1 is German (de-DE)
        self.simulate_combobox("contentLanguageComboBox", 1)
        self.assertEqual(self.settings_manager.locale, "de-DE")
        self.assert_file_value("Video/locale", "de-DE")

        # Index 5 is French (fr-FR)
        self.simulate_combobox("contentLanguageComboBox", 5)
        self.assertEqual(self.settings_manager.locale, "fr-FR")
        self.assert_file_value("Video/locale", "fr-FR")

    def test_content_language_displays_default_on_startup(self) -> None:
        combo = self.find_control("contentLanguageComboBox")
        self.assertEqual(combo.property("count"), 14)
        self.assertEqual(combo.property("currentIndex"), 2)
        self.assertEqual(combo.property("currentText"), "🇺🇸 English")
        self.assertEqual(combo.property("currentValue"), "en-US")

    def test_content_language_displays_saved_locale_on_startup(self) -> None:
        self.settings_manager.locale = "de-DE"
        page = self.component.create()
        self.assertIsNotNone(page)
        try:
            combo = page.findChild(QObject, "contentLanguageComboBox")
            self.assertIsNotNone(combo)
            self.assertEqual(combo.property("currentText"), "🇩🇪 Deutsch")
            self.assertEqual(combo.property("currentValue"), "de-DE")
            self.assertEqual(self.settings_manager.locale, "de-DE")
        finally:
            page.deleteLater()

    def test_strict_enforcement_checkbox(self) -> None:
        self.simulate_checkbox("strictEnforcementCheckBox", True)
        self.assertTrue(self.settings_manager.strict_enforcement)
        self.assert_file_value("Video/strict_enforcement", True)

        self.simulate_checkbox("strictEnforcementCheckBox", False)
        self.assertFalse(self.settings_manager.strict_enforcement)
        self.assert_file_value("Video/strict_enforcement", False)

    def test_result_limit_spinbox(self) -> None:
        self.simulate_spinbox("resultLimitSpinBox", 120)
        self.assertEqual(self.settings_manager.result_limit, 120)
        self.assert_file_value("Video/result_limit", 120)

    def test_output_path_textfield(self) -> None:
        test_path = "/media/test_downloads"
        self.simulate_textfield("outputPathInput", test_path)
        self.assertEqual(self.settings_manager.output_path, test_path)
        self.assert_file_value("Video/output_path", test_path)

    def test_output_folder_dialog(self) -> None:
        test_path = "/home/user/Videos/PornFetch"
        self.simulate_folder_dialog("outputFolderDialog", test_path)
        self.assertEqual(self.settings_manager.output_path, test_path)
        self.assert_file_value("Video/output_path", test_path)

    def test_write_metadata_checkbox(self) -> None:
        self.simulate_checkbox("writeMetadataCheckBox", False)
        self.assertFalse(self.settings_manager.write_metadata)
        self.assert_file_value("Video/write_metadata", False)

        self.simulate_checkbox("writeMetadataCheckBox", True)
        self.assertTrue(self.settings_manager.write_metadata)
        self.assert_file_value("Video/write_metadata", True)

    def test_skip_existing_files_checkbox(self) -> None:
        self.simulate_checkbox("skipExistingFilesCheckBox", False)
        self.assertFalse(self.settings_manager.skip_existing_files)
        self.assert_file_value("Video/skip_existing_files", False)

        self.simulate_checkbox("skipExistingFilesCheckBox", True)
        self.assertTrue(self.settings_manager.skip_existing_files)
        self.assert_file_value("Video/skip_existing_files", True)

    def test_track_videos_checkbox(self) -> None:
        self.simulate_checkbox("trackVideosCheckBox", True)
        self.assertTrue(self.settings_manager.track_videos)
        self.assert_file_value("Video/track_videos", True)

        self.simulate_checkbox("trackVideosCheckBox", False)
        self.assertFalse(self.settings_manager.track_videos)
        self.assert_file_value("Video/track_videos", False)

    def test_pocketbase_data_path_textfield(self) -> None:
        test_path = "/var/lib/pocketbase_custom"
        self.simulate_textfield("databasePathInput", test_path)
        self.assertEqual(self.settings_manager.pocketbase_data_path, test_path)
        self.assert_file_value("Video/pocketbase_data_path", test_path)

    def test_pocketbase_folder_dialog(self) -> None:
        test_path = "/opt/pocketbase_store"
        self.simulate_folder_dialog("pocketbaseFolderDialog", test_path)
        self.assertEqual(self.settings_manager.pocketbase_data_path, test_path)
        self.assert_file_value("Video/pocketbase_data_path", test_path)

