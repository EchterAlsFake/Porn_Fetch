from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PySide6.QtCore import QSettings, QUrl

from src.backend.config import SettingsManager


class TestSettingsManagerComprehensive(unittest.TestCase):
    """Direct unit tests for 100% branch and edge-case coverage on SettingsManager."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.ini_path = Path(self.temp_dir.name) / "manager_test.ini"
        self.qsettings = QSettings(str(self.ini_path), QSettings.Format.IniFormat)
        self.manager = SettingsManager(self.qsettings)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_getters_with_type_fallbacks(self) -> None:
        # get_bool
        self.manager._settings.setValue("Test/bool_true", True)
        self.manager._settings.setValue("Test/bool_str_true", "True")
        self.manager._settings.setValue("Test/bool_str_false", "false")
        self.manager._settings.setValue("Test/bool_int", 1)
        self.assertTrue(self.manager.get_bool("Test/bool_true"))
        self.assertTrue(self.manager.get_bool("Test/bool_str_true"))
        self.assertFalse(self.manager.get_bool("Test/bool_str_false"))
        self.assertTrue(self.manager.get_bool("Test/bool_int"))
        self.assertFalse(self.manager.get_bool("Test/non_existent", False))
        self.assertTrue(self.manager.get_bool("Test/non_existent", True))

        # get_int
        self.manager._settings.setValue("Test/int_val", 42)
        self.manager._settings.setValue("Test/int_str", "100")
        self.manager._settings.setValue("Test/int_invalid", "not_a_number")
        self.assertEqual(self.manager.get_int("Test/int_val"), 42)
        self.assertEqual(self.manager.get_int("Test/int_str"), 100)
        self.assertEqual(self.manager.get_int("Test/int_invalid", 7), 7)
        self.assertEqual(self.manager.get_int("Test/missing", 99), 99)

        # get_float
        self.manager._settings.setValue("Test/float_val", 3.14)
        self.manager._settings.setValue("Test/float_str", "2.718")
        self.manager._settings.setValue("Test/float_invalid", "not_float")
        self.assertAlmostEqual(self.manager.get_float("Test/float_val"), 3.14)
        self.assertAlmostEqual(self.manager.get_float("Test/float_str"), 2.718)
        self.assertAlmostEqual(self.manager.get_float("Test/float_invalid", 1.23), 1.23)
        self.assertAlmostEqual(self.manager.get_float("Test/missing", 0.5), 0.5)

        # get_str
        self.manager._settings.setValue("Test/str_val", "hello")
        self.assertEqual(self.manager.get_str("Test/str_val"), "hello")
        self.assertEqual(self.manager.get_str("Test/missing", "default_str"), "default_str")

    def test_path_helpers(self) -> None:
        url = self.manager.path_to_file_url("/tmp/test/path")
        self.assertTrue(url.isLocalFile())
        self.assertIn("test/path", url.toLocalFile())

        parent_url = self.manager.parent_directory_url("/tmp/test/path/file.txt")
        self.assertTrue(parent_url.isLocalFile())
        self.assertIn("test/path", parent_url.toLocalFile())

        local = self.manager.local_path_from_url(QUrl.fromLocalFile("/tmp/sample"))
        self.assertTrue(local.endswith("sample"))

        empty_local = self.manager.local_path_from_url(QUrl(""))
        self.assertEqual(empty_local, "")

    def test_no_op_setters_when_value_unchanged(self) -> None:
        """Verifies that setting a property to its current value does not re-emit signals."""
        signals_emitted = []
        self.manager.qualityChanged.connect(lambda v: signals_emitted.append("quality"))
        self.manager.modelVideosChanged.connect(lambda v: signals_emitted.append("model_videos"))
        self.manager.localeChanged.connect(lambda v: signals_emitted.append("locale"))
        self.manager.strictEnforcementChanged.connect(lambda v: signals_emitted.append("strict_enforcement"))
        self.manager.resultLimitChanged.connect(lambda v: signals_emitted.append("result_limit"))
        self.manager.outputPathChanged.connect(lambda v: signals_emitted.append("output_path"))
        self.manager.writeMetadataChanged.connect(lambda v: signals_emitted.append("write_metadata"))
        self.manager.skipExistingFilesChanged.connect(lambda v: signals_emitted.append("skip_existing_files"))
        self.manager.trackVideosChanged.connect(lambda v: signals_emitted.append("track_videos"))
        self.manager.pocketbaseDataPathChanged.connect(lambda v: signals_emitted.append("pocketbase_data_path"))
        self.manager.downloadWorkersChanged.connect(lambda v: signals_emitted.append("download_workers"))
        self.manager.networkDelayChanged.connect(lambda v: signals_emitted.append("network_delay"))
        self.manager.parallelDownloadsChanged.connect(lambda v: signals_emitted.append("parallel_downloads"))
        self.manager.retriesChanged.connect(lambda v: signals_emitted.append("retries"))
        self.manager.timeoutChanged.connect(lambda v: signals_emitted.append("timeout"))
        self.manager.processingDelayChanged.connect(lambda v: signals_emitted.append("processing_delay"))
        self.manager.speedLimitChanged.connect(lambda v: signals_emitted.append("speed_limit"))
        self.manager.videosConcurrencyChanged.connect(lambda v: signals_emitted.append("videos_concurrency"))
        self.manager.pagesConcurrencyChanged.connect(lambda v: signals_emitted.append("pages_concurrency"))
        self.manager.responseCacheSizeChanged.connect(lambda v: signals_emitted.append("response_cache_size"))
        self.manager.responseCacheTTLChanged.connect(lambda v: signals_emitted.append("response_cache_ttl"))
        self.manager.segmentCacheSizeChanged.connect(lambda v: signals_emitted.append("segment_cache_size"))
        self.manager.segmentCacheTTLChanged.connect(lambda v: signals_emitted.append("segment_cache_ttl"))
        self.manager.requestInitialRetryDelayChanged.connect(lambda v: signals_emitted.append("request_initial_retry_delay"))
        self.manager.requestRetryMaxDelayChanged.connect(lambda v: signals_emitted.append("request_retry_max_delay"))
        self.manager.requestRetryMultiplierChanged.connect(lambda v: signals_emitted.append("request_retry_multiplier"))
        self.manager.requestRetryJitterChanged.connect(lambda v: signals_emitted.append("request_retry_jitter"))
        self.manager.updateChecksChanged.connect(lambda v: signals_emitted.append("update_checks"))
        self.manager.supressErrorsChanged.connect(lambda v: signals_emitted.append("supress_errors"))
        self.manager.trustEnvironmentChanged.connect(lambda v: signals_emitted.append("trust_environment"))
        self.manager.debugModeChanged.connect(lambda v: signals_emitted.append("debug_mode"))
        self.manager.logLevelChanged.connect(lambda v: signals_emitted.append("log_level"))
        self.manager.httpVersionChanged.connect(lambda v: signals_emitted.append("http_version"))
        self.manager.impersonationChanged.connect(lambda v: signals_emitted.append("impersonation"))
        self.manager.customJA3Changed.connect(lambda v: signals_emitted.append("custom_ja3"))
        self.manager.interfaceChanged.connect(lambda v: signals_emitted.append("interface"))
        self.manager.anonymousModeChanged.connect(lambda v: signals_emitted.append("anonymous_mode"))
        self.manager.encryptedCHChanged.connect(lambda v: signals_emitted.append("encrypted_ch"))
        self.manager.dnsOverHTTPSChanged.connect(lambda v: signals_emitted.append("dns_over_https"))
        self.manager.enableTorChanged.connect(lambda v: signals_emitted.append("enable_tor"))
        self.manager.enableTorServerRoutingChanged.connect(lambda v: signals_emitted.append("enable_tor_server_routing"))
        self.manager.dnsServerChanged.connect(lambda v: signals_emitted.append("dns_server"))
        self.manager.fallbackDNSChanged.connect(lambda v: signals_emitted.append("fallback_dns"))
        self.manager.sniObfuscationChanged.connect(lambda v: signals_emitted.append("sni_obfuscation"))
        self.manager.sniObfuscationStrictProfileChanged.connect(lambda v: signals_emitted.append("sni_obfuscation_strict_profile"))
        self.manager.proxyChanged.connect(lambda v: signals_emitted.append("proxy"))
        self.manager.proxySSLVerificationChanged.connect(lambda v: signals_emitted.append("proxy_ssl_verification"))
        self.manager.languageChanged.connect(lambda v: signals_emitted.append("language"))
        self.manager.fontSizeChanged.connect(lambda v: signals_emitted.append("font_size"))
        self.manager.coreStyleChanged.connect(lambda v: signals_emitted.append("core_style"))
        self.manager.darkModeChanged.connect(lambda v: signals_emitted.append("dark_mode"))
        self.manager.accentColorChanged.connect(lambda v: signals_emitted.append("accent_color"))

        # Re-assign current values
        self.manager.quality = self.manager.quality
        self.manager.model_videos = self.manager.model_videos
        self.manager.locale = self.manager.locale
        self.manager.strict_enforcement = self.manager.strict_enforcement
        self.manager.result_limit = self.manager.result_limit
        self.manager.output_path = self.manager.output_path
        self.manager.write_metadata = self.manager.write_metadata
        self.manager.skip_existing_files = self.manager.skip_existing_files
        self.manager.track_videos = self.manager.track_videos
        self.manager.pocketbase_data_path = self.manager.pocketbase_data_path
        self.manager.download_workers = self.manager.download_workers
        self.manager.network_delay = self.manager.network_delay
        self.manager.parallel_downloads = self.manager.parallel_downloads
        self.manager.retries = self.manager.retries
        self.manager.timeout = self.manager.timeout
        self.manager.processing_delay = self.manager.processing_delay
        self.manager.speed_limit = self.manager.speed_limit
        self.manager.videos_concurrency = self.manager.videos_concurrency
        self.manager.pages_concurrency = self.manager.pages_concurrency
        self.manager.response_cache_size = self.manager.response_cache_size
        self.manager.response_cache_ttl = self.manager.response_cache_ttl
        self.manager.segment_cache_size = self.manager.segment_cache_size
        self.manager.segment_cache_ttl = self.manager.segment_cache_ttl
        self.manager.request_initial_retry_delay = self.manager.request_initial_retry_delay
        self.manager.request_retry_max_delay = self.manager.request_retry_max_delay
        self.manager.request_retry_multiplier = self.manager.request_retry_multiplier
        self.manager.request_retry_jitter = self.manager.request_retry_jitter
        self.manager.update_checks = self.manager.update_checks
        self.manager.supress_errors = self.manager.supress_errors
        self.manager.trust_environment = self.manager.trust_environment
        self.manager.debug_mode = self.manager.debug_mode
        self.manager.log_level = self.manager.log_level
        self.manager.http_version = self.manager.http_version
        self.manager.impersonation = self.manager.impersonation
        self.manager.custom_ja3 = self.manager.custom_ja3
        self.manager.interface = self.manager.interface
        self.manager.anonymous_mode = self.manager.anonymous_mode
        self.manager.encrypted_ch = self.manager.encrypted_ch
        self.manager.dns_over_https = self.manager.dns_over_https
        self.manager.enable_tor = self.manager.enable_tor
        self.manager.enable_tor_server_routing = self.manager.enable_tor_server_routing
        self.manager.dns_server = self.manager.dns_server
        self.manager.fallback_dns = self.manager.fallback_dns
        self.manager.sni_obfuscation = self.manager.sni_obfuscation
        self.manager.sni_obfuscation_strict_profile = self.manager.sni_obfuscation_strict_profile
        self.manager.proxy = self.manager.proxy
        self.manager.proxy_ssl_verification = self.manager.proxy_ssl_verification
        self.manager.language = self.manager.language
        self.manager.font_size = self.manager.font_size
        self.manager.core_style = self.manager.core_style
        self.manager.dark_mode = self.manager.dark_mode
        self.manager.accent_color = self.manager.accent_color

        self.assertEqual(signals_emitted, [], f"No signals should be emitted on identical assignments: {signals_emitted}")

    def test_sni_modes_and_error_handling(self) -> None:
        # Invalid mode raises ValueError
        with self.assertRaises(ValueError):
            self.manager.set_sni_obfuscation_mode("invalid_mode")

        # Switching to lite when already lite is a no-op
        self.manager.set_sni_obfuscation_mode("lite")
        self.manager.set_sni_obfuscation_mode("lite")

        # Setting sni_obfuscation_lite directly
        self.manager.sni_obfuscation_lite = True
        self.assertTrue(self.manager.sni_obfuscation_lite)
        self.assertFalse(self.manager.sni_obfuscation_strict)

        self.manager.sni_obfuscation_lite = False
        self.assertFalse(self.manager.sni_obfuscation_lite)

        # Setting sni_obfuscation_strict directly
        self.manager.sni_obfuscation_strict = True
        self.assertTrue(self.manager.sni_obfuscation_strict)
        self.assertFalse(self.manager.sni_obfuscation_lite)

        self.manager.sni_obfuscation_strict = False
        self.assertFalse(self.manager.sni_obfuscation_strict)

    def test_error_reporting_consent_and_logging(self) -> None:
        self.assertFalse(self.manager.error_reporting_decided)
        self.assertFalse(self.manager.enable_logging)

        # First explicit consent
        self.manager.set_error_reporting_consent(True)
        self.assertTrue(self.manager.error_reporting_decided)
        self.assertTrue(self.manager.enable_logging)

        # Changing consent
        self.manager.set_error_reporting_consent(False)
        self.assertFalse(self.manager.enable_logging)

        # enable_logging setter when decided
        self.manager.enable_logging = True
        self.assertTrue(self.manager.enable_logging)

    def test_apply_proxy_settings_variations(self) -> None:
        # No-op when unchanged
        self.manager.apply_proxy_settings(self.manager.proxy, self.manager.proxy_ssl_verification)

        # Proxy only change
        self.manager.apply_proxy_settings("http://test.local:8080", self.manager.proxy_ssl_verification)
        self.assertEqual(self.manager.proxy, "http://test.local:8080")

        # SSL verification only change
        self.manager.apply_proxy_settings("http://test.local:8080", False)
        self.assertFalse(self.manager.proxy_ssl_verification)

        # Both change
        self.manager.apply_proxy_settings("socks5://10.0.0.1:9050", True)
        self.assertEqual(self.manager.proxy, "socks5://10.0.0.1:9050")
        self.assertTrue(self.manager.proxy_ssl_verification)

    def test_legacy_database_path_and_refresh(self) -> None:
        self.assertEqual(self.manager.legacy_database_path, "./downloads.db")
        self.manager.refresh()
        self.manager.sync()

    def test_set_settings_storage(self) -> None:
        new_ini = Path(self.temp_dir.name) / "new_store.ini"
        new_qs = QSettings(str(new_ini), QSettings.Format.IniFormat)
        self.manager.set_settings_storage(new_qs)
        self.manager.result_limit = 300
        self.manager.sync()
        self.assertTrue(new_ini.exists())
        self.assertIn("result_limit=300", new_ini.read_text())

    def test_proxy_and_ssl_direct_setters(self) -> None:
        self.manager.proxy = "http://direct.proxy:8080"
        self.assertEqual(self.manager.proxy, "http://direct.proxy:8080")
        # No-op re-assignment
        self.manager.proxy = "http://direct.proxy:8080"

        self.manager.proxy_ssl_verification = False
        self.assertFalse(self.manager.proxy_ssl_verification)
        # No-op re-assignment
        self.manager.proxy_ssl_verification = False

    def test_sni_normalization_branches(self) -> None:
        # Branch 1: both lite and strict are True -> lite should be forced to False
        self.qsettings.setValue("Privacy/sni_obfuscation_lite", True)
        self.qsettings.setValue("Privacy/sni_obfuscation_strict", True)
        self.manager._normalize_sni_obfuscation_mode()
        self.assertFalse(self.manager.get_bool("Privacy/sni_obfuscation_lite", False))
        self.assertTrue(self.manager.get_bool("Privacy/sni_obfuscation_strict", False))

        # Branch 2: sni_obfuscation enabled but neither lite nor strict is set -> lite should be set to True
        self.qsettings.setValue("Privacy/sni_obfuscation", True)
        self.qsettings.setValue("Privacy/sni_obfuscation_lite", False)
        self.qsettings.setValue("Privacy/sni_obfuscation_strict", False)
        self.manager._normalize_sni_obfuscation_mode()
        self.assertTrue(self.manager.get_bool("Privacy/sni_obfuscation_lite", False))

    def test_default_settings_manager_refresh(self) -> None:
        temp_ini = Path(self.temp_dir.name) / "default_test.ini"
        default_qs = QSettings(str(temp_ini), QSettings.Format.IniFormat)
        # Create a manager without custom_settings passed to __init__
        with patch("src.backend.config.QSettings", return_value=default_qs):
            sm = SettingsManager()
            self.assertIsNone(sm._custom_settings)
            sm.refresh()

    def test_get_str_none_fallback(self) -> None:
        with patch.object(self.qsettings, "value", return_value=None):
            self.assertEqual(self.manager.get_str("NonExistentKey", "my_default"), "my_default")


if __name__ == "__main__":
    unittest.main()
