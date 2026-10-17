# Provider URL and API audit

Checked 2026-10-17 against the current Porn Fetch working tree and all 13 sibling
`/home/asuna/PycharmProjects/unofficial-api-for-<provider>` checkouts.

**The principal problem is broader than routing.** Several legitimate URLs reach
the correct provider, then fail during profile enumeration because the API builds
incorrect request URLs or parses the wrong response format. Adding live tests
without fixing these would expose real failures immediately.

This is the dated pre-fix analysis. Its observations and hashes remain unchanged
as baseline evidence. See [the implementation follow-up](URL_ROUTING_FIXES.md)
for the subsequent fixes, versions, and verification.

## Evidence and limits

- All 13 API packages were inspected, including their model classes, client
  factories, ID extraction, profile/collection iterators, and link construction.
  Every Python source file in those packages matched the installed copy in Porn
  Fetch's `.venv` at audit time. These findings therefore apply to the app's
  installed dependencies as well as the sibling sources.
- Direct, bounded requests through `BaseCore` retrieved all 13 homepages. Across
  34 page checks, 31 returned HTTP 200; two particular profile URLs timed out and
  a synthetic Thumbzilla playlist ID returned 404. Neither timeout establishes
  that a format is invalid. A successful homepage is also not a successful
  profile scrape.
- Fourteen real API metadata calls succeeded, covering all providers: profiles
  for the 11 providers with profile support, a second PornHub profile type,
  Beeg video metadata, and XFreeHD album metadata. This did **not** establish
  successful video enumeration or download for those URLs.
- Thirteen listing responses were fetched and passed to the corresponding API
  item extractor. These included three Porntrex pagination variants. Metadata
  loading for the extracted video items and media downloads were not performed.
- The offline probe captured 136 behavior observations: 49 routing decisions,
  51 pagination constructions, 12 XVideos rewrites, seven video ID extractions,
  four Beeg API request constructions, and 13 locale-header checks. These are
  observations, not 136 passing tests. Synthetic IDs and slugs are deliberately
  used there. The header checks create and close sessions without requests.
- Public website links and observed redirects are primary evidence for current
  site behavior. Public yt-dlp source provides additional, clearly identified
  evidence for historical/embed/alternate-host formats. A format in an extractor
  is not proof that the site still serves it or that Porn Fetch supports it.
- This is a bounded inventory, not a claim to enumerate every private endpoint,
  temporary mirror, historical alias, experiment, or region-dependent redirect.

Artifacts:

- [Offline observations and source hashes](url-routing-audit/offline.json)
- [Online response, metadata, and listing observations](url-routing-audit/online.json)
- [Offline reproducer](url-routing-audit/offline_probe.py)

Reproduce without network access, from the repository root:

```sh
uv run --no-sync python docs/url-routing-audit/offline_probe.py --output /tmp/provider-url-audit.json
```

Use `--api-root /path/to/checkouts` if the provider repositories are not siblings
of Porn Fetch. The reproducer substitutes request functions and stream factories;
it does not execute the live checks. Raw HTML is temporary audit data and is not
committed. `online.json` is a dated observation record, not a promise of future
availability. Its `listing_extractors` entries describe raw extraction, not full
GUI processing. SpankBang's localized base URL is supplied as its real iterator
does.

## Highest-priority findings

