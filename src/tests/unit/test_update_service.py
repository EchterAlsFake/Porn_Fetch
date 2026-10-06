"""Unit tests for Qt IFW auto-update integration and maintenance tool orchestration."""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from src.backend.update_service import (
    AutoUpdater,
    CheckUpdates,
    find_maintenance_tool,
)
from src.licensing.client import LicenseStatus
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
            with patch("src.backend.update_service.find_maintenance_tool", return_value=tmp_path):
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

            updater = AutoUpdater(before_update=mock_cleanup, license_status=AsyncMock(return_value=LicenseStatus("valid", True, license_expires_at=RELEASE_TIMESTAMP)))

            with patch("src.backend.update_service.find_maintenance_tool", return_value=tmp_path):
                with patch("subprocess.Popen") as mock_popen:
                    with patch("PySide6.QtCore.QCoreApplication.quit") as mock_quit:
                        with patch.object(CheckUpdates, "check_signed_repository", AsyncMock(return_value={"release_timestamp": RELEASE_TIMESTAMP})), patch.object(updater, "_stage_repository", AsyncMock(return_value=tmp_path.parent)):
                            await updater._run()
                        self.assertTrue(cleanup_called, "Pre-update cleanup hook was not invoked")
                        mock_popen.assert_called_once()
                        self.assertIn("--set-temp-repository", mock_popen.call_args.args[0])
                        mock_quit.assert_called_once()
        finally:
            tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
