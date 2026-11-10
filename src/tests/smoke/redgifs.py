"""Opt-in RedGIFs routing, complete public listings and real RAW downloads.

Run: python -m src.tests.smoke.redgifs --report /tmp/redgifs-integration.json
Uses isolated download folders. No requests occur on import or unittest discovery.
"""

import argparse
import asyncio
import json
import subprocess
import tempfile
from pathlib import Path

from base_api.modules.config import RuntimeConfig

from src.cli.downloads import download_video
from src.cli.media import prepare_video
from src.cli.providers import ClientPool
from src.cli.settings import CliSettings
from src.shared.media import select_allowed_quality
from src.shared.provider_routing import ContentKind, container_stream, route_url, unwrap_scrape_result
from src.shared.redgifs import rendition_map


async def collect(stream):
    try:
        return [unwrap_scrape_result(x) async for x in stream]
    finally:
        await stream.aclose()


def probe(file):
    d = json.loads(
        subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(file)])
    )
    s = next(x for x in d["streams"] if x["codec_type"] == "video")
    return {
        "width": s["width"],
        "height": s["height"],
        "duration": float(d["format"]["duration"]),
        "bytes": file.stat().st_size,
        "audio": any(x["codec_type"] == "audio" for x in d["streams"]),
    }


async def run(report_path: Path):
    report = {"routes": [], "listings": [], "downloads": []}
    for url, kind in [
        ("https://redgifs.com/ifr/hotpinkacrobatickitfox", ContentKind.VIDEO),
        ("https://media.redgifs.com/HotpinkAcrobaticKitfox-mobile.mp4", ContentKind.VIDEO),
        ("https://www.redgifs.com/users/nickiipeach", ContentKind.PROFILE),
        ("https://www.redgifs.com/niches/duo-chastity", ContentKind.COLLECTION),
        ("https://www.redgifs.com/users/weirdjack/collections/d7ddef5fb0", ContentKind.COLLECTION),
    ]:
        r = route_url(url)
        assert r.kind == kind
        report["routes"].append({"url": url, "kind": str(kind)})
    for url in [
        "https://redgifs.com/search?query=test",
        "https://redgifs.com/users/weirdjack/collections",
        "https://media.redgifs.com/HotpinkAcrobaticKitfox-poster.jpg",
        "https://api.redgifs.com/v2/gifs/test",
        "https://redgifs.com.attacker.invalid/watch/test",
        "https://redgifs.com/users/weirdjack/images",
    ]:
        try:
            route_url(url)
        except ValueError:
            pass
        else:
            raise AssertionError(url)
    cfg = RuntimeConfig()
    cfg.request_delay = 2
    cfg.request_attempts = 2
    cfg.videos_concurrency = 1
    cfg.pages_concurrency = 1
    async with ClientPool(cfg) as pool:
        client = pool.client("redgifs")
        for url, path, key in [
            (
                "https://www.redgifs.com/users/nickiipeach",
                "v2/users/nickiipeach/search?count=40&order=new&type=g",
                "gifs",
            ),
            (
                "https://www.redgifs.com/niches/duo-chastity",
                "v2/niches/duo-chastity/gifs?count=40&order=new&type=g",
                "gifs",
            ),
            (
                "https://www.redgifs.com/users/weirdjack/collections/d7ddef5fb0",
                "v2/users/weirdjack/collections/d7ddef5fb0/gifs?count=40",
                "gifs",
            ),
        ]:
            route, target = await pool.resolve(url, pages=30)
            raw = await client._api.get(path + "&page=1")
            expected = []
            image_count = 0
            for page in range(1, raw["pages"] + 1):
                d = raw if page == 1 else await client._api.get(path + f"&page={page}")
                expected.extend(g["id"] for g in d[key] if g["type"] == 1)
                image_count += sum(g["type"] == 2 for g in d[key])
            videos = await collect(container_stream(target, pages=30, provider="redgifs"))
            assert [v.video_id for v in videos] == expected and expected
            assert len(expected) == len(set(expected))
            row = await prepare_video(videos[0], "redgifs")
            assert row.title and row.author and row.length and row.qualities
            result = {
                "url": url,
                "expected": len(expected),
                "actual": len(videos),
                "images_excluded": image_count,
                "first_qualities": row.qualities,
            }
            report["listings"].append(result)
            print("LISTING", result, flush=True)
        settings = CliSettings(
            skip_existing=False, write_metadata=False, download_workers=2, request_delay=2, request_attempts=2
        )
        with tempfile.TemporaryDirectory(prefix="pf-redgifs-check-") as directory:
            for video_id in ["hotpinkacrobatickitfox", "happyfrenchindianspinyloach"]:
                route, video = await pool.resolve("https://www.redgifs.com/watch/" + video_id)
                row = await prepare_video(video, "redgifs")
                mapping = await rendition_map(video)
                assert sorted(mapping) == row.qualities
                assert row.length == 1
                for q in row.qualities:
                    file = Path(directory) / f"{video_id}-{q}.mp4"
                    result = await download_video(
                        video, file, q, settings, has_premium=True, available_qualities=row.qualities
                    )
                    assert result.status == "completed"
                    info = probe(file)
                    assert min(info["width"], info["height"]) == q and abs(info["duration"] - video.duration) < 0.3
                    report["downloads"].append({"id": video_id, "quality": q, **info})
                    print("DOWNLOAD", report["downloads"][-1], flush=True)
                allowed = select_allowed_quality("best", row.qualities, False)
                assert int(allowed) <= 720
                file = Path(directory) / f"{video_id}-free.mp4"
                result = await download_video(video, file, "best", settings, has_premium=False)
                assert result.status == "completed"
                info = probe(file)
                assert min(info["width"], info["height"]) <= 720
                report["downloads"].append({"id": video_id, "quality": "free-best", **info})
        report_path.write_text(json.dumps(report, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=Path(tempfile.gettempdir()) / "redgifs-integration.json")
    args = parser.parse_args()
    asyncio.run(run(args.report))


if __name__ == "__main__":
    main()
