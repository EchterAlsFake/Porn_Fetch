# iOS toolchain investigation — 2026-10-28

## Latest verified result: Python + PySide + QML visible in Simulator

**The Python/Qt Hello World now builds, signs, installs and displays successfully.** Captured and visually inspected `build/qt-screenshot.png`: “Hello World! Python + PySide6 + QML” on the dark background. Runtime output in `build/qt-runtime.log` reports `HELLO_WORLD_PYSIDE_STARTED`, embedded Python 3.15.0rc2, and `sys.platform == 'ios'`. Xcode reports `BUILD SUCCEEDED` in `build/qt-build.log`.

This session now has full access. Downloads and CoreSimulator commands work; the agent runs simulator operations as the normal user using `sudo -H -u asuna`, rather than creating a root-owned simulator device set. Earlier sandbox observations below are historical.

Reopen the tested app from normal Terminal:

```sh
cd /Users/asuna/ios-lab
./run-qt.sh
```

The example defaults and launch script select `QT_QUICK_BACKEND=rhi`, `QSG_RHI_BACKEND=opengl`, and `QSG_RENDER_LOOP=basic` for the simulator probe. Logs confirm **Apple Software Renderer, OpenGL ES 3.0**. The original `QT_QUICK_BACKEND=software` rendered the scene offscreen but produced a black display because Qt's iOS backing store tried to present it with unavailable Metal. Setting only `QT_WIDGETS_RHI_BACKEND` did not change that path. Use the working OpenGL configuration for this VM; choose the appropriate backend separately for a physical phone.

The installed host deployment environment contains PySide6-Essentials 6.12.0, shiboken6 6.12.0, certifi and tqdm. qtpip 0.2.0 unexpectedly required commercial credentials for this command. Instead, the official public release wheels were downloaded from `download.qt.io/official_releases/QtForPython/`. Their SHA-256 checksums match Qt's published values:

- PySide Intel simulator wheel: `ed778985072fdbbed6b9894f22470cddf59ae29076dee34f077005de65d50e57`
- shiboken Intel simulator wheel: `baff42a0dd79f803fb7219a471a33c892a35da6626338905b625f951bbde5743`

`prepare-qt.sh` has been corrected to use those public files and the smaller Essentials host package. The steps have now been exercised individually; the script as a whole has only been syntax checked. Qt's deployment tool downloaded and verified its pinned Python 3.15.0rc2 framework. The full project's declared Python 3.14 requirement is a separate compatibility issue; this isolated probe does not import the app.

QML is stored in `qt/qml/Main.qml` and included explicitly in `qt/pysidedeploy.spec`, allowing static plugins to be resolved. Generated project: `qt/deployment/ios_x86_64_simulator/HelloPySide.xcodeproj`. Build command:

```sh
. ./env.sh
xcodebuild -project qt/deployment/ios_x86_64_simulator/HelloPySide.xcodeproj \
  -scheme HelloPySide -configuration Debug \
  -destination id=7DFE048D-AB3D-453F-AE58-D474EF4C4569 \
  -derivedDataPath build/qt-derived -jobs 2 build
./run-qt.sh
```

Approximately 4.7 GiB free remains at this stage. The unoptimized simulator app is roughly 756 MiB; payload reduction is deferred. No Qt source was needed for this simulator milestone. The wheel's `qt.toolchain.cmake` explicitly specifies minimum iOS **18**, so this result still cannot be transferred directly to the iPhone 7 running iOS 15.8.8. The jailbreak type/rootless status is still needed before phone deployment planning.

The sections below preserve the initial investigation and intermediate results; this section supersedes their unfinished simulator status.

## Update after runtime installation

The runtime volume `iOS_23D8133` is installed and simulator devices now exist for iOS 26.3. The iPhone 16e UUID is `7DFE048D-AB3D-453F-AE58-D474EF4C4569`. Launch the native probe from normal Terminal with:

```sh
cd /Users/asuna/ios-lab
./run-native.sh 7DFE048D-AB3D-453F-AE58-D474EF4C4569
```

The agent retried simctl after installation; its sandbox still blocks the CoreSimulator connection. This does not demonstrate a failure of the installed runtime. Native launch remains unverified until the normal-user command succeeds.

The project checkout has also advanced to `b38c98e`, with a clean tracked working tree at inspection. Approximately **6.1 GiB** remains free after runtime installation. Reclaim or expand disk space before downloading Qt/Python bundles or attempting source builds. Historical findings below describe the initial inspection unless stated otherwise.

## Result so far

**Compilation works. Simulator execution and Python-on-iOS execution are not yet verified.**

Created this independent lab without editing Porn Fetch. Both native builds succeeded:

| Artifact | Architecture / platform | Verified |
| --- | --- | --- |
| `build/simulator/HelloNative.app` | x86_64 iOS Simulator | Compiles, links, ad-hoc signature validates, plist validates |
| `build/device/HelloNative.app` | arm64 iOS device | Compiles and links; intentionally unsigned |
| `qt/main.py` | Desktop Python/PySide offscreen | QML loads, creates a root window, event loop exits successfully with `--smoke-test` |

