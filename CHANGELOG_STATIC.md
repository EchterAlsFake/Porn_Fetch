# Porn Fetch 3.9 beta

These notes cover the current 3.9 development tree and changes since 3.8, updated through 28 October 2026. This remains a beta: implemented features, automated checks and verified platform builds are distinguished below.

The checkout remains a free sandbox simulation for this beta. These application changes do not enable real payments.

### Supported websites and URL handling

- Added RedTube, Thumbzilla and Tube8 video and profile integration.
- Added EMPFlix and TNAFlix video downloads, metadata and the profile/channel routes each provider exposes.
- The video-provider inventory now covers PornHub, XHamster, XNXX, XVideos, Eporner, SpankBang, YouPorn, Beeg, RedTube, Thumbzilla, Tube8, XFreeHD, Porntrex, EMPFlix and TNAFlix.
- Expanded model, pornstar, creator, user and channel URL handling according to each provider's actual capabilities.
- Added public playlist/collection routing for PornHub, XVideos, YouPorn and RedTube. Thumbzilla has a playlist route and parser, but live playlist verification still needs a usable public fixture.
- Added gallery handling for supported album links in the CLI, including XFreeHD and PornHub.
- Unified provider hostname and content-type routing between the GUI and CLI. Unsupported directories, resource types and tabs produce an actionable error instead of entering the wrong parser.
- Improved handling of localized video paths, profile aliases, explicit video tabs and supported mirror hosts. Relative listing links retain their provider origin.
- Preserve case-sensitive video IDs and distinguish the requested source URL from its redirected transport URL.
- Preserve pagination filters and replace existing page parameters instead of appending conflicting page numbers or nesting resource prefixes.
- Resolve profile identity before reading an AJAX video tab. Follow supported XVideos profile-to-channel redirects and XHamster user-to-creator links.
- Honor PornHub's uploaded/featured source selection when preparing a model or user list.
- Replaced the app's separately maintained Supported Websites page with a browser link to [pornfetch.to/#websites](https://pornfetch.to/#websites).

### Downloads, selection and queue controls

- Rebuilt the desktop download list around per-video quality, selection, status, progress, start, stop, resume and removal controls.
- Added automatic removal of completed desktop downloads from the visible list while retaining their history when tracking is enabled.
- Added manual removal of pending, queued and active entries. Active writers stop before their row is removed, and removing one job does not stop unrelated downloads.
- Fixed visible row numbering so entries no longer all display `1`. Numbers update when entries are removed or completed.
- Fixed column spacing so Stop / Resume and Progress do not overlap regardless of the available window width.
- Made selection, Download Selected and per-row actions use stable job identities as rows are inserted, removed and automatically cleared.
- Improved HLS stop/resume so retained segments and checkpoint progress are reused rather than requested again unnecessarily.
- Fixed RAW resume starting at byte zero after a partial download. The shared downloader now persists checkpoints and resumes with byte ranges when the server supports them.
- Direct-file downloads can use concurrent parts when supported by the server, with configurable bandwidth limits.
- Simplified the option label to **Cleanup on stop** and added adjacent help explaining that deleting partial segments and temporary files prevents later resumption from that progress.
- With cleanup disabled, stopping retains reusable partial data. With cleanup enabled, a later start performs a fresh transfer.
- Completion releases temporary segment/checkpoint data. Fixed cases where finished HLS downloads could retain substantial temporary data in memory.
- Treat native failed-download reports as failures that can be retried, rather than displaying a false successful completion.
- Cancel queued semaphore waits immediately, including jobs stopped before their coroutine first starts. Apply changed parallel limits when idle, deferring changes while active tasks drain.
- Improved HLS joining, progress reporting and handling of streams with unusual timestamps.
- Support YouPorn's direct-file fallback when an HLS stream is unavailable; tests record the transport actually selected.
- Corrected the displayed duration unit: prepared durations are normalized to minutes and displayed without converting them a second time.
- Added the missing 144p filter choice and retained per-video quality selection. The 4K filter corresponds to 2160p.
- Preserve quality entitlement checks in single and selected downloads; higher-quality and parallel-download features require an eligible license.

