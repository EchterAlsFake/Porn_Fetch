import os
import asyncio

from dataclasses import dataclass, field
from PySide6.QtCore import QObject, QAbstractListModel, Qt, QModelIndex, Slot
from enum import IntEnum
from backend.config import TEMP_DIRECTORY_SEGMENTS, TEMP_DIRECTORY_STATES


@dataclass
class DownloadTask:
    identifier: int
    video: object
    title: str
    author: str
    display_duration: str
    sort_duration: str
    thumbnail: str
    qualities: list[int]

    progress: int = 0
    selected_quality: int = 0
    status: str = "Idle"

    stop_event: asyncio.Event = field(default_factory=asyncio.Event)

    @property
    def segment_dir(self) -> str:
        return os.path.join(TEMP_DIRECTORY_SEGMENTS, self.title)

    @property
    def segment_state_path(self) -> str:
        return os.path.join(TEMP_DIRECTORY_STATES, self.title)


class DownloadRoles(IntEnum):
    IdentifierRole = Qt.ItemDataRole.UserRole + 1
    TitleRole = Qt.ItemDataRole.UserRole + 2
    AuthorRole = Qt.ItemDataRole.UserRole + 3
    DurationRole = Qt.ItemDataRole.UserRole + 4
    ThumbnailRole = Qt.ItemDataRole.UserRole + 5
    QualitiesRole = Qt.ItemDataRole.UserRole + 6
    ProgressRole = Qt.ItemDataRole.UserRole + 7
    StatusRole = Qt.ItemDataRole.UserRole + 8


class DownloadManagerModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._tasks: list[DownloadTask] = []
        self._lookup: dict[int, int] = {}

    def rowCount(self, /, parent = QModelIndex()) -> int:
        return len(self._tasks)

    def roleNames(self) -> dict[int, bytes]:
        return {
            DownloadRoles.IdentifierRole: b"identifier",
            DownloadRoles.TitleRole: b"title",
            DownloadRoles.AuthorRole: b"author",
            DownloadRoles.DurationRole: b"duration",
            DownloadRoles.ThumbnailRole: b"thumbnail",
            DownloadRoles.QualitiesRole: b"qualities",
            DownloadRoles.ProgressRole: b"progress",
            DownloadRoles.StatusRole: b"status"
        }

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._tasks)):
            return None

        task = self._tasks[index.row()]

        if role == DownloadRoles.IdentifierRole:
            return task.identifier
        elif role == DownloadRoles.TitleRole:
            return task.title
        elif role == DownloadRoles.AuthorRole:
            return task.author
        elif role == DownloadRoles.DurationRole:
            return task.display_duration
        elif role == DownloadRoles.ThumbnailRole:
            return task.thumbnail
        elif role == DownloadRoles.QualitiesRole:
            return task.qualities
        elif role == DownloadRoles.ProgressRole:
            return task.progress
        elif role == DownloadRoles.StatusRole:
            return task.status
        return None

    def add_task_from_signal(self, task: DownloadTask):
        """Replaces your old tree widget insertion code."""
        start_row = len(self._tasks)
        self.beginInsertRows(QModelIndex(), start_row, start_row)
        self._tasks.append(task)
        self._lookup[task.identifier] = start_row
        self.endInsertRows()

    @Slot(int, int)
    def update_progress(self, identifier: int, new_progress: int):
        """Safely mutates network progress state and tells the UI to repaint."""
        if identifier in self._lookup:
            row = self._lookup[identifier]
            task = self._tasks[row]
            task.progress = new_progress

            # Target specifically the progress column/role loop
            model_index = self.index(row, 0)
            self.dataChanged.emit(model_index, model_index, [DownloadRoles.ProgressRole])

    def get_task(self, identifier: int) -> DownloadTask | None:
        if identifier in self._lookup:
            return self._tasks[self._lookup[identifier]]
        return None