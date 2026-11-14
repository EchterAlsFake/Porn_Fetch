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

`test_first_run_setup` exercises real QML with isolated settings: explicit license
acceptance, the offer acknowledgement, reporting scope, interruption/resumption,
one-time completion and Android folder selection/cancellation in both orientations.
`test_build_smoke_isolation` runs desktop and mobile smoke startup with existing
settings and download checkpoints and verifies they remain byte-for-byte unchanged.
It launches from a read-only directory on Unix, with disposable logs. macOS CI
also launches the packaged executable from `/` to catch working-directory writes.
Native Android picker permissions and external-player access still need a device.

The setup suite also sends real Qt key events through all five pages, including
explicit reporting selection, text scrolling, focus visibility, Back/Escape,
Tab/Shift+Tab, and restoring focus after folder-picker cancellation/selection.
The picker result is simulated at the native-dialog boundary in these tests.
For a TV build, start with fresh application settings and use only the remote:

1. Use Up/Down to scroll each page's text. Right or center moves from the reader
   to the next control; Left/Right and Up/Down move between controls.
2. Use center to check license acceptance, continue free, explicitly choose a
   reporting option, expand its disclosure, and acknowledge the message. Verify
   the focus outline stays visible and arrows alone do not select reporting.
3. Use Back to revisit a page, then return. On the first page Back focuses the
   exit button; exiting still requires center.
4. Open the folder picker, cancel with Back, and reopen it with center. Select
   a writable shared folder and finish setup. Restart to verify completion and
   retained storage permission.

Some Android TV images have no usable document-tree picker. On the Android 16
TV emulator checked on 2026-11-09, the following resolves to
`com.android.tv.frameworkpackagestubs/.Stubs$DocumentsStub`:

```sh
adb shell cmd package resolve-activity --brief -a android.intent.action.OPEN_DOCUMENT_TREE
```

That stub cannot supply a folder. Install a compatible document-tree picker or
use an image/device that supplies one to test custom folder selection. To finish
setup without a picker on Android 10+, select **Use shared Downloads/Porn Fetch**
with the D-pad, then Finish setup. Verify a completed file appears in shared
Downloads/Porn Fetch, can be read by another app, and survives restarting Porn
Fetch. Test skip-existing as well. No broad storage permission is needed. Native
export errors must keep the original private download and report failure rather
than announce completion. The setup suite covers the alternative choice; the
storage and queue tests cover asynchronous results and routing to the helper.
The native helper was separately validated with synthetic bytes in an isolated
APK on TV API 36 and Automotive API 33 on 2026-11-09; a rebuilt Porn Fetch APK
still needs an integrated device check. Private app storage remains insufficient
as the final destination. The rest of the application still needs separate TV
navigation work.

The helper asks before accessing websites, browser sessions or real media.
Ordinary unit and integration discovery must stay offline.

The update-dialog regression is offline and uses the software renderer by
default. On a Linux desktop, exercise the real Wayland/OpenGL renderer with:

```sh
PORNFETCH_NATIVE_UPDATE_TEST=1 uv run --no-sync python -m unittest src.tests.integration.test_update_dialog
```

This opens isolated desktop and mobile test windows and verifies startup
presentation, the saved opt-out, manual review and Markdown/HTML formatting with
the full release notes. Desktop review also exercises Activity. It does not install an
update or change your normal settings. The native check caught the Qt Quick
render-thread crash that the software renderer did not reproduce.

Android's native installer handoff must be checked separately from dialog
presentation. Initialize both `PornFetchPlatform` and `PornFetchNotifications`,
stage a newer APK signed with the installed test app's key, and atomically rename
the `install-update.json` request into private files. With unknown-source access
disabled, verify that Android opens its permission settings; after allowing access
and returning, verify that the update confirmation opens. Cancel the installation
and check a notification command is also consumed. Use an isolated test package
to preserve the user's app and settings. Both command types must share one native
root-directory FileObserver: Android can replace a callback when a second observer
watches that same directory.
On 2026-11-14, this handoff passed on the connected API 36 phone using production
native helpers in an isolated APK with a synthetic, same-key newer candidate.
The test installation was cancelled and the probe removed. This validates the
native prompt and permission-return path, not full Porn Fetch update installation.

`src.tests.integration.test_contrast_theme` renders the real desktop window in
Material and Fusion styles while toggling dark/light mode and high contrast. It
checks button foreground/background pairs, field outlines, statistics surfaces,
the native application palette and all fourteen bundled content-language flag
images, then opens the language popup. Check Windows title-bar appearance and
native Windows style on Windows as well; offscreen tests do not validate those.

## Live checks

These commands contact real providers. Download checks save actual media and
need FFmpeg. Account checks read a browser session only when explicitly selected.
Use `--help` for each runner's current options; not every runner shares the same
filters. Reports distinguish failed, skipped, blocked and manual checks.

Run with `uv run --no-sync python -m src.tests.smoke.NAME`:

