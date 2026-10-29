# Physical iPhone build lab

Target: iPhone 7 (`iPhone9,1`), arm64, iOS 15.8.8, palera1n rootless. SSH uses the dedicated lab key and host alias from `../ssh/config`; installation uses the phone's existing sudo authentication. No password is embedded in these files.

**Current result: the real Porn Fetch app is installed and running on the phone, and the user confirmed its interface is visible.** See `PORN-FETCH-DEVICE-RESULT.md` for the exact build, data paths, rebuild/deployment commands and remaining media-processing limits.

Verified on the phone:

- Native UIKit Hello World: `NATIVE-DEVICE-RESULT.md`.
- Official embedded CPython 3.15.0rc2: `PYTHON-DEVICE-RESULT.md`.
- Python + custom PySide/Qt 6.12 UI, visually confirmed on the phone: `PYTHON-QT-DEVICE-RESULT.md`.
- Metal Qt Quick/Material rendering and real touch input: `QML-DEVICE-RESULT.md`.
- Real Porn Fetch source app: `PORN-FETCH-DEVICE-RESULT.md`.
- CFFI calls/callbacks, chompjs, selectolax, curl-cffi synchronous/asynchronous HTTPS, cryptography Ed25519 and AES-GCM: `NATIVE-MODULES-RESULT.md`.

The simulator app and its build scripts remain under `../pornfetch`.

## Qt source build

Sources are shallow clones of upstream v6.12.0 under `qt-src`. `qtbase` revision is `025bdad181de241e81bf853c8a2d7bf3d19261a9`. Host Qt tools are installed into `qt-host`; target libraries go into `qt-ios15`. Source/build directories are separate from the simulator's prebuilt wheel kit.

Run `sh build-qt-host.sh`, `sh build-qt-host-modules.sh`, then `sh build-qt-device-base.sh`. The host declarative configuration disables `qml_animation`, which skips host Qt Quick libraries while retaining the command line QML tools needed for cross compilation. The target build retains Qt Quick normally.

Qt 6.12's supported iOS minimum is 18. This experiment explicitly targets 15.0 and requires source compatibility work; passing compilation alone does not establish full compatibility. All four source languages have unguarded API availability warnings promoted to errors in the device build.

Current `qtbase` changes are saved in `patches/qtbase-ios15.patch`:

- Use Qt's existing generic mutex path and the upstream 6.8.3 public Mach-semaphore implementation when targeting iOS below 17.4. Current Qt's `os_sync_*` locking calls require iOS 17.4. The restored file preserves its upstream copyright/license.
- Guard Metal 3 capability detection and newer HDR setters/headroom queries behind runtime iOS 16 availability checks. Older iOS retains standard dynamic range rendering and disables unsupported indirect-command-buffer capability.
- Guard newer calendar permission, accessibility toggle traits, Pencil hover/rotation and HDR notification calls, retaining older supported behavior.

Qt base has built and installed successfully. The widget test passes its contended mutex check and produces the expected offscreen image. The first installations showed a black screen: both Metal device creation and OpenGL ES context creation were denied. Adding the GPU-only `com.apple.security.iokit-user-client-class` entitlement in `qt-app.entitlements.plist` made both APIs work; diagnostics now report `Apple A10 GPU`, an active/exposed native window, and successful Metal swapchain composition/presentation. The user subsequently visually confirmed the Python/PySide test app on the phone. Logs/results: `../build/qt-phone-runtime.log`, `../build/qt-phone-device-result.json`, `../build/python-qt-device-result.json`.

An explicit UIApplicationSceneManifest is also supplied by `finalize-qt-app.py` because the Ninja build does not generate Xcode's app metadata. No system-wide sandbox/jailbreak settings were changed. The signing entitlement grants only the enumerated graphics driver classes; it does not add general filesystem access or disable sandboxing.

Rebuild the remaining target Qt modules with `sh build-qt-modules.sh`, then `sh build-pyside.sh`. Bindings use the upstream 6.12 host generator wheel already installed in `../.venv`; a separate `build-venv` contains the source build's pinned packaging tools. CPython uses the official framework already verified on the phone.

The next native UI checks have source/build scripts ready: `qt-hello` / `build-qt-hello.sh` (widgets plus contended mutex exercise), then `qt-quick-hello` / `build-qt-quick-hello.sh` (Material QML and a rendered window capture). Install with `sh deploy-app.sh QtPhoneHello` or `sh deploy-app.sh QtQuickPhoneHello`. These are not marked verified until phone results are retrieved.

## Native Python dependencies

`sh build-libffi.sh` and `../.venv/bin/python build-native-python.py` produce separate arm64/iOS 15 extensions in `native/packages`. `bash build-native-modules.sh` packages a UIKit/Python app for native checks, using CPython's official framework-marker packaging functions. Run `sh deploy-app.sh NativeModules` to install/launch. Results are written in the app's Documents directory.

`sh build-cryptography.sh` builds OpenSSL 3.5.9 and cryptography 50.0.2 for arm64/iOS 15 with the isolated Rust toolchain under `../toolchains`. Build output is separate from the successful simulator build. The cryptography source's previously documented cross-compilation correction is shared with that build.

Downloads: `artifacts/libcurl-ios-arm64.tar.gz`, upstream curl-impersonate v2.3.1 ARM64 iOS static library, SHA-256 `16a3095fe0b107af2007be22b87c9f594658a04a22ad694abfd460f9bd70743e`, verified against upstream release metadata saved at `../build/curl-impersonate-release.json`.

Porn Fetch's actual interface has been verified on the phone. Media downloads through that UI and FFmpeg-dependent processing remain unverified. No live provider/account/media tests run automatically in this lab.
