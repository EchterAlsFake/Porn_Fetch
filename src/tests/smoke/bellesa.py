"""Opt-in Bellesa Video/Channel/Performer integration with real requests.

Run: python -m src.tests.smoke.bellesa --report /tmp/bellesa-integration.json
Downloads complete media into temporary folders; never runs during test discovery.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from urllib.parse import urlencode

from base_api.modules.config import RuntimeConfig

from src.cli.downloads import DownloadController, download_video
from src.cli.media import prepare_video
from src.cli.providers import ClientPool
from src.cli.settings import CliSettings
from src.shared.access import public_collection_items
from src.shared.media import select_allowed_quality
from src.shared.provider_routing import route_url


async def collect(stream):
    try:
        return [item async for item in stream]
    finally:
        await stream.aclose()


def probe(path):
    result = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path),
    ]))
    video = next(stream for stream in result["streams"] if stream["codec_type"] == "video")
    return {"width": video["width"], "height": video["height"],
            "duration": float(result["format"]["duration"]), "bytes": path.stat().st_size,
            "audio": any(stream["codec_type"] == "audio" for stream in result["streams"]),
            "tags": result["format"].get("tags", {})}


async def rendered_listing(core, path, query, page):
    text = await core.fetch_text("https://www.bellesa.co" + path + "?" + urlencode({**query, "page": page}))
    match = re.search(r"window\.__INITIAL_DATA__\s*=\s*(.*?);</script>", text, re.S)
    assert match, path
    state = json.loads(match[1])
    assert state["pagination"]["page"] == page
    return state


async def run(report_path, *, downloads=True):
    from bellesa_api import Channel, Performer, Video

    report = {"package": version("unofficial-api-for-bellesa"), "started_at_utc": datetime.now(timezone.utc).isoformat(),
              "routes": [], "profiles": [], "downloads": [], "profile_http": []}
    runtime = RuntimeConfig()
    runtime.request_attempts = 2
    runtime.timeout = 25
    runtime.pages_concurrency = 1
    runtime.videos_concurrency = 2
    runtime.max_workers_download = 3
    settings = CliSettings(skip_existing=False, write_metadata=True, download_workers=3, request_attempts=2)
    async with ClientPool(runtime) as pool:
        for host in ("bellesa.co", "www.bellesa.co"):
            for path, expected in (("videos/7054", Video), ("channels/zero-to-hero", Channel),
                                   ("performers/lily-starfire", Performer)):
                url = f"https://{host}/{path}"
                route, target = await pool.resolve(url)
                assert route.provider == "bellesa" and isinstance(target, expected)
                assert target.url.startswith(f"https://{host}/")
                if isinstance(target, Video):
                    row = await prepare_video(target, route.provider)
                    assert row.title == "Aiden Ashley's House Party" and row.length == 1
                    assert row.author == target.author and row.thumbnail_url and row.publish_date
                    assert row.qualities == [360, 450, 720, 1080, 1440, 2160]
                    assert target.loaded_sources == frozenset({"api", "media"})
                else:
                    assert target.name and target.profile_id
                    response = await target.core.request(url)
                    assert response.status_code == 200
                    report["profile_http"].append({"url": url, "status": response.status_code,
                                                   "final_url": str(response.url),
                                                   "content_type": response.headers.get("content-type")})
                report["routes"].append({"url": url, "class": type(target).__name__})
                report_path.write_text(json.dumps(report, indent=2) + "\n")
        for url in (
            "https://www.bellesa.co/", "https://www.bellesa.co/videos", "https://www.bellesa.co/channels",
            "https://www.bellesa.co/performers", "https://www.bellesa.co/videos/categories/sensual",
            "https://www.bellesa.co/search?q=romance", "https://www.bellesa.co/story/all",
            "https://www.bellesa.co/channels/zero-to-hero/videos", "https://de.bellesa.co/videos/7054",
            "https://bellesa.co.attacker.invalid/videos/7054", "https://www.bellesa.co:444/videos/7054",
            "https://user:password@www.bellesa.co/videos/7054",
        ):
            try:
                route_url(url)
            except ValueError:
                continue
            raise AssertionError(f"Unsupported route accepted: {url}")
        client = pool.client("bellesa")
        assert client.core is pool.cores["bellesa"] and client.core.configuration is runtime
        for kind, handle, expected_count in (("performers", "lily-starfire", 3),
                                             ("performers", "kenna-james", 57),
                                             ("channels", "belle-says", 4),
                                             ("channels", "zero-to-hero", 30),
                                             ("channels", "erikalust", 24)):
            url = f"https://www.bellesa.co/{kind}/{handle}"
            path = f"/performers/{handle}" if kind == "performers" else "/videos"
            query = {"sort": "recent"}
            if kind == "channels":
                query["providers"] = handle
            first = await rendered_listing(client.core, path, query, 1)
            expected = [str(video["id"]) for video in first["videos"]]
            pages = first["pagination"]["pages"]
            for page in range(2, pages + 1):
                state = await rendered_listing(client.core, path, query, page)
                expected.extend(str(video["id"]) for video in state["videos"])
            assert len(expected) == len(set(expected)) == first["pagination"]["total"] == expected_count
            videos = await collect(pool.media_stream(url, pages=pages))
            assert [video.video_id for video in videos] == expected
            _, profile = await pool.resolve(url)
            stream = profile.videos(pages=1, start_page=pages + 1)
            async with stream:
                assert [result.unwrap() async for result in stream] == []
            preview = await collect(public_collection_items(pool.media_stream(url, pages=pages), False))
            assert [video.video_id for video in preview] == expected[:5]
            report["profiles"].append({"kind": kind, "handle": handle, "expected": len(expected),
                                       "actual": len(videos), "pages": pages, "free_preview": len(preview)})
            report_path.write_text(json.dumps(report, indent=2) + "\n")
            print("PROFILE", report["profiles"][-1], flush=True)
        _, video = await pool.resolve("https://www.bellesa.co/videos/7054")
        row = await prepare_video(video, "bellesa")
        _, older = await pool.resolve("https://www.bellesa.co/videos/1094")
        older_row = await prepare_video(older, "bellesa")
        assert older_row.length == 10 and older_row.qualities == [480, 600, 960]
        assert select_allowed_quality("best", older_row.qualities, False) == "600"
        if downloads:
            with tempfile.TemporaryDirectory(prefix="porn-fetch-bellesa-") as directory:
                for source, metadata, request, premium in [
                    *[(video, row, quality, True) for quality in row.qualities],
                    (video, row, "best", False), (older, older_row, "best", False),
                ]:
                    selected = int(select_allowed_quality(request, metadata.qualities, premium))
                    target = Path(directory) / f"{source.video_id}-{request}-{premium}.mp4"
                    progress = []
                    outcome = await download_video(
                        source, target, request, settings, has_premium=premium,
                        available_qualities=metadata.qualities, metadata=metadata,
                        controller=DownloadController(
                            url=source.url, target=target, provider="bellesa",
                            state_directory=Path(directory) / "state",
                        ),
                        progress=lambda *value: progress.append(value),
                    )
                    assert outcome.status == "completed" and not outcome.missing_segments
                    info = await asyncio.to_thread(probe, target)
                    assert min(info["width"], info["height"]) == selected
                    assert info["audio"] and abs(info["duration"] - source.duration) <= max(3, source.duration * 0.02)
                    assert progress and info["bytes"] > 10000
                    assert info["tags"].get("title") == metadata.title
                    assert info["tags"].get("artist") == metadata.author
                    if not premium:
                        assert selected <= 720
                    report["downloads"].append({"video_id": source.video_id, "request": request,
                                                "premium": premium, "quality": selected, **info})
                    report_path.write_text(json.dumps(report, indent=2) + "\n")
                    print("DOWNLOAD", {k: v for k, v in report["downloads"][-1].items() if k != "tags"}, flush=True)
        report["metadata_only"] = not downloads
        report_path.write_text(json.dumps(report, indent=2) + "\n")
    assert pool.clients == {} and pool.cores == {}
    print("PASS Bellesa integration. Report:", report_path, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=Path(tempfile.gettempdir()) / "bellesa-integration.json")
    parser.add_argument("--metadata-only", action="store_true", help="Check live routes and listings without media downloads")
    args = parser.parse_args()
    asyncio.run(run(args.report, downloads=not args.metadata_only))


if __name__ == "__main__":
    main()
