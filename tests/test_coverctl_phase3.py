from __future__ import annotations

import json
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PRODUCT_ROOT = Path(__file__).resolve().parents[1]
MANAGE = PRODUCT_ROOT / "scripts" / "manage_cover_project.py"
COVERCTL = PRODUCT_ROOT / "scripts" / "coverctl.py"


ENGINE_ROUTING = """# Engine Routing

## Article Diagnosis
- Reader pain / desire: AI practice cannot become publishable content.
- Hook type: concrete system proof.
- Visual proof needed: a tactile content flywheel.
- Identity constraints: PigeonYang anime identity.
- Platform constraints: WeChat main cover.

## Candidate Engines

### Candidate 1
- Child skill: pigeonyang-cover-style-he-tongxue
- Candidate internal paradigms: Macro Proof State; Oversized Object Demonstration; Binary Test
- Selected internal paradigm: Macro Proof State
- Fit score: 0.92
- Why it fits: turns abstract AI workflow into a visible proof object.
- Why this paradigm fits: the article needs one readable proof object instead of a multi-step diagram.
- What visual promise it creates: messy inputs become article output.
- Risk: too much machine detail.
- User-facing recommendation reason: best match for maker proof.
- Direction reference prompt: optional only.

## Rejected Engines
- Child skill: pigeonyang-cover-style-dan-koe
- Why rejected: too text-authority first.

## Recommendation
Use recommendation cards in directions.md.
"""


DIRECTIONS = """# Skill Recommendation Packet

## Recommendation 1
- Recommended child skill: pigeonyang-cover-style-he-tongxue
- Selected internal paradigm: Macro Proof State
- Fit score: 0.92
- Why this skill is recommended: the article is about making an AI workflow feel like a real product.
- Why this paradigm fits: the cover can make one output screen or workbench object the first read.
- Rejected internal paradigms: Binary Test lacks a true before/after pair; Absurd Utility Action would overplay the article.
- Target canvas: WeChat public account article main cover, 2350x1000, 2.35:1, x=675..1675
- Hook angle: messy practice materials become publishable content.
- Proposed on-cover copy: 这是内容飞轮
- Visual premise: a compact workbench device turns SKILL, APP, LOG, 截图 into one polished article card.
- PigeonYang character pose / expression: calm maker-demonstrator beside the device.
- Background, object, or proof cue: off-white workbench, one circular flywheel, one output card.
- Text hierarchy: title first, proof device second, labels third.
- Why it may improve open rate: concrete proof object makes the abstract system understandable.
- Risk or possible misread: may become a dense architecture diagram if overdone.
"""


EXECUTION_PACKET = """# Execution Design Packet

## Copy Approval
Approved child skill: pigeonyang-cover-style-he-tongxue.
Selected internal paradigm: Macro Proof State.
Approved copy: 这是内容飞轮.

## Selected Internal Paradigm
Macro Proof State: make one proof object or output screen the first read.

## Rejected Internal Paradigms
Binary Test lacks a true before/after pair; Absurd Utility Action would overplay the article.

## Article Hook Translation
Turn abstract AI content workflow into a tactile proof object.

## Cover Storyboard
PigeonYang demonstrates a compact content flywheel device.

## Design Layout Brief
Title and face stay inside x=675..1675; object remains central.

## Copy Hierarchy
Only main title plus short object labels.

## Reference Handling
Preserve PigeonYang identity from the private reference image.

## Identity And Final-Prompt Firewall
The prompt must preserve identity and must not name public creators.

## Pre-Generation Self-Check
- Engine match: pass
- Story clarity: pass
- Copy isolation: pass
- Platform safe area: pass
- Target canvas: pass
- Reference handling: pass
- Identity firewall: pass
- Drift risk: controlled

## Post-Generation Dimension Check
- Required preset: wechat-article-main
- Exact target canvas: 2350x1000
- Ratio-only preview policy: preview only
- Finalization rule: exact pass required
"""


FINAL_PROMPT = """Create a finished WeChat public account article main cover.
Use 2.35:1 aspect ratio and target canvas 2350x1000 pixels.
Keep the main face, title, and proof object inside the central square-safe zone x=675..1675.
Preserve PigeonYang anime identity from the private identity reference image: silver-gray short hair, glasses, refined all-black clothing, calm intelligent expression.
The subject must not resemble any public creator.
The only main title is: 这是内容飞轮.
Show a clean workbench proof object that turns SKILL, APP, LOG, 截图 into one polished article card and feedback signal.
"""


