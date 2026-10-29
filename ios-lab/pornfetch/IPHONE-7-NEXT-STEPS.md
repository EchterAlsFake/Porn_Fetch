# iPhone 7 deployment plan

Target: iPhone 7 (arm64/A10), iOS 15.8.8, palera1n rootless. The actual app and its native dependencies work in the Intel simulator. Wi-Fi SSH is configured and working from this VM using the lab key.

Physical phone progress on 2026-10-28: the real Porn Fetch app has been built, installed and launched, and the user confirmed its interface is visible on the phone. Source-built Qt/PySide 6.12 targets iOS 15; Python 3.15.0rc2, all native dependency checks (including cryptography), Metal QML rendering and physical touch input have passed. See `../device/PORN-FETCH-DEVICE-RESULT.md` for exact builds, installation, data paths and remaining limits. Phone media downloads, FFmpeg-dependent processing and background-transfer behavior remain to be validated.

## Main uncertainty: Qt on iOS 15

The current Qt 6.12 kit is built for iOS 18 minimum. Its toolchain file was checked locally, and Qt documents iOS 18+ support. Existing native-extension recipes also currently target minimum iOS 18. A device wheel for arm64 alone does not solve this minimum-version mismatch, and lowering Info.plist does not supply missing OS APIs.

The next build experiment should be a **tiny Qt/PySide Hello World on arm64/iOS 15**, before building the entire application for the phone. This is an unsupported compatibility investigation, not a promised one-flag rebuild.

Investigate current Qt 6.12 source with deployment target 15.0: compile only the necessary modules, audit newer API usage, add guarded compatibility fallbacks where feasible, and inspect the output's platform/minimum-version commands and linked symbols. Then rebuild matching PySide/shiboken bindings against that exact Qt kit. Test on the phone to identify actual loader/runtime errors. Preserve the functioning simulator build.

If current Qt needs an unreasonable number of backports, reconsider the Qt/PySide version strategy. Older Qt versions supported iOS 15, but arbitrarily downgrading conflicts with the repository's maintained-dependency requirement and can lose current Python/PySide compatibility. Establish maintenance/support and binding compatibility before choosing that route.

Source modules needed from the current application's imports/QML: qtbase, qtdeclarative, qtshadertools, qt5compat and qtsvg, plus matching host tools and pyside-setup. These v6.12.0 sources have been cloned under `../device/qt-src`; the physical build uses separate output directories from the simulator.

## Practical sequence

1. **Reach the phone.** Prefer Wi-Fi SSH for this VM to avoid USB passthrough complexity. Install/configure an SSH server using the phone's jailbreak package manager if needed, and establish access using a local terminal/key. Do not put passwords in chat. USB forwarding is another option once the Arch host passes the phone through to macOS.
2. **Native device sanity test.** Sign and install the existing tiny UIKit arm64 app, already compiled with minimum iOS 15.0. This validates installation, rootless paths and app registration independently of Qt/Python.
3. **Resolve Qt/PySide iOS 15 compatibility.** Build/test the tiny arm64 Qt/Python app described above. Do not interpret a simulator build as evidence that current Qt runs on iOS 15.
4. **Rebuild native extensions for arm64 and iOS 15.** libffi/CFFI, chompjs, selectolax, curl-cffi/curl-impersonate and cryptography/OpenSSL all need device-target artifacts. Reuse the proven source versions/recipes, changing architecture, SDK and minimum OS as appropriate. Audit upstream prebuilt curl libraries' actual deployment targets before reusing them. Repeat the dependency probe on-device, including callbacks and asynchronous HTTPS.
5. **Package the real app.** Use rootless architecture `iphoneos-arm64` and the `/var/jb` installation prefix where appropriate. Sign executable code/frameworks using the jailbreak-compatible tooling, register the app, and preserve app-writable paths and package data. The exact signing/trust-cache behavior must be verified against the installed palera1n environment.
6. **Test under phone constraints.** Startup, UI responsiveness, network/HTTPS, representative downloads, screen locking/background transitions and memory pressure. The iPhone 7 has much less memory than this VM. Its A10 has a GPU; the VM-specific OpenGL CPU-renderer workaround should not be imposed automatically on the physical device.

## What the successful download establishes

The user's simulator download produced a healthy fragmented MP4 without invoking local FFmpeg. Full decoding on the host passed for both tracks. This establishes that this provider/container/download path works. It does not prove remuxing or metadata writing works without FFmpeg on iOS.

For media paths that require FFmpeg processing, either expose appropriately built FFmpeg libraries through an in-process adapter, or separately investigate a jailbreak-specific executable execution arrangement. Standard embedded iOS Python's subprocess restrictions still apply to the current build; a jailbreak does not automatically change that build's Python APIs.

## References

- [Current Qt iOS requirements and deployment-target cautions](https://doc.qt.io/qt-6/ios.html)
- [Qt for Python iOS cross-compilation and packaging](https://doc.qt.io/qtforpython-6/deployment/deployment-pyside6-ios-deploy.html)
- [Theos rootless layout and package architecture](https://theos.dev/docs/rootless)
- [CPython on iOS](https://docs.python.org/3.15/using/ios.html)
