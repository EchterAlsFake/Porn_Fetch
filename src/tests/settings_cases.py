"""Explicit desktop settings inventory; no Qt startup or network on import."""
from dataclasses import dataclass


@dataclass(frozen=True)
class SettingCase:
    control: str
    prop: str
    key: str
    kind: str
    values: tuple
    runtime: str = ""
    group: str = ""
    tab: int = 0


def case(control, prop, section, kind, values, runtime="", group="", tab=0):
    key = {"parallel_downloads": "semaphore", "enable_logging": "network_logging"}.get(prop, prop)
    return SettingCase(control, prop, f"{section}/{key}", kind, values, runtime, group or prop, tab)


SETTINGS = (
    case("defaultQualityCombo", "quality", "Video", "combo", (8, 11), group="media"),
    case("modelVideosCombo", "model_videos", "Video", "combo", (1, 2), group="profiles"),
    case("contentLanguageComboBox", "locale", "Video", "locale", ("de-DE", "fr-FR"), "locale", "locale"),
    case("strictEnforcementCheckBox", "strict_enforcement", "Video", "check", (True, False), group="profiles"),
    case("resultLimitSpinBox", "result_limit", "Video", "spin", (1, 2), group="profiles"),
    case("outputPathInput", "output_path", "Video", "path", ("output-a", "output-b"), group="media"),
    case("writeMetadataCheckBox", "write_metadata", "Video", "check", (False, True), group="media"),
    case("skipExistingFilesCheckBox", "skip_existing_files", "Video", "check", (False, True), group="media"),
    case("trackVideosCheckBox", "track_videos", "Video", "check", (True, False), group="database"),
    case("databasePathInput", "pocketbase_data_path", "Video", "path", ("database-a", "database-b"), group="database"),
    case("downloadWorkersSpinBox", "download_workers", "Performance", "spin", (1, 2), "max_workers_download", "workers", 1),
    case("networkDelaySpinBox", "network_delay", "Performance", "spin", (1, 0), "request_delay", "delay", 1),
    case("parallelDownloadsSpinBox", "parallel_downloads", "Performance", "spin", (2, 1), group="parallel", tab=1),
    case("retriesSpinBox", "retries", "Performance", "spin", (2, 1), "request_attempts", "retry", 1),
    case("timeoutSpinBox", "timeout", "Performance", "spin", (1, 2), "timeout", "timeout", 1),
    case("processingDelaySpinBox", "processing_delay", "Performance", "spin", (1, 0), group="processing", tab=1),
    case("speedLimitSpinBox", "speed_limit", "Performance", "decimal", (0.5, 1.0), "max_bandwidth_mb", "speed", 1),
    case("videosConcurrencySpinBox", "videos_concurrency", "Performance", "spin", (1, 2), "videos_concurrency", "profiles", 1),
    case("pagesConcurrencySpinBox", "pages_concurrency", "Performance", "spin", (1, 2), "pages_concurrency", "profiles", 1),
    case("responseCacheSizeSpinBox", "response_cache_size", "Performance", "spin", (0, 1), "response_cache_size_bytes", "cache", 1),
    case("responseCacheTTLSpinBox", "response_cache_ttl", "Performance", "spin", (1, 2), "response_cache_ttl", "cache", 1),
    case("segmentCacheSizeSpinBox", "segment_cache_size", "Performance", "spin", (0, 1), "segment_cache_size_bytes", "cache", 1),
    case("segmentCacheTTLSpinBox", "segment_cache_ttl", "Performance", "spin", (1, 2), "segment_cache_ttl", "cache", 1),
    case("requestInitialRetryDelaySpinBox", "request_initial_retry_delay", "Performance", "decimal", (0.05, 0.1), "request_retry_initial_delay", "retry", 1),
    case("requestRetryMaxDelaySpinBox", "request_retry_max_delay", "Performance", "decimal", (0.2, 0.3), "request_retry_max_delay", "retry", 1),
    case("requestRetryMultiplierSpinBox", "request_retry_multiplier", "Performance", "decimal", (3.0, 2.0), "request_multiplier", "retry", 1),
    case("requestRetryJitterSpinBox", "request_retry_jitter", "Performance", "decimal", (0.0, 0.01), "request_retry_jitter", "retry", 1),
    case("updateChecksCheckBox", "update_checks", "Misc", "check", (False, True), group="updates", tab=2),
    case("supressErrorsCheckBox", "supress_errors", "Misc", "check", (True, False), group="errors", tab=2),
    case("enableLoggingCheckBox", "enable_logging", "Misc", "check", (True, False), group="errors", tab=2),
    case("trustEnvironmentCheckBox", "trust_environment", "Misc", "check", (True, False), "trust_env", "network", 2),
    case("debugModeCheckBox", "debug_mode", "Misc", "check", (True, False), group="logging", tab=2),
    case("logLevelComboBox", "log_level", "Misc", "combo", (2, 3), group="logging", tab=2),
    case("httpVersionInput", "http_version", "Misc", "text", ("v1", "v2"), "http_version", "network", 2),
    case("impersonationInput", "impersonation", "Misc", "text", ("safari", "chrome"), "impersonation", "network", 2),
    case("customJA3Input", "custom_ja3", "Misc", "text", ("771,4865-4866-4867,0-23-65281-10-11,29-23-24,0", ""), "custom_ja3", "tls", 2),
    case("interfaceInput", "interface", "Misc", "text", ("127.0.0.1", ""), "interface", "network", 2),
    case("anonymousModeCheckBox", "anonymous_mode", "Privacy", "check", (True, False), group="ui", tab=3),
    case("encryptedCHCheckBox", "encrypted_ch", "Privacy", "check", (False, True), group="tls", tab=3),
    case("dnsOverHTTPSCheckBox", "dns_over_https", "Privacy", "check", (False, True), group="dns", tab=3),
    case("torRoutingComboBox", "service_transport", "Privacy", "tor", ("tor", "tor_all", "direct"), "service_transport", "tor", 3),
    case("dnsPrimaryInput", "dns_server", "Privacy", "text", ("https://cloudflare-dns.com/dns-query", "https://dns.quad9.net/dns-query"), group="dns", tab=3),
    case("dnsFallbackInput", "fallback_dns", "Privacy", "text", ("https://cloudflare-dns.com/dns-query", "https://dns.quad9.net/dns-query"), group="dns", tab=3),
    case("sniObfuscationCheckBox", "sni_obfuscation", "Privacy", "check", (True, False), group="sni", tab=3),
    case("sniLiteRadio", "sni_obfuscation_lite", "Privacy", "radio", (True,), group="sni", tab=3),
    case("sniStrictRadio", "sni_obfuscation_strict", "Privacy", "radio", (True,), group="strict", tab=3),
    case("strictProfileCombo", "sni_obfuscation_strict_profile", "Privacy", "profile", ("Strict Reverse", "Strict Desync", "Strict Fragmentation"), group="strict", tab=3),
    case("proxyWindow", "proxy", "Privacy", "proxy", ("http://127.0.0.1:9", ""), "proxy", "network", 3),
    case("proxyWindow", "proxy_ssl_verification", "Privacy", "ssl", (False, True), "verify_ssl", "tls", 3),
    case("guiLanguageComboBox", "language", "UI", "combo", (2, 1), group="translation", tab=4),
    case("fontSizeSpinBox", "font_size", "UI", "spin", (16, 12), group="ui", tab=4),
    case("coreStyleComboBox", "core_style", "UI", "style", ("Fusion", "Material"), group="style", tab=4),
    case("darkModeSwitch", "dark_mode", "UI", "switch", (False, True), group="ui", tab=4),
    case("activityGlowSwitch", "activity_glow_enabled", "UI", "switch", (False, True), group="ui", tab=4),
    case("accentColorComboBox", "accent_color", "UI", "accent", ("#f44336", "#4caf50"), group="ui", tab=4),
)
CASE_BY_PROPERTY = {setting.prop: setting for setting in SETTINGS}
