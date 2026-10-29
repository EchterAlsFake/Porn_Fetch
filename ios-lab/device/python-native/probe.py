"""Real native module checks on the phone; no provider or media requests."""
import asyncio
import importlib.util
import json
from pathlib import Path
import sys
import traceback

results = {"python": sys.version, "platform": sys.platform, "checks": {}}

def check(name, action):
    try:
        results["checks"][name] = {"passed": True, "detail": action()}
    except Exception:
        results["checks"][name] = {"passed": False, "error": traceback.format_exc()}

def cffi_check():
    from cffi import FFI
    ffi = FFI()
    ffi.cdef("size_t strlen(const char *);")
    assert ffi.dlopen(None).strlen(b"iphone") == 6
    callback = ffi.callback("int(int)", lambda x: x + 7)
    assert callback(5) == 12
    return "libc call and callback passed"

def chomp_check():
    import chompjs
    assert chompjs.parse_js_object("{phone: 'iPhone 7', value: 7}") == {"phone": "iPhone 7", "value": 7}
    return "JavaScript object parsed"

def selecto_check():
    from selectolax.lexbor import LexborHTMLParser
    assert LexborHTMLParser('<p class="test">device</p>').css_first("p.test").text() == "device"
    return "HTML and CSS selector passed"

def curl_check():
    import certifi
    from curl_cffi import requests
    with requests.Session(impersonate="chrome", verify=certifi.where()) as session:
        response = session.get("https://example.com", timeout=30)
        assert response.status_code == 200 and "Example Domain" in response.text
    return "Chrome impersonation / verified HTTPS 200"

def async_curl_check():
    import certifi
    from curl_cffi.requests import AsyncSession
    async def request():
        async with AsyncSession(impersonate="chrome", verify=certifi.where()) as session:
            response = await session.get("https://example.com", timeout=30)
            assert response.status_code == 200 and "Example Domain" in response.text
        return "asyncio / Chrome impersonation / verified HTTPS 200"
    return asyncio.run(request())

def cryptography_check():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    key = Ed25519PrivateKey.generate()
    message = b"iPhone 7 native cryptography"
    key.public_key().verify(key.sign(message), message)
    aes = AESGCM(AESGCM.generate_key(bit_length=128))
    nonce = b"012345678901"
    assert aes.decrypt(nonce, aes.encrypt(nonce, message, b"device"), b"device") == message
    return "Ed25519 sign/verify and AES-GCM round trip passed"

for name, action in [("cffi", cffi_check), ("chompjs", chomp_check), ("selectolax", selecto_check),
                     ("curl_cffi", curl_check), ("async_curl_cffi", async_curl_check)]:
    check(name, action)
if importlib.util.find_spec("cryptography") is not None:
    check("cryptography", cryptography_check)
results["all_passed"] = all(item["passed"] for item in results["checks"].values())
destination = Path.home() / "Documents/native-module-results.json"
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_text(json.dumps(results, indent=2))
print("NATIVE_MODULE_RESULTS", json.dumps(results), flush=True)
