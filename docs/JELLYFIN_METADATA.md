# Jellyfin metadata export

## Use Media Library Export

Desktop Settings → Video → **Media Library Export · Premium** enables automatic
NFO, JSON and available primary-artwork export. Choose sidecars beside each video
or one folder per new video. Export is off by default. Source categories can be
mapped to genres; mapping credited providers/publishers/channels into the studio
field is a separate, unchecked option. Unsupported metadata stays empty.

To repair an existing file, choose it in the same panel, optionally enter its
original video URL, preview the fields and choose Export metadata. A matching
Porn Fetch JSON record allows local regeneration without fetching the source.
Existing and manually edited NFO/artwork are preserved. Automatic export does not
modify a file skipped by the downloader.

CLI examples:

```sh
porn-fetch-cli --url VIDEO_URL --metadata-export jellyfin --metadata-layout scene-folder
porn-fetch-cli --export-metadata-for /media/example.mp4 --source-url VIDEO_URL --dry-run
porn-fetch-cli --export-metadata-for /media/example.mp4 --source-url VIDEO_URL
porn-fetch-cli --export-metadata-for /media/example.mp4
```

Repeat `--export-metadata-for` for multiple files. Supply one `--source-url` per
file, or omit URLs to use saved JSON. `--replace-metadata` explicitly authorizes
replacing sidecars during metadata-only export. `--metadata-genres` and
`--metadata-studio-fallback` control the optional mappings. These operations check
the existing Premium entitlement; generated files need no license to read.

The optional server connection requires a server URL, a local media root and the
corresponding root inside Jellyfin. Store the API key through the desktop password
field or provide `PORNFETCH_JELLYFIN_API_KEY` in the CLI environment. Keys are kept
separately from settings and exports, in the shared app-data directory, with mode
0600 on Unix. Requests use a dedicated session without provider cookies, follow
the All app traffic Tor policy and never silently fall back to a direct route.
Notifications are batched after sidecars are written. This does not upload videos.

Activity provides retry for failed automatic exports/notifications in the current
session. CLI notification retry is `--retry-jellyfin /media/example.mp4`. After a
restart, use metadata-only export to repair a bundle; if its JSON was never saved,
provide the original URL again. Metadata-only operations do not prepare download
qualities or transfer media, although a provider's own metadata loader can include
a player-service request.

The initial UI is desktop-only. Native mobile document-tree/MediaStore bundle
publication is deliberately unavailable until separately implemented and verified.

The eight provider metadata updates were published on GitHub and PyPI on
2026-11-14: Bellesa 1.0.1, Porndoe 1.0.2, Eporner and XVideos 2.5.4, YouPorn
1.8.4, XNXX 2.4.5, Pornhub 5.4.8 and Beeg 1.7.5. Porn Fetch's dependency
minimums now require these releases. The development environment's editable
provider installs can be replaced with package-index releases using `uv sync`.

## Research and design

Research date: 2026-11-14. The research and implementation design below explain
the export policy; the usage section above describes the implemented workflow.
Findings use the current repository, Jellyfin's public
documentation and upstream source. The follow-up [provider audit](PROVIDER_METADATA.md)
pins all 21 provider revisions and checks their extraction code. Jellyfin links
to `master` can change; supported server releases and clients must be verified
during implementation.

## Recommendation

Build **Media Library Export** as a Premium feature. The first release should
turn each completed download into a portable library folder containing the video,
NFO metadata, local artwork and a versioned Porn Fetch JSON record. Follow with
bulk export for existing downloads and an optional Jellyfin connection.

The customer benefit is a library ready to browse by title, performer, studio,
date and tags, using the information available from each provider. Exporting
during acquisition avoids having to identify the same video again later.

