"""Optional Qt-free MP4 metadata writer."""
from __future__ import annotations

import logging
import os
import tempfile
from typing import Any

from .errors import MetadataWriteError
from .media import VideoObject


def _is_attached_pic(stream: Any) -> bool:
    disposition = getattr(stream, "disposition", None)
    if disposition is None:
        return False
    attached = getattr(disposition, "attached_pic", None)
    if attached is not None:
        try:
            return attached in disposition
        except TypeError:
            return bool(attached)
    return False


def write_tags(path: str, data: VideoObject) -> bool:
    try:
        import av
    except ImportError:
        return False

    thumbnail: Any = getattr(data, "thumbnail_data", None)
    directory = os.path.dirname(path) or "."
    with tempfile.NamedTemporaryFile(dir=directory, delete=False, suffix=".mp4") as temporary:
        temporary_path = temporary.name
    try:
        with av.open(path) as source, av.open(temporary_path, mode="w", format="mp4") as target:
            mapping = {}
            for stream in source.streams:
                if stream.type == "video" and _is_attached_pic(stream):
                    continue
                if hasattr(target, "add_stream_from_template"):
                    mapping[stream] = target.add_stream_from_template(template=stream)
                else:
                    mapping[stream] = target.add_stream(template=stream)
            target.metadata.update({
                key: str(value) for key, value in {
                    "title": data.title, "artist": data.author,
                    "genre": "XXX", "date": data.publish_date,
                }.items() if value is not None
            })
            thumbnail_stream = None
            if thumbnail:
                codec = "png" if thumbnail.startswith(b"\x89PNG\r\n\x1a\n") else "mjpeg"
                thumbnail_stream = target.add_stream(codec, rate=1)
                thumbnail_stream.disposition.attached_pic = True
            for packet in source.demux():
                if packet.stream in mapping:
                    if packet.dts is None:
                        continue
                    packet.stream = mapping[packet.stream]
                    target.mux(packet)
            if thumbnail and thumbnail_stream:
                packet = av.Packet(thumbnail)
                packet.stream = thumbnail_stream
                target.mux(packet)
        os.replace(temporary_path, path)
        return True
    except Exception as error:
        raise MetadataWriteError(str(error)) from error
    finally:
        if os.path.exists(temporary_path):
            try:
                os.unlink(temporary_path)
            except OSError:
                logging.warning("Could not remove temporary metadata file %s", temporary_path)
