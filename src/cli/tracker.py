"""PocketBase tracking and statistics integration for the Porn Fetch CLI."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from src.backend.database import PocketBaseError, PocketBaseTracker
from src.backend.media import VideoObject
from .downloads import DownloadOutcome
from .settings import CliSettings

logger = logging.getLogger(__name__)

_CLI_TRACKER: PocketBaseTracker | None = None
_CLI_TRACKER_KEY: tuple[str, bool, str, str] | None = None


def get_cli_tracker(settings: CliSettings) -> PocketBaseTracker:
    """Return the shared PocketBaseTracker configured with *settings*."""
    global _CLI_TRACKER, _CLI_TRACKER_KEY
    key = (
        str(Path(settings.pocketbase_data_path).resolve()),
        bool(settings.track_videos),
        str(settings.pocketbase_binary or ""),
        str(Path(settings.legacy_database_path).resolve()),
    )
    if _CLI_TRACKER is None or _CLI_TRACKER_KEY != key:
        _CLI_TRACKER = PocketBaseTracker(
            data_path=settings.pocketbase_data_path,
            enabled=settings.track_videos,
            binary_path=settings.pocketbase_binary or None,
            legacy_sqlite_path=settings.legacy_database_path,
        )
        _CLI_TRACKER_KEY = key
    return _CLI_TRACKER


async def ensure_cli_tracker(settings: CliSettings) -> PocketBaseTracker | None:
    """Ensure the tracker is started; return None gracefully if disabled or unavailable."""
    if not settings.track_videos:
        return None
    tracker = get_cli_tracker(settings)
    try:
        await tracker.start()
        return tracker
    except PocketBaseError as exc:
        logger.warning("PocketBase tracking is enabled but unavailable: %s", exc)
        return None
    except Exception as exc:
        logger.exception("Unexpected error starting PocketBase tracker: %s", exc)
        return None


async def record_cli_download(
    settings: CliSettings,
    video: VideoObject | Any,
    outcome: DownloadOutcome | str,
    *,
    target: str | Path | None = None,
    quality: str | int | None = None,
    origin_url: str = "",
    origin_name: str = "",
) -> dict[str, Any] | None:
    """Record a completed, failed, paused, or cancelled download in PocketBase."""
    if not settings.track_videos:
        return None

    status = outcome.status if isinstance(outcome, DownloadOutcome) else str(outcome)
    output_path = target or (outcome.path if isinstance(outcome, DownloadOutcome) else None)

    # Normalize to VideoObject
    if isinstance(video, VideoObject):
        v = video
        v.status = status
        if output_path:
            v.output_path = Path(output_path)
        if quality:
            v.selected_quality = str(quality)
        if origin_url and not v.origin_iterator_url:
            v.origin_iterator_url = origin_url
        if origin_name and not v.origin_iterator_name:
            v.origin_iterator_name = origin_name
        if isinstance(outcome, DownloadOutcome) and outcome.missing_segments:
            v.missing_segments = list(outcome.missing_segments)
    else:
        # Generic object or album fallback
        url = str(getattr(video, "url", "") or "")
        title = str(getattr(video, "title", "") or "Untitled")
        video_id = str(getattr(video, "video_id", "") or title or url)
        author = str(getattr(video, "author", "") or "")
        v = VideoObject(
            url=url,
            title=title,
            author=author,
            length=getattr(video, "length", None),
            tags=getattr(video, "tags", None) or [],
            thumbnail_url=str(getattr(video, "thumbnail_url", "") or ""),
            video_id=video_id,
            publish_date=getattr(video, "publish_date", None),
            qualities=getattr(video, "qualities", None) or [],
            status=status,
            output_path=Path(output_path) if output_path else None,
            selected_quality=str(quality) if quality else "",
            origin_iterator_url=origin_url or None,
            origin_iterator_name=origin_name or None,
            is_hls=getattr(video, "is_hls", False),
        )

    tracker = await ensure_cli_tracker(settings)
    if tracker is None:
        return None

    try:
        return await tracker.save_video(v)
    except Exception as exc:
        logger.warning("Failed to record video %s to PocketBase: %s", v.url, exc)
        return None


def print_dashboard_stats(stats: dict[str, Any], console: Console | None = None) -> None:
    """Render a styled Rich dashboard table and overview panel for statistics."""
    out = console or Console()
    enabled = stats.get("enabled", False)
    total = stats.get("total", 0)
    successful = stats.get("successful", 0)
    failed = stats.get("failed", 0)
    other = stats.get("other", 0)
    rate = stats.get("successRate", 0)
    size_mb = stats.get("totalSizeMb", 0.0)
    last_dt = stats.get("lastDownloaded", "")

    size_display = f"{size_mb / 1024:.2f} GB" if size_mb >= 1024 else f"{size_mb:.1f} MB"
    status_text = "[bold green]Active[/]" if enabled else "[dim yellow]Disabled[/]"

    grid = Table.grid(padding=(0, 3))
    grid.add_column(style="bold cyan")
    grid.add_column(style="bold white")
    grid.add_column(style="bold cyan")
    grid.add_column(style="bold white")

    grid.add_row("Status:", status_text, "Total Tracked:", str(total))
    grid.add_row("Successful:", f"[bold green]{successful}[/]", "Success Rate:", f"[bold green]{rate}%[/]")
    grid.add_row("Failed:", f"[bold red]{failed}[/]", "Total Stored:", size_display)
    grid.add_row("Other/Pending:", f"[yellow]{other}[/]", "Last Activity:", last_dt or "[dim]None[/]")

    panel = Panel(
        grid,
        title="[bold #ff2a85]📊 PocketBase Download Statistics[/]",
        subtitle="[dim]Shared persistence with Porn Fetch GUI[/]",
        border_style="#00e5ff",
        padding=(1, 2),
    )
    out.print(panel)

    sources = stats.get("sources", [])
    if sources:
        table = Table(
            title="Download Sources Breakdown",
            title_style="bold #ff2a85",
            border_style="bright_black",
            header_style="bold #00e5ff",
        )
        table.add_column("Source / Origin", style="bold white", min_width=24)
        table.add_column("Total", justify="right")
        table.add_column("Successful", justify="right", style="green")
        table.add_column("Failed", justify="right", style="red")
        table.add_column("Other", justify="right", style="yellow")

        for s in sources:
            table.add_row(
                s.get("name", "Unknown"),
                str(s.get("total", 0)),
                str(s.get("successful", 0)),
                str(s.get("failed", 0)),
                str(s.get("other", 0)),
            )
        out.print(table)


def print_failed_downloads(failed_records: list[dict[str, Any]], console: Console | None = None) -> None:
    """Render a table displaying failed downloads."""
    out = console or Console()
    if not failed_records:
        out.print("[bold green]✓ No failed downloads recorded in the database.[/]")
        return

    table = Table(
        title=f"Failed Downloads ({len(failed_records)} records)",
        title_style="bold red",
        border_style="red",
        header_style="bold #ff2a85",
    )
    table.add_column("Title", style="bold white", max_width=36)
    table.add_column("Video ID", style="cyan", max_width=18)
    table.add_column("Status", style="red")
    table.add_column("URL", style="dim", overflow="fold")

    for r in failed_records:
        table.add_row(
            r.get("title", "") or "[dim]Untitled[/]",
            r.get("video_id", "") or "-",
            r.get("status", "failed"),
            r.get("url", ""),
        )
    out.print(table)


def print_origin_iterators(iterators: list[dict[str, Any]], console: Console | None = None) -> None:
    """Render a table of tracked origin iterators (profiles and collections)."""
    out = console or Console()
    if not iterators:
        out.print("[dim]No origin iterators or collections recorded yet.[/]")
        return

    table = Table(
        title=f"Tracked Origins & Collections ({len(iterators)})",
        title_style="bold #00e5ff",
        border_style="bright_black",
        header_style="bold #ff2a85",
    )
    table.add_column("Name", style="bold white", min_width=20)
    table.add_column("Source URL", style="cyan", overflow="fold")

    for item in iterators:
        table.add_row(item.get("name", "Unknown"), item.get("url", ""))
    out.print(table)


async def close_cli_tracker() -> None:
    """Close the running CLI PocketBaseTracker child process if active."""
    global _CLI_TRACKER, _CLI_TRACKER_KEY
    tracker, _CLI_TRACKER = _CLI_TRACKER, None
    _CLI_TRACKER_KEY = None
    if tracker is not None:
        await tracker.close()
