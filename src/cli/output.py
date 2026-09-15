from __future__ import annotations

from pathlib import Path

from src.backend.media import VideoObject
from .settings import CliSettings


def output_path_for(media: VideoObject, settings: CliSettings) -> Path:
    rendered = settings.path_template
    for name, value in {
        "title": media.title, "author": media.author, "video_id": media.video_id,
    }.items():
        rendered = rendered.replace(f"${name}", str(value))
    rendered = rendered.strip() or media.title
    target = Path(rendered)
    if target.is_absolute() or ".." in target.parts:
        target = Path(media.title)
    if target.suffix.casefold() != ".mp4":
        target = target.with_suffix(".mp4")
    return Path(settings.output_path) / target
