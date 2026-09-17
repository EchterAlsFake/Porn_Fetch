from __future__ import annotations

import json
from io import StringIO
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from rich.console import Console

from src.backend.error_reporting import (
    MAX_BODY_BYTES,
    MAX_MESSAGE_CHARS,
    ERROR_REPORT_DISCLOSURE,
    ERROR_REPORT_EXAMPLE,
    _payload_bytes,
    build_error_report,
    redact_log_text,
    report_exception,
    report_public_error,
    safe_url,
)
from src.cli.settings import CliSettings, SettingsStore, prompt_error_reporting_consent


class ErrorReportFormattingTests(unittest.TestCase):
    def test_first_run_text_describes_the_actual_report(self) -> None:
        for detail in (
            "correlation ID", "UTC timestamp", "query strings", "cookies",
            "2,000 characters", "4 KiB", "not to log or store client IP addresses",
        ):
            self.assertIn(detail, ERROR_REPORT_DISCLOSURE)
        self.assertIn("video_url=https://example.com/watch/example-video", ERROR_REPORT_EXAMPLE)
        self.assertIn("traceback:", ERROR_REPORT_EXAMPLE)

    def test_safe_url_preserves_reproduction_path_only(self) -> None:
        value = safe_url("https://user:password@example.com/watch/abc?token=secret#private")
        self.assertEqual(value, "https://example.com/watch/abc")
        self.assertEqual(
            redact_log_text("https://example.com/home/alice/video"),
            "https://example.com/home/alice/video",
        )

    def test_redaction_removes_sensitive_values(self) -> None:
        raw = (
            "https://example.com/watch/abc?token=secret\n"
            "Authorization: Bearer credential\n"
            "Cookie: session=credential\n"
            "password=hunter2 email=user@example.com ip=192.0.2.4 path=/home/alice/project"
        )
        redacted = redact_log_text(raw)
        for secret in ("secret", "credential", "hunter2", "user@example.com", "192.0.2.4", "alice"):
            self.assertNotIn(secret, redacted)
        self.assertIn("https://example.com/watch/abc", redacted)

    def test_report_has_context_traceback_and_contract_limits(self) -> None:
        try:
            raise RuntimeError("synthetic failure")
        except RuntimeError as error:
            message, report_id = build_error_report(
                error,
                operation="scrape video",
                location="Example.scrape",
                context={"video_url": "https://example.com/video/42?account=private"},
                correlation_id="test-correlation",
            )

        self.assertEqual(report_id, "test-correlation")
        self.assertIn("operation=scrape video", message)
        self.assertIn("location=Example.scrape", message)
        self.assertIn("video_url=https://example.com/video/42", message)
        self.assertIn("Traceback (most recent call last)", message)
        self.assertIn("RuntimeError: synthetic failure", message)
        self.assertLessEqual(len(message), MAX_MESSAGE_CHARS)
        self.assertLessEqual(len(_payload_bytes(message)), MAX_BODY_BYTES)
        self.assertEqual(set(json.loads(_payload_bytes(message))), {"message"})


class ErrorReportDeliveryTests(unittest.IsolatedAsyncioTestCase):
    async def test_delivery_uses_exact_public_contract(self) -> None:
        session = AsyncMock()
        session.post.return_value.status_code = 204
        with patch("src.backend.error_reporting.AsyncSession", return_value=session):
            delivered = await report_public_error("synthetic diagnostic")

        self.assertTrue(delivered)
        _, kwargs = session.post.await_args
        self.assertEqual(json.loads(kwargs["content"]), {"message": "synthetic diagnostic"})
        self.assertFalse(kwargs["allow_redirects"])
        session.close.assert_awaited_once()

    async def test_disabled_reporting_does_not_send(self) -> None:
        with patch(
            "src.backend.error_reporting.report_public_error", new_callable=AsyncMock,
        ) as sender:
            report_id = await report_exception(
                RuntimeError("synthetic"),
                operation="test",
                location="ErrorReportDeliveryTests",
                enabled=False,
            )
        self.assertEqual(len(report_id), 12)
        sender.assert_not_awaited()


class ErrorReportConsentTests(unittest.IsolatedAsyncioTestCase):
    async def test_legacy_enabled_value_is_inactive_until_decided(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = SettingsStore(Path(directory) / "settings.json")
            store.save(CliSettings(error_reporting=True, error_reporting_decided=False))
            loaded = store.load()

        self.assertFalse(loaded.error_reporting)
        self.assertFalse(loaded.error_reporting_decided)

    async def test_cli_prompt_persists_explicit_consent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = SettingsStore(Path(directory) / "settings.json")
            selector = MagicMock()
            selector.ask_async = AsyncMock(return_value=True)
            console = Console(file=StringIO(), force_terminal=False)
            questionary = SimpleNamespace(
                Choice=lambda label, value: (label, value),
                select=lambda *args, **kwargs: selector,
            )
            with patch.dict("sys.modules", {"questionary": questionary}):
                updated = await prompt_error_reporting_consent(
                    CliSettings(), store, console=console,
                )
            loaded = store.load()

        self.assertTrue(updated.error_reporting)
        self.assertTrue(updated.error_reporting_decided)
        self.assertTrue(loaded.error_reporting)
        self.assertTrue(loaded.error_reporting_decided)

    async def test_cancelled_cli_prompt_does_not_record_consent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = SettingsStore(Path(directory) / "settings.json")
            selector = MagicMock()
            selector.ask_async = AsyncMock(return_value=None)
            questionary = SimpleNamespace(
                Choice=lambda label, value: (label, value),
                select=lambda *args, **kwargs: selector,
            )
            with patch.dict("sys.modules", {"questionary": questionary}):
                updated = await prompt_error_reporting_consent(
                    CliSettings(),
                    store,
                    console=Console(file=StringIO(), force_terminal=False),
                )

        self.assertFalse(updated.error_reporting)
        self.assertFalse(updated.error_reporting_decided)
        self.assertFalse(store.path.exists())

    async def test_enabled_reporting_is_best_effort(self) -> None:
        with patch(
            "src.backend.error_reporting.report_public_error",
            new=AsyncMock(side_effect=RuntimeError("delivery failed")),
        ):
            report_id = await report_exception(
                RuntimeError("original"),
                operation="test",
                location="ErrorReportDeliveryTests",
                enabled=True,
            )
        self.assertEqual(len(report_id), 12)

    async def test_session_construction_failure_is_ignored(self) -> None:
        with patch(
            "src.backend.error_reporting.AsyncSession",
            side_effect=RuntimeError("session unavailable"),
        ):
            report_id = await report_exception(
                RuntimeError("original"),
                operation="test",
                location="ErrorReportDeliveryTests",
                enabled=True,
            )
        self.assertEqual(len(report_id), 12)


if __name__ == "__main__":
    unittest.main()