| ID | Finding | Evidence | Repair location |
|---|---|---|---|
| U01 | XNXX profile listing responses are JSON, but its iterator uses an HTML extractor. | Real response contained 50 video entries; `extractor_html()` returned zero. Profile metadata still succeeded. | `xnxx_api/api.py:260`, `xnxx_api/modules/consts.py:16` |
| U02 | XVideos has the same JSON/HTML mismatch. | Real listing response contained 36 entries; `extractor_account()` returned zero. Metadata reported eight pages. | `xvideos_api/api.py:460`, `xvideos_api/modules/consts.py:34` |
| U03 | RedTube's current plural channel path is missing. | The site links `/channels/vip-4k`; the API's `get_channel()` loaded it, but Porn Fetch routes it as a video. | `src/shared/provider_routing.py` profile recognition **and** handler selection |
| U04 | XVideos profile normalization creates invalid nested profile prefixes. | `Pornstar._sanitize_url()` changes `/models/example` to `/pornstars/models/example`. The preceding router fix alone cannot solve this. | `xvideos_api/api.py:492`, `:503` |
| U05 | A query changes a bare XVideos channel into a video. | `/teddy_tarantino` is a profile; `/teddy_tarantino?utm_source=share` is a video. | `src/shared/provider_routing.py:80` |
| U06 | Beeg corrupts IDs and treats URL syntax as part of the key. | `/-012340` becomes key `1234`, losing a significant trailing zero. A trailing slash produces an empty key; `?t=...` pollutes the API endpoint. | `beeg_api/beeg_api.py:41` |
| U07 | Porntrex repeats the first page. | `pages=2` generates `from=00` and `from=01`. Live `00` and `01` returned the same ordered 120 IDs; `02` returned the next set. | `porntrex_api/api.py:355` |
| U08 | Many iterators append paths/queries to the entire URL string. | A profile ending `?utm_source=share` becomes `...?utm_source=share/videos?...`; fragments hide appended pagination from HTTP entirely. | Multiple APIs; details below |
| U09 | SpankBang fetches an extra page and creates double slashes. | `pages=2` generates the base URL plus `/2/` and `/3/`; a base ending `/` produces `//2/`. Server tolerance is not a sound contract. | `spankbang_api/api.py:153` |
| U10 | Eporner cannot derive the ID from a supported embed format. | `/embed/AbC123/` yields `video_id=None`; `/video-AbC123?utm_source=share` includes the query in the ID. | `eporner_api/api.py:122` |
| U11 | Directory pages are mistaken for individual profiles, collections, or videos. | `/channels/`, `/channel`, `/pornstars/`, `/playlists/`, and provider homepages reach inappropriate handlers. | Shared route classification and validation |
| U12 | Redirects are followed, but their resolved identity is not retained by provider objects. | PornHub `/model/teddy-tarantino` redirected to `/pornstar/teddy-tarantino`; XVideos `/profiles/teddy_tarantino` redirected to `/channels/teddy_tarantino`. Objects retained their input URLs/classes. | API URL handling and shared adapter contract |
| U13 | Five API constructors discard the configured language header. | With German configured, PornHub/RedTube/Thumbzilla/Tube8 set `en,en-US`; SpankBang removes `Accept-Language`. The other eight preserve it. | API Client constructors; CLI initialization consistency |

U01/U02 are direct parser-contract failures: `Helper._process_page()` passes
`core.fetch_text()` output straight to the extractor. There is no intervening
JSON-to-HTML conversion. The native JSON `videos` objects have fields including
`id`, `eid`, `u`, `t`, and others. Map those fields deliberately into the existing
Video model after checking their meaning; do not assume one JSON field is a full
absolute URL merely from its name.

## Website inventory and implementation review

Notation: `{id}`, `{name}`, and `{slug}` are placeholders. A directory such as
`/channels/` is a different resource from `/channel/{name}/`. Singular/plural
forms below are identified separately; they are not universally interchangeable.

### 1. PornHub