| NAME | What it checks |
| --- | --- |
| `bellesa` | Bellesa Video/Channel/Performer routes, complete profiles, all measured qualities, metadata and free limits |
| `youjizz` | YouJizz Video/Collection/Pornstar/User, complete profiles, measured HLS qualities, free limits and GUI preparation |
| `porn` | Porn.com Video/Collection/Channel/Pornstar, native scene filtering, complete profiles, free/premium HLS and GUI preparation |
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
uv run --no-sync python -m src.tests.smoke.profile_urls --filter porndoe --items 2
uv run --no-sync python -m src.tests.smoke.profile_urls --filter pornhat --include-variants --items 2
uv run --no-sync python -m src.tests.smoke.download_lifecycle --provider pornhat --scenario pause-resume --quality 360
QT_QUICK_BACKEND=software uv run --no-sync python -m src.tests.smoke.download_gui --provider pornhat --scenario pause-resume --quality 480
uv run --no-sync python -m src.tests.smoke.download_lifecycle --provider porndoe --scenario pause-resume
uv run --no-sync python -m src.tests.smoke.download_gui --provider porndoe --scenario pause-resume
uv run --no-sync python -m src.tests.smoke.download_gui --provider eporner --scenario pause-resume
uv run --no-sync python -m src.tests.smoke.collections_gui --provider xvideos --kind playlist
uv run --no-sync python -m src.tests.smoke.application_recovery --offline-only
uv run --no-sync python -m src.tests.smoke.settings_gui --help
uv run --no-sync python Porn_Fetch_CLI.py --test-mode --filter XFreeHD --test-downloads
```

Pornhat integration was checked on 2026-11-09 using the published
`unofficial-api-for-pornhat==0.1.0`, `eaf-base-api==4.2.6` and Python 3.15.2.
Only Video, Model and Channel are integrated. All ten accepted hosts prepared
video ID 684951 with a three-minute duration and 360p/480p/720p qualities.
Four live GUI profile cases passed with no skips: Model, Channel, a German
model and a `.one` channel. Complete ordered profile listings matched their
live HTML: 200/200 model IDs across 59,59,59,23 cards, and 471/471 channel IDs
across seven 59-card pages and a 58-card final page.

CLI pause/resume completed FFmpeg-readable 156.48-second output at every exposed
quality (360p, 480p, 720p), retaining and reusing segments. The real desktop
Downloads QML workflow also passed Stop/Resume at 480p with segment reuse,
completion at 100%, and a readable full output file. Use the documented software
renderer in headless environments: the initial default-renderer run crashed
before recording a result, while the software-renderer run passed. These live
checks use isolated settings, output folders and reports under `/tmp`; they do
not add network requests to ordinary CI. Native Android/iOS packages were not rebuilt.

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
- Check app icons in the launcher, taskbar/Dock, window and installer at normal
  and high display scaling. `test_app_icons` checks the shipped desktop frames,
  padding, Android mask safety and opaque iOS artwork; iOS staging checks verify
  that Xcode receives its asset catalog. Native appearance still needs OS builds.
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

## RedGIFs integration

[RedGIFs integration checks](REDGIFS.md#validation-on-2026-11-10) cover the
Video/GIF, User/profile, Niche/playlist and mixed Collection/playlist paths, measured
RAW quality selection and complete public video listings. The opt-in runner is
`python -m src.tests.smoke.redgifs`; existing download lifecycle and GUI runners
also accept `--provider redgifs`. No requests run on import or normal discovery.

## Bellesa integration

The published `unofficial-api-for-bellesa>=1.0.0` package is integrated for Video,
Channel and Performer only. The `bellesa` helper suite is explicitly online and
media-enabled. All files and retained state use isolated temporary directories.

```sh
uv run --no-sync python -m src.tests.smoke.bellesa --report /tmp/bellesa-integration.json
QT_QPA_PLATFORM=offscreen QT_QUICK_BACKEND=software uv run --no-sync python -m src.tests.smoke.profile_urls --filter bellesa --include-variants --items 2 --report /tmp/bellesa-profiles-gui.json
uv run --no-sync python -m src.tests.smoke.download_lifecycle --provider bellesa --quality 450 --report /tmp/bellesa-lifecycle.json
QT_QPA_PLATFORM=offscreen QT_QUICK_BACKEND=software uv run --no-sync python -m src.tests.smoke.download_gui --provider bellesa --quality 450 --report /tmp/bellesa-downloads-gui.json
```

`bellesa --metadata-only` omits media downloads while retaining real requests and
complete profile reconciliation. The full runner downloads all six actual
qualities of video 7054 plus free-best samples at 720p and 600p (an older 4:3
video). Metadata export, playable dimensions, audio and duration are checked.
See [the recorded Bellesa results](BELLESA.md) for exact commands and limits.

## Porn.com integration

[Porn.com integration](PORN.md) records the published-wheel checks for the four
supported types, twelve hosts, native scene filtering, complete profile feeds,
free preview, actual qualities, metadata and GUI/CLI downloads. The opt-in
`python -m src.tests.smoke.porn --gui` runner performs real requests and complete
downloads by default; `--metadata-only` omits media transfers. Existing lifecycle
and desktop download runners also accept `--provider porn`. Other provider
interfaces, keyword search and external referral downloads remain excluded.


## YouJizz integration

Only Video, Collection, Pornstar and User are integrated through the published
`unofficial-api-for-youjizz>=0.1.0` package. The opt-in `youjizz` helper suite
makes real requests and complete HLS downloads; normal discovery starts no new
provider traffic. `python -m src.tests.smoke.youjizz --gui` covers both hosts,
complete pornstar/user listings, typed collections, free previews, all rendition
tiers on the five media samples, CLI metadata export and real GUI preparation.
Use `--metadata-only` to omit complete media transfers. Existing CLI lifecycle
and desktop controls runners accept `--provider youjizz`. See [YouJizz](YOUJIZZ.md)
for the exact commands, results and platform limits.
