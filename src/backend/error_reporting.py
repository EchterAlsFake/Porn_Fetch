"""Privacy-first, best-effort reporting to the public error-log relay."""
from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
import json
import logging
import platform
import re
import traceback
from typing import Any
from urllib.parse import urlsplit, urlunsplit
import uuid

from curl_cffi.requests import AsyncSession


ERROR_REPORT_URL = "https://api.echteralsfake.me/error_log"
MAX_MESSAGE_CHARS = 2_000
MAX_BODY_BYTES = 4_096
_LOGGER = logging.getLogger(__name__)

ERROR_REPORT_DISCLOSURE = """Automatic error reports are sent only after an operation fails. Each report contains a random per-error correlation ID, UTC timestamp, Porn Fetch version, operating system and architecture, operation and class/function location, error type, relevant provider/quality/index context, the failed URL's scheme/host/path, and the exception traceback.

Before transmission, Porn Fetch removes URL credentials, query strings and fragments, authorization values, cookies, named passwords/tokens/keys/secrets, email addresses, IP addresses, control characters, and user-home names. Reports are capped at 2,000 characters and the complete JSON request at 4 KiB. The HTTPS request contains only {\"message\": \"...\"}; it sends no application credentials, cookies, authorization header, Origin, or Referer. Delivery failures are ignored and never break downloads.

The relay is configured not to log or store client IP addresses. PocketBase stores only the redacted message, and its public collection API is disabled. Redaction is a safety net and cannot guarantee removal of every possible personal or secret value. Reporting can be changed later in Settings."""

ERROR_REPORT_EXAMPLE = """Porn Fetch error report
correlation_id=a1b2c3d4e5f6
timestamp=2026-01-15T12:34:56+00:00
version=3.9
platform=Linux-x86_64
operation=scrape video metadata
location=PornHubVideo.load_fields
error_type=RuntimeError
video_url=https://example.com/watch/example-video
provider=pornhub
video_index=4
traceback:
Traceback (most recent call last):
  File \"[USER HOME]/Porn_Fetch/provider.py\", line 42, in load_fields
    raise RuntimeError(\"selector did not match\")
RuntimeError: selector did not match"""

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
    """Keep a reproducible URL location without credentials, query, or fragment."""
    try:
        parsed = urlsplit(value.strip())
    except ValueError:
        return "[invalid URL]"
    if parsed.scheme.casefold() not in {"http", "https"} or not parsed.hostname:
        return "[invalid URL]"
    host = parsed.hostname
    if _IPV4_RE.fullmatch(host) or ":" in host:
        host = "[IP redacted]"
    elif ":" in host:
        host = f"[{host}]"
    try:
        port = f":{parsed.port}" if parsed.port is not None else ""
    except ValueError:
        port = ""
    return urlunsplit((parsed.scheme.casefold(), f"{host}{port}", parsed.path or "/", "", ""))


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


def _format_traceback(error: BaseException) -> str:
    rendered = traceback.TracebackException.from_exception(
        error, capture_locals=False,
    ).format(chain=True)
    return "".join(rendered).rstrip()


def _clean_context(context: Mapping[str, Any] | None) -> list[str]:
    lines: list[str] = []
    remaining = 600
    for key, value in (context or {}).items():
        if remaining <= 0 or value is None or value == "":
            continue
        safe_key = re.sub(r"[^a-zA-Z0-9_.-]", "_", str(key))[:50]
        if "url" in safe_key.casefold():
            safe_value = safe_url(str(value))
        else:
            safe_value = redact_log_text(value).replace("\n", " ")
        line = f"{safe_key}={safe_value[:240]}"[:remaining]
        lines.append(line)
        remaining -= len(line) + 1
    return lines


def build_error_report(
    error: BaseException,
    *,
    operation: str,
    location: str,
    context: Mapping[str, Any] | None = None,
    correlation_id: str | None = None,
    version: str = "3.9",
) -> tuple[str, str]:
    """Build one relay-safe report and return it with its correlation ID."""
    report_id = correlation_id or uuid.uuid4().hex[:12]
    header = [
        "Porn Fetch error report",
        f"correlation_id={report_id}",
        f"timestamp={datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"version={redact_log_text(version)}",
        f"platform={platform.system()}-{platform.machine()}",
        f"operation={redact_log_text(operation)}",
        f"location={redact_log_text(location)}",
        f"error_type={type(error).__name__}",
        *_clean_context(context),
        "traceback:",
    ]
    prefix = redact_log_text("\n".join(header)) + "\n"
    trace = redact_log_text(_format_traceback(error))
    available = MAX_MESSAGE_CHARS - len(prefix)
    if available <= 0:
        message = prefix[:MAX_MESSAGE_CHARS]
    elif len(trace) <= available:
        message = prefix + trace
    else:
        marker = "[traceback truncated to relay limit]\n"
        message = prefix + marker + trace[-max(0, available - len(marker)):]
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
    session: AsyncSession | None = None
    try:
        session = AsyncSession(
            headers={"Content-Type": "application/json"},
            cookies={},
            discard_cookies=True,
            default_headers=False,
            trust_env=False,
        )
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
        if session is not None:
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
    version: str = "3.9",
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
