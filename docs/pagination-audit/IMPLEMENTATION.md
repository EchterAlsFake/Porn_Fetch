# Pagination implementation and live verification

Updated 2026-11-15. The implementation is in the workspace and installed into `Porn_Fetch/.venv` from editable sibling sources. **The unconditional all-routes completion gate is not met.** Public pagination has passing nonempty examples for every provider that exposes it, but the external and fixture limits below remain.

## Implemented contract

- Migrated 106 listing methods across 20 providers. Beeg exposes no paginated listing API and is unchanged. Porngo is outside Porn Fetch’s dependency list.
- `pages` is a positive integer or exactly `"all"`; `start_page` is a positive one-based integer. Defaults are one source page. Existing names and raw photo/image interfaces remain. Image aggregation retains its existing all-images default.
- Shared lazy discovery reuses each fetched listing response with the existing Helper item pipeline. Repeat detection retains page digests; optional item deduplication retains stable identities. Item loading/concurrency/order remain in `IteratorConfig`; ordinary provider defaults preserve source order.
- `PaginatedStream.summary` separates exhaustion, a requested page limit, failure/incomplete output and cancellation. Skipped page/item errors become visible yielded errors. A requested finite limit cannot establish completeness.
- Explicit source bounds take precedence over empty filtered pages. Ordinary next links, JSON page metadata, response headers, KVS blocks, chunk endpoints and YouJizz’s native all-ID list each have source-specific adapters.
- A 404 after an advertised next link is an error. Only explicit speculative probes or a validated initial out-of-range request may use a provider’s terminal-error rule. Repeated payloads require a separately parsed source page number; repeated URLs still fail.
- Porn Fetch creator scans use a single `pages="all"` traversal and stable identity deduplication. Existing interactive page limits remain application policy. No frontend keyword search was added.

## Live defects found and fixed

1. Eporner’s moving link window and XVideos’ hardcoded ten-page cap truncated full scans. Navigation now controls completion.
2. PornHub aliases dropped pagination tabs. Profiles resolve their canonical identity before building tab URLs.
3. PornHub uploads contained both `#moreData` and ordinary numbered links. Treating the container as terminal stopped after page one; the corrected full scan yields 369 videos over ten pages.
4. Empty PornHub user sections fell back to unrelated sidebar cards. Empty sections now stay empty; missing expected sections raise.
5. PornHub playlist/chunk and HubTraffic parsers no longer hide missing identities or parser failures. Unavailable-only playlist chunks do not imply exhaustion.
6. PornHub GIF/user extractors used sets and photos used completion order. Source order is preserved.
7. EMPFlix studio accounts live at `/profile/<handle>` and can show `Videos (0)` while later pages contain videos. The studio fixture yields 230 entries; no stale counter is used as a bound.
8. Previous-link class names could match “next”. Next-control matching now distinguishes those tokens and verifies expected page values.
9. XVideos returned a numeric JSON title (`tf=500`); HTML decoding failed the whole page. The title is normalized to a string, and the complete performer scan now matches all 562 entries.
10. RedTube and Tube8 user tabs use JSON `videos-data` feeds. Real feed URLs and `data.pagination` are read from the live page; unavailable collections remain errors.
11. xHamster private playlists use a path page number and embedded pagination template, rather than `?page=`. Listing identities and bounds now use that state.
12. YouJizz public-user batches now use the shared paginator and visible failure policy: 557 uploads, 24 thumbnail batches, five items in the final batch.
13. Root/account redirects, partial stream closure and metadata/header reuse have explicit guards. The shared redirect guard also preserves the existing foreign-response identity contract.

14. XVideos/XNXX search can switch to opaque tracking links between requests. Stable public video keys are read from the cards; watch routes are constructed without decoding tokens and verified against live player pages.

## Complete public examples

Every row below passed an independent ordered comparison against the intended live source region/feed, terminal navigation checks, last-page offset and beyond-last checks. Counts are snapshots of live pages, not future assertions. “Responses” includes an empty boundary probe where needed. Source duplicates remain visible; creator scans deduplicate them.

