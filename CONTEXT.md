# Repository context for AI agents

This file is maintained as a concise map of the current development tree. Read it together with `BACKEND.md`. For any SNI proxy work, also read `SNI_PROXY_AGENT_HANDOFF.md` in full before changing code.

## Project

- Name: Porn Fetch
- Current source version: 3.9
- Current release notes: root `CHANGELOG_STATIC.md`; full history: `docs/CHANGELOG.md`.
- Manual builds take a full `release_version` in the workflow; CI stamps that version
  and one workflow timestamp into all binaries and release metadata.
- Python: 3.14 (the repository default)
- GUI: PySide6 / Qt 6 with QML
- CLI: Questionary and Rich, with no Qt dependency
- Networking: asynchronous `curl-cffi` through `eaf_base_api`
- Package manager and runner: `uv`

> [!CAUTION]
> The latest published binary release is massively outdated. The current source, documentation, screenshots, settings, and workflows describe the in-development 3.9 application and may not match the published 3.8 release.

## Architectural rules

- Keep `src/cli`, `src/shared`, `src/licensing`, and `src/database/core.py` free of PySide6 imports. The CLI must run on headless systems such as Termux.
- GUI adapters belong in `src/backend` or an explicitly named adapter module such as `src/database/bridge.py`.
- Android GUI download tracking and statistics are disabled; do not add a second database backend. Desktop tracking uses PocketBase. Licensing storage is separate.
- Prefer asyncio tasks and cooperative cancellation. Do not introduce QThread-based worker logic.
- Keyword search is intentionally unavailable for legal reasons in every frontend. Do not expose upstream search APIs.
- Schema-1 licensing, Stripe checkout/session identifiers, and their compatibility shims have been removed. Do not restore them.
- Keep generated or runtime data out of Git: databases, logs, downloads, caches, packet captures, and temporary build output are ignored.
- Keep implementation straightforward. Add a new abstraction only when it gives a clear boundary or removes real duplication.
- The user considers licensing lifecycle already tested and does not want more lifecycle tests. Abrupt interruption/forced-kill recovery is outside application scope. The user will verify CLI/GUI updates using a GitHub build.

## Entry points

- `main.py` is a small compatibility launcher for the desktop GUI. The implementation is in `src/backend/application.py`.
- `Porn_Fetch_CLI.py` is the headless CLI launcher. It imports only the Qt-free CLI stack.
- `src/tests/helper.py` is the interactive Questionary test selector.

## Source layout

### `src/backend/`

Desktop application logic and Qt-facing adapters:

- `application.py`: GUI composition root and QML-facing backend.
- `video_processor.py`: asynchronous iterator preparation and filtering for the GUI.
- `config.py`: QSettings-backed GUI configuration.
- `clients.py`: provider-client lifecycle and runtime networking configuration.
- `download_manager.py`: QML download list/model integration.
- `license_bridge.py`: Qt adapter for schema-2 licensing.
- `sni_*.py` and `tls_client_hello.py`: SNI proxy implementation; see the dedicated handoff first.
- `installation.py`, `uninstallation.py`, `update_service.py`: desktop platform services.

### `src/frontend/`

QML, images, translations, screenshots, and the Qt resource manifest. Run `src/frontend/update.sh` or `update.ps1` after changing resources or translatable UI text.

### `src/cli/`

Qt-free terminal interface:

- `wizard.py`: small interactive menu/composition root and compatibility façade.
- `flows/`: focused download, model, account, settings, licensing, statistics,
  rendering, and session-lifecycle workflows.
- `batch.py`: non-interactive arguments and the CLI entry function.
- `providers.py`: provider URL routing and client pool.
- `downloads.py`: asynchronous downloads and resume state.
- `settings.py`, `model_store.py`, `tracker.py`: local configuration and persistence.
- `selftest/`: separated offline, online-provider, and active-download diagnostics.

### `src/shared/`

