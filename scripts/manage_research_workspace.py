#!/usr/bin/env python3
"""Manage PigeonYang cover-style research workspaces and retention."""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import re
import shutil
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


CONFIG_PATH = (
    Path.home()
    / ".codex"
    / "pigeonyang-cover-style-distiller"
    / "config.json"
)
TZ = ZoneInfo("Asia/Shanghai")


def now() -> datetime:
    return datetime.now(TZ)


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    if not value:
        raise ValueError("value must contain at least one ASCII letter or digit")
    return value


def iso(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def read_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_manifest(path: Path, data: dict) -> None:
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temp_path, path)


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def save_config(data: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    temp_path = CONFIG_PATH.with_suffix(CONFIG_PATH.suffix + ".tmp")
    temp_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temp_path, CONFIG_PATH)


def resolve_root(args: argparse.Namespace) -> Path:
    if getattr(args, "root", None):
        return args.root.resolve()
    config = load_config()
    configured = config.get("workspace_root")
    if configured:
        return Path(configured).expanduser().resolve()
    raise SystemExit(
        "No workspace root configured. Run: "
        "python manage_research_workspace.py set-root --workspace-root <path>"
    )


@contextlib.contextmanager
def manifest_lock(run_dir: Path):
    lock_path = run_dir / "manifest.json.lock"
    deadline = time.monotonic() + 30
    fd = None
    while time.monotonic() < deadline:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.write(fd, str(os.getpid()).encode("ascii"))
            break
        except FileExistsError:
            time.sleep(0.1)
    if fd is None:
        raise TimeoutError(f"timed out waiting for manifest lock: {lock_path}")
    try:
        yield
    finally:
        os.close(fd)
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def compact_slug(value: str, fallback: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return (value or fallback)[:80].strip("-") or fallback


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    for counter in range(2, 1000):
        candidate = path.with_name(f"{stem}-{counter}{suffix}")
        if not candidate.exists():
            return candidate
    raise FileExistsError(f"could not create unique path for {path}")


def manifest_for_run(run_dir: Path) -> tuple[Path, dict]:
    manifest_path = run_dir.resolve() / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"manifest not found: {manifest_path}")
    return manifest_path, read_manifest(manifest_path)


def command_init(args: argparse.Namespace) -> int:
    creator_id = slugify(args.creator_id)
    created = now()
    run_id = args.run_id or created.strftime("%Y%m%d-%H%M%S")
    root = resolve_root(args)
    run_dir = root / creator_id / run_id

    if run_dir.exists() and not args.force:
        raise FileExistsError(f"{run_dir} already exists; pass --force to reuse it")

    for child in [
        "covers",
        "sources/articles",
        "sources/transcripts",
        "sources/pages",
        "distillation",
        "prompts",
        "generated",
    ]:
        (run_dir / child).mkdir(parents=True, exist_ok=True)

    manifest_path = run_dir / "manifest.json"
    if not manifest_path.exists() or args.force:
        manifest = {
            "schema_version": 1,
            "creator_id": creator_id,
            "creator_name": args.creator_name,
            "run_id": run_id,
            "created_at": iso(created),
            "retention": {
                "covers_delete_after_days": args.covers_delete_after_days,
                "sources_delete_after_days": args.sources_delete_after_days,
                "distillation": "keep",
                "prompts": "keep",
                "generated": "keep",
            },
            "covers": [],
            "process_sources": [],
            "artifacts": {
                "research_md": "distillation/research.md",
                "child_skill": None,
            },
        }
        write_manifest(manifest_path, manifest)

    print(run_dir)
    return 0


def command_set_root(args: argparse.Namespace) -> int:
    workspace_root = args.workspace_root.expanduser().resolve()
    if workspace_root.exists() and not workspace_root.is_dir():
        raise NotADirectoryError(workspace_root)
    if not workspace_root.exists():
        workspace_root.mkdir(parents=True, exist_ok=True)

    data = load_config()
    data["workspace_root"] = str(workspace_root)
    data["updated_at"] = iso(now())
    save_config(data)
    print(workspace_root)
    return 0


