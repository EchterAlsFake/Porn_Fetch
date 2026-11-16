# Pagination investigation and proposed migration

Investigated 2026-11-14. This is a design report, not an implementation or a
claim that all existing pagination works. No provider behavior was changed.

## Recommendation

Standardize the public listing contract across the 21 providers in Porn Fetch's
`pyproject.toml`, and implement pagination scheduling once in eaf-base-api.
Keep each website's route building, response parsing and terminal evidence in
its provider. Different wire mechanisms are necessary; different meanings for
`pages` are not.

Use this interface on video lists, profiles, collections, search, directories,
account feeds, shorts and image lists wherever the provider actually offers them:

```python
container.videos(pages=1, *, start_page=1, iterator_config=None)
container.videos(pages="all", *, start_page=1, iterator_config=None)
```

Existing method names can remain (`get_videos`, `search`, etc.). `pages` is a
positive integer counting source listing pages from the starting position, or
exactly `"all"`. Public page numbering starts at one; providers translate to
zero-based paths internally. Reject booleans, fractions, numeric strings, zero
and negatives in the final contract. Default to one page in the next breaking
release. Keep ordering, loading, retries and concurrency in `IteratorConfig`.
Do not add frontend keyword search: the library contract and application policy
are separate.

A valid exhausted listing yields no items. A missing profile, unexpected redirect,
challenge page, parser failure or failed request must remain an error. A requested
page budget being consumed is different from confirmed exhaustion.

## Scope and evidence

- Audited source interfaces for all 21 provider dependency names;
  Porngo is present in the workspace but is not a Porn Fetch dependency.
- Read the shared Helper scheduler, IteratorConfig, provider routing, creator
  discovery and frontend page limits. Source inventory includes commit IDs,
  method signatures and line locations. Local uncommitted changes may exist;
  a commit ID alone does not describe those changes.
- Made 76 recorded HTML/feed requests across 59 probe cases, plus six recorded
  JSON listing requests and an ordinary RedGIFs anonymous-token bootstrap.
  Redirect chains are handled by the HTTP client and are not separately counted.
- Every provider received live requests. RedGIFs and Beeg return application
  shells in HTML, so HTML alone cannot establish their pagination.
- Requests used curl_cffi with Chrome impersonation, four workers at most and
  25-second timeouts. No browser cookies, credentials or protection bypasses.
- `live-observations.json` preserves requested/final URLs, status, title, response
  sizes and hashes, plus sanitized API pagination observations. Raw temporary
  captures remain under `/tmp/pagination-audit`; they are not repository fixtures.
- This was representative mechanism and boundary investigation, not exhaustive
  testing of every method, sort, locale, account or every page of every profile.
  Production extractor counts below are diagnostics unless independently
  reconciled. No downloads or unrelated full provider suites were run.

## Confirmed problems

### Eporner truncates an apparent all-pages scan

`BaseProfile._load_html` takes the largest visible numbered link as `total_pages`.
For Riley Reid, page one exposes links through 9. Requests to pages 9 and 10
both contain videos; page 9 exposes links through 14, page 10 through 15.
The production extractor returns 38 entries on each of pages 1, 9 and 10.
Those counts alone do not prove that every entry belongs to the main listing,
but the moving pagination window proves that 9 is not the terminal page.
`videos(pages=0)` therefore uses an incorrect stopping bound on this sample.
Follow the actual next link until a verified terminal page. A visible maximum
is a discovered lower bound, not a total.

### Porn Fetch and PornHub disagree about `all`

`src/shared/creator_scans.py` maps PornHub to `"all"`, but the local PornHub
profile/channel/playlist methods use `range(1, pages + 1)` with integer arguments.
Routing does not translate that sentinel. This path can fail with a type error.
The creator scanner is an existing untracked workspace file; it was not created
or modified for this investigation. Its other legacy-provider path repeatedly
fetches prefixes of 1, 2, 4, ... pages and eventually reports coverage unverified.
New pagination should eliminate this replay as a way to discover the next page.
Identity membership remains useful for recovery over changing feeds.

### XVideos search silently caps `all`

`Client.search` turns `pages="all"` into ten pages. It also accepts numeric
strings and silently falls back to two pages for other values. That contradicts
exhaustive scan semantics and hides invalid input. Profiles have separate
zero-means-all behavior; playlists use integer-only finite ranges.

### Shared infrastructure cannot discover pages dynamically

