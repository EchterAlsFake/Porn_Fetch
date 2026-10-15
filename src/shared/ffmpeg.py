"""FFmpeg binary discovery and media processing (remuxing and metadata writing)."""
from __future__ import annotations

import logging
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from .errors import MetadataWriteError

logger = logging.getLogger("FFmpeg")


def _find_original_executable() -> Path | None:
    """Returns the true executable path, ignoring onefile or temp extractions."""
    try:
        import __compiled__
        orig = getattr(__compiled__, "original_argv0", None)
        if orig and Path(orig).exists():
            return Path(orig).resolve()
    except (ImportError, OSError, TypeError):
        pass

    if appimage := os.environ.get("APPIMAGE"):
        if Path(appimage).exists():
            return Path(appimage).resolve()

    if sys.argv and Path(sys.argv[0]).exists():
        return Path(sys.argv[0]).resolve()

    return None


def find_ffmpeg() -> Path | None:
    """Discover the bundled or system FFmpeg executable."""
    binary_name = "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"

    # 1. Environment variable override
    if configured := os.environ.get("PORN_FETCH_FFMPEG_BINARY"):
        candidate = Path(configured).expanduser()
        if candidate.is_file() and (sys.platform == "win32" or os.access(candidate, os.X_OK)):
            return candidate.resolve()

    candidates: list[Path] = []

    # 2. Paths relative to current running executable
    orig = _find_original_executable()
    if orig is not None:
        exec_dir = orig.parent
        candidates.append(exec_dir / "third_party" / binary_name)
        candidates.append(exec_dir / binary_name)
        # macOS App bundle: Contents/MacOS/
        candidates.append(exec_dir / "Contents" / "MacOS" / "third_party" / binary_name)
        candidates.append(exec_dir / "Contents" / "MacOS" / binary_name)
        if exec_dir.name == "MacOS" and exec_dir.parent.name == "Contents":
            candidates.append(exec_dir.parent.parent.parent / "third_party" / binary_name)

    # 3. Project root (development tree)
    project_root = Path(__file__).resolve().parents[2]
    candidates.append(project_root / "third_party" / binary_name)
    candidates.append(project_root / binary_name)

    for cand in candidates:
        if cand.is_file() and (sys.platform == "win32" or os.access(cand, os.X_OK)):
            return cand.resolve()

    # 4. System PATH fallback
    if in_path := shutil.which(binary_name) or shutil.which("ffmpeg"):
        p = Path(in_path)
        if p.is_file():
            return p.resolve()

    return None


def has_ffmpeg() -> bool:
    """Return True if FFmpeg binary is available on the system or bundled."""
    return find_ffmpeg() is not None


def remux_ts_to_mp4(
    input_path: Path | str,
    output_path: Path | str,
    ffmpeg_bin: Path | str | None = None,
) -> bool:
    """Remux an MPEG-TS container into a faststart MP4 container."""
    ffmpeg = Path(ffmpeg_bin) if ffmpeg_bin else find_ffmpeg()
    if not ffmpeg:
        raise FileNotFoundError("FFmpeg executable not found. Install FFmpeg or bundle it in third_party/.")

    in_p = Path(input_path).resolve()
    out_p = Path(output_path).resolve()

    # The bundled FFmpeg only copies streams; it has no encoders.
    cmd_copy = [
        str(ffmpeg),
        "-y",
        "-v", "error",
        "-i", str(in_p),
        "-c", "copy",
        "-movflags", "+faststart",
        str(out_p),
    ]
    proc = subprocess.run(cmd_copy, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg stream-copy remux failed: {proc.stderr.strip()}")

    return True


def write_metadata_tags(path: str | Path, data: Any) -> bool:
    """Write tags and optional cover thumbnail into an MP4 file using FFmpeg."""
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        logger.warning("FFmpeg not found; skipping MP4 metadata tagging.")
        return False

    target_path = Path(path).resolve()
    if not target_path.is_file():
        return False

    directory = target_path.parent
    temporary_output = directory / f".tmp_meta_{target_path.name}"
    temporary_thumb: Path | None = None

    thumbnail: bytes | None = getattr(data, "thumbnail_data", None)

    try:
        cmd = [
            str(ffmpeg),
            "-y",
            "-v", "error",
            "-i", str(target_path),
        ]

        if thumbnail and isinstance(thumbnail, bytes) and len(thumbnail) > 0:
            suffix = ".png" if thumbnail.startswith(b"\x89PNG\r\n\x1a\n") else ".jpg"
            with tempfile.NamedTemporaryFile(dir=directory, delete=False, suffix=suffix) as tf:
                tf.write(thumbnail)
                temporary_thumb = Path(tf.name)

            cmd.extend([
                "-i", str(temporary_thumb),
                "-map", "0:v:0",
                "-map", "0:a?",
                "-map", "1:v:0",
                "-c", "copy",
                "-disposition:v:1", "attached_pic",
            ])
        else:
            cmd.extend([
                "-map", "0",
                "-c", "copy",
            ])

        metadata_fields = {
            "title": getattr(data, "title", None),
            "artist": getattr(data, "author", None),
            "genre": "XXX",
            "date": getattr(data, "publish_date", None),
        }
        for key, val in metadata_fields.items():
            if val is not None:
                cmd.extend(["-metadata", f"{key}={val}"])

        cmd.extend(["-movflags", "+faststart", str(temporary_output)])

        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise MetadataWriteError(f"FFmpeg tagging failed: {proc.stderr.strip()}")

        os.replace(temporary_output, target_path)
        return True

    except Exception as error:
        if isinstance(error, MetadataWriteError):
            raise
        raise MetadataWriteError(str(error)) from error

    finally:
        if temporary_output.exists():
            try:
                temporary_output.unlink(missing_ok=True)
            except OSError:
                pass
        if temporary_thumb and temporary_thumb.exists():
            try:
                temporary_thumb.unlink(missing_ok=True)
            except OSError:
                pass
