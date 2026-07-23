from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from PySide6.QtCore import QObject, Signal


@dataclass(slots=True)
class VideoObject:
    title: str
    author: str
    length: str
    tags: list[str] | None
    thumbnail_url: str
    video_id: str
    publish_date: datetime
    qualities: list[str]
    status: str
    identifier: str | None = None
    output_path: Path | None = None


class DownloadManager(QObject): # Inherit from QObject so we can work with Slots and Signals
    video_added = Signal(VideoObject)
    video_updated = Signal(VideoObject)
    video_removed = Signal(int)

    def __init__(self):
        super().__init__()
        self._videos: dict[str, VideoObject] = {}

    def add_video(self, video: VideoObject) -> None:
        self._videos[video.identifier] = video
        self.video_added.emit(video)

    def update_status(self, identifier: str, new_status):
        if video := self._videos.get(identifier):
            video.status = new_status
            self.video_updated.emit(video)

    def remove_video(self, identifier: str):
        if identifier in self._videos.keys():
            del self._videos[identifier]
            self.video_removed.emit(identifier)

    def get_video(self, identifier: str) -> VideoObject | None:
        if identifier in self._videos:
            return self._videos[identifier]

        return None
