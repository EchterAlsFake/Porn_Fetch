"""
This file handles the license checks. It uses a public and private key to verify if a given license
was created by my server and is valid.

If it is, it will be returned to the GUI with the enabled features.

Format is like this:

{
  "schema": 1,
  "product": "porn-fetch",
  "kid": "v1",
  "alg": "ed25519",
  "license_key": "PF-3G8K9-7D2QH-...",
  "stripe_session_id": "cs_test_...",
  "created_at": "2025-12-15T12:34:56Z",
  "features": ["full_unlock"],
  "sig": "BASE64_SIGNATURE"
}
"""
import base64
import json

from pathlib import Path
from dataclasses import dataclass
from typing import Any, Dict, Optional
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


public_key = None


def _canonical_json_bytes(obj: Dict[str, Any]) -> bytes:
    # Deterministic JSON encoding for signing/verifying
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


@dataclass(frozen=True)
class LicenseCheckResult:
    valid: bool
    reason: str
    data: Optional[Dict[str, Any]] = None


class LicenseManager:
    """
    - App embeds PUBLIC_KEY_B64 only
    - User imports a .license file
    - verifies signature offline and cache it locally
    """
    def __init__(self, public_key_b64: str, storage_path: Path, expected_product: str = "porn-fetch"):
        self._pub = Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key_b64))
        self._storage_path = storage_path
        self._expected_product = expected_product

    @property
    def storage_path(self) -> Path:
        return self._storage_path

    def load_installed(self) -> LicenseCheckResult:
        if not self._storage_path.exists():
            return LicenseCheckResult(False, "No license installed.")
        try:
            raw = self._storage_path.read_text(encoding="utf-8")
            data = json.loads(raw)
        except Exception:
            return LicenseCheckResult(False, "Installed license file is unreadable/corrupted.")
        return self.validate(data)

    def install_from_file(self, src_path: Path) -> LicenseCheckResult:
        try:
            data = json.loads(src_path.read_text(encoding="utf-8"))
        except Exception:
            return LicenseCheckResult(False, "Selected file is not valid JSON.")

        res = self.validate(data)
        if not res.valid:
            return res

        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._storage_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return LicenseCheckResult(True, "License installed successfully.", data=res.data)

    def validate(self, lic: Dict[str, Any]) -> LicenseCheckResult:
        # Basic schema checks
        for k in ["schema", "product", "kid", "alg", "license_key", "stripe_session_id", "created_at", "features", "sig"]:
            if k not in lic:
                return LicenseCheckResult(False, f"Missing field: {k}")

        if lic["schema"] != 1:
            return LicenseCheckResult(False, "Unsupported license schema.")
        if lic["product"] != self._expected_product:
            return LicenseCheckResult(False, "License is for a different product.")
        if lic["alg"] != "ed25519":
            return LicenseCheckResult(False, "Unsupported signature algorithm.")
        if not isinstance(lic["features"], list):
            return LicenseCheckResult(False, "Invalid 'features' field.")

        # Verify signature
        sig_b64 = lic.get("sig", "")
        try:
            sig = base64.b64decode(sig_b64)
        except Exception:
            return LicenseCheckResult(False, "Signature is not valid base64.")

        payload = dict(lic)
        payload.pop("sig", None)
        msg = _canonical_json_bytes(payload)

        try:
            self._pub.verify(sig, msg)
        except Exception:
            return LicenseCheckResult(False, "Signature verification failed (license is not authentic).")

        return LicenseCheckResult(True, "License is valid.", data=lic)


    def has_feature(self, feature: str) -> bool:
        res = self.load_installed()
        return bool(res.valid and res.data and feature in res.data.get("features", []))



