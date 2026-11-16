"""Compare complete live streams with independently selected source listing IDs."""

import argparse
import asyncio
import importlib
import json
import re
from contextlib import aclosing
from urllib.parse import parse_qs, urljoin, urlsplit

from base_api import BaseCore
from base_api.modules.config import RuntimeConfig
from selectolax.lexbor import LexborHTMLParser

from .common import OUTPUT, cases, collect, config


def identity(site, url):
    parts = urlsplit(url)
    path = parts.path.rstrip("/")
    if site == "pornhub":
        return parse_qs(parts.query).get("viewkey", [path])[0]
    if site == "porn":
        match = re.search(r"/scene/(\d+)", path)
        return match[1] if match else path
    if site in {"xvideos", "xnxx"}:
        if path.startswith("/prof-video-click/"):
            return path.split("/")[-2]
        match = re.search(r"/video[.-]([^/]+)", path)
        return match[1] if match else path
    if site == "eporner":
        match = re.search(r"/(?:video-|hd-porn/)([^/]+)", path)
        return match[1] if match else path
    if site == "youjizz":
        match = re.search(r"/videos/[^/]*?(\d+)\.html", path)
        return match[1] if match else path
    return path


class SourceCore(BaseCore):
    async def fetch_text(self, url, **kwargs):
        text = await super().fetch_text(url, **kwargs)
        if self.source_site == "youjizz" and "/api/thumbs?" in url:
            self.thumbnail_batches = getattr(self, "thumbnail_batches", 0) + 1
        try:
            observed = source_rows(self.source_site, url, text)
            if observed is not None:
                urls, key = observed
                self.source_pages[key] = (url, None, urls)
                self.last_source = (url, text)
                if len(self.source_pages) % 20 == 0:
                    print(
                        json.dumps({"provider": self.source_site, "progress_pages": len(self.source_pages)}), flush=True
                    )
        except Exception as error:
            self.observer_errors.append(type(error).__name__ + ": " + str(error))
        return text


