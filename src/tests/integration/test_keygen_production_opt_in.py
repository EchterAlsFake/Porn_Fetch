"""Explicit, non-destructive public validation of an EXISTING activated TEST install.

PF_KEYGEN_INTEGRATION=1 PF_KEYGEN_TEST_LICENSE_FILE=/private/test.license
PF_KEYGEN_TEST_INSTALLATION_ID=<existing UUID> uv run python -m unittest ...
Never creates/deletes machines, renews, suspends, purchases, or prints credentials.
Validation may update Keygen's last-validated timestamp.
"""
import json
import os
import tempfile
import unittest
import uuid
from pathlib import Path

from src.licensing.client import LicenseClient
from src.licensing.transport import LicensingCore


@unittest.skipUnless(os.environ.get("PF_KEYGEN_INTEGRATION") == "1", "Explicit production TEST-license opt-in required")
class PublicKeygenIntegration(unittest.IsolatedAsyncioTestCase):
    async def test_existing_activation_and_signed_checkout(self):
        configuration = json.loads(Path("src/licensing/production.json").read_text())
        key = json.loads(Path(os.environ["PF_KEYGEN_TEST_LICENSE_FILE"]).read_bytes())["license_key"]
        installation = os.environ["PF_KEYGEN_TEST_INSTALLATION_ID"]
        self.assertEqual(uuid.UUID(installation).version, 4)
        self.assertEqual(str(uuid.UUID(installation)), installation)
        with tempfile.TemporaryDirectory() as directory:
            async with LicensingCore() as core:
                client = LicenseClient(directory, core=core, **configuration)
                claims = client.verify_key(key)
                response = await client._request("POST", "licenses/actions/validate-key", key, json_data={"meta":{"key":key,"scope":{"fingerprint":installation,"product":configuration["product_id"],"policy":configuration["policy_id"]}}})
                self.assertIs(response["meta"]["valid"], True, "Existing TEST installation did not validate")
                certificate = (await client._request("POST", f"machines/{installation}/actions/check-out", key, json_data={"meta":{"ttl":604800,"algorithm":"base64+ed25519","include":["license"]}}))["data"]["attributes"]["certificate"]
                permit = client.verify_permit(certificate, license_id=claims["license"]["id"], installation_id=installation, now=client.clock())
                self.assertIsNotNone(permit["license_expiry"])
                await client.close()
