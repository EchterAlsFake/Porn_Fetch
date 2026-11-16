# Manual verification report: v3.9.1 to current development

Assessment date: 2026-11-16. Reviewed HEAD: `85b6723274232f30b6c9130273abe3d194ad86a6`.
This is a source assessment and manual test plan requested for this change set.
Unchecked boxes are proposed checks, not executed results or a release-readiness declaration.

## Scope and assessment

`v3.9.1` points to `f5d2148`, a hotfix branch off `010b0a2` (`v3.9.0`). It is
**not an ancestor of current master**. Consequently:

- `git log v3.9.1..HEAD` contains **16 commits** unique to the development branch,
  including provider integrations authored before the hotfix was tagged.
- **Eight** of those commits have dates after the v3.9.1 tag's commit date,
  2026-11-12 16:38:51 +01:00. They are marked **After tag** below.
- The hotfix itself changed only the PornHub API requirement in three dependency
  inputs. It did not contain the later Jellyfin, Creators or update-channel work.
- There is substantial **uncommitted/untracked work** on top of HEAD, including
  TV/Automotive controls, the offline website catalog, publication fixes and native
  packaging fixes. A build from committed HEAD alone does not contain that work.
  The final section explicitly separates its checks.

The review used commit diffs, final implementation, dependency inputs, build
workflows, test inventories and existing guides. It did not newly run provider
requests, account login, Jellyfin requests, actual updates, installers or licensing
lifecycle tests. Earlier test evidence in the repository/session is useful, but
is not a pass for the exact candidate APK/installer you will test.

The greatest risks are at feature boundaries, rather than the presence of a new
button: shared download state, repeated discovery, free/Premium gates, data
migration, signed release identity and native Android bridges. The broad provider
API major-version upgrades in `2c247b2` make the existing providers regression
subjects too. A successful source preview cannot establish that its installer
contains the necessary Python packages, native libraries or runtime resources.

### Findings established by source/history inspection

1. **Historical broken intermediate provider commit.** `1d66a40` calls lazy imports
   from `src.shared.porn` and `src.shared.youjizz`, but those modules are absent
   from that commit's tree. `7fb263b` adds them. This is repaired at HEAD; do not
   cherry-pick or build the earlier integration without its adapter commit.
2. **Release-note attribution needs review.** `CHANGELOG_STATIC.md` is headed
   `3.9.1 (hotfix)` but describes features added after the actual v3.9.1 tag.
   The README download link still targets v3.9.1. Test the candidate build's own
   version and contents, not an assumption based on that heading/link.
3. **Development version values require CI stamping.** The source defaults include
   `BUILD_VERSION = "3.9.0"`. That is not evidence that CI's final release identity
   is wrong; it makes checking stamping in every published artifact essential.
4. **Provider documentation is inconsistent.** The current router has 21 providers;
   `docs/WEBSITES.md` has 20 table rows and omits RedGIFs. Links to `BELLESA.md`,
   `REDGIFS.md`, `PORN.md` and `YOUJIZZ.md` reference absent files. Some verification
   material was consolidated into `docs/TESTING.md`, but the remaining links need
   correction. These are documentation findings, not live download failures.
5. **Known support boundaries remain.** Mobile GUI library-sidecar export is not
   implemented; iOS Creators is unavailable; Android history/statistics remain
   disabled. There is no new periodic/closed-app download scheduler. Android 9
   still needs a working folder picker. The uncommitted Automotive implementation
   does not implement native OEM `FocusParkingView`/`FocusArea` integration.

No new functional failure is asserted solely because a live or native check is
pending. Conversely, an existing offline test, provider 403, skipped fixture or
native-helper probe must not be reported as a successful full application test.

## Commit-by-commit assessment

Checklist IDs below identify the corresponding manual targets. Assess the final
candidate, with historical observations retained to explain dependencies.

| Commit/date | Relation to tag date | What actually changed and assessment | Manual targets |
| --- | --- | --- | --- |
| `f5d2148`, Nov 12 | Baseline tag, separate branch | PornHub API minimum raised to 5.4.7 in desktop, Android and iOS inputs for the 410 hotfix. This is the baseline, not a large feature release. | CORE-05; PKG-01 |
| `2a9c7ae`, Nov 9 | Earlier development | README/release presentation, feature/privacy copy and archived changelog updates. No new runtime subsystem. README begins referencing artwork added by the next commit. | DOC-01–03 |
| `1c879d0`, Nov 9 | Earlier development | Adds showcase artwork and its generation prompt. Visual/documentation change. Check that the shipped/repository README reference resolves. | DOC-01 |
| `b9a4591`, Nov 9 | Earlier development | Progress-image query label changes to version 4.0. No application version change. | DOC-01–02 |
| `bc08e00`, Nov 9 | Earlier development | Porndoe MP4 video/profile support and shared GUI/CLI routing; also meaningful Android setup D-pad/folder handling, packaging/recipe changes and removal of Weblate deployment files. Treat Android changes separately from the provider title. | SITE-01; CORE; AND-01–05; UI-01; PKG-03 |
| `38f5708`, Nov 9 | Earlier development | Pornhat videos, models/channels, accepted language/alias hosts and HLS dispatch. Updates all packaging inputs and explicit iOS wheel staging. | SITE-02; CORE; PKG-04 |
| `445d991`, Nov 10 | Earlier development | Bellesa and RedGIFs adapters; RedGIFs rendition measurement and image filtering; Android MediaStore helper and TV launcher/banner; native Python, cryptography and curl recipes for target ABIs. High packaging/storage impact. | SITE-03–04; AND-01–07; PKG-03–04 |
| `1d66a40`, Nov 11 | Earlier development | Porn.com and YouJizz routing, metadata, quality and download integration. Missing shared adapters are added later by `7fb263b`. Deletes standalone provider guides while some links remain. | SITE-05–06; DOC-03 |
| `14d41d3`, Nov 12 | Earlier than tag by minutes | Raises master-side PornHub requirement to 5.4.7 in the same three inputs as the separate hotfix. Later requirements supersede it. | CORE-05; PKG-01 |
| `520dc3f`, Nov 12 | **After tag** | Reorganizes release notes around the PornHub hotfix. Later commits append broader changes under that heading. No runtime behavior by itself. | DOC-02 |
| `a06a661`, Nov 12 | **After tag** | README download button targets v3.9.1. No runtime code. | DOC-01–02 |
| `7fb263b`, Nov 14 | **After tag** | Adds Porn.com page-type resolution/referral filtering and YouJizz validated pornstar/collection/quality adapters, plus live smoke runners. Completes the earlier provider integration. | SITE-05–06; SITE-08 |
| `572cf4b`, Nov 14 | **After tag** | Premium library export, normalized portable metadata, NFO/JSON/artwork, metadata-only preview/repair/retry, optional Jellyfin notifications, desktop UI and CLI flags. Touches ordinary completion/finalization and provider metadata requirements. High file-preservation risk. | META; CORE-01–04; PRIV-01–03 |
| `9fd3500`, Nov 14 | **After tag** | Android history/Back/edge gestures and input policy; native installer permission-return and shared FileObserver fix; update-size/progress presentation; PornHub HLS/MP4 recovery adapter; automatic Android signing and SDK/build-tool handling. | AND; CORE-05–07; UPD-07–12; PKG-03 |
| `41bcd40`, Nov 15 | **After tag** | Adds `uv.lock` to `.gitignore`; the diff itself does not remove a tracked lockfile or change runtime code. Builds resolve fresh dependencies, so test the exact built dependency set. | PKG-01; OPS-01; SITE matrix |
| `2c247b2`, Nov 16 | **After tag** | CLI prompt/terminal redesign; Creators persistence, scans, preview gates, queue integration and recovery; embedded Android PocketBase; broad provider major-version updates and unified pagination audit/runners. Tests cover much, but package/native integration remains substantial. | CLI; CR; SITE matrix; AND-08–10; PKG-03–04 |
| `85b6723`, Nov 16 | **After tag** | Stable/Beta settings, numeric selection, independently signed feeds/caches, pinned offers, UI/CLI controls, build/publisher channel propagation and legacy feed renewal. Removes unsigned informational fallback from normal desktop discovery. Requires deployed matching server/feed paths. | UPD; OPS; PKG-01–02 |