def source_rows(site, requested, content):
    """No production extractors are called here."""
    value = str(content).lstrip()
    base = getattr(content, "url", None) or requested
    if value.startswith(("{", "[")):
        data = json.loads(content)
        if site in {"xvideos", "xnxx"} and isinstance(data, dict) and "videos" in data:
            return [
                urljoin(
                    base,
                    "/video-" + row["eid"] + "/"
                    if site == "xnxx" and row["u"].startswith("/prof-video-click/")
                    else row["u"],
                )
                for row in data["videos"]
            ], data["current_page"]
        if site == "bellesa" and isinstance(data, list):
            return ["https://www.bellesa.co/videos/" + str(row["id"]) for row in data], int(
                content.headers["x-pagination-page"]
            )
        if site == "redgifs" and isinstance(data, dict) and "gifs" in data:
            return ["https://www.redgifs.com/watch/" + row["id"].lower() for row in data["gifs"]], data["page"]
        if site == "youjizz" and isinstance(data, list) and data and all(isinstance(row, (int, str)) for row in data):
            return ["https://www.youjizz.com/videos/video-" + str(row) + ".html" for row in data], 0
        return None
    tree = LexborHTMLParser(content)
    if site == "xhamster":
        script = tree.css_first("#initials-script")
        if script and "window.initials=" in script.text():
            data = json.loads(script.text().split("window.initials=", 1)[1].strip().rstrip(";"))
            lists = []
            for candidate in [
                data.get("searchResult"),
                data.get("layoutPage", {}).get("videoListProps"),
                data.get("pagesCategoryComponent", {}).get("trendingVideoListProps"),
                data.get("trendingVideoSectionComponent"),
                data.get("newestVideoSectionComponent"),
                data.get("videoListProps"),
            ]:
                if isinstance(candidate, dict):
                    candidate = candidate.get("videoListProps", candidate)
                    if isinstance(candidate.get("videoThumbProps"), list):
                        lists.extend(candidate["videoThumbProps"])
            rows = [
                urljoin(base, row["pageURL"])
                for row in lists
                if isinstance(row, dict)
                and row.get("pageURL")
                and "/shorts/" not in row["pageURL"]
                and "/moments/" not in row["pageURL"]
                and row.get("videoType") != "moment"
            ]
            return list(dict.fromkeys(rows)), requested
    if site == "pornhub":
        if "/videos" not in urlsplit(base).path and "/playlist/viewChunked" not in urlsplit(base).path:
            return None  # Profile identity preflight is not a listing page.
        root = (
            tree.css_first("#mostRecentVideosSection")
            or tree.css_first("div.profileVids")
            or tree.css_first("#videoSearchResult")
            or tree.css_first("#moreData")
        )
        if root is None:
            for unrelated in tree.css(
                "header, #header, .headerSubMenu, #hottestMenuSection, .feedRight, #bottomVideos"
            ):
                unrelated.decompose()
            root = tree
        anchors = [card.css_first('a[href*="view_video"]') for card in root.css("li.pcVideoListItem, li.videoBox")]
        anchors = [anchor for anchor in anchors if anchor is not None]
    elif site == "eporner":
        anchors = tree.css("#vidresults div.mb p.mbtit a[href]")
    elif site in {"empflix", "tnaflix"}:
        anchors = tree.css("div[data-vid] a.video-thumb[href], div[data-vid] a.thumb[href]")
    elif site == "porntrex":
        block = parse_qs(urlsplit(requested).query).get("block_id", [None])[0]
        root = tree.css_first("#" + block) if block else None
        if root is None:
            raise AssertionError("Independent observer did not find the intended KVS block")
        anchors = root.css("div.video-preview-screen.video-item.thumb-item a.thumb[href]")
    elif site == "redtube":
        root = tree.css_first("ul#playlist_videos, ul.videos_grid")
        anchors = root.css("li[data-video-id] a.video_link[href]") if root else []
    elif site in {"thumbzilla", "tube8", "youporn"}:
        root = tree.css_first("div.full-row-thumbs, div.three-thumbs-row")
        anchors = root.css("article.video-box.pc.js_video-box.js-pop a.video-box-image[href]") if root else []
    elif site == "porndoe":
        anchors = tree.css(".video-item .video-item-link[href]")
    elif site == "pornhat":
        anchors = tree.css('#custom_list_videos_common_videos_list_items .thumb-video > a[href*="/video/"]')
    elif site == "porn":
        rows = [
            "https://www.porn.com/scene/" + n.attributes["data-itemid"]
            for n in tree.css("main .list-videos > .list-global__item[data-itemid]")
        ]
        return rows, requested
    elif site == "youjizz":
        if "/api/" in urlsplit(requested).path:
            return None
        anchors = tree.css("a.frame[data-video-id]:not(.related-thumb)")
    elif site == "spankbang":
        roots = tree.css('div[x-data="videoList"]')
        if roots:
            root = max(roots, key=lambda node: len(node.css('div.js-video-item, div[data-testid="video-item"]')))
        else:
            root = tree
        anchors = root.css('div.js-video-item a[href*="/video/"], div[data-testid="video-item"] a[href*="/video/"]')
    else:
        raise AssertionError("No independent source observer for " + site)
    return list(dict.fromkeys(urljoin(base, n.attributes["href"]) for n in anchors)), requested


