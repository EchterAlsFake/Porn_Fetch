# Restart handoff — 2026-10-28

## Superseding update after disk expansion

The VM now has 53 GiB free at the start of this phase (roughly 49 GiB after builds), 16 logical CPUs and 16 GiB RAM. **The actual Porn Fetch app now builds and runs in the simulator**, displaying its real mobile Downloads UI and normal beta disclaimer. The process was observed remaining alive and idle. Read `README.md` in this directory for the current instructions and limits; the earlier blocker list below is historical.

All six native runtime checks passed inside the simulator: CFFI calls/callbacks, chompjs parsing, selectolax parsing, curl-cffi impersonated HTTPS, cryptography Ed25519 and asynchronous HTTPS using patched QtAsyncio. Results: `../build/native-probe-results.json`. Native builds now include libffi 3.8.0, OpenSSL 3.5.9, cryptography 50.0.2 and the downloaded curl-impersonate 2.3.1 static library. Rust is installed under `../toolchains/`. No Qt source was needed.

Real source edits are currently limited to `/Users/asuna/Porn_Fetch/src/backend/application.py` for explicit iOS mobile handling. The existing licensing flow and beta consent remain intact. No media downloads or provider-account/live lifecycle tests were performed. FFmpeg subprocess-based processing remains unresolved for iOS, as do physical iOS 15 compatibility and the app metadata's Python 3.14 range versus embedded 3.15. These are not solved by the successful launch.

Launch the installed app: `./run-application.sh --launch-only`. Re-stage changes: `../.venv/bin/python prepare-application.py`, then `./run-application.sh`. The validated Hello World is preserved. The normal beta disclaimer is awaiting the user's own review/OK action. Physical phone work remains deferred.

## Active task

Get the **actual Porn Fetch application running in the Intel iOS simulator first**, using the prebuilt Qt/PySide kit. Physical iPhone work is deferred. The phone is iPhone 7, iOS 15.8.8, palera1n **rootless**, not currently reachable. Do not spend time setting up phone connectivity/signing until the simulator app works.

The user is restarting the VM to enlarge the disk. Around **20 GB free** is the requested working room; no additional RAM needed yet. Check `df -h /` after restarting; enlarging the host disk may also require expanding the guest partition/APFS container.

## Proven baseline

- `/Users/asuna/ios-lab/qt` contains the working Python/PySide/QML Hello World.
- Native and Qt simulator apps both built, signed, installed and visibly rendered.
- Qt 6.12.0 Intel simulator wheel, embedded Python **3.15.0rc2**; host deployment venv uses Python 3.13.16.
- Working renderer: `QT_QUICK_BACKEND=rhi`, `QSG_RHI_BACKEND=opengl`, `QSG_RENDER_LOOP=basic`. Logs identify Apple's CPU Software Renderer. Qt's `software` adaptation gives a black screen because presentation still tries to use Metal.
- Run `/Users/asuna/ios-lab/run-qt.sh` after reboot; it can boot the saved simulator UUID.
- Simulator UUID: `7DFE048D-AB3D-453F-AE58-D474EF4C4569` (iPhone 16e, installed iOS 26.3).
- Full filesystem/network access is active. Run Simulator as asuna: `sudo -H -u asuna env DEVELOPER_DIR=... xcrun ...`, not as root's simulator user.
- Xcode remains `/Users/asuna/Downloads/Xcode.app`, SDK 26.2. See `../env.sh`.
- Working screenshot: `../build/qt-screenshot.png`. Build/deploy/runtime logs also in `../build/`.

## Application source

`/Users/asuna/Porn_Fetch`, clean tracked working tree at last check, commit `b38c98e`. User authorizes discarding local changes that interfere with syncing, but do not push. Read AGENTS.md, BACKEND.md, CONTEXT.md before editing. Source files have not been modified by the iOS work.

Current pyproject requires Python `>=3.14,<3.15`. The embedded 3.15 runtime is outside that declared range; compatibility needs to be investigated honestly, not silently ignored. Current GUI composition root: `src/backend/application.py`. It imports all provider clients and native dependencies at startup. A QML-only display with replacement backends is not a working port of the app.

Updated source no longer uses the earlier optional PyAV implementation. `src/shared/ffmpeg.py` delegates to **FFmpeg executable** discovery and subprocess-based media processing in eaf_base_api. This needs an iOS strategy. Desktop PocketBase/updater/browser-cookie assumptions also need platform handling. Do not bypass licensing or substitute fake networking to make imports appear successful.

## Dependency audit

PyPI JSON metadata checked on 2026-10-28:

