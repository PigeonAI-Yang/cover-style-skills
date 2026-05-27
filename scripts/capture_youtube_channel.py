#!/usr/bin/env python3
"""Capture YouTube channel video cards into a managed research run."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
MANAGE_WORKSPACE = PRODUCT_ROOT / "scripts" / "manage_research_workspace.py"


class CaptureError(RuntimeError):
    """Raised when YouTube capture cannot proceed safely."""


def build_channel_videos_url(channel_id: str) -> str:
    return f"https://www.youtube.com/channel/{channel_id}/videos"


def extract_json_object_after(text: str, marker: str) -> dict[str, Any]:
    match = re.search(marker, text)
    if not match:
        raise CaptureError(f"marker not found: {marker}")
    start = match.end()
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(text[start:], start):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : index + 1])
    raise CaptureError("unterminated JSON object")


def find_regex(text: str, pattern: str, default: str | None = None) -> str:
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    if default is not None:
        return default
    raise CaptureError(f"pattern not found: {pattern}")


def request_text(url: str, *, timeout: int = 30) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8")


def request_json(url: str, body: dict[str, Any], *, timeout: int = 30) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
            "Content-Type": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def collect_by_key(value: Any, key: str) -> list[Any]:
    output: list[Any] = []
    if isinstance(value, dict):
        if key in value:
            output.append(value[key])
        for child in value.values():
            output.extend(collect_by_key(child, key))
    elif isinstance(value, list):
        for child in value:
            output.extend(collect_by_key(child, key))
    return output


def collect_lockups(value: Any) -> list[dict[str, Any]]:
    return [
        item
        for item in collect_by_key(value, "lockupViewModel")
        if isinstance(item, dict)
        and item.get("contentType") == "LOCKUP_CONTENT_TYPE_VIDEO"
        and item.get("contentId")
    ]


def collect_content_strings(value: Any) -> list[str]:
    output: list[str] = []
    if isinstance(value, dict):
        content = value.get("content")
        if isinstance(content, str) and content.strip():
            output.append(content.strip())
        text = value.get("text")
        if isinstance(text, str) and text.strip():
            output.append(text.strip())
        simple_text = value.get("simpleText")
        if isinstance(simple_text, str) and simple_text.strip():
            output.append(simple_text.strip())
        for child in value.values():
            output.extend(collect_content_strings(child))
    elif isinstance(value, list):
        for child in value:
            output.extend(collect_content_strings(child))
    return output


def get_video_title(lockup: dict[str, Any]) -> str:
    title = (
        lockup.get("metadata", {})
        .get("lockupMetadataViewModel", {})
        .get("title", {})
        .get("content")
    )
    return str(title or lockup.get("contentId") or "").strip()


def get_metadata_text(lockup: dict[str, Any]) -> str:
    metadata = (
        lockup.get("metadata", {})
        .get("lockupMetadataViewModel", {})
        .get("metadata", {})
        .get("contentMetadataViewModel", {})
        .get("metadataRows", [])
    )
    values: list[str] = []
    for value in collect_content_strings(metadata):
        if value not in values:
            values.append(value)
    return " | ".join(values[:8])


def get_thumbnail_url(lockup: dict[str, Any]) -> str:
    video_id = str(lockup.get("contentId") or "")
    maxres = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
    sources = (
        lockup.get("contentImage", {})
        .get("thumbnailViewModel", {})
        .get("image", {})
        .get("sources", [])
    )
    if not isinstance(sources, list):
        return maxres
    source_urls = [
        str(item.get("url") or "")
        for item in sorted(
            [source for source in sources if isinstance(source, dict)],
            key=lambda item: int(item.get("width") or 0),
            reverse=True,
        )
    ]
    return maxres if video_id else next((url for url in source_urls if url), "")


def lockup_to_row(lockup: dict[str, Any]) -> dict[str, Any]:
    video_id = str(lockup.get("contentId") or "").strip()
    title = get_video_title(lockup)
    return {
        "video_id": video_id,
        "title": title,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "thumbnail_url": get_thumbnail_url(lockup),
        "metadata": get_metadata_text(lockup),
    }


def dedupe_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    output: list[dict[str, Any]] = []
    for row in rows:
        video_id = str(row.get("video_id") or "")
        if not video_id or video_id in seen:
            continue
        normalized = dict(row)
        normalized["rank"] = len(output) + 1
        output.append(normalized)
        seen.add(video_id)
    return output


def find_chip_token(initial_data: dict[str, Any], label: str) -> str:
    chips = [
        chip for chip in collect_by_key(initial_data, "chipViewModel") if isinstance(chip, dict)
    ]
    for chip in chips:
        if str(chip.get("text") or "").strip().lower() == label.strip().lower():
            token = (
                chip.get("tapCommand", {})
                .get("innertubeCommand", {})
                .get("continuationCommand", {})
                .get("token")
            )
            if token:
                return str(token)
    available = [str(chip.get("text") or "") for chip in chips]
    raise CaptureError(f"chip {label!r} not found; available chips: {available}")


def find_next_grid_continuation(response: dict[str, Any]) -> str | None:
    endpoints: list[tuple[str, str]] = []

    def walk(value: Any, path: str = "") -> None:
        if isinstance(value, dict):
            command = value.get("continuationCommand")
            if isinstance(command, dict) and command.get("token"):
                endpoints.append((path, str(command["token"])))
            for key, child in value.items():
                walk(child, f"{path}/{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{path}[{index}]")

    walk(response)
    for path, token in endpoints:
        if "continuationItemRenderer" in path:
            return token
    return None


def parse_initial_page(html: str) -> tuple[dict[str, Any], str, dict[str, Any]]:
    initial_data = extract_json_object_after(html, r"var ytInitialData\s*=\s*")
    api_key = find_regex(html, r'"INNERTUBE_API_KEY":"([^"]+)"')
    client_version = find_regex(html, r'"INNERTUBE_CONTEXT_CLIENT_VERSION":"([^"]+)"')
    visitor_data = find_regex(html, r'"VISITOR_DATA":"([^"]+)"', "")
    context = {
        "client": {
            "clientName": "WEB",
            "clientVersion": client_version,
            "hl": "en",
            "gl": "US",
            "visitorData": visitor_data,
        }
    }
    return initial_data, api_key, context


def capture_rows(
    *,
    channel_id: str,
    chip_label: str,
    max_videos: int,
    max_pages: int | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
    channel_url = build_channel_videos_url(channel_id)
    html = request_text(channel_url, timeout=45)
    initial_data, api_key, context = parse_initial_page(html)
    token = find_chip_token(initial_data, chip_label)

    rows: list[dict[str, Any]] = []
    pages: list[dict[str, Any]] = []
    page_index = 0

    while token:
        if max_pages is not None and page_index >= max_pages:
            break
        page_index += 1
        response = request_json(
            f"https://www.youtube.com/youtubei/v1/browse?key={api_key}",
            {"context": context, "continuation": token},
            timeout=45,
        )
        page_lockups = collect_lockups(response)
        page_rows = [lockup_to_row(lockup) for lockup in page_lockups]
        pages.append(
            {
                "page": page_index,
                "video_count": len(page_rows),
                "first_title": page_rows[0]["title"] if page_rows else "",
                "last_title": page_rows[-1]["title"] if page_rows else "",
            }
        )
        rows = dedupe_rows([*rows, *page_rows])
        if len(rows) >= max_videos:
            return rows[:max_videos], pages, channel_url
        token = find_next_grid_continuation(response)
        time.sleep(0.35)

    return rows[:max_videos], pages, channel_url


def run_manage(args: list[str]) -> str:
    result = subprocess.run(
        [sys.executable, str(MANAGE_WORKSPACE), *args],
        cwd=PRODUCT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if result.returncode != 0:
        raise CaptureError(
            "manage_research_workspace.py failed\n"
            f"ARGS: {' '.join(args)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result.stdout.strip()


def init_run(args: argparse.Namespace) -> Path:
    if not args.skip_cleanup:
        run_manage(["cleanup"])
    run_id = args.run_id or (
        dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        + f"-youtube-{args.chip_label.lower()}-top{args.max_videos}"
    )
    command = [
        "init",
        "--creator-id",
        args.creator_id,
        "--creator-name",
        args.creator_name,
        "--run-id",
        run_id,
    ]
    if args.force_run:
        command.append("--force")
    return Path(run_manage(command)).resolve()


def write_capture_json(
    run_dir: Path,
    *,
    args: argparse.Namespace,
    rows: list[dict[str, Any]],
    pages: list[dict[str, Any]],
    channel_url: str,
) -> Path:
    output = {
        "schema_version": 1,
        "creator_id": args.creator_id,
        "creator_name": args.creator_name,
        "source": "YouTube channel Videos tab via static HTML and youtubei browse continuations",
        "source_url": channel_url,
        "channel_id": args.channel_id,
        "chip_label": args.chip_label,
        "captured_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "page_count": len(pages),
        "total_unique_videos": len(rows),
        "pages": pages,
        "videos": rows,
    }
    output_path = run_dir / "generated" / f"youtube-{args.chip_label.lower()}-top{len(rows)}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path


def download_file(url: str, target: Path, *, referer: str) -> None:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
            "Referer": referer,
        },
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(request, timeout=30) as response:
        target.write_bytes(response.read())


def image_suffix(url: str) -> str:
    suffix = Path(urllib.parse.urlparse(url).path).suffix.lower()
    return suffix if suffix in {".jpg", ".jpeg", ".png", ".webp"} else ".jpg"


def fallback_thumbnail_urls(video_id: str, preferred: str) -> list[str]:
    candidates = [
        preferred,
        f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg",
        f"https://i.ytimg.com/vi/{video_id}/sddefault.jpg",
        f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
    ]
    output: list[str] = []
    for candidate in candidates:
        if candidate and candidate not in output:
            output.append(candidate)
    return output


def add_source(run_dir: Path, source_json: Path, channel_url: str) -> None:
    run_manage(
        [
            "add-source",
            "--run-dir",
            str(run_dir),
            "--file",
            str(source_json),
            "--title",
            "YouTube channel video cards captured via static HTML and youtubei",
            "--url",
            channel_url,
            "--source-type",
            "data",
        ]
    )
    run_manage(
        [
            "set-artifact",
            "--run-dir",
            str(run_dir),
            "--key",
            "youtube_source_json",
            "--value",
            source_json.relative_to(run_dir).as_posix(),
        ]
    )


def compact_slug(value: str, fallback: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return (value or fallback)[:80].strip("-") or fallback


def download_and_register_covers(
    run_dir: Path,
    rows: list[dict[str, Any]],
    *,
    referer: str,
    keep_cache: bool,
) -> dict[str, Any]:
    cache = run_dir / "generated" / "download-cache"
    failures: list[dict[str, Any]] = []
    registered = 0

    for row in rows:
        rank = int(row["rank"])
        video_id = str(row["video_id"])
        temp_file: Path | None = None
        used_url = ""
        error_messages: list[str] = []
        for thumbnail_url in fallback_thumbnail_urls(video_id, str(row.get("thumbnail_url") or "")):
            temp_file = cache / f"{rank:03d}-{video_id}{image_suffix(thumbnail_url)}"
            try:
                download_file(thumbnail_url, temp_file, referer=referer)
                used_url = thumbnail_url
                break
            except Exception as exc:  # noqa: BLE001 - try fallback image URLs.
                error_messages.append(f"{thumbnail_url}: {exc}")
                temp_file = None
        if temp_file is None or not temp_file.exists():
            failures.append(
                {
                    "rank": rank,
                    "video_id": video_id,
                    "title": row.get("title"),
                    "thumbnail_url": row.get("thumbnail_url"),
                    "errors": error_messages,
                }
            )
            continue
        try:
            selected_reason = (
                f"YouTube {row.get('chip_label') or 'Popular'} rank {rank} of {len(rows)}; "
                f"metadata: {row.get('metadata') or ''}"
            )
            run_manage(
                [
                    "add-cover",
                    "--run-dir",
                    str(run_dir),
                    "--file",
                    str(temp_file),
                    "--video-title",
                    str(row.get("title") or video_id),
                    "--video-url",
                    str(row.get("url") or f"https://www.youtube.com/watch?v={video_id}"),
                    "--thumbnail-url",
                    used_url,
                    "--selected-reason",
                    selected_reason,
                    "--index",
                    str(rank),
                ]
            )
            registered += 1
            time.sleep(0.08)
        except Exception as exc:  # noqa: BLE001 - report and continue.
            failures.append(
                {
                    "rank": rank,
                    "video_id": video_id,
                    "title": row.get("title"),
                    "thumbnail_url": used_url,
                    "errors": [str(exc)],
                }
            )

    failure_path = run_dir / "generated" / "cover-download-failures.json"
    failure_path.write_text(
        json.dumps(failures, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if cache.exists() and not keep_cache:
        resolved_cache = cache.resolve()
        resolved_run = run_dir.resolve()
        if not os.path.commonpath([resolved_cache, resolved_run]) == str(resolved_run):
            raise CaptureError(f"Refusing to delete outside run dir: {resolved_cache}")
        shutil.rmtree(cache)
    return {"registered": registered, "failed": len(failures), "failure_path": failure_path}


def generate_contact_sheet(run_dir: Path) -> Path | None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return None

    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    covers = sorted(manifest.get("covers", []), key=lambda item: int(item["index"]))
    if not covers:
        return None

    thumb_w, thumb_h = 240, 135
    label_h = 34
    cols = 5
    rows = (len(covers) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "white")
    draw = ImageDraw.Draw(sheet)

    font = ImageFont.load_default()
    for candidate in [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]:
        if candidate.exists():
            try:
                font = ImageFont.truetype(str(candidate), 13)
                break
            except Exception:
                pass

    for entry in covers:
        idx = int(entry["index"]) - 1
        x = (idx % cols) * thumb_w
        y = (idx // cols) * (thumb_h + label_h)
        with Image.open(run_dir / entry["local_path"]) as image:
            image = image.convert("RGB")
            image.thumbnail((thumb_w, thumb_h), Image.LANCZOS)
            canvas = Image.new("RGB", (thumb_w, thumb_h), (245, 245, 245))
            canvas.paste(image, ((thumb_w - image.width) // 2, (thumb_h - image.height) // 2))
        sheet.paste(canvas, (x, y))
        label = f"{int(entry['index']):03d} {entry['video_title'][:18]}"
        draw.rectangle([x, y + thumb_h, x + thumb_w, y + thumb_h + label_h], fill=(250, 250, 250))
        draw.text((x + 4, y + thumb_h + 4), label, fill=(0, 0, 0), font=font)

    output = run_dir / "distillation" / "sample-contact-sheet.jpg"
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)
    run_manage(
        [
            "set-artifact",
            "--run-dir",
            str(run_dir),
            "--key",
            "contact_sheet",
            "--value",
            output.relative_to(run_dir).as_posix(),
        ]
    )
    return output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Capture a YouTube channel's video cards.")
    parser.add_argument("--creator-id", required=True)
    parser.add_argument("--creator-name", required=True)
    parser.add_argument("--channel-id", required=True)
    parser.add_argument("--run-id")
    parser.add_argument("--chip-label", default="Popular")
    parser.add_argument("--max-pages", type=int)
    parser.add_argument("--max-videos", type=int, default=120)
    parser.add_argument("--force-run", action="store_true")
    parser.add_argument("--skip-cleanup", action="store_true")
    parser.add_argument("--no-download-covers", action="store_true")
    parser.add_argument("--keep-download-cache", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    run_dir = init_run(args)
    rows, pages, channel_url = capture_rows(
        channel_id=args.channel_id,
        chip_label=args.chip_label,
        max_videos=args.max_videos,
        max_pages=args.max_pages,
    )
    for row in rows:
        row["chip_label"] = args.chip_label
    source_json = write_capture_json(
        run_dir,
        args=args,
        rows=rows,
        pages=pages,
        channel_url=channel_url,
    )
    add_source(run_dir, source_json, channel_url)

    cover_result = {"registered": 0, "failed": 0, "failure_path": None}
    contact_sheet = None
    if not args.no_download_covers:
        cover_result = download_and_register_covers(
            run_dir,
            rows,
            referer=channel_url,
            keep_cache=args.keep_download_cache,
        )
        contact_sheet = generate_contact_sheet(run_dir)

    print(
        json.dumps(
            {
                "run_dir": str(run_dir),
                "source_json": str(source_json),
                "videos": len(rows),
                "pages": len(pages),
                "covers_registered": cover_result["registered"],
                "cover_failures": cover_result["failed"],
                "failure_path": str(cover_result["failure_path"])
                if cover_result["failure_path"]
                else None,
                "contact_sheet": str(contact_sheet) if contact_sheet else None,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
