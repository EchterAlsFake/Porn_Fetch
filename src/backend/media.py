"""Qt-free media models shared by the graphical and terminal frontends."""
from __future__ import annotations

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


@dataclass(slots=True)
class VideoObject:
    url: str
    title: str
    author: str
    length: int | None
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

