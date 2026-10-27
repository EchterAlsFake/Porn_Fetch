"""Opt-in desktop queue/concurrency checks using real HLS and RAW downloads.

Run: uv run python -m src.tests.smoke.download_queue
"""
from __future__ import annotations

import argparse
import asyncio
import logging
import os
import shutil
import tempfile
import time
import traceback
from contextlib import AsyncExitStack, ExitStack, redirect_stderr, redirect_stdout
from contextvars import ContextVar
from functools import wraps
from pathlib import Path
from unittest.mock import patch

from src.cli.providers import ClientPool
from src.cli.settings import CliSettings
from src.tests.smoke.download_gui import DownloadWindow, artifacts, isolated_settings, make_report, save_report
from src.tests.smoke.download_lifecycle import ObservedCore, lifecycle_fixtures, media_requests, require, validate_media

CASES = {"parallel-1": 1, "parallel-2": 2, "stop-remove": 2}
REQUEST_JOB = ContextVar("desktop_queue_job", default="prepare")


class QueueCore(ObservedCore):
    """Keep passive request attribution local to each native download task."""

    @property
    def phase(self):
        return REQUEST_JOB.get()

    @phase.setter
    def phase(self, value):
        REQUEST_JOB.set(value)


class NativeDownloads:
    """Observe entry/exit around the unchanged native provider download methods."""

    def __init__(self, videos, limit, errors):
        self.jobs = {id(video.source_video): job for job, video in videos.items()}
        require(len(self.jobs) == len(videos), "Queued rows share a native video instance")
        self.limit, self.errors = limit, errors
        self.active = set()
        self.peak = 0
        self.records = {job: [] for job in videos}
        self.started = time.monotonic()
        self.classes = {type(video.source_video) for video in videos.values()}
        self.stack = ExitStack()

    def __enter__(self):
        for cls in self.classes:
            original = cls.download

            def wrap(original):
                @wraps(original)
                async def observed(source, *args, **kwargs):
                    job = self.jobs[id(source)]
                    token = REQUEST_JOB.set(job)
                    record = {"started_seconds": round(time.monotonic() - self.started, 4)}
                    self.records[job].append(record)
                    self.active.add(job)
                    self.peak = max(self.peak, len(self.active))
                    if len(self.active) > self.limit:
                        self.errors.append("Native download count exceeded the configured parallel limit")
                    try:
                        result = await original(source, *args, **kwargs)
                        record["result"] = getattr(result, "status", str(result))
                        return result
                    except BaseException as error:
                        record["error_type"] = type(error).__name__
                        raise
                    finally:
                        record["finished_seconds"] = round(time.monotonic() - self.started, 4)
                        self.active.discard(job)
                        REQUEST_JOB.reset(token)
                return observed

            self.stack.enter_context(patch.object(cls, "download", wrap(original)))
        return self

    def __exit__(self, *error):
        return self.stack.__exit__(*error)


def queue_jobs(model):
    return [model.data(model.index(i, 0), model.JobIdRole) for i in range(model.rowCount())]


def verify_numbering(gui, videos):
    gui.pump()
    model = gui.backend._downloads_model
    for index, job in enumerate(queue_jobs(model)):
        title = f"{index + 1}) {videos[job].title}"
        require(model.data(model.index(index, 0), model.TitleRole) == title, "Queue model numbering is stale")
        require(gui.control("downloadRow", job).property("title") == title, "Rendered numbering is stale")
        require(gui.control("downloadRow", job).property("jobId") == job, "A row changed its job identity")


def job_requests(pool, job):
    return [entry for core in pool.cores.values() for entry in media_requests(core, job)]