Useful evidence: [provider routing](../src/shared/provider_routing.py),
[PornHub recovery](../src/shared/pornhub_download.py),
[library export](../src/shared/library_export.py),
[Jellyfin transport](../src/shared/jellyfin.py),
[creator discovery](../src/shared/creator_scans.py),
[creator dispatcher](../src/backend/creator_bridge.py),
[channel policy](../src/shared/update_channels.py),
[Android update verification](../src/shared/android_updates.py), and the
[release guide](RELEASING.md).

## Test setup and order

Use disposable download/library directories and a test profile or OS account.
Keep the normal installation's settings and files intact. Use an existing Premium
test profile and a separate free profile; this plan does not ask you to repeat
payment/activation/renewal lifecycle testing already considered complete.
Forced-kill and power-loss recovery are outside this plan; close normally when
checking restart recovery.

Record for each run: candidate commit and whether local changes are included,
version/channel, installation type, OS/architecture, dependency/build identity,
test ID, actual result, and a short log/screenshot on failure. Mark unavailable
fixtures **Blocked** and unsupported targets **N/A**, with a reason. Only tick a
box when its expected outcome is observed on the named target.

Prepare:

- The signed installer/APK/CLI archive actually intended for distribution, plus an
  old v3.9.1 test installation for upgrade checks. Do not substitute a source run.
- One accessible short HLS video, one accessible MP4/RAW video, a small profile,
  a multi-page collection, and a collection with unavailable/referral/image entries.
- Free and Premium test contexts, a test Jellyfin Movies library if that integration
  is being checked, and a test output destination on Android.
- For controlled-only cases: signed Stable/Beta test feeds, a provider/CDN failure
  fixture, and a creator source whose listing you can change. These scenarios
  cannot reliably be forced by repeatedly clicking a random public video.

Run P0 first: package startup/upgrade, one HLS and RAW transfer, normal restart
recovery, Creators baseline/rescan, sidecar preservation, channel selection and
Android update permission return. Then run the provider matrix and P1 presentation
checks. On one desktop, cover the provider matrix in GUI and CLI. On other OSes,
repeat representative HLS, RAW, collection, persistence and installer checks;
repeat a provider-specific case there if behavior differs.

### Platform coverage

| Target | Minimum manual coverage |
| --- | --- |
| Windows, macOS, Linux GUI | Exact shipped installer on a clean test account; upgrade; HLS/RAW; Creators; library export; update handoff; native rendering. Test each shipped architecture's startup. |
| Frozen CLI on shipped OS/architectures | Launch outside checkout; interactive and batch flows; plain/non-TTY modes; transfer/resume; self-update. Include experimental architectures only when actually shipped. |
| Android ARM64 and every other shipped ABI | Install/start, complete setup, HLS/RAW export, Creators runtime/restart and same-key update. Emulator startup on x86 does not establish ARM runtime behavior. |
| Android phone/tablet | Touch, keyboard, Back, rotation, SAF/MediaStore, native installer. |
| Android TV / AAOS | Committed setup/navigation/storage checks apply; the extended controls in WIP apply only to a build including those local changes. |
| iOS ARM64 IPA | Real sideloaded startup, new-provider imports, download/save, and update-catalog handoff. Creators and GUI library export remain unavailable. |

## P0: package, identity and upgrade checks

- [ ] **PKG-01 — Target: every final installer, CLI build, APK and IPA being shipped.**
  **Test:** Check version/channel in the UI or CLI and artifact metadata against the selected build and commit.
  **Expected:** The candidate's stamped identity agrees everywhere; it does not accidentally ship development `3.9.0` identity or a different channel.
- [ ] **PKG-02 — Target: v3.9.1 desktop test installation upgraded to the candidate.**
  **Test:** Save non-default settings, a usable destination and a paused desktop download; install/update normally.
  **Expected:** Settings, completed setup, entitlement state, files and supported existing recovery data survive. No silent downgrade or repeated first-use flow.
- [ ] **PKG-03 — Target: Android APKs for each shipped ABI.**
  **Test:** Install the final APK, open it from the launcher, finish setup and open Creators.
  **Expected:** No missing `jwt`, Qt/SVG, curl/cryptography or PocketBase native-library import/loading failure. Images render and the app stays running.
- [ ] **PKG-04 — Target: final iOS IPA on a device.**
  **Test:** Sideload, open from the Home screen, then prepare one new-provider video and save it through the supported iOS flow.
  **Expected:** Startup and imports work in the actual bundle; the existing download/save flow works. Creators shows its unavailable state rather than crashing.
- [ ] **PKG-05 — Target: installed desktop optional components.**
  **Test:** Open Creators without PocketBase, then install/repair it through the supported component flow and choose Check again.
  **Expected:** A persistent, actionable dependency error appears before adding a URL; successful repair enables Add without corrupting ordinary downloads.
- [ ] **PKG-06 — Target: packaged GUI/CLI launched outside the repository.**
  **Test:** Launch by desktop icon/Explorer/Finder and run the CLI from another directory, including a path with spaces.
  **Expected:** Resources, trust roots, legal notices, Python imports and helpers resolve independently of the checkout/current directory.
- [ ] **PKG-07 — Target: fresh candidate test profile.**
  **Test:** Complete setup, close/reopen, and separately interrupt setup using a normal close before finishing.
  **Expected:** Completed choices persist; interrupted setup resumes only outstanding steps. Merely opening a step does not count as accepting/choosing it.
