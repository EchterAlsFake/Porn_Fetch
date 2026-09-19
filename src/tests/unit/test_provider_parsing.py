"""Focused tests for provider date and duration normalization."""

import unittest
from datetime import timezone

from src.shared.provider_parsing import parse_length, parse_publish_date


class DurationParsingTests(unittest.TestCase):
    def test_common_duration_formats(self):
        self.assertEqual(parse_length("16:19"), 16)
        self.assertEqual(parse_length("1h 2m 3s"), 62)
        self.assertEqual(parse_length("PT11M42S"), 12)

    def test_provider_numeric_units(self):
        self.assertEqual(parse_length(120, video_source="pornhub"), 2)
        self.assertEqual(parse_length(12, video_source="xnxx"), 12)

    def test_missing_duration(self):
        self.assertIsNone(parse_length(None))
        self.assertIsNone(parse_length("not available"))


class PublishDateParsingTests(unittest.TestCase):
    def test_iso_date_is_normalized_to_utc(self):
        parsed = parse_publish_date("2026-09-19T12:30:00+02:00")

        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.tzinfo, timezone.utc)
        self.assertEqual(parsed.hour, 10)

    def test_human_readable_and_missing_dates(self):
        self.assertEqual(
            parse_publish_date("Published on September 17, 2024").date().isoformat(),
            "2024-09-17",
        )
        self.assertIsNone(parse_publish_date("N/A"))


if __name__ == "__main__":
    unittest.main()
