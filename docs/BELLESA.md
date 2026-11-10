# Bellesa in Porn Fetch

Porn Fetch uses the published [unofficial-api-for-bellesa 1.0.0](https://pypi.org/project/unofficial-api-for-bellesa/1.0.0/)
package. Only **Video, Channel and Performer** are integrated. Source/library docs
are at [Bellesa API](https://docs.echteralsfake.me/bellesa/).

## Entry points

| Type | Example | Porn Fetch flow |
|---|---|---|
| Video | `https://www.bellesa.co/videos/7054` | Video URL / batch URL |
| Channel | `https://www.bellesa.co/channels/zero-to-hero` | Model URL / CLI profile URL |
| Performer | `https://www.bellesa.co/performers/lily-starfire` | Model URL / CLI profile URL |

Bare `bellesa.co` and `www.bellesa.co` are accepted. Video URLs may include a title
slug after the numeric ID. The CLI's username/handle prompt offers `bellesa` and
constructs a Performer URL; paste a full URL for a channel. These use the existing
queue, filters, selection, output, metadata and download controls.

The router rejects homepages, directories, category/search/story URLs, unsupported
profile tabs, unrelated subdomains, lookalike hosts and credential-bearing URLs.
The library's other getters, search, categories, related-video methods and account
capabilities are not exposed through Porn Fetch.

## Preparation, downloads and lifecycle

Both GUI and CLI load API metadata and the lazy media source. The standard app row
retains title, first channel/provider as author, stable ID, tags, thumbnail and UTC
publication date. Duration seconds are converted to the app's rounded minutes.
A 31-second video displays 1 minute; the 619-second sample displays 10 minutes.

Qualities use measured rendition dimensions, not site marketing labels. A site
label of 480 commonly measures 800x450. An older 4:3 sample exposes 640x480,
800x600 and 1280x960, represented as 480/600/960p. Both adapters resolve these
through the library's media loader. Numeric app qualities go unchanged to shared
HLS selection. Porn Fetch uses HLS for this provider; no separate MP4-format UI
was added.

The usual free quality limit of 720p and five-video public profile preview apply.
The preview is applied before filters and index ranges. Measured dimensions also
apply at CLI download dispatch, including when no prepared row was supplied.
Existing metadata, filename presets, queue progress, mobile export and retained
HLS segment stop/resume paths remain in use.

The GUI owns a Bellesa MediaCore/client alongside the other providers. Settings
refresh replaces its session in place, retires and closes the old session, and
preserves the client/core identity. Shutdown closes it. CLI clients come from the
shared ClientPool and close with the pool. All requests/downloads use the supplied
shared backend; no independent transport or downloader was introduced.

## Packaging

- Desktop/CLI dependency: `unofficial-api-for-bellesa>=1.0.0` in `pyproject.toml`.
- Android: Bellesa is included in `buildozer.spec` requirements.
- iOS: the pure requirements pin 1.0.0; device preparation installs the pure wheel
  into archived overlays without replacing native dependencies.
- GUI static imports and CLI provider-registry discovery include the module in
  the existing desktop packaging paths.
- Provider permission and third-party inventories include the additional package.

Native Android/iOS artifacts and signed desktop installers were not rebuilt in
this integration. Source dependency inputs and the Python distribution were checked.

## Live verification on 2026-11-10

Checks used the **published PyPI wheel**, Python 3.15.2, eaf-base-api 4.2.6 and
PySide6 6.12.0. Files/state/configuration were isolated in temporary directories.
No browser cookies, production license lifecycle or user download folders were used.

- Six real host/type combinations passed: both accepted hosts for Video, Channel
  and Performer. Unsupported application routes were rejected.
- Four real GUI profile cases passed, two rows each, with Qt row roles/signals,
  source identity, author/duration/thumbnail/qualities and HLS stream resolution.
- Five complete public profile listings matched independent rendered state:

| Profile | Pages | Expected IDs | App stream IDs | Free preview |
|---|---:|---:|---:|---:|
| performers/lily-starfire | 1 | 3 | 3 | 3 |
| performers/kenna-james | 7 | 57 | 57 | 5 |
| channels/belle-says | 1 | 4 | 4 | 4 |
| channels/zero-to-hero | 2 | 30 | 30 | 5 |
| channels/erikalust | 1 | 24 | 24 | 5 |

The comparisons preserved sequence and checked beyond-last termination. Lily
Starfire's broader profile count is 7 while the free listing contains 3. Channel
pagination uses the filtered video endpoint, avoiding the site's page-dropping
channel redirect. No missing, unexpected or duplicate IDs remained.

Eight complete CLI files passed ffprobe dimensions, audio, duration and exported
title/artist checks:

| Video | Request / access | Selected quality | Output | Duration (s) | Bytes |
|---|---|---:|---|---:|---:|
| 7054 | 360 / premium | 360 | 640x360 | 30.101 | 2410854 |
| 7054 | 450 / premium | 450 | 800x450 | 30.135 | 4654319 |
| 7054 | 720 / premium | 720 | 1280x720 | 30.135 | 8119734 |
| 7054 | 1080 / premium | 1080 | 1920x1080 | 30.135 | 13412464 |
| 7054 | 1440 / premium | 1440 | 2560x1440 | 30.135 | 23497921 |
| 7054 | 2160 / premium | 2160 | 3840x2160 | 30.135 | 47581187 |
| 7054 | best / free | 720 | 1280x720 | 30.135 | 8119734 |
| 1094 | best / free | 600 | 800x600 | 618.432 | 102069504 |

The six explicit qualities cover every rendition exposed by the short sample.
Free-best selected 720p for video 7054 and 600p for the 4:3 video 1094, staying
within the free entitlement boundary.

- CLI lifecycle: **2 passed, 0 failed, 0 manual** at 450p. Pause retained two
  segments and resume reused them; cleanup removed resumable state and a fresh
  download requested all segments again. Finished output was FFmpeg-readable.
- Real desktop QML Downloads controls: **3 passed, 0 failed, 0 blocked, 0 manual**
  at 450p for pause/resume, cleanup and remove.
- Real GUI client settings/session refresh and shutdown passed; title, duration,
  author and measured qualities survived refresh on the same client/core.
- Focused unit checks: **84 passed**. Pyright: **0 errors, 0 warnings**.

## Repeatable commands

From the project root with dependencies installed:

```sh
uv run --no-sync python -m src.tests.smoke.bellesa --report /tmp/bellesa-app-integration.json
QT_QPA_PLATFORM=offscreen QT_QUICK_BACKEND=software uv run --no-sync python -m src.tests.smoke.profile_urls --filter bellesa --include-variants --items 2 --report /tmp/bellesa-app-profiles-gui.json
uv run --no-sync python -m src.tests.smoke.download_lifecycle --provider bellesa --quality 450 --report /tmp/bellesa-app-lifecycle.json
QT_QPA_PLATFORM=offscreen QT_QUICK_BACKEND=software uv run --no-sync python -m src.tests.smoke.download_gui --provider bellesa --quality 450 --report /tmp/bellesa-app-gui-downloads.json
```

These commands make real requests; download checks transfer complete media.
`bellesa --metadata-only` keeps route/profile checks and omits media downloads.
The interactive test helper classifies this suite as both online and media-enabled.
Normal unit discovery makes no provider requests.

Exact offline check selection used for this integration:

```sh
uv run --no-sync python -m unittest src.tests.unit.test_provider_features src.tests.unit.test_provider_parsing src.tests.unit.test_download_gui_inventory src.tests.unit.test_ios_app src.tests.unit.test_legal_documents src.tests.unit.test_api_audit_routes src.tests.unit.test_cli_services src.tests.unit.test_cli_wizard src.tests.unit.test_download_options src.tests.unit.test_download_recovery src.tests.unit.test_collection_inventory src.tests.unit.test_premium_access
uv run --no-sync pyright
```

Reports are in the `/tmp` paths above; they are not committed runtime artifacts.
Profile fixtures record the corresponding live HTTP and GUI outcomes in
`docs/url-routing-audit/profile-fixtures.json`.

These are representative changing-catalog checks, not a complete catalog crawl.
English is the verified locale. No authentication, paid playback, protected-media
bypass, other host families or unused library features are claimed.