| Package | Checked version | Intel iOS wheels on PyPI |
| --- | --- | --- |
| curl-cffi | 0.17.0 | None |
| cffi | 2.1.1 | ARM64 iOS wheels exist, **no Intel iOS wheel** |
| selectolax | 1.0.2 | None |
| cryptography | 50.0.2 | None |
| chompjs | 1.4.1 | C extension, needs target build |
| browser-cookie3 | 0.20.1 | Pure Python entry point but pulls lz4 and pycryptodomex; desktop cookie extraction is not an iOS feature |

Other runtime deps include eaf-base-api 4.2.5, provider APIs, TUF 7, rich, certifi, dateutil, platformdirs. Inspect the complete lockfile graph. Provider APIs bring selectolax and chompjs. QtAsyncio requires the repository's descriptor/context patch; inspect `scripts/patch_qtasyncio.py` and adapt/test for embedded Python 3.15.

BeeWare's secondary repository was checked at `https://pypi.anaconda.org/beeware/simple/cryptography/`; its newest observed Intel iOS crypto wheel is 47.0.0 cp313-abi3. This is older than the current app dependency stack. Do not install old crypto blindly; repository rules require maintained dependencies. Current cryptography likely needs a Rust/OpenSSL cross-build. No Rust/cargo was found in PATH.

## Useful progress before restart

1. Downloaded current curl-impersonate **v2.3.1 Intel iOS simulator libraries** from the upstream GitHub release. Archive: `libcurl-ios-simulator.tar.gz` in this directory. Published GitHub asset SHA-256 was verified:
   `2c221bf3b440e155acc4f9402702021a426b49f751cb5ecc63cf3164e67742e5`.
   It contains a merged `libcurl-impersonate.a`, dylibs and curl headers. This can avoid rebuilding its large dependency tree. Release metadata is saved in `../build/curl-impersonate-release.json`.
2. Downloaded and hash-verified PyPI source archives for cffi 2.1.1, chompjs 1.4.1 and curl-cffi 0.17.0. Sources are under `native/*-src/`.
3. Successfully compiled and linked chompjs's `_chompjs` C extension against the embedded Python 3.15 headers for **x86_64 iOS Simulator, minimum iOS 18**, using Xcode Clang. Artifact: `native/packages/_chompjs.cpython-315-iphonesimulator.so`. `file` and `vtool -show-build` verify the platform. **Runtime import/parsing is not yet tested.** `build-small-extensions.sh` reproduces it.
4. Tried compiling CFFI using Apple's SDK libffi and macOS headers. Clang explicitly rejects ffi functions as unavailable on iOS. Do not suppress those annotations as a workaround. Build a proper Intel iOS libffi, then set `LIBFFI_IOS_PREFIX` before running the script. CFFI build is currently deferred, not successful.

## Native packaging direction

The official Python framework includes `build/utils.sh` with `install_dylib`, `process_dylibs`, `install_python`. These convert `.so` files into signed `.framework` bundles plus `.fwork` import markers. Reuse that approach for third-party extensions, metadata and package data instead of copying desktop `.so` files.

Framework location:
`/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/Python.xcframework`

Target headers:
`ios-arm64_x86_64-simulator/Python.framework/Headers`

The generated Qt deployment tool currently only handles app Python/QML files and PySide; third-party packaging needs a deliberate additional build phase. Keep the working Hello World as a baseline while preparing a separate application project. Avoid duplicating the large Qt kit unnecessarily when disk is limited.

## System changes from deferred phone work

Before the simulator-first clarification, a Homebrew `ldid` installation was started. It pulled build dependencies and began building openssl@3. It was **stopped** after phone work was deferred, to leave no compilation running across the user's reboot. It did not finish installing ldid. Logs: `../build/ldid-install.log`. Check Homebrew's local state before relying on newly installed tools; do not resume the phone signing installation for the simulator task.

## Suggested next actions

1. Confirm free disk and restore simulator baseline.
2. Cross-build libffi/CFFI for the existing embedded Python; package and run actual import, callback and parsing probes in the simulator.
3. Generate curl-cffi's C wrapper with host CFFI, compile it for the iOS target against the downloaded static curl library; run real HTTPS/async callback checks without fetching adult media.
4. Build selectolax/chompjs and cryptography; preserve licenses, metadata and data files.
5. Bundle real application dependencies and source, add explicit iOS platform handling, then launch and fix actual startup failures. Audit FFmpeg/subprocess behavior separately.

Relevant primary sources: [Qt deployment](https://doc.qt.io/qtforpython-6/deployment/deployment-pyside6-ios-deploy.html), [CPython iOS](https://docs.python.org/3.15/using/ios.html), [curl-impersonate v2.3.1 release](https://github.com/lexiforest/curl-impersonate/releases/tag/v2.3.1), [BeeWare iOS package guidance](https://briefcase.beeware.org/en/latest/reference/platforms/iOS/xcode/).
