# Work on Porn Fetch

Start with [source setup](INSTALLATION.md#run-from-source). Use Python 3.15,
PySide6/QML for the GUI, and asyncio for background work. Read `BACKEND.md` and
`CONTEXT.md` before changing the backend. Read `SNI_PROXY_AGENT_HANDOFF.md` before
changing the SNI proxy.

## Code layout

| Folder | Purpose |
| --- | --- |
| `src/backend` | Qt adapters, GUI startup, downloads, settings and notifications |
| `src/frontend/UI` | Desktop and mobile QML |
| `src/cli` | Qt-free interactive and batch CLI |
| `src/shared` | Provider routing, metadata, downloads, paths and network services |
| `src/database` | PocketBase process, REST client, history and GUI bridge |
| `src/licensing` | Shared license verification and storage |
| `src/tests` | Offline tests and opt-in live checks |
| `scripts`, `packaging` | Build helpers and platform templates |

`main.py` and `Porn_Fetch_CLI.py` are launchers. GUI startup lives in
`src/backend/application.py`. Keep CLI, shared code, licensing and
`src/database/core.py` free of Qt imports. Use `base_api` for provider networking
and downloads. Close clients and async iterators when work ends or is cancelled.
Do not add QThread workers or nested GUI event loops.

## GUI changes

Edit QML and Python source, then rebuild resources:

```sh
uv run --no-sync python scripts/translations.py extract
uv run --no-sync python scripts/translations.py build
uv run --no-sync python scripts/compile_qml.py
```

The frontend `update.sh` and `update.ps1` scripts run these steps too.
After async shutdown, `src/backend/qml_lifecycle.py` destroys QML windows before
engine-owned Python adapters. Keep this explicit order: reference cycles can
otherwise leave bindings alive after their context objects disappear.

Do not edit generated `resources.py` or QM files by hand. Draft translation
catalogs are kept for contributors; the released interface stays English.

App icon artwork lives in `src/frontend/graphics/logo_artwork.png`. After changing
it, run `python scripts/generate_app_icons.py` in the GUI environment before
rebuilding resources. Commit the generated square PNGs, multi-size Windows ICO,
macOS ICNS, Android adaptive foreground and opaque iOS asset catalog. Desktop
artwork fills 92% of its square canvas; Android keeps separate padding for its
launcher mask. Windows icon frames must not exceed 256px. The runtime window and
tray share `app_icon.py`, with an additional 1024px PNG for large/high-DPI requests.
The iOS staging script attaches the catalog to Xcode's Resources build phase.

Use the shared notification presenter for messages and decisions. It keeps a
bounded session history and does not stop the event loop. Optional system
notifications are off by default and use generic text. They do not keep mobile
downloads running in the background. Test focus, keyboard navigation, reduced
motion and high contrast when changing controls; see [testing](TESTING.md).

Use the shared `Theme.qml` colors and `AppButton`, `AppTextField`, `AppComboBox`
and `AppSpinBox` controls. Their contrast overrides restore the original style
bindings when disabled. Respect `dark_mode` in high contrast: light contrast uses
black text on white with navy selections, while dark contrast uses white on black
with yellow selections. Selection text uses the matching inverse color. Keep
`ThemeManager`'s native palette aligned with QML and avoid forcing high contrast
into a dark Material theme. Content-language selectors share
`ContentLanguageComboBox.qml`; bundle its flag SVGs and their MIT notice instead
of depending on platform emoji fonts.

Both layouts use `FirstRunSetup.qml` before the main interface. It shows the full
bundled license, requires an unchecked acceptance box, presents the premium offer,
asks for Off/Basic/Full reporting, then shows the Ukraine message. Android also
requires an accessible output folder through the system picker. Cancelling the
picker keeps setup open. The shared content is in `LicenseOfferContent.qml` and
`UkraineMessageContent.qml`; their external links open only when clicked.

Each step saves only when the user explicitly continues. Interrupted setup resumes
the remaining steps. `Onboarding/license_accepted_text`, `license_accepted_sha256`
and `license_accepted_at` record the text, digest and UTC time of acceptance.
`Onboarding/setup_completed`, `license_offer_seen`, `ukraine_message_seen`, reporting
choices and the Android folder survive preference resets and updates. Deleting
application settings removes them. `Backend.start_configured_services()` waits for
completion before starting licensing, history and pending startup update requests.
`--smoke-test` uses temporary settings/cache/licensing storage, skips the wizard,
and starts no async services, so building cannot consume first-use state.

Optional error reports use `src/shared/error_reporting.py` for the GUI and CLI.
Basic mode omits exception messages, URLs, paths and tracebacks. Separately opting
into Full mode adds full Python tracebacks, exception chains and diagnostic context,
including failing video URLs and query strings. Reports remain private and are used
only for debugging; the disclosure explicitly disclaims interest in viewing habits.
GUI settings and `--[no-]error-reporting-full-traceback` can change that scope.
Consent version 2 invalidates older opt-ins; existing v2 detailed opt-ins keep their
previously consented scope and opt-outs remain disabled. Keep the shared disclosure
and both settings interfaces consistent. Local notification redaction is separate.
The receiver in the adjacent Server project needs its matching hook, 1 MiB proxy
limit and `1793750400_full_error_reports.js` migration deployed before release.
Reports beyond that request limit are skipped, never silently truncated.

Failed download rows keep the full Python traceback, exception chain and video
URL in session memory for the user-opened error dialog and its Copy text action,
independently of reporting consent. Anonymous Mode hides and closes this details
view. Activity and system notifications still use redacted summaries.

Startup update checks open the update dialog by default. `Misc/update_prompts`
stores the user's opt-out separately from `Misc/update_checks`; manual checks and
Activity's Review update action still open it. Close Activity before dispatching
an action that opens another dialog. Release notes use selectable `TextArea`
readers with explicit Markdown/HTML formats and clickable links in both layouts.
Keep `TextEdit.NativeRendering`: the old rich-text scene-graph rendering crashed
in Qt 6.12's `QSGBatchRenderer::Renderer::prepareAlphaBatches` on native
Wayland/NVIDIA. Clear the notes and set the format before assigning new content
so Qt does not parse Markdown as HTML while changing formats.

## Downloads and storage

The native provider libraries own media transfers. The GUI and CLI own queue
state and cooperative stop requests. A normal close stops writers, saves queue
snapshots, flushes history and closes network/database services. Reopening restores
paused jobs; resuming fetches fresh provider metadata. Cookies and passwords are
not saved in queue snapshots. Forced-kill and power-loss recovery are outside the
current scope.

Desktop history uses PocketBase. Android history/statistics are disabled. Do not
add another database backend for mobile. Queue checkpoints use the writable cache
folder and are separate from history. Clearing temporary files can destroy saved
progress; active downloads receive a warning with an option to continue anyway.

Installation changes belong to Qt Maintenance Tool. Never copy a running app's
single executable or delete its app-data directory to simulate installation.
Portable and source copies have no installer-managed removal action.

## Networking and Tor

Service routing offers Off, Updates + licensing, and All app traffic. Tor starts
when needed. A Tor failure must fail the request without falling back to a direct
connection. All app traffic includes provider pages and downloads, but not an
external browser or other applications. Loopback PocketBase requests stay local.
It uses remote SOCKS hostname resolution and takes precedence over saved media
proxy, SNI and interface settings. Leaving that mode restores the saved settings.

`src/shared/service_transport.py` routes app services. `tor_transport.py` routes
providers and media. `tor_runtime.py` owns the Tor process, local ports and private
data directory. TLS verification remains enabled. Source runs can set
`PORNFETCH_TOR_BINARY` to an installed Tor executable; the app still starts its own
process. Packaged runtimes come from the verified sources in
`packaging/tor_sources.json`. Updating this requires checking the signed upstream
manifest and hashes. Bridge/pluggable-transport configuration is not included.

## Dependencies and versions

Use `uv sync --upgrade` at setup. CI does the same. `uv.lock` is a generated local
file, not a checked-in release requirement. `--no-sync` keeps a build environment
stable after patching. Dependency audits fail CI on reported vulnerabilities.
GitHub Actions use verified commit references; Dependabot checks them daily.

Native source archives, mobile wheels, Python ABIs, and patched build tools can
need exact versions. Keep each version with its matching checksum and patch.
The preserved iOS native overlay is a separate build input, not a desktop wheel
installation. Update it with its native libraries and test on a phone.

`src/shared/version.py` defines the development version. Release CI stamps the
chosen full version and one workflow timestamp before compiling. Do not use the
user's clock to decide a release date. [Release instructions](RELEASING.md) explain
signatures, update metadata and publication.

Before opening a PR, run the relevant [offline tests](TESTING.md). Do not add real
provider requests, browser-cookie access or downloads to ordinary CI.
