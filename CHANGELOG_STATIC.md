# v4.0
## Website support and downloads
- Added Porndoe videos, pornstar profiles and channels, using MP4 downloads.
- Added Pornhat videos, model profiles and channels, including supported localized
  domains and the pornhat.one alias.
- Added Bellesa videos, performers and channels, using measured HLS quality tiers.
- Added RedGIFs videos, users, niches and user collections. Still images are
  excluded from video listings; MP4 quality selection uses actual dimensions.
- Added Porn.com videos, collections, channels and pornstars, with page-type
  detection and external referral filtering before the free preview limit.
- Added YouJizz videos, numbered collections, directory-verified pornstar pages
  and user uploads.
- Updated provider APIs and shared pagination handling across existing providers.
  Supported full-listing scans traverse every page and surface incomplete scans.
- Improved PornHub recovery with bounded source refreshes, MP4 fallback, clearer
  exhausted-source errors and preservation of existing MP4 resume checkpoints.
- Added an offline Supported websites page on desktop and mobile with all 21
  providers, domain/name and capability filters, and supported-link guidance.

## Creator subscriptions

- Added persistent Creators subscriptions with source names, destinations, saved
  quality ceilings, manual scans and scan-on-startup.
- Added paged discovery results, status counts, scan progress and recent attempt
  history, distinguishing partial attempts from completed scans.
- Premium supports full archives and optional automatic downloading of new
  discoveries after the first successful baseline. The initial baseline does not
  automatically download the existing archive.
- Free users can scan, download and resume the same five preview videos per
  subscription at up to 720p. Rescans do not rotate the preview into a full archive.
- Creator jobs use the existing queue and preserve identity, quality, destination
  and HLS/MP4 checkpoints across normal close and reopen. Completed identities are
  shared between subscriptions; removing a subscription preserves downloaded files.
- Added proactive storage availability checks and repair guidance. Creators works
  independently of optional history recording; Android embeds PocketBase and keeps
  recovery state in private app data. iOS Creators remains unavailable.
- Improved Creators placement, controls, contrast and subscription defaults. New
  subscriptions use Best available; the first Premium GUI unlock sets global
  quality to Best available once and preserves later user choices.

## Media library and Jellyfin

- Added Premium desktop GUI and CLI export of NFO files, portable JSON metadata
  and artwork, with Alongside and Scene-folder layouts.
- Added metadata preview, dry-run, repair and retry for existing videos, including
  repair from saved JSON without downloading the video again.
- Added ownership checks that preserve manually edited sidecars unless replacement
  is explicitly requested, plus optional genre/studio mappings and settings help.
- Added optional Jellyfin library notifications, local-to-server path mapping,
  batched updates and separate notification retry. Notification failures preserve
  downloaded media and exported sidecars; credentials stay out of exported metadata.
- Applied anonymous-mode redaction to the new library and creator surfaces.
  Automatic library-sidecar export is not available in the mobile GUI.

## CLI

- Redesigned interactive menus with breadcrumbs, restored selections, keyboard
  navigation, searchable settings, validation and clearer progress presentation.
- Added compact narrow-terminal layouts and a plain numbered-menu mode for basic
  terminals, disabled color and non-interactive environments.
- Integrated creator workflows, library metadata commands and update-channel
  settings while retaining existing batch flags and configuration compatibility.

## Android, TV and Automotive

- Added TV launcher integration and a banner, optional touchscreen/Leanback
  requirements, larger TV text and screen margins.
- Added spatial D-pad navigation, visible focus, focused-item scrolling, lazy-list
  traversal, center/Enter activation and predictable Back/focus restoration.
- Added remote editing and adjustment modes for text, sliders and number controls;
  improved keyboard/remote access to setup, dialogs, Settings and download controls.
- Added page history and edge-swipe Back navigation, touch-aware focus policy and
  system-controlled portrait/landscape rotation with responsive layouts.
- Added a shared Downloads destination through MediaStore on Android 10+, including
  incomplete-copy cleanup and app-owned skip-existing checks. Android 9 still
  requires a working folder picker. Prepared jobs retain their saved destination.
- Added TV/car web-address dialogs and pasted license-file contents in Android
  Settings, reducing reliance on a browser or document picker.
- Added optional Android Automotive OS integration with vehicle UX restrictions,
  a restricted-use overlay, safe-area handling, larger shared controls and an
  explicit Car layout for generic head units.
- Added handling for delivered rotary encoder and directional events. Native OEM
  RotaryService FocusParkingView/FocusArea integration is not implemented; this
  does not provide Android Auto or CarPlay projection support.
- Fixed update installation after returning from unknown-source permission
  settings and preserved shared native file-observer callbacks.
- Added update download sizes and clearer APK byte progress. Android builds align,
  sign and verify APKs automatically, and packaging checks native ABI requirements.

## Stable/Beta updates and release packaging

- Added independently saved Stable/Beta preferences in GUI and CLI. Stable receives
  Stable releases; Beta receives the newest eligible Stable or Beta release without
  downgrading. Existing preferences migrate to Stable; fresh installs follow the
  build's channel.
- Added channel-specific signed desktop, CLI and Android feeds, pinned update
  offers and channel/identity verification. Normal desktop discovery no longer
  falls back to unsigned release information. iOS updates remain manual sideloading.
- Propagated a shared numeric version, channel, commit and timestamp through build
  artifacts, website catalogs and GitHub prerelease publication.
- Added scheduled renewal of Stable, Beta and legacy signed metadata while
  preserving payload identity and existing trust roots. Missing desktop feeds are
  skipped; invalid metadata and server errors still fail renewal.
- Preserved legacy Stable upgrade feeds and added authenticated expired-metadata
  recovery, immutable publication retries and resumable GitHub draft uploads.
- Added website APK re-signing with the release key, retaining identical bytes
  when an APK already has the correct signature.
- Added stamped wheel/source distributions and an installed-wheel CLI smoke check,
  requested experimental-build publication gates, checked PocketBase downloads,
  native Android notices and Windows executable version stamping.
- Updated Qt/Android native deployment recipes and bundled bindings, provider
  staging for iOS, dependency resolution, tests and release documentation.
- Fixed CI import lint, nullable Porn.com HTML attributes and a Creators access
  callback during GUI teardown.
