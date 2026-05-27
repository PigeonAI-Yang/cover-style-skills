#!/usr/bin/env python3
"""Capture Bilibili creator video cards through the local Chrome CDP proxy."""

from __future__ import annotations

import argparse
import datetime as dt
import json
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

ORDER_LABELS = {
    "latest": "最新发布",
    "most-played": "最多播放",
    "most-faved": "最多收藏",
}


class CaptureError(RuntimeError):
    """Raised when capture cannot proceed safely."""


def strip_image_transform(url: str) -> str:
    """Remove Bilibili image resize suffix such as @672w_378h_1c.webp."""
    return url.split("@", 1)[0]


def normalize_video_url(bv: str) -> str:
    return f"https://www.bilibili.com/video/{bv}/"


def parse_page_count(text: str) -> int | None:
    match = re.search(r"共\s*(\d+)\s*页", text)
    if not match:
        return None
    return int(match.group(1))


def dedupe_and_rank(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    output: list[dict[str, Any]] = []
    for row in rows:
        bv = str(row.get("bv") or "").strip()
        if not bv or bv in seen:
            continue
        normalized = dict(row)
        normalized["rank"] = len(output) + 1
        normalized["url"] = normalize_video_url(bv)
        normalized["thumbnail_url"] = strip_image_transform(
            str(normalized.get("thumbnail_url") or "")
        )
        output.append(normalized)
        seen.add(bv)
    return output


def compact_visible_stats(raw_text: str) -> str:
    return " ".join(raw_text.split()[:4])


def request_json(
    url: str,
    *,
    method: str = "GET",
    body: str | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    data = body.encode("utf-8") if body is not None else None
    request = urllib.request.Request(url, data=data, method=method)
    if body is not None:
        request.add_header("Content-Type", "text/plain; charset=utf-8")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise CaptureError(f"CDP proxy request failed: {url}: {exc}") from exc
    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CaptureError(f"CDP proxy returned non-JSON response: {payload[:200]}") from exc


class CdpClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def check(self) -> None:
        request_json(f"{self.base_url}/targets", timeout=10)

    def new_tab(self, url: str) -> str:
        encoded = urllib.parse.quote(url, safe="")
        payload = request_json(f"{self.base_url}/new?url={encoded}", timeout=60)
        target_id = payload.get("targetId")
        if not target_id:
            raise CaptureError(f"CDP proxy did not return targetId: {payload}")
        return str(target_id)

    def eval(self, target_id: str, script: str) -> Any:
        payload = request_json(
            f"{self.base_url}/eval?target={urllib.parse.quote(target_id)}",
            method="POST",
            body=script,
            timeout=60,
        )
        if "error" in payload:
            raise CaptureError(str(payload["error"]))
        return payload.get("value")

    def scroll_bottom(self, target_id: str) -> None:
        request_json(
            f"{self.base_url}/scroll?target={urllib.parse.quote(target_id)}&direction=bottom",
            timeout=30,
        )

    def close(self, target_id: str) -> None:
        request_json(
            f"{self.base_url}/close?target={urllib.parse.quote(target_id)}",
            timeout=30,
        )


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
        + f"-bilibili-cdp-{args.order}"
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


def click_order(client: CdpClient, target_id: str, label: str) -> None:
    script = f"""
(() => {{
  const label = {json.dumps(label, ensure_ascii=False)};
  const item = Array.from(document.querySelectorAll('.radio-filter__item, button, a, div'))
    .find((el) => (el.textContent || '').trim() === label);
  if (!item) return {{clicked: false, found: false, label, body: document.body.innerText.slice(0, 1000)}};
  item.click();
  return {{clicked: true, found: true, label}};
}})()
"""
    result = None
    deadline = time.monotonic() + 25
    while time.monotonic() < deadline:
        result = client.eval(target_id, script)
        if result and result.get("clicked"):
            time.sleep(2)
            return
        time.sleep(1)
    raise CaptureError(f"Could not click order filter {label!r}: {result}")


def click_page(client: CdpClient, target_id: str, page: int) -> None:
    script = f"""
(() => {{
  const page = String({page});
  const button = Array.from(document.querySelectorAll('.vui_pagenation--btn, button'))
    .find((el) => (el.textContent || '').trim() === page);
  if (!button) return {{clicked: false, page, footer: document.querySelector('.video-footer')?.innerText || ''}};
  button.click();
  return {{clicked: true, page}};
}})()
"""
    result = client.eval(target_id, script)
    if not result or not result.get("clicked"):
        raise CaptureError(f"Could not click page {page}: {result}")
    time.sleep(2)


def scroll_load(client: CdpClient, target_id: str, rounds: int) -> None:
    for _ in range(rounds):
        client.scroll_bottom(target_id)
        time.sleep(0.7)


def extract_page(client: CdpClient, target_id: str, page: int) -> dict[str, Any]:
    script = f"""
(() => {{
  const anchors = Array.from(document.querySelectorAll('a[href*="/video/"]'));
  const seen = new Set();
  const rows = [];
  for (const a of anchors) {{
    const href = a.href || '';
    const match = href.match(/\\/video\\/(BV[^/?#]+)/);
    const bv = match ? match[1] : '';
    if (!bv || seen.has(bv)) continue;
    const card = a.closest('.bili-video-card') ||
      a.closest('.upload-video-card') ||
      a.closest('.small-item') ||
      a.closest('li') ||
      a.closest('[class*="card"]') ||
      a.parentElement;
    const scope = card || a.parentElement;
    const img = scope ? scope.querySelector('img') : null;
    const rawText = ((scope ? scope.innerText : a.innerText) || '')
      .trim()
      .replace(/\\s+/g, ' ');
    const linkedTitles = Array.from(scope?.querySelectorAll('a[href*="/video/"]') || [])
      .map((x) => (x.innerText || '').trim())
      .filter(Boolean)
      .sort((x, y) => y.length - x.length);
    const title = ((img && img.alt) || linkedTitles[0] || '').trim();
    rows.push({{
      page: {page},
      page_rank: rows.length + 1,
      bv,
      url: `https://www.bilibili.com/video/${{bv}}/`,
      title,
      thumbnail_url: img ? ((img.currentSrc || img.src || '').split('@')[0]) : '',
      raw_text: rawText,
      visible_stats: rawText.split(/\\s+/).slice(0, 4).join(' ')
    }});
    seen.add(bv);
  }}
  return {{
    page: {page},
    href: location.href,
    title: document.title,
    pagination: (document.querySelector('.video-footer')?.innerText || '').trim(),
    active_filters: Array.from(document.querySelectorAll('.radio-filter__item'))
      .map((el) => {{ return {{text: (el.textContent || '').trim(), className: el.className}}; }}),
    count: rows.length,
    rows
  }};
}})()
"""
    result = client.eval(target_id, script)
    if not isinstance(result, dict):
        raise CaptureError(f"Unexpected extract result for page {page}: {result}")
    return result


def capture_video_rows(
    client: CdpClient,
    target_id: str,
    *,
    order_label: str,
    scroll_rounds: int,
    max_pages: int | None,
    max_videos: int | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    click_order(client, target_id, order_label)
    pages: list[dict[str, Any]] = []

    current_page = 1
    while True:
        scroll_load(client, target_id, scroll_rounds)
        page_data = extract_page(client, target_id, current_page)
        pages.append(page_data)

        page_count = parse_page_count(str(page_data.get("pagination") or "")) or current_page
        if max_pages is not None:
            page_count = min(page_count, max_pages)
        rows = dedupe_and_rank([row for page in pages for row in page.get("rows", [])])
        if max_videos is not None and len(rows) >= max_videos:
            return rows[:max_videos], pages
        if current_page >= page_count:
            return rows, pages
        current_page += 1
        click_page(client, target_id, current_page)


def write_capture_json(
    run_dir: Path,
    *,
    args: argparse.Namespace,
    pages: list[dict[str, Any]],
    videos: list[dict[str, Any]],
    space_url: str,
) -> Path:
    output = {
        "schema_version": 1,
        "creator_id": args.creator_id,
        "creator_name": args.creator_name,
        "source": "Bilibili space web page via Chrome CDP",
        "source_url": space_url,
        "order": args.order,
        "order_label": ORDER_LABELS[args.order],
        "captured_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "page_count": len(pages),
        "total_unique_videos": len(videos),
        "pages": pages,
        "videos": videos,
    }
    output_path = run_dir / "generated" / f"bilibili-cdp-{args.order}-videos.json"
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


def add_source(run_dir: Path, source_json: Path, space_url: str) -> None:
    run_manage(
        [
            "add-source",
            "--run-dir",
            str(run_dir),
            "--file",
            str(source_json),
            "--title",
            "Bilibili creator video cards captured via Chrome CDP",
            "--url",
            space_url,
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
            "cdp_source_json",
            "--value",
            source_json.relative_to(run_dir).as_posix(),
        ]
    )


def download_and_register_covers(
    run_dir: Path,
    videos: list[dict[str, Any]],
    *,
    referer: str,
    keep_cache: bool,
) -> dict[str, Any]:
    cache = run_dir / "generated" / "download-cache"
    failures: list[dict[str, Any]] = []
    registered = 0

    for video in videos:
        rank = int(video["rank"])
        bv = str(video["bv"])
        thumbnail_url = str(video.get("thumbnail_url") or "")
        if not thumbnail_url:
            failures.append({"rank": rank, "bv": bv, "error": "missing thumbnail_url"})
            continue

        temp_file = cache / f"{rank:03d}-{bv}{image_suffix(thumbnail_url)}"
        try:
            download_file(thumbnail_url, temp_file, referer=referer)
            selected_reason = (
                f"current Bilibili web CDP rank {rank} of {len(videos)}; "
                f"visible stats: {video.get('visible_stats') or compact_visible_stats(str(video.get('raw_text') or ''))}"
            )
            run_manage(
                [
                    "add-cover",
                    "--run-dir",
                    str(run_dir),
                    "--file",
                    str(temp_file),
                    "--video-title",
                    str(video.get("title") or bv),
                    "--video-url",
                    str(video.get("url") or normalize_video_url(bv)),
                    "--thumbnail-url",
                    thumbnail_url,
                    "--selected-reason",
                    selected_reason,
                    "--index",
                    str(rank),
                ]
            )
            registered += 1
            time.sleep(0.12)
        except Exception as exc:  # noqa: BLE001 - report and continue batch capture.
            failures.append(
                {
                    "rank": rank,
                    "bv": bv,
                    "title": video.get("title"),
                    "thumbnail_url": thumbnail_url,
                    "error": str(exc),
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
        if not str(resolved_cache).startswith(str(resolved_run)):
            raise CaptureError(f"Refusing to delete outside run dir: {resolved_cache}")
        shutil.rmtree(resolved_cache)
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
    parser = argparse.ArgumentParser(
        description="Capture Bilibili creator video cards via web-access Chrome CDP."
    )
    parser.add_argument("--creator-id", required=True)
    parser.add_argument("--creator-name", required=True)
    parser.add_argument("--mid", required=True, help="Bilibili creator mid")
    parser.add_argument("--run-id")
    parser.add_argument("--order", choices=sorted(ORDER_LABELS), default="most-played")
    parser.add_argument("--max-pages", type=int)
    parser.add_argument("--max-videos", type=int)
    parser.add_argument("--scroll-rounds", type=int, default=10)
    parser.add_argument("--cdp-proxy", default="http://localhost:3456")
    parser.add_argument("--force-run", action="store_true")
    parser.add_argument("--skip-cleanup", action="store_true")
    parser.add_argument("--no-download-covers", action="store_true")
    parser.add_argument("--keep-download-cache", action="store_true")
    parser.add_argument("--keep-tab", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    space_url = f"https://space.bilibili.com/{args.mid}/upload/video"
    run_dir = init_run(args)
    client = CdpClient(args.cdp_proxy)
    target_id: str | None = None

    try:
        client.check()
        target_id = client.new_tab(space_url)
        videos, pages = capture_video_rows(
            client,
            target_id,
            order_label=ORDER_LABELS[args.order],
            scroll_rounds=args.scroll_rounds,
            max_pages=args.max_pages,
            max_videos=args.max_videos,
        )
        source_json = write_capture_json(
            run_dir,
            args=args,
            pages=pages,
            videos=videos,
            space_url=space_url,
        )
        add_source(run_dir, source_json, space_url)

        cover_result = {"registered": 0, "failed": 0, "failure_path": None}
        contact_sheet = None
        if not args.no_download_covers:
            cover_result = download_and_register_covers(
                run_dir,
                videos,
                referer=space_url,
                keep_cache=args.keep_download_cache,
            )
            contact_sheet = generate_contact_sheet(run_dir)

        print(
            json.dumps(
                {
                    "run_dir": str(run_dir),
                    "source_json": str(source_json),
                    "videos": len(videos),
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
    finally:
        if target_id and not args.keep_tab:
            try:
                client.close(target_id)
            except Exception:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
