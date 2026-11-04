# Test Porn Fetch

Use an isolated test environment. Do not point tests at your normal download or
history folders. Source tests do not prove that a signed installer works on a
clean machine.

## Offline checks

```sh
uv sync --upgrade --extra gui --group dev
uv run --no-sync python scripts/patch_qtasyncio.py .venv
uv run --no-sync python -m unittest discover -s src/tests/unit -p 'test_*.py'
uv run --no-sync python -m unittest discover -s src/tests/integration -p 'test_*.py'
uv run --no-sync python Porn_Fetch_CLI.py --test-mode --filter offline
uv run --no-sync python main.py --smoke-test
```

On a Linux machine without a display, set `QT_QPA_PLATFORM=offscreen` and
`QT_QUICK_BACKEND=software` before the GUI commands. CI also checks Python with
Ruff and Pyright, validates translations and workflows, builds Python packages,
and audits dependencies. A vulnerability reported by the audit fails the job.

To choose a suite interactively:

```sh
uv run --no-sync python src/tests/helper.py
```

The helper asks before accessing websites, browser sessions or real media.
Ordinary unit and integration discovery must stay offline.

## Live checks

These commands contact real providers. Download checks save actual media and
need FFmpeg. Account checks read a browser session only when explicitly selected.
Use `--help` for each runner's current options; not every runner shares the same
filters. Reports distinguish failed, skipped, blocked and manual checks.

Run with `uv run --no-sync python -m src.tests.smoke.NAME`:

| NAME | What it checks |
| --- | --- |
| `profile_urls --include-variants` | Profile URL aliases, real metadata and GUI rows; no media downloads |
| `download_lifecycle` | CLI HLS/RAW pause, resume, cleanup and restart |
| `download_gui` | Desktop buttons, progress, quality, stop/remove and finished files |
| `download_queue` | Parallel limits, queued cancellation and independent downloads |
| `settings_gui` | Settings saved to disk, live consumers and observable effects |
| `statistics_gui` | Real PocketBase history, totals, privacy and persistence |
| `download_advanced` | Filters, ranges, filenames and output validation |
| `application_recovery` | Normal close/reopen, retained transfers and queued jobs |
| `collections_gui` | Public profiles/playlists through to selected downloads |
| `account_gui --browser brave` | Account controls, real cookies and lists in desktop/mobile QML |
| `account_cookies --browser brave` | Account API checks without media downloads |

The CLI self-test checks gallery titles and image URLs. Adding `--test-downloads`
also downloads the selected gallery into a temporary directory and checks the
file count and image signatures, in addition to the active video download.

Examples:

```sh
uv run --no-sync python -m src.tests.smoke.download_gui --list
uv run --no-sync python -m src.tests.smoke.download_gui --provider eporner --scenario pause-resume
uv run --no-sync python -m src.tests.smoke.collections_gui --provider xvideos --kind playlist
uv run --no-sync python -m src.tests.smoke.application_recovery --offline-only
uv run --no-sync python -m src.tests.smoke.settings_gui --help
uv run --no-sync python Porn_Fetch_CLI.py --test-mode --filter XFreeHD --test-downloads
```

## Free and premium feature tests

Feature tests use an explicit synthetic entitlement in the isolated diagnostic
backend. They do not load a real license file or contact the license service.
The same entitlement is provided to the real backend and QML controls; the
production download/collection policies remain active.

```sh
uv run --no-sync python -m src.tests.smoke.download_queue --access free
uv run --no-sync python -m src.tests.smoke.download_queue --access premium
uv run --no-sync python -m src.tests.smoke.collections_gui --provider xvideos --kind playlist --access free
uv run --no-sync python -m src.tests.smoke.collections_gui --provider xvideos --kind playlist --access premium
```

The queue runner defaults to both access levels. Free checks serial transfers
even with an old larger semaphore; premium checks limits one/two and independent
stop/remove. Collection checks default to premium for full pagination. Their
free mode checks the first five videos, rejects ranges beyond the preview,
applies filters and downloads a selected preview row. Reports record the access
level. Settings diagnostics use premium to exercise all paid controls.