- [ ] **PKG-08 — Target: genuine Android upgrade from the older signed app.**
  **Test:** Install a newer candidate signed with the matching release certificate over the old test installation.
  **Expected:** Android accepts the upgrade and preserves settings/output access. Old Android jobs are not assumed recoverable where the old app never persisted them.

## Provider matrix: all 21 providers

For each row, use current accessible URLs from the app's accepted routes and
`docs/url-routing-audit/profile-fixtures.json`. On the primary desktop, check both
GUI and CLI: prepare a video, inspect metadata/qualities, complete one permitted
small download and play/seek it. Then exercise the listed profile/collection type
in its matching input. Use a source with more than one page when checking paging.

**Common expected outcome for every row:** the provider is recognized, the right
entry point is used, metadata belongs to the selected video, offered dimensions
are plausible, free limits are enforced, later-page IDs do not disappear or repeat,
and the completed file is readable. A genuine blocked/private/unavailable video
must produce a useful failure, not an empty success or a corrupt completed file.
The following rows add provider-specific expected outcomes.

| Check | Testing target and action | Additional expected outcome |
| --- | --- | --- |
| [ ] SITE-01 | **Porndoe:** `/watch/<id>`, pornstar and channel profiles; try one localized host. | MP4/RAW download works; the two profile types use Model URL. Duration is not mistaken for minutes. Unsupported model/playlist objects are not invented. |
| [ ] SITE-02 | **Pornhat:** video, `/models/` and `/sites/`; try one language host and `.one`. | HLS works; models/channels route correctly. Unsupported tags, paysite directories and playlists are rejected. |
| [ ] SITE-03 | **Bellesa:** video, Channel and Performer; include one rendition whose label differs from its dimensions. | Quality follows measured dimensions, e.g. a nominal 480 rendition may be 450p. The free ceiling is preserved; channel/performer listings work. |
| [ ] SITE-04 | **RedGIFs:** watch/embed, a user, niche and collection; include a mixed-image collection and portrait video. | Still images do not consume the video preview. MP4 SD/HD labels map to measured tiers; portrait videos are not mislabeled by their long dimension. |
| [ ] SITE-05 | **Porn.com:** native scene, generic collection, channel and pornstar, including an outbound referral card. | Shared `/<slug>` paths resolve by actual page type; the matching GUI field is required. Referrals are excluded before the free five-video preview. |
| [ ] SITE-06 | **YouJizz:** video/embed, numbered collection, verified pornstar link and public User uploads. | Actual 288p/368p tiers appear when provided. Directory-verified `/search/<name>-1.html` pornstar links work, general searches do not. User sort/page parameters behave consistently. |
| [ ] REG-01 | **PornHub:** ordinary video, Short, model/pornstar, user uploads and public playlist. | Uploads versus published videos are not confused; Shorts retain their supported path. Use CORE-05–07 for recovery. |
| [ ] REG-02 | **Eporner:** video, pornstar and channel; one localized accepted URL. | Numeric qualities resolve to the correct source/codec; channel paging works. |
| [ ] REG-03 | **XNXX:** video and public profile/user, including a multi-page profile. | Current links prepare; later pages and empty profiles do not crash. |
| [ ] REG-04 | **XVideos:** video, model/pornstar/channel and playlist; include a redirecting profile. | Redirected channels, later pages and HTML-escaped titles work; unsupported Quickies are not silently accepted as ordinary videos. |
| [ ] REG-05 | **XHamster:** video, supported Moment, creator/user/channel; authenticated list if available. | Video durations/qualities are plausible and the correct public/account feed is loaded. |
| [ ] REG-06 | **SpankBang:** video and a supported creator/profile/channel. | The major API update has not broken preparation, paging or download dispatch. |
| [ ] REG-07 | **YouPorn:** video, pornstar/channel and public collection; MP4 fallback fixture if available. | Public collections work. Unknown-resolution MP4 behavior still obeys its existing Premium gate. |
| [ ] REG-08 | **Beeg:** one public video. | Video-only support remains usable; no unsupported profile flow is advertised. |
| [ ] REG-09 | **Porntrex:** video and model/channel. | Quality selection, page traversal and native transfer complete. |
| [ ] REG-10 | **XFreeHD:** one public video, plus a small CLI gallery if available. | Video download works; photo-gallery support remains a CLI-specific feature. |
| [ ] REG-11 | **RedTube:** video, pornstar/channel/user and public playlist. | Appropriate containers and later pages still work after the major API change. |
| [ ] REG-12 | **Thumbzilla:** video, pornstar/channel/amateur and public playlist. | Reachable pages reconcile; a genuine traversal boundary is reported as incomplete, not full coverage. |
| [ ] REG-13 | **Tube8:** video and pornstar/channel/user; one supported alternate host. | Its adapter and localized routing remain usable; a failing late page is not silently counted as a complete scan. |
| [ ] REG-14 | **EMPFlix:** video and public profile/pornstar. | Correct metadata, source resolution and strict listing completion. |
| [ ] REG-15 | **TNAFlix:** video and profile/pornstar/channel. | Correct metadata, source resolution and strict listing completion. |

- [ ] **SITE-07 — Target: free versus Premium provider-container flows.**
  **Test:** Load the same public profile/collection with more than five playable videos in both contexts.
  **Expected:** Free exposes the five-video preview and at most 720p; Premium can traverse the full supported listing and higher available tiers.
- [ ] **SITE-08 — Target: unsupported provider inputs.**
  **Test:** Paste a general search, directory, category or wrong-kind URL into the relevant new-provider input.
  **Expected:** Clear rejection/guidance; keyword video search is not exposed and a directory is not misrepresented as a single creator.
- [ ] **SITE-09 — Target: multi-page discovery with a controlled late-page failure.**
  **Test:** Compare unique IDs across pages, then cause a later page to fail using a fixture.
  **Expected:** A full Premium traversal reaches genuine exhaustion. Failed traversal is marked incomplete/failed and keeps discovered data; there is no false success from an early subset.

## P0: shared transfers and recovery

- [ ] **CORE-01 — Target: ordinary desktop GUI HLS transfer.**
  **Test:** Start, Stop, Resume and complete a small download; play and seek near its end.
  **Expected:** Progress and button state follow the job, retained segments are reused, and the resulting file is complete/readable.
- [ ] **CORE-02 — Target: ordinary GUI/CLI MP4/RAW transfer.**
  **Test:** Stop after measurable bytes, resume and complete.
  **Expected:** The partial transfer resumes coherently, without duplicated output, lost progress or a misleading completed status.
- [ ] **CORE-03 — Target: normal close/reopen with a paused or active job.**
  **Test:** Note job ID, filename, quality and destination; close normally, reopen and resume.
  **Expected:** Restored work is paused with the same identity/quality/path and usable checkpoint. No duplicate new job is created for that same saved transfer.
- [ ] **CORE-04 — Target: cleanup-on-stop and skip-existing.**
  **Test:** Stop once with cleanup disabled and once enabled; separately queue a completed existing file with skip-existing enabled.
  **Expected:** Retained work can resume; explicitly cleaned work loses that checkpoint. Skipping an existing video does not overwrite it or silently rewrite its sidecars.
