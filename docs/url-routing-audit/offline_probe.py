"""Capture provider URL behavior offline; requests and scraping are replaced with mocks.

Run with the project's virtualenv. API checkouts default to sibling directories.
Synthetic URLs probe construction only; they are not live media fixtures.
"""

import argparse
import asyncio
import hashlib
import importlib
import importlib.util
import json
import logging
import subprocess
import sys
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

PROJECT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--api-root", type=Path, default=PROJECT.parent)
parser.add_argument("--output", type=Path, default=Path(__file__).with_name("offline.json"))
args = parser.parse_args()
sys.path.insert(0, str(PROJECT))
sys.path.insert(0, str(args.api_root / "eaf_base_api"))
from base_api import BaseCore  # noqa: E402
from base_api.modules.config import RuntimeConfig  # noqa: E402

from src.shared.provider_routing import PROVIDER_MODULES, resolve_container, route_url  # noqa: E402

logging.disable(logging.CRITICAL)
installed = {name: Path(importlib.util.find_spec(module).origin).parent for name, module in PROVIDER_MODULES.items()}
roots = {name: args.api_root / f"unofficial-api-for-{name}" for name in PROVIDER_MODULES}
for root in roots.values():
    sys.path.insert(0, str(root))
modules = {
    name: importlib.import_module(module + (".beeg_api" if name == "beeg" else ".api"))
    for name, module in PROVIDER_MODULES.items()
}


class EmptyStream:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    def __aiter__(self):
        return self

    async def __anext__(self):
        raise StopAsyncIteration


