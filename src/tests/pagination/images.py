from .common import *
from .full import ObserveCore
from selectolax.lexbor import LexborHTMLParser
from urllib.parse import urljoin


async def main():
    out = []
    cfg = RuntimeConfig()
    cfg.request_attempts = 3
    async with ObserveCore(configuration=cfg) as core:
        for site, url in [
            ("xfreehd", "https://beta.xfreehd.com/album/14805/woman-boy-18-nudists"),
            ("pornhub", "https://www.pornhub.com/album/80426065"),
        ]:
            try:
                m = importlib.import_module(site + "_api.api")
                obj = m.Album(url=url, core=core)
                if site == "xfreehd":
                    await obj.load_sources("html")
                    last = obj.total_pages_count
                    expected = []
                    counts = []
                    for page in range(1, last + 1):
                        from base_api import update_url_query

                        text = await core.fetch_text(update_url_query(url, page=page))
                        p = LexborHTMLParser(text)
                        rows = [a.attributes["href"] for a in p.css("div.thumb-overlay.album-thumb a[href]")]
                        counts.append(len(rows))
                        expected += rows
                    expected = list(dict.fromkeys(expected))
                    actual = await obj.get_all_images()
                    assert expected and expected == actual, "album image listing mismatch"
                    assert await obj.get_images_by_page(last + 1) == [], "beyond-final images"
                    assert await obj.get_all_images(pages=1, start_page=last) == await obj.get_images_by_page(last), (
                        "image start offset"
                    )
                else:
                    # Photos retain their dictionary interface; independently enumerate links.
                    text = await core.fetch_text(url)
                    p = LexborHTMLParser(text)
                    expected = list(
                        dict.fromkeys(
                            urljoin(text.url, n.attributes["href"])
                            for n in p.css('ul.photosAlbumsListing li a[href*="/photo/"]')
                        )
                    )
                    core.received = []
                    core.record = True
                    async with aclosing(obj.get_photos(pages=1)) as stream:
                        actual = [d["url"] async for d in stream]
                    core.record = False
                    consumed = core.received[-1]
                    p = LexborHTMLParser(consumed)
                    expected = list(
                        dict.fromkeys(
                            urljoin(consumed.url, n.attributes["href"])
                            for n in p.css('ul.photosAlbumsListing li a[href*="/photo/"]')
                        )
                    )
                    assert expected and expected == actual, (
                        f"photo page mismatch expected={len(expected)} actual={len(actual)} first={expected[:2]} actual_first={actual[:2]}"
                    )
                    core.received = []
                    core.record = True
                    async with aclosing(obj.get_photos(pages="all")) as stream:
                        all_photos = [d["url"] async for d in stream]
                    core.record = False
                    complete = []
                    counts = []
                    for content in core.received:
                        tree = LexborHTMLParser(content)
                        rows = list(
                            dict.fromkeys(
                                urljoin(content.url, n.attributes["href"])
                                for n in tree.css('ul.photosAlbumsListing li a[href*="/photo/"]')
                            )
                        )
                        complete += rows
                        counts.append(len(rows))
                    assert complete == all_photos, "full album differs from its actual source pages"
                    assert not [
                        a
                        for a in tree.css(".pagination3 a, .pagination a")
                        if a.text(strip=True).lower() == "next" and a.attributes.get("href")
                    ], "album scan stopped before source next link"
                    expected = complete
                    actual = all_photos
                    async with aclosing(obj.get_photos(pages="all", start_page=len(counts) + 1)) as stream:
                        assert not [row async for row in stream], "beyond-final photo page returned entries"
                    last = len(counts)
                row = {
                    "provider": site,
                    "kind": "Album",
                    "status": "PASS",
                    "pages": last,
                    "page_counts": counts,
                    "expected": len(expected),
                    "actual": len(actual),
                }
            except Exception as e:
                row = {"provider": site, "kind": "Album", "status": "FAIL", "error": type(e).__name__ + ": " + str(e)}
            print(json.dumps(row), flush=True)
            out.append(row)
    (OUTPUT / "images.json").write_text(json.dumps(out, indent=2))
    if any(row["status"] != "PASS" for row in out):
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