- [ ] **CORE-05 — Target: PornHub recovery on a controlled expiring/broken-source fixture.**
  **Test:** Exercise a video whose initial HLS source returns 410 or otherwise becomes stale.
  **Expected:** Recovery remains bounded, refreshes sources through the provider and can use the supported MP4 fallback. The UI remains responsive.
- [ ] **CORE-06 — Target: exhausted PornHub sources and unrelated failures.**
  **Test:** Use one fixture with no working HLS/MP4 after recovery and another with a filesystem failure or cancellation.
  **Expected:** Exhaustion produces the clear PornHub-source message. Cancellation and local file errors retain their own meaning rather than being relabeled as a server-source outage.
- [ ] **CORE-07 — Target: PornHub RAW fallback checkpoint.**
  **Test:** Once fallback is using MP4, stop and resume/reopen that job at a numeric quality ceiling.
  **Expected:** The RAW checkpoint stays RAW, is not overwritten by an HLS attempt, and selected quality never exceeds the ceiling.
- [ ] **CORE-08 — Target: queue concurrency and cancellation.**
  **Test:** Queue more jobs than the parallel limit; cancel one waiting job and stop one active job.
  **Expected:** Only the allowed number transfer, queued cancellation does not start the job, and unrelated jobs continue with independent states.
- [ ] **CORE-09 — Target: failed row, retry and session manager.**
  **Test:** Fail a job, inspect Error details, retry, then clear the main list and open Download manager.
  **Expected:** Retry updates the same logical job; session records remain meaningful after queue-row removal. Session-only history is not falsely promised across application restarts.
- [ ] **CORE-10 — Target: controls retained after provider updates.**
  **Test:** Apply a range/filter and custom filename to a small supported listing, then download selected entries.
  **Expected:** Filtering, selection, filename templates and the quality ceiling affect actual output, not just the displayed rows.

## P0: Media Library Export and Jellyfin

This feature targets desktop GUI and CLI. The mobile GUI is not expected to
publish multi-file NFO/artwork bundles.

- [ ] **META-01 — Target: default settings and free profile.**
  **Test:** Download with library export off; attempt to enable/use Premium export without Premium.
  **Expected:** Off creates no library sidecars. Free access is blocked clearly; ordinary allowed video downloads still work.
- [ ] **META-02 — Target: Premium automatic Alongside export.**
  **Test:** Complete a video with export enabled beside its existing filename.
  **Expected:** Video, `<stem>.nfo`, `<stem>.pornfetch.json` and available `<stem>-poster` artwork are consistent; no unrelated file is modified.
- [ ] **META-03 — Target: Premium Scene-folder layout.**
  **Test:** Start a new download using that layout, including two different videos with the same title.
  **Expected:** Separate provider/kind/identity-qualified scene paths avoid collisions; `movie.nfo`, `pornfetch.json` and available `poster` artwork accompany the correct video.
- [ ] **META-04 — Target: metadata field correctness.**
  **Test:** Compare title, description, date, runtime, performer credits and identity against a known source; include an item with missing fields.
  **Expected:** Known fields are correct and XML is escaped. Missing cast/date/studio stays absent; uploader/channel names are not invented as performers or production studios.
- [ ] **META-05 — Target: genre and studio-fallback options.**
  **Test:** Export with both options off, then individually enable them on suitable sources.
  **Expected:** Categories become genres only when opted in. Credited providers/publishers/channels enter studio fallback only when opted in; explicit producer data remains distinguishable.
- [ ] **META-06 — Target: real Jellyfin library import.**
  **Test:** Add a completed test bundle to a test Movies library and refresh it.
  **Expected:** Jellyfin associates NFO/artwork with the intended video and playback works. Provider-specific IDs are metadata, not a promise of universal deduplication.
- [ ] **META-07 — Target: manual sidecar/artwork preservation.**
  **Test:** Edit an exported NFO and replace its artwork; run normal repair/re-export. Compare hashes/content before and after.
  **Expected:** Your edits are preserved and the app reports that preservation. Owned, unchanged outputs can be refreshed without altering the video.
- [ ] **META-08 — Target: explicit CLI replacement.**
  **Test:** On a disposable bundle, repeat metadata-only export using `--replace-metadata`.
  **Expected:** Replacement occurs only with that explicit option, applies to the chosen sidecars and leaves video bytes unchanged.
- [ ] **META-09 — Target: saved-JSON metadata repair without network.**
  **Test:** Keep valid Porn Fetch JSON, remove an owned NFO, disable network and repair without a source URL.
  **Expected:** Metadata is regenerated from JSON; no video transfer or quality preparation is required.
- [ ] **META-10 — Target: metadata-only preview with an original URL.**
  **Test:** Choose an existing completed video and valid source URL, then preview or use CLI `--dry-run`.
  **Expected:** Correct fields/output plan appear without writing sidecars or downloading the video. A provider metadata loader may contact its player service.
- [ ] **META-11 — Target: CLI repair argument validation.**
  **Test:** Supply two files with mismatched source-URL counts; also combine a metadata-only request with a download request.
  **Expected:** Clear argument errors before work starts. Valid one-URL-per-file batches operate on the requested files only.
- [ ] **META-12 — Target: artwork or sidecar write failure.**
  **Test:** Use a controlled artwork failure or non-writable test destination during finalization.
  **Expected:** The downloaded video remains saved/readable. The app reports the export/artwork failure and offers the supported repair/retry rather than losing the successful transfer.
- [ ] **META-13 — Target: Jellyfin local/server path mapping.**
  **Test:** Configure valid differing local/server roots, then try a file outside the configured local root.
  **Expected:** Notifications use the mapped server path. An outside-root or invalid mapping fails explicitly; local sidecars/video remain intact.
- [ ] **META-14 — Target: Jellyfin credentials and notification failure/retry.**
  **Test:** Use a valid test key, then an invalid key/offline test server; retry through Activity or CLI `--retry-jellyfin FILE`.
  **Expected:** Successful notifications reach the test server. Failures remain distinct from video/export success; notification-only retry does not re-download or rewrite the video.
- [ ] **META-15 — Target: simultaneous completion and notification batching.**
  **Test:** Complete several short exports together and inspect the test server's received update paths.
  **Expected:** The intended files are notified without losing paths or sending duplicate updates for the same path in a batch.
- [ ] **META-16 — Target: portable JSON and privacy.**
  **Test:** Inspect exported JSON and NFO for a source loaded with an authenticated session.
  **Expected:** Public source identity is retained, including needed PornHub viewkey; cookies, credentials, Jellyfin keys and transient signed stream/image URLs are not exported.

## P0: Creators discovery, storage and downloads

- [ ] **CR-01 — Target: Creators availability with history disabled.**
  **Test:** Disable optional history and open Creators with a valid PocketBase runtime.
  **Expected:** Creator storage remains available and uses the shared database service; optional history being off does not disable subscriptions.
