# RedGIFs in Porn Fetch

The GUI and CLI use `unofficial-api-for-redgifs>=1.0.0` through the configured shared
network backend. RedGIFs GIFs are video clips served as MP4; use the existing Video
section. This integration does not convert clips into `.gif` files.

| RedGIFs resource | Porn Fetch section | Example |
| --- | --- | --- |
| Video/GIF watch or embed link | Video | `https://www.redgifs.com/watch/hotpinkacrobatickitfox` |
| User/creator | Model / Pornstar | `https://www.redgifs.com/users/nickiipeach` |
| Niche | Playlist / Collection | `https://www.redgifs.com/niches/duo-chastity` |
| Public collection | Playlist / Collection | `https://www.redgifs.com/users/weirdjack/collections/d7ddef5fb0` |

Bare/www `redgifs.com` page hosts and `media.redgifs.com` MP4 identity links are accepted.
A collection URL is resolved before its enclosing user path, so it does not fetch the
user's entire upload list. Collections with an optional display-name suffix resolve to
the same owner/folder identity. User `/videos` links resolve to the base user profile.
Directories, searches, image tabs, still-image URLs, account routes and unverified hosts
are rejected. Keyword search remains unavailable in Porn Fetch.

User and niche streams select their video tab. Public collections may contain still
images; those records are excluded before the existing video preview/processing limits.
There is no image-gallery workflow or separate GIF tab in this integration.

## CLI examples

```sh
python Porn_Fetch_CLI.py --url https://www.redgifs.com/watch/hotpinkacrobatickitfox --quality 480
python Porn_Fetch_CLI.py --model https://www.redgifs.com/users/nickiipeach
python Porn_Fetch_CLI.py --playlist https://www.redgifs.com/niches/duo-chastity
python Porn_Fetch_CLI.py --collection https://www.redgifs.com/users/weirdjack/collections/d7ddef5fb0
```

The interactive profile workflow also accepts a username after selecting `redgifs`.
Existing free/premium quality, bulk-preview, queue and concurrency rules apply. In free
use, public profile/niche/collection preparation retains the existing five-video preview.

## Metadata and quality selection

Both preparation adapters load API metadata and HTML display titles. The API supplies
publication date, duration seconds, uploader, tags and thumbnails; duration is normalized
to the application's rounded minutes. No author-profile request is needed per video.
The provider's source-aware fields remain unchanged for inspection/export.

RedGIFs supplies rendition names (`sd`/`hd`) rather than guaranteed numeric resolutions.
`src/shared/redgifs.py` reads bounded MP4 metadata ranges through the supplied core and
maps actual pixel dimensions to the app's numeric quality choices. Portrait resolution
uses the shorter dimension: 480×854 becomes 480p, and 1080×1920 becomes 1080p. A legacy
1280×640 clip is 640p, regardless of its HD marketing label. No fixed 720p SD assumption
is used. Measurements use the shared bounded TTL response cache and are cleared with
settings/session cache refresh. Unreadable dimensions raise an error rather than silently
selecting an unverified rendition.

The dispatcher translates the chosen numeric resolution back to the exact rendition
label and uses `DownloadConfigRAW`. The CLI measures the real choices even when a caller
omits its prepared quality list; a video with no permitted rendition fails instead of
falling back above the free limit. Silent renditions are not an additional UI quality.
The usual progress, cooperative stop, byte checkpoints, resume, skip-existing, filenames,
metadata-writing and mobile export paths remain in use. HLS playlists are not sent to
the HLS downloader, and authorization headers remain scoped to API requests.

## Validation on 2026-11-10

Tests used real requests with the current connection. The final CLI integration and
lifecycle runs used the published 1.0.0 wheel, whose API implementation matched the
local reference used for desktop checks. Ordinary request/backoff settings were used;
no account cookies or user license/history/download state were used for tests.

Complete app streams were compared page by page to the intended live JSON video IDs:

| Source | Expected / actual video IDs | Other records |
| --- | --- | --- |
| User `nickiipeach` | 17 / 17 | Video tab selected |
| Niche `duo-chastity` | 5 / 5 | Video filter selected |
| Collection `weirdjack/d7ddef5fb0` | 244 / 244 | Two still images intentionally excluded from 246 public items |

Six complete CLI downloads covered both measured renditions on a portrait and a legacy
landscape sample, plus free `best` selection on each. ffprobe verified dimensions,
duration, file size and audio:

| Sample | Selected tiers | Actual output |
| --- | --- | --- |
| `hotpinkacrobatickitfox` | 480p / 1080p; free best = 480p | 480×854 / 1080×1920; 6.467 seconds |
| `happyfrenchindianspinyloach` | 320p / 640p; free best = 640p | 640×320 / 1280×640; 15 seconds |

Real Qt list preparation added two native rows from each User, Niche and Collection
flow with correct origins, titles and numeric qualities. The existing desktop QML test
selected 480p with keyboard input, stopped a real transfer, resumed retained bytes,
validated the finished MP4 with FFmpeg and verified completed-row removal. The CLI
lifecycle test also passed 480p pause/resume with retained bytes and readable media.
Small header probes are retained in the request evidence but are separated from RAW
output bytes in the passive test observer; resume-range/prefix assertions remain intact.
The focused regression run passed 57 tests, and type checking passed for the shared
RedGIFs adapter, provider routing and CLI client pool.

Repeat the opt-in live checks (network and ffprobe/FFmpeg required):

```sh
.venv/bin/python -m src.tests.smoke.redgifs --report /tmp/redgifs-integration.json
.venv/bin/python -m src.tests.smoke.download_lifecycle --provider redgifs --scenario pause-resume --quality 480 --report /tmp/redgifs-cli-resume.json
QT_QPA_PLATFORM=offscreen QT_QUICK_BACKEND=software .venv/bin/python -m src.tests.smoke.download_gui --provider redgifs --scenario pause-resume --quality 480 --report /tmp/redgifs-gui-download.json
```

These checks are opt-in and do not run during normal unit-test discovery. They download
to temporary folders and record reports without signed CDN queries or session tokens.
The existing library's unstable ordering for equal-timestamp uploads and possible stale
public counters remain upstream limitations. HTTP 429 remains a real failure handled by
the configured backend retries, not an empty successful list.

Android and iOS dependency/staging inputs include the provider. Native mobile builds
and device playback were not rerun for this integration. Desktop/CLI functionality does
not establish that those native packages have been built or deployed.