| Provider | Profile type | Responses | Source / API entries | Unique entries | Last page / items | Beyond last |
|---|---|---:|---:|---:|---|---|
| bellesa | Channel | 2 | 30 / 30 | 30 | 2 / 6 | empty |
| empflix | Profile | 3 | 119 / 119 | 119 | 2 / 59 | empty |
| eporner | Pornstar | 41 | 1558 / 1558 | 1558 | 41 / 38 | empty |
| porn | Collection | 235 | 12919 / 12919 | 12915 | 234 / 37 | empty |
| porndoe | Pornstar | 4 | 83 / 83 | 83 | 4 / 11 | empty |
| pornhat | Model | 4 | 202 / 202 | 202 | 4 / 25 | empty |
| pornhub | Model | 4 | 138 / 138 | 138 | 4 / 18 | empty |
| porntrex | Model | 28 | 3331 / 3331 | 3325 | 28 / 91 | empty |
| redgifs | User | 1 | 17 / 17 | 17 | 1 / 17 | empty |
| redtube | Channel | 40 | 793 / 793 | 793 | 40 / 13 | visible_http_404 |
| spankbang | Creator | 1 | 8 / 8 | 8 | 1 / 8 | empty |
| thumbzilla | Channel | 71 | 1418 / 1418 | 1059 | 71 / 18 | visible_http_404 |
| tnaflix | Channel | 5 | 77 / 77 | 77 | 4 / 5 | empty |
| tube8 | Channel | 23 | 460 / 460 | 459 | 23 / 20 | visible_http_404 |
| xhamster | Creator | 6 | 233 / 233 | 229 | 6 / 3 | visible_http_404 |
| xnxx | User | 72 | 3568 / 3568 | 3568 | 72 / 19 | empty |
| xvideos | Channel | 8 | 270 / 270 | 270 | 8 / 18 | empty |
| youjizz | Pornstar | 1 | 6 / 6 | 6 | 1 / 6 | empty |
| youporn | Channel | 17 | 393 / 393 | 387 | 17 / 9 | visible_http_404 |
| xfreehd | Album images | 2 | 13 / 13 | 13 | 2 / 1 | empty |
| pornhub | Album images | 3 | 197 / 197 | 197 | 3 / 5 | empty |
| beeg | No listing pagination | N/A | N/A | N/A | N/A | N/A |

The complete fixture URLs are in `src/tests/pagination/common.py`; Thumbzilla uses `/channel/letsdoeit-bonus/` and Tube8 uses `/channel/aunt-judys-xxx/`. Image URLs are in `images.py`. `live-results.json` records the additional profile/collection comparisons and boundary results.

Additional complete scans include EMPFlix studio/Pornstar, TNAFlix Profile/Pornstar, PornHub Channel/Pornstar/uploads/playlist, Porntrex Channel, RedTube/Thumbzilla/Tube8 Pornstar, XVideos Pornstar, xHamster Channel/Pornstar, YouPorn Pornstar/Collection, Bellesa Performer/Category, Porndoe Channel, Pornhat Channel, Porn.com Channel/Pornstar, RedGIFs mixed collection, and YouJizz User.

Count differences belong to the source: Thumbzilla’s fixture exposes 1,418 rows but only 1,059 unique IDs; its pages 66/67 repeat a full payload while canonical page numbers and subsequent pages advance. Porn.com’s fixture header reports 17,450 while the exposed listing contains 12,919 rows. TNAFlix’s Lisa Ann header reports 4.9K while the exposed numbered listing contains 6,952 unique entries. These counters are not used to force completeness. XNXX and Pornhat counts changed during the investigation; comparisons use the exact consumed responses.

## Other verification

- Search: 20/20 passing provider checks, first/second/two-page offsets. Every provider search is independently reconciled with its actual consumed HTML/JSON responses, so changing rankings and tracking tokens cannot hide missing rows or create false cross-request mismatches.
- Directories/client methods: 20/20 pass, including Bellesa performer/channel search, provider directories, Eporner category pages, XVideos playlist, PornHub GIF and HubTraffic search. HubTraffic uses independent same-response comparison because results can change between calls.
- Additional finite fixtures: 39/43 pass. Four nonempty-fixture gates remain: two source-confirmed empty PornHub user tabs, RedTube’s currently unauthenticated user feed, and an unavailable Tube8 public user collection. Their empty/unavailable guards are checked separately; they are not counted as successful nonempty pagination.
- Indexed full/boundary comparisons: XVideos 270, XNXX 3,568, Bellesa 30, RedGIFs mixed collection 246. The mixed collection preserves image/video semantics.
- Authenticated source comparisons: ten checks pass with three source-confirmed empty fixtures. Nonempty results are XVideos 17/8; xHamster liked/private playlist 11/11; PornHub history 84 over two pages, favorites 12, recommendations 378 over 18 pages. No private item IDs, cookies, usernames or signed feed URLs are included in this report.
- Lifecycle: strict parameter validation before network, one fetch per complete Bellesa page, cancellation after partial consumption, finite-limit status and out-of-range behavior pass. The real page-101 failures remain incomplete even when a terminal-404 hook is supplied.
- Application creator scan: 473 source entries become 472 stable identities, in source order, over nine pages; no prefix replay.
- Existing regressions: shared backend 59 passed / 238 skipped; app routing/provider/CLI/collection tests 42 passed; existing download compatibility tests six passed. Skipped tests are not counted as live successes.
- All 21 changed wheels build and contain the new modules. Installed editable versions match their metadata; `uv pip check --python Porn_Fetch/.venv/bin/python` passes. Wheel hashes are recorded in `live-results.json`.
- No new offline/mocked tests were authored. New suites make real requests, unwrap every result and close streams. No media downloads were added to this pagination task.

