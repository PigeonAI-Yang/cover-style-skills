from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PRODUCT_ROOT / "scripts" / "capture_bilibili_space.py"

spec = importlib.util.spec_from_file_location("capture_bilibili_space", SCRIPT)
assert spec and spec.loader
capture_bilibili_space = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture_bilibili_space)


class CaptureBilibiliSpaceTest(unittest.TestCase):
    def test_parse_page_count(self) -> None:
        self.assertEqual(
            capture_bilibili_space.parse_page_count("1\n2\n3\n下一页\n共 3 页 / 93 个，跳至\n页"),
            3,
        )
        self.assertIsNone(capture_bilibili_space.parse_page_count("no pagination"))

    def test_strip_image_transform(self) -> None:
        self.assertEqual(
            capture_bilibili_space.strip_image_transform(
                "https://i0.hdslb.com/bfs/archive/a.jpg@672w_378h_1c.webp"
            ),
            "https://i0.hdslb.com/bfs/archive/a.jpg",
        )

    def test_dedupe_and_rank(self) -> None:
        rows = [
            {
                "bv": "BV1",
                "url": "bad",
                "thumbnail_url": "https://i0.hdslb.com/a.jpg@672w.webp",
            },
            {"bv": "BV1", "thumbnail_url": "https://i0.hdslb.com/duplicate.jpg"},
            {"bv": "BV2", "thumbnail_url": "https://i0.hdslb.com/b.png"},
        ]
        deduped = capture_bilibili_space.dedupe_and_rank(rows)
        self.assertEqual([row["bv"] for row in deduped], ["BV1", "BV2"])
        self.assertEqual([row["rank"] for row in deduped], [1, 2])
        self.assertEqual(deduped[0]["url"], "https://www.bilibili.com/video/BV1/")
        self.assertEqual(deduped[0]["thumbnail_url"], "https://i0.hdslb.com/a.jpg")

    def test_compact_visible_stats(self) -> None:
        self.assertEqual(
            capture_bilibili_space.compact_visible_stats(
                "3374.2万 24.3万 07:34 【何同学】有多快？"
            ),
            "3374.2万 24.3万 07:34 【何同学】有多快？",
        )


if __name__ == "__main__":
    unittest.main()
