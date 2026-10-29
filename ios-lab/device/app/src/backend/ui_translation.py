"""Apply the saved GUI language to Qt's translator and the live QML engine."""
from PySide6.QtCore import QCoreApplication, QLocale, QObject, QTranslator, Slot


class UiTranslation(QObject):
    def __init__(self, settings, engine):
        super().__init__(engine)
        self.settings, self.engine = settings, engine
        self.translator = QTranslator(self)
        self.catalog_loaded = False
        settings.languageChanged.connect(self.apply)
        self.apply(settings.language)

    @Slot(int)
    def apply(self, index):
        app = QCoreApplication.instance()
        if app is None:
            return
        app.removeTranslator(self.translator)
        language = {1: "en", 2: "de_DE", 3: "zh_CN", 4: "fr"}.get(index, QLocale.system().name())
        self.catalog_loaded = False
        if not language.startswith("en") and language != "C":
            catalog = "de_DE" if language.startswith("de") else "zh_CN" if language.startswith("zh") else language.split("_")[0]
            self.catalog_loaded = self.translator.load(f":/translations/translations/qm/{catalog}.qm")
            if self.catalog_loaded:
                app.installTranslator(self.translator)
        self.engine.setUiLanguage(language)
        self.engine.retranslate()
