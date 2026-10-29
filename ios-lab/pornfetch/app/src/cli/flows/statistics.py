"""Interactive PocketBase statistics and history flow."""
from __future__ import annotations

import questionary

from ..tracker import print_dashboard_stats, print_failed_downloads, print_origin_iterators
from .context import WizardContext
from .ui import WIZARD_STYLE, print_error, print_success


async def handle_statistics_dashboard(ctx: WizardContext) -> None:
    """Display PocketBase download statistics, history, and tracked origins."""
    while True:
        status_badge = "[bold green]Active[/]" if ctx.settings.track_videos else "[dim yellow]Disabled[/]"
        action = await questionary.select(
            f"PocketBase Statistics & History (Tracking: {status_badge}):",
            choices=[
                questionary.Choice("📊 View Overview Statistics & Source Breakdown", value="overview"),
                questionary.Choice("⚠️  View Failed Downloads", value="failed"),
                questionary.Choice("📁 View Tracked Sources / Collections", value="origins"),
                questionary.Choice(
                    f"{'🛑 Disable' if ctx.settings.track_videos else '✅ Enable'} Download Tracking",
                    value="toggle",
                ),
                questionary.Choice("📦 Auto-Install / Verify PocketBase Binary", value="install_pb"),
                questionary.Choice("⚙️  Configure Database Paths", value="config"),
                questionary.Choice("🔙 Back to Main Menu", value="back"),
            ],
            style=WIZARD_STYLE,
        ).ask_async()

        if not action or action == "back":
            break

        if action == "install_pb":
            from .settings import handle_pocketbase_install_flow
            await handle_pocketbase_install_flow(ctx)
            continue

        if action == "toggle":
            new_state = not ctx.settings.track_videos
            ctx.settings = ctx.settings.overridden(track_videos=new_state)
            ctx.settings_store.save(ctx.settings)
            ctx.console.print(
                f"[bold green]Download tracking {'enabled' if new_state else 'disabled'}.[/]"
            )
            continue

        if action == "config":
            new_path = await questionary.text(
                "PocketBase data directory path:",
                default=ctx.settings.pocketbase_data_path,
                style=WIZARD_STYLE,
            ).ask_async()
            if new_path and new_path.strip():
                ctx.settings = ctx.settings.overridden(pocketbase_data_path=new_path.strip())
                ctx.settings_store.save(ctx.settings)
                print_success(ctx.console, "Configuration Saved", f"Data path set to: {new_path.strip()}")
            continue

        if not ctx.settings.track_videos:
            ctx.console.print("[yellow]Tracking is currently disabled in settings.[/]")
            ask_start = await questionary.confirm(
                "Would you like to start PocketBase anyway to inspect existing stored data?",
                default=True,
                style=WIZARD_STYLE,
            ).ask_async()
            if not ask_start:
                continue

        with ctx.console.status("[bold cyan]Connecting to PocketBase service...[/]"):
            try:
                from src.database import PocketBaseError, PocketBaseTracker
                temp_tracker = PocketBaseTracker(
                    data_path=ctx.settings.pocketbase_data_path,
                    enabled=True,
                    binary_path=ctx.settings.pocketbase_binary or None,
                    legacy_sqlite_path=ctx.settings.legacy_database_path,
                )
                await temp_tracker.start()
            except PocketBaseError as exc:
                print_error(
                    ctx.console,
                    "PocketBase Unavailable",
                    str(exc),
                )
                if "binary was not found" in str(exc).lower():
                    should_install = await questionary.confirm(
                        "PocketBase executable was not found. Would you like to auto-install it now?",
                        default=True,
                        style=WIZARD_STYLE,
                    ).ask_async()
                    if should_install:
                        from .settings import handle_pocketbase_install_flow
                        installed = await handle_pocketbase_install_flow(ctx)
                        if installed:
                            continue
                continue
            except Exception as exc:
                print_error(ctx.console, "Database Error", str(exc))
                continue

        try:
            if action == "overview":
                stats = temp_tracker.get_dashboard_stats()
                print_dashboard_stats(stats, ctx.console)
            elif action == "failed":
                failed = temp_tracker.get_failed_videos()
                print_failed_downloads(failed, ctx.console)
            elif action == "origins":
                iterators = temp_tracker.get_available_iterators()
                print_origin_iterators(iterators, ctx.console)
        finally:
            await temp_tracker.close()
