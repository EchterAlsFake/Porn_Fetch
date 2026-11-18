"""Install the GUI language before creating any user-facing objects."""
import os

from PySide6.QtCore import Property, QCoreApplication, QFile, QLibraryInfo, QLocale, QObject, QTranslator

from src.backend.ui_languages import LANGUAGES, RELEASE_LOCALES, catalog_for_locale


class UiTranslation(QObject):
    def __init__(self, settings, engine):
        super().__init__(engine)
        self.translator = QTranslator(self)
        self.source_translator = QTranslator(self)
        self.qt_translator = QTranslator(self)
        self.quick_translator = QTranslator(self)
        self._options = []
        paths = {}
        preview = os.environ.get("PORN_FETCH_PREVIEW_TRANSLATIONS") == "1"
        for index, (code, label, catalog) in enumerate(LANGUAGES):
            if catalog in RELEASE_LOCALES:
                path = f":/translations/{catalog}.qm"
                if preview and not QFile.exists(path):
                    path = f":/translations/drafts/{catalog}.qm"
                if not QFile.exists(path):
                    continue
                paths[catalog] = path
            elif code not in {"system", "en"}:
                continue
            if code != "system":
                self._options.append({"index": index, "label": label})

        app = QCoreApplication.instance()
        if self.source_translator.load(":/translations/en.qm"):
            app.installTranslator(self.source_translator)
        self._startup_preference = settings.language
        code = LANGUAGES[self._startup_preference][0]
        candidates = QLocale.system().uiLanguages() if code == "system" else [code]
        locale = QLocale("en")
        self.catalog_loaded = False
        for candidate in candidates:
            catalog = catalog_for_locale(candidate)
            if catalog == "en":
                break
            if catalog in paths and self.translator.load(paths[catalog]) and not self.translator.isEmpty():
                locale = QLocale(candidate)
                break

        QLocale.setDefault(locale)
        app.setLayoutDirection(locale.textDirection())
        qt_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
        if self.qt_translator.load(locale, "qtbase", "_", qt_path):
            app.installTranslator(self.qt_translator)
        if self.quick_translator.load(locale, "qtdeclarative", "_", qt_path):
            app.installTranslator(self.quick_translator)
        # Install app strings last so they can also cover missing Qt contexts.
        if not self.translator.isEmpty():
            self.catalog_loaded = app.installTranslator(self.translator)

        #: Option in Appearance settings. Follow the operating system's preferred UI languages.
        self._options.insert(0, {"index": 0, "label": self.tr("System default")})
        if all(option["index"] != self._startup_preference for option in self._options):
            self._startup_preference = 1
        engine.setUiLanguage(locale.name())

    @Property("QVariantList", constant=True)
    def languages(self):
        return self._options

    @Property(int, constant=True)
    def startupPreference(self):
        return self._startup_preference