def command_show_config(args: argparse.Namespace) -> int:
    data = load_config()
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def command_add_cover(args: argparse.Namespace) -> int:
    run_dir = args.run_dir.resolve()
    source_file = args.file.resolve()
    if not source_file.exists():
        raise FileNotFoundError(source_file)

    with manifest_lock(run_dir):
        manifest_path, manifest = manifest_for_run(run_dir)
        index = args.index or (len(manifest.get("covers", [])) + 1)
        slug = compact_slug(args.video_title, f"cover-{index:03d}")
        target = unique_path(run_dir / "covers" / f"{index:03d}-{slug}{source_file.suffix.lower()}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target)

        entry = {
            "index": index,
            "video_title": args.video_title,
            "video_url": args.video_url,
            "thumbnail_url": args.thumbnail_url,
            "local_path": target.relative_to(run_dir).as_posix(),
            "selected_reason": args.selected_reason,
            "captured_at": iso(now()),
        }
        manifest.setdefault("covers", []).append(entry)
        write_manifest(manifest_path, manifest)
    print(target)
    return 0


def command_add_source(args: argparse.Namespace) -> int:
    run_dir = args.run_dir.resolve()
    source_file = args.file.resolve()
    if not source_file.exists():
        raise FileNotFoundError(source_file)

    with manifest_lock(run_dir):
        manifest_path, manifest = manifest_for_run(run_dir)
        source_type = compact_slug(args.source_type, "source")
        slug = compact_slug(args.title, f"source-{len(manifest.get('process_sources', [])) + 1:03d}")
        target_dir = run_dir / "sources" / f"{source_type}s"
        target = unique_path(target_dir / f"{slug}{source_file.suffix.lower()}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target)

        entry = {
            "title": args.title,
            "url": args.url,
            "local_path": target.relative_to(run_dir).as_posix(),
            "source_type": args.source_type,
            "captured_at": iso(now()),
        }
        manifest.setdefault("process_sources", []).append(entry)
        write_manifest(manifest_path, manifest)
    print(target)
    return 0


def command_set_artifact(args: argparse.Namespace) -> int:
    run_dir = args.run_dir.resolve()
    with manifest_lock(run_dir):
        manifest_path, manifest = manifest_for_run(run_dir)
        artifacts = manifest.setdefault("artifacts", {})
        value_path = Path(args.value)
        try:
            value = value_path.resolve().relative_to(run_dir).as_posix()
        except (ValueError, OSError):
            value = args.value
        artifacts[args.key] = value
        write_manifest(manifest_path, manifest)
    print(f"{args.key}={value}")
    return 0


def delete_tree_contents(target: Path) -> int:
    deleted = 0
    if not target.exists():
        return deleted
    for item in target.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()
        deleted += 1
    return deleted


def mark_deleted(entries: list[dict], section: str, cutoff: datetime) -> None:
    stamp = iso(now())
    for entry in entries:
        if entry.get("deleted_at"):
            continue
        entry["deleted_at"] = stamp
        entry["delete_reason"] = f"{section} retention expired before {iso(cutoff)}"


def command_cleanup(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    if not root.exists():
        print("No research root found.")
        return 0

    deleted_runs = 0
    deleted_sections = 0
    current = now()

    for manifest_path in root.glob("*/*/manifest.json"):
        run_dir = manifest_path.parent
        manifest = read_manifest(manifest_path)
        created_at = datetime.fromisoformat(manifest["created_at"])
        retention = manifest.get("retention", {})

        covers_days = int(retention.get("covers_delete_after_days", 30))
        sources_days = int(retention.get("sources_delete_after_days", 90))

        covers_cutoff = current - timedelta(days=covers_days)
        sources_cutoff = current - timedelta(days=sources_days)

        changed = False
        if created_at < covers_cutoff:
            count = delete_tree_contents(run_dir / "covers")
            if count:
                deleted_sections += count
                mark_deleted(manifest.get("covers", []), "covers", covers_cutoff)
                changed = True

        if created_at < sources_cutoff:
            count = delete_tree_contents(run_dir / "sources")
            if count:
                deleted_sections += count
                mark_deleted(manifest.get("process_sources", []), "sources", sources_cutoff)
                changed = True

        if changed:
            manifest["last_cleanup_at"] = iso(current)
            write_manifest(manifest_path, manifest)

        if args.delete_empty_runs:
            keep_paths = [
                run_dir / "distillation" / "research.md",
                run_dir / "prompts",
                run_dir / "generated",
                manifest_path,
            ]
            has_keep_artifacts = any(path.exists() for path in keep_paths)
            if not has_keep_artifacts:
                shutil.rmtree(run_dir)
                deleted_runs += 1

    print(f"Deleted sections/files: {deleted_sections}; deleted runs: {deleted_runs}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)

    set_root = sub.add_parser("set-root")
    set_root.add_argument("--workspace-root", required=True, type=Path)
    set_root.set_defaults(func=command_set_root)

    show_config = sub.add_parser("show-config")
    show_config.set_defaults(func=command_show_config)

    init = sub.add_parser("init")
    init.add_argument("--creator-id", required=True)
    init.add_argument("--creator-name", required=True)
    init.add_argument("--run-id")
    init.add_argument("--covers-delete-after-days", type=int, default=30)
    init.add_argument("--sources-delete-after-days", type=int, default=90)
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=command_init)

    add_cover = sub.add_parser("add-cover")
    add_cover.add_argument("--run-dir", required=True, type=Path)
    add_cover.add_argument("--file", required=True, type=Path)
    add_cover.add_argument("--video-title", required=True)
    add_cover.add_argument("--video-url", required=True)
    add_cover.add_argument("--thumbnail-url", required=True)
    add_cover.add_argument("--selected-reason", required=True)
    add_cover.add_argument("--index", type=int)
    add_cover.set_defaults(func=command_add_cover)

    add_source = sub.add_parser("add-source")
    add_source.add_argument("--run-dir", required=True, type=Path)
    add_source.add_argument("--file", required=True, type=Path)
    add_source.add_argument("--title", required=True)
    add_source.add_argument("--url", required=True)
    add_source.add_argument("--source-type", required=True)
    add_source.set_defaults(func=command_add_source)

    set_artifact = sub.add_parser("set-artifact")
    set_artifact.add_argument("--run-dir", required=True, type=Path)
    set_artifact.add_argument("--key", required=True)
    set_artifact.add_argument("--value", required=True)
    set_artifact.set_defaults(func=command_set_artifact)

    cleanup = sub.add_parser("cleanup")
    cleanup.add_argument("--delete-empty-runs", action="store_true")
    cleanup.set_defaults(func=command_cleanup)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

