"""iOS adapter for base_api's local FFmpeg operations (no Qt dependency)."""
from pathlib import Path
import os
import tempfile

import _ios_ffmpeg


def library_path():
    return Path(_ios_ffmpeg.__file__).resolve()


def remux_ts_to_mp4(input_path, output_path, *, metadata=None, thumbnail=None):
    from base_api.modules.ffmpeg import _extract_metadata_fields, _extract_thumbnail_bytes
    source, destination = Path(input_path).resolve(), Path(output_path).resolve()
    if source == destination:
        raise ValueError("Remux input and output must be different files")
    destination.parent.mkdir(parents=True, exist_ok=True)
    cover = _extract_thumbnail_bytes(metadata, thumbnail)
    temporary_cover = None
    try:
        if cover:
            suffix = ".png" if cover.startswith(b"\x89PNG\r\n\x1a\n") else ".jpg"
            with tempfile.NamedTemporaryFile(dir=destination.parent, suffix=suffix, delete=False) as stream:
                stream.write(cover)
                temporary_cover = Path(stream.name)
        _ios_ffmpeg.remux(str(source), str(destination), _extract_metadata_fields(metadata),
                          str(temporary_cover) if temporary_cover else None)
        return True
    except BaseException:
        destination.unlink(missing_ok=True)
        raise
    finally:
        if temporary_cover:
            temporary_cover.unlink(missing_ok=True)


def write_metadata_tags(path, data, *, thumbnail=None):
    from base_api.modules.errors import MetadataWriteError
    source = Path(path).resolve()
    if not source.is_file():
        return False
    descriptor, name = tempfile.mkstemp(dir=source.parent, suffix=".mp4", prefix=".ios-tags-")
    os.close(descriptor)
    temporary = Path(name)
    try:
        remux_ts_to_mp4(source, temporary, metadata=data, thumbnail=thumbnail)
        os.replace(temporary, source)
        return True
    except Exception as error:
        raise MetadataWriteError(str(error)) from error
    finally:
        temporary.unlink(missing_ok=True)