`Helper.iterator` accepts a `Sequence[str]` and materializes it as a tuple.
It schedules a fixed URL list. Providers consequently duplicate discovery loops,
preflight requests, page-count inference, validation and stream wrapping.
`IteratorConfig()` defaults to completion order and yielded errors;
`make_iterator_config()` defaults to original order and skipped errors.
Pagination completion cannot be inferred from item iteration alone, especially
when page failures are skipped.

### Status, visible links and item counts are insufficient terminal signals

- Pornhat Armani Black page 4 is HTTP 200; page 5 is HTTP 404.
- Porndoe Eva Elfie pages 1 and 4 produce 24 and 11 entries; page 5 is HTTP 200
  with zero entries. Its pager still contains earlier page links.
- EMPFlix Dani Daniels pages 1/2 produce 60/59 extractor entries; pages 3/4
  are HTTP 200 with zero entries, even though page one advertised page 3.
  An advertised maximum can overestimate as well as underestimate.
- YouJizz Abby Marie has six listing entries on page one, zero on page two,
  both HTTP 200.
- Bellesa zero-to-hero API pages 1/2/3 contain 24/6/0 items. Headers explicitly
  report 30 items, 24 per page, two total pages, and the requested current page.
- RedGIFs nickiipeach reports one page and 17 items; requesting page two still
  returns HTTP 200 and metadata `page=2, pages=1, total=17`. Inspect metadata;
  HTTP success alone does not mean that a requested page exists.

## Provider-by-provider findings

All rows refer to local source plus the live samples in the evidence JSON.
A mechanism observed on one content type does not establish every other type.

| Provider | Current pagination | Live observation and required change |
| --- | --- | --- |
| Beeg | No paginated listing interface in current wrapper | Homepage is a small JS shell. No pagination migration for existing single-video API; discovering a catalog API would be separate functionality. |
| Bellesa | `pages=1`, `start_page=1`, `"all"`; header-bounded JSON lists | Channel HTML resolves to `/videos?providers=zero-to-hero`; its observed page-two link preserves that filter. JSON boundary verified above. Retain header validation; share scheduling and reuse first response. |
| EMPFlix | Integer pages, default 1; `?page=N` | Profile pages 1/2 differ; 3/4 empty. Existing `is_next_page` helper has no caller. Add next/empty-state adapter and start/all support. |
| Eporner | Profiles default `pages=0` for all; search defaults 2 and uses public JSON API | Profile uses numbered path segments and a moving link window. Remove max-visible-link total inference; use next links. Search needs separate API metadata adapter. |
| Porn.com | `pages=1`, `start_page`, `"all"`; sequential `?pg=N` | Collection, channel and pornstar next links work. Existing implementation deliberately probes beyond missing navigation because links can underreport content. Preserve this provider-specific rule and distinguish native scenes from external referral cards. |
| Porndoe | Usually `pages=2`, `start_page`, `"all"`; preflight HTML total then fixed URLs | Star/channel `?page=N` and explicit Last links observed. Empty beyond last verified for star. Preserve filter/tab and validate returned current page; reuse initial response. |
| Pornhat | `pages=1`, `start_page`, `"all"`; preflight total then fixed URLs | Model/channel numbered path links observed, model terminal 404 verified. Preserve named listing-region validation and bound before requesting beyond-last. |
| PornHub | Integer ranges, generally default 5; profiles and accounts differ from playlist chunks | Model fixture redirects to `/pornstar/teddy-tarantino`; playlist HTML is live. Chunk method uses `/playlist/viewChunked` and a page token. Add all/start and independent adapters per tab/chunk endpoint; validate redirect identity/type. Playlist chunk exhaustion is not yet live reconciled. |
| Porntrex | Integer ranges default 2; KVS AJAX block with `from=NN` | HTML exposes separate video and album pagers using data parameters and fragment links. Existing video-block page-two request returned HTTP 200 fragment. Read block-specific data parameters and terminal navigation; do not mix album counts. |
| RedGIFs | `pages=1`, `start_page`, `"all"`, `count`; API `pages` bounds | HTML user/niche/collection are shells. Anonymous public user JSON reports page/pages/total and also cursor fields. Keep documented integer paging for these routes; validate each response, exclude promoted/prefetched lists, preserve mixed collection item semantics. Cursor fields do not prove that this route requires cursor pagination. |
| RedTube | Integer ranges default 2; `?page=N`; separate playlists | Actual channel `/channels/freeuse` and page two work, German next navigation retains locale. Add shared start/all and pager parsing. Initial `/users` directory probe was 404; that is not a pagination failure. |
| SpankBang | Profiles default 0 but fetch at least one page; search default 2 | Creator page one returned HTML; page two returned 403. Missing generic next anchors does not establish exhaustion. Confirm current listing request through ordinary browser network inspection before implementing terminal rules. No bypass attempted. |
| Thumbzilla | Integer ranges default 2; legacy iterator-config alias | Channel/pornstar numbered query links observed; channel page two works. Parse actual pager controls, not unrelated video links whose classes include “page”. Add start/all consistently to profiles/playlists/search. No public playlist reconciliation here. |
| TNAFlix | Integer ranges default 1; `?page=N` | Channel pages 1/2 and next links work. Like EMPFlix, an unused next-page parser exists. Connect adapter to scheduler and verify terminal empty state. |
| Tube8 | Integer ranges default 2; `?page=N` | Team Skeet channel and page two work. `/channels/` directory probe was 404; real singular `/channel/.../` works. Distinguish profile HTML and any `videos-data` feeds. |
| XFreeHD | Search integer ranges default 5; album exposes a single page getter and separate all-image iterator | Homepage next link is `/page=2`, not a query parameter. Search and album code use query pages. Do not impose homepage routes on those endpoints; unify album bounds/error behavior and stream contract. Search/album terminal cases still need targeted live verification. |
| XHamster | Integer ranges default 2; profile paths, search query, separate shorts | Creator links go `/creators/comatozze/2`; pages 1/2 work. Keep profile/search/shorts adapters separate; initial-state metadata and next links should drive completion. |
| XNXX | Profiles `pages=0` all; zero-based JSON feed; search has different zero behavior | Cory Chase JSON feed pages 0/1 report `current_page=0/1`, `nb_videos=3572`, `nb_per_page=50`, 50 videos each. Normalize public numbering; use feed metadata rather than page-card count. |
| XVideos | Profiles zero-means-all; finite playlist ranges; search `all` capped at 10 | Playlist navigation displays page 2 as path `/1`, last link `/175`. Correct normalized profile JSON route `/channels/teddy_tarantino/videos/best/0` reports 270 total, 36 per page; page 1 is distinct. Bare profile JSON path returned 404, so preserve canonical section normalization. |
| YouPorn | Integer ranges default 2; search default 0 still means at least one | Channel and collection query page-two requests work. Add start/all and endpoint-specific terminal signals; keep collection scope separate from recommendations. |
| YouJizz | `pages=1`, `start_page`, `"all"`; sequential numbered HTML; user IDs chunked locally | Popular-list next link works. Star has six results and empty next page. Public user endpoint returns 544 IDs; wrapper slices them into batches of 24, so its pages are logical batches, not HTML pages. Document batch size and preserve full ID ordering. |

