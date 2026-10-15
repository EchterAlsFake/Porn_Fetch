"""Privacy-first, best-effort reporting to the public error-log relay."""
from __future__ import annotations

import json
import logging
import platform
import re
import uuid
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from curl_cffi.requests import AsyncSession

from .version import __version__

ERROR_REPORT_URL = "https://api.pornfetch.to/error_log"
MAX_MESSAGE_CHARS = 2_000
MAX_BODY_BYTES = 4_096
_LOGGER = logging.getLogger(__name__)

ERROR_REPORT_DISCLOSURE = """Optional automatic error reports are sent only after an operation fails and only if you enable them. Each report contains a random per-error correlation ID, UTC timestamp, Porn Fetch version, operating system and architecture, error class, and code function names. New reports omit video URLs, provider/context values, filenames, source lines, exception messages, browsing history and download records.

Reports are capped at 2,000 characters and the complete JSON request at 4 KiB. The HTTPS request to api.pornfetch.to/error_log contains only {\"message\": \"...\"}; it sends no application credentials, cookies or authorization header. This connection is separate from the media-provider proxy settings. The server necessarily receives connection metadata during transport and is configured not to log or store client IP addresses in diagnostic records. Delivery failures do not interrupt downloads.

Reports are stored privately in PocketBase and scheduled for deletion after 30 days (hourly cleanup). Older application versions may send URL paths and redacted tracebacks; query strings and named secrets are filtered, but redaction is not guaranteed anonymisation. You may decline without losing functionality and withdraw consent in Settings at any time. This stops future reports without changing the lawfulness of earlier processing. Privacy details: https://pornfetch.to/privacy_policy"""

ERROR_REPORT_EXAMPLE = """Porn Fetch error report
correlation_id=a1b2c3d4e5f6
timestamp=2026-10-14T12:00:00+00:00
version=3.9
platform=Linux-x86_64
error_type=RuntimeError
functions=load_fields,fetch_metadata"""

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
    """Apply the application's reference redaction policy before transmission."""
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


def build_error_report(
    error: BaseException,
    *,
    operation: str,
    location: str,
    context: Mapping[str, Any] | None = None,
    correlation_id: str | None = None,
    version: str = __version__,
) -> tuple[str, str]:
    """Use structural diagnostics only; never format exception text or user context."""
    report_id = correlation_id or uuid.uuid4().hex[:12]
    def identifier(value: str) -> str:
        return value if re.fullmatch(r"[A-Za-z0-9_.-]{1,80}", value) else "unknown"
    frames = []
    tb = error.__traceback__
    while tb is not None and len(frames) < 12:
        frames.append(identifier(tb.tb_frame.f_code.co_name))
        tb = tb.tb_next
    message = "\n".join([
        "Porn Fetch error report",
        f"correlation_id={identifier(report_id)}",
        f"timestamp={datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"version={identifier(version)}",
        f"platform={identifier(platform.system())}-{identifier(platform.machine())}",
        f"error_type={identifier(type(error).__name__)}",
        "functions=" + ",".join(frames),
    ])
    return _fit_payload(message), report_id


def _payload_bytes(message: str) -> bytes:
    return json.dumps(
        {"message": message}, ensure_ascii=False, separators=(",", ":"),
    ).encode("utf-8")


def _fit_payload(message: str) -> str:
    message = message[:MAX_MESSAGE_CHARS]
    if len(_payload_bytes(message)) <= MAX_BODY_BYTES:
        return message
    low, high = 0, len(message)
    while low < high:
        middle = (low + high + 1) // 2
        if len(_payload_bytes(message[:middle])) <= MAX_BODY_BYTES:
            low = middle
        else:
            high = middle - 1
    return message[:low]


async def report_public_error(message: str) -> bool:
    """Submit an already formatted diagnostic without propagating failures."""
    safe_message = _fit_payload(redact_log_text(message))
    if not safe_message.strip():
        return False
    try:
        session = AsyncSession(
            headers={"Content-Type": "application/json"},
            cookies={},
            discard_cookies=True,
            default_headers=False,
            trust_env=False,
        )
    except Exception:
        _LOGGER.debug("Could not create error-report session", exc_info=True)
        return False
    try:
        response = await session.post(
            ERROR_REPORT_URL,
            content=_payload_bytes(safe_message),
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
        message, report_id = build_error_report(
            error,
            operation=operation,
            location=location,
            context=context,
            correlation_id=report_id,
            version=version,
        )
        if enabled:
            await report_public_error(message)
    except Exception:
        _LOGGER.debug("Could not build error report", exc_info=True)
    return report_id