### Filters and custom output filenames

- Added title, author and tag regular expressions, minimum/maximum duration and quality, publication-date bounds, result limits and start/end source positions.
- Make Start/End inclusive original source positions, applied before filtering. Filenames retain those source indexes even when the visible list is renumbered.
- Apply combined filters together, with case-insensitive regular expressions. Tag expressions can match an individual tag.
- Treat publication-date limits as inclusive calendar dates.
- Validate invalid regexes, dates, reversed ranges and malformed filename templates before starting network preparation.
- Preserve original desktop list titles and author names for display and filtering. Sanitize metadata only when constructing filesystem paths.
- Handle foreign alphabets, emoji, combining Unicode, `/`, `\\`, `|`, reserved Windows filenames, trailing dots/spaces, control characters and very long filenames more safely.
- Prevent title/author metadata from introducing directories or escaping the intended filename component. Directory separators deliberately written in a custom template remain supported.
- Keep a video titled `~` from being interpreted as a request to use the home directory.
- Add the expected media extension when a title contains dots that are not a recognized video extension.
- Implemented the **Options** dialog for custom title formatting, documenting `$title`, `$author`, `$video_id`, `$index`, `$publish_date`, `$length`, `$output_path`, `${name}` syntax and `$$` for a literal dollar sign.
- Connected the keyboard-shortcuts dialog.

### Account login and account collections

- Added XHamster and XVideos account integration alongside PornHub, using the authentication methods each site exposes.
- Reorganized PornHub login so email/password and a full-width Login button come first, followed by one row of history, recommendation, subscription-feed and favorite actions. Username and browser-cookie import are grouped separately below.
- Replaced permanent login-page instructions with a **How to login** dialog explaining the site-specific flow, cookies and browser extraction.
- Import actual browser sessions through `browser_cookie3`; desktop testing includes Brave. Browser-cookie import is not offered as an Android OS feature.
- Verify imported sessions against the server's authenticated state. Cookie presence or constructing an Account object alone no longer establishes a successful login.
- Use PornHub's authenticated account menu to determine the username where needed.
- Fetch PornHub watch history, recommendations, subscription feed and favorites; XHamster liked videos/account playlists; and XVideos watch later, history and liked videos.
- Support XVideos session-token login. XVideos password/CAPTCHA login is not added by this release.
- Fixed XHamster liked-list extraction from embedded account JSON instead of accidentally reading recommendation thumbnails.
- Handle expired/rejected authentication, invalid collections, duplicate actions and cancellation without leaving the account page stuck in a loading state.
- Treat a missing later account-list page as the end of pagination while keeping first-page, authentication and video-metadata failures visible.
- Keep account secrets out of saved download-recovery snapshots and diagnostic result summaries.

### Desktop interface and settings

- Rebuilt the desktop interface in QML, covering downloads, accounts, settings, statistics, licensing and information.
- Added Material appearance, accent colors, dark mode and activity glow, with live updates where supported.
- Align switch controls to the left of their settings control column instead of centering them in the available space.
- Added attributed icons beside the Video, Performance, System, Privacy and UI settings categories.
- Made Tor routing labels and help more prominent.
- Fixed overlapping cards in the information/credits layout and improved resizing behavior.
- Added scrollable dialogs for longer help and notices, including title-formatting guidance and third-party notices.
- Apply logging, preparation delay, cache, retry, network, provider and idle download-concurrency settings to their actual runtime consumers.
- Persist settings to disk and reload them consistently. Language and Material appearance changes update the live QML interface; settings that need a restart still explain that requirement.
- Added a first-run beta disclaimer with a 30-second reading period in desktop, Android and CLI flows.
- Added an explicit first-run choice for optional error reporting, with privacy-sensitive details redacted from reports.
- Improved anonymous mode so sensitive video details and widgets are hidden when enabled.

### Download history and statistics

