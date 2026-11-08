# Repository context

Read this file with `BACKEND.md`. For SNI proxy work, also read
`docs/SNI_PROXY_AGENT_HANDOFF.md` before changing code.

## Project and boundaries

Porn Fetch 3.9 uses Python 3.15, PySide6/QML for its GUI and Questionary/Rich for
its CLI. Provider networking uses asynchronous `eaf_base_api` and `curl_cffi`.
Read [the developer guide](docs/FOR_DEVELOPERS.md) for the source map.

- Keep `src/cli`, `src/shared`, `src/licensing` and `src/database/core.py` free of
  PySide6 imports. Qt adapters belong in `src/backend` or a named bridge module.
- Use asyncio and cooperative cancellation, never QThread workers.
- User-facing copy about the author uses I/my, never we/our, "the operator" or
  "the developer". Use standard punctuation instead of em/en dashes in app copy.
- Keyword search is intentionally unavailable in every frontend.
- Android history/statistics are disabled; do not add another database backend.
  Desktop tracking uses PocketBase. Licensing storage is separate.
- Licensing schema 1, Stripe session identifiers and beta compatibility shims
  were removed. Do not restore them.
- The user considers licensing lifecycle testing complete and does not want more
  lifecycle tests. Forced-kill/power-loss recovery is outside the requested scope.
  The user will verify GUI/CLI updates using a GitHub build.
- Preserve existing user work. Keep runtime files, caches and build output out of Git.
- The user specifically reviewed retained application code and translations and
  confirmed that earlier contributions needing additional relicensing permission
  were removed. Treat that ownership review as established for this release;
  third-party components still retain their licenses. Private license sharing is
  allowed with individual family members and real-life personal friends met in
  person, with ten active installations total. Community/server membership alone
  is not friendship for this permission. LICENSE section 6 now preserves mandatory
  rights only; its optional termination/cure-period wording was removed.

## Current behavior

The desktop entry point is `main.py`; its backend is `src/backend/application.py`.
`Porn_Fetch_CLI.py` loads the headless CLI. Mobile uses the shared backend and
`AndroidMain.qml`. The interface is **English-only**. Translation catalogs and
Weblate integration are unfinished; language selectors remain disabled.

First use runs `FirstRunSetup.qml` before showing the main interface in either
layout. It presents the full application license with an unchecked acceptance
box, the €29.99 lifetime Premium offer, Off/Basic/Full error-reporting choices, the Ukraine message,
and an Android output-folder step. Only explicit Continue actions save completed
steps; reopening an interrupted setup resumes outstanding steps. Acceptance saves
the actual displayed license, its SHA-256 and a UTC timestamp. The completion,
acceptance, offer/message acknowledgements, reporting choice and Android folder
survive preference resets and updates; deleting application settings removes them.
Licensing, history and startup update requests wait until setup finishes.
The shared surface scrolls on small screens and respects mobile safe areas.
A small sparkle button in the upper-right corner of the Ukraine setup step
opens the music-video Easter egg only when clicked. Its tooltip says "Curious?"
without revealing the destination. The flag is decorative.
Android requires a shared output folder: private app files are inaccessible to
ordinary players/file managers. The system picker retains access for future
launches. Cancelling keeps setup open. Android packaging must include QtSvg and
its image and icon plugins for the bundled SVG artwork.
Android requirements must include PyJWT: licensing imports `jwt` during startup.
The APK checker inspects `libpybundle.so` for that package as well as checking
native libraries, so a successful native-library check cannot hide its omission.
On 2026-11-08, the installed 3.8.3 ARM64 APK on an Android 16 phone reproduced
`ModuleNotFoundError: jwt`. A temporary side-by-side copy with PyJWT 2.15.1 added
to its Python runtime bundle reached the first-use screen and stayed running.
That verifies this startup fix on the device, not a rebuilt official APK or other
ABIs. The original app's data and first-use choices were preserved.

