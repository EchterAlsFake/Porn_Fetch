"""Keygen CE client using Porn Fetch's shared asynchronous BaseCore transport."""
from __future__ import annotations

import asyncio
import base64
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime
import json
import math
import os
from pathlib import Path
import sqlite3
import time
from typing import Any, Callable, Protocol
import uuid

from base_api.modules.errors import AccessDeniedError, HTTPStatusError
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

WEEK = 604800
DAY = 86400


class AsyncRequestCore(Protocol):
    async def request(self, url: str, **kwargs: Any) -> Any: ...


class LicenseError(ValueError):
    """Invalid input or unusable local licensing state; contains no credentials."""


class TemporaryFailure(Exception):
    pass


class Rejected(Exception):
    def __init__(self, state: str):
        self.state = state


@dataclass(frozen=True)
class LicenseStatus:
    state: str
    allowed: bool
    expires_at: float | None = None


def decode(value: str, *, url: bool = False) -> bytes:
    return base64.b64decode(value, altchars=b"-_" if url else None, validate=True)


def timestamp(value: str) -> float:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Naive timestamp")
    return parsed.timestamp()


class LicenseClient:
    """Persist and validate schema-2 licenses without owning a network session."""

    def __init__(
        self,
        state_dir: str | Path,
        *,
        core: AsyncRequestCore,
        public_key: str,
        account_id: str,
        product_id: str,
        policy_id: str,
        base_url: str = "https://licenses.echteralsfake.me",
        clock: Callable[[], float] = time.time,
        monotonic: Callable[[], float] = time.monotonic,
    ) -> None:
        if not base_url.startswith("https://"):
            raise LicenseError("The licensing endpoint must use HTTPS")
        try:
            self.public_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key))
        except (TypeError, ValueError):
            raise LicenseError("The bundled licensing public key is invalid") from None
        self.account_id = account_id
        self.product_id = product_id
        self.policy_id = policy_id
        self.core = core
        self.base_url = base_url.rstrip("/") + "/v1/"
        self.clock = clock
        self.monotonic = monotonic
        self.anchor_wall = clock()
        self.anchor_mono = monotonic()
        self.directory = Path(state_dir)
        self.path = self.directory / "licensing.sqlite3"
        self._closed = False

    @staticmethod
    def _validate_state(state: Any) -> dict[str, Any]:
        def finite_number(value: Any) -> bool:
            return (
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and math.isfinite(value)
            )

        if not isinstance(state, dict) or not isinstance(state.get("licenses"), dict):
            raise LicenseError(
                "Local license state is unreadable; do not reset it automatically"
            )
        try:
            installation_id = uuid.UUID(state.get("installation_id", ""))
        except (AttributeError, TypeError, ValueError):
            installation_id = None
        if installation_id is None or installation_id.version != 4:
            raise LicenseError(
                "Local license state is unreadable; do not reset it automatically"
            )
        if "last_seen" in state and not finite_number(state["last_seen"]):
            raise LicenseError(
                "Local license state is unreadable; do not reset it automatically"
            )

        licenses = state["licenses"]
        for license_id, record in licenses.items():
            if (
                not isinstance(license_id, str)
                or not isinstance(record, dict)
                or not isinstance(record.get("key"), str)
                or not finite_number(record.get("first_import"))
                or not isinstance(record.get("activated"), bool)
            ):
                raise LicenseError(
                    "Local license state is unreadable; do not reset it automatically"
                )
            optional_numbers = ("retry_at", "renewed")
            if any(
                name in record and not finite_number(record[name])
                for name in optional_numbers
            ):
                raise LicenseError(
                    "Local license state is unreadable; do not reset it automatically"
                )
            if "failures" in record and (
                not isinstance(record["failures"], int)
                or isinstance(record["failures"], bool)
            ):
                raise LicenseError(
                    "Local license state is unreadable; do not reset it automatically"
                )
            if "offline" in record and not isinstance(record["offline"], bool):
                raise LicenseError(
                    "Local license state is unreadable; do not reset it automatically"
                )
            if "blocked" in record and record["blocked"] is not None and not isinstance(
                record["blocked"], str
            ):
                raise LicenseError(
                    "Local license state is unreadable; do not reset it automatically"
                )
            if "permit" in record and record["permit"] is not None and not isinstance(
                record["permit"], str
            ):
                raise LicenseError(
                    "Local license state is unreadable; do not reset it automatically"
                )

        active = state.get("active")
        if active is not None and (not isinstance(active, str) or active not in licenses):
            raise LicenseError(
                "Local license state is unreadable; do not reset it automatically"
            )
        return state

    def _prepare_state_path(self) -> None:
        try:
            self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
            if os.name != "nt":
                os.chmod(self.directory, 0o700)
            if not self.path.exists():
                try:
                    descriptor = os.open(
                        self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600
                    )
                except FileExistsError:
                    # Another application process won the first-start race.
                    pass
                else:
                    os.close(descriptor)
            if os.name != "nt":
                os.chmod(self.path, 0o600)
        except OSError:
            raise LicenseError(
                "Local license state is unreadable; do not reset it automatically"
            ) from None

    @asynccontextmanager
    async def _state(self):
        self._prepare_state_path()
        deadline = asyncio.get_running_loop().time() + 30
        connection = None
        try:
            while True:
                try:
                    connection = sqlite3.connect(self.path, timeout=0)
                    connection.execute(
                        "CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY, value TEXT NOT NULL)"
                    )
                    connection.execute("BEGIN IMMEDIATE")
                    break
                except sqlite3.OperationalError as error:
                    if connection is not None:
                        connection.close()
                        connection = None
                    if "locked" not in str(error).casefold() or asyncio.get_running_loop().time() >= deadline:
                        raise LicenseError(
                            "Local license state is unreadable; do not reset it automatically"
                        ) from None
                    await asyncio.sleep(0.05)
            row = connection.execute("SELECT value FROM state WHERE id=1").fetchone()
            if row:
                state = self._validate_state(json.loads(row[0]))
            else:
                state = {
                    "installation_id": str(uuid.uuid4()),
                    "licenses": {},
                }
            yield state
            connection.execute("INSERT OR REPLACE INTO state VALUES (1, ?)", (json.dumps(state),))
            connection.commit()
        except (sqlite3.Error, json.JSONDecodeError):
            if connection is not None:
                connection.rollback()
            raise LicenseError("Local license state is unreadable; do not reset it automatically") from None
        finally:
            if connection is not None:
                connection.close()

    async def close(self) -> None:
        """Release this logical client; the application owns and closes BaseCore."""
        self._closed = True

    def verify_key(self, key: str) -> dict[str, Any]:
        try:
            if not isinstance(key, str) or len(key) > 16384 or not key.startswith("key/"):
                raise ValueError
            message, signature = key.rsplit(".", 1)
            self.public_key.verify(decode(signature, url=True), message.encode("ascii"))
            payload = json.loads(decode(message[4:], url=True))
            if (
                payload["account"]["id"] != self.account_id
                or payload["product"]["id"] != self.product_id
                or payload["policy"]["id"] != self.policy_id
                or payload["policy"]["duration"] is not None
                or payload["license"]["expiry"] is not None
            ):
                raise ValueError
            uuid.UUID(payload["license"]["id"])
            timestamp(payload["license"]["created"])
            return payload
        except (ValueError, KeyError, TypeError, UnicodeError, InvalidSignature):
            raise LicenseError("License signature or signed claims are invalid") from None

    def verify_permit(
        self,
        certificate: str,
        *,
        license_id: str,
        installation_id: str,
        now: float,
    ) -> dict[str, Any]:
        try:
            if not isinstance(certificate, str) or len(certificate) > 65536:
                raise ValueError
            prefix = "-----BEGIN MACHINE FILE-----\n"
            suffix = "-----END MACHINE FILE-----\n"
            if not certificate.startswith(prefix) or not certificate.endswith(suffix):
                raise ValueError
            encoded = "".join(certificate[len(prefix):-len(suffix)].split())
            document = json.loads(decode(encoded))
            if document["alg"] != "base64+ed25519":
                raise ValueError
            self.public_key.verify(
                decode(document["sig"]),
                ("machine/" + document["enc"]).encode("ascii"),
            )
            payload = json.loads(decode(document["enc"]))
            meta = payload["meta"]
            machine = payload["data"]
            issued = timestamp(meta["issued"])
            expiry = timestamp(meta["expiry"])
            if type(meta["ttl"]) is not int or not 0 < meta["ttl"] <= WEEK:
                raise ValueError
            if abs(expiry - issued - meta["ttl"]) > 1 or issued > now + 300:
                raise ValueError
            relationships = machine["relationships"]
            if (
                machine["type"] != "machines"
                or relationships["account"]["data"]["id"] != self.account_id
                or relationships["product"]["data"]["id"] != self.product_id
                or relationships["license"]["data"]["id"] != license_id
                or machine["attributes"]["fingerprint"] != installation_id
            ):
                raise ValueError
            licenses = [
                item for item in payload["included"]
                if item["type"] == "licenses" and item["id"] == license_id
            ]
            if len(licenses) != 1:
                raise ValueError
            attributes = licenses[0]["attributes"]
            if attributes["suspended"] or attributes["expiry"] is not None:
                raise ValueError
            if licenses[0]["relationships"]["policy"]["data"]["id"] != self.policy_id:
                raise ValueError
            return {"issued": issued, "expiry": expiry, "machine_id": machine["id"]}
        except (ValueError, KeyError, TypeError, UnicodeError, InvalidSignature):
            raise LicenseError("Machine permit signature or signed claims are invalid") from None

    async def _request(
        self,
        method: str,
        path: str,
        key: str,
        *,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        request = self.core.request(
            url=self.base_url + path,
            method=method,
            headers={
                "Authorization": "License " + key,
                "Accept": "application/vnd.api+json",
                "Content-Type": "application/vnd.api+json",
                "User-Agent": "license-client",
            },
            json_data=json_data,
            allow_redirects=False,
        )
        try:
            response = await request
        except AccessDeniedError:
            raise Rejected("rejected") from None
        except HTTPStatusError as error:
            if error.status_code in (408, 425, 429) or error.status_code >= 500:
                raise TemporaryFailure from None
            if error.status_code == 404:
                raise Rejected("not_found") from None
            if error.status_code in (409, 422) and method == "POST" and path == "machines":
                raise Rejected("machine_conflict_or_limit") from None
            raise Rejected("rejected") from None
        except Exception:
            raise TemporaryFailure from None
        if response.status_code == 204:
            return {}
        try:
            return response.json()
        except (ValueError, TypeError, AttributeError):
            raise TemporaryFailure from None

    async def import_license(self, blob: bytes | str) -> LicenseStatus:
        if self._closed:
            raise LicenseError("The licensing client is closed")
        try:
            if len(blob) > 32768:
                raise ValueError
            envelope = json.loads(blob)
            if envelope["schema"] != 2:
                raise ValueError
            key = envelope["license_key"]
            claims = self.verify_key(key)
        except (ValueError, KeyError, TypeError):
            raise LicenseError("Import a valid schema-2 license file") from None
        license_id = claims["license"]["id"]
        async with self._state() as state:
            state["active"] = license_id
            record = state["licenses"].setdefault(
                license_id,
                {"key": key, "first_import": self.clock(), "activated": False},
            )
            if record["key"] != key:
                raise LicenseError("A different credential already exists for this license")
        return await self.check(force=True)

    async def _refresh(
        self,
        state: dict[str, Any],
        record: dict[str, Any],
        license_id: str,
        now: float,
    ) -> dict[str, Any]:
        key = record["key"]
        fingerprint = state["installation_id"]
        response = await self._request(
            "POST",
            "licenses/actions/validate-key",
            key,
            json_data={"meta": {"key": key, "scope": {
                "fingerprint": fingerprint,
                "product": self.product_id,
                "policy": self.policy_id,
            }}},
        )
        meta = response["meta"]
        code = meta.get("code")
        if not meta.get("valid") and code not in (
            "NO_MACHINE", "NO_MACHINES", "FINGERPRINT_SCOPE_MISMATCH"
        ):
            raise Rejected(
                "revoked" if code in ("SUSPENDED", "EXPIRED")
                else "installation_limit" if code in (
                    "TOO_MANY_MACHINES", "MACHINE_LIMIT_EXCEEDED"
                )
                else "rejected"
            )
        ambiguous_machine_error = False
        if not meta.get("valid"):
            try:
                await self._request(
                    "POST",
                    "machines",
                    key,
                    json_data={"data": {
                        "type": "machines",
                        "attributes": {"fingerprint": fingerprint},
                        "relationships": {"license": {"data": {
                            "type": "licenses", "id": license_id,
                        }}},
                    }},
                )
            except Rejected as error:
                if error.state != "machine_conflict_or_limit":
                    raise
                ambiguous_machine_error = True
        try:
            machine = (await self._request("GET", "machines/" + fingerprint, key))["data"]
        except Rejected as error:
            if ambiguous_machine_error and error.state == "not_found":
                raise Rejected("installation_limit") from None
            raise
        certificate = (await self._request(
            "POST",
            "machines/" + machine["id"] + "/actions/check-out",
            key,
            json_data={"meta": {
                "ttl": WEEK,
                "algorithm": "base64+ed25519",
                "include": ["license"],
            }},
        ))["data"]["attributes"]["certificate"]
        permit = self.verify_permit(
            certificate,
            license_id=license_id,
            installation_id=fingerprint,
            now=now,
        )
        if permit["expiry"] <= now:
            raise LicenseError("The renewed permit has already expired")
        record.update(
            permit=certificate,
            activated=True,
            blocked=None,
            offline=False,
            retry_at=0,
            failures=0,
            renewed=permit["issued"],
        )
        return permit

    async def check(self, *, force: bool = False) -> LicenseStatus:
        if self._closed:
            raise LicenseError("The licensing client is closed")
        now = self.clock()
        async with self._state() as state:
            license_id = state.get("active")
            if not license_id:
                return LicenseStatus("unlicensed", False)
            record = state["licenses"][license_id]
            try:
                self.verify_key(record["key"])
            except LicenseError:
                return LicenseStatus("invalid_signature", False)
            expected = self.anchor_wall + (self.monotonic() - self.anchor_mono)
            rollback = now < max(state.get("last_seen", now), expected) - 300
            state["last_seen"] = max(now, state.get("last_seen", now))
            due = force or rollback or now - record.get("renewed", 0) >= DAY
            if due and (force or now >= record.get("retry_at", 0)):
                try:
                    await self._refresh(state, record, license_id, now)
                except TemporaryFailure:
                    failures = min(record.get("failures", 0) + 1, 7)
                    record.update(
                        offline=True,
                        failures=failures,
                        retry_at=now + min(60 * 2 ** (failures - 1), 3600),
                    )
                except Rejected as error:
                    record.update(blocked=error.state, retry_at=now + 60)
                except (LicenseError, KeyError, TypeError):
                    record.update(blocked="invalid_signature", retry_at=now + 60)
            if rollback:
                return LicenseStatus("clock_invalid", False)
            if record.get("blocked"):
                return LicenseStatus(record["blocked"], False)
            if record["activated"]:
                try:
                    permit = self.verify_permit(
                        record["permit"],
                        license_id=license_id,
                        installation_id=state["installation_id"],
                        now=now,
                    )
                except (LicenseError, KeyError):
                    return LicenseStatus("invalid_signature", False)
                expiry = permit["expiry"]
                return LicenseStatus(
                    "expired_grace" if now >= expiry
                    else "offline_grace" if record.get("offline")
                    else "valid",
                    now < expiry,
                    expiry,
                )
            expiry = record["first_import"] + WEEK
            return LicenseStatus(
                "provisional" if now < expiry else "expired_grace",
                now < expiry,
                expiry,
            )

    async def deactivate(self) -> LicenseStatus:
        if self._closed:
            raise LicenseError("The licensing client is closed")
        async with self._state() as state:
            license_id = state.get("active")
            if not license_id:
                return LicenseStatus("unlicensed", False)
            record = state["licenses"][license_id]
            try:
                machine = (await self._request(
                    "GET", "machines/" + state["installation_id"], record["key"]
                ))["data"]
                await self._request("DELETE", "machines/" + machine["id"], record["key"])
            except TemporaryFailure:
                return LicenseStatus("deactivation_pending", False)
            except Rejected as error:
                if error.state != "not_found":
                    return LicenseStatus("deactivation_failed", False)
            record.update(blocked="deactivated", permit=None, activated=True, retry_at=0)
            state.pop("active", None)
            return LicenseStatus("deactivated", False)
