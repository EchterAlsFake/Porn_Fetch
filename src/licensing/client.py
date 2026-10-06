"""Keygen CE client using Porn Fetch's shared asynchronous BaseCore transport."""
from __future__ import annotations

import asyncio
import base64
import json
import math
import os
import sqlite3
import time
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Protocol
from urllib.parse import urlsplit

from base_api.modules.errors import AccessDeniedError, HTTPStatusError
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from src.shared.version import RELEASE_TIMESTAMP

WEEK = 604800
DAY = 86400


class AsyncRequestCore(Protocol):
    async def request(self, url: str, **kwargs: Any) -> Any: ...


class LicenseError(ValueError):
    """Invalid input or unusable local licensing state; contains no credentials."""


class TemporaryFailure(Exception):
    def __init__(self, state: str = "network_unavailable"):
        self.state = state


class BetaLicenseError(LicenseError):
    """An old credential must never be sent to the production endpoint."""


BETA_MESSAGE = "This beta license belongs to an older licensing system and is no longer valid for the production release."
BETA_POLICY = "564897fa-b8d9-4871-82a4-0b49fd50bc1e"
BETA_ACCOUNT = "2779db33-8e9b-4c5f-b1b5-ee5957939c20"


class Rejected(Exception):
    def __init__(self, state: str):
        self.state = state


