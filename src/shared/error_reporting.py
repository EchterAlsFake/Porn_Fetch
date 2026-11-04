"""Optional, best-effort exception reports to the private error-log receiver."""
from __future__ import annotations

import json
import logging
import platform
import re
import sys
import traceback
import uuid
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from base_api.modules.errors import MediaLoadErrors
from curl_cffi.requests import AsyncSession

from .version import __version__

ERROR_REPORT_URL = "https://api.pornfetch.to/error_log"
MAX_BODY_BYTES = 1_048_576
ERROR_REPORT_CONSENT_VERSION = 2
_LOGGER = logging.getLogger(__name__)

ERROR_REPORT_DISCLOSURE = """Error reports are optional and disabled until you explicitly enable them. If enabled, Porn Fetch automatically sends a detailed report after an operation fails. You can decline and still use all app features.

What a report contains
- A random correlation ID to identify that error.
- The UTC timestamp, app version, operating system and CPU architecture.
- The full Python traceback, including chained exceptions, error messages, source-code lines, filenames and line numbers.
- The video URL that caused the failure, including its path and query string, when available. Related playlist, model or source URLs may also be included.
- The operation, code location and diagnostic context, such as the provider and selected quality.

These details can reveal which adult content you accessed. URLs, error messages and file paths can contain sensitive or personal information, such as account details, URL tokens or your local username. Reports are not anonymous. Python local-variable dumps, browsing history and download records are not collected. The app does not attach account credentials, cookies or authorization headers, but sensitive values may appear in the traceback or URLs.

How reports are sent
Reports are sent over HTTPS directly to the developer's server at api.pornfetch.to/error_log. They are securely stored on that server, never shared with third parties and used only to reproduce, diagnose and fix application errors. Media-provider proxy settings do not control this connection; the app's All app traffic Tor setting applies separately.

The server receives connection metadata while handling the request. It is configured not to log or store client IP addresses in diagnostic records. If sending a report fails, your download continues.

Storage and deletion
Reports are stored privately in PocketBase and deleted manually. The operator plans to delete them with the next published version. There is no fixed storage period or automatic cleanup.

Turning this off stops future reports. It does not delete reports already sent or change the lawfulness of their earlier processing. To request deletion, send the correlation ID to support@echteralsfake.me.

If you previously enabled reports containing only structural diagnostics, you must choose again before these more detailed reports can be sent.

Privacy details: https://pornfetch.to/privacy_policy"""

ERROR_REPORT_EXAMPLE = """Porn Fetch error report
correlation_id=a1b2c3d4e5f6
timestamp=2026-10-14T12:00:00+00:00
version=3.9
platform=Linux-x86_64
error_type=RuntimeError
operation=prepare scraped video
location=ProcessVideos.start_processing
context={"video_url":"https://example.com/watch?v=42","provider":"example"}

Traceback (most recent call last):
  File "video_processor.py", line 180, in start_processing
    video = await get_video(video_url)
  File "provider.py", line 42, in get_video
    raise RuntimeError("Could not load video sources")
RuntimeError: Could not load video sources"""

_URL_RE = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
_EMAIL_RE = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")
_IPV4_RE = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
_IPV6_RE = re.compile(r"(?<![\w:])(?:[0-9A-Fa-f]{0,4}:){2,7}[0-9A-Fa-f]{0,4}(?![\w:])")
_HEADER_SECRET_RE = re.compile(
    r"(?im)\b(authorization|proxy-authorization|cookie|set-cookie)(\s*[:=]\s*)[^\r\n]+"
)
_HOME_PATH_RE = re.compile(
    r"(?i)(?<![A-Za-z0-9_.:/])(?:[A-Z]:\\Users\\|/(?:home|Users)/)[^/\\\s]+"
)
_SECRET_RE = re.compile(
    r"(?i)\b(authorization|cookie|set-cookie|password|passwd|proxy_auth|"
    r"api[_-]?key|license[_-]?key|secret|session[_-]?token|token)\b"
    r"(\s*[:=]\s*)(\"[^\"\r\n]*\"|'[^'\r\n]*'|[^\s,;}]+)"
)
_CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def safe_url(value: str) -> str:
    """Retain only the scheme and hostname; omit all content-specific URL parts."""
    try:
        parsed = urlsplit(value.strip())
    except ValueError:
        return "[invalid URL]"
    if parsed.scheme.casefold() not in {"http", "https"} or not parsed.hostname:
        return "[invalid URL]"
    host = parsed.hostname
    if _IPV4_RE.fullmatch(host) or ":" in host:
        host = "[IP redacted]"
    return urlunsplit((parsed.scheme.casefold(), host, "/", "", ""))


