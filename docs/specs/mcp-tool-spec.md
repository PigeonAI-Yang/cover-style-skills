# SPEC: Local MCP Workflow Engine

## Purpose
The MCP should make the cover workflow stable. It should not replace Agent design judgment.

Prototype implementation:

- `mcp-server/cover_project_server.py`
- `mcp-server/README.md`
- `scripts/coverctl.py`

The prototype wraps `scripts/manage_cover_project.py` for legacy project
operations and `scripts/coverctl.py` for workflow gates. It uses dependency-free
JSON-RPC stdio for local validation. Treat it as an implementation scaffold, not
as a replacement for Codex's creative/runtime image path.

## Current Limitation
The prototype currently protects filesystem writes and project metadata, but it
does not enforce the cover-production sequence. An Agent can still skip
child-skill routing, skip the execution packet, write a final prompt by hand, or
call image generation before identity-reference and dimension gates are proven.

Phase 3 upgrades the MCP from a project-file boundary into a workflow gate. The
MCP still should not decide creative direction, but it must refuse deterministic
state transitions when required upstream artifacts or validation results are
missing.

## Responsibility Split
Skill responsibilities:
- Interpret article meaning.
- Choose cover hooks.
- Design child-skill recommendation cards.
- Write execution packets and final prompts.
- Judge creative fit and iteration direction.

MCP responsibilities:
- Create private project folders.
- Save and read project artifacts.
- Resolve platform cover specs.
- Run deterministic validation.
- Record outputs and metrics.
- Prevent accidental writes to the product repo.
- Track workflow state and refuse invalid transitions.
- Prove that generation preflight has passed before a final image can be marked.

## Workflow State Model
Each private cover project has an explicit state derived from project artifacts
and validation results. The server should compute state from files instead of
trusting an Agent's claim.

| State | Required artifact or result | Next allowed action |
|---|---|---|
| `brief_created` | `brief.json` and optional `source.md` | route article |
| `routing_completed` | `engine-routing.md` and `directions.md` | approve child skill |
| `child_skill_approved` | `approved-direction.md` | save execution packet |
| `execution_packet_saved` | `execution-packet.md` | save final prompt |
| `final_prompt_saved` | `prompt-final.txt` | run prompt firewall |
| `prompt_firewall_passed` | `firewall-result.json` with pass status | run generation preflight |
| `generation_preflight_passed` | `generation-preflight.json` with pass status | call image generation outside MCP or record output |
| `generation_output_recorded` | output file and `generation-manifest.json` | verify dimensions |
| `dimension_verified` | `dimension-check.json` with exact pass | mark final |
| `final_marked` | `review.md` or `final-manifest.json` | record metrics |

Hard rule: no state can be advanced by text alone. Every transition must be
backed by a known artifact, a validation result, or a registered generated file.

## MVP Tools

### `create_cover_project`
Creates a private project folder under `J:\PigeonYang\cover-style-distiller\cover-projects`.

Inputs:
- `title`
- `platform`
- `slug` optional

Outputs:
- `project_id`
- `project_path`

Implementation: `scripts/manage_cover_project.py create`.

### `save_brief`
Writes `brief.json` and optional `source.md`.

Implementation status: covered by `create_cover_project` for MVP creation.

### `save_directions`
Writes `directions.md` containing the child-skill recommendation packet: child
skill, fit score, recommendation reason, proposed design scheme, proposed copy,
risk, and canvas constraints.

Implementation: `scripts/manage_cover_project.py save-artifact --artifact directions`.

Phase 3 validation:
- Refuse if `engine-routing.md` is missing.
- Require each recommendation to name a child skill, fit score, proposed copy,
  canvas preset, target canvas, safe area, design scheme, and risk.
- Require at least one recommended child skill and no more than three.

### `save_approved_direction`
Writes the selected direction and approved copy.

Implementation: `scripts/manage_cover_project.py set-approved`.

Phase 3 validation:
- `direction_id` must resolve to a recommendation in `directions.md`.
- The approved record must store the selected child skill and exact on-cover
  copy. The approval object is the child skill, not a generic visual direction.

