"""
QML ↔ Python bridge for the license widget.

Exposes LicenseManager state as observable Qt properties so the QML UI
can react to changes automatically (no polling, no imperative refresh).
"""

from pathlib import Path
from typing import Callable, Optional

from PySide6.QtCore import QObject, QUrl, Property, Signal, Slot

from src.backend.check_license import LicenseManager, LicenseCheckResult
from src.backend.config import PUBLIC_KEY_B64
from src.backend.helper_functions import default_license_path


class LicenseBridge(QObject):
    """Bridge between the LicenseManager backend and the QML front-end."""

    # ── Signals ──────────────────────────────────────────────────────
    statusChanged = Signal()
    importFinished = Signal(bool, str)  # success, message

    # ── Constructor ──────────────────────────────────────────────────
    def __init__(
        self,
        setup_restrictions: Callable,
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)
        self._setup_restrictions = setup_restrictions

        self._lic = LicenseManager(
            public_key_b64=PUBLIC_KEY_B64,
            storage_path=default_license_path(),
            expected_product="porn-fetch",
        )

        self._is_valid: bool = False
        self._reason: str = ""
        self._license_key: str = ""
        self._features: list[str] = []

        # Initial load
        self._apply_result(self._lic.load_installed())

    # ── Qt Properties (read-only, observed by QML) ───────────────────

    @Property(bool, notify=statusChanged)
    def isValid(self) -> bool:
        return self._is_valid

    @Property(str, notify=statusChanged)
    def reason(self) -> str:
        return self._reason

    @Property(str, notify=statusChanged)
    def licenseKey(self) -> str:
        return self._license_key

    @Property(list, notify=statusChanged)
    def features(self) -> list[str]:
        return self._features

    # ── Slots (callable from QML) ────────────────────────────────────

    @Slot()
    def refresh(self) -> None:
        """Re-read the installed license and update all properties."""
        self._apply_result(self._lic.load_installed())

    @Slot(QUrl)
    def installFromPath(self, file_url: QUrl) -> None:
        """Install a license from a QUrl (called by the QML FileDialog).

        Args:
            file_url: A QUrl (e.g. QUrl('file:///home/user/key.license')).
                      QML FileDialogs return url types which map to QUrl.
        """
        print(f"[LicenseBridge] installFromPath called with: {file_url}")
        path = file_url.toLocalFile()
        print(f"[LicenseBridge] Resolved local path: '{path}'")
        if not path:
            print("[LicenseBridge] Empty path, aborting")
            return

        try:
            res = self._lic.install_from_file(Path(path))
            print(f"[LicenseBridge] Result: valid={res.valid}, reason={res.reason}")
            self._apply_result(self._lic.load_installed())
            self.importFinished.emit(res.valid, res.reason)
        except Exception as exc:
            print(f"[LicenseBridge] Exception during install: {exc}")
            self.importFinished.emit(False, f"Import error: {exc}")

    # ── Internal ─────────────────────────────────────────────────────

    def _apply_result(self, res: LicenseCheckResult) -> None:
        self._is_valid = res.valid
        self._reason = res.reason
        self._license_key = (res.data or {}).get("license_key", "")
        self._features = (res.data or {}).get("features", [])
        self.statusChanged.emit()
        self._setup_restrictions()
