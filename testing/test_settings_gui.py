from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["PORN_FETCH_TEST_ENV"] = "1"

from PySide6.QtCore import QObject, Property, QSettings, QUrl, Signal, Slot
from PySide6.QtGui import QGuiApplication, QAccessible
from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent
from PySide6.QtQuickControls2 import QQuickStyle

from src.backend.config import SettingsManager, __org_name__, __app_name__
from src.frontend.UI import resources

resources.qInitResources()
QQuickStyle.setStyle("Material")

# Ensure singleton QGuiApplication exists
_app = QGuiApplication.instance() or QGuiApplication([])


class _TestBackend(QObject):
    proxyTestSucceeded = Signal(str, dict)
    proxyTestFailed = Signal(str, str)
    proxySslError = Signal(str, str)

    def __init__(self, settings_manager: SettingsManager, bridge: _TestBridge | None = None) -> None:
        super().__init__()
        self.settings = settings_manager
        self.bridge = bridge

    @Property(str, constant=True)
    def errorReportDisclosure(self) -> str:
        return "Test Disclosure"

    @Slot(int)
    def set_default_quality(self, index: int) -> None:
        quality = self.settings.mappings_quality.get(index)
        if quality is None:
            return
        requires_license = index in (0, 1, 3, 4, 5)
        if requires_license and not (self.bridge and self.bridge.isPremium):
            return
        self.settings.quality = index

    @Slot(str, bool)
    def testProxy(self, proxy_url: str, verify_ssl: bool) -> None:
        pass

    @Slot(str, bool)
    def applyProxy(self, proxy_url: str, verify_ssl: bool) -> None:
        self.settings.apply_proxy_settings(proxy_url, verify_ssl)

    @Slot()
    def reset_pornfetch(self) -> None:
        self.settings.reset()

    @Slot()
    def clear_temporary_files(self) -> None:
        pass


class _TestBridge(QObject):
    def __init__(self, premium: bool = True) -> None:
        super().__init__()
        self._is_premium = premium

    @Property(bool, constant=True)
    def isPremium(self) -> bool:
        return self._is_premium

    def set_premium(self, premium: bool) -> None:
        self._is_premium = premium


class SettingsGUITestBase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.ini_path = Path(self.temp_dir.name) / "test_settings.ini"
        self.qsettings = QSettings(str(self.ini_path), QSettings.Format.IniFormat)
        self.settings_manager = SettingsManager(self.qsettings)
        self.bridge = _TestBridge(premium=True)
        self.backend = _TestBackend(self.settings_manager, self.bridge)

        self.engine = QQmlApplicationEngine()
        self.engine.rootContext().setContextProperty("appSettings", self.settings_manager)
        self.engine.rootContext().setContextProperty("backend", self.backend)
        self.engine.rootContext().setContextProperty("bridge", self.bridge)

        ui_dir = Path("src/frontend/UI").resolve()
        self.engine.addImportPath(str(ui_dir))

        qml_path = ui_dir / "SettingsPage.qml"
        self.component = QQmlComponent(self.engine, QUrl.fromLocalFile(str(qml_path)))
        if self.component.isError():
            errors = "\n".join(e.toString() for e in self.component.errors())
            self.fail(f"Failed to load SettingsPage.qml:\n{errors}")

        self.root = self.component.create()
        self.assertIsNotNone(self.root, "SettingsPage root item should not be None")

    def tearDown(self) -> None:
        del self.root
        del self.component
        del self.engine
        del self.backend
        del self.bridge
        del self.settings_manager
        del self.qsettings
        self.temp_dir.cleanup()

    # --- Simulation helpers ---

    def find_control(self, name: str) -> QObject:
        item = self.root.findChild(QObject, name)
        self.assertIsNotNone(item, f"Control with objectName '{name}' not found")
        return item

    def simulate_combobox(self, name: str, index: int) -> None:
        combo = self.find_control(name)
        combo.setProperty("currentIndex", index)
        combo.activated.emit(index)

    def simulate_checkbox(self, name: str, checked: bool) -> None:
        cb = self.find_control(name)
        cb.setProperty("checked", checked)
        cb.toggled.emit()

    def simulate_switch(self, name: str, checked: bool) -> None:
        sw = self.find_control(name)
        sw.setProperty("checked", checked)
        sw.toggled.emit()

    def simulate_spinbox(self, name: str, value: int) -> None:
        sb = self.find_control(name)
        sb.setProperty("value", value)
        sb.valueModified.emit()

    def simulate_decimal_spinbox(self, name: str, value: float) -> None:
        dsb = self.find_control(name)
        factor = float(dsb.property("factor") or 100.0)
        dsb.setProperty("value", int(round(value * factor)))
        dsb.valueModified.emit()

    def simulate_textfield(self, name: str, text: str) -> None:
        tf = self.find_control(name)
        tf.setProperty("text", text)
        tf.editingFinished.emit()

    def simulate_radio(self, name: str) -> None:
        radio = self.find_control(name)
        radio.clicked.emit()

    def simulate_folder_dialog(self, name: str, folder_path: str) -> None:
        dlg = self.find_control(name)
        folder_url = QUrl.fromLocalFile(folder_path)
        dlg.setProperty("currentFolder", folder_url)
        dlg.setProperty("selectedFolder", folder_url)
        dlg.accepted.emit()

    def simulate_proxy_acceptance(self, proxy_url: str, verify_ssl: bool) -> None:
        pw = self.find_control("proxyWindow")
        pw.proxyAccepted.emit(proxy_url, verify_ssl)

    def simulate_reset_button(self) -> None:
        btn = self.find_control("resetSettingsButton")
        btn.clicked.emit()

    def read_fresh_settings(self) -> QSettings:
        self.settings_manager.sync()
        return QSettings(str(self.ini_path), QSettings.Format.IniFormat)

    def assert_file_value(self, key: str, expected_value: object) -> None:
        fresh = self.read_fresh_settings()
        val = fresh.value(key)
        if isinstance(expected_value, bool):
            if isinstance(val, str):
                actual_bool = val.lower() == "true"
            else:
                actual_bool = bool(val)
            self.assertEqual(actual_bool, expected_value, f"File key '{key}' was {val!r}, expected {expected_value!r}")
        elif isinstance(expected_value, int):
            self.assertEqual(int(val), expected_value, f"File key '{key}' was {val!r}, expected {expected_value!r}")
        elif isinstance(expected_value, float):
            self.assertAlmostEqual(float(val), expected_value, places=2, msg=f"File key '{key}' was {val!r}, expected {expected_value!r}")
        else:
            self.assertEqual(str(val), str(expected_value), f"File key '{key}' was {val!r}, expected {expected_value!r}")


