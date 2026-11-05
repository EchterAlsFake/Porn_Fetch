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
- Keyword search is intentionally unavailable in every frontend.
- Android history/statistics are disabled; do not add another database backend.
  Desktop tracking uses PocketBase. Licensing storage is separate.
- Licensing schema 1, Stripe session identifiers and beta compatibility shims
  were removed. Do not restore them.
- The user considers licensing lifecycle testing complete and does not want more
  lifecycle tests. Forced-kill/power-loss recovery is outside the requested scope.
  The user will verify GUI/CLI updates using a GitHub build.
- Preserve existing user work. Keep runtime files, caches and build output out of Git.

## Current behavior

The desktop entry point is `main.py`; its backend is `src/backend/application.py`.
`Porn_Fetch_CLI.py` loads the headless CLI. Mobile uses the shared backend and
`AndroidMain.qml`. The interface is **English-only**. Translation catalogs and
Weblate integration are unfinished; language selectors remain disabled.

First launch shows the €19.99 license offer, then the
Ukraine message and error-reporting consent. `Onboarding/license_offer_seen`
and `Onboarding/ukraine_message_seen` survive preference resets and updates.
The offer opens pornfetch.to for purchase and has a free Continue action.
On mobile, the license offer and Ukraine message fill the window while respecting
system safe areas. Android then asks users without a saved output folder to choose
one through the system picker. Cancelling keeps setup open; an existing selection
skips setup. The picker retains access for future launches. Android packaging must
include QtSvg and its image and icon plugins for the bundled SVG artwork.

Optional error reports now include full Python tracebacks, chained exceptions
and supplied diagnostic context, including video URLs and query strings.
Detailed-report consent version 2 requires older opt-ins to choose again;
existing opt-outs stay disabled. GUI and CLI share the disclosure. The adjacent
Server project's updated hook, proxy limit and PocketBase message-field migration
must be deployed before the client is released. Accepted reports are preserved
verbatim; requests over 1 MiB are skipped instead of truncated.

Qt Installer Framework owns desktop installation, component changes, updates
and removal. Source and portable copies have no in-app installer/uninstaller.
Active-download temporary cleanup asks for confirmation but remains allowed.

Desktop update discovery opens a dialog by default. `Misc/update_prompts` saves
the opt-out independently of startup checks; manual review remains available.
Long release notes use a plain-text reader to avoid the Qt Quick rich-text
renderer crash confirmed on Wayland/NVIDIA. Update payloads use HTTP/1.1 after
reproducing an HTTP/2 reset at 1 MiB; TUF streams resume with validated ranges.
The signed maintenance component is required but not Essential, avoiding IFW's
separate tool-first update/restart. Update launch uses normal async shutdown.

The interactive CLI main menu includes Check for Updates, using the same signed
updater and confirmation as `self-update`. Only a successfully staged update
closes the menu and its session resources so the helper can replace the binary;
declining, failed checks and up-to-date results return to the menu.

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

`scripts/build_desktop.py` is the shared local GUI/CLI builder. It generates
paths from platform templates, keeps the full deployment folder, assembles
helper binaries and legal files, and checks startup. Existing outputs are not
overwritten. Local builds have no publisher signature; macOS uses ad-hoc signing.
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
Windows FFmpeg notice collection reads zlib.h directly from the selected MSYS2
Clang prefix. Do not launch bare pkg-config/cygpath with only a child env PATH:
Windows CreateProcess resolves executable names against the parent's environment.

`scripts/build_output.py` always streams child stdout/stderr to the terminal while
retaining the complete compiler log. Python children use unbuffered output, and
silent steps emit a heartbeat every 60 seconds. Verbose mode adds diagnostics;
FFmpeg and GUI compilation output must remain visible by default.

Ordinary dependency ranges and GitHub actions are updated frequently. Matching
native toolchains and checksummed archives stay pinned until replaced together.
Android uses Qt/PySide 6.12.0 cp315 wheels, target Python 3.15.2 and NDK r28c.
The wrapper regenerates machine paths and patches Qt's preload library names
for Android 13. All four Python 3.15 CI targets built on 2026-11-03; physical
device startup of those artifacts was not established by that build result.

The shared cross-platform CI pipeline includes the iOS GUI, using Python 3.15.2 ARM64 macOS host tools and the published matching
Qt/PySide device inputs. The preserved lab still embeds Python 3.15.0rc2.
Its native dependency archive is required; a public clone alone is insufficient.
iOS 15+ is officially supported with a native GUI. CI produces an IPA for sideloading re-signing and publishes it through the same website/release jobs. The embedded 3.15.0rc2 runtime must be rebuilt together with its native dependencies to change its patch version. The user confirmed license activation,
downloading, remuxing and playback on a non-jailbroken iPhone 7 on 2026-10-30.
That does not validate every later artifact or device. See [iOS](docs/iOS.md).

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
