"""The list model must preserve the shared model's duration unit."""
import unittest
from types import SimpleNamespace

from src.backend.download_manager import DownloadListModel
from src.shared.provider_parsing import parse_length


class DownloadDurationTests(unittest.TestCase):
    def test_normalized_minutes_are_not_formatted_as_seconds(self):
        model = DownloadListModel()
        for index, (length, expected) in enumerate([(parse_length(720, "pornhub"), "12 min"), (None, "N/A")]):
            video = SimpleNamespace(length=length, qualities=[720], selected_quality=None,
                                    identifier=str(index), video_id=str(index), index=None,
                                    title="Example", author="Example")
            model.add_video(video, "720")
            self.assertEqual(model.data(model.index(index, 0), model.DurationRole), expected)
