"""Interactive workflow for resuming or purging paused downloads."""
from __future__ import annotations

import asyncio
from pathlib import Path

import questionary
from rich.table import Table

from ..downloads import DownloadController, PausedStore, clear_resume_state, download_gallery, download_video
from ..media import prepare_video
from ..tracker import record_cli_download
from .context import WizardContext
from .ui import WIZARD_STYLE, make_download_progress, print_success


async def handle_resume_paused(ctx: WizardContext) -> None:
    """Review, resume, or purge saved paused downloads."""
    store = PausedStore()
    paused_items = store.load()
    if not paused_items:
        ctx.console.print("[yellow]No paused downloads found.[/]")
        return

    table = Table(title=f"Paused Downloads ({len(paused_items)} saved)", border_style="#ff2a85")
    table.add_column("#", style="cyan", justify="right")
    table.add_column("Title", style="bold white")
    table.add_column("Quality", style="magenta")
    table.add_column("Kind", style="blue")
    table.add_column("Provider", style="green")
    table.add_column("Paused At", style="dim")

    for i, item in enumerate(paused_items, 1):
        paused_dt = item.get("paused_at", "")[:19].replace("T", " ")
        table.add_row(
            str(i),
            item.get("title") or Path(item.get("target", "")).name or item.get("url", ""),
            str(item.get("quality", "best")),
            item.get("kind", "video"),
            item.get("provider", "unknown"),
            paused_dt,
        )

    ctx.console.print()
    ctx.console.print(table)
    ctx.console.print()

    action = await questionary.select(
        "Choose an action:",
        choices=[
            questionary.Choice("▶️  Resume all paused downloads", value="resume_all"),
            questionary.Choice("▶️  Resume a specific download", value="resume_single"),
            questionary.Choice("🗑️  Cancel and delete a paused job", value="delete_single"),
            questionary.Choice("🧹 Clear all paused jobs and purge temporary files", value="clear_all"),
            questionary.Choice("🔙 Back to Main Menu", value="back"),
        ],
        style=WIZARD_STYLE,
    ).ask_async()

    if action in {None, "back"}:
        return

    if action == "clear_all":
        confirm = await questionary.confirm(
            "Are you sure you want to clear all paused downloads and purge partial files?",
            default=False,
            style=WIZARD_STYLE,
        ).ask_async()
        if confirm:
            for item in paused_items:
                target = item.get("target")
                if target:
                    clear_resume_state(target)
            store.clear()
            ctx.console.print("[green]All paused downloads cleared and temporary files purged.[/]")
        return

    if action == "delete_single":
        item_choices = [
            questionary.Choice(
                f"{i}. {item.get('title') or Path(item.get('target', '')).name}",
                value=item,
            )
            for i, item in enumerate(paused_items, 1)
        ]
        item_choices.append(questionary.Choice("🔙 Cancel", value=None))
        picked = await questionary.select("Select job to remove:", choices=item_choices, style=WIZARD_STYLE).ask_async()
        if picked:
            target = picked.get("target")
            if target:
                clear_resume_state(target)
                store.remove(target)
            if picked.get("url"):
                store.remove(picked.get("url"))
            ctx.console.print(f"[green]Removed '{picked.get('title')}' and purged partial files.[/]")
        return

    items_to_resume = paused_items if action == "resume_all" else []
    if action == "resume_single":
        item_choices = [
            questionary.Choice(
                f"{i}. {item.get('title') or Path(item.get('target', '')).name}",
                value=item,
            )
            for i, item in enumerate(paused_items, 1)
        ]
        item_choices.append(questionary.Choice("🔙 Cancel", value=None))
        picked = await questionary.select("Select job to resume:", choices=item_choices, style=WIZARD_STYLE).ask_async()
        if not picked:
            return
        items_to_resume = [picked]

    has_premium = (await ctx.check_license()).allowed
    for item in items_to_resume:
        url = item.get("url")
        target_path = Path(item.get("target", ""))
        quality = item.get("quality", "best")
        title = item.get("title") or target_path.name
        kind = item.get("kind", "video")

        ctx.console.print(f"\n[cyan]▶ Resuming: [bold white]{title}[/][/]")
        controller = DownloadController(
            url=url, target=target_path, title=title, quality=quality, kind=kind,
        )

        with make_download_progress(ctx.console) as progress:
            task_id = progress.add_task(f"Resuming {title[:35]}...", total=None)

            def on_progress(completed: int, total: int, unit: str = "items") -> None:
                progress.update(task_id, completed=completed, total=total if total > 0 else None, unit=unit)

            try:
                route, source = await ctx.pool.resolve(url)
                if kind == "gallery":
                    outcome = await download_gallery(
                        source,
                        target_path.parent,
                        controller=controller,
                        progress=on_progress,
                        concurrency=ctx.settings.videos_concurrency,
                    )
                else:
                    media = await prepare_video(source, route.provider)
                    outcome = await download_video(
                        source,
                        target_path,
                        quality,
                        ctx.settings,
                        has_premium=has_premium,
                        controller=controller,
                        progress=on_progress,
                        available_qualities=media.qualities,
                    )
            except (KeyboardInterrupt, asyncio.CancelledError):
                controller.pause()
                ctx.console.print("\n[yellow]Download paused again. Saved to resume list.[/]")
                break
            except Exception as exc:
                ctx.console.print(f"[red]Failed to resume {title}: {exc}[/]")
                continue

        if outcome.status == "completed":
            print_success(ctx.console, "Download Completed", f"Successfully saved to:\n[bold white]{outcome.path}[/]")
            store.remove(url)
            store.remove(target_path)
            clear_resume_state(target_path)
        elif outcome.status == "paused":
            ctx.console.print("[yellow]Paused and saved to resume list.[/]")

        await record_cli_download(
            ctx.settings,
            video=media if "media" in locals() and media is not None else source,
            outcome=outcome,
            target=target_path,
            quality=quality,
            origin_url=url,
            origin_name=title,
        )
