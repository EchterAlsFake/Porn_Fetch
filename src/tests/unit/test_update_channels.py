"""Channel isolation, release selection, and migration without network requests."""
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from src.shared.update_channels import eligible_channels, newest, validate_release, version_parts


class ChannelPolicyTests(unittest.TestCase):
    def test_beta_receives_newest_release_including_stable(self):
        stable = {"version": "3.9.3", "channel": "stable"}
        beta = {"version": "3.9.2", "channel": "beta"}
        self.assertEqual(eligible_channels("stable"), ("stable",))
        self.assertEqual(eligible_channels("beta"), ("stable", "beta"))
        self.assertIs(newest([stable, beta]), stable)
        beta["version"] = "3.9.4"
        self.assertIs(newest([stable, beta]), beta)
        self.assertEqual(version_parts("3.9"), version_parts("3.9.0"))

    def test_signed_release_must_match_requested_channel(self):
        with self.assertRaisesRegex(ValueError, "channel"):
            validate_release({"version": "3.9.2", "channel": "beta"}, "stable")

    def test_settings_migration_and_new_beta_install(self):
        from PySide6.QtCore import QSettings

        from src.backend.config import SettingsManager
        from src.cli.settings import SettingsStore
        with tempfile.TemporaryDirectory() as temporary, patch("src.shared.version.BUILD_CHANNEL", "beta"):
            store = QSettings(str(Path(temporary) / "gui.ini"), QSettings.IniFormat)
            manager = SettingsManager(store)
            self.assertEqual(manager.update_channel, "beta")
            manager.update_channel = "stable"
            self.assertEqual(SettingsManager(store).update_channel, "stable")
            old = QSettings(str(Path(temporary) / "old.ini"), QSettings.IniFormat)
            old.setValue("Misc/update_checks", True)
            self.assertEqual(SettingsManager(old).update_channel, "stable")
            cli = Path(temporary) / "cli.json"
            cli.write_text(json.dumps({"settings": {"quality": "720"}}))
            self.assertEqual(SettingsStore(cli).load().update_channel, "stable")

    def test_cli_override_uses_independent_feeds_without_saving(self):
        from src.cli import self_update
        with tempfile.TemporaryDirectory() as temporary:
            build = Path(temporary) / "build.json"
            build.write_text(json.dumps({"version": "3.9.0", "target": "linux/amd64.zip"}))
            settings = SimpleNamespace(update_channel="stable")
            clients = [MagicMock(), MagicMock()]
            for client, channel, version in zip(clients, ("stable", "beta"), ("3.9.1", "3.9.2")):
                client.get_targetinfo.return_value = SimpleNamespace(
                    length=123, custom={"channel": channel, "version": version, "release_timestamp": 1791244800})
            with patch("src.cli.settings.SettingsStore") as store, \
                 patch.object(self_update, "BUILD_FILE", build), \
                 patch.object(self_update, "user_cache_dir", return_value=temporary), \
                 patch.object(self_update, "REPOSITORY_URL", self_update.UPDATE_REPO_URL + "/"), \
                 patch.object(self_update, "Updater", side_effect=clients) as factory, \
                 patch("src.shared.service_transport.ServiceFetcher"), redirect_stdout(io.StringIO()) as output:
                store.return_value.load.return_value = settings
                self.assertEqual(self_update.run_self_update(check_only=True, assume_yes=False, channel="beta"), 0)
                self.assertIn("3.9.2 Beta", output.getvalue())
                store.return_value.save.assert_not_called()
                calls = [call.kwargs for call in factory.call_args_list]
                self.assertNotEqual(calls[0]["metadata_dir"], calls[1]["metadata_dir"])
                self.assertTrue(calls[0]["metadata_base_url"].endswith("/stable/metadata/"))
                self.assertTrue(calls[1]["metadata_base_url"].endswith("/beta/metadata/"))


class DesktopChannelTests(unittest.IsolatedAsyncioTestCase):
    async def test_channel_selection_and_final_stable_release(self):
        from src.backend.update_service import CheckUpdates
        stable = {"channel": "stable", "version": "3.9.3"}
        beta = {"channel": "beta", "version": "3.9.2"}
        with patch.object(CheckUpdates, "_check_repository", AsyncMock(side_effect=[stable, beta])) as fetch:
            self.assertIs(await CheckUpdates.check_signed_repository(channel="beta"), stable)
            self.assertEqual([call.args[0] for call in fetch.await_args_list], ["stable", "beta"])
        with patch.object(CheckUpdates, "_check_repository", AsyncMock(return_value=stable)) as fetch:
            self.assertIs(await CheckUpdates.check_signed_repository(channel="stable"), stable)
            fetch.assert_awaited_once_with("stable", include_current=False)

    async def test_switching_to_stable_never_offers_older_release(self):
        from src.backend.update_service import CheckUpdates
        metadata = SimpleNamespace(signed=SimpleNamespace(targets={}))
        release = {"version": "3.9.1", "channel": "stable"}
        with patch("src.backend.update_service.service_core.request", AsyncMock(return_value=SimpleNamespace(status_code=200, content=b"signed"))), \
             patch("src.backend.update_service.verify_repository_manifest", return_value=(metadata, release)), \
             patch("src.backend.update_service.ROOT_FILE", SimpleNamespace(read_bytes=lambda: b"root")), \
             patch("src.backend.update_service.QFile") as resource, \
             patch("src.backend.update_service.__version__", "3.9.2"):
            resource.return_value.exists.return_value = False
            self.assertIsNone(await CheckUpdates.check_signed_repository(channel="stable"))