class TestVideoTabGUI(SettingsGUITestBase):
    """Verifies that every change made on the Video settings tab modifies the actual settings file."""

    def test_quality_combobox_licensed(self) -> None:
        # Index 0 is 'best' (requires license)
        self.simulate_combobox("defaultQualityCombo", 0)
        self.assertEqual(self.settings_manager.quality, 0)
        self.assert_file_value("Video/quality", 0)

        # Index 6 is '720p'
        self.simulate_combobox("defaultQualityCombo", 6)
        self.assertEqual(self.settings_manager.quality, 6)
        self.assert_file_value("Video/quality", 6)

    def test_quality_combobox_unlicensed_enforcement(self) -> None:
        # Unlicensed user attempting premium quality (index 0 'best')
        self.bridge.set_premium(False)
        self.settings_manager.quality = 6
        self.simulate_combobox("defaultQualityCombo", 0)
        # Should stay 6 because premium quality is rejected for unlicensed users
        self.assertEqual(self.settings_manager.quality, 6)
        self.assert_file_value("Video/quality", 6)

        # Unlicensed user selecting non-premium quality (index 8 '480p')
        self.simulate_combobox("defaultQualityCombo", 8)
        self.assertEqual(self.settings_manager.quality, 8)
        self.assert_file_value("Video/quality", 8)

    def test_model_videos_combobox(self) -> None:
        # Index 1: "Uploaded Videos"
        self.simulate_combobox("modelVideosCombo", 1)
        self.assertEqual(self.settings_manager.model_videos, 1)
        self.assert_file_value("Video/model_videos", 1)

        # Index 2: "Featured Videos"
        self.simulate_combobox("modelVideosCombo", 2)
        self.assertEqual(self.settings_manager.model_videos, 2)
        self.assert_file_value("Video/model_videos", 2)

    def test_content_language_combobox(self) -> None:
        # Index 1 is German (de-DE)
        self.simulate_combobox("contentLanguageComboBox", 1)
        self.assertEqual(self.settings_manager.locale, "de-DE")
        self.assert_file_value("Video/locale", "de-DE")

        # Index 5 is French (fr-FR)
        self.simulate_combobox("contentLanguageComboBox", 5)
        self.assertEqual(self.settings_manager.locale, "fr-FR")
        self.assert_file_value("Video/locale", "fr-FR")

    def test_strict_enforcement_checkbox(self) -> None:
        self.simulate_checkbox("strictEnforcementCheckBox", True)
        self.assertTrue(self.settings_manager.strict_enforcement)
        self.assert_file_value("Video/strict_enforcement", True)

        self.simulate_checkbox("strictEnforcementCheckBox", False)
        self.assertFalse(self.settings_manager.strict_enforcement)
        self.assert_file_value("Video/strict_enforcement", False)

    def test_result_limit_spinbox(self) -> None:
        self.simulate_spinbox("resultLimitSpinBox", 120)
        self.assertEqual(self.settings_manager.result_limit, 120)
        self.assert_file_value("Video/result_limit", 120)

    def test_output_path_textfield(self) -> None:
        test_path = "/media/test_downloads"
        self.simulate_textfield("outputPathInput", test_path)
        self.assertEqual(self.settings_manager.output_path, test_path)
        self.assert_file_value("Video/output_path", test_path)

    def test_output_folder_dialog(self) -> None:
        test_path = "/home/user/Videos/PornFetch"
        self.simulate_folder_dialog("outputFolderDialog", test_path)
        self.assertEqual(self.settings_manager.output_path, test_path)
        self.assert_file_value("Video/output_path", test_path)

    def test_write_metadata_checkbox(self) -> None:
        self.simulate_checkbox("writeMetadataCheckBox", False)
        self.assertFalse(self.settings_manager.write_metadata)
        self.assert_file_value("Video/write_metadata", False)

        self.simulate_checkbox("writeMetadataCheckBox", True)
        self.assertTrue(self.settings_manager.write_metadata)
        self.assert_file_value("Video/write_metadata", True)

    def test_skip_existing_files_checkbox(self) -> None:
        self.simulate_checkbox("skipExistingFilesCheckBox", False)
        self.assertFalse(self.settings_manager.skip_existing_files)
        self.assert_file_value("Video/skip_existing_files", False)

        self.simulate_checkbox("skipExistingFilesCheckBox", True)
        self.assertTrue(self.settings_manager.skip_existing_files)
        self.assert_file_value("Video/skip_existing_files", True)

    def test_track_videos_checkbox(self) -> None:
        self.simulate_checkbox("trackVideosCheckBox", True)
        self.assertTrue(self.settings_manager.track_videos)
        self.assert_file_value("Video/track_videos", True)

        self.simulate_checkbox("trackVideosCheckBox", False)
        self.assertFalse(self.settings_manager.track_videos)
        self.assert_file_value("Video/track_videos", False)

    def test_pocketbase_data_path_textfield(self) -> None:
        test_path = "/var/lib/pocketbase_custom"
        self.simulate_textfield("databasePathInput", test_path)
        self.assertEqual(self.settings_manager.pocketbase_data_path, test_path)
        self.assert_file_value("Video/pocketbase_data_path", test_path)

    def test_pocketbase_folder_dialog(self) -> None:
        test_path = "/opt/pocketbase_store"
        self.simulate_folder_dialog("pocketbaseFolderDialog", test_path)
        self.assertEqual(self.settings_manager.pocketbase_data_path, test_path)
        self.assert_file_value("Video/pocketbase_data_path", test_path)


