"""Direct-only emergency issuance. No customer database or primary-server dependency."""
from __future__ import annotations

import asyncio
import json
import os
import time
from pathlib import Path

import jwt
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from starlette.applications import Starlette
from starlette.requests import ClientDisconnect, Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from src.licensing.crypto import (
    EMERGENCY_KEY_ID,
    LicenseError,
    emergency_claims,
    timestamp,
    verify_license_key,
)

CONTROL = Path('/run/pornfetch-emergency-control/enabled')
MAX_BODY = 20 * 1024


def create_app(config: dict, signing_key, *, enabled_path: Path = CONTROL, clock=time.time):
    public_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(config['public_key']))
    tokens, last = 120.0, time.monotonic()

    def response(body, status):
        return JSONResponse(body, status_code=status, headers={'Cache-Control': 'no-store'})

    async def issue(request: Request):
        nonlocal tokens, last
        if not enabled_path.is_file():
            return response({'error': 'emergency_disabled'}, 503)
        current = time.monotonic()
        tokens = min(120.0, tokens + (current - last) * 10)
        last = current
        if tokens < 1:
            return response({'error': 'rate_limited'}, 429)
        tokens -= 1
        if request.headers.get('content-type', '').split(';')[0].strip().lower() != 'application/json':
            return response({'error': 'json_required'}, 415)
        try:
            raw = bytearray()
            async with asyncio.timeout(10):
                async for chunk in request.stream():
                    raw.extend(chunk)
                    if len(raw) > MAX_BODY:
                        return response({'error': 'request_too_large'}, 413)
            data = json.loads(raw)
            if not isinstance(data, dict) or set(data) != {'license_key', 'installation_id', 'nonce'}:
                raise LicenseError('Invalid request')
            claims = verify_license_key(data['license_key'], public_key,
                                        account_id=config['account_id'], product_id=config['product_id'],
                                        policy_id=config['policy_id'])
            now = int(clock())
            if timestamp(claims['license']['created']) > now + 300:
                raise LicenseError('Invalid license date')
            payload = emergency_claims(data['license_key'], claims['license']['id'],
                                       data['installation_id'], data['nonce'], now)
        except (ValueError, TypeError, KeyError, AttributeError, TimeoutError, ClientDisconnect):
            return response({'error': 'invalid_request_or_license'}, 400)
        # Recheck after reading: disabling must also stop requests awaiting a body.
        if not enabled_path.is_file():
            return response({'error': 'emergency_disabled'}, 503)
        token = jwt.encode(payload, signing_key, algorithm='EdDSA', headers={'kid': EMERGENCY_KEY_ID})
        return response({'permit': token}, 200)

    return Starlette(routes=[Route('/api/pornfetch-emergency/v1/permit', issue, methods=['POST'])])


def production_app():
    config = json.loads(Path('/etc/pornfetch-emergency/production.json').read_text())
    private_key = load_pem_private_key((Path(os.environ['CREDENTIALS_DIRECTORY']) / 'signing.pem').read_bytes(), password=None)
    return create_app(config, private_key)
