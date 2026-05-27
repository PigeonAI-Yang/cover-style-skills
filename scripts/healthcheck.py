#!/usr/bin/env python3
"""Report repository, research, MCP, and project health for the cover product."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PRODUCT_ROOT.parent


def run(args: list[str], cwd: Path = PRODUCT_ROOT) -> dict:
    try:
        result = subprocess.run(
            args,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except FileNotFoundError as exc:
        return {"ok": False, "returncode": None, "stdout": "", "stderr": str(exc)}


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def child_skills() -> list[dict]:
    root = PRODUCT_ROOT / "child-skills"
    rows: list[dict] = []
    if not root.exists():
        return rows
    for path in sorted(root.iterdir()):
        if not path.is_dir():
            continue
        meta = load_json(path / "skill.json")
        rows.append(
            {
                "name": meta.get("name") or path.name,
                "kind": meta.get("kind"),
                "version": meta.get("version"),
                "has_skill_md": (path / "SKILL.md").exists(),
            }
        )
    return rows


def design_standards() -> list[dict]:
    root = PRODUCT_ROOT / "design-standards"
    rows: list[dict] = []
    if not root.exists():
        return rows
    for path in sorted(root.iterdir()):
        if path.is_dir():
            rows.append(
                {
                    "creator": path.name,
                    "has_design_standard": (path / "design-standard.md").exists(),
                }
            )
    return rows


def research_runs() -> dict:
    root = WORKSPACE_ROOT / "research-runs"
    legacy = PRODUCT_ROOT / "research"
    rows: list[dict] = []
    if root.exists():
        for creator in sorted(root.iterdir()):
            if not creator.is_dir():
                continue
            for run_dir in sorted(creator.iterdir()):
                if not run_dir.is_dir():
                    continue
                rows.append(
                    {
                        "creator": creator.name,
                        "run": run_dir.name,
                        "has_manifest": (run_dir / "manifest.json").exists(),
                        "has_research": (run_dir / "distillation" / "research.md").exists(),
                        "has_design_standard": (
                            run_dir / "distillation" / "design-standard.md"
                        ).exists(),
                    }
                )
    return {
        "root": str(root),
        "exists": root.exists(),
        "runs": rows,
        "legacy_product_research_exists": legacy.exists(),
    }


def git_status() -> dict:
    status = run(["git", "status", "--short", "--branch"])
    lines = status["stdout"].splitlines() if status["stdout"] else []
    return {
        "ok": status["ok"],
        "branch": lines[0] if lines else "",
        "dirty_entries": lines[1:],
    }


def mcp_status() -> dict:
    config = run(
        [
            "pigeonyang-cover-mcp",
            "--product-root",
            str(PRODUCT_ROOT),
            "--print-config",
        ]
    )
    return {
        "ok": config["ok"],
        "stdout": config["stdout"],
        "stderr": config["stderr"],
    }


def project_states() -> list[dict]:
    root = WORKSPACE_ROOT / "cover-projects"
    rows: list[dict] = []
    if not root.exists():
        return rows
    for project_dir in sorted(root.iterdir()):
        if not project_dir.is_dir() or project_dir.name.startswith("_"):
            continue
        result = run(
            [
                sys.executable,
                str(PRODUCT_ROOT / "scripts" / "coverctl.py"),
                "get-state",
                "--project-path",
                str(project_dir),
                "--json",
            ]
        )
        data = json.loads(result["stdout"]) if result["ok"] and result["stdout"] else {}
        rows.append(
            {
                "project": project_dir.name,
                "state": data.get("state") if data else "ERROR",
                "blockers": data.get("blockers") if data else [result["stderr"]],
            }
        )
    return rows


def build_report() -> dict:
    return {
        "product": "Creator Cover Paradigm Distiller",
        "product_root": str(PRODUCT_ROOT),
        "workspace_root": str(WORKSPACE_ROOT),
        "git": git_status(),
        "child_skills": child_skills(),
        "design_standards": design_standards(),
        "research_runs": research_runs(),
        "mcp": mcp_status(),
        "cover_projects": project_states(),
    }


def print_text(report: dict) -> None:
    print(f"Product: {report['product']}")
    print(f"Product root: {report['product_root']}")
    print(f"Workspace root: {report['workspace_root']}")
    print("")
    print(f"Git: {report['git'].get('branch')}")
    print(f"Dirty entries: {len(report['git'].get('dirty_entries') or [])}")
    print("")
    print(f"Child skills: {len(report['child_skills'])}")
    for item in report["child_skills"]:
        status = "OK" if item["has_skill_md"] else "MISSING SKILL.md"
        print(f"- {item['name']} ({item.get('kind')}, {item.get('version')}): {status}")
    print("")
    print(f"Design standards: {len(report['design_standards'])}")
    for item in report["design_standards"]:
        status = "OK" if item["has_design_standard"] else "MISSING"
        print(f"- {item['creator']}: {status}")
    research = report["research_runs"]
    print("")
    print(f"Research root: {research['root']}")
    print(f"Research runs: {len(research['runs'])}")
    print(f"Legacy product/research exists: {research['legacy_product_research_exists']}")
    print("")
    print(f"MCP: {'OK' if report['mcp']['ok'] else 'FAIL'}")
    if not report["mcp"]["ok"]:
        print(report["mcp"]["stderr"])
    print("")
    print(f"Cover projects: {len(report['cover_projects'])}")
    for item in report["cover_projects"]:
        blockers = item.get("blockers") or []
        suffix = "" if not blockers else " | " + "; ".join(blockers)
        print(f"- {item['project']}: {item['state']}{suffix}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    report = build_report()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_text(report)

    failed = not report["mcp"]["ok"] or not report["research_runs"]["exists"]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

