"""
This file stores the main instance of Porn Fetch's configuration file,
so that only one instance is active, preventing memory errors and disk
overwriting when different classes hold their own instances and overwrite
each other.
"""
# config.py
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QObject, Property, QSettings, QUrl, Signal, Slot

__license__ = "GPL 3"
__version__ = "3.9"
__author__ = "Johannes Habel"
__next_release__ = "4.0"
__type__ = "release"
__bundle_id__ = "fi.echteralsfake.pornfetch"
__app_id__ = "pornfetch"
__app_name__ = "Porn Fetch"
__org_name__ = "EchterAlsFake"


PUBLIC_KEY_B64 = 'zGUmG8Z5InvoYIwnIokQi+SysjEodvfP8kLoCur3KjM=' # This is the public key for the license verification
IS_SOURCE_RUN = True

TEMP_DIRECTORY = ".temp"
TEMP_DIRECTORY_STATES = Path(TEMP_DIRECTORY).joinpath("states")
TEMP_DIRECTORY_SEGMENTS = Path(TEMP_DIRECTORY).joinpath("segments")


class SettingsManager(QObject):
    qualityChanged = Signal(int)
    anonymousModeChanged = Signal(bool)
    updateChecksChanged = Signal(bool)
    languageChanged = Signal(int)
    sniProxyChanged = Signal(str)
    fontSizeChanged = Signal(int)
    themeChanged = Signal(int)
    reloadClients = Signal(object)
    restartRequired = Signal()
    databaseChanged = Signal(str)
    moveDatabase = Signal(str, str)

    # For Theming
    coreStyleChanged = Signal(str)
    darkModeChanged = Signal(bool)
    accentColorChanged = Signal(str)

    # Missing Signals
    networkLoggingChanged = Signal(bool)

    # These Signals are not needed yet, but who knows
    logLevelChanged = Signal(int)
    supressErrorsChanged = Signal(bool)
    pagesConcurrencyChanged = Signal(int)
    videosConcurrencyChanged = Signal(int)
    processingDelayChanged = Signal(int)
    timeoutChanged = Signal(int)
    retriesChanged = Signal(int)
    parallelDownloadsChanged = Signal(int)
    networkDelayChanged = Signal(int)
    downloadWorkersChanged = Signal(int)
    outputPathChanged = Signal(str)
    skipExistingFilesChanged = Signal(bool)
    writeMetadataChanged = Signal(bool)
    resultLimitChanged = Signal(int)
    strictEnforcementChanged = Signal(bool)
    modelVideosChanged = Signal(int)
    localeChanged = Signal(str)
    trackVideosChanged = Signal(bool)
    speedLimitChanged = Signal(float)
    responseCacheSizeChanged = Signal(int)
    responseCacheTTLChanged = Signal(int)
    segmentCacheSizeChanged = Signal(int)
    segmentCacheTTLChanged = Signal(int)
    requestInitialRetryDelayChanged = Signal(float)
    requestRetryMaxDelayChanged = Signal(float)
    requestRetryMultiplierChanged = Signal(float)
    requestRetryJitterChanged = Signal(float)
    trustEnvironmentChanged = Signal(bool)
    debugModeChanged = Signal(bool)
    httpVersionChanged = Signal(str)
    impersonationChanged = Signal(str)
    customJA3Changed = Signal(str)
    interfaceChanged = Signal(str)
    encryptedCHChanged = Signal(bool)
    dnsOverHTTPSChanged = Signal(bool)
    enableTorChanged = Signal(bool)
    enableTorServerRoutingChanged = Signal(bool)
    dnsServerChanged = Signal(str)
    fallbackDNSChanged = Signal(str)
    sniObfuscationChanged = Signal(bool)
    sniObfuscationLiteChanged = Signal(bool)
    sniObfuscationStrictChanged = Signal(bool)
    sniObfuscationStrictProfileChanged = Signal(str)
    proxyChanged = Signal(str)
    proxySSLVerificationChanged = Signal(bool)

    def __init__(self):
        super().__init__()
        self._settings = QSettings(__org_name__, __app_name__)
        self._normalize_sni_obfuscation_mode()
        # Runtime-only URL owned by SNIProxyManager; never persist ephemeral ports.
        self.active_sni_proxy_url: str | None = None
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
            10: 250,
            11: 240,
            12: 144
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

    def reset(self):
        self._settings.clear() # Resets settings back to default

    def get_bool(self, key: str, default: bool = False) -> bool:
        val = self._settings.value(key, defaultValue=default)
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            return val.lower() == 'true'
        return bool(val)

    def get_int(self, key: str, default: int = 0) -> int:
        val = self._settings.value(key, defaultValue=default)
        if isinstance(val, (int, float, str)):
            try:
                return int(val)
            except (ValueError, TypeError):
                pass
        return default

    def get_float(self, key: str, default: float = 0.0) -> float:
        val = self._settings.value(key, defaultValue=default)
        if isinstance(val, (int, float, str)):
            try:
                return float(val)
            except (ValueError, TypeError):
                pass
        return default

    def get_str(self, key: str, default: str = "") -> str:
        val = self._settings.value(key, defaultValue=default)
        if val is None:
            return default
        return str(val)

    def _normalize_sni_obfuscation_mode(self) -> None:
        """Repair mode pairs written by older two-way QML toggle handlers."""

        enabled = self.get_bool("Privacy/sni_obfuscation", False)
        lite = self.get_bool("Privacy/sni_obfuscation_lite", False)
        strict = self.get_bool("Privacy/sni_obfuscation_strict", False)
        changed = False

        if lite and strict:
            # Strict could only become true through an explicit user choice,
            # whereas Lite was historically left behind by the QML handler.
            self._settings.setValue("Privacy/sni_obfuscation_lite", False)
            changed = True
        elif enabled and not (lite or strict):
            self._settings.setValue("Privacy/sni_obfuscation_lite", True)
            changed = True

        if changed:
            self._settings.sync()

    def _set_sni_obfuscation_mode(self, mode: str) -> None:
        if mode not in {"lite", "strict"}:
            raise ValueError(f"Unknown SNI obfuscation mode: {mode!r}")

        lite = mode == "lite"
        strict = mode == "strict"
        lite_changed = lite != self.sni_obfuscation_lite
        strict_changed = strict != self.sni_obfuscation_strict
        if not (lite_changed or strict_changed):
            return

        # Persist both halves before notifying QML so observers can never see
        # an intermediate state with both modes enabled (or neither enabled).
        self._settings.setValue("Privacy/sni_obfuscation_lite", lite)
        self._settings.setValue("Privacy/sni_obfuscation_strict", strict)
        self._settings.sync()
        if lite_changed:
            self.sniObfuscationLiteChanged.emit(lite)
        if strict_changed:
            self.sniObfuscationStrictChanged.emit(strict)
        self.restartRequired.emit()

    @Slot(str)
    def set_sni_obfuscation_mode(self, mode: str) -> None:
        """Atomically select the Lite or Strict SNI implementation from QML."""

        self._set_sni_obfuscation_mode(mode)

    @staticmethod
    def _absolute_path(path: str) -> Path:
        return Path(path).expanduser().resolve()

    @Slot(str, result=QUrl)
    def path_to_file_url(self, path: str) -> QUrl:
        """Convert a persisted local path into a URL accepted by Qt dialogs."""
        return QUrl.fromLocalFile(str(self._absolute_path(path)))

    @Slot(str, result=QUrl)
    def parent_directory_url(self, path: str) -> QUrl:
        """Return the containing folder URL for a persisted file path."""
        return QUrl.fromLocalFile(str(self._absolute_path(path).parent))

    @Slot(QUrl, result=str)
    def local_path_from_url(self, file_url: QUrl) -> str:
        """Convert a URL selected by a Qt dialog back into a local path."""
        local_path = file_url.toLocalFile()
        return str(Path(local_path)) if local_path else ""


    # Video related
    @Property(int, notify=qualityChanged)
    def quality(self) -> int:
        return self.get_int("Video/quality", 5)

    @quality.setter
    def quality(self, val):
        if val != self.quality:      # noinspection PyPropertyDefinition
            self._settings.setValue("Video/quality", val)
            self.qualityChanged.emit(val)

    @Property(int, notify=modelVideosChanged)
    def model_videos(self) -> int:
        return self.get_int("Video/model_videos", 0)

    @model_videos.setter
    def model_videos(self, val):
        if val != self.model_videos:
            self._settings.setValue("Video/model_videos", val)
            self.modelVideosChanged.emit(val)

    @Property(str, notify=localeChanged)
    def locale(self) -> str:
        return self.get_str("Video/locale", "en-US")

    @locale.setter
    def locale(self, val: str):
        if val != self.locale:
            self._settings.setValue("Video/locale", val)
            self.localeChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(bool, notify=strictEnforcementChanged)
    def strict_enforcement(self) -> bool:
        return self.get_bool("Video/strict_enforcement", False)

    @strict_enforcement.setter
    def strict_enforcement(self, val: bool):
        if val != self.strict_enforcement: # type: ignore
            self._settings.setValue("Video/strict_enforcement", val)
            self.strictEnforcementChanged.emit(val)

    @Property(int, notify=resultLimitChanged)
    def result_limit(self) -> int:
        return self.get_int("Video/result_limit", 50)

    @result_limit.setter
    def result_limit(self, val):
        if val != self.result_limit:
            self._settings.setValue("Video/result_limit", val)
            self.resultLimitChanged.emit(val)

    @Property(str, notify=outputPathChanged)
    def output_path(self) -> str:
        return self.get_str("Video/output_path", "./")

    @output_path.setter
    def output_path(self, val):
        if val != self.output_path:
            self._settings.setValue("Video/output_path", val)
            self.outputPathChanged.emit(val)

    @Property(bool, notify=writeMetadataChanged)
    def write_metadata(self) -> bool:
        return self.get_bool("Video/write_metadata", True)

    @write_metadata.setter
    def write_metadata(self, val):
        if val != self.write_metadata:
            self._settings.setValue("Video/write_metadata", val)
            self.writeMetadataChanged.emit(val)

    @Property(bool, notify=skipExistingFilesChanged)
    def skip_existing_files(self) -> bool:
        return self.get_bool("Video/skip_existing_files", True)

    @skip_existing_files.setter
    def skip_existing_files(self, val):
        if val != self.skip_existing_files:
            self._settings.setValue("Video/skip_existing_files", val)
            self.skipExistingFilesChanged.emit(val)

    @Property(bool, notify=trackVideosChanged)
    def track_videos(self) -> bool:
        return self.get_bool("Video/track_videos", False)

    @track_videos.setter
    def track_videos(self, val):
        if val != self.track_videos:
            self._settings.setValue("Video/track_videos", val)
            self.trackVideosChanged.emit(val)
            self.restartRequired.emit()

    @Property(str, notify=databaseChanged)
    def database_path(self) -> str:
        return self.get_str("Video/database_path", "./downloads.db")

    @database_path.setter
    def database_path(self, val):
        if val != self.database_path:

            current_path = self.database_path

            self._settings.setValue("Video/database_path", val)
            self.databaseChanged.emit(val)
            self.restartRequired.emit()
            self.moveDatabase.emit(current_path, val)

    # Performance related
    @Property(int, notify=downloadWorkersChanged)
    def download_workers(self) -> int:
        return self.get_int("Performance/download_workers", 20)

    @download_workers.setter
    def download_workers(self, val):
        if val != self.download_workers:
            self._settings.setValue("Performance/download_workers", val)
            self.downloadWorkersChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(int, notify=networkDelayChanged)
    def network_delay(self) -> int:
        return self.get_int("Performance/network_delay", 0)

    @network_delay.setter
    def network_delay(self, val):
        if val != self.network_delay:
            self._settings.setValue("Performance/network_delay", val)
            self.networkDelayChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(int, notify=parallelDownloadsChanged)
    def parallel_downloads(self) -> int:
        return self.get_int("Performance/semaphore", 1)

    @parallel_downloads.setter
    def parallel_downloads(self, val):
        if val != self.parallel_downloads:
            self._settings.setValue("Performance/semaphore", val)
            self.parallelDownloadsChanged.emit(val)

    @Property(int, notify=retriesChanged)
    def retries(self) -> int:
        return self.get_int("Performance/retries", 4)

    @retries.setter
    def retries(self, val):
        if val != self.retries:
            self._settings.setValue("Performance/retries", val)
            self.retriesChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(int, notify=timeoutChanged)
    def timeout(self) -> int:
        return self.get_int("Performance/timeout", 10)

    @timeout.setter
    def timeout(self, val):
        if val != self.timeout:
            self._settings.setValue("Performance/timeout", val)
            self.timeoutChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(int, notify=processingDelayChanged)
    def processing_delay(self) -> int:
        return self.get_int("Performance/processing_delay", 0)

    @processing_delay.setter
    def processing_delay(self, val):
        if val != self.processing_delay:
            self._settings.setValue("Performance/processing_delay", val)
            self.processingDelayChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(float, notify=speedLimitChanged)
    def speed_limit(self) -> float:
        return self.get_float("Performance/speed_limit", 0.0)

    @speed_limit.setter
    def speed_limit(self, val):
        if val != self.speed_limit:
            self._settings.setValue("Performance/speed_limit", val)
            self.speedLimitChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(int, notify=videosConcurrencyChanged)
    def videos_concurrency(self) -> int:
        return self.get_int("Performance/videos_concurrency", 10)

    @videos_concurrency.setter
    def videos_concurrency(self, val):
        if val != self.videos_concurrency:
            self._settings.setValue("Performance/videos_concurrency", val)
            self.videosConcurrencyChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(int, notify=pagesConcurrencyChanged)
    def pages_concurrency(self) -> int:
        return self.get_int("Performance/pages_concurrency", 2)

    @pages_concurrency.setter
    def pages_concurrency(self, val):
        if val != self.pages_concurrency:
            self._settings.setValue("Performance/pages_concurrency", val)
            self.pagesConcurrencyChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(int, notify=responseCacheSizeChanged)
    def response_cache_size(self) -> int:
        return self.get_int("Performance/response_cache_size", 32)

    @response_cache_size.setter
    def response_cache_size(self, val):
        if val != self.response_cache_size:
            self._settings.setValue("Performance/response_cache_size", val)
            self.responseCacheSizeChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(int, notify=responseCacheTTLChanged)
    def response_cache_ttl(self) -> int:
        return self.get_int("Performance/response_cache_ttl", 300)

    @response_cache_ttl.setter
    def response_cache_ttl(self, val):
        if val != self.response_cache_ttl:
            self._settings.setValue("Performance/response_cache_ttl", val)
            self.responseCacheTTLChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(int, notify=segmentCacheSizeChanged)
    def segment_cache_size(self) -> int:
        return self.get_int("Performance/segment_cache_size", 8)

    @segment_cache_size.setter
    def segment_cache_size(self, val):
        if val != self.segment_cache_size:
            self._settings.setValue("Performance/segment_cache_size", val)
            self.segmentCacheSizeChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(int, notify=segmentCacheTTLChanged)
    def segment_cache_ttl(self) -> int:
        return self.get_int("Performance/segment_cache_ttl", 300)

    @segment_cache_ttl.setter
    def segment_cache_ttl(self, val):
        if val != self.segment_cache_ttl:
            self._settings.setValue("Performance/segment_cache_ttl", val)
            self.segmentCacheTTLChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(float, notify=requestInitialRetryDelayChanged)
    def request_initial_retry_delay(self) -> float:
        return self.get_float("Performance/request_initial_retry_delay", 0.5)

    @request_initial_retry_delay.setter
    def request_initial_retry_delay(self, val):
        if val != self.request_initial_retry_delay:
            self._settings.setValue("Performance/request_initial_retry_delay", val)
            self.requestInitialRetryDelayChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(float, notify=requestRetryMaxDelayChanged)
    def request_retry_max_delay(self) -> float:
        return self.get_float("Performance/request_retry_max_delay", 30)

    @request_retry_max_delay.setter
    def request_retry_max_delay(self, val):
        if val != self.request_retry_max_delay:
            self._settings.setValue("Performance/request_retry_max_delay", val)
            self.requestRetryMaxDelayChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(float, notify=requestRetryMultiplierChanged)
    def request_retry_multiplier(self) -> float:
        return self.get_float("Performance/request_retry_multiplier", 2)

    @request_retry_multiplier.setter
    def request_retry_multiplier(self, val):
        if val != self.request_retry_multiplier:
            self._settings.setValue("Performance/request_retry_multiplier", val)
            self.requestRetryMultiplierChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(float, notify=requestRetryJitterChanged)
    def request_retry_jitter(self) -> float:
        return self.get_float("Performance/request_retry_jitter", 0.5)

    @request_retry_jitter.setter
    def request_retry_jitter(self, val):
        if val != self.request_retry_jitter:
            self._settings.setValue("Performance/request_retry_jitter", val)
            self.requestRetryJitterChanged.emit(val)
            self.reloadClients.emit(val)

    # System / Misc related
    @Property(bool, notify=updateChecksChanged)
    def update_checks(self) -> bool:
        return self.get_bool("Misc/update_checks", True)

    @update_checks.setter
    def update_checks(self, val):
        if val != self.update_checks:
            self._settings.setValue("Misc/update_checks", val)
            self.updateChecksChanged.emit(val)

    @Property(bool, notify=supressErrorsChanged)
    def supress_errors(self) -> bool:
        return self.get_bool("Misc/supress_errors", False)

    @supress_errors.setter
    def supress_errors(self, val):
        if val != self.supress_errors:
            self._settings.setValue("Misc/supress_errors", val)
            self.supressErrorsChanged.emit(val)

    @Property(bool, notify=networkLoggingChanged)
    def enable_logging(self) -> bool:
        return self.get_bool("Misc/network_logging", False)

    @enable_logging.setter
    def enable_logging(self, val):
        if val != self.enable_logging:
            self._settings.setValue("Misc/network_logging", val)
            self.networkLoggingChanged.emit(val)

    @Property(bool, notify=trustEnvironmentChanged)
    def trust_environment(self) -> bool:
        return self.get_bool("Misc/trust_environment", False)

    @trust_environment.setter
    def trust_environment(self, val):
        if val != self.trust_environment:
            self._settings.setValue("Misc/trust_environment", val)
            self.trustEnvironmentChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(bool, notify=debugModeChanged)
    def debug_mode(self) -> bool:
        return self.get_bool("Misc/debug_mode", False)

    @debug_mode.setter
    def debug_mode(self, val):
        if val != self.debug_mode:
            self._settings.setValue("Misc/debug_mode", val)
            self.debugModeChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(int, notify=logLevelChanged) # Can't be changed dynamically
    def log_level(self) -> int:
        return self.get_int("Misc/log_level", 0)

    @log_level.setter
    def log_level(self, val):
        if val != self.log_level:
            self._settings.setValue("Misc/log_level", val)
            self.logLevelChanged.emit(val)

    @Property(str, notify=httpVersionChanged)
    def http_version(self) -> str:
        return self.get_str("Misc/http_version", "v2")

    @http_version.setter
    def http_version(self, val):
        if val != self.http_version:
            self._settings.setValue("Misc/http_version", val)
            self.httpVersionChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(str, notify=impersonationChanged)
    def impersonation(self) -> str:
        return self.get_str("Misc/impersonation", "chrome")

    @impersonation.setter
    def impersonation(self, val):
        if val != self.impersonation:
            self._settings.setValue("Misc/impersonation", val)
            self.impersonationChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(str, notify=customJA3Changed)
    def custom_ja3(self) -> str:
        return self.get_str("Misc/custom_ja3", "")

    @custom_ja3.setter
    def custom_ja3(self, val):
        if val != self.custom_ja3:
            self._settings.setValue("Misc/custom_ja3", val)
            self.customJA3Changed.emit(val)
            self.reloadClients.emit(val)

    @Property(str, notify=interfaceChanged)
    def interface(self) -> str:
        return self.get_str("Misc/interface", "")

    @interface.setter
    def interface(self, val):
        if val != self.interface:
            self._settings.setValue("Misc/interface", val)
            self.interfaceChanged.emit(val)
            self.reloadClients.emit(val)

    # Privacy Settings

    @Property(bool, notify=anonymousModeChanged)
    def anonymous_mode(self) -> bool:
        return self.get_bool("Privacy/anonymous_mode", False)

    @anonymous_mode.setter
    def anonymous_mode(self, val):
        if val != self.anonymous_mode:
            self._settings.setValue("Privacy/anonymous_mode", val)
            self.anonymousModeChanged.emit(val)

    @Property(bool, notify=encryptedCHChanged)
    def encrypted_ch(self) -> bool:
        return self.get_bool("Privacy/encrypted_ch", True)

    @encrypted_ch.setter
    def encrypted_ch(self, val):
        if val != self.encrypted_ch:
            self._settings.setValue("Privacy/encrypted_ch", val)
            self.encryptedCHChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(bool, notify=dnsOverHTTPSChanged)
    def dns_over_https(self) -> bool:
        return self.get_bool("Privacy/dns_over_https", True)

    @dns_over_https.setter
    def dns_over_https(self, val):
        if val != self.dns_over_https:
            self._settings.setValue("Privacy/dns_over_https", val)
            self.dnsOverHTTPSChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(bool, notify=enableTorChanged)
    def enable_tor(self) -> bool:
        return self.get_bool("Privacy/enable_tor", False)

    @enable_tor.setter
    def enable_tor(self, val):
        if val != self.enable_tor:
            self._settings.setValue("Privacy/enable_tor", val)
            self.enableTorChanged.emit(val)
            self.restartRequired.emit()

    @Property(bool, notify=enableTorServerRoutingChanged)
    def enable_tor_server_routing(self):
        return self.get_bool("Privacy/enable_tor_server_routing", True)

    @enable_tor_server_routing.setter
    def enable_tor_server_routing(self, val):
        if val != self.enable_tor_server_routing:
            self._settings.setValue("Privacy/enable_tor_server_routing", val)
            self.enableTorServerRoutingChanged.emit(val)
            self.restartRequired.emit()

    @Property(str, notify=dnsServerChanged)
    def dns_server(self) -> str:
        return self.get_str("Privacy/dns_server", "https://dns.mullvad.net/dns-query")

    @dns_server.setter
    def dns_server(self, val):
        if val != self.dns_server:
            self._settings.setValue("Privacy/dns_server", val)
            self.dnsServerChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(str, notify=fallbackDNSChanged)
    def fallback_dns(self) -> str:
        return self.get_str("Privacy/fallback_dns", "https://dns.quad9.net/dns-query")

    @fallback_dns.setter
    def fallback_dns(self, val):
        if val != self.fallback_dns:
            self._settings.setValue("Privacy/fallback_dns", val)
            self.fallbackDNSChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(bool, notify=sniObfuscationChanged)
    def sni_obfuscation(self) -> bool:
        return self.get_bool("Privacy/sni_obfuscation", False)

    @sni_obfuscation.setter
    def sni_obfuscation(self, val):
        if val != self.sni_obfuscation:
            if val and not (self.sni_obfuscation_lite or self.sni_obfuscation_strict):
                self._settings.setValue("Privacy/sni_obfuscation_lite", True)
                self.sniObfuscationLiteChanged.emit(True)
            self._settings.setValue("Privacy/sni_obfuscation", val)
            self.sniObfuscationChanged.emit(val)
            self.restartRequired.emit()

    @Property(bool, notify=sniObfuscationLiteChanged)
    def sni_obfuscation_lite(self) -> bool:
        return self.get_bool("Privacy/sni_obfuscation_lite", False)

    @sni_obfuscation_lite.setter
    def sni_obfuscation_lite(self, val):
        val = bool(val)
        if val:
            self._set_sni_obfuscation_mode("lite")
        elif self.sni_obfuscation_lite:
            self._settings.setValue("Privacy/sni_obfuscation_lite", False)
            self._settings.sync()
            self.sniObfuscationLiteChanged.emit(False)
            self.restartRequired.emit()

    @Property(bool, notify=sniObfuscationStrictChanged)
    def sni_obfuscation_strict(self) -> bool:
        return self.get_bool("Privacy/sni_obfuscation_strict", False)

    @sni_obfuscation_strict.setter
    def sni_obfuscation_strict(self, val):
        val = bool(val)
        if val:
            self._set_sni_obfuscation_mode("strict")
        elif self.sni_obfuscation_strict:
            self._settings.setValue("Privacy/sni_obfuscation_strict", False)
            self._settings.sync()
            self.sniObfuscationStrictChanged.emit(False)
            self.restartRequired.emit()

    @Property(str, notify=sniObfuscationStrictProfileChanged)
    def sni_obfuscation_strict_profile(self) -> str:
        return self.get_str("Privacy/sni_obfuscation_strict_profile", "Strict Fragmentation")

    @sni_obfuscation_strict_profile.setter
    def sni_obfuscation_strict_profile(self, val):
        if val != self.sni_obfuscation_strict_profile:
            self._settings.setValue("Privacy/sni_obfuscation_strict_profile", val)
            self.sniObfuscationStrictProfileChanged.emit(val)
            self.restartRequired.emit()


    @Property(str, notify=proxyChanged)
    def proxy(self) -> str:
        return self.get_str("Privacy/proxy", "")

    @proxy.setter
    def proxy(self, val):
        if val != self.proxy:
            self._settings.setValue("Privacy/proxy", val)
            self.proxyChanged.emit(val)
            self.reloadClients.emit(val)

    @Property(bool, notify=proxySSLVerificationChanged)
    def proxy_ssl_verification(self) -> bool:
        return self.get_bool("Privacy/proxy_ssl_verification", True)

    @proxy_ssl_verification.setter
    def proxy_ssl_verification(self, val):
        if val != self.proxy_ssl_verification:
            self._settings.setValue("Privacy/proxy_ssl_verification", val)
            self.proxySSLVerificationChanged.emit(val)
            self.reloadClients.emit(val)

    def apply_proxy_settings(self, proxy_url: str, verify_ssl: bool) -> None:
        """Atomically persist proxy settings and rebuild clients exactly once."""

        proxy_changed = proxy_url != self.proxy
        verification_changed = verify_ssl != self.proxy_ssl_verification
        if not (proxy_changed or verification_changed):
            return
        self._settings.setValue("Privacy/proxy", proxy_url)
        self._settings.setValue("Privacy/proxy_ssl_verification", verify_ssl)
        if proxy_changed:
            # SNIProxyManager receives this before reloadClients and rebuilds its
            # upstream chain so the new local URL is ready for fresh sessions.
            self.proxyChanged.emit(proxy_url)
        if verification_changed:
            self.proxySSLVerificationChanged.emit(verify_ssl)
        self.reloadClients.emit(proxy_url)

    # UI Settings

    @Property(int, notify=languageChanged)
    def language(self) -> int:
        return self.get_int("UI/language", 0)

    @language.setter
    def language(self, val):
        if val != self.language:
            self._settings.setValue("UI/language", val)
            self.languageChanged.emit(val)

    @Property(int, notify=fontSizeChanged)
    def font_size(self) -> int:
        return self.get_int("UI/font_size", 12)

    @font_size.setter
    def font_size(self, val):
        if val != self.font_size:
            self._settings.setValue("UI/font_size", val)

            self.fontSizeChanged.emit(val)
            self._apply_global_font(val)

    def _apply_global_font(self, size: int):
        app = QGuiApplication.instance()
        if app:
            font = app.font()
            font.setPointSize(size)
            app.setFont(font)

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

app_settings = SettingsManager() # Singleton instance shared globally :)