- [ ] **CR-02 — Target: add/edit subscription.**
  **Test:** Add a supported source with a name/destination; change the global quality; create another source; edit the first.
  **Expected:** Source type is resolved correctly, new sources default to Best available, and editing retains saved quality rather than adopting the global setting.
- [ ] **CR-03 — Target: normalized duplicate subscription URLs.**
  **Test:** Re-enter the same logical source using a page parameter/trailing slash variant.
  **Expected:** Pagination is normalized to the subscription identity; equivalent sources are not silently duplicated. Legitimately different feed/sort identities remain meaningful.
- [ ] **CR-04 — Target: first full Premium scan and rescan.**
  **Test:** Scan a known multi-page source twice, comparing unique IDs/counts.
  **Expected:** Both scans genuinely traverse the listing; unchanged identities are not duplicated. Last attempt and last completed scan are distinct and scan history is accurate.
- [ ] **CR-05 — Target: dashboard paging and status counts.**
  **Test:** Use more than 12 discovered videos; move between pages and status filters.
  **Expected:** All appropriate records are reachable with coherent counts and page bounds; changing a filter does not leave an invalid empty page.
- [ ] **CR-06 — Target: stop/fail partway through a scan.**
  **Test:** Stop a multi-page scan and separately use a controlled later-page failure; scan again.
  **Expected:** Partial discoveries persist. The attempt is stopped/incomplete/failed, not a completed baseline. Retry starts a proper full traversal without duplicates.
- [ ] **CR-07 — Target: automatic-download baseline.**
  **Test:** Enable automatic downloading on a new controlled source, finish its first full scan, then add one new source video and rescan.
  **Expected:** Existing archive items are not automatically bulk-downloaded by the first baseline. Only eligible additions after a successful baseline auto-queue.
- [ ] **CR-08 — Target: startup scanning.**
  **Test:** Enable Scan when Porn Fetch starts, close/reopen normally and wait; remain open afterward.
  **Expected:** Startup scan runs after setup/entitlement readiness, once per launch. No periodic or closed-app scan scheduler is implied.
- [ ] **CR-09 — Target: creator quality ceiling and worker limits.**
  **Test:** Set a subscription's numeric ceiling below the global setting, then request more downloads than the parallel limit.
  **Expected:** Actual transfers honor the subscription ceiling and existing concurrency gates, with bounded preparation/dispatch and coherent progress.
- [ ] **CR-10 — Target: creator HLS and RAW normal restart recovery.**
  **Test:** For each transfer type, pause or close normally after progress; reopen and resume.
  **Expected:** The same job ID, filename, chosen quality, destination and native partial state are reused; completed files are readable.
- [ ] **CR-11 — Target: destination changes after preparation.**
  **Test:** Prepare/pause a job for folder A, change global/subscription destination to B, then resume that job and prepare a new one.
  **Expected:** The existing job remains pinned to A; eligible newly prepared work uses the new destination as configured.
- [ ] **CR-12 — Target: video shared by two subscriptions.**
  **Test:** Discover the same provider/video through two sources, complete it, then rescan/request it through the other source.
  **Expected:** Completion/identity is shared and unnecessary duplicate transfers are avoided; membership-specific state remains separate.
- [ ] **CR-13 — Target: ignoring and removing sources.**
  **Test:** Ignore one shared video in one subscription, then remove a subscription with completed/shared jobs.
  **Expected:** Ignore is membership-specific. Removal preserves downloaded files and jobs still referenced elsewhere; unrelated subscriptions remain valid.
- [ ] **CR-14 — Target: persistent free preview.**
  **Test:** In a free context, scan a source with more than five videos, download/ignore some, rescan and restart.
  **Expected:** The same five durable preview identities remain eligible, including completed/ignored ones; the preview does not rotate into a free full archive. Quality stays at most 720p.
- [ ] **CR-15 — Target: free requests for full archives, automation or saved high-quality work.**
  **Test:** Attempt automatic download/full archive work and resume a previously prepared above-720p job in the free test context.
  **Expected:** Premium-only actions are blocked; high-quality saved work remains paused rather than silently downloading or overwriting its checkpoint at another quality.
- [ ] **CR-16 — Target: entitlement mode captured by an in-progress scan.**
  **Test:** In a controlled test context, let a scan start in preview mode and make Premium available before it finishes.
  **Expected:** That attempt remains a preview and does not establish a full baseline. A subsequent full Premium scan is needed. This tests the new feature boundary, not licensing-server lifecycle correctness.
- [ ] **CR-17 — Target: migration of an existing draft/test creator database.**
  **Test:** Open a backup copy of a pre-current creator database with known records.
  **Expected:** Migrations preserve existing records and make current paging/counts/batch operations usable; migration failure is visible and Add remains unavailable until repaired.
- [ ] **CR-18 — Target: completion after queue-row removal and missing finished file.**
  **Test:** Complete a creator transfer, let the ordinary queue remove it, restart and rescan; separately move a finished test file deliberately.
  **Expected:** Completion remains committed before row removal. A moved/deleted completed file is not automatically redownloaded merely because it disappeared; that is the current documented behavior.
- [ ] **CR-19 — Target: one-time Premium quality default.**
  **Test:** In a fresh test profile, observe the first Premium UI initialization; then choose a lower global quality and restart/refresh the existing entitlement.
  **Expected:** First initialization selects Best available once. Later refreshes preserve the user's chosen quality. Use an existing Premium test entitlement; no payment or renewal lifecycle retest is needed.

## P1: CLI presentation and workflow regressions

- [ ] **CLI-01 — Target: frozen CLI Home and action restoration.**
  **Test:** Enter Download, Settings and administrative menus, then Escape/back out repeatedly.
  **Expected:** Breadcrumbs and selection return to the intended action; prompts do not accidentally launch a previous choice.
- [ ] **CLI-02 — Target: Settings search, including no results.**
  **Test:** Filter by a setting name, description and original configuration key; clear it; enter a no-match query and press Enter.
  **Expected:** Search finds the right settings and contextual help; no-match Enter activates nothing. This is settings filtering, not video keyword search.
- [ ] **CLI-03 — Target: setting validation and persistence.**
  **Test:** Edit a numeric setting with one invalid and one valid value; cancel another edit; restart.
  **Expected:** Invalid values are rejected, cancellation preserves the prior value, and valid changes persist and affect the existing service consumers.
- [ ] **CLI-04 — Target: narrow/short terminals and live resize.**
  **Test:** Use approximately 40×12, then 80×24 and a wider terminal while in a long menu/table.
  **Expected:** Selection/help remain accessible, output does not erase unrelated scrollback, and narrow tables become readable labeled records.
- [ ] **CLI-05 — Target: keyboard controls and multi-selection.**
  **Test:** Use arrows, Tab/Shift+Tab, Page Up/Down, Space, Enter and Escape on a long selection.
  **Expected:** Unavailable choices are skipped, Space toggles only the intended rows and Enter confirms the visible selection.
