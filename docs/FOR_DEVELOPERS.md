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

Use the shared notification presenter for messages and decisions. It keeps a
bounded session history and does not stop the event loop. Optional system
notifications are off by default and use generic text. They do not keep mobile
downloads running in the background. Test focus, keyboard navigation, reduced
motion and high contrast when changing controls; see [testing](TESTING.md).

First launch shows the beta notice, `LicenseOfferDialog.qml`, then the personal
message in `UkraineMessageDialog.qml`, followed by error-reporting consent.
The license offer uses `Onboarding/license_offer_seen`, independent of the app
version and preserved when resetting preferences. Both layouts share the dialogs. Its
`Onboarding/ukraine_message_seen` setting is saved when the dialog opens. Keep
this key independent of the release version and preserve it when resetting
preferences, so updates do not repeat the message. Deleting app data also
removes this record. The corner star opens YouTube only when clicked.

Optional error reports use `src/shared/error_reporting.py` for the GUI and CLI.
With explicit consent they send full Python tracebacks, exception chains and
diagnostic context, including failing video URLs and query strings. Reports are
stored privately for debugging. The detailed-report consent version invalidates
older opt-ins; existing opt-outs remain disabled. Keep both consent dialogs and
the CLI disclosure consistent. Local notification redaction is separate from
report contents. The receiver in the adjacent Server project needs its matching
hook, 1 MiB proxy limit and `1793750400_full_error_reports.js` migration deployed
before releasing this client. Reports beyond that request limit are skipped,
never silently truncated.

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
