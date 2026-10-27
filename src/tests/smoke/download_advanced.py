"""Desktop advanced controls: real provider metadata/media plus explicit title fixtures."""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import re
import shutil
import tempfile
import traceback
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import AsyncMock, patch

from src.shared.download_options import video_file_path
from src.shared.media import VideoFilters, VideoObject
from src.tests.smoke.download_lifecycle import lifecycle_fixtures, require, validate_media
from src.tests.unit.test_download_options import TITLES

FIELDS = {
    "title_regex": ("downloadTitleRegex", "text", ""), "author_regex": ("downloadAuthorRegex", "text", ""),
    "tags_regex": ("downloadTagsRegex", "text", ""), "duration_minimum": ("downloadMinimumDuration", "value", 0),
    "duration_maximum": ("downloadMaximumDuration", "value", 0), "quality_minimum": ("downloadMinimumQuality", "currentIndex", 0),
    "quality_maximum": ("downloadMaximumQuality", "currentIndex", 0), "published_after": ("downloadAfterDate", "text", ""),
    "published_before": ("downloadBeforeDate", "text", ""), "start_index": ("downloadStartIndex", "value", 0),
    "end_index": ("downloadEndIndex", "value", 0),
}
QUALITIES = ("Any", "144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "4k")
LIVE = ("real-metadata", "real-regexes", "real-numeric-date-filters", "real-combined-filters", "real-gui-submit", "real-video-range", "real-formatted-download")
OFFLINE = ("input-validation", "unusual-title-fixtures", "output-templates", "options-and-shortcuts")


class AdvancedChecks:
    def __init__(self, gui, settings, directory, args):
        from PySide6.QtCore import QObject
        self.gui, self.settings, self.directory, self.args = gui, settings, directory, args
        self.page = gui.window.findChild(QObject, "downloadsPage")
        assert self.page is not None
        self.seeds = []

    def control(self, name):
        from PySide6.QtCore import QObject
        result = self.gui.window.findChild(QObject, name)
        assert result is not None, f"Missing advanced control {name}"
        return result

    def configure(self, values=None, pattern="$index-$title.mp4"):
        values = values or {}
        for key, (name, prop, default) in FIELDS.items():
            value = values.get(key, default)
            if key.startswith("quality_"):
                value = QUALITIES.index(value) if value else 0
            self.control(name).setProperty(prop, value)
        self.control("downloadTitlePattern").setProperty("text", pattern)
        self.gui.pump()

    def filters(self):
        from PySide6.QtQml import QQmlExpression
        expression = QQmlExpression(self.gui.engine.rootContext(), self.page, "getFilters()")
        value, undefined = expression.evaluate()
        require(not undefined and not expression.hasError(), "Production getFilters() failed")
        return value.toVariant() if hasattr(value, "toVariant") else value

    def clear(self):
        model = self.gui.backend._downloads_model
        for row in reversed(range(model.rowCount())):
            self.gui.backend.remove_video(model.data(model.index(row, 0), model.JobIdRole))
        self.gui.pump()
        self.gui.errors.clear()

    async def prepare(self, sources, expected, values=None, pattern="$index-$title.mp4"):
        self.clear()
        self.configure(values, pattern)

        async def stream():
            for source in sources:
                yield source

        # These are actual native provider objects; source loading and the real
        # library caches remain intact. Only the explicit synthetic fixture group
        # below substitutes its metadata loader.
        await self.gui.backend.process_videos(stream(), pattern, VideoFilters(**self.filters()))
        require(not self.gui.errors, f"Advanced processing reported errors: {self.gui.errors}")
        model = self.gui.backend._downloads_model
        require(model.rowCount() == expected, f"Expected {expected} filtered rows, got {model.rowCount()}")
        self.control("downloadListButton").clicked.emit()
        self.gui.pump()
        require(not self.gui.warnings, f"QML warnings: {self.gui.warnings[:2]}")
        return [model.get_video(model.data(model.index(row, 0), model.JobIdRole)) for row in range(model.rowCount())]

    async def metadata(self):
        from src.backend import clients
        from src.cli.selftest.cases import SINGLE_VIDEO_TESTS
        urls = dict(SINGLE_VIDEO_TESTS)
        evidence = []
        for name in ("PornHub", "Eporner", "XVideos"):
            source = await clients.get_video(urls[name])
            video = await clients.load_video_attributes(source)
            require(video.title == str(source.title or "untitled"), "Provider title was sanitized before filtering")
            self.seeds.append((source, video))
            evidence.append({"provider": name, "url": video.url, "title": video.title, "author": video.author,
                             "tags": video.tags, "minutes": video.length, "qualities": video.qualities,
                             "date": video.publish_date.isoformat() if video.publish_date else None})
        return {"data_kind": "real-provider-metadata", "videos": evidence}

    async def evaluate(self, video, accepted, values):
        """Run the production matcher on unchanged, actually fetched metadata.

        Re-fetching a channel page for every regex adds upstream failures without
        improving matcher coverage. Full GUI URL preparation is checked separately.
        """
        from src.backend.video_processor import ProcessVideos
        self.configure(values)
        filters = VideoFilters(**self.filters())
        processor = ProcessVideos(None, "$title", filters, self.gui.backend.download_manager, False, asyncio.Event())
        require(processor.process_filter(filters, video) == accepted, f"Real metadata matched incorrectly: {values}")

    async def regexes(self):
        checks = []
        for source, video in self.seeds:
            fields = {"title_regex": video.title, "author_regex": video.author}
            if video.tags:
                fields["tags_regex"] = video.tags[0]
            for key, actual in fields.items():
                swapped = re.sub(r"[A-Za-z]", lambda match: match[0].swapcase(), actual)
                for expression, accepted in ((r"\A" + re.escape(swapped) + r"\Z", True),
                                              (r"(?!)", False),
                                              (r"(?:never-match-this-alternative|" + re.escape(actual) + ")", True)):
                    await self.evaluate(video, accepted, {key: expression})
                    checks.append({"url": video.url, "filter": key, "regex": expression, "accepted": accepted})
        require(len(checks) >= 18, "Real fixtures did not exercise title/author regex pairs")
        return {"data_kind": "real-provider-metadata", "cases": checks}

    async def numeric_dates(self):
        cases = []
        for source, video in self.seeds:
            if video.length:
                tests = [({"duration_minimum": video.length, "duration_maximum": video.length}, True),
                         ({"duration_minimum": video.length + 1}, False),
                         ({"duration_maximum": video.length - 1}, False)] if video.length > 1 else []
                for values, accepted in tests:
                    await self.evaluate(video, accepted, values)
                    cases.append({"url": video.url, "filters": values, "accepted": accepted})
            highest = max(video.qualities)
            limits = [(label, VideoFilters.quality_value(label)) for label in QUALITIES[1:]]
            lower = max((item for item in limits if item[1] <= highest), key=lambda item: item[1])
            upper = next((item for item in limits if item[1] > highest), None)
            tests = [({"quality_minimum": lower[0]}, True)]
            if upper:
                tests.append(({"quality_minimum": upper[0]}, False))
            below = [item for item in limits if item[1] < highest]
            if below:
                tests.append(({"quality_maximum": below[-1][0]}, False))
            for values, accepted in tests:
                await self.evaluate(video, accepted, values)
                cases.append({"url": video.url, "filters": values, "accepted": accepted})
            if video.publish_date:
                day = video.publish_date.date()
                for values, accepted in (({"published_after": day.isoformat(), "published_before": day.isoformat()}, True),
                                          ({"published_after": (day + timedelta(days=1)).isoformat()}, False),
                                          ({"published_before": (day - timedelta(days=1)).isoformat()}, False)):
                    await self.evaluate(video, accepted, values)
                    cases.append({"url": video.url, "filters": values, "accepted": accepted})
        require(any("published_before" in case["filters"] for case in cases), "No real publication-date fixture was exercised")
        return {"cases": cases, "quality_semantics": "Highest available resolution; 4k means 2160p"}

    async def combined(self):
        source, video = next((source, video) for source, video in self.seeds if video.tags and video.length and video.publish_date)
        values = {"title_regex": re.escape(video.title), "author_regex": re.escape(video.author),
                  "tags_regex": re.escape(video.tags[0]), "duration_minimum": video.length,
                  "published_before": video.publish_date.date().isoformat(), "quality_minimum": "144p"}
        await self.evaluate(video, True, values)
        for key in ("title_regex", "author_regex", "tags_regex"):
            await self.evaluate(video, False, values | {key: "(?!)"})
        return {"url": video.url, "all_conditions_required": True, "cases": 4}

    async def submit(self):
        source, video = self.seeds[1]
        for expression, count in ((re.escape(video.title), 1), ("(?!)", 0)):
            self.clear()
            self.configure({"title_regex": expression})
            self.control("videoUrlInput").setProperty("text", video.url)
            self.gui.click("getVideoButton")
            task = self.gui.backend._video_fetch_task
            require(task is not None, "GUI did not start actual URL preparation")
            await self.gui.wait(task.done, "Real GUI filter request did not finish")
            await task
            require(self.gui.backend._downloads_model.rowCount() == count, "GUI filter was not applied to the real URL")
        return {"real_url_pass_and_reject": True}

    async def ranges(self):
        sources = [source for source, _ in self.seeds]
        self.settings.result_limit = 3
        try:
            rows = await self.prepare(sources, 2, {"start_index": 2, "end_index": 3})
            require([row.url for row in rows] == [video.url for _, video in self.seeds[1:]], "Range selected the wrong videos")
            require([row.index for row in rows] == [2, 3] and [row.output_path.name[:2] for row in rows] == ["02", "03"],
                    "Range lost original fetch positions in filename indexes")
            await self.prepare(sources, 1, {"end_index": 1})
            await self.prepare(sources, 0, {"start_index": 2, "end_index": 3, "title_regex": r"\A" + re.escape(self.seeds[0][1].title) + r"\Z"})
        finally:
            self.settings.result_limit = 1
        return {"inclusive_range": [2, 3], "zero_start": True, "range_before_filter": True}

    async def validation(self):
        cases = [({"title_regex": "["}, "$title"), ({"author_regex": "("}, "$title"),
                 ({"tags_regex": "a{2,1}"}, "$title"), ({"published_after": "2026-02-30"}, "$title"),
                 ({"duration_minimum": 10, "duration_maximum": 5}, "$title"),
                 ({"start_index": 3, "end_index": 2}, "$title"), ({}, "$unknown"), ({}, "${title"), ({}, "../$title")]
        for values, pattern in cases:
            self.clear()
            self.configure(values, pattern)
            self.control("videoUrlInput").setProperty("text", "https://www.eporner.com/video-invalid/unused/")
            self.gui.click("getVideoButton")
            require(self.gui.backend._video_fetch_task is None and not self.gui.backend.busy,
                    "Invalid options started network preparation")
            require(len(self.gui.errors) == 1, "Invalid options did not produce one actionable GUI error")
        self.gui.errors.clear()
        return {"invalid_inputs_rejected_before_fetch": len(cases)}

    async def title_fixtures(self):
        from PySide6.QtQml import QQmlEngine, QQmlExpression

        from src.backend.video_processor import ProcessVideos
        paths = []
        for index, title in enumerate(TITLES, 1):
            metadata = VideoObject(url=f"https://fixture.invalid/{index}", title=title, author="作者 / Studio | A",
                                   video_id=str(index), length=12, tags=["日本語", "literal / | +.*"],
                                   thumbnail_url="", publish_date=datetime(2026, 10, 27, 22, tzinfo=timezone.utc),
                                   qualities=[144, 720, 2160], status="pending")
            with patch.object(ProcessVideos, "process_single_video", AsyncMock(return_value=(object(), metadata))):
                rows = await self.prepare([f"fixture-{index}"], 1,
                                          {"title_regex": r"\A" + re.escape(title) + r"\Z",
                                           "author_regex": re.escape(metadata.author),
                                           "tags_regex": re.escape("literal / | +.*")})
            row = rows[0]
            job = row.identifier
            await self.gui.wait(lambda: bool(self.gui.controls("downloadRow", job)), "Fixture row was not rendered")
            label = self.gui.control("downloadTitleLabel", job)
            require(label.property("text") == "1) " + title, "Rendered title lost its original Unicode/symbols")
            expression = QQmlExpression(QQmlEngine.contextForObject(label), label, "textFormat === Text.PlainText")
            plain, undefined = expression.evaluate()
            require(not undefined and not expression.hasError() and plain, "Title was interpreted as rich text")
            path = video_file_path(row.output_path)
            require(path.parent == Path(self.settings.output_path), "Title metadata created directories or escaped the output folder")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"Explicit synthetic filename fixture, not media")
            require(path.is_file() and row.title == title, "Filename creation modified original metadata")
            paths.append(path.name)
        # Calendar-day inclusivity, 4K boundaries and missing metadata are deterministic here.
        processor = ProcessVideos(None, "$title", VideoFilters(), self.gui.backend.download_manager, False, asyncio.Event())
        require(processor.process_filter(VideoFilters(published_before="2026-10-27", quality_minimum="4k"), metadata),
                "Same-day/4K boundary was rejected")
        require(processor.process_filter(VideoFilters(title_regex="русский", author_regex="émilie", tags_regex="日本語"),
                                         replace(metadata, title="РУССКИЙ タイトル", author="Émilie")),
                "Unicode case-insensitive title/author/tag matching failed")
        for rules, absent in ((VideoFilters(duration_maximum=20), replace(metadata, length=None)),
                              (VideoFilters(published_after="2026-10-01"), replace(metadata, publish_date=None)),
                              (VideoFilters(tags_regex=".*"), replace(metadata, tags=[])),
                              (VideoFilters(quality_maximum="720p"), replace(metadata, qualities=[]))):
            require(not processor.process_filter(rules, absent), "Missing metadata bypassed an active filter")
        return {"data_kind": "synthetic-metadata", "fixtures": len(TITLES), "actual_filenames": paths,
                "no_media_fabricated": True, "missing_metadata_rejected": True}

    async def templates(self):
        from src.backend.video_processor import ProcessVideos
        metadata = VideoObject(url="https://fixture.invalid/template", title="日本語 / Hello | World", author="作者 / Studio",
                               video_id="id/42", length=12, tags=[], thumbnail_url="", publish_date=datetime(2026, 10, 27),
                               qualities=[720], status="pending")
        patterns = ("", "$title", "${title}_$video_id", "$author/$index - $title", "$output_path/$author/$title",
                    "$publish_date-$length-$$-$title", str(self.directory / "explicit" / "$title"))
        paths = []
        for pattern in patterns:
            with patch.object(ProcessVideos, "process_single_video", AsyncMock(return_value=(object(), replace(metadata)))):
                rows = await self.prepare(["fixture"], 1, pattern=pattern)
            path = video_file_path(rows[0].output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"Explicit template fixture")
            require(path.is_relative_to(self.directory), "Template escaped the diagnostic workspace")
            require(not any(c in path.name for c in '/\\|:*?"<>'), "Template left illegal filename characters")
            paths.append(str(path.relative_to(self.directory)))
        return {"data_kind": "synthetic-metadata", "patterns": list(patterns), "actual_paths": paths}

    async def dialogs(self):
        from PySide6.QtCore import QMetaObject
        for button, dialog, phrase in (("downloadTitleOptionsButton", "titleOptionsDialog", "$title"),
                                       ("downloadKeyboardButton", "downloadKeyboardDialog", "Enter")):
            self.control(button).clicked.emit()
            self.gui.pump()
            popup = self.control(dialog)
            require(popup.property("visible") and phrase in popup.property("message"), "Advanced help button did not open its dialog")
            QMetaObject.invokeMethod(popup, "close")
            self.gui.pump()
        return {"formatting_options_and_keyboard_help": True}

    async def download(self):
        self.clear()
        pattern = "日本語 & Grüße/$author/$index - $title | final.mp4"
        self.configure(pattern=pattern)
        url = next(url for provider, _, url in lifecycle_fixtures() if provider == "pornhub")
        job, video = await self.gui.load(url, None, filename=pattern)
        self.gui.click("downloadStartButton", job)
        await self.gui.wait(lambda: not self.gui.backend._download_tasks, "Formatted real download did not finish")
        require(video.status == "completed" and video.output_path.is_relative_to(Path(self.settings.output_path)), "Formatted download failed")
        require("日本語 & Grüße" in video.output_path.parts and "|" not in video.output_path.name, "Formatted path was not applied")
        probe = await validate_media(video.output_path, self.args.ffmpeg, video.length)
        return {"data_kind": "real-provider-media", "filename": video.output_path.name, "probe": probe}


