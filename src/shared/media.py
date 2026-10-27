"""Qt-free media models shared by the graphical and terminal frontends."""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

try:
    from base_api.modules.static_functions import normalize_quality
except ImportError:  # Keep configuration/self-test imports dependency-light.
    def normalize_quality(value: str | int) -> int:
        text = str(value).strip().casefold().removesuffix("p")
        return int(text)


FREE_MAXIMUM_QUALITY = 720
PREMIUM_QUALITY_NAMES = {
    "best", "half", "4k", "uhd", "2k", "qhd", "fullhd", "fhd",
}


def xfreehd_quality(quality: str | int) -> str:
    """Translate UI resolutions to the provider's documented SD/HD names."""
    text = str(quality).strip().casefold()
    if text in {"sd", "worst"}:
        return "sd"
    if text in {"hd", "best", "half"}:
        return "hd"
    return "hd" if normalize_quality(quality) >= 720 else "sd"


def quality_requires_premium(quality: str | int) -> bool:
    """Return whether *quality* is restricted to licensed installations."""
    if str(quality).strip().casefold() in PREMIUM_QUALITY_NAMES:
        return True
    try:
        return int(normalize_quality(quality)) > FREE_MAXIMUM_QUALITY
    except (TypeError, ValueError):
        return False


def select_allowed_quality(
    preferred_quality: str | int,
    available_qualities: list[str | int],
    has_premium: bool,
) -> str:
    """Select the requested quality or the highest permitted concrete stream."""
    available = [str(quality) for quality in available_qualities]
    preferred = str(preferred_quality or "")
    if preferred in available and (
        has_premium or not quality_requires_premium(preferred)
    ):
        return preferred

    allowed = available if has_premium else [
        quality for quality in available if not quality_requires_premium(quality)
    ]
    if not allowed:
        return ""

    def rank(quality: str) -> tuple[int, int]:
        try:
            return 1, int(normalize_quality(quality))
        except (TypeError, ValueError):
            return 0, 0

    return max(allowed, key=rank)


@dataclass(slots=True)
class VideoFilters:
    duration_minimum: int | None = None
    duration_maximum: int | None = None
    author_regex: str | None = None
    tags_regex: str | None = None
    title_regex: str | None = None
    quality_minimum: str | None = None
    quality_maximum: str | None = None
    published_before: str | None = None
    published_after: str | None = None
    start_index: int = 0
    end_index: int = 0

    @staticmethod
    def quality_value(value: str | int) -> int:
        return 2160 if str(value).strip().casefold() == "4k" else normalize_quality(value)

    def validate(self) -> None:
        for label, pattern in (("Title", self.title_regex), ("Author", self.author_regex), ("Tags", self.tags_regex)):
            if pattern:
                try:
                    re.compile(pattern, re.IGNORECASE)
                except re.error as error:
                    raise ValueError(f"{label} regex is invalid: {error.msg}") from error
        for label, minimum, maximum in (
            ("Duration", self.duration_minimum, self.duration_maximum),
            ("Quality", self.quality_value(self.quality_minimum) if self.quality_minimum else None,
             self.quality_value(self.quality_maximum) if self.quality_maximum else None),
        ):
            if (minimum is not None and minimum < 0) or (maximum is not None and maximum < 0):
                raise ValueError(f"{label} limits must not be negative.")
            if minimum is not None and maximum is not None and minimum > maximum:
                raise ValueError(f"{label} minimum must not exceed maximum.")
        after = datetime.fromisoformat(self.published_after).date() if self.published_after else None
        before = datetime.fromisoformat(self.published_before).date() if self.published_before else None
        if after is not None and before is not None and after > before:
            raise ValueError("The publication date 'after' must not exceed 'before'.")
        if self.start_index < 0 or self.end_index < 0:
            raise ValueError("Start and End must not be negative.")
        if self.end_index and max(1, self.start_index) > self.end_index:
            raise ValueError("Start must not exceed End. Use 0 for no End limit.")


@dataclass(slots=True)
class VideoObject:
    url: str
    title: str
    author: str
    length: int | None  # Rounded minutes, as returned by parse_length().
    tags: list[str] | None
    thumbnail_url: str
    video_id: str
    publish_date: datetime | None
    qualities: list[int]
    status: str
    identifier: str | None = None
    output_path: Path | None = None
    index: int | None = None
    selected_quality: str | None = None
    source_video: object | None = None
    origin_iterator_url: str | None = None
    origin_iterator_name: str | None = None
    is_hls: bool | None = None
    missing_segments: list[int] | None = None
    is_from_account: bool = False
    thumbnail_data: bytes | None = None


