"""Opt-in provider diagnostics that perform real network requests."""
from __future__ import annotations

import asyncio
import time

from ..media import prepare_video
from ..providers import ClientPool, route_url
from .models import TestResult


def _error(error: Exception, timeout: float) -> str:
    if isinstance(error, (TimeoutError, asyncio.TimeoutError)):
        return f"Timed out after {timeout:.0f}s"
    return (str(error).strip() or type(error).__name__).splitlines()[0][:160]


async def test_video(name: str, url: str, pool: ClientPool, timeout: float = 60.0) -> TestResult:
    started = time.perf_counter()
    try:
        async def load():
            route, source = await pool.resolve(url)
            return await prepare_video(source, route.provider)

        media = await asyncio.wait_for(load(), timeout)
        assert media.title and media.title != "Untitled"
        assert media.qualities
        details = f"{media.title[:35]} | {media.qualities}"
        return TestResult("Provider", name, url, True, details, time.perf_counter() - started)
    except Exception as error:
        return TestResult("Provider", name, url, False, "", time.perf_counter() - started, _error(error, timeout))


async def test_gallery(name: str, url: str, pool: ClientPool, timeout: float = 60.0) -> TestResult:
    started = time.perf_counter()
    try:
        _route, album = await asyncio.wait_for(pool.resolve(url), timeout)
        title = getattr(album, "title", None) or "Untitled"
        return TestResult("Gallery", name, url, True, str(title)[:60], time.perf_counter() - started)
    except Exception as error:
        return TestResult("Gallery", name, url, False, "", time.perf_counter() - started, _error(error, timeout))


async def test_stream(category: str, name: str, url: str, pool: ClientPool, timeout: float = 60.0) -> TestResult:
    started = time.perf_counter()
    try:
        async def first_item():
            async for item in pool.media_stream(url, pages=1):
                return item
            return None

        item = await asyncio.wait_for(first_item(), timeout)
        assert item is not None
        route = route_url(url)
        return TestResult(category, name, url, True, f"{route.kind.value}: first item loaded", time.perf_counter() - started)
    except Exception as error:
        return TestResult(category, name, url, False, "", time.perf_counter() - started, _error(error, timeout))
