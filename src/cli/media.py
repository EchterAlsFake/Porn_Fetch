"""Provider-neutral media preparation for terminal and batch consumers."""
from __future__ import annotations

from datetime import datetime, timezone
import inspect
import re
from typing import Any

from src.backend.media import VideoObject


async def prepare_video(video: Any, provider: str) -> VideoObject:
    loaders = getattr(video, "loader_methods", {}) or {}
    source = "api" if provider == "beeg" and "api" in loaders else "html"
    if source in loaders:
        await video.load_sources(source)

    title = _value(video, "title") or _value(video, "video_id") or "Untitled"
    author = await _author(video, provider)
    qualities = await available_qualities(video)
    tags = _value(video, "tags") or _value(video, "categories") or []
    if isinstance(tags, str):
        tags = [item.strip() for item in tags.split(",") if item.strip()]
    elif isinstance(tags, dict):
        tags = list(tags)
    else:
        tags = [str(item) for item in (tags or [])]

    length = _value(video, "duration") or _value(video, "length") or _value(video, "length_seconds")
    return VideoObject(
        url=str(_value(video, "url") or ""),
        title=_safe_title(str(title)),
        author=str(author or "N/A"),
        length=_minutes(length),
        tags=tags,
        thumbnail_url=str(
            _value(video, "thumbnail_url") or _value(video, "thumbnail") or ""
        ),
        video_id=str(_value(video, "video_id") or title),
        publish_date=_date(_value(video, "publish_date") or _value(video, "created_at")),
        qualities=qualities,
        status="pending",
        source_video=video,
    )


async def available_qualities(video: Any) -> list[int]:
    hls = _value(video, "m3u8_base_url")
    if hls:
        core = _value(video, "core") or _value(_value(video, "client"), "core")
        return sorted({int(item) for item in await core.list_available_qualities(hls)})

    method = getattr(video, "video_qualities", None)
    if method:
        values = method() if callable(method) else method
        if hasattr(values, "__await__"):
            values = await values
    else:
        values = _value(video, "available_qualities") or []
    result: set[int] = set()
    for item in values or []:
        match = re.search(r"\d+", str(item))
        if match:
            result.add(int(match.group()))
    return sorted(result)


async def _author(video: Any, provider: str) -> str:
    # 1. Author information dictionary (e.g. PornHub)
    info = _value(video, "author_information")
    if isinstance(info, dict) and info.get("name"):
        return str(info["name"])

    # 2. Direct string fields
    for field in ("author_name", "uploader", "uploader_name"):
        val = _value(video, field)
        if isinstance(val, str) and val.strip():
            return val.strip()

    # 3. Pornstars list (e.g. XHamster)
    pornstars = _value(video, "pornstars")
    if pornstars:
        if isinstance(pornstars, (list, tuple, set)):
            names = [str(p) for p in pornstars if p]
            if names:
                return ", ".join(names)
        elif isinstance(pornstars, str) and pornstars.strip():
            return pornstars.strip()

    # 4. Check video.author (could be str, coroutine, property, or method)
    author_attr = getattr(video, "author", None)
    if author_attr is not None:
        try:
            val = author_attr() if callable(author_attr) else author_attr
            if inspect.isawaitable(val):
                val = await val
            if isinstance(val, str) and val.strip():
                return val.strip()
            name = getattr(val, "name", None)
            if name and isinstance(name, str) and name.strip():
                return name.strip()
        except Exception:
            pass

    # 5. Check video.get_author (e.g. XVideos)
    getter = getattr(video, "get_author", None)
    if getter is not None:
        try:
            val = getter() if callable(getter) else getter
            if inspect.isawaitable(val):
                val = await val
            if isinstance(val, str) and val.strip():
                return val.strip()
            name = getattr(val, "name", None)
            if name and isinstance(name, str) and name.strip():
                return name.strip()
        except Exception:
            pass

    return "N/A"


def _value(value: Any, name: str) -> Any:
    try:
        return getattr(value, name, None)
    except Exception:
        return None


def _safe_title(value: str) -> str:
    return re.sub(r"[\\/:*?\"<>|\x00-\x1f]", "_", value).strip(" .") or "Untitled"


def _minutes(value: Any) -> int | None:
    if value is None:
        return None
    try:
        if isinstance(value, (int, float)):
            return max(0, round(float(value) / 60))
        parts = [int(part) for part in str(value).split(":")]
        if len(parts) == 3:
            return round((parts[0] * 3600 + parts[1] * 60 + parts[2]) / 60)
        if len(parts) == 2:
            return round((parts[0] * 60 + parts[1]) / 60)
        return round(float(value) / 60)
    except (TypeError, ValueError):
        return None


def _date(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if not value:
        return None
    try:
        result = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return result if result.tzinfo else result.replace(tzinfo=timezone.utc)
    except ValueError:
        return None
