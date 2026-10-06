"""Production lifecycle tests: synthetic keys, no live server or customer data."""
import base64
import json
import sqlite3
import tempfile
import unittest
import uuid
from contextlib import closing
from pathlib import Path
from urllib.parse import urlparse

from src.licensing import LicenseClient, LicenseError
from src.licensing.client import BETA_ACCOUNT, BETA_POLICY, DAY, WEEK, BetaLicenseError
from src.shared.version import RELEASE_TIMESTAMP
from src.tests.license_fixtures import (
    ACCOUNT,
    LICENSE,
    MACHINE,
    NOW,
    POLICY,
    PRIVATE,
    PRODUCT,
    PUBLIC,
    iso,
    permit,
    signed_key,
)


class FakeResponse:
    def __init__(self, status_code=200, payload=None):
        self.status_code, self.payload = status_code, payload

    def json(self):
        if self.payload is None:
            raise ValueError("bad JSON")
        return self.payload


class FakeBaseCore:
    def __init__(self):
        self.online = True
        self.now = NOW
        self.entitlement = NOW + 366 * DAY
        self.machines = {}
        self.requests = []
        self.code = None
        self.limit = 10
        self.failure = None
        self.post_create_failure = False
        self.lost_create = False
        self.override = None
        self.certificate_transform = lambda cert: cert

    async def request(self, url, **kwargs):
        self.requests.append({"url": url, **kwargs})
        if not self.online:
            raise ConnectionError("no network")
        if self.failure:
            raise self.failure
        if self.override:
            return self.override
        path = urlparse(url).path
        if not path.startswith(f"/v1/accounts/{ACCOUNT}/"):
            raise AssertionError("Unscoped API path")
        method = kwargs["method"]
        if path.endswith("validate-key"):
            self.fingerprint = kwargs["json_data"]["meta"]["scope"]["fingerprint"]
            code = self.code or ("VALID" if self.fingerprint in self.machines else "NO_MACHINES" if not self.machines else "FINGERPRINT_SCOPE_MISMATCH")
            if self.post_create_failure and self.machines:
                code = "SUSPENDED"
            return FakeResponse(payload={"meta": {"valid": code in ("VALID", "EXPIRED"), "code": code}, "data": {
                "type": "licenses", "id": LICENSE,
                "relationships": {k: {"data": {"id": v}} for k, v in (("account", ACCOUNT), ("product", PRODUCT), ("policy", POLICY))},
            }})
        if path.endswith("/machines") and method == "POST":
            if len(self.machines) >= self.limit:
                return FakeResponse(422, {"errors": [{"code": "MACHINE_LIMIT_EXCEEDED"}]})
            fingerprint = kwargs["json_data"]["data"]["attributes"]["fingerprint"]
            self.machines[fingerprint] = MACHINE
            if self.lost_create:
                raise TimeoutError
            return FakeResponse(201, {"data": {"id": MACHINE}})
        if path.endswith("check-out"):
            return FakeResponse(payload={"data": {"attributes": {"certificate": self.certificate_transform(permit(self.fingerprint, now=self.now, license_expiry=iso(self.entitlement)))}}})
        if method == "DELETE":
            self.machines.clear()
            return FakeResponse(204)
        fingerprint = path.rsplit("/", 1)[-1]
        if fingerprint not in self.machines:
            return FakeResponse(404, {"errors": []})
        return FakeResponse(payload={"data": {"id": self.machines[fingerprint]}})


def resign(claims):
    message = "key/" + base64.urlsafe_b64encode(json.dumps(claims, indent=3).encode()).decode()
    return message + "." + base64.urlsafe_b64encode(PRIVATE.sign(message.encode())).decode()


class LicenseClientTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.now = NOW
        self.core = FakeBaseCore()
        self.client = self.make_client()

    async def asyncTearDown(self):
        await self.client.close()
        self.directory.cleanup()

    def make_client(self, **overrides):
        args = dict(core=self.core, public_key=PUBLIC, account_id=ACCOUNT, product_id=PRODUCT,
                    policy_id=POLICY, clock=lambda: self.now, monotonic=lambda: self.now, release_timestamp=NOW)
        args.update(overrides)
        return LicenseClient(self.directory.name, **args)

    async def import_file(self):
        self.core.now = self.now
        return await self.client.import_license(json.dumps({"schema": 2, "license_key": signed_key()}))

    def mutate_state(self, change):
        with closing(sqlite3.connect(Path(self.directory.name) / "licensing.sqlite3")) as db:
            state = json.loads(db.execute("SELECT value FROM state WHERE id=1").fetchone()[0])
            change(state)
            db.execute("UPDATE state SET value=? WHERE id=1", (json.dumps(state),))
            db.commit()

    async def test_valid_signature_and_literal_noncanonical_json(self):
        claims = self.client.verify_key(signed_key())
        self.assertEqual(self.client.verify_key(resign(claims)), claims)

    async def test_modified_payload_and_signature_and_wrong_public_key(self):
        key = signed_key()
        message, sig = key.split(".")
        changed = self.client.verify_key(key)
        changed["license"]["expiry"] = iso(NOW + 99 * WEEK)
        modified = "key/" + base64.urlsafe_b64encode(json.dumps(changed).encode()).decode() + "." + sig
        for bad in (modified, message + "." + base64.urlsafe_b64encode(b"x" * 64).decode(), " " + key, key + "\n"):
            with self.subTest(kind=bad == modified), self.assertRaises(LicenseError):
                self.client.verify_key(bad)
        other = self.make_client(public_key="00" * 32)
        with self.assertRaises(LicenseError):
            other.verify_key(key)

    async def test_wrong_signed_account_product_policy(self):
        for field in ("account", "product", "policy"):
            claims = self.client.verify_key(signed_key())
            claims[field]["id"] = str(uuid.uuid4())
            with self.subTest(field=field), self.assertRaises(LicenseError):
                self.client.verify_key(resign(claims))
        self.assertFalse(self.core.requests)

    async def test_fresh_activation_revalidates_before_checkout(self):
        status = await self.import_file()
        self.assertTrue(status.allowed)
        self.assertEqual([r["url"].split("/")[-1] for r in self.core.requests],
                         ["validate-key", "machines", "validate-key", self.core.fingerprint, "check-out"])
        creation = self.core.requests[1]["json_data"]["data"]
        self.assertEqual(creation["attributes"], {"fingerprint": self.core.fingerprint})
        self.assertEqual(uuid.UUID(self.core.fingerprint).version, 4)
        self.assertNotIn("id", creation)  # Keygen owns resource IDs.

    async def test_post_create_validation_denial_never_unlocks(self):
        self.core.post_create_failure = True
        result = await self.import_file()
        self.assertFalse(result.allowed)
        self.assertEqual(result.state, "suspended")
        self.assertFalse(any(r["url"].endswith("check-out") for r in self.core.requests))

    async def test_same_install_restart_does_not_create_machine(self):
        await self.import_file()
        fingerprint = self.core.fingerprint
        await self.client.close()
        self.client = self.make_client()
        await self.client.check()
        self.assertEqual(self.core.fingerprint, fingerprint)
        self.assertEqual(sum(r["url"].endswith("/machines") for r in self.core.requests), 1)
        self.assertEqual(sum(r["url"].endswith("validate-key") for r in self.core.requests), 3)

    async def test_second_installation_uses_second_uuid(self):
        await self.import_file()
        with tempfile.TemporaryDirectory() as other:
            client = self.make_client()
            client.directory = Path(other)
            client.path = client.directory / "licensing.sqlite3"
            self.assertTrue((await client.import_license(signed_key())).allowed)
            await client.close()
        self.assertEqual(len(self.core.machines), 2)

    async def test_machine_limit(self):
        self.core.limit = 0
        status = await self.import_file()
        self.assertEqual(status.state, "installation_limit")
        self.assertFalse(status.allowed)

    async def test_arbitrary_failures_do_not_activate(self):
        for code in ("SUSPENDED", "EXPIRED_INVALID", "PRODUCT_SCOPE_MISMATCH", "POLICY_SCOPE_MISMATCH", "HEARTBEAT_DEAD", "MACHINE_SCOPE_REQUIRED"):
            self.core.code = code
            self.assertFalse((await self.import_file()).allowed)
        self.assertFalse(self.core.machines)

    async def test_suspension_sticky_during_outage(self):
        await self.import_file()
        self.core.code = "SUSPENDED"
        denied = await self.client.check(force=True)
        self.assertEqual(denied.state, "suspended")
        self.assertTrue(denied.server_rejected)
        self.core.online = False
        self.assertFalse((await self.client.check(force=True)).allowed)

    async def test_http_403_is_sticky_and_has_no_activation(self):
        self.core.override = FakeResponse(403, {"errors": [{"code": "LICENSE_SUSPENDED"}]})
        self.assertEqual((await self.import_file()).state, "suspended")
        self.core.override = None
        self.core.online = False
        self.assertFalse((await self.client.check(force=True)).allowed)

    async def test_first_activation_requires_network(self):
        self.core.online = False
        for _ in range(2):
            result = await self.import_file()
            self.assertFalse(result.allowed)
            self.assertEqual(result.state, "network_unavailable")

    async def test_offline_within_and_outside_exact_seven_days(self):
        await self.import_file()
        self.core.online = False
        self.now += WEEK - 1
        self.assertEqual((await self.client.check(force=True)).state, "offline_grace")
        self.now += 1
        result = await self.client.check(force=True)
        self.assertEqual(result.state, "expired_grace")
        self.assertFalse(result.allowed)

    async def test_active_entitlement_and_expired_old_build(self):
        self.core.entitlement = NOW + DAY
        self.assertTrue((await self.import_file()).allowed)
        self.now += 2 * DAY
        self.core.now = self.now
        self.core.code = "EXPIRED"
        status = await self.client.check(force=True)
        self.assertTrue(status.allowed)
        self.assertEqual(status.state, "update_entitlement_expired")
        self.core.online = False
        self.assertTrue((await self.client.check(force=True)).allowed)

    async def test_new_build_requires_renewal_same_key_no_new_machine(self):
        self.core.entitlement = NOW - 1
        status = await self.import_file()
        self.assertEqual(status.state, "renewal_required")
        self.assertFalse(status.allowed)
        fingerprint = self.core.fingerprint
        self.core.entitlement = NOW + 366 * DAY
        self.assertTrue((await self.client.check(force=True)).allowed)
        self.assertEqual(self.core.fingerprint, fingerprint)
        self.assertEqual(sum(r["url"].endswith("/machines") for r in self.core.requests), 1)
        self.assertEqual({r["headers"]["Authorization"] for r in self.core.requests}, {"License " + signed_key()})

    async def test_entitlement_equality_is_inclusive(self):
        self.core.entitlement = NOW
        self.assertTrue((await self.import_file()).allowed)

    async def test_cache_tampering_cannot_extend_signed_entitlement(self):
        self.core.entitlement = NOW - 1
        await self.import_file()
        self.mutate_state(lambda s: s["licenses"][s["active"]].update(license_expiry=NOW + WEEK))
        self.core.online = False
        self.assertEqual((await self.client.check()).state, "renewal_required")

    async def test_corrupt_installation_id_is_preserved_and_denied(self):
        await self.import_file()
        self.mutate_state(lambda s: s.update(installation_id="broken"))
        self.core.requests.clear()
        with self.assertRaises(LicenseError):
            await self.client.check()
        self.assertFalse(self.core.requests)

    async def test_corrupt_cache_timestamp_and_permit(self):
        for field, value in (("last_successful_validation", float("nan")), ("last_successful_validation", "bad")):
            with tempfile.TemporaryDirectory() as directory:
                client = self.make_client()
                client.directory = Path(directory)
                client.path = client.directory / "licensing.sqlite3"
                await client.import_license(signed_key())
                async with client._state() as state:
                    state["licenses"][LICENSE][field] = value
                with self.assertRaises(LicenseError):
                    await client.check()
        await self.import_file()
        self.mutate_state(lambda s: s["licenses"][s["active"]].update(permit="broken"))
        self.core.online = False
        self.assertFalse((await self.client.check()).allowed)

    async def test_5xx_timeout_malformed_json_are_temporary(self):
        for response, error, state in ((FakeResponse(503), None, "server_unavailable"), (None, TimeoutError(), "network_unavailable"), (FakeResponse(200), None, "malformed_response"), (FakeResponse(200, []), None, "malformed_response"), (FakeResponse(200, {"meta": []}), None, "malformed_response")):
            self.core.override, self.core.failure = response, error
            with self.subTest(state=state):
                result = await self.import_file()
                self.assertEqual(result.state, state)
                self.assertFalse(result.allowed)
        self.core.override = self.core.failure = None
        await self.import_file()
        self.core.override = FakeResponse(503)
        result = await self.client.check(force=True)
        self.assertTrue(result.allowed)
        self.assertEqual(result.failure, "server_unavailable")

    async def test_no_secret_in_error_or_log(self):
        self.core.failure = RuntimeError(signed_key())
        with self.assertNoLogs(level="DEBUG"):
            result = await self.import_file()
        self.assertNotIn(signed_key(), str(result))

    async def test_beta_migration_rejects_without_network(self):
        for field, value in (("account", BETA_ACCOUNT), ("policy", BETA_POLICY)):
            claims = self.client.verify_key(signed_key())
            claims[field]["id"] = value
            with self.assertRaises(BetaLicenseError):
                await self.client.import_license(resign(claims))
        with self.assertRaises(BetaLicenseError):
            await self.client.import_license('{"schema":1}')
        self.assertFalse(self.core.requests)

    async def test_beta_cache_never_sent_on_startup_or_deactivation(self):
        await self.import_file()
        claims = self.client.verify_key(signed_key())
        claims["policy"]["id"] = BETA_POLICY
        self.mutate_state(lambda s: s["licenses"][s["active"]].update(key=resign(claims)))
        self.core.requests.clear()
        self.assertEqual((await self.client.check(force=True)).state, "beta_license")
        with self.assertRaises(BetaLicenseError):
            await self.client.deactivate()
        self.assertFalse(self.core.requests)

    async def test_old_provisional_cache_cannot_grant_access(self):
        await self.import_file()
        self.mutate_state(lambda s: s["licenses"][s["active"]].pop("cache_version"))
        self.core.online = False
        self.assertFalse((await self.client.check()).allowed)

    async def test_clock_rollback_denies_grace(self):
        await self.import_file()
        self.now -= 600
        self.core.online = False
        self.assertEqual((await self.client.check()).state, "clock_invalid")

    async def test_permit_tampering_wrong_identity_excess_ttl(self):
        for cert in (permit("wrong"), permit("id", ttl=WEEK + 1), permit("id", ttl=0), permit("id")[:-12]):
            with self.assertRaises(LicenseError):
                self.client.verify_permit(cert, license_id=LICENSE, installation_id="id", now=NOW)

    async def test_timeouts_account_path_and_privacy(self):
        await self.import_file()
        for request in self.core.requests:
            self.assertFalse(request["allow_redirects"])
            self.assertEqual(request["timeout"], (5, 20))
            self.assertFalse(request["retry_non_idempotent"])
            self.assertTrue(request["url"].startswith(f"https://licenses.pornfetch.to/v1/accounts/{ACCOUNT}/"))
        self.assertEqual((Path(self.directory.name)/"licensing.sqlite3").stat().st_mode & 0o777, 0o600)

    async def test_deactivation_reuses_installation_identifier(self):
        await self.import_file()
        original = self.core.fingerprint
        self.assertEqual((await self.client.deactivate()).state, "deactivated")
        await self.import_file()
        self.assertEqual(self.core.fingerprint, original)

    async def test_lost_machine_create_response_is_reconciled(self):
        self.core.lost_create = True
        self.assertTrue((await self.import_file()).allowed)
        self.assertEqual(sum(r["url"].endswith("/machines") for r in self.core.requests), 1)

    def test_production_configuration_and_release_timestamp(self):
        config = json.loads(Path("src/licensing/production.json").read_text())
        self.assertEqual(config, {"base_url":"https://licenses.pornfetch.to", "account_id":"b0fab530-8614-45cb-8627-12ee594fb973", "product_id":"5d5e8829-838b-4dd4-8bfc-2491aa0f82d3", "policy_id":"7038281b-2429-4aa4-81db-4f04a87e7184", "public_key":"d24ec8bb5f78cc79f95751a3e1988107379a00cb89246b7f3318977dd2be9477"})
        self.assertEqual(iso(RELEASE_TIMESTAMP), "2026-10-06T00:00:00+00:00")

    async def test_denials_with_no_data_or_non_json_body_stay_denied(self):
        await self.import_file()
        self.core.override = FakeResponse(200, {"meta": {"valid": False, "code": "NOT_FOUND"}, "data": None})
        self.assertEqual((await self.client.check(force=True)).state, "not_found")
        self.core.override = FakeResponse(403)
        self.assertEqual((await self.client.check(force=True)).state, "suspended_or_denied")
        self.core.override = None
        self.core.online = False
        self.assertFalse((await self.client.check(force=True)).allowed)

    async def test_expired_false_is_not_overridden_as_perpetual_success(self):
        self.core.override = FakeResponse(200, {"meta": {"valid": False, "code": "EXPIRED"}, "data": None})
        status = await self.import_file()
        self.assertFalse(status.allowed)
        self.assertEqual(status.state, "entitlement_server_denied")
        self.assertFalse(self.core.machines)

    async def test_signed_commercial_null_entitlement_does_not_mean_unlimited_updates(self):
        self.core.certificate_transform = lambda _: permit(self.core.fingerprint, now=self.now)
        self.assertFalse((await self.import_file()).allowed)

    async def test_service_state_error_clears_previous_premium_status(self):
        from src.licensing.service import LicenseService
        service = LicenseService(self.client)
        service.status = await self.import_file()
        self.mutate_state(lambda s: s.update(installation_id="corrupt"))
        with self.assertRaises(LicenseError):
            await service.check()
        self.assertFalse(service.status.allowed)

    async def test_transport_does_not_inherit_insecure_scraper_configuration(self):
        from base_api.modules.config import RuntimeConfig

        from src.licensing.service import create_license_service
        config = RuntimeConfig()
        config.verify_ssl = False
        config.proxy = "http://example.invalid"
        service = create_license_service(config, self.directory.name, production_config={
            "public_key": PUBLIC, "account_id": ACCOUNT, "product_id": PRODUCT,
            "policy_id": POLICY, "base_url": "https://licenses.pornfetch.to",
        })
        try:
            self.assertTrue(service.core.configuration.verify_ssl)
            self.assertFalse(service.core.configuration.trust_env)
            self.assertIsNone(service.core.configuration.proxy)
        finally:
            await service.close()

    async def test_feature_gate_expires_between_async_refreshes(self):
        from src.licensing.service import LicenseService
        service = LicenseService(self.client)
        service.status = await self.import_file()
        self.now += WEEK
        self.assertFalse(service.status.allowed)
        self.assertEqual(service.status.state, "expired_grace")

    def test_fixed_keygen_format_vector(self):
        fixture = json.loads(Path("src/tests/fixtures/keygen_ed25519_vector.json").read_text())
        self.assertEqual(self.client.verify_key(fixture["license_key"])["license"]["id"], LICENSE)


if __name__ == "__main__":
    unittest.main()
