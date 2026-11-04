from __future__ import annotations

import json
import tempfile
import traceback
import unittest
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from base_api.modules.errors import MediaLoadErrors
from rich.console import Console

from src.cli.settings import CliSettings, SettingsStore, prompt_error_reporting_consent
from src.shared.error_reporting import (
    ERROR_REPORT_CONSENT_VERSION,
    ERROR_REPORT_DISCLOSURE,
    ERROR_REPORT_EXAMPLE,
    MAX_BODY_BYTES,
    _payload_bytes,
    build_error_report,
    redact_log_text,
    report_exception,
    report_public_error,
    safe_url,
)


class ErrorReportFormattingTests(unittest.TestCase):
    def test_first_run_text_describes_the_actual_report(self) -> None:
        for detail in (
            "correlation ID", "UTC timestamp", "full Python traceback", "video URL",
            "query string", "cookies", "securely stored", "never shared with third parties",
            "used only to reproduce, diagnose and fix", "not anonymous",
        ):
            self.assertIn(detail, ERROR_REPORT_DISCLOSURE)
        self.assertIn('"video_url":', ERROR_REPORT_EXAMPLE)
        self.assertIn("Traceback (most recent call last):", ERROR_REPORT_EXAMPLE)

    def test_safe_url_preserves_reproduction_path_only(self) -> None:
        value = safe_url("https://user:password@example.com/watch/abc?token=secret#private")
        self.assertEqual(value, "https://example.com/")
        self.assertEqual(
            redact_log_text("https://example.com/home/alice/video"),
            "https://example.com/",
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
        self.assertIn("https://example.com/", redacted)

    def test_report_has_full_chained_traceback_and_reproduction_context(self) -> None:
        try:
            try:
                raise ValueError("original provider failure " + "漢" * 3000)
            except ValueError as cause:
                raise RuntimeError("synthetic failure") from cause
        except RuntimeError as error:
            expected_traceback = "".join(traceback.format_exception(error))
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
        self.assertIn("https://example.com/video/42?account=private", message)
        self.assertIn("error_type=RuntimeError", message)
        self.assertIn(expected_traceback, message)
        self.assertGreater(len(_payload_bytes(message)), 4096)
        self.assertEqual(set(json.loads(_payload_bytes(message))), {"message"})

    def test_media_source_failure_includes_its_own_traceback(self) -> None:
        try:
            raise ValueError("provider source failed")
        except ValueError as source_error:
            expected_traceback = "".join(traceback.format_exception(source_error))
            error = MediaLoadErrors((source_error,))

        message, _ = build_error_report(error, operation="load sources", location="provider")
        self.assertIn("MediaLoadErrors", message)
        self.assertIn("Media source failure 1:", message)
        self.assertIn(expected_traceback, message)


class ErrorReportDeliveryTests(unittest.IsolatedAsyncioTestCase):
    async def test_delivery_uses_exact_public_contract(self) -> None:
        message = (
            "video_url=https://example.com/watch?v=42&token=reproduction\n"
            + "traceback line 漢\n" * 500
            + "RuntimeError: original exception message\n"
        )
        session = AsyncMock()
        session.post.return_value.status_code = 204
        with patch("src.shared.error_reporting.AsyncSession", return_value=session):
            delivered = await report_public_error(message)

        self.assertTrue(delivered)
        _, kwargs = session.post.await_args
        self.assertEqual(json.loads(kwargs["content"]), {"message": message})
        self.assertFalse(kwargs["allow_redirects"])
        session.close.assert_awaited_once()

    async def test_oversized_report_is_not_silently_shortened(self) -> None:
        with patch("src.shared.error_reporting.AsyncSession") as session:
            self.assertFalse(await report_public_error("x" * MAX_BODY_BYTES))
        session.assert_not_called()

    async def test_disabled_reporting_does_not_send(self) -> None:
        with patch(
            "src.shared.error_reporting.report_public_error", new_callable=AsyncMock,
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
    async def test_existing_opt_in_requires_consent_for_detailed_reports(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = SettingsStore(Path(directory) / "settings.json")
            store.save(CliSettings(error_reporting=True, error_reporting_decided=True))
            loaded = store.load()

        self.assertFalse(loaded.error_reporting)
        self.assertFalse(loaded.error_reporting_decided)

    async def test_existing_opt_out_stays_disabled_without_another_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = SettingsStore(Path(directory) / "settings.json")
            store.save(CliSettings(error_reporting=False, error_reporting_decided=True))
            loaded = store.load()

        self.assertFalse(loaded.error_reporting)
        self.assertTrue(loaded.error_reporting_decided)

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
        self.assertEqual(loaded.error_reporting_consent_version, ERROR_REPORT_CONSENT_VERSION)

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
            "src.shared.error_reporting.report_public_error",
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
            "src.shared.error_reporting.AsyncSession",
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