- Rebuilt desktop tracking with a local PocketBase service and added a statistics dashboard. The CLI can discover or install PocketBase; legacy SQLite records can be imported.
- Track prepared videos, completion, stopped/failed transfers, retries and their originating profile or playlist.
- Update an existing history entry when a job resumes or retries instead of creating duplicate completion records.
- Preserve the source name and URL so statistics can group downloads by model, channel or collection.
- Make Statistics Refresh reload the database cache asynchronously instead of only repainting old values.
- Keep history after a video is removed from the download list, and retain it across normal application restarts.
- Honor disabled tracking and anonymous presentation. Android does not start a download-history database.
- Share database signal wiring between normal startup and diagnostic workflows so initialization failures and busy state are handled consistently.
- Fixed generated PocketBase passwords beginning with `-` being parsed as command-line options.

### Desktop shutdown and paused-job recovery

- Added coordinated teardown for normal window closing: stop active downloads cooperatively, cancel queued work, save the queue, flush history and close provider sessions and PocketBase.
- Restore unfinished desktop rows as **paused** after reopening. Transfers resume only when the user explicitly clicks Resume.
- Restore job identity, output paths, chosen quality and retained progress without making provider requests during startup.
- Obtain a fresh native provider object when Resume is clicked, rather than serializing live sessions or provider objects.
- Discard incompatible HLS state if the selected or permitted quality has changed.
- Store queue snapshots and native HLS state in a writable application cache directory instead of depending on the current working directory.
- Write recovery metadata atomically and exclude cookies, passwords and native objects from it.
- Flush pending history before moving its database directory during shutdown.
- These changes concern normal close/reopen behavior; forced-kill and power-loss recovery are outside the implemented test scope.

### Networking and privacy

- Moved the provider network layer to asynchronous `curl-cffi` through `eaf_base_api`, with browser impersonation, HTTP-version selection, retries, caching and shared proxy handling.
- Added HTTP, HTTPS and SOCKS proxy configuration with a desktop connection test.
- Added configurable DNS over HTTPS, primary/fallback resolvers, Encrypted Client Hello, network-interface binding and browser-style TLS fingerprints. Optional desktop SNI obfuscation modes remain available.
- Apply provider-session changes without requiring a restart, then close replaced sessions and their background tasks.
- Honor the configured fallback DNS-over-HTTPS resolver after primary-resolution failure.
- Added managed Tor routing choices: Off, updates/licensing only, or all app traffic including provider requests and media downloads.
- Start an app-owned Tor client on demand, show bootstrap progress, and stop routed requests on failure rather than falling back to a direct connection.
- In all-traffic mode, use remote SOCKS hostname resolution, keep PocketBase loopback requests local, and prevent custom proxies, interface settings, environment bypasses or QUIC from silently changing the selected route.
- Require acknowledgment before routing bandwidth-heavy video downloads through Tor. External browser links and other applications are outside Porn Fetch's route.
- Added clearer service-failure notices distinguishing Tor startup problems, an unreachable service and temporary server errors, with repeated notifications grouped.
- Refreshed dependencies and the lockfile, including the shared downloader fixes now present in published releases.

### Automatic updates

#### Desktop GUI

- Added automatic update handoff for installations managed by Qt Installer Framework. The old macOS Sparkle updater has been removed.
- Check signed release metadata and download/hash-verify the repository metadata and payloads into local staging before launching the Qt Maintenance Tool.
- Reject external payload substitutions and do not offer automatic installation from unauthenticated fallback update information.
- Close PocketBase and provider sessions before the updater handoff to reduce locked-file failures, particularly on Windows.
- Display the current release notes as Markdown in the update dialog, verifying the downloaded notes against the signed release metadata.
- Check update eligibility against the release timestamp. Portable/source installations retain their appropriate manual update method.

#### Standalone CLI

- Added `self-update --check`, interactive `self-update`, and `self-update --yes` for supported standalone binaries.
- Verify signed updates through The Update Framework (TUF), then replace the executable and bundled PocketBase with a separate update helper.
- Keep previous files and a staging result for recovery and diagnosis if installation fails.
- Fixed standalone certificate-bundle discovery and added visible update download progress.
- Leave source checkouts and package-manager installations to their original update method.

#### Android

