# Supported websites

For Porn Fetch 3.9 (desktop, Android, and CLI).

**Yes** = supported · **—** = unavailable.

| Website | Videos | Profiles/channels | Playlists/collections | Shorts | Search | Login | Photo albums |
|:--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| PornHub | Yes | Yes | Yes | Yes | — | Yes | CLI only |
| Eporner | Yes | Yes | — | — | — | — | — |
| XNXX | Yes | Yes | — | — | — | — | — |
| XVideos | Yes | Yes | Yes | — | — | Yes | — |
| XHamster | Yes | Yes | Account only | Yes | — | Yes | — |
| SpankBang | Yes | Yes | — | — | — | — | — |
| YouJizz | Yes | Pornstar, User | Collection | — | — | — | — |
| YouPorn | Yes | Yes | Yes | — | — | — | — |
| Beeg | Yes | — | — | — | — | — | — |
| Bellesa | Yes | Channel, Performer | — | — | — | — | — |
| Porn.com | Native scenes | Channel, Pornstar | Collection | — | — | — | — |
| Porntrex | Yes | Yes | — | — | — | — | — |
| XFreeHD | Yes | — | — | — | — | — | CLI only |
| RedTube | Yes | Yes | Yes | — | — | — | — |
| Thumbzilla | Yes | Yes | Yes | — | — | — | — |
| Tube8 | Yes | Yes | — | — | — | — | — |
| EMPFlix | Yes | Yes | — | — | — | — | — |
| TNAFlix | Yes | Yes | — | — | — | — | — |
| Pornhat | Yes | Yes | — | — | — | — | — |
| Porndoe | Yes | Yes | — | — | — | — | — |


> [!CAUTION]
> Searching is intentionally not supported since v3.9 due to legal reasons 


Paste the website's full video, profile, or playlist URL.
Supported profile types vary by website. Photo albums are CLI-only.
Keyword search is unavailable for legal reasons.

Porndoe accepts `/watch/<id>`, `/pornstars-profile/<name>`, and
`/channel-profile/<name>` URLs, including localized Porndoe subdomains.
Use the Video URL field for a video and the Model URL field for a pornstar or
channel. The CLI also accepts a Porndoe pornstar slug (such as `eva-elfie`) in
the profile workflow.
Downloads use the available MP4 qualities with the usual queue, filters,
pause/resume, output naming and metadata options. Porndoe does not expose
separate model or playlist objects. Categories, directories and related-video
browsing are outside this integration.

Pornhat supports only `/video/<slug>/` videos, `/models/<slug>/` models and
`/sites/<slug>/` channels. Use the Video URL field for videos and the Model URL
field for either profile type. The CLI profile flow also accepts a model slug.
Accepted hosts are `pornhat.com`, `www.pornhat.com`, `pornhat.one`,
`www.pornhat.one` and `de`, `fr`, `it`, `es`, `pt`, `hi` under `pornhat.com`.
Downloads resolve the provider's lazy HLS sources and use the existing quality,
queue, output, metadata and stop/resume controls. Categories/tags, paysite
collections, search, directories, playlists and account methods are not exposed.

Bellesa supports `/videos/<id>` (with an optional title slug),
`/channels/<handle>`, and `/performers/<handle>` on `bellesa.co` and
`www.bellesa.co`. Use Video URL for videos and Model URL for channels or
performers. The CLI profile flow accepts a performer handle; paste a full URL
for a channel. Only these three object types are integrated.

Bellesa uses the existing HLS download, quality, metadata, output and stop/resume
controls. Displayed qualities are actual rendition dimensions: a site label of
480 commonly means 450p, and older 4:3 videos can expose 480p, 600p and 960p.
The usual free 720p limit and five-video public profile preview apply.
See [Bellesa integration](BELLESA.md) for scope and live verification.

Availability and quality depend on the video, your region, and any required website
account. Free downloads are limited to 720p; higher qualities require a Porn Fetch
license. Some YouPorn MP4-only videos also require a license because their
resolution is unknown.

HQporner, MissAV, and unlisted websites are not supported.

Porn.com accepts native `/scene/<id>[/<slug>]` videos and individual collection,
channel and pornstar URLs such as `/yoga-porn`, `/brazzers` and `/mia-khalifa`.
Use Video URL for scenes, Model URL for channels/pornstars, and Playlist/Collection
URL for generic collections. The CLI resolves the actual page type automatically.
Referrals to other websites are excluded before the five-video free preview.
Only Video, Collection, Channel and Pornstar are integrated; source indexes,
directories, keyword search and other provider interfaces are not exposed.
See [Porn.com integration](PORN.md).

YouJizz supports Video, Collection, Pornstar and User only on `youjizz.com` and
`www.youjizz.com`. Video URLs include `/videos/<slug>-<id>.html` and
`/videos/embed/<id>`; numbered popular/newest/top/trending/HD lists use the
Playlist/Collection URL flow. Pornstar directory links use `/search/<name>-1.html`
and are validated against the actual directory before the Model URL flow loads
them. Public users use `/profile/user/<id>[/videos]`. General keyword searches,
category/tag routes, random lists, directories and account methods are excluded.
HLS downloads use actual measured quality tiers, including older 288p/368p
renditions, with the existing free preview, quality limits and stop/resume flow.
See [YouJizz integration](YOUJIZZ.md) for route examples and live evidence.
