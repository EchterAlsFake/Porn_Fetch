"""Console runner for the separated CLI diagnostic suites."""
from __future__ import annotations

import asyncio
import time
from typing import Any, Coroutine

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..providers import ClientPool
from ..settings import CliSettings
from .cases import COLLECTION_TESTS, GALLERY_TESTS, PROFILE_TESTS, SHORTS_TESTS, SINGLE_VIDEO_TESTS
from .downloads import test_active_download
from .models import TestResult
from .offline import run_offline_tests
from .online import test_gallery, test_stream, test_video


async def run_cli_self_test(
    filter_pattern: str | None = None,
    concurrency: int = 2,
    include_downloads: bool = False,
) -> int:
    console = Console()
    started = time.perf_counter()
    pattern = filter_pattern.casefold().strip() if filter_pattern else ""
    offline_only = pattern in {"offline", "unit", "core"}
    results = await run_offline_tests()

    if not offline_only:
        settings = CliSettings()
        pool = ClientPool(settings.to_runtime_config())
        semaphore = asyncio.Semaphore(concurrency)

        async def limited(operation: Coroutine[Any, Any, TestResult]) -> TestResult:
            async with semaphore:
                return await operation

        def selected(cases: list[tuple[str, str]]) -> list[tuple[str, str]]:
            if not pattern:
                return cases
            return [case for case in cases if pattern in " ".join(case).casefold()]

        try:
            operations = [limited(test_video(name, url, pool)) for name, url in selected(SINGLE_VIDEO_TESTS + SHORTS_TESTS)]
            operations += [limited(test_gallery(name, url, pool)) for name, url in selected(GALLERY_TESTS)]
            operations += [limited(test_stream("Collection", name, url, pool)) for name, url in selected(COLLECTION_TESTS)]
            operations += [limited(test_stream("Profile", name, url, pool)) for name, url in selected(PROFILE_TESTS)]
            results.extend(await asyncio.gather(*operations))
            if include_downloads:
                results.append(await test_active_download(pool, settings))
        finally:
            await pool.close()

    table = Table(title="Porn Fetch test results", border_style="#ff2a85")
    table.add_column("Result")
    table.add_column("Category")
    table.add_column("Test")
    table.add_column("Details")
    for result in results:
        status = "[green]PASS[/]" if result.passed else "[red]FAIL[/]"
        table.add_row(status, result.category, result.name, result.details or str(result.error))
    console.print(table)

    failed = sum(not result.passed for result in results)
    console.print(Panel(
        f"{len(results) - failed} passed, {failed} failed in {time.perf_counter() - started:.1f}s",
        border_style="green" if not failed else "yellow",
    ))
    return 1 if failed else 0