- [ ] **CLI-06 — Target: plain and color-free modes.**
  **Test:** Run with `PORNFETCH_PLAIN=1`; separately use `NO_COLOR=1` and a dumb terminal.
  **Expected:** Plain mode uses numbered menus without cursor-control sequences; no-color mode still has a visible selection indicator.
- [ ] **CLI-07 — Target: non-TTY/EOF and text defaults.**
  **Test:** Use redirected input in a test shell, EOF at a prompt, empty text and `/clear` in plain mode.
  **Expected:** The CLI cancels or consumes input deterministically without hanging; empty input retains a default and `/clear` explicitly empties it.
- [ ] **CLI-08 — Target: existing batch commands.**
  **Test:** Run a URL, profile, playlist and saved-job resume command using existing flags/settings JSON.
  **Expected:** Argument names, config keys and paths remain compatible; the UI rewrite has not changed their underlying download behavior.
- [ ] **CLI-09 — Target: account workflows.**
  **Test:** Use an owned test account/browser session through supported account lists, including a multi-select list.
  **Expected:** Authentication and selected feed/list behavior work; credentials are not printed in headers, lists or help.
- [ ] **CLI-10 — Target: visible progress and interrupted commands.**
  **Test:** Observe HLS, RAW and collection progress; cancel a prompt or stop a transfer through supported controls.
  **Expected:** Units remain explicit, the terminal is usable afterward, and job cancellation does not silently start extra work.
- [ ] **CLI-11 — Target: interactive versus batch metadata operations.**
  **Test:** Set library-export options through interactive Settings, then execute a valid batch export and metadata-only repair.
  **Expected:** Both frontends consume the intended saved settings and preserve the same sidecar ownership rules.
- [ ] **CLI-12 — Target: history/database administrative flows.**
  **Test:** Inspect history, return, change the configured test database setting through the supported flow and reopen history.
  **Expected:** One tracker/service lifecycle is respected; switching does not reset an active service's credentials or break subsequent downloads.

## P0/P1: Android native integration

- [ ] **AND-01 — Target: setup on a touch phone and a TV remote.**
  **Test:** Scroll text, check acceptance, choose reporting explicitly, revisit steps and finish storage setup.
  **Expected:** Inputs are reachable; arrows alone do not choose reporting. Touch does not acquire unwanted automatic focus outlines; remote focus is visible.
- [ ] **AND-02 — Target: SAF folder picker.**
  **Test:** Cancel, reopen, choose a folder and restart before exporting a file.
  **Expected:** Cancel leaves setup/previous destination intact. Accepted read/write access persists and another app can read the completed output.
- [ ] **AND-03 — Target: MediaStore fallback on Android 10+, including a picker-stub TV/AAOS image.**
  **Test:** Choose Use shared Downloads/Porn Fetch and complete a short transfer.
  **Expected:** Setup finishes without a picker or broad storage permission; shared output is published only after copying and is playable externally.
- [ ] **AND-04 — Target: shared export failure and skip-existing.**
  **Test:** Use a controlled missing-source/write failure, then repeat an already published filename with skip-existing enabled.
  **Expected:** Failure keeps the private original and removes incomplete published output. Skip checks the app's published destination rows without silently claiming an unrelated file.
- [ ] **AND-05 — Target: Back, Settings details and edge swipes.**
  **Test:** Visit several pages, enter a Settings detail, use hardware Back/header Back and inward edge swipes; try short/vertical drags and a modal dialog.
  **Expected:** All valid Back actions follow the same history, detail returns to categories first, and short/vertical/modal drags do not navigate the page underneath.
- [ ] **AND-06 — Target: portrait/landscape phone and fixed-orientation car/TV.**
  **Test:** Rotate the phone with and without rotation lock and open the same pages on a fixed-orientation display.
  **Expected:** System orientation policy wins and usable layout follows width; no forced-orientation flicker loop or inaccessible controls.
- [ ] **AND-07 — Target: TV launcher and bundled graphics.**
  **Test:** Rebuild/install the APK and open it from the TV Apps list; inspect banner, icons and setup SVGs.
  **Expected:** A readable Porn Fetch launcher/banner is present; missing touchscreen is not an installation requirement and artwork is not blank.
- [ ] **AND-08 — Target: actual Android Creators runtime on ARM64 and other shipped ABIs.**
  **Test:** Add a source, complete a scan, pause HLS/RAW work, close normally and reopen.
  **Expected:** Embedded PocketBase loads, migrations/authentication work, subscriptions persist and prepared jobs restore paused with private checkpoints.
- [ ] **AND-09 — Target: creator export destination pinning on Android.**
  **Test:** Prepare work for shared destination A, change the app folder to B and resume.
  **Expected:** Existing jobs finish into A; future prepared jobs use their newly configured destination. Private app files are not presented as externally accessible final output.
- [ ] **AND-10 — Target: Android/iOS feature availability boundaries.**
  **Test:** Open history/statistics and library-export-related entry points on mobile, and Creators on iOS.
  **Expected:** Unsupported features stay unavailable with useful messaging; no hidden fallback claims desktop-only functionality succeeded.

## P0: signed updates and channel selection

For controlled feed cases, use isolated signed staging repositories and test
builds. A normal user clicking Check for updates cannot force a missing/tampered
feed, a newer release or a metadata publication race.

| Check | Testing target/setup | Expected selection/result |
| --- | --- | --- |
| [ ] UPD-01 | Existing Stable settings; Stable 3.9.2 and Beta 3.9.3 available; installed 3.9.1. | Stable 3.9.2 only. Upgrade introduces a Stable preference without converting existing users to Beta. |
| [ ] UPD-02 | Beta selected with the same controlled releases. | Beta 3.9.3, because it is numerically newer. |
| [ ] UPD-03 | Beta selected; Stable 3.9.4 and Beta 3.9.3 available. | Stable 3.9.4. Beta preference includes newer Stable releases. |
| [ ] UPD-04 | Installed Beta 3.9.3, switch to Stable while only Stable 3.9.2 exists. | Preference persists and a new check occurs, but there is no downgrade offer. |
| [ ] UPD-05 | Equal numeric versions on both feeds in a test fixture. | Stable wins a tie. A missing feed/target reported as 404 can yield no offer; invalid/expired signed metadata remains an error, not unsigned fallback. |
| [ ] UPD-06 | Fresh Beta build profile versus a pre-existing profile. | Fresh Beta settings follow build channel; an existing profile without the preference migrates to Stable. GUI and CLI preferences are stored independently. |

- [ ] **UPD-07 — Target: manual/startup update preferences in desktop and Android.**
  **Test:** Disable automatic dialogs, restart with a newer test offer, then open manual review; separately disable startup checks.
  **Expected:** Dialog opt-out and checking are separate preferences. Manual checking/review remains available and correctly labels installed/offered versions and channels.
