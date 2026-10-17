# URL audit implementation follow-up

Implemented 2026-10-17. The [audit](URL_ROUTING_AUDIT.md) and original observation
files are historical baseline evidence, not the current implementation status.

## API versions

| Package | Version |
|---|---|
| eaf_base_api | 4.2.2 |
| PornHub | 5.4.5 |
| Eporner | 2.4.3 |
| XNXX | 2.4.3 |
| XVideos | 2.5.2 |
| XHamster | 2.6.3 |
| SpankBang | 2.4.3 |
| YouPorn | 1.8.2 |
| Beeg | 1.7.3 |
| Porntrex | 1.8.2 |
| XFreeHD | 1.7.3 |
| RedTube | 1.4.3 |
| Thumbzilla | 1.4.2 |
| Tube8 | 1.3.2 |

The provider packages require `eaf-base-api>=4.2.2`. The shared core supplies
query replacement and path composition helpers and records same-site redirect
destinations as `BaseMedia.resolved_url`. The caller's URL remains separate from
this transport metadata. Redirect identity survives text-cache hits.

## Changes

- XNXX and XVideos parse the profile listing JSON and resolve item links against
  the submitted provider host. XNXX uses the response's `eid` for canonical video
  identity; its profile-click URL contains a different tracking token. XVideos
  profile aliases replace the resource prefix rather than nesting prefixes.
- Profile, collection, playlist and album pagination compose paths and queries
  separately, replace existing page keys, retain filters, and remove document
  anchors. Porntrex starts at page 1; SpankBang requests the specified number of
  pages. Eporner infers its page count from pagination links instead of assuming
  a fixed number of videos per page.
- Beeg keeps significant trailing zeros and excludes queries/slashes from the
  resource key. Eporner recognizes embed IDs and resolves listing links once.
  Known PornHub, Eporner, YouPorn and SpankBang player-only variants normalize to
  the corresponding full page before parsing.
- The five affected client constructors preserve the configured language header.
  Listing extractors preserve localized origins when resolving relative links.
- Porn Fetch shares hostname policy between GUI and CLI routing, recognizes
  plural RedTube channels and XVideos bare channels with queries/video tabs,
  follows XVideos profile-to-channel identity, and honors explicit PornHub
  uploaded/featured tab selection. Unsupported directory/type/short-tab inputs
  are rejected rather than falling through to the single-video parser.

Unverified historical mirrors and unimplemented resource families were not
advertised as newly supported. GIFs, Quickies, unsupported profile tabs, and
unsupported provider playlists/albums still require their own extraction paths.
The separate live GUI profile diagnostic suite discussed with the audit remains
future work; these changes repair the underlying APIs and routing first.

## Verification

- 24 focused offline regressions across the 13 provider repositories.
- 230 relevant shared-core tests passed; 32 optional-provider/environment cases
  were skipped.
- 38 focused Porn Fetch unit/Qt integration checks and four CLI offline checks.
- All 14 API/core source and wheel packages built successfully.
- All 11 providers with profile support enumerated a real listing and loaded
  HTML metadata for the first returned video, using the local fixed sources.
  [Post-fix observations](url-routing-audit/post-fix-online.json) record those
  bounded checks. No media files were downloaded.

Build artifacts and raw network responses remain outside Git. Version bumps and
Git pushes do not themselves publish packages to PyPI; distribution lockfiles
remain tied to their existing published artifacts until a package release.
