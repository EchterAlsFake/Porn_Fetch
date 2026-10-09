"""Pure provider value normalization shared by frontend adapters."""
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from dateutil.relativedelta import relativedelta

_RELATIVE_RE = re.compile(
    r"^\s*(?P<num>\d+)\s*(?P<unit>second|minute|hour|day|week|month|year)s?\s+ago\s*$",
    re.IGNORECASE,
)
_PUBLISHED_ON_RE = re.compile(
    r"^\s*published\s+on\s+(?P<date>.+?)\s*$",
    re.IGNORECASE,
)
_NOT_AVAILABLE_RE = re.compile(r"^\s*(not\s+available|n/?a|none|null)?\s*$", re.IGNORECASE)


def parse_publish_date(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(value, timezone.utc)
        except (ValueError, OverflowError, OSError):
            return None

    s = str(value).strip()
    if _NOT_AVAILABLE_RE.match(s):
        return None

    now_utc = datetime.now(timezone.utc)
    if now_utc.tzinfo is None:
        now_utc = now_utc.replace(tzinfo=timezone.utc)
    else:
        now_utc = now_utc.astimezone(timezone.utc)

    # 1) Relative: "7 days ago", "4 months ago", etc.
    m = _RELATIVE_RE.match(s)
    if m:
        num = int(m.group("num"))
        unit = m.group("unit").lower()

        if unit in ("second", "minute", "hour", "day", "week"):
            seconds = {
                "second": 1,
                "minute": 60,
                "hour": 3600,
                "day": 86400,
                "week": 7 * 86400,
            }[unit]
            return now_utc - timedelta(seconds=num * seconds)

        # month/year need calendar arithmetic
        if relativedelta is None:
            raise ImportError(
                "Parsing 'months ago'/'years ago' requires python-dateutil. "
                "Install with: pip install python-dateutil"
            )

        if unit == "month":
            return now_utc - relativedelta(months=num)
        if unit == "year":
            return now_utc - relativedelta(years=num)

    # 2) "Published on September 17, 2024"
    m = _PUBLISHED_ON_RE.match(s)
    if m:
        s = m.group("date").strip()

    # 3) Try ISO 8601 (handles "2025-10-17T22:56:30+00:00")
    # datetime.fromisoformat also accepts "YYYY-MM-DD" and "YYYY-MM-DD HH:MM:SS" in many cases.
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            # Assume naive timestamps are UTC. Change this if you prefer local time.
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        pass

    # 4) Try common long-form date (after stripping "Published on")
    # Example: "September 17, 2024"
    for fmt in ("%B %d, %Y", "%b %d, %Y", "%a, %d %b %Y %H:%M:%S %z"):
        try:
            dt = datetime.strptime(s, fmt)
            return dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue

    return None


def parse_length(
    length: str | int | float | None,
    video_source: str | None = None,
) -> int | None:
    """
    Parse a video duration and return its length in rounded minutes.

    Supported examples:
        16:19
        123
        12.5
        9 Min
        247min 02sec
        59m 40s
        1h 2m 3s
        24 seconds
        PT00H11M42S
        PT11M42S
        PT2H
        PT42S

    Digits-only strings depend on `video_source`:
        - PornHub, Eporner, xHamster, SpankBang, Beeg, Redtube,
          Tube8, Thumbzilla, and XFreeHD values are interpreted as seconds.
        - Other provider values are interpreted as minutes.

    Returns:
        int:
            Rounded duration in minutes.
            Positive durations below 0.5 minutes are returned as 1.

        None:
            If no duration was provided or the format could not be parsed.
    """

    def rounded_minutes(minutes: float) -> int:
        """Round minutes, but keep any positive duration at at least 1 minute."""
        result = round(minutes)
        return max(1, result) if minutes > 0 else 0

    if length is None or length == "" or str(length).casefold() == "not available":
        return None

    seconds_sources = {
        "pornhub", "phub", "eporner", "xhamster", "spankbang", "beeg",
        "redtube", "tube8", "thumbzilla", "xfreehd",
    }
    source = (video_source or "").casefold()

    # Numeric values from several providers are documented as seconds.
    if isinstance(length, (int, float)):
        value = float(length)
        return rounded_minutes(value / 60 if source in seconds_sources else value)

    s = str(length).strip()
    s_lower = s.lower()

    if not s:
        return None

    # ---------------------------------------------------------
    # ISO 8601 duration:
    # PT00H11M42S
    # PT11M42S
    # PT2H
    # PT42S
    # PT1H2.5M
    iso_match = re.fullmatch(
        r"PT"
        r"(?:(?P<hours>\d+(?:\.\d+)?)H)?"
        r"(?:(?P<minutes>\d+(?:\.\d+)?)M)?"
        r"(?:(?P<seconds>\d+(?:\.\d+)?)S)?",
        s,
        flags=re.IGNORECASE,
    )

    if iso_match and any(iso_match.groupdict().values()):
        hours = float(iso_match.group("hours") or 0)
        minutes = float(iso_match.group("minutes") or 0)
        seconds = float(iso_match.group("seconds") or 0)

        total_minutes = (
            hours * 60
            + minutes
            + seconds / 60
        )

        return rounded_minutes(total_minutes)

    # ---------------------------------------------------------
    # Colon format:
    # 16:19 -> 16 minutes, 19 seconds
    #
    # Also handles:
    # 1:02:03 -> 1 hour, 2 minutes, 3 seconds
    parts = s.split(":")

    if len(parts) in (2, 3) and all(part.isdigit() for part in parts):
        if len(parts) == 2:
            minutes, seconds = map(int, parts)
            total_minutes = minutes + seconds / 60

        else:
            hours, minutes, seconds = map(int, parts)
            total_minutes = hours * 60 + minutes + seconds / 60

        return rounded_minutes(total_minutes)

    # ---------------------------------------------------------
    # Digits only.
    if s.isdigit():
        value = int(s)
        if source in seconds_sources:
            return rounded_minutes(value / 60)

        # xnxx and unknown sources are interpreted as minutes.
        return value

    # ---------------------------------------------------------
    # Plain decimal -> assume minutes.
    #
    # Examples:
    # 12.5
    # 0.25
    if re.fullmatch(r"\d+(?:\.\d+)?", s):
        return rounded_minutes(float(s))

    # ---------------------------------------------------------
    # Human-readable units.
    #
    # Examples:
    # 59m 40s
    # 1h 2m 3s
    # 247min 02sec
    # 24 seconds
    # 17 min
    # 1 hour 24 minutes
    unit_multipliers = {
        # Hours
        "h": 60,
        "hr": 60,
        "hrs": 60,
        "hour": 60,
        "hours": 60,

        # Minutes
        "m": 1,
        "min": 1,
        "mins": 1,
        "minute": 1,
        "minutes": 1,

        # Seconds
        "s": 1 / 60,
        "sec": 1 / 60,
        "secs": 1 / 60,
        "second": 1 / 60,
        "seconds": 1 / 60,
    }

    matches = re.findall(
        r"(\d+(?:\.\d+)?)\s*"
        r"(hours?|hrs?|h|minutes?|mins?|m|seconds?|secs?|s)\b",
        s_lower,
    )

    if matches:
        total_minutes = sum(
            float(value) * unit_multipliers[unit]
            for value, unit in matches
        )

        return rounded_minutes(total_minutes)

    return None
