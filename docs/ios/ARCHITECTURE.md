# iOS implementation and validation

This describes the port recorded on 2026-10-28. For commands, see
[Building for iOS](BUILDING.md). Recorded results are evidence from that experiment,
not a claim that later changes have passed device regression checks.

## Application integration

`src/backend/application.py` recognizes `sys.platform == "ios"` and treats iOS
as mobile alongside Android. It selects the existing `AndroidMain.qml` layout
and Material style, avoids the separate desktop splash and automatic desktop SNI
service startup, disables desktop PocketBase tracking, and puts licensing data
in Qt's writable AppDataLocation. Android-specific display/storage code remains
Android-specific.

The rest of the iOS tooling is isolated under `ios-lab/`. The device and simulator
launchers stage the current repository's real backend/QML, not another maintained
copy of the application. They use `Documents/PornFetch` inside the app data
container as the working directory. The device finalizer enables Files sharing
and opening documents in place. Original licensing and beta-consent behavior
are retained.

The normal desktop Python constraint stays `>=3.14,<3.15`. The lab uses an official
embedded CPython **3.15.0rc2** framework and independently staged dependencies.
The successful experiment does not establish full application compatibility with
Python 3.15 or change the supported desktop environment.

## Device and simulator kits

| | Physical device | Original Intel simulator |
| --- | --- | --- |
| Target | arm64, iOS 15.0 minimum | x86_64, iOS 18 minimum |
| Runtime tested | iPhone 7, iOS 15.8.8, palera1n rootless | iOS 26.3 on Intel macOS VM |
| Qt/PySide | Source-built 6.12.0 with compatibility patch | Official prebuilt 6.12.0 wheels |
| Graphics | Metal on Apple A10 GPU | OpenGL CPU renderer, basic render loop |
| Native artifacts | `device/native/`, `device/wheels/` | `pornfetch/native/`, `wheels/` |
| FFmpeg adapter | Integrated | Not integrated |

Qt 6.12's [supported iOS configuration](https://doc.qt.io/qt-6/ios.html) starts at
iOS 18. The patched iOS 15 kit is an experimental compatibility build, not an
upstream-supported deployment configuration. Changing a plist's minimum version
cannot replace unavailable system APIs.

[`qtbase-ios15.patch`](../../ios-lab/device/patches/qtbase-ios15.patch) restores
the public Mach-semaphore mutex implementation from upstream Qt 6.8.3 for targets
below iOS 17.4, retaining its license notice. It also guards newer calendar,
accessibility, Pencil and Metal/HDR APIs with availability checks. Older systems
retain supported behavior, including standard dynamic range rendering. Target
builds turn unguarded API availability warnings into errors.

The physical app needs an explicit scene manifest and the GPU-driver classes in
[`qt-app.entitlements.plist`](../../ios-lab/device/qt-app.entitlements.plist).
Without those GPU permissions, the early jailbreak-signed probes could not obtain
Metal/GLES contexts and displayed black. The finalizer signs frameworks and the
executable with Procursus `ldid`; the executable receives that entitlement.
No JIT entitlement or system-wide sandbox change was required. This is distinct
from normal Apple developer signing and has not established an App Store path.

## Native Python dependencies

The recorded stack uses libffi 3.8.0 / CFFI 2.1.1, chompjs 1.4.1,
selectolax 1.0.2, curl-cffi 0.17.0 / curl-impersonate 2.3.1, and
cryptography 50.0.2 / OpenSSL 3.5.9. Device and simulator libraries are built
against their own SDK, deployment target, architecture and embedded Python headers.
Desktop wheels and Apple's libcurl do not substitute for these builds.

