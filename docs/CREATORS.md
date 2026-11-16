# Creator subscriptions

On desktop, the PocketBase component must be installed. Installer users can add
it through Maintenance Tool. Android APKs bundle the native runtime automatically.
Source runs can use the existing CLI
`--install-pocketbase` option or set `PORN_FETCH_POCKETBASE_BINARY` to an existing
executable. After first-use setup, the app proactively checks the runtime and opens
the local database. Add subscription stays disabled until that succeeds. Missing
or broken PocketBase is shown in the dashboard with platform-specific setup
instructions, selectable error details and **Check again**. Installer builds also
provide **Manage components**. No URL is needed to discover a missing dependency.
A retry applies migrations and checks the batch API before enabling Add.

The **Creators** page on desktop and Android follows supported creator, channel, performer,
playlist and collection URLs. Add a URL, name, output folder and quality. Source
type is resolved through the actual provider API. New subscriptions always default
to **Best available**, independently of the global quality setting. Editing an
existing subscription retains its saved quality. A first scan creates the local
catalogue; **Download pending** requests the existing catalogue. Premium is
required for full creator archives, higher resolutions and automatic downloads.
Free users can scan, download, pause and resume five videos per subscription at
up to 720p. The same five membership identities remain eligible across rescans,
retries and relaunches, including ignored/completed entries. Free video pages and
counts show that preview; older Premium catalogues remain stored. The dispatcher
checks eligibility again and the existing engine receives a preview index 1–5,
so normal collection and quality gates still apply. Automatic queueing stays
Premium-only. Saved progress above 720p remains paused when using the trial.
Free discovery is explicitly labelled as a five-video preview. Each scan keeps the free/Premium mode it started
with, even if entitlement changes while it is running. A preview never establishes
a full-scan baseline.

The dashboard shows discovered video counts and page progress where the provider
exposes it, separate last-attempt/last-complete timestamps in local time, and the
latest ten scan attempts with trigger, outcome, completion time and errors. Page
counts are pages reached, not a promised remote total or a percentage.

**Scan when Porn Fetch starts** runs once per launch after first-use setup and
the initial entitlement check. **Scan now** performs another full traversal.
There is no periodic or closed-app scheduler. **Automatically download new videos**
is opt-in and applies to additions after the first successful full scan. An
incomplete initial scan does not establish that baseline.

Pause downloads before closing, or close normally and let the application stop
its writers. Interrupted transfers reopen paused; **Resume / download pending**
reuses their saved identifiers, filenames, selected quality and native checkpoints.
Changing subscription settings affects videos that have not yet been prepared.
Downloaded videos remain completed if a file is later deliberately moved/deleted.
Removing a subscription preserves files, history, and jobs shared with other
subscriptions. Ignoring a video applies to that subscription's membership.

A persistent Premium banner and subscription-dialog copy explain the trial and
full-archive limits. Details use separate colored status counters and labeled
quality/destination/scan-date cards, including human-readable quality names.
Creator buttons use 48-pixel minimum targets, larger text/padding and primary
colors with luminance-selected black/white text. They have animated hover/press
colors and a small scale change,
including highlighted buttons. Reduced motion and high contrast disable the scale
animation; keyboard focus remains visible.

The first time Premium becomes available in the GUI, the global quality preference
switches to **Best available** (including 4K when offered). An onboarding marker
persists this one-time change across restarts and preference resets. Subsequent
license refreshes and unlocks preserve quality choices the user makes afterward.
This preference change does not alter the licensing protocol or entitlement rules.

## Storage and execution

`src/database/creators.py` adds subscriptions, scan attempts, shared video records,
memberships and a SQL counts view. The old draft schema is upgraded without
removing its records. The existing PocketBase tracker owns one shared process;
creator storage works when optional history recording is disabled. Its authenticated
loopback batch API commits up to 25 discoveries per transaction. The dashboard
requests twelve expanded membership rows per page.

`src/shared/creator_library.py` persists identities before preparing downloads.
Scans restart from page one and reconcile membership; moving page numbers and
already-known first pages are never used as an early stopping rule. Scans preserve
partial discoveries when stopped or when a provider fails. A successful rescan
does not delete records absent from a moving remote listing.

`src/backend/creator_sources.py` uses fresh listing sessions with the existing
media transport, settings and provider cookies. `src/shared/creator_scans.py`
requests `pages="all"`, `start_page=1`, original order, listing-only loading and
strict errors. Exposed paginator summaries must report exhaustion. Provider
async-generator facades without a public summary use the strict all-pages contract;
errors are unwrapped and raised instead of being skipped. RedGIFs still images and
Porn.com outbound referral cards are excluded.

`src/backend/creator_bridge.py` dispatches at most twice the configured parallel
limit into the existing GUI engine. It resolves player metadata at execution,
reconciles ordinary queue rows and completed history, and stores a local metadata
snapshot before transfer. Numeric subscription quality is a ceiling; it must not
be silently replaced by a higher global preference. Native completion is captured
before the engine removes its completed row. Fresh provider metadata is resolved
when a restored job resumes; signed media URLs and cookies are never persisted.

## Android runtime and resume

