"""Modern interactive terminal wizard for Porn Fetch using questionary and rich."""
from __future__ import annotations

import asyncio
from dataclasses import fields, replace
from datetime import datetime, timezone
import inspect
import json
from pathlib import Path
import re
import sys
from typing import Any, Callable

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    ProgressColumn,
    Task,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.table import Table
from rich.text import Text

from src.backend.media import VideoObject, quality_requires_premium, select_allowed_quality
from src.backend.error_reporting import report_exception
from .accounts import AccountService
from .downloads import DownloadOutcome, download_gallery, download_video
from .licensing import LicenseService, create_license_service
from .media import prepare_video
from .model_store import ModelStore
from .output import output_path_for
from .providers import ClientPool, ContentKind, Route, route_url, unwrap_scrape_result
from .settings import CliSettings, SettingsStore, prompt_error_reporting_consent


# Custom prompt style matching the pink (#ff2a85) & cyan (#00e5ff) aesthetic of Porn Fetch QML
WIZARD_STYLE = questionary.Style([
    ("qmark", "fg:#00e5ff bold"),
    ("question", "bold"),
    ("answer", "fg:#ff2a85 bold"),
    ("pointer", "fg:#ff2a85 bold"),
    ("highlighted", "fg:#00e5ff bold"),
    ("selected", "fg:#ff2a85"),
    ("separator", "fg:#6c757d"),
    ("instruction", "fg:#6c757d italic"),
    ("text", ""),
    ("disabled", "fg:#858585 italic"),
])


class SmartUnitsColumn(ProgressColumn):
    """Render download totals according to their explicit progress unit."""

    def render(self, task: Task) -> Text:
        if task.total is None:
            return Text("...", style="dim")
        unit = getattr(task, "fields", {}).get("unit")
        if unit == "bytes" or (unit is None and task.total > 50_000):
            completed_mb = task.completed / (1024 * 1024)
            total_mb = task.total / (1024 * 1024)
            return Text(f"{completed_mb:.1f} / {total_mb:.1f} MB", style="cyan")
        if unit == "segments":
            return Text(f"{int(task.completed)} / {int(task.total)} segments", style="cyan")
        return Text(f"{int(task.completed)} / {int(task.total)} items", style="cyan")


class DownloadSpeedColumn(ProgressColumn):
    """Render byte rates for RAW downloads and segment rates for HLS downloads."""

    def __init__(self) -> None:
        super().__init__()
        self._transfer_speed = TransferSpeedColumn()

    def render(self, task: Task) -> Text:
        unit = getattr(task, "fields", {}).get("unit")
        if unit in {None, "bytes"}:
            return self._transfer_speed.render(task)

        label = "segments" if unit == "segments" else "items"
        speed = task.finished_speed or task.speed
        if speed is None:
            return Text(f"? {label}/sec", style="dim")
        return Text(f"{speed:.1f} {label}/sec", style="green")


def make_download_progress(console: Console) -> Progress:
    """Build a rich progress bar with a unit-aware rate and ETA."""
    return Progress(
        TextColumn("[bold cyan]{task.description}[/]"),
        BarColumn(bar_width=None, complete_style="#ff2a85", finished_style="bold green"),
        TaskProgressColumn(),
        SmartUnitsColumn(),
        DownloadSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
    )


def print_banner(console: Console, license_state: str | None = None) -> None:
    """Render a compact, styled header panel without clearing scrollback."""
    banner = Text()
    banner.append("⚡ ", style="bold #00e5ff")
    banner.append("PORN FETCH", style="bold #ff2a85")
    banner.append(" CLI ", style="bold #00e5ff")
    banner.append("v3.9", style="dim")
    if license_state:
        state_clean = license_state.replace("_", " ").title()
        if license_state.lower() in {"valid", "active"}:
            banner.append("  •  [Premium: Active]", style="bold green")
        elif license_state.lower() in {"provisional", "offline_grace"}:
            banner.append(f"  •  [License: {state_clean}]", style="bold yellow")
        else:
            banner.append(f"  •  [License: {state_clean}]", style="dim")

    panel = Panel(
        banner,
        subtitle="[dim]Modern Interactive Terminal Wizard[/]",
        border_style="#ff2a85",
        padding=(0, 2),
    )
    console.print(panel)


