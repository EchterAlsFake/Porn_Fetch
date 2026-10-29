"""Explicitly opt-in diagnostics that download real media."""
from __future__ import annotations

import tempfile
import time
from pathlib import Path

from ..downloads import download_video
from ..media import prepare_video
from ..providers import ClientPool
from ..settings import CliSettings
from .cases import ACTIVE_DOWNLOAD_URL
from .models import TestResult


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
