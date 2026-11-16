"""QML adapter and bounded download dispatcher for the persistent creator library."""
from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Property, QObject, Signal, Slot

from src.backend import clients
from src.backend.config import IS_ANDROID, TEMP_DIRECTORY, app_settings
from src.backend.creator_sources import resolve_subscription, scan_subscription
from src.database.creators import MEMBERSHIPS, SCANS, SUBSCRIPTIONS, VIDEOS, CreatorRepository, quoted
from src.database.service import PocketBaseService
from src.shared.creator_library import ACTIVE, CreatorLibrary, identity, source_url
from src.shared.download_options import filename_component
from src.shared.download_recovery import queue_record
from src.shared.media import VideoObject, quality_requires_premium, select_allowed_quality
from src.shared.provider_routing import route_url

logger = logging.getLogger(__name__)
STATES = ["", "new", "pending", "downloading", "paused", "completed", "failed", "ignored"]


class CreatorBridge(QObject):
    changed = Signal()
    aboutToChange = Signal()
    saveFinished = Signal(str, str)

    def __init__(self, backend, tracker, *, supported=True, parent=None):
        super().__init__(parent)
        self.backend, self.tracker, self.supported = backend, tracker, supported
        self.library = None
        self.repo = None
        self._sources, self._rows = [], []
        self._history = []
        self._total = 0
        self._selection = ("", "", 1)
        self._message = "" if supported else "Creator subscriptions are not available on iOS yet."
        self._availability = "checking" if supported else "unsupported"
        self._availability_error = ""
        self._availability_task = None
        self._saving = False
        self._tasks = set()
        self._workers = {}
        self._job_videos = {}
        self._dirty_jobs = set()
        self._job_states = {}
        self._job_errors = {}
        self._event = asyncio.Event()
        self._start_lock = asyncio.Lock()
        self._job_write_lock = asyncio.Lock()
        self._refresh_task = None
        self._refresh_dirty = False
        self._dispatcher = None
        self._closing = False
        self._started = False
        backend._downloads_model.dataChanged.connect(self._downloads_changed)
        backend.download_manager.video_updated.connect(self._video_updated)
        app_settings.outputPathChanged.connect(self._defaults_changed)
        app_settings.androidOutputFolderChanged.connect(self._defaults_changed)

    @Property(list, notify=changed)
    def sources(self):
        return self._sources

    @Property(list, notify=changed)
    def videos(self):
        return self._rows

    @Property(list, notify=changed)
    def scanHistory(self):
        return self._history

    @Property(int, notify=changed)
    def videoTotal(self):
        return self._total

    @Property(str, notify=changed)
    def message(self):
        return self._message

    @Property(bool, notify=changed)
    def available(self):
        return self._availability == "ready"

    @Property(str, notify=changed)
    def availability(self):
        return self._availability

    @Property(str, notify=changed)
    def availabilityError(self):
        return self._availability_error

    @Property(bool, constant=True)
    def canManageComponents(self):
        return self.supported and not IS_ANDROID and bool(getattr(self.backend, "maintenance_available", False))

    @Property(str, constant=True)
    def availabilityHelp(self):
        if not self.supported:
            return self.tr("Creator subscriptions need a native PocketBase runtime. This is not available on iOS yet.")
        if IS_ANDROID:
            return self.tr("1. Install an updated Porn Fetch APK for your device architecture. PocketBase is included in the APK.\n2. Reopen Porn Fetch and choose Check again.\nIf you build from source, use scripts/build_android.py so the PocketBase library is compiled and bundled.")
        if self.canManageComponents:
            return self.tr("1. Choose Manage components below.\n2. Select the PocketBase component and finish the installation. Close Porn Fetch if the installer asks.\n3. Return to Creators and choose Check again.")
        return self.tr("1. For a source checkout, run this command from the project folder:\nuv run python Porn_Fetch_CLI.py --install-pocketbase\n2. For a portable copy, place the PocketBase executable in third_party beside Porn Fetch, or install it on PATH. You can also set PORN_FETCH_POCKETBASE_BINARY to its full path.\n3. Choose Check again. If PocketBase is already installed, open the error details and check its executable and database folder permissions.")

    @Slot()
    def manageComponents(self):
        if self.canManageComponents:
            self.backend.open_maintenance("components")

    @Property(bool, notify=changed)
    def saving(self):
        return self._saving

    @Property(bool, notify=changed)
    def premium(self):
        return self.backend.has_premium_access()

    @Slot()
    def refreshAccess(self):
        self.changed.emit()
        self.request_refresh()

    @Property(bool, notify=changed)
    def activity(self):
        return self._saving or bool(self._workers) or bool(self.library and any(not task.done() for task in self.library.scan_tasks.values()))

    @Slot()
    def _defaults_changed(self):
        self.changed.emit()

    @Property(str, constant=True)
    def defaultQuality(self):
        return "best"

    @Property(str, notify=changed)
    def defaultFolder(self):
        if IS_ANDROID:
            return app_settings.android_output_folder
        return str(Path(app_settings.output_path).expanduser().resolve())

    @Property(bool, constant=True)
    def mobileStorage(self):
        return IS_ANDROID

    def _spawn(self, coroutine):
        task = asyncio.create_task(coroutine)
        self._tasks.add(task)
        task.add_done_callback(self._done)
        return task

    def _done(self, task):
        self._tasks.discard(task)
        if not task.cancelled() and (error := task.exception()):
            logger.error("Creator operation failed", exc_info=(type(error), error, error.__traceback__))
            self._message = str(error)
            self.changed.emit()

    async def ensure_ready(self):
        if not self.supported:
            raise RuntimeError(self._message)
        async with self._start_lock:
            if self.library is not None:
                return self.library
            self._availability = "checking"
            self._availability_error = ""
            self.changed.emit()
            try:
                await asyncio.to_thread(self._check_runtime)
                client = await self.tracker.open_database()
                repo = CreatorRepository(client)
                await repo.enable_batches()
                library = CreatorLibrary(repo, scan_subscription,
                    changed=self.request_refresh, premium=self.backend.has_premium_access, mobile=IS_ANDROID)
                await library.recover()
                async for row in repo.all(VIDEOS, filter='job != "" && status != "completed"'):
                    self._job_videos[row["job"]] = row["id"]
                self.repo, self.library = repo, library
                self._dispatcher = self._spawn(self._dispatch())
                self._availability = "ready"
            except Exception as error:
                self._availability = "unavailable"
                self._availability_error = str(error)
                raise
            finally:
                self.changed.emit()
        return self.library

    def _check_runtime(self):
        if self.tracker.is_running:
            return
        if IS_ANDROID:
            from src.database.android import AndroidPocketBaseService
            AndroidPocketBaseService(self.tracker.data_path)._load()
        else:
            from src.database.installer import verify_pocketbase_binary
            service = self.tracker._service or PocketBaseService(self.tracker.data_path, binary_path=self.tracker.binary_path)
            verify_pocketbase_binary(service.find_binary())

    @Slot()
    def checkAvailability(self):
        if not self.supported or self._closing:
            return
        if self._availability_task is None or self._availability_task.done():
            self._availability_task = self._spawn(self._check_availability())

    async def _check_availability(self):
        try:
            await self.ensure_ready()
            await self._refresh()
        except Exception:
            logger.info("Creator PocketBase check failed: %s", self._availability_error)

    def start(self):
        if self._started or not self.supported:
            return
        self._started = True
        self._availability_task = self._spawn(self._startup())

    async def _startup(self):
        try:
            library = await self.ensure_ready()
        except Exception:
            logger.info("Creator PocketBase is unavailable: %s", self._availability_error)
            return
        # The initial entitlement check is already started by first-use startup.
        while self.backend._license_bridge is not None and self.backend._license_bridge.busy and not self._closing:
            await asyncio.sleep(.1)
        await self._refresh()
        for source in self._sources:
            if source.get("startup") and not self._closing:
                self._watch_scan(library.scan(source["id"], "startup"))

    def request_refresh(self):
        self._event.set()
        self._refresh_dirty = True
        if not self._closing and (self._refresh_task is None or self._refresh_task.done()):
            self._refresh_task = self._spawn(self._refresh_loop())

    async def _refresh_loop(self):
        while self._refresh_dirty and not self._closing:
            self._refresh_dirty = False
            await asyncio.sleep(.15)
            await self._refresh()

    async def _refresh(self):
        if self.library is None:
            return
        sources = await self.library.subscriptions()
        rows, total, history = [], 0, []
        source_id, status, page = self._selection
        if source_id and any(s["id"] == source_id for s in sources):
            history = (await self.repo.page(SCANS, size=10, filter=f"subscription = {quoted(source_id)}", sort="-started,id"))["items"]
            result = await self.repo.video_page(source_id, status, page, preview=not self.premium)
            total = result["totalItems"]
            for member in result["items"]:
                video = member.get("expand", {}).get("video", {})
                row = dict(video, id=member["id"], videoId=video["id"], status="ignored" if member["ignored"] else video["status"],
                           duration=video.get("duration", ""), published=video.get("published", ""), quality=video.get("quality") or "", progress=video.get("progress", 0))
                row["title"] = row.get("title") or Path(video["url"].split("?")[0]).name or "Video"
                if row["status"] in {"preparing", "queued"}:
                    row["status"] = "pending"
                rows.append(row)
        if self._selection != (source_id, status, page):
            self.request_refresh()
            return
        self.aboutToChange.emit()
        self._sources, self._rows, self._total, self._history = sources, rows, total, history
        self.changed.emit()

    @Slot(str, int, int)
    def select(self, id, filter_index, page):
        self._selection = (id, STATES[max(0, min(filter_index, len(STATES) - 1))], max(1, page + 1))
        self.request_refresh()

    @Slot(str, result=str)
    def providerForUrl(self, url):
        try:
            return route_url(source_url(url)).provider
        except ValueError:
            return ""

    @Slot(str, "QVariantMap")
    def save(self, id, values):
        if self._saving or self._closing:
            return
        self._saving = True
        self.changed.emit()
        self._spawn(self._save(id, values))

    async def _save(self, id, values):
        error = ""
        try:
            library = await self.ensure_ready()
            id = await library.save(id, values, resolve_subscription)
            app_settings._settings.setValue("Creators/enabled", True)
            app_settings.sync()
            self._watch_scan(library.scan_tasks.get(id))
            await self._refresh()
        except Exception as exc:
            error = str(exc)
        finally:
            self._saving = False
            self.changed.emit()
            self.saveFinished.emit(id, error)

    def _watch_scan(self, task):
        if task is not None:
            task.add_done_callback(lambda finished: self._scan_done(finished))

    def _scan_done(self, task):
        if not task.cancelled() and (error := task.exception()):
            self._message = str(error)
        self.request_refresh()

    @Slot(str)
    def scan(self, id):
        if self._closing:
            return
        async def action():
            library = await self.ensure_ready()
            active = library.scan_tasks.get(id)
            if active is not None and not active.done():
                await library.cancel_scan(id)
            else:
                self._watch_scan(library.scan(id))
        self._spawn(action())

    @Slot(str, str)
    def bulk(self, id, action):
        if self._closing:
            return
        async def apply():
            library = await self.ensure_ready()
            if action == "pause":
                await self._pause(id)
            else:
                await library.queue(id, action)
            self.request_refresh()
        self._spawn(apply())

    def _stop_job(self, job):
        self.backend.stop_download(job)
        task = self.backend._download_tasks.get(job)
        if (task is None or task.done()) and self.backend._downloads_model.get_video(job) is not None:
            self.backend._downloads_model.set_status(job, "cancelled")

    async def _pause(self, source_id):
        async for member in self.repo.all(MEMBERSHIPS, filter=f"subscription = {quoted(source_id)}"):
            video = await self.repo.get(VIDEOS, member["video"])
            if video["status"] in ACTIVE:
                if video.get("job"):
                    self._stop_job(video["job"])
                await self.repo.put(VIDEOS, video["id"], {"status": "paused"})

    @Slot(str, str, str)
    def videoAction(self, source_id, member_id, action):
        if self._closing:
            return
        async def apply():
            await self.ensure_ready()
            member = await self.repo.get(MEMBERSHIPS, member_id)
            if member["subscription"] != source_id:
                raise ValueError("This video belongs to a different subscription.")
            video = await self.repo.get(VIDEOS, member["video"])
            if action in {"ignored", "new"}:
                await self.repo.put(MEMBERSHIPS, member_id, {"ignored": action == "ignored"})
            elif action == "paused":
                if video.get("job"):
                    self._stop_job(video["job"])
                if video["status"] != "completed":
                    await self.repo.put(VIDEOS, video["id"], {"status": "paused"})
            elif action == "downloading":
                await self.library.download_index(source_id, video["id"])
                if video["status"] not in {"completed", "downloading", "preparing", "queued"}:
                    await self.repo.put(VIDEOS, video["id"], {"status": "pending", "owner": (video.get("owner") or source_id) if self.premium else source_id, "error": ""})
            self.request_refresh()
        self._spawn(apply())

    @Slot(str)
    def remove(self, id):
        if self._closing:
            return
        async def apply():
            library = await self.ensure_ready()
            async for member in self.repo.all(MEMBERSHIPS, filter=f"subscription = {quoted(id)}"):
                video = await self.repo.get(VIDEOS, member["video"])
                if video.get("owner") != id:
                    continue
                other = await self.repo.find(MEMBERSHIPS, f"video = {quoted(video['id'])} && subscription != {quoted(id)} && ignored = false")
                data = {"owner": other["subscription"] if other else ""}
                if not other and video["status"] in ACTIVE:
                    if video.get("job"):
                        self._stop_job(video["job"])
                    data["status"] = "paused"
                await self.repo.put(VIDEOS, video["id"], data)
            await library.remove(id)
            await self._refresh()
        self._spawn(apply())

    async def _dispatch(self):
        while not self._closing:
            self._event.clear()
            capacity = (max(1, int(app_settings.parallel_downloads)) if self.premium else 1) * 2 - len(self._workers)
            if capacity > 0:
                rows = await self.repo.page(VIDEOS, size=capacity, filter='status = "pending"', sort="id")
                for video in rows["items"]:
                    if video["id"] in self._workers:
                        continue
                    if await self._download_index(video) is None:
                        self._event.set()  # Continue past older Premium-only pending jobs.
                        continue
                    await self.repo.put(VIDEOS, video["id"], {"status": "preparing"})
                    task = self._spawn(self._run_video(video))
                    self._workers[video["id"]] = task
                    task.add_done_callback(lambda done, id=video["id"]: self._worker_done(id))
            await self._event.wait()

    async def _download_index(self, record):
        try:
            return await self.library.download_index(record.get("owner", ""), record["id"])
        except PermissionError as error:
            if record.get("job"):
                self._stop_job(record["job"])
            await self.repo.put(VIDEOS, record["id"], {"status": "paused", "error": str(error)})
            return None

    def _worker_done(self, id):
        self._workers.pop(id, None)
        self.request_refresh()

    async def _completed_history(self, record):
        history = await self.repo.find("video_records", f"url = {quoted(record['url'])} && status = \"completed\"")
        if history:
            return history
        key = record["identity"].split(":video:", 1)[-1]
        async for candidate in self.repo.all("video_records", filter=f"video_id = {quoted(key)} && status = \"completed\""):
            try:
                provider = route_url(candidate["url"]).provider
                if provider == record["provider"] and identity(provider, candidate["url"], candidate.get("video_id")) == record["identity"]:
                    return candidate
            except ValueError:
                continue
        return None

    async def _run_video(self, record):
        job = record.get("job") or uuid.uuid4().hex
        video = None
        created = False
        self._job_errors.pop(job, None)
        try:
            download_index = await self._download_index(record)
            if download_index is None:
                return
            snapshot = record.get("snapshot")
            if snapshot and not self.premium and quality_requires_premium(snapshot.get("selected_quality", "")):
                await self.repo.put(VIDEOS, record["id"], {"status": "paused", "error": "Saved progress uses a Premium quality. Activate Premium to resume it; the free preview supports up to 720p."})
                return
            # Reuse an ordinary queue row instead of starting the same transfer twice.
            for row in tuple(self.backend._downloads_model._items):
                candidate = row["_video"]
                try:
                    provider = route_url(candidate.url).provider
                    if identity(provider, candidate.url, candidate.video_id) == record["identity"]:
                        video, job = candidate, str(candidate.identifier)
                        break
                except ValueError:
                    continue
            self._job_videos[job] = record["id"]
            await self.repo.put(VIDEOS, record["id"], {"job": job})
            if video is None:
                history = await self._completed_history(record)
                if history:
                    await self.repo.put(VIDEOS, record["id"], {"status": "completed", "progress": 100, "output_path": history.get("output_path", "")})
                    return
                snapshot = record.get("snapshot")
                if snapshot:
                    values = dict(snapshot)
                    values.pop("progress", None)
                    values["thumbnail_url"] = ""
                    values["publish_date"] = datetime.fromisoformat(values["publish_date"]) if values.get("publish_date") else None
                    values["output_path"] = Path(values["output_path"])
                    video = VideoObject(**values)
                else:
                    source = await self.repo.get(SUBSCRIPTIONS, record["owner"])
                    if not source.get("folder"):
                        raise ValueError("Choose a download destination in this subscription's settings.")
                    native = await clients.get_video(record["url"])
                    video = await clients.load_video_attributes(native)
                    preference = source.get("quality") or "best"
                    offered = video.qualities
                    if preference.isdecimal():
                        offered = [q for q in offered if str(q).isdecimal() and int(q) <= int(preference)]
                        preference = "best"
                    quality = select_allowed_quality(preference, offered, self.backend.has_premium_access())
                    if not quality:
                        raise ValueError("This video does not offer a stream at 720p or below for the free preview. Higher resolutions require Premium." if not self.premium else "This video does not offer the requested quality.")
                    video.identifier = job
                    video.source_video = native
                    video.origin_iterator_url, video.origin_iterator_name = source["url"], source["name"]
                    video.index = download_index
                    video.selected_quality = quality
                    filename = filename_component(video.title) + " [" + filename_component(record["id"]) + "].mp4"
                    if IS_ANDROID:
                        video.output_path = Path(TEMP_DIRECTORY) / "creator-downloads" / filename
                        video.export_destination = source["folder"]
                    else:
                        video.output_path = Path(source["folder"]) / filename
                video.status = "cancelled"
                await self.repo.put(VIDEOS, record["id"], {"title": video.title, "quality": str(video.selected_quality),
                    "output_path": str(video.output_path), "snapshot": queue_record(video)})
                if (await self.repo.get(VIDEOS, record["id"]))["status"] != "preparing" or self._closing:
                    return
                remaining = await self.repo.find(MEMBERSHIPS, f"video = {quoted(record['id'])} && ignored = false")
                if remaining is None:
                    await self.repo.put(VIDEOS, record["id"], {"status": "new"})
                    return
                selected_quality = str(video.selected_quality)
                self.backend.download_manager.add_video(video)
                created = True
                # Adding a row applies global preferences; subscriptions retain their own quality.
                self.backend._downloads_model.set_video_quality(job, selected_quality)
                self.backend._downloads_model.set_status(job, "queued")
            download_index = await self._download_index(dict(record, job=job))
            if download_index is None:
                return
            video.index = download_index
            previous_task = self.backend._download_tasks.get(job)
            if video.source_video is None or (record.get("snapshot") and (previous_task is None or previous_task.done())):
                self.backend._downloads_model.set_status(job, "queued")
                native = await clients.get_video(video.url)
                fresh = await clients.load_video_attributes(native)
                selected = str(video.selected_quality)
                for field in ("title", "author", "length", "tags", "thumbnail_url", "video_id", "publish_date", "qualities", "library_metadata"):
                    setattr(video, field, getattr(fresh, field))
                video.source_video = native
                self.backend._downloads_model.refresh_metadata(job)
                if selected not in [str(q) for q in fresh.qualities]:
                    raise ValueError("The saved quality is no longer available. Choose another quality in Downloads; existing progress was kept.")
                self.backend._downloads_model.set_video_quality(job, selected)
            if self.backend._downloads_model.get_status(job) == "completed":
                await self.repo.put(VIDEOS, record["id"], {"status": "completed", "progress": 100})
                return
            if (await self.repo.get(VIDEOS, record["id"]))["status"] in {"paused", "new", "failed", "completed"}:
                return
            previous_task = self.backend._download_tasks.get(job)
            if previous_task is None or previous_task.done():
                self.backend._downloads_model.set_status(job, "cancelled")
            self.backend.download_video(job)
            task = self.backend._download_tasks.get(job)
            if task is None:
                raise ValueError("The download could not be started. Check the selected quality and destination.")
            await asyncio.shield(task)
            await self._save_job(job)
            if created and self.backend._downloads_model.get_status(job) == "completed":
                self.backend.remove_video(job)
        except asyncio.CancelledError:
            await self.repo.put(VIDEOS, record["id"], {"status": "paused"})
            raise
        except Exception as exc:
            current = await self.repo.get(VIDEOS, record["id"])
            if current["status"] != "paused":
                self._job_errors[job] = str(exc)
                if self.backend._downloads_model.get_video(job) is not None:
                    self.backend._downloads_model.set_error(job, "", str(exc))
                    self.backend._downloads_model.set_status(job, "failed")
                await self.repo.put(VIDEOS, record["id"], {"status": "failed", "error": str(exc)})

    def _downloads_changed(self, first, last, roles):
        for row in range(first.row(), last.row() + 1):
            job = self.backend._downloads_model.data(self.backend._downloads_model.index(row, 0), self.backend._downloads_model.JobIdRole)
            if job in self._job_videos:
                self._capture_job(job)
                self._dirty_jobs.add(job)
        if self._dirty_jobs:
            self._schedule_job_save()

    def _video_updated(self, video):
        if video.identifier in self._job_videos:
            self._capture_job(video.identifier, video)
            self._dirty_jobs.add(video.identifier)
            self._schedule_job_save()

    def _schedule_job_save(self):
        task = getattr(self, "_job_save_task", None)
        if task is None or task.done():
            self._job_save_task = self._spawn(self._flush_jobs())

    async def _flush_jobs(self):
        while self._dirty_jobs:
            await asyncio.sleep(.25)
            jobs, self._dirty_jobs = self._dirty_jobs, set()
            for job in jobs:
                await self._save_job(job)
            self.request_refresh()

    def _capture_job(self, job, video=None):
        model = self.backend._downloads_model
        video = video or model.get_video(job)
        if video is None:
            return
        status = model.get_status(job) or video.status
        status = {"cancelled": "paused", "stopping": "paused"}.get(status, status)
        row = model._row_by_id.get(job)
        progress = model.data(model.index(row, 0), model.ProgressRole) if row is not None else 0
        # The production engine removes completed rows synchronously after its signal.
        # Capture their final snapshot now, before scheduling an asynchronous write.
        self._job_states[job] = {"status": status, "progress": 100 if status == "completed" else progress,
            "title": video.title, "quality": str(video.selected_quality or ""),
            "snapshot": queue_record(video, progress), "output_path": str(video.output_path),
            "error": self._job_errors.get(job, "Download failed. Open Downloads for error details.") if status == "failed" else ""}

    async def _save_job(self, job):
        async with self._job_write_lock:
            if job not in self._job_videos:
                return
            self._capture_job(job)
            payload = self._job_states.get(job)
            if payload is None:
                return
            await self.repo.put(VIDEOS, self._job_videos[job], payload)
            if payload["status"] == "completed":
                self._job_states.pop(job, None)
                self._job_errors.pop(job, None)
                self._job_videos.pop(job, None)
                self._dirty_jobs.discard(job)

    async def stop(self):
        self._closing = True
        if self.library:
            await self.library.close()
        tasks = [t for t in [self._dispatcher, *self._workers.values()] if t is not None and not t.done()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    async def close(self):
        await self.stop()
        pending = [t for t in self._tasks if t is not asyncio.current_task() and not t.done()]
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
        if self._dirty_jobs:
            await self._flush_jobs()