This fits the existing €29.99 lifetime Premium offer. Existing Premium customers
already have all future released features included; this should be another reason
to buy Premium, with no separate integration subscription. See
[the existing offer](LICENSING.md#premium-licenses).

## What Jellyfin supports

- Local NFO metadata is built in. Jellyfin reads it with priority over remote
  metadata. It supports titles, plots, dates, runtime, studios, actors, genres,
  tags and provider identifiers. Enabling the NFO saver is for Jellyfin's own
  exports, not a prerequisite for importing Porn Fetch's files.
  [Jellyfin NFO documentation](https://jellyfin.org/docs/general/server/metadata/nfo/)
- Movies can use individual folders with local artwork. Supported image names
  include `poster`, `fanart` and `landscape`. Movies also support multiple video
  versions with matching filename prefixes and version suffixes.
  [Movie organization and artwork](https://jellyfin.org/docs/general/server/media/movies/)
- A dedicated Movies library is the proposed target for individual scenes.
  Jellyfin discourages mixed libraries because of unreliable metadata results.
  [Library types](https://jellyfin.org/docs/general/server/libraries/)
- The upstream NFO parser accepts arbitrary named `uniqueid` providers. A Porn
  Fetch identifier can therefore be retained as metadata. This does not install
  a provider that resolves that identifier, or guarantee automatic deduplication.
  [NFO parser](https://github.com/jellyfin/jellyfin/blob/master/MediaBrowser.XbmcMetadata/Parsers/BaseNfoParser.cs)

A Jellyfin server plugin is unnecessary for this first release. A separate API
connection can add convenience later without becoming a requirement for playback.

## Current Porn Fetch capabilities and gaps

| Area | Repository finding | Proposed change |
| --- | --- | --- |
| Metadata output | `src/shared/metadata.py` delegates embedded MP4 tags and thumbnail writing to `eaf_base_api`; there is no NFO exporter. | Keep embedded tags and add a separate sidecar exporter. |
| Shared data | `src/shared/media.py:VideoObject` keeps title, author, rounded duration minutes, tags, thumbnail, URL, ID and publication date. | Preserve description, separate performers/studios/uploader, provider identity and precise duration when available. |
| Field meaning | `author` can represent uploader, channel or a joined performer list, depending on provider. | Export explicit roles; never infer the cast or studio from `author`. |
| Stable identity | GUI preparation in `src/backend/clients.py` uses the title as `video_id` for several providers. CLI preparation also has a title fallback. | Use actual provider IDs where available, otherwise a deterministic identity from a canonical public page URL. |
| Preparation | GUI and CLI prepare metadata separately in `src/backend/clients.py` and `src/cli/media.py`. | Share export normalization so the same source produces equivalent files in both frontends. |
| Paths | `src/shared/download_options.py` already sanitizes template values and supports folders. | Add an explicit library preset and collision-safe provider identity; current placeholders lack a provider field. |
| Completion | GUI and CLI have separate completion/tagging paths. | Call one shared exporter after successful completion; support a metadata-only retry. |
| Mobile | GUI completion exports one video file through `_save_to_output_folder`; Android uses document trees or MediaStore. | Treat a multi-file library package as additional storage work, not as automatically supported by the current video export. |

The [completed source audit](PROVIDER_METADATA.md) found nine providers with
direct cast names and three with cast profile URLs. Nine currently expose no
separate populated cast list. No provider supplies a universally reliable
production-studio field. Bellesa credits content providers; Porndoe combines
producer and publisher roles. Most remaining organization-like credits are
uploaders or channels. Runtime fill rates remain unmeasured: this was a source
audit, not a live-site survey.

Lazy fields must be loaded through the existing async `BaseMedia`/`BaseCore`
mechanisms. Export should not depend on retaining an arbitrary native provider
object or serializing its internals.

## Proposed export contract

Use one scene per folder. Include a provider and stable ID in the folder and
basename to distinguish identical titles. Omit an unknown year instead of using
the download year. For example, with fictional metadata:

```text
Library/
  Example Scene (2026) - bellesa-12345/
    Example Scene (2026) - bellesa-12345.mp4
    movie.nfo
    poster.jpg
    landscape.jpg
    fanart.jpg
    pornfetch.json
```

Artwork files are conditional. Preserve a provider's landscape thumbnail as
landscape artwork; offer a poster crop or padded composition with a preview when
no portrait image exists. Do not stretch it or promise distinct artwork where
only one image exists. Save actual image bytes with the correct extension.

| Preserved field | NFO representation | Export policy |
| --- | --- | --- |
| Title / description | `title` / `plot` | Omit missing descriptions; normalize markup to readable text. |
| Publication date | `premiered`, `year` | Keep provider publication semantics; do not invent an original studio release date. |
| Performers | Repeated `actor` elements with `name` | Only explicitly supplied cast; keep IDs/profile URLs in JSON too. |
| Studio | Repeated `studio` elements | Only known production studios; source website and uploader stay separate. |
| Tags / categories | Repeated `tag`; optional curated `genre` | Preserve tags without turning every tag into a genre. |
| Duration | `runtime` in minutes | Keep exact seconds in JSON if available; let Jellyfin probe the downloaded file. |
| Source identity | `uniqueid` with a Porn Fetch namespace | Use a provider-qualified ID; never fabricate IMDb/TMDb identifiers. |
| Source URL / export details | `pornfetch.json` | Keep canonical public page URL, schema version and export timestamp. |

These mappings use Jellyfin's supported fields and Kodi's movie NFO structure.
Runtime is measured in minutes in the NFO format. Technical stream details should
come from the downloaded file, not the requested quality or rounded duration.
[Jellyfin NFO fields](https://jellyfin.org/docs/general/server/metadata/nfo/),
[Kodi movie NFO specification](https://kodi.wiki/view/NFO_files/Movies)

Illustrative NFO, with only known fields emitted:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<movie>
  <title>Example Scene</title>
  <plot>Provider-supplied description.</plot>
  <premiered>2026-10-01</premiered>
  <year>2026</year>
  <studio>Example Studio</studio>
  <actor><name>Example Performer</name></actor>
  <tag>Example category</tag>
  <uniqueid type="pornfetch" default="true">bellesa:12345</uniqueid>
</movie>
```

Use a standard XML serializer for escaping. JSON is a documented, allowlisted
export of normalized data, not a dump of the provider object. It preserves fields
that have no reliable Jellyfin mapping and supports later re-export without
fetching the source again. Jellyfin does not consume `pornfetch.json` itself.

Download artwork locally through the provider core. Avoid expiring CDN URLs,
authenticated image URLs, cookies, stream URLs and tokens in exported files.
Performer photos are a later enhancement: verify Jellyfin's actor-image handling
and paths from the server/container before claiming they work portably.

## Optional Jellyfin connection

The video and sidecars must first reach storage Jellyfin can read. The integration
should initially use a local folder or an already mounted NAS share. A metadata
API call does not upload the video or make a client filesystem path available to
the server.

Let the user configure server URL, credential, target library and a path mapping,
for example `/mnt/nas/library` locally to `/media/library` inside the Jellyfin
container. After publishing a complete bundle, batch change notifications with:

```http
POST /Library/Media/Updated
Content-Type: application/json

{"Updates":[{"Path":"/media/library/Example Scene (2026) - bellesa-12345/Example Scene (2026) - bellesa-12345.mp4","UpdateType":"Created"}]}
```

This endpoint reports changed paths to the library monitor. A successful response
does not prove the scan has finished. Refreshing an existing item uses
`POST /Items/{itemId}/Refresh`; it cannot discover a new file without an item ID.
Avoid scanning every library after every download. Verify endpoint behavior and
credential permissions against the server releases actually supported.
[Library controller](https://github.com/jellyfin/jellyfin/blob/master/Jellyfin.Api/Controllers/LibraryController.cs),
[change notification schema](https://github.com/jellyfin/jellyfin/blob/master/Jellyfin.Api/Models/LibraryDtos/MediaUpdateInfoDto.cs),
[path schema](https://github.com/jellyfin/jellyfin/blob/master/Jellyfin.Api/Models/LibraryDtos/MediaUpdateInfoPathDto.cs),
[item refresh controller](https://github.com/jellyfin/jellyfin/blob/master/Jellyfin.Api/Controllers/ItemRefreshController.cs)

Use the existing asynchronous networking stack with explicit Jellyfin-specific
configuration. Keep credentials out of logs and exports. Define local-server
routing explicitly under Tor modes; never silently bypass the user's policy.
An unavailable server should leave the video and metadata export successful,
with a separately retryable notification.

## Paid feature boundary and product sequence

| Stage | Deliverable | Relative effort |
| --- | --- | --- |
| 1 | Premium export preset: NFO, available local artwork, JSON, stable paths and GUI/CLI parity for new downloads. | Moderate; metadata normalization is the main prerequisite. |
| 2 | Bulk export and repair for previously downloaded files, field preview, artwork choice and dry run. | Moderate to high; matching old files safely needs explicit source associations. |
| 3 | Optional Jellyfin connection, path mapping, batched notifications and retry status. | Moderate; server/storage setup drives support costs. |
| Later | Performer images, user-controlled alias/tag rules, collections and additional server profiles. | Variable; validate each compatibility claim. |

Keep existing embedded MP4 metadata behavior available as it is. Premium gates
new library export and automation in shared backend code used by GUI and CLI.
Generated files remain readable indefinitely, including when Porn Fetch's
license cannot currently be validated. Existing sidecars should not depend on a
running Porn Fetch installation.

Backfilling should start with a known source URL or saved source identity. Old
title-based IDs and incomplete download history cannot reliably identify every
file. Do not promise universal automatic matching or cross-site deduplication.

## Existing ecosystem and differentiation

This is an established use case. Stash's community **mcMetadata** plugin already
exports NFOs, artwork and performer images and offers organization, dry runs and
bulk processing. The **Jellyfin.Plugin.Stash** project offers a metadata provider
backed by a local Stash instance.
[mcMetadata](https://github.com/carrotwaxr/stash-plugins/blob/main/plugins/mcMetadata/README.md),
[Jellyfin.Plugin.Stash](https://github.com/DirtyRacer1337/Jellyfin.Plugin.Stash)

Porn Fetch's proposed distinction is acquisition-time export with no separate
catalog service to populate first. This is a product hypothesis, not evidence of
market size or willingness to pay. Ask interested users to try a small export
and assess time saved before investing in advanced server management.

The same NFO foundation could support Kodi and a Stash import workflow: Stash's
community nfoSceneParser can import scene information from NFOs. Treat those as
separate verified profiles rather than claiming universal interoperability.
[Stash NFO importer](https://github.com/stashapp/CommunityScripts/blob/main/plugins/nfoSceneParser/README.md)

## Implementation and focused verification

- Keep normalization and writers in Qt-free `src/shared`; use stdlib XML/JSON.
  Keep networking async and reuse provider cores and caching.
- Write sidecars through temporary siblings and replace completed files. Stage
  new bundles outside the watched library when possible; notify Jellyfin only
  after publication. Do not export paused, cancelled or incomplete downloads.
- Preserve existing user-authored NFO/artwork by default. Track generated files
  separately, preview replacements and leave whole-item metadata locking opt-in.
  Avoid having both Jellyfin's NFO saver and Porn Fetch overwrite the same files.
- Represent video completion, metadata export and server notification separately.
  An export failure must support retry without downloading the video again.
- Support ordinary desktop and headless CLI filesystems first. Mobile export
  needs explicit support for sidecars and directories at the chosen destination;
  a ZIP export is an option for later transfer, not something Jellyfin scans.
- Verify one real import on the chosen supported Jellyfin release and a repeat
  scan: title, date, tags, explicit cast/studio, images, custom ID and playback.
  Also check equivalent GUI/CLI export, XML escaping, preserved edits, a cancelled
  download producing no bundle and a failed notification preserving export.
- New settings/dialogs must follow existing keyboard and TV remote navigation
  requirements. No changes to licensing lifecycle behavior are needed.

The initial research did not modify an existing Jellyfin instance. Implementation
validation on 2026-11-14 used a disposable, loopback-only Jellyfin 12.4.0 server
with synthetic video and artwork. Import verified title, description, platform
date/year, actor, producer, tags, genres, custom Porn Fetch ID and primary image.
A repeat scan retained the item ID; the actual change-notification endpoint
accepted the application request, and direct playback returned the original
video bytes. This establishes that server's import/API behavior, not every client
or live provider's current field availability. The fixture server was stopped
after verification; existing servers and user libraries were not touched.

## Concrete implementation plan

This sequence is based on the pinned [provider audit](PROVIDER_METADATA.md).
The initial deliverable is desktop and headless CLI export for new downloads,
with all 21 providers producing the subset they actually support. It requires no
new database, Jellyfin server plugin or external metadata service. Application
and provider implementation changes below are proposed, not already made.

### 1. Retain source roles and fix ambiguous provider output

Make small changes in the provider repositories, release them, then raise Porn
Fetch's minimum versions in desktop and mobile dependency inputs. Keep downloads
and routing behavior separate from these metadata changes.

| Repository / extraction path | Specific change | Why it comes first |
| --- | --- | --- |
| Bellesa `modules/consts.py:video_fields` | Add full content-provider references with IDs/handles, names and URLs; retain existing author fields. | Multiple provider names are currently discarded. Preserve the credited role without declaring a studio. |
| Porndoe `modules/consts.py:extract_video` | Preserve producer and publisher separately; mark/omit title-only description fallback. | The current combined author cannot establish a production credit. |
| Eporner `Video._extract_html` | Retain the names and URLs already available in JSON-LD actor objects. | Avoid another request for each performer just to obtain a name. |
| XVideos `Video._extract_html` | Retain cast link labels; qualify publication-date source; expose stable public-route identity independently of listing seeds. | Avoid slug-derived cast names and comment timestamps presented as publication dates. |
| YouPorn `Video._extract_data` | Retain cast link labels alongside existing URLs. | Avoid resolving every performer profile for basic credits. |
| XNXX `Video._extract_html` | Qualify/remove the `dispo` comment-date fallback; provide public-route identity for direct links. | A listing-only ID and an unqualified timestamp are unreliable export inputs. |
| Beeg `Video._load_api` | Preserve typed owner/person references separately from flattened tags and author; retain the media key. | Existing role flags are lost. Validate person-tag semantics before promoting them to cast credits. |
| Pornhub `Short._extract_html` | Require a match for an explicitly requested short before returning metadata, or report that identity is unconfirmed. | Export must not silently attach the first short's metadata to another requested item. |

Do not block basic export on adding unsupported studio/cast extraction to every
provider. For example, Tube8 and Thumbzilla can ship their real title, description,
date, image and duration subset while cast/taxonomy remain unavailable. Where a
publication source cannot yet be distinguished, omit the ambiguous NFO date.

### 2. Add one Qt-free export snapshot and provider adapter

Create `src/shared/library_metadata.py` for a small set of dataclasses and
`src/shared/provider_metadata.py` for explicit per-provider extraction. Use a
provider dispatch table, not generic reflection across similarly named fields.

The proposed snapshot contains:

| Group | Fields / meaning |
| --- | --- |
| Identity | Schema version, provider, media kind (`video`/`short`), public source ID, canonical page URL; named alternate IDs where useful. |
| Text | Title, optional nonduplicate description. |
| Timing | Precise duration seconds when known; raw publication text, normalized date, source kind and precision. Keep original-date semantics separate from export time. |
| People and credits | Explicit performer references; uploader/creator reference; separate channels, publishers, content providers and producers. A reference needs only name, optional ID and URL. |
| Classification | Separate source tags and categories, with stable order and duplicate removal. |
| Images | Available cover/thumbnail references and their actual roles; no implied portrait/backdrop classification. |
| Optional extras | Allowlisted engagement values with their scales, source flags, niche IDs and action markers. No raw provider objects or dictionaries. |

Keep runtime image-fetch references separate from the portable JSON representation;
persist downloaded artwork paths rather than expiring or authenticated URLs.
Canonical public profile links may be retained. Do not walk into profiles,
comments, related scenes, accounts or media manifests just to build the default
snapshot.

Call `collect_library_metadata(provider, source_video, prepared_video)` from both
`src/backend/clients.py` and `src/cli/media.py` when Premium export is enabled.
Reuse already-loaded sources. Any additional lazy loading uses `load_fields` or
`load_sources` on the existing core, respecting language and network policy.
Keep prepared display titles and existing quality calculations authoritative;
metadata collection must not switch them by fetching a higher-priority source.
Separate precise duration parsing from the current rounded display minutes.

Attach the result through an optional `VideoObject.library_metadata` field. Update
GUI resume's metadata refresh assignment to include it. Explicitly exclude this
nested object from `download_recovery.SAVED_FIELDS` and recollect it on resume;
the current automatic field enumeration is not a nested-dataclass serializer.
Do not turn queue checkpoints into a new metadata/history store.

Maintain a small static capability table for previews: supported-but-empty and
unsupported fields should be distinguishable without constructing a general
provenance framework. Dates and organizational roles need explicit semantics;
most simple text fields do not need a separate provenance object each.

### 3. Establish export identity and field rules

Use `provider + media_kind + public_source_id` for export identity. Prefer
provider IDs that are stable for both direct and listing-created videos. Beeg
uses its media key; SpankBang uses its public route token. For XVideos/XNXX,
preserve public route tokens and listing/internal numeric IDs as distinct values
unless their equivalence is established. Use a canonical-public-URL digest only
when no stable source ID can be extracted, and label it as a URL-derived key.

Never use a title as identity, merge cross-site videos automatically, or treat a
short as the full video. New export paths use the stable identity. Existing files
are not renamed when the export setting is enabled.

Default NFO rules:

- `title`: the existing selected display title. `plot`: a genuine available
  description, excluding missing values and title-only duplicates.
- `actor`: explicit scene cast only. Profile URLs without resolved names remain
  references in JSON. Prefer the proposed same-page API improvements over extra
  performer-profile requests.
- `studio`: an explicit producer or user-confirmed mapping. Credited providers,
  publishers, channels and uploaders stay distinct in JSON. The preview can offer
  an explicit choice to map credited providers/channels into the studio field.
- `premiered`/`year`: a sufficiently precise source-platform publication/video
  creation date, described as such. Exclude relative estimates, page comments,
  fact creation and image dates. Original production release remains unknown
  unless explicitly supplied.
- `tag`: source tags; retain source categories separately and optionally map them
  to genres. Keep rating snapshots in JSON initially; omit unsupported official
  ratings, director/writer credits and invented external IDs.
- `runtime`: use known duration or a probe of the final media; never multiply
  rounded display minutes and label the result as precise seconds. Omit technical
  stream details when no file-derived measurement exists.

### 4. Write a portable bundle without changing embedded-tag behavior

Create `src/shared/library_export.py` with `plan_export(...)` and
`export_library_bundle(...)`. Use standard-library XML/JSON. Reuse the injected
provider core for image downloads and existing filename sanitation. NFO/JSON
export itself must not require FFmpeg.

The explicit Jellyfin folder preset produces one scene folder, `movie.nfo`,
`pornfetch.json` and available primary artwork. Preserve source image aspect ratio
and actual file format. Do not generate cropped posters, synthesize backdrops or
download preview videos in the first release. A later artwork editor can add
those choices. Reject sprite/mosaic/timeline images as primary cover candidates.

For metadata-only export beside an existing file in a shared directory, use
`<stem>.nfo`, `<stem>-poster.<ext>` and `<stem>.pornfetch.json`. This avoids a shared
`movie.nfo` describing multiple unrelated videos. Folder organization applies to
new downloads only when explicitly selected.

The versioned JSON records normalized source data, selected file identity and an
allowlist of generated relative paths/digests. Use that record to identify which
sidecars Porn Fetch generated and detect later edits; do not overwrite unrelated
or edited NFO/artwork by default. Preview replacements and make forced replacement
an explicit action. Write each sidecar through a temporary sibling and replace it
on completion. Stage new folders outside the watched library when practical.

Preserve `write_tags` and current embedded-tag behavior. The inspected base API's
object path emits only title/artist/genre/date, so a richer VideoObject alone will
not change embedded output. If richer embedding is added later, pass a controlled
metadata mapping supported by the base API; never pass the complete export JSON
as FFmpeg metadata.

### 5. Integrate completion, retry and shared Premium enforcement

Add the new export entitlement check in `src/shared/access.py`, using the existing
licensing service result. Enforce it at export execution for GUI and CLI. Keep
metadata already written readable permanently and leave existing free embedded
metadata behavior available.

Invoke one shared finalization function from GUI completion in
`src/backend/application.py` and CLI completion in `src/cli/downloads.py`. Remove
duplicate post-download export responsibilities from individual CLI flows as
they adopt that function, including batch, single, scrape, tracked-model and
resume paths. This also addresses the currently separate fallback-tagging paths.

Keep three outcomes distinct: video saved, metadata export, server notification.
Paused/cancelled/failed transfers do not publish a bundle. A skipped existing
file is not automatically re-exported; metadata-only mode handles it explicitly.
An export failure leaves the video intact and offers retry against the same file
and snapshot, without downloading it again. Persist only an allowlisted pending
export record when retry must survive an app restart; the normal exported JSON
supports subsequent local regeneration. Reuse cache storage, not another DB.

### 6. Expose settings and metadata-only export

Add matching GUI/CLI settings for export mode (`off`/`jellyfin`), output layout
(`alongside`/`scene-folder`) and category-to-genre mapping. Default to off until
the user chooses export. Keep studio fallback disabled by default. A per-item
preview shows available values and identifies uploader/channel/provider roles
without pretending empty fields have been filled.

Proposed batch interface: `--metadata-export jellyfin` for normal downloads, and
`--export-metadata-for FILE --source-url URL [--dry-run]` for an existing file.
Wire these into `build_parser`, `ACTION_DESTINATIONS`, settings conversion and
action dispatch. Metadata-only mode must not enter the download/quality path.
Local regeneration from a matching saved Porn Fetch JSON should work offline.
Bulk regeneration starts with these saved records or explicit file/URL pairs;
matching arbitrary historical filenames is outside the initial release.

Add the corresponding keyboard-accessible GUI export settings and a preview/
retry action using existing notifications. Preserve Tab/D-pad navigation, visible
focus, Back/Escape behavior and focus restoration.

### 7. Add the optional server connection after portable export works

Create `src/shared/jellyfin.py` using the existing async transport. Configure a
server URL, credential and explicit local-to-server path mapping. Publish all
sidecars before batching `/Library/Media/Updated` notifications. Retry an offline
server independently from video/export status. Use a targeted refresh only after
an item ID exists. Do not add remote file upload or whole-library scanning to
every completion.

Keep this optional and local-first. Define credential storage and routing under
existing Tor modes before exposing Connect. No media inventory or source URLs
need to be sent to Porn Fetch's licensing/payment service.

### 8. Validate the first release and defer independent features

Use focused offline fixture checks for the 21 extraction mappings, including
the two short types and the semantics found in this audit. Check XML escaping,
unknown fields, distinct roles, source identity from a direct link and a listing,
and preservation of manual sidecar edits. Reuse provider fixtures for upstream
changes. Do not expand licensing lifecycle testing.

Exercise normal GUI and CLI completion plus resume once, verify metadata-only
mode transfers no media, and check that an export/notification failure preserves
the video. Then import a small representative library into a specifically
recorded Jellyfin version and verify cast, dates, taxonomy, artwork and a repeat
scan. Live provider checks remain explicit and opt-in; source coverage is not a
claim of current per-site availability.

Defer automatic performer photos/profile enrichment, collections, chapter export,
cross-site matching, poster generation, external metadata databases and remote
file transfer. Mobile has the same normalized data, but document-tree/MediaStore
bundle publication needs a separate implementation; enable mobile export only
after its actual multi-file destination behavior has been verified.

The first release is complete when every registered provider has an explicit
mapping, all entry points use the shared export/finalization behavior, incomplete
downloads publish nothing, edited metadata is preserved, and a recorded Jellyfin
import demonstrates the supported subset. Empty studio fields are a correct
outcome when no reliable production credit exists.
