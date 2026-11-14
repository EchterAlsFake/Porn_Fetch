# Provider metadata capabilities

Audit date: 2026-11-14. Scope: all 21 providers registered in
`src/shared/provider_routing.py`, including the Pornhub and xHamster short-video
types. This audits the latest GitHub source, not just Porn Fetch's current
adapters or provider field declarations. See the
[implementation plan](JELLYFIN_METADATA.md#concrete-implementation-plan).

## Method and confidence

The 15 existing provider checkouts under `/home/asuna/PycharmProjects` were clean
and updated with `git pull --ff-only --no-rebase`. Six missing repositories were
cloned from `EchterAlsFake` on GitHub: Bellesa, Porn.com, Porndoe, Pornhat,
RedGIFs and YouJizz. Pornhub fast-forwarded to newer code; the other existing
providers were already current. `eaf_base_api` was also updated and inspected.
All 22 resulting checkouts were clean and matched their fetched upstream heads.
The source appendix pins the exact revisions and package versions inspected.

Each video model was checked against its loader, extraction code, relevant
helper functions and listing-seeded fields. Profile helpers were inspected where
the video exposes performer links instead of names. No live site requests or
media downloads were run for this audit. A parser's ability to extract a field
does not establish its fill rate across a website. Conversely, an absent API
field does not prove the website itself never publishes that information.

## Capability matrix

Every provider has a code path for title, duration and at least one video image.
That is a capability, not a guarantee for every item. The matrix describes regular
videos; short-video differences follow below. `Names` means scene-associated cast
names are extracted. `Links` means names need profile resolution or an API
enhancement. All descriptions can be missing or contain site-generated text.

| Provider | Description | Publication information | Cast today | Taxonomy | Credited organization / author semantics |
| --- | --- | --- | --- | --- | --- |
| [Beeg][beeg] | Absent | `fc_facts[0].fc_created` | No separate cast; person flags collapsed into tags/author | Tags | Owner/person-derived `author`; role is ambiguous |
| [Bellesa][bellesa] | Plain text and HTML | `posted_on` timestamp | Names + profile URLs | Tags + categories + primary category | Explicit `content_provider` relation; first provider name and all channel URLs retained |
| [EMPFlix][empflix] | JSON-LD/description/OG | `uploadDate` + separate relative text | Name/URL dictionaries | Category dictionaries; `tags` repeats category labels | Profile/channel uploader; verification badge is not a production credit |
| [Eporner][eporner] | HTML JSON-LD | API `added`; absent from HTML output | Actor profile URLs | API keywords + HTML tags/categories | Uploader separate from JSON-LD actor links |
| [Porn.com][porn] | Absent from scene parser | Absent from scene parser | Names + profile URLs | Category labels/URLs exposed as tags | Credited channel; optional listing `source_name` is a source reference |
| [Porndoe][porndoe] | JSON-LD/meta, then title fallback | JSON-LD `uploadDate` + separate relative text | Name/URL dictionaries | Tags + category dictionaries/URLs | JSON-LD `producer`, falling back to `publisher`, combined into one author field |
| [Pornhat][pornhat] | JSON-LD | JSON-LD `uploadDate` | Names + profile URLs | Tags + URLs | JSON-LD author + `/sites/` channel link; `/paysite/` reference separate |
| [Pornhub][pornhub] | JSON-LD/meta/body | API date or HTML date text/JSON-LD | Names | Tags + categories | Uploader name/link/avatar/information; no explicit studio field |
| [Porntrex][porntrex] | Description region text | Displayed metadata text | Absent | Tags + categories | Username/uploader |
| [RedGIFs][redgifs] | API description and HTML page description | API `createDate`; separate HTML publication date | Absent | Tags + niche IDs + content classification | Creator account, not a scene cast list |
| [Redtube][redtube] | Absent | Displayed date-added text | Names + profile URLs | Tags + categories + timestamped action tags | Uploader account, with ID/type/avatar/verification |
| [SpankBang][spankbang] | Meta description | Absent | Absent | Tags | Uploader/profile name |
| [Thumbzilla][thumbzilla] | JSON-LD/meta | Displayed date or JSON-LD `uploadDate` | Declared, not populated | Absent from video parser | Author value/uploader name; may be a structured value |
| [TNAFlix][tnaflix] | JSON-LD/description/OG | `uploadDate` + separate relative text | Name/URL dictionaries | Category dictionaries; `tags` repeats category labels | Profile/channel uploader |
| [Tube8][tube8] | JSON-LD/meta | Displayed date or JSON-LD `uploadDate` | Declared, not populated | Absent from video parser | Author value/uploader name; may be a structured value |
| [XFreeHD][xfreehd] | Absent | Displayed date text | Absent | Tags + categories | Uploader + profile URL/avatar |
| [xHamster][xhamster] | Entity/model/meta | Created timestamp/tooltip + relative text | Names | Tags + categories | Uploader separate from cast |
| [XNXX][xnxx] | JSON-LD/meta | JSON-LD `uploadDate`, or unqualified `dispo` comment fallback | Absent | Tags/category-like fallback strings | Uploader name |
| [XVideos][xvideos] | JSON-LD/meta, then title fallback | JSON-LD `uploadDate`, or unqualified `dispo` comment fallback | Profile URLs | Tags | Uploader name/link |
| [YouPorn][youporn] | Absent | Displayed published-date text | Profile URLs | Tags + categories | Uploader ID/type/name/link |
| [YouJizz][youjizz] | JSON-LD/OG | JSON-LD `uploadDate`, or displayed pretty-date fallback | Absent | Tags | Uploader ID/name/link |

Nine providers currently extract scene-associated cast names directly: Bellesa,
EMPFlix, Porn.com, Porndoe, Pornhat, Pornhub, Redtube, TNAFlix and xHamster. Three more expose
cast links: Eporner, XVideos and YouPorn. The remaining nine do not currently expose
a separate populated cast list. A creator account is not evidence that its owner
appears in the video.

## Studio and publisher policy

No audited video model exposes a dedicated, consistently populated production
studio field. Preserve the relationships that actually exist:

- **Bellesa:** `content_provider` is the strongest explicit supplier credit.
  `video_fields` keeps only the first provider name in `author`; names for
  additional providers are discarded, although their URLs remain. This can
  support a credited-provider field now, and complete provider credits after a
  small API extension. It does not independently establish who produced a scene.
- **Porndoe:** an explicit JSON-LD producer is potentially a production credit,
  but the parser merges `producer` and `publisher`. Preserve their original roles
  upstream before treating the current `author_name` as a studio.
- **Pornhat and Porn.com:** channel/site/source relationships are useful credits,
  but the parser does not establish that they are production studios.
- **All other providers:** uploader, owner, creator, verification badges and brand
  names inside tags are insufficient to infer a studio.

Recommended default: export `<studio>` only for an explicitly identified producer
or a user-confirmed studio mapping. Retain credited providers, publishers and
channels separately in JSON. Offer an explicit option to use those credits in
Jellyfin's studio field, with the source role visible in the preview. Avoid a
silent `studio = author` fallback.

## Provider details and export limits

### Beeg

`_load_api` returns tags, thumbnail, author and date that the current GUI adapter
replaces with “Not available”. Recover those existing fields first. The thumbnail
is constructed from the media key and a fact offset; `fc_created` is the fact's
creation date, not a proven original scene release date. The current author is
the first qualifying owner/person tag and can lose the distinction between them.
Use the video's `key` as its stable media identity: `video_id` currently comes
from a nested data-record ID. Person/owner flags are not exposed separately.
There is no description, discrete cast list or studio field today.

### Bellesa

API and HTML initial-state data share `video_fields`. Export description, tags,
separate categories, named performers and credited-provider references. The API
also offers views, likes, primary category and highlights. `posted_on` is the
platform publication date. Performer profiles can supply IDs, names, images,
logos and a hero image through additional requests. Scene thumbnails and preview
clips are not automatically portrait posters or full trailers. Preserve all
provider names upstream instead of fetching every channel just to recover them.

### EMPFlix

The parser separates cast dictionaries from the uploader and returns description,
upload date, duration, image, categories and engagement values. Category names
are duplicated into `tags`, so normalize duplicates without losing the category
role. Mosaic templates and preview clips exist, but a mosaic is not a poster.
Channel profiles may add branding and a website with another request; these are
account details, not a production-studio guarantee.

### Eporner

Export description, uploader, tags/categories and actor URLs from HTML. Load API
metadata for exact duration, publication date, rating, keywords and an image
gallery only when existing language policy permits it. HTML also supplies image
and rating metadata. `authors_urls` actually comes from JSON-LD `actor`, despite
its name; `get_authors()` resolves these to Pornstar profiles. Actor names already
present in that JSON-LD are discarded today. Retain them upstream to avoid a
profile request per performer. Strict-language HTML-only use must leave API-only
fields unavailable rather than bypassing that setting.

### Porn.com

Scene HTML gives cast names/URLs, a channel credit, category labels/URLs, duration,
thumbnail and thumbnail sequence template/count. `language` is the HTML document
language. Description and publication date are not returned. Rating and source
fields are optional listing seeds, so a direct link and a listing-created object
can differ. Do not fabricate a date from acquisition time or a synopsis from the
title. A source or referral link is not an IMDb/TMDb identity or studio credit.

### Porndoe

Export actor dictionaries, separate tags/categories, description and upload date.
The description may be the title when no other text exists: suppress that
duplicate in NFO. Preserve explicit producer/publisher roles with an API change.
The metadata parser initializes dislikes, ratings, VR/exclusive flags and preview
URL to `None`; declaration alone cannot support advertising those features.
The normal HTML loader also calls the player service, so a metadata-only refresh
currently includes that extra request. Store both public and internal IDs with
different roles; use the public watch identity for matching.

### Pornhat

Export description, upload date, cast names/URLs, tags/URLs, author/channel and
thumbnail/poster references. Media resolution is a separate source and is not
needed just to retain these metadata fields. Preview data and advertised source
qualities also exist. `/sites/` and `/paysite/` links have distinct meanings;
retaining a reference does not require adding a new discovery feature. HTML
language is UI language, not audio-language evidence.

### Pornhub

Regular videos expose cast names, separate tags/categories, description, date,
duration, author references/avatar, views, rating percentage and content flags.
HTML and API values can differ; preserve existing locale/source choices. Cast
names lack corresponding video-level profile URLs. Author imagery belongs to
the uploader and cannot automatically serve as each actor's photo.

**Shorties differ:** duration, tags/categories, author/avatar and meta-description
are available, although the GUI currently drops duration and taxonomy. There is
no publication-date or separate cast field. Do not assign the full video's date,
cast or studio to the short automatically. The short parser can fall back to the
first item if the requested item is not found; check identity before exporting
metadata. Never serialize its token, media definitions or direct stream URLs.

### Porntrex

Export description, username, tags/categories, thumbnail and displayed duration
and date. Date text needs format validation; its existence does not establish an
exact UTC timestamp. The API also exposes views and subscriber count. `license_code`,
`lrc` and `rnd` are player/download internals, not licensing or descriptive
metadata for export. There is no separate cast or studio relationship.

### RedGIFs

Use API data for duration, dimensions, audio flag, description, creation date,
creator, tags, niches, poster/thumbnail and engagement. HTML provides the display
title and a separately named publication date/page description. The two sources
must not be assumed identical. Niche names require additional lookup; keep IDs
when unresolved. Dimensions describe provider media, not necessarily the chosen
download rendition. `raw_metadata` and `html_metadata` include nested internals:
export an allowlist, never those entire dictionaries. There is no cast/studio.

### Redtube

Export explicit performer names/URLs, taxonomy, date-added text, thumbnail,
duration and uploader references. Preserve timestamped `action_tags` separately
from normal tags. Current GUI preparation selects action-tag keys and loses
their timing and potentially ordinary tags. They could support future chapter
work, but their presence is not proof of complete or accurate chapter markers.
No description field is returned. Uploader avatar/type/verification are useful
account metadata, not actor photos or studio evidence.

### SpankBang

Export title, meta-description, uploader name, tags, thumbnail, duration and
available rating. No publication date or separate cast/studio field is returned.
There is no `video_id` field on Video; derive identity from the normalized public
video route. `image` is extracted from avatar alt text or author text, not an
image URL. Do not use it as artwork. Some optional values are listing seeds.

### Thumbzilla

Export description, duration, thumbnail, title, date and author value when
present. `performers`, `uploader_url` and `preview_video_url` are declared but not
populated by the video parser or listing extractor. There are no returned tags
or categories. `publish_date_thumbnail` can describe an ImageObject; it is not
additional evidence of the video's publication date. The JSON-LD parser favors
graph-shaped data; do not assume every schema variant is covered.

### TNAFlix

Its regular-video extraction is equivalent to EMPFlix at these revisions, with
site-specific URLs. Export named cast/links, description, upload date, categories,
thumbnail, duration and uploader; deduplicate category-derived tags. Mosaic and
preview URLs and engagement values are also available. Channel branding remains
separate from a production credit. Keep a distinct provider identity even though
the parser implementations are similar.

### Tube8

Like Thumbzilla, this exposes description, duration, thumbnail, title, date and
author. Performer, uploader-URL and preview fields are not populated; tags and
categories are absent. Video metadata and image metadata can be mixed by parser
fallbacks, so prefer the video's date. Porn Fetch uses a local Tube8 client wrapper
for routing, but its Video data still comes from this upstream model.

### XFreeHD

Export uploader name/URL/avatar, thumbnail, duration, tags, categories, displayed
date and rating. The public video ID is already extracted in `__post_init__` but
the GUI uses the title instead. No description, scene cast or studio field is
returned. Validate displayed date formats; preserve raw text when an exact date
cannot be established. Category fallback scanning can be broad, so treat it as
source taxonomy rather than verified production metadata.

### xHamster

Regular videos separate cast, categories, tags and uploader, and expose a
description, thumbnail, created value, rating, duration and content flags. The
current GUI prefers relative `date_ago` over `created_timestamp`; export should
prefer a parseable absolute creation value. Some missing numeric fields default
to zero, which must not be advertised as measured values without source evidence.
`orientation` describes a content category, not video rotation or aspect ratio.

**Moments differ:** title, creator/link/logo, tags, thumbnail/poster, duration,
created value and engagement are returned. No separate description, cast list or
studio credit is returned. Preserve the media kind in the export identity.

### XNXX

Export description, uploader, tags, thumbnail, duration and views. Prefer JSON-LD
`uploadDate`; do not treat a `dispo ... Loaded !` comment as a verified upload or
release date. The direct video parser does not populate `video_id`/`video_eid`,
although listings can seed them. Stable identity must work from a direct URL as
well. There is no separate cast or studio field. Minute-only duration fallbacks
are less precise than an actual file probe.

### XVideos

Export uploader/link, tags, description, image, displayed duration, engagement and
cast profile URLs. Description may duplicate the title. Cast labels are discarded
while parsing `li.model` links; expose them upstream instead of guessing names
from URL slugs. Direct video loading does not populate `video_id`, although
listing extraction can. As on XNXX, qualify/remove the comment-date fallback.
The preview clip URL is constructed from the thumbnail path rather than supplied
as a verified separate resource; do not promise it exists without checking.

### YouPorn

Export separate tags/categories, uploader ID/type/name/link, published-date text,
duration, thumbnail, rating and performer links. The `pornstars` helper resolves
those links with additional profile requests; it is an async generator property,
not an already-loaded list. Current generic CLI author fallback must not stringify
that object as a cast name. Expose link labels upstream for a cheaper path to
cast names. No video description or explicit studio field is returned.

### YouJizz

HTML provides description, publication data, tags, uploader identity, exact
duration when structured data has it and precise public rating/vote values. The
thumbnail API adds preview clip, sprite/count, HD flag and alternative title/
duration/views. Do not let optional API metadata unexpectedly replace localized
HTML choices. Sprite sheets are not posters. No scene cast list or studio field
is returned, even though the API also has separate pornstar profile classes.

## Cross-provider rules

- Omit unknown fields. An empty list, parser placeholder, zero fallback, website
  name or copied title is not a rich metadata result.
- Preserve publication semantics and precision. Upload, fact creation, image
  publication, relative display text and original release are different things.
  Relative text remains raw metadata by default, not an invented exact NFO date.
- HTML language, locale and segment/orientation fields do not establish spoken
  language, nationality, technical orientation or certification.
- A video thumbnail may be reused as primary artwork with its ratio preserved.
  Source coverage does not imply portrait posters, full backdrops or actor photos.
- Engagement can be retained with its original scale. No universal conversion
  from likes/percentages to Jellyfin community ratings is justified by this audit.
- No universal director, writer, production country, official age rating, IMDb/
  TMDb ID or original release date was found. Do not infer them from tags or URLs.

## Source revisions

Links below identify the exact audited parser source. Bellesa, Porndoe, RedGIFs and
YouJizz use extraction helpers in `modules/consts.py`; the other links point to
the video implementations. Versions are declared repository package versions,
not a claim that an environment or published wheel was upgraded.

| Provider | Version | Git revision |
| --- | --- | --- |
| [beeg][beeg] | 1.7.4 | `c65f06853dfc` |
| [bellesa][bellesa] | 1.0.0 | `a09699c0a208` |
| [empflix][empflix] | 1.0.1 | `d720a082d37b` |
| [eporner][eporner] | 2.5.3 | `36abac916a88` |
| [porn][porn] | 0.1.0 | `3bab77fd3385` |
| [porndoe][porndoe] | 1.0.1 | `739b107b701a` |
| [pornhat][pornhat] | 0.1.0 | `f27b1b4aa549` |
| [pornhub][pornhub] | 5.4.7 | `5f0e69548937` |
| [porntrex][porntrex] | 1.8.3 | `e428c219ed6b` |
| [redgifs][redgifs] | 1.0.0 | `ab6ded790c64` |
| [redtube][redtube] | 1.4.4 | `f5e0c5b91705` |
| [spankbang][spankbang] | 2.4.4 | `9c9f3f4c6ecc` |
| [thumbzilla][thumbzilla] | 1.4.3 | `1ef42e864373` |
| [tnaflix][tnaflix] | 1.0.1 | `dad878c484f9` |
| [tube8][tube8] | 1.3.3 | `54a4a1f195ab` |
| [xfreehd][xfreehd] | 1.7.4 | `ec0a808d146a` |
| [xhamster][xhamster] | 2.6.5 | `4b91daa64db2` |
| [xnxx][xnxx] | 2.4.4 | `b571ee7129a6` |
| [xvideos][xvideos] | 2.5.3 | `6fce1547c868` |
| [youporn][youporn] | 1.8.3 | `e9a3bd8ed611` |
| [youjizz][youjizz] | 0.1.0 | `7748080fb728` |

The shared FFmpeg implementation was inspected at
[`eaf_base_api 32a2877fda36`](https://github.com/EchterAlsFake/eaf_base_api/blob/32a2877fda36317b414f0f7700219bc625eaf3cd/base_api/modules/ffmpeg.py#L151).
Its object-based metadata path currently emits title, artist, genre and date;
adding fields to VideoObject alone will not export rich embedded metadata.

[beeg]: https://github.com/EchterAlsFake/unofficial-api-for-beeg/blob/c65f06853dfcc3c14053ae7e2efff1dcba0713e7/beeg_api/beeg_api.py#L87
[bellesa]: https://github.com/EchterAlsFake/unofficial-api-for-bellesa/blob/a09699c0a208768ac5a46e7c15d4d592c4270e25/bellesa_api/modules/consts.py#L76
[empflix]: https://github.com/EchterAlsFake/unofficial-api-for-empflix/blob/d720a082d37b65643552daeb2c06acbdd320ef1e/empflix_api/api.py#L108
[eporner]: https://github.com/EchterAlsFake/unofficial-api-for-eporner/blob/36abac916a8847b79162591fdc55c971993f2c2f/eporner_api/api.py#L90
[porn]: https://github.com/EchterAlsFake/unofficial-api-for-porn/blob/3bab77fd33858c0837c83de2b93fae39b3138e69/porn_api/api.py#L65
[porndoe]: https://github.com/EchterAlsFake/unofficial-api-for-porndoe/blob/739b107b701a3a2f964dd71ff09de97503bdf9da/porndoe_api/modules/consts.py#L166
[pornhat]: https://github.com/EchterAlsFake/unofficial-api-for-pornhat/blob/f27b1b4aa549f3c133a8d04a4109a2feeeb18ede/pornhat_api/api.py#L128
[pornhub]: https://github.com/EchterAlsFake/unofficial-api-for-pornhub/blob/5f0e6954893721d7175aff97b8fed036a2f975ac/pornhub_api/api.py#L2550
[porntrex]: https://github.com/EchterAlsFake/unofficial-api-for-porntrex/blob/e428c219ed6bdc47e3d860b24a15f23f0f7f5f4f/porntrex_api/api.py#L85
[redgifs]: https://github.com/EchterAlsFake/unofficial-api-for-redgifs/blob/ab6ded790c6467a2f172ae2e2de036235f4a1cd2/redgifs_api/modules/consts.py#L43
[redtube]: https://github.com/EchterAlsFake/unofficial-api-for-redtube/blob/f5e0c5b917053f6c16f62ef7444a23d65baaf38a/redtube_api/api.py#L139
[spankbang]: https://github.com/EchterAlsFake/unofficial-api-for-spankbang/blob/9c9f3f4c6ecc0ce35653036640554c50c463b33b/spankbang_api/api.py#L265
[thumbzilla]: https://github.com/EchterAlsFake/unofficial-api-for-thumbzilla/blob/1ef42e8643736b0db36c8fa5386eb17ba47878c2/thumbzilla_api/api.py#L113
[tnaflix]: https://github.com/EchterAlsFake/unofficial-api-for-tnaflix/blob/dad878c484f93871ad4482fec60b1af1b1f77927/tnaflix_api/api.py#L108
[tube8]: https://github.com/EchterAlsFake/unofficial-api-for-tube8/blob/54a4a1f195ab0141bcdc6aa7f42f6bd42b3fbbd4/tube8_api/api.py#L158
[xfreehd]: https://github.com/EchterAlsFake/unofficial-api-for-xfreehd/blob/ec0a808d146aeb59900bd2a6db054b2c547b8d43/xfreehd_api/api.py#L119
[xhamster]: https://github.com/EchterAlsFake/unofficial-api-for-xhamster/blob/4b91daa64db28e035bb83919a2fdd1902ca8233c/xhamster_api/api.py#L466
[xnxx]: https://github.com/EchterAlsFake/unofficial-api-for-xnxx/blob/b571ee7129a6c195a08679fea4881477e783c10d/xnxx_api/api.py#L86
[xvideos]: https://github.com/EchterAlsFake/unofficial-api-for-xvideos/blob/6fce1547c868bcab3d98a4dae3ea1cef75d9d11b/xvideos_api/api.py#L175
[youporn]: https://github.com/EchterAlsFake/unofficial-api-for-youporn/blob/e9a3bd8ed6110a9e3a660623dd3dcd38bdc8358d/youporn_api/api.py#L446
[youjizz]: https://github.com/EchterAlsFake/unofficial-api-for-youjizz/blob/7748080fb728ea1adac84ed8ab4b8705e705f4b9/youjizz_api/modules/consts.py#L75
