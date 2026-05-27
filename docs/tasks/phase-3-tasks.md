# TASKS: Phase 3

## Goal
Turn the cover workflow from advisory skill instructions into an enforced local
workflow gate. The Agent may still make creative judgments, but deterministic
state transitions must be validated by scripts or MCP tools.

## Task 1: Workflow State Model
Status: completed 2026-05-27

- Define the project state machine from `brief_created` to `final_marked`.
- Compute state from project files instead of chat history.
- Add machine-readable validation results for firewall, generation preflight,
  generation manifest, dimension check, and final manifest.
- Refuse downstream operations when required upstream artifacts are missing.

Acceptance:
- A command or MCP tool can return current project state and blocking reasons.
- Missing `approved-direction.md` blocks execution packet save.
- Missing `execution-packet.md` blocks final prompt save.

Implementation:
- `scripts/coverctl.py get-state`
- State result files: `firewall-result.json`, `generation-preflight.json`,
  `generation-manifest.json`, `dimension-check.json`, `final-manifest.json`

## Task 2: MCP Tool Expansion
Status: completed 2026-05-27

- Extend `product/mcp-server/cover_project_server.py` beyond filesystem wrapper
  behavior.
- Add tools or equivalent command paths for:
  - `get_project_state`
  - `save_engine_routing`
  - `save_skill_recommendations`
  - `save_execution_packet`
  - `save_final_prompt`
  - `verify_prompt_firewall`
  - `preflight_generation`
  - `record_generation_output`
  - `verify_image_dimensions`
  - `mark_final`

Acceptance:
- Tool list exposes workflow-gate operations.
- Invalid transition attempts return structured errors.
- Existing project-path safety rules remain intact.

Implementation:
- `mcp-server/cover_project_server.py` now routes gated operations through
  `scripts/coverctl.py`.
- Legacy `save_artifact` redirects gated artifacts and refuses direct
  `approved-direction` writes.

## Task 3: Execution Packet Gate
Status: completed 2026-05-27

- Require approved child skill and exact on-cover copy before saving an execution
  packet.
- Validate required packet sections:
  - copy approval
  - topic translation
  - cover storyboard
  - design layout brief
  - copy hierarchy
  - reference handling
  - identity and final-prompt firewall
  - pre-generation self-check
  - post-generation dimension check
- Block weak packets instead of compensating with longer image prompts.

Acceptance:
- Packet save fails without approved child skill.
- Packet save fails when reference handling or firewall sections are missing.

Implementation:
- `scripts/coverctl.py save-execution-packet`

## Task 4: Final Prompt And Firewall Gate
Status: completed 2026-05-27

- Save final prompts only after a valid execution packet exists.
- Wrap `scripts/verify_prompt_firewall.py` through MCP or `coverctl`.
- Persist `firewall-result.json`.
- Require platform, aspect ratio, target canvas, safe area, and identity-reference
  language.
- Block public creator names, style-copy wording, and missing identity
  requirement.

Acceptance:
- Final prompt cannot be marked firewall-passed from chat text alone.
- Forbidden creator aliases fail the gate.
- Missing WeChat canvas strings fail the gate.

Implementation:
- `scripts/coverctl.py save-final-prompt`
- `scripts/coverctl.py verify-prompt-firewall`

## Task 5: Identity Reference Preflight
Status: completed 2026-05-27

- Add `generation-preflight.json`.
- Require the private identity reference for PigeonYang WeChat covers by default:
  `J:\PigeonYang\cover-style-distiller\cover-projects\_identity\pigeonyang-character-reference.png`
- Record whether the available generation backend can explicitly receive the
  reference image.
- If reference-image mode is `text_only` or `unknown`, return `prompt_only`
  instead of allowing final generation.

Acceptance:
- A required identity reference with unknown image-input capability blocks final
  generation.
- The system can still produce a prompt-only deliverable with a clear missing
  condition.

Implementation:
- `scripts/coverctl.py preflight-generation`

## Task 6: Generation Output Registration
Status: completed 2026-05-27

- Copy generated images into the private project's `outputs/` directory without
  deleting originals.
- Write `generation-manifest.json` with source path, copied path, prompt hash,
  backend label, reference-image mode, and timestamp.
- Mark outputs generated without explicit identity reference as review-only when
  identity reference was required.

Acceptance:
- A generated image outside the private project is not final-eligible until
  registered.
- Manifest records whether reference image was explicitly passed.

Implementation:
- `scripts/coverctl.py record-generation-output`

## Task 7: Dimension Verification And Finalization
Status: completed 2026-05-27

- Wrap `scripts/verify_image_dimensions.py`.
- Persist `dimension-check.json`.
- Require exact `2350x1000` pass for WeChat article main final covers.
- Add `mark_final` gate that refuses ratio-only passes and unregistered outputs.

Acceptance:
- `1923x818` can pass ratio-only preview checks but cannot be marked final.
- `mark_final` fails without exact dimension verification.

Implementation:
- `scripts/coverctl.py verify-image-dimensions`
- `scripts/coverctl.py mark-final`

## Task 8: Codex Integration Path
Status: completed 2026-05-27

- Decide whether Phase 3 uses a registered MCP server, a local `coverctl`
  command, or both.
- Document the shortest local run path.
- If using MCP, add setup instructions and verify the server appears as callable
  tools in Codex.
- If using `coverctl`, make the Agent workflow call it before any generation.

Acceptance:
- A new Codex session can discover or run the gate without relying on memory.
- The documented run path reproduces state checks on a private cover project.

Implementation:
- Canonical local path: `scripts/coverctl.py`.
- MCP wrapper path: `mcp-server/cover_project_server.py`.
- Workflow references added to `SKILL.md`, `mcp-server/README.md`, and
  `docs/specs/agent-workflow-spec.md`.
- Installable MCP entrypoint: `pigeonyang-cover-mcp`.
- Packaging spec: `docs/specs/mcp-package-spec.md`.

## Task 9: Regression Dry Run
Status: completed 2026-05-27

- Re-run the AI Flywheel Builder cover project from the saved article material.
- Produce a child-skill recommendation packet first.
- Save execution packet, final prompt, firewall result, generation preflight,
  output manifest, dimension check, and review notes.
- Do not generate final output if identity reference cannot be explicitly passed.

Acceptance:
- The previous failure mode, hand-written prompt plus direct generation, is
  blocked by tooling.
- The project can end in either `final_marked` or `prompt_only_blocked`, with a
  machine-readable reason.

Progress:
- Added automated regression coverage in `tests/test_coverctl_phase3.py`.
- Re-ran the existing AI Flywheel Builder private project through `coverctl`.
- Produced `engine-routing.md`, `directions.md`, `approved-direction.md`,
  `execution-packet.md`, `prompt-final.txt`, `firewall-result.json`, and
  `generation-preflight.json`.
- Final state is `prompt_only_blocked` with machine-readable blocker:
  required identity reference is not proven as an explicit image input.
