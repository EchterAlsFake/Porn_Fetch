# Developer guide

> [!CAUTION]
> The latest published binary release is massively outdated. This guide describes the in-development 3.9 source tree; it may not match the current 3.8 download.

Porn Fetch uses Python 3.15, `uv`, an asynchronous backend, a PySide6/QML desktop frontend, and a separate headless CLI built with Questionary and Rich.

## Set up a development checkout

Install `uv`, then run:

```bash
uv sync --extra gui --group dev
```

The repository's `.python-version` selects Python 3.15. Video remuxing and metadata writing use a separate, minimal LGPL-only FFmpeg executable in `third_party/` (or system PATH). See [FFmpeg builds](FFMPEG.md) for the pinned source, capabilities, and toolchains.

Desktop builds pin Nuitka 4.3.3, whose Python 3.15 support is still experimental.
Some native dependencies currently build from source on Python 3.15; use the
platform compiler/toolchain installed by CI or the installation scripts.
Android builds pin Python and hostpython 3.15.2 and require the new `cp315`
Qt wheels from the pinned `6.12.0-api28` release. See [Android CI](ANDROID_CI.md)
for wheel checksums and build inputs. Current release progress is maintained in
the [server checklist](https://pornfetch.to/checklist).
After syncing, apply and verify `scripts/patch_qtasyncio.py .venv`. Besides the
event-loop fixes, it preloads the executor before PySide6's module attribute
hook can expose Python 3.15's deferred import object to `asyncio.to_thread`.

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

Windows builds use Certum SimplySign through the `signing` environment, including
the Qt maintenance tool. See [Windows signing](WINDOWS_SIGNING.md) for secrets,
signing order and verification.

The experimental iOS build uses the separate recipes in `ios-lab/`. See
[iOS build and deployment](ios/BUILDING.md) for the preserved macOS toolchain,
device and simulator targets, signing, and dependency rebuild order.

## Implementation notes

- Use asyncio rather than QThread worker code.
- Keep shared models independent of Qt.
- Schema-1 license and Stripe checkout/session logic is intentionally gone. Current licensing is schema 2.
- Read `BACKEND.md` before changing provider/client behavior.
- Read `SNI_PROXY_AGENT_HANDOFF.md` in full before changing SNI proxy behavior or its tests.
