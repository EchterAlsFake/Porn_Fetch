"""
This file is responsible for managing the login to the sites + automatic cookie retrieval
"""

import asyncio
import http.cookiejar
from collections.abc import AsyncIterator, Mapping

from base_api import ErrorAction, ErrorMode, ScrapeErrorContext, make_iterator_config
from base_api.modules.config import IteratorConfig
from pornhub_api.modules.errors import ClientAlreadyLogged, LoginFailed
from xhamster_api.modules.errors import LoginFailed as xhLoginFailed

from src.backend import clients
from src.shared.errors import CookiesNotFound, LoginError
from src.shared.logging_setup import configure_app_logging
from src.shared.provider_accounts import (
    connect_pornhub_cookies,
    connect_xvideos_cookies,
    valid_xhamster_playlist_url,
    verify_account_session,
)

logger = configure_app_logging(logger_name="PornFetch - [Login Manager]")

_XVIDEOS_LOGIN_COOKIES = ("session_token", "session_token_auth")


def _account_page_error(context: ScrapeErrorContext) -> ErrorAction:
    """A missing later page ends pagination; first-page/auth failures stay visible."""
    if context.page_index > 0:
        error: BaseException | None = context.error
        seen = set()
        while error is not None and id(error) not in seen:
            seen.add(id(error))
            if getattr(error, "status_code", None) == 404:
                return ErrorAction.SKIP
            error = error.__cause__
    return ErrorAction.YIELD


def _account_video_iterator_config(*, post: bool = False) -> IteratorConfig:
    """Load the HTML metadata consumed by the shared video-list pipeline."""
    return make_iterator_config(load_specific_sources=("html",), page_request_method="POST" if post else "GET",
                                page_error_mode=ErrorMode.YIELD, item_error_mode=ErrorMode.YIELD,
                                page_error_handler=_account_page_error)


def provider_is_logged_in(provider: str) -> bool:
    provider_key = provider.strip().casefold()
    if provider_key == "pornhub":
        return bool(clients.ph_client.logged)
    if provider_key == "xhamster":
        return clients.xh_client.account is not None
    if provider_key == "xvideos":
        return clients.xv_client.account is not None
    return False


def get_account_video_iterator(
    provider: str,
    collection: str,
    playlist_url: str = "",
) -> tuple[AsyncIterator, str]:
    """Return a provider account iterator and its user-facing source name."""
    provider_key = provider.strip().casefold()
    collection_key = collection.strip().casefold()

    if not provider_is_logged_in(provider_key):
        raise LoginError(f"Please log in to {provider} before fetching account videos.")

    if provider_key == "pornhub":
        account = clients.ph_client.account
        if collection_key == "history":
            return (
                account.get_history(iterator_config=_account_video_iterator_config()),
                "PornHub watch history",
            )
        if collection_key == "feed":
            return (account.get_feed(section="videos", iterator_config=_account_video_iterator_config()),
                    "PornHub subscription feed")
        if collection_key == "recommended":
            return (
                account.get_recommended(iterator_config=_account_video_iterator_config()),
                "PornHub recommendations",
            )
        if collection_key == "favorites":
            return (
                account.get_favorites(iterator_config=_account_video_iterator_config()),
                "PornHub favorites",
            )

    elif provider_key == "xhamster":
        account = clients.xh_client.account
        if account is None:
            raise LoginError("Please log in to XHamster before fetching account videos.")
        if collection_key == "liked":
            return (
                account.get_liked_videos(
                    iterator_config=_account_video_iterator_config()
                ),
                "XHamster liked videos",
            )
        if collection_key == "playlist":
            if not valid_xhamster_playlist_url(playlist_url):
                raise LoginError("Please enter a valid XHamster account playlist URL.")
            return (
                account.get_account_playlist(
                    url=playlist_url.strip(),
                    iterator_config=_account_video_iterator_config(),
                ),
                "XHamster account playlist",
            )

    elif provider_key == "xvideos":
        account = clients.xv_client.account
        if account is None:
            raise LoginError("Please log in to XVideos before fetching account videos.")
        if collection_key == "watch_later":
            return account.get_watch_later_videos(iterator_config=_account_video_iterator_config(post=True)), "XVideos watch later"
        if collection_key == "history":
            # The pinned provider's method reads /history/, despite its name.
            return account.get_recommended_videos(iterator_config=_account_video_iterator_config(post=True)), "XVideos watch history"
        if collection_key == "liked":
            return account.get_liked_videos(iterator_config=_account_video_iterator_config(post=True)), "XVideos liked videos"

    raise LoginError(f"{collection!r} is not available for {provider} accounts.")