Do not add a license-verification bypass or a premium environment variable to
the normal application. `PATH` selects executables, not license files. Keep real
activation/device-binding validation in the existing explicitly enabled license
tests; these feature tests do not establish license-service readiness.

Settings effects that need Tor or Strict SNI require their explicit flags and a
suitable environment. Leaving them off does not count as a pass. The UI language
control is disabled because the app is English-only. Provider content language
is a separate setting and remains testable.

`settings_gui --effect system-notification-controls` checks the actual QML
opt-in/out, persistence and native bridge request files in an isolated directory.
OS permission dialogs and delivery still require the native checks below.

The password-account runner uses a Zenity prompt. It never accepts a password
on the command line:

```sh
uv run --no-sync python -m src.tests.smoke.account_passwords \
  --pornhub-email 'your-test-email@example.com' --xhamster-username 'your-test-username'
```

Use a currently authenticated browser for cookie checks. OS keyring failures,
expired sessions and missing private-playlist fixtures must remain visible.
Do not treat a public playlist as proof that private access works.

Account lists may legitimately be empty. The GUI runner checks the real empty
state, idle controls and absence of provider errors, and records `EMPTY` without
claiming rendered-video coverage. Missing session cookies remain failures with
an actionable message; cookie values are never included in reports.

## Provider fixtures and limits

`docs/url-routing-audit/profile-fixtures.json` is the shared profile inventory.
The GUI diagnostics and packaged app use it. Keep it when cleaning documentation.
The fixture checker is `docs/url-routing-audit/check_profile_fixtures.py`.
Download and collection inventories live with their runners in `src/tests`.

SpankBang media workflows are manual in both CLI and desktop runners: its current
HLS fixture lists CDN segments that return HTTP 404. Metadata checks still run.
To explicitly retry those media checks without hiding failures, use
`download_lifecycle --provider spankbang --include-manual-providers`. Manual
cases appear separately in reports and are never counted as passed.
Thumbzilla playlists need a working
public fixture. RedTube/Tube8 User pages may have public metadata without a
public video feed. A skipped or unavailable fixture is not a successful test.

Live checks stop on CAPTCHA, access denials and unknown challenges. Recognized
PornHub math responses may reach the existing provider handler. Rate-limit
responses use bounded retries and respect Retry-After. Do not bypass the guard to
make a report green. Do not include cookies, signed media links or passwords in
reports or bug reports.

The tests check real HTTP range/segment reuse and validate finished files with
FFmpeg. Explicit synthetic filename fixtures cover names that public videos may
not supply. Forced-kill and power-loss recovery are not part of the current scope.

## Accessibility and native checks

Use the actual release artifact on each supported OS:

- Navigate with only the keyboard. Check tab order, visible focus, dialogs,
  cancellation, and focus returning after a dialog closes.
- Test a screen reader: NVDA on Windows, VoiceOver on macOS/iOS, Orca on Linux,
  and TalkBack on Android. Check labels, progress, errors and restart notices.
- Check high contrast, reduced motion, larger text and a small window/screen.
- Allow and deny system-notification permission. Notifications must stay generic
  and the app must still show results when OS delivery is unavailable.
- Check fresh installation, optional components, upgrade and uninstall. Preserve
  your normal files by using a disposable user/profile and test output folder.
- On mobile, check folder access, saving files, keyboard/safe areas, app suspension
  and returning to the app. Desktop-rendered mobile QML cannot test these OS rules.

`scripts/audit_gui.py` inventories controls; it does not replace these checks.
Use the live website checklist for release status rather than adding another
local checklist.

## Fake update display

In one terminal run `uv run --no-sync python src/tests/smoke/fake_update_server.py`.
In another, set `PORNFETCH_UPDATE_URL=http://127.0.0.1:8765/update` and start the GUI.
The server provides fake notes and harmless links, not an installable binary.
Automatic installation still requires valid signed update metadata.
