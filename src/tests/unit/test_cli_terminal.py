"""Offline keyboard/layout checks; never contact providers or licensing servers."""
from __future__ import annotations

import asyncio
import io
import unittest
from dataclasses import fields
from unittest.mock import patch

from prompt_toolkit.application import create_app_session
from prompt_toolkit.data_structures import Size
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output.vt100 import Vt100_Output
from rich.console import Console

from src.cli import prompts
from src.cli.flows.settings import SETTINGS_METADATA, setting_value
from src.cli.settings import CliSettings
from src.cli.terminal import Table, make_download_progress, print_banner, print_error, print_screen

SIZES = [(32, 8), (40, 12), (60, 18), (80, 24), (120, 40)]


class TerminalLayoutTests(unittest.TestCase):
    def test_every_configuration_key_is_discoverable(self):
        self.assertEqual({field.name for field in fields(CliSettings)}, set(SETTINGS_METADATA))
        settings = CliSettings(proxy="https://secret:password@example.com", proxy_auth="secret")
        self.assertNotIn("secret", setting_value(settings, "proxy"))
        self.assertNotIn("secret", setting_value(settings, "proxy_auth"))

    def test_sections_tables_and_progress_fit_terminal_widths(self):
        for width, height in SIZES:
            with self.subTest(width=width, height=height):
                output = io.StringIO()
                console = Console(file=output, width=width, height=height, color_system=None)
                print_banner(console, "valid")
                print_screen(console, "Queue")
                table = Table(title="Queue")
                for name in ("Title", "Status", "Progress", "URL"):
                    table.add_column(name)
                table.add_row("A long media title for responsive layout", "Paused", "4 / 12 segments", "https://example.com/video")
                console.print(table)
                print_error(console, "Failed", "A literal [filename] could not be opened.")
                progress = make_download_progress(console)
                progress.add_task("Download", completed=4, total=12, unit="segments")
                console.print(progress.get_renderable())
                rendered = output.getvalue()
                self.assertIn("Paused", rendered)
                self.assertIn("4 / 12 segments", rendered)
                self.assertIn("[filename]", rendered)
                self.assertTrue(all(len(line) <= width for line in rendered.splitlines()), rendered)

    def test_plain_menu_filter_disabled_choices_and_validation(self):
        choices = [prompts.Choice("Locked", value="locked", disabled="Premium"),
                   prompts.Choice("Output folder", value="path", description="output_path")]
        with patch("builtins.input", side_effect=["1", "/output_path", "1"]):
            self.assertEqual(prompts.PlainPrompt("select", "Settings", choices).ask(), "path")
        with patch("builtins.input", return_value="b"):
            self.assertIsNone(prompts.PlainPrompt("select", "Settings", choices).ask())
        with patch("builtins.input", side_effect=["invalid", "12"]):
            prompt = prompts.PlainPrompt("text", "Limit", validate=lambda v: True if v.isdigit() else "Use a number")
            self.assertEqual(prompt.ask(), "12")


class KeyboardTests(unittest.IsolatedAsyncioTestCase):
    async def run_prompt(self, keys, *, size=(80, 24), choices=None, searchable=False, resize=None):
        stream = io.StringIO()
        dimensions = [size]
        output = Vt100_Output(stream, lambda: Size(rows=dimensions[0][1], columns=dimensions[0][0]), term="xterm")
        with create_pipe_input() as keyboard, create_app_session(input=keyboard, output=output):
            with patch("src.cli.prompts.plain_mode", return_value=False):
                prompt = prompts.select("Settings", choices=choices or [
                    prompts.Separator("Video"),
                    prompts.Choice("Locked", value="locked", disabled="Premium"),
                    *[prompts.Choice(f"Option {i}", value=i, description=f"Context for setting {i}") for i in range(40)],
                ], searchable=searchable)
            task = asyncio.create_task(prompt.ask_async())
            await asyncio.sleep(0.03)
            if resize:
                dimensions[0] = resize
                prompt.application._on_resize()
                await asyncio.sleep(0.03)
            if keys.endswith("\r"):
                keyboard.send_text(keys[:-1])
                await asyncio.sleep(0.06)
                screen = prompt.application.renderer._last_screen
                snapshot = "\n".join("".join(char.char for _, char in sorted(row.items()))
                                     for _, row in sorted(screen.data_buffer.items()))
                keyboard.send_text("\r")
            else:
                snapshot = ""
                keyboard.send_text(keys)
            result = await asyncio.wait_for(task, timeout=3)
        return result, snapshot

    async def test_keyboard_navigation_scrolls_at_multiple_sizes(self):
        for size in SIZES:
            with self.subTest(size=size):
                result, rendered = await self.run_prompt("\x1b[B" * 30 + "\r", size=size)
                self.assertEqual(result, 30)
                self.assertIn("Context for setting 30", rendered)
                self.assertNotIn("Window too small", rendered)
                self.assertLessEqual(len(rendered.splitlines()), size[1])
                self.assertTrue(all(len(line) <= size[0] for line in rendered.splitlines()))

    async def test_search_matches_configuration_keys_and_prevents_empty_accept(self):
        choices = [prompts.Choice("Output folder", value="path", description="Video / output_path"),
                   prompts.Choice("Quality", value="quality", description="Preferred quality")]
        result, _ = await self.run_prompt("output_path\r", choices=choices, searchable=True)
        self.assertEqual(result, "path")
        result, rendered = await self.run_prompt("missing\r\x15quality\r", choices=choices, searchable=True)
        self.assertEqual(result, "quality")
        self.assertNotIn("Exception", rendered)

    async def test_escape_and_resize(self):
        result, _ = await self.run_prompt("\x1b", size=(40, 12))
        self.assertIsNone(result)
        result, _ = await self.run_prompt("\t\r", size=(120, 40), resize=(32, 8))
        self.assertEqual(result, 1)

    async def test_checkbox_and_text_use_escape_navigation(self):
        for kind in ("checkbox", "text", "confirm"):
            with self.subTest(kind=kind):
                output = Vt100_Output(io.StringIO(), lambda: Size(rows=12, columns=40), term="xterm")
                with create_pipe_input() as keyboard, create_app_session(input=keyboard, output=output):
                    with patch("src.cli.prompts.plain_mode", return_value=False):
                        kwargs = {"choices": ["First", "Second"]} if kind == "checkbox" else {}
                        prompt = getattr(prompts, kind)("Choose", **kwargs)
                    task = asyncio.create_task(prompt.ask_async())
                    await asyncio.sleep(0.02)
                    keyboard.send_text("\x1b")
                    self.assertIsNone(await asyncio.wait_for(task, 3))


if __name__ == "__main__":
    unittest.main()
