import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace

from PySide6.QtCore import QCoreApplication, QFile

from src.backend.download_manager import DownloadListModel
from src.backend.license_bridge import LicenseBridge, load_production_config
from src.licensing import LicenseError, LicenseStatus


class FakeLicenseClient:
    def __init__(self) -> None:
        self.status = LicenseStatus("unlicensed", False)
        self.import_error: LicenseError | None = None
        self.import_calls = 0
        self.closed = False
        self.check_forces: list[bool] = []

    async def check(self, *, force: bool = False) -> LicenseStatus:
        self.check_forces.append(force)
        return self.status

    async def import_license(self, blob: bytes) -> LicenseStatus:
        self.import_calls += 1
        if self.import_error is not None:
            raise self.import_error
        return self.status

    async def deactivate(self) -> LicenseStatus:
        self.status = LicenseStatus("deactivated", False)
        return self.status

    async def close(self) -> None:
        self.closed = True


class LicenseIntegrationTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.qt_app = QCoreApplication.instance() or QCoreApplication([])

    async def asyncSetUp(self) -> None:
        self.client = FakeLicenseClient()
        self.bridge = LicenseBridge(self.client)

    async def asyncTearDown(self) -> None:
        await self.bridge.shutdown()

    async def test_async_check_updates_the_feature_gate(self) -> None:
        self.client.status = LicenseStatus("valid", True, time.time() + 3600)

        await self.bridge._run_check(force=True)

        self.assertTrue(self.bridge.isPremium)
        self.assertEqual(self.bridge.state, "valid")

    async def test_start_schedules_initial_check_on_the_running_loop(self) -> None:
        self.client.status = LicenseStatus("valid", True, time.time() + 3600)

        task = self.bridge.start()

        self.assertIsNotNone(task)
        await task
        self.assertTrue(self.bridge.isPremium)
        self.assertFalse(self.bridge.busy)
        self.assertEqual(self.client.check_forces, [True])

    async def test_online_rejection_emits_notice(self) -> None:
        notices = []
        self.bridge.licenseRejected.connect(notices.append)
        self.client.status = LicenseStatus("revoked", False, server_rejected=True)

        await self.bridge._run_check(force=True)

        self.assertEqual(len(notices), 1)
        self.assertIn("support@echteralsfake.me", notices[0])

    async def test_download_model_uses_license_status_allowed(self) -> None:
        model = DownloadListModel(premium_access=lambda: self.bridge.isPremium)
        video = SimpleNamespace(selected_quality="720")
        model._items.append({
            "jobId": "one",
            "availableQualities": ["720", "1080"],
            "selectedQuality": "720",
            "_video": video,
        })
        model._row_by_id["one"] = 0

        self.assertFalse(model.set_video_quality("one", "1080"))
        self.bridge._set_status(LicenseStatus("valid", True))
        self.assertTrue(model.set_video_quality("one", "1080"))
        self.bridge._set_status(LicenseStatus("expired_grace", False))
        self.assertFalse(model.set_video_quality("one", "1080"))

    async def test_oversized_import_is_bounded_and_never_reaches_client(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            license_path = Path(directory) / "oversized.license"
            license_path.write_bytes(b"x" * 32769)

            await self.bridge._import_from_path(license_path)

        self.assertEqual(self.client.import_calls, 0)
        self.assertEqual(self.bridge.state, "unlicensed")

    async def test_malformed_replacement_does_not_remove_current_access(self) -> None:
        self.bridge._set_status(LicenseStatus("valid", True))
        self.client.import_error = LicenseError("Import a valid schema-2 license file")
        with tempfile.TemporaryDirectory() as directory:
            license_path = Path(directory) / "bad.license"
            license_path.write_text("not JSON", encoding="utf-8")

            await self.bridge._import_from_path(license_path)

        self.assertTrue(self.bridge.isPremium)
        self.assertEqual(self.bridge.state, "valid")

    async def test_shutdown_closes_the_long_lived_client(self) -> None:
        await self.bridge.shutdown()
        self.assertTrue(self.client.closed)

    def test_bundled_configuration_contains_only_public_identifiers(self) -> None:
        config = load_production_config()
        self.assertEqual(
            set(config),
            {"public_key", "account_id", "product_id", "policy_id", "base_url"},
        )
        self.assertFalse(any("token" in key or "private" in key for key in config))

    def test_production_configuration_is_embedded_in_qt_resources(self) -> None:
        import src.frontend.UI.resources  # noqa: F401

        self.assertTrue(QFile.exists(":/licensing/production.json"))
        self.assertEqual(
            load_production_config(),
            __import__("json").loads(Path("src/licensing/production.json").read_text()),
        )

    async def test_license_bridge_expiry_properties(self) -> None:
        now = time.time()
        # Lifetime valid license
        self.bridge._set_status(LicenseStatus("valid", True, expires_at=now + 604800, next_check_at=now + 604800))
        self.assertEqual(self.bridge.licenseExpiresAt, "Lifetime / Never")
        self.assertNotEqual(self.bridge.nextCheckAt, "")

        # Expiring license
        exp_ts = now + 86400 * 30
        self.bridge._set_status(LicenseStatus("valid", True, expires_at=now + 604800, license_expires_at=exp_ts, next_check_at=now + 604800))
        self.assertNotEqual(self.bridge.licenseExpiresAt, "Lifetime / Never")
        self.assertIn(":", self.bridge.licenseExpiresAt)

    async def test_first_activation_signal_and_show_help(self) -> None:
        activations = []
        self.bridge.firstActivation.connect(lambda: activations.append(True))

        # Initial state is unlicensed (allowed == False)
        self.assertFalse(self.bridge.isValid)

        # Calling showActivationHelp slot emits signal
        self.bridge.showActivationHelp()
        self.assertEqual(len(activations), 1)

        # Import valid license when previously not allowed -> emits firstActivation
        self.client.status = LicenseStatus("valid", True, expires_at=time.time() + 604800)
        with tempfile.TemporaryDirectory() as directory:
            license_path = Path(directory) / "test.license"
            license_path.write_text('{"schema": 2}', encoding="utf-8")
            await self.bridge._import_from_path(license_path)

        self.assertEqual(len(activations), 2)


if __name__ == "__main__":
    unittest.main()
