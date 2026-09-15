"""Memory-only account login and collection routing."""
from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Mapping
import http.cookiejar
from typing import Any
from urllib.parse import urlparse

from .providers import ClientPool


class AccountService:
    def __init__(self, pool: ClientPool) -> None:
        self.pool = pool

    def logged_in(self, provider: str) -> bool:
        key = provider.casefold()
        client = self.pool.client(key)
        if key == "pornhub":
            return bool(getattr(client, "logged", False))
        return getattr(client, "account", None) is not None

    async def login(
        self,
        provider: str,
        *,
        username: str = "",
        password: str = "",
        tokens: Mapping[str, str] | None = None,
        browser: bool = False,
    ) -> bool:
        key = provider.casefold()
        if key not in {"pornhub", "xhamster", "xvideos"}:
            raise ValueError(f"accounts are not supported for {provider}")
        client = self.pool.client(key)
        cookies: Any = await browser_cookies(key) if browser else dict(tokens or {})
        if key == "pornhub":
            if browser:
                if not cookies:
                    raise ValueError("PornHub browser cookies were not found")
                client.core.session.cookies.update(cookies)
                client.logged = True
                return True
            client.credentials.update({"email": username, "password": password})
            return bool(await client.login())
        if key == "xhamster":
            account = await client.login(
                username="" if browser or cookies else username,
                password="" if browser or cookies else password,
                cookies=cookies or None,
            )
            client.account = account
            return account is not None

        required = ("session_token", "session_token_auth")
        values = dict(cookies or tokens or {})
        if any(not values.get(name) for name in required):
            raise ValueError("Both XVideos session tokens are required")
        client.account = client.get_account(cookies=values)
        return client.account is not None

    def collection(
        self, provider: str, collection: str, playlist_url: str = ""
    ) -> tuple[AsyncIterator[Any], str]:
        key = provider.casefold()
        name = collection.casefold()
        if not self.logged_in(key):
            raise ValueError(f"log in to {provider} first")
        account = self.pool.client(key).account
        if key == "pornhub":
            methods = {"history": "get_history", "recommended": "get_recommended", "favorites": "get_favorites"}
        elif key == "xhamster":
            methods = {"liked": "get_liked_videos", "playlist": "get_account_playlist"}
            if name == "playlist":
                parsed = urlparse(playlist_url)
                if parsed.scheme != "https" or "xhamster.com" not in (parsed.hostname or "") or "/my/playlists/" not in parsed.path:
                    raise ValueError("a valid XHamster account playlist URL is required")
                return account.get_account_playlist(url=playlist_url), "XHamster account playlist"
        else:
            methods = {
                "watch_later": "get_watch_later_videos", "recommended": "get_recommended_videos",
                "liked": "get_liked_videos",
            }
        method = methods.get(name)
        if not method:
            raise ValueError(f"{collection} is unavailable for {provider}")
        return getattr(account, method)(), f"{provider.title()} {collection.replace('_', ' ')}"


async def browser_cookies(provider: str) -> http.cookiejar.CookieJar:
    return await asyncio.to_thread(_read_browser_cookies, provider)


def _read_browser_cookies(provider: str) -> http.cookiejar.CookieJar:
    import browser_cookie3

    merged = http.cookiejar.CookieJar()
    for name in ("chrome", "firefox", "edge", "brave", "opera", "vivaldi", "safari", "librewolf"):
        loader = getattr(browser_cookie3, name, None)
        if loader is None:
            continue
        try:
            for cookie in loader(domain_name=provider):
                if provider in (cookie.domain or "").casefold():
                    merged.set_cookie(cookie)
        except Exception:
            continue
    return merged
