# Desktop teardown and recovery

Run the helper and select **Live application teardown and recovery**, or run:

```bash
uv run python -m src.tests.smoke.application_recovery
```

Eight workflows run in 16 independent GUI processes. The first process closes
its native window through the same `ApplicationShutdown.qml` component used by
the desktop app. Production teardown stops that process's actual asyncio loop.
A second process starts from a different working directory and checks recovery.
Requests, provider download methods, filesystem writes and PocketBase are real.

## Coverage

| Workflow | Checks |
| --- | --- |
| Idle | Repeated close starts one teardown; native window, tasks and sessions close; reopening makes no provider requests |
| Preparation | Close while a real Eporner request is active; preparation cancels and reopening does not restart it |
| Pending history write | Close while a real PocketBase write is queued; the write completes and survives reopening |
| Database folder move | Close the real database service before moving its folder; reopen the moved database and verify its history |
| HLS retained | Close a partial PornHub download with a second row queued; restore both paused, resume one, and prove retained segments are not fetched again |
| HLS cleanup | Close with cleanup enabled; verify partial artifacts are removed and explicit Resume downloads the complete segment set |
| RAW retained | Close a partial Eporner transfer; resume through HTTP 206/Content-Range and verify the retained file prefix is unchanged |
| RAW cleanup | Close with cleanup enabled; explicit Resume starts at byte zero |

Completed outputs are probed with FFmpeg. Queued rows must not start writing,
recovered rows must remain idle until clicked, and completion/removal must clear
their recovery records. History must update the existing video record rather
than duplicate it. Every worker checks that application tasks and network
sessions close, and its PocketBase process stops. The supervisor checks child
PIDs and reports a failure if application teardown leaves one running.

The history-write scenario uses a timing barrier before forwarding a real
request, released after window closing begins. This prevents a fast machine
from completing the write before shutdown is tested; no successful database
response is fabricated. The same scenario deliberately generates a password
beginning with `-` to test PocketBase CLI argument handling. The generated
credential stays inside the diagnostic process.

## Recovery behavior

On desktop startup, unfinished rows are restored **paused**, with their original
job identity, selected quality, output path and progress. Startup reads local
metadata only. Clicking Resume obtains a fresh native provider object/session,
checks its available permitted qualities, and uses the retained checkpoint.
If the selected/permitted resolution changes, incompatible HLS segments are
discarded so they cannot be reused under the wrong quality label.
No browser cookies, passwords, native sessions or in-memory provider objects
are serialized in the queue snapshot.

Window closing asks download writers to stop cooperatively and cancels queued
work. It allows up to 30 seconds for active downloads before forced task
cancellation. It then saves the queue, allows pending history writes up to 15
seconds to settle, stops PocketBase, and closes transports and other services.
Repeated close requests reuse the same teardown. New fetch/download work is
rejected during shutdown.

Queue snapshots and HLS checkpoints use Qt's writable generic cache directory
under `PornFetch` (normally `~/.cache/PornFetch` on Linux). Atomic snapshots are
saved off the GUI thread. Output paths are stored as absolute paths; recovery
works independently of the launch directory. RAW checkpoints remain alongside
their output files. Old orphan `.temp` artifacts from earlier builds are not
automatically migrated into a queue that did not previously exist.

Cleanup on stop still applies to active downloads during closing. Its rows can
be restored, but Resume starts a new transfer after their partial files were
removed. Completed and manually removed rows are not restored.

These checks cover graceful native window closing and reopening. They do not
claim power-loss/forced-kill durability, automatic recovery of old orphan
checkpoints, or live shutdown of an activated licensing/Tor/Strict SNI session.
Connectivity-loss testing is separate; this suite does not disconnect the host.

## Running and isolation

Use the project's GUI/development dependencies and FFmpeg. If PocketBase is
absent, the existing installer downloads the pinned binary into the diagnostic
workspace. An installed binary can be supplied through
`PORN_FETCH_POCKETBASE_BINARY`. The default stop-phase media cap is 0.5 MiB/s so
a genuine partial transfer can be observed; explicit recovery is uncapped.

```bash
# Inventory without Qt or requests.
uv run python -m src.tests.smoke.application_recovery --list

# Actual idle close/reopen contract, with HTTP rejected in both workers.
uv run python -m src.tests.smoke.application_recovery --offline-only

# Focus on selected workflows.
uv run python -m src.tests.smoke.application_recovery \
  --case hls-retain --case raw-retain
```

`--timeout` sets each worker's deadline (default 180 seconds). All settings,
cache, media, logs and database folders are isolated. Existing user downloads,
accounts, settings and history are not modified; SpankBang is not contacted.

Default report: `/tmp/porn-fetch-application-recovery.json`. Per-process logs use
the same filename stem. `--report PATH` overrides this. Reports preserve the
original workflow error separately from teardown-verification errors and record
real request/checkpoint reuse evidence without signed CDN query parameters.
Workspaces are removed at completion; reports and logs remain.

The idle contract and queue serialization tests run in normal offline test
discovery. The live workflows remain opt-in. These are desktop checks; Android
device recovery is outside this suite.
