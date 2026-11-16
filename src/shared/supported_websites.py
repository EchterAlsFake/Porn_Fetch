"""Offline website catalog for the native overview, keyed by the shared router."""
from .provider_routing import COLLECTION_SEGMENTS, PROFILE_SEGMENTS, PROVIDER_MODULES

# Describe only entry points exposed by Porn Fetch, not the whole provider API.
WEBSITES = {
    "beeg": ("Beeg", "beeg.com", "Individual video links."),
    "bellesa": ("Bellesa", "bellesa.co", "Videos: /videos/<id>. Profiles: /channels/<handle> or /performers/<handle>."),
    "empflix": ("EMPFlix", "empflix.com", "Individual videos, pornstar pages and public profiles."),
    "eporner": ("Eporner", "eporner.com", "Individual videos, pornstar pages and channels."),
    "porn": ("Porn.com", "porn.com", "Videos: /scene/<id>. Channel, pornstar and collection links share /<slug>; use the matching input field."),
    "porndoe": ("Porndoe", "porndoe.com", "Videos: /watch/<id>. Profiles: /pornstars-profile/<slug> or /channel-profile/<slug>."),
    "pornhat": ("Pornhat", "pornhat.com", "Videos: /video/<slug>. Profiles: /models/<slug> or /sites/<slug>. Also accepts pornhat.one."),
    "pornhub": ("PornHub", "pornhub.com", "Individual videos and Shorts, model, pornstar, user and channel pages, and public playlists."),
    "porntrex": ("PornTrex", "porntrex.com", "Individual videos, model pages and channels."),
    "redgifs": ("RedGIFs", "redgifs.com", "Watch/embed and CDN MP4 links. Users go in Model URL; niches and public user collections go in Playlist/Collection URL. Still images are excluded."),
    "redtube": ("RedTube", "redtube.com", "Individual videos, pornstar, channel, amateur and user pages, and public playlists."),
    "spankbang": ("SpankBang", "spankbang.com", "Individual videos and pornstar, creator, profile or channel pages."),
    "thumbzilla": ("Thumbzilla", "thumbzilla.com", "Individual videos, pornstar, channel and amateur pages, and public playlists."),
    "tnaflix": ("TNAFlix", "tnaflix.com", "Individual videos, public profiles, pornstar pages and channels."),
    "tube8": ("Tube8", "tube8.com", "Individual videos and pornstar, channel, amateur or user pages. Also accepts tube8.fr and tube8.es."),
    "xfreehd": ("XFreeHD", "xfreehd.com", "Individual video links."),
    "xhamster": ("xHamster", "xhamster.com", "Individual videos and Moments, pornstar, creator, user and channel pages."),
    "xnxx": ("XNXX", "xnxx.com", "Individual videos and public user/profile links."),
    "xvideos": ("XVideos", "xvideos.com", "Individual videos, pornstar/model and channel pages, and public playlists. Quickies are not supported."),
    "youjizz": ("YouJizz", "youjizz.com", "Individual videos, public user uploads and verified pornstar links. Numbered popular, newest, top-rated, trending and HD lists use Playlist/Collection URL. General search is not supported."),
    "youporn": ("YouPorn", "youporn.com", "Individual videos, pornstar pages, channels and public video collections."),
}


def supported_websites() -> list[dict]:
    """Derive capability filters from the same registries used for routing."""
    return [
        {"id": key, "name": WEBSITES[key][0], "domain": WEBSITES[key][1],
         "details": WEBSITES[key][2], "profiles": key in PROFILE_SEGMENTS,
         "collections": key in COLLECTION_SEGMENTS}
        for key in sorted(PROVIDER_MODULES, key=lambda key: WEBSITES[key][0].casefold())
    ]