- Added a separate signed Android TUF feed with APK architecture, package, version, release timestamp and hash metadata.
- Verify the downloaded APK, update entitlement and signing identity before handing it to Android's installer through a read-only content URI.
- Let Android request installation permission and final confirmation; updates are not installed silently.
- Preserve the installed application if an update is cancelled or verification/download fails.
- Android update and installation flows still require validation on real devices and built APKs.

### CLI workflows

- Rebuilt the terminal app around separate flows for videos, profiles/playlists, account access, settings, licensing, tracked sources, history and statistics.
- Keep CLI and shared services free of Qt dependencies so they can run on headless systems, including Termux.
- Accept multiple supported source URLs in batch mode, with quality/output overrides and optional continuation past failed entries.
- Track model/profile pages, scan for new videos and manage a pending download queue.
- Added pause, resume and cancel controls, including saved paused jobs that can continue in a later CLI session.
- Improved progress display, optional MP4 metadata writing, unavailable-video reporting and normalization of provider quality APIs.
- Added explicit offline/provider/download diagnostics and a shared interactive test selector.

### Provider-library fixes used by Porn Fetch

These are the provider versions required by the current application manifest. The summaries cover changes used by Porn Fetch's own video, account, profile, collection, gallery or download paths.

#### [PornHub 5.4.6](https://github.com/EchterAlsFake/unofficial-api-for-pornhub/blob/master/CHANGELOG.md)

- Corrected regular-user upload routes and made profile listing extraction more resilient.
- Improved normalization of embedded and relative video links and extraction of localized profile statistics.
- Improved author handling for the video/short types consumed by the app, including channel authors.
- The live-test guard now lets recognized PornHub math challenges reach the existing native `eaf_base_api` handler. It previously stopped the response before that handler could run.
- Corrected pagination-test identities to retain PornHub's public `viewkey`; stripping every query parameter had made different videos appear identical.

#### [XHamster 2.6.5](https://github.com/EchterAlsFake/unofficial-api-for-xhamster/blob/main/CHANGELOG.md)

- Restored shorts/moments extraction from current page data and DOM layouts, preserving regional hosts and the correct profile listing route.
- Read hydrated listing metadata so later cards retain their thumbnails and durations.
- Improved Full HD/UHD recognition and handling of missing short metadata.
- Includes the earlier account-JSON extraction fix used for liked videos, and reports rejected credentials as a failed login.
- Updated the app's pagination test to allow a real overlapping page prefix while still requiring a new later-page video; a fully repeated page still fails.

#### [XNXX 2.4.4](https://github.com/EchterAlsFake/unofficial-api-for-xnxx/blob/master/CHANGELOG.md)

- Read video metadata from JSON-LD arrays and graph objects.
- Handle empty profiles without division-by-zero errors and close profile scrapers when iteration stops early.
- Preserve canonical video identity when listing click links contain a separate tracking token.

#### [XVideos 2.5.3](https://github.com/EchterAlsFake/unofficial-api-for-xvideos/blob/master/CHANGELOG.md)

- Return actual listing thumbnails and decoded titles, decode HTML entities in profile JSON, and exclude cards that are not videos.
- Handle empty channels and model/profile aliases more consistently.
- Expose uploader names from video-page metadata. Porn Fetch uses those names instead of making a separate author/statistics request for every prepared row, retaining the native lookup when the name is unavailable.
- Close the inner profile scraper when iteration ends early, preventing leftover prefetches from racing later requests.
- Support the author-helper calling conventions consumed by shared metadata preparation.

#### [Eporner 2.5.3](https://github.com/EchterAlsFake/unofficial-api-for-eporner/blob/master/CHANGELOG.md)

- Correct listing IDs, embed links, keywords, thumbnails and duration types.
- Select download qualities for the requested codec and handle absolute media URLs correctly.
- Tolerate additional JSON-LD shapes and optional metadata.
- Recognize localized video paths, German/French profile statistics and missing channels that incorrectly return HTTP 200.
- The app now reads Eporner's real quality method instead of requesting a nonexistent `video_qualities` dataclass field.