def verify_terminal(site, url, content, profile_url):
    value = str(content).lstrip()
    if value.startswith(("{", "[")):
        data = json.loads(content)
        if site in {"xvideos", "xnxx"}:
            assert data["current_page"] + 1 >= (data["nb_videos"] + data["nb_per_page"] - 1) // data["nb_per_page"], (
                "Stopped before JSON final page"
            )
        elif site == "bellesa":
            assert int(content.headers["x-pagination-page"]) >= int(content.headers["x-pagination-pages-total"]), (
                "Stopped before header final page"
            )
        elif site == "redgifs":
            assert data["page"] >= data["pages"], "Stopped before API final page"
        return
    tree = LexborHTMLParser(content)
    if site == "pornhub" and "/playlist/viewChunked" in urlsplit(url).path:
        assert not tree.css("li.pcVideoListItem, li.videoBox"), "Playlist chunk did not reach an empty source response"
        return
    base = getattr(content, "url", None) or url
    prefix = urlsplit(profile_url).path.rstrip("/")
    if site == "pornhub":
        prefix = "/" + "/".join(urlsplit(base).path.strip("/").split("/")[:2])
        button = tree.css_first("#moreDataBtn[onclick]")
        if button:
            match = re.search(r"loadMoreData\(\s*(['\"])(.*?)\1\s*,\s*['\"]?(\d+)", button.attributes["onclick"])
            if match and urlsplit(match[2]).path.startswith(urlsplit(base).path.rstrip("/")):
                assert int(parse_qs(urlsplit(base).query).get("page", [1])[0]) >= int(match[3]), (
                    "Stopped before load-more final page"
                )
    if site == "porntrex":
        current = int(parse_qs(urlsplit(url).query)["from"][0])
        block = parse_qs(urlsplit(url).query)["block_id"][0]
        root = tree.css_first("#" + block)
        for node in root.css("[data-parameters]"):
            match = re.search(r"(?:^|;)from:(\d+)(?:;|$)", node.attributes["data-parameters"])
            assert not match or int(match[1]) <= current, "Stopped before KVS final page"
        return
    for anchor in tree.css("a[href]"):
        href = anchor.attributes["href"]
        if not href or href.startswith(("#", "javascript:")):
            continue
        target = urljoin(base, href)
        if not urlsplit(target).path.startswith(prefix):
            continue
        text = anchor.text(strip=True).casefold()
        classes = anchor.attributes.get("class", "").casefold()
        marked = anchor.attributes.get("rel") == "next" or any(
            token in {"next", "next-page", "next_page", "nmnext", "pagination-next"}
            or token.endswith(("--next", "-next", "_next"))
            for token in classes.split()
        )
        assert not (text in {"next", "next page", "weiter", "nächste", "›", "»", ">>"} or marked), (
            "Source still exposes a next page: " + site
        )