Build `--smoke-test` startup uses a temporary QSettings file, download cache and
licensing directory, plus disposable logs. It keeps the launch working directory
so macOS CI can check startup from `/`. It skips setup and starts no async services;
it must never consume the user's first-use choices or touch their existing download
checkpoints.

Optional reports stay disabled until explicitly enabled. Basic reports exclude
exception messages, URLs, local paths and tracebacks. A separate Full choice adds
complete Python tracebacks, exception chains and supplied diagnostic context,
including video URLs and query strings. Both modes use the shared private-report
and debugging-only disclosure. GUI settings and CLI flags can change the scope.
Detailed-report consent version 2 still invalidates older opt-ins; existing v2
full-report opt-ins retain their previously consented scope, and opt-outs remain
disabled. The adjacent Server project's updated hook, proxy limit and PocketBase
message-field migration must be deployed before the client is released. Accepted
reports are preserved verbatim; requests over 1 MiB are skipped, never truncated.

Qt Installer Framework owns desktop installation, component changes, updates
and removal. Source and portable copies have no in-app installer/uninstaller.
Active-download temporary cleanup asks for confirmation but remains allowed.
In-app updates and component management download the complete signed repository
through the app's service transport, including its managed Tor/onion route.
IFW receives only that verified local repository and `--no-proxy`. Component
management accepts the current release but rejects older repositories. Uninstall
uses an empty local repository and needs no network connection.
The interactive CLI shares one PocketBase tracker between downloads and history
inspection. Close it before changing database configuration or disabling tracking;
starting a second service on the same database resets its shared credentials.

Desktop update discovery opens a dialog by default. `Misc/update_prompts` saves
the opt-out independently of startup checks; manual review remains available.
Release notes use selectable TextArea readers with explicit Markdown/HTML formats
and native glyph rendering. The previous Qt Quick rich-text renderer crashed on
Wayland/NVIDIA; keep the native rendering setting for long notes. Update payloads use HTTP/1.1 after
reproducing an HTTP/2 reset at 1 MiB; TUF streams resume with validated ranges.
The signed maintenance component is required but not Essential, avoiding IFW's
separate tool-first update/restart. Update launch uses normal async shutdown.

The interactive CLI main menu includes Check for Updates, using the same signed
updater and confirmation as `self-update`. Only a successfully staged update
closes the menu and its session resources so the helper can replace the binary;
declining, failed checks and up-to-date results return to the menu.

Android and iOS check for updates at startup after first-use setup, respecting
`Misc/update_checks` and the independent dialog opt-out. Mobile Settings exposes
both preferences and a manual check. Android keeps its signed APK installer flow.
iOS discovers published ARM64 IPAs from the website release catalog and offers
the iOS download page for manual sideloading; it never installs updates in-app.

Failed download details keep full Python tracebacks, causes and video URLs in
session memory, independently of report consent. Activity summaries remain
redacted, and Anonymous Mode hides and closes the detailed-error dialog.

`eaf-base-api>=4.2.6` makes FFmpeg remux/tagging subprocesses noninteractive with
explicit null input and captured output. This removes dependence on Windows
console handles when launching from Explorer or Start Menu. Version 4.2.6 is
published on PyPI and GitHub, with a verified fresh PyPI installation.

GUI feedback uses `notifications.py` and `NotificationPanel.qml`: asynchronous
session-only Recent activity and queued decisions. Desktop activity is in the
navigation row; mobile activity is under More. There is no top notification banner. Optional system
notifications are disabled by default and use generic text. They do not enable
background downloads. Mobile copies completed files to the selected output
folder automatically; there is no per-video Save action. Native notification
and assistive-technology checks require devices.

High contrast respects the selected light/dark mode. `Theme.qml` defines the
shared colors; `AppButton`, `AppTextField`, `AppComboBox` and `AppSpinBox` add
contrast rendering while retaining normal style bindings when disabled. Dark
contrast uses black/white with yellow selections; light contrast uses white/black
with navy selections. `ThemeManager` synchronizes the application palette and
native color scheme. Content-language flags are bundled SVG images from
flag-icons (MIT), rather than font-dependent emoji, in both layouts.

