from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from base_api.modules.static_functions import normalize_quality
from PySide6.QtCore import QObject, Signal, QAbstractListModel, QModelIndex, Qt

from src.backend.config import app_settings


FREE_MAXIMUM_QUALITY = 720
PREMIUM_QUALITY_NAMES = {"best", "half", "4k", "uhd", "2k", "qhd", "fullhd", "fhd"}


def quality_requires_premium(quality: str | int) -> bool:
    """Return whether a quality can only be used with the full unlock."""
    normalized = normalize_quality(quality)
    if str(normalized) in PREMIUM_QUALITY_NAMES:
        return True

    try:
        return int(normalized) > FREE_MAXIMUM_QUALITY
        # If the quality is bigger than 720p (defines as maximum free) user needs a license
    except (ValueError, TypeError):
        return False # If my check fails for whatever reason we are kind and assume it doesn't require a license.
        # Otherwise a bug in production could break the app and I don't want that to happen lol


def select_allowed_quality(
    preferred_quality: str | int, # The quality user chose in settings
    available_qualities: list[str | int], # The actual available qualities, depends on per video / page
    has_premium: bool, # For license enforcing
) -> str:
    """Choose the preferred stream or the highest stream the user may access."""
    available = [str(quality) for quality in available_qualities] # Consistent string comprehension
    preferred = str(preferred_quality or "") # fallback just in case I fucked up in my code

    if preferred in available and (has_premium or not quality_requires_premium(preferred)):
        return preferred # Checks if the preferred quality exists  + licensing enforcement

    allowed = available if has_premium else [
        quality for quality in available if not quality_requires_premium(quality)
    ] # Licensing enforcement, either all qualities are available, or only those in the free section

    if not allowed:
        return "" # Rejects the selected quality, because user does not have premium

    def quality_rank(quality: str) -> tuple[int, int]:
        normalized = normalize_quality(quality)
        try:
            return 1, int(normalized)
        except ValueError:
            # Keep named fallbacks such as "worst" below concrete streams.
            return 0, 0

    return max(allowed, key=quality_rank)
    # (1, 1080) wins over (1, 720)
    # (1, 144) wins over (0, 0)
    # (0, 0) is used for a string representation


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
    url: str
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
    source_video: object | None = None

    # These will be dynamically written to
    origin_iterator_url: str | None = None
    origin_iterator_name: str | None = None
    is_hls: bool | None = None
    missing_segments: list[int] | None = None


