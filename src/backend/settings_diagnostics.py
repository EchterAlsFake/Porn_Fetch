"""Isolated settings-page contracts using the real backend and provider cores."""
from __future__ import annotations

import asyncio
import configparser
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QEvent, QMetaObject, QObject, QSettings, Qt, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtTest import QSignalSpy

from src.tests.settings_cases import CASE_BY_PROPERTY, SETTINGS
from src.tests.smoke.download_lifecycle import require


class SettingsWindow:
    def __init__(self, directory):
        from src.backend import clients
        from src.backend.account_diagnostics import UI, make_account_backend
        from src.backend.config import app_settings
        from src.backend.theme_manager import ThemeManager
        from src.backend.tor_status import TorStatus
        from src.backend.ui_translation import UiTranslation
        from src.frontend.UI import resources

        resources.qInitResources()
        self.directory = Path(directory)
        self.path = self.directory / "settings.ini"
        self.settings = app_settings
        self.old_settings, self.old_custom = app_settings._settings, app_settings._custom_settings
        self.disk = QSettings(str(self.path), QSettings.Format.IniFormat)
        # Initial isolated startup values; actual changes below always use QML.
        for key, value in {"Privacy/dns_over_https": False, "Privacy/encrypted_ch": False,
                           "Performance/download_workers": 1, "Performance/videos_concurrency": 1,
                           "Performance/retries": 1, "Performance/timeout": 20,
                           "Video/output_path": str(self.directory / "media"),
                           "Video/pocketbase_data_path": str(self.directory / "database")}.items():
            self.disk.setValue(key, value)
        app_settings.set_settings_storage(self.disk)
        self.backend = make_account_backend()
        self.backend._pending_parallel_limit = None
        self.backend._pending_pocketbase_move = None
        self.backend._restart_warning_shown = True
        self.backend._download_semaphore = asyncio.Semaphore(app_settings.parallel_downloads)
        self.backend.bind_runtime_settings()
        self.backend.load_clients()
        self.restart = QSignalSpy(app_settings.restartRequired)
        self.errors = []
        self.backend.showMessage.connect(self.errors.append)
        self.engine = QQmlApplicationEngine()
        self.warnings = []
        self.engine.warnings.connect(lambda errors: self.warnings.extend(str(e) for e in errors))
        context = self.engine.rootContext()
        context.setContextProperty("appSettings", app_settings)
        context.setContextProperty("backend", self.backend)
        self.theme = ThemeManager(self.engine)
        context.setContextProperty("themeManager", self.theme)
        self.tor_status = TorStatus(self.engine)
        context.setContextProperty("torStatus", self.tor_status)
        self.translation = UiTranslation(app_settings, self.engine)
        self.engine.loadData(b'''
import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts
ApplicationWindow {
    visible: true; width: 1700; height: 1100
    font.pointSize: appSettings.font_size
    property bool androidLayout: false
    property QtObject bridge: QtObject { property bool isPremium: false }
    Material.theme: appSettings.dark_mode ? Material.Dark : Material.Light
    Material.accent: appSettings.accent_color
    readonly property color appliedBackground: Material.background
    readonly property color appliedAccent: Material.accent
    RowLayout {
        anchors.fill: parent
        SettingsPage { objectName: "settingsPage"; Layout.fillWidth: true; Layout.fillHeight: true }
        DownloadsPage { objectName: "downloadsPage"; Layout.fillWidth: true; Layout.fillHeight: true }
    }
    ActivityEdge {
        objectName: "settingsActivity"; anchors.fill: parent
        enabled: appSettings.activity_glow_enabled; active: true
        accentColor: appSettings.accent_color
    }
}
''', QUrl.fromLocalFile(str(UI / "SettingsDiagnostic.qml")))
        require(bool(self.engine.rootObjects()), "Production Settings/Downloads pages did not load")
        self.window = self.engine.rootObjects()[0]
        self.page = self.window.findChild(QObject, "settingsPage")
        assert self.page is not None, "Settings page is missing"
        self.model = self.backend._downloads_model
        self.pump()
        self.clients = clients

    @staticmethod
    def pump():
        QGuiApplication.processEvents()

    def control(self, name):
        assert self.page is not None
        result = self.page.findChild(QObject, name)
        assert result is not None, f"Missing settings control: {name}"
        return result

    def activate(self, prop, value):
        setting = CASE_BY_PROPERTY[prop]
        self.control("settingsStack").setProperty("currentIndex", setting.tab)
        self.pump()
        control = self.control(setting.control)
        kind = setting.kind
        if kind in {"check", "switch"}:
            control.setProperty("checked", value)
            control.toggled.emit()
        elif kind in {"text", "path"}:
            control.setProperty("text", str(value))
            require(control.property("acceptableInput"), f"Test value rejected by {setting.control}")
            control.editingFinished.emit()
        elif kind in {"spin", "decimal"}:
            factor = float(control.property("factor") or 1) if kind == "decimal" else 1
            control.setProperty("value", round(value * factor))
            control.valueModified.emit()
        elif kind in {"proxy", "ssl"}:
            control.proxyAccepted.emit(value if kind == "proxy" else (self.settings.proxy or "http://127.0.0.1:9"),
                                       value if kind == "ssl" else self.settings.proxy_ssl_verification)
        elif kind == "radio":
            self.settings.sni_obfuscation = True
            control.clicked.emit()
        else:
            if kind == "combo":
                index = value
            elif kind == "locale":
                index = list(self.clients.SUPPORTED_CONTENT_LOCALES).index(value)
            elif kind == "tor":
                index = ["direct", "tor", "tor_all"].index(value)
            elif kind == "profile":
                self.settings.sni_obfuscation = True
                self.settings.set_sni_obfuscation_mode("strict")
                index = ["Strict Fragmentation", "Strict Reverse", "Strict Desync"].index(value)
            elif kind == "style":
                index = ["Material", "Fusion", "Universal", "Windows"].index(value)
            elif kind == "accent":
                index = ["#6366f1", "#f44336", "#4caf50", "#ff9800", "#9c27b0"].index(value)
            else:
                raise AssertionError(f"Unknown settings action: {kind}")
            control.setProperty("currentIndex", index)
            control.activated.emit(index)
            if kind == "tor" and value == "tor_all":
                warning = self.control("torAllTrafficWarning")
                require(warning.property("visible"), "All-traffic routing skipped its confirmation")
                QMetaObject.invokeMethod(warning, "accept", Qt.ConnectionType.DirectConnection)
        self.pump()
        self.settings.sync()
        require(getattr(self.settings, prop) == value, f"QML failed to change {prop}")
        self.verify_disk(setting, value)
        require(not self.warnings, f"QML warnings: {self.warnings[:2]}")

    def verify_disk(self, setting, value):
        # ConfigParser has no access to Qt's shared in-process QSettings cache.
        parser = configparser.ConfigParser(interpolation=None)
        parser.optionxform = str
        parser.read(self.path)
        section, key = setting.key.split("/", 1)
        raw = parser[section][key]
        expected = str(value).lower() if isinstance(value, bool) else str(value)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            require(float(raw) == float(value), f"Disk value differs for {setting.prop}")
        else:
            # QSettings quotes strings containing commas/semicolons.
            require(raw.strip('"') == expected, f"Disk value differs for {setting.prop}: {raw!r}")
        from src.backend.config import SettingsManager
        restored = SettingsManager(QSettings(str(self.path), QSettings.Format.IniFormat))
        require(getattr(restored, setting.prop) == value, f"Reload lost {setting.prop}")

    def verify_runtime(self, setting, value):
        from curl_cffi.const import CurlOpt

        from src.shared.tor_transport import FAIL_CLOSED_PROXY

        settings = self.settings
        expected = value
        if setting.runtime in {"response_cache_size_bytes", "segment_cache_size_bytes"}:
            expected *= 1024 * 1024
        elif setting.runtime in {"proxy", "interface", "custom_ja3"}:
            expected = expected or None
        elif setting.runtime == "locale":
            expected = self.clients.generate_locale_headers_and_cookies(value)[0]["Accept-Language"]
        if setting.prop == "proxy" and settings.service_transport == "tor_all":
            expected = FAIL_CLOSED_PROXY
        from src.shared.provider_routing import PROVIDER_MODULES
        for provider in PROVIDER_MODULES:
            core = self.clients.client_for(provider).core
            cfg, session = core.configuration, core.session
            require(session is not None, f"{provider} lost its active session")
            if setting.runtime:
                require(getattr(cfg, setting.runtime) == expected,
                        f"Active {provider} configuration ignored {setting.prop}")
            if setting.prop == "encrypted_ch":
                require(session.curl_options[CurlOpt.ECH] == (b"true" if value else b"false"),
                        "ECH did not reach the active curl session")
            elif setting.prop in {"dns_over_https", "dns_server", "fallback_dns"}:
                require(cfg.dns_over_https == (settings.dns_server if settings.dns_over_https else None),
                        "Primary DNS did not reach active providers")
                require(cfg.fallback_dns == (settings.fallback_dns if settings.dns_over_https else None),
                        "Fallback DNS did not reach active providers")
            elif setting.prop == "locale":
                headers, cookies = self.clients.generate_locale_headers_and_cookies(value)
                require(session.headers["Accept-Language"] == headers["Accept-Language"], "Live session language is stale")
                require(all(session.cookies.get(key) == text for key, text in cookies.items()), "Live language cookies are stale")
        if setting.prop == "parallel_downloads":
            require(self.backend._download_semaphore._value == value, "Active parallel limit was not updated")
        if setting.prop == "log_level":
            import logging
            require(self.backend.logger.level == getattr(logging, settings.log_level_map[value]), "Backend logger level is stale")
        return bool(setting.runtime or setting.prop in {"encrypted_ch", "dns_over_https", "dns_server", "fallback_dns",
                                                       "parallel_downloads", "log_level"})

    def inventory(self):
        import re

        from src.backend.account_diagnostics import UI
        source = (UI / "SettingsPage.qml").read_text() + (UI / "TorRouting.qml").read_text()
        named = set(re.findall(r'objectName:\s*"([^"]+)"', source))
        covered = {setting.control for setting in SETTINGS}
        ancillary = {"settingsStack", "outputFolderDialog", "pocketbaseFolderDialog", "torStatusLabel",
                     "torAllTrafficWarning", "resetSettingsButton"}
        require(not (named - covered - ancillary), f"Settings inventory has uncovered controls: {named - covered - ancillary}")
        return len(covered)

    async def close(self):
        try:
            self.settings.reloadClients.disconnect(self.backend.load_clients)
            self.settings.parallelDownloadsChanged.disconnect(self.backend.update_parallel_downloads)
        except RuntimeError:
            pass
        for event in self.backend._download_stop_events.values():
            event.set()
        tasks = tuple(self.backend._background_tasks)
        if tasks:
            await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), 30)
        await self.clients.close_all_clients()
        app = QCoreApplication.instance()
        if app is not None:
            app.removeTranslator(self.translation.translator)
        self.window.close()
        self.window.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        self.engine.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        self.settings._settings, self.settings._custom_settings = self.old_settings, self.old_custom
