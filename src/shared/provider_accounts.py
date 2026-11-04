"""Account-session helpers used by both frontends."""
from __future__ import annotations

import re
from typing import Any
from urllib.parse import unquote, urlsplit

from base_api import CachePolicy
from selectolax.lexbor import LexborHTMLParser


class AccountSessionError(ValueError):
    """An app-generated account failure safe to show without upstream secrets."""


def valid_xhamster_playlist_url(url: str) -> bool:
    parsed = urlsplit(url.strip())
    host = (parsed.hostname or "").casefold()
    return (parsed.scheme == "https" and (host == "xhamster.com" or host.endswith(".xhamster.com"))
            and re.fullmatch(r"/my/(?:playlists|favorites/videos)/[^/]+/?", parsed.path) is not None)


async def verify_account_session(client: Any, provider: str) -> str:
    """Check the server's authenticated UI, bypassing cached/anonymous pages.

    Cookie presence and provider Account constructors do not establish login.
    Only return the PornHub username from its authenticated account menu.
    """
    sites = {"pornhub": "https://www.pornhub.com/", "xhamster": "https://xhamster.com/",
             "xvideos": "https://www.xvideos.com/"}
    html = await client.core.fetch_text(sites[provider], cache_policy=CachePolicy.BYPASS)
    if provider == "xvideos":
        if re.search(r'"is_logged"\s*:\s*true\b', html):
            return ""
    else:
        tree = LexborHTMLParser(html)
        logout = any(re.search(r"/(?:logout|log_out)(?:/|$)", urlsplit(node.attributes.get("href", "")).path)
                     for node in tree.css("a[href]"))
        if logout and provider == "xhamster":
            return ""
        if logout and provider == "pornhub":
            node = tree.css_first('.profileData a.username[href*="/users/"]')
            if node is not None:
                path = urlsplit(node.attributes.get("href", "")).path
                match = re.fullmatch(r"/users/([^/]+)/?", path)
                if match:
                    return unquote(match[1])
    raise AccountSessionError(
        f"{provider.title()} did not confirm an authenticated browser session. "
        "Sign in again in the selected browser or refresh the session tokens."
    )


async def connect_pornhub_cookies(client: Any, cookies: Any, username: str = "") -> bool:
    """Attach imported cookies and the username required by account collections.

    Discover the username from the authenticated account menu. When a username
    is supplied, require it to match the browser account before enabling feeds.
    """
    name = username.strip()
    client.logged = False
    if not cookies:
        raise ValueError("PornHub browser cookies were not found")
    if name and not re.fullmatch(r"[\w.-]+", name):
        raise ValueError("Enter the PornHub username for the imported browser session (not your email).")
    client.core.session.cookies.clear()
    client.core.session.cookies.update(cookies)
    actual_name = await verify_account_session(client, "pornhub")
    if name and name.casefold() != actual_name.casefold():
        raise ValueError("The PornHub username does not match the imported browser session")
    name = actual_name
    client.account.name = name
    client.account.user = await client.get_user(f"https://www.pornhub.com/users/{name}", load_html=False)
    client.logged = True
    return True


async def connect_xvideos_cookies(client: Any, cookies: Any, *, browser_jar: Any = None) -> bool:
    """Scope manually supplied tokens to the site, then verify the session."""
    values = dict(cookies)
    client.account = None
    missing = [name for name in ("session_token", "session_token_auth") if not values.get(name)]
    if missing:
        raise AccountSessionError(
            "XVideos session is incomplete. Missing cookies: " + ", ".join(missing)
            + ". Sign in again in the selected browser or supply both session tokens."
        )
    client.core.session.cookies.clear()
    if browser_jar is not None:
        client.core.session.cookies.update(browser_jar)
    for name, value in values.items():
        client.core.session.cookies.set(name, value, domain=".xvideos.com", path="/")
    try:
        client.get_account(cookies=values)
        await verify_account_session(client, "xvideos")
    except Exception:
        client.account = None
        raise
    return client.account is not None
