"""Explicit live GUI profile test runner. Reads metadata/playlists, never media.

    uv run python -m src.tests.smoke.profile_urls --include-variants
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import tempfile
import time
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path


async def run(args):
    from PySide6.QtTest import QAbstractItemModelTester

    from src.backend import clients
    from src.backend.application import stop_flag
    from src.backend.profile_diagnostics import (
        ProfileFeedUnavailable,
        load_profile_cases,
        make_test_backend,
        test_profile_url,
    )

    cases = load_profile_cases(include_variants=args.include_variants, pattern=args.filter)
    for provider in {case["provider"] for case in cases}:
        configuration = clients.client_for(provider).core.configuration
        configuration.timeout = 20
        configuration.request_attempts = 1
        configuration.request_delay = 0
    results = []
    report = {
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Real GUI profile dispatch, preparation, Qt list roles/signals and stream URL resolution; no media downloads",
        "items_per_case": args.items, "pages_per_case": 1, "results": results,
    }
    try:
        with args.report.with_suffix(".log").open("w", encoding="utf-8") as log:
            for number, case in enumerate(cases, 1):
                started = time.monotonic()
                backend = make_test_backend()
                tester = QAbstractItemModelTester(
                    backend._downloads_model, QAbstractItemModelTester.FailureReportingMode.Warning,
                )
                stop_flag.clear()
                result = {"id": case["id"], "url": case["url"], "provider": case["provider"]}
                try:
                    with redirect_stdout(log), redirect_stderr(log):
                        result.update(await test_profile_url(
                            backend, backend._downloads_model, case, timeout=args.timeout, items=args.items,
                        ))
                    result["passed"] = True
                except ProfileFeedUnavailable as error:
                    result.update(passed=False, skipped=True, skip_reason=str(error), **error.metadata)
                except Exception as error:
                    result.update(passed=False, error_type=type(error).__name__, error=str(error))
                result["elapsed_seconds"] = round(time.monotonic() - started, 2)
                results.append(result)
                args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
                status = "SKIP" if result.get("skipped") else ("PASS" if result["passed"] else "FAIL")
                detail = result.get("skip_reason") or result.get("error") or f"{result['rows']} rows"
                print(f"[{number}/{len(cases)}] {status} {case['id']} — {detail}", flush=True)
                del tester, backend
    finally:
        await clients.close_all_clients()
        stop_flag.clear()
    passed = sum(result["passed"] for result in results)
    skipped = sum(bool(result.get("skipped")) for result in results)
    failed = len(results) - passed - skipped
    report.update(passed=passed, skipped=skipped, failed=failed)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"{passed} passed, {skipped} skipped, {failed} failed. Report: {args.report}")
    return int(failed != 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include-variants", action="store_true")
    parser.add_argument("--filter", default="", help="Fixture ID/provider/URL substring")
    parser.add_argument("--items", type=int, choices=(1, 2, 3), default=2)
    parser.add_argument("--timeout", type=float, default=90)
    parser.add_argument("--report", type=Path, default=Path(tempfile.gettempdir()) / "porn-fetch-profile-smoke.json")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    # Set these before importing GUI modules: no splash, windows or real settings.
    os.environ["PORN_FETCH_TEST_ENV"] = "1"
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    logging.disable(logging.CRITICAL)
    with tempfile.TemporaryDirectory(prefix="porn-fetch-profile-config-") as configuration:
        os.environ["XDG_CONFIG_HOME"] = configuration
        from PySide6.QtGui import QGuiApplication

        app = QGuiApplication.instance() or QGuiApplication([])
        status = asyncio.run(run(args))
        app.processEvents()
        return status


if __name__ == "__main__":
    raise SystemExit(main())
