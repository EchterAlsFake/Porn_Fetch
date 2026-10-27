"""Opt-in whole desktop Settings page persistence, runtime and effect checks."""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import tempfile
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

from src.tests.settings_cases import SETTINGS


async def run(args, directory):
    from src.backend.settings_diagnostics import SettingsWindow
    from src.tests.smoke.download_lifecycle import require

    report = {"scope": "Desktop SettingsPage disk persistence, real runtime consumers and observable effects",
              "started_at_utc": datetime.now(timezone.utc).isoformat(),
              "offline_only": args.offline_only, "settings": [], "effects": [], "interrupted": False}
    args.report.parent.mkdir(parents=True, exist_ok=True)

    def save():
        report["persistence_passed"] = sum(row["persistence"] == "PASS" for row in report["settings"])
        report["failed"] = sum(row["persistence"] == "FAIL" for row in report["settings"])
        report["failed"] += sum(effect["status"] == "FAIL" for effect in report["effects"])
        report["failed"] += int(report.get("auxiliary", {}).get("status") == "FAIL")
        report["effects_verified"] = sum(row["effect"] == "PASS" for row in report["settings"])
        report["unverified_settings"] = [row["setting"] for row in report["settings"] if row["effect"] == "UNVERIFIED"]
        report["offline_http_attempts"] = args.blocked_requests
        args.report.write_text(json.dumps(report, indent=2) + "\n")

    gui = SettingsWindow(directory)
    try:
        report["inventory_controls"] = gui.inventory()
        with args.report.with_suffix(".log").open("w") as log:
            for setting in SETTINGS:
                print(f"CHECK {setting.prop}", flush=True)
                record = {"setting": setting.prop, "control": setting.control, "effect_group": setting.group,
                          "persistence": "FAIL", "active_configuration": "NOT_APPLICABLE", "effect": "UNVERIFIED"}
                report["settings"].append(record)
                try:
                    with redirect_stdout(log), redirect_stderr(log):
                        runtime = False
                        for value in setting.values:
                            if setting.kind == "path":
                                value = str(directory / value)
                            gui.activate(setting.prop, value)
                            runtime = gui.verify_runtime(setting, value) or runtime
                            await gui.clients.close_retired_sessions()
                        require(gui.restart.count() > 0 if setting.group in {"sni", "strict", "style", "database"} else True,
                                "Restart-only setting emitted no restart notification")
                    record.update(persistence="PASS", active_configuration="PASS" if runtime else "NOT_APPLICABLE")
                except Exception as error:
                    import traceback
                    traceback.print_exc(file=log)
                    record.update(error_type=type(error).__name__, error=str(error))
                save()
                print(f"{record['persistence']} {setting.prop}" + (f": {record['error']}" if record.get('error') else ""), flush=True)
            if not args.offline_only:
                from src.tests.smoke.settings_effects import run_effects
                await run_effects(gui, args, report, save, log)
            from src.tests.smoke.settings_effects import auxiliary_controls
            try:
                with redirect_stdout(log), redirect_stderr(log):
                    evidence = await auxiliary_controls(gui)
                report["auxiliary"] = {"status": "PASS", "evidence": evidence}
            except Exception as error:
                report["auxiliary"] = {"status": "FAIL", "error": str(error)}
    except asyncio.CancelledError:
        report["interrupted"] = not bool(report.get("blocked"))
        save()
        return 1 if report.get("blocked") else 130
    finally:
        await gui.close()
    save()
    print(f"{report['persistence_passed']}/{len(SETTINGS)} settings persisted; "
          f"{report['effects_verified']}/{len(SETTINGS)} effects verified; {report['failed']} failures. Report: {args.report}")
    return int(bool(report["failed"] or (args.require_all and report["unverified_settings"])))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline-only", action="store_true", help="Check all QML controls, disk and runtime mapping without HTTP requests")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--effect", action="append", help="Focus a named effect group; persistence/runtime checks still cover every setting")
    parser.add_argument("--require-all", action="store_true", help="Fail if any actual effect remains unverified")
    parser.add_argument("--tor", action="store_true", help="Also bootstrap real Tor and verify its routes (metadata only)")
    parser.add_argument("--strict", action="store_true", help="Also verify real privileged Strict SNI profiles")
    parser.add_argument("--report", type=Path, default=Path(tempfile.gettempdir()) / "porn-fetch-settings.json")
    args = parser.parse_args()
    args.blocked_requests = 0
    if args.timeout <= 0:
        parser.error("Timeout must be positive")
    if args.list:
        for setting in SETTINGS:
            print(f"{setting.control}: {setting.key}; runtime={setting.runtime or 'application consumer'}; effect={setting.group}")
        print(f"{len(SETTINGS)} settings. No requests or Qt startup.")
        return 0
    args.report = args.report.resolve()
    os.environ["PORN_FETCH_TEST_ENV"] = "1"
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ["QML_DISABLE_DISK_CACHE"] = "1"
    logging.disable(logging.CRITICAL)
    with tempfile.TemporaryDirectory(prefix="porn-fetch-settings-") as directory:
        os.environ["XDG_CONFIG_HOME"] = str(Path(directory) / "configuration")
        os.environ["XDG_CACHE_HOME"] = str(Path(directory) / "cache")
        os.environ["XDG_DATA_HOME"] = str(Path(directory) / "data")
        # Keep any native diagnostic log files out of the user's working tree.
        original_directory = Path.cwd()
        os.chdir(directory)
        try:
            from PySide6.QtGui import QGuiApplication
            from PySide6.QtQuickControls2 import QQuickStyle
            QQuickStyle.setStyle("Material")
            app = QGuiApplication.instance() or QGuiApplication([])
            with ExitStack() as safety:
                if args.offline_only:
                    from unittest.mock import patch

                    from base_api import BaseCore
                    from curl_cffi.requests import AsyncSession

                    async def forbidden(*params, **options):
                        args.blocked_requests += 1
                        raise AssertionError("HTTP request attempted during offline settings contracts")
                    safety.enter_context(patch.object(BaseCore, "request", forbidden))
                    safety.enter_context(patch.object(AsyncSession, "request", forbidden))
                status = asyncio.run(run(args, Path(directory)))
            app.processEvents()
            return status or int(bool(args.blocked_requests))
        except KeyboardInterrupt:
            print(f"Stopped. Partial report: {args.report}")
            return 130
        finally:
            os.chdir(original_directory)


if __name__ == "__main__":
    raise SystemExit(main())
