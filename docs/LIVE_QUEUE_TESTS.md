# Live desktop queue and concurrency tests

```bash
uv run python -m src.tests.smoke.download_queue
```

The helper also offers **Live desktop queue and concurrency (limits 1/2,
stop/remove isolation)**, with its existing network/media-download confirmation.
Normal offline tests and CI do not start this suite.

All three cases load four real rows through Get Video: PornHub HLS, Eporner RAW,
PornHub HLS, Eporner RAW. Each row has a separate native media object and output
filename. They exercise Select All, Clear Selection, individual checkboxes,
Download Selected and its duplicate-start guard. Jobs are addressed by stable
IDs even as completed/removed rows change their indices.

| Case | Required evidence |
| --- | --- |
| `parallel-1` | Exactly one native transfer active; the other selected jobs queue without media output; every selected job eventually completes once; the unselected fourth row stays untouched |
| `parallel-2` | Two overlapping native download calls, never more than two; queued work starts as slots become available; selection, completion removal and numbering remain correct |
| `stop-remove` | Remove the fourth queued job without waiting for active work or starting its downloader; stop the active RAW job; remove the active first HLS job while the other HLS job has partial progress; the surviving job continues and completes |

Native provider methods are wrapped only to count entry/exit and forward the
original arguments, results and exceptions. Real HTTP/media requests are
attributed to their owning download task with a ContextVar, including child HLS
workers. No native downloader, response, progress update or media file is
substituted. Every completed output must contain a readable video stream and a
plausible duration according to FFmpeg. Completion must remove resume artifacts.

The default native HLS bandwidth setting is 1 MiB/s per core so stop/removal
can be observed before the short fixture finishes; there are no injected success
responses or artificial progress callbacks. This is not a speed benchmark. A
fixture that finishes before the required concurrent interaction fails explicitly.

Settings, outputs and checkpoints use isolated temporary directories. No browser
cookies, saved jobs, licensing or download tracking are used. SpankBang is not
contacted; its desktop lifecycle workflows remain manual. Android device testing
is deferred to v4.0.

```bash
# Inventory only, without Qt startup or network requests.
uv run python -m src.tests.smoke.download_queue --list

# Select one case, bound each phase and retain files for inspection.
uv run python -m src.tests.smoke.download_queue --case stop-remove --timeout 180 --keep-artifacts
```

`--case` is repeatable; default is all three. `--quality HEIGHT` requires an exact
available resolution at or below 720p. `--bandwidth MIB_PER_SECOND` changes the
native HLS bandwidth setting. `--report PATH` changes the JSON/log location;
`--artifacts-dir DIRECTORY` selects the parent of an isolated workspace.

Default reports are `/tmp/porn-fetch-download-queue.json` and
`/tmp/porn-fetch-download-queue.log`. Reports are saved after each case and record
the selected parallel limit, actual peak native concurrency, per-job call intervals,
selection/cancellation/removal evidence, request attribution and media validation.
The local diagnostic log may include upstream URLs and tracebacks. Files are
removed unless `--keep-artifacts` is set. Ctrl+C stops writers before closing
sessions, saves an interrupted result and exits with code 130. Access restrictions
stop the run; HTTP 429 uses the bounded cooldown policy from the desktop lifecycle
suite. Manual cases or interrupted/blocked work never count as passes.

The deterministic queue regression also verifies that a cancelled semaphore wait
finishes without releasing the unrelated active slot, both before and after the
queued coroutine starts. This guards prompt cancellation without simulating a
successful provider download.
