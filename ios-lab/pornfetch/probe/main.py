"""Run real native-dependency checks inside embedded iOS Python."""
import json
import os
from pathlib import Path
import traceback
import asyncio

os.environ.setdefault("QT_QUICK_BACKEND", "rhi")
os.environ.setdefault("QSG_RHI_BACKEND", "opengl")
os.environ.setdefault("QSG_RENDER_LOOP", "basic")

from PySide6.QtCore import QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
import PySide6.QtAsyncio as QtAsyncio

app = QGuiApplication([])
engine = QQmlApplicationEngine()
engine.load(str(Path(__file__).parent / "qml" / "Main.qml"))
if not engine.rootObjects():
    raise SystemExit("Probe QML did not load")
window = engine.rootObjects()[0]


async def run_checks():
    await asyncio.sleep(0.5)
    results = {}
    def check(name, operation):
        try:
            results[name] = {"ok": True, "result": operation()}
        except Exception:
            results[name] = {"ok": False, "error": traceback.format_exc()}
        print("NATIVE_PROBE", name, json.dumps(results[name]), flush=True)

    def cffi_check():
        from cffi import FFI
        ffi = FFI()
        ffi.cdef("size_t strlen(const char *);")
        assert ffi.dlopen(None).strlen(b"simulator") == 9
        callback = ffi.callback("int(int)", lambda value: value + 7)
        assert callback(5) == 12
        return "libc call and C callback passed"

    def chomp_check():
        import chompjs
        value = chompjs.parse_js_object('{answer: 42, valid: true}')
        assert value == {"answer": 42, "valid": True}
        return value

    check("cffi", cffi_check)
    check("chompjs", chomp_check)
    def selectolax_check():
        from selectolax.lexbor import LexborHTMLParser
        tree = LexborHTMLParser('<html><body><p class="test">parsed</p></body></html>')
        assert tree.css_first('.test').text() == 'parsed'
        return 'HTML parsing passed'

    def curl_check():
        from curl_cffi import requests
        response = requests.get('https://example.com', impersonate='chrome', timeout=20)
        assert response.status_code == 200
        assert 'Example Domain' in response.text
        return {'status': response.status_code, 'bytes': len(response.content)}

    check("selectolax", selectolax_check)
    check("curl HTTPS", curl_check)
    def crypto_check():
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        key = Ed25519PrivateKey.generate()
        signature = key.sign(b'iOS cryptography probe')
        key.public_key().verify(signature, b'iOS cryptography probe')
        return 'Ed25519 signing and verification passed'

    check("cryptography", crypto_check)
    try:
        from curl_cffi.requests import AsyncSession
        async with AsyncSession() as session:
            response = await session.get('https://example.com', impersonate='chrome', timeout=20)
            assert response.status_code == 200
            assert 'Example Domain' in response.text
        results['QtAsyncio HTTPS'] = {'ok': True, 'result': response.status_code}
    except Exception:
        results['QtAsyncio HTTPS'] = {'ok': False, 'error': traceback.format_exc()}
    result_text = "\n".join(f'{name}: {"PASS" if item["ok"] else "FAIL"}'
                            for name, item in results.items())
    window.setProperty("results", result_text)
    print("NATIVE_PROBE_COMPLETE", json.dumps(results), flush=True)


QtAsyncio.run(run_checks(), handle_sigint=False)
