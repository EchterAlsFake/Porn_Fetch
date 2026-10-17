# Live profile URL tests

The opt-in suite exercises **33 primary branches across all 13 profile-capable
providers** through the real GUI backend and download list model. Beeg and
XFreeHD have no Model/Channel/Pornstar API; their video/album checks stay separate.

The [JSON inventory](url-routing-audit/profile-fixtures.json) contains 89 records:
33 primary fixtures, 49 variants, six explicit replacements and one empty-listing
diagnostic. Nine unsuitable candidates are retained as negative evidence and
linked to replacements. Positive fixtures deduplicate to 76 distinct URLs.

URLs were sourced from sibling APIs' real network tests and current website
links, then checked locally with bounded curl GET requests and redirects on
2026-10-17. Static parser examples are identified separately. Primary HTTP
results are 27 responses with status 200 and three SpankBang responses with 403.
**403 is access restricted, not an invalid URL**: all three primary SpankBang
branches passed the actual app pipeline and HLS checks.

## What is verified

Each case resolves the provider and profile factory, loads identity metadata,
then calls the real `Backend._process_model_url()` with one page and at most two
videos. The path includes `ProcessVideos`, `DownloadManager`, the backend's Qt
signal and `DownloadListModel`; no prepared videos or list rows are mocked.

The validator checks profile identity, insertion signals, title, author,
duration, video/thumbnail URLs, video ID, tags, qualities, selected quality,
origin identity and output path. It checks the corresponding Qt roles, requires
pending state with zero progress, and checks that no output media file exists.
XNXX's User schema exposes video/page counts instead of a name; those counts
must be positive. Mutable titles and exact listing counts are not hardcoded.

For HLS videos, `get_segments()` must return a nonempty list of absolute HTTP(S)
segment URLs. For direct-file providers and YouPorn's MP4 fallback, a usable
stream URL must resolve without fetching it. A request guard blocks media/segment
GETs, binary reads and download entry points. Thumbnails remain URL metadata;
no images, video segments or MP4 bodies are fetched, and the standalone runner
opens no visible windows.

The live run covered 73 distinct URLs: **70 passed, three skipped, zero failed**.
The three skips are RedTube's numeric User, its playlists-tab variant, and
Tube8's numeric User. Their public profile metadata is verified, and their video
feeds are attempted on every run. RedTube's public page exposes playlists while
its video endpoint requires login; Tube8's public video endpoint returns an
empty unsuccessful response. These skips do not claim successful list coverage
for those two User types. Their public Channel/Pornstar/Amateur cases pass.

## Run explicitly

```sh
uv sync --extra gui --group dev
uv run python -m src.tests.smoke.profile_urls
uv run python -m src.tests.smoke.profile_urls --include-variants
uv run python -m src.tests.smoke.profile_urls --include-variants --filter spankbang
```

`--items 1|2|3`, `--timeout SECONDS` and `--report PATH` bound work and control
reporting. Each case records JSON results as it finishes; verbose diagnostic
output goes to a sibling `.log`. The default report is
`porn-fetch-profile-smoke.json` in the system temporary directory. The process
returns nonzero for failures and counts skips separately. Qt uses the offscreen
platform and the standalone runner isolates configuration/output directories.

The interactive `uv run src/tests/helper.py` also offers this suite. Desktop
flags are `main.py --test-profiles`, `main.py --test-profile-variants`, and the
existing `main.py --test` (video cases plus primary profiles). Live checks never
run implicitly under ordinary unit/integration discovery or CI.

## Primary fixtures

URLs are code text to avoid inline site previews. The two restricted User feeds
are identified above; all other primary branches have list/stream coverage.

| Provider | Type / intended factory | URL | curl |
|---|---|---|---|
| pornhub | model / `get_model()` | `https://www.pornhub.com/model/catalina-days` | 200 |
| pornhub | pornstar / `get_pornstar()` | `https://www.pornhub.com/pornstar/danny-d` | 200 |
| pornhub | user / `get_user()` | `https://www.pornhub.com/users/chappy1918` | 200 |
| pornhub | channel / `get_channel()` | `https://www.pornhub.com/channels/brazzers/` | 200 |
| eporner | pornstar / `get_pornstar()` | `https://www.eporner.com/pornstar/riley-reid/` | 200 |
| eporner | channel / `get_channel()` | `https://www.eporner.com/channel/blacked/` | 200 |
| xnxx | user / `get_user()` | `https://www.xnxx.com/pornstar/cory-chase` | 200 |
| xvideos | channel / `get_channel()` | `https://de.xvideos.com/teddy_tarantino` | 200 |
| xvideos | pornstar / `get_pornstar()` | `https://de.xvideos.com/pornstars/sweetie-fox1` | 200 |
| xhamster | creator / `get_creator()` | `https://xhamster.com/creators/comatozze` | 200 |
| xhamster | pornstar / `get_pornstar()` | `https://xhamster.com/pornstars/polly-yangs` | 200 |
| xhamster | channel / `get_channel()` | `https://xhamster.com/channels/brazzers` | 200 |
| spankbang | creator / `get_creator()` | `https://spankbang.com/kxrn/creator/yvonna/` | 403 |
| spankbang | channel / `get_channel()` | `https://de.spankbang.com/ho/channel/brazzers/` | 403 |
| spankbang | pornstar / `get_pornstar()` | `https://spankbang.com/32/pornstar/angela+white/` | 403 |
| youporn | channel / `get_channel()` | `https://www.youporn.com/channel/mia-khalifa/` | 200 |
| youporn | pornstar / `get_pornstar()` | `https://www.youporn.com/pornstar/eva-elfie/` | 200 |
| porntrex | model / `get_model()` | `https://www.porntrex.com/models/rose/` | 200 |
| porntrex | channel / `get_channel()` | `https://www.porntrex.com/channels/brazzers/` | 200 |
| redtube | channel / `get_channel()` | `https://de.redtube.com/channels/freeuse` | 200 |
| redtube | pornstar / `get_pornstar()` | `https://de.redtube.com/pornstar/leny+evil` | 200 |
| redtube | amateur / `get_amateur()` | `https://de.redtube.com/amateur/littlereislin-ph-2` | 200 |
| redtube | user / `get_user()` | `https://www.redtube.com/user/31618721` | 200 |
| thumbzilla | channel / `get_channel()` | `https://www.thumbzilla.com/channel/brazzers/` | 200 |
| thumbzilla | pornstar / `get_pornstar()` | `https://www.thumbzilla.com/pornstar/nancy-a/` | 200 |
| thumbzilla | amateur / `get_amateur()` | `https://www.thumbzilla.com/amateur/0princesspeachy0-ph/` | 200 |
| tube8 | channel / `get_channel()` | `https://www.tube8.com/channel/brazzers/` | 200 |
| tube8 | pornstar / `get_pornstar()` | `https://www.tube8.com/pornstar/nancy-a/` | 200 |
| tube8 | amateur / `get_amateur()` | `https://www.tube8.com/amateur/e6cd031-ph/` | 200 |
| tube8 | user / `get_user()` | `https://www.tube8.com/user/31618721/` | 200 |

