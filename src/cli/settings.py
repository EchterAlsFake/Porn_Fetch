"""Validated, atomic CLI settings and one-time legacy INI migration."""
from __future__ import annotations

import configparser
from dataclasses import asdict, dataclass, fields, replace
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any

from .paths import config_dir


SETTINGS_VERSION = 2


@dataclass(slots=True)
class CliSettings:
    # Video
    quality: str = "best"
    profile_video_mode: str = "videos"
    locale: str = "en-US"
    strict_language: bool = False
    result_limit: int = 50
    output_path: str = "."
    path_template: str = "$title"
    write_metadata: bool = True
    skip_existing: bool = True
    # Performance
    parallel_downloads: int = 2
    processing_delay: float = 0.0
    request_delay: int = 0
    timeout: int = 20
    request_attempts: int = 4
    retry_initial_delay: float = 0.5
    retry_max_delay: float = 30.0
    retry_multiplier: float = 2.0
    retry_jitter: float = 0.5
    bandwidth_limit_mb: float = 0.0
    download_workers: int = 20
    pages_concurrency: int = 2
    videos_concurrency: int = 5
    response_cache_mb: int = 32
    response_cache_ttl: float = 300.0
    segment_cache_mb: int = 8
    segment_cache_ttl: float = 300.0
    # Network / privacy
    proxy: str = ""
    proxy_auth: str = ""
    interface: str = ""
    http_version: str = "v2"
    ip_preference: str = "auto"
    dns_over_https: bool = False
    doh_endpoint: str = "https://cloudflare-dns.com/dns-query"
    impersonation: str = "chrome"
    custom_ja3: str = ""
    verify_ssl: bool = True
    trust_environment: bool = False
    encrypted_client_hello: bool = False
    # Logging / appearance
    log_level: str = "INFO"
    debug: bool = False
    error_reporting: bool = False
    error_reporting_decided: bool = False
    theme: str = "textual-dark"

    def validate(self) -> None:
        positive = (
            "result_limit", "parallel_downloads", "timeout", "request_attempts",
            "download_workers", "pages_concurrency", "videos_concurrency",
        )
        for name in positive:
            if int(getattr(self, name)) < 1:
                raise ValueError(f"{name.replace('_', ' ')} must be at least 1")
        nonnegative = (
            "processing_delay", "request_delay", "retry_initial_delay",
            "retry_max_delay", "retry_jitter", "bandwidth_limit_mb",
            "response_cache_mb", "response_cache_ttl", "segment_cache_mb",
            "segment_cache_ttl",
        )
        for name in nonnegative:
            if float(getattr(self, name)) < 0:
                raise ValueError(f"{name.replace('_', ' ')} cannot be negative")
        if self.retry_multiplier < 1:
            raise ValueError("retry multiplier must be at least 1")
        if self.http_version not in {"v1", "v2", "v3"}:
            raise ValueError("http version must be v1, v2 or v3")
        if self.ip_preference not in {"auto", "ipv4", "ipv6"}:
            raise ValueError("IP preference must be auto, ipv4 or ipv6")
        if self.profile_video_mode not in {"videos", "uploads", "both"}:
            raise ValueError("profile video mode must be videos, uploads or both")
        if self.log_level.upper() not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError("log level must be DEBUG, INFO, WARNING, ERROR or CRITICAL")
        if not self.output_path.strip():
            raise ValueError("output path cannot be blank")

    def overridden(self, **values: Any) -> "CliSettings":
        valid = {key: value for key, value in values.items() if value is not None}
        result = replace(self, **valid)
        result.validate()
        return result

    def to_runtime_config(self):
        """Return a dedicated BaseCore RuntimeConfig; never mutate its singleton."""
        from base_api.modules.config import RuntimeConfig

        self.validate()
        runtime = RuntimeConfig()
        runtime.response_cache_size_bytes = self.response_cache_mb * 1024 * 1024
        runtime.response_cache_ttl = self.response_cache_ttl
        runtime.segment_cache_size_bytes = self.segment_cache_mb * 1024 * 1024
        runtime.segment_cache_ttl = self.segment_cache_ttl
        runtime.request_attempts = self.request_attempts
        runtime.request_retry_initial_delay = self.retry_initial_delay
        runtime.request_retry_max_delay = self.retry_max_delay
        runtime.request_multiplier = self.retry_multiplier
        runtime.request_retry_jitter = self.retry_jitter
        runtime.request_delay = self.request_delay
        runtime.timeout = self.timeout
        runtime.max_bandwidth_mb = self.bandwidth_limit_mb or None
        runtime.proxy = self.proxy.strip() or None
        runtime.proxy_auth = self.proxy_auth.strip() or None
        runtime.interface = self.interface.strip() or None
        runtime.http_version = self.http_version
        runtime.ip_resolve = {"auto": None, "ipv4": 1, "ipv6": 2}[self.ip_preference]
        runtime.dns_over_https = self.doh_endpoint.strip() if self.dns_over_https else None
        runtime.impersonation = self.impersonation.strip() or "chrome"
        runtime.custom_ja3 = self.custom_ja3.strip() or None
        runtime.verify_ssl = self.verify_ssl
        runtime.trust_env = self.trust_environment
        runtime.max_workers_download = self.download_workers
        runtime.pages_concurrency = self.pages_concurrency
        runtime.videos_concurrency = self.videos_concurrency
        headers, cookies = locale_headers_and_cookies(self.locale)
        runtime.locale = headers["Accept-Language"]
        runtime.cookies = cookies
        # BaseCore versions that support ECH consume this optional setting.
        runtime.encrypted_client_hello = self.encrypted_client_hello
        runtime.strict_language = self.strict_language
        runtime.profile_video_mode = self.profile_video_mode
        return runtime


