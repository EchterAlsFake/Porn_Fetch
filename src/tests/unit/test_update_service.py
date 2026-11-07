"""Unit tests for Qt IFW auto-update integration and maintenance tool orchestration."""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from src.backend.update_service import (
    AutoUpdater,
    CheckUpdates,
    find_maintenance_tool,
)
from src.shared.version import RELEASE_TIMESTAMP


class UpdateServiceTests(unittest.TestCase):
    def test_version_parts_parsing(self):
        self.assertEqual(CheckUpdates._version_parts("3.9.0"), (3, 9))
        self.assertEqual(CheckUpdates._version_parts("3.10.1"), (3, 10, 1))
        self.assertEqual(CheckUpdates._version_parts("v3.9.0"), (3, 9))
        self.assertTrue(CheckUpdates._version_parts("3.10.0") > CheckUpdates._version_parts("3.9.0"))
        self.assertTrue(CheckUpdates._version_parts("3.9.1") > CheckUpdates._version_parts("3.9.0"))
        self.assertFalse(CheckUpdates._version_parts("3.9.0") > CheckUpdates._version_parts("3.9.0"))

    def test_find_maintenance_tool_via_env(self):
        with tempfile.NamedTemporaryFile(suffix=".exe" if sys.platform == "win32" else "", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            if sys.platform != "win32":
                tmp_path.chmod(0o755)
            with patch.dict(os.environ, {"PORNFETCH_MAINTENANCETOOL_PATH": str(tmp_path)}):
                found = find_maintenance_tool()
                self.assertIsNotNone(found)
                self.assertEqual(found, tmp_path.resolve())
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_find_maintenance_tool_missing(self):
        with patch.dict(os.environ, {"PORNFETCH_MAINTENANCETOOL_PATH": "/path/to/nonexistent/maintenancetool"}):
            with patch("src.backend.update_service.get_original_executable_path", return_value=None):
                found = find_maintenance_tool()
                self.assertIsNone(found)

    def test_find_macos_maintenance_tool_beside_app(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            app_executable = target / "Porn Fetch.app" / "Contents" / "MacOS" / "Porn Fetch"
            tool = target / "maintenancetool.app" / "Contents" / "MacOS" / "maintenancetool"
            tool.parent.mkdir(parents=True)
            tool.write_text("tool")
            tool.chmod(0o755)
            with patch("src.backend.update_service.sys.platform", "darwin"):
                with patch("src.backend.update_service.get_original_executable_path", return_value=app_executable):
                    self.assertEqual(find_maintenance_tool(), tool.resolve())


class AsyncUpdateServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_component_manager_stages_current_repository_before_ifw_launch(self):
        shutdown = MagicMock()
        updater = AutoUpdater(request_shutdown=shutdown)
        update = {"version": "3.9"}
        with patch("src.backend.update_service.find_maintenance_tool", return_value=Path("/tool")), \
                patch.object(CheckUpdates, "check_signed_repository", AsyncMock(return_value=update)) as check, \
                patch.object(updater, "_stage_repository", AsyncMock(return_value=Path("/verified"))) as stage, \
                patch("src.backend.update_service.subprocess.Popen") as launch:
            await updater.run("components")
        check.assert_awaited_once_with(include_current=True)
        stage.assert_awaited_once_with(update)
        self.assertEqual(launch.call_args.args[0], [
            "/tool", "--start-package-manager", "--set-temp-repository", Path("/verified").as_uri(), "--no-proxy",
        ])
        shutdown.assert_called_once()

    async def test_component_preparation_failure_never_launches_ifw_or_closes_app(self):
        from src.shared.tor_runtime import TorUnavailable

        shutdown = MagicMock()
        updater = AutoUpdater(request_shutdown=shutdown)
        with patch("src.backend.update_service.find_maintenance_tool", return_value=Path("/tool")), \
                patch.object(CheckUpdates, "check_signed_repository", AsyncMock(side_effect=TorUnavailable("offline"))), \
                patch("src.backend.update_service.subprocess.Popen") as launch:
            await updater.run("components")
        launch.assert_not_called()
        shutdown.assert_not_called()

    async def test_component_discovery_accepts_current_version_but_rejects_older_repository(self):
        release = {"version": "3.9"}
        core = SimpleNamespace(request=AsyncMock(return_value=SimpleNamespace(status_code=200, content=b"signed")))
        with patch("src.backend.update_service.service_core", core), \
                patch("src.backend.update_service.QFile") as resource, \
                patch("src.backend.update_service.ROOT_FILE") as root, \
                patch("src.backend.update_service.__version__", "3.9.0"), \
                patch("src.backend.update_service.verify_repository_manifest", return_value=(object(), release)):
            resource.return_value.exists.return_value = False
            root.read_bytes.return_value = b"root"
            self.assertIsNone(await CheckUpdates.check_signed_repository())
            self.assertEqual((await CheckUpdates.check_signed_repository(include_current=True))["version"], "3.9")
            release["version"] = "3.8"
            with self.assertRaisesRegex(ValueError, "older"):
                await CheckUpdates.check_signed_repository(include_current=True)

    async def test_tor_metadata_errors_report_the_response_without_unsigned_fallback(self):
        from src.shared.service_transport import ServicePolicy, TorServiceFailure

        for status in (302, 404, 502, 200):
            with self.subTest(status=status):
                policy = ServicePolicy(SimpleNamespace(service_transport="tor"))
                core = SimpleNamespace(
                    tor_enabled=True, policy=policy,
                    request=AsyncMock(return_value=SimpleNamespace(
                        status_code=status, content=b"" if status == 502 else b"<html>Not an update manifest</html>",
                        headers={"Content-Type": "text/html"},
                    )),
                )
                with patch("src.backend.update_service.service_core", core), \
                     patch("src.backend.update_service.QFile") as resource, \
                     patch.object(CheckUpdates, "check_via_http", new=AsyncMock()) as fallback, \
                     patch("src.shared.service_transport.failure_listener") as notice:
                    resource.return_value.exists.return_value = False
                    with self.assertRaises(TorServiceFailure) as raised:
                        await CheckUpdates.check()
                self.assertIn("signed update metadata over Tor", str(raised.exception))
                self.assertIn("No direct connection was attempted", str(raised.exception))
                if status != 200:
                    self.assertIn(f"HTTP {status}", str(raised.exception))
                self.assertEqual(notice.call_args.args[0], str(raised.exception))
                fallback.assert_not_awaited()
                core.request.assert_awaited_once()

    async def test_missing_tor_update_failure_preserves_reason_without_stacking_dialogs(self):
        from src.backend.application import Backend
        from src.shared.service_transport import TorServiceFailure
        from src.shared.tor_runtime import TOR_BINARY_MISSING_MESSAGE

        backend = SimpleNamespace(
            _update_check_manual=True, notifications=MagicMock(), logger=MagicMock(),
            updateStatus=MagicMock(), tr=lambda text: text,
        )
        with patch.object(CheckUpdates, "check", AsyncMock(side_effect=TorServiceFailure(TOR_BINARY_MISSING_MESSAGE))):
            await Backend._check_for_updates(backend)
        self.assertEqual(backend.updateStatus.emit.call_args.args[0], TOR_BINARY_MISSING_MESSAGE)
        self.assertEqual(backend.notifications.publish.call_args.args[0], TOR_BINARY_MISSING_MESSAGE)
        self.assertFalse(backend.notifications.publish.call_args.kwargs["direct"])

    async def test_no_update_result_is_direct_only_for_manual_checks(self):
        from src.backend.application import Backend

        for manual in (False, True):
            backend = SimpleNamespace(
                _update_check_manual=manual, notifications=MagicMock(),
                updateStatus=MagicMock(), tr=lambda text: text,
            )
            with patch.object(CheckUpdates, "check", AsyncMock(return_value=None)):
                await Backend._check_for_updates(backend)
            if manual:
                self.assertTrue(backend.notifications.publish.call_args.kwargs["direct"])
            else:
                backend.notifications.publish.assert_not_called()
            self.assertFalse(backend._update_check_manual)

    async def test_update_uses_normal_shutdown_only_after_successful_launch(self):
        shutdown = MagicMock()
        updater = AutoUpdater(request_shutdown=shutdown)
        with patch("src.backend.update_service.find_maintenance_tool", return_value=Path("/tool")), \
             patch.object(CheckUpdates, "check_signed_repository", AsyncMock(return_value={})), \
             patch.object(updater, "_stage_repository", AsyncMock(return_value=Path("/verified"))), \
             patch("subprocess.Popen", side_effect=OSError("could not launch")) as launch, \
             patch("src.backend.update_service.QCoreApplication.quit") as quit_app:
            await updater.run()
            shutdown.assert_not_called()
            quit_app.assert_not_called()
            launch.side_effect = None
            await updater.run()
            shutdown.assert_called_once()
            quit_app.assert_not_called()

    async def test_missing_maintenance_tool_finishes_without_starting_installation(self):
        updater = AutoUpdater()
        finished = []
        updater.finished.connect(lambda: finished.append(True))
        with (
            patch("src.backend.update_service.find_maintenance_tool", return_value=None),
            patch("subprocess.Popen") as launch,
        ):
            await updater.run()
        launch.assert_not_called()
        self.assertEqual(finished, [True])

    async def test_signed_updates_are_offered_without_license_bridge(self):
        from src.backend.application import Backend

        backend = SimpleNamespace(
            _license_bridge=None, updateAvailable=MagicMock(), updateStatus=MagicMock(), logger=MagicMock(),
            _update_check_manual=False, notifications=MagicMock(), tr=lambda text: text,
        )
        for source in ("signed_repository", "signed_android", "http"):
            with self.subTest(source=source), patch("src.backend.application.IS_SOURCE_RUN", False), \
                 patch("src.backend.application.find_maintenance_tool", return_value=Path("/tool")), \
                 patch.object(CheckUpdates, "check", AsyncMock(return_value={
                "source": source, "version": "3.10", "release_timestamp": RELEASE_TIMESTAMP,
            })):
                await Backend._check_for_updates(backend)
                details = backend.updateAvailable.emit.call_args.args[0]
                self.assertTrue(details["automatic"])
                self.assertEqual(backend.notifications.publish.call_args.kwargs["action"], "updates")
                Backend.review_update(backend)
                self.assertFalse(backend.updateAvailable.emit.call_args.args[0]["automatic"])
                self.assertEqual(details["install_allowed"], source != "http")
                if source == "signed_repository":
                    self.assertIn("save download progress", details["entitlement_message"])

    async def test_android_updater_without_license_requests_install(self):
        updater = AutoUpdater()
        with (
            patch("src.shared.android_updates.is_android_device", return_value=True),
            patch("src.shared.android_updates.download_and_request_install") as install,
            patch("src.licensing.service.create_license_service", side_effect=AssertionError("Updates must not contact licensing")),
        ):
            await updater._run()
            install.assert_called_once()
            self.assertIs(install.call_args.args[-1], updater._android_cancel)

    async def test_check_via_maintenancetool_with_updates(self):
        xml_output = (
            b"<updates>\n"
            b'  <update name="Porn Fetch Core Application" version="3.10.0" size="12345678"/>\n'
            b"</updates>\n"
        )
        with tempfile.NamedTemporaryFile(suffix=".exe" if sys.platform == "win32" else "", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            if sys.platform != "win32":
                tmp_path.chmod(0o755)
            with patch("src.backend.update_service.find_maintenance_tool", return_value=tmp_path), \
                 patch("src.backend.update_service.service_core", SimpleNamespace(tor_enabled=False)):
                mock_proc = AsyncMock()
                mock_proc.communicate.return_value = (xml_output, b"")
                with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
                    result = await CheckUpdates.check_via_maintenancetool()
                    self.assertIsNotNone(result)
                    self.assertEqual(result["version"], "3.10.0")
                    self.assertEqual(result["name"], "Porn Fetch Core Application")
                    self.assertEqual(result["source"], "maintenancetool")
        finally:
            tmp_path.unlink(missing_ok=True)

    async def test_auto_updater_runs_cleanup_and_spawns(self):
        with tempfile.NamedTemporaryFile(suffix=".exe" if sys.platform == "win32" else "", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            if sys.platform != "win32":
                tmp_path.chmod(0o755)

            cleanup_called = False

            async def mock_cleanup():
                nonlocal cleanup_called
                cleanup_called = True

            updater = AutoUpdater(before_update=mock_cleanup)

            with patch("src.backend.update_service.find_maintenance_tool", return_value=tmp_path):
                with patch("subprocess.Popen") as mock_popen:
                    with patch("PySide6.QtCore.QCoreApplication.quit") as mock_quit:
                        with patch.object(CheckUpdates, "check_signed_repository", AsyncMock(return_value={"release_timestamp": RELEASE_TIMESTAMP})), patch.object(updater, "_stage_repository", AsyncMock(return_value=tmp_path.parent)):
                            await updater._run()
                        self.assertTrue(cleanup_called, "Pre-update cleanup hook was not invoked")
                        mock_popen.assert_called_once()
                        self.assertEqual(mock_popen.call_args.args[0], [
                            str(tmp_path), "--updater", "--set-temp-repository", tmp_path.parent.as_uri(),
                            "--no-proxy",
                        ])
                        mock_quit.assert_called_once()
        finally:
            tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()


class MaintenanceAndCleanupTests(unittest.TestCase):
    def test_maintenance_opens_interactive_mode_with_space_in_path(self):
        from src.backend.update_service import launch_maintenance_tool

        tool = Path("/some folder/maintenancetool")
        with tempfile.TemporaryDirectory() as directory, \
                patch("src.backend.update_service.shared_data_dir", return_value=Path(directory)), \
                patch("src.backend.update_service.subprocess.Popen") as launch:
            launch_maintenance_tool(tool, "uninstall")
            command = launch.call_args.args[0]
            self.assertEqual(command[:3], [str(tool), "--start-uninstaller", "--set-temp-repository"])
            self.assertTrue(command[3].startswith("file:"))
            self.assertEqual(command[4], "--no-proxy")
            self.assertEqual(len(list(Path(directory).rglob("Updates.xml"))), 1)
        self.assertEqual(launch.call_args.kwargs["cwd"], str(tool.parent))

    def test_active_cleanup_waits_for_confirmation_but_acceptance_clears(self):
        from src.backend.application import Backend

        backend = SimpleNamespace(
            _download_tasks={1: SimpleNamespace(done=lambda: False)},
            notifications=MagicMock(), tr=lambda text: text, _clear_temporary_files=MagicMock(),
        )
        Backend.clear_temporary_files(backend)
        backend._clear_temporary_files.assert_not_called()
        self.assertEqual(backend.notifications.request_decision.call_args.args[0], "clear-temporary-files")
        Backend._accept_decision(backend, "clear-temporary-files")
        backend._clear_temporary_files.assert_called_once()

    def test_idle_cleanup_does_not_prompt(self):
        from src.backend.application import Backend

        backend = SimpleNamespace(_download_tasks={}, notifications=MagicMock(), _clear_temporary_files=MagicMock())
        Backend.clear_temporary_files(backend)
        backend.notifications.request_decision.assert_not_called()
        backend._clear_temporary_files.assert_called_once()

    def test_failed_maintenance_launch_keeps_app_open(self):
        from src.backend.application import Backend

        backend = SimpleNamespace(notifications=MagicMock(), logger=MagicMock(), tr=lambda text: text,
                                  initiate_shutdown=MagicMock(), _auto_update_task=None)
        with patch("src.backend.application.find_maintenance_tool", return_value=Path("/tool")), \
             patch("src.backend.application.launch_maintenance_tool", side_effect=OSError("failed")):
            Backend._accept_decision(backend, "maintenance-uninstall")
        backend.initiate_shutdown.assert_not_called()
        self.assertEqual(backend.notifications.publish.call_args.kwargs["severity"], "error")
