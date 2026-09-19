#!/usr/bin/env python3
"""Interactive Questionary launcher for Porn Fetch test suites."""
from __future__ import annotations

import asyncio
import os
import subprocess
import sys
from pathlib import Path

import questionary

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SUITES = {
    "unit": (
        "Offline unit tests",
        [sys.executable, "-m", "unittest", "discover", "-s", "src/tests/unit", "-p", "test_*.py"],
    ),
    "integration": (
        "Qt and service integration tests",
        [sys.executable, "-m", "unittest", "discover", "-s", "src/tests/integration", "-p", "test_*.py"],
    ),
    "cli_offline": (
        "CLI offline self-test",
        [sys.executable, "Porn_Fetch_CLI.py", "--test-mode", "--filter", "offline"],
    ),
    "lint": (
        "Ruff lint checks",
        [
            sys.executable, "-m", "ruff", "check",
            "main.py", "Porn_Fetch_CLI.py", "src/shared", "src/database",
            "src/licensing", "src/cli", "src/tests", "scripts",
        ],
    ),
    "types": (
        "Focused Pyright checks",
        [sys.executable, "-m", "pyright"],
    ),
    "providers": (
        "Online provider checks",
        [sys.executable, "Porn_Fetch_CLI.py", "--test-mode"],
    ),
    "downloads": (
        "Online checks plus active download",
        [sys.executable, "Porn_Fetch_CLI.py", "--test-mode", "--test-downloads"],
    ),
    "sni": (
        "SNI proxy smoke request",
        [sys.executable, "src/tests/smoke/sni_proxy_smoke.py", "https://example.com/"],
    ),
}

ONLINE = {"providers", "downloads", "sni"}


async def choose_suites() -> list[str]:
    choices = [
        questionary.Choice(label, value=key)
        for key, (label, _command) in SUITES.items()
    ]
    selected = await questionary.checkbox(
        "Select test suites to run:",
        choices=choices,
    ).ask_async()
    if not selected:
        return []

    if ONLINE.intersection(selected):
        allowed = await questionary.confirm(
            "Allow real network requests for the selected online tests?",
            default=False,
        ).ask_async()
        if not allowed:
            selected = [suite for suite in selected if suite not in ONLINE]

    if "downloads" in selected:
        allowed = await questionary.confirm(
            "Allow an actual media download into a temporary directory?",
            default=False,
        ).ask_async()
        if not allowed:
            selected.remove("downloads")
    return selected


def run_suite(key: str) -> int:
    label, command = SUITES[key]
    print(f"\n=== {label} ===", flush=True)
    environment = os.environ.copy()
    environment["PORN_FETCH_TEST_ENV"] = "1"
    environment.setdefault("QT_QPA_PLATFORM", "offscreen")
    return subprocess.run(command, cwd=PROJECT_ROOT, env=environment, check=False).returncode


async def async_main() -> int:
    selected = await choose_suites()
    if not selected:
        print("No test suites selected.")
        return 0

    failures = []
    for key in selected:
        if await asyncio.to_thread(run_suite, key):
            failures.append(SUITES[key][0])

    if failures:
        print("\nFailed suites:")
        for label in failures:
            print(f"- {label}")
        return 1
    print("\nAll selected suites passed.")
    return 0


def main() -> int:
    return asyncio.run(async_main())


if __name__ == "__main__":
    raise SystemExit(main())
