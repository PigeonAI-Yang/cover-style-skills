#!/usr/bin/env python3
"""Manage private PigeonYang cover production projects."""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


TZ = ZoneInfo("Asia/Shanghai")
PRODUCT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PRODUCT_ROOT.parent
DEFAULT_PROJECT_ROOT = WORKSPACE_ROOT / "cover-projects"
DEFAULT_IDENTITY_REFERENCE = (
    DEFAULT_PROJECT_ROOT / "_identity" / "pigeonyang-character-reference.png"
)
TEMPLATE_ROOT = PRODUCT_ROOT / "templates" / "cover-project"

COVER_MODES = {
    "wechat-article-main": {
        "platform": "wechat",
        "width": 2350,
        "height": 1000,
        "ratio": "2.35:1",
        "preset": "wechat-article-main",
        "label": "WeChat public account article main cover",
    },
    "wechat-article-square": {
        "platform": "wechat",
        "width": 1080,
        "height": 1080,
        "ratio": "1:1",
        "preset": "wechat-article-square",
        "label": "WeChat public account article square cover",
    },
}

ARTIFACT_FILES = {
    "source": "source.md",
    "engine-routing": "engine-routing.md",
    "directions": "directions.md",
    "direction-reference-prompts": "direction-reference-prompts.md",
    "approved-direction": "approved-direction.md",
    "execution-packet": "execution-packet.md",
    "prompt-final": "prompt-final.txt",
    "review": "review.md",
}

STATUS_BY_ARTIFACT = {
    "directions": "directions_ready",
    "approved-direction": "direction_approved",
    "execution-packet": "direction_approved",
    "prompt-final": "prompt_ready",
    "review": "reviewed",
}

VALID_STATUSES = {
    "brief_created",
    "directions_ready",
    "direction_approved",
    "prompt_ready",
    "generated",
    "published",
    "reviewed",
}

METRIC_FIELDS = {
    "published_at",
    "article_url",
    "selected_output",
    "open_rate",
    "reads",
    "shares",
    "subjective_score",
    "notes",
}


def now() -> datetime:
    return datetime.now(TZ)


