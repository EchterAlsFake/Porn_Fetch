# Public model and playlist workflows

Run from the project root:

```bash
uv run python -m src.tests.smoke.collections_gui
```

The helper offers **Live model/playlist end to end** with explicit network and
media-download confirmations. This suite renders the production desktop
DownloadsPage and StatisticsPage, clicks their actual source, cancellation,
quality and selection controls, and uses the real provider libraries, media,
FFmpeg and PocketBase. Browser cookies and account sessions are not needed.
Normal CI and unit/integration discovery never run these live downloads.

Each supported public source exercises this checklist:

| Check | Evidence |
| --- | --- |
| Source submission | Actual model/playlist input and button, busy state, duplicate submission rejection, rendered title/author/duration/quality roles and original source identity |
| Result limit | Three real rows when available; no output files during preparation |
| Filters | Anchored title/author expressions select the expected actually fetched candidate; a rejecting expression produces no rows |
| Inclusive range | Source positions 2–3 retain their original indexes and filename prefixes |
| Cancellation | Cancel Loading after a real row arrives, cancelled native task, idle controls and a stable list |
| Pagination | Native first-page extraction followed by real later-page rows. Overlapping prefixes are allowed, but the GUI must load a genuinely new video; a fully repeated page fails. A genuinely empty later page is reported as end of source, not as later-page coverage |
| Selected download | Actual quality popup and Select All/Clear/individual selection; only the selected source row calls the native downloader, produces readable media, and automatically clears |
| History/statistics | Real REST records retain source URL/name and source relations, exactly one completion is stored, and the production dashboard displays matching totals/source groups |

The result limit bounds candidates examined within the selected range, rather
than the number accepted by filters. Pagination intentionally consumes the real
first page before preparing the next two entries. It never truncates a native
page to manufacture pagination. If those entries overlap page one, the test uses
the native page's actual identities to set another GUI range covering its first
new entry. The report records the overlap and selected source position. This may require substantial metadata traffic,
particularly for providers that eagerly load skipped entries.

The inventory covers all 13 supported profile providers and all five supported
playlist providers. It has 16 automated source workflows, one manual source
(SpankBang), and one unverified source (Thumbzilla playlists). Beeg and XFreeHD
have no public profile/playlist route in the application. One representative
public profile per provider is used; the separate 76-case profile smoke suite
retains the larger URL-alias/localization matrix.

SpankBang always remains MANUAL and makes no automated website requests.
Thumbzilla's library exposes playlists, but no usable public fixture was found
or supplied. Its channel is tested; its playlist remains UNVERIFIED. A supplied
public fixture can enable that case with `--source thumbzilla.playlist=URL`.
Neither state counts as passed. A selection containing only these entries writes
a report without starting Qt or requiring FFmpeg/PocketBase/network requests.

```bash
# Inventory only; no Qt or network.
uv run python -m src.tests.smoke.collections_gui --list

# Focus providers or source kind.
uv run python -m src.tests.smoke.collections_gui --provider eporner
uv run python -m src.tests.smoke.collections_gui --provider xvideos --kind playlist

# Replace a public fixture without changing provider code.
uv run python -m src.tests.smoke.collections_gui \
  --provider redtube --kind playlist \
  --source redtube.playlist=https://www.redtube.com/playlist/273511

# Offline production-control contracts, also run by integration discovery.
uv run python -m src.tests.smoke.collections_gui --offline-only
```

`--provider` is repeatable. `--kind` accepts `model` or `playlist`. `--timeout`
(default 600 seconds) bounds each entire source workflow, and `--report PATH`
changes the JSON/log location (default `/tmp/porn-fetch-collections.json` and
`.log`). Stage progress and partial results are saved during execution. Native
page indexes, non-sensitive pagination parameters and hashed video identities
are recorded. Logs may include full upstream URLs and tracebacks. Temporary
settings, caches, media and databases are removed after the run; personal state
is untouched. Lowest available reported quality at or below 720p limits transfers.

Explicit access controls stop that provider; later cases for it are BLOCKED,
while independent providers may continue. The recognized HTTP-200 PornHub math
payload on HTTPS `pornhub.com` hosts is delegated to the existing native
`eaf_base_api` handler. CAPTCHA pages, unsupported scripts and HTTP denials still
stop the provider. Each case's `native_challenges` records delegations without
tokens/cookies. The test guard implements no solver. HTTP 429
uses the existing bounded account diagnostic recovery: at least 30 seconds of
cooldown followed by at least five seconds between requests. Intentional waits
extend deadlines. Ordinary upstream HTTP/parser failures remain failures and
are not reclassified as success. A failed or blocked automated case exits with
code 1; Ctrl+C saves the partial report and exits with code 130.

The initial verification found a native RedTube parser bug: playlists use
`ul#playlist_videos` rather than the profile's `ul.videos_grid`. The fix and offline
regressions are in the sibling `unofficial-api-for-redtube` checkout. Until it is
released and installed, use that actual source directly:

```bash
PYTHONPATH=/home/asuna/PycharmProjects/unofficial-api-for-redtube \
  uv run python -m src.tests.smoke.collections_gui --provider redtube --kind playlist
```

The XVideos library checkout at
`/home/asuna/PycharmProjects/unofficial-api-for-xvideos` now exposes `Video.author_name`
from the video page's uploader label. Porn Fetch uses it to avoid requesting a
separate channel/statistics feed for every prepared video. Older library versions
or pages without that label retain the native author lookup. The profile feed can
still return intermittent upstream HTTP 500s; required feed failures remain failures.
The library also waits for the underlying scraper to close when profile iteration
stops early, preventing leftover prefetches from racing the next source request.
The cancellation check reports early task completion/cancellation immediately
instead of waiting out the entire workflow timeout for a row that cannot arrive.
Until the library fixes are released and installed, use both checkouts:

```bash
PYTHONPATH=/home/asuna/PycharmProjects/unofficial-api-for-redtube:/home/asuna/PycharmProjects/unofficial-api-for-xvideos \
  uv run python -m src.tests.smoke.collections_gui
```

Earlier PornHub runs were incorrectly blocked by the test guard before the
native math handler could run. The guard now recognizes that specific native
protocol. PornHub video identity comparisons retain `viewkey`; discarding all
query parameters had made different videos appear identical during pagination.
Other tracking parameters are discarded before hashing identities.
The XNXX fixture now uses the existing Alex Adams profile after the Cory Chase
endpoint returned HTTP 500. One run timed out before cancellation could obtain
a row; a subsequent bounded run completed the entire real workflow successfully.

This is a defined action checklist, not a claim of 100% line/branch coverage.
Android device checks, licensing lifecycle, forced-kill recovery and packaged
CLI/GUI update verification are outside this suite's scope. The latter will be
checked separately using the user's GitHub builds.
