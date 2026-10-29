"""One-time terminal beta consent, before creating application services."""
from __future__ import annotations

import asyncio
import sys

import questionary
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from src.shared.beta_disclaimer import (
    BETA_DISCLAIMER_TEXT,
    BETA_DISCLAIMER_VERSION,
    DisclaimerReadDelay,
)

from .settings import CliSettings, SettingsStore


async def prompt_beta_disclaimer(
    settings: CliSettings,
    store: SettingsStore,
    *,
    console: Console | None = None,
) -> CliSettings | None:
    """Return accepted settings, or None when startup must stop."""
    if settings.beta_disclaimer_version == BETA_DISCLAIMER_VERSION:
        return settings

    output = console or Console(stderr=True)
    output.print(Panel(Text(BETA_DISCLAIMER_TEXT), title="Porn Fetch v3.9 BETA disclaimer", padding=(1, 2)))
    if not sys.stdin.isatty() or not output.is_terminal:
        output.print(
            "First-run beta consent is required. Run Porn_Fetch_CLI.py interactively in a terminal, "
            "read the disclaimer for 30 seconds and select OK before using unattended commands.",
            style="yellow",
        )
        return None

    delay = DisclaimerReadDelay()
    delay.start()
    with Live(console=output, auto_refresh=False, transient=True) as countdown:
        while delay.remaining_seconds > 0:
            countdown.update(
                Text(f"Please read the disclaimer. OK available in {delay.remaining_seconds} seconds."),
                refresh=True,
            )
            await asyncio.sleep(1)

    choice = await questionary.select(
        "Consent to the experimental beta release?",
        choices=["OK", "Exit"],
    ).ask_async()
    if choice != "OK":
        return None

    updated = settings.overridden(beta_disclaimer_version=BETA_DISCLAIMER_VERSION)
    store.save(updated)
    return updated