class TestPerformanceTabGUI(SettingsGUITestBase):
    """Verifies that every change made on the Performance settings tab modifies the actual settings file."""

    def test_download_workers_spinbox(self) -> None:
        self.simulate_spinbox("downloadWorkersSpinBox", 32)
        self.assertEqual(self.settings_manager.download_workers, 32)
        self.assert_file_value("Performance/download_workers", 32)

    def test_network_delay_spinbox(self) -> None:
        self.simulate_spinbox("networkDelaySpinBox", 5)
        self.assertEqual(self.settings_manager.network_delay, 5)
        self.assert_file_value("Performance/network_delay", 5)

    def test_parallel_downloads_spinbox(self) -> None:
        self.simulate_spinbox("parallelDownloadsSpinBox", 4)
        self.assertEqual(self.settings_manager.parallel_downloads, 4)
        self.assert_file_value("Performance/semaphore", 4)

    def test_retries_spinbox(self) -> None:
        self.simulate_spinbox("retriesSpinBox", 8)
        self.assertEqual(self.settings_manager.retries, 8)
        self.assert_file_value("Performance/retries", 8)

    def test_timeout_spinbox(self) -> None:
        self.simulate_spinbox("timeoutSpinBox", 25)
        self.assertEqual(self.settings_manager.timeout, 25)
        self.assert_file_value("Performance/timeout", 25)

    def test_processing_delay_spinbox(self) -> None:
        self.simulate_spinbox("processingDelaySpinBox", 3)
        self.assertEqual(self.settings_manager.processing_delay, 3)
        self.assert_file_value("Performance/processing_delay", 3)

    def test_speed_limit_decimal_spinbox(self) -> None:
        self.simulate_decimal_spinbox("speedLimitSpinBox", 14.5)
        self.assertAlmostEqual(self.settings_manager.speed_limit, 14.5, places=2)
        self.assert_file_value("Performance/speed_limit", 14.5)

    def test_videos_concurrency_spinbox(self) -> None:
        self.simulate_spinbox("videosConcurrencySpinBox", 16)
        self.assertEqual(self.settings_manager.videos_concurrency, 16)
        self.assert_file_value("Performance/videos_concurrency", 16)

    def test_pages_concurrency_spinbox(self) -> None:
        self.simulate_spinbox("pagesConcurrencySpinBox", 5)
        self.assertEqual(self.settings_manager.pages_concurrency, 5)
        self.assert_file_value("Performance/pages_concurrency", 5)

    def test_response_cache_size_spinbox(self) -> None:
        self.simulate_spinbox("responseCacheSizeSpinBox", 64)
        self.assertEqual(self.settings_manager.response_cache_size, 64)
        self.assert_file_value("Performance/response_cache_size", 64)

    def test_response_cache_ttl_spinbox(self) -> None:
        self.simulate_spinbox("responseCacheTTLSpinBox", 600)
        self.assertEqual(self.settings_manager.response_cache_ttl, 600)
        self.assert_file_value("Performance/response_cache_ttl", 600)

    def test_segment_cache_size_spinbox(self) -> None:
        self.simulate_spinbox("segmentCacheSizeSpinBox", 16)
        self.assertEqual(self.settings_manager.segment_cache_size, 16)
        self.assert_file_value("Performance/segment_cache_size", 16)

    def test_segment_cache_ttl_spinbox(self) -> None:
        self.simulate_spinbox("segmentCacheTTLSpinBox", 900)
        self.assertEqual(self.settings_manager.segment_cache_ttl, 900)
        self.assert_file_value("Performance/segment_cache_ttl", 900)

    def test_request_initial_retry_delay_decimal_spinbox(self) -> None:
        self.simulate_decimal_spinbox("requestInitialRetryDelaySpinBox", 1.75)
        self.assertAlmostEqual(self.settings_manager.request_initial_retry_delay, 1.75, places=2)
        self.assert_file_value("Performance/request_initial_retry_delay", 1.75)

    def test_request_retry_max_delay_decimal_spinbox(self) -> None:
        self.simulate_decimal_spinbox("requestRetryMaxDelaySpinBox", 45.0)
        self.assertAlmostEqual(self.settings_manager.request_retry_max_delay, 45.0, places=2)
        self.assert_file_value("Performance/request_retry_max_delay", 45.0)

    def test_request_retry_multiplier_decimal_spinbox(self) -> None:
        self.simulate_decimal_spinbox("requestRetryMultiplierSpinBox", 3.5)
        self.assertAlmostEqual(self.settings_manager.request_retry_multiplier, 3.5, places=2)
        self.assert_file_value("Performance/request_retry_multiplier", 3.5)

    def test_request_retry_jitter_decimal_spinbox(self) -> None:
        self.simulate_decimal_spinbox("requestRetryJitterSpinBox", 0.8)
        self.assertAlmostEqual(self.settings_manager.request_retry_jitter, 0.8, places=2)
        self.assert_file_value("Performance/request_retry_jitter", 0.8)


