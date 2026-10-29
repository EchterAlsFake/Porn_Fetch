"""Read-only helpers for importing the former SQLite database."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any


def _format_date(value: Any) -> str:
    if not value:
        return ""
    if isinstance(value, datetime):
        if value.tzinfo:
            return value.astimezone().isoformat(timespec="milliseconds")
        return value.isoformat(timespec="milliseconds")
    return str(value)


def _load_json(value: Any) -> Any:
    if value in (None, ""):
        return []
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return []
    return value


def _read_legacy_sqlite(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Read the previous Peewee database without retaining Peewee as a dependency."""
    with sqlite3.connect(f"file:{path}?mode=ro", uri=True) as connection:
        connection.row_factory = sqlite3.Row
        tables = {
            row[0] for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        if not {"originiterator", "videorecord"}.issubset(tables):
            return [], []
        origins = [dict(row) for row in connection.execute("SELECT url, name FROM originiterator")]
        raw_videos = [dict(row) for row in connection.execute("SELECT * FROM videorecord")]
    videos = []
    for record in raw_videos:
        videos.append({
            "url": record.get("url") or "",
            "title": record.get("title") or "",
            "video_id": record.get("video_id") or "",
            "author": record.get("author") or "",
            "length": record.get("length") or "",
            "thumbnail_url": record.get("thumbnail_url") or "",
            "publish_date": record.get("publish_date") or "",
            "status": record.get("status") or "",
            "tags": _load_json(record.get("tags_json")),
            "qualities": _load_json(record.get("qualities_json")),
            "identifier": record.get("identifier") or "",
            "output_path": record.get("output_path") or "",
            "selected_quality": record.get("selected_quality") or "",
            "file_size_mb": float(record.get("file_size_mb") or 0),
            "downloaded_at": record.get("downloaded_at") or "",
            "is_hls": bool(record.get("is_hls")),
            "missing_segments": _load_json(record.get("missing_segments")),
            "is_from_account": bool(record.get("is_from_account")),
            "origin_iterator_url": record.get("origin_iterator_url") or "",
        })
    return origins, videos
