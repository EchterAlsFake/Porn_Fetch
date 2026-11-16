"""Opt-in creator scans and native transfers in disposable application state.

python -m src.tests.smoke.creators --pocketbase /path/to/pocketbase [--downloads] [--resume]
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import tempfile
from pathlib import Path


async def run(args, workspace, report, pump):
    from src.backend import clients
    from src.backend.creator_bridge import CreatorBridge
    from src.backend.creator_sources import resolve_subscription
    from src.database.creators import SUBSCRIPTIONS, VIDEOS
    from src.database.tracker import PocketBaseTracker
    from src.shared.creator_library import identity
    from src.tests.smoke.download_gui import DownloadWindow, isolated_settings
    from src.tests.smoke.download_lifecycle import lifecycle_fixtures

    tracker = bridge = window = None

    async def open_session():
        nonlocal tracker, bridge, window
        tracker = PocketBaseTracker(workspace / "db", enabled=False, binary_path=args.pocketbase)
        window = DownloadWindow(args.timeout, premium=not args.free)
        window.backend._library_pending = {}
        bridge = CreatorBridge(window.backend, tracker)
        await bridge.ensure_ready()

    async def close_session():
        if bridge:
            await bridge.stop()
        if window:
            await window.shutdown()
        if bridge:
            await bridge.close()
        if tracker:
            await tracker.close()

    async def wait_video(provider, predicate):
        async with asyncio.timeout(args.timeout):
            while True:
                pump()
                rows = (await bridge.repo.page(VIDEOS, filter=f'provider = "{provider}"'))["items"]
                if rows:
                    row = rows[0]
                    if row["status"] == "failed":
                        raise AssertionError(row["error"])
                    if predicate(row):
                        return row
                await asyncio.sleep(.02)

    with isolated_settings(workspace):
        try:
            await open_session()
            id = await bridge.library.save("", {"url": args.source, "name": "Creator scan check", "folder": str(workspace), "quality": "480"}, resolve_subscription)
            await bridge.library.scan_tasks[id]
            source = await bridge.repo.get(SUBSCRIPTIONS, id)
            assert source["status"] == ("preview" if args.free else "complete"), source["error"]
            count = (await bridge.repo.video_page(id))["totalItems"]
            assert count > 0
            bridge.library.scan(id)
            await bridge.library.scan_tasks[id]
            assert (await bridge.repo.video_page(id))["totalItems"] == count
            if args.free:
                assert count <= 5
            report.append({"check": "preview_scan_and_rescan" if args.free else "full_scan_and_rescan", "status": "PASS", "unique_videos": count})
            print(json.dumps(report[-1]), flush=True)
            if not (args.downloads or args.resume):
                return
            # Clear discovery records so each fixture's state query selects its single transfer.
            await bridge.library.remove(id)
            async for row in bridge.repo.all(VIDEOS):
                await bridge.repo.delete(VIDEOS, row["id"])
            for provider, transport, url in lifecycle_fixtures():
                if provider not in {"bellesa", "redgifs"}:
                    continue
                source = await bridge.repo.create(SUBSCRIPTIONS, {"url": "https://www.bellesa.co/channels/live" if provider == "bellesa" else "https://www.redgifs.com/users/demo",
                    "provider": provider, "name": "Native transfer check", "folder": str(workspace / provider), "quality": "best" if args.free else "480"})
                await bridge.repo.remember_many(source, [{"identity": identity(provider, url), "url": url, "provider": provider, "title": "Native transfer"}], "2026-11-16")
                await bridge.library.queue(source["id"], "download")
                paused = False
                if args.resume:
                    row = await wait_video(provider, lambda v: v["status"] == "completed" or v["progress"] > 0)
                    assert row["status"] != "completed", "Transfer finished before the stop checkpoint could be tested"
                    bridge.bulk(source["id"], "pause")
                    row = await wait_video(provider, lambda v: v["status"] == "paused")
                    previous_job, previous_path = row["job"], row["output_path"]
                    await close_session()
                    await open_session()
                    await bridge.library.queue(source["id"], "download")
                    paused = True
                row = await wait_video(provider, lambda v: v["status"] == "completed")
                if paused:
                    assert (row["job"], row["output_path"]) == (previous_job, previous_path)
                output = Path(row["output_path"])
                if args.free:
                    assert int(row["quality"]) <= 720
                    assert row["snapshot"]["index"] <= 5
                assert output.is_file() and output.stat().st_size > 10000
                from src.shared.ffmpeg import find_ffmpeg
                ffmpeg = str(find_ffmpeg())
                process = await asyncio.create_subprocess_exec(ffmpeg, "-v", "error", "-i", str(output), "-t", "1", "-f", "null", "-",
                    stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE)
                _, stderr = await process.communicate()
                assert process.returncode == 0, stderr.decode(errors="replace")
                report.append({"check": "native_transfer", "provider": provider, "transport": transport, "status": "PASS", "free_preview": args.free, "quality": row["quality"], "close_reopen_resume": paused, "bytes": output.stat().st_size})
                print(json.dumps(report[-1]), flush=True)
        finally:
            await close_session()
            await clients.close_all_clients()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pocketbase", type=Path, required=True)
    parser.add_argument("--source", default="https://www.bellesa.co/channels/zero-to-hero")
    parser.add_argument("--downloads", action="store_true")
    parser.add_argument("--free", action="store_true", help="verify the five-video/720p trial without Premium")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--timeout", type=float, default=240)
    parser.add_argument("--report", type=Path, default=Path(tempfile.gettempdir()) / "pornfetch-creators-live.json")
    args = parser.parse_args()
    os.environ["PORN_FETCH_TEST_ENV"] = "1"
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ.setdefault("QT_QUICK_BACKEND", "software")
    os.environ["QML_DISABLE_DISK_CACHE"] = "1"
    report = []
    try:
        with tempfile.TemporaryDirectory(prefix="creator-live-config-") as settings, tempfile.TemporaryDirectory(prefix="creator-live-") as workspace:
            os.environ["XDG_CONFIG_HOME"] = settings
            from PySide6.QtGui import QGuiApplication
            from PySide6.QtQuickControls2 import QQuickStyle
            QQuickStyle.setStyle("Material")
            app = QGuiApplication.instance() or QGuiApplication([])
            asyncio.run(run(args, Path(workspace), report, app.processEvents))
    except Exception as error:
        report.append({"status": "FAIL", "error": str(error)})
        raise
    finally:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
