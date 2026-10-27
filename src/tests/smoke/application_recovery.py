"""Real desktop close/reopen workflows, supervised across independent processes."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import logging
import os
import re
import shutil
import signal
import sys
import tempfile
import traceback
from contextlib import ExitStack
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import patch

from src.tests.smoke.download_lifecycle import lifecycle_fixtures, public_url, require, validate_media

if TYPE_CHECKING:
    from src.database.bridge import DatabaseBridge
    from src.database.client import PocketBaseClient
    from src.tests.smoke.download_gui import DownloadWindow

CASES = ("idle", "preparation", "database-write", "database-move", "hls-retain", "hls-cleanup", "raw-retain", "raw-cleanup")


def write_result(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def cleanup_owned_processes(result):
    for pid in result.get("child_pids", []):
        try:
            os.kill(pid, 0)
        except OSError:
            continue
        result.update(passed=False, error="Application left an owned PocketBase process running")
        os.kill(pid, signal.SIGTERM)


class NetworkEvidence:
    """Only observe/delegate actual native requests, segments and playlist plans."""
    def __init__(self, clients):
        self.requests, self.segments, self.plans, self.sessions = [], [], [], []
        self.started = asyncio.Event()
        from src.shared.provider_routing import PROVIDER_MODULES
        for core in {clients.client_for(name).core for name in PROVIDER_MODULES} | {clients.core}:
            self.watch(core)

    def watch(self, core):
        session = core.session
        if session is None:
            return
        self.sessions.append(session)
        original = session.request

        async def request(method, url, **options):
            headers = options.get("headers") or {}
            entry = {"method": method, "url": public_url(url), "range": headers.get("Range") or headers.get("range"), "bytes": 0}
            self.requests.append(entry)
            self.started.set()
            response = await original(method, url, **options)
            entry.update(status=response.status_code, content_range=response.headers.get("Content-Range"),
                         content_type=response.headers.get("Content-Type", ""))
            if options.get("stream"):
                iterator = response.aiter_content

                async def content(*args, **kwargs):
                    async for chunk in iterator(*args, **kwargs):
                        entry["bytes"] += len(chunk)
                        yield chunk

                response.aiter_content = content
            else:
                entry["bytes"] = len(response.content)
            return response

        original_segment, original_plan = core.download_segment, core.get_segments

        async def segment(url, *args, **options):
            self.segments.append(public_url(url))
            return await original_segment(url, *args, **options)

        async def plan(*args, **options):
            segments = await original_plan(*args, **options)
            self.plans.append([public_url(url) for url in segments])
            return segments

        session.request, core.download_segment, core.get_segments = request, segment, plan


class RecoveryWorker:
    def __init__(self, args, app, loop):
        self.args, self.app, self.loop = args, app, loop
        self.directory = args.workspace
        self.result = {"case": args.case, "phase": args.phase, "passed": False, "child_pids": []}
        self._gui: DownloadWindow | None = None
        self._db: DatabaseBridge | None = None
        self._evidence: NetworkEvidence | None = None
        self.pending_write_released = False
        self.snapshots = []
        self.stack = ExitStack()

    @property
    def gui(self) -> DownloadWindow:
        assert self._gui is not None, "Application window did not initialize"
        return self._gui

    @property
    def db(self) -> DatabaseBridge:
        assert self._db is not None, "Database bridge did not initialize"
        return self._db

    @property
    def evidence(self) -> NetworkEvidence:
        assert self._evidence is not None, "Native request observation did not initialize"
        return self._evidence

    @property
    def database_client(self) -> PocketBaseClient:
        client = self.db.tracker._client
        assert client is not None, "No real database client"
        return client

    def save(self):
        write_result(self.args.result, self.result)

    async def setup(self):
        from PySide6.QtCore import QSettings
        from PySide6.QtTest import QSignalSpy

        from src.backend import clients
        from src.backend.account_diagnostics import AccountAccessGuard, extend_timeout_for_wait
        from src.backend.config import TEMP_DIRECTORY, app_settings
        from src.database.bridge import DatabaseBridge
        from src.tests.smoke.download_gui import DownloadWindow
        self.clients, self.settings = clients, app_settings
        self.state_directory = Path(TEMP_DIRECTORY).resolve()
        self.result["state_directory"] = str(self.state_directory)
        disk = QSettings(str(self.directory / "settings.ini"), QSettings.Format.IniFormat)
        if self.args.phase == "stop":
            for key, value in {"Video/output_path": str(self.directory / "media"), "Video/result_limit": 2,
                               "Video/pocketbase_data_path": str(self.directory / "history"),
                               "Video/database_path": str(self.directory / "legacy.db"),
                               "Video/track_videos": self.args.case not in {"idle", "preparation"},
                               "Video/write_metadata": False, "Privacy/dns_over_https": False,
                               "Privacy/encrypted_ch": False, "Privacy/service_transport": "direct",
                               "Misc/network_logging": False, "Misc/trust_environment": False,
                               "Performance/download_workers": 1, "Performance/videos_concurrency": 1,
                               "Performance/pages_concurrency": 1, "Performance/timeout": 20,
                               "Performance/retries": 2}.items():
                disk.setValue(key, value)
        disk.setValue("Performance/speed_limit", self.args.bandwidth if self.args.phase == "stop" else 0)
        app_settings.set_settings_storage(disk)
        self._gui = DownloadWindow(self.args.timeout, application_close=True)
        def popup_error(text="", *args, **kwargs):
            self.result.setdefault("notifications", []).append(str(text))
            self.gui.errors.append(str(text))
        # Observe genuine GUI notifications without a modal dialog blocking the
        # unattended worker's shutdown/deadline handling.
        self.stack.enter_context(patch("src.backend.application.ui_popup", popup_error))
        backend = self.gui.backend
        backend._proxy_test_task = None
        backend._pending_pocketbase_move = None
        backend._shutdown_task = None
        backend.load_clients()
        backend.bind_download_recovery()
        self.shutdown = QSignalSpy(backend.shutdown_complete)
        self._evidence = NetworkEvidence(clients)
        self.guard = self.stack.enter_context(AccountAccessGuard(
            on_wait=lambda seconds: extend_timeout_for_wait(self.gui.active_timeout, seconds)))
        self.gui.check_access = self.guard.raise_if_blocked
        self._db = DatabaseBridge(parent=self.gui.engine)
        backend.bind_database_bridge(self.db)
        if self.args.case == "database-write":
            import secrets
            original_password = secrets.token_urlsafe
            self.stack.enter_context(patch("src.database.service.secrets.token_urlsafe",
                                           lambda size: "-" + original_password(size)))
            self.result["leading_dash_password_tested"] = True
        self.db.start()
        await self.gui.wait(lambda: not self.db.busy, "Database startup did not settle")
        if self.db.tracker.is_running:
            service = self.db.tracker._service
            assert service is not None and service.process is not None
            self.result["child_pids"].append(service.process.pid)
        self.result["queue_restored_without_provider_requests"] = not self.evidence.requests
        self.save()

    def close(self):
        backend = self.gui.backend
        self.gui.window.close()
        task = backend._shutdown_task
        require(task is not None and backend._is_shutting_down, "Native window close did not begin actual teardown")
        self.gui.window.close()
        require(backend._shutdown_task is task, "Repeated close started a second teardown")

    async def scenario(self):
        await self.setup()
        if self.args.phase == "stop":
            await self.stop_phase()
        else:
            await self.resume_phase()
        self.close()

    async def stop_phase(self):
        gui, backend = self.gui, self.gui.backend
        case = self.args.case
        fixtures = {provider: url for provider, _, url in lifecycle_fixtures()}
        if case == "idle":
            return
        if case == "preparation":
            gui.control("videoUrlInput").setProperty("text", fixtures["eporner"])
            gui.click("getVideoButton")
            await self.evidence.started.wait()
            task = backend._video_fetch_task
            require(task is not None and not task.done() and backend.busy, "No live preparation was active at close")
            self.result["preparation_was_active"] = True
            return
        if case == "database-write":
            from src.database.client import PocketBaseClient
            from src.database.constants import VIDEO_COLLECTION
            entered, release = asyncio.Event(), asyncio.Event()
            original = PocketBaseClient.request

            async def observed(client, method, path, *args, **options):
                if method in {"POST", "PATCH"} and f"/{VIDEO_COLLECTION}/" in path:
                    entered.set()
                    await release.wait()  # Timing only; the native request is still executed unchanged.
                return await original(client, method, path, *args, **options)

            self.stack.enter_context(patch.object(PocketBaseClient, "request", observed))
            job, video = await gui.load(fixtures["pornhub"], None, filename="history-write.mp4")
            await entered.wait()
            require(self.db.busy, "No genuine history write was pending")

            async def release_after_close():
                while not backend._is_shutting_down:
                    await asyncio.sleep(.01)
                await asyncio.sleep(.3)
                release.set()
                self.pending_write_released = True

            self.loop.create_task(release_after_close(), name="release-history-write")
            self.result["history_url"] = video.url
            self.result["history_write_pending_at_close"] = True
            return
        if case == "database-move":
            job, video = await gui.load(fixtures["pornhub"], None, filename="history-move.mp4")
            await gui.wait(lambda: not self.db.busy, "Initial history did not save")
            old, new = self.settings.pocketbase_data_path, str(self.directory / "moved-history")
            # Capture the notification only; use the actual move-request handler.
            self.stack.enter_context(patch("src.backend.application.ui_popup", lambda *args, **kwargs: None))
            backend.pocketbase_data_changed(old, new)
            self.settings.pocketbase_data_path = new
            self.result["history_url"] = video.url
            self.result["old_database_path"] = old
            return
        provider = "pornhub" if case.startswith("hls") else "eporner"
        other = "eporner" if provider == "pornhub" else "pornhub"
        cleanup = case.endswith("cleanup")
        job, video = await gui.load(fixtures[provider], None, filename="active.mp4")
        queued, queued_video = await gui.load(fixtures[other], None, append=True, filename="queued.mp4")
        gui.set_cleanup(cleanup)
        gui.click("downloadSelectAllButton")
        gui.click("downloadSelectedButton")
        model = backend._downloads_model
        await gui.wait(lambda: 1 <= gui.control("downloadRow", job).property("progress") < 90,
                       "No genuine partial media progress before close")
        assert queued_video.output_path is not None
        require(model.get_status(queued) == "queued" and not queued_video.output_path.exists(), "Queued job started writing")
        self.result.update(job=job, queued_job=queued, video_url=video.url, output=str(video.output_path),
                           minutes=video.length, cleanup=cleanup, queued_output=str(queued_video.output_path))
        self.save()

    async def resume_phase(self):
        from src.database.constants import VIDEO_COLLECTION
        from src.tests.smoke.download_gui import artifacts
        prior = json.loads((self.directory / "stop.json").read_text())
        gui, backend, model = self.gui, self.gui.backend, self.gui.backend._downloads_model
        require(self.result["queue_restored_without_provider_requests"], "Reopening automatically contacted a provider")
        if self.args.case in {"idle", "preparation"}:
            require(not backend._download_tasks and not backend.busy, "Fresh process resumed work automatically")
            return
        history = await self.database_client.list_records(VIDEO_COLLECTION)
        if self.args.case in {"database-write", "database-move"}:
            require(any(row["url"] == prior["history_url"] for row in history), "History write/move did not survive exit")
            if self.args.case == "database-move":
                require(not Path(prior["old_database_path"]).exists(), "Old database folder was not moved")
            require(model.rowCount() == 1 and model.get_status(model.data(model.index(0, 0), model.JobIdRole)) == "cancelled",
                    "Prepared history row did not return paused")
            self.result["history_persisted"] = True
            return
        require(model.rowCount() == 2 and not backend._download_tasks, "Interrupted and queued rows did not restore paused")
        for job in (prior["job"], prior["queued_job"]):
            restored = model.get_video(job)
            assert restored is not None
            require(model.get_status(job) == "cancelled" and restored.source_video is None,
                    "Restored row was not paused with a fresh provider lookup deferred")
            await gui.wait(lambda: bool(gui.controls("downloadRow", job)), "Restored delegate did not render")
            require(gui.control("downloadStopResumeButton", job).isEnabled(), "Restored row offers no Resume action")
        video = model.get_video(prior["job"])
        assert video is not None and video.output_path is not None
        gui.click("downloadRemoveButton", prior["queued_job"])
        self.evidence.requests.clear()
        gui.click("downloadStopResumeButton", prior["job"])
        require(prior["job"] in backend._download_tasks, "Restored Resume control did not create a real download task")
        await gui.wait(lambda: not backend._download_tasks, "Resume in the fresh process did not complete")
        require(video.status == "completed" and model.rowCount() == 0, "Resumed row failed or did not clear")
        require(not Path(prior["queued_output"]).exists(), "Unselected queued row started on reopen")
        if self.args.case.startswith("hls"):
            require(self.evidence.segments, "Resume made no real HLS segment requests")
            plan = self.evidence.plans[-1] if self.evidence.plans else prior.get("checkpoint_segments", [])
            require(plan, "No native playlist/checkpoint segment plan was observed")
            fetched = set(self.evidence.segments)
            if prior["cleanup"]:
                require(set(plan) <= fetched, "Cleanup restart did not fetch every HLS segment")
            else:
                kept = prior["retained_indices"]
                require(kept and all(plan[index] not in fetched for index in kept), "Resume fetched retained HLS segments again")
                self.result["segments_reused"] = len(kept)
        else:
            requests = [row for row in self.evidence.requests if row["bytes"] and (row["range"] or "video/" in row.get("content_type", ""))]
            require(requests, "RAW resume transferred no real media")
            first = requests[0]
            start = re.fullmatch(r"bytes=(\d+)-(\d*)", first["range"] or "bytes=0-")
            assert start is not None, "Invalid RAW Range"
            if prior["cleanup"]:
                require(int(start[1]) == 0, "Cleanup restart did not begin at byte zero")
            else:
                served = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)", first.get("content_range") or "")
                require(int(start[1]) >= prior["retained_bytes"] and first["status"] == 206 and served is not None
                        and int(served[1]) == int(start[1]), "RAW resume did not confirm checkpoint reuse with HTTP 206")
                with video.output_path.open("rb") as stream:
                    require(hashlib.sha256(stream.read(prior["prefix_length"])).hexdigest() == prior["prefix_sha256"],
                            "RAW resume changed retained bytes")
                self.result["bytes_reused"] = prior["retained_bytes"]
        probe = await validate_media(video.output_path, shutil.which("ffmpeg"), video.length)
        require(artifacts(self.state_directory, video, prior["job"]) == [video.output_path], "Completion left checkpoint artifacts")
        self.result.update(media=probe, fresh_provider_lookup=True)
        await gui.wait(lambda: not self.db.busy, "Final history update did not settle")
        history = await self.database_client.list_records(VIDEO_COLLECTION)
        require(len([row for row in history if row["url"] == video.url and row["status"] == "completed"]) == 1,
                "Recovered completion did not update its unique history record")

    async def qt_pump(self):
        while True:
            self.app.processEvents()
            await asyncio.sleep(.01)

    async def supervise(self):
        try:
            await asyncio.wait_for(self.scenario(), self.args.timeout)
        except BaseException as error:
            self.result.update(error_type=type(error).__name__, error=str(error), traceback=traceback.format_exc())
            if self._gui is not None and not self.gui.backend._is_shutting_down:
                self.gui.backend.initiate_shutdown()
            else:
                self.loop.stop()

    async def finish(self):
        from base_api.modules.static_functions import segment_file_path

        from src.shared.download_recovery import read_queue
        from src.tests.smoke.download_gui import artifacts
        backend = self.gui.backend
        assert backend._shutdown_task is not None, "No actual teardown task"
        await backend._shutdown_task
        require(self.shutdown.count() == 1, "Shutdown completion did not fire exactly once")
        require(not self.gui.window.isVisible(), "Native window remained open")
        require(not backend._background_tasks and not backend._download_tasks, "Application tasks survived teardown")
        require(all(session._closed for session in self.evidence.sessions), "Native network sessions survived teardown")
        require(not self.db.tracker.is_running, "PocketBase survived teardown")
        if self.args.case == "database-write" and self.args.phase == "stop":
            require(self.pending_write_released, "Shutdown cancelled the pending history write instead of flushing it")
        saved = read_queue(self.state_directory / "download-queue.json")
        if self.args.phase == "stop" and "job" in self.result:
            job = self.result["job"]
            video = next(video for video, _ in saved if video.identifier == job)
            require(len(saved) == 2 and not Path(self.result["queued_output"]).exists(), "Queued job was not stopped/persisted")
            if self.result["cleanup"]:
                require(not artifacts(self.state_directory, video, job), "Shutdown cleanup retained partial artifacts")
                self.result["cleanup_verified"] = True
            elif self.args.case.startswith("hls"):
                checkpoint = self.state_directory / "states" / job
                payload = json.loads(checkpoint.read_text())
                segment_dir = self.state_directory / "segments" / job
                retained = [index for index in range(len(payload["segments"]))
                            if (path := Path(segment_file_path(segment_dir, index, payload["segment_index_width"]))).is_file()
                            and path.stat().st_size]
                require(0 < len(retained) < len(payload["segments"]), "No real partial HLS checkpoint survived")
                self.result["retained_indices"] = retained
                self.result["checkpoint_segments"] = [public_url(url) for url in payload["segments"]]
            else:
                output = Path(self.result["output"])
                payload = json.loads(Path(f"{output}.raw-state.json").read_text())
                kept = sum(payload["progress"])
                require(0 < kept < payload["size"], "No real partial RAW checkpoint survived")
                with output.open("rb") as stream:
                    prefix = stream.read(min(65536, kept))
                self.result.update(retained_bytes=kept, prefix_length=len(prefix), prefix_sha256=hashlib.sha256(prefix).hexdigest())
        if self.args.phase == "resume" and self.args.case.startswith(("hls", "raw")):
            require(not saved, "Completed/removed rows remained in the queue snapshot")
        self.result.update(shutdown_once=True, network_closed=True, database_stopped=True,
                           queue_rows=len(saved), requests=self.evidence.requests)
        self.result["passed"] = "error" not in self.result
        await self.gui.shutdown()


def worker(args):
    args.workspace.mkdir(parents=True, exist_ok=True)
    working_directory = args.workspace if args.phase == "stop" else args.workspace / "different-working-directory"
    working_directory.mkdir(exist_ok=True)
    os.chdir(working_directory)
    for kind in ("CONFIG", "DATA", "CACHE"):
        os.environ[f"XDG_{kind}_HOME"] = str(args.workspace / kind.lower())
    os.environ["PORN_FETCH_TEST_ENV"] = "1"
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ["QML_DISABLE_DISK_CACHE"] = "1"
    logging.disable(logging.CRITICAL)
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtQuickControls2 import QQuickStyle
    QQuickStyle.setStyle("Material")
    app = QGuiApplication([])
    app.setQuitOnLastWindowClosed(False)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    instance = RecoveryWorker(args, app, loop)
    def interrupted():
        instance.result.update(passed=False, error="Interrupted by supervisor")
        if instance._gui is not None:
            instance.gui.backend.initiate_shutdown()
        else:
            loop.stop()
    for signum in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(signum, interrupted)
        except (NotImplementedError, RuntimeError):
            pass
    pump = loop.create_task(instance.qt_pump(), name="recovery-qt-pump")
    loop.create_task(instance.supervise(), name="recovery-scenario")
    safety = ExitStack()
    if args.case == "idle":
        from base_api import BaseCore
        from curl_cffi.requests import AsyncSession

        async def forbidden(*params, **options):
            raise AssertionError("Idle teardown attempted HTTP")
        safety.enter_context(patch.object(BaseCore, "request", forbidden))
        safety.enter_context(patch.object(AsyncSession, "request", forbidden))
    try:
        loop.run_forever()  # The production teardown stops this actual event loop.
        loop.run_until_complete(instance.finish())
    except BaseException as error:
        instance.result["passed"] = False
        if "error" in instance.result:
            instance.result["teardown_verification_error"] = str(error)
        else:
            instance.result.update(error_type=type(error).__name__, error=str(error), traceback=traceback.format_exc())
    finally:
        if instance._evidence is not None:
            instance.result.update(requests=instance.evidence.requests, segment_requests=instance.evidence.segments,
                                   segment_plans=instance.evidence.plans)
        pump.cancel()
        pending = asyncio.all_tasks(loop)
        instance.result["remaining_tasks"] = [task.get_name() for task in pending if task is not pump]
        if instance.result["remaining_tasks"]:
            instance.result.update(passed=False, error="Tasks remained after application teardown")
        for task in pending:
            task.cancel()
        if pending:
            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.run_until_complete(loop.shutdown_default_executor())
        instance.stack.close()
        safety.close()
        loop.close()
        instance.save()
    return int(not instance.result["passed"])


async def run(args, workspace):
    selected = ("idle",) if args.offline_only else tuple(args.case or CASES)
    report = {"scope": "Actual desktop close/reopen in independent processes", "results": []}
    root = Path(__file__).resolve().parents[3]
    environment = os.environ.copy()
    if any(case not in {"idle", "preparation"} for case in selected):
        from src.database.installer import download_and_extract_pocketbase
        from src.database.service import PocketBaseService
        try:
            binary = PocketBaseService(workspace / "probe").find_binary()
        except Exception:
            binary = await asyncio.to_thread(download_and_extract_pocketbase, target_dir=workspace / "bin")
        environment["PORN_FETCH_POCKETBASE_BINARY"] = str(binary)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    for case in selected:
        item = {"case": case, "passed": False, "phases": []}
        report["results"].append(item)
        directory = workspace / case
        directory.mkdir()
        for phase in ("stop", "resume"):
            print(f"RUN {case} {phase}", flush=True)
            result_path = directory / f"{phase}.json"
            process = await asyncio.create_subprocess_exec(
                sys.executable, "-m", "src.tests.smoke.application_recovery", "--worker", "--case", case,
                "--phase", phase, "--workspace", str(directory), "--result", str(result_path),
                "--timeout", str(args.timeout), "--bandwidth", str(args.bandwidth),
                cwd=root, env=environment, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
            )
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), args.timeout + 45)
            except TimeoutError:
                process.kill()
                stdout, stderr = await process.communicate()
            except asyncio.CancelledError:
                if process.returncode is None:
                    process.terminate()
                    try:
                        await asyncio.wait_for(process.wait(), 50)
                    except TimeoutError:
                        process.kill()
                        await process.wait()
                if result_path.exists():
                    cleanup_owned_processes(json.loads(result_path.read_text()))
                raise
            output = args.report.with_name(args.report.stem + f"-{case}-{phase}.log")
            output.write_bytes(stdout + stderr)
            result = json.loads(result_path.read_text()) if result_path.exists() else {"passed": False, "error": "Worker produced no result"}
            item["phases"].append(result)
            cleanup_owned_processes(result)
            if process.returncode or not result["passed"]:
                item["error"] = result.get("error", f"Worker exited {process.returncode}")
                break
        item["passed"] = len(item["phases"]) == 2 and all(phase["passed"] for phase in item["phases"])
        report["passed"] = sum(row["passed"] for row in report["results"])
        report["failed"] = sum(not row["passed"] for row in report["results"])
        write_result(args.report, report)
        print(("PASS " if item["passed"] else "FAIL ") + case + (": " + item["error"][:350] if "error" in item else ""), flush=True)
    print(f"{report['passed']} passed, {report['failed']} failed. Report: {args.report}")
    return int(bool(report["failed"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=CASES, action="append")
    parser.add_argument("--offline-only", action="store_true")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--bandwidth", type=float, default=.5, help="Native media cap before closing; resume is uncapped")
    parser.add_argument("--report", type=Path, default=Path(tempfile.gettempdir()) / "porn-fetch-application-recovery.json")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--phase", choices=("stop", "resume"), help=argparse.SUPPRESS)
    parser.add_argument("--workspace", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--result", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.timeout <= 0 or args.bandwidth <= 0:
        parser.error("Timeout and bandwidth must be positive")
    if args.list:
        print("\n".join(CASES))
        return 0
    if args.worker:
        args.case = args.case[0]
        return worker(args)
    if not args.offline_only and any(case.startswith(("hls", "raw")) for case in (args.case or CASES)):
        require(shutil.which("ffmpeg"), "FFmpeg is required for media recovery checks")
    args.report = args.report.resolve()
    try:
        with tempfile.TemporaryDirectory(prefix="porn-fetch-app-recovery-") as directory:
            return asyncio.run(run(args, Path(directory)))
    except KeyboardInterrupt:
        print(f"Stopped. Partial report: {args.report}")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
