"""Explicitly opt-in diagnostics that download real media."""
from __future__ import annotations

import asyncio
import tempfile
import time
from pathlib import Path

from ..downloads import download_gallery, download_video
from ..media import prepare_video
from ..providers import ClientPool
from ..settings import CliSettings
from .cases import ACTIVE_DOWNLOAD_URL
from .models import TestResult
from .online import _error, gallery_metadata


async def test_active_gallery_download(name: str, url: str, pool: ClientPool, timeout: float = 120) -> TestResult:
    started = time.perf_counter()
    try:
        async with asyncio.timeout(timeout):
            _route, album = await pool.resolve(url)
            images = await gallery_metadata(album)
            with tempfile.TemporaryDirectory(prefix="porn-fetch-gallery-test-") as directory:
                outcome = await download_gallery(album, directory, concurrency=2)
                files = list(outcome.path.iterdir())
                assert outcome.status == "completed" and len(files) == len(images)
                for path in files:
                    with path.open("rb") as image:
                        header = image.read(12)
                    assert (header.startswith((b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n", b"GIF87a", b"GIF89a"))
                            or (header.startswith(b"RIFF") and header[8:12] == b"WEBP")), "Downloaded file is not an image"
        return TestResult("Download", name, url, True, f"{len(files)} image files verified", time.perf_counter() - started)
    except Exception as error:
        return TestResult("Download", name, url, False, "", time.perf_counter() - started, _error(error, timeout))


async def test_active_download(pool: ClientPool, settings: CliSettings) -> TestResult:
    started = time.perf_counter()
    try:
        route, source = await pool.resolve(ACTIVE_DOWNLOAD_URL)
        media = await prepare_video(source, route.provider)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "active-download-test.mp4"
            outcome = await download_video(
                media.source_video,
                target,
                "worst",
                settings,
                has_premium=False,
                available_qualities=media.qualities,
            )
            assert outcome.status == "completed"
            assert target.is_file() and target.stat().st_size > 0
            size_mb = target.stat().st_size / (1024 * 1024)
        return TestResult("Download", "Active media download", ACTIVE_DOWNLOAD_URL, True, f"Downloaded {size_mb:.1f} MiB", time.perf_counter() - started)
    except Exception as error:
        return TestResult("Download", "Active media download", ACTIVE_DOWNLOAD_URL, False, "", time.perf_counter() - started, str(error))
