# Building for iOS

Porn Fetch officially supports iOS 15.0 and later with a native ARM64 GUI. The IPA is installed through a sideloading tool that re-signs and provisions it; no jailbreak is required. Device testing includes an iPhone 7 on iOS 15.8.8.

The app checks for new iOS releases at startup after first-use setup. Settings
lets you disable startup checks or update dialogs and check manually. When a
new IPA is available, **Open downloads** opens the iOS download page. Install
the new IPA with your sideloading tool.

## GitHub Actions

The **Cross-Platform Build Pipeline** builds iOS on macOS ARM64 with Xcode alongside the other platforms. Choose `gui`, `both`, or `ios` and supply a three-part
`release_version`. It uses Python 3.15.2 for host deployment tools and the matching
Qt/PySide 6.12.0 device wheels with embedded Python 3.15.0rc2 from
[the iOS toolchain release](https://github.com/EchterAlsFake/PySide6-to-iOS/releases/tag/6.12.0-ios15-cp315).
The workflow verifies the pinned manifest and asset checksums. The embedded runtime remains 3.15.0rc2 until the matching runtime and native dependencies are rebuilt and published together. It receives the same application version and original run timestamp as every other platform. Enable `deploy_website` and the existing redistribution acknowledgment to publish the IPA, checksum and notices on the website. GitHub Release publication includes the IPA too.

An Ubuntu job restores the required native dependencies from the archived lab.
Its token needs access to the draft snapshot release. A public clone alone does
not contain those dependencies. These native packages and their Python metadata
must be updated together; desktop wheels cannot replace them.

Staging installs the pure Python PyJWT wheel using the requirement in
`pyproject.toml`, since the archived overlay predates that startup dependency.
It disables dependency resolution so the matching native packages stay intact.
The Xcode bundle phase checks the built app for `jwt` and its distribution
metadata; CI repeats that check on the final IPA before uploading it.

The output is `PornFetch_ios_GUI_arm64_resign.ipa`. It has ad-hoc signatures,
not an Apple distribution signature or provisioning profile. Re-sign and
provision it with your own sideloading setup before installing. Security tools
may warn about self-built files. The workflow checks packaging but does not
install on a phone. Test startup and a download on the intended device.

Before staging, CI runs `packaging/prepare_ios_legal.py` with the verified
FFmpeg 9.0.2 source archive. The helper checks the restored extension's recorded
hash and retains its actual build configuration. Both the IPA and the separate
legal archive receive the FFmpeg source, bridge sources and replacement
instructions. Local native rebuilds prepare the same materials automatically.
Use `IOS_PYTHON_XCFRAMEWORK` to select the matching published Python headers.
The FFmpeg bundle's `REBUILD.md` also explains replacement in an existing IPA
without access to the private native dependency snapshot.

## Download and verify

Install the GitHub CLI, GnuPG and zstd, authenticate `gh` with an account that
can read the draft, then download into an empty directory:

```sh
gh release download ios-iphone7-snapshot-2026-10-28 \
  --repo EchterAlsFake/Porn_Fetch --dir ios-snapshot
cd ios-snapshot
gpg --verify SHA256SUMS.asc SHA256SUMS
shasum -a 256 -c SHA256SUMS
cat ios-lab-full-snapshot.tar.zst.part-* | zstd -d | tar -xf -
```

Import the signer's [public key](https://github.com/EchterAlsFake/EchterAlsFake/blob/main/public-key_v3.asc) through your trusted channel before verifying.
The recorded fingerprint is
`7082BBFF855D47C6BB13C3BF6AC58B8CA26D1C5F` (Johannes Habel).
On Linux, `sha256sum -c SHA256SUMS` can replace `shasum`.

The four numbered parts are **one** zstd-compressed tar archive; concatenate
them in filename order. Compressed size is about 7.43 GB and the archived file
contents total about 21.16 GB. Allow additional disk space for downloads,
extraction, the current checkout, Xcode and rebuilding. All part sizes and hashes
are in [`snapshot-assets.json`](../ios-lab/snapshot-assets.json).

Extraction produces:

```text
ios-lab/
python-ios/3.15.0rc2/
```

Keep an untouched extracted copy if you need the historical state. For a baseline
rebuild, place these trees at the original macOS paths without overwriting an
existing lab:

```text
/Users/asuna/ios-lab/
/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/
```

For example, if neither destination exists:

```sh
test ! -e /Users/asuna/ios-lab && mv ios-lab /Users/asuna/ios-lab
mkdir -p /Users/asuna/.pyside6_ios/Python-iOS
test ! -e /Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2 && \
  mv python-ios/3.15.0rc2 /Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2
```

The original paths appear in generated projects, venv shebangs and native build
configuration. Restoring elsewhere requires updating those paths and rebuilding
or regenerating affected components. The snapshot's macOS tools and iOS binaries
cannot build or run natively on Linux.


## Prepare the workspace

Keep the current Git checkout at `/Users/asuna/Porn_Fetch` and the restored lab
at `/Users/asuna/ios-lab`. After restoration, overlay the maintained build sources
onto the restored lab, preserving its ignored dependency/build directories:

```sh
cd /Users/asuna/Porn_Fetch
rsync -a --exclude='.gitignore' ios-lab/ /Users/asuna/ios-lab/
export PORN_FETCH_SOURCE=/Users/asuna/Porn_Fetch
cd /Users/asuna/ios-lab
. ./env.sh
mkdir -p build device/artifacts
xcodebuild -version
xcrun --sdk iphoneos --show-sdk-path
.venv/bin/python --version
.venv/bin/pyside6-ios-deploy --help
test -x device/tools/ldid
test -d device/qt-ios15/lib/cmake/Qt6
test -d /Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/Python.xcframework
```

Use a normal macOS Terminal user. Do not run the build or Simulator as root.
Complete Xcode's first-launch setup if requested. The deployment environment
must have `pyside6-rcc` and `pyside6-ios-deploy` from the matching 6.12.0 host tools.
If a restored venv cannot start, recreate it at the same path with Python 3.13
and the package versions recorded in `HOST-ENVIRONMENT.json`; the custom host
generator wheel is preserved under `device/artifacts/`.

## Build the device application

With the restored kit, wheels and native packages in place:

```sh
cd /Users/asuna/ios-lab/device
../.venv/bin/python prepare-application.py
set -o pipefail
sh build-application.sh 2>&1 | tee ../build/device-app-build.log
```

Preparation copies **the current repository's** `src/` into the staging tree,
generates a binary `resources.rcc`, copies the Python dependency overlay, adds
arm64 native extensions, and applies the iOS FFmpeg dispatch patch to the staged
`base_api`. It generates
`app/deployment/ios_arm64/PornFetch.xcodeproj` and customizes its bundle phase
to retain nested QML, Python packages, certificates and package metadata.

The build script runs `xcodebuild` for Release/iphoneos with ordinary Apple code
signing disabled. `finalize-qt-app.py` then adds scene metadata and Files sharing,
removes desktop/test stdlib payload, signs each framework and the executable with
`ldid`, and creates the transfer archive. This signing path is specific to the
tested jailbroken device.

Outputs:

- `app-derived/Build/Products/Release-iphoneos/PornFetch.app`
- `artifacts/PornFetch.tar`
- `../build/device-app-build.log`

Inspect the executable before installing:

```sh
file app-derived/Build/Products/Release-iphoneos/PornFetch.app/PornFetch_bin
xcrun vtool -show-build app-derived/Build/Products/Release-iphoneos/PornFetch.app/PornFetch_bin
plutil -lint app-derived/Build/Products/Release-iphoneos/PornFetch.app/Info.plist
```

Expected target: arm64, platform iOS, minimum OS 15.0. An arm64 **simulator**
binary is still the wrong platform; architecture alone is insufficient.

## Install and launch on the phone

Use the already configured palera1n rootless phone with SSH, `sudo`, `uicache`,
and `uiopen`. Jailbreak installation itself is outside this build guide.
Create your own `ios-lab/ssh/config` and private key; these are not in the
snapshot. For example, replace the host, user and identity values:

```sshconfig
Host ios-phone
    HostName YOUR_PHONE_ADDRESS
    User mobile
    IdentityFile /absolute/path/to/your/private_key
    IdentitiesOnly yes
```

Verify the host key and key authentication in your terminal, then deploy:

```sh
cd /Users/asuna/ios-lab/device
ssh -F ../ssh/config ios-phone 'uname -m'
sh deploy-app.sh PornFetch
```

The script stops the lab app, replaces
`/var/jb/Applications/PornFetch.app`, registers it and launches bundle ID
`local.asuna.PornFetch`. Installation prompts for the phone user's sudo password;
the script does not store it. The app's separate data container is retained.

The launcher writes `Documents/PornFetch/ios-runtime.log` in its data container.
Downloads and runtime files live in `Documents/PornFetch`; Files sharing exposes
the Documents folder. Licensing uses Qt's writable AppDataLocation. Container
UUIDs vary, so do not reuse the historical absolute data-container path.

Verify the actual interface on the phone and inspect its runtime log. A successful
Xcode build alone does not establish successful launch, rendering or downloading.
Representative downloads and playback are manual, opt-in checks.

## Incremental rebuilds

After Python/QML/resource edits, restage and rebuild:

```sh
cd /Users/asuna/ios-lab/device
../.venv/bin/python prepare-application.py --stage-only
set -o pipefail
sh build-application.sh 2>&1 | tee ../build/device-app-build.log
sh deploy-app.sh PornFetch
```

Use preparation **without** `--stage-only` for the initial build or changes to
QML inventory, Qt modules, wheel selection, or project settings. The flag reuses
the existing Xcode project. Staging replaces its generated source copy; edit the
main repository, not `device/app/src`.

For FFmpeg bridge changes, run `../.venv/bin/python build-ffmpeg.py` before
restaging. It expects `device/artifacts/ffmpeg-9.0.2.tar.xz` with the recorded
SHA-256. Its flags come from the main repository's
`packaging/ffmpeg_configure_flags.txt`.

## Rebuild device dependencies from preserved sources

This section is optional when reusing the restored kit. Source revisions and
hashes are in [`BUILD-REVISIONS.json`](../ios-lab/device/BUILD-REVISIONS.json)
and [`native-build-manifest.json`](../ios-lab/pornfetch/native-build-manifest.json).
Keep simulator and device build products separate.

### Qt and PySide

Qt sources are under `device/qt-src/`: qtbase, qtshadertools, qtsvg,
qtdeclarative, qt5compat, and pyside-setup, all at the recorded 6.12.0 revisions.
The snapshot already contains the patched Qt source. If replacing qtbase with
a fresh checkout at its pinned revision, apply
`device/patches/qtbase-ios15.patch` once, before building. Do not reapply it to
the restored source. It includes the older Mach-semaphore implementation with
its upstream license notice.

```sh
cd /Users/asuna/ios-lab/device
sh build-qt-host.sh
sh build-qt-host-modules.sh
sh build-qt-device-base.sh
sh build-qt-modules.sh
PYSIDE_MODULES=Core,Gui,Network,OpenGL,Svg sh build-pyside.sh
sh build-pyside.sh --reuse-build
```

The first PySide pass builds OpenGL before the full Quick bindings so its
generated headers are available. The second uses the default complete subset:
Core, Gui, Network, OpenGL, Svg, Qml, Quick, QuickControls2. The kit is static,
arm64, with deployment target 15.0. Target compilation enables errors for
unguarded newer Apple APIs. Host QML tools are built separately; disabling
`qml_animation` there skips unneeded host Qt Quick libraries.

Confirm `device/wheels/` contains one full matching PySide/shiboken pair before
regenerating the app. The manifest distinguishes the earlier Core-only wheels
from the full application wheels. Their names are the same; their hashes differ.
Locally rebuilt wheel hashes may differ from the archived artifacts.

### Native networking, parsing, cryptography and media

The recipes expect extracted sources at these paths under `pornfetch/native/`:

```text
libffi-3.8.0/
openssl-3.5.9/
cffi-src/cffi-2.1.1/
chompjs-src/chompjs-1.4.1/
selectolax-src/selectolax-1.0.2/
curl-cffi-src/curl_cffi-0.17.0/
cryptography-src/cryptography-50.0.2/
```

The curl device archive is `device/artifacts/libcurl-ios-arm64.tar.gz`
(curl-impersonate 2.3.1, SHA-256
`16a3095fe0b107af2007be22b87c9f594658a04a22ad694abfd460f9bd70743e`).
Its headers and merged static library are restored in `device/native/libcurl-ios/`.
Use that device library, not the simulator library or Apple's system libcurl.

```sh
cd /Users/asuna/ios-lab/device
sh build-libffi.sh
../.venv/bin/python build-native-python.py
sh build-cryptography.sh
../.venv/bin/python build-ffmpeg.py
```

Cryptography uses the isolated Rust toolchain under `ios-lab/toolchains/`, target
`aarch64-apple-ios`, and static OpenSSL. The preserved cryptography source also
restricts its macOS compiler-runtime linkage to apple-darwin targets; retain
that cross-build correction if using a fresh source archive. It is not included
as a separate first-party patch, so the restored source is the baseline.

The device recipe consumes the pure-Python/data overlay in `pornfetch/vendor/`
and replaces its native modules with the device builds. To update the pure
dependency graph deliberately, run `pornfetch/prepare-pure-deps.py` using the
lab venv with uv installed. It resolves current dependencies into a local
`uv.lock` and excludes native/browser-cookie packages. It does not replace the native builds or prepare the QtAsyncio overlay.
Keep the matching package metadata and certificates. For the recorded baseline,
reuse the archived overlay; changing dependencies requires new device validation.

Optional focused probes before the full app:

```sh
cd /Users/asuna/ios-lab/device
sh build-qt-quick-hello.sh
sh deploy-app.sh QtQuickPhoneHello
bash build-native-modules.sh
sh deploy-app.sh NativeModules
```

The native probe performs real HTTPS requests to example.com. These commands
install separate lab apps and do not run automatically during normal builds.

## Intel simulator

This target was verified on an x86_64 Mac, with an iOS 26.3 simulator runtime,
official Qt/PySide 6.12.0 Intel simulator wheels (minimum iOS 18), the same
embedded Python, and separately compiled x86_64 native dependencies. It does not
use the phone's iOS 15 kit or FFmpeg adapter. Apple Silicon simulator builds need
a different wheel/native target and have not been validated.

Restore the snapshot and overlay the maintained scripts as above. If the runtime
is missing, `sh setup-simulator.sh` runs Xcode setup and downloads a universal
iOS runtime; use Xcode to create a simulator if necessary. Select its actual UUID:

```sh
cd /Users/asuna/ios-lab
. ./env.sh
xcrun simctl list devices available
export SIM_ID=YOUR_SIMULATOR_UUID
sh run-native.sh "$SIM_ID"
cd pornfetch
../.venv/bin/python prepare-application.py
bash run-application.sh
```

Preparation uses the restored unpacked official wheel kit at
`qt/deployment/ios_x86_64_simulator/_wheels`, applies the repository's QtAsyncio
patch for embedded Python 3.15, and generates the app project. The launcher
boots the simulator, builds, installs and opens the real app. Use
`bash run-application.sh --launch-only` to reopen an already installed build.
Runtime output is in `ios-lab/build/app-runtime.log` and `.err`.

The VM launcher selects `QT_QUICK_BACKEND=rhi`, `QSG_RHI_BACKEND=opengl` and
`QSG_RENDER_LOOP=basic`. Qt's software adaptation produced a black window in
that VM. These overrides do not belong in the physical-device launcher.

To rebuild the simulator dependencies from the preserved inputs:

```sh
cd /Users/asuna/ios-lab/pornfetch
sh build-libffi.sh
LIBFFI_IOS_PREFIX="$PWD/native/libffi-ios" sh build-small-extensions.sh
../.venv/bin/python build-selectolax.py
../.venv/bin/python build-curl-wrapper.py
sh build-openssl.sh
sh build-cryptography.sh
../.venv/bin/python prepare-pure-deps.py
../.venv/bin/python prepare-probe.py
bash run-probe.sh
../.venv/bin/python prepare-application.py
bash run-application.sh
```

`run-probe.sh` expects the selected simulator to be booted; `run-native.sh`
above establishes that state. The Rust toolchain needs `x86_64-apple-ios`.
`prepare-qt.sh` can regenerate the initial Qt simulator probe using official
wheels, but it is not a bootstrap for the full app's native dependencies.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Missing kit, vendor package, source archive or signing tool | Restore the complete snapshot; a clone only contains first-party sources |
| Generated project uses an obsolete repository path | Export `PORN_FETCH_SOURCE` and rerun preparation without `--stage-only` |
| Python version rejected by project installation | Use the isolated lab environments; do not install the desktop project into embedded Python |
| Newer-iOS symbol or minimum-OS loader failure | Use the patched device Qt kit and arm64/iOS 15 native artifacts, not official iOS 18 wheels |
| Phone UI is black | Check the main executable's GPU entitlement and scene metadata from the finalizer |
| Simulator UUID not found | Select an available device and export its `SIM_ID`; archived CoreSimulator devices are not included |
| Download has `.mp4` name but is unplayable MPEG-TS | Verify `_ios_ffmpeg` is bundled, the base_api patch is applied and remuxing is enabled |

For upstream background, see [Qt for Python's iOS deployment tool](https://doc.qt.io/qtforpython-6/deployment/deployment-pyside6-ios-deploy.html),
[Qt's supported iOS configurations](https://doc.qt.io/qt-6/ios.html), and
[CPython's iOS embedding and extension packaging](https://docs.python.org/3.15/using/ios.html).
The local patches and jailbreak installation steps extend beyond those supported
upstream workflows.
