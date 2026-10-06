"""Interactive CLI composition root and backwards-compatible public façade."""
from __future__ import annotations

import argparse
import asyncio
from typing import Any

import questionary
from rich.console import Console
from rich.panel import Panel

from .downloads import PausedStore
from .flows import (
    handle_account_auth,
    handle_batch_management,
    handle_download_single,
    handle_license_management,
    handle_resume_paused,
    handle_scrape_profile,
    handle_settings,
    handle_statistics_dashboard,
)
from .flows.context import WizardContext
from .flows.ui import (
    WIZARD_STYLE,
    DownloadSpeedColumn,
    SmartUnitsColumn,
    make_download_progress,
    print_banner,
    print_error,
    print_success,
)
from .settings import SettingsStore, prompt_error_reporting_consent

__all__ = [
    "DownloadSpeedColumn",
    "SmartUnitsColumn",
    "WIZARD_STYLE",
    "WizardContext",
    "handle_account_auth",
    "handle_batch_management",
    "handle_download_single",
    "handle_license_management",
    "handle_resume_paused",
    "handle_scrape_profile",
    "handle_settings",
    "handle_statistics_dashboard",
    "make_download_progress",
    "print_banner",
    "print_error",
    "print_success",
    "run_wizard",
]


async def run_wizard(args: argparse.Namespace | None = None) -> int:
    """Run the interactive terminal menu and close session resources cleanly."""
    console = Console()
    store = SettingsStore()
    settings = store.load()

    explicit_reporting_choice = getattr(args, "error_reporting", None) if args else None
    if explicit_reporting_choice is not None:
        settings = settings.overridden(
            error_reporting=explicit_reporting_choice,
            error_reporting_decided=True,
        )
        store.save(settings)
    elif not settings.error_reporting_decided:
        settings = await prompt_error_reporting_consent(settings, store, console=console)

    overrides: dict[str, Any] = {}
    if args is not None:
        if getattr(args, "quality", None):
            overrides["quality"] = args.quality
        if getattr(args, "output", None):
            overrides["output_path"] = args.output
    if overrides:
        settings = settings.overridden(**overrides)

    ctx = WizardContext(settings, store, console)
    await ctx.check_license(force=True)

    try:
        while True:
            console.print()
            print_banner(console, license_state=ctx.license_service.status.state)
            console.print()

            paused_items = PausedStore().load()
            main_choices = [
                questionary.Choice("📥 Download Single URL (Video, album, or direct link)", value="single"),
            ]
            if paused_items:
                main_choices.append(questionary.Choice(
                    f"⏯️  Resume Paused Downloads ({len(paused_items)} saved job{'s' if len(paused_items) > 1 else ''})",
                    value="resume",
                ))
            main_choices.extend([
                questionary.Choice("👤 Scrape Profile / Playlist (Fetch model or playlist content)", value="scrape"),
                questionary.Choice("📋 Batch / Queue Management (Review tracked models or queued links)", value="batch"),
                questionary.Choice("📊 Download Statistics & History (PocketBase dashboard & tracking)", value="stats"),
                questionary.Choice("🔑 Account & Authentication (Login credentials, browser cookie import)", value="auth"),
                questionary.Choice("⚙️  Settings & Configuration (Output path, naming templates, preferred quality)", value="settings"),
                questionary.Choice("📜 License Management (Check status, import key/file, deactivate)", value="license"),
                questionary.Choice("🧪 Run Self-Test Suite (Automated check for supported sites & features)", value="test"),
                questionary.Choice("❌ Exit", value="exit"),
            ])

            action = await questionary.select(
                "Main Menu (use arrow keys to navigate):",
                choices=main_choices,
                style=WIZARD_STYLE,
            ).ask_async()

            if action in {None, "exit"}:
                break

            try:
                if action == "single":
                    await handle_download_single(ctx)
                elif action == "resume":
                    await handle_resume_paused(ctx)
                elif action == "scrape":
                    await handle_scrape_profile(ctx)
                elif action == "batch":
                    await handle_batch_management(ctx)
                elif action == "stats":
                    await handle_statistics_dashboard(ctx)
                elif action == "auth":
                    await handle_account_auth(ctx)
                elif action == "settings":
                    await handle_settings(ctx)
                elif action == "license":
                    await handle_license_management(ctx)
                elif action == "test":
                    from .tests import run_cli_self_test
                    await run_cli_self_test()
            except asyncio.CancelledError:
                console.print("\n[yellow]Operation cancelled.[/]")
            except Exception as error:
                report_id = await ctx.report(
                    error, "run interactive CLI action", "src.cli.wizard.run_wizard",
                    action=action,
                )
                print_error(console, "Unexpected Error", f"{error}\nError ID: {report_id}")
    finally:
        await ctx.close()
        console.print()
        console.print(Panel(
            "[bold #ff2a85]Thank you for using Porn Fetch CLI![/]\n"
            "[dim]All tasks completed. Session closed cleanly.[/]",
            border_style="#00e5ff",
            padding=(0, 2),
        ))

    return 0