def print_error(console: Console, title: str, message: str) -> None:
    """Print a neat error panel for caught exceptions."""
    console.print(Panel(
        f"[bold red]{message}[/]",
        title=f"[bold red]{title}[/]",
        border_style="red",
        padding=(0, 2),
    ))


def print_success(console: Console, title: str, message: str) -> None:
    """Print a styled success panel."""
    console.print(Panel(
        f"[bold green]{message}[/]",
        title=f"[bold green]{title}[/]",
        border_style="green",
        padding=(0, 2),
    ))


class WizardContext:
    """Session context managing settings, active client pool, licensing, and accounts."""

    def __init__(
        self,
        settings: CliSettings,
        settings_store: SettingsStore,
        console: Console | None = None,
        *,
        model_store: ModelStore | None = None,
        pool: ClientPool | None = None,
        license_service: LicenseService | None = None,
    ) -> None:
        self.settings = settings
        self.settings_store = settings_store
        self.console = console or Console()
        self.model_store = model_store or ModelStore()
        config = self.settings.to_runtime_config()
        self.pool = pool or ClientPool(config)
        self.license_service = license_service or create_license_service(config)
        self.account_service = AccountService(self.pool)

    async def check_license(self, force: bool = False) -> Any:
        try:
            return await self.license_service.check(force=force)
        except Exception:
            return self.license_service.status

    async def report(
        self, error: BaseException, operation: str, location: str, **context: Any,
    ) -> str:
        return await report_exception(
            error,
            operation=operation,
            location=location,
            context=context,
            enabled=self.settings.error_reporting,
        )

    async def refresh_pool(self) -> None:
        """Rebuild client pool and license service when settings change."""
        old_pool = self.pool
        old_lic = self.license_service
        config = self.settings.to_runtime_config()
        self.pool = ClientPool(config)
        self.license_service = create_license_service(config)
        await self.check_license()
        self.account_service = AccountService(self.pool)
        await old_lic.close()
        await old_pool.close()

    async def close(self) -> None:
        try:
            await self.license_service.close()
        except Exception:
            pass
        try:
            await self.pool.close()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Sub-Flow 1: Download Single URL
# ---------------------------------------------------------------------------

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

    # Start download with rich progress
    stop_event = asyncio.Event()
    with make_download_progress(ctx.console) as progress:
        task_id = progress.add_task(f"Downloading {title[:35]}...", total=None)

        def on_progress(completed: int, total: int, unit: str = "items") -> None:
            progress.update(task_id, completed=completed, total=total if total > 0 else None, unit=unit)

        try:
            if media is None:
                outcome = await download_gallery(
                    source,
                    ctx.settings.output_path,
                    stop_event=stop_event,
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
                    stop_event=stop_event,
                    progress=on_progress,
                    available_qualities=media.qualities,
                )
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
                from src.backend.metadata import write_tags
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


# ---------------------------------------------------------------------------
# Sub-Flow 2: Scrape Profile / Playlist
# ---------------------------------------------------------------------------

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
        overall_task = progress.add_task(f"[bold #ff2a85]Queue Progress[/]", total=len(selected_items))

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
                            from src.backend.metadata import write_tags
                            write_tags(str(outcome.path), med)
                        except Exception:
                            pass
                else:
                    failed_count += 1
            except Exception:
                failed_count += 1
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


# ---------------------------------------------------------------------------
# Sub-Flow 3: Batch / Queue Management
# ---------------------------------------------------------------------------

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
                                        from src.backend.metadata import write_tags
                                        write_tags(str(outcome.path), media)
                                    except Exception:
                                        pass
                            else:
                                fail_count += 1
                        except Exception:
                            fail_count += 1
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


# ---------------------------------------------------------------------------
# Sub-Flow 4: Account & Authentication
# ---------------------------------------------------------------------------