## Complete small-profile comparisons

The final BaseCore runs passed both ordered comparisons with no missing or
unexpected URLs:

| Profile | Independent HTML page sizes | API count | Result |
| --- | --- | --- | --- |
| Porndoe Eva Elfie | 24, 24, 24, 11 | 83 | 83/83, exact order |
| Pornhat Armani Black | 59, 59, 59, 24 | 201 | 201/201, exact order |

These checks cover four pages of each selected profile and `pages="all"`,
with listing-only media construction. They do not establish every profile type,
filter or ordering mode. Counts are live observations, not fixed future fixtures.
See `profile-reconciliation.json`. These additional BaseCore requests are separate
from the 76 recorded HTTP probe responses above.

## Shared design

Add a small listing/page abstraction to eaf-base-api, beside the existing media
pipeline. A provider adapter should produce a parsed page with:

- Listing entries, requested and resolved page identity, and logical page number.
- An explicit next request or confirmed terminal state; unknown remains unknown.
- Optional trustworthy total pages/items, page size, and server current-page value.
- The provenance of totals and terminal decisions, including whether counts include
  external cards, unavailable entries, images, duplicates or promoted content.

Requests must be representable with method, URL and relevant body/headers/context;
keep tokens and cursors opaque and out of logs. All runtime HTTP stays in BaseCore.
Keep raw listing entries separate from loaded media so pages can be inspected
without fetching every detail page. Reuse Helper's item processing and cleanup;
do not implement another HTTP/retry stack.

For verified indexed feeds, schedule lazily with bounded concurrency once a reliable
bound is known. For next-link/cursor feeds, discover pages sequentially and retain
concurrent item processing. Do not materialize huge URL lists or issue requests
past a known terminal bound. Reuse the discovery response instead of fetching it
again; caches are not a guarantee against redundant requests.