def get_site_cookies(website: str, *, browser_name: str | None = None) -> http.cookiejar.CookieJar:
    """
    Safely queries available desktop browsers for cookies matching site keywords.
    Handles TLD variants automatically and catches platform-specific exceptions.
    """
    merged_jar = http.cookiejar.CookieJar()
    try:
        import browser_cookie3
    except ImportError:
        logger.warning("browser_cookie3 is not available on this platform.")
        return merged_jar

    website = website.lower()
    # Map of loader functions available in browser_cookie3
    browser_loaders = [
        ("Chrome", getattr(browser_cookie3, "chrome", None)),
        ("Firefox", getattr(browser_cookie3, "firefox", None)),
        ("Edge", getattr(browser_cookie3, "edge", None)),
        ("Brave", getattr(browser_cookie3, "brave", None)),
        ("Opera", getattr(browser_cookie3, "opera", None)),
        ("Vivaldi", getattr(browser_cookie3, "vivaldi", None)),
        ("Safari", getattr(browser_cookie3, "safari", None)),
        ("LibreWolf", getattr(browser_cookie3, "librewolf", None)),
    ]

    found_domains: set[str] = set()

    for candidate_name, loader in browser_loaders:
        if browser_name is not None and candidate_name.casefold() != browser_name.casefold():
            continue
        if loader is None:
            continue

        try:
            # Fetch cookies from this specific browser
            jar = loader(domain_name=website)

            for cookie in jar:
                domain = (cookie.domain or "").lower()

                # Check if the cookie domain contains any of our target keywords
                if website in domain:
                    merged_jar.set_cookie(cookie)
                    found_domains.add(domain)

        except Exception as e:
            # Catch common issues: missing browsers, locked DBs, OS keychain denials
            logger.debug("Skipping %s: %s", candidate_name, type(e).__name__)
            continue

    logger.info(f"Successfully extracted cookies for domains: {found_domains}")
    return merged_jar


class LoginPornhub:
    @staticmethod
    async def login(email: str = "", password: str = "", from_browser: bool = False) -> bool:
        if from_browser:
            logger.info("Trying Login for PornHub... [Cookies - Browser]")
            cookies = await asyncio.to_thread(get_site_cookies, "pornhub")
            if cookies:
                logger.info("Injecting Cookies!")
                return await connect_pornhub_cookies(clients.ph_client, cookies, email)

            raise CookiesNotFound

        try:
            logger.info("Trying Login for PornHub.... [Authentication]")
            clients.ph_client.credentials.update({"email": email, "password": password})
            if await clients.ph_client.login():
                logger.info("Login Successful!")
                return True

            else:
                logger.error("Login failed for an unknown reason!")
                return False

        except LoginFailed:
            logger.error("Login failed for an unknown reason! [2]")
            raise

        except ClientAlreadyLogged:
            logger.error("You are already logged in!")
            raise


class LoginXhamster:
    @staticmethod
    async def login(
        username: str | None = None,
        password: str | None = None,
        custom_cookies: Mapping[str, str] | None = None,
        from_browser: bool = False,
    ) -> bool:
        try:
            if custom_cookies:
                logger.info("Trying Login for XHamster [Cookies]")
                clients.xh_client.account = None
                clients.xh_client.core.initialize_session()
                session = clients.xh_client.core.session
                if session is None:
                    raise LoginError("Could not initialize the XHamster session")
                session.cookies.clear()
                account = await clients.xh_client.login(
                    username="",
                    password="",
                    cookies=dict(custom_cookies),
                )
                await verify_account_session(clients.xh_client, "xhamster")
                clients.xh_client.account = account
                return account is not None

            if username and password:
                logger.info("Trying Login for Xhamster [Authentication]")
                account = await clients.xh_client.login(username=username, password=password)
                clients.xh_client.account = account
                return account is not None

            if from_browser:
                logger.info("Trying Login for Xhamster [Cookies - Browser]")
                cookies = await asyncio.to_thread(get_site_cookies, "xhamster")
                if cookies:
                    logger.info("Injecting Cookies!")
                    clients.xh_client.account = None
                    clients.xh_client.core.initialize_session()
                    session = clients.xh_client.core.session
                    if session is None:
                        raise LoginError("Could not initialize the XHamster session")
                    session.cookies.clear()
                    account = await clients.xh_client.login(
                        username="",
                        password="",
                        cookies=cookies,
                    )
                    await verify_account_session(clients.xh_client, "xhamster")
                    clients.xh_client.account = account
                    return account is not None

                raise CookiesNotFound

            return False

        except xhLoginFailed as e:
            logger.info(f"Login failed due to an unknown reason! ->: {e}")
            raise


class LoginXVideos:
    @staticmethod
    async def login(
        custom_cookies: Mapping[str, str] | None = None,
        from_browser: bool = False,
    ) -> bool:
        browser_jar = None
        if from_browser:
            logger.info("Trying Login for XVideos [Cookies - Browser]")
            browser_cookies = await asyncio.to_thread(get_site_cookies, "xvideos")
            if not browser_cookies:
                raise CookiesNotFound

            browser_jar = browser_cookies
            custom_cookies = {
                cookie.name: cookie.value
                for cookie in browser_cookies
                if cookie.name in _XVIDEOS_LOGIN_COOKIES and cookie.value
            }

        cookies = dict(custom_cookies or {})
        missing = [name for name in _XVIDEOS_LOGIN_COOKIES if not cookies.get(name)]
        if missing:
            if from_browser:
                raise CookiesNotFound(
                    "XVideos login cookies were not found. Make sure you are logged in to "
                    "XVideos in a supported browser."
                )
            raise LoginError(
                "Both the XVideos session token and session token auth are required."
            )

        logger.info("Trying Login for XVideos [Cookies]")
        return await connect_xvideos_cookies(clients.xv_client, cookies, browser_jar=browser_jar)
