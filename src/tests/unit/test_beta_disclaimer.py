from __future__ import annotations

import io
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from rich.console import Console

from src.cli.beta_disclaimer import prompt_beta_disclaimer
from src.cli.settings import SettingsStore
from src.shared.beta_disclaimer import BETA_DISCLAIMER_VERSION, DisclaimerReadDelay


class DisclaimerReadDelayTests(unittest.TestCase):
    def test_requires_a_full_30_seconds_after_display(self):
        now = [100.0]
        with patch("src.shared.beta_disclaimer.time", SimpleNamespace(monotonic=lambda: now[0])):
            delay = DisclaimerReadDelay()
            self.assertEqual(delay.remaining_seconds, 30)
            delay.start()
            now[0] = 129.999
            self.assertEqual(delay.remaining_seconds, 1)
            now[0] = 130.0
            self.assertEqual(delay.remaining_seconds, 0)


class CliBetaDisclaimerTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.store = SettingsStore(Path(self.temporary.name) / "settings.json")
        self.settings = self.store.load(legacy_paths=[])
        self.console = Console(file=io.StringIO(), force_terminal=True, width=100)

    async def test_waits_before_prompting_and_saves_only_after_ok(self):
        await self._prompt_after_delay("OK")
        self.assertEqual(self.store.load().beta_disclaimer_version, BETA_DISCLAIMER_VERSION)

    async def test_exit_does_not_save_acceptance(self):
        result = await self._prompt_after_delay("Exit")
        self.assertIsNone(result)
        self.assertEqual(self.store.load().beta_disclaimer_version, "")

    async def _prompt_after_delay(self, choice):
        now = [100.0]

        async def advance(seconds):
            now[0] += seconds

        def prompt(*args, **kwargs):
            self.assertGreaterEqual(now[0], 130.0)
            self.assertEqual(self.store.load().beta_disclaimer_version, "")
            return SimpleNamespace(ask_async=AsyncMock(return_value=choice))

        with (
            patch("src.shared.beta_disclaimer.time", SimpleNamespace(monotonic=lambda: now[0])),
            patch("src.cli.beta_disclaimer.asyncio.sleep", side_effect=advance),
            patch("src.cli.beta_disclaimer.sys.stdin.isatty", return_value=True),
            patch("src.cli.beta_disclaimer.questionary.select", side_effect=prompt),
        ):
            return await prompt_beta_disclaimer(self.settings, self.store, console=self.console)

    async def test_unattended_first_run_stops_without_prompt_or_acceptance(self):
        with (
            patch("src.cli.beta_disclaimer.sys.stdin.isatty", return_value=False),
            patch("src.cli.beta_disclaimer.questionary.select") as prompt,
        ):
            result = await prompt_beta_disclaimer(self.settings, self.store, console=self.console)
        self.assertIsNone(result)
        prompt.assert_not_called()
        self.assertEqual(self.store.load().beta_disclaimer_version, "")

    async def test_previously_accepted_notice_does_not_delay_or_prompt(self):
        self.settings = self.settings.overridden(beta_disclaimer_version=BETA_DISCLAIMER_VERSION)
        self.store.save(self.settings)
        with (
            patch("src.cli.beta_disclaimer.asyncio.sleep", new_callable=AsyncMock) as sleep,
            patch("src.cli.beta_disclaimer.questionary.select") as prompt,
        ):
            result = await prompt_beta_disclaimer(self.settings, self.store, console=self.console)
        self.assertIs(result, self.settings)
        sleep.assert_not_called()
        prompt.assert_not_called()
