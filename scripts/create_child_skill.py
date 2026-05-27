#!/usr/bin/env python3
"""Create an indexable PigeonYang cover-style child skill from design standard markdown."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_STANDARD_SECTIONS = [
    "## Scope",
    "## Evidence Summary",
    "## Core Design DNA",
    "## Cover Generation Engine",
    "## Popular Paradigms",
    "## Topic Translation Rules",
    "## Cover Storyboard Rules",
    "## Design Layout Brief Rules",
    "## Copy Hierarchy Rules",
    "## Platform Adaptation",
    "## Layout Patterns",
    "## Subject Rules",
    "## Reference Image Handling",
    "## Identity And Final Prompt Firewall",
    "## Text Rules",
    "## Typography Layout System",
    "## Color And Lighting Rules",
    "## Hook Mechanics",
    "## GPT Image 2 Prompt Contract",
    "## Negative Constraints",
    "## User Intake Questions",
    "## Quality Checklist",
]


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    if not value:
        raise ValueError("creator id must contain at least one ASCII letter or digit")
    return value


def yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def validate_standard(standard: str) -> None:
    missing = [section for section in REQUIRED_STANDARD_SECTIONS if section not in standard]
    if missing:
        raise ValueError(
            "design standard is missing required section(s): " + ", ".join(missing)
        )


def build_skill_md(creator_id: str, creator_name: str, standard: str) -> str:
    skill_name = f"pigeonyang-cover-style-{creator_id}"
    description = (
        f"PigeonYang-branded skill that uses the distilled {creator_name} video cover and thumbnail design pattern "
        "to write GPT Image 2-ready prompts for original user covers. Trigger when "
        f"the user asks for a cover in {creator_name}'s style, references "
        f"{creator_name} thumbnails, or asks to apply this creator cover formula."
    )
    return f'''---
name: {skill_name}
description: "{yaml_escape(description)}"
---

# PigeonYang {creator_name} Cover Style

## Role

Use this distilled creator-cover pattern to write original, GPT Image 2-ready cover prompts for the user's video.

Do not copy existing {creator_name} thumbnails. Apply the transferable design strategy to the user's own topic, brand, face, product, and constraints.

## Identity And Final Prompt Firewall

The distilled creator name is an internal routing and analysis label only.

Never put `{creator_name}`, `{creator_name}-inspired`, `in the style of {creator_name}`, `like {creator_name}`, or equivalent creator-name shortcuts in the final GPT Image 2 generation prompt. Rewrite the pattern into concrete design rules: subject role, story moment, proof object, composition, typography, color, lighting, and negative constraints.

If the user supplies a portrait/reference image, that reference controls identity. Preserve the user's face, hair, glasses, clothing cues, body type, and other supplied identity traits. Redesign only the pose/action for the thumbnail hook unless the user explicitly asks to preserve the original pose. The final generation prompt must say the subject must not resemble any public creator, without naming {creator_name}.

## Required User Inputs

Ask the publishing platform first, then ask only for missing production fields.

Platform guidance:

| Platform | Recommended cover ratio | Target canvas | Notes |
|---|---:|---:|---|
| YouTube long video | 16:9 | 1280x720 | Best fit for wide comparison, crowd, and spectacle layouts. |
| Bilibili native upload | 1146:717, approx 16:10 | 1146x717 | Use when the cover is Bilibili-only; keep face/text in a 16:9 and 4:3 safe center area. |
| Bilibili cross-platform | 16:9 | 1920x1080 | Use when reusing with YouTube or wide feeds; preserve Bilibili-safe center crop. |
| Bilibili 4:3-safe | 4:3 | 1440x1080 | Use when the user cares about Bilibili card/homepage crop safety. |
| Douyin horizontal video | 4:3 | 1440x1080 | Compress wide logic; avoid critical side-edge text. |
| Douyin vertical video | 3:4 | 1080x1440 | Use portrait cover composition; keep face/text central and avoid edge-critical details. |
| Xiaohongshu | 3:4 | 1080x1440 | Use note/card style portrait composition. |
| Xiaohongshu square | 1:1 | 1080x1080 | Use central subject plus two contrast cues. |
| TikTok / Reels / Shorts | 9:16 | 1080x1920 | Use vertical poster logic; avoid YouTube-style split-screen. |
| WeChat video account | 6:7 or 3:4 | 1080x1260 or 1080x1440 | Ask for account preference if uncertain. |

Missing fields:

- video topic or title
- exact on-cover text, if any
- target platform, orientation, aspect ratio, and target canvas
- user's own portrait/reference image, if identity matters
- whether the reference pose should be preserved; default to redesigning the pose for the thumbnail hook
- must-include elements
- must-avoid elements
- brand or legal constraints

## Prompt Workflow

1. Extract the relevant design rules from the distilled research below.
2. Use the cover generation engine and topic translation rules to convert the user's raw topic into this creator's cover logic before choosing visual style.
3. Select one internal paradigm from `Popular Paradigms`. Record why it fits and why the other internal paradigms were rejected. If no paradigm fits, route away from this child skill.
4. Build a one-frame cover storyboard: visible conflict, subject action, proof object, emotional beat, viewer question, and forbidden static-poster failure mode.
5. Build a design layout brief: first-read, second-read, third-read, layout zones, visual weight, reading path, negative space, and forbidden layouts.
6. Build a copy hierarchy: main title, subtitle if any, state labels if any, object/zone binding, isolation rules, forbidden adjacency, and text removal rule.
7. Select the platform ratio and target canvas, then adapt the layout before writing the visual concept.
8. If a reference image is provided, split it into identity traits to preserve and pose/action traits to ignore unless the user explicitly asks to preserve them.
9. If the exact on-cover text is not supplied, or if the user's title is shortened or rewritten, run the Copy Approval Gate and wait for explicit approval of the exact on-cover text.
10. Produce an Execution Design Packet with copy approval, selected internal paradigm, rejected internal paradigms, topic translation, cover storyboard, design layout brief, copy hierarchy, reference handling, identity and final-prompt firewall, and pre-generation self-check.
11. If any self-check item fails, revise the Execution Design Packet before writing the final image prompt.
12. Map the approved storyboard and layout brief to one clear cover concept and choose the subject role/action required by the selected internal paradigm.
13. Write a GPT Image 2 prompt packet with platform adaptation, reference handling, identity preservation, composition, subject, typography layout system, lighting, readability, and negative constraints.
14. Save the exact final generation prompt through the mother skill's workflow gate, preferably `scripts/coverctl.py save-final-prompt`, then run `scripts/coverctl.py verify-prompt-firewall` with `{creator_name}` and common aliases passed as `--forbid`. If a portrait/reference image is supplied, require identity-reference handling. Do not generate if the firewall fails.
15. Run `scripts/coverctl.py preflight-generation`. If it returns `generate`, generate directly without asking for another approval. If it returns `prompt_only`, output the exact final prompt and the missing generation condition.
16. Register any generated output, verify dimensions, and mark final only through the workflow gate.

## Execution Gate

Do not write the final GPT Image 2 prompt, and do not generate an image, unless the current turn contains a concrete Execution Design Packet.

Required packet fields:

- Copy approval: exact approved on-cover text, or "no text". If the user's title was shortened or rewritten, include the approved candidate. Permission to shorten is not approval of a specific title.
- Selected internal paradigm: the chosen `Popular Paradigms` card and why it fits this task.
- Rejected internal paradigms: which other internal paradigms were considered and why they were not chosen.
- Topic translation: raw topic, creator-engine translation, click promise, visible stake, proof object, and forbidden drift.
- Cover storyboard: story moment, conflict, subject action, proof object, emotional beat, viewer question, and why it is not a static poster.
- Design layout brief: first-read, second-read, third-read, layout zones, visual weight, reading path, negative space, platform safe area, and forbidden layouts.
- Copy hierarchy: main title, subtitle if any, labels if any, object/zone binding, isolation rules, forbidden adjacency, and removal rule.
- Reference handling: identity traits to preserve, pose/action traits to ignore, and new hook-driven action.
- Identity and final-prompt firewall: who the subject must look like, which reference controls identity, which creator/style words are forbidden in the final prompt, how the creator pattern is rewritten without naming the creator, and the exact `verify_prompt_firewall.py` command that must pass before generation.
- Pre-generation self-check: engine match, story clarity, flat design hierarchy, copy isolation, platform safe area, reference handling, and drift risk.
- Post-generation dimension check: after image generation, verify actual pixel dimensions against the requested target canvas or aspect ratio before reporting success. Use the mother skill's `scripts/verify_image_dimensions.py` when a local generated file is available.

If the packet is weak, fix the packet first. Do not compensate by adding more visual adjectives to the final prompt.

## Copy Approval Gate

If changing the user's title, stop before final prompt writing and provide:

- 3-5 candidate on-cover titles
- the semantic meaning each candidate preserves
- the meaning each candidate drops or weakens
- one recommendation

Continue only after the user approves one exact title or provides replacement text.

## Output Format

```markdown
## Execution Design Packet
Copy approval:
Selected internal paradigm:
Rejected internal paradigms:
Topic translation:
Cover storyboard:
Design layout brief:
Copy hierarchy:
Reference handling:
Identity and final-prompt firewall:
Pre-generation self-check:

## Cover Prompt
<final GPT Image 2 prompt>

## Generation Settings
model: gpt-image-2
platform:
aspect_ratio:
target_canvas:
quality:
post_generation_check:

## Negative Constraints
<constraints>

## Iteration Plan
<2-3 likely improvements after first image>

## Generation Gate
<generate directly if preflight passes; otherwise output prompt_only with blocker>
```

## Design Standard

{standard.strip()}
'''


def build_openai_yaml(creator_name: str) -> str:
    return f'''display_name: "PigeonYang {yaml_escape(creator_name)} Cover Style"
short_description: "GPT Image 2 cover prompts in this creator pattern."
default_prompt: "Write a GPT Image 2 video cover prompt using this distilled cover pattern. Do not include the creator name or inspired-by wording in the final generation prompt."
'''


def build_skill_json(creator_id: str, version: str, kind: str) -> str:
    data = {
        "name": f"pigeonyang-cover-style-{creator_id}",
        "version": version,
        "kind": kind,
        "package": "pigeonyang-cover-style-skills",
        "package_version": version,
    }
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def resolve_skill_kind(skill_dir: Path, requested_kind: str | None) -> str:
    if requested_kind:
        return requested_kind
    metadata = skill_dir / "skill.json"
    if metadata.exists():
        data = json.loads(metadata.read_text(encoding="utf-8"))
        existing_kind = data.get("kind")
        if existing_kind in {"child", "child-example"}:
            return existing_kind
    return "child"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--creator-id", required=True)
    parser.add_argument("--creator-name", required=True)
    parser.add_argument("--source", required=True, type=Path, help="Path to distillation/design-standard.md")
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--skill-version", default="0.1.0")
    parser.add_argument("--kind", choices=["child", "child-example"])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    creator_id = slugify(args.creator_id)
    if not re.match(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$", args.skill_version):
        raise ValueError("--skill-version must be semantic, for example 0.1.0")
    source = args.source.resolve()
    output_root = args.output_root.resolve()
    if not source.exists():
        raise FileNotFoundError(source)

    skill_dir = output_root / f"pigeonyang-cover-style-{creator_id}"
    if skill_dir.exists() and not args.force:
        raise FileExistsError(f"{skill_dir} already exists; pass --force to overwrite")
    skill_kind = resolve_skill_kind(skill_dir, args.kind)

    standard = source.read_text(encoding="utf-8")
    validate_standard(standard)
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        build_skill_md(creator_id, args.creator_name, standard),
        encoding="utf-8",
    )
    (skill_dir / "skill.json").write_text(
        build_skill_json(creator_id, args.skill_version, skill_kind),
        encoding="utf-8",
    )
    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(exist_ok=True)
    (agents_dir / "openai.yaml").write_text(
        build_openai_yaml(args.creator_name),
        encoding="utf-8",
    )
    print(skill_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

