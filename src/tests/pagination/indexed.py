import asyncio
import importlib
import json
from contextlib import aclosing

from base_api import BaseCore
from base_api.modules.config import RuntimeConfig

from .common import OUTPUT, ic


async def check_profile(site, url):
    cfg = RuntimeConfig()
    cfg.request_attempts = 3
    async with BaseCore(configuration=cfg) as core:
        m = importlib.import_module(site + "_api.api")
        obj = (m.User if site == "xnxx" else m.Channel)(url=url, core=core)
        base = (
            "https://www.xnxx.com/pornstar/cory-chase"
            if site == "xnxx"
            else "https://de.xvideos.com/channels/teddy_tarantino"
        )
        first = json.loads(await core.fetch_text(base + "/videos/best/0"))
        size = int(first["nb_per_page"])
        last = (int(first["nb_videos"]) + size - 1) // size
        for page in [1, 2, last, last + 1]:
            data = json.loads(await core.fetch_text(base + f"/videos/best/{page - 1}"))
            expected = [str(v["id"]) for v in data.get("videos", [])]
            async with aclosing(obj.videos(pages=1, start_page=page, iterator_config=ic)) as stream:
                actual = [str(r.unwrap().video_id) async for r in stream]
            # Compare source IDs by URL path; hosts/locales can be normalized by Video.
            want = expected
            got = actual
            assert got == want, f"page {page} mismatch expected {len(want)} actual {len(got)}"
        # Full JSON profile, independently enumerate all wire pages.
        expected = []
        for p in range(last):
            data = json.loads(await core.fetch_text(base + f"/videos/best/{p}"))
            expected += [str(v["id"]) for v in data["videos"]]
        async with aclosing(obj.videos(pages="all", iterator_config=ic)) as stream:
            actual = [str(r.unwrap().video_id) async for r in stream]
        assert expected == actual, "full JSON profile mismatch"
        return {
            "provider": site,
            "status": "PASS",
            "pages": last,
            "expected": len(expected),
            "actual": len(actual),
            "boundary_pages": [1, 2, last, last + 1],
            "ordered_match": True,
        }


async def check_bellesa():
    cfg = RuntimeConfig()
    cfg.request_attempts = 3
    async with BaseCore(configuration=cfg) as core:
        m = importlib.import_module("bellesa_api.api")
        obj = m.Channel(core=core, url="https://www.bellesa.co/channels/zero-to-hero")
        from urllib.parse import urlencode

        base = "https://www.bellesa.co/api/rest/v1/videos?" + urlencode(
            {
                "filter[source]": "bellesa",
                "filter[provider]": "or:zero-to-hero",
                "limit": 24,
                "order[publishedAt]": "DESC",
            }
        )
        expected = []
        counts = []
        for p in [1, 2, 3]:
            r = await core.request(base + "&page=" + str(p))
            rows = r.json()
            counts.append(len(rows))
            expected += [str(v["id"]) for v in rows]
        async with aclosing(obj.videos(pages="all", iterator_config=ic)) as stream:
            actual = [str(r.unwrap().video_id) async for r in stream]
        assert expected == actual, "Bellesa full listing mismatch"
        return {
            "provider": "bellesa",
            "status": "PASS",
            "source_pages": counts,
            "expected": len(expected),
            "actual": len(actual),
            "ordered_match": True,
        }


async def check_redgifs():
    cfg = RuntimeConfig()
    cfg.request_attempts = 3
    async with BaseCore(configuration=cfg) as core:
        m = importlib.import_module("redgifs_api.api")
        client = m.Client(core=core)
        obj = await client.get_collection("weirdjack", "d7ddef5fb0", load_api=False)
        # Observe raw listing via the transport without invoking the production extractor.
        orig = client._api.fetch_text
        responses = []

        async def observe(url, **kw):
            content = await orig(url, **kw)
            if "/collections/" in url and "page=" in url:
                responses.append(json.loads(content))
            return content

        client._api.fetch_text = observe
        async with aclosing(obj.items(pages="all", count=40, iterator_config=ic)) as stream:
            actual = [r.unwrap().video_id async for r in stream]
        by_page = {d["page"]: d for d in responses if "gifs" in d}
        expected = [g["id"].lower() for p in sorted(by_page) for g in by_page[p]["gifs"]]
        assert expected and expected == actual, "RedGIFs full mixed collection mismatch"
        last = max(by_page)
        async with aclosing(obj.items(pages="all", count=40, start_page=last + 1, iterator_config=ic)) as stream:
            assert not [r.unwrap() async for r in stream]
        return {
            "provider": "redgifs",
            "status": "PASS",
            "pages": last,
            "expected": len(expected),
            "actual": len(actual),
            "ordered_match": True,
        }


async def main():
    out = []
    for site, fn in [
        ("xvideos", lambda: check_profile("xvideos", "https://de.xvideos.com/teddy_tarantino")),
        ("xnxx", lambda: check_profile("xnxx", "https://www.xnxx.com/pornstar/cory-chase")),
        ("bellesa", check_bellesa),
        ("redgifs", check_redgifs),
    ]:
        try:
            row = await fn()
        except Exception as e:
            row = {"provider": site, "status": "FAIL", "error": type(e).__name__ + ": " + str(e)}
        print(json.dumps(row), flush=True)
        out.append(row)
    (OUTPUT / "indexed.json").write_text(json.dumps(out, indent=2))
    if any(row["status"] != "PASS" for row in out):
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