def locale_headers_and_cookies(locale: str) -> tuple[dict[str, str], dict[str, str]]:
    normalized = (locale or "en-US").strip().replace("_", "-")
    parts = normalized.split("-", 1)
    language = parts[0].casefold() if parts[0] else "en"
    canonical = language if len(parts) == 1 else f"{language}-{parts[1].upper()}"
    accept = f"{canonical},{language};q=0.9,en-US;q=0.8,en;q=0.7"
    if language == "en":
        accept = f"{canonical},en;q=0.9"
    return {"Accept-Language": accept}, {
        "lang": language, "language": language, "locale": canonical,
    }


def default_settings_path() -> Path:
    return config_dir() / "settings.json"


class SettingsStore:
    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path) if path else default_settings_path()

    def load(self, legacy_paths: list[Path] | None = None) -> CliSettings:
        if self.path.exists():
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            values = raw.get("settings", raw)
            known = {field.name for field in fields(CliSettings)}
            settings = CliSettings(**{k: v for k, v in values.items() if k in known})
            if not settings.error_reporting_decided:
                settings = replace(settings, error_reporting=False)
            settings.validate()
            return settings

        settings = CliSettings()
        candidates = legacy_paths if legacy_paths is not None else _legacy_candidates()
        legacy = next((path for path in candidates if path.is_file()), None)
        if legacy:
            settings = _migrate_ini(legacy, settings)
        self.save(settings)
        return settings

    def save(self, settings: CliSettings) -> None:
        settings.validate()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(
            {"version": SETTINGS_VERSION, "settings": asdict(settings)},
            indent=2, ensure_ascii=False,
        ) + "\n"
        descriptor, temporary = tempfile.mkstemp(
            prefix=f".{self.path.name}.", dir=self.path.parent, text=True,
        )
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, self.path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)


async def prompt_error_reporting_consent(
    settings: CliSettings,
    store: SettingsStore,
    *,
    console: Any | None = None,
) -> CliSettings:
    """Show the one-time CLI disclosure and persist only an explicit choice."""
    if settings.error_reporting_decided:
        return settings

    import questionary
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text

    from src.backend.error_reporting import ERROR_REPORT_DISCLOSURE, ERROR_REPORT_EXAMPLE

    output = console or Console()
    output.print(Panel(
        Text(ERROR_REPORT_DISCLOSURE),
        title="[bold cyan]Optional automatic error reports[/]",
        border_style="cyan",
        padding=(1, 2),
    ))
    output.print(Panel(
        Text(ERROR_REPORT_EXAMPLE, style="dim"),
        title="Synthetic example of a stored report",
        border_style="bright_black",
        padding=(1, 2),
    ))
    choice = await questionary.select(
        "Enable automatic redacted error reports?",
        choices=[
            questionary.Choice("No, keep error reporting disabled", value=False),
            questionary.Choice("Yes, enable automatic error reports", value=True),
        ],
    ).ask_async()
    if choice is None:
        output.print("[yellow]No choice was saved; error reporting remains disabled.[/]")
        return settings

    updated = replace(
        settings,
        error_reporting=bool(choice),
        error_reporting_decided=True,
    )
    updated.validate()
    store.save(updated)
    output.print(
        "[green]Error reporting enabled.[/]" if choice
        else "[dim]Error reporting remains disabled.[/]"
    )
    return updated


def _legacy_candidates() -> list[Path]:
    executable = Path(sys.executable).resolve().parent / "config.ini"
    current = Path.cwd() / "config.ini"
    return list(dict.fromkeys((executable, current)))


def _migrate_ini(path: Path, defaults: CliSettings) -> CliSettings:
    parser = configparser.ConfigParser()
    parser.read(path, encoding="utf-8")
    values: dict[str, Any] = {}
    mappings = {
        ("Video", "output_path"): ("output_path", str),
        ("Video", "result_limit"): ("result_limit", int),
        ("Video", "write_metadata"): ("write_metadata", parser.getboolean),
        ("Video", "skip_existing_files"): ("skip_existing", parser.getboolean),
        ("Performance", "network_delay"): ("request_delay", int),
        ("Performance", "download_workers"): ("download_workers", int),
        ("Performance", "timeout"): ("timeout", int),
        ("Performance", "retries"): ("request_attempts", int),
        ("Performance", "pages_concurrency"): ("pages_concurrency", int),
        ("Performance", "videos_concurrency"): ("videos_concurrency", int),
        ("Performance", "speed_limit"): ("bandwidth_limit_mb", float),
    }
    qualities = {
        "0": "best", "1": "half", "2": "worst", "3": "2160", "4": "1440",
        "5": "1080", "6": "720", "7": "540", "8": "480", "9": "360",
        "10": "240", "11": "144",
    }
    if parser.has_option("Video", "quality"):
        raw = parser.get("Video", "quality")
        values["quality"] = qualities.get(raw, raw)
    for (section, option), (target, converter) in mappings.items():
        if not parser.has_option(section, option):
            continue
        try:
            if getattr(converter, "__self__", None) is parser:
                values[target] = converter(section, option)
            else:
                values[target] = converter(parser.get(section, option))
        except (TypeError, ValueError):
            continue
    migrated = replace(defaults, **values)
    migrated.validate()
    return migrated
