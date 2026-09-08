import json
from contextlib import closing
from pathlib import Path
import sqlite3
import tempfile
import unittest
from urllib.parse import urlparse

from base_api.modules.errors import HTTPStatusError, NetworkRequestError

from license_client import LicenseClient, LicenseError
from testing.license_fixtures import (
    ACCOUNT,
    LICENSE,
    NOW,
    POLICY,
    PRODUCT,
    PUBLIC,
    permit,
    signed_key,
)


class FakeResponse:
    def __init__(self, status_code: int, payload: dict | None = None) -> None:
        self.status_code = status_code
        self.payload = payload

    def json(self) -> dict:
        if self.payload is None:
            raise ValueError
        return self.payload


class FakeBaseCore:
    def __init__(self) -> None:
        self.online = False
        self.revoked = False
        self.limit = False
        self.fingerprint: str | None = None
        self.requests: list[dict] = []

    async def request(self, url: str, **kwargs) -> FakeResponse:
        self.requests.append({"url": url, **kwargs})
        if not self.online:
            raise NetworkRequestError("offline")
        path = urlparse(url).path
        method = kwargs.get("method", "GET")
        if path.endswith("validate-key"):
            return FakeResponse(200, {"meta": {
                "valid": bool(self.fingerprint) and not self.revoked,
                "code": "SUSPENDED" if self.revoked else "NO_MACHINES",
            }})
        if path.endswith("/machines") and method == "POST":
            if self.limit:
                raise HTTPStatusError("limit", 422, url)
            self.fingerprint = kwargs["json_data"]["data"]["attributes"]["fingerprint"]
            return FakeResponse(201, {"data": {"id": "machine"}})
        if path.endswith("check-out"):
            return FakeResponse(200, {"data": {"attributes": {
                "certificate": permit(self.fingerprint, now=self.now),
            }}})
        if method == "DELETE":
            self.fingerprint = None
            return FakeResponse(204)
        if self.fingerprint is None:
            raise HTTPStatusError("not found", 404, url)
        return FakeResponse(200, {"data": {"id": "machine"}})


class LicenseClientTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.now = NOW
        self.core = FakeBaseCore()
        self.core.now = self.now
        self.client = self.make_client()

    async def asyncTearDown(self) -> None:
        await self.client.close()
        self.directory.cleanup()

    def make_client(self) -> LicenseClient:
        return LicenseClient(
            self.directory.name,
            core=self.core,
            public_key=PUBLIC,
            account_id=ACCOUNT,
            product_id=PRODUCT,
            policy_id=POLICY,
            clock=lambda: self.now,
            monotonic=lambda: self.now,
        )

    async def import_file(self):
        self.core.now = self.now
        return await self.client.import_license(
            json.dumps({"schema": 2, "license_key": signed_key()})
        )

    async def test_provisional_deadline_survives_restart_and_reimport(self) -> None:
        self.assertEqual((await self.import_file()).state, "provisional")
        self.now += 604799
        await self.client.close()
        self.client = self.make_client()
        self.assertTrue((await self.import_file()).allowed)
        self.now += 1
        self.assertFalse((await self.import_file()).allowed)
        self.assertEqual((await self.client.check()).state, "expired_grace")

    async def test_activation_offline_expiry_and_recovery(self) -> None:
        self.core.online = True
        self.assertEqual((await self.import_file()).state, "valid")
        self.core.online = False
        self.now += 86400
        self.assertEqual((await self.client.check()).state, "offline_grace")
        self.now += 604800 - 86400
        self.assertFalse((await self.client.check()).allowed)
        self.core.online = True
        self.core.now = self.now
        self.assertTrue((await self.client.check(force=True)).allowed)

    async def test_denial_never_becomes_provisional(self) -> None:
        self.core.online = True
        self.core.limit = True
        self.assertEqual((await self.import_file()).state, "installation_limit")
        self.core.online = False
        self.assertFalse((await self.client.check(force=True)).allowed)
        self.assertFalse((await self.import_file()).allowed)

    async def test_revocation_stays_denied_during_outage(self) -> None:
        self.core.online = True
        await self.import_file()
        self.core.revoked = True
        self.assertEqual((await self.client.check(force=True)).state, "revoked")
        self.core.online = False
        self.assertFalse((await self.client.check(force=True)).allowed)

    async def test_tampering_wrong_product_and_excess_ttl(self) -> None:
        key = signed_key()
        with self.assertRaises(LicenseError):
            self.client.verify_key(key[:-5] + "AAAAA")
        self.client.product_id = ACCOUNT
        with self.assertRaises(LicenseError):
            self.client.verify_key(key)
        self.client.product_id = PRODUCT
        for ttl in (604801, 0):
            with self.assertRaises(LicenseError):
                self.client.verify_permit(
                    permit("fingerprint", ttl=ttl),
                    license_id=LICENSE,
                    installation_id="fingerprint",
                    now=NOW,
                )

    async def test_clock_rollback_requires_recovery(self) -> None:
        await self.import_file()
        self.now -= 600
        self.assertEqual((await self.client.check()).state, "clock_invalid")

    async def test_deactivation_needs_server_and_clears_access(self) -> None:
        self.core.online = True
        await self.import_file()
        self.core.online = False
        self.assertEqual((await self.client.deactivate()).state, "deactivation_pending")
        self.core.online = True
        self.assertEqual((await self.client.deactivate()).state, "deactivated")
        self.assertFalse((await self.client.check()).allowed)

    async def test_persistent_uuid_and_request_privacy(self) -> None:
        await self.client.check()
        async with self.client._state() as state:
            fingerprint = state["installation_id"]
        self.assertEqual(len(fingerprint), 36)
        other = self.make_client()
        async with other._state() as state:
            self.assertEqual(state["installation_id"], fingerprint)
        await other.close()
        self.assertEqual(
            (Path(self.directory.name) / "licensing.sqlite3").stat().st_mode & 0o777,
            0o600,
        )

    async def test_unreadable_existing_state_is_not_silently_recreated(self) -> None:
        await self.client.check()
        database_path = Path(self.directory.name) / "licensing.sqlite3"
        with closing(sqlite3.connect(database_path)) as connection:
            connection.execute("UPDATE state SET value='{}' WHERE id=1")
            connection.commit()

        broken_client = self.make_client()
        with self.assertRaises(LicenseError):
            await broken_client.check()
        with closing(sqlite3.connect(database_path)) as connection:
            self.assertEqual(connection.execute("SELECT value FROM state WHERE id=1").fetchone()[0], "{}")
        await broken_client.close()

    async def test_malformed_active_record_is_reported_as_local_state_error(self) -> None:
        await self.import_file()
        database_path = Path(self.directory.name) / "licensing.sqlite3"
        with closing(sqlite3.connect(database_path)) as connection:
            state = json.loads(
                connection.execute("SELECT value FROM state WHERE id=1").fetchone()[0]
            )
            state["licenses"][state["active"]]["first_import"] = "not-a-time"
            connection.execute(
                "UPDATE state SET value=? WHERE id=1", (json.dumps(state),)
            )
            connection.commit()

        with self.assertRaisesRegex(LicenseError, "Local license state is unreadable"):
            await self.client.check()

    def test_invalid_bundled_public_key_is_a_license_error(self) -> None:
        with self.assertRaisesRegex(LicenseError, "public key is invalid"):
            LicenseClient(
                self.directory.name,
                core=self.core,
                public_key="not-hex",
                account_id=ACCOUNT,
                product_id=PRODUCT,
                policy_id=POLICY,
            )

    async def test_requests_use_base_core_without_redirects(self) -> None:
        self.core.online = True
        await self.import_file()
        self.assertTrue(self.core.requests)
        for request in self.core.requests:
            self.assertTrue(request["url"].startswith("https://licenses.echteralsfake.me/v1/"))
            self.assertFalse(request["allow_redirects"])
            self.assertTrue(request["headers"]["Authorization"].startswith("License key/"))


if __name__ == "__main__":
    unittest.main()
