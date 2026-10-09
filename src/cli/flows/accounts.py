"""Interactive provider authentication and account collection flow."""
from __future__ import annotations

from typing import Any

import questionary
from rich.panel import Panel
from rich.table import Table

from src.shared.media import VideoObject

from ..media import prepare_video
from ..providers import ContentKind, Route, unwrap_scrape_result
from .context import WizardContext
from .ui import WIZARD_STYLE, print_error, print_success


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
            username = ""
            if provider == "PornHub":
                username = await questionary.text(
                    "PornHub username for this browser session (not email):", style=WIZARD_STYLE,
                ).ask_async() or ""
                if not username.strip():
                    continue
            with ctx.console.status(f"[bold green]Importing browser cookies for {provider}...[/]", spinner="dots"):
                try:
                    ok = await ctx.account_service.login(provider, username=username, browser=True)
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
                "PornHub": ["history", "recommended", "favorites", "feed"],
                "XHamster": ["liked", "playlist"],
                "XVideos": ["watch_later", "history", "liked"],
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
