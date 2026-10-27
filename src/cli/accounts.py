"""Memory-only account login and collection routing."""
from __future__ import annotations

import asyncio
import http.cookiejar
import logging
import re
from collections.abc import AsyncIterator, Mapping
from typing import Any

from src.shared.provider_accounts import (
    connect_pornhub_cookies,
    connect_xvideos_cookies,
    valid_xhamster_playlist_url,
    verify_account_session,
)
from src.shared.provider_routing import HOST_PATTERNS

from .providers import ClientPool

logger = logging.getLogger(__name__)


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
        browser_name: str | None = None,
    ) -> bool:
        key = provider.casefold()
        if key not in {"pornhub", "xhamster", "xvideos"}:
            raise ValueError(f"accounts are not supported for {provider}")
        client = self.pool.client(key)
        cookies: Any = await browser_cookies(key, browser_name=browser_name) if browser else dict(tokens or {})
        if browser or cookies:
            if key == "pornhub":
                client.logged = False
            else:
                client.account = None
            client.core.session.cookies.clear()
            client.core.session.cookies.update(cookies)
        if key == "pornhub":
            if browser:
                return await connect_pornhub_cookies(client, cookies, username)
            client.credentials.update({"email": username, "password": password})
            return bool(await client.login())
        if key == "xhamster":
            client.account = None
            account = await client.login(
                username="" if browser or cookies else username,
                password="" if browser or cookies else password,
                cookies=cookies or None,
            )
            if cookies:
                await verify_account_session(client, key)
            client.account = account
            return account is not None

        required = ("session_token", "session_token_auth")
        values = ({cookie.name: cookie.value for cookie in cookies}
                  if isinstance(cookies, http.cookiejar.CookieJar) else dict(cookies or {}))
        if any(not values.get(name) for name in required):
            raise ValueError("Both XVideos session tokens are required")
        return await connect_xvideos_cookies(client, values, browser_jar=cookies if browser else None)

    def collection(
        self, provider: str, collection: str, playlist_url: str = "", *, pages: int | None = None
    ) -> tuple[AsyncIterator[Any], str]:
        key = provider.casefold()
        name = collection.casefold()
        if not self.logged_in(key):
            raise ValueError(f"log in to {provider} first")
        account = self.pool.client(key).account
        options = {} if pages is None else {"pages": pages}
        if key == "pornhub":
            methods = {"history": "get_history", "recommended": "get_recommended", "favorites": "get_favorites", "feed": "get_feed"}
        elif key == "xhamster":
            methods = {"liked": "get_liked_videos", "playlist": "get_account_playlist"}
            if name == "playlist":
                if not valid_xhamster_playlist_url(playlist_url):
                    raise ValueError("a valid XHamster account playlist URL is required")
                return account.get_account_playlist(url=playlist_url, **options), "XHamster account playlist"
        else:
            methods = {
                "watch_later": "get_watch_later_videos", "history": "get_recommended_videos",
                "liked": "get_liked_videos",
            }
        method = methods.get(name)
        if not method:
            raise ValueError(f"{collection} is unavailable for {provider}")
        return getattr(account, method)(**options), f"{provider.title()} {collection.replace('_', ' ')}"


async def browser_cookies(provider: str, *, browser_name: str | None = None) -> http.cookiejar.CookieJar:
    return await asyncio.to_thread(_read_browser_cookies, provider, browser_name=browser_name)


def _read_browser_cookies(provider: str, *, browser_name: str | None = None) -> http.cookiejar.CookieJar:
    try:
        import browser_cookie3
    except ImportError:
        logger.warning("browser_cookie3 is not available on this platform.")
        return http.cookiejar.CookieJar()

    names = ("chrome", "firefox", "edge", "brave", "opera", "vivaldi", "safari", "librewolf")
    if browser_name is not None and browser_name not in names:
        raise ValueError("Unsupported browser")
    merged = http.cookiejar.CookieJar()
    for name in (browser_name,) if browser_name else names:
        loader = getattr(browser_cookie3, name, None)
        if loader is None:
            continue
        try:
            for cookie in loader(domain_name=provider):
                if re.search(HOST_PATTERNS[provider], cookie.domain or "", re.I):
                    merged.set_cookie(cookie)
        except Exception as error:
            logger.debug(
                "Could not read %s cookies for provider %s: %s",
                name,
                provider,
                type(error).__name__,
            )
            continue
    return merged
