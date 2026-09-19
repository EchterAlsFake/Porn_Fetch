# Developer guide

> [!CAUTION]
> The latest published binary release is massively outdated. This guide describes the in-development 3.9 source tree; it may not match the current 3.8 download.

Porn Fetch uses Python 3.14, `uv`, an asynchronous backend, a PySide6/QML desktop frontend, and a separate headless CLI built with Questionary and Rich.

## Set up a development checkout

Install `uv`, then run:

```bash
uv sync --extra gui --group dev
```

The repository's `.python-version` selects Python 3.14. The optional `av` extra installs PyAV on supported platforms when media metadata work requires it:

```bash
uv sync --extra gui --extra av --group dev
```

## Run the application

```bash
# Desktop GUI
uv run main.py

# Headless terminal interface
uv run Porn_Fetch_CLI.py
```

The CLI must remain usable without PySide6 or a display server. Never import `src.backend`, `src.frontend`, or `src.database.bridge` from the CLI/shared/licensing layers.

## Repository structure

- `src/backend/`: desktop application and Qt-facing adapters.
- `src/frontend/`: QML, resources, graphics, and translations.
- `src/cli/`: Questionary/Rich terminal frontend and batch commands. Interactive
  features live in `src/cli/flows/`; `wizard.py` only composes the main menu.
- `src/shared/`: Qt-free models and services used by both frontends.
- `src/database/`: separate PocketBase client, process service, tracker, legacy
  importer, compatibility exports, and the GUI bridge.
- `src/licensing/`: shared schema-2 licensing implementation.
- `src/tests/`: unit, integration, smoke, and manual test groups.
- `packaging/`: PyInstaller and PySide/Nuitka build specifications.
- `scripts/`: installation and build-maintenance scripts.
- `vendor/`: vendored platform components such as Sparkle.
- `docs/`: maintained documentation and historical release notes.

The root `main.py` and `Porn_Fetch_CLI.py` files are intentionally small launchers. GUI composition lives in `src/backend/application.py`.
Installed checkouts also provide `porn-fetch` and `porn-fetch-cli` entry points.

## Frontend resources and translations

After changing QML resources or translatable strings, run the update script for your platform:

```bash
bash src/frontend/update.sh
# or on Windows
pwsh src/frontend/update.ps1
```

The generated resource module remains in `src/frontend/UI/resources.py`. Do not hand-edit it.

## Tests

For the interactive selector:

```bash
uv run src/tests/helper.py
```

It lets you select offline unit tests, Qt/service integrations, CLI checks, online provider checks, active downloads, and the SNI smoke test. Network and real-download suites require explicit confirmation.

Direct commands are also available:

```bash
uv run python -m unittest discover -s src/tests/unit -p "test_*.py"
QT_QPA_PLATFORM=offscreen uv run python -m unittest discover -s src/tests/integration -p "test_*.py"
uv run Porn_Fetch_CLI.py --test-mode --filter offline
```

Normal CI runs only offline suites. Keep online/provider and active-download checks opt-in.

The Python version constant in `src/shared/version.py` is authoritative. Hatchling
reads it into package metadata, so releases only update that one file.

## Build files

Desktop builds use the platform specification in `packaging/pysidedeploy_*.spec`. The headless binary uses `packaging/pyinstaller_cli.spec`. The cross-platform build workflow is `.github/workflows/build_all.yml`.

The macOS Sparkle framework is stored in `vendor/macos/sparkle/`; `scripts/patch_macos_bundle.py` performs the final bundle patching.

## Implementation notes

- Use asyncio rather than QThread worker code.
- Keep shared models independent of Qt.
- Schema-1 license and Stripe checkout/session logic is intentionally gone. Current licensing is schema 2.
- Read `BACKEND.md` before changing provider/client behavior.
- Read `SNI_PROXY_AGENT_HANDOFF.md` in full before changing SNI proxy behavior or its tests.
