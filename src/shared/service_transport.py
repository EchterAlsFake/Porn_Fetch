"""Explicit routing for app-owned services, independent of media networking."""
from __future__ import annotations

import asyncio
from collections.abc import Callable
from urllib.parse import urlsplit

from base_api import BaseCore
from base_api.modules.config import RuntimeConfig
from curl_cffi import requests
from curl_cffi.const import CurlOpt
from tuf.ngclient.fetcher import FetcherInterface

from .tor_runtime import TorUnavailable, runtime

ONION_ORIGIN = "http://pornfetchc5ct7s7uiervf4ziymmus5gy33gyqc6vkdtqyr5pbxrxmid.onion"
SERVICE_ORIGINS = {"https://api.pornfetch.to": "", "https://pornfetch.to": "", "https://licenses.pornfetch.to": "/licensing"}
failure_listener: Callable[[str], None] | None = None
NETWORK_ERRORS = (ConnectionError, TimeoutError, requests.exceptions.RequestException)


class TorServiceFailure(TorUnavailable):
    """A failure on the app-owned service route, never a media-provider error."""


def service_failure_message(kind):
    detail = {
        "bootstrap": "Tor could not start or connect for Porn Fetch updates and licensing.",
        "connection": "Porn Fetch's update or licensing server could not be reached through Tor. The onion service or Tor connection may be unavailable.",
        "server": "Porn Fetch's update or licensing server returned a temporary error over Tor. Tor itself may still be connected.",
    }[kind]
    return (detail + "\n\nNo direct connection was attempted. Retry, or turn off Tor by selecting Off under "
            "Tor routing in Privacy settings and retry using a direct connection.\n\n"
            "If All app traffic is selected, video downloads and third-party websites also require Tor.")


def service_mode(settings=None):
    value = getattr(settings, "service_transport", None)
    if value == "tor_all":
        return "tor"
    if value in {"direct", "tor"}:
        return value
    return "tor" if getattr(settings, "enable_tor", False) and getattr(settings, "enable_tor_server_routing", False) else "direct"


class ServicePolicy:
    def __init__(self, settings=None, *, manager=None):
        self.settings = settings
        self.manager = manager or runtime
        self.last_failure = ""
        self._qt_mode = None
        changed = getattr(settings, "serviceTransportChanged", None)
        if changed is not None and hasattr(changed, "connect"):
            self._qt_mode = service_mode(settings)
            changed.connect(self._set_mode)

    def _set_mode(self, value):
        self._qt_mode = "tor" if value == "tor_all" else value
        self.last_failure = ""

    def failed(self, kind):
        message = service_failure_message(kind)
        self.last_failure = message
        if failure_listener is not None:
            try:
                failure_listener(message)
            except RuntimeError:
                # A queued GUI adapter may already have been destroyed on exit.
                pass
        return TorServiceFailure(message)

    def ready(self):
        try:
            return self.manager.ensure_ready()
        except (TorUnavailable, OSError) as error:
            raise self.failed("bootstrap") from error

    def response_received(self, status, *, via_tor):
        if via_tor and status >= 500:
            self.failed("server")
        elif 200 <= status < 300:
            self.last_failure = ""

    @property
    def tor_enabled(self):
        return (self._qt_mode if self._qt_mode is not None else service_mode(self.settings)) == "tor"

    def route(self, url):
        parsed = urlsplit(url)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        if parsed.username or parsed.password or parsed.fragment:
            raise ValueError("Invalid service URL")
        if not self.tor_enabled:
            if parsed.scheme != "https":
                raise ValueError("Direct service requests require HTTPS")
            return url, None
        if origin == ONION_ORIGIN:
            rewritten = url
        elif origin in SERVICE_ORIGINS:
            rewritten = ONION_ORIGIN + SERVICE_ORIGINS[origin] + parsed.path
            if parsed.query:
                rewritten += "?" + parsed.query
        else:
            raise TorUnavailable("This service has no configured onion route")
        proxy = self.ready()
        if not self.tor_enabled:
            self.manager.stop()
            raise TorUnavailable("Tor routing changed while connecting")
        return rewritten, proxy


