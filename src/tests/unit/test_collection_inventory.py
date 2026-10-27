"""Public source coverage cannot silently omit providers or invent fixtures."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.shared.provider_routing import COLLECTION_SEGMENTS, PROFILE_SEGMENTS
from src.tests.collection_cases import collection_cases
from src.tests.helper import MEDIA, ONLINE, SUITES
from src.tests.smoke.collections_gui import first_new_page_position, video_key


class CollectionInventoryTests(unittest.TestCase):
    def test_pornhub_identity_preserves_viewkey_without_tracking_parameters(self):
        first = "https://www.pornhub.com/view_video.php?viewkey=first"
        second = "https://www.pornhub.com/view_video.php?viewkey=second"
        self.assertNotEqual(video_key(first), video_key(second))
        self.assertEqual(video_key(first), video_key(first + "&utm_source=test&token=discarded"))
        self.assertEqual(video_key("https://www.xvideos.com/video.example/title?pl=123"),
                         video_key("https://www.xvideos.com/video.example/title?pl=456"))

    def test_partial_page_overlap_still_requires_a_genuinely_new_row(self):
        first = {"index": 0, "items": 4, "video_keys": ["a", "b", "c", "d"]}
        later = {"index": 1, "items": 4, "video_keys": ["c", "d", "e", "f"]}
        self.assertEqual(first_new_page_position([first, later]), 7)
        self.assertEqual(first_new_page_position([first, {**later, "video_keys": ["e", "f", "g", "h"]}]), 5)
        with self.assertRaisesRegex(AssertionError, "repeated the first page"):
            first_new_page_position([first, {**later, "video_keys": first["video_keys"]}])

    def test_all_supported_sources_have_explicit_states(self):
        cases = collection_cases()
        self.assertEqual({row["provider"] for row in cases if row["kind"] == "model"}, set(PROFILE_SEGMENTS))
        self.assertEqual({row["provider"] for row in cases if row["kind"] == "playlist"}, set(COLLECTION_SEGMENTS))
        self.assertEqual(len({row["id"] for row in cases}), len(cases))
        self.assertEqual([row["id"] for row in cases if row["status"] == "MANUAL"], ["spankbang.model"])
        self.assertEqual([row["id"] for row in cases if row["status"] == "UNVERIFIED"], ["thumbzilla.playlist"])
        self.assertTrue(all(row["url"] for row in cases if row["status"] == "AUTOMATED"))

    def test_fixture_overrides_validate_provider_and_content_kind(self):
        url = "https://www.redtube.com/playlist/273511"
        cases = collection_cases({"redtube.playlist": url})
        self.assertEqual(next(row["url"] for row in cases if row["id"] == "redtube.playlist"), url)
        for key, value in (("redtube.something", url), ("missing.playlist", url),
                           ("redtube.model", url), ("xvideos.playlist", url)):
            with self.subTest(key=key), self.assertRaises(ValueError):
                collection_cases({key: value})

    def test_manual_and_missing_only_runs_need_no_qt_network_or_media_tools(self):
        root = Path(__file__).resolve().parents[3]
        for arguments, state in ((["--provider", "spankbang"], "MANUAL"),
                                 (["--provider", "thumbzilla", "--kind", "playlist"], "UNVERIFIED")):
            with self.subTest(state=state), tempfile.TemporaryDirectory() as directory:
                report = Path(directory) / "result.json"
                result = subprocess.run([sys.executable, "-m", "src.tests.smoke.collections_gui", *arguments,
                                         "--report", str(report)], cwd=root, capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                data = json.loads(report.read_text())
                self.assertEqual(data["pass"], 0)
                self.assertEqual(data["results"][0]["status"], state)

    def test_helper_requires_both_network_and_media_confirmation(self):
        self.assertIn("collections_gui", ONLINE)
        self.assertIn("collections_gui", MEDIA)
        self.assertEqual(SUITES["collections_gui"][1][-1], "src.tests.smoke.collections_gui")