#### [SpankBang 2.4.4](https://github.com/EchterAlsFake/unofficial-api-for-spankbang/blob/master/CHANGELOG.md)

- Use more conservative listing concurrency and standard navigation headers.
- Improve regional profile paths/statistics and thumbnail, duration and stream-data parsing across page layouts.
- Retain earlier quality-detection improvements, including 4K stream identification.
- Desktop workflows remain marked manual until separately verified; a parser update alone does not establish working browser/CDN playback.

#### [YouPorn 1.8.3](https://github.com/EchterAlsFake/unofficial-api-for-youporn/blob/main/CHANGELOG.md)

- Handle empty listings, partial collections and users without public collections safely.
- Resolve absolute collection links without duplicating the provider hostname.
- Avoid loading unrelated title/name fields just to log helper operations used during metadata/collection handling.
- Correct duration normalization so minute values are not multiplied into incorrect validation expectations.
- Retain direct-MP4 fallback handling alongside HLS downloads.

#### [Beeg 1.7.4](https://github.com/EchterAlsFake/unofficial-api-for-beeg/blob/main/CHANGELOG.md)

- Preserve video keys in links copied from tag pages and retain significant trailing zeros.
- Expose author, tags, thumbnails and publication dates for consumers such as CLI metadata preparation.
- Return a useful unavailable-video error for missing/malformed API metadata instead of an indexing exception.

#### [RedTube 1.4.4](https://github.com/EchterAlsFake/unofficial-api-for-redtube/blob/main/CHANGELOG.md)

- Recognize playlist video containers as well as profile grids, rather than extracting zero videos from a populated playlist.
- Normalize supported profile routes and improve localized statistics and playlist counts.
- Return actual thumbnail URLs instead of lazy-loading placeholders or unprocessed `srcset` strings.
- Load optional uploader/performer data more safely and remove duplicate performer entries.

#### [Thumbzilla 1.4.3](https://github.com/EchterAlsFake/unofficial-api-for-thumbzilla/blob/main/CHANGELOG.md)

- Handle missing optional playlist metadata and short statistics layouts without crashing.
- Added parser regression coverage for playlist metadata; live playlist support remains unverified without a usable public fixture.

#### [Tube8 1.3.3](https://github.com/EchterAlsFake/unofficial-api-for-tube8/blob/main/CHANGELOG.md)

- Stop interpreting subscriber totals as video counts, including on French channel pages.
- Reject empty User pages instead of accepting generic session data as a valid profile identity.
- Keep public User-feed verification separate from working video, channel, pornstar and amateur routes.

#### [XFreeHD 1.7.4](https://github.com/EchterAlsFake/unofficial-api-for-xfreehd/blob/main/CHANGELOG.md)

- Normalize relative and embedded video/album links, return qualities consistently and accept numeric quality aliases.
- Tolerate optional ratings/duration metadata and expose private-video status without a metadata parser crash.
- Handle empty albums and invalid image-page numbers safely.
- The app reads the native quality method rather than a nonexistent lazy dataclass field.

#### [Porntrex 1.8.3](https://github.com/EchterAlsFake/unofficial-api-for-porntrex/blob/main/CHANGELOG.md)

- Recognize MP4 media URLs with signed query strings or fragments while preserving the tokens required to download them.
- Retain the corrected profile pagination and provider-origin handling used by model/channel preparation.

#### [EMPFlix 1.0.1](https://github.com/EchterAlsFake/unofficial-api-for-empflix/blob/main/CHANGELOG.md)

- Resolve short and embedded video links to a full watch page when metadata is missing.
- Return the appropriate profile/channel/pornstar identity for supported author links.
- Keep channel authors out of category/tag lists and parse abbreviated rating counts safely.
- Added parser fixtures for the supported page layouts.

#### [TNAFlix 1.0.1](https://github.com/EchterAlsFake/unofficial-api-for-tnaflix/blob/main/CHANGELOG.md)

- Follow canonical watch links when short/embed pages omit required video details.
- Normalize video/profile/channel/pornstar identities and support the author helpers used by metadata preparation.
- Keep channel authors out of tags/categories and tolerate missing source-size attributes and abbreviated rating counts.
- Added parser fixtures for the supported page layouts.

