"""Account-session helpers used by both frontends."""
from __future__ import annotations

import re
from typing import Any


async def connect_pornhub_cookies(client: Any, cookies: Any, username: str) -> bool:
    """Attach imported cookies and the username required by account collections.

    The provider has no cookie-login method that discovers the account name.
    Ask for the browser session's username rather than constructing /users/None.
    """
    name = username.strip()
    if not cookies:
        raise ValueError("PornHub browser cookies were not found")
    if not re.fullmatch(r"[\w.-]+", name):
        raise ValueError("Enter the PornHub username for the imported browser session (not your email).")
    client.core.session.cookies.update(cookies)
    client.account.name = name
    client.account.user = await client.get_user(f"https://www.pornhub.com/users/{name}", load_html=False)
    client.logged = True
    return True
