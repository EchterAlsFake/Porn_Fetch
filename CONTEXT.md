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

First launch shows the beta notice, then the €19.99 license offer, then the
Ukraine message and error-reporting consent. `Onboarding/license_offer_seen`
and `Onboarding/ukraine_message_seen` survive preference resets and updates.
The offer opens pornfetch.to for purchase and has a free Continue action.

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

GUI feedback uses `notifications.py` and `NotificationPanel.qml`: asynchronous
session-only Recent activity and queued decisions. Desktop activity is in the
navigation row; mobile activity is under More. There is no top notification banner. Optional system
notifications are disabled by default and use generic text. They do not enable
background downloads. Mobile copies completed files to the selected output
folder automatically; there is no per-video Save action. Native notification
and assistive-technology checks require devices.

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

Ordinary dependency ranges and GitHub actions are updated frequently. Matching
native toolchains and checksummed archives stay pinned until replaced together.
Android uses Qt/PySide 6.12.0 cp315 wheels, target Python 3.15.2 and NDK r28c.
The wrapper regenerates machine paths and patches Qt's preload library names
for Android 13. All four Python 3.15 CI targets built on 2026-11-03; physical
device startup of those artifacts was not established by that build result.

The separate iOS CI build uses ARM64 macOS host tools and the published matching
Qt/PySide device inputs. The preserved lab still embeds Python 3.15.0rc2.
Its native dependency archive is required; a public clone alone is insufficient.
CI produces an IPA for re-signing. The user confirmed license activation,
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