def iso(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def slugify(value: str, fallback: str = "cover") -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return (value or fallback)[:72].strip("-") or fallback


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(text, encoding="utf-8")
    os.replace(temp_path, path)


def atomic_write_json(path: Path, data: dict) -> None:
    atomic_write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_path(path: Path) -> str:
    return os.path.normcase(str(path.resolve()))


def is_inside(path: Path, root: Path) -> bool:
    child = normalize_path(path)
    parent = normalize_path(root)
    return child == parent or child.startswith(parent.rstrip("\\/") + os.sep)


@contextlib.contextmanager
def project_lock(project_path: Path):
    lock_path = project_path / ".cover-project.lock"
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
        raise TimeoutError(f"timed out waiting for project lock: {lock_path}")
    try:
        yield
    finally:
        os.close(fd)
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def validate_project_path(project_path: Path, project_root: Path) -> Path:
    resolved = project_path.resolve()
    root = project_root.resolve()
    product_root = PRODUCT_ROOT.resolve()

    if not is_inside(resolved, root):
        raise ValueError(f"project path must stay under private project root: {root}")
    if is_inside(resolved, product_root):
        raise ValueError(f"project path must not be inside product repo: {product_root}")
    return resolved


def render_template(template_name: str, context: dict[str, str]) -> str:
    template_path = TEMPLATE_ROOT / template_name
    text = template_path.read_text(encoding="utf-8")
    for key, value in context.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def unique_project_dir(root: Path, base_name: str) -> Path:
    candidate = root / base_name
    if not candidate.exists():
        return candidate
    for counter in range(2, 1000):
        numbered = root / f"{base_name}-{counter}"
        if not numbered.exists():
            return numbered
    raise FileExistsError(f"could not allocate a unique project folder for {base_name}")


def source_body_from_args(args: argparse.Namespace) -> tuple[str, str | None, str]:
    if args.source_file:
        source_file = args.source_file.resolve()
        if not source_file.exists():
            raise FileNotFoundError(source_file)
        return source_file.read_text(encoding="utf-8", errors="replace"), str(source_file), "file"
    if args.source_text:
        return args.source_text, None, "manual"
    if args.summary:
        return "No full draft provided. Use title and summary as source material.", None, "title_summary"
    return "No full draft provided. Use title only as source material.", None, "title"


def load_brief(project_path: Path) -> dict:
    brief_path = project_path / "brief.json"
    if not brief_path.exists():
        raise FileNotFoundError(f"brief.json not found: {brief_path}")
    return read_json(brief_path)


def save_brief(project_path: Path, brief: dict) -> None:
    atomic_write_json(project_path / "brief.json", brief)


def update_brief_status(
    project_path: Path,
    status: str | None = None,
    approval: dict | None = None,
) -> None:
    if status is None and approval is None:
        return
    brief = load_brief(project_path)
    if status is not None:
        if status not in VALID_STATUSES:
            raise ValueError(f"invalid status: {status}")
        brief["status"] = status
    if approval is not None:
        brief["approval"].update(approval)
    save_brief(project_path, brief)


def command_create(args: argparse.Namespace) -> int:
    project_root = args.root.resolve()
    project_root.mkdir(parents=True, exist_ok=True)
    validate_project_path(project_root, project_root)

    identity_reference = args.identity_reference.resolve()
    if not identity_reference.exists():
        raise FileNotFoundError(
            f"identity reference not found: {identity_reference}. "
            "Register the private PigeonYang character image before creating projects."
        )

    mode = COVER_MODES[args.cover_mode]
    created_at = iso(now())
    base_slug = slugify(args.slug or args.title)
    base_name = args.project_id or f"{now().strftime('%Y%m%d')}-{base_slug}"
    project_path = unique_project_dir(project_root, slugify(base_name, "cover-project"))
    project_path = validate_project_path(project_path, project_root)
    project_id = project_path.name

    source_body, source_file, input_type = source_body_from_args(args)
    summary = args.summary or ""
    target_canvas = f"{mode['width']}x{mode['height']} ({mode['ratio']})"

    context = {
        "PROJECT_ID": project_id,
        "ARTICLE_TITLE": args.title,
        "SUMMARY": summary or "(none)",
        "SOURCE_BODY": source_body,
        "TARGET_CANVAS": target_canvas,
        "IDENTITY_REFERENCE": str(identity_reference),
        "COVER_MODE": args.cover_mode,
    }

    project_path.mkdir(parents=True, exist_ok=False)
    (project_path / "outputs").mkdir()
    (project_path / "outputs" / "direction-references").mkdir()

    brief = {
        "schema_version": 1,
        "project_id": project_id,
        "created_at": created_at,
        "platform": mode["platform"],
        "cover_mode": args.cover_mode,
        "article_title": args.title,
        "summary": args.summary,
        "source_input": {
            "input_type": input_type,
            "source_file": source_file,
        },
        "target_canvas": {
            "width": mode["width"],
            "height": mode["height"],
            "ratio": mode["ratio"],
            "preset": mode["preset"],
        },
        "identity_reference": str(identity_reference),
        "status": "brief_created",
        "approval": {
            "direction_id": None,
            "approved_copy": None,
            "approved_at": None,
        },
    }
    metrics = {
        "schema_version": 1,
        "project_id": project_id,
        "platform": mode["platform"],
        "cover_mode": args.cover_mode,
        "created_at": created_at,
        "published_at": None,
        "article_url": None,
        "selected_output": None,
        "open_rate": None,
        "reads": None,
        "shares": None,
        "subjective_score": None,
        "notes": None,
    }

    atomic_write_json(project_path / "brief.json", brief)
    atomic_write_json(project_path / "metrics.json", metrics)
    atomic_write_text(project_path / "source.md", render_template("source.md", context))
    atomic_write_text(
        project_path / "engine-routing.md",
        render_template("engine-routing.md", context),
    )
    atomic_write_text(project_path / "directions.md", render_template("directions.md", context))
    atomic_write_text(
        project_path / "direction-reference-prompts.md",
        render_template("direction-reference-prompts.md", context),
    )
    atomic_write_text(
        project_path / "approved-direction.md",
        render_template("approved-direction.md", context),
    )
    atomic_write_text(
        project_path / "execution-packet.md",
        render_template("execution-packet.md", context),
    )
    atomic_write_text(
        project_path / "prompt-final.txt",
        render_template("prompt-final.txt", context),
    )
    atomic_write_text(project_path / "review.md", render_template("review.md", context))

    payload = {"project_id": project_id, "project_path": str(project_path)}
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else project_path)
    return 0


def command_validate_path(args: argparse.Namespace) -> int:
    project_root = args.root.resolve()
    project_path = validate_project_path(args.project_path, project_root)
    payload = {
        "project_path": str(project_path),
        "private_root": str(project_root),
        "product_root": str(PRODUCT_ROOT.resolve()),
        "status": "PASS",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else "PASS")
    return 0