async def run(args, directory):
    from PySide6.QtCore import QSettings

    from src.backend import clients
    from src.backend.account_diagnostics import AccountAccessGuard, extend_timeout_for_wait
    from src.backend.config import app_settings
    from src.tests.smoke.download_gui import DownloadWindow
    old, custom = app_settings._settings, app_settings._custom_settings
    disk = QSettings(str(directory / "settings.ini"), QSettings.Format.IniFormat)
    for key, value in {"Video/output_path": str(directory / "media"), "Video/result_limit": 1,
                       "Privacy/dns_over_https": False, "Privacy/encrypted_ch": False,
                       "Misc/network_logging": False, "Misc/trust_environment": False,
                       "Performance/download_workers": 1, "Performance/videos_concurrency": 1,
                       "Performance/pages_concurrency": 1, "Performance/retries": 2, "Performance/timeout": 25,
                       "Video/write_metadata": False}.items():
        disk.setValue(key, value)
    app_settings.set_settings_storage(disk)
    gui = DownloadWindow(args.timeout)
    gui.backend.load_clients()
    checks = AdvancedChecks(gui, app_settings, directory, args)
    names = OFFLINE if args.offline_only else LIVE + OFFLINE
    operations = dict(zip(LIVE + OFFLINE, (checks.metadata, checks.regexes, checks.numeric_dates, checks.combined,
                                         checks.submit, checks.ranges, checks.download, checks.validation,
                                         checks.title_fixtures, checks.templates, checks.dialogs)))
    report = {"scope": "Desktop advanced controls", "offline_only": args.offline_only,
              "results": [{"check": name, "status": "PENDING"} for name in names]}
    args.report.parent.mkdir(parents=True, exist_ok=True)

    def save():
        report["offline_http_attempts"] = args.http_attempts
        for status in ("PASS", "FAIL", "BLOCKED", "PENDING"):
            report[status.lower()] = sum(row["status"] == status for row in report["results"])
        args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")

    active_timeout = None
    guard = AccountAccessGuard(on_wait=lambda seconds: (extend_timeout_for_wait(active_timeout, seconds), extend_timeout_for_wait(gui.active_timeout, seconds)))
    gui.check_access = guard.raise_if_blocked
    try:
        with args.report.with_suffix(".log").open("w") as log, guard:
            for row in report["results"]:
                print("RUN " + row["check"], flush=True)
                try:
                    with redirect_stdout(log), redirect_stderr(log):
                        active_timeout = asyncio.timeout(args.timeout)
                        async with active_timeout:
                            row["evidence"] = await operations[row["check"]]()
                    row["status"] = "PASS"
                except asyncio.CancelledError:
                    row["status"] = "BLOCKED" if guard.blocked else "INTERRUPTED"
                    row["access_control"] = guard.blocked
                    raise
                except Exception as error:
                    traceback.print_exc(file=log)
                    row.update(status="FAIL", error=str(error), error_type=type(error).__name__)
                    break
                finally:
                    active_timeout = None
                    save()
                    print(row["status"] + " " + row["check"] + (": " + row["error"] if "error" in row else ""), flush=True)
    except asyncio.CancelledError:
        return 1 if guard.blocked else 130
    finally:
        await gui.shutdown()
        await clients.close_all_clients()
        app_settings._settings, app_settings._custom_settings = old, custom
        report["rate_limit_recovery"] = guard.rate_limit_events
        save()
    print(f"{report['pass']} passed, {report['fail']} failed, {report['pending']} not run. Report: {args.report}")
    return int(bool(report["fail"] or report["blocked"] or report["pending"] or args.http_attempts))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--offline-only", action="store_true", help="Explicit synthetic title/validation checks; HTTP is rejected")
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--report", type=Path, default=Path(tempfile.gettempdir()) / "porn-fetch-download-advanced.json")
    args = parser.parse_args()
    args.http_attempts = 0
    if args.list:
        print("\n".join(LIVE + OFFLINE))
        return 0
    if args.timeout <= 0:
        parser.error("Timeout must be positive")
    args.report = args.report.resolve()
    args.ffmpeg = shutil.which("ffmpeg")
    require(args.offline_only or args.ffmpeg, "FFmpeg is required for the real download check")
    os.environ["PORN_FETCH_TEST_ENV"] = "1"
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ["QML_DISABLE_DISK_CACHE"] = "1"
    logging.disable(logging.CRITICAL)
    with tempfile.TemporaryDirectory(prefix="porn-fetch-advanced-") as temporary:
        directory = Path(temporary)
        for key in ("CONFIG", "DATA", "CACHE"):
            os.environ[f"XDG_{key}_HOME"] = str(directory / key.lower())
        previous = Path.cwd()
        os.chdir(directory)
        try:
            from PySide6.QtGui import QGuiApplication
            from PySide6.QtQuickControls2 import QQuickStyle
            QQuickStyle.setStyle("Material")
            app = QGuiApplication.instance() or QGuiApplication([])
            with ExitStack() as safety:
                if args.offline_only:
                    from base_api import BaseCore
                    from curl_cffi.requests import AsyncSession

                    async def forbidden(*params, **options):
                        args.http_attempts += 1
                        raise AssertionError("HTTP attempted during synthetic advanced-control checks")
                    safety.enter_context(patch.object(BaseCore, "request", forbidden))
                    safety.enter_context(patch.object(AsyncSession, "request", forbidden))
                result = asyncio.run(run(args, directory))
            app.processEvents()
            return result
        except KeyboardInterrupt:
            print(f"Stopped. Partial report: {args.report}")
            return 130
        finally:
            os.chdir(previous)


if __name__ == "__main__":
    raise SystemExit(main())