async def main():
    output = {
        "provenance": {},
        "routing": [],
        "pagination": [],
        "normalization": [],
        "video_ids": [],
        "beeg_requests": [],
        "locale_headers": [],
    }
    for name, module in modules.items():
        path = Path(module.__file__)
        installed_path = installed[name] / path.name
        output["provenance"][name] = {
            "source": str(path),
            "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=roots[name], text=True).strip(),
            "local_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "installed_source": str(installed_path),
            "same_as_installed": installed_path.exists() and path.read_bytes() == installed_path.read_bytes(),
        }
    urls = [
        "https://de.pornhub.com/model/example/videos/upload?page=2",
        "https://www.pornhub.net/model/example",
        "https://www.pornhub.org/view_video.php?viewkey=ph123",
        "https://www.pornhub.com/gif/123",
        "https://www.pornhub.com/playlist/viewChunked?id=123",
        "https://www.eporner.com/channels/",
        "https://www.eporner.com/profile/example/",
        "https://www.eporner.com/embed/AbC123/",
        "https://www.xnxx3.com/profile/example",
        "https://www.xnxx.com/pornstar/example/videos/best/1",
        "https://de.xvideos.com/example",
        "https://de.xvideos.com/example?utm_source=share",
        "https://de.xvideos.com/example/videos/best/0",
        "https://www.xvideos.com/models/example",
        "https://www.xvideos.com/amateur-channels/example",
        "https://www.xvideos.com/example#quickies/a/abc123",
        "https://www.xvideos.es/video.abc123/example",
        "https://www.xvideos.com/embedframe/abc123",
        "https://xhamster.one/creators/example",
        "https://xhamster2.desi/creators/example",
        "https://xhvid.com/users/example",
        "https://xhamster.com/users/example/videos",
        "https://ge.xhamster.desi/creators/example/newest",
        "https://de.spankbang.com/abc/creator/example/",
        "https://de.spankbang.com/abc/channel/example/",
        "https://de.spankbang.com/en/pornstar/example/",
        "https://spankbang.com/abc/playlist/example",
        "https://spankbang.com/abc-def/playlist/example",
        "https://spankbang.com/abc/embed/",
        "https://www.youporn.com/channel/example/duration?page=2",
        "https://www.youporn.com/collections/videos/123/time?page=2",
        "https://www.youporn.com/users/example",
        "https://beeg.com/video/12345",
        "https://www.porntrex.com/models/example/",
        "https://www.porntrex.com/channels/example/",
        "https://www.porntrex.com/playlist/123/example/",
        "https://www.porntrex.com/playlists/",
        "https://beta.xfreehd.com/album/123/example?page=2",
        "https://de.redtube.com/123",
        "https://www.redtube.com.br/123",
        "https://embed.redtube.com/?id=123",
        "https://www.redtube.com/channel",
        "https://www.redtube.com/channels/vip-4k",
        "https://www.redtube.com/straight/playlists",
        "https://www.thumbzilla.com/video/ph123/example",
        "https://www.thumbzilla.com/amateurs/",
        "https://www.thumbzilla.com/playlist?playlist_id=123",
        "https://www.tube8.com/porn-video/123/",
        "https://www.tube8.com/category/example/123/",
    ]

    class Client:
        def __getattr__(self, name):
            async def method(*args, **kwargs):
                return name

            return method

    for url in urls:
        result = {"url": url}
        try:
            route = route_url(url)
            result.update(provider=route.provider, kind=route.kind.value)
            if route.kind.value in {"profile", "collection"}:
                result["method"] = await resolve_container(Client(), route)
        except Exception as error:
            result["error"] = type(error).__name__ + ": " + str(error)
        output["routing"].append(result)
    profiles = [
        ("pornhub", "Model", "get_videos", "https://de.pornhub.com/model/example"),
        ("pornhub", "Model", "get_uploads", "https://de.pornhub.com/model/example/videos/upload"),
        ("pornhub", "Channel", "get_videos", "https://de.pornhub.com/channels/example/videos"),
        ("eporner", "Pornstar", "videos", "https://de.eporner.com/pornstar/example/"),
        ("xnxx", "User", "videos", "https://www.xnxx.com/profile/example"),
        ("xvideos", "Pornstar", "videos", "https://de.xvideos.com/pornstars/example"),
        ("xhamster", "Creator", "videos", "https://ge.xhamster.desi/creators/example/newest"),
        ("spankbang", "Creator", "videos", "https://de.spankbang.com/abc/creator/example/"),
        ("youporn", "Channel", "videos", "https://www.youporn.com/channel/example/duration/"),
        ("youporn", "Collection", "videos", "https://www.youporn.com/collections/videos/123/"),
        ("porntrex", "Model", "videos", "https://www.porntrex.com/models/example/"),
        ("redtube", "User", "get_videos", "https://de.redtube.com/users/example"),
        ("redtube", "Playlist", "get_videos", "https://de.redtube.com/playlist?playlist_id=123"),
        ("thumbzilla", "Pornstar", "get_videos", "https://www.thumbzilla.com/pornstar/example/"),
        ("thumbzilla", "Playlist", "get_videos", "https://www.thumbzilla.com/playlist?playlist_id=123"),
        ("tube8", "User", "get_videos", "https://www.tube8.com/users/example"),
    ]
    for name, cls_name, method, url in profiles:
        module = modules[name]
        cls = getattr(module, cls_name)
        for suffix in ["", "?utm_source=share", "#videos"]:
            if "?" in url and suffix.startswith("?"):
                suffix = "&utm_source=share"
            calls = []

            def capture(*args, **kwargs):
                calls.extend(kwargs["target_page_urls"])
                return EmptyStream()

            with ExitStack() as stack:
                for symbol in ["scrape_stream", "_scrape_stream"]:
                    if hasattr(module, symbol):
                        stack.enter_context(patch.object(module, symbol, capture))
                if hasattr(module, "Helper"):
                    stack.enter_context(
                        patch.object(module, "Helper", lambda *args, **kwargs: SimpleNamespace(iterator=capture))
                    )
                stack.enter_context(patch.object(cls, "get_field", AsyncMock(return_value=2)))
                obj = cls(url=url + suffix, core=object())
                try:
                    async for _ in getattr(obj, method)(pages=2):
                        pass
                    result = {
                        "provider": name,
                        "class": cls_name,
                        "method": method,
                        "input": url + suffix,
                        "requests": calls,
                    }
                except Exception as error:
                    result = {
                        "provider": name,
                        "input": url + suffix,
                        "error": type(error).__name__ + ": " + str(error),
                    }
                output["pagination"].append(result)
    for name in ["Channel", "Pornstar"]:
        cls = getattr(modules["xvideos"], name)
        for url in [
            "https://de.xvideos.com/models/example",
            "https://de.xvideos.com/model/example",
            "https://de.xvideos.com/channels/example",
            "https://de.xvideos.com/example",
            "https://www.xvideos2.com/models/example",
            "https://de.xvideos.com/profiles/example/videos/best/0",
        ]:
            obj = cls(url=url, core=object())
            obj._sanitize_url()
            output["normalization"].append({"provider": "xvideos", "class": name, "input": url, "output": obj.url})
    for name, urls in {
        "pornhub": [
            "https://www.pornhub.com/view_video.php?viewkey=phABC&t=2",
            "https://www.pornhub.com/embed/phABC",
            "https://www.pornhub.com/video/show?viewkey=phABC",
        ],
        "eporner": [
            "https://de.eporner.com/video-AbC123/",
            "https://www.eporner.com/hd-porn/AbC123/",
            "https://www.eporner.com/embed/AbC123/",
            "https://www.eporner.com/video-AbC123?utm_source=share",
        ],
    }.items():
        for url in urls:
            video = modules[name].Video(url=url, core=object())
            output["video_ids"].append({"provider": name, "url": url, "id": video.video_id})
    module = modules["xfreehd"]
    for suffix in ["", "?utm_source=share", "#photos"]:
        url = "https://beta.xfreehd.com/album/123/example" + suffix
        album = module.Album(url=url, core=object())
        fetch = AsyncMock(return_value="<html></html>")
        with (
            patch.object(module, "get_html_content", fetch),
            patch.object(module.Album, "get_field", AsyncMock(return_value=2)),
        ):
            await album.get_images_by_page(2)
        output["pagination"].append(
            {
                "provider": "xfreehd",
                "class": "Album",
                "method": "get_images_by_page",
                "input": url,
                "requests": [call.kwargs["url"] for call in fetch.call_args_list],
            }
        )
    module = modules["beeg"]
    for url in [
        "https://beeg.com/-012340",
        "https://beeg.com/-012340?t=4-60",
        "https://beeg.com/-012340/",
        "https://beeg.com/video/12340",
    ]:
        fetch = AsyncMock(
            side_effect=[
                json.dumps({"file": {"data": [{"cd_value": "Example", "id": 1}], "fl_duration": 2}}),
                "example.m3u8",
            ]
        )
        with patch.object(module, "get_html_content", fetch):
            result = await module.Video(url=url, core=object())._load_api()
        output["beeg_requests"].append(
            {"url": url, "key": result["key"], "requests": [call.kwargs["url"] for call in fetch.call_args_list]}
        )
    for name, module in modules.items():
        configuration = RuntimeConfig()
        configuration.locale = "de-DE,de;q=0.9"
        async with BaseCore(configuration=configuration) as core:
            module.Client(core=core)
            output["locale_headers"].append(
                {
                    "provider": name,
                    "configured": configuration.locale,
                    "session_header": core.session.headers.get("Accept-Language"),
                    "requests": core.total_requests,
                }
            )
    args.output.write_text(json.dumps(output, indent=2))
    print("Counts:", {key: len(value) for key, value in output.items()})
    print(
        "Source differs from installed:",
        [name for name, info in output["provenance"].items() if not info["same_as_installed"]],
    )
    print("Probe errors:", [case for case in output["pagination"] if "error" in case])


if __name__ == "__main__":
    asyncio.run(main())