Theme controls group high contrast and reduced motion with the light/dark toggle.
Light mode has a saved 75–100% brightness slider that softens backgrounds in both
layouts and the native palette. High contrast keeps its full black/white colors
and disables that slider. XHamster credential login asks for an email address;
both forms flag usernames before submission and the login adapter validates them
before calling the provider.

`DownloadManagerPage.qml` shows an in-memory list of downloads started during the
current session in both layouts. Queue progress/status updates populate small
snapshots without retaining provider objects. Completed, stopped and failed entries
survive queue-row removal; retries update the same entry until it leaves the queue.
This session list resets on exit and does not use desktop or mobile database history.

App icons are generated from `graphics/logo_artwork.png` using
`scripts/generate_app_icons.py`: square desktop PNGs with reduced padding,
multi-size Windows ICO and macOS ICNS, a separate Android adaptive foreground,
and an opaque iOS asset catalog attached during staging. Runtime window/tray
icons share the native small sizes plus a high-resolution PNG. Linux uses the
installed `pornfetch.desktop` identity for launcher matching.

Graceful shutdown stops downloads cooperatively, saves paused queue snapshots
and flushes history before closing services. Recovery metadata uses the writable
Qt generic cache/PornFetch directory. It never serializes cookies, passwords or
native provider objects; resume fetches a fresh object. After async shutdown,
`qml_lifecycle.destroy_qml_engine` explicitly destroys QML roots before the engine
and its context adapters. Do not rely on Python garbage collection for this order. Temporary cleanup can
remove checkpoints. Old orphan temporary files are not automatically migrated.

Premium licensing is lifetime: EUR 29.99 once, with all future Porn Fetch updates
and features released included and no guaranteed duration of future development.
Signed keys require policy duration and license expiry to be null; signed machine
permits retain a seven-day freshness deadline. There is no release-date cutoff.
Activation, three-day initial outage grace and periodic validation remain. If I
permanently close licensing, provide an offline unlock before closure. The bundled
public policy ID remains `7038281b-2429-4aa4-81db-4f04a87e7184`. The server's
permanent model is deployed with `commercialModel=pornfetch-permanent-v1` and
`priceEur=29.99`. Fresh TEST-license activation, repeated validation and future-build
entitlement have been verified against the server. Existing beta records were left
alone, and renewal checkout requests are rejected. Distributed binaries still need
an updated build; do not change the account, product, public key or endpoint.

Emergency licensing is implemented at `https://echteralsfake.me/api/pornfetch-emergency/v1/permit`
on the independent Acer host `asuna@192.168.178.200`. Issuance is disabled by default,
after every restart, and after deployment. Enable manually only during a real primary
outage with `sudo pornfetch-emergencyctl enable`; `disable` stops new permits. Any
valid signed production lifetime key qualifies, including new installations, with
no revocation or installation-count enforcement. Separate signed seven-day permits
never extend locally; primary validation/rejection takes precedence. The signing
key is TPM-sealed on Acer; only its public key ships. Fallback requests require Tor
Off, with an explicit notice and no automatic direct connection. See
[the emergency runbook](deploy/emergency/README.md). Existing distributed clients
need a new build. The origins share the documented VPS edge, so this does not
cover shared-edge failure.
Reimporting a deactivated license during an outage reports `reactivation_required`:
a fresh primary or emergency permit is required, and reimport does not reset grace.
The license widget displays the actual failure reason without generic clock advice.
Desktop, mobile and CLI show the signed permit expiry separately from the next
online check/retry. A failed refresh may reschedule retries but never extends expiry.

Premium feature limits are shared in `src/shared/access.py`. Free use allows
up to 720p, one active download, and the first five videos of public model,
channel and playlist URLs. Apply that preview before filters and index ranges.
Account collections remain exempt. Check parallel limits at the backend and
queue, not only in QML. Existing public-collection queue rows beyond index five
also require premium access.

## Dependencies and builds

