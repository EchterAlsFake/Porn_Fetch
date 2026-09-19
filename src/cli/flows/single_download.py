"""Interactive workflow for one video, gallery, or direct URL."""
from __future__ import annotations

import asyncio
from pathlib import Path

import questionary
from rich.panel import Panel
from rich.table import Table

from src.shared.media import quality_requires_premium, select_allowed_quality

from ..downloads import DownloadController, download_gallery, download_video, has_resume_state
from ..media import prepare_video
from ..output import output_path_for
from ..providers import ContentKind
from ..tracker import record_cli_download
from .context import WizardContext
from .ui import WIZARD_STYLE, make_download_progress, print_error, print_success


async def handle_download_single(ctx: WizardContext) -> None:
    """Prompt for a single URL, display metadata, select quality, and download."""
    url = await questionary.text(
        "Enter video, album, or direct URL:",
        validate=lambda val: True if val.strip().startswith(("http://", "https://")) else "Please enter a valid HTTP or HTTPS URL",
        style=WIZARD_STYLE,
    ).ask_async()
    if not url:
        return
    url = url.strip()

    try:
        with ctx.console.status("[bold green]Fetching metadata...[/]", spinner="dots"):
            route, source = await ctx.pool.resolve(url)
            if route.kind == ContentKind.GALLERY:
                media = None
                title = getattr(source, "title", None) or "Album"
                qualities: list[int] = []
            else:
                media = await prepare_video(source, route.provider)
                title = media.title
                qualities = media.qualities
    except Exception as error:
        report_id = await ctx.report(
            error, "fetch video metadata", "src.cli.wizard.handle_download_single",
            video_url=url,
        )
        print_error(ctx.console, "Metadata Fetch Failed", f"Could not retrieve details for {url}:\n{error}\nError ID: {report_id}")
        return

    # Display clean metadata summary table
    meta_table = Table(show_header=False, box=None, padding=(0, 1))
    meta_table.add_row("[bold cyan]Provider:[/]", route.provider.title())
    meta_table.add_row("[bold cyan]Content Type:[/]", route.kind.value.capitalize())
    meta_table.add_row("[bold cyan]Title:[/]", title)
    if media is not None:
        meta_table.add_row("[bold cyan]Author:[/]", media.author)
        dur = f"{media.length} min" if media.length is not None else "Unknown"
        meta_table.add_row("[bold cyan]Duration:[/]", dur)
        q_str = ", ".join(f"{q}p" for q in qualities) if qualities else "Auto"
        meta_table.add_row("[bold cyan]Available Qualities:[/]", q_str)
    ctx.console.print(Panel(meta_table, title="[bold #00e5ff]Media Preview[/]", border_style="#00e5ff"))

    # Quality selection
    has_premium = ctx.license_service.status.allowed
    if route.kind == ContentKind.GALLERY:
        selected_quality = "best"
    else:
        choices = [
            questionary.Choice(
                "🌟 best (Highest available quality)",
                value="best",
                disabled="Locked: Requires License" if not has_premium else None,
            ),
        ]
        for q in reversed(qualities):
            req_prem = quality_requires_premium(q)
            is_locked = req_prem and not has_premium
            choices.append(questionary.Choice(
                f"🎬 {q}p",
                value=str(q),
                disabled="Locked: Requires License" if is_locked else None,
            ))
        choices.extend([
            questionary.Choice("📻 audio only / worst video", value="worst"),
            questionary.Choice("🔙 Cancel", value="__cancel__"),
        ])

        default_val = "best" if has_premium else "720"
        available_str = [str(q) for q in qualities]
        if not has_premium:
            allowed = [q for q in available_str if not quality_requires_premium(q)]
            default_val = allowed[0] if allowed else ("720" if "720" in available_str else "worst")

        selected_quality = await questionary.select(
            "Select download quality:",
            choices=choices,
            default=default_val,
            style=WIZARD_STYLE,
        ).ask_async()
        if not selected_quality or selected_quality == "__cancel__":
            return

        if not has_premium and quality_requires_premium(selected_quality):
            print_error(
                ctx.console,
                "License Required",
                f"Quality '{selected_quality}' is locked. Qualities above 720p require an active license.",
            )
            return

    # Determine destination
    if media is not None:
        target = output_path_for(media, ctx.settings)
    else:
        target = Path(ctx.settings.output_path) / title

    if target.exists() and ctx.settings.skip_existing:
        ctx.console.print(f"[yellow]File already exists: {target} (skipped)[/]")
        return

    controller = DownloadController(
        url=url,
        target=target,
        title=title,
        quality=selected_quality,
        kind="video" if media is not None else "gallery",
        provider=route.provider,
    )
    if has_resume_state(target):
        ctx.console.print(f"[cyan]ℹ Found existing partial download for {title[:35]}. Resuming...[/]")

    # Start download with rich progress
    with make_download_progress(ctx.console) as progress:
        task_id = progress.add_task(f"Downloading {title[:35]}...", total=None)

        def on_progress(completed: int, total: int, unit: str = "items") -> None:
            progress.update(task_id, completed=completed, total=total if total > 0 else None, unit=unit)

        try:
            if media is None:
                outcome = await download_gallery(
                    source,
                    ctx.settings.output_path,
                    controller=controller,
                    progress=on_progress,
                    concurrency=ctx.settings.videos_concurrency,
                )
            else:
                eff_quality = select_allowed_quality(selected_quality, media.qualities, has_premium) or selected_quality
                outcome = await download_video(
                    source,
                    target,
                    eff_quality,
                    ctx.settings,
                    has_premium=has_premium,
                    controller=controller,
                    progress=on_progress,
                    available_qualities=media.qualities,
                )
        except (KeyboardInterrupt, asyncio.CancelledError):
            ctx.console.print("\n[yellow]Download interrupted.[/]")
            interrupt_choice = await questionary.select(
                "Choose action for interrupted download:",
                choices=[
                    questionary.Choice("⏸️  Pause and save progress (resume later)", value="pause"),
                    questionary.Choice("🗑️  Cancel and delete partial files", value="cancel_clean"),
                    questionary.Choice("❌ Cancel without deleting partial files", value="cancel"),
                ],
                style=WIZARD_STYLE,
            ).ask_async()
            if interrupt_choice == "pause":
                controller.pause()
                ctx.console.print("[yellow]⏸️  Download paused and progress saved. You can resume it from the Main Menu.[/]")
                return
            elif interrupt_choice == "cancel_clean":
                controller.cancel(cleanup=True)
                ctx.console.print("[red]Download cancelled and partial files purged.[/]")
                return
            else:
                controller.cancel(cleanup=False)
                ctx.console.print("[red]Download cancelled.[/]")
                return
        except Exception as error:
            report_id = await ctx.report(
                error, "download selected media", "src.cli.wizard.handle_download_single",
                video_url=url, provider=route.provider,
            )
            print_error(ctx.console, "Download Failed", f"{error}\nError ID: {report_id}")
            return

    if outcome.status == "completed":
        if media is not None and ctx.settings.write_metadata and not outcome.skipped and outcome.path.suffix.casefold() == ".mp4" and outcome.path.exists():
            try:
                from src.shared.metadata import write_tags
                write_tags(str(outcome.path), media)
            except Exception as error:
                await ctx.report(
                    error, "write downloaded video metadata",
                    "src.cli.wizard.handle_download_single",
                    video_url=getattr(media, "url", url), provider=route.provider,
                )
                ctx.console.print(f"[yellow]Metadata write warning: {error}[/]")
        print_success(
            ctx.console,
            "Download Completed",
            f"Successfully saved to:\n[bold white]{outcome.path}[/]",
        )
    elif outcome.status == "paused":
        ctx.console.print("[yellow]⏸️  Download paused and saved. You can resume it anytime from the Main Menu.[/]")
    elif outcome.status == "cancelled":
        ctx.console.print("[yellow]Download was cancelled.[/]")
    else:
        report_id = await ctx.report(
            RuntimeError(f"Downloader returned status {outcome.status}"),
            "download selected media", "src.cli.wizard.handle_download_single",
            video_url=url, provider=route.provider, quality=selected_quality,
        )
        print_error(
            ctx.console, "Download Incomplete",
            f"Status: {outcome.status}\nError ID: {report_id}",
        )

    await record_cli_download(
        ctx.settings,
        video=media if media is not None else source,
        outcome=outcome,
        target=outcome.path,
        quality=selected_quality,
        origin_url=url,
        origin_name=getattr(media, "author", "") or "Direct download",
    )