async def check_case(args, case, limit, directory, ffmpeg, result):
    from src.backend import application, clients
    from src.backend.account_diagnostics import AccountAccessGuard, extend_timeout_for_wait

    runtime = CliSettings(download_workers=1, request_attempts=2, timeout=25,
                          videos_concurrency=1, pages_concurrency=1,
                          bandwidth_limit_mb=args.bandwidth, response_cache_mb=0,
                          segment_cache_mb=0).to_runtime_config()
    runtime.ffmpeg_path = str(ffmpeg)
    with isolated_settings(directory):
        gui = DownloadWindow(args.timeout, parallel=limit)
        backend, model = gui.backend, gui.backend._downloads_model
        guard = AccountAccessGuard(on_wait=lambda seconds: extend_timeout_for_wait(gui.active_timeout, seconds))
        gui.check_access = guard.raise_if_blocked
        observer = None
        try:
            async with AsyncExitStack() as lifecycle:
                pool = await lifecycle.enter_async_context(ClientPool(runtime, core_factory=QueueCore))
                lifecycle.push_async_callback(gui.shutdown)
                for provider, _, _ in args.fixtures:
                    pool.client(provider)
                result["requests_by_provider"] = {provider: core.requests for provider, core in pool.cores.items()}
                original_report = application.report_exception

                async def observed_error(error, **options):
                    traceback.print_exception(error)
                    return await original_report(error, **options)

                with (patch.object(clients, "client_for", pool.client),
                      patch.object(application, "report_exception", observed_error), guard):
                    result["stage"] = "prepare"
                    videos = {}
                    # Reuse real resources through separate native objects and
                    # unique output patterns; never fabricate a prepared row.
                    for index, provider in enumerate(("pornhub", "eporner", "pornhub", "eporner")):
                        url = next(url for name, _, url in args.fixtures if name == provider)
                        job, video = await gui.load(url, args.quality, append=True,
                                                    filename=f"queue-{index + 1}.mp4")
                        videos[job] = video
                    a, b, c, d = videos
                    verify_numbering(gui, videos)
                    gui.set_cleanup(True)
                    gui.click("downloadSelectAllButton")
                    require(model.selected_job_ids() == list(videos), "Select All missed rows")
                    gui.click("downloadClearSelectionButton")
                    require(model.selected_job_ids() == [], "Clear Selection left selected rows")
                    selected = list(videos) if case == "stop-remove" else [a, b, c]
                    for job in selected:
                        gui.click("downloadSelectCheck", job)
                    require(model.selected_job_ids() == selected, "Row selection differs from the GUI checkboxes")
                    result["selection_verified"] = True
                    observer = NativeDownloads(videos, limit, gui.errors)
                    with observer:
                        result["stage"] = "start"
                        gui.click("downloadSelectedButton")
                        tasks = dict(backend._download_tasks)
                        require(set(tasks) == set(selected), "Download Selected started the wrong rows")
                        gui.click("downloadSelectedButton")
                        require(backend._download_tasks == tasks, "Repeated start replaced or duplicated tasks")
                        await gui.wait(lambda: len(observer.active) == limit, "Native parallel slots were not filled")
                        queued = [job for job in selected if job not in observer.active]
                        require(len(queued) == len(selected) - limit, "Wrong number of queued jobs")
                        for job in queued:
                            require(model.get_status(job) == "queued" and not observer.records[job]
                                    and not artifacts(directory, videos[job], job),
                                    "A queued job started writing or bypassed the limit")
                            require(not gui.control("downloadStartButton", job).isEnabled(),
                                    "A queued row still permits another per-row start")
                        result["queued_without_transfer_verified"] = True
                        result["duplicate_start_guard_verified"] = True
                        if case == "stop-remove":
                            result["stage"] = "cancel-queued"
                            require(d in queued, "The removal target did not queue")
                            gui.click("downloadRemoveButton", d)
                            await gui.wait(lambda: d not in backend._download_tasks and d not in queue_jobs(model),
                                           "Queued removal waited for unrelated downloads")
                            require(not observer.records[d] and a in observer.active,
                                    "Queued removal started media or waited for the first active job to finish")
                            require(not artifacts(directory, videos[d], d), "Queued removal created partial files")
                            verify_numbering(gui, videos)
                            result["queued_removal_verified"] = True
                            actions = {"stopped": False, "removed": False, "survivor_progress": None}

                            def interrupt(*_):
                                try:
                                    if not actions["stopped"] and model.get_status(b) == "downloading":
                                        progress = gui.control("downloadRow", b).property("progress")
                                        if 1 <= progress < 95:
                                            actions["stopped"] = True
                                            gui.click("downloadStopResumeButton", b)
                                    if (actions["stopped"] and not actions["removed"] and c in observer.active
                                            and model.get_status(a) == "downloading"):
                                        a_progress = gui.control("downloadRow", a).property("progress")
                                        c_progress = gui.control("downloadRow", c).property("progress")
                                        if 1 <= a_progress < 95 and 1 <= c_progress < 95:
                                            actions["removed"] = True
                                            actions["survivor_progress"] = c_progress
                                            gui.click("downloadRemoveButton", a)
                                except Exception as error:
                                    gui.errors.append(str(error))

                            model.dataChanged.connect(interrupt)
                            try:
                                interrupt()
                                result["stage"] = "stop-and-remove-active"
                                await gui.wait(lambda: not backend._download_tasks,
                                               "Stopping/removing jobs stalled the remaining queue")
                            finally:
                                model.dataChanged.disconnect(interrupt)
                            require(actions["stopped"] and actions["removed"],
                                    "The real transfers finished before concurrent stop/removal could be observed")
                            require(videos[b].status == "cancelled" and queue_jobs(model) == [b],
                                    "Stopped row was lost or active/completed removals left incorrect rows")
                            require(videos[c].status == "completed", "The unrelated job did not finish")
                            require(not artifacts(directory, videos[a], a) and not artifacts(directory, videos[b], b),
                                    "Stopped/removed jobs left temporary media with cleanup enabled")
                            require(not observer.records[d], "Removed queued job made a native download call")
                            require(observer.records[c] and job_requests(pool, c), "Surviving job made no real media requests")
                            require(actions["survivor_progress"] < 100, "Surviving job was already complete at removal")
                            verify_numbering(gui, videos)
                            result.update(active_stop_verified=True, active_removal_verified=True,
                                          unrelated_completion_verified=True, cleanup_verified=True)
                            completed = [c]
                            gui.click("downloadRemoveButton", b)
                            require(model.rowCount() == 0, "Removing the stopped row failed")
                        else:
                            result["stage"] = "drain-queue"
                            await gui.wait(lambda: not backend._download_tasks, "Selected downloads did not drain")
                            require(queue_jobs(model) == [d] and model.get_status(d) == "pending",
                                    "An unselected row downloaded or a completed row remained")
                            require(not observer.records[d] and not job_requests(pool, d)
                                    and not artifacts(directory, videos[d], d), "Unselected job made media requests")
                            result["completed_jobs"] = {
                                job: {"status": videos[job].status, "native_calls": len(observer.records[job]),
                                      "media_requests": len(job_requests(pool, job))} for job in selected}
                            require(all(videos[job].status == "completed" and len(observer.records[job]) == 1
                                        and job_requests(pool, job) for job in selected),
                                    "Selected jobs did not complete exactly one native transfer each")
                            verify_numbering(gui, videos)
                            result.update(unselected_untouched_verified=True, automatic_removal_verified=True)
                            completed = selected
                            gui.click("downloadRemoveButton", d)
                            require(model.rowCount() == 0, "Pending survivor could not be removed")
                        require(observer.peak == limit and not observer.active,
                                "Native concurrency did not reach and respect the configured limit")
                        require(all(len(calls) <= 1 for calls in observer.records.values()),
                                "A queued job entered its native downloader more than once")
                        require(not backend._download_stop_events and not backend._download_tasks,
                                "Queue drained but task/stop-event entries remain")
                        result.update(parallel_limit_verified=True, peak_native_downloads=observer.peak,
                                      numbering_verified=True, task_cleanup_verified=True)
                        result["stage"] = "validate"
                        result["media"] = []
                        for job in completed:
                            video = videos[job]
                            result["media"].append(await validate_media(video.output_path, ffmpeg, video.length))
                            require(artifacts(directory, video, job) == [video.output_path],
                                    "Completed queue output retained resume artifacts")
                        require(not gui.errors and not gui.warnings, "Queue produced a GUI error")
                        result["stage"] = "completed"
        finally:
            await gui.shutdown()
            result["access_control"] = guard.blocked
            result["rate_limit_recovery"] = guard.rate_limit_events
            if observer is not None:
                result["native_calls"] = observer.records
                result["peak_native_downloads"] = observer.peak