class TestSystemTabGUI(SettingsGUITestBase):
    """Verifies that every change made on the System settings tab modifies the actual settings file."""

    def test_update_checks_checkbox(self) -> None:
        self.simulate_checkbox("updateChecksCheckBox", False)
        self.assertFalse(self.settings_manager.update_checks)
        self.assert_file_value("Misc/update_checks", False)

        self.simulate_checkbox("updateChecksCheckBox", True)
        self.assertTrue(self.settings_manager.update_checks)
        self.assert_file_value("Misc/update_checks", True)

    def test_supress_errors_checkbox(self) -> None:
        self.simulate_checkbox("supressErrorsCheckBox", True)
        self.assertTrue(self.settings_manager.supress_errors)
        self.assert_file_value("Misc/supress_errors", True)

        self.simulate_checkbox("supressErrorsCheckBox", False)
        self.assertFalse(self.settings_manager.supress_errors)
        self.assert_file_value("Misc/supress_errors", False)

    def test_enable_logging_checkbox(self) -> None:
        self.simulate_checkbox("enableLoggingCheckBox", True)
        self.assertTrue(self.settings_manager.enable_logging)
        self.assertTrue(self.settings_manager.error_reporting_decided)
        self.assert_file_value("Misc/network_logging", True)
        self.assert_file_value("Misc/error_reporting_decided", True)

        self.simulate_checkbox("enableLoggingCheckBox", False)
        self.assertFalse(self.settings_manager.enable_logging)
        self.assert_file_value("Misc/network_logging", False)

    def test_trust_environment_checkbox(self) -> None:
        self.simulate_checkbox("trustEnvironmentCheckBox", True)
        self.assertTrue(self.settings_manager.trust_environment)
        self.assert_file_value("Misc/trust_environment", True)

        self.simulate_checkbox("trustEnvironmentCheckBox", False)
        self.assertFalse(self.settings_manager.trust_environment)
        self.assert_file_value("Misc/trust_environment", False)

    def test_debug_mode_checkbox(self) -> None:
        self.simulate_checkbox("debugModeCheckBox", True)
        self.assertTrue(self.settings_manager.debug_mode)
        self.assert_file_value("Misc/debug_mode", True)

        self.simulate_checkbox("debugModeCheckBox", False)
        self.assertFalse(self.settings_manager.debug_mode)
        self.assert_file_value("Misc/debug_mode", False)

    def test_log_level_combobox(self) -> None:
        # Index 2 is "WARNING"
        self.simulate_combobox("logLevelComboBox", 2)
        self.assertEqual(self.settings_manager.log_level, 2)
        self.assert_file_value("Misc/log_level", 2)

        # Index 4 is "CRITICAL"
        self.simulate_combobox("logLevelComboBox", 4)
        self.assertEqual(self.settings_manager.log_level, 4)
        self.assert_file_value("Misc/log_level", 4)

    def test_http_version_textfield(self) -> None:
        self.simulate_textfield("httpVersionInput", "v3")
        self.assertEqual(self.settings_manager.http_version, "v3")
        self.assert_file_value("Misc/http_version", "v3")

    def test_impersonation_textfield(self) -> None:
        self.simulate_textfield("impersonationInput", "safari")
        self.assertEqual(self.settings_manager.impersonation, "safari")
        self.assert_file_value("Misc/impersonation", "safari")

    def test_custom_ja3_textfield(self) -> None:
        ja3_val = "771,4865-4866-4867,0-23-65281-10-11,29-23-24,0"
        self.simulate_textfield("customJA3Input", ja3_val)
        self.assertEqual(self.settings_manager.custom_ja3, ja3_val)
        self.assert_file_value("Misc/custom_ja3", ja3_val)

    def test_interface_textfield(self) -> None:
        self.simulate_textfield("interfaceInput", "tun0")
        self.assertEqual(self.settings_manager.interface, "tun0")
        self.assert_file_value("Misc/interface", "tun0")