Mach-O load commands show **minimum iOS 15.0, SDK 26.2** in both native executables. This demonstrates that the new SDK can build a basic app targeting iOS 15; it says nothing yet about Qt's compatibility or the phone's signing requirements.

The native app is UIKit/Objective-C, not Python or Qt. It isolates Apple's compiler, runtime installation, simulator boot and rendering before introducing Python and Qt.

## Machine findings

- Intel/x86_64 virtual Mac, macOS 15.7.2 (24G325). User reports 16 GB RAM and no GPU acceleration.
- Root filesystem: 64 GiB total, approximately **21 GiB free** at inspection.
- Xcode is `/Users/asuna/Downloads/Xcode.app`, version 26.3, build 17C528. Archive name identifies Release Candidate 2.
- Includes iPhoneOS and iPhoneSimulator SDK 26.2. The SDK supplies headers/libraries to build against. A simulator runtime is the separate installed OS needed to run an app.
- Global `xcode-select -p` points to `/Library/Developer/CommandLineTools`. Lab scripts select the full Xcode locally using `DEVELOPER_DIR`, so no global switch is necessary.
- No runtimes were found in the inspected CoreSimulator runtime/volume locations, and the user's simulator device directory contains no device instances.
- `/usr/local/bin/python3`: 3.13.16. Existing `/Users/asuna/.venv`: Python 3.13.11 and desktop PySide6 6.10.1; no `pyside6-ios-deploy` or qtpip.
- Homebrew, CMake 4.4.4 and Git are installed. No Qt source/iOS kit found in the locations inspected; the existing PySide installation supplies desktop Qt only.
- This is a scoped developer-toolchain audit, not an exhaustive inventory of private files or every installed application.

16 GB is enough to start with small probes. Keep source builds to roughly 2 parallel jobs initially. **Disk space is the more immediate constraint**: runtime downloads and installation need temporary space, and a source build needs considerably more. Aim for at least 40–60 GiB free before a Qt/PySide source build; this is a working estimate, not a measured requirement. Do not delete the Xcode archive until you decide you no longer need it.

Qt Quick's software renderer is selected in the Python probe. This reduces Qt's graphics requirements; it cannot provide graphics acceleration to Apple's Simulator. Whether this VM can boot and display a usable simulator remains an actual experiment. More RAM will not fix missing graphics support or blocked system services.

## Session restrictions

The agent process reports uid 0 but still runs inside a managed execution sandbox:

- Git fetch fails: `Could not resolve host: github.com`.
- pip cannot resolve pypi.org either.
- CoreSimulator XPC connections fail and simctl tries to use root's device set.
- Writes to system temporary/cache locations and sudo execution are restricted.

These observations do not establish that normal macOS Terminal has the same problems. Run simulator commands from Terminal as **asuna**, not as root and not with sudo around the whole script. Web documentation access is available separately to the agent and does not unblock shell downloads.

## First actions in normal Terminal

Open Terminal with Command-Space, type `Terminal`, press Return. Paste these commands:

```sh
cd /Users/asuna/ios-lab
./update-source.sh
./setup-simulator.sh
```

`update-source.sh` fetches GitHub and then resets tracked files to `origin/master`, as authorized. It does not push and does not erase untracked downloads/configuration. Fetch must succeed before the reset. Current inspected checkout is `1dad7e2`; it has a modified tracked `src/frontend/UI/resources.py`. The agent's fetch failed, so that edit has not been discarded and the source has **not** been updated. Re-read repository instructions and dependency requirements after updating; the application findings below describe this older checkout.

`setup-simulator.sh` uses the current Xcode location, completes first-launch setup, and downloads the **universal iOS runtime** including Intel support. It may request your Mac login password through sudo for first-launch setup; Terminal does not show password characters. It can take a long time and consume many GB. If disk space is low, enlarge the VM's disk first. If Xcode reports a license/setup requirement, open `Downloads/Xcode.app` in Finder and complete the displayed setup.

The script lists available simulator devices. If none exist after runtime installation, open Xcode's Simulator app and choose **File → New Simulator**, selecting an installed iOS runtime and an available iPhone model. It need not emulate an iPhone 7; simulator model and deployment target are different things.

Then:

```sh
./run-native.sh
./run-native.sh PASTE-A-SIMULATOR-UUID-HERE
```

The first command lists devices. Replace the placeholder in the second command with the UUID shown beside one of them. The script boots it, installs and launches the native Hello World, and saves `build/native-screenshot.png`. A successful compile alone is not a successful launch. The screenshot may catch the launch transition; confirm the text in Simulator itself.

No Apple developer membership is required for this simulator test. Keep Xcode in its present location for now; `env.sh` also recognizes `/Applications/Xcode.app` if you move it later.

## Python and Qt simulator step

Once native Hello World is visible, run:

```sh
cd /Users/asuna/ios-lab
./prepare-qt.sh
```

