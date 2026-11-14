from __future__ import annotations

from pathlib import Path

from src.shared.download_options import video_file_path, video_output_path
from src.shared.media import VideoObject

from .settings import CliSettings


def output_path_for(media: VideoObject, settings: CliSettings, *, premium: bool = False) -> Path:
    target = video_file_path(video_output_path(media, media.index or 1, settings.path_template, settings.output_path))
    if premium:
        from src.shared.library_export import ExportOptions, library_video_path
        target = library_video_path(target, media, ExportOptions.from_settings(settings))
    return target