Use `uv sync --upgrade` with the needed extras to resolve current compatible
packages, then `uv run --no-sync` to keep that environment through the build.
`uv.lock` and root `pysidedeploy.spec` are generated locally and ignored.
After refreshing GUI dependencies, apply and verify `scripts/patch_qtasyncio.py`.
The checkout and desktop convenience installers explicitly select Python 3.15.2,
matching CI. Installing a newer interpreter alone can leave an old alpha-backed
`.venv` selected; pass `--python 3.15.2` to sync. Early 3.15 alphas cannot load
current `curl_cffi` abi3t extensions. The desktop builder checks for a stable
interpreter and imports `curl_cffi` before helper downloads or compilation.
If uv cannot install the selected Python, the installers update uv's bundled
Python download catalog with `uv self update` and retry once.

`scripts/build_desktop.py` is the shared local GUI/CLI builder. It generates
paths from platform templates, keeps the full deployment folder, assembles
helper binaries and legal files, and checks startup. Existing outputs are not
overwritten. Local builds have no publisher signature; macOS uses ad-hoc signing.
Local macOS builds put `LEGAL/` and `LEGAL.zip` directly in `Contents/Resources`.
License inventories have dotted distribution directories such as `boolean.py`;
leaving those directories under `Contents/MacOS` makes codesign treat them as
malformed nested bundles, even after individual files are relocated.
The shared macOS repair stage relinks Homebrew OpenSSL to the bundled unversioned
copies, separately from Python's OpenSSL, and copies missing native dependencies
such as liblz4 into `Contents/Frameworks`. Each architecture and the merged
Universal bundle reject absolute non-system library dependencies before release;
startup on a runner with Homebrew installed is insufficient verification.
macOS GUI/CLI CI and the local convenience installer explicitly install Homebrew
LZ4 before Python dependencies. CI checks its versioned dylib before compilation;
the runner's default software list does not guarantee that library exists.
Resolve Homebrew source symlinks before Mach-O detection, preserving the recorded
ABI basename inside the bundle. `is_macho` skips symlinks during bundle traversal;
using it directly on a Homebrew dylib alias incorrectly reports a missing library.
See [installation](docs/INSTALLATION.md) and [release operations](docs/RELEASING.md).

The Windows convenience script runs the uv installer in a child PowerShell so
upstream `exit` calls cannot close an `irm ... | iex` caller. It saves a transcript
under the temporary `porn-fetch-build-logs` folder, prints failure details and
pauses on interactive failures unless `-NoPause` is set.
Missing Git is installed with winget's exact `Git.Git` package before cloning or
building. Refresh the process PATH from registered machine/user values so a
successful installation can be used immediately; existing Git is kept.
For bundled FFmpeg, it installs missing MSYS2 through winget, runs core/system
updates in separate pacman processes, and installs make/diffutils/pkgconf plus
the Clang toolchain and zlib for the actual Python architecture. CLANG64 and
CLANGARM64 match the native FFmpeg builder. `-WithoutFFmpeg` skips this setup.
Before syncing Python dependencies, vswhere checks for a modern Microsoft C++
compiler and Windows SDK for the selected Python architecture. Missing tools are
installed with Visual Studio 2022 Build Tools; incomplete Build Tools installs
are modified to add the C++ workload. Report required reboots without forcing one.
Fresh Windows installer checkouts go under the user's profile, not the calling
directory (administrator PowerShell often starts in System32). Application and
provider debug log files go under shared user data/logs on Windows and macOS, so
logging cannot require write access to a protected application/working folder.
Windows FFmpeg notice collection reads zlib.h directly from the selected MSYS2
Clang prefix. Do not launch bare pkg-config/cygpath with only a child env PATH:
Windows CreateProcess resolves executable names against the parent's environment.