async def handle_account_auth(ctx: WizardContext) -> None:
    """Handle site logins, browser cookie discovery, and account collection downloads."""
    while True:
        action = await questionary.select(
            "Account & Authentication:",
            choices=[
                questionary.Choice("🔑 Enter Credentials (Username / Password / Tokens)", value="credentials"),
                questionary.Choice("🍪 Load Browser Cookies (Chrome, Firefox, Brave, etc.)", value="cookies"),
                questionary.Choice("📋 View Account Login Status", value="status"),
                questionary.Choice("📥 Fetch Account Collection (Favorites, Liked, etc.)", value="collections"),
                questionary.Choice("🔙 Back to Main Menu", value="back"),
            ],
            style=WIZARD_STYLE,
        ).ask_async()

        if not action or action == "back":
            break

        if action == "status":
            table = Table(title="Account Login Status", border_style="#00e5ff", header_style="bold #ff2a85")
            table.add_column("Provider", style="bold cyan")
            table.add_column("Status", justify="center")
            for prov in ("PornHub", "XHamster", "XVideos"):
                logged = ctx.account_service.logged_in(prov)
                table.add_row(prov, "[bold green]Logged In[/]" if logged else "[dim]Not Logged In[/]")
            ctx.console.print(table)

        elif action == "credentials":
            provider = await questionary.select(
                "Select provider to authenticate:",
                choices=["PornHub", "XHamster", "XVideos", "Cancel"],
                style=WIZARD_STYLE,
            ).ask_async()
            if not provider or provider == "Cancel":
                continue

            if provider == "XVideos":
                token = await questionary.password("Enter XVideos session_token:", style=WIZARD_STYLE).ask_async()
                token_auth = await questionary.password("Enter XVideos session_token_auth:", style=WIZARD_STYLE).ask_async()
                if not token or not token_auth:
                    continue
                with ctx.console.status("[bold green]Authenticating XVideos tokens...[/]", spinner="dots"):
                    try:
                        ok = await ctx.account_service.login(
                            provider,
                            tokens={"session_token": token, "session_token_auth": token_auth},
                        )
                        if ok:
                            print_success(ctx.console, "Authentication", "Successfully authenticated XVideos tokens!")
                        else:
                            print_error(ctx.console, "Authentication Failed", "XVideos session tokens were rejected.")
                    except Exception as error:
                        await ctx.report(
                            error, "authenticate with session tokens",
                            "src.cli.wizard.handle_account_auth", provider=provider,
                        )
                        print_error(ctx.console, "Authentication Error", str(error))
            else:
                user = await questionary.text(f"Enter {provider} username or email:", style=WIZARD_STYLE).ask_async()
                secret = await questionary.password(f"Enter {provider} password:", style=WIZARD_STYLE).ask_async()
                if not user or not secret:
                    continue
                with ctx.console.status(f"[bold green]Logging in to {provider}...[/]", spinner="dots"):
                    try:
                        ok = await ctx.account_service.login(provider, username=user, password=secret)
                        if ok:
                            print_success(ctx.console, "Authentication", f"Successfully logged in to {provider}!")
                        else:
                            print_error(ctx.console, "Authentication Failed", f"Credentials rejected by {provider}.")
                    except Exception as error:
                        await ctx.report(
                            error, "authenticate with username", "src.cli.wizard.handle_account_auth",
                            provider=provider,
                        )
                        print_error(ctx.console, "Authentication Error", str(error))

        elif action == "cookies":
            provider = await questionary.select(
                "Select provider to import browser cookies:",
                choices=["PornHub", "XHamster", "XVideos", "Cancel"],
                style=WIZARD_STYLE,
            ).ask_async()
            if not provider or provider == "Cancel":
                continue
            with ctx.console.status(f"[bold green]Importing browser cookies for {provider}...[/]", spinner="dots"):
                try:
                    ok = await ctx.account_service.login(provider, browser=True)
                    if ok:
                        print_success(ctx.console, "Cookie Import", f"Successfully logged into {provider} with browser cookies!")
                    else:
                        print_error(ctx.console, "Cookie Import Failed", f"No valid session cookies found for {provider}.")
                except Exception as error:
                    await ctx.report(
                        error, "import browser authentication", "src.cli.wizard.handle_account_auth",
                        provider=provider,
                    )
                    print_error(ctx.console, "Cookie Import Error", str(error))

        elif action == "collections":
            logged_providers = [p for p in ("PornHub", "XHamster", "XVideos") if ctx.account_service.logged_in(p)]
            if not logged_providers:
                ctx.console.print(Panel("[yellow]Please log in to an account first.[/]", border_style="yellow"))
                continue
            prov = await questionary.select("Select account provider:", choices=logged_providers, style=WIZARD_STYLE).ask_async()
            if not prov:
                continue

            col_choices = {
                "PornHub": ["history", "recommended", "favorites"],
                "XHamster": ["liked", "playlist"],
                "XVideos": ["watch_later", "recommended", "liked"],
            }[prov]
            selected_col = await questionary.select(f"Select {prov} collection:", choices=col_choices, style=WIZARD_STYLE).ask_async()
            if not selected_col:
                continue

            playlist_url = ""
            if prov == "XHamster" and selected_col == "playlist":
                playlist_url = await questionary.text("Enter authenticated XHamster playlist URL:", style=WIZARD_STYLE).ask_async() or ""

            items: list[tuple[Route, Any, VideoObject | None]] = []
            with ctx.console.status(f"[bold green]Fetching {prov} {selected_col}...[/]", spinner="dots"):
                try:
                    stream, label = ctx.account_service.collection(prov, selected_col, playlist_url)
                    route = Route(prov.casefold(), ContentKind.COLLECTION, playlist_url or f"https://{prov.casefold()}.com/account")
                    async for result in stream:
                        source = unwrap_scrape_result(result)
                        media = await prepare_video(source, prov.casefold())
                        items.append((route, source, media))
                        if len(items) >= ctx.settings.result_limit:
                            break
                except Exception as error:
                    await ctx.report(
                        error, "fetch account collection", "src.cli.wizard.handle_account_auth",
                        provider=prov, collection=selected_col, playlist_url=playlist_url,
                    )
                    print_error(ctx.console, "Collection Fetch Failed", str(error))
                    continue

            if not items:
                ctx.console.print("[yellow]No items in this collection.[/]")
                continue

            col_table = Table(title=f"{prov} {selected_col.title()} ({len(items)} items)", border_style="#00e5ff", header_style="bold #ff2a85")
            col_table.add_column("Index", style="cyan", justify="right")
            col_table.add_column("Title", style="white")
            col_table.add_column("Duration", style="magenta")
            for idx, (_, _, med) in enumerate(items, 1):
                col_table.add_row(str(idx), med.title if med else "Item", f"{med.length} min" if med and med.length else "—")
            ctx.console.print(col_table)


