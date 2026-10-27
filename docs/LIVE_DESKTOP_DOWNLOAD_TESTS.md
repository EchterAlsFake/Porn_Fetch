# Live desktop download workflows

Run explicitly from the project root:

```bash
uv run python -m src.tests.smoke.download_gui
```

Or select **Live desktop download controls (14 providers, 42 workflows; SpankBang manual)** in
`uv run src/tests/helper.py`. The helper asks for network/media-download permission.
Normal unit/integration discovery and CI do not run this suite.

This renders the production desktop `DownloadsPage.qml` using PySide6, then
sends real mouse/keyboard events to its controls. It uses anonymous native
clients for all 14 automated providers, real metadata, real media requests,
the production GUI backend and real output files. No provider responses,
prepared rows, download results or media files are simulated. The native HTTP
observer only records requests; isolated real clients are injected into the
normal GUI provider lookup.

The default inventory is **42 automated workflows** (three per provider), plus
**three manual SpankBang workflows**. Fixtures come from the existing live-video
inventory; adding a provider without a fixture fails inventory validation.

| Providers | Transport |
| --- | --- |
| PornHub, XHamster, XNXX, XVideos, Beeg, RedTube, Thumbzilla, Tube8 | HLS |
| Eporner, XFreeHD, Porntrex, EMPFlix, TNAFlix | RAW |
| YouPorn | Verify and record its actual HLS/RAW selection |
| SpankBang | Manual only, due to current website/CDN playback issues |

SpankBang is never contacted by this runner, even with `--provider spankbang`.
The console and JSON `manual_checks` record its cases as `MANUAL`; they never
count as passed. A manual-only selection writes a report without starting Qt,
requiring FFmpeg, or making network requests. Exit code zero means the automated
selection passed (or had no automated work), not that manual cases were verified.

Each provider exercises three workflows:

| Workflow | Evidence |
| --- | --- |
| Pause/resume | Get Video, rendered metadata, actual quality popup selection, row selection and Download Selected, live model/delegate/progress-bar updates, Stop and Resume, retained HLS segments or RAW checkpoint/ranges, readable completed video and automatic row removal |
| Cleanup/restart | Advanced Configuration cleanup checkbox, per-row Download, Stop, absence of output/segments/checkpoints, Resume as a fresh transfer, readable output and automatic clearing |
| Manual removal | Remove a prepared row, reload a real video, remove during transfer, cooperative stop before removal, manager/list consistency and cleanup of partial files |

The stop trigger comes from a real progress notification between 1% and 95%,
then clicks the visible control. If the transfer finishes before interruption,
the case fails rather than claiming pause coverage. HTTP 206/Content-Range and
a retained-prefix hash establish RAW reuse. HLS resume must avoid re-requesting
saved segments. Cleanup/restart must request fresh segments or start at byte zero.
FFmpeg must read a video stream and a plausible duration from each completed
file; it does not decode every frame.

Settings, media, HLS state and RAW checkpoints use temporary directories. Browser
cookies, saved jobs, history, licensing and updater services are not used. Quality
is the lowest reported resolution at or below 720p. Tracking and metadata tagging
are outside this suite's scope. Android device checks are deferred to v4.0.
YouPorn's quality-unknown MP4 fallback cannot establish the free quality limit;
such a fixture fails preparation rather than silently bypassing the limit.

The JSON report and diagnostic log default to:

- `/tmp/porn-fetch-download-gui.json`
- `/tmp/porn-fetch-download-gui.log`

Results are saved after each case. Reports include request evidence with CDN
query parameters removed, stages, reuse/cleanup/removal assertions and media
validation. The local diagnostic log can include upstream URLs and tracebacks.
Artifacts are removed after each case unless `--keep-artifacts` is supplied.
Cooperative shutdown stops writers before closing their sessions or deleting files.
Ctrl+C saves the interrupted result and exits with code 130.

```bash
# Inventory only: no network, Qt startup or downloads.
uv run python -m src.tests.smoke.download_gui --list

# Focus on one provider/workflow.
uv run python -m src.tests.smoke.download_gui --provider eporner --scenario pause-resume

# Focus on several providers; each gets all three workflows.
uv run python -m src.tests.smoke.download_gui --provider xhamster --provider xfreehd

# Record the manual-only exception; makes no requests.
uv run python -m src.tests.smoke.download_gui --provider spankbang

# Require an exact available free resolution, retain artifacts, bound each phase.
uv run python -m src.tests.smoke.download_gui --quality 480 --keep-artifacts --timeout 300
```

`--provider PROVIDER` is repeatable and accepts every registered provider or `all`.
`--scenario` accepts `all` (default),
`pause-resume`, `cleanup`, or `remove`. `--report PATH` changes the report/log
location; `--artifacts-dir DIRECTORY` chooses the parent of an isolated workspace.

Explicit access denials, CAPTCHA pages and unsupported challenges stop the run.
Recognized HTTP-200 PornHub math challenges on HTTPS PornHub hosts pass unchanged
to the existing `eaf_base_api` handler. HTTP 429 recovery uses the
existing account diagnostic guard: at least 30 seconds (or longer Retry-After),
then five-second request spacing with bounded safe-read retries. Intentional
waiting extends the phase timeout. The test guard implements no solver or identity changes.

Once SpankBang playback works in a normal browser, manually repeat all three
workflows above through the desktop page with a working video. Check retained
progress for pause/resume, deleted temporary files for cleanup, and row removal
for pending/active/completed jobs. Until verified, leave the cases marked manual.

These workflows complement the 15-provider CLI lifecycle matrix. Passing
means this defined desktop action checklist works with the selected live media;
it does not mean 100% source line/branch coverage or exhaustive queue coverage.
