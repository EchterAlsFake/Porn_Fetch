"""Interactive application settings and schema-2 licensing flows."""
from __future__ import annotations

import re
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import questionary
from rich.panel import Panel
from rich.table import Table

from src.shared.media import quality_requires_premium

from ..settings import CliSettings
from .context import WizardContext
from .ui import WIZARD_STYLE, print_error, print_success

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
    # Database / Tracking
    "track_videos": ("Database", "Enable PocketBase download tracking & statistics"),
    "pocketbase_data_path": ("Database", "Directory for PocketBase database files"),
    "pocketbase_binary": ("Database", "Custom PocketBase executable path (leave empty for auto-detect)"),
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
