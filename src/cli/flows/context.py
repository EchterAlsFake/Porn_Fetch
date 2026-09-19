"""Lifecycle and shared state for one interactive CLI session."""
from __future__ import annotations

import logging
from typing import Any

from rich.console import Console

from src.licensing.service import LicenseService, create_license_service
from src.shared.error_reporting import report_exception

from ..accounts import AccountService
from ..model_store import ModelStore
from ..providers import ClientPool
from ..settings import CliSettings, SettingsStore
from ..tracker import close_cli_tracker

logger = logging.getLogger(__name__)


class WizardContext:
    """Session context managing settings, active client pool, licensing, and accounts."""

    def __init__(
        self,
        settings: CliSettings,
        settings_store: SettingsStore,
        console: Console | None = None,
        *,
        model_store: ModelStore | None = None,
        pool: ClientPool | None = None,
        license_service: LicenseService | None = None,
    ) -> None:
        self.settings = settings
        self.settings_store = settings_store
        self.console = console or Console()
        self.model_store = model_store or ModelStore()
        config = self.settings.to_runtime_config()
        self.pool = pool or ClientPool(config)
        self.license_service = license_service or create_license_service(config)
        self.account_service = AccountService(self.pool)

    async def check_license(self, force: bool = False) -> Any:
        try:
            return await self.license_service.check(force=force)
        except Exception as error:
            logger.debug("License status refresh failed: %s", type(error).__name__)
            return self.license_service.status

    async def report(
        self, error: BaseException, operation: str, location: str, **context: Any,
    ) -> str:
        return await report_exception(
            error,
            operation=operation,
            location=location,
            context=context,
            enabled=self.settings.error_reporting,
        )

    async def refresh_pool(self) -> None:
        """Rebuild client pool and license service when settings change."""
        old_pool = self.pool
        old_lic = self.license_service
        config = self.settings.to_runtime_config()
        self.pool = ClientPool(config)
        self.license_service = create_license_service(config)
        await self.check_license()
        self.account_service = AccountService(self.pool)
        await old_lic.close()
        await old_pool.close()

    async def close(self) -> None:
        try:
            await self.license_service.close()
        except Exception:
            logger.exception("Could not close the CLI license service")
        try:
            await self.pool.close()
        except Exception:
            logger.exception("Could not close the CLI provider pool")
        try:
            await close_cli_tracker()
        except Exception:
            logger.exception("Could not close the CLI download tracker")
