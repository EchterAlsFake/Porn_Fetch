# Porn Fetch on the physical iPhone 7

On 2026-10-28 the real Porn Fetch source application was built, signed, installed and launched on the iPhone 7 (`iPhone9,1`) running iOS 15.8.8 / palera1n rootless. The user confirmed **“Porn Fetch’s interface is visible.”**

The runtime log records the real backend import and successful client initialization/refresh. A live `PornFetch_bin` process was confirmed after launch. Evidence: `../build/pornfetch-phone-runtime.log`, `../build/pornfetch-phone-app.log`, `../build/pornfetch-phone-runtime-and-process.txt`. No automated provider, account, licensing-lifecycle or media-download tests were run.

## Exact build

- Source: `/Users/asuna/Porn_Fetch`, commit `b38c98e27b9318da374c1cf3a639b3e813b436e6`.
- Application source adjustment: the existing simulator-tested iOS mobile detection in `src/backend/application.py`. It uses the mobile layout, writable application data, Material style, and disables the desktop splash/SNI startup/database tracking on mobile. Original generated `resources.py` is untouched; `resources.rcc` is generated for the bundle.
- Embedded Python: official CPython 3.15.0rc2 iOS framework, independently verified on this phone.
- GUI: Qt/PySide 6.12.0, source-built for arm64 with minimum iOS 15.0. Qt compatibility patch and all pinned source revisions/wheel/archive hashes are saved under `patches` and `BUILD-REVISIONS.json`.
- Qt modules: base, ShaderTools, Svg, Declarative/Quick/Controls, Core5Compat/GraphicalEffects. Bindings: Core, Gui, Network, OpenGL, Svg, Qml, Quick, QuickControls2. Build the OpenGL bindings before Quick so generated header paths are available.
- Native dependencies: libffi 3.8.0 / CFFI 2.1.1, chompjs 1.4.1, selectolax 1.0.2, curl-cffi 0.17.0 / curl-impersonate 2.3.1, cryptography 50.0.2 / OpenSSL 3.5.9. All six native checks passed directly on the phone; see `NATIVE-MODULES-RESULT.md`.
- Python Qt window and Material QML rendering/touch were verified independently. The QML test read back a 750×1294 Metal-rendered image and recorded five real button taps.

## Installation and data

- Bundle ID: `local.asuna.PornFetch`.
- Installed app: `/var/jb/Applications/PornFetch.app`.
- Executable: `PornFetch_bin`.
- Current data container: `/private/var/mobile/Containers/Data/Application/DD69C8B2-BD02-4B6B-9822-06794E9B17D8`.
- Working directory, runtime logs and relative application files: `Documents/PornFetch` inside that container. Licensing uses Qt's writable AppDataLocation.
- File sharing and opening documents in place are enabled in Info.plist for access to the app's Documents folder.
- Main executable carries the explicit GPU-driver entitlement from `qt-app.entitlements.plist`. Without it, the first UI probes could not obtain Metal/GLES contexts and appeared black. The signature change enabled Apple A10 GPU access without global sandbox/jailbreak changes. No JIT entitlement was needed.
- Phone SSH uses the dedicated lab key; deployment sudo prompts normally. No password is saved in the scripts.

Build artifact: `app-derived/Build/Products/Release-iphoneos/PornFetch.app`. Transfer archive: `artifacts/PornFetch.tar` (about 311 MiB at this build). The archive SHA-256 is in `BUILD-REVISIONS.json`.

## Rebuild the application

After the source-built kit and full device wheels exist:

```sh
cd /Users/asuna/ios-lab/device
../.venv/bin/python prepare-application.py
sh build-application.sh > ../build/device-app-build.log 2>&1
sh deploy-app.sh PornFetch
```

The first command stages the real repository source/resources and dependency overlay and regenerates the Xcode project. The second builds for the phone and signs/packages the result. The last installs and launches it using SSH. It replaces only the lab app bundle and retains its separate data container.

## Remaining validation / features

The user downloaded a real video through this phone's UI and confirmed smooth operation and access in Files. The 445,108,800-byte download was MPEG-TS despite its `.mp4` filename, and Apple's media framework could not open it. An in-process FFmpeg 9.0.2 integration is now installed and remuxing is enabled for future downloads. The existing download was copied into a real faststart MP4 in 4.893 seconds; native AVFoundation decoded both audio and video successfully. Metadata and PNG cover-art writing also passed. The user confirmed video/audio playback in Files and successful automatic remuxing of a fresh in-app download. See `FFMPEG-DEVICE-RESULT.md` for the build, evidence and remaining checks.

The app's startup log contains OpenSSL's warning that its legacy provider could not load. Modern Ed25519/AES-GCM and certificate-verified HTTPS checks passed. Legacy cipher/provider features were not validated. Desktop-only services and Android-only export/install paths have not been ported to iOS. Background transfers and memory-pressure behavior remain unverified.

The working simulator project is preserved under `../pornfetch`. This physical device uses its own source-built Qt kit, native libraries, wheels, build directories, bundle ID and data container.
