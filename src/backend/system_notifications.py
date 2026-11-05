"""Optional system delivery; the in-app session model remains authoritative."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from PySide6.QtCore import Property, QFileSystemWatcher, QObject, Qt, QTimer, Signal, Slot
from PySide6.QtGui import QGuiApplication

from src.backend.app_icon import application_icon


class SystemNotifications(QObject):
    changed = Signal()
    activated = Signal()

    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self._tray = None
        self._state = "unavailable"
        self._pending = set()
        self._directory = None
        self._watcher = QFileSystemWatcher(self)
        if sys.platform == "ios":
            self._directory = Path.home() / "Library/Caches/PornFetchNotifications"
        elif sys.platform == "android" or hasattr(sys, "getandroidapilevel"):
            private = os.environ.get("ANDROID_PRIVATE")
            if private:
                self._directory = Path(private)
        if self._directory is not None:
            self._directory.mkdir(parents=True, exist_ok=True)
            self._watcher.addPath(str(self._directory))
            self._watcher.directoryChanged.connect(self.refresh)
            self.refresh()
            self._command("status")
        elif sys.platform in {"win32", "linux", "darwin"}:
            from PySide6.QtWidgets import QApplication, QSystemTrayIcon

            if isinstance(QGuiApplication.instance(), QApplication) and QSystemTrayIcon.isSystemTrayAvailable():
                self._tray = QSystemTrayIcon(application_icon(), self)
                self._tray.setToolTip(self.tr("Download notifications"))
                self._tray.messageClicked.connect(self.activated)
                self._state = "available" if QSystemTrayIcon.supportsMessages() else "unavailable"
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(1500)
        self._timer.timeout.connect(self._deliver)
        settings.systemNotificationsChanged.connect(self.set_enabled)
        app = QGuiApplication.instance()
        if app:
            app.applicationStateChanged.connect(self._application_state_changed)
            app.aboutToQuit.connect(self.close)
        if self._tray:
            self._tray.setVisible(settings.system_notifications)

    @Property(str, notify=changed)
    def status(self):
        if not self.settings.system_notifications:
            return self.tr("System notifications are off. Messages remain in Recent activity.")
        return {
            "allowed": self.tr("System notifications are enabled. Content is always private."),
            "available": self.tr("System notifications are enabled when supported by your desktop settings."),
            "denied": self.tr("Notifications are blocked in system settings. In-app messages remain available."),
            "pending": self.tr("Waiting for notification permission."),
            "unavailable": self.tr(
                "System notifications are unavailable in this session. In-app messages remain available."
            ),
        }.get(self._state, self.tr("Checking notification permission…"))

    @Slot(bool)
    def set_enabled(self, enabled):
        if self._tray:
            self._tray.setVisible(enabled)
        if self._directory:
            self._command("enable" if enabled else "disable")
        if not enabled:
            self._pending.clear()
            self._timer.stop()
        self.changed.emit()

    @Slot()
    def open_settings(self):
        if self._directory:
            self._command("settings")

    @Slot(str)
    def request(self, kind):
        app = QGuiApplication.instance()
        if (
            not self.settings.system_notifications
            or app is None
            or app.applicationState() == Qt.ApplicationState.ApplicationActive
        ):
            return
        self._pending.add(kind)
        self._timer.start()

    def _deliver(self):
        app = QGuiApplication.instance()
        kinds, self._pending = self._pending, set()
        if (
            not kinds
            or not self.settings.system_notifications
            or app is None
            or app.applicationState() == Qt.ApplicationState.ApplicationActive
        ):
            return
        message = (
            self.tr("Some downloads need attention. Open the application to review them.")
            if "failed" in kinds
            else self.tr("Downloads finished. Files use your configured output folder.")
        )
        if self._directory:
            self._command("notify", message=message)
        elif self._tray and self._state == "available":
            self._tray.showMessage(self.tr("Downloads"), message)

    def _application_state_changed(self, state):
        if state == Qt.ApplicationState.ApplicationActive:
            if self._directory:
                self._command("status")

    @Slot()
    def refresh(self, *_):
        try:
            value = json.loads((self._directory / "notifications-state.json").read_text())
            self._state = value["state"]
        except OSError, ValueError, KeyError, TypeError:
            return
        self.changed.emit()

    def _command(self, action, **values):
        try:
            path = self._directory / "notifications-request.json"
            temporary = path.with_suffix(".tmp")
            temporary.write_text(
                json.dumps({"action": action, "title": self.tr("Downloads"), **values}), encoding="utf-8"
            )
            temporary.replace(path)
        except OSError:
            self._state = "unavailable"
            self.changed.emit()

    @Slot()
    def close(self):
        self._timer.stop()
        if self._tray:
            self._tray.hide()