def command_save_artifact(args: argparse.Namespace) -> int:
    project_root = args.root.resolve()
    project_path = validate_project_path(args.project_path, project_root)
    if not project_path.exists():
        raise FileNotFoundError(project_path)

    if args.from_file:
        text = args.from_file.read_text(encoding="utf-8", errors="replace")
    else:
        text = args.text
    if text is None:
        raise ValueError("provide --text or --from-file")

    with project_lock(project_path):
        artifact_path = project_path / ARTIFACT_FILES[args.artifact]
        atomic_write_text(artifact_path, text.rstrip() + "\n")

        status = args.status
        if status == "auto":
            status = STATUS_BY_ARTIFACT.get(args.artifact)
        update_brief_status(project_path, status)
    print(artifact_path)
    return 0


def command_set_approved(args: argparse.Namespace) -> int:
    project_root = args.root.resolve()
    project_path = validate_project_path(args.project_path, project_root)
    approved_at = args.approved_at or iso(now())
    text = "\n".join(
        [
            "# Approved Direction",
            "",
            f"Project: `{project_path.name}`",
            "",
            f"- Approved direction: {args.direction_id}",
            f"- Exact approved on-cover copy: {args.approved_copy}",
            f"- Approval time: {approved_at}",
            f"- Notes: {args.notes or ''}",
            "",
        ]
    )
    with project_lock(project_path):
        atomic_write_text(project_path / "approved-direction.md", text)
        update_brief_status(
            project_path,
            "direction_approved",
            {
                "direction_id": args.direction_id,
                "approved_copy": args.approved_copy,
                "approved_at": approved_at,
            },
        )
    print(project_path / "approved-direction.md")
    return 0


def command_update_metrics(args: argparse.Namespace) -> int:
    project_root = args.root.resolve()
    project_path = validate_project_path(args.project_path, project_root)
    metrics_path = project_path / "metrics.json"
    if not metrics_path.exists():
        raise FileNotFoundError(metrics_path)

    with project_lock(project_path):
        metrics = read_json(metrics_path)
        changed = False
        for field in METRIC_FIELDS:
            value = getattr(args, field)
            if value is not None:
                metrics[field] = value
                changed = True

        if args.mark_published:
            update_brief_status(project_path, "published")

        if changed:
            atomic_write_json(metrics_path, metrics)

    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=DEFAULT_PROJECT_ROOT)
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create")
    create.add_argument("--title", required=True)
    create.add_argument("--summary")
    create.add_argument("--source-file", type=Path)
    create.add_argument("--source-text")
    create.add_argument("--slug")
    create.add_argument("--project-id")
    create.add_argument("--cover-mode", choices=sorted(COVER_MODES), default="wechat-article-main")
    create.add_argument("--identity-reference", type=Path, default=DEFAULT_IDENTITY_REFERENCE)
    create.add_argument("--json", action="store_true")
    create.set_defaults(func=command_create)

    validate_path = sub.add_parser("validate-path")
    validate_path.add_argument("--project-path", required=True, type=Path)
    validate_path.add_argument("--json", action="store_true")
    validate_path.set_defaults(func=command_validate_path)

    save_artifact = sub.add_parser("save-artifact")
    save_artifact.add_argument("--project-path", required=True, type=Path)
    save_artifact.add_argument("--artifact", choices=sorted(ARTIFACT_FILES), required=True)
    source = save_artifact.add_mutually_exclusive_group(required=True)
    source.add_argument("--text")
    source.add_argument("--from-file", type=Path)
    save_artifact.add_argument("--status", choices=["auto", *sorted(VALID_STATUSES)], default="auto")
    save_artifact.set_defaults(func=command_save_artifact)

    set_approved = sub.add_parser("set-approved")
    set_approved.add_argument("--project-path", required=True, type=Path)
    set_approved.add_argument("--direction-id", required=True)
    set_approved.add_argument("--approved-copy", required=True)
    set_approved.add_argument("--approved-at")
    set_approved.add_argument("--notes")
    set_approved.set_defaults(func=command_set_approved)

    update_metrics = sub.add_parser("update-metrics")
    update_metrics.add_argument("--project-path", required=True, type=Path)
    update_metrics.add_argument("--published-at")
    update_metrics.add_argument("--article-url")
    update_metrics.add_argument("--selected-output")
    update_metrics.add_argument("--open-rate", type=float)
    update_metrics.add_argument("--reads", type=int)
    update_metrics.add_argument("--shares", type=int)
    update_metrics.add_argument("--subjective-score", type=int, choices=range(1, 6))
    update_metrics.add_argument("--notes")
    update_metrics.add_argument("--mark-published", action="store_true")
    update_metrics.set_defaults(func=command_update_metrics)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
