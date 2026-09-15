"""Shared schema-2 licensing service used by both frontends."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from license_client import LicenseClient, LicenseStatus

from .paths import shared_data_dir


REASONS = {
    "unlicensed": "No schema-2 license is installed.",
    "valid": "License active.",
    "provisional": "License active; activation is pending.",
    "offline_grace": "License active in offline grace period.",
    "expired_grace": "The offline license permit has expired.",
    "deactivated": "This installation has been deactivated.",
    "deactivation_pending": "Deactivation is pending network access.",
    "clock_invalid": "The system clock could not be trusted.",
    "invalid_signature": "The installed license could not be verified.",
}


class LicenseService:
    def __init__(self, client: LicenseClient, core: Any | None = None) -> None:
        self.client = client
        self.core = core
        self.status = LicenseStatus("unlicensed", False)

    @property
    def reason(self) -> str:
        return REASONS.get(self.status.state, self.status.state.replace("_", " ").capitalize())

    async def check(self, *, force: bool = False) -> LicenseStatus:
        self.status = await self.client.check(force=force)
        return self.status

    async def import_file(self, path: str | Path) -> LicenseStatus:
        source = Path(path)
        if source.stat().st_size > 32 * 1024:
            raise ValueError("License files may not exceed 32 KiB")
        blob = source.read_bytes()
        self.status = await self.client.import_license(blob)
        return self.status

    async def deactivate(self) -> LicenseStatus:
        self.status = await self.client.deactivate()
        return self.status

    async def close(self) -> None:
        await self.client.close()
        if self.core is not None:
            await self.core.close()


def create_license_service(runtime_config: Any, state_path: str | Path | None = None) -> LicenseService:
    from base_api import BaseCore

    production_path = Path(__file__).resolve().parents[2] / "license_client" / "production.json"
    production = json.loads(production_path.read_text(encoding="utf-8"))
    core = BaseCore(configuration=runtime_config)
    client = LicenseClient(
        state_path or shared_data_dir(), core=core,
        public_key=production["public_key"], account_id=production["account_id"],
        product_id=production["product_id"], policy_id=production["policy_id"],
    )
    return LicenseService(client, core)
