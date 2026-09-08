import asyncio
from pathlib import Path
from types import SimpleNamespace
import tempfile
import time
import unittest

from PySide6.QtCore import QCoreApplication

from license_client import LicenseError, LicenseStatus
from src.backend.download_manager import DownloadListModel
from src.backend.license_bridge import LicenseBridge, load_production_config


class FakeLicenseClient:
    def __init__(self) -> None:
        self.status = LicenseStatus("unlicensed", False)
        self.import_error: LicenseError | None = None
        self.import_calls = 0
        self.closed = False

    async def check(self, *, force: bool = False) -> LicenseStatus:
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
            {"public_key", "account_id", "product_id", "policy_id"},
        )
        self.assertFalse(any("token" in key or "private" in key for key in config))


if __name__ == "__main__":
    unittest.main()
