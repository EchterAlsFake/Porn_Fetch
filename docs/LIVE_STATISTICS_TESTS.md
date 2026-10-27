# Desktop statistics and history tests

Run the helper and select **Live desktop statistics and history**, or run:

```bash
uv run python -m src.tests.smoke.statistics_gui
```

This opt-in suite uses production DownloadsPage and StatisticsPage QML, the
actual download backend, native provider libraries and a real PocketBase server.
It downloads one PornHub HLS video and one Eporner RAW video at their lowest
available free resolutions, and prepares one real public profile video. It does
not use browser cookies, accounts, SpankBang, mocked media or fabricated download
outcomes. FFmpeg probes both completed files.

The existing UI presents aggregate statistics rather than a separate history
table. Tests therefore check rendered statistics and the underlying persisted
history through real PocketBase REST requests, including the existing source
and failed-video query APIs. They do not introduce a history-management UI.

## Workflows

| Check | Evidence |
| --- | --- |
| Tracking disabled | The GUI displays its notice; real video preparation/removal creates no database or records |
| Empty dashboard | An actual empty PocketBase database produces zero totals, a zero success rate and the empty-source message |
| Pending history | Real provider metadata is saved before media transfer and counted as other/pending |
| HLS stop/resume | A real partial transfer becomes cancelled, then completed; retries update the same record, and auto-clearing the queue preserves history |
| RAW failure/retry | A genuine filesystem path conflict produces failed history; a successful real retry clears the failure without adding a second record |
| Source history | A real profile video retains its source association and failed-query entry; manually removing the queue row keeps its history |
| Privacy | Actual source labels are masked/unmasked; source URLs are not rendered, and masking leaves stored metadata unchanged |
| Refresh | An independent REST client renames a stored source; clicking the real Refresh button reloads it into the GUI |
| Restart | The PocketBase process and GUI bridge are stopped and recreated; saved records, identities and aggregate statistics survive |
| Tracking disabled after use | Disabling tracking starts no service and leaves existing database files intact; re-enabling restores history |
| Database startup failure | A genuine invalid database path emits the failure signal and returns the bridge to idle |

At each relevant stage the suite compares persisted metadata and statuses with
the actual prepared/downloaded objects, and compares the rendered cards and
source groups with the database records. It checks unique record identities,
outcome totals, success rate (completed divided by completed plus failed), real
file sizes, activity timestamps, source ordering and empty/disabled states.
Pending and cancelled records are excluded from that success-rate denominator.
Statistics describe the latest record per video URL, not a permanent count of
every retry attempt.

The deliberate download failure is caused by an owned path whose parent is a
file. The provider response and downloader result are never replaced. The
independent source rename is a real edit to the isolated database, not a fake
notification or injected in-memory cache entry.

## Isolation and requirements

Settings, media, partial segments, logs and PocketBase data use an isolated
temporary workspace. The user's existing settings, downloads and history are
not touched. The suite connects the database through the same production
backend binding used at application startup.

Install the project's GUI/development dependencies and have `ffmpeg` and
`ffprobe` on PATH. PocketBase is discovered normally; if absent, the existing
installer downloads the project's pinned binary into the temporary workspace.
You can supply an installed executable with `PORN_FETCH_POCKETBASE_BINARY`.

```bash
# Inventory only: no Qt startup or requests.
uv run python -m src.tests.smoke.statistics_gui --list

# Disabled/empty GUI contract only; HTTP is explicitly rejected.
uv run python -m src.tests.smoke.statistics_gui --offline-only

# Adjust the native bandwidth cap and per-workflow deadline if needed.
uv run python -m src.tests.smoke.statistics_gui --bandwidth 1 --timeout 360
```

The default native media cap is 2 MiB/s, and the per-workflow timeout is 240
seconds. HTTP 429 recovery follows the existing account tests' bounded cooldown
policy and extends deadlines. Explicit access controls and unsupported challenges
stop the run. Recognized HTTP-200 PornHub math responses pass unchanged to the
existing native library handler; see the policy in `LIVE_ACCOUNT_TESTS.md`.

The JSON report defaults to `/tmp/porn-fetch-statistics.json`; diagnostic details
go to the corresponding `.log`. Use `--report PATH` to override this. The report
distinguishes passed, failed, blocked and not-run checks. Dependent checks stop
after a failure, preserving the actual cause instead of cascading fake failures.
The workspace is removed after the run.

The disabled GUI contract also runs in normal offline integration discovery.
Live provider requests and media downloads remain opt-in. These are desktop
checks; Android tracking/statistics remain disabled. This is workflow coverage,
not a claim of 100% Python line or branch coverage.
