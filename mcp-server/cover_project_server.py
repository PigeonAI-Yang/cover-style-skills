#!/usr/bin/env python3
"""Dependency-free MCP-style wrapper around cover project scripts."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PRODUCT_ROOT / "scripts" / "manage_cover_project.py"
COVERCTL = PRODUCT_ROOT / "scripts" / "coverctl.py"

PLATFORM_CANVAS = {
    "wechat-article-main": {
        "platform": "wechat",
        "ratio": "2.35:1",
        "target_canvas": "2350x1000",
        "safe_area": "central 1000x1000 square-safe zone, x=675..1675",
    },
    "wechat-article-square": {
        "platform": "wechat",
        "ratio": "1:1",
        "target_canvas": "1080x1080",
        "safe_area": "self-contained square composition",
    },
}

TOOLS = [
    {
        "name": "create_cover_project",
        "description": "Create a private PigeonYang cover project.",
        "inputSchema": {
            "type": "object",
            "required": ["title"],
            "properties": {
                "title": {"type": "string"},
                "summary": {"type": "string"},
                "slug": {"type": "string"},
                "cover_mode": {
                    "type": "string",
                    "enum": ["wechat-article-main", "wechat-article-square"],
                },
            },
        },
    },
    {
        "name": "save_artifact",
        "description": "Save a known private project artifact.",
        "inputSchema": {
            "type": "object",
            "required": ["project_path", "artifact", "text"],
            "properties": {
                "project_path": {"type": "string"},
                "artifact": {
                    "type": "string",
                    "enum": [
                        "source",
                        "engine-routing",
                        "directions",
                        "approved-direction",
                        "execution-packet",
                        "prompt-final",
                        "review",
                    ],
                },
                "text": {"type": "string"},
            },
        },
    },
    {
        "name": "set_approved_direction",
        "description": "Record the approved child skill, internal paradigm, and exact cover copy.",
        "inputSchema": {
            "type": "object",
            "required": ["project_path", "direction_id", "approved_copy"],
            "properties": {
                "project_path": {"type": "string"},
                "direction_id": {"type": "string"},
                "child_skill": {"type": "string"},
                "internal_paradigm": {"type": "string"},
                "approved_copy": {"type": "string"},
                "notes": {"type": "string"},
            },
        },
    },
    {
        "name": "update_metrics",
        "description": "Update post-publish project metrics.",
        "inputSchema": {
            "type": "object",
            "required": ["project_path"],
            "properties": {
                "project_path": {"type": "string"},
                "published_at": {"type": "string"},
                "article_url": {"type": "string"},
                "selected_output": {"type": "string"},
                "open_rate": {"type": "number"},
                "reads": {"type": "integer"},
                "shares": {"type": "integer"},
                "subjective_score": {"type": "integer", "minimum": 1, "maximum": 5},
                "notes": {"type": "string"},
            },
        },
    },
    {
        "name": "validate_project_path",
        "description": "Validate private project location safety.",
        "inputSchema": {
            "type": "object",
            "required": ["project_path"],
            "properties": {"project_path": {"type": "string"}},
        },
    },
    {
        "name": "resolve_platform_canvas",
        "description": "Resolve supported platform canvas and safe-area rules.",
        "inputSchema": {
            "type": "object",
            "required": ["cover_mode"],
            "properties": {
                "cover_mode": {
                    "type": "string",
                    "enum": ["wechat-article-main", "wechat-article-square"],
                }
            },
        },
    },
    {
        "name": "get_project_state",
        "description": "Return computed workflow state and blocking reasons.",
        "inputSchema": {
            "type": "object",
            "required": ["project_path"],
            "properties": {"project_path": {"type": "string"}},
        },
    },
    {
        "name": "list_generation_backends",
        "description": "List configured image generation backends and reference-image capability rules.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "save_engine_routing",
        "description": "Save validated engine routing before recommendation cards.",
        "inputSchema": {
            "type": "object",
            "required": ["project_path", "text"],
            "properties": {
                "project_path": {"type": "string"},
                "text": {"type": "string"},
            },
        },
    },
    {
        "name": "save_skill_recommendations",
        "description": "Save validated child-skill recommendation packet.",
        "inputSchema": {
            "type": "object",
            "required": ["project_path", "text"],
            "properties": {
                "project_path": {"type": "string"},
                "text": {"type": "string"},
            },
        },
    },
    {
        "name": "save_execution_packet",
        "description": "Save validated execution design packet after child-skill approval.",
        "inputSchema": {
            "type": "object",
            "required": ["project_path", "text"],
            "properties": {
                "project_path": {"type": "string"},
                "text": {"type": "string"},
            },
        },
    },
    {
        "name": "save_final_prompt",
        "description": "Save validated final image prompt after execution packet.",
        "inputSchema": {
            "type": "object",
            "required": ["project_path", "text"],
            "properties": {
                "project_path": {"type": "string"},
                "text": {"type": "string"},
            },
        },
    },
    {
        "name": "verify_prompt_firewall",
        "description": "Run final prompt firewall and persist firewall-result.json.",
        "inputSchema": {
            "type": "object",
            "required": ["project_path"],
            "properties": {
                "project_path": {"type": "string"},
                "forbid": {"type": "array", "items": {"type": "string"}},
                "require_identity_reference": {"type": "boolean"},
            },
        },
    },
    {
        "name": "preflight_generation",
        "description": "Check whether final generation is allowed or prompt-only blocked.",
        "inputSchema": {
            "type": "object",
            "required": ["project_path", "generation_backend"],
            "properties": {
                "project_path": {"type": "string"},
                "generation_backend": {"type": "string"},
                "reference_image_mode": {
                    "type": "string",
                    "enum": ["auto", "explicit", "text_only", "unknown"],
                },
                "reference_evidence": {"type": "array", "items": {"type": "string"}},
            },
        },
    },
    {
        "name": "record_generation_output",
        "description": "Copy a generated image into outputs and persist generation-manifest.json.",
        "inputSchema": {
            "type": "object",
            "required": [
                "project_path",
                "source_image",
                "generation_backend",
                "reference_image_mode",
            ],
            "properties": {
                "project_path": {"type": "string"},
                "source_image": {"type": "string"},
                "output_name": {"type": "string"},
                "generation_backend": {"type": "string"},
                "reference_image_mode": {
                    "type": "string",
                    "enum": ["auto", "explicit", "text_only", "unknown"],
                },
            },
        },
    },
    {
        "name": "verify_image_dimensions",
        "description": "Run image dimension verification and persist dimension-check.json.",
        "inputSchema": {
            "type": "object",
            "required": ["project_path", "image"],
            "properties": {
                "project_path": {"type": "string"},
                "image": {"type": "string"},
                "preset": {"type": "string"},
                "ratio_only": {"type": "boolean"},
            },
        },
    },
    {
        "name": "mark_final",
        "description": "Mark a generated output final after manifest and exact dimension pass.",
        "inputSchema": {
            "type": "object",
            "required": ["project_path"],
            "properties": {
                "project_path": {"type": "string"},
                "output": {"type": "string"},
                "notes": {"type": "string"},
            },
        },
    },
]


def run_script(args: list[str]) -> str:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout).strip())
    return result.stdout.strip()


def run_coverctl(args: list[str]) -> str:
    result = subprocess.run(
        [sys.executable, str(COVERCTL), *args, "--json"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout).strip())
    return result.stdout.strip()


def optional_arg(args: list[str], name: str, value: Any) -> None:
    if value is not None:
        args.extend([name, str(value)])


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "create_cover_project":
        args = ["create", "--title", str(arguments["title"]), "--json"]
        optional_arg(args, "--summary", arguments.get("summary"))
        optional_arg(args, "--slug", arguments.get("slug"))
        optional_arg(args, "--cover-mode", arguments.get("cover_mode"))
        return text_result(run_script(args))

    if name == "save_artifact":
        artifact = str(arguments["artifact"])
        gated_commands = {
            "engine-routing": "save-engine-routing",
            "directions": "save-skill-recommendations",
            "execution-packet": "save-execution-packet",
            "prompt-final": "save-final-prompt",
        }
        if artifact in gated_commands:
            return text_result(
                run_coverctl(
                    [
                        gated_commands[artifact],
                        "--project-path",
                        str(arguments["project_path"]),
                        "--text",
                        str(arguments["text"]),
                    ]
                )
            )
        if artifact == "approved-direction":
            raise RuntimeError("use set_approved_direction so the child-skill gate can validate approval")
        output = run_script(
            [
                "save-artifact",
                "--project-path",
                str(arguments["project_path"]),
                "--artifact",
                artifact,
                "--text",
                str(arguments["text"]),
            ]
        )
        return text_result(output)

    if name == "set_approved_direction":
        args = [
            "set-approved",
            "--project-path",
            str(arguments["project_path"]),
            "--direction-id",
            str(arguments["direction_id"]),
            "--approved-copy",
            str(arguments["approved_copy"]),
        ]
        optional_arg(args, "--child-skill", arguments.get("child_skill"))
        optional_arg(args, "--internal-paradigm", arguments.get("internal_paradigm"))
        optional_arg(args, "--notes", arguments.get("notes"))
        return text_result(run_coverctl(args))

    if name == "update_metrics":
        args = ["update-metrics", "--project-path", str(arguments["project_path"])]
        for key in [
            "published_at",
            "article_url",
            "selected_output",
            "open_rate",
            "reads",
            "shares",
            "subjective_score",
            "notes",
        ]:
            optional_arg(args, "--" + key.replace("_", "-"), arguments.get(key))
        return text_result(run_script(args))

    if name == "validate_project_path":
        output = run_script(
            [
                "validate-path",
                "--project-path",
                str(arguments["project_path"]),
                "--json",
            ]
        )
        return text_result(output)

    if name == "resolve_platform_canvas":
        cover_mode = str(arguments["cover_mode"])
        if cover_mode not in PLATFORM_CANVAS:
            raise RuntimeError(f"unsupported cover mode: {cover_mode}")
        return text_result(json.dumps(PLATFORM_CANVAS[cover_mode], ensure_ascii=False, indent=2))

    if name == "get_project_state":
        return text_result(
            run_coverctl(["get-state", "--project-path", str(arguments["project_path"])])
        )

    if name == "list_generation_backends":
        return text_result(run_coverctl(["list-generation-backends"]))

    if name == "save_engine_routing":
        return text_result(
            run_coverctl(
                [
                    "save-engine-routing",
                    "--project-path",
                    str(arguments["project_path"]),
                    "--text",
                    str(arguments["text"]),
                ]
            )
        )

    if name == "save_skill_recommendations":
        return text_result(
            run_coverctl(
                [
                    "save-skill-recommendations",
                    "--project-path",
                    str(arguments["project_path"]),
                    "--text",
                    str(arguments["text"]),
                ]
            )
        )

    if name == "save_execution_packet":
        return text_result(
            run_coverctl(
                [
                    "save-execution-packet",
                    "--project-path",
                    str(arguments["project_path"]),
                    "--text",
                    str(arguments["text"]),
                ]
            )
        )

    if name == "save_final_prompt":
        return text_result(
            run_coverctl(
                [
                    "save-final-prompt",
                    "--project-path",
                    str(arguments["project_path"]),
                    "--text",
                    str(arguments["text"]),
                ]
            )
        )

    if name == "verify_prompt_firewall":
        args = ["verify-prompt-firewall", "--project-path", str(arguments["project_path"])]
        for term in arguments.get("forbid") or []:
            args.extend(["--forbid", str(term)])
        if arguments.get("require_identity_reference"):
            args.append("--require-identity-reference")
        return text_result(run_coverctl(args))

    if name == "preflight_generation":
        args = [
            "preflight-generation",
            "--project-path",
            str(arguments["project_path"]),
            "--generation-backend",
            str(arguments["generation_backend"]),
        ]
        optional_arg(args, "--reference-image-mode", arguments.get("reference_image_mode"))
        for evidence in arguments.get("reference_evidence") or []:
            args.extend(["--reference-evidence", str(evidence)])
        return text_result(run_coverctl(args))

    if name == "record_generation_output":
        args = [
            "record-generation-output",
            "--project-path",
            str(arguments["project_path"]),
            "--source-image",
            str(arguments["source_image"]),
            "--generation-backend",
            str(arguments["generation_backend"]),
            "--reference-image-mode",
            str(arguments["reference_image_mode"]),
        ]
        optional_arg(args, "--output-name", arguments.get("output_name"))
        return text_result(run_coverctl(args))

    if name == "verify_image_dimensions":
        args = [
            "verify-image-dimensions",
            "--project-path",
            str(arguments["project_path"]),
            "--image",
            str(arguments["image"]),
        ]
        optional_arg(args, "--preset", arguments.get("preset"))
        if arguments.get("ratio_only"):
            args.append("--ratio-only")
        return text_result(run_coverctl(args))

    if name == "mark_final":
        args = ["mark-final", "--project-path", str(arguments["project_path"])]
        optional_arg(args, "--output", arguments.get("output"))
        optional_arg(args, "--notes", arguments.get("notes"))
        return text_result(run_coverctl(args))

    raise RuntimeError(f"unknown tool: {name}")


def text_result(text: str, is_error: bool = False) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": text}], "isError": is_error}


def handle(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    msg_id = message.get("id")
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "pigeonyang-cover-project",
                    "version": "0.1.0",
                },
            },
        }
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = message.get("params") or {}
        try:
            result = call_tool(params["name"], params.get("arguments") or {})
        except Exception as exc:  # noqa: BLE001 - report tool errors through JSON-RPC.
            result = text_result(str(exc), is_error=True)
        return {"jsonrpc": "2.0", "id": msg_id, "result": result}
    if msg_id is None:
        return None
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"method not found: {method}"},
    }


def main() -> int:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            response = handle(json.loads(line))
        except Exception as exc:  # noqa: BLE001 - keep prototype server alive.
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(exc)},
            }
        if response is not None:
            print(json.dumps(response, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
