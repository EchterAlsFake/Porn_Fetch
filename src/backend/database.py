"""
Notice: This database feature is entirely optional!
"""
import json
import asyncio

from datetime import datetime
from src.backend.config import app_settings
from PySide6.QtCore import QObject, Slot, Signal
from src.backend.download_manager import VideoObject
from peewee import SqliteDatabase, Model, CharField, DateTimeField, BooleanField, TextField, FloatField, DatabaseProxy, \
    ForeignKeyField, JOIN, fn

db_proxy = DatabaseProxy()


class DatabaseBridge(QObject):
    # Signals to notify QML when data changes
    iteratorsChanged = Signal()
    statisticsChanged = Signal()
    downloadSaved = Signal(str)  # Emits video_id when saved

    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialize Peewee database on startup
        self._database = initialize_database()

    # =========================================================================
    # 1. SLOT CALLED BY YOUR BACKEND DOWNLOADER
    # =========================================================================
    @Slot(object)
    def on_video_updated(self, video: VideoObject):
        """
        Call this slot from your Python backend when a download finishes.
        Runs asynchronously off the UI thread!
        """
        if self._database is not None:
            asyncio.create_task(self._async_save_video(video))

    async def _async_save_video(self, video: VideoObject):
        # Offload SQLite disk I/O to threadpool
        video_id = await asyncio.to_thread(self._save_video, video)
        self.downloadSaved.emit(video_id)
        self.iteratorsChanged.emit()
        self.statisticsChanged.emit()

    @staticmethod
    def _save_video(video: VideoObject) -> str:
        """Perform the Peewee upsert; kept separate so it is easy to test."""
        file_size_mb = 0.0
        if video.output_path:
            try:
                file_size_mb = video.output_path.stat().st_size / (1024 * 1024)
            except OSError:
                # Failed and in-progress downloads may not have an output file yet.
                pass

        iterator_ref = None
        if video.origin_iterator_url:
            iterator_ref, _ = OriginIterator.get_or_create(
                url=video.origin_iterator_url,
                defaults={"name": video.origin_iterator_name or "Unknown Source"}
            )
            if video.origin_iterator_name and iterator_ref.name != video.origin_iterator_name:
                iterator_ref.name = video.origin_iterator_name
                iterator_ref.save(only=[OriginIterator.name])

        record, created = VideoRecord.get_or_create(
            url=video.url,
            defaults={
                "title": video.title,
                "video_id": video.video_id,
                "author": video.author,
                "length": str(video.length),
                "thumbnail_url": video.thumbnail_url,
                "publish_date": video.publish_date,
                "status": video.status,
                "tags_json": json.dumps(video.tags or []),
                "qualities_json": json.dumps(video.qualities or []),
                "identifier": video.identifier,
                "output_path": str(video.output_path) if video.output_path else None,
                "selected_quality": video.selected_quality,
                "file_size_mb": file_size_mb,
                "is_hls": video.is_hls,
                "missing_segments": video.missing_segments,
                "origin_iterator_url": video.origin_iterator_url,
                "origin_iterator": iterator_ref
            }
        )

        if not created:
            record.status = video.status
            record.output_path = str(video.output_path) if video.output_path else None
            record.selected_quality = video.selected_quality
            record.file_size_mb = file_size_mb
            record.is_hls = video.is_hls
            record.missing_segments = video.missing_segments
            record.origin_iterator_url = video.origin_iterator_url
            record.origin_iterator = iterator_ref
            record.downloaded_at = datetime.now()
            record.save()

        return record.video_id


    @Slot(result=list)
    def getAvailableIterators(self) -> list[dict]:
        """Returns all sources (Channels/Playlists) to display in QML ComboBox/Dialog."""
        if self._database is None:
            return []
        return list(OriginIterator.select().dicts())


    @Slot(str, result=list)
    def getFailedVideosForIterator(self, iterator_url: str) -> list[dict]:
        """Returns a list of failed video dicts formatted for QML views."""
        if self._database is None:
            return []

        def _fetch():
            query = VideoRecord.select().where(
                (VideoRecord.origin_iterator == iterator_url) &
                (VideoRecord.status == "failed")
            )
            return [
                {
                    "title": v.title,
                    "url": v.url,
                    "video_id": v.video_id,
                    "status": v.status
                }
                for v in query
            ]
        return _fetch()

    @staticmethod
    def _status_bucket(status: str | None) -> str:
        normalized = (status or "").strip().lower()
        if normalized in {"complete", "completed", "downloaded", "finished", "success", "successful"}:
            return "successful"
        if normalized in {"error", "failed", "failure"} or "fail" in normalized:
            return "failed"
        return "other"

    @Slot(result="QVariantMap")
    def getDashboardStats(self) -> dict:
        """Return compact, chart-ready download statistics for the QML dashboard."""
        empty_result = {
            "enabled": False,
            "total": 0,
            "successful": 0,
            "failed": 0,
            "other": 0,
            "successRate": 0,
            "totalSizeMb": 0.0,
            "lastDownloaded": "",
            "sources": [],
        }
        if self._database is None:
            return empty_result

        status_rows = (
            VideoRecord
            .select(VideoRecord.status, fn.COUNT(VideoRecord.url).alias("count"))
            .group_by(VideoRecord.status)
            .dicts()
        )
        totals = {"successful": 0, "failed": 0, "other": 0}
        for row in status_rows:
            totals[self._status_bucket(row["status"])] += row["count"]

        source_rows = (
            VideoRecord
            .select(
                OriginIterator.name.alias("source_name"),
                VideoRecord.status,
                fn.COUNT(VideoRecord.url).alias("count"),
            )
            .join(OriginIterator, JOIN.LEFT_OUTER)
            .group_by(OriginIterator.name, VideoRecord.status)
            .dicts()
        )
        sources_by_name: dict[str, dict] = {}
        for row in source_rows:
            name = row["source_name"] or "Direct downloads"
            source = sources_by_name.setdefault(
                name,
                {"name": name, "total": 0, "successful": 0, "failed": 0, "other": 0},
            )
            count = row["count"]
            bucket = self._status_bucket(row["status"])
            source["total"] += count
            source[bucket] += count

        total = sum(totals.values())
        downloaded = totals["successful"] + totals["failed"]
        size_and_date = (
            VideoRecord
            .select(
                fn.COALESCE(fn.SUM(VideoRecord.file_size_mb), 0).alias("total_size"),
                fn.MAX(VideoRecord.downloaded_at).alias("last_downloaded"),
            )
            .dicts()
            .get()
        )
        last_downloaded = size_and_date["last_downloaded"]
        if isinstance(last_downloaded, datetime):
            last_downloaded = last_downloaded.isoformat()
        elif last_downloaded:
            last_downloaded = str(last_downloaded)

        return {
            "enabled": True,
            "total": total,
            **totals,
            "successRate": round((totals["successful"] / downloaded) * 100) if downloaded else 0,
            "totalSizeMb": round(float(size_and_date["total_size"] or 0), 1),
            "lastDownloaded": last_downloaded or "",
            "sources": sorted(sources_by_name.values(), key=lambda source: source["total"], reverse=True),
        }


