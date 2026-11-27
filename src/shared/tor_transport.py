"""Tor routing for provider requests, including BaseCore's streaming downloads."""
from __future__ import annotations

import asyncio
from copy import copy
from functools import wraps

from base_api import BaseCore
from curl_cffi import CurlError
from curl_cffi.const import CurlOpt

from .public_media import RestrictedMediaError, check_public_host
from .tor_runtime import TorUnavailable, runtime

FAIL_CLOSED_PROXY = "socks5h://127.0.0.1:9"
ALL_TRAFFIC_NOTICE = (
    "Use Tor for all app traffic only if you live in a censored country where consuming "
    "pornography is illegal and can lead to jail time or other punishments.\n\n"
    "Video downloads use substantial bandwidth and slow the Tor network down for everyone else. "
    "Using Tor for downloads is morally discouraged unless it is strictly necessary.\n\n"
    "This routes Porn Fetch's Internet requests through Tor. It does not route other apps or "
    "links opened in your external browser, and it does not guarantee anonymity or safety."
)

_settings = None


def configure(settings):
    """Set the active frontend's settings for auxiliary app network requests."""
    global _settings
    _settings = settings


def all_traffic_enabled(settings=None):
    return getattr(settings if settings is not None else _settings, "service_transport", "direct") == "tor_all"


def tor_options(proxy):
    """Force remote DNS and TCP, ignoring environment bypasses and custom proxies."""
    return dict(proxy=proxy, trust_env=False, interface=None, http_version="v2",
                curl_options={CurlOpt.NOPROXY: b"", CurlOpt.DOH_URL: b"", CurlOpt.RESOLVE: [],
                              CurlOpt.ECH: b"false"})


class MediaCore(BaseCore):
    def __init__(self, configuration, *, settings=None, manager=None, account_only=False):
        super().__init__(configuration=configuration)
        self.account_only = account_only
        self.routing_settings = settings if settings is not None else configuration
        self.tor_manager = manager or runtime
        self._dns_fallback_core = None
        self._dns_fallback_session = None
        self._dns_fallback_lock = asyncio.Lock()

    def clone_for_retry(self, configuration):
        """Retain the same routing and account boundary when a provider renews a session."""
        return MediaCore(configuration, settings=self.routing_settings, manager=self.tor_manager,
                         account_only=self.account_only)

    def validate_playback(self, url, *, is_premium=None):
        if not self.account_only:
            check_public_host(url)
            if is_premium is True:
                raise RestrictedMediaError()

    async def close(self):
        if self._dns_fallback_core is not None:
            await self._dns_fallback_core.close()
            self._dns_fallback_core = None
            self._dns_fallback_session = None
        await super().close()

    async def _fallback_dns_request(self, session, args, kwargs):
        async with self._dns_fallback_lock:
            if self._dns_fallback_core is None or self._dns_fallback_session is not session:
                if self._dns_fallback_core is not None:
                    await self._dns_fallback_core.close()
                configuration = copy(self.configuration)
                configuration.dns_over_https = configuration.fallback_dns
                configuration.fallback_dns = None
                fallback = self.clone_for_retry(configuration)
                fallback.default_headers.update(self.default_headers)
                fallback.initialize_session()
                assert fallback.session is not None
                fallback.session.headers.update(session.headers)
                fallback.session.cookies.update(session.cookies)
                fallback.session.curl_options.update(session.curl_options)
                fallback.session.curl_options[CurlOpt.DOH_URL] = str(configuration.dns_over_https).encode()
                self._dns_fallback_core, self._dns_fallback_session = fallback, session
            fallback_session = self._dns_fallback_core.session
            assert fallback_session is not None
            fallback_session.headers.clear()
            fallback_session.headers.update(session.headers)
            fallback_session.cookies.clear()
            fallback_session.cookies.update(session.cookies)
        return await fallback_session.request(*args, **kwargs)

    def initialize_session(self):
        super().initialize_session()
        session = self.session
        if session is None or getattr(session, "_tor_routed", False):
            return
        request = session.request

        @wraps(request)
        async def routed_request(*args, **kwargs):
            if not self.account_only:
                url = kwargs.get("url") or (args[1] if len(args) > 1 else "")
                check_public_host(str(url))
            if all_traffic_enabled(self.routing_settings):
                # Guard the session, rather than only BaseCore.request: raw MP4
                # range downloads and streams also call the session directly.
                proxy = await asyncio.to_thread(self.tor_manager.ensure_ready)
                if not all_traffic_enabled(self.routing_settings):
                    raise TorUnavailable("Tor routing changed while connecting; retry the request")
                session.curl_options.update(tor_options(proxy)["curl_options"])
                session.trust_env = False
                session.interface = None
                session.proxy_auth = None
                kwargs.pop("proxies", None)
                kwargs.update(proxy=proxy, proxy_auth=None, interface=None, http_version="v2", verify=True)
            try:
                response = await request(*args, **kwargs)
            except CurlError as error:
                fallback = getattr(self.configuration, "fallback_dns", None)
                if (error.code != 6 or not self.configuration.dns_over_https or not fallback
                        or fallback == self.configuration.dns_over_https or all_traffic_enabled(self.routing_settings)):
                    raise
                self.logger.info("Primary DNS over HTTPS failed; trying the configured fallback")
                response = await self._fallback_dns_request(session, args, kwargs)
            if not self.account_only:
                try:
                    check_public_host(str(getattr(response, "url", "")))
                except RestrictedMediaError:
                    if kwargs.get("stream"):
                        if stop := getattr(response, "quit_now", None):
                            stop.set()
                        await response.aclose()
                    raise
            return response

        session.request = routed_request
        session._tor_routed = True