For truly cursor-only feeds, `start_page>1` must walk prior cursors, or use a
validated opaque continuation. Never manufacture a cursor from a page number.
No currently tested route requires exposing cursor syntax to ordinary callers.

Track completion explicitly: exhausted, requested limit reached, cancelled, or
failed/incomplete. Consider a stream summary with last source position and failure
counts; retain existing `ScrapeResult` items for compatibility. A skipped page
error must prevent an “exhausted” success summary. Full scans should raise or yield
visible errors and require the caller to check the summary before claiming coverage.

Detect repeated request identities, wrong server page numbers, wrong-resource
redirects and repeated full listing signatures. These indicate a loop or an
unreliable boundary; they should fail/invalidate completion, not silently end.
Do not use a page with no *new* identities as a universal terminal rule: pinned
items and overlapping pages occur. Prefer explicit next/terminal metadata.
Do not stop on a short page unless that endpoint's semantics justify it.

Preserve source order by default for listing methods, with explicit completion-order
opt-in. Page indexes must stay consistent across a multi-page stream, rather than
resetting for each internal Helper call. Deduplication should be explicit and use
stable provider IDs, preserve the first occurrence, and expose duplicate counts;
page budgets always count source pages before filtering/deduplication.

## Rollout and acceptance

1. Implement the shared validator, dynamic page scheduling, completion reporting,
   and response reuse in eaf-base-api. Preserve existing fixed-URL Helper callers.
2. Migrate two contrasting providers first: Bellesa for trustworthy indexed headers,
   Porn.com for sequential discovery with unreliable last links. Validate complete
   small listings before treating this as the cross-provider contract.
3. Fix Eporner truncation and XVideos `all` cap; add PornHub all/start support and
   reconcile canonical profile tabs and playlist chunks. These are priority defects.
4. Migrate simple query/path providers, then KVS blocks, JSON profile feeds and
   local YouJizz batches. Keep each route's independent terminal semantics.
5. Migrate Porn Fetch GUI/CLI/creator scans to the same options. Remove provider
   sentinel tables and geometric prefix scans only after migrated minimum package
   versions are required everywhere, including mobile dependency snapshots.
   GUI currently uses 30-page budgets and CLI commonly uses five; keep preview
   policy explicit instead of silently converting all interactive loads to full scans.
6. Deprecate legacy zero sentinels and inconsistent defaults for one compatibility
   window, then remove in a coordinated breaking release. Map old zero behavior
   per method; zero currently does not mean the same thing everywhere.

Use live checks for each distinct endpoint family, not just each provider name.
Required cases: first/second/middle/terminal/beyond-terminal; finite counts and
start offsets; empty and one-page lists; partial last page and exact size multiples;
filtered and sorted routes; localized hosts; duplicates/pinned/promoted cards;
wrong-page redirects; errors, cancellation, early close and bounded prefetch.
Compare independently extracted listing-region IDs to the public API page by page
and across complete small profiles/collections. Check that source filtering and
mixed collections do not change page accounting. Verify cached and uncached runs.
No saved-response or mock tests were introduced for this investigation.

Remaining gates: SpankBang second-page access; live PornHub playlist chunk
reconciliation; authenticated account feeds; XFreeHD search/album boundaries;
complete per-type profile/collection reconciliation for providers beyond the
small examples recorded separately. The report establishes the direction and
specific defects; it does not certify every existing API route as correct.

## Reproduction commands

Investigation scripts and raw captures are temporary, not production tests:

```sh
Porn_Fetch/.venv/bin/python /tmp/pagination-audit/probe.py
Porn_Fetch/.venv/bin/python /tmp/pagination-audit/followup.py
Porn_Fetch/.venv/bin/python /tmp/pagination-audit/boundaries.py
Porn_Fetch/.venv/bin/python /tmp/pagination-audit/json_probe.py
Porn_Fetch/.venv/bin/python /tmp/pagination-audit/profile_check.py
```

The first four scripts perform representative HTTP probes, not pass/fail suites.
`profile_check.py` compares independently selected HTML listing URLs with deferred
API objects using local provider sources and BaseCore, original order, single-page
concurrency, visible errors and stream closure. It fetches listing pages only,
without loading video detail pages. Its first run exposed a harness error using
an async generator as a context manager for Porndoe; the rerun uses `aclosing`.
This also illustrates the current inconsistency between async generators and
ScrapeStream return values.
