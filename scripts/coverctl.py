#!/usr/bin/env python3
"""Enforce PigeonYang cover project workflow gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import manage_cover_project as project


TZ = ZoneInfo("Asia/Shanghai")
PRODUCT_ROOT = Path(__file__).resolve().parents[1]
FIREWALL_SCRIPT = PRODUCT_ROOT / "scripts" / "verify_prompt_firewall.py"
DIMENSION_SCRIPT = PRODUCT_ROOT / "scripts" / "verify_image_dimensions.py"
GENERATION_BACKENDS_CONFIG = PRODUCT_ROOT / "config" / "generation-backends.json"

RESULT_FILES = {
    "firewall": "firewall-result.json",
    "preflight": "generation-preflight.json",
    "generation": "generation-manifest.json",
    "dimension": "dimension-check.json",
    "final": "final-manifest.json",
}

STATE_ORDER = [
    "brief_created",
    "routing_completed",
    "child_skill_approved",
    "execution_packet_saved",
    "final_prompt_saved",
    "prompt_firewall_passed",
    "generation_preflight_passed",
    "generation_output_recorded",
    "dimension_verified",
    "final_marked",
]

RECOMMENDATION_FIELDS = [
    "Recommended child skill",
    "Selected internal paradigm",
    "Fit score",
    "Why this skill is recommended",
    "Why this paradigm fits",
    "Target canvas",
    "Proposed on-cover copy",
    "Visual premise",
    "Rejected internal paradigms",
    "Risk or possible misread",
]

EXECUTION_PACKET_SECTIONS = [
    "Copy Approval",
    "Selected Internal Paradigm",
    "Rejected Internal Paradigms",
    "Article Hook Translation",
    "Cover Storyboard",
    "Design Layout Brief",
    "Copy Hierarchy",
    "Reference Handling",
    "Identity And Final-Prompt Firewall",
    "Pre-Generation Self-Check",
    "Post-Generation Dimension Check",
]

IDENTITY_PATTERNS = [
    re.compile(r"preserve .*identity", re.IGNORECASE),
    re.compile(r"preserve .*PigeonYang .*identity", re.IGNORECASE),
    re.compile(r"preserve .*anime identity", re.IGNORECASE),
    re.compile(r"保持.*人设"),
    re.compile(r"保留.*人设"),
    re.compile(r"保持.*身份参考"),
    re.compile(r"保留.*身份参考"),
]

PUBLIC_CREATOR_BLOCK_PATTERNS = [
    re.compile(r"must not resemble any public creator", re.IGNORECASE),
    re.compile(r"must not resemble a public creator", re.IGNORECASE),
    re.compile(r"不要像任何公众创作者"),
    re.compile(r"不得像任何公众创作者"),
]

REFERENCE_IMAGE_MODES = {"explicit", "text_only", "unknown"}


class GateError(ValueError):
    """Raised when a workflow gate refuses a transition."""


def now_iso() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def as_project_path(args: argparse.Namespace) -> Path:
    root = args.root.resolve()
    path = project.validate_project_path(args.project_path, root)
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_generation_backends(path: Path = GENERATION_BACKENDS_CONFIG) -> dict[str, dict]:
    data = read_json(path)
    backends = data.get("backends")
    if not isinstance(backends, dict):
        raise GateError(f"generation backend config is invalid: {path}")
    return backends


def resolve_generation_backend(name: str) -> dict:
    backends = load_generation_backends()
    backend = backends.get(name)
    if backend is None:
        raise GateError(f"unknown generation backend: {name}")
    return backend


def write_json(path: Path, data: dict) -> None:
    project.atomic_write_json(path, data)


def write_artifact(project_path: Path, name: str, text: str) -> Path:
    artifact_path = project_path / project.ARTIFACT_FILES[name]
    project.atomic_write_text(artifact_path, text.rstrip() + "\n")
    return artifact_path


def output(data: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(data.get("message") or json.dumps(data, ensure_ascii=False, indent=2))


def text_from_args(args: argparse.Namespace) -> str:
    if args.from_file:
        return args.from_file.read_text(encoding="utf-8", errors="replace")
    if args.text is None:
        raise GateError("provide --text or --from-file")
    return args.text


def update_brief_status(project_path: Path, status: str, **approval: str | None) -> None:
    brief = project.load_brief(project_path)
    brief["status"] = status
    if approval:
        brief.setdefault("approval", {}).update(approval)
    project.save_brief(project_path, brief)


def is_filled(value: str | None) -> bool:
    if value is None:
        return False
    stripped = value.strip()
    if not stripped:
        return False
    lowered = stripped.casefold()
    return lowered not in {"todo", "tbd", "none", "(none)", "null", "n/a", "-"}


def bullet_value(text: str, label: str) -> str | None:
    pattern = re.compile(r"(?im)^\s*[-*]\s*" + re.escape(label) + r"\s*:\s*(.*?)\s*$")
    match = pattern.search(text)
    if not match:
        return None
    return match.group(1).strip()


def section_body(text: str, heading: str) -> str:
    pattern = re.compile(r"(?im)^##\s+" + re.escape(heading) + r"\s*$")
    match = pattern.search(text)
    if not match:
        return ""
    next_match = re.search(r"(?m)^##\s+", text[match.end() :])
    end = match.end() + next_match.start() if next_match else len(text)
    return text[match.end() : end].strip()


def project_canvas(brief: dict) -> dict:
    target = brief.get("target_canvas") or {}
    preset = target.get("preset") or brief.get("cover_mode") or "wechat-article-main"
    width = target.get("width")
    height = target.get("height")
    ratio = target.get("ratio")
    if preset == "wechat-article-main":
        return {
            "platform_label": "WeChat public account article main cover",
            "target": f"{width or 2350}x{height or 1000}",
            "ratio": ratio or "2.35:1",
            "safe_area": "x=675..1675",
            "preset": preset,
        }
    if preset == "wechat-article-square":
        return {
            "platform_label": "WeChat public account article square cover",
            "target": f"{width or 1080}x{height or 1080}",
            "ratio": ratio or "1:1",
            "safe_area": "square",
            "preset": preset,
        }
    return {
        "platform_label": str(brief.get("platform") or "cover"),
        "target": f"{width}x{height}" if width and height else "",
        "ratio": ratio or "",
        "safe_area": "",
        "preset": preset,
    }


def identity_required(brief: dict) -> bool:
    return bool(str(brief.get("identity_reference") or "").strip())


def validate_engine_routing(project_path: Path, text: str | None = None) -> list[str]:
    text = text if text is not None else read_text(project_path / "engine-routing.md")
    errors: list[str] = []
    for heading in ["Article Diagnosis", "Candidate Engines", "Rejected Engines", "Recommendation"]:
        if f"## {heading}" not in text:
            errors.append(f"engine-routing.md missing section: {heading}")
    if not any(is_filled(value) for value in re.findall(r"(?im)^\s*[-*]\s*Child skill\s*:\s*(.*?)\s*$", text)):
        errors.append("engine-routing.md must include at least one filled child skill")
    if not any(
        is_filled(value)
        for value in re.findall(
            r"(?im)^\s*[-*]\s*(?:Selected internal paradigm|Candidate internal paradigms)\s*:\s*(.*?)\s*$",
            text,
        )
    ):
        errors.append("engine-routing.md must include at least one internal paradigm")
    if not any(is_filled(value) for value in re.findall(r"(?im)^\s*[-*]\s*Fit score\s*:\s*(.*?)\s*$", text)):
        errors.append("engine-routing.md must include at least one fit score")
    return errors


def recommendation_sections(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"(?im)^##\s+Recommendation\s+(\d+)\s*$", text))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((match.group(1), text[match.end() : end]))
    return sections


def parse_recommendations(text: str) -> dict[str, dict[str, str]]:
    parsed: dict[str, dict[str, str]] = {}
    for number, body in recommendation_sections(text):
        child_skill = bullet_value(body, "Recommended child skill")
        if not is_filled(child_skill):
            continue
        values = {field: bullet_value(body, field) or "" for field in RECOMMENDATION_FIELDS}
        values["Recommendation"] = number
        aliases = {
            number,
            f"recommendation-{number}",
            f"direction-{number}",
            f"candidate-{number}",
        }
        for alias in aliases:
            parsed[alias.casefold()] = values
    return parsed


def validate_recommendations(project_path: Path, text: str | None = None) -> list[str]:
    text = text if text is not None else read_text(project_path / "directions.md")
    brief = project.load_brief(project_path)
    canvas = project_canvas(brief)
    errors = validate_engine_routing(project_path)
    recommendations = parse_recommendations(text)
    unique_numbers = sorted({item["Recommendation"] for item in recommendations.values()})
    if not unique_numbers:
        errors.append("directions.md must include at least one filled recommendation")
    if len(unique_numbers) > 3:
        errors.append("directions.md must include no more than three recommendations")
    for number in unique_numbers:
        item = recommendations[f"recommendation-{number}"]
        for field in RECOMMENDATION_FIELDS:
            if not is_filled(item.get(field)):
                errors.append(f"Recommendation {number} missing field: {field}")
        target = item.get("Target canvas", "")
        if canvas["target"] and canvas["target"] not in target:
            errors.append(f"Recommendation {number} target canvas must include {canvas['target']}")
    return errors


def resolve_approval(project_path: Path) -> dict[str, str | None]:
    brief = project.load_brief(project_path)
    approval = brief.get("approval") or {}
    direction_id = approval.get("direction_id")
    approved_copy = approval.get("approved_copy")
    child_skill = approval.get("approved_child_skill")
    internal_paradigm = approval.get("approved_internal_paradigm")

    approved_text = read_text(project_path / "approved-direction.md")
    if not is_filled(child_skill):
        child_skill = bullet_value(approved_text, "Approved child skill") or bullet_value(
            approved_text, "Child skill"
        )
    if not is_filled(internal_paradigm):
        internal_paradigm = bullet_value(
            approved_text, "Approved internal paradigm"
        ) or bullet_value(approved_text, "Selected internal paradigm")

    if (not is_filled(child_skill) or not is_filled(internal_paradigm)) and is_filled(direction_id):
        recommendations = parse_recommendations(read_text(project_path / "directions.md"))
        match = recommendations.get(str(direction_id).casefold())
        if match:
            if not is_filled(child_skill):
                child_skill = match.get("Recommended child skill")
            if not is_filled(internal_paradigm):
                internal_paradigm = match.get("Selected internal paradigm")

    return {
        "direction_id": direction_id,
        "approved_copy": approved_copy,
        "approved_child_skill": child_skill,
        "approved_internal_paradigm": internal_paradigm,
    }


def validate_approval(project_path: Path) -> list[str]:
    errors = validate_recommendations(project_path)
    approval = resolve_approval(project_path)
    if not is_filled(approval.get("direction_id")):
        errors.append("approved direction id is missing")
    if not is_filled(approval.get("approved_copy")):
        errors.append("approved on-cover copy is missing")
    if not is_filled(approval.get("approved_child_skill")):
        errors.append("approved child skill is missing")
    if not is_filled(approval.get("approved_internal_paradigm")):
        errors.append("approved internal paradigm is missing")
    elif is_filled(approval.get("direction_id")):
        recommendations = parse_recommendations(read_text(project_path / "directions.md"))
        direction = recommendations.get(str(approval["direction_id"]).casefold())
        if direction and direction["Recommended child skill"] != approval["approved_child_skill"]:
            errors.append("approved child skill does not match selected recommendation")
        if (
            direction
            and direction["Selected internal paradigm"] != approval["approved_internal_paradigm"]
        ):
            errors.append("approved internal paradigm does not match selected recommendation")
    return errors


def validate_execution_packet(project_path: Path, text: str | None = None) -> list[str]:
    text = text if text is not None else read_text(project_path / "execution-packet.md")
    errors = validate_approval(project_path)
    approval = resolve_approval(project_path)
    for heading in EXECUTION_PACKET_SECTIONS:
        body = section_body(text, heading)
        if not body:
            errors.append(f"execution-packet.md missing filled section: {heading}")
    child_skill = approval.get("approved_child_skill")
    if is_filled(child_skill) and str(child_skill) not in text:
        errors.append("execution-packet.md must name the approved child skill internally")
    internal_paradigm = approval.get("approved_internal_paradigm")
    if is_filled(internal_paradigm) and str(internal_paradigm) not in text:
        errors.append("execution-packet.md must name the selected internal paradigm internally")
    return errors


def validate_final_prompt(project_path: Path, text: str | None = None) -> list[str]:
    text = text if text is not None else read_text(project_path / "prompt-final.txt")
    brief = project.load_brief(project_path)
    canvas = project_canvas(brief)
    errors = validate_execution_packet(project_path)
    if "placeholder" in text.casefold():
        errors.append("prompt-final.txt still contains placeholder text")
    for required in [canvas["platform_label"], canvas["ratio"], canvas["target"]]:
        if required and required not in text:
            errors.append(f"prompt-final.txt missing required canvas string: {required}")
    if canvas["safe_area"] and canvas["safe_area"] not in text:
        errors.append(f"prompt-final.txt missing safe-area string: {canvas['safe_area']}")
    if identity_required(brief):
        if not any(pattern.search(text) for pattern in IDENTITY_PATTERNS):
            errors.append("prompt-final.txt missing explicit identity preservation language")
        if not any(pattern.search(text) for pattern in PUBLIC_CREATOR_BLOCK_PATTERNS):
            errors.append("prompt-final.txt must block public-creator resemblance")
    return errors


def prompt_has_backend_marker(prompt: str, backend: dict) -> bool:
    markers = backend.get("explicit_prompt_markers") or []
    return any(str(marker).casefold() in prompt.casefold() for marker in markers)


def determine_reference_image_mode(
    *,
    requested_mode: str,
    backend_name: str,
    reference_evidence: list[str],
    prompt_text: str,
) -> tuple[str, dict]:
    backend = resolve_generation_backend(backend_name)
    support = backend.get("reference_image_support")
    default_mode = str(backend.get("default_reference_image_mode") or "unknown")
    if default_mode not in REFERENCE_IMAGE_MODES:
        raise GateError(f"invalid default reference mode for backend: {backend_name}")

    accepted = set(backend.get("accepted_reference_evidence") or [])
    evidence = set(reference_evidence)
    marker_ok = prompt_has_backend_marker(prompt_text, backend)
    evidence_ok = bool(evidence & accepted)

    if requested_mode != "auto":
        if requested_mode == "explicit":
            if support == "none":
                raise GateError(f"backend does not support reference images: {backend_name}")
            if not evidence_ok:
                raise GateError(
                    "explicit reference mode requires backend-accepted evidence: "
                    + ", ".join(sorted(accepted))
                )
            if not marker_ok:
                raise GateError("explicit reference mode requires prompt reference markers")
        return requested_mode, {
            "backend": backend,
            "requested_reference_image_mode": requested_mode,
            "reference_evidence": sorted(evidence),
            "accepted_reference_evidence": sorted(accepted),
            "prompt_marker_found": marker_ok,
            "evidence_matched": sorted(evidence & accepted),
        }

    if support == "explicit":
        resolved = "explicit" if marker_ok else default_mode
    elif support == "conditional":
        resolved = "explicit" if evidence_ok and marker_ok else default_mode
    elif support == "none":
        resolved = "text_only"
    else:
        resolved = default_mode

    return resolved, {
        "backend": backend,
        "requested_reference_image_mode": requested_mode,
        "reference_evidence": sorted(evidence),
        "accepted_reference_evidence": sorted(accepted),
        "prompt_marker_found": marker_ok,
        "evidence_matched": sorted(evidence & accepted),
    }


def result_status(path: Path, pass_values: set[str] | None = None) -> bool:
    data = read_json(path)
    if not data:
        return False
    pass_values = pass_values or {"PASS"}
    return str(data.get("status", "")).upper() in pass_values


def compute_state(project_path: Path) -> dict:
    blockers: list[str] = []
    states: list[str] = []

    try:
        brief = project.load_brief(project_path)
    except FileNotFoundError:
        return {
            "project_path": str(project_path),
            "state": "missing_brief",
            "states": [],
            "blockers": ["brief.json is missing"],
        }

    states.append("brief_created")

    routing_errors = validate_recommendations(project_path)
    if routing_errors:
        blockers.extend(routing_errors)
        return state_payload(project_path, "brief_created", states, blockers)
    states.append("routing_completed")

    approval_errors = validate_approval(project_path)
    if approval_errors:
        blockers.extend(approval_errors)
        return state_payload(project_path, "routing_completed", states, blockers)
    states.append("child_skill_approved")

    packet_errors = validate_execution_packet(project_path)
    if packet_errors:
        blockers.extend(packet_errors)
        return state_payload(project_path, "child_skill_approved", states, blockers)
    states.append("execution_packet_saved")

    prompt_errors = validate_final_prompt(project_path)
    if prompt_errors:
        blockers.extend(prompt_errors)
        return state_payload(project_path, "execution_packet_saved", states, blockers)
    states.append("final_prompt_saved")

    firewall_path = project_path / RESULT_FILES["firewall"]
    if not result_status(firewall_path):
        blockers.append("firewall-result.json pass status is missing")
        return state_payload(project_path, "final_prompt_saved", states, blockers)
    states.append("prompt_firewall_passed")

    preflight = read_json(project_path / RESULT_FILES["preflight"])
    if not preflight:
        blockers.append("generation-preflight.json is missing")
        return state_payload(project_path, "prompt_firewall_passed", states, blockers)
    if preflight.get("mode") == "prompt_only" and not preflight.get("allowed"):
        blockers.extend(preflight.get("blocking_reasons") or ["prompt-only generation block"])
        return state_payload(project_path, "prompt_only_blocked", states, blockers)
    if not preflight.get("allowed") or str(preflight.get("status", "")).upper() != "PASS":
        blockers.extend(preflight.get("blocking_reasons") or ["generation preflight did not pass"])
        return state_payload(project_path, "prompt_firewall_passed", states, blockers)
    states.append("generation_preflight_passed")

    generation = read_json(project_path / RESULT_FILES["generation"])
    if not generation:
        blockers.append("generation-manifest.json is missing")
        return state_payload(project_path, "generation_preflight_passed", states, blockers)
    states.append("generation_output_recorded")

    dimension = read_json(project_path / RESULT_FILES["dimension"])
    if not dimension or dimension.get("status") != "PASS" or dimension.get("mode") != "exact":
        blockers.append("dimension-check.json exact pass is missing")
        return state_payload(project_path, "generation_output_recorded", states, blockers)
    states.append("dimension_verified")

    final_manifest = read_json(project_path / RESULT_FILES["final"])
    if not final_manifest or final_manifest.get("status") != "FINAL":
        blockers.append("final-manifest.json is missing")
        return state_payload(project_path, "dimension_verified", states, blockers)
    states.append("final_marked")
    return state_payload(project_path, "final_marked", states, [])


def state_payload(project_path: Path, state: str, states: list[str], blockers: list[str]) -> dict:
    return {
        "project_path": str(project_path),
        "state": state,
        "states": states,
        "blockers": blockers,
    }


def command_get_state(args: argparse.Namespace) -> int:
    project_path = as_project_path(args)
    output(compute_state(project_path), args.json)
    return 0


def command_list_generation_backends(args: argparse.Namespace) -> int:
    backends = load_generation_backends()
    payload = {
        "schema_version": 1,
        "config": str(GENERATION_BACKENDS_CONFIG),
        "backends": backends,
    }
    output(payload, args.json)
    return 0


def command_save_engine_routing(args: argparse.Namespace) -> int:
    project_path = as_project_path(args)
    text = text_from_args(args)
    errors = validate_engine_routing(project_path, text)
    if errors:
        raise GateError("; ".join(errors))
    with project.project_lock(project_path):
        artifact_path = write_artifact(project_path, "engine-routing", text)
    output({"status": "PASS", "artifact": str(artifact_path)}, args.json)
    return 0


def command_save_skill_recommendations(args: argparse.Namespace) -> int:
    project_path = as_project_path(args)
    text = text_from_args(args)
    errors = validate_recommendations(project_path, text)
    if errors:
        raise GateError("; ".join(errors))
    with project.project_lock(project_path):
        artifact_path = write_artifact(project_path, "directions", text)
        update_brief_status(project_path, "routing_completed")
    output({"status": "PASS", "artifact": str(artifact_path)}, args.json)
    return 0


def command_set_approved(args: argparse.Namespace) -> int:
    project_path = as_project_path(args)
    errors = validate_recommendations(project_path)
    if errors:
        raise GateError("; ".join(errors))
    recommendations = parse_recommendations(read_text(project_path / "directions.md"))
    selected = recommendations.get(args.direction_id.casefold())
    if not selected:
        raise GateError(f"direction_id does not resolve to a recommendation: {args.direction_id}")
    child_skill = args.child_skill or selected["Recommended child skill"]
    if child_skill != selected["Recommended child skill"]:
        raise GateError("approved child skill does not match selected recommendation")
    internal_paradigm = args.internal_paradigm or selected["Selected internal paradigm"]
    if internal_paradigm != selected["Selected internal paradigm"]:
        raise GateError("approved internal paradigm does not match selected recommendation")
    approved_at = args.approved_at or now_iso()
    text = "\n".join(
        [
            "# Approved Direction",
            "",
            f"Project: `{project_path.name}`",
            "",
            f"- Approved direction: {args.direction_id}",
            f"- Approved child skill: {child_skill}",
            f"- Approved internal paradigm: {internal_paradigm}",
            f"- Exact approved on-cover copy: {args.approved_copy}",
            f"- Approval time: {approved_at}",
            f"- Notes: {args.notes or ''}",
            "",
        ]
    )
    with project.project_lock(project_path):
        project.atomic_write_text(project_path / "approved-direction.md", text)
        update_brief_status(
            project_path,
            "child_skill_approved",
            direction_id=args.direction_id,
            approved_child_skill=child_skill,
            approved_internal_paradigm=internal_paradigm,
            approved_copy=args.approved_copy,
            approved_at=approved_at,
        )
    output(
        {
            "status": "PASS",
            "approved_child_skill": child_skill,
            "approved_internal_paradigm": internal_paradigm,
        },
        args.json,
    )
    return 0


def command_save_execution_packet(args: argparse.Namespace) -> int:
    project_path = as_project_path(args)
    text = text_from_args(args)
    errors = validate_execution_packet(project_path, text)
    if errors:
        raise GateError("; ".join(errors))
    with project.project_lock(project_path):
        artifact_path = write_artifact(project_path, "execution-packet", text)
        update_brief_status(project_path, "execution_packet_saved")
    output({"status": "PASS", "artifact": str(artifact_path)}, args.json)
    return 0


def command_save_final_prompt(args: argparse.Namespace) -> int:
    project_path = as_project_path(args)
    text = text_from_args(args)
    errors = validate_final_prompt(project_path, text)
    if errors:
        raise GateError("; ".join(errors))
    with project.project_lock(project_path):
        artifact_path = write_artifact(project_path, "prompt-final", text)
        update_brief_status(project_path, "final_prompt_saved")
    output({"status": "PASS", "artifact": str(artifact_path)}, args.json)
    return 0


def command_verify_prompt_firewall(args: argparse.Namespace) -> int:
    project_path = as_project_path(args)
    prompt_errors = validate_final_prompt(project_path)
    if prompt_errors:
        raise GateError("; ".join(prompt_errors))

    brief = project.load_brief(project_path)
    prompt_file = project_path / "prompt-final.txt"
    cmd = [sys.executable, str(FIREWALL_SCRIPT), str(prompt_file)]
    for term in args.forbid or []:
        cmd.extend(["--forbid", term])
    require_identity = args.require_identity_reference or identity_required(brief)
    if require_identity:
        cmd.append("--require-identity-reference")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=False)
    payload = {
        "schema_version": 1,
        "checked_at": now_iso(),
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "prompt_file": str(prompt_file),
        "forbidden_terms": args.forbid or [],
        "require_identity_reference": require_identity,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }
    with project.project_lock(project_path):
        write_json(project_path / RESULT_FILES["firewall"], payload)
        if result.returncode == 0:
            update_brief_status(project_path, "prompt_firewall_passed")
    output(payload, args.json)
    return result.returncode


def command_preflight_generation(args: argparse.Namespace) -> int:
    project_path = as_project_path(args)
    brief = project.load_brief(project_path)
    prompt_text = read_text(project_path / "prompt-final.txt")
    reference_mode, backend_resolution = determine_reference_image_mode(
        requested_mode=args.reference_image_mode,
        backend_name=args.generation_backend,
        reference_evidence=args.reference_evidence or [],
        prompt_text=prompt_text,
    )
    blocking: list[str] = []
    blocking.extend(validate_approval(project_path))
    blocking.extend(validate_execution_packet(project_path))
    blocking.extend(validate_final_prompt(project_path))
    if not result_status(project_path / RESULT_FILES["firewall"]):
        blocking.append("prompt firewall has not passed")

    reference_capability_blockers: list[str] = []
    identity_ref = str(brief.get("identity_reference") or "").strip()
    if identity_required(brief):
        if not Path(identity_ref).exists():
            blocking.append(f"identity reference does not exist: {identity_ref}")
        if reference_mode != "explicit":
            reference_capability_blockers.append(
                "required identity reference is not proven as an explicit image input"
            )

    all_blockers = blocking + reference_capability_blockers
    if all_blockers and not blocking and reference_capability_blockers:
        allowed = False
        mode = "prompt_only"
        status = "BLOCKED"
    elif all_blockers:
        allowed = False
        mode = "blocked"
        status = "FAIL"
    else:
        allowed = True
        mode = "generate"
        status = "PASS"

    payload = {
        "schema_version": 1,
        "checked_at": now_iso(),
        "status": status,
        "allowed": allowed,
        "mode": mode,
        "generation_backend": args.generation_backend,
        "reference_image_mode": reference_mode,
        "requested_reference_image_mode": args.reference_image_mode,
        "reference_evidence": args.reference_evidence or [],
        "backend_capability": {
            "display_name": backend_resolution["backend"].get("display_name"),
            "kind": backend_resolution["backend"].get("kind"),
            "reference_image_support": backend_resolution["backend"].get(
                "reference_image_support"
            ),
            "default_reference_image_mode": backend_resolution["backend"].get(
                "default_reference_image_mode"
            ),
            "accepted_reference_evidence": backend_resolution["accepted_reference_evidence"],
            "prompt_marker_found": backend_resolution["prompt_marker_found"],
            "evidence_matched": backend_resolution["evidence_matched"],
        },
        "identity_reference_required": identity_required(brief),
        "identity_reference": identity_ref,
        "blocking_reasons": all_blockers,
    }
    with project.project_lock(project_path):
        write_json(project_path / RESULT_FILES["preflight"], payload)
        if allowed:
            update_brief_status(project_path, "generation_preflight_passed")
        elif mode == "prompt_only":
            update_brief_status(project_path, "prompt_only_blocked")
    output(payload, args.json)
    return 0 if allowed or mode == "prompt_only" else 1


def safe_output_name(value: str) -> str:
    name = Path(value).name
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip(".-")
    return name or "cover-output.png"


def unique_output_path(outputs_dir: Path, filename: str) -> Path:
    candidate = outputs_dir / filename
    if not candidate.exists():
        return candidate
    stem = candidate.stem
    suffix = candidate.suffix
    for counter in range(2, 1000):
        numbered = outputs_dir / f"{stem}-{counter}{suffix}"
        if not numbered.exists():
            return numbered
    raise FileExistsError(f"could not allocate output name for {filename}")


def sha256_text(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command_record_generation_output(args: argparse.Namespace) -> int:
    project_path = as_project_path(args)
    source = args.source_image.resolve()
    if not source.exists():
        raise FileNotFoundError(source)
    preflight = read_json(project_path / RESULT_FILES["preflight"])
    brief = project.load_brief(project_path)
    outputs_dir = project_path / "outputs"
    outputs_dir.mkdir(exist_ok=True)
    output_name = safe_output_name(args.output_name or source.name)
    destination = unique_output_path(outputs_dir, output_name)

    if source.resolve() != destination.resolve():
        shutil.copy2(source, destination)

    preflight_mode = preflight.get("reference_image_mode")
    final_eligible = bool(preflight.get("allowed")) and preflight_mode == "explicit"
    review_only_reason = None
    if args.reference_image_mode != "auto" and args.reference_image_mode != preflight_mode:
        final_eligible = False
        review_only_reason = "recorded reference mode does not match generation preflight"
    elif identity_required(brief) and preflight_mode != "explicit":
        final_eligible = False
        review_only_reason = "identity reference was required but not explicitly passed"
    elif not preflight.get("allowed"):
        final_eligible = False
        review_only_reason = "generation preflight did not pass"

    payload = {
        "schema_version": 1,
        "recorded_at": now_iso(),
        "status": "RECORDED",
        "source_path": str(source),
        "copied_path": str(destination),
        "relative_output": str(destination.relative_to(project_path)),
        "prompt_hash": sha256_text(project_path / "prompt-final.txt"),
        "generation_backend": args.generation_backend,
        "reference_image_mode": preflight_mode or args.reference_image_mode,
        "recorded_reference_image_mode": args.reference_image_mode,
        "identity_reference_required": identity_required(brief),
        "final_eligible": final_eligible,
        "review_only_reason": review_only_reason,
    }
    with project.project_lock(project_path):
        write_json(project_path / RESULT_FILES["generation"], payload)
        update_brief_status(project_path, "generation_output_recorded")
    output(payload, args.json)
    return 0


def resolve_image(project_path: Path, image: Path) -> Path:
    if image.is_absolute():
        return image.resolve()
    return (project_path / image).resolve()


def parse_dimension_stdout(stdout: str) -> dict:
    data: dict[str, str] = {}
    for line in stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            data[key.strip()] = value.strip()
    return data


def command_verify_image_dimensions(args: argparse.Namespace) -> int:
    project_path = as_project_path(args)
    brief = project.load_brief(project_path)
    image = resolve_image(project_path, args.image)
    if not image.exists():
        raise FileNotFoundError(image)
    preset = args.preset or project_canvas(brief)["preset"]
    cmd = [sys.executable, str(DIMENSION_SCRIPT), str(image), "--preset", preset]
    if args.ratio_only:
        cmd.append("--ratio-only")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=False)
    parsed = parse_dimension_stdout(result.stdout)
    payload = {
        "schema_version": 1,
        "checked_at": now_iso(),
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "image": str(image),
        "actual": parsed.get("actual"),
        "expected": parsed.get("expected"),
        "mode": parsed.get("mode"),
        "preset": preset,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }
    with project.project_lock(project_path):
        write_json(project_path / RESULT_FILES["dimension"], payload)
        if payload["status"] == "PASS" and payload["mode"] == "exact":
            update_brief_status(project_path, "dimension_verified")
    output(payload, args.json)
    return result.returncode


def command_mark_final(args: argparse.Namespace) -> int:
    project_path = as_project_path(args)
    generation = read_json(project_path / RESULT_FILES["generation"])
    if not generation:
        raise GateError("generation-manifest.json is missing")
    if not generation.get("final_eligible"):
        raise GateError(generation.get("review_only_reason") or "generation output is not final-eligible")
    dimension = read_json(project_path / RESULT_FILES["dimension"])
    if not dimension or dimension.get("status") != "PASS" or dimension.get("mode") != "exact":
        raise GateError("exact dimension check has not passed")
    output_path = generation.get("relative_output")
    if args.output:
        requested = resolve_image(project_path, args.output)
        recorded = Path(generation["copied_path"]).resolve()
        if requested != recorded:
            raise GateError("requested final output does not match generation manifest")
    payload = {
        "schema_version": 1,
        "finalized_at": now_iso(),
        "status": "FINAL",
        "selected_output": output_path,
        "dimension_check": str(project_path / RESULT_FILES["dimension"]),
        "generation_manifest": str(project_path / RESULT_FILES["generation"]),
        "notes": args.notes,
    }
    with project.project_lock(project_path):
        write_json(project_path / RESULT_FILES["final"], payload)
        metrics_path = project_path / "metrics.json"
        if metrics_path.exists():
            metrics = read_json(metrics_path)
            metrics["selected_output"] = output_path
            write_json(metrics_path, metrics)
        update_brief_status(project_path, "final_marked")
    output(payload, args.json)
    return 0


def add_text_source_args(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text")
    group.add_argument("--from-file", type=Path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=project.DEFAULT_PROJECT_ROOT)
    sub = parser.add_subparsers(dest="command", required=True)

    get_state = sub.add_parser("get-state")
    get_state.add_argument("--project-path", required=True, type=Path)
    get_state.add_argument("--json", action="store_true")
    get_state.set_defaults(func=command_get_state)

    list_backends = sub.add_parser("list-generation-backends")
    list_backends.add_argument("--json", action="store_true")
    list_backends.set_defaults(func=command_list_generation_backends)

    save_engine = sub.add_parser("save-engine-routing")
    save_engine.add_argument("--project-path", required=True, type=Path)
    add_text_source_args(save_engine)
    save_engine.add_argument("--json", action="store_true")
    save_engine.set_defaults(func=command_save_engine_routing)

    save_recs = sub.add_parser("save-skill-recommendations")
    save_recs.add_argument("--project-path", required=True, type=Path)
    add_text_source_args(save_recs)
    save_recs.add_argument("--json", action="store_true")
    save_recs.set_defaults(func=command_save_skill_recommendations)

    approve = sub.add_parser("set-approved")
    approve.add_argument("--project-path", required=True, type=Path)
    approve.add_argument("--direction-id", required=True)
    approve.add_argument("--approved-copy", required=True)
    approve.add_argument("--child-skill")
    approve.add_argument("--internal-paradigm")
    approve.add_argument("--approved-at")
    approve.add_argument("--notes")
    approve.add_argument("--json", action="store_true")
    approve.set_defaults(func=command_set_approved)

    packet = sub.add_parser("save-execution-packet")
    packet.add_argument("--project-path", required=True, type=Path)
    add_text_source_args(packet)
    packet.add_argument("--json", action="store_true")
    packet.set_defaults(func=command_save_execution_packet)

    prompt = sub.add_parser("save-final-prompt")
    prompt.add_argument("--project-path", required=True, type=Path)
    add_text_source_args(prompt)
    prompt.add_argument("--json", action="store_true")
    prompt.set_defaults(func=command_save_final_prompt)

    firewall = sub.add_parser("verify-prompt-firewall")
    firewall.add_argument("--project-path", required=True, type=Path)
    firewall.add_argument("--forbid", action="append", default=[])
    firewall.add_argument("--require-identity-reference", action="store_true")
    firewall.add_argument("--json", action="store_true")
    firewall.set_defaults(func=command_verify_prompt_firewall)

    preflight = sub.add_parser("preflight-generation")
    preflight.add_argument("--project-path", required=True, type=Path)
    preflight.add_argument("--generation-backend", required=True)
    preflight.add_argument(
        "--reference-image-mode",
        choices=["auto", "explicit", "text_only", "unknown"],
        default="auto",
    )
    preflight.add_argument(
        "--reference-evidence",
        action="append",
        default=[],
        help="Evidence that the backend received the reference image, e.g. attached_conversation_image.",
    )
    preflight.add_argument("--json", action="store_true")
    preflight.set_defaults(func=command_preflight_generation)

    record = sub.add_parser("record-generation-output")
    record.add_argument("--project-path", required=True, type=Path)
    record.add_argument("--source-image", required=True, type=Path)
    record.add_argument("--output-name")
    record.add_argument("--generation-backend", required=True)
    record.add_argument(
        "--reference-image-mode",
        choices=["auto", "explicit", "text_only", "unknown"],
        required=True,
    )
    record.add_argument("--json", action="store_true")
    record.set_defaults(func=command_record_generation_output)

    dimensions = sub.add_parser("verify-image-dimensions")
    dimensions.add_argument("--project-path", required=True, type=Path)
    dimensions.add_argument("--image", required=True, type=Path)
    dimensions.add_argument("--preset")
    dimensions.add_argument("--ratio-only", action="store_true")
    dimensions.add_argument("--json", action="store_true")
    dimensions.set_defaults(func=command_verify_image_dimensions)

    final = sub.add_parser("mark-final")
    final.add_argument("--project-path", required=True, type=Path)
    final.add_argument("--output", type=Path)
    final.add_argument("--notes")
    final.add_argument("--json", action="store_true")
    final.set_defaults(func=command_mark_final)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except Exception as exc:  # noqa: BLE001 - CLI should return clean gate errors.
        payload = {"status": "ERROR", "message": str(exc)}
        if getattr(args, "json", False):
            print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
        else:
            print(f"coverctl error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