### `save_execution_packet`
Writes `execution-packet.md`.

Implementation: `scripts/manage_cover_project.py save-artifact --artifact execution-packet`.

Phase 3 validation:
- Refuse if no approved child skill exists.
- Require packet sections for copy approval, topic translation, cover storyboard,
  design layout brief, copy hierarchy, reference handling, identity and
  final-prompt firewall, pre-generation self-check, and post-generation
  dimension check.
- Require the packet to name the approved child skill internally while preserving
  final-prompt firewall rules.

### `save_final_prompt`
Writes `prompt-final.txt`.

Implementation: `scripts/manage_cover_project.py save-artifact --artifact prompt-final`.

Phase 3 validation:
- Refuse if `execution-packet.md` is missing.
- Require explicit platform wording, aspect ratio, target canvas, and safe-area
  rules.
- If identity reference is required, require the prompt to mention the private
  identity reference requirement without leaking creator names or style-copy
  wording.

### `verify_prompt_firewall`
Checks for forbidden creator names, missing identity requirements, unsupported photorealistic drift, and missing platform canvas.

Phase 3 implementation:
- Wrap `scripts/verify_prompt_firewall.py`.
- Save a machine-readable `firewall-result.json`.
- Refuse pass status when forbidden creator names or aliases appear in
  `prompt-final.txt`.
- Refuse pass status when a required identity reference is not declared.
- Refuse pass status when WeChat canvas strings are missing.

### `resolve_platform_canvas`
Returns platform dimensions, ratio, and safe-area guidance. First required platform: WeChat public account cover.

Implementation: `mcp-server/cover_project_server.py` static resolver.

### `record_generation_output`
Copies or registers the generated image under `outputs/`.

For skill preview references, outputs should be stored under
`outputs/direction-references/` and linked from `directions.md`.

Phase 3 implementation:
- Copy, never move, generated images from Codex's generated image directory.
- Write `generation-manifest.json` with source path, copied path, prompt hash,
  generation backend label, reference-image capability declaration, and timestamp.
- If identity reference was required, record whether the backend call had an
  explicit reference-image input. If not, mark the output as review-only and not
  final-eligible.

### `verify_image_dimensions`
Checks output dimensions and aspect ratio.

Phase 3 implementation:
- Wrap `scripts/verify_image_dimensions.py`.
- Save `dimension-check.json`.
- Exact target canvas is required for final covers.
- Ratio-only pass is allowed only for optional previews or rejected experiments.

### `preflight_generation`
Determines whether the current project is allowed to generate a final image.

Inputs:
- `project_path`
- `generation_backend`
- `reference_image_mode`: `explicit`, `text_only`, or `unknown`

Outputs:
- `allowed`
- `mode`: `generate` or `prompt_only`
- blocking reasons
- required next artifact

Rules:
- Refuse if approved child skill, execution packet, final prompt, or firewall
  pass result is missing.
- Refuse final generation when identity reference is required and
  `reference_image_mode` is not `explicit`.
- Return `prompt_only` instead of `generate` when the only blocker is missing
  explicit reference-image capability.
- Save `generation-preflight.json`.

### `mark_final`
Marks a generated output as final.

Rules:
- Refuse unless `generation-manifest.json` exists.
- Refuse unless `dimension-check.json` has exact pass for the target canvas.
- Refuse if identity reference was required but generation manifest says the
  reference image was not explicitly passed.
- Record the selected output in `metrics.json` or `final-manifest.json`.

### `update_metrics`
Updates `metrics.json` after publishing.

Implementation: `scripts/manage_cover_project.py update-metrics`.

## Non-Goals
- MCP does not call GPT Image 2 in MVP.
- MCP does not publish to WeChat.
- MCP does not decide creative direction.
- MCP does not make an unsafe direct image-generation call just to avoid a
  prompt-only handoff. Reference-image capability must be explicit.

## Safety Rules
- Refuse project paths inside the product repo.
- Refuse writes outside the configured private project root unless explicitly allowed.
- Use JSON schemas for machine-written files.
- Keep every write idempotent or versioned.
- Refuse to mark final if any required gate is represented only by prose in a
  chat transcript.
