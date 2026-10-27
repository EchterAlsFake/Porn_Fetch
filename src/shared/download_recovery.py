"""Atomic desktop queue snapshots. Native objects, cookies and sessions are excluded."""
from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
from dataclasses import fields
from datetime import datetime
from pathlib import Path

from src.shared.media import VideoObject
from src.shared.provider_routing import ContentKind, route_url

SAVED_FIELDS = {field.name for field in fields(VideoObject)} - {"source_video", "thumbnail_data", "thumbnail_url"}


def discard_changed_hls_quality(checkpoint: Path, segments: Path, quality: str) -> bool:
    """Never label cached segments from one resolution as a different selection."""
    if not checkpoint.is_file():
        return False
    try:
        saved_quality = json.loads(checkpoint.read_text())["quality"]
    except (OSError, ValueError, KeyError, TypeError):
        return False  # The native downloader handles an unreadable checkpoint.
    if str(saved_quality) == str(quality):
        return False
    if segments.exists():
        shutil.rmtree(segments)
    checkpoint.unlink()
    return True


def queue_record(video: VideoObject, progress: int = 0) -> dict:
    record = {name: getattr(video, name) for name in SAVED_FIELDS}
    record["publish_date"] = video.publish_date.isoformat() if video.publish_date else None
    record["output_path"] = str(Path(video.output_path).resolve()) if video.output_path else None
    record["status"] = "cancelled"  # Reopening never starts a transfer automatically.
    record["progress"] = int(progress)
    return record


def read_queue(path: Path) -> list[tuple[VideoObject, int]]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema") != 1 or not isinstance(payload.get("rows"), list):
        raise ValueError("Unsupported saved download queue")
    rows, identifiers = [], set()
    for saved in payload["rows"]:
        if not isinstance(saved, dict):
            raise ValueError("Invalid saved download row")
        identifier = saved.get("identifier")
        if (not isinstance(identifier, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", identifier)
                or identifier in identifiers):
            raise ValueError("Invalid or duplicate saved download identifier")
        if route_url(saved["url"]).kind != ContentKind.VIDEO:
            raise ValueError("Saved queue contains an unsupported video URL")
        values = {name: saved[name] for name in SAVED_FIELDS if name in saved}
        values["publish_date"] = datetime.fromisoformat(saved["publish_date"]) if saved.get("publish_date") else None
        values["output_path"] = Path(saved["output_path"])
        values["thumbnail_url"] = ""
        values["source_video"] = None
        values["status"] = "cancelled"
        rows.append((VideoObject(**values), max(0, min(99, int(saved.get("progress", 0))))))
        identifiers.add(identifier)
    return rows


def write_queue(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".queue-", dir=path.parent, text=True)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump({"schema": 1, "rows": rows}, stream, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)