@dataclass(frozen=True)
class LicenseStatus:
    state: str
    allowed: bool
    expires_at: float | None = None
    license_expires_at: float | None = None
    next_check_at: float | None = None
    server_rejected: bool = False
    failure: str | None = None

    def entitled_to(self, release_timestamp: float) -> bool:
        return self.allowed and self.license_expires_at is not None and release_timestamp <= self.license_expires_at


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
        base_url: str = "https://licenses.pornfetch.to",
        clock: Callable[[], float] = time.time,
        monotonic: Callable[[], float] = time.monotonic,
        release_timestamp: float = RELEASE_TIMESTAMP,
    ) -> None:
        endpoint = urlsplit(base_url)
        if endpoint.scheme != "https" or not endpoint.netloc or endpoint.username or endpoint.password or endpoint.query or endpoint.fragment or endpoint.path not in ("", "/"):
            raise LicenseError("The licensing endpoint must use HTTPS")
        try:
            self.public_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key))
        except (TypeError, ValueError):
            raise LicenseError("The bundled licensing public key is invalid") from None
        self.account_id = account_id
        self.product_id = product_id
        self.policy_id = policy_id
        self.core = core
        self.base_url = base_url.rstrip("/") + "/v1/accounts/" + str(uuid.UUID(account_id)) + "/"
        self.release_timestamp = release_timestamp
        self.clock = clock
        self.monotonic = monotonic
        self.anchor_wall = clock()
        self.anchor_mono = monotonic()
        self.directory = Path(state_dir)
        self.path = self.directory / "licensing.sqlite3"
        self._closed = False
        self._startup_pending = True

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
        if installation_id is None or installation_id.version != 4 or str(installation_id) != state["installation_id"]:
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
            optional_numbers = ("retry_at", "renewed", "last_successful_validation")
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
            if "license_expiry" in record and record["license_expiry"] is not None and not finite_number(record["license_expiry"]):
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
            # Untrusted inspection is used ONLY to reject known beta material, never to grant access.
            candidate = json.loads(decode(message[4:], url=True))
            if isinstance(candidate, dict) and (candidate.get("account", {}).get("id") == BETA_ACCOUNT or candidate.get("policy", {}).get("id") == BETA_POLICY):
                raise BetaLicenseError(BETA_MESSAGE)
            self.public_key.verify(decode(signature, url=True), message.encode("ascii"))
            payload = json.loads(decode(message[4:], url=True))
            if (
                payload["account"]["id"] != self.account_id
                or payload["product"]["id"] != self.product_id
                or payload["policy"]["id"] != self.policy_id
            ):
                raise ValueError
            uuid.UUID(payload["license"]["id"])
            timestamp(payload["license"]["created"])
            lic_exp = payload["license"].get("expiry")
            if lic_exp is not None:
                timestamp(lic_exp)
            return payload
        except BetaLicenseError:
            raise
        except (ValueError, KeyError, TypeError, AttributeError, UnicodeError, InvalidSignature):
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
            if attributes["suspended"] is not False:
                raise ValueError
            lic_expiry = None
            if attributes.get("expiry") is not None:
                lic_expiry = timestamp(attributes["expiry"])
            if licenses[0]["relationships"]["policy"]["data"]["id"] != self.policy_id:
                raise ValueError
            return {
                "issued": issued,
                "expiry": expiry,
                "machine_id": machine["id"],
                "license_expiry": lic_expiry,
            }
        except (ValueError, KeyError, TypeError, AttributeError, UnicodeError, InvalidSignature):
            raise LicenseError("Machine permit signature or signed claims are invalid") from None

    async def _request(
        self,
        method: str,
        path: str,
        key: str,
        *,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        # Validation is safe to repeat. Machine creation and checkout are never retried here.
        attempts = 2 if method == "GET" or path == "licenses/actions/validate-key" else 1
        for attempt in range(attempts):
            try:
                async with asyncio.timeout(25):
                    response = await self.core.request(
                        url=self.base_url + path, method=method,
                        headers={"Authorization": "License " + key,
                                 "Accept": "application/vnd.api+json",
                                 "Content-Type": "application/vnd.api+json",
                                 "User-Agent": "PornFetch-license-client"},
                        json_data=json_data, allow_redirects=False,
                        timeout=(5, 20), retry_non_idempotent=False,
                    )
                status = response.status_code
                if status == 204:
                    return {}
                if status in (408, 425, 429) or status >= 500:
                    raise TemporaryFailure("server_unavailable")
                try:
                    body = response.json()
                    if not isinstance(body, dict):
                        raise ValueError
                except (ValueError, TypeError, AttributeError):
                    if status in (401, 403):
                        raise Rejected("suspended_or_denied" if status == 403 else "rejected") from None
                    if status == 404:
                        raise Rejected("not_found") from None
                    raise TemporaryFailure("malformed_response") from None
                if not 200 <= status < 300:
                    errors = body.get("errors", [])
                    codes = {item.get("code") for item in errors if isinstance(item, dict)} if isinstance(errors, list) else set()
                    if codes & {"MACHINE_LIMIT_EXCEEDED", "MACHINE_LIMIT_EXCEEDED_FOR_LICENSE", "TOO_MANY_MACHINES"}:
                        raise Rejected("installation_limit")
                    if codes & {"LICENSE_SUSPENDED"}:
                        raise Rejected("suspended")
                    if status == 403:
                        raise Rejected("suspended_or_denied")
                    if codes & {"FINGERPRINT_TAKEN"} and path == "machines":
                        raise Rejected("machine_conflict")
                    if status == 404:
                        raise Rejected("not_found")
                    raise Rejected("activation_failed" if path == "machines" else "rejected")
                return body
            except Rejected:
                raise
            except AccessDeniedError:
                raise Rejected("rejected") from None
            except HTTPStatusError as error:
                if error.status_code == 404:
                    raise Rejected("not_found") from None
                if error.status_code not in (408, 425, 429) and error.status_code < 500:
                    raise Rejected("activation_failed" if path == "machines" else "rejected") from None
                failure = TemporaryFailure("server_unavailable")
            except TemporaryFailure as error:
                failure = error
            except Exception:
                failure = TemporaryFailure("network_unavailable")
            if attempt + 1 == attempts:
                raise failure from None
            await asyncio.sleep(0.1)
        raise TemporaryFailure

    async def import_license(self, blob: bytes | str) -> LicenseStatus:
        if self._closed:
            raise LicenseError("The licensing client is closed")
        try:
            if len(blob) > 32768:
                raise ValueError
            text = blob.decode("utf-8") if isinstance(blob, bytes) else blob
            if text.startswith("key/"):
                key = text
            else:
                envelope = json.loads(text)
                if envelope["schema"] != 2:
                    raise BetaLicenseError(BETA_MESSAGE)
                key = envelope["license_key"]
            claims = self.verify_key(key)
        except BetaLicenseError:
            raise
        except (ValueError, KeyError, TypeError):
            raise LicenseError("Import a valid production license file or signed key") from None
        license_id = claims["license"]["id"]
        lic_expiry = None
        if claims["license"].get("expiry") is not None:
            lic_expiry = timestamp(claims["license"]["expiry"])
        async with self._state() as state:
            state["active"] = license_id
            record = state["licenses"].setdefault(
                license_id,
                {
                    "key": key,
                    "first_import": self.clock(),
                    "activated": False,
                    "license_expiry": lic_expiry,
                },
            )
            if record["key"] != key:
                raise LicenseError("A different credential already exists for this license")
            if "license_expiry" not in record or record.get("license_expiry") != lic_expiry:
                record["license_expiry"] = lic_expiry
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
        async def validate() -> dict[str, Any]:
            response = await self._request(
                "POST", "licenses/actions/validate-key", key,
                json_data={"meta": {"key": key, "scope": {
                    "fingerprint": fingerprint, "product": self.product_id, "policy": self.policy_id,
                }}},
            )
            meta = response.get("meta")
            data = response.get("data")
            if (not isinstance(meta, dict) or type(meta.get("valid")) is not bool
                    or not isinstance(meta.get("code"), str)):
                raise TemporaryFailure("malformed_response")
            if not meta["valid"] and meta["code"] not in ("NO_MACHINE", "NO_MACHINES", "FINGERPRINT_SCOPE_MISMATCH"):
                require_valid(meta)
            if not isinstance(data, dict):
                raise TemporaryFailure("malformed_response")
            if (data.get("type") != "licenses" or data.get("id") != license_id
                    or data["relationships"]["account"]["data"]["id"] != self.account_id
                    or data["relationships"]["product"]["data"]["id"] != self.product_id
                    or data["relationships"]["policy"]["data"]["id"] != self.policy_id):
                raise Rejected("rejected")
            # EXPIRED can be valid with MAINTAIN_ACCESS. Never override valid=false.
            if meta["valid"] and meta["code"] not in ("VALID", "EXPIRED"):
                raise Rejected("rejected")
            return meta

        def require_valid(meta: dict[str, Any]) -> None:
            if not meta["valid"]:
                raise Rejected({
                    "SUSPENDED": "suspended", "BANNED": "revoked",
                    "EXPIRED": "entitlement_server_denied", "NOT_FOUND": "not_found",
                    "TOO_MANY_MACHINES": "installation_limit",
                    "MACHINE_LIMIT_EXCEEDED": "installation_limit",
                }.get(meta["code"], "rejected"))

        meta = await validate()
        if not meta["valid"] and meta["code"] in ("NO_MACHINE", "NO_MACHINES", "FINGERPRINT_SCOPE_MISMATCH"):
            try:
                await self._request("POST", "machines", key, json_data={"data": {
                    "type": "machines", "attributes": {"fingerprint": fingerprint},
                    "relationships": {"license": {"data": {"type": "licenses", "id": license_id}}},
                }})
            except Rejected as error:
                if error.state != "machine_conflict":
                    raise
            except TemporaryFailure:
                # The server may have committed creation before the connection timed out.
                reconciled = await validate()
                if not reconciled["valid"]:
                    raise TemporaryFailure("network_unavailable") from None
            # A successful create (or duplicate fingerprint race) is not validation.
            meta = await validate()
        require_valid(meta)
        validated_at = self.clock()
        machine = (await self._request("GET", "machines/" + fingerprint, key))["data"]
        try:
            machine_id = str(uuid.UUID(machine["id"]))
        except (ValueError, TypeError, AttributeError):
            raise TemporaryFailure("malformed_response") from None
        certificate = (await self._request(
            "POST",
            "machines/" + machine_id + "/actions/check-out",
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
        if permit["license_expiry"] is None:
            raise LicenseError("The commercial entitlement deadline is missing")
        if permit["expiry"] <= now:
            raise LicenseError("The renewed permit has already expired")
        license_expiry = permit["license_expiry"]
        record.update(
            permit=certificate,
            activated=True,
            blocked=None,
            offline=False,
            retry_at=0,
            failures=0,
            renewed=permit["issued"],
            last_successful_validation=validated_at,
            cache_version=2,
            license_expiry=license_expiry,
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
                if self.verify_key(record["key"])["license"]["id"] != license_id:
                    raise LicenseError("Cached license identity mismatch")
            except BetaLicenseError:
                return LicenseStatus("beta_license", False)
            except LicenseError:
                return LicenseStatus("invalid_signature", False)
            expected = self.anchor_wall + (self.monotonic() - self.anchor_mono)
            rollback = now < max(state.get("last_seen", now), expected) - 300
            state["last_seen"] = max(now, state.get("last_seen", now))
            due = force or self._startup_pending or rollback or record.get("cache_version") != 2 or now - record.get("renewed", 0) >= DAY
            startup = self._startup_pending
            self._startup_pending = False
            server_rejected = False
            if due and (force or startup or now >= record.get("retry_at", 0)):
                try:
                    await self._refresh(state, record, license_id, now)
                except (TemporaryFailure, AttributeError, KeyError, TypeError) as error:
                    failures = min(record.get("failures", 0) + 1, 7)
                    record.update(
                        offline=True,
                        failure=error.state if isinstance(error, TemporaryFailure) else "malformed_response",
                        failures=failures,
                        retry_at=now + min(60 * 2 ** (failures - 1), 3600),
                    )
                except Rejected as error:
                    record.update(blocked=error.state, retry_at=now + 60)
                    server_rejected = True
                except LicenseError:
                    record.update(blocked="invalid_signature", retry_at=now + 60)
            now = self.clock()
            state["last_seen"] = max(now, state.get("last_seen", now))
            license_expiry = record.get("license_expiry")
            if rollback:
                return LicenseStatus("clock_invalid", False, license_expires_at=license_expiry)
            if record.get("blocked"):
                return LicenseStatus(
                    record["blocked"], False,
                    license_expires_at=license_expiry,
                    server_rejected=server_rejected,
                )
            if record["activated"] and record.get("cache_version") == 2:
                try:
                    permit = self.verify_permit(
                        record["permit"], license_id=license_id,
                        installation_id=state["installation_id"], now=now,
                    )
                    if permit["license_expiry"] is None:
                        raise LicenseError("Missing entitlement deadline")
                    last_success = record["last_successful_validation"]
                    if not permit["issued"] - 300 <= last_success <= permit["issued"] + 300:
                        raise LicenseError("Invalid cached validation time")
                except (LicenseError, KeyError):
                    return LicenseStatus("invalid_signature", False)
                expiry = min(permit["expiry"], last_success + WEEK)
                lic_exp = permit["license_expiry"]
                if lic_exp is not None and self.release_timestamp > lic_exp:
                    return LicenseStatus("renewal_required", False, expiry, lic_exp, expiry)
                return LicenseStatus(
                    "expired_grace" if now >= expiry
                    else "offline_grace" if record.get("offline")
                    else "update_entitlement_expired" if lic_exp is not None and now > lic_exp
                    else "valid",
                    now < expiry, expires_at=expiry, license_expires_at=lic_exp,
                    next_check_at=expiry, failure=record.get("failure") if record.get("offline") else None,
                )
            # No successful production validation: no offline access, including beta caches.
            return LicenseStatus(record.get("failure", "activation_required"), False)

    async def deactivate(self) -> LicenseStatus:
        if self._closed:
            raise LicenseError("The licensing client is closed")
        async with self._state() as state:
            license_id = state.get("active")
            if not license_id:
                return LicenseStatus("unlicensed", False)
            record = state["licenses"][license_id]
            self.verify_key(record["key"])
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
