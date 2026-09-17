from __future__ import annotations

import asyncio
from dataclasses import replace
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from rich.console import Console

from src.backend.media import VideoObject
from src.cli.batch import build_parser, main
from src.cli.downloads import DownloadOutcome
from src.cli.model_store import ModelStore
from src.cli.providers import ContentKind, Route
from src.cli.settings import CliSettings, SettingsStore
from src.cli.wizard import (
    DownloadSpeedColumn,
    SmartUnitsColumn,
    WizardContext,
    handle_account_auth,
    handle_batch_management,
    handle_download_single,
    handle_license_management,
    handle_scrape_profile,
    handle_settings,
    make_download_progress,
    print_banner,
    run_wizard,
)


class FakeQuestionaryPrompt:
    def __init__(self, value):
        self.value = value

    async def ask_async(self):
        return self.value

    def ask(self):
        return self.value


class WizardDualModeTests(unittest.TestCase):
    def test_argument_parser_flags(self):
        parser = build_parser()
        args = parser.parse_args(["--quality", "720", "--output", "/tmp/out", "--url", "https://example.com/v"])
        self.assertEqual(args.quality, "720")
        self.assertEqual(args.output, "/tmp/out")
        self.assertEqual(args.url, ["https://example.com/v"])
        self.assertFalse(args.interactive)

    @patch("src.cli.wizard.run_wizard", new_callable=AsyncMock)
    @patch("src.cli.batch.run_batch", new_callable=AsyncMock)
    def test_interactive_mode_triggered_when_no_args(self, mock_batch, mock_wizard):
        mock_wizard.return_value = 0
        code = main([])
        self.assertEqual(code, 0)
        mock_wizard.assert_called_once()
        mock_batch.assert_not_called()

    @patch("src.cli.wizard.run_wizard", new_callable=AsyncMock)
    @patch("src.cli.batch.run_batch", new_callable=AsyncMock)
    def test_interactive_flag_forces_wizard(self, mock_batch, mock_wizard):
        mock_wizard.return_value = 0
        code = main(["--interactive"])
        self.assertEqual(code, 0)
        mock_wizard.assert_called_once()
        mock_batch.assert_not_called()

    @patch("src.cli.wizard.run_wizard", new_callable=AsyncMock)
    @patch("src.cli.batch.run_batch", new_callable=AsyncMock)
    def test_cli_flags_run_headlessly(self, mock_batch, mock_wizard):
        mock_batch.return_value = 0
        code = main(["--url", "https://pornhub.com/view_video.php?viewkey=test", "--quality", "720p"])
        self.assertEqual(code, 0)
        mock_batch.assert_called_once()
        mock_wizard.assert_not_called()


class WizardRenderingTests(unittest.TestCase):
    def test_banner_rendering(self):
        string_io = io.StringIO()
        console = Console(file=string_io, force_terminal=True, width=80)
        print_banner(console, license_state="valid")
        output = string_io.getvalue()
        self.assertIn("PORN FETCH", output)
        self.assertIn("Premium: Active", output)

    def test_smart_units_column(self):
        col = SmartUnitsColumn()
        task_bytes = type("Task", (), {
            "completed": 10 * 1024 * 1024, "total": 50 * 1024 * 1024, "fields": {"unit": "bytes"},
        })()
        rendered_bytes = col.render(task_bytes)
        self.assertIn("MB", str(rendered_bytes))

        task_items = type("Task", (), {"completed": 5, "total": 20, "fields": {"unit": "items"}})()
        rendered_items = col.render(task_items)
        self.assertIn("5 / 20 items", str(rendered_items))

        task_segments = type("Task", (), {"completed": 5, "total": 20, "fields": {"unit": "segments"}})()
        rendered_segments = col.render(task_segments)
        self.assertIn("5 / 20 segments", str(rendered_segments))

    def test_download_speed_column_uses_segment_rate_for_hls(self):
        column = DownloadSpeedColumn()
        task = type("Task", (), {"fields": {"unit": "segments"}, "speed": 12.5, "finished_speed": None})()
        self.assertIn("12.5 segments/sec", str(column.render(task)))


class WizardFlowTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.settings_store = SettingsStore(self.root / "settings.json")
        self.settings = self.settings_store.load()
        self.model_store = ModelStore(self.root / "models.json")
        self.console = Console(file=io.StringIO(), force_terminal=False)

        self.fake_pool = MagicMock()
        self.fake_pool.close = AsyncMock()
        self.fake_pool.runtime_config = MagicMock()

        self.fake_license = MagicMock()
        self.fake_license.status = type("Status", (), {"state": "valid", "allowed": True, "expires_at": None})()
        self.fake_license.reason = "License active."
        self.fake_license.check = AsyncMock(return_value=self.fake_license.status)
        self.fake_license.close = AsyncMock()

        self.ctx = WizardContext(
            self.settings,
            self.settings_store,
            self.console,
            model_store=self.model_store,
            pool=self.fake_pool,
            license_service=self.fake_license,
        )

    async def asyncTearDown(self):
        await self.ctx.close()
        self.temp_dir.cleanup()

    @patch("questionary.select")
    @patch("questionary.text")
    @patch("src.cli.wizard.download_video", new_callable=AsyncMock)
    async def test_download_single_url_flow(self, mock_download_video, mock_text, mock_select):
        mock_text.return_value = FakeQuestionaryPrompt("https://pornhub.com/view_video.php?viewkey=123")
        mock_select.return_value = FakeQuestionaryPrompt("720")

        mock_video = MagicMock()
        mock_video.title = "Sample Video"
        mock_video.author = "Sample Author"
        mock_video.qualities = [360, 720, 1080]
        mock_video.length = 10
        route = Route("pornhub", ContentKind.VIDEO, "https://pornhub.com/view_video.php?viewkey=123")
        self.fake_pool.resolve = AsyncMock(return_value=(route, mock_video))

        mock_download_video.return_value = DownloadOutcome("completed", Path(self.root / "Sample Video.mp4"))

        with patch("src.cli.wizard.prepare_video", new_callable=AsyncMock, return_value=mock_video):
            await handle_download_single(self.ctx)

        mock_download_video.assert_called_once()
        args, kwargs = mock_download_video.call_args
        self.assertEqual(args[2], "720")
        self.assertTrue(kwargs["has_premium"])

    @patch("questionary.select")
    @patch("questionary.checkbox")
    @patch("questionary.text")
    @patch("src.cli.wizard.download_video", new_callable=AsyncMock)
    async def test_scrape_profile_flow(self, mock_download_video, mock_text, mock_checkbox, mock_select):
        mock_text.return_value = FakeQuestionaryPrompt("https://pornhub.com/model/testmodel")
        mock_checkbox.side_effect = [
            FakeQuestionaryPrompt(["videos"]),
            FakeQuestionaryPrompt([0]),
        ]
        mock_select.side_effect = [
            FakeQuestionaryPrompt("select"),
            FakeQuestionaryPrompt("best"),
        ]

        mock_video = MagicMock()
        mock_video.url = "https://pornhub.com/view_video.php?viewkey=abc"
        mock_video.title = "Model Clip"
        mock_video.author = "testmodel"
        mock_video.qualities = [720]
        mock_video.length = 5

        async def fake_stream(url, pages=5):
            yield mock_video

        self.fake_pool.media_stream = fake_stream
        mock_download_video.return_value = DownloadOutcome("completed", Path(self.root / "Model Clip.mp4"))

        with patch("src.cli.wizard.prepare_video", new_callable=AsyncMock, return_value=mock_video):
            await handle_scrape_profile(self.ctx)

        mock_download_video.assert_called_once()

    @patch("questionary.select")
    @patch("questionary.text")
    async def test_batch_management_flow(self, mock_text, mock_select):
        # 1: Add model, 2: View, 3: Back
        mock_select.side_effect = [
            FakeQuestionaryPrompt("add"),
            FakeQuestionaryPrompt("view"),
            FakeQuestionaryPrompt("back"),
        ]
        mock_text.return_value = FakeQuestionaryPrompt("https://pornhub.com/model/newbie")

        await handle_batch_management(self.ctx)

        models = self.model_store.models()
        self.assertEqual(len(models), 1)
        self.assertEqual(models[0][0], "https://pornhub.com/model/newbie")

    @patch("questionary.select")
    @patch("questionary.confirm")
    async def test_settings_modification_flow(self, mock_confirm, mock_select):
        # Edit setting 'skip_existing' from True to False, then Back
        mock_select.side_effect = [
            FakeQuestionaryPrompt("edit"),
            FakeQuestionaryPrompt("skip_existing"),
            FakeQuestionaryPrompt("back"),
        ]
        mock_confirm.return_value = FakeQuestionaryPrompt(False)

        await handle_settings(self.ctx)

        self.assertFalse(self.ctx.settings.skip_existing)
        reloaded = self.settings_store.load()
        self.assertFalse(reloaded.skip_existing)

    @patch("questionary.select")
    @patch("questionary.text")
    @patch("questionary.password")
    async def test_account_login_credentials_flow(self, mock_password, mock_text, mock_select):
        mock_select.side_effect = [
            FakeQuestionaryPrompt("credentials"),
            FakeQuestionaryPrompt("PornHub"),
            FakeQuestionaryPrompt("back"),
        ]
        mock_text.return_value = FakeQuestionaryPrompt("testuser")
        mock_password.return_value = FakeQuestionaryPrompt("secretpass")

        self.ctx.account_service.login = AsyncMock(return_value=True)

        await handle_account_auth(self.ctx)

        self.ctx.account_service.login.assert_called_once_with(
            "PornHub", username="testuser", password="secretpass",
        )

    @patch("questionary.select")
    @patch("questionary.confirm")
    async def test_license_management_flow(self, mock_confirm, mock_select):
        mock_select.side_effect = [
            FakeQuestionaryPrompt("check"),
            FakeQuestionaryPrompt("deactivate"),
            FakeQuestionaryPrompt("back"),
        ]
        mock_confirm.return_value = FakeQuestionaryPrompt(True)
        self.fake_license.deactivate = AsyncMock(return_value=self.fake_license.status)

        await handle_license_management(self.ctx)

        self.fake_license.check.assert_called()
        self.fake_license.deactivate.assert_called_once()

    @patch("questionary.select")
    async def test_unlicensed_quality_locked_in_settings(self, mock_select):
        # License is unallowed
        self.fake_license.status.allowed = False
        captured_choices = []
        action_seq = ["edit", "back"]

        def fake_select(prompt, choices=None, default=None, style=None):
            if "Settings & Configuration" in prompt:
                return FakeQuestionaryPrompt(action_seq.pop(0))
            elif "setting to modify" in prompt:
                return FakeQuestionaryPrompt("quality")
            elif "preferred quality" in prompt:
                captured_choices.extend(choices)
                return FakeQuestionaryPrompt("2160")
            return FakeQuestionaryPrompt("back")

        mock_select.side_effect = fake_select

        await handle_settings(self.ctx)

        # 2160, 1440, 1080, best must have disabled set
        locked_map = {c.value: c.disabled for c in captured_choices}
        self.assertTrue(locked_map.get("2160"))
        self.assertTrue(locked_map.get("1440"))
        self.assertTrue(locked_map.get("1080"))
        self.assertTrue(locked_map.get("best"))
        self.assertIsNone(locked_map.get("720"))
        self.assertIsNone(locked_map.get("480"))
        self.assertIsNone(locked_map.get("worst"))

        # The setting must NOT have been updated to 2160
        self.assertNotEqual(self.ctx.settings.quality, "2160")

    @patch("questionary.select")
    async def test_licensed_quality_allowed_in_settings(self, mock_select):
        self.fake_license.status.allowed = True
        captured_choices = []
        action_seq = ["edit", "back"]

        def fake_select(prompt, choices=None, default=None, style=None):
            if "Settings & Configuration" in prompt:
                return FakeQuestionaryPrompt(action_seq.pop(0))
            elif "setting to modify" in prompt:
                return FakeQuestionaryPrompt("quality")
            elif "preferred quality" in prompt:
                captured_choices.extend(choices)
                return FakeQuestionaryPrompt("2160")
            return FakeQuestionaryPrompt("back")

        mock_select.side_effect = fake_select

        await handle_settings(self.ctx)

        # All qualities must have disabled=None
        locked_map = {c.value: c.disabled for c in captured_choices}
        self.assertIsNone(locked_map.get("2160"))
        self.assertIsNone(locked_map.get("1080"))
        self.assertEqual(self.ctx.settings.quality, "2160")

    @patch("questionary.select")
    async def test_run_wizard_immediate_exit(self, mock_select):
        mock_select.return_value = FakeQuestionaryPrompt("exit")
        code = await run_wizard()
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