- [ ] **UPD-08 — Target: update download size, release notes and native renderer.**
  **Test:** Review a known-size offer and long Markdown/HTML notes, then download on the real desktop renderer and Android.
  **Expected:** Preview size is meaningful before confirmation. Progress does not clamp incorrectly; Android counts APK bytes, not metadata bytes. Notes scroll without a native-renderer crash.
- [ ] **UPD-09 — Target: installed desktop GUI update and component management.**
  **Test:** Accept a newer signed offer, then exercise component management for the current installed version.
  **Expected:** Verified repository bytes are staged and IFW handles installation/components. Current-version component management works; older repositories are refused. Portable/source copies retain their manual-update boundary.
- [ ] **UPD-10 — Target: Android unknown-source permission denied/allowed return path.**
  **Test:** Start a same-certificate newer update with permission initially disabled; deny once, then allow and return.
  **Expected:** Denial is visible. Allowing returns to installation confirmation using the retained, revalidated request, without requiring a second manual install action.
- [ ] **UPD-11 — Target: full Android same-key update.**
  **Test:** Cancel confirmation once, then complete a genuine newer APK installation and reopen.
  **Expected:** Cancel preserves the current app. Successful installation updates the version and retains app data/destination. Notification commands still work; they do not replace the installer observer.
- [ ] **UPD-12 — Target: wrong identity/certificate/ABI or changed accepted Android offer.**
  **Test:** Use isolated mismatched fixtures and change publication after an offer is accepted.
  **Expected:** Wrong identity/ABI/signature or changed version/hash is rejected. The current application remains usable and the user is told to check again where appropriate.
- [ ] **UPD-13 — Target: desktop accepted-offer pinning.**
  **Test:** Accept an offer, then replace its staging feed metadata/payload in a controlled fixture before completion.
  **Expected:** The accepted authenticated manifest/hashes govern staging; different bytes cannot silently become the installed update.
- [ ] **UPD-14 — Target: frozen CLI interactive self-update and per-command channel override.**
  **Test:** Decline an offer, cause one staging failure, then stage a valid newer update. Use `self-update --channel beta --check` separately.
  **Expected:** Decline/failure returns to a usable menu. Only successful staging closes resources for replacement; the binary updates. The command override does not overwrite the saved channel.
- [ ] **UPD-15 — Target: iOS update catalog.**
  **Test:** With a suitable newer ARM64 IPA in the test catalog, check Stable and Beta selection and open the offered link.
  **Expected:** Eligibility/version policy is consistent with the other frontends; the handoff is the correct download page, with manual sideloading rather than an in-app installer claim.
- [ ] **UPD-16 — Target: offline/cancelled update and Tor-routed update.**
  **Test:** Cancel a download, check offline and use an unavailable Tor route in a test network.
  **Expected:** Useful status and usable current app; no unverified installation or direct-network fallback when a Tor route is required.

## P1: privacy and cross-feature UI checks

- [ ] **PRIV-01 — Target: Anonymous Mode with Creators and export preview open.**
  **Test:** Open populated creator details and a metadata preview, then enable Anonymous Mode.
  **Expected:** Subscription/video titles, source URLs and destinations are hidden where promised; detailed error/metadata previews close or redact. Actual saved media is not deleted.
- [ ] **PRIV-02 — Target: Jellyfin request isolation.**
  **Test:** Use a controlled test server while the provider session has cookies/authentication.
  **Expected:** The notification has only the intended Jellyfin authentication and paths; provider cookies/auth headers do not cross into that session.
- [ ] **PRIV-03 — Target: Jellyfin under All app traffic Tor policy.**
  **Test:** Enable that route and observe the controlled server/network; then make Tor unavailable.
  **Expected:** The policy is honored with no silent direct fallback. An unreachable LAN-only Jellyfin server may fail through Tor, while local video/sidecars remain saved.
- [ ] **PRIV-04 — Target: reporting choices after CLI/settings navigation changes.**
  **Test:** Cancel a reporting edit and change between the explicit available scopes in a disposable profile.
  **Expected:** Cancel preserves consent, Off remains off, and Full is not enabled implicitly. This is a settings-integration check, not a rerun of the licensing/reporting backend lifecycle.
- [ ] **UI-01 — Target: keyboard-only desktop/new feature dialogs.**
  **Test:** Navigate Creators, library export, update selector and help with Tab/arrows/Enter/Escape, including opening/closing nested dialogs.
  **Expected:** Visible focus, reachable controls, stable return focus and no accidental underlying-page action.
- [ ] **UI-02 — Target: light/dark/high contrast/reduced motion and larger text.**
  **Test:** Toggle each while using new pages, including native platform style and the real GPU renderer.
  **Expected:** Labels/control states remain legible, selected/focused states differ clearly, reduced motion suppresses the intended animations, and controls remain reachable.
- [ ] **UI-03 — Target: GUI language versus content-language controls.**
  **Test:** Inspect language settings and the provider content-language selector/flag icons.
  **Expected:** The application stays English-only where translation selection is disabled; content-language controls and bundled SVG flags still work where supported.

## Maintainer P0/P1: build and publication operations

These checks are manual maintainer/staging work, not things the ordinary GUI can
verify. Use a disposable release namespace/staging service for negative fixtures.
This report does not authorize the assistant to publish or deploy anything.

- [ ] **OPS-01 — Target: clean dependency resolution for the final build.**
  **Test:** Build in a clean environment using the project's fresh-resolution policy and retain its dependency inventory.
  **Expected:** The pinned native inputs and resolved Python/provider packages match that build's requirements; success does not depend on editable/local packages or an old developer lockfile.
- [ ] **OPS-02 — Target: deployment prerequisites for channel feeds.**
  **Test:** Verify the matching Server Android routes/Caddy configuration, release intake and refresh endpoint on staging before testing clients.
  **Expected:** Signed channel-specific desktop, CLI and Android paths serve the intended artifacts; a missing deployment is diagnosed as such, not marked as an application test pass.
- [ ] **OPS-03 — Target: Stable/Beta release identity across CI outputs.**
  **Test:** Build one staging release per channel and compare GUI/CLI identity, signed target custom fields, catalog, release timestamp and GitHub prerelease flag.
  **Expected:** Each output agrees on channel/version/commit/identity and numeric versions increase for distinct releases.
- [ ] **OPS-04 — Target: metadata renewal and legacy compatibility feeds.**
  **Test:** Run the staging refresh and use an old client to discover a Stable bridge update.
  **Expected:** Valid metadata expiry/counters advance without changing payload identities; legacy feeds let old clients upgrade. Beta publication does not overwrite Stable compatibility feeds.
- [ ] **OPS-05 — Target: Android signing and alignment outputs.**
  **Test:** Build using a development key and separately the staging/release-signing path; inspect the final APK signature/alignment.
  **Expected:** Installable signed output is produced, 16 KiB alignment requirements are met and a debug certificate is not confused with the release update certificate.
