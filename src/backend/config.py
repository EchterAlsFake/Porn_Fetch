"""
This file stores the main instance of Porn Fetch's configuration file,
so that only one instance is active, preventing memory errors and disk
overwriting when different classes hold their own instances and overwrite
each other.
"""
# config.py
from pathlib import Path
from PySide6.QtCore import QObject, Signal, QSettings, Property

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
    debugModeChanged = Signal(bool)
    languageChanged = Signal(int)
    fontSizeChanged = Signal(int)
    themeChanged = Signal(int)
    reloadClients = Signal(object)

    # For Theming
    coreStyleChanged = Signal(str)
    darkModeChanged = Signal(bool)
    accentColorChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self._settings = QSettings(__org_name__, __app_name__)
        self.log_level_map: dict[int, str] = {
            0: "DEBUG",
            1: "INFO",
            2: "WARNING",
            3: "ERROR",
            4: "CRITICAL"
        }
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
        self.mappings_ui_language = {
            0: "system",
            1: "english",
            2: "german",
            3: "chinese",
            4: "french"
        }

    def refresh(self):
        self._settings = QSettings(__org_name__, __app_name__)

    def sync(self):
        self._settings.sync()

    def get_bool(self, key: str, default: bool = False) -> bool:
        val = self._settings.value(key, defaultValue=default)
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            return val.lower() == 'true'
        return bool(val)

    def get_int(self, key: str, default: int = 0) -> int:
        val = self._settings.value(key, defaultValue=default)
        try:
            return int(val)
        except (ValueError, TypeError):
            return default

    def get_float(self, key: str, default: float = 0.0) -> float:
        val = self._settings.value(key, defaultValue=default)
        try:
            return float(val)
        except (ValueError, TypeError):
            return default

    def get_str(self, key: str, default: str = "") -> str:
        val = self._settings.value(key, defaultValue=default)
        if val is None:
            return default
        return str(val)


    # Video related
    @Property(int)
    def quality(self) -> int:
        return self.get_int("Video/quality", 5)

    @Property(int)
    def model_videos(self) -> int:
        return self.get_int("Video/model_videos", 0)

    @Property(int)
    def result_limit(self) -> int:
        return self.get_int("Video/result_limit", 50)

    @Property(str)
    def output_path(self) -> str:
        return self.get_str("Video/output_path", "./")

    @Property(bool)
    def write_metadata(self) -> bool:
        return self.get_bool("Video/write_metadata", True)

    @Property(bool)
    def skip_existing_files(self) -> bool:
        return self.get_bool("Video/skip_existing_files", True)

    @Property(bool)
    def track_videos(self) -> bool:
        return self.get_bool("Video/track_videos", False)

    @Property(str)
    def database_path(self) -> str:
        return self.get_str("Video/database_path", "./downloads.db")

    # Performance related
    @Property(int)
    def parallel_downloads(self) -> int:
        return self.get_int("Performance/semaphore", 1)

    @Property(int)
    def network_delay(self) -> int:
        return self.get_int("Performance/network_delay", 0)

    @Property(int)
    def videos_concurrency(self) -> int:
        return self.get_int("Performance/videos_concurrency", 10)

    @Property(int)
    def pages_concurrency(self) -> int:
        return self.get_int("Performance/pages_concurrency", 2)

    @Property(int)
    def download_workers(self) -> int:
        return self.get_int("Performance/download_workers", 20)

    @Property(int)
    def timeout(self) -> int:
        return self.get_int("Performance/timeout", 10)

    @Property(int)
    def retries(self) -> int:
        return self.get_int("Performance/retries", 4)

    @Property(float, notify=reloadClients)
    def speed_limit(self) -> float:
        return self.get_float("Performance/speed_limit", 0.0)

    @Property(int)
    def processing_delay(self) -> int:
        return self.get_int("Performance/processing_delay", 0)

    # System / Misc related
    @Property(bool, notify=updateChecksChanged)
    def update_checks(self) -> bool:
        return self.get_bool("Misc/update_checks", True)

    @Property(bool)
    def supress_errors(self) -> bool:
        return self.get_bool("Misc/supress_errors", False)

    @Property(bool)
    def enable_logging(self) -> bool:
        return self.get_bool("Misc/network_logging", False)

    @Property(bool, notify=debugModeChanged)
    def debug_mode(self) -> bool:
        return self.get_bool("Misc/debug_mode", False)

    @Property(str, notify=None) # Can't be changed dynamically
    def log_level(self) -> int:
        return self.get_str("Misc/log_level", 0)

    @Property(str, notify=reloadClients)
    def interface(self) -> str:
        return self.get_str("Misc/interface", None)

    @Property(str, notify=reloadClients)
    def http_version(self) -> str:
        return self.get_str("Misc/http_version", "v2")

    @Property(bool, notify=anonymousModeChanged)
    def anonymous_mode(self) -> bool:
        return self.get_bool("Privacy/anonymous_mode", False)

    @Property(bool, notify=reloadClients)
    def encrypted_ch(self) -> bool:
        return self.get_bool("Privacy/encrypted_ch", True)

    @Property(bool, notify=reloadClients)
    def dns_over_https(self) -> bool:
        return self.get_bool("Privacy/dns_over_https", True)

    @Property(str, notify=reloadClients)
    def dns_server(self) -> str:
        return self.get_str("Privacy/dns_server", "https://dns.mullvad.net/dns-query")

    @Property(str, notify=reloadClients)
    def fallback_dns(self) -> str:
        return self.get_str("Privacy/fallback_dns", "https://dns.quad9.net/dns-query")

    @Property(bool, notify=reloadClients)
    def sni_obfuscation(self) -> bool:
        return self.get_bool("Privacy/sni_obfuscation", False)

    @Property(bool, notify=reloadClients)
    def sni_obfuscation_lite(self) -> bool:
        return self.get_bool("Privacy/sni_obfuscation_lite", False)

    @Property(bool, notify=reloadClients)
    def sni_obfuscation_strict(self) -> bool:
        return self.get_bool("Privacy/sni_obfuscation_strict", False)

    @Property(str, notify=reloadClients)
    def proxy(self) -> str:
        return self.get_str("Privacy/proxy", "")

    @Property(bool, notify=reloadClients)
    def proxy_ssl_verification(self) -> bool:
        return self.get_bool("Privacy/proxy_ssl_verification", True)

    @Property(int, notify=languageChanged)
    def language(self) -> int:
        return self.get_int("UI/language", 0)

    @Property(int, notify=fontSizeChanged)
    def font_size(self) -> int:
        return self.get_int("UI/font_size", 12)

    @Property(str, notify=coreStyleChanged)
    def core_style(self) -> str:
        # Basic, Fusion, Material, Universal, Windows
        return self.get_str("UI/core_style", "Material")

    @core_style.setter
    def core_style(self, val: str):
        if val != self.core_style:
            self._settings.setValue("UI/core_style", val)
            self.coreStyleChanged.emit(val)

    @Property(bool, notify=darkModeChanged)
    def dark_mode(self) -> bool:
        return self.get_bool("UI/dark_mode", True)

    @dark_mode.setter
    def dark_mode(self, val: bool):
        if val != self.dark_mode:
            self._settings.setValue("UI/dark_mode", val)
            self.darkModeChanged.emit(val)

    @Property(str, notify=accentColorChanged)
    def accent_color(self) -> str:
        return self.get_str("UI/accent_color", "#6366f1")

    @accent_color.setter
    def accent_color(self, val: str):
        if val != self.accent_color:
            self._settings.setValue("UI/accent_color", val)
            self.accentColorChanged.emit(val)


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

    @log_level.setter
    def log_level(self, val):
        if val != self.log_level:
            self._settings.setValue("Misc/log_level", val)

    @interface.setter
    def interface(self, val):
        if val != self.interface:
            self._settings.setValue("Misc/interface", val)
            self.reloadClients.emit(val)

    @http_version.setter
    def http_version(self, val):
        if val != self.http_version:
            self._settings.setValue("Misc/http_version", val)
            self.reloadClients.emit(val)

    @anonymous_mode.setter
    def anonymous_mode(self, val):
        if val != self.anonymous_mode:
            self._settings.setValue("Privacy/anonymous_mode", val)
            self.anonymousModeChanged.emit(val)

    @encrypted_ch.setter
    def encrypted_ch(self, val):
        if val != self.encrypted_ch:
            self._settings.setValue("Privacy/encrypted_ch", val)
            self.reloadClients.emit(val)

    @dns_over_https.setter
    def dns_over_https(self, val):
        if val != self.dns_over_https:
            self._settings.setValue("Privacy/dns_over_https", val)
            self.reloadClients.emit(val)

    @dns_server.setter
    def dns_server(self, val):
        if val != self.dns_server:
            self._settings.setValue("Privacy/dns_server", val)
            self.reloadClients.emit(val)

    @fallback_dns.setter
    def fallback_dns(self, val):
        if val != self.fallback_dns:
            self._settings.setValue("Privacy/fallback_dns", val)
            self.reloadClients.emit(val)

    @sni_obfuscation.setter
    def sni_obfuscation(self, val):
        if val != self.sni_obfuscation:
            self._settings.setValue("Privacy/sni_obfuscation", val)
            self.reloadClients.emit(val)

    @sni_obfuscation_lite.setter
    def sni_obfuscation_lite(self, val):
        if val != self.sni_obfuscation_lite:
            self._settings.setValue("Privacy/sni_obfuscation_lite", val)
            self.reloadClients.emit(val)

    @sni_obfuscation_strict.setter
    def sni_obfuscation_strict(self, val):
        if val != self.sni_obfuscation_strict:
            self._settings.setValue("Privacy/sni_obfuscation_strict", val)
            self.reloadClients.emit(val)

    @proxy.setter
    def proxy(self, val):
        if val != self.proxy:
            self._settings.setValue("Privacy/proxy", val)
            self.reloadClients.emit(val)

    @proxy_ssl_verification.setter
    def proxy_ssl_verification(self, val):
        if val != self.proxy_ssl_verification:
            self._settings.setValue("Privacy/proxy_ssl_verification", val)
            self.reloadClients.emit(val)

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

app_settings = SettingsManager() # Singleton instance shared globally :)