The bundle phase uses the official Python framework's `build/utils.sh`
`process_dylibs` function to turn extensions into signed frameworks and `.fwork`
import markers. Certificates, package data and `.dist-info` accompany the code.
This follows [CPython's iOS extension packaging](https://docs.python.org/3.15/using/ios.html).
QtAsyncio is copied into an isolated overlay and patched using the repository's
`scripts/patch_qtasyncio.py` for the embedded Python version.

Desktop browser-cookie extraction is omitted; the real backend imports it lazily.
That omission does not establish an alternative iOS browser-session import flow.

## In-process FFmpeg

The device build links FFmpeg **9.0.2** libavformat, libavcodec and libavutil into
the `_ios_ffmpeg` CPython extension. It stream-copies local media into faststart
MP4, writes tags and JPEG/PNG cover art, and releases the GIL during media I/O.
Tagging uses a temporary file and replaces the original only on success.

`device/native/packages/ios_ffmpeg.py` is the Python adapter.
`device/patch-ios-ffmpeg.py` adds three iOS-only dispatch branches to the **staged**
base_api FFmpeg module: discovery, remux and metadata. The saved patch is
[`base-api-ios-ffmpeg.patch`](../../ios-lab/device/patches/base-api-ios-ffmpeg.patch).
Desktop dispatch remains in the upstream module. The existing provider remux
operation already uses `asyncio.to_thread`; no Qt worker-thread logic is added.

No executable subprocess is needed. The build disables GPL, version3, nonfree,
network protocols and encoders. FFmpeg license notices and configuration are
bundled under `packages/ffmpeg-legal`. The snapshot preserves the source archive
and static build outputs. This adapter provides remuxing, not transcoding.

## Recorded validation

All reports below were copied from the original lab and are dated by that
experiment, 2026-10-28. Source revisions, target settings, wheel hashes and
FFmpeg input hashes are in
[`BUILD-REVISIONS.json`](../../ios-lab/device/BUILD-REVISIONS.json).

| Evidence | Recorded result |
| --- | --- |
| [Device native modules](../../ios-lab/results/native-modules-device-results.json) | CFFI call/callback, JS/HTML parsing, certificate-verified Chrome HTTPS, async HTTPS, Ed25519 and AES-GCM passed |
| [Simulator native modules](../../ios-lab/results/native-probe-results.json) | CFFI, parsers, verified HTTPS, async HTTPS and Ed25519 passed |
| [Python/Qt device probe](../../ios-lab/results/python-qt-device-result.json) | Embedded Python/PySide window active and exposed; user confirmed screen |
| [Material QML device probe](../../ios-lab/results/qt-quick-phone-result.json) | Metal rendering, 750×1294 capture, five actual button taps |
| [Device FFmpeg check](../../ios-lab/results/ffmpeg-phone-result.json) | 445,108,800-byte MPEG-TS remuxed in 4.893 seconds; AVFoundation decoded audio/video; metadata and PNG cover passed |
| [Remuxed file integrity](../../ios-lab/results/phone-remuxed-integrity.json) | Complete audio/video/cover decode; no corrupt packets, decoding errors or timestamp regressions; faststart verified |
| [Simulator download integrity](../../ios-lab/results/download-integrity.json) | Complete decode of one user-downloaded fragmented MP4; zero corrupt packets or decoding errors |

The user additionally confirmed the real app interface and smooth operation,
video/audio playback in Files, and automatic remuxing of a **fresh in-app
download** on the physical phone. These are manual confirmations rather than
automated provider coverage. The full device file check retained one PyAV
timescale warning with attached cover art; native playback and full decoding
still passed.

## Remaining work

- Background transfers, screen-lock transitions and memory-pressure behavior
  have not been validated.
- Account/browser-session flows, license activation and the full GUI/provider
  regression suite have not been repeated on iOS.
- Desktop updater, Tor, installer and Android export/install paths have not been
  ported as validated iOS workflows.
- OpenSSL logged a failure to load its legacy provider. Modern Ed25519/AES-GCM
  and certificate-verified HTTPS passed; legacy cipher features remain unverified.
- Other iPhones/iPads, Apple Silicon simulator builds and ordinary Apple signing
  remain unverified. There is no iOS release pipeline or public installable IPA.
- The scripts still depend on preserved lab inputs and absolute macOS toolchain
  paths. A clean bootstrap and portable build configuration remain future work.

Generated source duplicates, raw build logs, crash dumps, host-specific download
checkers and superseded handoff notes were removed from the maintained tree.
The original branch/tag and [full snapshot](SNAPSHOT.md) retain that history.
