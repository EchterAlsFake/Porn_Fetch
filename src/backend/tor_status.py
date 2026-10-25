"""Queued Qt adapter for the shared Tor runtime and Android installer results."""
import json
import os
import time
from pathlib import Path

from PySide6.QtCore import Property, QFileSystemWatcher, QObject, Signal, Slot

from src.shared import service_transport
from src.shared.tor_runtime import runtime


class TorStatus(QObject):
    changed = Signal()
    received = Signal(str, int)
    installResult = Signal(str)
    failureReceived = Signal(str)
    failure = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._text = "Tor starts when a license or update request needs it."
        self.received.connect(self._receive)
        runtime.progress = self.received.emit
        self._last_failure = ""
        self._last_notice_at = float("-inf")
        self.failureReceived.connect(self._failure)
        service_transport.failure_listener = self.failureReceived.emit
        self._watcher = QFileSystemWatcher(self)
        if os.environ.get("ANDROID_PRIVATE"):
            self._private = Path(os.environ["ANDROID_PRIVATE"])
            self._watcher.addPath(str(self._private))
            self._watcher.directoryChanged.connect(self._install_result)

    @Slot(str, int)
    def _receive(self, state, percentage):
        self._text = {"stopped": "Tor is stopped.", "ready": "Connected through Tor.",
                      "error": "Tor is unavailable. No direct connection was attempted.",
                      "connecting": f"Connecting to Tor… {percentage}%"}[state]
        self.changed.emit()

    @Property(str, notify=changed)
    def text(self):
        return self._text

    @Slot(str)
    def _failure(self, message):
        self._text = message
        self.changed.emit()
        now = time.monotonic()
        if message != self._last_failure or now - self._last_notice_at >= 60:
            self._last_failure, self._last_notice_at = message, now
            self.failure.emit(message)

    @Slot()
    def resetFailureNotice(self):
        self._last_failure = ""
        self._last_notice_at = float("-inf")

    def _install_result(self, *_):
        path = self._private / "install-result.json"
        try:
            value = json.loads(path.read_text())
            path.unlink()
            self.installResult.emit(str(value["message"]))
        except (OSError, ValueError, KeyError):
            pass
