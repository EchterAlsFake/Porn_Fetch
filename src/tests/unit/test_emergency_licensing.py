"""Focused emergency protocol checks, with synthetic credentials and no live issuance."""
import importlib.util
import json
import secrets
import tempfile
import unittest
import uuid
from pathlib import Path

import jwt
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from src.licensing.client import WEEK, LicenseClient, LicenseError
from src.licensing.crypto import (
    EMERGENCY_KEY_ID,
    EMERGENCY_URL,
    emergency_claims,
    verify_emergency_permit,
)
from src.licensing.service import LicenseService
from src.shared.tor_runtime import TorUnavailable
from src.tests.license_fixtures import ACCOUNT, LICENSE, NOW, POLICY, PRODUCT, PUBLIC, signed_key
from src.tests.unit.test_license_client import FakeBaseCore, FakeResponse, resign

SIGNER = Ed25519PrivateKey.generate()


def sign(claims):
    return jwt.encode(claims, SIGNER, algorithm='EdDSA', headers={'kid': EMERGENCY_KEY_ID})


class EmergencyProtocolTests(unittest.TestCase):
    def test_signed_bindings_and_time(self):
        installation = str(uuid.uuid4())
        nonce = secrets.token_hex(32)
        claims = emergency_claims(signed_key(), LICENSE, installation, nonce, int(NOW))
        args = dict(key=signed_key(), license_id=LICENSE, installation_id=installation, now=NOW, nonce=nonce)
        self.assertEqual(verify_emergency_permit(sign(claims), SIGNER.public_key(), **args), claims)
        for field, value in {
            'sub': str(uuid.uuid4()), 'license_sha256': '0' * 64,
            'installation_id': str(uuid.uuid4()), 'nonce': secrets.token_hex(32),
            'iss': 'other', 'aud': 'other', 'version': 2,
            'iat': int(NOW + 600), 'exp': int(NOW + WEEK + 1),
        }.items():
            with self.subTest(field=field), self.assertRaises(LicenseError):
                verify_emergency_permit(sign({**claims, field: value}), SIGNER.public_key(), **args)
        token = sign(claims)
        pieces = token.split('.')
        pieces[1] = pieces[1][::-1]
        with self.assertRaises(LicenseError):
            verify_emergency_permit('.'.join(pieces), SIGNER.public_key(), **args)
        with self.assertRaises(LicenseError):
            verify_emergency_permit(token, Ed25519PrivateKey.generate().public_key(), **args)
        for algorithm in ('none', 'HS256'):
            bad = jwt.encode(claims, None if algorithm == 'none' else b'x' * 32,
                             algorithm=algorithm, headers={'kid': EMERGENCY_KEY_ID})
            with self.assertRaises(LicenseError):
                verify_emergency_permit(bad, SIGNER.public_key(), **args)


class EmergencyCore(FakeBaseCore):
    def __init__(self):
        super().__init__()
        self.online = False
        self.emergency_calls = 0
        self.emergency_enabled = True
        self.tor_enabled = False

    async def prepare(self):
        if isinstance(self.failure, TorUnavailable):
            raise self.failure

    async def request(self, url, **kwargs):
        if url != EMERGENCY_URL:
            return await super().request(url, **kwargs)
        self.emergency_calls += 1
        if self.tor_enabled:
            raise AssertionError('Fallback must never be requested with Tor enabled')
        if not self.emergency_enabled:
            return FakeResponse(503, {})
        data = kwargs['json_data']
        claims = emergency_claims(data['license_key'], LICENSE, data['installation_id'], data['nonce'], int(self.now))
        return FakeResponse(payload={'permit': sign(claims)})


class EmergencyClientTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.core = EmergencyCore()
        self.client = self.make_client()

    def make_client(self):
        return LicenseClient(
            self.directory.name, core=self.core, public_key=PUBLIC, account_id=ACCOUNT,
            product_id=PRODUCT, policy_id=POLICY,
            emergency_public_key=SIGNER.public_key().public_bytes_raw().hex(),
            clock=lambda: self.core.now, monotonic=lambda: self.core.now,
        )

    async def asyncTearDown(self):
        await self.client.close()
        self.directory.cleanup()

    async def test_new_installation_cache_expiry_and_primary_recovery(self):
        status = await self.client.import_license(signed_key())
        self.assertEqual(status.state, 'emergency_access')
        self.assertEqual(status.expires_at, NOW + WEEK)
        async with self.client._state() as state:
            self.assertFalse(state['licenses'][LICENSE]['activated'])
            self.assertNotIn('permit', state['licenses'][LICENSE])
        self.core.emergency_enabled = False
        await self.client.close()
        self.client = self.make_client()
        self.assertTrue((await self.client.check()).allowed)
        self.assertEqual(self.core.emergency_calls, 1)
        self.core.now += WEEK
        self.assertFalse((await self.client.check(force=True)).allowed)
        self.core.online = True
        self.assertEqual((await self.client.check(force=True)).state, 'valid')
        async with self.client._state() as state:
            self.assertNotIn('emergency_permit', state['licenses'][LICENSE])

    async def test_disabled_fallback_preserves_keygen_grace_and_server_errors_qualify(self):
        self.core.online = True
        self.assertEqual((await self.client.import_license(signed_key())).state, 'valid')
        self.core.online = False
        self.core.emergency_enabled = False
        self.assertEqual((await self.client.check(force=True)).state, 'offline_grace')
        self.core.now += WEEK
        self.assertFalse((await self.client.check(force=True)).allowed)
        self.core.online = True
        self.core.override = FakeResponse(503, {})
        self.core.emergency_enabled = True
        self.assertEqual((await self.client.check(force=True)).state, 'emergency_access')

    async def test_primary_rejection_wins_and_later_emergency_can_restore_access(self):
        await self.client.import_license(signed_key())
        self.core.online = True
        self.core.code = 'SUSPENDED'
        self.assertFalse((await self.client.check(force=True)).allowed)
        self.assertEqual(self.core.emergency_calls, 1)
        self.core.online = False
        self.assertEqual((await self.client.check(force=True)).state, 'emergency_access')
        self.assertEqual(self.core.emergency_calls, 2)

    async def test_tor_notice_without_fallback_request(self):
        self.core.tor_enabled = True
        self.core.online = True
        self.core.failure = TorUnavailable('Tor route unavailable')
        service = LicenseService(self.client, self.core)
        service.status = await self.client.import_license(signed_key())
        self.assertEqual(self.core.emergency_calls, 0)
        self.assertIn('only be reached without Tor', service.reason)
        self.assertIn('echteralsfake.me', service.reason)

    async def test_invalid_primary_response_and_tls_do_not_trigger_emergency(self):
        from curl_cffi.requests.exceptions import SSLError
        self.core.online = True
        self.core.override = FakeResponse(200, [])
        await self.client.import_license(signed_key())
        self.assertEqual(self.core.emergency_calls, 0)
        self.core.override = None
        self.core.failure = SSLError('bad certificate')
        self.assertFalse((await self.client.check(force=True)).allowed)
        self.assertEqual(self.core.emergency_calls, 0)


@unittest.skipUnless(importlib.util.find_spec('starlette'), 'Install the emergency-server extra')
class EmergencyServerTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        from deploy.emergency.server import create_app
        self.directory = tempfile.TemporaryDirectory()
        self.enabled = Path(self.directory.name) / 'enabled'
        self.app = create_app(dict(public_key=PUBLIC, account_id=ACCOUNT, product_id=PRODUCT,
                                   policy_id=POLICY), SIGNER, enabled_path=self.enabled, clock=lambda: NOW)
        self.data = dict(license_key=signed_key(), installation_id=str(uuid.uuid4()), nonce=secrets.token_hex(32))

    async def asyncTearDown(self):
        self.directory.cleanup()

    async def post(self, data):
        messages = []

        async def receive():
            return {'type': 'http.request', 'body': json.dumps(data).encode(), 'more_body': False}

        async def send(message):
            messages.append(message)

        await self.app(dict(type='http', asgi={'version': '3.0'}, http_version='1.1', method='POST',
                            scheme='http', path='/api/pornfetch-emergency/v1/permit', query_string=b'',
                            headers=[(b'content-type', b'application/json')], client=('127.0.0.1', 1),
                            server=('127.0.0.1', 8014)), receive, send)
        return messages[0]['status'], json.loads(messages[1]['body'])

    async def test_manual_switch_and_valid_issuance(self):
        self.assertEqual((await self.post(self.data))[0], 503)
        self.enabled.touch()
        status, body = await self.post(self.data)
        self.assertEqual(status, 200)
        verify_emergency_permit(body['permit'], SIGNER.public_key(), key=self.data['license_key'],
                                license_id=LICENSE, installation_id=self.data['installation_id'],
                                nonce=self.data['nonce'], now=NOW)
        self.enabled.unlink()
        self.assertEqual((await self.post(self.data))[0], 503)

    async def test_bad_license_product_beta_and_oversized_request(self):
        from src.licensing.crypto import BETA_ACCOUNT, BETA_POLICY
        self.enabled.touch()
        self.assertEqual((await self.post({**self.data, 'license_key': signed_key() + 'x'}))[0], 400)
        for section, field, value in [('product', 'id', str(uuid.uuid4())),
                                      ('account', 'id', BETA_ACCOUNT), ('policy', 'id', BETA_POLICY)]:
            claims = self.client_claims()
            claims[section][field] = value
            with self.subTest(section=section):
                self.assertEqual((await self.post({**self.data, 'license_key': resign(claims)}))[0], 400)
        self.assertEqual((await self.post({**self.data, 'license_key': 'x' * 21000}))[0], 413)

    def client_claims(self):
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

        from src.licensing.crypto import verify_license_key
        return verify_license_key(signed_key(), Ed25519PublicKey.from_public_bytes(bytes.fromhex(PUBLIC)),
                                  account_id=ACCOUNT, product_id=PRODUCT, policy_id=POLICY)
