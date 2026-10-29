"""Shared Questionary styling and Rich rendering helpers."""
from __future__ import annotations

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
from rich.text import Text

from src.shared.version import __version__

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
    banner.append(f"v{__version__}", style="dim")
    if license_state:
        state_clean = license_state.replace("_", " ").title()
        if license_state.lower() in {"valid", "active", "update_entitlement_expired"}:
            banner.append("  •  [Premium: Active]", style="bold green")
        elif license_state.lower() in {"offline_grace"}:
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