All build scripts must always show full output, including dependency installation,
compiler output and build/patch diagnostics. Do not reintroduce quiet defaults or
require a verbosity flag. Shell wrappers stream stdout/stderr while retaining logs;
`scripts/build_output.py` does the same for compiler commands. Python children use
unbuffered output, and silent compiler steps emit a heartbeat every 60 seconds.
The Unix installer never runs a full Linux system upgrade: Arch uses only
`pacman -S --needed`, without a database refresh. Homebrew dependency installation
disables automatic updates and upgrades of already-installed formulae.
Interactive desktop GUI compilation also passes `--terminal` to the wrapper.
`build_terminal.py` uses Windows ConPTY (pywinpty, desktop-build only) or a Unix
pseudo-terminal to preserve Nuitka's own TTY-detected progress bars and raw log
control codes. Noninteractive output keeps the normal streaming path. Linking
has no Nuitka percentage information; retain the silent-stage heartbeat.

Ordinary dependency ranges and GitHub actions are updated frequently. Matching
native toolchains and checksummed archives stay pinned until replaced together.
Android uses Qt/PySide 6.12.0 cp315 wheels, target Python 3.15.2 and NDK r28c.
Android CI installs Ubuntu's Ant package and sets `android.ant_path` to
`/usr/share/ant`, avoiding Buildozer's legacy Ant 1.9.4 archive download.
The wrapper regenerates machine paths and patches Qt's preload library names
for Android 13. All four Python 3.15 CI targets built on 2026-11-03; physical
device startup of those artifacts was not established by that build result.
The Android deployment patch preserves configured Qt modules through PySide's
base initializer, and its template explicitly copies the SVG image/icon plugins
into the APK's native library folder. macOS packaging excludes the iOS source
asset catalog, which codesign rejects inside `Contents/MacOS`.

The shared cross-platform CI pipeline includes the iOS GUI, using Python 3.15.2 ARM64 macOS host tools and the published matching
Qt/PySide device inputs. The preserved lab still embeds Python 3.15.0rc2.
Its native dependency archive is required; a public clone alone is insufficient.
iOS 15+ is officially supported with a native GUI. CI produces an IPA for sideloading re-signing and publishes it through the same website/release jobs. The embedded 3.15.0rc2 runtime must be rebuilt together with its native dependencies to change its patch version. The user confirmed license activation,
downloading, remuxing and playback on a non-jailbroken iPhone 7 on 2026-10-30.
That does not validate every later artifact or device. See [iOS](docs/iOS.md).
The iOS legal preparation verifies the restored FFmpeg extension and upstream
source archive against their recorded hashes before staging the source, bridge,
configuration and rebuild/replacement instructions. Pass that native legal folder
explicitly to the collector; Python metadata discovery does not cover it.

Windows ARM64 GUI preparation applies the source-checked Nuitka 4.3.4 PE scanner
patch in `scripts/patch_nuitka.py`, reading only import tables and caching names
for unchanged files. Review it if a Nuitka update changes that function. GUI CI
persists Nuitka dependency/compiler caches by build environment; ARM64 Windows
jobs reuse vcpkg's ABI-validated OpenSSL packages. Windows FFmpeg caches keep the
unsigned executable with complete legal/source files separately from signing
staging, and verify hashes, LGPL configuration/license and remuxing before reuse.

## Testing and documentation

```sh
uv sync --upgrade --extra gui --group dev
uv run --no-sync python scripts/patch_qtasyncio.py .venv
uv run --no-sync python -m unittest discover -s src/tests/unit
uv run --no-sync python -m unittest discover -s src/tests/integration
uv run --no-sync python src/tests/helper.py
```

Live provider, download, browser-cookie and password tests are opt-in. Never
silently add them to ordinary CI. Fixtures remain in `docs/url-routing-audit/`.
See [testing](docs/TESTING.md) for runners, isolated state and native checks.
After UI text changes, run `scripts/translations.py extract`, `check`, then
`build`; the frontend update scripts also compile QML.

Use [docs/README.md](docs/README.md) as the guide index. Old task reports were
consolidated into the maintained guides; Git history retains the originals.
Release readiness belongs at <https://pornfetch.to/checklist>, not a new local
status document. Release notes are `CHANGELOG_STATIC.md`; older notes are in
`docs/CHANGELOG.md`. Source tests do not establish payment-server readiness.