**Current website evidence:** [homepage](https://www.pornhub.com/),
[channel](https://www.pornhub.com/channels/brazzers),
[profile redirect candidate](https://www.pornhub.com/model/teddy-tarantino).
The homepage directly exposed language hosts including `de`, `fr`, `it`, `pt`,
`es`, `rt`, `pl`, `jp`, `nl`, `fil`, `ar`, `cz`, and `cn` under `pornhub.com`.

**URL families:** `/view_video.php?viewkey={id}`; `/embed/{id}`;
`/video/show?viewkey={id}` (also described in the public extractor);
`/model/{name}`, `/pornstar/{name}`, `/users/{name}`, `/channels/{name}`;
profile tabs `/videos`, `/videos/upload`; `/playlist/{id}`; `/shorties/{id}`;
`/album/{id}` and `/gif/{id}`. The app also recognizes singular user/channel and
`/short/` aliases; these were not all independently verified live. Playlist
chunk endpoints are implementation URLs, not interchangeable user-facing IDs.

**API abstractions:** Video, Short, GIF, Album, Playlist, Model, Pornstar, User,
Channel, Account. `viewkey`/embed ID extraction handles the sampled canonical
video forms. Model/User/Pornstar share featured/upload iterators. They strip
some terminal `/videos[/upload]` suffixes, but operate on the whole string, so
queries/fragments defeat that cleanup. Channel appends `/videos` unconditionally,
so a channel URL already ending `/videos` becomes `/videos/videos`.
Playlist chunks and several relative links are rebuilt on `www.pornhub.com`,
discarding the submitted locale or premium host.

**Porn Fetch:** local `.com` subdomains and `pornhubpremium.com` match the provider.
Profile/playlist/album routing largely matches its intended supported features.
GIFs still fall through to Video despite the upstream GIF class; that is a feature
gap, not a reason to silently parse a GIF as a video. Premium-host recognition
does not prove premium extraction works: some API requests still target the free
site. `.net` and `.org` occur in
[public extractor source](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/pornhub.py),
but are rejected by the app and were not validated as live aliases in this audit.

**Local references:** `pornhub_api/api.py:492`, `:504`, `:1944`, `:2317`, `:2399`;
`pornhub_api/modules/consts.py` relative-link builders.

### 2. Eporner

**Primary sources:** [official API](https://www.eporner.com/api/v2/),
[channel directory](https://www.eporner.com/channels/),
[pornstar profile](https://www.eporner.com/pornstar/riley-reid/).
The directory links individual channels such as `/channel/blacked/`. Language
links use `ph`, `de`, `pl`, `fr`, `es`, `pt`, `it`, `nl`, and `jp` subdomains.

**URL families:** `/video-{id}/{slug}/`, historical `/hd-porn/{id}/{slug}/`,
`/embed/{id}/`; `/pornstar/{name}/`, `/channel/{name}/`; path pagination such as
`/pornstar/{name}/2/`. Some performer slugs include an extra opaque suffix; retain
the full slug rather than trying to derive a person's name. The site also has
playlists, photos, and GIF resources beyond this API's implemented abstractions.

**API:** Video, Pornstar, Channel. The video constructor recognizes `video-` and
`hd-porn/`, but misses embed IDs and does not delimit query strings in short
video URLs. Since Porn Fetch normally loads API and HTML sources, `id=None` is
an actionable issue, not just a missing display field. Profile `urljoin()` avoids
the query/fragment corruption seen elsewhere, but drops those components rather
than preserving filters and appends another page segment to already-paginated
paths. Total-page inference assumes 37 videos per page.

**Porn Fetch:** provider selection works for localized subdomains. `/channel/`
and `/pornstar/` select the correct methods. `/profile/` and plural channel paths
are accepted aliases in the router without equivalent live evidence here.
`/channels/` itself currently becomes a Channel object despite being a directory.
Playlist support is absent in the API/app, even though the website offers it.

**Local references:** `eporner_api/api.py:122`, `:130`, `:347`, `:520`.

### 3. XNXX

**Primary observations:** [homepage](https://www.xnxx.com/),
[profile](https://www.xnxx.com/pornstar/alex_adams69),
[listing endpoint](https://www.xnxx.com/pornstar/alex_adams69/videos/best/0).
[Public extractor source](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/xnxx.py)
also records `video.xnxx.com`, `www.xnxx3.com`, and both `video-{id}` and older
`video{id}` forms.

**URL families:** `/video-{id}/{slug}`, historical `/video{id}/{slug}`;
`/pornstar/{name}`, `/profile/{name}`; `/videos/best/{zero_based_page}` beneath
a profile. `user`/`users` paths are accepted by the app but were not verified
as equivalent website aliases. Do not infer every numbered mirror is live from
the app's `xnxx\d*` host pattern.

**API:** Video and User; a pornstar URL intentionally goes through `get_user()`.
Profile metadata succeeded and reported 27 pages. Enumeration is broken for the
sample because the listing endpoint returns structured JSON with 50 entries and
the iterator parses HTML. URL construction also appends `/videos/best/...` after
queries, fragments, or an already-present tab/page suffix. `pages=0` produces no
pages, unlike several other providers' interpretation of zero. The metadata
view-count regex requires English `video views`, a localization fragility.

**Porn Fetch:** `.com` and numbered `.com` hosts are recognized, including
subdomains. Provider and profile classification of the sampled pornstar URL are
correct; the failure is downstream in the API. Extracted HTML links are rebuilt
on `xnxx.com`, so even the older HTML pathway loses a submitted locale/mirror.

**Local references:** `xnxx_api/api.py:237`, `:245`, `:260`;
`xnxx_api/modules/consts.py:8`, `:16`.

### 4. XVideos

**Observed:** [bare channel](https://www.xvideos.com/teddy_tarantino),
[profile alias](https://www.xvideos.com/profiles/teddy_tarantino),
[listing JSON](https://www.xvideos.com/profiles/teddy_tarantino/videos/best/0).
The profile alias redirected to `/channels/teddy_tarantino`, showing that
`/profiles/` alone is not sufficient evidence that a resource is a Pornstar.

**URL families:** `/video.{opaque_id}/{slug}` and newer paths with intervening
numeric/position segments; historical `/video{numeric_id}/{slug}`;
`/embedframe/{id}`; bare `/{name}`, `/channels/{name}`, `/profiles/{name}`,
`/pornstars/{name}`, and the repository's `/models/{name}` fixtures;
`/videos/best/{page}` beneath a profile; `/favorite/{id}/{slug}` playlists.
The [public extractor](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/xvideos.py)
also records `xvideos.es`, `xvideos2.com`, `/amateur-channels/{name}`, and
`#quickies/a/{id}` short links. Those are additional candidates, not automatically
supported app features. The particular localized `/models/` fixture timed out;
its current live status remains unresolved.

**API:** Video, Channel, Pornstar, Account; playlists are returned as a generator.
Two independent blockers exist: the listing endpoint's JSON is sent to an HTML
extractor, and `_sanitize_url()` prefixes rather than replaces some profile
aliases. A localized `/models/example` becomes `/pornstars/models/example`.
The string replacement only handles `xvideos.com/`, so numbered mirrors behave
differently. `_load_html()` strips fragments/trailing slashes, but not query
strings or existing `/videos/best/N` suffixes. Playlist pagination appends `/{page}`
to the full URL too.

**Porn Fetch:** language subdomains and numbered `.com` hosts match. Bare-channel
routing wrongly requires an empty query; multi-segment bare-channel tabs are
mistaken for videos. `/profiles/` always chooses Pornstar even for the observed
Channel redirect. `/amateur-channels/` is unrecognized. Quickies fragments are
ignored when deciding content type, so a short link can become a full profile
scrape. `xvideos.es` is rejected. Repair JSON enumeration before broadening the
claimed URL coverage.

**Local references:** `xvideos_api/api.py:353`, `:460`, `:492`, `:503`, `:595`.

### 5. XHamster

**Primary observations:** [localized creator](https://ge.xhamster.desi/creators/comatozze),
[newest tab](https://ge.xhamster.desi/creators/comatozze/newest),
[associated user](https://ge.xhamster.desi/users/cumatozz).
The same person can have distinct creator and user URLs; they are not merely
translated slugs. The sampled creator returned metadata and 46 extracted entries.

**URL families:** `/videos/{slug}-{id}`, historical `/movies/{id}/{slug}.html`,
`/xembed.php?video={id}`; `/creators/{name}`, `/pornstars/{name}`,
`/channels/{name}`, `/users/{name}`; tabs such as `/newest`, `/videos`, `/shorts`;
path pagination `/2`, plus filters such as `tag`, `sort`, `channel`, and `f[0]`.
`/moments/{slug}-{id}` and `/shorts/{slug}-{id}` are short-video routes.

**API:** Video, Short, Creator, Pornstar, Channel, Account. Canonical creator
pagination works on the sampled `.desi` host and preserves that host. But
`build_page_url()` appends `/2` after the full URL, so queries/fragments break
pages after the first; already-paginated URLs also need normalization. Profile
short tabs exist upstream (`get_shorts`) but the app's generic profile pathway
always requests regular video enumeration. Embed-page handling was not verified.

**Porn Fetch:** the previous change added `.desi` and localized subdomains.
[Public extractor source](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/xhamster.py)
lists additional hosts including `.one`, numbered `.desi`, `xhms.pro`,
`xhday.com`, and `xhvid.com`; the app rejects these. Verify ownership/current
redirect behavior before adding individual aliases. The app also classifies
directory routes such as `/creators` as profiles. Its short resolver checks
substrings anywhere in the path, rather than an anchored resource pattern.

**Local references:** `xhamster_api/api.py:204`, `:218`, `:277`;
`xhamster_api/modules/consts.py:124`.

### 6. SpankBang

**Primary observations:** [localized creator](https://de.spankbang.com/jpqa/creator/freya+erlenberg/),
[pornstar](https://spankbang.com/en/pornstar/sharon+lee/),
[homepage](https://spankbang.com/).
Creator/channel IDs precede the resource type; the pornstar example uses a locale
segment. Literal `+` occurs inside path slugs and must not be decoded as a space
using query-string rules.

**URL families:** `/{id}/video/{slug}`, `/{id}/play/...`, `/{id}/embed/`;
`/{id}/creator/{slug}/`, `/{id}/channel/{slug}/`, `/en/pornstar/{slug}/`;
profile path pagination `/2/`, filters such as `?q=hd`;
`/{playlist_id}/playlist/{slug}` and
`/{playlist_id}-{video_id}/playlist/{slug}` in the
[public extractor](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/spankbang.py).
The latter is an individual playlist item, distinct from a whole playlist.

**API:** Video, Creator, Channel, Pornstar; no Playlist abstraction. Profile
metadata and 16 item extractions succeeded on the sample. The actual iterator
uses `urlsplit()`/`urljoin()` to preserve the listing host when resolving item
links, which is good. Pagination still adds an extra page, double slashes, and
suffixes behind queries/fragments. Embed/play inputs go straight to the video
HTML parser; no dedicated canonicalization was established.

**Porn Fetch:** the preceding positional routing fix handles the sampled creator,
channel, and pornstar paths. Localized subdomains match. Whole-playlist URLs
still fall through to Video, although playlist extraction is not implemented
upstream or advertised by the app. They should receive a clear unsupported-type
result. Direct `/profile/{name}` and `/creator/{name}` forms in routing are not
substitutes for validating the site's actual ID-prefixed forms.

**Local references:** `spankbang_api/api.py:153`, `:429`;
`spankbang_api/modules/consts.py:26`.

### 7. YouPorn

**Primary observations:** [homepage](https://www.youporn.com/),
[channel](https://www.youporn.com/channel/brazzers/).
Language hosts include `de`, `br`, `pl`, `fr`, `es`, `it`, `rt`, `jp`, `ar`, `id`.
Channel metadata and 24 listing entries were extracted successfully.

**URL families:** `/watch/{id}/{optional_slug}/`, `/embed/{id}/`;
`/channel/{name}/`, `/pornstar/{name}/`; optional `/rating`, `/views`, `/duration`
sorting tabs; `/collections/videos/{id}/` with sorting tabs including `/time`;
`?page=N`, and some listing filters. These families are also described by the
[public extractor](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/youporn.py).
Directories `/channels/`, `/pornstars/`, `/amateurs/`, and `/collections/` are not
individual resources.

**API:** Video, Channel, Pornstar, Collection, and an internal User class for
collection discovery. There is no public `Client.get_user()`/User video-stream
equivalent, nor an Amateur class. Current bare channel/profile pagination works,
but BaseProfile adds `/?page=` to a string with any existing query or fragment;
Collection adds a second `?`. Existing sort paths can be retained, but their
query parameters must be composed correctly. Item URLs are rebuilt on the base
YouPorn host, losing a requested language host.

**Porn Fetch:** supported channel/pornstar/collection routes select the expected
methods. User and amateur resources are not supported merely because they exist
on the site. `/collections/` without an ID is nevertheless classified as a
Collection. Embed inputs are not explicitly converted to watch pages; loading
their video metadata still needs a live fixture.

**Local references:** `youporn_api/api.py:146`, `:270`, `:385`, `:699`;
`youporn_api/modules/consts.py:31`.

### 8. Beeg

**Sources:** [site](https://beeg.com/) and
[public extractor](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/beeg.py).
The homepage is a JavaScript shell, so it is not a useful source of server-rendered
profile links. A real video metadata call succeeded through the local API.

**URL families:** `/-{padded_numeric_id}`, numeric variants, historical
`/video/{id}`, and URLs containing `?t={start}-{end}`. These are video formats;
no profile/channel abstraction is implemented by this API/app.

**API:** Video only. It derives the key from `url.split('/')[-1].strip('-0')`.
`strip` removes characters from **both** ends, so a meaningful trailing zero is
lost. It also uses the query as part of the API URL, and a trailing `/` yields
an empty key. Parse the path segment, validate digits, then remove only the
documented leading sign/padding. Whether to honor clip time ranges is a separate
capability decision; the parameter must not corrupt resource identity.

**Porn Fetch:** provider selection accepts localized/subdomain hosts under
`beeg.com` but does not validate video shape. It correctly chooses API-based
video loading. A routed `/video/...` URL is not evidence that the Beeg key parser
handles all its variants. Non-video navigation should not be presented as videos.

**Local reference:** `beeg_api/beeg_api.py:41`.

### 9. Porntrex

**Primary observations:** [homepage](https://www.porntrex.com/),
[model](https://www.porntrex.com/models/rose/),
[channels](https://www.porntrex.com/channels/),
[playlists](https://www.porntrex.com/playlists/).
The channel directory links `/channels/archivelust/` and similar individual pages.

**URL families:** `/video/{id}/{slug}`; `/models/{name}/`, `/channels/{name}/`;
playlists and albums also exist on the website. The sampled model uses AJAX
pagination with `mode=async`, `function=get_block`,
`block_id=list_videos_common_videos_list_norm`, `sort_by`, and `from`.
Site links expose `from:02` as the next page; the `#videos` anchor is page UI,
not part of the HTTP endpoint.

**API:** Video, Model, Channel. Model metadata and listing parsing succeeded,
but pagination starts at zero and duplicates the first page. Existing query
strings produce a second `?`; fragments swallow the AJAX parameters. The AJAX
timestamp is hard-coded, which is also brittle even though the sampled server
accepted requests without it. Construct query parameters structurally and derive
the pagination/block contract from the relevant listing rather than copying a
browser request wholesale.

**Porn Fetch:** singular/plural model/channel tokens are recognized; current
plural forms dispatch correctly. But model/channel directories are mistaken for
individual profiles. Website playlists/albums are not implemented in this API;
the app should clearly reject those types rather than fall through to Video.

**Local references:** `porntrex_api/api.py:295`, `:355`.

### 10. XFreeHD

**Primary observation:** [beta site](https://beta.xfreehd.com/). Its homepage links
videos under `/video/{id}/{slug}` and an `/albums` directory. The existing real
album fixture loaded and reported two pages through the API.

**URL families:** `/video/{id}/{slug}`; `/album/{id}/{slug}`; album pagination
`?page=N`. The established `beta.xfreehd.com` host and other subdomains match
the current provider regex. This audit did not establish equivalence between
every beta/main-host resource or a stable alternate-TLD scheme.

**API:** Video and Album only. Album `get_images_by_page()` and
`get_all_images()` append `?page=` to the entire input string. The offline probe
confirms that a copied URL with a query or `#photos` breaks page construction.
No Model/Channel API exists to wire up. Embed HTML can be extracted as metadata,
but accepting an embed URL as input is a separate unverified capability.

**Porn Fetch:** video provider selection and singular album classification are
correct for canonical shapes. Albums are CLI-only in the documented interface;
the GUI video input does not gain album support from shared classification.
`/albums` should be an unsupported directory, not a Video.

**Local references:** `xfreehd_api/api.py:290`, `:331`, `:343`, `:356`.

### 11. RedTube

**Primary observations:** [homepage](https://www.redtube.com/),
[channel](https://www.redtube.com/channels/vip-4k),
[playlist directory](https://www.redtube.com/straight/playlists).
The site links numeric `/playlist/{id}` resources and singular/plural channel
routes in different contexts. Language links include `de`, `pl`, `fr`, `es`,
`it`, `ru`, `jp`, `ar`, and `id`.

**URL families:** `/{numeric_id}`; `/channels/{name}`, `/channel/{name}`;
`/pornstar/{name}` (including literal `+` in some slugs); `/amateur/{name}`;
user profile routes implemented by the API; `/playlist/{id}` and query-ID
variants accepted by the app; `?page=N`, sorting/period filters. The
[public extractor](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/redtube.py)
records `redtube.com.br` and `embed.redtube.com/?id={id}`. Their current extraction
behavior was not tested here.

**API:** Video, Playlist, User, Pornstar, Amateur, Channel. A direct
`get_channel('/channels/vip-4k')` call succeeded, and its listing produced 20
entries. User/playlist pagination chooses `?` or `&`, which handles simple
existing queries better than several APIs. It still appends after fragments and
adds duplicate `page` keys to already-paginated URLs. HTML item links are forced
onto `www.redtube.com`, losing the localized origin.

**Porn Fetch:** localized `.com` hosts match, but plural `/channels/` is absent
from profile recognition **and** method selection. This is a confirmed gap in a
current, working API feature. `.com.br` is rejected. Embed host recognition alone
does not establish its parser support. Directory `/channel` is mistaken for an
individual Channel; `/straight/playlists` falls through to Video.

**Local references:** `redtube_api/api.py:552`, `:576`, `:674`, `:768`;
`redtube_api/modules/consts.py:24`.

### 12. Thumbzilla

**Primary observations:** [homepage](https://www.thumbzilla.com/),
[channel](https://www.thumbzilla.com/channel/public-agent/),
[pornstar](https://www.thumbzilla.com/pornstar/heidi-van-horny/).

**URL families:** current `/watch/{numeric_id}/`; `/channel/{name}/`,
`/pornstar/{name}/`, `/amateur/{name}/`; playlist forms implemented in the API;
`?page=N`. Historical `/video/{ph_viewkey}/{slug}` is described in the PornHub
[extractor](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/pornhub.py),
which treats that family through PornHub. Do not assume it is interchangeable
with Thumbzilla's current numeric-ID player.

**API:** Video, Playlist, Pornstar, Amateur, Channel; no public User abstraction.
Channel metadata and 20 listing entries succeeded. Profile query pagination
handles `?` versus `&` but not fragments or replacing existing page keys.
Playlist always appends `&page=`, which cannot work as a query parameter for a
path-ID URL without `?`. The synthetic query-ID fixture returned 404, so this
audit does not establish a currently valid public playlist URL; the existence
of the class and support matrix is insufficient evidence.

**Porn Fetch:** canonical profile routing matches the API. Legacy alphanumeric
`/video/ph...` paths fall through to the numeric-oriented Thumbzilla parser,
without the historical cross-provider treatment. `/amateurs/` is a directory
and unsupported by that profile route. Obtain one current playlist fixture
before describing the various playlist spellings as supported.

**Local references:** `thumbzilla_api/api.py:152`, `:324`, `:360`, `:473`, `:571`.

### 13. Tube8

**Primary observations:** [homepage](https://www.tube8.com/),
[channel](https://www.tube8.com/channel/brazzers/).
The retrieved homepage exposed `de`, `jp`, `it`, `ar`, and `id` language hosts.

**URL families:** current `/porn-video/{id}/`; `/channel/{name}/`,
`/pornstar/{name}/`, `/amateur/{name}/`; User paths supported by the API;
profile `?page=N`. The
[public legacy extractor](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/tube8.py)
records `/{category}/{slug}/{id}/` and nested embed/category paths, but marks
that extractor non-working. Treat these as historical candidates requiring
redirect/page validation, not current verified formats.

**API:** Video, User, Pornstar, Amateur, Channel; no Playlist. The current channel
loaded metadata and returned 20 extracted entries. Profile pagination always
adds `?page=`, so existing query strings and fragments break it. The video ID
URL fallback only handles `porn-video`/`video` prefixes; older category-style
URLs depend on page/player metadata that was not checked here.

**Porn Fetch:** current canonical types and localized hosts match. Unsupported
directories and historical paths are still accepted as Video by default. There
is no basis to advertise playlist support or assume every old embed URL works.

**Local references:** `tube8_api/api.py:195`, `:357`, `:413`, `:568`.

## Shared routing and localization conclusions

The shared [router](../src/shared/provider_routing.py) has a useful foundation:
it uses parsed hostnames and anchored domain boundaries, identifies the provider
before looking at path tokens, and keeps the original URL for requests. That
preserves case-sensitive IDs and encoded slugs. It does not mistake a provider
name in a query string on an unrelated host for the provider itself.

The remaining problems are concentrated in these areas:

1. **A known hostname is not sufficient to classify a Video.** The default
   Video fallback accepts directories, homepages, account pages, support
   subdomains, unsupported albums/playlists, and invalid resource paths. Use
   explicit resource patterns with required IDs/slugs and a clear unsupported
   result. Preserve the prohibition on keyword search; discovering website
   search URLs is not authorization to expose that capability.
2. **Resource type and tab/selection are separate.** A model's uploaded videos,
   featured videos, shorts, favorites, and photo albums are different selections.
   At present `ContentKind.PROFILE` loses this information, while frontend settings
   silently choose a stream. Decide which submitted tabs are honored, normalized,
   or rejected. Do not scrape a whole profile from an unrecognized short link.
3. **Do not use one universal locale-to-subdomain rule.** For example the sampled
   sites use `fil.pornhub.com`, `ph.eporner.com`, `rt.youporn.com`, and
   `ru.redtube.com`. Existing host-based detection accepts these language
   subdomains, which is good. Preserve the supplied host when appropriate;
   site-specific verified redirects should decide host changes.
4. **Query and fragment syntax needs deliberate handling.** Parse the URL,
   modify its path independently, and replace the provider's pagination key in
   parsed query pairs. Retain meaningful sort/filter parameters and opaque IDs.
   Ignore ordinary document anchors for HTTP construction, but recognize special
   fragments such as XVideos Quickies before removing them. `+` in a path is not
   a query-space escape. Do not lowercase IDs or decode/re-encode slugs casually.
5. **Redirect identity needs an explicit contract.** `BaseCore` follows redirects,
   while `fetch_content()` returns text and API objects retain their input URL.
   Known aliases can therefore fetch the right page once but build later requests
   from the wrong path or host. Track the resolved media identity separately from
   the user's original URL. Restrict canonicalization to verified provider targets;
   do not blindly trust every canonical tag or introduce arbitrary host rewrites.
6. **There are two hostname tables.** `HOST_PATTERNS` in shared routing and
   `SITE_PATTERNS` in GUI clients currently agree on the edited XHamster rule,
   but duplicate the policy. Use shared provider detection in the GUI, or at
   least derive the second table from the first. New aliases must work for both
   profile selection and subsequently returned video URLs.
7. **Language headers are a separate axis from URL language.** The GUI refresh
   explicitly reapplies configured language headers/cookies after restoring
   sessions. The CLI config also supplies locale settings, but an offline check
   confirmed that PornHub, RedTube, Thumbzilla, and Tube8 Client constructors
   replace a German header with `en,en-US`; SpankBang clears it. BaseCore uses
   session headers when preparing requests, so that discrepancy matters for the
   CLI, which lacks the GUI's refresh step. All eight other APIs preserved the
   header. Fix header precedence and check effective GUI/CLI behavior together;
   this finding alone does not establish that localized URLs fail. English-only
   metadata labels, notably XNXX's view regex, remain a parsing dependency.
8. **Alternative domains require evidence.** Some current patterns accept every
   numbered `.com` mirror without proof; other aliases in public extractors are
   rejected. Maintain a small, documented provider alias list and distinguish
   verified current hosts from historical candidates. Subdomain localization is
   not the same problem as an unrelated alternate registrable domain.

## Recommended repair order

1. **Repair enumeration correctness in the APIs.** Add XNXX/XVideos listing JSON
   parsers, fix Porntrex's first-page numbering, and correct Beeg's ID extraction.
   Keep the existing BaseCore/Helper lifecycle and Video models. This work belongs
   in the sibling API repositories, then in a dependency refresh for Porn Fetch.
2. **Close the app routing mismatches.** Add RedTube plural channels, fix bare
   XVideos channels with queries and known tab suffixes, and validate required
   profile/collection identifiers. Make handler selection use the same parsed
   resource information as classification.
3. **Normalize API request construction.** Fix XVideos prefix replacement;
   compose paths and query parameters correctly in all iterators; remove
   SpankBang's extra page; normalize recognized tab and page suffixes; preserve
   configured language headers through client construction. Share only genuinely
   common URL-building mechanics, rather than creating a large framework for
   unrelated website rules.
4. **Resolve alias/type policy.** Validate the historical/embed/alternate-host
   candidates with small public fixtures. Reject unimplemented GIF, Quickies,
   unsupported playlist/album, and profile-short variants clearly until their
   extraction path exists. Avoid turning every upstream abstraction into a
   new app feature as part of a routing repair.
5. **Add the live profile diagnostics discussed earlier.** For each supported
   provider/type, assert correct routing, nonempty enumeration, successful video
   metadata preparation, and real Qt model insertion. Add a small pagination
   check for providers whose first-page logic changed. A metadata-only assertion
   would have missed U01/U02.

Focused offline regressions should exercise confirmed failures and the supported
canonical cases. Keep live tests opt-in and bounded; do not add broad network
work to offline CI or require all historical/region-specific variants to pass.

## Fixture priorities for the next implementation phase

There are already usable starting points in `online.json`: successful API
metadata for each provider, and working raw listing extraction for most profile
providers. Recheck them immediately before adding durable smoke tests, since
account status, aliases, and available videos can change.

The most useful additional fixtures are:

| Fixture | What it will resolve |
|---|---|
| A currently active XVideos `/models/` URL and its final redirect | Valid alias normalization, beyond the old timed-out fixture |
| A public XVideos bare channel plus a normal share query and a video tab URL | Stable content classification across representations |
| One current Thumbzilla public playlist, copied from the website | Actual path-ID versus query-ID contract and pagination |
| A Beeg video whose significant ID ends in zero | A real regression fixture for the confirmed trimming bug |
| A SpankBang profile with at least two pages and a quality/sort filter | Correct page count, slash handling, and filter preservation |
| One model/channel with a known alias-to-different-profile-type redirect | Resolved identity and subsequent iterator behavior |
| A real embed URL for each provider that will claim embed-input support | Whether watch-page canonicalization is required |
| A public user/amateur URL for each advertised User/Amateur API branch | Avoid claiming coverage based only on a Channel fixture |

The supplied examples need not include specific titles or stable video counts.
The important assertions are the resource identity, intended selection, bounded
nonempty results, and successfully prepared rows.