Qt-free models and services shared by desktop and CLI: media models, metadata,
provider routing/discovery, account-session helpers, value parsing, errors,
error reporting, application paths, and the
shared version constant.

### `src/database/`

- `client.py`: small asynchronous PocketBase REST client.
- `service.py`: PocketBase executable discovery and child-process lifecycle.
- `tracker.py`: download persistence, caching, and statistics orchestration.
- `legacy.py`: read-only migration helpers for the former SQLite database.
- `core.py`: backwards-compatible exports for existing callers.
- `bridge.py`: QObject adapter used only by the desktop GUI.

### `src/licensing/`

Schema-2 license client, shared service, and production public configuration. It is shared by both frontends and must stay Qt-free.

### `src/tests/`

- `unit/`: deterministic, normally offline tests.
- `integration/`: Qt and cross-service integration tests.
- `smoke/`: explicit smoke scripts, some using the network.
- `manual/`: SNI lab instructions and isolated support tooling.
- `helper.py`: interactive suite selector with explicit online/download confirmations.

Live GUI profile checks use `src/backend/profile_diagnostics.py` and the JSON
inventory at `docs/url-routing-audit/profile-fixtures.json`. Run them explicitly
with `uv run python -m src.tests.smoke.profile_urls --include-variants`, or use
`main.py --test-profiles`. They prepare real list rows and resolve playlists,
while blocking media downloads. See `docs/URL_TEST_FIXTURES.md` for coverage and
public User-feed limitations.

## Repository support directories

- `docs/`: user/developer docs, release history, and project history.
- `packaging/`: PyInstaller and PySide/Nuitka build specifications.
- `scripts/`: install, maintenance, QtAsyncio, and macOS bundle scripts.
- `.github/workflows/`: offline CI and platform build pipelines.
- Android CI: `build_all.yml` builds all four ABIs using the existing patch/build
  scripts and Python 3.14 wheels. See `docs/ANDROID_CI.md` for signing secrets,
  Android-only runs and website publication.
- Tor: app-owned service routing and runtime are in `src/shared/service_transport.py`
  and `tor_runtime.py`; `tor_transport.py` routes provider pages and downloads for
  the optional All app traffic scope. See `docs/TOR_SUPPORT.md`. Android updates use the separate
  website-hosted TUF feed and a native user-confirmed installer bridge.

## Common commands

```bash
uv sync --extra gui --group dev
uv run Porn_Fetch_CLI.py
uv run main.py
uv run src/tests/helper.py
uv run python -m unittest discover -s src/tests/unit -p "test_*.py"
uv run python -m unittest discover -s src/tests/integration -p "test_*.py"
```

Online provider tests and active-download tests are opt-in through the helper. They must not be silently added to normal CI.
Live HLS/RAW pause/resume and cleanup checks cover all 15 providers (30 workflows), explicitly with
`uv run python -m src.tests.smoke.download_lifecycle` or through the helper.
Use `--list` for a no-network inventory, and repeat `--provider` for focused runs.
See `docs/LIVE_DOWNLOAD_TESTS.md`; these use real media and isolated CLI state.

Live desktop download controls use `uv run python -m src.tests.smoke.download_gui`
or the helper's **Live desktop download controls** selection. 42 automated workflows
cover 14 providers; SpankBang's three cases are explicitly manual and never make
automated requests, even when selected alone. YouPorn records its actual HLS/RAW
selection. Checks cover actual QML mouse/keyboard actions, quality selection,
Download Selected/per-row start, live progress, pause/resume reuse, cleanup/restart,
pending/active removal, completion auto-clearing, and FFmpeg validation. Native
clients/media and all files/settings are isolated; no cookies or tracking are used.
See `docs/LIVE_DESKTOP_DOWNLOAD_TESTS.md`. Android device checks are deferred to v4.0.
GUI HLS configuration retains partial segments only on a non-cleanup stop, releases
them on completion, and recognizes native `failed` reports as retryable failures.
Live multi-video queue checks use `uv run python -m src.tests.smoke.download_queue`
or the helper's **Live desktop queue and concurrency** selection. Four real HLS/RAW
rows exercise parallel limits 1/2, selection, duplicate starts, queued cancellation,
active stop/removal isolation, numbering and real output validation. Native calls
and HTTP requests are observed, not simulated; files/settings are isolated.
See `docs/LIVE_QUEUE_TESTS.md`. Stopping a queued task cancels its semaphore wait
immediately, including cancellation before the coroutine first runs; active writers
still stop cooperatively.

