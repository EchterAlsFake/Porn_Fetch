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
    "gui_profiles": (
        "Online GUI profile/list-model checks (metadata and playlists only)",
        [sys.executable, "-m", "src.tests.smoke.profile_urls", "--include-variants"],
    ),
    "downloads": (
        "Online checks plus active download",
        [sys.executable, "Porn_Fetch_CLI.py", "--test-mode", "--test-downloads"],
    ),
    "download_lifecycle": (
        "Live pause/resume and cleanup (15 providers, 30 media workflows)",
        [sys.executable, "-m", "src.tests.smoke.download_lifecycle"],
    ),
    "download_gui": (
        "Live desktop download controls (14 providers, 42 workflows; SpankBang manual)",
        [sys.executable, "-m", "src.tests.smoke.download_gui"],
    ),
    "download_queue": (
        "Live desktop queue and concurrency (limits 1/2, stop/remove isolation)",
        [sys.executable, "-m", "src.tests.smoke.download_queue"],
    ),
    "settings_gui": (
        "Complete desktop settings (55 settings, real runtime/network/media effects)",
        [sys.executable, "-m", "src.tests.smoke.settings_gui"],
    ),
    "statistics_gui": (
        "Live desktop statistics and history (real HLS/RAW downloads and PocketBase)",
        [sys.executable, "-m", "src.tests.smoke.statistics_gui"],
    ),
    "download_advanced": (
        "Advanced desktop download controls (real regex/filter data, unusual titles and media)",
        [sys.executable, "-m", "src.tests.smoke.download_advanced"],
    ),
    "application_recovery": (
        "Live application teardown and recovery (fresh processes, HLS/RAW and history)",
        [sys.executable, "-m", "src.tests.smoke.application_recovery"],
    ),
    "collections_gui": (
        "Live model/playlist end to end (pagination, filters, selected download and history)",
        [sys.executable, "-m", "src.tests.smoke.collections_gui"],
    ),
    "account_cookies": (
        "Live Brave cookie login and account lists (PornHub, XHamster, XVideos)",
        [sys.executable, "-m", "src.tests.smoke.account_cookies", "--browser", "brave"],
    ),
    "account_gui": (
        "Complete account GUI checks (real Brave cookies, desktop/mobile ListViews)",
        [sys.executable, "-m", "src.tests.smoke.account_gui", "--browser", "brave"],
    ),
    "sni": (
        "SNI proxy smoke request",
        [sys.executable, "src/tests/smoke/sni_proxy_smoke.py", "https://example.com/"],
    ),
}

ONLINE = {"providers", "gui_profiles", "downloads", "download_lifecycle", "download_gui", "download_queue", "settings_gui",
          "statistics_gui", "download_advanced", "application_recovery", "collections_gui", "account_cookies", "account_gui", "sni"}

MEDIA = {"downloads", "download_lifecycle", "download_gui", "download_queue", "settings_gui",
         "statistics_gui", "download_advanced", "application_recovery", "collections_gui"}


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

    if MEDIA.intersection(selected):
        allowed = await questionary.confirm(
            "Allow actual media downloads into temporary directories?",
            default=False,
        ).ask_async()
        if not allowed:
            selected = [suite for suite in selected
                        if suite not in MEDIA]
    if {"account_cookies", "account_gui"}.intersection(selected):
        allowed = await questionary.confirm(
            "Read Brave cookies for PornHub, XHamster and XVideos and access their account lists?",
            default=False,
        ).ask_async()
        if not allowed:
            selected = [suite for suite in selected if suite not in {"account_cookies", "account_gui"}]
    if "account_gui" in selected:
        playlist = await questionary.text(
            "Optional XVideos playlist URL (leave blank for account-page actions only):",
        ).ask_async()
        if playlist and playlist.strip():
            SUITES["account_gui"][1].extend(["--xvideos-playlist", playlist.strip()])
            private = await questionary.confirm(
                "Is this playlist private? Also verify that anonymous clients cannot read it?",
                default=False,
            ).ask_async()
            if private:
                SUITES["account_gui"][1].append("--xvideos-private")
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