# ---------------------------------------------------------------------------
# Sub-Flow 5: Settings & Configuration
# ---------------------------------------------------------------------------

SETTINGS_METADATA: dict[str, tuple[str, str]] = {
    # Video
    "quality": ("Video", "Preferred download quality (best, 1080, 720, worst)"),
    "output_path": ("Video", "Output directory for media files"),
    "path_template": ("Video", "Naming template for media files ($title, $author, $video_id)"),
    "result_limit": ("Video", "Max search or scrape result count"),
    "skip_existing": ("Video", "Skip downloads if file exists"),
    "write_metadata": ("Video", "Embed metadata tags in downloaded MP4 files"),
    "profile_video_mode": ("Video", "Scrape mode: videos, uploads, or both"),
    "locale": ("Video", "Preferred language / locale (e.g. en-US, de-DE)"),
    "strict_language": ("Video", "Strictly enforce language headers"),
    # Performance
    "parallel_downloads": ("Performance", "Simultaneous active downloads"),
    "download_workers": ("Performance", "Concurrent chunk/segment workers"),
    "timeout": ("Performance", "Network request timeout (seconds)"),
    "request_attempts": ("Performance", "Number of request retry attempts"),
    "bandwidth_limit_mb": ("Performance", "Bandwidth speed limit in MB/s (0 = unlimited)"),
    "processing_delay": ("Performance", "Delay between dispatches (seconds)"),
    # Network / Privacy
    "proxy": ("Network", "Proxy URL (http:// or socks5://)"),
    "http_version": ("Network", "HTTP protocol version (v1, v2, v3)"),
    "ip_preference": ("Network", "IP version preference (auto, ipv4, ipv6)"),
    "impersonation": ("Network", "TLS fingerprint impersonation (chrome, safari)"),
    "dns_over_https": ("Network", "Use DNS-over-HTTPS resolver"),
    "verify_ssl": ("Network", "Verify TLS/SSL certificates"),
    # Logging
    "log_level": ("Logging", "Logging verbosity (DEBUG, INFO, WARNING, ERROR)"),
    "debug": ("Logging", "Enable detailed diagnostic logs"),
}