class ServiceCore(BaseCore):
    def __init__(self, settings=None, *, policy=None):
        self.policy = policy or ServicePolicy(settings)
        config = RuntimeConfig()
        config.verify_ssl = True
        config.trust_env = False
        config.cookies = None
        config.request_attempts = 1
        config.http_version = "v2"
        config.dns_over_https = None
        super().__init__(configuration=config)

    def initialize_session(self):
        super().initialize_session()
        if self.session is not None:
            self.session.curl_options[CurlOpt.NOPROXY] = b""

    @property
    def tor_enabled(self):
        return self.policy.tor_enabled

    async def prepare(self):
        if self.tor_enabled:
            await asyncio.to_thread(self.policy.ready)

    async def request(self, url, *, method="GET", headers=None, json_data=None,
                      timeout=(30, 120), allow_redirects=False, retry_non_idempotent=False):
        routed, proxy = await asyncio.to_thread(self.policy.route, url)
        self.initialize_session()
        assert self.session is not None
        # Explicit request options prevent session/environment proxy inheritance.
        try:
            response = await self.session.request(method=method, url=routed, headers=headers, json=json_data,
                                                 timeout=timeout, allow_redirects=False, verify=True,
                                                 proxy=proxy or "")
        except NETWORK_ERRORS as error:
            if proxy:
                raise self.policy.failed("connection") from error
            raise
        self.policy.response_received(response.status_code, via_tor=bool(proxy))
        return response

    async def fetch_bytes(self, url, **kwargs):
        response = await self.request(url, **kwargs)
        response.raise_for_status()
        return response.content

    async def download_verified(self, url, target, path):
        routed, proxy = await asyncio.to_thread(self.policy.route, url)
        self.initialize_session()
        assert self.session is not None
        total = 0
        try:
            async with self.session.stream("GET", routed, proxy=proxy or "", allow_redirects=False,
                                           verify=True, timeout=(30, 120)) as response:
                self.policy.response_received(response.status_code, via_tor=bool(proxy))
                if response.status_code != 200:
                    raise ValueError("Update download failed")
                with path.open("wb") as destination:
                    async for chunk in response.aiter_content(chunk_size=65536):
                        total += len(chunk)
                        if total > target.length:
                            raise ValueError("Update download exceeds signed length")
                        destination.write(chunk)
            with path.open("rb") as source:
                target.verify_length_and_hashes(source)
        except NETWORK_ERRORS as error:
            path.unlink(missing_ok=True)
            if proxy:
                raise self.policy.failed("connection") from error
            raise
        except BaseException:
            path.unlink(missing_ok=True)
            raise


class ServiceFetcher(FetcherInterface):
    """Synchronous streaming TUF adapter; TUF owns size/hash verification."""
    def __init__(self, settings=None, *, policy=None):
        self.policy = policy or ServicePolicy(settings)
        self.on_chunk = None

    def _fetch(self, url):
        routed, proxy = self.policy.route(url)
        try:
            with requests.Session(trust_env=False, verify=True, curl_options={CurlOpt.NOPROXY: b""}) as session:
                with session.stream("GET", routed, proxy=proxy or "", allow_redirects=False,
                                    timeout=(30, 120)) as response:
                    self.policy.response_received(response.status_code, via_tor=bool(proxy))
                    if response.status_code != 200:
                        from tuf.api.exceptions import DownloadHTTPError
                        raise DownloadHTTPError("Update download failed", response.status_code)
                    for chunk in response.iter_content(chunk_size=65536):
                        if self.on_chunk:
                            self.on_chunk(len(chunk))
                        yield chunk
        except NETWORK_ERRORS as error:
            if proxy:
                raise self.policy.failed("connection") from error
            raise
