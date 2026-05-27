from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PRODUCT_ROOT / "scripts" / "capture_youtube_channel.py"

spec = importlib.util.spec_from_file_location("capture_youtube_channel", SCRIPT)
assert spec and spec.loader
capture_youtube_channel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture_youtube_channel)


class CaptureYouTubeChannelTest(unittest.TestCase):
    def test_build_channel_videos_url(self) -> None:
        self.assertEqual(
            capture_youtube_channel.build_channel_videos_url("UC123"),
            "https://www.youtube.com/channel/UC123/videos",
        )

    def test_extract_json_object_after(self) -> None:
        value = capture_youtube_channel.extract_json_object_after(
            'x var ytInitialData = {"a":{"b":1},"c":"}"}; y',
            r"var ytInitialData\s*=\s*",
        )
        self.assertEqual(value, {"a": {"b": 1}, "c": "}"})

    def test_find_chip_token(self) -> None:
        data = {
            "chipViewModel": {
                "text": "Popular",
                "tapCommand": {
                    "innertubeCommand": {
                        "continuationCommand": {"token": "TOKEN"}
                    }
                },
            }
        }
        self.assertEqual(capture_youtube_channel.find_chip_token(data, "Popular"), "TOKEN")

    def test_dedupe_rows(self) -> None:
        rows = [
            {"video_id": "a", "title": "A"},
            {"video_id": "a", "title": "A duplicate"},
            {"video_id": "b", "title": "B"},
        ]
        output = capture_youtube_channel.dedupe_rows(rows)
        self.assertEqual([row["video_id"] for row in output], ["a", "b"])
        self.assertEqual([row["rank"] for row in output], [1, 2])


if __name__ == "__main__":
    unittest.main()