## Replacements and exclusions

All six replacements for the originally excluded candidates returned HTTP 200
with local curl. Further GUI checks found an empty Porntrex channel, an
unsupported Eporner User page and a RedTube alias with unknown identity. Their
alternatives are included too; exclusions remain in the JSON with `replaced_by`
and reciprocal `replaces` links.

| Excluded candidate | Reason | Positive alternative |
|---|---|---|
| `https://www.pornhub.com/user/617235451/` | unavailable candidate | `https://www.pornhub.com/users/chappy1918` |
| `https://www.eporner.com/profile/BALove_PMV/` | unsupported resource | `https://www.eporner.com/channel/blacked/` |
| `https://www.xnxx.com/profile/alex_adams69` | unavailable candidate | `https://www.xnxx.com/pornstar/alex_adams69` |
| `https://de.xvideos.com/teddy_tarantino/videos/best/0` | unavailable candidate | `https://www.xvideos.com/channels/teddy_tarantino/videos/best/0` |
| `https://www.redtube.com/channel/vip-4k` | unavailable candidate | `https://www.redtube.com/channels/vip-4k` |
| `https://www.redtube.com/users/31618721` | identity unverified | `https://www.redtube.com/user/31618721` |
| `https://de.thumbzilla.com/channel/brazzers/` | transport inconclusive | `https://www.thumbzilla.com/channel/brazzers/` |
| `https://www.tube8.com/user/midnightmusex/` | identity unverified | `https://www.tube8.com/user/31618721/` |
| `https://www.porntrex.com/channels/nubile-films/` | empty listing | `https://www.porntrex.com/channels/brazzers/` |

The Tube8 replacement verifies a real identity, but its User feed remains an
explicit skip. An available public Channel/Pornstar case cannot establish User
feed support. Eporner `/profile/` is a different, unimplemented User abstraction;
it is rejected rather than incorrectly passed to `get_channel()`.

## Variants and application fixes

- Localized hosts, aliases, redirects, slash/page forms, sorting/quality filters
  and share query/fragment inputs are represented. Derived URLs are labelled;
  they are not presented as links copied from the website.
- Eporner's real German `/pornostar/` path and localized `/porno-video/` video
  paths now resolve correctly. Case-sensitive API IDs are retained even when a
  listing supplies a different numeric HTML `data-id`.
- PornHub, XNXX and XVideos AJAX/video tabs resolve identity through the base
  profile. Queries and case are retained; PornHub's requested upload mode stays
  separate from redirects, and iterator bounds apply to uploads too.
- XHamster User pages follow their explicitly linked Creator identity from the
  personal-info block. Unrelated recommended Creator links are not used.
- Porntrex's old Nubile Films fixture currently lists no videos; the primary
  channel fixture is now Brazzers, verified through the actual list pipeline.
- XVideos' bare channel tab returned 404, while its `/channels/` equivalent
  returned usable listing JSON. Thumbzilla's guessed `de.` host failed DNS;
  the canonical host is used instead.

Fixed provider/core releases are required in `pyproject.toml` and `uv.lock`, with
HLS support enabled. The JSON is included in wheels and desktop build specs so
the desktop diagnostics can run from packaged applications too.

## Recheck HTTP observations separately

```sh
python docs/url-routing-audit/check_profile_fixtures.py
python docs/url-routing-audit/check_profile_fixtures.py --include-variants
python docs/url-routing-audit/check_profile_fixtures.py --case pornhub.model --case spankbang.channel
```

This text-only checker stores response bodies temporarily and never follows
page links. It reports HTTP status, redirects and transport errors to
`/tmp/porn-fetch-profile-url-checks.json`; it does not assert GUI success or
silently overwrite the dated fixture observations.
