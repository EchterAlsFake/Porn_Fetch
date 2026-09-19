"""Interactive tracked-model and queue management flow."""
from __future__ import annotations

import questionary
from rich.panel import Panel
from rich.table import Table

from src.shared.media import select_allowed_quality

from ..downloads import download_video
from ..media import prepare_video
from ..output import output_path_for
from ..tracker import record_cli_download
from .context import WizardContext
from .ui import WIZARD_STYLE, make_download_progress, print_success


async def handle_batch_management(ctx: WizardContext) -> None:
    """Review tracked models, scan for new URLs, and process pending queues."""
    while True:
        action = await questionary.select(
            "Batch & Queue Management:",
            choices=[
                questionary.Choice("📊 View Tracked Models & Status", value="view"),
                questionary.Choice("➕ Add Profile / Model URL to Track", value="add"),
                questionary.Choice("🔍 Scan Tracked Models for New Videos", value="scan"),
                questionary.Choice("⚡ Download All Pending Videos", value="download"),
                questionary.Choice("➖ Remove a Tracked Model", value="remove"),
                questionary.Choice("🔙 Back to Main Menu", value="back"),
            ],
            style=WIZARD_STYLE,
        ).ask_async()

        if not action or action == "back":
            break

        if action == "view":
            models = ctx.model_store.models()
            if not models:
                ctx.console.print(Panel("[yellow]No models are currently tracked.[/]", border_style="yellow"))
                continue
            table = Table(title="Tracked Profiles & Models", border_style="#00e5ff", header_style="bold #ff2a85")
            table.add_column("Profile / Model URL", style="white", overflow="ellipsis")
            table.add_column("Downloaded", style="green", justify="center")
            table.add_column("Pending", style="bold yellow", justify="center")
            table.add_column("Total", style="cyan", justify="center")
            for model_url, state in models:
                dl = len(state["downloaded"])
                pd = len(state["pending"])
                table.add_row(model_url, str(dl), str(pd), str(dl + pd))
            ctx.console.print(table)

        elif action == "add":
            url = await questionary.text("Enter model / profile URL to track:", style=WIZARD_STYLE).ask_async()
            if url and url.strip():
                if ctx.model_store.add(url.strip()):
                    print_success(ctx.console, "Added", f"Added {url.strip()} to tracked database.")
                else:
                    ctx.console.print(f"[yellow]{url.strip()} is already being tracked.[/]")

        elif action == "remove":
            models = ctx.model_store.models()
            if not models:
                ctx.console.print("[yellow]No models available to remove.[/]")
                continue
            choices = [questionary.Choice(url, value=url) for url, _ in models]
            choices.append(questionary.Choice("🔙 Cancel", value="__cancel__"))
            target = await questionary.select("Select model to remove:", choices=choices, style=WIZARD_STYLE).ask_async()
            if target and target != "__cancel__":
                ctx.model_store.remove(target)
                print_success(ctx.console, "Removed", f"Removed {target} from tracked database.")

        elif action == "scan":
            models = ctx.model_store.models()
            if not models:
                ctx.console.print("[yellow]No tracked models found to scan.[/]")
                continue
            scan_table = Table(title="Scan Results", border_style="#00e5ff", header_style="bold #ff2a85")
            scan_table.add_column("Model URL", style="white")
            scan_table.add_column("New Pending Discovered", style="bold green", justify="center")

            with ctx.console.status("[bold green]Scanning tracked models for new videos...[/]", spinner="dots"):
                for model_url, _ in models:
                    found_urls: list[str] = []
                    try:
                        async for video in ctx.pool.media_stream(model_url, pages=5):
                            v_url = getattr(video, "url", None)
                            if v_url:
                                found_urls.append(str(v_url))
                        added = ctx.model_store.update_pending(model_url, found_urls)
                        scan_table.add_row(model_url, str(added))
                    except Exception as error:
                        await ctx.report(
                            error, "scan tracked model", "src.cli.wizard.handle_batch_management",
                            model_url=model_url,
                        )
                        scan_table.add_row(model_url, f"[red]Error: {error}[/]")
            ctx.console.print(scan_table)

        elif action == "download":
            models = ctx.model_store.models()
            total_pending = sum(len(state["pending"]) for _, state in models)
            if total_pending == 0:
                ctx.console.print(Panel("[yellow]No pending videos to download.[/]", border_style="yellow"))
                continue
            confirm = await questionary.confirm(
                f"Download all {total_pending} pending videos across {len(models)} tracked models?",
                default=True,
                style=WIZARD_STYLE,
            ).ask_async()
            if not confirm:
                continue

            has_premium = ctx.license_service.status.allowed
            success_count = 0
            fail_count = 0

            with make_download_progress(ctx.console) as progress:
                overall_task = progress.add_task("[bold #ff2a85]Downloading Pending...[/]", total=total_pending)
                for model_url, state in models:
                    for pending_url in list(state["pending"]):
                        task_id = progress.add_task(f"Downloading {pending_url[:30]}...", total=None)

                        def on_pending_progress(completed: int, total: int, unit: str = "items") -> None:
                            progress.update(task_id, completed=completed, total=total if total > 0 else None, unit=unit)

                        try:
                            route, source = await ctx.pool.resolve(pending_url)
                            media = await prepare_video(source, route.provider)
                            eff_q = select_allowed_quality(ctx.settings.quality, media.qualities, has_premium) or ctx.settings.quality
                            target = output_path_for(media, ctx.settings)
                            outcome = await download_video(
                                source,
                                target,
                                eff_q,
                                ctx.settings,
                                has_premium=has_premium,
                                progress=on_pending_progress,
                                available_qualities=media.qualities,
                            )
                            if outcome.status == "completed":
                                success_count += 1
                                ctx.model_store.mark_downloaded(model_url, pending_url)
                                if ctx.settings.write_metadata and not outcome.skipped and outcome.path.suffix.casefold() == ".mp4" and outcome.path.exists():
                                    try:
                                        from src.shared.metadata import write_tags
                                        write_tags(str(outcome.path), media)
                                    except Exception as error:
                                        await ctx.report(
                                            error,
                                            "write download metadata",
                                            "src.cli.flows.models.handle_batch_management",
                                        )
                            else:
                                fail_count += 1
                            await record_cli_download(
                                ctx.settings,
                                video=media,
                                outcome=outcome,
                                target=target,
                                quality=eff_q,
                                origin_url=model_url,
                                origin_name=model_url,
                            )
                        except Exception as error:
                            fail_count += 1
                            await ctx.report(
                                error,
                                "download tracked video",
                                "src.cli.flows.models.handle_batch_management",
                                video_url=pending_url,
                                model_url=model_url,
                            )
                            if "media" in locals() and media is not None:
                                await record_cli_download(
                                    ctx.settings,
                                    video=media,
                                    outcome="failed",
                                    origin_url=model_url,
                                    origin_name=model_url,
                                )
                        finally:
                            progress.remove_task(task_id)
                            progress.advance(overall_task)

            ctx.console.print(Panel(
                f"[bold green]Completed:[/] {success_count}\n"
                f"[bold red]Failed:[/] {fail_count}\n"
                f"[bold cyan]Total Pending Processed:[/] {total_pending}",
                title="Batch Download Summary",
                border_style="#00e5ff",
            ))
