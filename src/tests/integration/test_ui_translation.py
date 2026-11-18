"""Offline GUI language compatibility and live translation contracts."""
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PySide6.QtCore import QCoreApplication, QFile, QLocale, QObject, QSettings, QTranslator, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from src.backend.config import SettingsManager
from src.backend.ui_languages import catalog_for_locale
from src.backend.ui_translation import UiTranslation
from src.frontend.UI import resources  # noqa: F401


class TranslationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QGuiApplication.instance() or QGuiApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = QSettings(str(Path(self.temp.name) / "settings.ini"), QSettings.Format.IniFormat)
        self.settings = SettingsManager(self.store)
        self.previous_locale = QLocale()
        self.previous_direction = self.app.layoutDirection()

    def tearDown(self):
        QLocale.setDefault(self.previous_locale)
        self.app.setLayoutDirection(self.previous_direction)
        self.temp.cleanup()

    def test_legacy_preferences_migrate_and_locale_survives_restart(self):
        self.store.setValue("UI/language", 2)
        self.assertEqual(self.settings.language, 2)
        self.assertEqual(self.store.value("UI/language_locale"), "de_DE")
        self.settings.language = 5
        self.assertEqual(SettingsManager(self.store).language, 5)
        self.assertEqual(self.store.value("UI/language_locale"), "it")

    def test_region_matching(self):
        self.assertEqual(catalog_for_locale("de_AT"), "de_DE")
        self.assertEqual(catalog_for_locale("es_MX"), "es")
        self.assertEqual(catalog_for_locale("hi"), "hi_IN")
        self.assertEqual(catalog_for_locale("zh_Hans_SG"), "zh_CN")
        self.assertIsNone(catalog_for_locale("zh_TW"))
        self.assertIsNone(catalog_for_locale("zh_Hant_HK"))

    def _load_translated_gui(self):
        engine = QQmlApplicationEngine()
        translation = UiTranslation(self.settings, engine)
        engine.rootContext().setContextProperty("appSettings", self.settings)
        engine.rootContext().setContextProperty("uiTranslation", translation)
        ui = Path(__file__).resolve().parents[2] / "frontend/UI"
        engine.loadData(b'''import QtQuick
Item {
    GuiLanguageSelector {}
    property string label: qsTranslate("DownloadsPage", "Get Video")
    property string missing: qsTranslate("DownloadsPage", "Untranslated fixture")
}''', QUrl.fromLocalFile(str(ui / 'TranslationFixture.qml')))
        return engine, translation

    def test_language_change_is_applied_on_restart_with_english_fallback(self):
        language_path = ":/translations/de_DE.qm"
        if not QFile.exists(language_path):
            language_path = ":/translations/drafts/de_DE.qm"
        catalog = QTranslator()
        self.assertTrue(catalog.load(language_path))
        expected = catalog.translate("DownloadsPage", "Get Video") or "Get Video"
        self.settings.language = 1
        with patch.dict(os.environ, {"PORN_FETCH_PREVIEW_TRANSLATIONS": "1"}):
            engine, translation = self._load_translated_gui()
            self.assertEqual(engine.rootObjects()[0].property("label"), "Get Video")
            item = engine.rootObjects()[0]
            picker = item.findChild(QObject, "guiLanguageComboBox")
            self.assertTrue(picker.property("enabled"))
            self.assertEqual(picker.property("currentText"), "English")
            position = next(i for i, option in enumerate(translation.languages) if option["index"] == 2)
            picker.setProperty("currentIndex", position)
            picker.activated.emit(position)
            self.assertEqual(self.settings.language, 2)
            self.assertEqual(translation.startupPreference, 1)
            self.assertEqual(engine.uiLanguage(), "en_US")
            self.assertEqual(engine.rootObjects()[0].property("label"), "Get Video")

            restarted, translated = self._load_translated_gui()
            self.assertTrue(translated.catalog_loaded)
            self.assertEqual(translated.startupPreference, 2)
            self.assertEqual(restarted.uiLanguage(), "de_DE")
            root = restarted.rootObjects()[0]
            self.assertEqual(root.property("label"), expected)
            self.assertEqual(root.property("missing"), "Untranslated fixture")

    def test_partial_catalog_requires_preview_and_english_plural_is_available(self):
        self.settings.language = 2
        with patch.dict(os.environ, {"PORN_FETCH_PREVIEW_TRANSLATIONS": "0"}):
            engine, translation = self._load_translated_gui()
            released = QFile.exists(":/translations/de_DE.qm")
            self.assertEqual(translation.catalog_loaded, released)
            self.assertIn(2 if released else 1, [option["index"] for option in translation.languages])
            if not released:
                self.assertNotIn(2, [option["index"] for option in translation.languages])
                self.assertEqual(engine.uiLanguage(), "en_US")
                self.assertEqual(QCoreApplication.translate("CreatorsPage", "%n video(s) found", None, 1),
                                 "1 video found")
                self.assertEqual(QCoreApplication.translate("CreatorsPage", "%n video(s) found", None, 2),
                                 "2 videos found")

    def test_accessibility_preferences_persist(self):
        self.settings.reduced_motion = True
        self.settings.high_contrast = True
        reloaded = SettingsManager(self.store)
        self.assertTrue(reloaded.reduced_motion)
        self.assertTrue(reloaded.high_contrast)

    def test_help_button_exposes_action_and_touch_target(self):
        from PySide6.QtCore import QObject
        from PySide6.QtGui import QAccessible, QAccessibleActionInterface

        engine = QQmlApplicationEngine()
        engine.rootContext().setContextProperty("appSettings", self.settings)
        ui = Path(__file__).resolve().parents[2] / "frontend/UI"
        engine.loadData(b'import QtQuick\nimport QtQuick.Controls\nApplicationWindow { visible: true; width: 640; height: 480; HelpButton { objectName: "help"; helpText: "Accessible help fixture" } }', QUrl.fromLocalFile(str(ui / "AccessibilityFixture.qml")))
        self.app.processEvents()
        window = engine.rootObjects()[0]
        button = window.findChild(QObject, "help")
        self.assertIsNotNone(button)
        self.assertGreaterEqual(button.property("implicitHeight"), 48)
        self.assertGreaterEqual(button.property("implicitWidth"), 48)
        interface = QAccessible.queryAccessibleInterface(button)
        self.assertIsNotNone(interface)
        self.assertEqual(interface.text(QAccessible.Text.Name), "Help")
        action = interface.actionInterface()
        self.assertIn(QAccessibleActionInterface.pressAction(), action.actionNames())
        action.doAction(QAccessibleActionInterface.pressAction())
        self.app.processEvents()
        dialog = button.findChild(QObject, "helpDialog")
        self.assertTrue(dialog.property("visible"))
        window.close()
