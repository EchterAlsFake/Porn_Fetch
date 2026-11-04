"""Offline GUI language compatibility and live translation contracts."""
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
import tempfile
import unittest
from pathlib import Path

from PySide6.QtCore import QLocale, QSettings, QUrl
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
        self.assertEqual(catalog_for_locale("zh_Hans_SG"), "zh_CN")
        self.assertIsNone(catalog_for_locale("zh_TW"))
        self.assertIsNone(catalog_for_locale("zh_Hant_HK"))

    def test_old_language_preferences_still_render_english(self):
        engine = QQmlApplicationEngine()
        self.settings.language = 1
        translation = UiTranslation(self.settings, engine)
        engine.loadData(b'import QtQuick\nQtObject { property string label: qsTranslate("DownloadsPage", "Get Video"); property string missing: qsTranslate("DownloadsPage", "Untranslated fixture") }', QUrl())
        root = engine.rootObjects()[0]
        self.assertEqual(root.property("label"), "Get Video")
        self.settings.language = 2
        self.assertFalse(translation.catalog_loaded)
        self.assertEqual(root.property("label"), "Get Video")
        self.assertEqual(engine.uiLanguage(), "en_US")
        self.assertEqual(root.property("missing"), "Untranslated fixture")
        self.settings.language = 1
        self.assertEqual(root.property("label"), "Get Video")
        self.app.removeTranslator(translation.translator)
        self.app.removeTranslator(translation.qt_translator)
        self.app.removeTranslator(translation.quick_translator)

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