## Outstanding gates

1. **Upstream truncation:** Thumbzilla Brazzers and Tube8 TeamSkeet page 100 expose a Next link to 101, which returns HTTP 404. Tube8 authentication did not remove the limit. The implementation surfaces the hole; this listing route does not expose subsequent pages. This is an expected failure of full coverage, not a full-scan pass.
2. **Thumbzilla legacy playlists:** repeated online searches, primary navigation and candidate routes found no working public playlist URL. The existing class remains for compatibility; missing playlist markup raises instead of returning unrelated homepage videos. Playlist pagination is unverified. A real supported route or confirmation that the site retired it is required.
3. **RedTube/Tube8 user feeds:** earlier authorized signed-in accounts returned successful JSON with count=0 and totalPages=0. Current Brave jars no longer contain signed-in sessions; both homepages show Login, and RedTube’s protected feed returns HTTP 401. A fresh sign-in is pending. Empty accounts cannot establish nonempty multi-page advancement even after authentication succeeds.
4. **Other empty fixtures:** PornHub public-user videos/uploads, subscriptions/feed and XVideos watch-later are source-confirmed empty. Empty behavior is verified; nonempty advancement for those routes remains unverified. The xHamster private fixture has one page, so its first/all/beyond behavior passes but multi-page advancement lacks a fixture.
5. **Release:** planned new provider/base versions are unpublished. They are installed locally from sibling sources, not downloaded as released packages. The base lock is updated to 4.3.0. Provider/application registry locks must be regenerated after coordinated publication; their hashes were not fabricated. No publication or push was performed.

## Reproduction

Run from `/home/asuna/PycharmProjects` using the existing environment:

```sh
Porn_Fetch/.venv/bin/python Porn_Fetch/scripts/pagination_live.py --workspace /home/asuna/PycharmProjects --suite complete_profiles --boundaries --output-dir /home/asuna/PycharmProjects/.pagination-live-2026-11-15/recheck-profiles
Porn_Fetch/.venv/bin/python Porn_Fetch/scripts/pagination_live.py --workspace /home/asuna/PycharmProjects --suite profiles --search --output-dir /home/asuna/PycharmProjects/.pagination-live-2026-11-15/recheck-search
Porn_Fetch/.venv/bin/python Porn_Fetch/scripts/pagination_live.py --workspace /home/asuna/PycharmProjects --suite clients --output-dir /home/asuna/PycharmProjects/.pagination-live-2026-11-15/recheck-clients
```

The same runner exposes `profiles --extra`, `complete_profiles --extra --provider <name> --kind <type>`, `indexed`, `images`, `account_complete`, `user_feeds`, `controls`, `negative`, and `creator_scan`. Authentication suites read only the explicitly authorized Brave domains. Cookie values and private identities remain in memory. Use explicit output directories to preserve evidence across temporary-directory cleanup.

Existing regression commands:

```sh
(cd eaf_base_api && uv run --frozen --group dev pytest tests -q)
(cd Porn_Fetch && .venv/bin/python -m unittest src.tests.unit.test_cli_services src.tests.unit.test_api_audit_routes src.tests.unit.test_provider_parsing src.tests.unit.test_collection_inventory src.tests.unit.test_provider_features -q)
(cd Porn_Fetch && .venv/bin/python -m unittest src.tests.unit.test_pornhub_download src.tests.unit.test_download_recovery -q)
```

Current durable captures/logs/wheels live outside the repositories in `.pagination-live-2026-11-15/`. Only sanitized counts and public fixture references are included in the tracked report.

PornHub source preservation: the workspace checkout was 5.4.8 while Porn Fetch required the published 5.4.9 interface. The published 5.4.9 download module/error/export changes were preserved during the pagination migration (wheel SHA-256 `5df10a91a0486b5c60c3242a9de23ab358530e23d3892ded247cea5597be0538`). These are upstream compatibility changes, not a new downloader implementation.