def run_command(args: list[str], expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", check=False)
    if result.returncode != expected:
        raise AssertionError(
            f"expected {expected}, got {result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def run_coverctl(root: Path, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    return run_command([sys.executable, str(COVERCTL), "--root", str(root), *args], expected)


def fake_png(path: Path, width: int, height: int) -> None:
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", width, height))


class CoverctlPhase3Test(unittest.TestCase):
    def test_workflow_gates_prompt_only_and_final_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            root = temp_path / "cover-projects"
            identity = temp_path / "identity.png"
            identity.write_bytes(b"identity-reference")

            created = run_command(
                [
                    sys.executable,
                    str(MANAGE),
                    "--root",
                    str(root),
                    "create",
                    "--title",
                    "AI Flywheel Builder",
                    "--identity-reference",
                    str(identity),
                    "--json",
                ]
            )
            project_path = Path(json.loads(created.stdout)["project_path"])

            early_prompt = run_coverctl(
                root,
                "save-final-prompt",
                "--project-path",
                str(project_path),
                "--text",
                FINAL_PROMPT,
                "--json",
                expected=1,
            )
            self.assertIn("execution-packet.md", early_prompt.stderr)

            run_coverctl(
                root,
                "save-engine-routing",
                "--project-path",
                str(project_path),
                "--text",
                ENGINE_ROUTING,
                "--json",
            )
            run_coverctl(
                root,
                "save-skill-recommendations",
                "--project-path",
                str(project_path),
                "--text",
                DIRECTIONS,
                "--json",
            )
            approved = run_coverctl(
                root,
                "set-approved",
                "--project-path",
                str(project_path),
                "--direction-id",
                "direction-1",
                "--approved-copy",
                "这是内容飞轮",
                "--json",
            )
            self.assertEqual(
                json.loads(approved.stdout)["approved_internal_paradigm"],
                "Macro Proof State",
            )
            run_coverctl(
                root,
                "save-execution-packet",
                "--project-path",
                str(project_path),
                "--text",
                EXECUTION_PACKET,
                "--json",
            )
            run_coverctl(
                root,
                "save-final-prompt",
                "--project-path",
                str(project_path),
                "--text",
                FINAL_PROMPT,
                "--json",
            )
            run_coverctl(
                root,
                "verify-prompt-firewall",
                "--project-path",
                str(project_path),
                "--forbid",
                "He Tongxue",
                "--json",
            )

            prompt_only = run_coverctl(
                root,
                "preflight-generation",
                "--project-path",
                str(project_path),
                "--generation-backend",
                "codex-image-gen",
                "--json",
            )
            self.assertEqual(json.loads(prompt_only.stdout)["mode"], "prompt_only")
            self.assertEqual(json.loads(prompt_only.stdout)["reference_image_mode"], "unknown")

            state = run_coverctl(
                root,
                "get-state",
                "--project-path",
                str(project_path),
                "--json",
            )
            self.assertEqual(json.loads(state.stdout)["state"], "prompt_only_blocked")

            run_coverctl(
                root,
                "preflight-generation",
                "--project-path",
                str(project_path),
                "--generation-backend",
                "codex-image-gen",
                "--reference-evidence",
                "attached_conversation_image",
                "--json",
            )
            generated = temp_path / "generated.png"
            fake_png(generated, 2350, 1000)
            run_coverctl(
                root,
                "record-generation-output",
                "--project-path",
                str(project_path),
                "--source-image",
                str(generated),
                "--output-name",
                "cover-v001.png",
                "--generation-backend",
                "codex-image-gen",
                "--reference-image-mode",
                "explicit",
                "--json",
            )
            run_coverctl(
                root,
                "verify-image-dimensions",
                "--project-path",
                str(project_path),
                "--image",
                "outputs/cover-v001.png",
                "--json",
            )
            run_coverctl(root, "mark-final", "--project-path", str(project_path), "--json")

            final_state = run_coverctl(
                root,
                "get-state",
                "--project-path",
                str(project_path),
                "--json",
            )
            self.assertEqual(json.loads(final_state.stdout)["state"], "final_marked")


if __name__ == "__main__":
    unittest.main()
