# Desktop settings tests

Run the helper and select **Complete desktop settings**, or run directly:

```bash
uv run python -m src.tests.smoke.settings_gui
```

The suite loads the production desktop Settings and Downloads pages with the real
backend and provider libraries. It changes all 55 persisted setting properties
through their QML controls/signals. It checks the actual INI file independently
of Qt's shared settings cache, reloads saved values, and checks configuration on
all 15 active provider cores. Application settings such as theme and output path
are checked at their application consumers instead of pretending they configure
provider networking. SpankBang receives configuration checks only; no requests
are made to it.

All settings, output, partial files, logs, caches, certificates, and databases use
temporary directories. Your normal settings, cookies, downloads, and database
are not modified. The suite makes real public provider requests and downloads
real videos; it does not import accounts. Folder selection, temporary-file
cleanup, and Reset Settings also operate only on diagnostic files. Installation
and uninstallation buttons are outside the saved-settings inventory and are not
invoked.

## Checks

| Area | Observable behavior |
| --- | --- |
| Video | Real PornHub downloads at 240p/480p, FFmpeg resolution and metadata, output folders, and skip versus replace of an existing file |
| Profiles | Real profile feeds, selected feed type, result limits, strict source loading, and observed native page/item concurrency |
| Performance | Real native HLS worker concurrency, HLS/RAW parallel limits, preparation/download delay, measured bandwidth, request spacing and timeouts |
| Retries | Real HTTP 503 responses and observed attempts, exponential delays, maximum delay, and native jitter calculation |
| Caches | Real response and provider playlist requests, cache hits, expiry and disabled caches |
| HTTP/TLS | Actual request headers, browser fingerprints, custom JA3 cipher offers, certificate verification, interface binding and environment/custom proxies |
| DNS | Real provider requests using DoH, operating-system DNS, and fallback recovery after an unreachable primary DoH resolver |
| Privacy | Rendered sensitive-text masking, actual ECH ClientHello offers, and real Lite SNI helper routing |
| UI | Rendered font, Material colors, accent, activity glow and translated labels; saved style applied in a fresh Qt process |
| System | Actual log filtering/debug files, suppressed GUI errors, and consent-controlled report delivery to a local receiver |
| Startup | Production QML update gate schedules an actual update task only when enabled; task is cancelled before contacting the update endpoint |
| Tracking | Real PocketBase processes/databases in two selected folders; the startup consumer reads tracking enablement and path from saved settings |

Fault and timing checks use real HTTP/TLS servers on loopback, including actual
self-signed TLS and deliberately slow/error responses. All client requests go
through the installed native library; responses are not mocked. Observers wrap
and delegate real calls. Real provider metadata, profiles, playlists and media
are tested separately where provider behavior matters. Error reporting is sent
only to an isolated local receiver, never production telemetry.

The native segment-cache setting currently caches resolved playlist URL lists;
the suite tests that behavior rather than claiming it caches downloaded media
bytes. ECH checks prove an offer was sent, not successful negotiation or hostname
secrecy. SNI checks prove routing through the selected helper, not censorship
bypass. Language catalogs have English fallbacks for untranslated entries; live
switching is verified using existing production labels translated into German,
French and Chinese.

## Requirements and optional routes

Use the project's GUI and development dependencies. `ffmpeg`/`ffprobe` must be
available, and `openssl` generates a temporary test certificate. If PocketBase
is not installed, the existing installer downloads the project's pinned version
into the diagnostic workspace. You can instead supply its executable through
`PORN_FETCH_POCKETBASE_BINARY`.

The default run verifies effects for 52 of 55 settings. Tor routing and the two
Strict SNI properties are explicitly **UNVERIFIED**, rather than reported as
passed without exercising their routes. Enable those checks only on a machine
with the corresponding runtime and privileges already configured:

```bash
# Bootstrap real Tor; check an onion service and the provider core's Tor route.
uv run python -m src.tests.smoke.settings_gui --tor

# Exercise the real Strict Fragmentation, Reverse and Desync helpers.
uv run python -m src.tests.smoke.settings_gui --strict

# Require actual-effect verification for every setting.
uv run python -m src.tests.smoke.settings_gui --tor --strict --require-all
```

Strict falling back to Lite fails the Strict check. The suite does not elevate
itself or install a privileged backend. Read [SNI setup](../SNI_PROXY_AGENT_HANDOFF.md)
and [Tor support](TOR_SUPPORT.md) before enabling these optional checks. Tor tests
use metadata only, without Tor media downloads. Restart-required settings are
verified by reconstructing their actual consumer or starting a fresh process;
an already-running download is not expected to switch transport mid-transfer.

## Focused and offline runs

```bash
# List the inventory without starting Qt or making requests.
uv run python -m src.tests.smoke.settings_gui --list

# Every setting's QML, disk and runtime contract, with HTTP explicitly rejected.
uv run python -m src.tests.smoke.settings_gui --offline-only

# All persistence checks, but only these live-effect groups.
uv run python -m src.tests.smoke.settings_gui \
  --effect real-media --effect live-parallel
```

The offline contract also runs in ordinary integration-test discovery. Live
effects remain opt-in. Other effect group names appear in the JSON report and
`src/tests/smoke/settings_effects.py`. `--timeout` sets the per-group deadline
(default 180 seconds); rate-limit recovery waits extend it.

Default report: `/tmp/porn-fetch-settings.json`, with diagnostic details in
`/tmp/porn-fetch-settings.log`. Override it with `--report PATH`.
Persistence, active configuration, and observable effects have separate statuses.
The report lists failures, unverified settings, and per-group evidence. An
ordinary exit code of zero means the requested checks had no failures; it does
not imply optional routes were verified. `--require-all` also fails on missing
effect verification. Access denials, CAPTCHA pages and unsupported challenges
stop the run with a partial report. Recognized HTTP-200 PornHub math responses
pass unchanged to the existing native library handler; 429 recovery follows the
account tests' bounded cooldown policy. See `LIVE_ACCOUNT_TESTS.md`.

This is settings checklist coverage, not a claim of 100% Python line or branch
coverage, full localization, or Android device coverage.
