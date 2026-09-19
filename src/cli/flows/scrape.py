"""Interactive profile and playlist discovery/download workflow."""
from __future__ import annotations

from typing import Any

import questionary
from rich.panel import Panel
from rich.table import Table

from src.shared.media import VideoObject, quality_requires_premium, select_allowed_quality

from ..downloads import download_gallery, download_video
from ..media import prepare_video
from ..output import output_path_for
from ..providers import ContentKind, Route, route_url
from ..tracker import record_cli_download
from .context import WizardContext
from .ui import WIZARD_STYLE, make_download_progress, print_error, print_success


async def handle_scrape_profile(ctx: WizardContext) -> None:
    """Prompt for profile/playlist URL or username, preview items, and download."""
    target_input = await questionary.text(
        "Enter profile / playlist URL (or model username):",
        style=WIZARD_STYLE,
    ).ask_async()
    if not target_input or not target_input.strip():
        return
    target_input = target_input.strip()

    if not target_input.startswith(("http://", "https://")):
        provider = await questionary.select(
            "Select provider for this username:",
            choices=[
                "pornhub", "xhamster", "xvideos", "eporner", "spankbang",
                "porntrex", "xnxx", "youporn", "redtube", "thumbzilla", "tube8",
            ],
            style=WIZARD_STYLE,
        ).ask_async()
        if not provider:
            return
        if provider == "pornhub":
            url = f"https://www.pornhub.com/model/{target_input}"
        elif provider == "xhamster":
            url = f"https://xhamster.com/creators/{target_input}"
        elif provider == "xvideos":
            url = f"https://www.xvideos.com/pornstars/{target_input}"
        elif provider == "eporner":
            url = f"https://www.eporner.com/pornstar/{target_input}/"
        elif provider == "spankbang":
            url = f"https://spankbang.com/pornstar/{target_input}"
        else:
            url = f"https://www.{provider}.com/pornstar/{target_input}"
    else:
        url = target_input

    # Multi-select for content types
    content_types = await questionary.checkbox(
        "Select content types to scrape:",
        choices=[
            questionary.Choice("Videos (full length)", value="videos", checked=True),
            questionary.Choice("Uploads / User videos", value="uploads", checked=False),
            questionary.Choice("Both (Videos & Uploads)", value="both", checked=False),
        ],
        style=WIZARD_STYLE,
    ).ask_async()
    if not content_types:
        content_types = ["videos"]
    mode = "both" if ("both" in content_types or ("videos" in content_types and "uploads" in content_types)) else ("uploads" if "uploads" in content_types else "videos")

    try:
        route = route_url(url)
    except Exception as error:
        print_error(ctx.console, "Invalid URL", str(error))
        return

    items: list[tuple[Route, Any, VideoObject | None]] = []
    with ctx.console.status(f"[bold green]Scraping {route.provider.title()} ({url})...[/]", spinner="dots"):
        ctx.pool.runtime_config.profile_video_mode = mode
        try:
            async for source in ctx.pool.media_stream(url, pages=5):
                media = None if route.kind == ContentKind.GALLERY else await prepare_video(source, route.provider)
                items.append((route, source, media))
                if len(items) >= ctx.settings.result_limit:
                    break
        except Exception as error:
            report_id = await ctx.report(
                error, "scrape profile or playlist", "src.cli.wizard.handle_scrape_profile",
                source_url=url, provider=route.provider,
            )
            print_error(ctx.console, "Scraping Failed", f"{error}\nError ID: {report_id}")
            return

    if not items:
        ctx.console.print(Panel("[yellow]No media items found for this profile or playlist.[/]", border_style="yellow"))
        return

    display_name = next(
        (
            str(media.author)
            for _item_route, _source, media in items
            if media is not None and media.author
        ),
        route.provider.title(),
    )

    # Display preview table [Index, Title, Duration, Quality]
    preview_table = Table(
        title=f"Discovered Content ({len(items)} items)",
        border_style="#00e5ff",
        header_style="bold #ff2a85",
    )
    preview_table.add_column("Index", style="bold cyan", justify="right")
    preview_table.add_column("Title", style="white", max_width=45, overflow="ellipsis")
    preview_table.add_column("Duration", style="magenta", justify="center")
    preview_table.add_column("Quality", style="green")

    for idx, (rt, src, med) in enumerate(items, 1):
        if med is None:
            preview_table.add_row(str(idx), getattr(src, "title", "Album"), "—", "Gallery")
        else:
            dur = f"{med.length} min" if med.length is not None else "—"
            q_str = ", ".join(f"{q}p" for q in med.qualities) if med.qualities else "Auto"
            preview_table.add_row(str(idx), med.title, dur, q_str)

    ctx.console.print(preview_table)

    # Prompt action: download all, select specific, track, or cancel
    action = await questionary.select(
        "Action for discovered items:",
        choices=[
            questionary.Choice(f"📥 Download All ({len(items)} items)", value="all"),
            questionary.Choice("🎯 Select specific items to download", value="select"),
            questionary.Choice("📋 Save model to Tracked Models database", value="track"),
            questionary.Choice("🔙 Back to Main Menu", value="cancel"),
        ],
        style=WIZARD_STYLE,
    ).ask_async()

    if not action or action == "cancel":
        return

    if action == "track":
        ctx.model_store.add(url)
        urls_to_track = [m.url for _, _, m in items if m and m.url]
        ctx.model_store.update_pending(url, urls_to_track)
        print_success(ctx.console, "Tracked", f"Added {url} to database with {len(urls_to_track)} pending items.")
        return

    if action == "all":
        selected_items = items
    else:
        item_choices = []
        for idx, (rt, src, med) in enumerate(items):
            item_title = med.title if med else getattr(src, "title", "Album")
            dur_str = f" ({med.length} min)" if med and med.length else ""
            item_choices.append(questionary.Choice(
                f"[{idx+1}] {item_title[:45]}{dur_str}",
                value=idx,
                checked=False,
            ))
        chosen_indices = await questionary.checkbox(
            "Select items (space to toggle, enter to proceed):",
            choices=item_choices,
            style=WIZARD_STYLE,
        ).ask_async()
        if not chosen_indices:
            ctx.console.print("[yellow]No items selected.[/]")
            return
        selected_items = [items[i] for i in chosen_indices]

    # Prompt quality override
    has_premium = ctx.license_service.status.allowed
    q_choices = []
    for q in ["best", "1080", "720", "480", "360", "worst"]:
        req_prem = quality_requires_premium(q)
        is_locked = req_prem and not has_premium
        title = f"🎬 {q}p" if q.isdigit() else f"🌟 {q}"
        q_choices.append(questionary.Choice(
            title=title,
            value=q,
            disabled="Locked: Requires License" if is_locked else None,
        ))

    default_q = ctx.settings.quality
    if not has_premium and quality_requires_premium(default_q):
        default_q = "720"

    quality_choice = await questionary.select(
        "Select quality for downloads:",
        choices=q_choices,
        default=default_q,
        style=WIZARD_STYLE,
    ).ask_async()
    if not quality_choice:
        return

    if not has_premium and quality_requires_premium(quality_choice):
        print_error(
            ctx.console,
            "License Required",
            f"Quality '{quality_choice}' is locked. Qualities above 720p require an active license.",
        )
        return
    completed_count = 0
    failed_count = 0

    with make_download_progress(ctx.console) as progress:
        overall_task = progress.add_task("[bold #ff2a85]Queue Progress[/]", total=len(selected_items))

        for rt, src, med in selected_items:
            item_title = med.title if med else getattr(src, "title", "Album")
            current_task = progress.add_task(f"Downloading {item_title[:30]}...", total=None)

            def on_item_progress(completed: int, total: int, unit: str = "items") -> None:
                progress.update(current_task, completed=completed, total=total if total > 0 else None, unit=unit)

            try:
                if med is None:
                    outcome = await download_gallery(
                        src,
                        ctx.settings.output_path,
                        progress=on_item_progress,
                        concurrency=ctx.settings.videos_concurrency,
                    )
                else:
                    target = output_path_for(med, ctx.settings)
                    eff_q = select_allowed_quality(quality_choice, med.qualities, has_premium) or quality_choice
                    outcome = await download_video(
                        src,
                        target,
                        eff_q,
                        ctx.settings,
                        has_premium=has_premium,
                        progress=on_item_progress,
                        available_qualities=med.qualities,
                    )
                if outcome.status == "completed":
                    completed_count += 1
                    if med and ctx.settings.write_metadata and not outcome.skipped and outcome.path.suffix.casefold() == ".mp4" and outcome.path.exists():
                        try:
                            from src.shared.metadata import write_tags
                            write_tags(str(outcome.path), med)
                        except Exception as error:
                            await ctx.report(
                                error,
                                "write download metadata",
                                "src.cli.flows.scrape.handle_scrape_profile",
                            )
                else:
                    failed_count += 1
                await record_cli_download(
                    ctx.settings,
                    video=med if med is not None else src,
                    outcome=outcome,
                    target=target if med is not None else ctx.settings.output_path,
                    quality=eff_q if med is not None else None,
                    origin_url=url,
                    origin_name=display_name,
                )
            except Exception as error:
                failed_count += 1
                await ctx.report(
                    error,
                    "download scraped item",
                    "src.cli.flows.scrape.handle_scrape_profile",
                    source_url=url,
                )
                if med is not None:
                    await record_cli_download(
                        ctx.settings,
                        video=med,
                        outcome="failed",
                        origin_url=url,
                        origin_name=display_name,
                    )
            finally:
                progress.remove_task(current_task)
                progress.advance(overall_task)

    ctx.console.print(Panel(
        f"[bold green]Completed:[/] {completed_count}\n"
        f"[bold red]Failed:[/] {failed_count}\n"
        f"[bold cyan]Total processed:[/] {len(selected_items)}",
        title="[bold #00e5ff]Queue Summary[/]",
        border_style="#00e5ff",
    ))