class TestPrivacyTabGUI(SettingsGUITestBase):
    """Verifies that every change made on the Privacy settings tab modifies the actual settings file."""

    def test_anonymous_mode_checkbox(self) -> None:
        self.simulate_checkbox("anonymousModeCheckBox", True)
        self.assertTrue(self.settings_manager.anonymous_mode)
        self.assert_file_value("Privacy/anonymous_mode", True)

        self.simulate_checkbox("anonymousModeCheckBox", False)
        self.assertFalse(self.settings_manager.anonymous_mode)
        self.assert_file_value("Privacy/anonymous_mode", False)

    def test_encrypted_ch_checkbox(self) -> None:
        self.simulate_checkbox("encryptedCHCheckBox", False)
        self.assertFalse(self.settings_manager.encrypted_ch)
        self.assert_file_value("Privacy/encrypted_ch", False)

        self.simulate_checkbox("encryptedCHCheckBox", True)
        self.assertTrue(self.settings_manager.encrypted_ch)
        self.assert_file_value("Privacy/encrypted_ch", True)

    def test_dns_over_https_checkbox(self) -> None:
        self.simulate_checkbox("dnsOverHTTPSCheckBox", False)
        self.assertFalse(self.settings_manager.dns_over_https)
        self.assert_file_value("Privacy/dns_over_https", False)

        self.simulate_checkbox("dnsOverHTTPSCheckBox", True)
        self.assertTrue(self.settings_manager.dns_over_https)
        self.assert_file_value("Privacy/dns_over_https", True)

    def test_enable_tor_checkbox(self) -> None:
        self.simulate_checkbox("enableTorCheckBox", True)
        self.assertTrue(self.settings_manager.enable_tor)
        self.assert_file_value("Privacy/enable_tor", True)

        self.simulate_checkbox("enableTorCheckBox", False)
        self.assertFalse(self.settings_manager.enable_tor)
        self.assert_file_value("Privacy/enable_tor", False)

    def test_enable_tor_server_routing_checkbox(self) -> None:
        self.simulate_checkbox("enableTorServerRoutingCheckBox", False)
        self.assertFalse(self.settings_manager.enable_tor_server_routing)
        self.assert_file_value("Privacy/enable_tor_server_routing", False)

        self.simulate_checkbox("enableTorServerRoutingCheckBox", True)
        self.assertTrue(self.settings_manager.enable_tor_server_routing)
        self.assert_file_value("Privacy/enable_tor_server_routing", True)

    def test_primary_dns_textfield(self) -> None:
        test_dns = "https://1.1.1.1/dns-query"
        self.simulate_textfield("dnsPrimaryInput", test_dns)
        self.assertEqual(self.settings_manager.dns_server, test_dns)
        self.assert_file_value("Privacy/dns_server", test_dns)

    def test_fallback_dns_textfield(self) -> None:
        test_dns = "https://8.8.8.8/dns-query"
        self.simulate_textfield("dnsFallbackInput", test_dns)
        self.assertEqual(self.settings_manager.fallback_dns, test_dns)
        self.assert_file_value("Privacy/fallback_dns", test_dns)

    def test_sni_obfuscation_checkbox_and_modes(self) -> None:
        # Enable SNI obfuscation
        self.simulate_checkbox("sniObfuscationCheckBox", True)
        self.assertTrue(self.settings_manager.sni_obfuscation)
        self.assertTrue(self.settings_manager.sni_obfuscation_lite)
        self.assert_file_value("Privacy/sni_obfuscation", True)
        self.assert_file_value("Privacy/sni_obfuscation_lite", True)

        # Switch to Strict mode via RadioButton
        self.simulate_radio("sniStrictRadio")
        self.assertTrue(self.settings_manager.sni_obfuscation_strict)
        self.assertFalse(self.settings_manager.sni_obfuscation_lite)
        self.assert_file_value("Privacy/sni_obfuscation_strict", True)
        self.assert_file_value("Privacy/sni_obfuscation_lite", False)

        # Switch back to Lite mode via RadioButton
        self.simulate_radio("sniLiteRadio")
        self.assertTrue(self.settings_manager.sni_obfuscation_lite)
        self.assertFalse(self.settings_manager.sni_obfuscation_strict)
        self.assert_file_value("Privacy/sni_obfuscation_lite", True)
        self.assert_file_value("Privacy/sni_obfuscation_strict", False)

    def test_strict_profile_combobox(self) -> None:
        self.settings_manager.sni_obfuscation = True
        self.settings_manager.set_sni_obfuscation_mode("strict")

        # Index 1: "Strict Reverse"
        self.simulate_combobox("strictProfileCombo", 1)
        self.assertEqual(self.settings_manager.sni_obfuscation_strict_profile, "Strict Reverse")
        self.assert_file_value("Privacy/sni_obfuscation_strict_profile", "Strict Reverse")

        # Index 2: "Strict Desync"
        self.simulate_combobox("strictProfileCombo", 2)
        self.assertEqual(self.settings_manager.sni_obfuscation_strict_profile, "Strict Desync")
        self.assert_file_value("Privacy/sni_obfuscation_strict_profile", "Strict Desync")

    def test_proxy_window_configuration(self) -> None:
        # Applying proxy through ProxyWindow accepted signal
        self.simulate_proxy_acceptance("socks5://127.0.0.1:1080", False)
        self.assertEqual(self.settings_manager.proxy, "socks5://127.0.0.1:1080")
        self.assertFalse(self.settings_manager.proxy_ssl_verification)
        self.assert_file_value("Privacy/proxy", "socks5://127.0.0.1:1080")
        self.assert_file_value("Privacy/proxy_ssl_verification", False)

        # Disabling proxy
        self.simulate_proxy_acceptance("", True)
        self.assertEqual(self.settings_manager.proxy, "")
        self.assertTrue(self.settings_manager.proxy_ssl_verification)
        self.assert_file_value("Privacy/proxy", "")
        self.assert_file_value("Privacy/proxy_ssl_verification", True)


