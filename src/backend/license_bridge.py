"""Qt adapter for the shared asynchronous schema-2 licensing client."""
from __future__ import annotations

import asyncio
from datetime import datetime
import json
from pathlib import Path

from PySide6.QtCore import QObject, Property, QTimer, QUrl, Signal, Slot

from src.cli.licensing import LicenseService


MAX_LICENSE_BYTES = 32 * 1024


def load_production_config() -> dict[str, str]:
    path = Path(__file__).resolve().parents[2] / "license_client" / "production.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    allowed = {"public_key", "account_id", "product_id", "policy_id"}
    if set(data) != allowed:
        raise ValueError("The bundled license configuration contains unexpected fields")
    return data


class LicenseBridge(QObject):
    importFinished = Signal(bool, str)
    statusChanged = Signal()

    def __init__(self, service):
        super().__init__()
        self._service = service if isinstance(service, LicenseService) else LicenseService(service)
        self._busy = False
        QTimer.singleShot(0, self._startup_check)

    @Property(bool, notify=statusChanged)
    def isValid(self) -> bool:
        return self._service.status.allowed

    @Property(bool, notify=statusChanged)
    def isPremium(self) -> bool:
        return self._service.status.allowed

    @Property(str, notify=statusChanged)
    def state(self) -> str:
        return self._service.status.state

    @Property(str, notify=statusChanged)
    def reason(self) -> str:
        return self._service.reason

    @Property(str, notify=statusChanged)
    def expiresAt(self) -> str:
        expiry = self._service.status.expires_at
        return "" if expiry is None else datetime.fromtimestamp(expiry).astimezone().isoformat(timespec="minutes")

    @Property(bool, notify=statusChanged)
    def busy(self) -> bool:
        return self._busy

    # Compatibility properties retained while the QML migrates from schema 1.
    @Property(str, notify=statusChanged)
    def licenseKey(self) -> str:
        return ""

    @Property(list, notify=statusChanged)
    def features(self) -> list[str]:
        return ["full_unlock"] if self.isPremium else []

    def _set_status(self, status) -> None:
        self._service.status = status
        self.statusChanged.emit()

    async def _run_check(self, *, force: bool = False):
        status = await self._service.check(force=force)
        self._set_status(status)
        return status

    async def _import_from_path(self, path: Path):
        previous = self._service.status
        try:
            if path.stat().st_size > MAX_LICENSE_BYTES:
                raise ValueError("License files may not exceed 32 KiB")
            status = await self._service.client.import_license(path.read_bytes())
            self._set_status(status)
            self.importFinished.emit(status.allowed, self.reason)
            return status
        except Exception as error:
            self._service.status = previous
            self.statusChanged.emit()
            self.importFinished.emit(False, str(error))
            return previous

    def _start(self, operation_factory, *, imported: bool = False) -> None:
        if self._busy:
            return
        self._busy = True
        self.statusChanged.emit()

        async def run() -> None:
            success = False
            message = ""
            try:
                await operation_factory()
                success = self.isValid
                message = self.reason
            except Exception as error:
                message = str(error)
            finally:
                self._busy = False
                self.statusChanged.emit()
                if imported:
                    self.importFinished.emit(success, message)

        asyncio.create_task(run())

    @Slot(str)
    def installFromPath(self, file_url: str) -> None:
        local = Path(QUrl(file_url).toLocalFile())
        self._start(lambda: self._import_from_path(local))

    @Slot()
    def _startup_check(self) -> None:
        self._start(lambda: self._run_check(force=False))

    @Slot()
    def refresh(self) -> None:
        self._start(lambda: self._run_check(force=True))

    @Slot()
    def deactivate(self) -> None:
        self._start(self._deactivate)

    async def _deactivate(self):
        status = await self._service.deactivate()
        self._set_status(status)
        return status

    async def close(self) -> None:
        await self._service.close()

    async def shutdown(self) -> None:
        await self.close()