This prepared script has passed shell syntax checking but **has not been executed against the network**. It creates a separate virtual environment, installs pinned 6.12.0 desktop deployment tools, downloads Intel simulator wheels using qtpip, checks for one matching PySide/shiboken pair, and generates/opens a `HelloPySide.xcodeproj` under `qt/deployment/`. The deployment tool obtains the embedded Python framework. If packages or matching wheels are unavailable or qtpip requests credentials, preserve its output so we can resolve that exact problem; do not substitute desktop wheels for iOS wheels. Review qtpip's available version options if its default downloads a newer release.

In the opened Xcode project, select **HelloPySide**, select the same iPhone simulator as the destination near the top of the window, then click the triangular Run button (Command-R). This is the first test that actually proves Python + PySide + QML on iOS. The existing Python 3.13 host can run the deployment tools; Python embedded inside the app is separate. The full app's Python 3.14 requirement must be checked against the embedded framework before porting it.

Reference: [Qt iOS deployment tool](https://doc.qt.io/qtforpython-6/deployment/deployment-pyside6-ios-deploy.html), [Qt 6.12 release](https://www.qt.io/blog/qt-for-python-release-6.12-is-here), [Intel/universal simulator setup](https://doc.qt.io/qt-6/ios.html).

## iPhone 7 on iOS 15.8.8

This phone is arm64. A simulator binary cannot be installed on it even if the simulated UI works. Its jailbreak type and rootless/rootful arrangement are still unknown; these determine packaging, signing and installation details later.

Current Qt 6.12 documents **iOS 18+** support. A jailbreak does not supply the newer UIKit/system APIs that such binaries may expect. Lowering the minimum version in a plist is insufficient. See [Qt platform requirements](https://doc.qt.io/qt-6/ios.html). Xcode 26.3 itself supports iOS 15 deployment, so Xcode is not the same compatibility obstacle: [Apple requirements](https://developer.apple.com/xcode/system-requirements).

The phone route is a separate feasibility investigation: find a maintained Qt branch compatible with iOS 15 and determine whether current PySide iOS support can be backported to it, or whether current Qt can be patched and rebuilt to operate correctly on iOS 15. Matching Qt/PySide versions and static iOS initialization matter. Neither path is proven or promised. Older Qt compatibility tables alone do not establish a viable maintained PySide build. We should avoid installing arbitrary old Qt versions or large source trees before selecting this strategy.

The native arm64 build gives us a very small test app when we reach the phone stage. It still needs appropriate signing and installation; no phone has been contacted or modified.

## Full app port: findings from the currently checked-out source

| Component | Work to investigate |
| --- | --- |
| Python | `pyproject.toml` requires >=3.14,<3.15. Installed 3.13 cannot satisfy the complete project as declared. Recheck after updating. |
| PySide/QML | GUI uses Qt Quick, Controls and other plugins, plus QtAsyncio. Need correct static plugin/QML inclusion and asynchronous networking checks. Desktop wheels are unusable on iOS. |
| curl-cffi | Core networking dependency through eaf_base_api. Need an iOS build of its CFFI binding and curl-impersonate dependency chain for each target. Apple's system libcurl is not a replacement for browser fingerprinting. First test a minimal import and HTTPS request separately. |
| selectolax | Native extension/parser: cross-build for the same embedded Python, architecture and iOS target, then validate parsing independently. Inspect the updated upstream package graph before writing recipes. |
| FFmpeg/PyAV | Current source uses optional PyAV imports; inspect the full backend before disabling features. Cross-build FFmpeg libraries plus PyAV if those features are required. Prefer linked libraries for the normal iOS app path; do not assume spawning an ffmpeg executable will work. |
| cryptography | Additional native/Rust dependency; needs compatible iOS packaging. |
| Browser cookies | Desktop browser-cookie extraction assumptions do not transfer to iOS app storage. Need an explicit supported account/cookie workflow. |
| PocketBase | Existing desktop service starts a child executable. Disable unsupported desktop tracking or deliberately redesign it; do not accidentally start it on iOS. |
| Platform checks | Several branches recognize Android only; embedded CPython reports `sys.platform == 'ios'`. Add explicit iOS handling for paths, desktop services, dialogs and updater behavior. |
| App files/data | Use app-writable locations, bundle resources and metadata deliberately; do not assume desktop paths or pip installation at runtime. |

CPython's standard iOS build embeds inside an app and does not support subprocesses. A jailbreak may enable alternative arrangements, but that requires separate proof and may require a different Python build. See [Python on iOS](https://docs.python.org/3.14/using/ios.html) and [mobile platform limitations](https://docs.python.org/3.14/library/intro.html#mobile-platforms). [curl-cffi upstream](https://github.com/lexiforest/curl_cffi) documents its impersonation features and desktop installation targets.

Proceed in this order: native simulator launch → Python/Qt simulator launch → iOS 15-compatible Qt/PySide feasibility → tiny Qt app on the phone → native dependencies individually → full application. Simulator success is useful evidence, but does not resolve the iOS 15 compatibility problem.
