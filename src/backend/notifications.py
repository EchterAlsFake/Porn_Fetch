"""GUI-owned, bounded session feedback. Publishing never enters a local event loop."""

from __future__ import annotations

import hashlib
import re
from datetime import datetime

from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtGui import QGuiApplication

from src.shared.error_reporting import redact_log_text


def public_message(value: object) -> str:
    """Messages and clipboard support must not expose URLs, credentials or tracebacks."""
    text = str(value or "").split("Traceback (most recent call last):", 1)[0]
    text = text.split("Debug for GitHub", 1)[0]
    text = re.sub(r"(?:https?|socks5?h?|file|content)://\S+", "[redacted]", text)
    text = re.sub(r"(?m)(?:[A-Za-z]:[\\/]|/(?:home|Users|data|storage|private|tmp)/)\S+", "[redacted]", text)
    return redact_log_text(text).strip()[:3000]


class NotificationCenter(QObject):
    changed = Signal()
    announced = Signal(str, bool)
    systemRequested = Signal(str)
    decisionAccepted = Signal(str)
    directRequested = Signal(str, str)

    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self._entries: list[dict] = []
        self._next_id = 0
        self._banner_id = ""
        self._completed = 0
        self._restart = False
        self._shutting_down = False
        self._decisions = []
        settings.anonymousModeChanged.connect(self._privacy_changed)

    @Property("QVariantList", notify=changed)
    def entries(self):
        return [dict(entry) for entry in reversed(self._entries)]

    @Property("QVariantMap", notify=changed)
    def latest(self):
        return next((dict(e) for e in self._entries if e["id"] == self._banner_id), {})

    @Property(bool, notify=changed)
    def restartRequired(self):
        return self._restart

    @Property(bool, notify=changed)
    def shuttingDown(self):
        return self._shutting_down

    @Property("QVariantMap", notify=changed)
    def pendingDecision(self):
        return dict(self._decisions[0]) if self._decisions else {}

    def request_decision(self, action, title, message):
        if not any(item["action"] == action for item in self._decisions):
            self._decisions.append({"action": action, "title": title, "message": message})
            self.changed.emit()

    @Slot(str, bool)
    def resolve_decision(self, action, accepted):
        if self._decisions and self._decisions[0]["action"] == action:
            self._decisions.pop(0)
            self.changed.emit()
            if accepted:
                self.decisionAccepted.emit(action)

    def publish(
        self,
        message: str,
        title: str = "",
        severity: str = "info",
        *,
        key: str = "",
        action: str = "",
        details: str = "",
        quiet: bool = False,
        direct: bool = False,
    ):
        severity = severity if severity in {"info", "success", "warning", "error"} else "info"
        message, title, details = map(public_message, (message, title, details))
        if key == "operation-error":
            # Coalesce the same cause, while preserving unrelated errors.
            cause = message.split("Error ID:", 1)[0]
            key += ":" + hashlib.sha256(cause.encode()).hexdigest()[:16]
        if not message:
            message = self.tr("The operation could not be completed. Please try again.")
        if not title or title == "Notice":
            title = {
                "error": self.tr("Action needed"),
                "warning": self.tr("Please check"),
                "success": self.tr("Completed"),
                "info": self.tr("Information"),
            }[severity]
        # Anonymous mode may be switched on after an entry was created. Do not
        # retain arbitrary caller text that could contain a media title or name.
        if self.settings.anonymous_mode:
            title, message, details = self._private_text(severity)
        preserve_error = self.latest.get("severity") == "error" and severity not in {"error", "warning"}
        entry = next((e for e in self._entries if key and e["key"] == key), None)
        if entry is None:
            self._next_id += 1
            entry = {"id": str(self._next_id), "count": 0, "key": key}
        else:
            self._entries.remove(entry)
        entry.update(
            title=title,
            message=message,
            details=details,
            severity=severity,
            action=action,
            count=entry["count"] + 1,
            time=datetime.now().strftime("%H:%M"),
        )
        self._entries.append(entry)
        self._entries = self._entries[-50:]
        if not quiet and not preserve_error:
            self._banner_id = entry["id"]
        self.changed.emit()
        # Presentation coalesces announcements, including bursts of repeated errors.
        if not quiet and not preserve_error:
            self.announced.emit(f"{title}. {message}", severity == "error")
        if direct and not quiet:
            self.directRequested.emit(title, message)
        return entry["id"]

    @Slot(str, str, str)
    def show(self, message: str, title: str, severity: str):
        self.publish(message, title, severity)

    @Slot(str, result=str)
    def safe_text(self, message):
        return self._private_text("info")[1] if self.settings.anonymous_mode else public_message(message)

    def download_completed(self):
        self._completed += 1
        self.publish(
            self.tr("Downloads completed this session: %s. Files are saved to your configured output folder.")
            % self._completed,
            self.tr("Download complete"),
            "success",
            key="download-completed",
            action="output",
        )
        self.systemRequested.emit("completed")

    def download_failed(self, report_id: str, message: str = ""):
        self.publish(
            message
            or self.tr("A download failed. Check your connection and output folder, then retry the failed rows."),
            self.tr("Download failed"),
            "error",
            key="download-failed",
            action="retry",
            details=self.tr("Error ID: %s") % report_id,
            quiet=self.settings.supress_errors,
        )
        self.systemRequested.emit("failed")

    def require_restart(self):
        self._restart = True
        self.changed.emit()
        self.announced.emit(self.tr("Restart required. Your settings will take effect after restarting."), False)
        self.directRequested.emit(self.tr("Restart required"), self.tr("Restart Porn Fetch to apply your changed settings."))

    def begin_shutdown(self):
        self._shutting_down = True
        self.changed.emit()
        self.announced.emit(self.tr("Closing. Stopping downloads and saving application state."), False)

    @Slot()
    def dismiss(self):
        self._banner_id = ""
        self.changed.emit()

    @Slot()
    def clear(self):
        self._entries.clear()
        self._banner_id = ""
        self.changed.emit()

    @Slot(str)
    def copy(self, identifier: str):
        entry = next((e for e in self._entries if e["id"] == identifier), None)
        if entry:
            text = "\n\n".join(filter(None, (entry["title"], entry["message"], entry["details"])))
            QGuiApplication.clipboard().setText(text)
            self.announced.emit(self.tr("Copied to clipboard."), False)

    def _private_text(self, severity):
        return (
            self.tr("Application update"),
            self.tr("An operation needs attention. Check the task status.")
            if severity in {"error", "warning"}
            else self.tr("The operation finished. Check the task status."),
            "",
        )

    def _privacy_changed(self, anonymous):
        if anonymous:
            for entry in self._entries:
                entry["title"], entry["message"], entry["details"] = self._private_text(entry["severity"])
            self.changed.emit()
