# Python native modules on the physical iPhone

All six checks passed on 2026-10-28 inside `NativeModules.app` on the physical iPhone 7 (arm64), iOS 15.8.8, palera1n rootless, embedded CPython 3.15.0rc2.

Result copied directly from the phone: `../build/native-modules-device-results.json`.

1. CFFI 2.1.1 with libffi 3.8.0: libc `strlen` call and a Python callback through libffi.
2. chompjs 1.4.1: JavaScript object parsed and compared with the expected Python dictionary.
3. selectolax 1.0.2: Lexbor HTML parsing and CSS selection.
4. curl-cffi 0.17.0 / curl-impersonate 2.3.1: Chrome impersonation, certificate-verified HTTPS request to example.com, status 200 and expected page text.
5. curl-cffi AsyncSession: the same request using real asyncio, status 200 and expected content.
6. cryptography 50.0.2 / OpenSSL 3.5.9: Ed25519 signing/verification and an AES-GCM authenticated-encryption round trip.

No provider/account/media requests were made. The simulator artifacts were not modified.

The first callback check crashed because CFFI selected its own closure allocator while the target libffi uses Apple trampoline tables. `build-native-python.py` now defines `FFI_AVAILABLE_APPLE=1` and `FFI_EXEC_TRAMPOLINE_TABLE=1` for the CFFI compilation. This selects libffi's matching closure allocator and structure layout. The callback succeeds without adding JIT entitlements or changing the jailbreak configuration. Initial crash report is retained at `../build/native-modules-first-crash.ips`.

Rebuild: `sh build-libffi.sh`, then `../.venv/bin/python build-native-python.py`, then `bash build-native-modules.sh`. Install using `sh deploy-app.sh NativeModules`; phone sudo prompts normally. No password is stored in any build/deployment script.

Bundle ID: `local.asuna.NativeModules`. Installed under `/var/jb/Applications/NativeModules.app`. Data container at this run: `/private/var/mobile/Containers/Data/Application/FE262142-97F3-4AD8-8BDB-8C8A2A6DCCF6`. Results are in its Documents directory.

Qt/PySide UI presentation was subsequently verified; see `PYTHON-QT-DEVICE-RESULT.md`, `QML-DEVICE-RESULT.md` and `PORN-FETCH-DEVICE-RESULT.md`. FFmpeg processing remains unverified.
