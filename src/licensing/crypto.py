"""Shared offline license and emergency JWS verification. No networking or Qt."""
from __future__ import annotations

import base64
import hashlib
import json
import uuid
from datetime import datetime
from typing import Any

import jwt
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

WEEK = 604800
EMERGENCY_URL = "https://echteralsfake.me/api/pornfetch-emergency/v1/permit"
EMERGENCY_ISSUER = "https://echteralsfake.me/pornfetch-emergency"
EMERGENCY_AUDIENCE = "pornfetch-premium-emergency"
EMERGENCY_KEY_ID = "emergency-2026-01"
BETA_MESSAGE = "This beta license belongs to an older licensing system and is no longer valid for the production release."
BETA_POLICY = "564897fa-b8d9-4871-82a4-0b49fd50bc1e"
BETA_ACCOUNT = "2779db33-8e9b-4c5f-b1b5-ee5957939c20"


class LicenseError(ValueError):
    """Invalid licensing data; messages contain no credentials."""


class BetaLicenseError(LicenseError):
    """A credential from the retired licensing system."""


def decode(value: str, *, url: bool = False) -> bytes:
    return base64.b64decode(value, altchars=b"-_" if url else None, validate=True)


def timestamp(value: str) -> float:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Naive timestamp")
    return parsed.timestamp()


def verify_license_key(key: str, public_key: Ed25519PublicKey, *, account_id: str,
                       product_id: str, policy_id: str) -> dict[str, Any]:
    try:
        if not isinstance(key, str) or len(key) > 16384 or not key.startswith("key/"):
            raise ValueError
        message, signature = key.rsplit(".", 1)
        # Untrusted inspection is used ONLY to reject known beta material, never to grant access.
        candidate = json.loads(decode(message[4:], url=True))
        if isinstance(candidate, dict) and (candidate.get("account", {}).get("id") == BETA_ACCOUNT or candidate.get("policy", {}).get("id") == BETA_POLICY):
            raise BetaLicenseError(BETA_MESSAGE)
        public_key.verify(decode(signature, url=True), message.encode("ascii"))
        payload = json.loads(decode(message[4:], url=True))
        if (
            payload["account"]["id"] != account_id
            or payload["product"]["id"] != product_id
            or payload["policy"]["id"] != policy_id
            or payload["policy"]["duration"] is not None
        ):
            raise ValueError
        uuid.UUID(payload["license"]["id"])
        timestamp(payload["license"]["created"])
        # Only an explicit signed null means permanent; missing claims fail.
        if payload["license"]["expiry"] is not None:
            raise ValueError
        return payload
    except BetaLicenseError:
        raise
    except (ValueError, KeyError, TypeError, AttributeError, UnicodeError, InvalidSignature):
        raise LicenseError("License signature or signed claims are invalid") from None


def validate_challenge(nonce: str, installation_id: str) -> None:
    if not isinstance(nonce, str) or len(nonce) != 64:
        raise LicenseError("Invalid emergency challenge")
    try:
        if bytes.fromhex(nonce).hex() != nonce:
            raise ValueError
        installation = uuid.UUID(installation_id)
        if installation.version != 4 or str(installation) != installation_id:
            raise ValueError
    except (ValueError, TypeError, AttributeError):
        raise LicenseError("Invalid emergency challenge") from None


def emergency_claims(key: str, license_id: str, installation_id: str, nonce: str, now: int) -> dict:
    validate_challenge(nonce, installation_id)
    return {
        "version": 1, "iss": EMERGENCY_ISSUER, "aud": EMERGENCY_AUDIENCE,
        "sub": license_id, "license_sha256": hashlib.sha256(key.encode("ascii")).hexdigest(),
        "installation_id": installation_id, "nonce": nonce, "iat": now, "exp": now + WEEK,
    }


def verify_emergency_permit(token: str, public_key: Ed25519PublicKey, *, key: str,
                            license_id: str, installation_id: str, now: float,
                            nonce: str | None = None) -> dict:
    try:
        if not isinstance(token, str) or len(token) > 8192:
            raise ValueError
        header = jwt.get_unverified_header(token)
        if header != {"alg": "EdDSA", "kid": EMERGENCY_KEY_ID, "typ": "JWT"}:
            raise ValueError
        claims = jwt.decode(
            token, public_key, algorithms=["EdDSA"],
            issuer=EMERGENCY_ISSUER, audience=EMERGENCY_AUDIENCE,
            options={"verify_exp": False, "verify_iat": False, "verify_nbf": False,
                     "strict_aud": True, "require": ["iat", "exp", "sub", "iss", "aud"]},
        )
        validate_challenge(claims["nonce"], claims["installation_id"])
        if (type(claims["version"]) is not int or claims["version"] != 1
                or claims["sub"] != license_id or claims["installation_id"] != installation_id
                or claims["license_sha256"] != hashlib.sha256(key.encode("ascii")).hexdigest()
                or (nonce is not None and claims["nonce"] != nonce)
                or type(claims["iat"]) is not int or type(claims["exp"]) is not int
                or not 0 < claims["exp"] - claims["iat"] <= WEEK
                or claims["iat"] > now + 300):
            raise ValueError
        return claims  # Expiry is checked by callers so expired caches remain readable.
    except (jwt.InvalidTokenError, ValueError, TypeError, KeyError, AttributeError, UnicodeError):
        raise LicenseError("Emergency permit could not be verified") from None
