"""Public model/playlist E2E inventory; importing it never starts Qt or HTTP."""
import json
from pathlib import Path

from src.shared.provider_routing import COLLECTION_SEGMENTS, PROFILE_SEGMENTS, route_url


def collection_cases(overrides=None):
    path = Path(__file__).resolve().parents[2] / "docs/url-routing-audit/profile-fixtures.json"
    profiles = {}
    for fixture in json.loads(path.read_text())["cases"]:
        if fixture["tier"] == "primary" and fixture["positive_smoke_candidate"]:
            profiles.setdefault(fixture["provider"], fixture["url"])
    # The former Cory Chase fixture's native profile endpoint returns HTTP 500.
    profiles["xnxx"] = "https://www.xnxx.com/pornstar/alex_adams69"
    playlists = {
        "pornhub": "https://www.pornhub.com/playlist/119820351",
        "xvideos": "https://de.xvideos.com/favorite/89127817/playlist_3",
        "youporn": "https://www.youporn.com/collections/videos/38771091/",
        "redtube": "https://www.redtube.com/playlist/4237321",
        "thumbzilla": None,
    }
    for key, url in (overrides or {}).items():
        targets = {"model": profiles, "playlist": playlists}
        provider, separator, kind = key.partition(".")
        if not separator or kind not in targets or provider not in targets[kind]:
            raise ValueError(f"Unknown source {key!r}; use a supported PROVIDER.model or PROVIDER.playlist")
        target = targets[kind]
        route = route_url(url)
        if route.provider != provider or route.kind.value != ("profile" if kind == "model" else "collection"):
            raise ValueError(f"Source URL does not match {key}")
        target[provider] = url
    assert set(profiles) == set(PROFILE_SEGMENTS), "Model provider inventory is incomplete"
    assert set(playlists) == set(COLLECTION_SEGMENTS), "Playlist provider inventory is incomplete"
    cases = []
    for kind, urls in (("model", profiles), ("playlist", playlists)):
        for provider, url in urls.items():
            state, reason = "AUTOMATED", ""
            if provider == "spankbang":
                state, reason = "MANUAL", "Website/CDN remains manual; no automated requests"
            elif url is None:
                state, reason = "UNVERIFIED", "No public playlist fixture found or supplied; library route is not claimed verified"
            if url is not None:
                route = route_url(url)
                assert route.provider == provider and route.kind.value == ("profile" if kind == "model" else "collection")
            cases.append({"id": f"{provider}.{kind}", "provider": provider, "kind": kind,
                          "url": url, "status": state, "reason": reason})
    return cases
