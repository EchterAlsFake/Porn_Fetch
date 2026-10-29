"""Qt adapter for the shared beta disclaimer and its reading delay."""
from __future__ import annotations

from PySide6.QtCore import Property, QObject, QTimer, Signal, Slot

from src.backend.config import SettingsManager
from src.shared.beta_disclaimer import BETA_DISCLAIMER_TEXT, DisclaimerReadDelay


class BetaDisclaimerBridge(QObject):
    remainingSecondsChanged = Signal()

    def __init__(self, settings: SettingsManager, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._settings = settings
        self._delay = DisclaimerReadDelay()
        self._timer = QTimer(self)
        self._timer.setInterval(200)
        self._timer.timeout.connect(self._refresh_countdown)

    @Property(str, constant=True)
    def text(self) -> str:
        return BETA_DISCLAIMER_TEXT

    @Property(int, notify=remainingSecondsChanged)
    def remainingSeconds(self) -> int:
        return self._delay.remaining_seconds

    @Slot()
    def startReading(self) -> None:
        self._delay.start()
        self.remainingSecondsChanged.emit()
        self._timer.start()

    @Slot()
    def stopReading(self) -> None:
        self._timer.stop()
        self._delay = DisclaimerReadDelay()
        self.remainingSecondsChanged.emit()

    def _refresh_countdown(self) -> None:
        self.remainingSecondsChanged.emit()
        if self.remainingSeconds == 0:
            self._timer.stop()

    @Slot(result=bool)
    def accept(self) -> bool:
        if self._delay.remaining_seconds > 0:
            return False
        self._settings.accept_beta_disclaimer()
        return True