async def check(case, *, boundaries=False):
    site, cls, url, method = case
    settings = RuntimeConfig()
    settings.request_attempts = 3
    settings.request_delay = 0.25
    async with SourceCore(configuration=settings) as core:
        core.source_site = site
        core.source_pages = {}
        core.observer_errors = []
        core.last_source = None
        module = importlib.import_module(site + "_api.api")
        kwargs = {"name": "Abby Marie"} if site == "youjizz" and cls == "Pornstar" else {}
        obj = getattr(module, cls)(core=core, url=url, **kwargs)
        stream = getattr(obj, method)(pages="all", start_page=1, iterator_config=config)
        async with aclosing(stream):
            actual = [identity(site, result.unwrap().url) async for result in stream]
        assert not core.observer_errors, "Independent observer failed: " + str(core.observer_errors)
        source_pages = core.source_pages
        expected = [identity(site, u) for _, _, urls in source_pages.values() for u in urls]
        assert expected and actual, "Known fixture did not expose a nonempty listing"
        if actual != expected:
            if core.last_source:
                (OUTPUT / (site + "-mismatch.html")).write_text(str(core.last_source[1]))
            (OUTPUT / (site + "-identity-difference.json")).write_text(
                json.dumps(
                    {
                        "actual": actual,
                        "expected": expected,
                        "pages": {str(k): [identity(site, v) for v in row[2]] for k, row in source_pages.items()},
                    },
                    indent=2,
                )
            )
        assert actual == expected, (
            f"Independent source mismatch expected={len(expected)} actual={len(actual)} missing={len(set(expected) - set(actual))} unexpected={len(set(actual) - set(expected))}"
        )
        last_url, last_content = core.last_source
        try:
            verify_terminal(site, last_url, last_content, url)
        except AssertionError:
            (OUTPUT / (site + "-terminal.html")).write_text(str(last_content))
            raise
        if getattr(stream, "summary", None):
            assert stream.summary.exhausted, "Stream did not confirm exhaustion"
        source_page_count = len(source_pages)
        thumbnail_batches = getattr(core, "thumbnail_batches", None)
        boundary_result = {}
        if boundaries:
            ordered_pages = list(source_pages.values())
            if site == "youjizz" and cls == "User":
                last_page = (len(expected) + 23) // 24
                expected_tail = expected[(last_page - 1) * 24 :]
            else:
                last_page = max(index + 1 for index, (_, _, urls) in enumerate(ordered_pages) if urls)
                expected_tail = [identity(site, u) for u in ordered_pages[last_page - 1][2]]
            tail = await collect(getattr(obj, method)(pages=1, start_page=last_page, iterator_config=config))
            assert [identity(site, u) for u in tail] == expected_tail, "Last-page offset differs from the source"
            beyond_behavior = "empty"
            try:
                beyond = await collect(getattr(obj, method)(pages=1, start_page=last_page + 1, iterator_config=config))
                assert not beyond, "Beyond-last request returned unrelated/repeated items"
            except Exception as error:
                from base_api.modules.pagination import http_status_is

                if not http_status_is(error, 404):
                    raise
                beyond_behavior = "visible_http_404"
            boundary_result = {
                "last_nonempty_page": last_page,
                "last_page_items": len(tail),
                "beyond_page": last_page + 1,
                "beyond_behavior": beyond_behavior,
            }
        return {
            "provider": site,
            "kind": cls,
            "method": method,
            "status": "PASS",
            "source_pages": source_page_count,
            "expected": len(expected),
            "actual": len(actual),
            "unique_items": len(set(actual)),
            "source_duplicate_items": len(expected) - len(set(expected)),
            **({"thumbnail_batches": thumbnail_batches} if site == "youjizz" and cls == "User" else {}),
            "ordered_match": True,
            "terminal_verified": True,
            **boundary_result,
        }


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", action="append")
    parser.add_argument("--extra", action="store_true")
    parser.add_argument("--kind", action="append")
    parser.add_argument("--method", action="append")
    parser.add_argument("--boundaries", action="store_true")
    args = parser.parse_args()
    if args.extra:
        from .extra_cases import extras

        cases[:] = [case for case in extras if case[3] in {"videos", "get_videos", "get_uploads"}]
    selected = [case for case in cases if not args.provider or case[0] in args.provider]
    selected = [case for case in selected if not args.kind or case[1] in args.kind]
    selected = [case for case in selected if not args.method or case[3] in args.method]
    # Keep separate evidence of the large-channel 100-page upstream cap.
    selected = [
        (
            site,
            cls,
            "https://www.thumbzilla.com/channel/letsdoeit-bonus/"
            if site == "thumbzilla" and cls == "Channel"
            else "https://www.tube8.com/channel/aunt-judys-xxx/"
            if site == "tube8" and cls == "Channel"
            else url,
            method,
        )
        for site, cls, url, method in selected
    ]
    sem = asyncio.Semaphore(2)
    out = []

    async def one(case):
        async with sem:
            try:
                row = await check(case, boundaries=args.boundaries)
            except Exception as error:
                row = {
                    "provider": case[0],
                    "kind": case[1],
                    "status": "FAIL",
                    "error": type(error).__name__ + ": " + str(error),
                }
            print(json.dumps(row), flush=True)
            out.append(row)
            (OUTPUT / "complete-profiles.json").write_text(json.dumps(out, indent=2))

    await asyncio.gather(*(one(case) for case in selected))
    if any(row["status"] != "PASS" for row in out):
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
