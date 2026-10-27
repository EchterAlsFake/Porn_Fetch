"""Public model/playlist desktop E2E: native pagination, filters, downloads and history."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import logging
import os
import re
import shutil
import sys
import tempfile
import traceback
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from src.tests.collection_cases import collection_cases
from src.tests.smoke.download_lifecycle import public_url, require, validate_media


class CollectionProbe:
    """Passive native scraper/preparation observers; no results are replaced."""
    def __init__(self):
        self.stage = ""
        self.pages, self.items, self.candidates = [], {}, []
        self.stack = ExitStack()

    def __enter__(self):
        from base_api import Helper

        from src.backend.video_processor import ProcessVideos
        page_method, item_method = Helper._process_page, Helper._process_item
        prepare_method = ProcessVideos.process_single_video

        async def page(helper, job, *args, **options):
            stage = self.stage
            result = await page_method(helper, job, *args, **options)
            query = parse_qs(urlsplit(job.url).query)
            self.pages.append({"stage": stage, "index": job.index, "url": public_url(job.url),
                               "pagination_query": {key: query[key] for key in ("page", "p") if key in query},
                               "items": len(result.items),
                               "video_keys": [video_key(item.url) for item in result.items],
                               "error": str(result.result.error) if result.result is not None else None})
            return result

        async def item(helper, job, *args, **options):
            stage = self.stage
            result = await item_method(helper, job, *args, **options)
            if result.result is not None and result.result.succeeded:
                self.items[stage, id(result.result.item)] = job.page_index
            return result

        async def prepare(value):
            stage = self.stage
            source, video = await prepare_method(value)
            self.candidates.append({"stage": stage, "url": video.url, "title": video.title,
                                    "author": video.author, "minutes": video.length,
                                    "page_index": self.items.get((stage, id(source)))})
            return source, video

        from unittest.mock import patch
        self.stack.enter_context(patch.object(Helper, "_process_page", page))
        self.stack.enter_context(patch.object(Helper, "_process_item", item))
        self.stack.enter_context(patch.object(ProcessVideos, "process_single_video", staticmethod(prepare)))
        return self

    def __exit__(self, *error):
        return self.stack.__exit__(*error)


def jobs(gui):
    model = gui.backend._downloads_model
    return [model.data(model.index(row, 0), model.JobIdRole) for row in range(model.rowCount())]


def video_key(url):
    identity = public_url(url)
    # PornHub's identity is in the query, unlike the path IDs of other sources.
    # Keep that public ID while still discarding playlist/tracking/CDN tokens.
    viewkey = parse_qs(urlsplit(url).query).get("viewkey")
    if viewkey:
        identity += "?viewkey=" + viewkey[0]
    return hashlib.sha256(identity.encode()).hexdigest()[:20]


def first_new_page_position(pages):
    """Find a real later-page position despite overlapping/pinned entries."""
    ordered = sorted(pages, key=lambda page: page["index"])
    first, *later = ordered
    require(first["index"] == 0 and bool(later), "Pagination has no first/later page evidence")
    known = set(first["video_keys"])
    position = first["items"] + 1
    for page in later:
        for offset, key in enumerate(page["video_keys"]):
            if key not in known:
                return position + offset
        position += page["items"]
    raise AssertionError("Later-page requests repeated the first page's videos")


def task_trace(task):
    """Record native await locations when a live source stalls."""
    coroutine, frames = task.get_coro(), []
    while coroutine is not None:
        frame = getattr(coroutine, "cr_frame", None) or getattr(coroutine, "gi_frame", None)
        if frame is not None:
            frames.append(f"{frame.f_code.co_filename}:{frame.f_lineno} {frame.f_code.co_name}")
        coroutine = getattr(coroutine, "cr_await", None) or getattr(coroutine, "gi_yieldfrom", None)
    return {"task": task.get_name(), "await_stack": frames}


class CollectionChecks:
    def __init__(self, gui, settings, database, dashboard, case, probe, args, progress):
        self.gui, self.settings, self.db, self.dashboard = gui, settings, database, dashboard
        self.case, self.probe, self.args = case, probe, args
        self.progress = progress
        self.model = gui.backend._downloads_model

    def control(self, name):
        from PySide6.QtCore import QObject
        item = self.gui.window.findChild(QObject, name)
        assert item is not None, f"Missing production control {name}"
        return item

    async def drain(self):
        await self.gui.wait(lambda: not self.db.busy, "History writes did not settle")
        await asyncio.sleep(0)
        self.gui.pump()

    async def clear(self):
        await self.drain()
        for job in jobs(self.gui):
            self.gui.backend.remove_video(job)
        self.gui.pump()

    async def start(self, stage, *, limit=3, start=0, end=0, title="", author="", minimum=0):
        await self.clear()
        self.progress(stage)
        self.probe.stage = stage
        self.settings.result_limit = limit
        self.settings.processing_delay = 0
        for name, prop, value in (("downloadStartIndex", "value", start), ("downloadEndIndex", "value", end),
                                   ("downloadTitleRegex", "text", title), ("downloadAuthorRegex", "text", author),
                                   ("downloadMinimumDuration", "value", minimum), ("downloadMaximumDuration", "value", 0),
                                   ("downloadTagsRegex", "text", ""), ("downloadMinimumQuality", "currentIndex", 0),
                                   ("downloadMaximumQuality", "currentIndex", 0), ("downloadAfterDate", "text", ""),
                                   ("downloadBeforeDate", "text", "")):
            self.control(name).setProperty(prop, value)
        self.control("downloadTitlePattern").setProperty("text", "$index-$video_id.mp4")
        field = "modelUrlInput" if self.case["kind"] == "model" else "playlistUrlInput"
        button = "getModelVideosButton" if self.case["kind"] == "model" else "getPlaylistVideosButton"
        self.control(field).setProperty("text", self.case["url"])
        self.gui.window.requestActivate()
        self.gui.pump()
        self.gui.click(button)
        task = self.gui.backend._video_fetch_task
        assert task is not None, "Source button did not start the real GUI preparation task"
        self.control(field).setProperty("text", self.case["url"])
        self.gui.pump()
        require(self.gui.backend.busy, "Source preparation did not expose busy state")
        require(not self.control(button).isEnabled() and self.control("cancelLoadingButton").isEnabled(),
                "Source controls did not reflect busy state")
        # The actual backend also rejects duplicate fetches while busy.
        operation = self.gui.backend.process_model_url if self.case["kind"] == "model" else self.gui.backend.process_playlist_url
        operation(self.case["url"], "$title", {})
        require(self.gui.backend._video_fetch_task is task, "Repeated source request started another task")
        return task

    async def finish(self, task):
        await self.gui.wait(task.done, "Source preparation did not finish")
        await task
        await asyncio.sleep(0)
        await self.drain()
        require(not self.gui.backend.busy and not self.control("cancelLoadingButton").isEnabled(), "Fetch left stale busy controls")
        button = "getModelVideosButton" if self.case["kind"] == "model" else "getPlaylistVideosButton"
        require(self.control(button).isEnabled(), "Source button did not recover after preparation")
        require(not self.gui.errors, f"GUI reported an error: {self.gui.errors[:1]}")
        return await self.verify_rows()

    async def verify_rows(self):
        from PySide6.QtCore import QMetaObject, Qt

        from src.backend.account_diagnostics import visual_items
        expected = jobs(self.gui)
        QMetaObject.invokeMethod(self.gui.control("downloadList"), "forceLayout", Qt.ConnectionType.DirectConnection)
        self.gui.pump()
        rows = []
        for index, job in enumerate(expected):
            video = self.model.get_video(job)
            assert video is not None and video.output_path is not None, "Prepared row lost its media/path"
            require(video.source_video is not None, "Prepared row lost its native video")
            require(video.origin_iterator_url == self.case["url"] and bool(video.origin_iterator_name), "Source identity was lost")
            require(self.model.get_status(job) == "pending" and not video.output_path.exists(), "Preparation started a media transfer")
            await self.gui.wait(lambda: bool(self.gui.controls("downloadRow", job)), "Source delegate did not render")
            labels = [item.property("text") for item in visual_items(self.gui.control("downloadRow", job))]
            require(f"{index + 1}) {video.title}" in labels and video.author in labels, "Rendered source metadata differs")
            duration = self.model.tr("%d min") % int(video.length) if video.length is not None else "N/A"
            require(self.model.data(self.model.index(index, 0), self.model.DurationRole) == duration and duration in labels,
                    "Rendered duration differs from the prepared video")
            require(self.model.data(self.model.index(index, 0), self.model.AvailableQualitiesRole) == [str(q) for q in video.qualities],
                    "Available quality roles differ from the native video")
            rows.append(video)
        require(len({video.url for video in rows}) == len(rows), "Source inserted duplicate video URLs")
        require(not self.gui.warnings and not self.dashboard.warnings, "Production QML emitted binding warnings")
        return rows

    async def workflow(self, result):
        baseline = await self.finish(await self.start("baseline"))
        require(0 < len(baseline) <= 3, "Expected bounded, nonempty source rows")
        first = next((page for page in self.probe.pages if page["stage"] == "baseline" and page["index"] == 0), None)
        assert first is not None, "No real first-page extraction was observed"
        require(first["items"] > 0, "The native first page contained no videos")
        if first["items"] >= 3:
            require(len(baseline) == 3, "Result limit did not produce exactly three available rows")
        result["baseline"] = {"rows": len(baseline), "first_page_items": first["items"], "result_limit": 3}
        # Exercise actual GUI filtering; calculate the expectation from unchanged
        # real candidates rather than calling the production matcher in the test.
        target = baseline[0]
        matching = await self.finish(await self.start("filter-match", title=r"\A" + re.escape(target.title) + r"\Z",
                                                      author=r"\A" + re.escape(target.author) + r"\Z"))
        candidates = [row for row in self.probe.candidates if row["stage"] == "filter-match"]
        expected = [row["url"] for row in candidates if row["title"].lower() == target.title.lower()
                    and row["author"].lower() == target.author.lower()]
        require(expected and [row.url for row in matching] == expected, "Matching GUI regexes did not select the expected real candidate")
        rejected = await self.finish(await self.start("filter-reject", title="(?!)"))
        require(not rejected, "Rejecting GUI regex retained source rows")
        result["filters"] = {"real_candidate_match": True, "rejected_rows": 0}
        ranged = await self.finish(await self.start("range", start=2, end=3))
        if first["items"] >= 3:
            require([video.index for video in ranged] == [2, 3], "Inclusive GUI range did not select original positions 2/3")
            require([video.output_path.name[:2] for video in ranged] == ["02", "03"], "Original range indexes were lost in filenames")
        result["range"] = {"positions": [video.index for video in ranged]}
        # Delay is a real app setting and guarantees the user can cancel after
        # one native row arrives without a fast source completing first.
        task = await self.start("cancel", limit=50)
        self.settings.processing_delay = 1
        await self.gui.wait(lambda: self.model.rowCount() >= 1 or task.done(), "Cancellation fixture produced no real row")
        require(not task.cancelled(), "Native source preparation was cancelled before the user clicked Cancel Loading")
        if task.done():
            await task
        require(self.model.rowCount() >= 1, "Source preparation ended without a row before Cancel Loading")
        require(not task.done(), "Preparation ended before cancellation could be exercised")
        self.gui.click("cancelLoadingButton")
        self.progress("cancel-settling")
        await self.gui.wait(task.done, "Cancel Loading did not settle")
        await asyncio.gather(task, return_exceptions=True)
        await asyncio.sleep(.15)
        count = self.model.rowCount()
        self.gui.pump()
        require(task.cancelled() and not self.gui.backend.busy and self.model.rowCount() == count, "Cancellation did not leave a stable, idle list")
        self.settings.processing_delay = 0
        result["cancel"] = {"native_rows_before_cancel": count, "task_cancelled": True}
        # Traverse the native first page without fabricating/truncating it.
        # The GUI prepares the first two actual entries from the next page.
        paged = await self.finish(await self.start("pagination", limit=2, start=first["items"] + 1, end=first["items"] + 2))
        later = [page for page in self.probe.pages if page["stage"] == "pagination" and page["index"] >= 1]
        require(later, "No real later-page request/extraction was observed")
        prepared = [row for row in self.probe.candidates if row["stage"] == "pagination"]
        if paged:
            pages = [page for page in self.probe.pages if page["stage"] == "pagination"]
            position = first_new_page_position(pages)
            page_one = next(page for page in pages if page["index"] == 0)
            overlapping_prefix = position - page_one["items"] - 1
            if not any(video_key(row.url) not in page_one["video_keys"] for row in paged):
                # A site may legitimately repeat a few cards at the page boundary.
                # Use the actual source range to render a distinct card; never
                # discard/reorder native entries to make the assertion pass.
                paged = await self.finish(await self.start("pagination-distinct", limit=2, start=position, end=position + 1))
                prepared = [row for row in self.probe.candidates if row["stage"] == "pagination-distinct"]
                page_one = next(page for page in self.probe.pages if page["stage"] == "pagination-distinct" and page["index"] == 0)
                require(paged, "Distinct later-page source position produced no GUI rows")
            require(all(row["page_index"] is not None and row["page_index"] >= 1 for row in prepared),
                    "Pagination did not put later-page videos into the actual model")
            require(any(video_key(row.url) not in page_one["video_keys"] for row in paged),
                    "Distinct later-page rows repeated the first page's videos")
            result["pagination"] = {"later_page_rows": len(paged), "page_indexes": [row["page_index"] for row in prepared],
                                    "overlapping_prefix_rows": overlapping_prefix, "first_distinct_position": position}
        else:
            require(all(not page["items"] and not page["error"] for page in later), "Empty pagination was caused by an upstream error")
            result["pagination"] = {"later_page_rows": 0, "end_of_source_verified": True}
            paged = await self.finish(await self.start("download-fallback"))
        require(paged, "No real source row remains available for the selected download")
        await self.download_selected(paged, result)

    async def download_selected(self, rows, result):
        self.progress("selected-download-and-history")
        from PySide6.QtCore import Qt
        from PySide6.QtTest import QTest

        from src.database.constants import ORIGIN_COLLECTION, VIDEO_COLLECTION
        from src.tests.smoke.download_queue import NativeDownloads
        candidates = [row for row in rows if any(quality <= 720 for quality in row.qualities)]
        require(candidates, "Source exposed no downloadable quality at or below 720p")
        # Prefer the shortest available real source video; never replace it with
        # a convenient unrelated fixture from another input path.
        video = min(candidates, key=lambda row: row.length if row.length is not None else float("inf"))
        job = video.identifier
        available = [str(quality) for quality in video.qualities]
        quality = min(quality for quality in video.qualities if quality <= 720)
        combo = self.gui.control("downloadQualityCombo", job)
        self.gui.click("downloadQualityCombo", job)
        self.gui.pump()
        QTest.keyClick(self.gui.window, Qt.Key.Key_Home)
        for _ in range(available.index(str(quality))):
            QTest.keyClick(self.gui.window, Qt.Key.Key_Down)
        QTest.keyClick(self.gui.window, Qt.Key.Key_Return)
        QTest.qWait(180)
        self.gui.pump()
        require(str(video.selected_quality) == str(quality) and str(combo.property("currentText")) == str(quality),
                "Actual quality selector ignored the source row")
        self.gui.click("downloadSelectAllButton")
        require(len(self.model.selected_job_ids()) == len(rows), "Select All missed source rows")
        self.gui.click("downloadClearSelectionButton")
        require(not self.model.selected_job_ids(), "Clear Selection missed source rows")
        self.gui.click("downloadSelectCheck", job)
        all_videos = {row.identifier: row for row in rows}
        with NativeDownloads(all_videos, 1, self.gui.errors) as observer:
            self.gui.click("downloadSelectedButton")
            require(set(self.gui.backend._download_tasks) == {job}, "Download Selected queued an unselected source row")
            await self.gui.wait(lambda: not self.gui.backend._download_tasks, "Selected real source download did not finish")
            require(observer.records[job] and all(not observer.records[other] for other in all_videos if other != job),
                    "Native download selection differed from the actual GUI selection")
        require(video.status == "completed" and job not in jobs(self.gui), "Completed source row did not automatically clear")
        for other in rows:
            if other.identifier != job:
                require(self.model.get_status(other.identifier) == "pending" and not other.output_path.exists(),
                        "Unselected source row transferred media")
        probe = await validate_media(video.output_path, self.args.ffmpeg, video.length)
        await self.drain()
        client = self.db.tracker._client
        assert client is not None
        records = await client.list_records(VIDEO_COLLECTION)
        origins = await client.list_records(ORIGIN_COLLECTION)
        require(len(origins) == 1 and origins[0]["url"] == self.case["url"], "History lost its source URL/identity")
        successes = [row for row in records if row["status"] == "completed"]
        require(len(successes) == 1 and successes[0]["url"] == video.url, "History duplicated or missed the selected completion")
        require(all(row["origin_iterator_url"] == self.case["url"] and row["origin_iterator"] == origins[0]["id"] for row in records),
                "Prepared/completed history records lost their source association")
        stats = self.dashboard.statistics()
        require(stats["successful"] == 1 and stats["total"] == len(records) and len(stats["sources"]) == 1,
                "Rendered dashboard did not update after the collection download")
        source = stats["sources"][0]
        require(source["name"] == origins[0]["name"] and source["total"] == len(records), "Dashboard source group differs from actual history")
        result["download"] = {"url": video.url, "quality": quality, "probe": probe, "unselected_rows": len(rows) - 1,
                              "native_calls": 1, "history_records": len(records), "source_name": source["name"]}


async def run(args, directory):
    from PySide6.QtCore import QSettings

    from src.backend import clients
    from src.backend.account_diagnostics import AccountAccessGuard, extend_timeout_for_wait
    from src.backend.config import app_settings
    from src.database.bridge import DatabaseBridge
    from src.tests.smoke.download_gui import DownloadWindow
    from src.tests.smoke.statistics_gui import Dashboard
    previous = app_settings._settings, app_settings._custom_settings
    disk = QSettings(str(directory / "settings.ini"), QSettings.Format.IniFormat)
    for key, value in {"Video/track_videos": True, "Video/write_metadata": False,
                       "Video/database_path": str(directory / "legacy.db"), "Video/result_limit": 3,
                       "Privacy/dns_over_https": False, "Privacy/encrypted_ch": False,
                       "Misc/network_logging": False, "Misc/trust_environment": False,
                       "Performance/download_workers": 2, "Performance/videos_concurrency": 1,
                       "Performance/pages_concurrency": 1, "Performance/retries": 2, "Performance/timeout": 25}.items():
        disk.setValue(key, value)
    app_settings.set_settings_storage(disk)
    gui = DownloadWindow(args.timeout)
    gui.backend.load_clients()
    report = {"scope": "Actual public model/playlist GUI pagination, selected media and source history",
              "planned_sources": args.cases, "results": []}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    active_timeout = None
    blocked_providers, rate_events = {}, []

    def save():
        for status in ("PASS", "FAIL", "MANUAL", "UNVERIFIED", "BLOCKED"):
            report[status.lower()] = sum(row["status"] == status for row in report["results"])
        args.report.write_text(json.dumps(report, indent=2) + "\n")

    db = dashboard = None
    try:
        with args.report.with_suffix(".log").open("w", buffering=1) as log:
            for case in args.cases:
                result = dict(case)
                report["results"].append(result)
                if case["status"] != "AUTOMATED":
                    print(case["status"] + " " + case["id"] + ": " + case["reason"], flush=True)
                    save()
                    continue
                if case["provider"] in blocked_providers:
                    result.update(status="BLOCKED", access_control=blocked_providers[case["provider"]])
                    save()
                    print("BLOCKED " + case["id"] + ": provider already stopped at access control", flush=True)
                    continue
                result["status"] = "RUNNING"
                guard = AccountAccessGuard(on_wait=lambda seconds: (extend_timeout_for_wait(active_timeout, seconds), extend_timeout_for_wait(gui.active_timeout, seconds)))
                gui.check_access = guard.raise_if_blocked
                print("RUN " + case["id"], flush=True)
                console = sys.stdout
                def progress(stage):
                    result["stage"] = stage
                    save()
                    print("  " + case["id"] + " " + stage, file=console, flush=True)
                probe = None
                try:
                    with redirect_stdout(log), redirect_stderr(log), guard:
                        active_timeout = asyncio.timeout(args.timeout)
                        async with active_timeout:
                            current = directory / case["id"]
                            app_settings.output_path = str(current / "media")
                            app_settings.pocketbase_data_path = str(current / "history")
                            db = DatabaseBridge(parent=gui.engine)
                            gui.backend.bind_database_bridge(db)
                            dashboard = Dashboard(db, app_settings)
                            db.start()
                            database = db
                            await gui.wait(lambda: not database.busy, "Real database startup did not finish")
                            gui.window.requestActivate()
                            gui.pump()
                            with CollectionProbe() as probe:
                                checks = CollectionChecks(gui, app_settings, db, dashboard, case, probe, args, progress)
                                await checks.workflow(result)
                                result["native_pages"] = probe.pages
                    result["status"] = "PASS"
                except asyncio.CancelledError:
                    result.update(status="BLOCKED" if guard.blocked else "INTERRUPTED", access_control=guard.blocked)
                    if guard.blocked:
                        blocked_providers[case["provider"]] = guard.blocked
                    else:
                        raise
                except Exception as error:
                    traceback.print_exc(file=log)
                    result.update(status="FAIL", error_type=type(error).__name__, error=str(error) or type(error).__name__,
                                  pending_tasks=[task_trace(task) for task in asyncio.all_tasks() if task is not asyncio.current_task()])
                finally:
                    active_timeout = None
                    result["native_challenges"] = guard.native_challenge_events
                    if probe is not None:
                        result["native_pages"] = probe.pages
                    fetch = gui.backend._video_fetch_task
                    if fetch is not None and not fetch.done():
                        fetch.cancel()
                    for event in gui.backend._download_stop_events.values():
                        event.set()
                    tasks = tuple(gui.backend._background_tasks)
                    if tasks:
                        _, pending = await asyncio.wait(tasks, timeout=30)
                        for task in pending:
                            task.cancel()
                        await asyncio.gather(*tasks, return_exceptions=True)
                    if dashboard is not None:
                        dashboard.close()
                        dashboard = None
                    if db is not None:
                        manager = gui.backend.download_manager
                        manager.video_added.disconnect(db.on_video_updated)
                        manager.video_updated.disconnect(db.on_video_updated)
                        db.busyChanged.disconnect(gui.backend._update_activity)
                        db.initializationFailed.disconnect(gui.backend.handle_message)
                        await db.close()
                        gui.backend.database_bridge = None
                        db.deleteLater()
                        db = None
                    for job in jobs(gui):
                        gui.backend.remove_video(job)
                    gui.errors.clear()
                    rate_events.extend(guard.rate_limit_events)
                    save()
                    print(result["status"] + " " + case["id"] + (": " + result["error"][:250] if "error" in result else ""), flush=True)
    except asyncio.CancelledError:
        return 130
    finally:
        await gui.shutdown()
        await clients.close_all_clients()
        app_settings._settings, app_settings._custom_settings = previous
        report["rate_limit_recovery"] = rate_events
        save()
    print(f"{report['pass']} passed, {report['fail']} failed, {report['blocked']} blocked, "
          f"{report['manual']} manual, {report['unverified']} unverified. Report: {args.report}")
    return int(bool(report["fail"] or report["blocked"]))


async def offline_contract(args, directory):
    """Production source controls reject invalid inputs before any HTTP call."""
    from unittest.mock import patch

    from base_api import BaseCore
    from curl_cffi.requests import AsyncSession
    from PySide6.QtCore import QObject, QSettings

    from src.backend.config import app_settings
    from src.tests.smoke.download_gui import DownloadWindow

    previous = app_settings._settings, app_settings._custom_settings
    app_settings.set_settings_storage(QSettings(str(directory / "settings.ini"), QSettings.Format.IniFormat))
    app_settings.track_videos = False
    report = {"offline_only": True, "http_attempts": 0, "results": []}

    async def forbidden(*params, **options):
        report["http_attempts"] += 1
        raise AssertionError("Source validation attempted HTTP")

    gui = DownloadWindow(args.timeout)
    try:
        with patch.object(BaseCore, "request", forbidden), patch.object(AsyncSession, "request", forbidden):
            for kind in ("model", "playlist"):
                field = "modelUrlInput" if kind == "model" else "playlistUrlInput"
                button = "getModelVideosButton" if kind == "model" else "getPlaylistVideosButton"
                gui.control(field).setProperty("text", "")
                gui.pump()
                require(not gui.control(button).isEnabled(), "Empty source URL enabled submission")
                report["results"].append({"id": kind + ".empty", "status": "PASS"})
                wrong_kind = ("https://www.pornhub.com/playlist/119820351" if kind == "model"
                              else "https://www.pornhub.com/model/catalina-days")
                for label, url, regex in (("unsupported", "https://example.invalid/profile", ""),
                                           ("single-video", "https://www.pornhub.com/view_video.php?viewkey=example", ""),
                                           ("wrong-kind", wrong_kind, ""),
                                           ("invalid-regex", "https://www.pornhub.com/model/catalina-days" if kind == "model"
                                            else "https://www.pornhub.com/playlist/119820351", "[")):
                    gui.errors.clear()
                    title_filter = gui.window.findChild(QObject, "downloadTitleRegex")
                    assert title_filter is not None
                    title_filter.setProperty("text", regex)
                    gui.control(field).setProperty("text", url)
                    gui.pump()
                    gui.click(button)
                    task = gui.backend._video_fetch_task
                    if task is not None:
                        await asyncio.wait_for(task, 5)
                        await asyncio.sleep(0)
                    gui.pump()
                    require(len(gui.errors) == 1 and not gui.backend.busy and not jobs(gui),
                            f"{kind}.{label} did not reject input cleanly: {gui.errors}")
                    require(not gui.control("cancelLoadingButton").isEnabled(), "Invalid input left Cancel Loading enabled")
                    report["results"].append({"id": kind + "." + label, "status": "PASS"})
            require(not gui.warnings and not report["http_attempts"], "Validation emitted warnings or attempted HTTP")
    finally:
        gui.errors.clear()
        await gui.shutdown()
        app_settings._settings, app_settings._custom_settings = previous
        report["pass"] = len(report["results"])
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(f"{report['pass']} source validation checks passed; {report['http_attempts']} HTTP attempts")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", action="append", help="Focus one or more supported providers")
    parser.add_argument("--kind", choices=("model", "playlist"))
    parser.add_argument("--source", action="append", default=[], metavar="PROVIDER.KIND=URL", help="Override a public source fixture")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--offline-only", action="store_true", help="Actual source validation controls; HTTP is rejected")
    parser.add_argument("--timeout", type=float, default=600, help="Maximum seconds per source workflow")
    parser.add_argument("--report", type=Path, default=Path(tempfile.gettempdir()) / "porn-fetch-collections.json")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("Timeout must be positive")
    try:
        overrides = dict(value.split("=", 1) for value in args.source)
        inventory = collection_cases(overrides)
    except ValueError as error:
        parser.error(str(error))
    unknown = set(args.provider or ()) - {case["provider"] for case in inventory}
    if unknown:
        parser.error("Unsupported source providers: " + ", ".join(sorted(unknown)))
    args.cases = [case for case in inventory
                  if (not args.provider or case["provider"] in args.provider) and (not args.kind or case["kind"] == args.kind)]
    if not args.cases:
        parser.error("No matching supported model/playlist sources")
    if args.list:
        for case in args.cases:
            print(case["status"], case["id"], case["url"] or case["reason"])
        return 0
    args.report = args.report.resolve()
    if not args.offline_only and not any(case["status"] == "AUTOMATED" for case in args.cases):
        args.report.parent.mkdir(parents=True, exist_ok=True)
        report = {"results": args.cases, "pass": 0, "fail": 0, "blocked": 0,
                  "manual": sum(case["status"] == "MANUAL" for case in args.cases),
                  "unverified": sum(case["status"] == "UNVERIFIED" for case in args.cases)}
        args.report.write_text(json.dumps(report, indent=2) + "\n")
        for case in args.cases:
            print(case["status"], case["id"], case["reason"])
        return 0
    args.ffmpeg = shutil.which("ffmpeg")
    require(args.offline_only or args.ffmpeg, "FFmpeg is required for real collection downloads")
    os.environ["PORN_FETCH_TEST_ENV"] = "1"
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ["QML_DISABLE_DISK_CACHE"] = "1"
    logging.disable(logging.CRITICAL)
    with tempfile.TemporaryDirectory(prefix="porn-fetch-collections-") as temporary:
        directory = Path(temporary)
        for kind in ("CONFIG", "CACHE", "DATA"):
            os.environ[f"XDG_{kind}_HOME"] = str(directory / kind.lower())
        previous = Path.cwd()
        os.chdir(directory)
        try:
            if not args.offline_only:
                from src.database.installer import download_and_extract_pocketbase
                from src.database.service import PocketBaseService
                try:
                    binary = PocketBaseService(directory / "probe").find_binary()
                except Exception:
                    binary = download_and_extract_pocketbase(target_dir=directory / "bin")
                os.environ["PORN_FETCH_POCKETBASE_BINARY"] = str(binary)
            from PySide6.QtGui import QGuiApplication
            from PySide6.QtQuickControls2 import QQuickStyle
            QQuickStyle.setStyle("Material")
            app = QGuiApplication.instance() or QGuiApplication([])
            app.setQuitOnLastWindowClosed(False)
            result = asyncio.run(offline_contract(args, directory) if args.offline_only else run(args, directory))
            app.processEvents()
            return result
        except KeyboardInterrupt:
            print(f"Stopped. Partial report: {args.report}")
            return 130
        finally:
            os.chdir(previous)


if __name__ == "__main__":
    raise SystemExit(main())