`native/pocketbase` embeds the same PocketBase 0.40.4 Go package used on desktop
as `libpornfetch_pocketbase.so`, with Android NDK r28c/API 28 builds for arm64-v8a,
armeabi-v7a (ARMv7), x86 (i686), and x86_64. `scripts/build_android.py` compiles the
selected runtime before deployment. Its helper automatically fetches a
SHA-256-verified Go 1.27.4 toolchain if needed. Go module checksums are committed.
The APK hook stages the library and dependency notices; publication checks require
both. Build outputs stay in `build/android-pocketbase/<ABI>/`. See the
[native build instructions](../native/pocketbase/README.md).

`src/database/android.py` loads the extracted APK library through ctypes. The Go
server binds only an ephemeral loopback port, applies the same JavaScript
migrations and authenticates the existing Python client with a fresh startup
password. The tracker owns one instance shared by subscriptions. Android history
and statistics stay disabled; no replacement database is introduced.

Queue recovery used to be bound only for the desktop layout, while Creators had
no Android PocketBase service. Both missing connections are now implemented.
Android queue JSON and HLS/RAW state live in private application data, rather than
the system cache. Creator media is staged privately and exported through the
existing SAF/MediaStore helper. Each prepared job persists its destination URI,
job ID, quality and filename. Reopening restores paused rows and checkpoints;
changing the app's destination does not redirect an existing creator job. Choose
**Use current app download folder** in subscription settings to change future
jobs. Removing app data or explicitly clearing download files removes recovery
state. Android background execution remains subject to OS process/lifecycle limits;
this does not introduce a closed-app scheduler or foreground download service.

## Verification

Offline UI and scan-boundary checks:

```sh
.venv/bin/python -m unittest src.tests.unit.test_creator_scans src.tests.integration.test_creators_preview src.tests.integration.test_android_navigation
```

Actual PocketBase integration checks use disposable data directories and require
an explicitly supplied binary. They cover normal restart, interrupted/failed scans,
baseline/automatic behavior, shared membership, draft migration, database pagination,
real QML bindings and controlled transfer lifecycle events:

```sh
PORN_FETCH_TEST_POCKETBASE=/path/to/pocketbase .venv/bin/python -m unittest src.tests.integration.test_creator_library src.tests.integration.test_creator_bridge
```

The live runner uses isolated settings and disposable downloads. By default it
fully scans and rescans the Bellesa example channel. `--downloads` adds real HLS
and RAW files; `--resume` also stops each transfer and reconstructs the session
from PocketBase before resuming. Files are checked with FFmpeg and removed after
the run. Reports contain counts and outcomes, without signed media URLs.

```sh
.venv/bin/python -m src.tests.smoke.creators --pocketbase /path/to/pocketbase
.venv/bin/python -m src.tests.smoke.creators --pocketbase /path/to/pocketbase --resume
.venv/bin/python -m src.tests.smoke.creators --pocketbase /path/to/pocketbase --free --resume
```

2026-11-15 verification used released provider/base packages: the Bellesa fixture
reconciled 30 unique videos across a full scan/rescan. Bellesa HLS and RedGIFs RAW
transfers completed and passed media readability checks, including normal
pause/close/reopen/resume with stable job IDs and paths. A Porndoe fixture's media
server returned HTTP 403; that attempt remained failed and was not counted as a
successful transfer. Existing provider pagination reconciliation is documented in
[pagination implementation](pagination-audit/IMPLEMENTATION.md).

The free creator trial was also exercised with the real engine: a five-video
Bellesa preview/rescan, Bellesa 720p HLS and RedGIFs 480p RAW completed, including
pause/close/reopen/resume with stable job IDs/paths and FFmpeg readability checks.
The repository/bridge test verifies exactly five native dispatches, a 720p ceiling,
rescan-stable membership, blocked sixth jobs and Premium-only automatic queues.

## Current limits

All four Android libraries were compiled from source and have 16 KiB ELF load
alignment. Native dlopen checks on the x86 Android TV API 36 and x86_64 Automotive
API 33 emulators applied real migrations, authenticated and committed 30 videos
through the batch API. The x86 check also stopped/reopened and retained all rows.
An isolated host test of the same Go bridge verifies Android tracker selection,
creator scans, private partial files/checkpoints and queue/destination recovery.
These checks do not establish full APK startup or real Android media exports;
a rebuilt APK still needs that end-to-end device test. ARM/ARM64 runtime testing
also remains pending. iOS Creators remains unavailable pending its native runtime;
the existing iOS downloader is unchanged.

The embedded host test is opt-in:

```sh
cd native/pocketbase
go build -buildmode=c-shared -o /tmp/pornfetch-pocketbase-host.so .
cd ../..
PORN_FETCH_TEST_POCKETBASE_LIBRARY=/tmp/pornfetch-pocketbase-host.so .venv/bin/python -m unittest src.tests.integration.test_android_pocketbase
```

For the manual feature check, add one small source, let its first scan finish,
start a download, pause, close normally and reopen. Confirm the library, progress,
quality and destination, then resume and verify playback in shared Downloads or
the chosen folder. Scan again and inspect recent attempts. Repeat once with
automatic downloads enabled after the baseline. A full Android APK rebuild is
required; replacing Python/QML files alone does not add its native library.

Provider availability still limits discovery. An advertised next page returning
404, a challenge, or an inaccessible feed remains incomplete, even if earlier
pages produced videos. Some Thumbzilla/Tube8 listings expose a page-101 boundary;
see the pagination audit. The dashboard never treats those failures as full
coverage. Normal close/reopen is supported; forced-kill/power-loss durability and
cross-device synchronization are outside this implementation.
