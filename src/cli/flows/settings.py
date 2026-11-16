"""Interactive application settings and schema-2 licensing flows."""
from __future__ import annotations

import asyncio
import re
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.database.installer import (
    DEFAULT_POCKETBASE_VERSION,
    check_system_path,
    download_and_extract_pocketbase,
    resolve_platform,
    verify_pocketbase_binary,
)
from src.licensing.service import rejection_notice
from src.shared.media import quality_requires_premium
from src.shared.tor_transport import ALL_TRAFFIC_NOTICE

from .. import prompts as questionary
from ..settings import CliSettings, prompt_error_reporting_consent
from ..terminal import Panel, Table
from .context import WizardContext
from .ui import WIZARD_STYLE, print_error, print_screen, print_success

SETTINGS_METADATA: dict[str, tuple[str, str]] = {
    "update_channel": ("Updates", "Stable releases only, or the newest Beta/Stable release. Switching never downgrades."),
    # Video
    "quality": ("Video", "Preferred download quality (best, 1080, 720, worst)"),
    "output_path": ("Video", "Output directory for media files"),
    "path_template": ("Video", "Naming template for media files ($title, $author, $video_id)"),
    "result_limit": ("Video", "Max profile or playlist result count"),
    "skip_existing": ("Video", "Skip downloads if file exists"),
    "write_metadata": ("Video", "Embed metadata tags in downloaded MP4 files"),
    "metadata_export": ("Video", "Premium library export: off or jellyfin"),
    "metadata_layout": ("Video", "Library layout: alongside or scene-folder"),
    "metadata_genres": ("Video", "Export source categories as Jellyfin genres"),
    "metadata_studio_fallback": ("Video", "Use credited providers/publishers/channels as studios"),
    "jellyfin_url": ("Video", "Optional Jellyfin server URL (API key: PORNFETCH_JELLYFIN_API_KEY)"),
    "jellyfin_local_root": ("Video", "Local media root for Jellyfin path mapping"),
    "jellyfin_server_root": ("Video", "Media root as seen by Jellyfin"),
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
    "service_transport": ("Network", "Tor routing: direct, tor (updates/licensing), tor_all (all app traffic)"),
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


# Keys are unchanged. Internal consent fields remain visible but cannot be edited
# independently of the disclosure that owns them.
SETTINGS_METADATA.update({
    "request_delay": ("Performance", "Delay between requests in seconds"),
    "retry_initial_delay": ("Performance", "Initial retry delay in seconds"),
    "retry_max_delay": ("Performance", "Maximum retry delay in seconds"),
    "retry_multiplier": ("Performance", "Backoff multiplier between retries"),
    "retry_jitter": ("Performance", "Random retry delay adjustment"),
    "pages_concurrency": ("Performance", "Concurrent listing pages"),
    "videos_concurrency": ("Performance", "Concurrent video metadata requests"),
    "response_cache_mb": ("Cache", "Maximum response cache size in MB"),
    "response_cache_ttl": ("Cache", "Response cache lifetime in seconds"),
    "segment_cache_mb": ("Cache", "Maximum segment cache size in MB"),
    "segment_cache_ttl": ("Cache", "Segment cache lifetime in seconds"),
    "proxy_auth": ("Network", "Proxy authentication credentials; hidden in lists"),
    "custom_ja3": ("Network", "Custom JA3 TLS fingerprint, empty to use impersonation"),
    "interface": ("Network", "Network interface to bind, empty for automatic"),
    "doh_endpoint": ("Network", "DNS-over-HTTPS resolver endpoint"),
    "trust_environment": ("Network", "Use environment proxy and certificate settings"),
    "encrypted_client_hello": ("Network", "Enable encrypted TLS ClientHello when supported"),
    "error_reporting": ("Logging", "Choose Off, Basic or Full private error reports with the full disclosure"),
    "error_reporting_full_traceback": ("Logging", "Full reports include tracebacks and video URLs; opens consent choices"),
    "error_reporting_decided": ("Logging", "Read only: whether an explicit reporting choice has been saved"),
    "error_reporting_consent_version": ("Logging", "Read only: disclosure version recorded with the reporting choice"),
    "legacy_database_path": ("Database", "Legacy database path retained for configuration compatibility"),
})
for _key in ("metadata_export", "metadata_layout", "metadata_genres", "metadata_studio_fallback",
             "jellyfin_url", "jellyfin_local_root", "jellyfin_server_root"):
    SETTINGS_METADATA[_key] = ("Library export", SETTINGS_METADATA[_key][1])

SETTING_NAMES = {
    "quality": "Quality", "output_path": "Output folder", "path_template": "File naming",
    "result_limit": "Result limit", "profile_video_mode": "Profile content",
    "bandwidth_limit_mb": "Speed limit (MB/s)", "service_transport": "Tor routing",
    "verify_ssl": "Verify certificates", "dns_over_https": "DNS over HTTPS",
    "pocketbase_binary": "PocketBase executable", "pocketbase_data_path": "Database folder",
    "error_reporting": "Automatic error reports", "error_reporting_full_traceback": "Detailed error reports",
}
READ_ONLY_SETTINGS = {"error_reporting_decided", "error_reporting_consent_version"}


def setting_name(key: str) -> str:
    return SETTING_NAMES.get(key, key.replace("_", " ").capitalize())


def setting_value(settings: CliSettings, key: str) -> str:
    value = getattr(settings, key)
    if key in {"proxy_auth", "proxy"} and value:
        return "Configured (hidden)"
    if isinstance(value, bool):
        return "On" if value else "Off"
    return str(value) if value != "" else "Not set"


async def choose_setting(ctx: WizardContext, category: str | None = None, default: str | None = None) -> str | None:
    print_screen(ctx.console, "Settings", category or "Search all")
    choices = []
    for key, (group, description) in SETTINGS_METADATA.items():
        if category and group != category:
            continue
        value = setting_value(ctx.settings, key)
        if key == "quality" and not ctx.license_service.status.allowed and quality_requires_premium(str(ctx.settings.quality)):
            value += " (Premium required)"
        label = f"{setting_name(key)}: {value}"
        # Keep values concise; the focused description retains the full value.
        if len(label) > 64:
            label = label[:61] + "..."
        choices.append(questionary.Choice(
            label, value=key,
            description=f"{description}\n{group} / {key} | Current: {value}",
        ))
    choices.append(questionary.Choice("Back", value="__cancel__", description="Return to settings categories"))
    return await questionary.select(
        "Select a setting to modify:", choices=choices, searchable=True, default=default, style=WIZARD_STYLE,
    ).ask_async()


async def handle_pocketbase_install_flow(ctx: WizardContext) -> Path | None:
    """Check PATH or auto-download PocketBase and update settings."""
    path_binary = check_system_path()
    if path_binary:
        ctx.console.print(f"PocketBase detected: {path_binary}", markup=False)
        choice = await questionary.select(
            "Choose a PocketBase executable:",
            choices=[
                questionary.Choice("Use detected system PATH binary", value="use_path"),
                questionary.Choice("Download & install dedicated binary", value="download"),
                questionary.Choice("Cancel", value="cancel"),
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
    """Browse categories and edit through the existing validation/save path."""
    category = None
    focused = None
    selected_keys = {}
    while True:
        if category is None:
            print_screen(ctx.console, "Settings")
        categories = list(dict.fromkeys(group for group, _ in SETTINGS_METADATA.values()))
        choices = [questionary.Choice("Search all settings", value="edit")]
        choices.extend(questionary.Choice(group, value=group) for group in categories)
        choices.extend([
            questionary.Separator("Administration"),
            questionary.Choice("Install or detect PocketBase", value="install_pb"),
            questionary.Choice("Reset settings to defaults", value="reset"),
            questionary.Choice("Back", value="back"),
        ])
        if category is None:
            action = await questionary.select(
                "Settings & Configuration:", choices=choices, default=focused, style=WIZARD_STYLE,
            ).ask_async()
            if not action or action == "back":
                break
            focused = action
        else:
            action = category

        if action == "install_pb":
            await handle_pocketbase_install_flow(ctx)
            continue
        if action == "reset":
            confirm = await questionary.confirm("Reset all settings to defaults?", default=False, style=WIZARD_STYLE).ask_async()
            if confirm:
                defaults = CliSettings()
                ctx.settings_store.save(defaults)
                ctx.settings = defaults
                await ctx.refresh_pool()
                print_success(ctx.console, "Reset Settings", "Settings restored to defaults.")
            continue

        if action == "edit" or action in categories:
            category = action if action in categories else None
            target_setting = await choose_setting(ctx, category, selected_keys.get(category))
            if not target_setting or target_setting == "__cancel__":
                category = None
                continue
            selected_keys[category] = target_setting
            if target_setting in READ_ONLY_SETTINGS:
                ctx.console.print("[dim]This value is managed by the reporting consent choice.[/]")
                continue
            if target_setting in {"error_reporting", "error_reporting_full_traceback"}:
                previous = ctx.settings
                updated = await prompt_error_reporting_consent(
                    ctx.settings.overridden(error_reporting_decided=False), ctx.settings_store, console=ctx.console,
                )
                if updated.error_reporting_decided:
                    ctx.settings = updated
                    await ctx.refresh_pool()
                else:
                    ctx.settings = previous
                continue
            print_screen(ctx.console, "Settings", category or "Search all", setting_name(target_setting))
            ctx.console.print(SETTINGS_METADATA[target_setting][1], markup=False)
            current_val = getattr(ctx.settings, target_setting)
            new_val: Any = None

            if target_setting == "update_channel":
                new_val = await questionary.select(
                    "Update channel:", choices=[questionary.Choice("Stable", value="stable"),
                                               questionary.Choice("Beta", value="beta")],
                    default=current_val, style=WIZARD_STYLE,
                ).ask_async()
            elif target_setting == "service_transport":
                new_val = await questionary.select(
                    "Tor routing:",
                    choices=[questionary.Choice("Off", value="direct"),
                             questionary.Choice("Updates + licensing only", value="tor"),
                             questionary.Choice("All app traffic (including downloads)", value="tor_all")],
                    default=current_val, style=WIZARD_STYLE,
                ).ask_async()
                if new_val == "tor_all" and current_val != "tor_all":
                    ctx.console.print(Panel(ALL_TRAFFIC_NOTICE, title="Using Tor for video downloads"))
                    if not await questionary.confirm("Enable Tor for all app traffic?", default=False, style=WIZARD_STYLE).ask_async():
                        continue
            elif target_setting == "metadata_export":
                new_val = await questionary.select(
                    "Automatic library export:",
                    choices=[questionary.Choice("Off", value="off"),
                             questionary.Choice("Jellyfin (Premium)", value="jellyfin",
                                                disabled=None if ctx.license_service.status.allowed else "Requires Premium")],
                    default=current_val if ctx.license_service.status.allowed else "off", style=WIZARD_STYLE,
                ).ask_async()
            elif target_setting == "metadata_layout":
                new_val = await questionary.select("Library layout:", choices=["alongside", "scene-folder"],
                                                   default=current_val, style=WIZARD_STYLE).ask_async()
            elif isinstance(current_val, bool):
                new_val = await questionary.confirm(f"Enable {target_setting}?", default=current_val, style=WIZARD_STYLE).ask_async()
            elif target_setting == "quality":
                has_premium = ctx.license_service.status.allowed
                qualities_list = ["best", "2160", "1440", "1080", "720", "480", "360", "worst"]
                quality_choices = []
                for q in qualities_list:
                    req_prem = quality_requires_premium(q)
                    is_locked = req_prem and not has_premium
                    disabled_msg = "Locked: Requires License" if is_locked else None
                    title = f"{q}p" if q.isdigit() else q
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
                new_val = await questionary.select("Select log level:", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default=current_val, style=WIZARD_STYLE).ask_async()
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
                        questionary.Choice("Auto-detect or Auto-install", value="auto"),
                        questionary.Choice("Enter custom path manually", value="manual"),
                        questionary.Choice("Clear (use auto-detect)", value="clear"),
                        questionary.Choice("Cancel", value="cancel"),
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
                raw = await (questionary.password if target_setting == "proxy_auth" else questionary.text)(
                    f"Enter new value for {setting_name(target_setting)}:",
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
                    if target_setting == "parallel_downloads" and int(new_val) > 1 and not ctx.license_service.status.allowed:
                        raise ValueError("Parallel downloads require an active premium license. Free use allows one download at a time.")
                    updated = replace(ctx.settings, **{target_setting: new_val})
                    updated.validate()
                    ctx.settings_store.save(updated)
                    ctx.settings = updated
                    await ctx.refresh_pool()
                    print_success(ctx.console, "Setting Updated", f"{setting_name(target_setting)}: {setting_value(ctx.settings, target_setting)}")
                    if target_setting == "update_channel":
                        from ..self_update import run_self_update
                        await asyncio.to_thread(run_self_update, check_only=True, assume_yes=False)
                except Exception as error:
                    print_error(ctx.console, "Validation Error", str(error))


# ---------------------------------------------------------------------------
# Sub-Flow 6: License Management
# ---------------------------------------------------------------------------

async def handle_license_management(ctx: WizardContext) -> None:
    """Check license validity, import schema-2 keys/files, and deactivate."""
    print_screen(ctx.console, "License")
    ctx.console.print(
        "[cyan]Lifetime Premium:[/] Buy once, use forever. EUR 29.99 at https://pornfetch.to/porn_fetch. "
        "Import the license file here.\n"
        "[dim]Use Premium on up to 10 active installations. Every future Porn Fetch update and feature I release is included. "
        "Future development has no guaranteed duration. Activation and periodic online validation are required, "
        "with up to 7 days offline after a successful check. If I permanently close the licensing service, "
        "I will provide an offline unlock before closure so existing buyers can continue using Premium.[/dim]"
    )
    focused = None
    while True:
        action = await questionary.select(
            "License Management:",
            choices=[
                questionary.Choice("Check / Refresh License Status", value="check"),
                questionary.Choice("Import License Key / File", value="import"),
                questionary.Choice("Deactivate Current License (frees 1 of 10 machine seats)", value="deactivate"),
                questionary.Choice("Back to Main Menu", value="back"),
            ],
            default=focused, style=WIZARD_STYLE,
        ).ask_async()
        focused = action

        if not action or action == "back":
            break

        if action == "check":
            with ctx.console.status("[bold cyan]Checking license status with server...[/]", spinner="dots"):
                status = await ctx.check_license(force=True)

            license_expiry_str = "-"
            lic_exp = getattr(status, "license_expires_at", None)
            if status.allowed:
                if lic_exp is None:
                    license_expiry_str = "Lifetime / Never"
                else:
                    license_expiry_str = datetime.fromtimestamp(lic_exp, tz=timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")
            elif lic_exp is not None:
                license_expiry_str = datetime.fromtimestamp(lic_exp, tz=timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")

            next_check_str = "-"
            check_time = getattr(status, "next_check_at", None) or getattr(status, "expires_at", None)
            if check_time is not None:
                next_check_str = datetime.fromtimestamp(check_time, tz=timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")
            permit_expiry = getattr(status, "expires_at", None)
            permit_expiry_str = "-" if permit_expiry is None else datetime.fromtimestamp(
                permit_expiry, tz=timezone.utc,
            ).astimezone().strftime("%Y-%m-%d %H:%M")

            table = Table(show_header=False, box=None, padding=(0, 1))
            table.add_row("[bold cyan]State:[/]", f"[bold green]{status.state}[/]" if status.allowed else f"[bold yellow]{status.state}[/]")
            table.add_row("[bold cyan]Description:[/]", ctx.license_service.reason)
            table.add_row("[bold cyan]Features:[/]", "[bold green]Premium unlocked (>720p, bulk and parallel downloads)[/]" if status.allowed else "[dim]Standard free tier (<=720p)[/]")
            expiry_display = (
                f"{license_expiry_str} [dim](all future updates and features included)[/dim]"
                if license_expiry_str == "Lifetime / Never"
                else license_expiry_str
            )
            table.add_row("[bold cyan]Premium license expires:[/]", expiry_display)
            table.add_row("[bold cyan]Machine Limit:[/]", "10 machines (use Deactivate to unlink seats)")
            table.add_row("[bold cyan]Offline Permit Expires:[/]", permit_expiry_str)
            table.add_row("[bold cyan]Next Online Check:[/]", next_check_str)

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

            with ctx.console.status("[bold cyan]Importing and verifying license...[/]", spinner="dots"):
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

            with ctx.console.status("[bold cyan]Deactivating license...[/]", spinner="dots"):
                try:
                    status = await ctx.license_service.deactivate()
                    print_success(ctx.console, "License Deactivated", f"State: {status.state}\n{ctx.license_service.reason}")
                except Exception as error:
                    print_error(ctx.console, "Deactivation Error", str(error))
