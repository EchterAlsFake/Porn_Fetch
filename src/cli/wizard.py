"""Interactive CLI composition root and backwards-compatible public façade."""
from __future__ import annotations

import argparse
import asyncio
from typing import Any

from src.shared.error_reporting import ERROR_REPORT_CONSENT_VERSION

from . import prompts as questionary
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
    print_screen,
    print_success,
)
from .settings import SettingsStore, prompt_error_reporting_consent
from .terminal import terminal_console

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
    "handle_self_update",
    "handle_settings",
    "handle_statistics_dashboard",
    "make_download_progress",
    "print_banner",
    "print_error",
    "print_success",
    "run_wizard",
]


async def handle_self_update() -> bool:
    """Run the signed updater and signal when the menu must exit for replacement."""
    from .self_update import run_self_update

    staged = False

    def mark_staged() -> None:
        nonlocal staged
        staged = True

    await asyncio.to_thread(run_self_update, check_only=False, assume_yes=False, on_staged=mark_staged)
    return staged


async def run_wizard(args: argparse.Namespace | None = None) -> int:
    """Run the interactive terminal menu and close session resources cleanly."""
    console = terminal_console()
    store = SettingsStore()
    settings = store.load()
    explicit_reporting_choice = getattr(args, "error_reporting", None) if args else None
    if explicit_reporting_choice is not None:
        settings = settings.overridden(
            error_reporting=explicit_reporting_choice,
            error_reporting_decided=True,
            error_reporting_consent_version=ERROR_REPORT_CONSENT_VERSION,
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

    focused = None
    try:
        while True:
            print_banner(console, license_state=ctx.license_service.status.state)
            print_screen(console)

            paused_items = PausedStore().load()
            main_choices = [
                questionary.Separator("Downloads"),
                questionary.Choice("Download URL", value="single", description="Video, album or direct media link"),
            ]
            if paused_items:
                main_choices.append(questionary.Choice(
                    f"Resume paused downloads ({len(paused_items)})", value="resume",
                    description="Resume saved jobs or remove their partial files",
                ))
            main_choices.extend([
                questionary.Choice("Scrape profile or playlist", value="scrape"),
                questionary.Choice("Queue and tracked profiles", value="batch"),
                questionary.Separator("Tools and preferences"),
                questionary.Choice("Statistics and history", value="stats"),
                questionary.Choice("Accounts and authentication", value="auth"),
                questionary.Choice("Settings", value="settings"),
                questionary.Choice("License", value="license"),
                questionary.Choice("Check for Updates", value="update"),
                questionary.Choice("Diagnostics", value="test", description="Run the existing supported-site self-tests"),
                questionary.Separator(),
                questionary.Choice("Exit", value="exit"),
            ])

            action = await questionary.select(
                "Choose an action:", choices=main_choices, default=focused, style=WIZARD_STYLE,
            ).ask_async()
            focused = action

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
                elif action == "update":
                    if await handle_self_update():
                        break
                elif action == "test":
                    from .selftest import run_cli_self_test
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
        console.print("[dim]Session closed.[/]")

    return 0