async def handle_settings(ctx: WizardContext) -> None:
    """Display configuration table, allow inline editing, and persist changes."""
    while True:
        action = await questionary.select(
            "Settings & Configuration:",
            choices=[
                questionary.Choice("📄 View All Settings", value="view"),
                questionary.Choice("✏️  Modify a Setting", value="edit"),
                questionary.Choice("🔄 Reset to Default Settings", value="reset"),
                questionary.Choice("🔙 Back to Main Menu", value="back"),
            ],
            style=WIZARD_STYLE,
        ).ask_async()

        if not action or action == "back":
            break

        if action == "view":
            table = Table(title="Configuration Settings", border_style="#00e5ff", header_style="bold #ff2a85")
            table.add_column("Category", style="bold cyan")
            table.add_column("Setting", style="bold white")
            table.add_column("Value", style="bold green")
            table.add_column("Description", style="dim")

            has_premium = ctx.license_service.status.allowed
            for name, (category, desc) in SETTINGS_METADATA.items():
                val = getattr(ctx.settings, name, "")
                val_str = str(val)
                if name == "quality" and not has_premium and quality_requires_premium(val_str):
                    val_str = f"{val_str} [bold yellow](Locked: Free tier <=720p)[/]"
                table.add_row(category, name, val_str, desc)
            ctx.console.print(table)

        elif action == "reset":
            confirm = await questionary.confirm("Reset all settings to defaults?", default=False, style=WIZARD_STYLE).ask_async()
            if confirm:
                defaults = CliSettings()
                ctx.settings_store.save(defaults)
                ctx.settings = defaults
                await ctx.refresh_pool()
                print_success(ctx.console, "Reset Settings", "Settings restored to defaults.")

        elif action == "edit":
            has_premium = ctx.license_service.status.allowed
            choices = []
            for name, (category, desc) in SETTINGS_METADATA.items():
                current_val = getattr(ctx.settings, name)
                tag = ""
                if name == "quality" and not has_premium and quality_requires_premium(str(current_val)):
                    tag = " (Locked: >720p requires license)"
                choices.append(questionary.Choice(
                    f"[{category}] {name} = {current_val}{tag}",
                    value=name,
                ))
            choices.append(questionary.Choice("🔙 Cancel", value="__cancel__"))

            target_setting = await questionary.select(
                "Select a setting to modify:",
                choices=choices,
                style=WIZARD_STYLE,
            ).ask_async()

            if not target_setting or target_setting == "__cancel__":
                continue

            current_val = getattr(ctx.settings, target_setting)
            new_val: Any = None

            if isinstance(current_val, bool):
                new_val = await questionary.confirm(f"Enable {target_setting}?", default=current_val, style=WIZARD_STYLE).ask_async()
            elif target_setting == "quality":
                has_premium = ctx.license_service.status.allowed
                qualities_list = ["best", "2160", "1440", "1080", "720", "480", "360", "worst"]
                quality_choices = []
                for q in qualities_list:
                    req_prem = quality_requires_premium(q)
                    is_locked = req_prem and not has_premium
                    disabled_msg = "Locked: Requires License" if is_locked else None
                    title = f"🎬 {q}p" if q.isdigit() else f"🌟 {q}"
                    quality_choices.append(questionary.Choice(
                        title=title,
                        value=q,
                        disabled=disabled_msg,
                    ))

                default_val = str(current_val)
                if not has_premium and quality_requires_premium(default_val):
                    default_val = "720"

                new_val = await questionary.select(
                    "Select preferred quality:",
                    choices=quality_choices,
                    default=default_val,
                    style=WIZARD_STYLE,
                ).ask_async()

                if new_val and not has_premium and quality_requires_premium(new_val):
                    print_error(
                        ctx.console,
                        "License Required",
                        f"Quality '{new_val}' is locked. Qualities above 720p require an active license.",
                    )
                    new_val = None
            elif target_setting == "profile_video_mode":
                new_val = await questionary.select("Select profile mode:", choices=["videos", "uploads", "both"], default=current_val, style=WIZARD_STYLE).ask_async()
            elif target_setting == "http_version":
                new_val = await questionary.select("Select HTTP version:", choices=["v1", "v2", "v3"], default=current_val, style=WIZARD_STYLE).ask_async()
            elif target_setting == "ip_preference":
                new_val = await questionary.select("Select IP preference:", choices=["auto", "ipv4", "ipv6"], default=current_val, style=WIZARD_STYLE).ask_async()
            elif target_setting == "log_level":
                new_val = await questionary.select("Select log level:", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default=current_val, style=WIZARD_STYLE).ask_async()
            elif isinstance(current_val, int):
                raw = await questionary.text(
                    f"Enter new integer value for {target_setting}:",
                    default=str(current_val),
                    validate=lambda val: True if val.strip().isdigit() else "Please enter a valid positive integer",
                    style=WIZARD_STYLE,
                ).ask_async()
                if raw is not None:
                    new_val = int(raw.strip())
            elif isinstance(current_val, float):
                raw = await questionary.text(
                    f"Enter new float value for {target_setting}:",
                    default=str(current_val),
                    validate=lambda val: True if re.match(r"^\d+(\.\d+)?$", val.strip()) else "Please enter a valid number",
                    style=WIZARD_STYLE,
                ).ask_async()
                if raw is not None:
                    new_val = float(raw.strip())
            else:
                raw = await questionary.text(
                    f"Enter new value for {target_setting}:",
                    default=str(current_val),
                    style=WIZARD_STYLE,
                ).ask_async()
                if raw is not None:
                    new_val = raw.strip()

            if new_val is not None:
                if target_setting == "quality" and not ctx.license_service.status.allowed and quality_requires_premium(str(new_val)):
                    print_error(
                        ctx.console,
                        "License Required",
                        f"Quality '{new_val}' is locked. Qualities above 720p require an active license.",
                    )
                    continue
                try:
                    updated = replace(ctx.settings, **{target_setting: new_val})
                    updated.validate()
                    ctx.settings_store.save(updated)
                    ctx.settings = updated
                    await ctx.refresh_pool()
                    print_success(ctx.console, "Setting Updated", f"Set [bold cyan]{target_setting}[/] = [bold white]{new_val}[/]")
                except Exception as error:
                    print_error(ctx.console, "Validation Error", str(error))


