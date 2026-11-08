"""Production lifecycle tests: synthetic keys, no live server or customer data."""
import base64
import json
import logging
import os
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
    issuance,
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
        self.entitlement = None
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
            return FakeResponse(payload={"data": {"attributes": {"certificate": self.certificate_transform(permit(self.fingerprint, now=self.now, license_expiry=iso(self.entitlement) if self.entitlement is not None else None))}}})
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
        for section, field in (("license", "expiry"), ("policy", "duration")):
            del claims[section][field]
            with self.subTest(section=section, claim="missing"), self.assertRaises(LicenseError):
                self.client.verify_key(resign(claims))
            claims[section][field] = "never"
            with self.subTest(section=section, claim="malformed"), self.assertRaises(LicenseError):
                self.client.verify_key(resign(claims))
            claims[section][field] = None

    async def test_signed_permit_from_future_reports_clock_mismatch(self):
        self.core.certificate_transform = lambda certificate: permit(
            self.core.fingerprint, now=self.now + 7200,
            license_expiry=None,
        )
        status = await self.import_file()
        self.assertEqual(status.state, "clock_mismatch")
        self.assertFalse(status.allowed)
        self.core.certificate_transform = lambda certificate: certificate
        self.assertTrue((await self.client.check(force=True)).allowed)

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

    async def test_initial_grace_has_fixed_three_day_deadline(self):
        self.core.online = False
        first = await self.import_file()
        self.assertTrue(first.allowed)
        self.assertEqual(first.state, "initial_offline_grace")
        self.assertEqual(first.expires_at, NOW + 3 * DAY)
        self.now += 3 * DAY - 1
        self.client = self.make_client()
        self.assertEqual((await self.import_file()).expires_at, first.expires_at)
        self.assertTrue((await self.client.check()).allowed)
        self.now += 1
        expired = await self.import_file()
        self.assertFalse(expired.allowed)
        self.assertEqual(expired.state, "initial_grace_expired")
        self.core.online = True
        self.core.now = self.now
        self.assertEqual((await self.client.check(force=True)).state, "valid")

    async def test_initial_rejection_survives_restart_reimport_and_outage(self):
        self.core.code = "SUSPENDED"
        self.assertFalse((await self.import_file()).allowed)
        self.core.online = False
        self.client = self.make_client()
        self.assertEqual((await self.import_file()).state, "suspended")
        self.assertFalse((await self.client.check(force=True)).allowed)

    async def test_initial_grace_stops_on_explicit_denial(self):
        self.core.online = False
        self.assertTrue((await self.import_file()).allowed)
        self.core.online = True
        self.core.override = FakeResponse(200, {"meta": {"valid": False}})
        self.assertFalse((await self.client.check(force=True)).allowed)
        self.core.online = False
        self.assertFalse((await self.client.check(force=True)).allowed)

    async def test_non_json_denial_and_malformed_explicit_denial_remain_blocked(self):
        for response in (FakeResponse(422), FakeResponse(200, {"meta": {"valid": False, "code": []}})):
            self.core.online = True
            self.core.override = response
            self.assertFalse((await self.import_file()).allowed)
            self.core.online = False
            self.assertFalse((await self.client.check(force=True)).allowed)

    async def test_initial_grace_rejects_a_signed_license_with_a_cutoff(self):
        self.core.online = False
        with self.assertRaises(LicenseError):
            await self.client.import_license(signed_key(expiry=iso(NOW - DAY)))
        self.assertFalse(self.core.requests)

    async def test_tls_and_programming_errors_do_not_start_grace(self):
        from curl_cffi.requests.exceptions import SSLError
        for error in (SSLError("trust failed"), RuntimeError("unexpected")):
            self.core.failure = error
            self.assertFalse((await self.import_file()).allowed)

    async def test_initial_service_gate_expires_without_refresh(self):
        from src.licensing.service import LicenseService
        self.core.online = False
        service = LicenseService(self.client)
        service.status = await self.import_file()
        self.now += 3 * DAY
        self.assertFalse(service.status.allowed)
        self.assertEqual(service.status.state, "initial_grace_expired")

    async def test_offline_within_and_outside_exact_seven_days(self):
        active = await self.import_file()
        self.assertIsNone(active.license_expires_at)
        self.assertEqual(active.expires_at, NOW + WEEK)
        self.core.online = False
        self.now += WEEK - 1
        cached = await self.client.check(force=True)
        self.assertEqual(cached.state, "offline_grace")
        self.assertTrue(cached.allowed)
        self.assertIsNone(cached.license_expires_at)
        self.assertEqual(cached.expires_at, active.expires_at)
        self.now += 1
        result = await self.client.check(force=True)
        self.assertEqual(result.state, "expired_grace")
        self.assertFalse(result.allowed)
        self.assertFalse(result.entitled_to(NOW + 25 * 365 * DAY))

    async def test_lifetime_stays_valid_in_later_years(self):
        self.assertTrue((await self.import_file()).allowed)
        self.now += 25 * 365 * DAY
        self.core.now = self.now
        status = await self.client.check(force=True)
        self.assertTrue(status.allowed)
        self.assertEqual(status.state, "valid")
        self.assertIsNone(status.license_expires_at)
        self.core.online = False
        self.assertTrue((await self.client.check(force=True)).allowed)

    async def test_future_build_uses_same_lifetime_key_and_machine(self):
        self.assertTrue((await self.import_file()).allowed)
        fingerprint = self.core.fingerprint
        await self.client.close()
        self.client = self.make_client(release_timestamp=NOW + 25 * 365 * DAY)
        status = await self.client.check()
        self.assertTrue(status.allowed)
        self.assertIsNone(status.license_expires_at)
        self.assertEqual(self.core.fingerprint, fingerprint)
        self.assertEqual(sum(r["url"].endswith("/machines") for r in self.core.requests), 1)
        self.assertEqual({r["headers"]["Authorization"] for r in self.core.requests}, {"License " + signed_key()})

    async def test_lifetime_status_covers_future_releases(self):
        status = await self.import_file()
        self.assertTrue(status.entitled_to(NOW + 25 * 365 * DAY))

    async def test_missing_or_non_null_signed_expiry_is_denied_online_and_cached(self):
        self.assertTrue((await self.import_file()).allowed)
        for attributes in (
            {"suspended": False},
            {"suspended": False, "expiry": "never"},
            {"suspended": False, "expiry": iso(NOW + WEEK)},
        ):
            included = issuance(LICENSE)
            included.update(type="licenses", attributes=attributes)
            certificate = permit(self.core.fingerprint, included=[included])
            for source in ("refresh", "cache"):
                with self.subTest(attributes=attributes, source=source):
                    self.core.online = True
                    self.core.certificate_transform = lambda cert: cert
                    self.assertTrue((await self.client.check(force=True)).allowed)
                    if source == "refresh":
                        self.core.certificate_transform = lambda cert: certificate
                        status = await self.client.check(force=True)
                    else:
                        # An unsigned null in local storage cannot repair signed claims.
                        self.mutate_state(lambda s: s["licenses"][s["active"]].update(
                            permit=certificate, license_expiry=None,
                        ))
                        self.core.online = False
                        status = await self.client.check()
                    self.assertFalse(status.allowed)
                    self.assertEqual(status.state, "invalid_signature")

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
                self.assertEqual(result.state, "initial_offline_grace" if state == "network_unavailable" else state)
                self.assertEqual(result.allowed, state == "network_unavailable")
        self.core.override = self.core.failure = None
        await self.import_file()
        self.core.override = FakeResponse(503)
        result = await self.client.check(force=True)
        self.assertTrue(result.allowed)
        self.assertEqual(result.failure, "server_unavailable")

    async def test_no_secret_in_error_or_log(self):
        key = signed_key()
        self.core.failure = RuntimeError(key)
        with self.assertLogs(level="DEBUG") as logs:
            # Capture even when the client emits nothing; asyncio may emit
            # harmless slow-task warnings on a busy runner.
            logging.getLogger(__name__).debug("Checking license failure log redaction")
            result = await self.import_file()
        self.assertNotIn(key, "\n".join(logs.output))
        self.assertNotIn(key, str(result))

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
        if os.name != "nt":
            # Windows reports DOS read/write flags, not POSIX permission bits.
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
        self.assertEqual(config, {"base_url":"https://licenses.pornfetch.to", "account_id":"b0fab530-8614-45cb-8627-12ee594fb973", "product_id":"5d5e8829-838b-4dd4-8bfc-2491aa0f82d3", "policy_id":"7038281b-2429-4aa4-81db-4f04a87e7184", "public_key":"d24ec8bb5f78cc79f95751a3e1988107379a00cb89246b7f3318977dd2be9477", "emergency_public_key":"e7e3950f0bf9cda2974372fe68f6c068b138ce205f3915c9fd1c85c8ce8b0569"})
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
        self.assertEqual(status.state, "rejected")
        self.assertFalse(self.core.machines)

    async def test_signed_lifetime_null_expiry_allows_premium(self):
        self.core.certificate_transform = lambda _: permit(self.core.fingerprint, now=self.now)
        active = await self.import_file()
        self.assertTrue(active.allowed)
        self.assertIsNone(active.license_expires_at)
        self.assertEqual(active.expires_at, NOW + WEEK)
        await self.client.close()
        self.core.online = False
        self.client = self.make_client(release_timestamp=NOW + 25 * 365 * DAY)
        cached = await self.client.check()
        self.assertTrue(cached.allowed)
        self.assertEqual(cached.state, "offline_grace")
        self.assertIsNone(cached.license_expires_at)
        self.assertTrue(cached.entitled_to(self.client.release_timestamp))
        self.assertEqual(cached.expires_at, active.expires_at)

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
