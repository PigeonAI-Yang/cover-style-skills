#!/usr/bin/env python3
"""Verify generated cover image dimensions against PigeonYang platform presets."""

from __future__ import annotations

import argparse
import struct
from pathlib import Path


PRESETS = {
    "youtube-long": (1280, 720),
    "bilibili-native": (1146, 717),
    "bilibili-16x9": (1920, 1080),
    "bilibili-4x3": (1440, 1080),
    "douyin-horizontal": (1440, 1080),
    "douyin-vertical": (1080, 1440),
    "xiaohongshu-portrait": (1080, 1440),
    "xiaohongshu-square": (1080, 1080),
    "tiktok-reels-shorts": (1080, 1920),
    "wechat-video-6x7": (1080, 1260),
    "wechat-video-3x4": (1080, 1440),
    "wechat-article-main": (2350, 1000),
    "wechat-article-square": (1080, 1080),
}


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        header = f.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("not a PNG file")
    return struct.unpack(">II", header[16:24])


def jpeg_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG file")
    i = 2
    while i < len(data):
        while i < len(data) and data[i] == 0xFF:
            i += 1
        if i >= len(data):
            break
        marker = data[i]
        i += 1
        if marker in {0xD8, 0xD9, 0x01} or 0xD0 <= marker <= 0xD7:
            continue
        if i + 2 > len(data):
            break
        segment_len = struct.unpack(">H", data[i : i + 2])[0]
        if segment_len < 2 or i + segment_len > len(data):
            break
        if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
            if segment_len < 7:
                break
            height = struct.unpack(">H", data[i + 3 : i + 5])[0]
            width = struct.unpack(">H", data[i + 5 : i + 7])[0]
            return width, height
        i += segment_len
    raise ValueError("could not find JPEG size")


def image_size(path: Path) -> tuple[int, int]:
    suffix = path.suffix.lower()
    if suffix == ".png":
        return png_size(path)
    if suffix in {".jpg", ".jpeg"}:
        return jpeg_size(path)
    raise ValueError(f"unsupported image format: {suffix}")


def parse_size(value: str) -> tuple[int, int]:
    parts = value.lower().replace(" ", "").split("x")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("size must look like 1080x1440")
    try:
        width, height = int(parts[0]), int(parts[1])
    except ValueError as exc:
        raise argparse.ArgumentTypeError("size must contain integers") from exc
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("size values must be positive")
    return width, height


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preset", choices=sorted(PRESETS))
    group.add_argument("--size", type=parse_size, help="Expected size, for example 1080x1440")
    parser.add_argument(
        "--ratio-only",
        action="store_true",
        help="Accept any dimensions with the same aspect ratio as the target size.",
    )
    parser.add_argument("--tolerance", type=float, default=0.003, help="Ratio tolerance.")
    args = parser.parse_args()

    path = args.image.resolve()
    if not path.exists():
        raise FileNotFoundError(path)

    actual = image_size(path)
    expected = PRESETS[args.preset] if args.preset else args.size

    if args.ratio_only:
        actual_ratio = actual[0] / actual[1]
        expected_ratio = expected[0] / expected[1]
        ok = abs(actual_ratio - expected_ratio) <= args.tolerance
    else:
        ok = actual == expected

    print(f"image={path}")
    print(f"actual={actual[0]}x{actual[1]}")
    print(f"expected={expected[0]}x{expected[1]}")
    print(f"mode={'ratio' if args.ratio_only else 'exact'}")
    print(f"status={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

