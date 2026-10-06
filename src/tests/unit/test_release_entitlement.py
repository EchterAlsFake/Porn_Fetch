"""Release signatures, artifact binding, and installer entitlement gates."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from src.backend.update_service import AutoUpdater, CheckUpdates
from src.cli import self_update
from src.licensing.client import LicenseStatus
from src.shared.release import update_eligibility, verify_repository_manifest
from src.shared.version import RELEASE_TIMESTAMP
from src.tests.unit.test_cli_self_update import keys_script, load_script

signer = load_script("sign_desktop_release")


class SignedReleaseTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        (self.repo / "Updates.xml").write_text('<Updates><PackageUpdate><Name>com.echteralsfake.pornfetch</Name><Version>3.10</Version><ReleaseDate>2026-10-06</ReleaseDate></PackageUpdate></Updates>')
        (self.repo / "payload.7z").write_bytes(b"test binary")
        self.root = self.base / "root.json"
        keys_script.initialize(self.base / "keys", self.root)
        signer.sign_repository(self.repo, "linux_amd64", "3.10", self.base / "keys/online.pem", self.root)

    def verify(self):
        return verify_repository_manifest((self.repo / "release.json").read_bytes(), self.root.read_bytes(), "linux_amd64")

    def test_signed_version_release_and_artifact_hashes(self):
        metadata, release = self.verify()
        self.assertEqual(release["release_timestamp"], RELEASE_TIMESTAMP)
        metadata.signed.targets["payload.7z"].verify_length_and_hashes(b"test binary")
        with self.assertRaises(Exception):
            metadata.signed.targets["payload.7z"].verify_length_and_hashes(b"bad binary")

    def test_changed_release_date_and_wrong_root_rejected(self):
        payload = json.loads((self.repo / "release.json").read_text())
        payload["signed"]["release"]["release_timestamp"] -= 86400
        with self.assertRaises(Exception):
            verify_repository_manifest(json.dumps(payload).encode(), self.root.read_bytes(), "linux_amd64")
        other = self.base / "other.json"
        keys_script.initialize(self.base / "other-keys", other)
        with self.assertRaises(Exception):
            verify_repository_manifest((self.repo / "release.json").read_bytes(), other.read_bytes(), "linux_amd64")

    def test_entitled_and_renewal_required_updates(self):
        status = LicenseStatus("valid", True, license_expires_at=RELEASE_TIMESTAMP)
        self.assertTrue(update_eligibility(status, RELEASE_TIMESTAMP)[0])
        allowed, text = update_eligibility(status, RELEASE_TIMESTAMP + 86400)
        self.assertFalse(allowed)
        self.assertIn("Renew", text)
        self.assertIn("06 October 2026", text)

    async def test_qt_stage_verifies_all_bytes_before_launch(self):
        metadata, release = self.verify()
        update = {**release, "metadata": metadata, "repository_url": "https://updates.example/"}
        async def request(url, **kwargs):
            return SimpleNamespace(content=(self.repo / url.rsplit("/", 1)[-1]).read_bytes())
        updater = AutoUpdater()
        with patch("src.backend.update_service.shared_data_dir", return_value=self.base), patch("src.backend.update_service.clients.core.request", side_effect=request):
            stage = await updater._stage_repository(update)
            self.assertEqual((stage / "payload.7z").read_bytes(), b"test binary")
            (self.repo / "payload.7z").write_bytes(b"tampering")
            with self.assertRaises(Exception):
                await updater._stage_repository(update)

    async def test_qt_renewal_required_does_not_download_quit_or_cleanup(self):
        updater = AutoUpdater(before_update=AsyncMock(), license_status=AsyncMock(return_value=LicenseStatus("valid", True, license_expires_at=RELEASE_TIMESTAMP-1)))
        with patch("src.backend.update_service.find_maintenance_tool", return_value=self.base / "tool"), patch.object(CheckUpdates, "check_signed_repository", AsyncMock(return_value={"release_timestamp":RELEASE_TIMESTAMP})), patch.object(updater, "_stage_repository", AsyncMock()) as stage, patch("subprocess.Popen") as launch:
            await updater._run()
            launch.assert_not_called()
            stage.assert_not_called()
            updater.before_update.assert_not_called()

    async def test_unsigned_discovery_never_offers_install(self):
        with patch.object(CheckUpdates,"check_signed_repository", AsyncMock(side_effect=ValueError)), patch.object(CheckUpdates,"check_via_http", AsyncMock(return_value={"version":"4.0"})):
            self.assertFalse((await CheckUpdates.check())["install_allowed"])


class CliEntitlementTests(unittest.TestCase):
    def test_cli_blocks_unentitled_update_before_download(self):
        from unittest.mock import MagicMock
        target = SimpleNamespace(custom={"version":"999.0", "release_timestamp":RELEASE_TIMESTAMP})
        updater = MagicMock()
        updater.get_targetinfo.return_value = target
        with tempfile.TemporaryDirectory() as cache, patch.object(self_update, "Updater", return_value=updater), patch.object(self_update,"user_cache_dir",return_value=cache), patch.object(self_update,"_license_status",AsyncMock(return_value=LicenseStatus("valid",True,license_expires_at=RELEASE_TIMESTAMP-1))), patch.object(self_update,"_installation_path") as installation:
            self.assertEqual(self_update.run_self_update(check_only=False,assume_yes=True),1)
            updater.download_target.assert_not_called()
            installation.assert_not_called()

    def test_cli_missing_release_date_cannot_install(self):
        from unittest.mock import MagicMock
        updater = MagicMock()
        updater.get_targetinfo.return_value = SimpleNamespace(custom={"version":"999.0"})
        with tempfile.TemporaryDirectory() as cache, patch.object(self_update, "Updater", return_value=updater), patch.object(self_update,"user_cache_dir",return_value=cache):
            self.assertEqual(self_update.run_self_update(check_only=False,assume_yes=True),1)
            updater.download_target.assert_not_called()
