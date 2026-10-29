"""Restore paused rows locally and coalesce desktop queue saves off the GUI thread."""
from __future__ import annotations

import asyncio
from pathlib import Path

from src.shared.download_recovery import queue_record, read_queue, write_queue


class DownloadRecovery:
    def __init__(self, backend, path: Path):
        self.backend, self.path = backend, path
        self.task = None
        self.closing = False
        self.restoring = False
        self.dirty = False
        self.lock = asyncio.Lock()
        self.model = backend._downloads_model
        self.model.rowsInserted.connect(self.changed)
        self.model.rowsRemoved.connect(self.changed)
        self.model.dataChanged.connect(self.changed)

    def restore(self):
        self.restoring = True
        try:
            for video, progress in read_queue(self.path):
                quality = video.selected_quality
                self.backend.download_manager.add_video(video)
                self.model.set_video_quality(video.identifier, quality)
                self.model.set_status(video.identifier, "cancelled")
                self.model.update_progress(video.identifier, progress)
        except (OSError, ValueError, TypeError, KeyError) as error:
            self.backend.logger.warning("Could not restore the saved download queue: %s", error)
        finally:
            self.restoring = False

    def changed(self, *_):
        if self.closing or self.restoring:
            return
        self.dirty = True
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return
        if self.task is None or self.task.done():
            self.task = loop.create_task(self._delayed_save(), name="download-queue-save")

    async def _delayed_save(self):
        try:
            while self.dirty:
                self.dirty = False
                await asyncio.sleep(.2)
                await self.save()
        except OSError:
            self.backend.logger.exception("Could not save the download queue")

    async def save(self):
        async with self.lock:
            rows = []
            for row in range(self.model.rowCount()):
                index = self.model.index(row, 0)
                job = self.model.data(index, self.model.JobIdRole)
                if self.model.get_status(job) != "completed":
                    rows.append(queue_record(self.model.get_video(job), self.model.data(index, self.model.ProgressRole)))
            await asyncio.to_thread(write_queue, self.path, rows)

    async def close(self):
        self.closing = True
        if self.task is not None:
            await self.task
        await self.save()
