from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from PySide6.QtCore import QObject, Signal, QAbstractListModel, QModelIndex, Property, Qt


@dataclass(slots=True)
class VideoFilters:
    duration_minimum: int | None = None
    duration_maximum: int | None = None
    author_regex: str | None = None
    tags_regex: str | None = None
    title_regex: str | None = None
    quality_minimum: str | None = None
    quality_maximum: str | None = None
    published_before: str | None = None
    published_after: str | None = None


@dataclass(slots=True)
class VideoObject:
    title: str
    author: str
    length: int
    tags: list[str] | None
    thumbnail_url: str
    video_id: str
    publish_date: datetime
    qualities: list[str]
    status: str
    identifier: str | None = None
    output_path: Path | None = None
    index: int | None = None
    selected_quality: str | None = None


class DownloadListModel(QAbstractListModel):
    JobIdRole = Qt.ItemDataRole.UserRole + 1
    TitleRole = Qt.ItemDataRole.UserRole + 2
    AuthorRole = Qt.ItemDataRole.UserRole + 3
    DurationRole = Qt.ItemDataRole.UserRole + 4
    AvailableQualitiesRole = Qt.ItemDataRole.UserRole + 5
    SelectedQualityRole = Qt.ItemDataRole.UserRole + 6
    ProgressRole = Qt.ItemDataRole.UserRole + 7

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = []

    def roleNames(self):
        return {
            self.JobIdRole: b"jobId",
            self.TitleRole: b"title",
            self.AuthorRole: b"author",
            self.DurationRole: b"duration",
            self.AvailableQualitiesRole: b"availableQualities",
            self.SelectedQualityRole: b"selectedQuality",
            self.ProgressRole: b"progress"
        }

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._items)):
            return None

        item = self._items[index.row()]

        if role == self.JobIdRole:
            return item.get("jobId", "")
        elif role == self.TitleRole:
            return item.get("title", "")
        elif role == self.AuthorRole:
            return item.get("author", "")
        elif role == self.DurationRole:
            return item.get("duration", "")
        elif role == self.AvailableQualitiesRole:
            return item.get("availableQualities", [])
        elif role == self.SelectedQualityRole:
            return item.get("selectedQuality", "")
        elif role == self.ProgressRole:
            return item.get("progress", 0)

        return None

    def add_video(self, video: VideoObject, preferred_quality: str):
        if video.length in (None, "Not Available"):
            display_duration = "N/A"

        else:
            minutes, seconds = divmod(int(video.length), 60)
            display_duration = f"{minutes:02d}:{seconds:02d}"

        # 1. NEW: Force all qualities to be strings so they match QML perfectly
        string_qualities = [str(q) for q in video.qualities] if video.qualities else []

        # 2. Use the new string list for the fallback check
        selected_quality = preferred_quality if preferred_quality in string_qualities else (
            string_qualities[0] if string_qualities else "best")

        job_id = video.video_id or video.identifier or str(len(self._items))
        item_data = {
            "jobId": str(job_id),
            "title": f"{video.index}) {video.title}" if video.index else video.title,
            "author": video.author,
            "duration": display_duration,
            "availableQualities": video.qualities,
            "selectedQuality": selected_quality,
            "progress": 0  # Starts at 0%
        }

        self.beginInsertRows(QModelIndex(), len(self._items), len(self._items))
        self._items.append(item_data)
        self.endInsertRows()

    def set_video_quality(self, job_id: str, new_quality: str):
        for row, item in enumerate(self._items):
            if item["jobId"] == str(job_id):
                item["selectedQuality"] = new_quality

                # Tell QML to redraw this specific row
                idx = self.index(row, 0)
                self.dataChanged.emit(idx, idx, [self.SelectedQualityRole])
                break

    def update_progress(self, job_id: str, progress: int):
        for row, item in enumerate(self._items):
            if item["jobId"] == str(job_id):
                item["progress"] = progress
                index = self.index(row, 0)
                self.dataChanged.emit(index, index, [self.ProgressRole])
                break


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