# ---------------------------------------------------------------------------
# Sub-Flow 6: License Management
# ---------------------------------------------------------------------------

async def handle_license_management(ctx: WizardContext) -> None:
    """Check license validity, import schema-2 keys/files, and deactivate."""
    while True:
        action = await questionary.select(
            "License Management:",
            choices=[
                questionary.Choice("🔍 Check / Refresh License Status", value="check"),
                questionary.Choice("📥 Import License Key / File", value="import"),
                questionary.Choice("⚠️  Deactivate Current License", value="deactivate"),
                questionary.Choice("🔙 Back to Main Menu", value="back"),
            ],
            style=WIZARD_STYLE,
        ).ask_async()

        if not action or action == "back":
            break

        if action == "check":
            with ctx.console.status("[bold green]Checking license status with server...[/]", spinner="dots"):
                status = await ctx.check_license(force=True)

            expiry = "—"
            if status.expires_at is not None:
                expiry = datetime.fromtimestamp(status.expires_at, tz=timezone.utc).astimezone().isoformat(timespec="minutes")

            table = Table(show_header=False, box=None, padding=(0, 1))
            table.add_row("[bold cyan]State:[/]", f"[bold green]{status.state}[/]" if status.allowed else f"[bold yellow]{status.state}[/]")
            table.add_row("[bold cyan]Description:[/]", ctx.license_service.reason)
            table.add_row("[bold cyan]Features:[/]", "[bold green]Premium unlocked (1080p+, fast downloads)[/]" if status.allowed else "[dim]Standard free tier (<=720p)[/]")
            table.add_row("[bold cyan]Expires:[/]", expiry)

            border = "green" if status.allowed else "yellow"
            ctx.console.print(Panel(table, title="[bold #00e5ff]License Information[/]", border_style=border))

        elif action == "import":
            path_or_key = await questionary.text(
                "Enter path to schema-2 license file (or paste JSON license):",
                style=WIZARD_STYLE,
            ).ask_async()
            if not path_or_key or not path_or_key.strip():
                continue
            path_or_key = path_or_key.strip()

            with ctx.console.status("[bold green]Importing and verifying license...[/]", spinner="dots"):
                try:
                    if Path(path_or_key).is_file():
                        status = await ctx.license_service.import_file(path_or_key)
                    else:
                        status = await ctx.license_service.client.import_license(path_or_key)
                        ctx.license_service.status = status
                    print_success(
                        ctx.console,
                        "License Imported",
                        f"Status: [bold white]{status.state}[/]\n{ctx.license_service.reason}",
                    )
                except Exception as error:
                    print_error(ctx.console, "License Import Failed", str(error))

        elif action == "deactivate":
            confirm = await questionary.confirm(
                "Are you sure you want to deactivate the license on this device?",
                default=False,
                style=WIZARD_STYLE,
            ).ask_async()
            if not confirm:
                continue

            with ctx.console.status("[bold green]Deactivating license...[/]", spinner="dots"):
                try:
                    status = await ctx.license_service.deactivate()
                    print_success(ctx.console, "License Deactivated", f"State: {status.state}\n{ctx.license_service.reason}")
                except Exception as error:
                    print_error(ctx.console, "Deactivation Error", str(error))


