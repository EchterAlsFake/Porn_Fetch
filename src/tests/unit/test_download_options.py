"""Explicit unusual-title fixtures; these are filesystem tests, not fake media."""
from __future__ import annotations

import tempfile
import unicodedata
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

from src.shared.download_options import filename_component, title_template, video_file_path, video_output_path
from src.shared.media import VideoFilters

TITLES = (
    "日本語のタイトル・中文・한국어", "Русский заголовок — українська", "عنوان عربي بالعربية",
    "Grüße & déjà vu — español ¿sí?", "Emoji 👩🏽‍💻 ❤️ 👨‍👩‍👧‍👦", "Cafe\u0301 et re\u0301sume\u0301",
    "Before / middle | after \\ tail", '<tag> & "quotes" : * ? | / \\',
    "../../outside/keep-the-whole-title", "C:\\Windows\\title", "CON", "NUL.txt", "COM1", "LPT9.mp4",
    "...   ", "control\x00\x01\n\r\tend", "Cost $5 ${video_id}", "Dr. Example. Part 2",
    "Full width Ａ／Ｂ：Ｃ", "direction\u202etxt.exe", "長い題名🙂" * 120, "~", "~root", "A/B", "A|B",
)


class DownloadOptionsTests(unittest.TestCase):
    def video(self, title="Example", **overrides):
        values = dict(title=title, author="Studio / Channel | Name", video_id="id/42", length=12,
                      publish_date=datetime(2026, 10, 27, 22, 45, tzinfo=timezone.utc))
        return SimpleNamespace(**(values | overrides))

    def test_unusual_titles_create_real_portable_files_without_losing_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            for index, title in enumerate(TITLES, 1):
                with self.subTest(title=title[:60]):
                    video = self.video(title)
                    path = video_file_path(video_output_path(video, index, "$index-$title", base))
                    self.assertEqual(path.parent, base)
                    self.assertLessEqual(len(path.name.encode("utf-8")), 244)
                    self.assertNotRegex(path.name, r'[<>:"/\\|?*\x00-\x1f\x7f]')
                    path.write_bytes(b"explicit filename fixture")
                    self.assertTrue(path.is_file())
                    self.assertEqual(video.title, title, "Output sanitation must not mutate display/filter metadata")

    def test_preserves_unicode_and_both_sides_of_separators(self):
        self.assertEqual(filename_component("Before / after | final"), "Before _ after _ final")
        for title in TITLES[:6]:
            self.assertEqual(filename_component(title), unicodedata.normalize("NFC", title).replace("?", "_"))
        self.assertEqual(filename_component("NUL.txt"), "_NUL.txt")
        self.assertEqual(filename_component("..."), "untitled")

    def test_long_titles_remain_distinct_after_truncation(self):
        prefix = "長い題名🙂" * 120
        self.assertNotEqual(filename_component(prefix + "a"), filename_component(prefix + "b"))

    def test_index_distinguishes_titles_that_sanitize_to_the_same_name(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = [video_output_path(self.video(title), index, "$index-$title", directory)
                     for index, title in enumerate(("A/B", "A|B"), 1)]
            self.assertNotEqual(*paths)

    def test_template_fields_dates_literals_and_explicit_folders(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            video = self.video("Before/After | Last")
            path = video_output_path(video, 3, "$output_path/$author/${index}_${title}_${video_id}_$publish_date-$length-$$", base)
            self.assertEqual(path, base / "Studio _ Channel _ Name" /
                             "03_Before_After _ Last_id_42_2026-10-27-12-$")
            self.assertEqual(video_output_path(video, 1, str(base / "explicit" / "$title"), base).parent,
                             base / "explicit")
            unknown = video_output_path(self.video(publish_date=None, length=None), 1, "$publish_date-$length", base)
            self.assertEqual(unknown.name, "unknown-unknown")

    def test_templates_reject_typos_and_traversal(self):
        for pattern in ("$unknown", "${title", "$", "${publish_date:%Y}", "$title/"):
            with self.subTest(pattern=pattern), self.assertRaises(ValueError):
                title_template(pattern)
        with tempfile.TemporaryDirectory() as directory, self.assertRaises(ValueError):
            video_output_path(self.video(), 1, "../$title", directory)

    def test_media_extension_survives_dots_and_long_unicode(self):
        self.assertEqual(video_file_path(Path("Dr. Example. Part 2")).name, "Dr. Example. Part 2.mp4")
        self.assertEqual(video_file_path(Path("movie.MP4")).name, "movie.MP4")

    def test_invalid_filters_fail_before_loading_any_video(self):
        for values in ({"title_regex": "["}, {"author_regex": "("}, {"tags_regex": "a{2,1}"},
                       {"duration_minimum": 10, "duration_maximum": 5},
                       {"quality_minimum": "4k", "quality_maximum": "1440p"},
                       {"published_after": "2026-02-30"},
                       {"published_after": "2026-10-28", "published_before": "2026-10-27"},
                       {"start_index": 3, "end_index": 2}):
            with self.subTest(values=values), self.assertRaises(ValueError):
                VideoFilters(**values).validate()
        self.assertEqual(VideoFilters.quality_value("4k"), 2160)
