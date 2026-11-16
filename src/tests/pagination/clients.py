import asyncio
import importlib
import json

from base_api.modules.config import RuntimeConfig

from .common import OUTPUT, ObservedCore, collect, config

client_cases = [
    ("bellesa", "get_videos", [], {}),
    ("bellesa", "get_performers", [], {}),
    ("bellesa", "search", ["lily"], {"kind": "performer"}),
    ("bellesa", "search", ["massage"], {"kind": "channel"}),
    ("porndoe", "get_videos", [], {}),
    ("porndoe", "get_pornstars", [], {}),
    ("porndoe", "get_channels", [], {}),
    ("pornhat", "get_videos", [], {}),
    ("pornhat", "get_models", [], {}),
    ("pornhat", "get_channels", [], {}),
    ("porn", "pornstars", [], {}),
    ("porn", "channels", [], {}),
    ("redgifs", "search_images", ["massage"], {}),
    ("redgifs", "search_users", ["massage"], {}),
    ("redgifs", "get_niches", [], {}),
    ("youjizz", "videos", [], {}),
    ("xvideos", "get_playlist", ["https://de.xvideos.com/favorite/89127817/playlist_3"], {}),
    ("eporner", "get_videos_by_category", ["japanese"], {}),
    ("pornhub", "search_gifs", ["massage"], {}),
    ("pornhub", "search_hubtraffic", ["massage"], {"sort_by": "newest"}),
]


async def check(case):
    site, method, args, kw = case
    cfg = RuntimeConfig()
    cfg.request_attempts = 3
    async with ObservedCore(configuration=cfg) as core:
        m = importlib.import_module(site + "_api.api")
        c = m.Client(core=core)
        fn = getattr(c, method)
        a = await collect(fn(*args, **kw, pages=1, start_page=1, iterator_config=config))
        first_end = len(core.observed)
        b = await collect(fn(*args, **kw, pages=1, start_page=2, iterator_config=config))
        second_end = len(core.observed)
        ab = await collect(fn(*args, **kw, pages=2, start_page=1, iterator_config=config))
        assert a, "EMPTY_UNVERIFIED: selected listing has no entries"
        if site == "pornhub" and method == "search_hubtraffic":
            from urllib.parse import parse_qs, urlsplit

            def source_rows(responses, start):
                rows = []
                for requested, _, content in responses:
                    if int(parse_qs(urlsplit(requested).query).get("page", [1])[0]) < start:
                        continue  # Validated first-page preflight for an offset.
                    data = json.loads(content)
                    rows.extend(row["url"].rstrip("/") for row in data["videos"])
                return rows

            assert a == source_rows(core.observed[:first_end], 1)
            assert b == source_rows(core.observed[first_end:second_end], 2)
            assert ab == source_rows(core.observed[second_end:], 1), "HubTraffic differs from its live source pages"
        else:
            assert a + b == ab, f"page slicing mismatch {len(a)}/{len(b)}/{len(ab)}"
        assert not b or a != b, "repeated page"
        return {
            "provider": site,
            "method": method,
            "options": kw,
            "status": "PASS",
            "counts": [len(a), len(b), len(ab)],
            "independent_same_response_match": site == "pornhub" and method == "search_hubtraffic",
        }


async def main():
    out = []
    sem = asyncio.Semaphore(2)

    async def one(case):
        async with sem:
            try:
                row = await asyncio.wait_for(check(case), 180)
            except Exception as e:
                row = {
                    "provider": case[0],
                    "method": case[1],
                    "options": case[3],
                    "status": "FAIL",
                    "error": type(e).__name__ + ": " + str(e),
                }
            out.append(row)
            print(json.dumps(row), flush=True)

    await asyncio.gather(*(one(c) for c in client_cases))
    (OUTPUT / "clients.json").write_text(json.dumps(out, indent=2))
    if any(row["status"] != "PASS" for row in out):
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