# ---------------------------------------------------------------------------
# Main Interactive Wizard Loop
# ---------------------------------------------------------------------------

async def run_wizard(args: Any = None) -> int:
    """Launch the main scrollback-preserving interactive terminal wizard."""
    console = Console()
    store = SettingsStore()
    settings = store.load()

    explicit_reporting_choice = (
        getattr(args, "error_reporting", None) if args is not None else None
    )
    if explicit_reporting_choice is not None:
        settings = settings.overridden(
            error_reporting=explicit_reporting_choice,
            error_reporting_decided=True,
        )
        store.save(settings)
    elif not settings.error_reporting_decided:
        settings = await prompt_error_reporting_consent(settings, store, console=console)

    # Apply overrides from command-line arguments if provided
    overrides: dict[str, Any] = {}
    if args is not None:
        if getattr(args, "quality", None):
            overrides["quality"] = args.quality
        if getattr(args, "output", None):
            overrides["output_path"] = args.output
    if overrides:
        settings = settings.overridden(**overrides)

    ctx = WizardContext(settings, store, console)
    await ctx.check_license()

    try:
        while True:
            console.print()
            print_banner(console, license_state=ctx.license_service.status.state)
            console.print()

            action = await questionary.select(
                "Main Menu (use arrow keys to navigate):",
                choices=[
                    questionary.Choice("📥 Download Single URL (Video, album, or direct link)", value="single"),
                    questionary.Choice("👤 Scrape Profile / Playlist (Fetch model or playlist content)", value="scrape"),
                    questionary.Choice("📋 Batch / Queue Management (Review tracked models or queued links)", value="batch"),
                    questionary.Choice("🔑 Account & Authentication (Login credentials, browser cookie import)", value="auth"),
                    questionary.Choice("⚙️  Settings & Configuration (Output path, naming templates, preferred quality)", value="settings"),
                    questionary.Choice("📜 License Management (Check status, import key/file, deactivate)", value="license"),
                    questionary.Choice("❌ Exit", value="exit"),
                ],
                style=WIZARD_STYLE,
            ).ask_async()

            if action in {None, "exit"}:
                break

            try:
                if action == "single":
                    await handle_download_single(ctx)
                elif action == "scrape":
                    await handle_scrape_profile(ctx)
                elif action == "batch":
                    await handle_batch_management(ctx)
                elif action == "auth":
                    await handle_account_auth(ctx)
                elif action == "settings":
                    await handle_settings(ctx)
                elif action == "license":
                    await handle_license_management(ctx)
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
