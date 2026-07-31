"""
This file stores the main instance of Porn Fetch's configuration file,
so that only one instance is active, preventing memory errors and disk
overwriting when different classes hold their own instances and overwrite
each other.
"""
# config.py
from pathlib import Path
from PySide6.QtCore import QObject, Signal, QSettings, Property
from src.frontend.UI.theme import MATERIAL_THEMES, THEME_DISPLAY_NAMES, get_theme_colors

__license__ = "GPL 3"
__version__ = "3.9"
__author__ = "Johannes Habel"
__next_release__ = "4.0"
__type__ = "release"
__bundle_id__ = "me.echteralsfake.pornfetch"
__app_id__ = "pornfetch"
__app_name__ = "Porn Fetch"
__org_name__ = "EchterAlsFake"


PUBLIC_KEY_B64 = 'zGUmG8Z5InvoYIwnIokQi+SysjEodvfP8kLoCur3KjM=' # This is the public key for the license verification
IS_SOURCE_RUN = True

TEMP_DIRECTORY = ".temp"
TEMP_DIRECTORY_STATES = Path(TEMP_DIRECTORY).joinpath("states")
TEMP_DIRECTORY_SEGMENTS = Path(TEMP_DIRECTORY).joinpath("segments")


class SettingsManager(QObject):
    anonymousModeChanged = Signal(bool)
    updateChecksChanged = Signal(bool)
    speedLimitChanged = Signal(float)
    debugModeChanged = Signal(bool)
    languageChanged = Signal(int)
    fontSizeChanged = Signal(int)
    themeChanged = Signal(int)

    def __init__(self):
        super().__init__()
        self._settings = QSettings()
        self.mappings_quality: dict[int, str | int] = {
            0: "best",
            1: "half",
            2: "worst",
            3: 2160,
            4: 1440,
            5: 1080,
            6: 720,
            7: 540,
            8: 480,
            9: 360,
            10: 240,
            11: 144
        }
        self.mappings_ui_theme = {i: name for i, name in enumerate(THEME_DISPLAY_NAMES)}
        self.mappings_ui_language = {
            0: "system",
            1: "english",
            2: "german",
            3: "chinese",
            4: "french"
        }

    def refresh(self):
        self._settings = QSettings()

    def sync(self):
        self._settings.sync()

    # Video related
    @Property(int)
    def quality(self) -> int:
        # noinspection PyTypeChecker
        return self._settings.value("Video/quality", defaultValue=5, type=int)

    @Property(int)
    def model_videos(self) -> int:
        # noinspection PyTypeChecker
        return int(self._settings.value("Video/model_videos", defaultValue=0, type=int))

    @Property(int)
    def result_limit(self) -> int:
        # noinspection PyTypeChecker
        return self._settings.value("Video/result_limit", defaultValue=50, type=int)

    @Property(str)
    def output_path(self) -> str:
        # noinspection PyTypeChecker
        return self._settings.value("Video/output_path", defaultValue="./", type=str)

    @Property(bool)
    def write_metadata(self) -> bool:
        # noinspection PyTypeChecker
        return self._settings.value("Video/write_metadata", defaultValue=True, type=bool)

    @Property(bool)
    def skip_existing_files(self) -> bool:
        # noinspection PyTypeChecker
        return self._settings.value("Video/skip_existing_files", defaultValue=True, type=bool)

    @Property(bool)
    def track_videos(self) -> bool:
        # noinspection PyTypeChecker
        return self._settings.value("Video/track_videos", defaultValue=False, type=bool)

    @Property(str)
    def database_path(self) -> str:
        # noinspection PyTypeChecker
        return self._settings.value("Video/database_path", defaultValue="./downloads.db", type=str)

    # Performance related
    @Property(int)
    def parallel_downloads(self) -> int:
        # noinspection PyTypeChecker
        return self._settings.value("Performance/semaphore", defaultValue=1, type=int)

    @Property(int)
    def network_delay(self) -> int:
        # noinspection PyTypeChecker
        return self._settings.value("Performance/network_delay", defaultValue=0, type=int)

    @Property(int)
    def videos_concurrency(self) -> int:
        # noinspection PyTypeChecker
        return self._settings.value("Performance/videos_concurrency", defaultValue=10, type=int)

    @Property(int)
    def pages_concurrency(self) -> int:
        # noinspection PyTypeChecker
        return self._settings.value("Performance/pages_concurrency", defaultValue=2, type=int)

    @Property(int)
    def download_workers(self) -> int:
        # noinspection PyTypeChecker
        return self._settings.value("Performance/download_workers", defaultValue=20, type=int)

    @Property(int)
    def timeout(self) -> int:
        # noinspection PyTypeChecker
        return self._settings.value("Performance/timeout", defaultValue=10, type=int)

    @Property(int)
    def retries(self) -> int:
        # noinspection PyTypeChecker
        return self._settings.value("Performance/retries", defaultValue=4, type=int)

    @Property(float, notify=speedLimitChanged)
    def speed_limit(self) -> float:
        # noinspection PyTypeChecker
        return self._settings.value("Performance/speed_limit", defaultValue=0.0, type=float)

    @Property(int)
    def processing_delay(self) -> int:
        # noinspection PyTypeChecker
        return self._settings.value("Performance/processing_delay", defaultValue=0, type=int)

    # System / Misc related
    @Property(bool, notify=updateChecksChanged)
    def update_checks(self) -> bool:
        # noinspection PyTypeChecker
        return self._settings.value("Misc/update_checks", defaultValue=True, type=bool)

    @Property(bool, notify=anonymousModeChanged)
    def anonymous_mode(self) -> bool:
        # noinspection PyTypeChecker
        return self._settings.value("Misc/anonymous_mode", defaultValue=False, type=bool)

    @Property(bool)
    def supress_errors(self) -> bool:
        # noinspection PyTypeChecker
        return self._settings.value("Misc/supress_errors", defaultValue=False, type=bool)

    @Property(bool)
    def enable_logging(self) -> bool:
        # noinspection PyTypeChecker
        return self._settings.value("Misc/network_logging", defaultValue=False, type=bool)

    @Property(bool, notify=debugModeChanged)
    def debug_mode(self) -> bool:
        # noinspection PyTypeChecker
        return self._settings.value("Misc/debug_mode", defaultValue=False, type=bool)

    @Property(bool)
    def use_truststore(self) -> bool:
        # noinspection PyTypeChecker
        return self._settings.value("Misc/use_truststore", defaultValue=False, type=bool)

    @Property(int, notify=languageChanged)
    def language(self) -> int:
        # noinspection PyTypeChecker
        return self._settings.value("UI/language", defaultValue=0, type=int)

    @Property(int, notify=fontSizeChanged)
    def font_size(self) -> int:
        # noinspection PyTypeChecker
        return self._settings.value("UI/font_size", defaultValue=12, type=int)

    @Property(int, notify=themeChanged)
    def theme(self) -> int:
        # noinspection PyTypeChecker
        return self._settings.value("UI/theme", defaultValue=0, type=int)

    @Property(list, constant=True)
    def theme_names(self) -> list:
        return THEME_DISPLAY_NAMES

    @Property(str, notify=themeChanged)
    def theme_primary_color(self) -> str:
        return get_theme_colors(self.theme)["primary"]

    @Property(str, notify=themeChanged)
    def theme_bg_color(self) -> str:
        return get_theme_colors(self.theme)["background"]

    @Property(str, notify=themeChanged)
    def theme_fg_color(self) -> str:
        return get_theme_colors(self.theme)["foreground"]

    @Property(bool, notify=themeChanged)
    def theme_is_dark(self) -> bool:
        return get_theme_colors(self.theme)["is_dark"]

    #### --------------- Writing Settings ---------------- ####

    # Video related
    @quality.setter
    def quality(self, val):
        if val != self.quality:
            self._settings.setValue("Video/quality", val)
            self.qualityChanged.emit(val)

    @model_videos.setter
    def model_videos(self, val):
        if val != self.model_videos:
            self._settings.setValue("Video/model_videos", val)
            self.modelVideosChanged.emit(val)

    @result_limit.setter
    def result_limit(self, val):
        if val != self.result_limit:
            self._settings.setValue("Video/result_limit", val)
            self.resultLimitChanged.emit(val)

    @output_path.setter
    def output_path(self, val):
        if val != self.output_path:
            self._settings.setValue("Video/output_path", val)
            self.outputPathChanged.emit(val)

    @write_metadata.setter
    def write_metadata(self, val):
        if val != self.write_metadata:
            self._settings.setValue("Video/write_metadata", val)
            self.writeMetadataChanged.emit(val)

    @skip_existing_files.setter
    def skip_existing_files(self, val):
        if val != self.skip_existing_files:
            self._settings.setValue("Video/skip_existing_files", val)
            self.skipExistingFilesChanged.emit(val)

    @track_videos.setter
    def track_videos(self, val):
        if val != self.track_videos:
            self._settings.setValue("Video/track_videos", val)

    @database_path.setter
    def database_path(self, val):
        if val != self.database_path:
            self._settings.setValue("Video/database_path", val)

    # Performance related
    @parallel_downloads.setter
    def parallel_downloads(self, val):
        if val != self.parallel_downloads:
            self._settings.setValue("Performance/semaphore", val)
            self.parallelDownloadsChanged.emit(val)

    @network_delay.setter
    def network_delay(self, val):
        if val != self.network_delay:
            self._settings.setValue("Performance/network_delay", val)

    @videos_concurrency.setter
    def videos_concurrency(self, val):
        if val != self.videos_concurrency:
            self._settings.setValue("Performance/videos_concurrency", val)

    @pages_concurrency.setter
    def pages_concurrency(self, val):
        if val != self.pages_concurrency:
            self._settings.setValue("Performance/pages_concurrency", val)

    @download_workers.setter
    def download_workers(self, val):
        if val != self.download_workers:
            self._settings.setValue("Performance/download_workers", val)

    @timeout.setter
    def timeout(self, val):
        if val != self.timeout:
            self._settings.setValue("Performance/timeout", val)

    @retries.setter
    def retries(self, val):
        if val != self.retries:
            self._settings.setValue("Performance/retries", val)

    @speed_limit.setter
    def speed_limit(self, val):
        if val != self.speed_limit:
            self._settings.setValue("Performance/speed_limit", val)
            self.speedLimitChanged.emit(val)

    @processing_delay.setter
    def processing_delay(self, val):
        if val != self.processing_delay:
            self._settings.setValue("Performance/processing_delay", val)

    # System / Misc related
    @update_checks.setter
    def update_checks(self, val):
        if val != self.update_checks:
            self._settings.setValue("Misc/update_checks", val)
            self.updateChecksChanged.emit(val)

    @anonymous_mode.setter
    def anonymous_mode(self, val):
        if val != self.anonymous_mode:
            self._settings.setValue("Misc/anonymous_mode", val)
            self.anonymousModeChanged.emit(val)

    @supress_errors.setter
    def supress_errors(self, val):
        if val != self.supress_errors:
            self._settings.setValue("Misc/supress_errors", val)
            self.supressErrorsChanged.emit(val)

    @enable_logging.setter
    def enable_logging(self, val):
        if val != self.enable_logging:
            self._settings.setValue("Misc/network_logging", val)
            self.networkLoggingChanged.emit(val)

    @debug_mode.setter
    def debug_mode(self, val):
        if val != self.debug_mode:
            self._settings.setValue("Misc/debug_mode", val)
            self.debugModeChanged.emit(val)

    @use_truststore.setter
    def use_truststore(self, val):
        if val != self.use_truststore:
            self._settings.setValue("Misc/use_truststore", val)

    @language.setter
    def language(self, val):
        if val != self.language:
            self._settings.setValue("UI/language", val)
            self.languageChanged.emit(val)

    @font_size.setter
    def font_size(self, val):
        if val != self.font_size:
            self._settings.setValue("UI/font_size", val)
            self.fontSizeChanged.emit(val)

    @theme.setter
    def theme(self, val):
        val = int(val)
        if val != self.theme:
            self._settings.setValue("UI/theme", val)
            self.themeChanged.emit(val)

app_settings = SettingsManager() # Singleton instance shared globally :)