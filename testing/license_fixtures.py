"""Synthetic Ed25519 fixtures; this file never contains production private keys."""
import base64
from datetime import datetime, timezone
import json

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


PRIVATE = Ed25519PrivateKey.from_private_bytes(bytes(range(32)))
PUBLIC = PRIVATE.public_key().public_bytes_raw().hex()
ACCOUNT = "11111111-1111-4111-8111-111111111111"
PRODUCT = "22222222-2222-4222-8222-222222222222"
POLICY = "33333333-3333-4333-8333-333333333333"
LICENSE = "44444444-4444-4444-8444-444444444444"
MACHINE = "55555555-5555-4555-8555-555555555555"
NOW = 1788696000.0


def iso(value: float) -> str:
    return datetime.fromtimestamp(value, timezone.utc).isoformat()


def signed_key(license_id: str = LICENSE) -> str:
    claims = {
        "account": {"id": ACCOUNT},
        "product": {"id": PRODUCT},
        "policy": {"id": POLICY, "duration": None},
        "user": None,
        "license": {"id": license_id, "created": iso(NOW), "expiry": None},
    }
    encoded = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode()
    message = "key/" + encoded
    return message + "." + base64.urlsafe_b64encode(PRIVATE.sign(message.encode())).decode()


def issuance(license_id: str) -> dict:
    return {
        "id": license_id,
        "attributes": {"key": signed_key(license_id), "scheme": "ED25519_SIGN"},
        "relationships": {"policy": {"data": {"id": POLICY}}},
    }


def permit(fingerprint: str, now: float = NOW, ttl: int = 604800, **changes) -> str:
    license_data = issuance(LICENSE)
    license_data.update(type="licenses")
    license_data["attributes"].update(suspended=False, expiry=None)
    data = {
        "meta": {"issued": iso(now), "expiry": iso(now + ttl), "ttl": ttl},
        "data": {
            "type": "machines",
            "id": MACHINE,
            "attributes": {"fingerprint": fingerprint},
            "relationships": {
                name: {"data": {"id": value}}
                for name, value in (
                    ("account", ACCOUNT),
                    ("product", PRODUCT),
                    ("license", LICENSE),
                )
            },
        },
        "included": [license_data],
    }
    data.update(changes)
    encoded = base64.b64encode(json.dumps(data).encode()).decode()
    document = {
        "enc": encoded,
        "sig": base64.b64encode(PRIVATE.sign(("machine/" + encoded).encode())).decode(),
        "alg": "base64+ed25519",
    }
    return (
        "-----BEGIN MACHINE FILE-----\n"
        + base64.b64encode(json.dumps(document).encode()).decode()
        + "\n-----END MACHINE FILE-----\n"
    )
