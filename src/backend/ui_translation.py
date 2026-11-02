"""Apply GUI and Qt catalogs, locale formatting and direction to the live engine."""
from PySide6.QtCore import QCoreApplication, QLibraryInfo, QLocale, QObject, QTranslator, Slot
from PySide6.QtGui import QGuiApplication

from src.backend.ui_languages import LANGUAGES, catalog_for_locale


class UiTranslation(QObject):
    def __init__(self, settings, engine):
        super().__init__(engine)
        self.settings, self.engine = settings, engine
        self.translator = QTranslator(self)
        self.qt_translator = QTranslator(self)
        self.quick_translator = QTranslator(self)
        self.catalog_loaded = False
        settings.languageChanged.connect(self.apply)
        self.apply(settings.language)

    @Slot(int)
    def apply(self, index):
        app = QCoreApplication.instance()
        if app is None:
            return
        app.removeTranslator(self.translator)
        app.removeTranslator(self.qt_translator)
        app.removeTranslator(self.quick_translator)
        code = LANGUAGES[index][0] if 0 <= index < len(LANGUAGES) else "system"
        locale = QLocale.system() if code == "system" else QLocale(code)
        if locale.language() == QLocale.Language.C:
            locale = QLocale("en")
        QLocale.setDefault(locale)
        if isinstance(app, QGuiApplication):
            app.setLayoutDirection(locale.textDirection())
        qt_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
        if self.qt_translator.load(locale, "qtbase", "_", qt_path):
            app.installTranslator(self.qt_translator)
        if self.quick_translator.load(locale, "qtdeclarative", "_", qt_path):
            app.installTranslator(self.quick_translator)
        catalog = catalog_for_locale(locale.name())
        self.catalog_loaded = False
        if catalog:
            self.catalog_loaded = self.translator.load(f":/translations/translations/qm/{catalog}.qm")
            if self.catalog_loaded:
                app.installTranslator(self.translator)
        self.engine.setUiLanguage(locale.name())
        self.engine.retranslate()
