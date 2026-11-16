"""Shared Questionary styling and Rich rendering helpers."""
from __future__ import annotations

import os
from contextlib import contextmanager

import questionary
from rich.console import Console
from rich.panel import Panel as RichPanel
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
from rich.table import Column
from rich.table import Table as RichTable
from rich.text import Text
from rich.theme import Theme

from src.shared.version import __version__

# Cyan indicates interaction; pink is reserved for the application wordmark.
WIZARD_STYLE = questionary.Style([
    ("", "bg:#101820 fg:#e5edf5"),
    ("qmark", "fg:#00e5ff bold"),
    ("question", "bold"),
    ("answer", "fg:#00e5ff bold"),
    ("pointer", "fg:#00e5ff bold"),
    ("highlighted", "bg:#00e5ff fg:#101820 bold"),
    ("selected", "fg:#00e5ff"),
    ("separator", "fg:#aab4c0"),
    ("instruction", "fg:#aab4c0"),
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


def terminal_console(**kwargs) -> Console:
    """Respect standard color preferences and offer an explicit ASCII mode."""
    plain = os.environ.get("PORNFETCH_PLAIN", "").lower() in {"1", "true", "yes"} or os.environ.get("TERM") == "dumb"
    kwargs.setdefault("theme", Theme({"progress.description": "cyan", "progress.percentage": "cyan"}))
    if plain:
        kwargs.update(color_system=None, force_terminal=False)
    return TerminalConsole(**kwargs)


class TerminalConsole(Console):
    """Loading feedback also remains visible in the line-oriented interface."""

    def status(self, status, **kwargs):
        if self.is_terminal:
            return super().status(status, **kwargs)

        @contextmanager
        def plain_status():
            self.print(status)
            yield

        return plain_status()


class Panel(RichPanel):
    """Content sections share typography instead of surrounding every state in a box."""

    def __rich_console__(self, console, options):
        if self.title:
            yield self.title if isinstance(self.title, Text) else Text.from_markup(str(self.title), style="bold")
        yield self.renderable
        if self.subtitle:
            yield self.subtitle if isinstance(self.subtitle, Text) else Text.from_markup(str(self.subtitle), style="dim")


class Table(RichTable):
    """Quiet tables on desktop; labeled records when columns would be cramped."""

    def __init__(self, *args, **kwargs):
        self._records = []
        kwargs.update(box=None, border_style="dim", header_style="bold cyan", title_style="bold")
        kwargs.setdefault("padding", (0, 1))
        super().__init__(*args, **kwargs)

    def add_row(self, *renderables, **kwargs):
        self._records.append(renderables)
        super().add_row(*renderables, **kwargs)

    def __rich_console__(self, console, options):
        if options.max_width >= 64 or len(self.columns) <= 1:
            yield from super().__rich_console__(console, options)
            return
        if self.title:
            yield Text.from_markup(str(self.title), style="bold")
        for index, row in enumerate(self._records, 1):
            if not self.show_header:
                for offset in range(0, len(row), 2):
                    value = row[offset + 1] if offset + 1 < len(row) else ""
                    yield Text.from_markup(f"{row[offset]} {value}")
                continue
            yield Text(f"{index}.", style="cyan")
            for column, value in zip(self.columns, row):
                if value is None:
                    continue
                label = Text.from_markup(str(column.header)).plain
                yield Text(f"{label}: ", style="bold") + (
                    value if isinstance(value, Text) else Text.from_markup(str(value))
                )


def make_download_progress(console: Console) -> Progress:
    """Use fewer columns on narrow screens without changing progress units."""
    columns = [TextColumn("{task.description}", table_column=Column(
        max_width=max(8, console.width // 3), overflow="ellipsis", no_wrap=True,
    ))]
    if console.width >= 40:
        columns.append(TaskProgressColumn())
    if console.width >= 64:
        columns.insert(1, BarColumn(bar_width=None, complete_style="cyan", finished_style="green"))
    columns.append(SmartUnitsColumn())
    if console.width >= 90:
        columns.extend([DownloadSpeedColumn(), TimeRemainingColumn()])
    # Non-interactive consoles get a final snapshot, without animated escape output.
    return Progress(*columns, console=console, auto_refresh=console.is_terminal,
                    disable=False, expand=False)


def print_banner(console: Console, license_state: str | None = None) -> None:
    """Compact header that wraps naturally without a decorative frame."""
    banner = Text("PORN FETCH", style="bold #ff2a85")
    banner.append(f"  v{__version__}", style="dim")
    if license_state:
        state = license_state.replace("_", " ").title()
        if license_state.lower() in {"valid", "active"}:
            banner.append("  |  Premium: Active", style="green")
        else:
            banner.append(f"  |  License: {state}", style="yellow" if license_state in {
                "offline_grace", "emergency_access"
            } else "dim")
    console.print(banner)


def print_screen(console: Console, *path: str) -> None:
    trail = Text("Home", style="dim")
    for part in path:
        trail.append(" / ", style="dim")
        trail.append(part, style="bold cyan")
    console.print()
    console.print(trail)


def print_error(console: Console, title: str, message: str) -> None:
    console.print(Text(f"Error: {title}", style="bold red"))
    console.print(Text(message))


def print_success(console: Console, title: str, message: str) -> None:
    console.print(Text(f"Success: {title}", style="bold green"))
    console.print(Text.from_markup(message))