class TestUITabGUI(SettingsGUITestBase):
    """Verifies that every change made on the UI settings tab modifies the actual settings file."""

    def test_gui_language_combobox(self) -> None:
        # Index 2: "German"
        self.simulate_combobox("guiLanguageComboBox", 2)
        self.assertEqual(self.settings_manager.language, 2)
        self.assert_file_value("UI/language", 2)

        # Index 4: "French"
        self.simulate_combobox("guiLanguageComboBox", 4)
        self.assertEqual(self.settings_manager.language, 4)
        self.assert_file_value("UI/language", 4)

    def test_font_size_spinbox(self) -> None:
        self.simulate_spinbox("fontSizeSpinBox", 16)
        self.assertEqual(self.settings_manager.font_size, 16)
        self.assert_file_value("UI/font_size", 16)

    def test_core_style_combobox(self) -> None:
        # Index 1: "Fusion"
        self.simulate_combobox("coreStyleComboBox", 1)
        self.assertEqual(self.settings_manager.core_style, "Fusion")
        self.assert_file_value("UI/core_style", "Fusion")

        # Index 2: "Universal"
        self.simulate_combobox("coreStyleComboBox", 2)
        self.assertEqual(self.settings_manager.core_style, "Universal")
        self.assert_file_value("UI/core_style", "Universal")

    def test_dark_mode_switch(self) -> None:
        self.simulate_switch("darkModeSwitch", False)
        self.assertFalse(self.settings_manager.dark_mode)
        self.assert_file_value("UI/dark_mode", False)

        self.simulate_switch("darkModeSwitch", True)
        self.assertTrue(self.settings_manager.dark_mode)
        self.assert_file_value("UI/dark_mode", True)

    def test_accent_color_combobox(self) -> None:
        # Index 1: "#f44336" (Red)
        self.simulate_combobox("accentColorComboBox", 1)
        self.assertEqual(self.settings_manager.accent_color, "#f44336")
        self.assert_file_value("UI/accent_color", "#f44336")

        # Index 2: "#4caf50" (Green)
        self.simulate_combobox("accentColorComboBox", 2)
        self.assertEqual(self.settings_manager.accent_color, "#4caf50")
        self.assert_file_value("UI/accent_color", "#4caf50")


class TestResetSettingsGUI(SettingsGUITestBase):
    """Verifies that clicking the Reset button clears and resets settings back to defaults."""

    def test_reset_settings_button(self) -> None:
        # Change multiple settings
        self.simulate_spinbox("fontSizeSpinBox", 22)
        self.simulate_spinbox("resultLimitSpinBox", 999)
        self.simulate_textfield("httpVersionInput", "v3")

        self.assert_file_value("UI/font_size", 22)
        self.assert_file_value("Video/result_limit", 999)
        self.assert_file_value("Misc/http_version", "v3")

        # Click reset button
        self.simulate_reset_button()

        # Check that settings manager and file reverted to defaults
        fresh = self.read_fresh_settings()
        self.assertEqual(fresh.allKeys(), [])
        self.assertEqual(self.settings_manager.font_size, 12)
        self.assertEqual(self.settings_manager.result_limit, 50)
        self.assertEqual(self.settings_manager.http_version, "v2")


