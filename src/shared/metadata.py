"""Optional Qt-free MP4 metadata writer using FFmpeg."""
from __future__ import annotations

from .ffmpeg import write_metadata_tags
from .media import VideoObject


def write_tags(path: str, data: VideoObject) -> bool:
    """Write tags and thumbnail to an MP4 video file using FFmpeg."""
    return write_metadata_tags(path, data)
