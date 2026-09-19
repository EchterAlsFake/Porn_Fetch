from __future__ import annotations

from src.tests.integration.settings_support import SettingsGUITestBase


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

