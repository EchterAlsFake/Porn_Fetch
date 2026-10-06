"""Qt adapter for the shared asynchronous schema-2 licensing client."""
from __future__ import annotations

import asyncio
import json
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Property, QFile, QIODevice, QObject, QUrl, Signal, Slot

from src.licensing.service import LicenseService, rejection_notice

MAX_LICENSE_BYTES = 32 * 1024


def load_production_config() -> dict[str, str]:
    resource = QFile(":/licensing/production.json")
    if resource.exists():
        if not resource.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            raise OSError("Could not open the bundled license configuration")
        try:
            raw = bytes(resource.readAll()).decode("utf-8")
        finally:
            resource.close()
    else:
        path = Path(__file__).resolve().parents[1] / "licensing" / "production.json"
        raw = path.read_text(encoding="utf-8")

    data = json.loads(raw)
    allowed = {"public_key", "account_id", "product_id", "policy_id", "base_url"}
    if not isinstance(data, dict) or set(data) != allowed or not all(
        isinstance(value, str) and value for value in data.values()
    ):
        raise ValueError("The bundled license configuration contains unexpected fields")
    return data


class LicenseBridge(QObject):
    importFinished = Signal(bool, str)
    statusChanged = Signal()
    entitlementChanged = Signal()
    firstActivation = Signal()
    licenseRejected = Signal(str)

    def __init__(self, service, parent: QObject | None = None):
        super().__init__(parent)
        self._service = service if isinstance(service, LicenseService) else LicenseService(service)
        self._entitlement = (False, None)
        self._busy = False
        self._task: asyncio.Task[None] | None = None
        self._monitor_task: asyncio.Task[None] | None = None

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
    def licenseExpiresAt(self) -> str:
        if not self._service.status.allowed and self._service.status.state in ("unlicensed", "deactivated"):
            return ""
        expiry = self._service.status.license_expires_at
        if expiry is None:
            return "Lifetime / Never" if self._service.status.allowed else ""
        return datetime.fromtimestamp(expiry).astimezone().strftime("%Y-%m-%d %H:%M")

    @Property(str, notify=statusChanged)
    def nextCheckAt(self) -> str:
        if not self._service.status.allowed and self._service.status.state in ("unlicensed", "deactivated"):
            return ""
        check_time = self._service.status.next_check_at or self._service.status.expires_at
        return "" if check_time is None else datetime.fromtimestamp(check_time).astimezone().strftime("%Y-%m-%d %H:%M")

    @Property(str, notify=statusChanged)
    def expiresAt(self) -> str:
        expiry = self._service.status.expires_at
        return "" if expiry is None else datetime.fromtimestamp(expiry).astimezone().isoformat(timespec="minutes")

    @Property(bool, notify=statusChanged)
    def busy(self) -> bool:
        return self._busy

    def _set_status(self, status) -> None:
        self._service.status = status
        self.statusChanged.emit()
        entitlement = (status.allowed, status.license_expires_at)
        if entitlement != self._entitlement:
            self._entitlement = entitlement
            self.entitlementChanged.emit()
        if status.server_rejected:
            self.licenseRejected.emit(rejection_notice(status.state))

    async def _run_check(self, *, force: bool = False):
        try:
            status = await self._service.check(force=force)
        finally:
            self.statusChanged.emit()
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
            if not previous.allowed and status.allowed:
                self.firstActivation.emit()
            return status
        except Exception as error:
            self._service.status = previous
            self.statusChanged.emit()
            self.importFinished.emit(False, str(error))
            return previous

    async def _import_from_content_uri(self, file_url: str):
        previous = self._service.status
        try:
            source = QFile(file_url)
            if not source.open(QIODevice.OpenModeFlag.ReadOnly):
                raise OSError(source.errorString())
            try:
                blob = bytes(source.read(MAX_LICENSE_BYTES + 1))
            finally:
                source.close()
            if len(blob) > MAX_LICENSE_BYTES:
                raise ValueError("License files may not exceed 32 KiB")
            status = await self._service.client.import_license(blob)
            self._set_status(status)
            self.importFinished.emit(status.allowed, self.reason)
            if not previous.allowed and status.allowed:
                self.firstActivation.emit()
            return status
        except Exception as error:
            self._service.status = previous
            self.statusChanged.emit()
            self.importFinished.emit(False, str(error))
            return previous

    def _start(self, operation_factory, *, imported: bool = False) -> asyncio.Task[None] | None:
        if self._busy:
            return None

        # Resolve the loop before changing state or constructing a coroutine.
        # Qt timers may run while QML is loading, before QtAsyncio.run() has
        # installed a running asyncio loop.
        loop = asyncio.get_running_loop()
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

        task = loop.create_task(run(), name="license-operation")
        self._task = task

        def clear_task(completed: asyncio.Task[None]) -> None:
            if self._task is completed:
                self._task = None

        task.add_done_callback(clear_task)
        return task

    def start(self) -> asyncio.Task[None] | None:
        """Start the initial license check from the running QtAsyncio loop."""
        if self._monitor_task is None:
            async def monitor():
                while True:
                    await asyncio.sleep(60)
                    if not self._busy:
                        self._start(lambda: self._run_check())
            self._monitor_task = asyncio.create_task(monitor(), name="license-refresh")
        return self._start(lambda: self._run_check(force=True))

    @Slot(str)
    def installFromPath(self, file_url: str) -> None:
        url = QUrl(file_url)
        if url.scheme() == "content":
            self._start(lambda: self._import_from_content_uri(file_url))
        else:
            local = Path(url.toLocalFile() if url.isLocalFile() else file_url)
            self._start(lambda: self._import_from_path(local))

    @Slot(str)
    def installFromText(self, text: str) -> None:
        async def install():
            previous = self._service.status
            status = await self._service.client.import_license(text)
            self._set_status(status)
            if status.allowed and not previous.allowed:
                self.firstActivation.emit()
        self._start(install, imported=True)

    @Slot()
    def refresh(self) -> None:
        self._start(lambda: self._run_check(force=True))

    @Slot()
    def showActivationHelp(self) -> None:
        self.firstActivation.emit()

    @Slot()
    def deactivate(self) -> None:
        self._start(self._deactivate)

    async def _deactivate(self):
        status = await self._service.deactivate()
        self._set_status(status)
        return status

    async def close(self) -> None:
        if self._monitor_task is not None:
            self._monitor_task.cancel()
            await asyncio.gather(self._monitor_task, return_exceptions=True)
            self._monitor_task = None
        if self._task is not None and not self._task.done():
            self._task.cancel()
            await asyncio.gather(self._task, return_exceptions=True)
        self._task = None
        await self._service.close()

    async def shutdown(self) -> None:
        await self.close()
