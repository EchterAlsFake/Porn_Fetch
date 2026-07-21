"""
This file is responsible for managing the login to the sites + automatic cookie retrieval
"""

import http
import browser_cookie3

from src.backend import clients
from base_api.modules.logger import configure_app_logging
from src.backend.errors import CookiesNotFound, LoginError
from xhamster_api.modules.errors import LoginFailed as xhLoginFailed
from pornhub_api.modules.errors import LoginFailed, ClientAlreadyLogged


logger = configure_app_logging(logger_name="PornFetch - [Login Manager]")


def get_site_cookies(website: str) -> http.cookiejar.CookieJar:
    """
    Safely queries available desktop browsers for cookies matching site keywords.
    Handles TLD variants automatically and catches platform-specific exceptions.
    """
    merged_jar = http.cookiejar.CookieJar()
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

    for browser_name, loader in browser_loaders:
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
            logger.debug(f"Skipping {browser_name}: {e}")
            continue

    logger.info(f"Successfully extracted cookies for domains: {found_domains}")
    return merged_jar


class LoginPornhub:
    @staticmethod
    async def login(email: str, password: str, from_browser: bool = False):
        if from_browser:
            logger.info("Trying Login for PornHub... [Cookies - Browser]")
            cookies = get_site_cookies(website="pornhub")
            if cookies:
                logger.info("Injecting Cookies!")
                clients.ph_client.core.session.cookies.update(cookies)
                return True

            raise CookiesNotFound

        try:
            logger.info("Trying Login for PornHub.... [Authentication]")
            clients.ph_client = clients.ph_Client(email=email, password=password, core=clients.ph_client.core)

            if clients.ph_client.logged:
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
    async def login(username: str | None = None, password: str | None = None,  custom_cookies: dict | None = None,
              from_browser: bool = False) -> bool:
        try:
            if custom_cookies:
                logger.info("Trying Login for XHamster [Cookies]")
                await clients.xh_client.login(cookies=custom_cookies)

                if clients.xh_client.account:
                    return True

                else:
                    logger.error("Login failed for an unknown reason!")
                    return False


            elif username and password:
                logger.info("Trying Login for Xhamster [Authentication]")
                await clients.xh_client.login(username=username, password=password)

                if clients.xh_client.account:
                    return True

                else:
                    logger.error("Login failed for an unknown reason!")
                    return False

            elif from_browser:
                logger.info("Trying Login for Xhamster [Cookies - Browser]")
                cookies = get_site_cookies("xhamster")
                if cookies:
                    logger.info("Injecting Cookies!")
                    clients.xh_client.core.session.cookies.update(cookies)

                    return True

                raise CookiesNotFound

        except xhLoginFailed as e:
            logger.info(f"Login failed due to an unknown reason! ->: {e}")
            raise xhLoginFailed(str(e))


class LoginXVideos:
    @staticmethod
    async def login(custom_cookies: dict | None = None, from_browser: bool = False) -> bool:
        try:
            if from_browser:
                logger.info("Trying Login for XVideos [Cookies - Browser]")
                cookies = get_site_cookies("xvideos")
                if cookies:
                    logger.info("Injecting Cookies!")
                    clients.xv_client.core.session.cookies.update(cookies)
                    return True

                raise CookiesNotFound

            if custom_cookies:
                logger.info("Trying Login for XVideos [Cookies]")
                clients.xv_client.core.session.cookies.update(custom_cookies)
                return True

        except Exception as e:
            raise LoginError(str(e))
