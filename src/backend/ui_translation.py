"""Keep the interface in English while translation support is unfinished."""
from PySide6.QtCore import QCoreApplication, QLibraryInfo, QLocale, QObject, QTranslator, Slot
from PySide6.QtGui import QGuiApplication


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
        # Draft catalogs are kept for contributors, but this release is English-only.
        locale = QLocale("en")
        QLocale.setDefault(locale)
        if isinstance(app, QGuiApplication):
            app.setLayoutDirection(locale.textDirection())
        qt_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
        if self.qt_translator.load(locale, "qtbase", "_", qt_path):
            app.installTranslator(self.qt_translator)
        if self.quick_translator.load(locale, "qtdeclarative", "_", qt_path):
            app.installTranslator(self.quick_translator)
        self.catalog_loaded = False
        self.engine.setUiLanguage(locale.name())
        self.engine.retranslate()