def redact_log_text(value: object) -> str:
    """Hide sensitive details in local notification text, separate from reports."""
    text = _CONTROL_RE.sub("", str(value))
    text = _URL_RE.sub(lambda match: safe_url(match.group(0).rstrip(".,);]")), text)
    text = _HEADER_SECRET_RE.sub(
        lambda match: f"{match.group(1)}{match.group(2)}[REDACTED]", text,
    )
    text = _SECRET_RE.sub(lambda match: f"{match.group(1)}{match.group(2)}[REDACTED]", text)
    text = _EMAIL_RE.sub("[EMAIL REDACTED]", text)
    text = _IPV4_RE.sub("[IP REDACTED]", text)
    text = _IPV6_RE.sub("[IP REDACTED]", text)
    text = _HOME_PATH_RE.sub("[USER HOME]", text)
    return text


def _format_traceback(error: BaseException) -> str:
    diagnostic = traceback.TracebackException.from_exception(
        error, capture_locals=False,
        max_group_width=sys.maxsize, max_group_depth=sys.maxsize,
    )
    return "".join(diagnostic.format(chain=True))


def build_error_report(
    error: BaseException,
    *,
    operation: str,
    location: str,
    context: Mapping[str, Any] | None = None,
    correlation_id: str | None = None,
    version: str = __version__,
) -> tuple[str, str]:
    """Keep the complete exception chain and supplied reproduction context."""
    report_id = correlation_id or uuid.uuid4().hex[:12]
    diagnostic = _format_traceback(error)
    # The provider API keeps source tracebacks in a tuple rather than in the
    # Python exception chain, so standard traceback formatting omits them.
    current = error
    seen = set()
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        if isinstance(current, MediaLoadErrors):
            for index, source_error in enumerate(current.errors, start=1):
                diagnostic += f"\nMedia source failure {index}:\n" + _format_traceback(source_error)
        current = current.__cause__ or (None if current.__suppress_context__ else current.__context__)
    message = "\n".join([
        "Porn Fetch error report",
        f"correlation_id={report_id}",
        f"timestamp={datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"version={version}",
        f"platform={platform.system()}-{platform.machine()}",
        f"error_type={type(error).__name__}",
        f"operation={operation}",
        f"location={location}",
        "context=" + json.dumps(dict(context or {}), ensure_ascii=False, default=str),
        "",
        diagnostic,
    ])
    return message, report_id


def _payload_bytes(message: str) -> bytes:
    return json.dumps(
        {"message": message}, ensure_ascii=False, separators=(",", ":"),
    ).encode("utf-8")


async def report_public_error(message: str) -> bool:
    """Submit an already formatted diagnostic without propagating failures."""
    if not message.strip():
        return False
    body = _payload_bytes(message)
    if len(body) > MAX_BODY_BYTES:
        _LOGGER.warning("Error report exceeds the receiver's request limit; report was not sent")
        return False
    try:
        from src.shared.tor_transport import all_traffic_enabled, runtime, tor_options
        options = {}
        if all_traffic_enabled():
            import asyncio
            options = tor_options(await asyncio.to_thread(runtime.ensure_ready))
        session = AsyncSession(
            headers={"Content-Type": "application/json"},
            cookies={},
            discard_cookies=True,
            default_headers=False,
            **(options or {"trust_env": False}),
        )
    except Exception:
        _LOGGER.debug("Could not create error-report session", exc_info=True)
        return False
    try:
        response = await session.post(
            ERROR_REPORT_URL,
            content=body,
            timeout=5,
            allow_redirects=False,
        )
        if response.status_code == 204:
            return True
        if response.status_code != 429:
            _LOGGER.warning("Error report was rejected with HTTP %s", response.status_code)
    except Exception:
        _LOGGER.debug("Error report delivery failed", exc_info=True)
    finally:
        try:
            await session.close()
        except Exception:
            _LOGGER.debug("Could not close error-report session", exc_info=True)
    return False


async def report_exception(
    error: BaseException,
    *,
    operation: str,
    location: str,
    context: Mapping[str, Any] | None = None,
    enabled: bool,
    version: str = __version__,
) -> str:
    """Report an exception when opted in and always return a local correlation ID."""
    report_id = uuid.uuid4().hex[:12]
    try:
        if enabled:
            message, report_id = build_error_report(
                error,
                operation=operation,
                location=location,
                context=context,
                correlation_id=report_id,
                version=version,
            )
            await report_public_error(message)
    except Exception:
        _LOGGER.debug("Could not build error report", exc_info=True)
    return report_id