- [ ] **OPS-06 — Target: final package/legal inventories and helper components.**
  **Test:** Inspect downloaded distribution contents and the installed component selection.
  **Expected:** Required libraries, exact dependency notices and appropriate helper executables accompany the package; private build logs/keys and diagnostic unsigned APKs are not release assets.

## Documentation checks

- [ ] **DOC-01 — Target: README artwork, download button and progress badge.**
  **Test:** Open them from the repository/release view used by users.
  **Expected:** Artwork renders; download points to the intended published version/channel; the 4.0 progress badge is not mistaken for the installed application's version.
- [ ] **DOC-02 — Target: candidate release notes and version labels.**
  **Test:** Compare the final candidate's feature list with its commit/build identity and update dialog notes.
  **Expected:** The narrow v3.9.1 hotfix is distinguished from later development features; notes include the actual shipped changes rather than claiming them for the old tag.
- [ ] **DOC-03 — Target: provider support table and internal guide links.**
  **Test:** Reconcile the table with the router and follow provider-guide links.
  **Expected:** All 21 providers, including RedGIFs, are represented accurately and no link points to a removed guide. The current missing row/broken links are established findings to fix.

## Separate checklist: uncommitted working-tree additions

Run these only when the candidate includes the local modifications/untracked files
reviewed on 2026-11-16. They must not be attributed to `85b6723` or expected in a
CI artifact built solely from current committed master.

- [ ] **WIP-01 — Target: offline Supported websites catalog, desktop/phone/tablet.**
  **Test:** Disconnect network, open the catalog, filter names/domains and capabilities, expand guidance and return.
  **Expected:** All 21 router providers are present with appropriate capabilities. Filtering is local catalog filtering, not video search; keyboard/touch layouts work.
- [ ] **WIP-02 — Target: relocated Creators navigation and icons.**
  **Test:** Open Creators beside Account on desktop/tablet and from phone navigation; return to Downloads/Settings/catalog.
  **Expected:** Correct pages open, focus/index state remains coherent, and the bundled icon is visible on each layout.
- [ ] **WIP-03 — Target: complete Android TV remote navigation.**
  **Test:** Using only D-pad/center/Back, add a URL, use filters, select quality, start/stop/resume, open Manager/Account/Settings/Creators/catalog and help/error dialogs.
  **Expected:** Controls have visible focus, arrows and center work, focused controls scroll into view, and closing dialogs restores their opener without acting on the underlying page.
- [ ] **WIP-04 — Target: long lazy lists and list mutations on TV.**
  **Test:** Traverse far beyond the initially visible rows, move back, then remove a focused row or let it finish.
  **Expected:** New rows remain reachable, disabled/hidden actions are skipped and focus recovers to a usable control rather than disappearing.
- [ ] **WIP-05 — Target: TV editing, adjustment and selector popups.**
  **Test:** Center enters URL/title-format/license text editing or slider/number adjustment; Back finishes; open a selector and choose/cancel.
  **Expected:** Native input works, value changes are saved, and arrows resume navigation afterward. An open selector traps selection instead of moving the underlying page.
- [ ] **WIP-06 — Target: TV/car links, pasted license and shared destination choices.**
  **Test:** Open a help/purchase link, use pasted license-file contents in a test profile and choose shared Downloads from Settings/Add videos.
  **Expected:** Links display a usable address without requiring a browser; text import uses the existing bridge; storage choice is retained without a document picker on supported Android versions.
- [ ] **WIP-07 — Target: raw automotive rotary input and delivered nudges.**
  **Test:** Rotate both directions through controls and a long reader; center-adjust a value; choose inside an open combo popup; switch to touch.
  **Expected:** Sequential focus, value/selection changes and scrolling work without leaking input to hidden pages. Touch restores its normal policy; mouse/media/volume/Home behavior is preserved.
- [ ] **WIP-08 — Target: real AAOS UX restriction transitions and lifecycle.**
  **Test:** On an appropriate test vehicle/image, enter/leave a system restriction; pause/resume while editing; repeat from setup and creator details.
  **Expected:** Underlying content and link launches are blocked while restricted; history/setup survive; editing/adjustment ends on pause even if Qt only observes resumed state. OS parked-use restrictions are not bypassed.
- [ ] **WIP-09 — Target: AAOS compatibility UI, generic head unit and wide displays.**
  **Test:** Compare a system-compatibility device with one needing app Back/Close, then enable manual Car layout on a generic Android head unit.
  **Expected:** Navigation is available without duplicate app-level controls where the system supplies them. Safe areas/large shared targets remain usable in portrait and ultrawide layouts. Manual layout does not claim a missing vehicle API exists.
- [ ] **WIP-10 — Target: native OEM RotaryService controllers.**
  **Test:** Identify whether the device delivers raw events or consumes them in its accessibility-based RotaryService; exercise the actual controller through all key flows.
  **Expected:** For a claim of full support, native focus must enter, traverse and leave the Qt scene correctly. The current code lacks FocusParkingView/FocusArea integration: record that limitation/blocked coverage rather than counting raw-event tests as proof. Android Auto and CarPlay are not supported projection targets.
- [ ] **WIP-11 — Target: website APK re-signing and publication retry.**
  **Test:** In staging, publish an artifact with a different development certificate, then retry publication with the already-correct signed APK.
  **Expected:** Public APKs use the release certificate; same-key installation works. Repeating correct signing preserves bytes so catalog hashes/identity stay immutable.
- [ ] **WIP-12 — Target: interrupted GitHub/CLI publication and expired metadata recovery.**
  **Test:** Interrupt a staging asset upload, retry identical artifacts, then attempt changed bytes under the same version; separately renew expired but authenticated prior metadata.
  **Expected:** Identical retries resume safely; conflicting bytes/tag/channel are rejected. Renewal preserves authenticated identity/counters and does not silently reset trust.
- [ ] **WIP-13 — Target: Python wheel/sdist and experimental release gating.**
  **Test:** Install the built wheel into a clean environment outside the checkout; exercise its CLI; simulate a requested experimental-build failure on staging CI.
  **Expected:** Installed CLI works with stamped identity. Requested failed targets block the relevant publication rather than yielding an apparently complete release.
- [ ] **WIP-14 — Target: PocketBase checksums, target notices and Windows file version.**
  **Test:** Verify a known runtime download, reject a controlled changed archive, inspect final Android notices and Windows executable properties.
  **Expected:** Known checksums succeed, altered/unknown archives fail, target-specific notices ship, and executable metadata matches the stamped version.

## Suggested first session

If time is limited, start with PKG-01–03, CORE-01–03, CR-01/04/07/10/14,
META-02/07/09/14, UPD-01–04/10/11/14 and CLI-02/04/06. These cover the
highest-impact cross-feature failures before spending time on cosmetic checks.
For a candidate including local TV/Automotive work, add WIP-03/05/07–10.
A blocked fixture or unsupported platform still needs an explicit recorded reason;
it is not a successful verification.