class DownloadListModel(QAbstractListModel):
    # The roles define the data source, so QML knows what to ask for
    JobIdRole = Qt.ItemDataRole.UserRole + 1
    TitleRole = Qt.ItemDataRole.UserRole + 2
    AuthorRole = Qt.ItemDataRole.UserRole + 3
    DurationRole = Qt.ItemDataRole.UserRole + 4
    AvailableQualitiesRole = Qt.ItemDataRole.UserRole + 5
    SelectedQualityRole = Qt.ItemDataRole.UserRole + 6
    ProgressRole = Qt.ItemDataRole.UserRole + 7
    SelectedRole = Qt.ItemDataRole.UserRole + 8
    StatusRole = Qt.ItemDataRole.UserRole + 9

    def __init__(self, parent=None, premium_access=None):
        super().__init__(parent)
        self._items = []
        self._row_by_id: dict[str, int] = {}  # O(1) row lookup cache because why not optimizing for nanoseconds xD
        self._premium_access = premium_access or (lambda: False) # The function which checks if user has premium access
        app_settings.qualityChanged.connect(self.update_all_qualities)
        # if the user changed the preferred quality in settings it will instantly update all rows

    def has_premium_access(self) -> bool:
        return bool(self._premium_access()) # Evaluates the function

    def update_all_qualities(self, new_quality_idx: int) -> None:
        preferred_quality = str(app_settings.mappings_quality.get(new_quality_idx, "best"))
        has_premium = self.has_premium_access()

        for row, item in enumerate(self._items):
            selected_quality = select_allowed_quality(
                preferred_quality,
                item.get("availableQualities", []),
                has_premium,
            )
            if item.get("selectedQuality") != selected_quality:
                item["selectedQuality"] = selected_quality
                item["_video"].selected_quality = selected_quality or None
                idx = self.index(row, 0)
                self.dataChanged.emit(idx, idx, [self.SelectedQualityRole])

    def enforce_quality_access(self) -> None:
        self.update_all_qualities(app_settings.quality)

    def roleNames(self):
        return {
            self.JobIdRole: b"jobId",
            self.TitleRole: b"title",
            self.AuthorRole: b"author",
            self.DurationRole: b"duration",
            self.AvailableQualitiesRole: b"availableQualities",
            self.SelectedQualityRole: b"selectedQuality",
            self.ProgressRole: b"progress",
            self.SelectedRole: b"selected",
            self.StatusRole: b"status",
            # Creates the role names as bytes, so the underlying C++ Shiboken engine doesn't have to convert
            # this in each call. Looks weird I know, but this is more memory efficient and faster
        }

    def rowCount(self, parent=QModelIndex()):
        return len(self._items) # Returns the total amount of rows

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        "This function returns the actual data for a given role, so the data from the item"
        if not index.isValid() or not (0 <= index.row() < len(self._items)):
            return None # Checks if the requested index even exists, if not, returns None

        item = self._items[index.row()] # Gets the item based on the row index that was requested

        # Returns the data based on the provided role with fallbacks if stuff doesn't exist
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
            return item.get("progress", 0) # Please don't be zero ahh
        elif role == self.SelectedRole:
            return item.get("selected", False)
        elif role == self.StatusRole:
            return item.get("status", "pending")

        return None

    def add_video(self, video: VideoObject, preferred_quality: str) -> str:
        """This function is called by the Backend class and adds an actual video. QML picks it up and creates the row"""
        if video.length in (None, "Not Available"): # Not all videos have a length attribute
            display_duration = "N/A"

        else:
            minutes, seconds = divmod(int(video.length), 60) # Format it pretty to display hours : minutes
            display_duration = f"{minutes:02d}:{seconds:02d}"

        selected_quality = select_allowed_quality(
            preferred_quality,
            video.qualities or [],
            self.has_premium_access(),
        ) # Determines the quality just like above
        video.selected_quality = selected_quality or None

        job_id = str(video.identifier or video.video_id or len(self._items)) # Job ID for unique reference of the row
        item_data = {
            "jobId": str(job_id),
            "title": f"{video.index}) {video.title}" if video.index else video.title,
            "author": video.author,
            "duration": display_duration,
            "availableQualities": video.qualities,
            "selectedQuality": selected_quality,
            "progress": 0,  # Starts at 0%
            "selected": False,
            "status": "pending",
            "_video": video, # Stores the actual data from the video object
        }

        new_row = len(self._items)
        self.beginInsertRows(QModelIndex(), len(self._items), len(self._items)) # Tells Qt to start creating
        self._items.append(item_data) # Puts the tem data into the row
        self._row_by_id[job_id] = new_row
        self.endInsertRows() # Stops creating (QML starts displaying the row here)
        return selected_quality # For verification the actual quality is returned

    def set_video_quality(self, job_id: str, new_quality: str) -> bool:
        """This applies a new quality based on the users choice for a given video"""
        row = self._row_by_id.get(job_id)

        if row is None:
            return False

        if quality_requires_premium(new_quality) and not self.has_premium_access():
            return False # aborts if the user doesn't have permission

        item = self._items[row]

        if new_quality not in item.get("availableQualities", []):
            return False

        if item["selectedQuality"] != new_quality:
            item["selectedQuality"] = new_quality
            item["_video"].selected_quality = new_quality

            idx = self.index(row, 0)
            self.dataChanged.emit(idx, idx, [self.SelectedQualityRole])

        return True

    def get_video(self, job_id: str) -> VideoObject | None:
        row = self._row_by_id.get(str(job_id))
        if row is None:
            return None
        return self._items[row]["_video"]

    def get_status(self, job_id: str) -> str | None:
        row = self._row_by_id.get(str(job_id))
        if row is None:
            return None
        return self._items[row].get("status", "pending")

    def selected_job_ids(self) -> list[str]:
        return [item["jobId"] for item in self._items if item.get("selected", False)]

    def set_selected(self, job_id: str, selected: bool) -> bool:
        row = self._row_by_id.get(str(job_id))
        if row is None:
            return False

        item = self._items[row]
        selected = bool(selected)
        if item.get("selected") != selected:
            item["selected"] = selected
            idx = self.index(row, 0)
            self.dataChanged.emit(idx, idx, [self.SelectedRole])
        return True

    def set_all_selected(self, selected: bool) -> None:
        if not self._items:
            return

        changed_rows = []
        selected = bool(selected)
        for row, item in enumerate(self._items):
            if item.get("selected") != selected:
                item["selected"] = selected
                changed_rows.append(row)

        if changed_rows:
            first = self.index(changed_rows[0], 0)
            last = self.index(changed_rows[-1], 0)
            self.dataChanged.emit(first, last, [self.SelectedRole])

    def set_status(self, job_id: str, status: str) -> None:
        row = self._row_by_id.get(str(job_id))
        if row is None:
            return

        item = self._items[row]
        if item.get("status") != status:
            item["status"] = status
            idx = self.index(row, 0)
            self.dataChanged.emit(idx, idx, [self.StatusRole])


    def update_progress(self, job_id: str, progress: int) -> None:
        row = self._row_by_id.get(str(job_id))
        if row is None:
            return

        item = self._items[row]
        if item["progress"] != progress:  # Avoid redundant QML repaints
            item["progress"] = progress
            idx = self.index(row, 0)
            self.dataChanged.emit(idx, idx, [self.ProgressRole])


class DownloadManager(QObject): # Inherit from QObject so we can work with Slots and Signals
    video_added = Signal(VideoObject) # Tells the list model when a new video is there
    video_updated = Signal(VideoObject) # Updates the status for a video
    video_removed = Signal(int) # Removes the row

    def __init__(self):
        super().__init__()
        self._videos: dict[str, VideoObject] = {} # Keeps track of the current videos

    def add_video(self, video: VideoObject) -> None:
        # Notice: This function is connected to the database bridge using a Signal
        self._videos[video.identifier] = video # Adds a new video using the identifier
        self.video_added.emit(video)

    def update_status(self, identifier: str, new_status):
        # Notice: This function is connected to the database bridge using a Signal
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
