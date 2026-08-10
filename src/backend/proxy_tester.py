"""Validation and connectivity testing for user supplied proxy URLs."""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlsplit

from curl_cffi.const import CurlInfo
from curl_cffi.requests import AsyncSession


PROXY_TEST_URL = "https://speed.cloudflare.com/__down?bytes=262144"
SUPPORTED_PROXY_SCHEMES = frozenset(
    {"http", "https", "socks4", "socks4a", "socks5", "socks5h"}
)


@dataclass(frozen=True, slots=True)
class ProxyTestResult:
    response_time_ms: int
    connection_time_ms: int
    connection_speed_mbps: float
    ssl_verified: bool
    status_code: int
    remote_ip: str
    downloaded_bytes: int
    ssl_verification_enabled: bool

    def as_qml_map(self) -> dict[str, object]:
        return {
            "responseTimeMs": self.response_time_ms,
            "connectionTimeMs": self.connection_time_ms,
            "connectionSpeedMbps": self.connection_speed_mbps,
            "sslStatus": (
                "Verification disabled"
                if not self.ssl_verification_enabled
                else "Verified"
                if self.ssl_verified
                else "Not verified"
            ),
            "sslVerificationEnabled": self.ssl_verification_enabled,
            "statusCode": self.status_code,
            "remoteIp": self.remote_ip,
            "downloadedBytes": self.downloaded_bytes,
        }


def validate_proxy_url(proxy_url: str) -> str:
    """Return a normalized proxy URL or raise ``ValueError`` with a UI-safe reason."""
    proxy_url = proxy_url.strip()
    if not proxy_url:
        raise ValueError("Enter a proxy address.")
    if re.search(r"\s", proxy_url):
        raise ValueError("The proxy URL cannot contain whitespace.")

    try:
        parsed = urlsplit(proxy_url)
        port = parsed.port
    except ValueError as error:
        raise ValueError("The proxy host or port is malformed.") from error

    if parsed.scheme.lower() not in SUPPORTED_PROXY_SCHEMES:
        raise ValueError("Choose HTTP, HTTPS, SOCKS4, SOCKS4A, SOCKS5, or SOCKS5H.")
    if not parsed.hostname:
        raise ValueError("Enter a proxy host.")
    if port is None:
        raise ValueError("Enter a proxy port.")
    if not 1 <= port <= 65535:
        raise ValueError("The proxy port must be between 1 and 65535.")
    if parsed.path not in ("", "/") or parsed.query or parsed.fragment:
        raise ValueError("A proxy URL cannot contain a path, query, or fragment.")

    return proxy_url


async def test_proxy(
    proxy_url: str,
    timeout: float,
    verify_ssl: bool = True,
) -> ProxyTestResult:
    """Make an HTTPS request through ``proxy_url`` and collect basic stats."""
    proxy_url = validate_proxy_url(proxy_url)
    info_fields = [
        CurlInfo.CONNECT_TIME,
        CurlInfo.STARTTRANSFER_TIME,
        CurlInfo.SSL_VERIFYRESULT,
        CurlInfo.PROXY_SSL_VERIFYRESULT,
    ]

    async with AsyncSession(
        proxy=proxy_url,
        timeout=timeout,
        verify=verify_ssl,
        trust_env=False,
        curl_infos=info_fields,
    ) as session:
        response = await session.get(PROXY_TEST_URL)
        response.raise_for_status()

    total_seconds = max(response.elapsed.total_seconds(), 0.001)
    downloaded_bytes = response.download_size or len(response.content)
    speed_mbps = (downloaded_bytes * 8) / total_seconds / 1_000_000

    return ProxyTestResult(
        response_time_ms=round(
            float(response.infos.get(CurlInfo.STARTTRANSFER_TIME, total_seconds)) * 1000
        ),
        connection_time_ms=round(
            float(response.infos.get(CurlInfo.CONNECT_TIME, 0.0)) * 1000
        ),
        connection_speed_mbps=round(speed_mbps, 2),
        ssl_verified=(
            verify_ssl
            and response.infos.get(CurlInfo.SSL_VERIFYRESULT, 1) == 0
            and response.infos.get(CurlInfo.PROXY_SSL_VERIFYRESULT, 0) == 0
        ),
        status_code=response.status_code,
        remote_ip=response.primary_ip,
        downloaded_bytes=downloaded_bytes,
        ssl_verification_enabled=verify_ssl,
    )