### Shared API/download engine

- Require [eaf_base_api 4.2.5](https://github.com/EchterAlsFake/eaf_base_api/blob/master/CHANGELOG.md), including resumable RAW downloader changes previously available only in the source checkout.
- Preserve resumable byte offsets/checkpoints and validate ranged responses instead of silently treating a restarted RAW transfer as resumed progress.
- Sanitize automatic download filenames and provide a safe fallback when no title is available.
- Fixed contextual logging failures for URLs containing percent escapes.
- Load metadata through explicit sources/fields, retaining clear errors for unresolved or unavailable values instead of relying on legacy `.load()` behavior.
- Keep request/download error context consistent across providers, with bounded retries and explicit unavailable-resource handling.
- Bound asynchronous page/item work, preserve original order where requested, and clean up unfinished scraper tasks.
- Keep the native PornHub math handler, retry budget and cooldown behavior in the shared library; the app's test guard does not implement a second solver.

### Test coverage and diagnostics

Added substantial offline and opt-in live coverage around the production GUI, CLI, provider libraries, filesystem and local database. Positive live paths use actual requests and media; protocol/error contracts and unusual-title fixtures are explicitly separate.

| Area | Implemented checks |
| --- | --- |
| Offline and Qt integration | URL routing, provider adapters, input validation, persistence, real QML bindings, settings consumers, error/cancellation recovery, update verification and application startup |
| Provider/profile metadata | All 15 video providers, supported shorts/galleries, and a 76-case profile URL/alias/localization inventory feeding actual GUI models |
| CLI download lifecycle | 30 pause/resume and cleanup/restart workflows across 15 providers, using the native HLS/RAW transport selected by each provider |
| Desktop download controls | 42 automated workflows across 14 providers: real controls, progress, quality, stop/resume, cleanup, removal and completion clearing; SpankBang is a separate manual exception |
| Queue/concurrency | Three multi-video workflows using real HLS/RAW transfers, limits 1/2, duplicate starts, queued cancellation and isolation when active jobs are stopped/removed |
| Desktop settings | Persistence checks for 55 settings, independent disk reads/reloads, active provider configuration and observable effects; optional Tor/Strict SNI effects require their own environment |
| Statistics/history | Eleven workflows covering actual PocketBase records, aggregates/source groups, retry/resume updates, privacy, refresh, restart persistence and disabled/error states |
| Advanced controls | Eleven groups using real video metadata, regex/range/date/quality filters, templates and a real formatted download, plus 25 explicit synthetic unusual-title fixtures |
| Normal teardown/recovery | Eight workflows in 16 independent GUI processes, covering preparation, pending database writes, database moves and retained/cleaned HLS/RAW transfers |
| Public model/playlist workflow | 16 automated source workflows from input through limits/filters/ranges, cancellation, native later-page rows, selected media and source history/statistics; SpankBang is manual and Thumbzilla playlists remain unverified |
| Account controls | Default 36-check desktop/mobile-QML action inventory, real browser-cookie sessions and account lists, list metadata, tokens, help, busy state, cancellation and errors; optional private-playlist verification and separate local password checks |

- Added `uv run src/tests/helper.py` selections for the live suites, with explicit network, media-download and browser-session confirmations as appropriate.
- Live download checks observe actual HTTP range/segment reuse and use FFmpeg to verify a readable output video stream and plausible duration. They do not substitute fake successful transfers.
- Isolate settings, outputs, queue snapshots and PocketBase data from personal application state. Save JSON reports, stages, library versions and diagnostic logs for follow-up.
- Keep live suites out of ordinary unit/integration discovery and CI. Ordinary integration tests include offline GUI contracts that reject network calls.
- Handle HTTP 429 with a minimum 30-second cooldown, longer `Retry-After` values when supplied, and at least five seconds between requests after rate limiting; retries of safe reads are bounded.
- Stop on explicit access denials, CAPTCHA pages and unsupported scripts. Let only recognized HTTP-200 PornHub math payloads on HTTPS PornHub hosts reach the existing native handler, recording delegations without cookies/tokens.
- Detect genuinely repeated pagination while permitting real overlapping entries at page boundaries. Retain public IDs such as PornHub `viewkey` in hashed video comparisons.
- Require actual authenticated server state for account success and explicit anonymous-denial evidence before claiming a private playlist is authorized correctly.
- Add line/branch reporting through `coverage`, including an HTML report when requested. Workflow/checklist counts are not a claim of 100% Python line or branch coverage.
- Treat failed, blocked, skipped, manual and unverified cases as distinct outcomes. External website changes, unavailable fixtures and expired sessions remain visible instead of being counted as passes.
- The focused PornHub model and playlist rerun passed after the guard/identity corrections; the latest integration run completed 165 tests with one existing skip. These are verification snapshots, not a blanket all-platform or all-suite success claim.

### Android, packaging and release workflows

- Replaced the old Kotlin Android app with an experimental QML layout featuring phone/tablet navigation, download cards, safe-area/layout work and file export through Android's picker.
- Added GitHub Actions APK jobs for arm64-v8a, armeabi-v7a, x86_64 and x86. Android-only workflow selection is available alongside desktop GUI, CLI and combined builds.
- Updated the Android build path for Python 3.14 and matching PySide6/Shiboken wheels, with checksum verification before deployment patches.
- Fixed native dependency recipes, target-ABI cryptography builds, Android command-line-tool discovery and clean-build registration of the Qt activity JARs.
- Preserve maintained native recipes outside deployment cleanup, and keep build failures visible through shell pipelines and per-ABI diagnostic artifacts.
- Added APK signing with a persistent signing identity, signature verification and checksum sidecars. Publishing requires signed APKs; unsigned build artifacts are explicitly diagnostic.
- Added website release publication and the signed Android update feed, including publication-only retries from existing successful build artifacts without recompiling them.
- Stamp one release version and original workflow timestamp into the binaries, update metadata and release assets; workflow reruns retain that timestamp.
- Allow separate GUI/CLI builds, and include only successful target artifacts in signed update repositories.
- Add offline CI gates, compiled GUI/CLI smoke checks, platform bundle checks, and post-upload signature/hash/download verification before release publication.
- Improved macOS runtime/plugin packaging and Intel/ARM64 bundle checks, and fixed installer archive handling for paths containing spaces.
- Package PocketBase, optional installer components, third-party notices and managed Tor runtimes where supported. Keep Android/device and platform-specific runtime verification separate from workflow lint.
- Refresh signed update metadata between releases and support retrying website publication using retained artifacts.
- The current source uses the Porn Fetch Source-Available License 1.0. Provider/shared API libraries use AGPL; the existing GPL 3.8 release retains its original license.
- Moved application service, update and website links to `pornfetch.to`.

### Removals and remaining limits

- Removed in-app keyword search, thumbnail display and the Eporner tools screen. Upstream library capabilities do not automatically become app features.
- Removed HQPorner, MissAV and Porngo from the application's supported-site list, and removed the kill-switch feature.
- Removed the old macOS Sparkle update path and the former Kotlin Android application.
- Linux s390x/ppc64le and Windows x86 builds remain paused where required networking binaries are unavailable or fail their build/runtime checks. Experimental targets are published only after their own checks succeed.
- SpankBang desktop workflows remain manual; Thumbzilla public playlists need a fixture; a working Tube8 public User feed is not claimed from generic profile/session markup.
- Recent live diagnostics still require follow-up for the XFreeHD desktop RAW-resume reuse assertion and a Tube8 User fixture. XVideos cookie checks depend on a currently authenticated browser session. These outstanding checks are not described as fixed by the other API updates.
- Tor/Strict SNI live effects, Android device behavior and packaged CLI/GUI installation/update behavior need their respective environment/build verification. Desktop-rendered mobile QML checks do not establish Android OS/device coverage.
- Licensing lifecycle retesting and forced-kill/power-loss recovery were not added to the new live matrix. Android device testing remains deferred while that platform is experimental.
