"""FFmpeg binary discovery and media processing, delegating to eaf_base_api."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from base_api.modules.errors import MetadataWriteError as _BaseMetadataWriteError
from base_api.modules.ffmpeg import (
    _find_original_executable,
)
from base_api.modules.ffmpeg import (
    find_ffmpeg as _base_find_ffmpeg,
)
from base_api.modules.ffmpeg import (
    remux_ts_to_mp4 as _base_remux_ts_to_mp4,
)
from base_api.modules.ffmpeg import (
    write_metadata_tags as _base_write_metadata_tags,
)

from .errors import MetadataWriteError

_PROJECT_ROOT = Path(__file__).resolve().parents[2]


def find_ffmpeg(ffmpeg_bin: Path | str | None = None) -> Path | None:
    """Discover the bundled or system FFmpeg executable."""
    return _base_find_ffmpeg(
        ffmpeg_bin,
        original_executable=_find_original_executable(),
        extra_roots=(_PROJECT_ROOT,),
    )


def has_ffmpeg() -> bool:
    """Return True if FFmpeg binary is available on the system or bundled."""
    return find_ffmpeg() is not None


def remux_ts_to_mp4(
    input_path: Path | str,
    output_path: Path | str,
    ffmpeg_bin: Path | str | None = None,
    *,
    metadata: Any = None,
    thumbnail: bytes | Path | str | None = None,
) -> bool:
    """Remux an MPEG-TS container into a faststart MP4 container (optionally with metadata in one pass)."""
    resolved_bin = Path(ffmpeg_bin) if ffmpeg_bin else find_ffmpeg()
    return _base_remux_ts_to_mp4(
        input_path,
        output_path,
        ffmpeg_bin=resolved_bin,
        metadata=metadata,
        thumbnail=thumbnail,
        extra_roots=(_PROJECT_ROOT,),
    )


def write_metadata_tags(
    path: str | Path,
    data: Any,
    ffmpeg_bin: Path | str | None = None,
    *,
    thumbnail: bytes | Path | str | None = None,
) -> bool:
    """Write tags and optional cover thumbnail into an MP4 file using FFmpeg."""
    resolved_bin = Path(ffmpeg_bin) if ffmpeg_bin else find_ffmpeg()
    try:
        return _base_write_metadata_tags(
            path,
            data,
            ffmpeg_bin=resolved_bin,
            thumbnail=thumbnail,
            extra_roots=(_PROJECT_ROOT,),
        )
    except _BaseMetadataWriteError as error:
        if isinstance(error, MetadataWriteError):
            raise
        raise MetadataWriteError(str(error)) from error