class TestRestartDialogUX(unittest.TestCase):
    """Verifies the UX requirement: the restart-required dialog must only be shown once per session."""

    def test_backend_setting_requires_restart_shown_only_once(self) -> None:
        from main import Backend

        backend = Backend()
        self.assertFalse(backend._restart_warning_shown)

        with patch("main.ui_popup") as mock_popup:
            backend.setting_requires_restart()
            self.assertEqual(mock_popup.call_count, 1)
            self.assertTrue(backend._restart_warning_shown)

            # Second trigger in the same session
            backend.setting_requires_restart()
            self.assertEqual(mock_popup.call_count, 1)

            # Third trigger in the same session
            backend.setting_requires_restart()
            self.assertEqual(mock_popup.call_count, 1)

    def test_restart_dialog_triggered_by_multiple_setting_changes_only_once(self) -> None:
        from main import Backend

        with tempfile.TemporaryDirectory() as tmpdir:
            ini_path = Path(tmpdir) / "test_restart.ini"
            qs = QSettings(str(ini_path), QSettings.Format.IniFormat)
            mgr = SettingsManager(qs)

            backend = Backend()
            # Connect manager to backend's slot
            mgr.restartRequired.connect(backend.setting_requires_restart)

            with patch("main.ui_popup") as mock_popup:
                # 1st change that requires restart: track_videos
                mgr.track_videos = True
                self.assertEqual(mock_popup.call_count, 1)

                # 2nd change in same session: enable_tor
                mgr.enable_tor = True
                self.assertEqual(mock_popup.call_count, 1)

                # 3rd change in same session: pocketbase_data_path
                mgr.pocketbase_data_path = "/new/pb/dir"
                self.assertEqual(mock_popup.call_count, 1)

                # 4th change in same session: core_style
                mgr.core_style = "Fusion"
                self.assertEqual(mock_popup.call_count, 1)

                # 5th change in same session: set_sni_obfuscation_mode
                mgr.set_sni_obfuscation_mode("strict")
                self.assertEqual(mock_popup.call_count, 1)


class TestInputMaskingAndValidation(SettingsGUITestBase):
    """Verifies that input masking, regular expression validators, and safe fallbacks operate properly in QML."""

    def test_http_version_validation(self) -> None:
        tf = self.find_control("httpVersionInput")

        # Valid v1
        tf.setProperty("text", "v1")
        self.assertTrue(tf.property("acceptableInput"))
        tf.editingFinished.emit()
        self.assertEqual(self.settings_manager.http_version, "v1")

        # Valid v3
        tf.setProperty("text", "v3")
        self.assertTrue(tf.property("acceptableInput"))
        tf.editingFinished.emit()
        self.assertEqual(self.settings_manager.http_version, "v3")

        # Invalid v9: should fail acceptableInput, reject update, and restore previous setting
        tf.setProperty("text", "v9")
        self.assertFalse(tf.property("acceptableInput"))
        tf.editingFinished.emit()
        self.assertEqual(self.settings_manager.http_version, "v3")
        self.assertEqual(tf.property("text"), "v3")

    def test_dns_inputs_validation(self) -> None:
        primary = self.find_control("dnsPrimaryInput")
        fallback = self.find_control("dnsFallbackInput")

        # Valid DoH URLs
        primary.setProperty("text", "https://security.cloudflare-dns.com/dns-query")
        self.assertTrue(primary.property("acceptableInput"))
        primary.editingFinished.emit()
        self.assertEqual(self.settings_manager.dns_server, "https://security.cloudflare-dns.com/dns-query")

        fallback.setProperty("text", "https://dns.quad9.net/dns-query")
        self.assertTrue(fallback.property("acceptableInput"))
        fallback.editingFinished.emit()
        self.assertEqual(self.settings_manager.fallback_dns, "https://dns.quad9.net/dns-query")

        # Invalid strings containing spaces
        primary.setProperty("text", "https://invalid url with spaces")
        self.assertFalse(primary.property("acceptableInput"))
        primary.editingFinished.emit()
        self.assertEqual(self.settings_manager.dns_server, "https://security.cloudflare-dns.com/dns-query")
        self.assertEqual(primary.property("text"), "https://security.cloudflare-dns.com/dns-query")

        fallback.setProperty("text", "not a valid dns address")
        self.assertFalse(fallback.property("acceptableInput"))
        fallback.editingFinished.emit()
        self.assertEqual(self.settings_manager.fallback_dns, "https://dns.quad9.net/dns-query")
        self.assertEqual(fallback.property("text"), "https://dns.quad9.net/dns-query")

    def test_custom_ja3_validation(self) -> None:
        tf = self.find_control("customJA3Input")

        # Valid JA3 format
        valid_ja3 = "771,4865-4866-4867,0-23-65281,29-23,0"
        tf.setProperty("text", valid_ja3)
        self.assertTrue(tf.property("acceptableInput"))
        tf.editingFinished.emit()
        self.assertEqual(self.settings_manager.custom_ja3, valid_ja3)

        # Invalid JA3 containing letters
        tf.setProperty("text", "invalid_letters_here")
        self.assertFalse(tf.property("acceptableInput"))
        tf.editingFinished.emit()
        self.assertEqual(self.settings_manager.custom_ja3, valid_ja3)
        self.assertEqual(tf.property("text"), valid_ja3)

    def test_interface_validation(self) -> None:
        tf = self.find_control("interfaceInput")

        # Valid interface
        tf.setProperty("text", "wlan0")
        self.assertTrue(tf.property("acceptableInput"))
        tf.editingFinished.emit()
        self.assertEqual(self.settings_manager.interface, "wlan0")

        # Invalid interface containing space
        tf.setProperty("text", "wlan 0 invalid")
        self.assertFalse(tf.property("acceptableInput"))
        tf.editingFinished.emit()
        self.assertEqual(self.settings_manager.interface, "wlan0")
        self.assertEqual(tf.property("text"), "wlan0")

    def test_impersonation_validation(self) -> None:
        tf = self.find_control("impersonationInput")

        # Valid impersonation
        tf.setProperty("text", "safari_15_5")
        self.assertTrue(tf.property("acceptableInput"))
        tf.editingFinished.emit()
        self.assertEqual(self.settings_manager.impersonation, "safari_15_5")

        # Invalid impersonation with special characters
        tf.setProperty("text", "chrome@#$%")
        self.assertFalse(tf.property("acceptableInput"))
        tf.editingFinished.emit()
        self.assertEqual(self.settings_manager.impersonation, "safari_15_5")
        self.assertEqual(tf.property("text"), "safari_15_5")

    def test_path_sanitization_and_empty_protection(self) -> None:
        out_tf = self.find_control("outputPathInput")
        db_tf = self.find_control("databasePathInput")

        # Path with surrounding spaces gets trimmed
        out_tf.setProperty("text", "   /custom/videos/path   ")
        out_tf.editingFinished.emit()
        self.assertEqual(self.settings_manager.output_path, "/custom/videos/path")

        db_tf.setProperty("text", "   /custom/pb/path   ")
        db_tf.editingFinished.emit()
        self.assertEqual(self.settings_manager.pocketbase_data_path, "/custom/pb/path")

        # Empty or whitespace-only path is rejected and restored to previous valid path
        out_tf.setProperty("text", "   ")
        out_tf.editingFinished.emit()
        self.assertEqual(self.settings_manager.output_path, "/custom/videos/path")
        self.assertEqual(out_tf.property("text"), "/custom/videos/path")

        db_tf.setProperty("text", "   ")
        db_tf.editingFinished.emit()
        self.assertEqual(self.settings_manager.pocketbase_data_path, "/custom/pb/path")
        self.assertEqual(db_tf.property("text"), "/custom/pb/path")


