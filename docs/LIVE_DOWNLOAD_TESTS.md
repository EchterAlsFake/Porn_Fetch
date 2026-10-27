# Live download lifecycle tests

This opt-in suite exercises the real CLI download dispatcher and
`DownloadController`, real provider clients, `eaf_base_api`, curl-cffi, and real
media for **all 15 supported providers**. It does not substitute providers,
responses, downloaders or media files. A passive observer records requests while
delegating unchanged to the real transport. These are CLI/controller workflow
checks; they do not drive QML controls or authenticate accounts.

## Run

From the project root:

```bash
uv run python -m src.tests.smoke.download_lifecycle
```

Or select **Live pause/resume and cleanup (15 providers, 30 media workflows)**:

```bash
uv run src/tests/helper.py
```

The helper asks for network and media-download confirmation. Direct invocation
explicitly opts into both. Ordinary unit/integration test discovery and CI do
not run this suite.

FFmpeg must be available through the app's normal binary discovery. It remuxes
HLS output and probes completed videos for a readable video stream and duration.
The probe checks container metadata, not decoding of every frame.

The RAW workflows require the corrected base-api implementation with persistent
RAW checkpoints. After that release is published, refresh the dependency and
project environment:

```bash
uv lock --upgrade-package eaf-base-api
uv sync --extra gui --group dev
```

For sibling source checkouts, the unpublished API fix can be used explicitly:

```bash
PYTHONPATH=../eaf_base_api uv run python -m src.tests.smoke.download_lifecycle --provider eporner
```

The report records both installed versions and the actual `base_api_source`.

## Provider matrix

Each provider runs **pause/resume** and **cleanup/restart** independently, giving
**30 cases**. The maintained single-video fixtures in
`src/cli/selftest/cases.py` supply URLs; PornHub retains its already-verified Short
fixture. The inventory checks that every registered provider has a fixture.

| Providers | Expected transport |
| --- | --- |
| PornHub, XHamster, XNXX, XVideos, SpankBang, Beeg, RedTube, Thumbzilla, Tube8 | HLS |
| Eporner, XFreeHD, Porntrex, EMPFlix, TNAFlix | RAW |
| YouPorn | Record the provider's actual HLS/MP4 selection |

YouPorn can expose an MP4 fallback without resolution metadata. A fixture with
no verified quality at or below 720p fails preparation explicitly; the suite
does not bypass quality restrictions or silently claim coverage of that fallback.

- A full run can complete 30 downloads plus their interrupted first transfers.
- By default every case selects the lowest available resolution, capped at 720p.
  `--quality HEIGHT` requires an exact available resolution at or below 720p.
- Cases run sequentially, with one download worker and disabled response/playlist
  caches, so retained progress cannot be supplied by the HTTP cache.
- Every case owns its core/session and closes it on success or failure.
- Media, checkpoint files and paused jobs use an isolated run directory.
  The runner does not access saved user jobs, browser profiles or accounts.
- Without `--keep-artifacts`, each case's files are removed after its report is
  saved, keeping disk use bounded to one case rather than all 30 outputs.

## What is verified

### Pause/resume

Pause after two HLS segments or a meaningful amount of RAW data, require saved
progress, then resume through the app and require completion without the
existing-file shortcut.

For HLS, inspect saved segment files and require that retained segments are not
requested again. Initial resume progress must include them.

For RAW, require a checkpoint whose byte counts match the paused progress.
Resumed media requests must start after the retained prefix, return HTTP 206,
and have matching Content-Range offsets/total. Initial resume progress must
include retained bytes. The final file length must match the server total and
the retained prefix must remain unchanged.

The observer also counts actual streaming bytes consumed. A headers-only GET
probe used when a CDN rejects HEAD is not mistaken for a full-file re-download;
the resume checks examine the requests whose media bodies were consumed.

A fresh re-download does not pass as a successful resume. Old RAW files without
valid checkpoints are restarted safely by the library, so this suite always
creates new partial downloads before attempting resume.

### Cleanup/restart

Interrupt with `cancel(cleanup=True)`, wait for workers to exit, then require
removal of partial output, HLS segments, assembly temporaries, RAW checkpoints,
state files and the paused-job entry.

Restart and require a complete, readable video fetched using new requests. HLS
must request every segment in its freshly resolved manifest and start progress
from zero/its first segment. Signed URLs and CDN hosts may change between the
interruption and restart; literal URL equality across transfers is not required.
RAW must begin at byte zero. Completion must remove remaining resume artifacts
and the paused-job entry.

## Select providers, workflows or replacement videos

```bash
# Inspect the complete matrix without network requests, downloads or FFmpeg.
uv run python -m src.tests.smoke.download_lifecycle --list

# Run both workflows for one provider and keep files for inspection.
uv run python -m src.tests.smoke.download_lifecycle --provider xfreehd --keep-artifacts

# Select several providers and just the pause/resume workflow.
uv run python -m src.tests.smoke.download_lifecycle --provider empflix --provider tnaflix --scenario pause-resume

# Explicitly check a different rendition when a CDN has broken low-quality media.
# The test fails if this exact resolution is unavailable; there is no automatic fallback.
uv run python -m src.tests.smoke.download_lifecycle --provider spankbang --quality 480

# Replace an unavailable fixture while retaining provider/video validation.
uv run python -m src.tests.smoke.download_lifecycle --provider xnxx --url 'xnxx=https://www.xnxx.com/video-REPLACEMENT/title'

# Add the live execution to an existing Python coverage report.
uv run coverage run --append -m src.tests.smoke.download_lifecycle
uv run coverage html
```

`--provider` and `--url PROVIDER=URL` are repeatable. Omit `--provider`, or use
`--provider all`, for all providers. `--scenario` accepts `all`, `pause-resume`
and `cleanup`. The existing `--hls-url` and `--raw-url` options continue to replace
the PornHub and Eporner fixtures respectively.

## Reports and limits

The JSON report and companion log default to the system temporary directory:
`porn-fetch-download-lifecycle.json` and `porn-fetch-download-lifecycle.log`.
The report is initialized before downloads and updated after each case. It
records planned cases, selected providers, actual transport, library versions,
source checkout, quality, expected duration, progress, reuse/cleanup evidence, HTTP ranges/statuses,
elapsed time and the failing stage. The log contains tracebacks. One failed
provider/workflow does not stop the remaining cases. Failures are not silently
skipped or retried as whole workflows; transport retries remain bounded.

Each finished transfer records its outcome, missing segment indices, HTTP error
counts and first failing URL. A failure such as an HTTP 404 segment response
before the interruption is evidence of unavailable CDN media, rather than proof
that resuming is broken. Such cases still fail; the suite does not discard missing
segments. Check the report and explicitly use `--quality` or `--url` to investigate
another rendition or fixture. Bounded upstream segment retries can still make a
broken HLS fixture take several minutes.

`--report PATH` selects the report destination. `--artifacts-dir DIRECTORY`
selects a parent for a new isolated run directory. `--keep-artifacts` retains all
media and state for inspection; otherwise they are removed and the report/log
remain. `--timeout SECONDS` bounds each download phase (default 600); metadata
calls are bounded to at most 90 seconds each and cooperative shutdown gets an
additional 15 seconds.

Ctrl+C stops the active downloader cooperatively and closes its client session.
The partial report includes the interrupted case with `interrupted: true`,
separately from failed cases, and the command exits with code 130 without a
traceback. `--keep-artifacts` also applies to interrupted runs; otherwise the
isolated run directory is removed after shutdown.
