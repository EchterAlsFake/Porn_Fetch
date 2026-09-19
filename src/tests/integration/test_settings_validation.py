from __future__ import annotations

from PySide6.QtGui import QAccessible

from src.tests.integration.settings_support import SettingsGUITestBase


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

