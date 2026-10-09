"""Interactive application settings and schema-2 licensing flows."""
from __future__ import annotations

import asyncio
import re
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import questionary
from rich.panel import Panel
from rich.table import Table

from src.database.installer import (
    DEFAULT_POCKETBASE_VERSION,
    check_system_path,
    download_and_extract_pocketbase,
    resolve_platform,
    verify_pocketbase_binary,
)
from src.licensing.service import rejection_notice
from src.shared.media import quality_requires_premium

from ..settings import CliSettings
from .context import WizardContext
from .ui import WIZARD_STYLE, print_error, print_success

SETTINGS_METADATA: dict[str, tuple[str, str]] = {
    # Video
    "quality": ("Video", "Preferred download quality (best, 1080, 720, worst)"),
    "output_path": ("Video", "Output directory for media files"),
    "path_template": ("Video", "Naming template for media files ($title, $author, $video_id)"),
    "result_limit": ("Video", "Max profile or playlist result count"),
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


async def handle_pocketbase_install_flow(ctx: WizardContext) -> Path | None:
    """Check PATH or auto-download PocketBase and update settings."""
    path_binary = check_system_path()
    if path_binary:
        choice = await questionary.select(
            f"PocketBase was detected on PATH:\n  [bold cyan]{path_binary}[/]\nWhat would you like to do?",
            choices=[
                questionary.Choice("✅ Use detected system PATH binary", value="use_path"),
                questionary.Choice("📥 Download & install dedicated binary", value="download"),
                questionary.Choice("🔙 Cancel", value="cancel"),
            ],
            style=WIZARD_STYLE,
        ).ask_async()

        if choice in {None, "cancel"}:
            return None

        if choice == "use_path":
            try:
                version_info = verify_pocketbase_binary(path_binary)
                ctx.settings = ctx.settings.overridden(pocketbase_binary=str(path_binary))
                ctx.settings_store.save(ctx.settings)
                print_success(
                    ctx.console,
                    "PocketBase Configured",
                    f"Configured system binary: {path_binary}\nVersion: {version_info}",
                )
                return path_binary
            except Exception as exc:
                print_error(ctx.console, "Verification Failed", f"Binary on PATH failed check: {exc}")

    try:
        os_label, arch_label, _ = resolve_platform()
    except Exception as exc:
        print_error(ctx.console, "Platform Error", str(exc))
        return None

    confirm = await questionary.confirm(
        f"Download PocketBase v{DEFAULT_POCKETBASE_VERSION} for your system ({os_label}_{arch_label})?",
        default=True,
        style=WIZARD_STYLE,
    ).ask_async()

    if not confirm:
        return None

    with ctx.console.status("[bold cyan]Downloading and installing PocketBase...[/]"):
        try:
            binary_path = await asyncio.to_thread(
                download_and_extract_pocketbase,
                version=DEFAULT_POCKETBASE_VERSION,
            )
            version_info = verify_pocketbase_binary(binary_path)
        except Exception as exc:
            print_error(ctx.console, "Installation Failed", str(exc))
            return None

    ctx.settings = ctx.settings.overridden(pocketbase_binary=str(binary_path))
    ctx.settings_store.save(ctx.settings)
    print_success(
        ctx.console,
        "PocketBase Installed",
        f"Successfully installed at: [bold cyan]{binary_path}[/]\nVersion: [bold green]{version_info}[/]",
    )
    return binary_path


async def handle_settings(ctx: WizardContext) -> None:
    """Display configuration table, allow inline editing, and persist changes."""
    while True:
        action = await questionary.select(
            "Settings & Configuration:",
            choices=[
                questionary.Choice("📄 View All Settings", value="view"),
                questionary.Choice("✏️  Modify a Setting", value="edit"),
                questionary.Choice("📦 Auto-Install / Detect PocketBase", value="install_pb"),
                questionary.Choice("🔄 Reset to Default Settings", value="reset"),
                questionary.Choice("🔙 Back to Main Menu", value="back"),
            ],
            style=WIZARD_STYLE,
        ).ask_async()

        if not action or action == "back":
            break

        if action == "install_pb":
            await handle_pocketbase_install_flow(ctx)
            continue

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
            elif target_setting == "pocketbase_binary":
                pb_action = await questionary.select(
                    "PocketBase binary configuration:",
                    choices=[
                        questionary.Choice("🚀 Auto-detect or Auto-install", value="auto"),
                        questionary.Choice("✏️  Enter custom path manually", value="manual"),
                        questionary.Choice("🔄 Clear (use auto-detect)", value="clear"),
                        questionary.Choice("🔙 Cancel", value="cancel"),
                    ],
                    style=WIZARD_STYLE,
                ).ask_async()
                if pb_action == "auto":
                    await handle_pocketbase_install_flow(ctx)
                    continue
                elif pb_action == "clear":
                    new_val = ""
                elif pb_action == "manual":
                    raw = await questionary.text(
                        "Enter path to PocketBase executable:",
                        default=str(current_val),
                        style=WIZARD_STYLE,
                    ).ask_async()
                    if raw is not None:
                        new_val = raw.strip()
                else:
                    continue
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
    ctx.console.print(
        "[cyan]Production license:[/] Visit https://pornfetch.to/ to purchase or renew. "
        "Import the license file here.\n"
        "[dim]Note: Each license allows up to 10 machines. Permanent licenses provide lifetime access "
        "to the current release and include updates for 1 year after first activation.[/dim]"
    )
    while True:
        action = await questionary.select(
            "License Management:",
            choices=[
                questionary.Choice("🔍 Check / Refresh License Status", value="check"),
                questionary.Choice("📥 Import License Key / File", value="import"),
                questionary.Choice("⚠️  Deactivate Current License (frees 1 of 10 machine seats)", value="deactivate"),
                questionary.Choice("🔙 Back to Main Menu", value="back"),
            ],
            style=WIZARD_STYLE,
        ).ask_async()

        if not action or action == "back":
            break

        if action == "check":
            with ctx.console.status("[bold green]Checking license status with server...[/]", spinner="dots"):
                status = await ctx.check_license(force=True)

            license_expiry_str = "—"
            lic_exp = getattr(status, "license_expires_at", None)
            if status.allowed:
                if lic_exp is None:
                    license_expiry_str = "Lifetime / Never"
                else:
                    license_expiry_str = datetime.fromtimestamp(lic_exp, tz=timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")
            elif lic_exp is not None:
                license_expiry_str = datetime.fromtimestamp(lic_exp, tz=timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")

            next_check_str = "—"
            check_time = getattr(status, "next_check_at", None) or getattr(status, "expires_at", None)
            if check_time is not None:
                next_check_str = datetime.fromtimestamp(check_time, tz=timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")

            table = Table(show_header=False, box=None, padding=(0, 1))
            table.add_row("[bold cyan]State:[/]", f"[bold green]{status.state}[/]" if status.allowed else f"[bold yellow]{status.state}[/]")
            table.add_row("[bold cyan]Description:[/]", ctx.license_service.reason)
            table.add_row("[bold cyan]Features:[/]", "[bold green]Premium unlocked (1080p+, fast downloads)[/]" if status.allowed else "[dim]Standard free tier (<=720p)[/]")
            expiry_display = (
                f"{license_expiry_str} [dim](valid for current release, 1 yr updates included)[/dim]"
                if license_expiry_str == "Lifetime / Never"
                else license_expiry_str
            )
            table.add_row("[bold cyan]Update entitlement ends:[/]", expiry_display)
            table.add_row("[bold cyan]Machine Limit:[/]", "10 machines (use Deactivate to unlink seats)")
            table.add_row("[bold cyan]Offline Permit Expires:[/]", next_check_str)

            border = "green" if status.allowed else "yellow"
            ctx.console.print(Panel(table, title="[bold #00e5ff]License Information[/]", border_style=border))

        elif action == "import":
            path_or_key = await questionary.text(
                "Enter license file path, signed key, or JSON license:",
                style=WIZARD_STYLE,
            ).ask_async()
            if not path_or_key or not path_or_key.strip():
                continue
            path_or_key = path_or_key.strip()

            with ctx.console.status("[bold green]Importing and verifying license...[/]", spinner="dots"):
                try:
                    if len(path_or_key) < 240 and not path_or_key.startswith(("key/", "{")) and Path(path_or_key).is_file():
                        status = await ctx.license_service.import_file(path_or_key)
                    else:
                        status = await ctx.license_service.client.import_license(path_or_key)
                        ctx.license_service.status = status
                    if status.server_rejected:
                        print_error(ctx.console, "License Rejected", rejection_notice(status.state))
                    elif not status.allowed:
                        print_error(ctx.console, "Activation incomplete", ctx.license_service.reason)
                    else:
                        print_success(
                            ctx.console,
                            "License Imported",
                            f"Status: [bold white]{status.state}[/]\n{ctx.license_service.reason}",
                        )
                except Exception as error:
                    print_error(ctx.console, "License Import Failed", str(error))

        elif action == "deactivate":
            confirm = await questionary.confirm(
                "Are you sure you want to deactivate the license on this device? (This unlinks the machine to free up 1 of your 10 machine seats)",
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
