# Advanced desktop download controls

Run the helper and choose **Advanced desktop download controls**, or run:

```bash
uv run python -m src.tests.smoke.download_advanced
```

The suite has 11 groups. It fetches actual PornHub, Eporner and XVideos videos
through their installed libraries, tests their metadata against the production
filter implementation, submits real URLs through the desktop GUI, checks an
inclusive video range, and downloads a real PornHub HLS video into a formatted
Unicode path. FFmpeg verifies that completed output is readable media.

The filter matrix reuses the unchanged metadata fetched at the start. It does
not manufacture provider responses or repeatedly fetch an author page for each
regex. The separate GUI submission and range checks use the real preparation
pipeline. An upstream request failure remains a failure, with details in the
report; it is not silently treated as a filter rejection.

## Coverage

| Group | Checks |
| --- | --- |
| Real metadata | Original titles, author, tags, duration, resolutions and dates from three actual provider libraries |
| Real regexes | Anchored literals, escaped punctuation, case differences, alternation and non-matches against real titles, authors and tags |
| Real numeric/date filters | Inclusive duration boundaries, minimum/maximum quality, same-day publication limits, and rejection outside bounds |
| Combined filters | All conditions must match; one failing regex rejects an otherwise matching real video |
| GUI submission | Actual Get Video actions accept/reject a real URL according to the entered regex |
| Video range | Start/End select original positions inclusively, before other filters; filenames retain those original indexes |
| Formatted download | Actual HLS transfer into nested folders containing Japanese/German text and sanitized punctuation |
| Validation | Malformed regexes, invalid dates, inverted limits and invalid templates produce a GUI error before starting a fetch |
| Unusual-title fixtures | 25 explicitly synthetic metadata cases, real GUI rows and real filesystem writes, without fake media |
| Templates | Every supported placeholder, `${...}`, literal `$$`, nested folders, explicit absolute paths and default naming |
| Dialogs | Title formatting Options and Keyboard shortcuts open their actual help dialogs |

The unusual-title cases include Japanese, Chinese, Korean, Cyrillic, Arabic,
accents, decomposed Unicode, emoji/ZWJ sequences, `/`, `\\`, `|`, quotes, angle
brackets, control characters, traversal-like strings, Windows reserved names,
leading tilde, dots, dollar signs and long multibyte titles. Synthetic groups
are explicitly labelled in the report. They substitute metadata only; their
filesystem writes are identified as test files, never validated as downloaded
video. Ordinary unit tests also exercise path sanitation, long-name collisions,
extensions and the original-title adapter contract.

## Defined behavior

- Regexes use Python `re` with `IGNORECASE`. Tag matching succeeds when any one
  tag matches. Regex matching uses original metadata, before filename sanitation.
- All enabled filters combine with AND. Missing duration/date/tags/qualities
  fail a filter that requires that field.
- Duration values are the app's normalized, rounded minutes. Quality range
  filters the highest available resolution; it does not choose the download
  resolution. `4k` means 2160 vertical pixels. Premium download limits still apply.
- Publication limits include the entire selected calendar day.
- Start/End are inclusive positions beginning at 1. Start 0 means the first
  video, End 0 means no end limit. Positions are applied before filters; the
  settings result limit caps candidates examined within that range.
- Original titles/authors remain unchanged in metadata and render as plain text.
  Filename components preserve Unicode with NFC normalization and replace unsafe
  characters with `_`. Metadata separators cannot create directories. Only
  separators written into the template can do so.
- Windows reserved names are prefixed, empty components get a fallback, and long
  UTF-8 components are shortened with a stable hash. A video titled `~` remains
  inside the output directory; a home path is expanded only if written explicitly
  in the template. Parent traversal is rejected.
- `$publish_date` produces `YYYY-MM-DD`; missing date/length values produce
  `unknown`. Unsupported placeholders and malformed template syntax are errors.
  Ordinary dots in titles no longer prevent adding `.mp4`.

Distinct titles can sanitize to the same basename, for example `A/B` and `A|B`.
Use `$index` or `$video_id` in the template to distinguish them. The tests verify
the indexed case; they do not claim universal automatic filename deduplication.

## Running and reports

GUI/development dependencies and FFmpeg are required for the full run. No
accounts, cookies, PocketBase or SpankBang requests are used. Settings, files,
logs and caches are confined to a temporary workspace, which is removed when
the run finishes. Existing user settings/downloads remain untouched.

```bash
# Inventory without starting Qt or making requests.
uv run python -m src.tests.smoke.download_advanced --list

# Explicit title fixtures, validation, templates and dialogs; HTTP is rejected.
uv run python -m src.tests.smoke.download_advanced --offline-only

# Allow more time per group on a slower connection.
uv run python -m src.tests.smoke.download_advanced --timeout 360
```

Default report: `/tmp/porn-fetch-download-advanced.json`; diagnostic details go
to the corresponding `.log`. Override with `--report PATH`. Reports distinguish
passed, failed, blocked and not-run groups, with individual filter cases and
synthetic versus actual-provider data identified. Dependent groups stop after
a failure. Rate-limit waits extend deadlines. CAPTCHA pages, unsupported
challenges and access denials stop the run. Recognized HTTP-200 PornHub math
responses pass unchanged to the existing native library handler; see
`LIVE_ACCOUNT_TESTS.md`.

The offline contract is included in ordinary integration-test discovery. Live
requests and downloads remain opt-in. These are desktop controls and filename
tests, not a claim of Android device coverage or testing every possible regex.
