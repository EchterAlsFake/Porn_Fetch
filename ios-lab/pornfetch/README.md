# Porn Fetch in the Intel iOS simulator

The real application now builds, signs, installs and launches in the iOS 26.3 simulator. Its mobile Downloads screen and normal beta disclaimer are visible. No replacement networking backend or licensing bypass is used. Screenshot: `../build/pornfetch-screenshot.png`.

## Launch

From normal macOS Terminal:

```sh
cd /Users/asuna/ios-lab/pornfetch
./run-application.sh --launch-only
```

The script boots the existing iPhone 16e simulator if needed and launches the installed app. Review the normal beta disclaimer and click OK in the app if you agree. The usual licensing flow remains active.

To refresh the staged source, rebuild and reinstall after editing the repository:

```sh
cd /Users/asuna/ios-lab/pornfetch
../.venv/bin/python prepare-application.py
./run-application.sh
```

Run these as `asuna`; `run-application.sh` automatically switches to that user if invoked as root. Xcode remains in Downloads. The generated Xcode project is `app/deployment/ios_x86_64_simulator/PornFetch.xcodeproj`.

## What was verified

All of these execute inside embedded Python in the simulator, not in desktop Python:

- CFFI 2.1.1: call libc `strlen` and invoke a C callback, using a target-built libffi 3.8.0.
- chompjs 1.4.1: parse a real JavaScript object.
- selectolax 1.0.2: parse HTML and select an element using CSS.
- curl-cffi 0.17.0 / curl-impersonate 2.3.1: verified HTTPS request with Chrome impersonation to `https://example.com`, returning HTTP 200 and the expected page.
- cryptography 50.0.2 / OpenSSL 3.5.9: generate an Ed25519 key, sign data and verify the signature.
- Patched QtAsyncio: asynchronous HTTPS through curl-cffi, returning HTTP 200.
- Real Porn Fetch startup: all provider clients initialize, the actual QML/resource bundle loads and the process remains running at its normal beta disclaimer.

The native probe source is in `probe/`. Its latest complete results are in `../build/native-probe-results.json`; raw logs are `probe-runtime.log` and `probe-runtime.err` in the same build directory.

No provider-account login, production license activation, media download, or full UI regression suite has been performed. The source repository requests explicit opt-in for those live tests; this port's network checks used example.com only. A working launch is not evidence that every feature is portable.

**User download update:** the user subsequently downloaded a real video in the simulator. A read-only full decode check verified its 398,679,164-byte fragmented MP4: 1280×720 H.264 at 30 fps, stereo AAC at 44.1 kHz, approximately 33:56. All 61,073 video frames and 87,678 audio frames decoded, with no decoder warnings/errors, corrupt packets or timestamp regressions. MP4 box lengths cover the entire file and the file remained unchanged during the check. Results: `../build/download-integrity.json`; checker: `check-downloaded-media.py`. This proves that particular download path works without a local FFmpeg remux. Media-processing modes that require FFmpeg remain unimplemented. See `IPHONE-7-NEXT-STEPS.md` for the phone plan.

## Material limitations

- **FFmpeg media processing is not yet implemented for iOS.** The updated application delegates to an FFmpeg executable and subprocesses. Standard embedded iOS Python does not support that execution model. We need a library-based/native adapter before claiming remuxing, metadata writing and all download modes work.
- Desktop browser-cookie extraction is omitted. The application already loads browser-cookie3 lazily and handles its absence. Native browser storage is not accessible using desktop assumptions.
- Desktop PocketBase tracking and SNI service startup are disabled on iOS. The existing mobile layout is reused. Desktop-style updater/Tor/installer workflows are not validated on iOS.
- The official Qt iOS wheels embed **Python 3.15.0rc2**. The application metadata still requires **Python >=3.14,<3.15**. This is an explicitly experimental target: the validated startup and dependency checks establish useful compatibility, but do not justify changing the application's supported Python range for all platforms.
- These Qt 6.12 libraries target **iOS 18+**, so they cannot be transferred directly to the iPhone 7 running iOS 15.8.8. Physical phone work remains deferred at the user's request.

## Implementation

Qt and PySide use their official prebuilt Intel iOS simulator wheel. No Qt source build was required. The existing unpacked kit is shared with the working Hello World, which remains under `../qt/`.

The VM has no Metal support. The working graphics settings are `QT_QUICK_BACKEND=rhi`, `QSG_RHI_BACKEND=opengl` and `QSG_RENDER_LOOP=basic`; Qt logs identify Apple's OpenGL CPU software renderer. Qt's own `software` adaptation still attempted Metal presentation and produced a black window in this VM.

Native Python extensions are cross-compiled against the embedded Python headers and Simulator SDK, then converted into signed frameworks with `.fwork` import markers using the official Python framework's `build/utils.sh`. The bundle phase preserves package data and `.dist-info`, including certificates and metadata needed by curl-cffi. Native packages are in `native/packages/`; Python/data overlays are in `vendor/`.

`prepare-application.py` stages the actual repository source, builds a binary Qt resource file and applies the repository's QtAsyncio compatibility patch to an isolated iOS overlay for Python 3.15. Source resources.py and the desktop PySide environment are untouched. The only production source edits so far are in `src/backend/application.py`: recognize iOS as mobile, use the existing mobile layout and app-data path, avoid the separate splash and disable desktop service startup.

The host build venv uses Python 3.13. Rust 1.99.1 and the Intel iOS target are installed under `../toolchains/`, rather than changing the login shell configuration. Cryptography's local source has one cross-build adjustment: its macOS compiler-runtime linkage is restricted to apple-darwin targets, avoiding a macOS library in an iOS binary. The Python framework is supplied to the linker through a local target-prefix layout.

## Native build recipes

Sources/versions and hashes are recorded in `native-build-manifest.json`. Source archives were verified against upstream GitHub asset digests or PyPI metadata before extraction.

```sh
./build-libffi.sh
LIBFFI_IOS_PREFIX="$PWD/native/libffi-ios" ./build-small-extensions.sh
../.venv/bin/python build-selectolax.py
../.venv/bin/python build-curl-wrapper.py
./build-openssl.sh
./build-cryptography.sh
../.venv/bin/python prepare-pure-deps.py
../.venv/bin/python prepare-probe.py
./run-probe.sh
../.venv/bin/python prepare-application.py
./run-application.sh
```

The source-fetching steps were performed during setup; these recipes expect the verified source folders already present. Keep this directory across VM restarts. Build logs are in `../build/`. This is local build tooling, not a published reproducible SDK installer.
