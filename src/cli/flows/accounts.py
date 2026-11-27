"""Interactive provider authentication and account collection flow."""
from __future__ import annotations

from contextlib import aclosing

from src.shared.account_capabilities import account_providers
from src.shared.media import VideoObject
from src.shared.public_media import account_video_row

from .. import prompts as questionary
from ..providers import unwrap_scrape_result
from ..terminal import Panel, Table
from .context import WizardContext
from .ui import WIZARD_STYLE, print_error, print_screen, print_success


async def handle_account_auth(ctx: WizardContext) -> None:
    """Handle site logins, browser cookie discovery, and account collection downloads."""
    print_screen(ctx.console, "Accounts")
    providers = {provider.name: provider for provider in account_providers()}
    manual_login = [name for name, provider in providers.items() if provider.login]
    browser_login = [name for name, provider in providers.items() if provider.browser_import]
    focused = None
    while True:
        action = await questionary.select(
            "Account & Authentication:",
            choices=[
                questionary.Choice("Enter Credentials (Username / Password / Tokens)", value="credentials"),
                questionary.Choice("Load Browser Cookies (Chrome, Firefox, Brave, etc.)", value="cookies"),
                questionary.Choice("View Account Login Status", value="status"),
                questionary.Choice("Fetch Account Collection (Favorites, Liked, etc.)", value="collections"),
                questionary.Choice("Back to Main Menu", value="back"),
            ],
            default=focused, style=WIZARD_STYLE,
        ).ask_async()
        focused = action

        if not action or action == "back":
            break

        if action == "status":
            table = Table(title="Account Login Status", border_style="#00e5ff", header_style="bold cyan")
            table.add_column("Provider", style="bold cyan")
            table.add_column("Status", justify="center")
            for name, provider in providers.items():
                if not (provider.login or provider.browser_import):
                    status = "[dim]Account access unavailable[/]"
                elif ctx.account_service.logged_in(name):
                    status = "[bold cyan]Logged In[/]"
                else:
                    status = "[dim]Not Logged In[/]"
                table.add_row(name, status)
            ctx.console.print(table)

        elif action == "credentials":
            provider = await questionary.select(
                "Select provider to authenticate:",
                choices=[*manual_login, "Cancel"],
                style=WIZARD_STYLE,
            ).ask_async()
            if not provider or provider == "Cancel":
                continue

            if providers[provider].login == "tokens":
                token = await questionary.password("Enter XVideos session_token:", style=WIZARD_STYLE).ask_async()
                token_auth = await questionary.password("Enter XVideos session_token_auth:", style=WIZARD_STYLE).ask_async()
                if not token or not token_auth:
                    continue
                with ctx.console.status("[bold cyan]Authenticating XVideos tokens...[/]", spinner="dots"):
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
                user = await questionary.text(f"Enter {provider} email address:", style=WIZARD_STYLE).ask_async()
                secret = await questionary.password(f"Enter {provider} password:", style=WIZARD_STYLE).ask_async()
                if not user or not secret:
                    continue
                with ctx.console.status(f"[bold cyan]Logging in to {provider}...[/]", spinner="dots"):
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
                choices=[*browser_login, "Cancel"],
                style=WIZARD_STYLE,
            ).ask_async()
            if not provider or provider == "Cancel":
                continue
            username = ""
            if providers[provider].browser_import == "username":
                username = await questionary.text(
                    f"{provider} username for this browser session (not email):", style=WIZARD_STYLE,
                ).ask_async() or ""
                if not username.strip():
                    continue
            with ctx.console.status(f"[bold cyan]Importing browser cookies for {provider}...[/]", spinner="dots"):
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
            logged_providers = [
                name for name, provider in providers.items()
                if provider.collections and ctx.account_service.logged_in(name)
            ]
            if not logged_providers:
                ctx.console.print(Panel("[yellow]Please log in to an account first.[/]", border_style="yellow"))
                continue
            prov = await questionary.select("Select account provider:", choices=logged_providers, style=WIZARD_STYLE).ask_async()
            if not prov:
                continue

            collections = {collection.key: collection for collection in providers[prov].collections}
            selected_col = await questionary.select(
                f"Select {prov} collection:",
                choices=[questionary.Choice(collection.label, value=collection.key)
                         for collection in collections.values()],
                style=WIZARD_STYLE,
            ).ask_async()
            if not selected_col:
                continue

            collection = collections[selected_col]
            playlist_url = ""
            if collection.url_hint:
                playlist_url = await questionary.text(
                    f"Enter {prov} account playlist URL:", style=WIZARD_STYLE,
                ).ask_async() or ""

            items: list[VideoObject] = []
            with ctx.console.status(f"[bold cyan]Fetching account videos from {prov}...[/]", spinner="dots"):
                try:
                    stream, label = ctx.account_service.collection(prov, selected_col, playlist_url)
                    provider_key = providers[prov].key
                    async with aclosing(stream) as collection_items:
                        async for result in collection_items:
                            source = unwrap_scrape_result(result)
                            items.append(account_video_row(source, provider_key))
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

            col_table = Table(title=f"{label} ({len(items)} items)", border_style="#00e5ff", header_style="bold cyan")
            col_table.add_column("Index", style="cyan", justify="right")
            col_table.add_column("Title", style="white")
            col_table.add_column("Duration", style="magenta")
            col_table.add_column("Access")
            for idx, med in enumerate(items, 1):
                col_table.add_row(str(idx), med.title, f"{med.length} min" if med.length else "-",
                                  "Restricted" if med.provider_restricted else "Public access unchecked")
            ctx.console.print(col_table)