async def run(args, workspace, ffmpeg):
    from src.backend import clients

    report = make_report(args, workspace)
    report.update(scope="Real desktop multi-video queue, native provider concurrency and media files",
                  planned_cases=len(args.cases), bandwidth_limit_mb=args.bandwidth)
    save_report(report, args.report)
    try:
        with args.report.with_suffix(".log").open("w") as log:
            for case, limit in args.cases:
                print(f"RUN desktop queue {case} (limit {limit})", flush=True)
                directory = workspace / case
                directory.mkdir()
                result = {"case": case, "parallel_limit": limit, "passed": False}
                started = time.monotonic()
                with redirect_stdout(log), redirect_stderr(log):
                    try:
                        await check_case(args, case, limit, directory, ffmpeg, result)
                        result["passed"] = True
                    except asyncio.CancelledError:
                        if result.get("access_control"):
                            result["blocked"] = True
                        else:
                            result["interrupted"] = True
                            report["interrupted"] = True
                    except Exception as error:
                        result.update(error_type=type(error).__name__, error=str(error))
                        traceback.print_exc(file=log)
                result["elapsed_seconds"] = round(time.monotonic() - started, 2)
                report["results"].append(result)
                save_report(report, args.report)
                status = ("PASS" if result["passed"] else "BLOCKED" if result.get("blocked")
                          else "STOP" if result.get("interrupted") else "FAIL")
                print(f"{status} desktop queue {case} [{result.get('stage', 'prepare')}] {result.get('error', '')}", flush=True)
                if not args.keep_artifacts:
                    shutil.rmtree(directory)
                if report["interrupted"] or result.get("blocked"):
                    print(f"Stopped. Partial report: {args.report}", flush=True)
                    return 1 if result.get("blocked") else 130
    finally:
        await clients.close_all_clients()
    print(f"{report['passed']} passed, {report['failed']} failed. Report: {args.report}")
    return int(bool(report["failed"]))


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=("all", *CASES), action="append")
    parser.add_argument("--quality", type=int, help="Exact available resolution at or below 720p")
    parser.add_argument("--bandwidth", type=float, default=1, help="Native per-core HLS bandwidth limit in MiB/s")
    parser.add_argument("--timeout", type=float, default=600, help="Maximum seconds per preparation/download phase")
    parser.add_argument("--report", type=Path, default=Path(tempfile.gettempdir()) / "porn-fetch-download-queue.json")
    parser.add_argument("--artifacts-dir", type=Path)
    parser.add_argument("--keep-artifacts", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args(argv)
    if args.timeout <= 0 or args.bandwidth <= 0 or (args.quality is not None and not 0 < args.quality <= 720):
        parser.error("Timeout/bandwidth must be positive and quality must be between 1 and 720")
    selected = set(args.case or ("all",))
    args.cases = [(case, limit) for case, limit in CASES.items() if "all" in selected or case in selected]
    args.fixtures = [fixture for fixture in lifecycle_fixtures() if fixture[0] in {"pornhub", "eporner"}]
    args.scenarios, args.manual_checks = (), []
    return args


def main():
    args = parse_args()
    if args.list:
        for case, limit in args.cases:
            print(f"desktop queue {case}: limit {limit}, four real rows (PornHub HLS + Eporner RAW)")
        print("No network requests or Qt startup.")
        return 0
    from src.shared.ffmpeg import find_ffmpeg
    ffmpeg = find_ffmpeg()
    if ffmpeg is None:
        raise SystemExit("FFmpeg is required to validate completed queue outputs")
    os.environ["PORN_FETCH_TEST_ENV"] = "1"
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ["QML_DISABLE_DISK_CACHE"] = "1"
    logging.disable(logging.CRITICAL)
    if args.artifacts_dir:
        args.artifacts_dir.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(prefix="porn-fetch-download-queue-", dir=args.artifacts_dir))
    print(f"Live desktop queue: {len(args.cases)} cases. Workspace: {workspace}", flush=True)
    try:
        with tempfile.TemporaryDirectory(prefix="porn-fetch-download-queue-config-") as configuration:
            os.environ["XDG_CONFIG_HOME"] = configuration
            from PySide6.QtGui import QGuiApplication
            from PySide6.QtQuickControls2 import QQuickStyle
            QQuickStyle.setStyle("Material")
            app = QGuiApplication.instance() or QGuiApplication([])
            status = asyncio.run(run(args, workspace, ffmpeg))
            app.processEvents()
            return status
    except KeyboardInterrupt:
        print(f"Stopped. Partial report: {args.report}")
        return 130
    finally:
        if not args.keep_artifacts:
            shutil.rmtree(workspace)


if __name__ == "__main__":
    raise SystemExit(main())