Desktop settings checks use `uv run python -m src.tests.smoke.settings_gui` or
the helper's **Complete desktop settings** entry. All 55 settings are changed
through production QML, independently read from disk, reloaded, and checked
against the real runtime consumers (all 15 provider cores where applicable).
Observable effects use real HTTP/TLS requests, public profiles/playlists, HLS/RAW
media, FFmpeg, Qt styles and isolated PocketBase databases. Controlled faults use
real loopback servers rather than mocked responses. Tor and Strict SNI routes
require explicit `--tor`/`--strict`; omitted effects remain UNVERIFIED. The
offline contract is part of integration discovery and rejects every HTTP call.
See `docs/LIVE_SETTINGS_TESTS.md` for the scope, report and focused commands.
Settings now update idle download semaphores (deferring changes until active
tasks drain), logging levels, preparation delay, DoH fallback and live QML
language/Material appearance. Untranslated catalog entries retain English.

Desktop statistics/history checks use
`uv run python -m src.tests.smoke.statistics_gui` or the helper's **Live desktop
statistics and history** entry. Eleven dependent workflows use real HLS/RAW
downloads, a public profile and real PocketBase processes. They verify stored
metadata, stop/resume and failure/retry updates without duplicates, aggregate
cards/source groups, privacy, list removal preserving history, REST refresh,
restart persistence, disabled tracking and startup errors. All data is isolated.
The disabled GUI contract is included in ordinary integration discovery with
HTTP rejected. See `docs/LIVE_STATISTICS_TESTS.md`. Statistics Refresh now reloads
the actual PocketBase cache asynchronously rather than only redrawing it;
startup and diagnostics share `Backend.bind_database_bridge` signal wiring.

Advanced desktop download checks use
`uv run python -m src.tests.smoke.download_advanced` or the helper's **Advanced
desktop download controls** entry. Real PornHub/Eporner/XVideos metadata feeds
the actual regex/duration/quality/date matcher; separate real GUI submissions,
range selection and a Unicode-path HLS download exercise preparation and output.
Twenty-five explicitly synthetic title fixtures cover unusual languages,
punctuation, reserved names and long filenames in real GUI/filesystem checks.
See `docs/LIVE_ADVANCED_DOWNLOAD_TESTS.md`; the offline contract rejects HTTP.
Original titles are preserved for display/filtering; portable component sanitation
is in Qt-free `src/shared/download_options.py`. Invalid filter/template inputs
are rejected before fetching, publication dates are inclusive calendar days,
Start/End now select inclusive original video positions before filters, dots do
not suppress the media extension, and the Keyboard shortcuts dialog is wired.

Desktop close/reopen checks use
`uv run python -m src.tests.smoke.application_recovery` or the helper's **Live
application teardown and recovery** entry. Eight workflows use 16 independent
GUI processes: idle, active preparation, pending history writes, database moves,
and retained/cleaned HLS/RAW transfers with a second queued row. A fresh process
uses a different working directory and verifies paused restoration, explicit
native resume, real checkpoint reuse, history and clean process/task shutdown.
See `docs/LIVE_APPLICATION_RECOVERY_TESTS.md`. The idle contract rejects HTTP.
`ApplicationShutdown.qml` is shared by desktop Main and the diagnostic window.
Teardown cooperatively stops downloads, saves queue snapshots and flushes history
before closing services. `src/shared/download_recovery.py` handles atomic metadata
snapshots; `src/backend/download_recovery.py` restores paused rows without HTTP.
Snapshots/HLS checkpoints now use the writable Qt generic cache/PornFetch folder;
native objects/cookies/passwords are never serialized. Resume fetches a fresh
provider object. The PocketBase command uses `--` before credentials so generated
passwords beginning with `-` are not parsed as flags. Old orphan `.temp` files
are not automatically migrated; force-kill/power-loss recovery is outside the user's scope.

