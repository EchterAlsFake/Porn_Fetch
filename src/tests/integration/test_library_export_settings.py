from PySide6.QtCore import QObject, Qt
from PySide6.QtQuick import QQuickWindow
from PySide6.QtTest import QTest

from src.tests.integration.settings_support import SettingsGUITestBase, _app


class LibraryExportSettingsTests(SettingsGUITestBase):
    def test_anonymous_mode_clears_preview_and_hides_file_and_source(self):
        panel = self.find_control("libraryExportSettings")
        reader = self.find_control("metadataPreviewText")
        panel.setProperty("hasPreview", True)
        reader.setProperty("text", "Private metadata preview")
        self.find_control("metadataVideoFile").setProperty("text", "/media/example.mp4")
        self.find_control("metadataSourceUrl").setProperty("text", "https://bellesa.co/videos/123")
        self.settings_manager.anonymous_mode = True
        self.assertEqual(reader.property("text"), "")
        self.assertFalse(panel.property("hasPreview"))
        self.assertFalse(self.find_control("metadataPreviewButton").property("enabled"))
        for name in ("metadataVideoFile", "metadataSourceUrl"):
            control = self.find_control(name)
            self.assertNotEqual(control.property("displayText"), control.property("text"))

    def test_settings_are_saved_and_free_mode_cannot_enable_export(self):
        self.simulate_combobox("metadataExportMode", 1)
        self.assert_file_value("Library/metadata_export", "jellyfin")
        self.simulate_combobox("metadataExportLayout", 1)
        self.assert_file_value("Library/metadata_layout", "scene-folder")
        self.simulate_checkbox("metadataExportGenres", True)
        self.assert_file_value("Library/metadata_genres", True)
        self.simulate_checkbox("metadataExportStudioFallback", True)
        self.assert_file_value("Library/metadata_studio_fallback", True)
        self.simulate_textfield("jellyfinUrl", "http://localhost:8096")
        self.assert_file_value("Library/jellyfin_url", "http://localhost:8096")
        self.bridge.set_premium(False)
        self.simulate_combobox("metadataExportMode", 1)
        self.assertEqual(self.settings_manager.metadata_export, "off")

    def test_dpad_navigation_and_return_activation(self):
        window = QQuickWindow()
        window.resize(1000, 800)
        self.root.setParentItem(window.contentItem())
        self.root.setWidth(1000)
        self.root.setHeight(800)
        window.show()
        window.requestActivate()
        try:
            mode = self.find_control("metadataExportMode")
            layout = self.find_control("metadataExportLayout")
            genres = self.find_control("metadataExportGenres")
            mode.forceActiveFocus()
            _app.processEvents()
            QTest.keyClick(window, Qt.Key.Key_Down)
            help_button = self.find_control("layoutChoiceLibraryHelp")
            self.assertTrue(help_button.hasActiveFocus())
            QTest.keyClick(window, Qt.Key.Key_Return)
            QTest.qWait(250)
            dialog = help_button.findChild(QObject, "helpDialog")
            self.assertTrue(dialog.property("visible"))
            QTest.keyClick(window, Qt.Key.Key_Escape)
            QTest.qWait(250)
            self.assertFalse(dialog.property("visible"))
            self.assertTrue(help_button.hasActiveFocus())
            QTest.keyClick(window, Qt.Key.Key_Down)
            self.assertTrue(layout.hasActiveFocus())
            QTest.keyClick(window, Qt.Key.Key_Down)
            self.assertTrue(self.find_control("genresLibraryHelp").hasActiveFocus())
            QTest.keyClick(window, Qt.Key.Key_Down)
            self.assertTrue(genres.hasActiveFocus())
            QTest.keyClick(window, Qt.Key.Key_Return)
            self.assertTrue(self.settings_manager.metadata_genres)
            self.assert_file_value("Library/metadata_genres", True)
        finally:
            self.root.setParentItem(None)
            window.close()
            window.deleteLater()
