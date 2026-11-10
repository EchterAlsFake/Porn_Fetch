"""RedGIFs rendition labels mapped to measured resolutions for both frontends.

Only small MP4 metadata ranges are read, through the supplied core. Files and
resume state remain entirely owned by the shared RAW downloader.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from base_api import RequestCacheKey
from base_api.modules.static_functions import choose_quality_from_list

_HEADER_SIZE = 65536
_MAX_MOOV_SIZE = 2 * 1024 * 1024


def _boxes(data: bytes):
    offset = 0
    while offset + 8 <= len(data):
        size = int.from_bytes(data[offset : offset + 4], "big")
        kind = data[offset + 4 : offset + 8]
        header = 8
        if size == 1:
            if offset + 16 > len(data):
                return
            size = int.from_bytes(data[offset + 8 : offset + 16], "big")
            header = 16
        if size == 0:
            size = len(data) - offset
        if size < header:
            raise ValueError("Invalid MP4 metadata box")
        yield offset, size, kind, header
        offset += size


def _dimensions(moov: bytes) -> tuple[int, int]:
    for offset, size, kind, header in _boxes(moov):
        if offset + size > len(moov):
            raise ValueError("Incomplete MP4 metadata")
        if kind in {b"moov", b"trak"}:
            try:
                return _dimensions(moov[offset + header : offset + size])
            except LookupError:
                continue
        if kind == b"tkhd" and size >= 84:
            # Track-header width/height are the last two 16.16 fixed-point values.
            width = int.from_bytes(moov[offset + size - 8 : offset + size - 4], "big") >> 16
            height = int.from_bytes(moov[offset + size - 4 : offset + size], "big") >> 16
            if width > 0 and height > 0:
                return width, height
    raise LookupError("MP4 has no video track dimensions")


async def _range(core: Any, url: str, start: int, end: int) -> bytes:
    response = await core.request(url, headers={"Range": f"bytes={start}-{end}"})
    match = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)", response.headers.get("Content-Range", ""))
    if response.status_code != 206 or not match or int(match[1]) != start or int(match[2]) > end:
        raise ValueError("RedGIFs did not return the requested MP4 metadata range")
    data = response.content
    if len(data) != int(match[2]) - start + 1:
        raise ValueError("Incomplete RedGIFs MP4 metadata range")
    return data


async def _resolution(core: Any, url: str) -> int:
    start = 0
    for _ in range(8):
        data = await _range(core, url, start, start + _HEADER_SIZE - 1)
        for offset, size, kind, header in _boxes(data):
            if kind == b"moov":
                if size > _MAX_MOOV_SIZE:
                    raise ValueError("RedGIFs MP4 metadata exceeds the inspection limit")
                moov = data[offset : offset + size]
                if len(moov) < size:
                    moov = await _range(core, url, start + offset, start + offset + size - 1)
                width, height = _dimensions(moov)
                # Portrait 480x854 is a 480p rendition, not an invented 720p SD tier.
                return min(width, height)
            if offset + size + 8 > len(data):
                start += offset + size
                break
        else:
            break
    raise ValueError("RedGIFs MP4 has no readable resolution metadata")


async def rendition_map(video: Any) -> dict[int, str]:
    await video.load_fields("sources", "media_type")
    if video.media_type != 1:
        raise ValueError("Use a RedGIFs video/GIF URL; still images are not supported")
    sources = {label: url for label, url in (video.sources or {}).items() if label in {"sd", "hd"}}
    fingerprint = hashlib.sha256(json.dumps(sources, sort_keys=True).encode()).hexdigest()
    key = RequestCacheKey(
        method="MP4-RENDITIONS",
        url=video.url,
        allow_redirects=True,
        params_fingerprint=fingerprint,
        body_fingerprint="",
        headers_fingerprint="",
        cookies_fingerprint="",
    )
    cached = video.core.cache.get_response(key)
    if cached is not None:
        return {int(quality): label for quality, label in json.loads(cached).items()}
    result = {}
    for label in ("sd", "hd"):
        if label in sources:
            result[await _resolution(video.core, sources[label])] = label
    if not result:
        raise ValueError("RedGIFs exposes no downloadable video renditions")
    video.core.cache.set_response(key, json.dumps(result))
    return result


async def available_qualities(video: Any) -> list[int]:
    return sorted(await rendition_map(video))


async def quality_label(video: Any, quality: str | int) -> str:
    mapping = await rendition_map(video)
    preference = {"sd": "worst", "hd": "best"}.get(str(quality).strip().casefold(), quality)
    chosen = choose_quality_from_list(sorted(mapping), preference)
    return mapping[chosen]