Public model/playlist end-to-end checks use
`uv run python -m src.tests.smoke.collections_gui` or the helper's **Live
model/playlist end to end** entry. All supported public source routes have an
explicit inventory: 16 automated workflows, SpankBang manual, Thumbzilla playlist
unverified without a public fixture. Actual desktop inputs/buttons, limits,
regexes, inclusive ranges, cancellation, native later-page provenance, selected
media/FFmpeg validation and PocketBase source history/statistics are exercised.
Offline invalid-source/filter contracts reject HTTP in integration discovery.
See `docs/LIVE_COLLECTION_TESTS.md`; local RedTube playlist extraction needs the
sibling library fix until released. Unsupported/interactive challenges block that
provider; recognized PornHub math responses reach the native handler, and real
upstream failures remain visible. These complement,
rather than replace, the 76 metadata-only URL-variant checks.
Pagination allows real page-boundary overlap (XHamster currently repeats some
entries); it uses another actual GUI range to load a new later-page entry and
still rejects fully repeated pages. The sibling XVideos library now extracts
`Video.author_name` from the video page; the GUI adapter uses it to avoid an
unnecessary author/statistics request per row, with native lookup for older
versions or missing labels. Use its source via PYTHONPATH until released.
Its profile iterator now explicitly closes the inner scraper before returning
from an early stop, avoiding asynchronous prefetch cleanup racing later fetches.

Live cookie-account checks use `uv run python -m src.tests.smoke.account_cookies --browser brave`
and the helper's explicit browser-session confirmation. They cover PornHub,
XHamster and XVideos with real account lists and video metadata, without media
downloads or password submission. See `docs/LIVE_ACCOUNT_TESTS.md`. The XHamster
account JSON extractor fix is in the sibling `unofficial-api-for-xhamster` checkout
until the provider release is published; use `PYTHONPATH` to test that source.
`src.tests.smoke.account_passwords` runs the same checks for PornHub/XHamster
from fresh password sessions, collecting a shared test password through Zenity.
XVideos password login is excluded; its library exposes cookies/tokens only.
The helper's **Complete account GUI checks** runs
`src.tests.smoke.account_gui`: real browser imports, production desktop/mobile
QML actions, the real GUI list pipeline and rendered delegate metadata, plus
deterministic control/error/cancellation contracts. Its 36-check default action
matrix reports checklist coverage separately from Python line/branch coverage.
Optional XVideos playlist/private fixtures have explicit authenticated/anonymous
checks; private authorization is never inferred from a public fixture.
The shared live diagnostic guard stops access denials, CAPTCHA pages and unknown
JavaScript challenges. It delegates only recognized HTTP-200 math payloads on
HTTPS PornHub hosts to the existing `eaf_base_api` handler, recording events
without cookies/tokens. Previously the guard incorrectly blocked those native
responses. Collection pagination hashes retain the public `viewkey` query ID so
distinct PornHub videos remain distinguishable. For HTTP 429 the guard honors Retry-After with a 30-second
minimum cooldown, then space requests by at least 5 seconds across all cores;
safe read retries are bounded. Intentional waits extend check deadlines and are
reported separately. See the rate-control flags in `docs/LIVE_ACCOUNT_TESTS.md`.
Later pagination 404s are terminal pages; first-page/auth/item failures remain
visible. Installed XHamster 2.6.3 lacks the local account JSON parser fix; reports
show the actual source and whether the known fix is present.
The user reports the complete account suite passing after these fixes and considers
the Account page complete for the current release; Android device checks are deferred.
