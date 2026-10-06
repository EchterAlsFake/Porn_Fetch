"""Shared schema-2 licensing service used by both frontends."""
from __future__ import annotations

import json
import time
from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path
from typing import Any

from src.shared.paths import shared_data_dir

from .client import LicenseClient, LicenseError, LicenseStatus

REASONS = {
    "unlicensed": "No production license is installed.",
    "valid": "License active. This build is permanently entitled.",
    "activation_required": "Connect to activate this installation.",
    "activation_failed": "This installation could not be activated. Please contact support.",
    "offline_grace": "License server unavailable. Using the last successful validation.",
    "expired_grace": "Please connect to validate your license; the 7-day offline grace has ended.",
    "update_entitlement_expired": "Update entitlement expired. This version remains licensed permanently. Renew to receive newer Porn Fetch versions.",
    "renewal_required": "This version was released after your update entitlement ended. Renew to use this version; your earlier entitled versions remain licensed.",
    "entitlement_server_denied": "The server denied access after update entitlement ended. Your entitled versions remain licensed; contact support to correct the licensing policy.",
    "suspended_or_denied": "License authentication was denied. The license may be suspended; please contact support.",
    "suspended": "This license is suspended. Please contact support.",
    "revoked": "The licensing server has revoked this license.",
    "installation_limit": "This license has reached its activation limit.",
    "rejected": "The licensing server rejected this license.",
    "not_found": "The licensing server could not find this license or machine.",
    "deactivated": "This installation has been deactivated.",
    "deactivation_pending": "Deactivation is pending network access.",
    "deactivation_failed": "Deactivation failed. Please try again.",
    "clock_invalid": "Please correct the system clock and validate again.",
    "local_state_invalid": "Local licensing data could not be read. Contact support before resetting it to preserve your installation identity.",
    "invalid_signature": "The installed license or cached validation could not be verified. Please validate online again.",
    "network_unavailable": "Network unavailable. Connect to complete license activation.",
    "server_unavailable": "License server unavailable. Please try again shortly.",
    "malformed_response": "The license server returned an unreadable response. Please try again.",
    "beta_license": "This beta license belongs to an older licensing system and is no longer valid for the production release.",
}


def rejection_notice(state: str) -> str:
    return REASONS.get(state, REASONS["rejected"]) + "\n\nFor help, contact support@echteralsfake.me."


class LicenseService:
    def __init__(self, client: LicenseClient, core: Any | None = None) -> None:
        self.client = client
        self.core = core
        self.status = LicenseStatus("unlicensed", False)

    @property
    def status(self) -> LicenseStatus:
        # Frontend feature gates must not retain access after the offline deadline
        # while the user leaves the application open between asynchronous checks.
        status = self._status
        clock = getattr(self.client, "clock", time.time)
        if status.allowed and status.expires_at is not None and clock() >= status.expires_at:
            return replace(status, state="expired_grace", allowed=False)
        return status

    @status.setter
    def status(self, status: LicenseStatus) -> None:
        self._status = status

    @property
    def reason(self) -> str:
        reason = REASONS.get(self.status.state, self.status.state.replace("_", " ").capitalize())
        if self.status.state in ("update_entitlement_expired", "renewal_required") and self.status.license_expires_at is not None:
            from datetime import datetime, timezone
            end = datetime.fromtimestamp(self.status.license_expires_at, timezone.utc).strftime("%d %B %Y")
            reason = f"Your update entitlement ended on {end}. " + reason
        return reason

    async def check(self, *, force: bool = False) -> LicenseStatus:
        try:
            self.status = await self.client.check(force=force)
        except LicenseError:
            self.status = LicenseStatus("local_state_invalid", False)
            raise
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


def create_license_service(
    runtime_config: Any,
    state_path: str | Path | None = None,
    *,
    production_config: Mapping[str, str] | None = None,
) -> LicenseService:
    from .transport import LicensingCore

    if production_config is None:
        production_path = Path(__file__).with_name("production.json")
        production = json.loads(production_path.read_text(encoding="utf-8"))
    else:
        production = dict(production_config)
    core = LicensingCore()
    client = LicenseClient(
        state_path or shared_data_dir(), core=core,
        public_key=production["public_key"], account_id=production["account_id"],
        product_id=production["product_id"], policy_id=production["policy_id"],
        base_url=production["base_url"],
    )
    return LicenseService(client, core)