class TestSettingsAccessibility(SettingsGUITestBase):
    """Verifies that all GUI controls expose correct Accessible properties for screen readers."""

    def test_accessible_properties_on_controls(self) -> None:
        controls_to_check = [
            ("defaultQualityCombo", "Quality"),
            ("modelVideosCombo", "Model Videos"),
            ("contentLanguageComboBox", "Content Language"),
            ("strictEnforcementCheckBox", "Strict Enforcement for content language"),
            ("resultLimitSpinBox", "Max Result Limit"),
            ("outputPathInput", "Output Path"),
            ("writeMetadataCheckBox", "Write metadata"),
            ("skipExistingFilesCheckBox", "Skip existing files"),
            ("trackVideosCheckBox", "Track Videos in PocketBase"),
            ("databasePathInput", "PocketBase Data Folder"),
            ("downloadWorkersSpinBox", "Download workers"),
            ("networkDelaySpinBox", "Network delay"),
            ("parallelDownloadsSpinBox", "Parallel Downloads"),
            ("retriesSpinBox", "Maximum retries"),
            ("timeoutSpinBox", "Maximum timeout"),
            ("processingDelaySpinBox", "Processing Delay"),
            ("speedLimitSpinBox", "Speed Limit"),
            ("videosConcurrencySpinBox", "Videos Concurrency"),
            ("pagesConcurrencySpinBox", "Pages Concurrency"),
            ("updateChecksCheckBox", "Search for Updates"),
            ("supressErrorsCheckBox", "Ignore Errors"),
            ("enableLoggingCheckBox", "Allow redacted error reports"),
            ("trustEnvironmentCheckBox", "Trust Environment"),
            ("debugModeCheckBox", "Enable Debug Mode"),
            ("logLevelComboBox", "Log Level"),
            ("httpVersionInput", "HTTP Version"),
            ("impersonationInput", "Browser Impersonation Target"),
            ("customJA3Input", "Custom JA3 String"),
            ("interfaceInput", "Network Interface or IP"),
            ("anonymousModeCheckBox", "Anonymous Mode"),
            ("encryptedCHCheckBox", "Encrypted Client Hello"),
            ("dnsOverHTTPSCheckBox", "DNS over HTTPS"),
            ("enableTorCheckBox", "Enable Tor Integration"),
            ("dnsPrimaryInput", "Primary DNS over HTTPS Server"),
            ("dnsFallbackInput", "Fallback DNS over HTTPS Server"),
            ("sniObfuscationCheckBox", "SNI Obfuscation"),
            ("sniLiteRadio", "Lite SNI Obfuscation"),
            ("sniStrictRadio", "Strict SNI Obfuscation"),
            ("guiLanguageComboBox", "Graphical User Interface Language"),
            ("fontSizeSpinBox", "Font Size"),
            ("coreStyleComboBox", "Application Style"),
            ("darkModeSwitch", "Dark Mode"),
            ("accentColorComboBox", "Application Accent Color"),
            ("resetSettingsButton", "Reset Porn Fetch to default settings"),
        ]

        for obj_name, expected_name in controls_to_check:
            ctrl = self.find_control(obj_name)
            self.assertIsNotNone(ctrl, f"Control {obj_name} not found in QML hierarchy")
            iface = QAccessible.queryAccessibleInterface(ctrl)
            if iface is not None:
                acc_name = iface.text(QAccessible.Text.Name)
                self.assertEqual(acc_name, expected_name, f"Accessible name mismatch for {obj_name}")


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