class ListField(TextField):
    def db_value(self, value):
        if value is None:
            return None
        return json.dumps(value)  # Converts list -> '[1, 2, 3]' for SQL

    def python_value(self, value):
        if value is None:
            return []
        return json.loads(value)  # Converts '[1, 2, 3]' -> list for Python


class BaseModel(Model):
    class Meta:
        database = db_proxy


# E.g., Playlists, Channels, Models etc.
class OriginIterator(BaseModel):
    url = CharField(unique=True, primary_key=True)  # Primary key lookup
    name = CharField()


class VideoRecord(BaseModel):
    # This is the primary lookup key
    url = CharField(unique=True, index=True)

    title = CharField()
    video_id = CharField()
    author = CharField()
    length = CharField()
    thumbnail_url = CharField()
    publish_date = DateTimeField()
    status = CharField()

    tags_json = TextField(null=True)
    qualities_json = TextField()

    # Optional stuff
    identifier = CharField(null=True)
    output_path = CharField(null=True)
    selected_quality = CharField(null=True)

    file_size_mb = FloatField(default=0.0)
    downloaded_at = DateTimeField(default=datetime.now)

    is_hls = BooleanField(null=True) # If no, will be treated as a normal MP4 stream
    missing_segments = ListField(null=True)
    is_from_account = BooleanField(null=True) # If the user logged into his own account and fetched his own playlist or sum
    origin_iterator_url = CharField(null=True) # The origin iterator URL e.g., from a Model, Channel, Playlist and so on

    origin_iterator = ForeignKeyField(OriginIterator, backref="videos",
                                      null=True, on_delete="SET NULL")


def initialize_database():
    if app_settings.track_videos:
        db = SqliteDatabase(
            app_settings.database_path,
            pragmas={
                'journal_mode': 'wal',
                'synchronous': 'normal',
                'cache_size': -16000,
            }
        )
        db_proxy.initialize(db)
        db.connect()
        db.create_tables([OriginIterator, VideoRecord])
        return db

    return None


def get_available_iterators():
    """Returns a list of dicts: [{'name': 'Channel A', 'url': '...'}, ...]"""
    return list(OriginIterator.select().dicts())


# 2. Fetch failed videos for the selected iterator URL
def get_failed_videos_for_iterator(iterator_url: str):
    """SQLite filters both status and iterator URL in a single fast query!"""
    return VideoRecord.select().where(
        (VideoRecord.origin_iterator == iterator_url) &
        (VideoRecord.status == "failed")
    )
