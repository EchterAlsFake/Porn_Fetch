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
  and `tor_runtime.py`; see `docs/TOR_SUPPORT.md`. Android updates use the separate
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
