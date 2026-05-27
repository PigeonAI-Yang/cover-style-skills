# SPEC: Agent Cover Workflow

## Runtime
The workflow runs in Codex. Skills handle reasoning and prompt design. Scripts or MCP tools handle deterministic project operations.

The Agent must treat deterministic workflow gates as executable constraints, not
as optional documentation. If a local MCP or `coverctl` gate exists, final prompt
writing, generation preflight, output registration, dimension verification, and
final marking must go through that gate.

Deterministic project operations are implemented in:

- `scripts/manage_cover_project.py`
- `scripts/coverctl.py`
- `schemas/cover-project/brief.schema.json`
- `schemas/cover-project/metrics.schema.json`
- `templates/cover-project/`
- `docs/specs/skill-router-spec.md`

## Inputs
The Agent accepts any of:

- Article title only
- Title plus summary
- Full article Markdown
- Existing draft file path

When input is weak, the Agent should still produce child-skill recommendations,
but must mark assumptions explicitly.

## Workflow
1. Create or select a private cover project under `cover-projects` with `scripts/manage_cover_project.py create`.
2. Save the raw input as project source material.
3. Extract article promise, reader pain, contradiction, stakes, and strongest open-rate hook.
4. Write `engine-routing.md`: diagnose the article and recommend suitable child
   skills.
5. Rank up to three child skill and internal paradigm pairings. Prefer existing
   child skills when their cover generation engine and a specific internal
   paradigm fit the article.
6. Present a skill recommendation packet: child skill and selected internal
   paradigm first, then reason, proposed design scheme, proposed copy, and risk.
7. Ask Yang to approve one child skill, one internal paradigm, and final cover
   copy.
8. Build an execution design packet with the approved child skill and internal
   paradigm.
9. Write the final GPT Image 2 prompt.
10. Run prompt firewall checks.
11. Run generation preflight. If identity reference is required but cannot be
    explicitly passed into the available image-generation backend, stop and
    deliver the final prompt as prompt-only.
12. Generate the image through Codex's native GPT Image 2 path only after
    preflight passes.
13. Register the generated output in the private project.
14. Verify image dimensions and obvious identity drift.
15. Mark the output final only after exact dimension verification and identity
    review pass.
16. After publishing, record metrics with `scripts/manage_cover_project.py update-metrics`.

## Mandatory Gate Rules
- Do not hand-write a final prompt directly from the article or from a chat
  summary. The final prompt must follow the approved child skill, selected
  internal paradigm, and execution packet.
- Do not call image generation before the prompt firewall passes.
- Do not claim identity preservation when the runtime cannot prove that the
  private identity reference image was passed as an explicit image input.
- Do not treat a generated image as final until it is registered, exact
  dimension-checked, and reviewed for identity drift.
- Do not use low-fidelity previews as the default approval gate. They are
  optional comparison aids only when Yang asks for them.

## Skill Recommendation Packet
Each recommendation card must include:

- Recommended child skill
- Selected internal paradigm
- Fit score
- Target canvas and preset
- Why this child skill is recommended for the article
- Why this internal paradigm fits
- Rejected internal paradigms
- Hook angle
- Proposed cover copy
- Visual premise
- Character pose / expression
- Background or proof object
- Text hierarchy
- Why it may improve open rate
- Risk or possible misread

The skill-selection gate is reasoning-first, not mockup-first. Yang approves the
recommended child skill and internal paradigm from the router's article
diagnosis, fit reason, design scheme, and risk. Low-fidelity mock images are not
required and should not be used as the default approval gate.

Final prompts and any user-requested visual comparison prompts must include the
platform, aspect ratio, target canvas, and safe-area rules explicitly:

- `WeChat public account article main cover`
- `2.35:1`
- `target canvas 2350x1000 pixels`
- central square-safe zone `x=675..1675`

Optional visual comparisons, when explicitly requested, should be saved under:

```text
outputs/direction-references/
```

They are not the default gate and are not final covers.

After generation, optional preview images should be checked with
`scripts/verify_image_dimensions.py --preset wechat-article-main --ratio-only`.
Exact canvas failures are acceptable for optional previews only if recorded;
final accepted covers must pass exact target canvas verification.

## Internal Design Engines

PigeonYang WeChat covers should not bypass the distilled child skills. Use child
skills as internal visual engines, then translate the chosen engine into original
PigeonYang-branded design rules.

Routing is recorded in `engine-routing.md`. This file is the bridge between the
user's draft and the child-skill library.

Suggested routing:

- `pigeonyang-cover-style-dan-koe`: thesis/warning/identity-reframe article.
- `pigeonyang-cover-style-he-tongxue`: AI tool, workflow, prototype, proof object.
- `pigeonyang-cover-style-yingshijufeng`: documentary proof, hidden mechanism, real scene.
- `pigeonyang-cover-style-mrbeast`: high-stakes physicalized premise, output scale, challenge.

Creator names are allowed in internal project notes but forbidden in generated
image prompts. Final prompts must pass the prompt firewall.

## Approval Gates
- Copy Approval Gate: final on-cover text requires Yang's approval.
- Skill Approval Gate: final prompt generation only happens after Yang sees the
  skill recommendation packet and approves one child skill plus one internal
  paradigm.
- Identity Gate: final prompt must require the fixed PigeonYang character identity.
- Style Gate: final prompt must keep anime / refined illustration style and forbid photorealistic person replacement.
- Privacy Gate: project artifacts must not be written inside the product repo.
- Generation Preflight Gate: final image generation only happens when prompt
  firewall, identity-reference capability, approved child skill, selected
  internal paradigm, and execution packet gates pass.
- Finalization Gate: final status only happens after generated output
  registration and exact target canvas verification.

## Private Project Structure
Use this structure for each real production task:

```text
cover-projects/
  YYYYMMDD-slug/
    brief.json
    source.md
    engine-routing.md
    directions.md
    direction-reference-prompts.md
    approved-direction.md
    execution-packet.md
    prompt-final.txt
    outputs/
      direction-references/
      cover-v001.png
    metrics.json
    review.md
```

The script must refuse writes outside `J:\PigeonYang\cover-style-distiller\cover-projects`
or inside `J:\PigeonYang\cover-style-distiller\product`.

## Script Commands

Create a project:

```powershell
python scripts\manage_cover_project.py create --title "<title>" --cover-mode wechat-article-main
```

Validate a path:

```powershell
python scripts\manage_cover_project.py validate-path --project-path J:\PigeonYang\cover-style-distiller\cover-projects\<project-id>
```

Save an artifact:

```powershell
python scripts\manage_cover_project.py save-artifact --project-path <project-path> --artifact directions --from-file <directions-file>
```

Approve one child skill recommendation, internal paradigm, and exact cover copy:

```powershell
python scripts\manage_cover_project.py set-approved --project-path <project-path> --direction-id direction-2 --approved-copy "<copy>"
```

Update metrics:

```powershell
python scripts\manage_cover_project.py update-metrics --project-path <project-path> --open-rate 0.18 --reads 1000
```

Phase 3 workflow gates:

```powershell
python scripts\coverctl.py get-state --project-path <project-path> --json
python scripts\coverctl.py save-engine-routing --project-path <project-path> --from-file engine-routing.md --json
python scripts\coverctl.py save-skill-recommendations --project-path <project-path> --from-file directions.md --json
python scripts\coverctl.py set-approved --project-path <project-path> --direction-id direction-1 --approved-copy "<copy>" --json
python scripts\coverctl.py save-execution-packet --project-path <project-path> --from-file execution-packet.md --json
python scripts\coverctl.py save-final-prompt --project-path <project-path> --from-file prompt-final.txt --json
python scripts\coverctl.py verify-prompt-firewall --project-path <project-path> --forbid "He Tongxue" --json
python scripts\coverctl.py preflight-generation --project-path <project-path> --generation-backend codex-image-gen --reference-image-mode explicit --json
python scripts\coverctl.py record-generation-output --project-path <project-path> --source-image <generated-image> --generation-backend codex-image-gen --reference-image-mode explicit --json
python scripts\coverctl.py verify-image-dimensions --project-path <project-path> --image outputs\cover-v001.png --json
python scripts\coverctl.py mark-final --project-path <project-path> --json
```

## Metrics Schema
`metrics.json` should allow manual updates after publishing:

```json
{
  "platform": "wechat",
  "published_at": null,
  "article_url": null,
  "selected_output": null,
  "open_rate": null,
  "reads": null,
  "shares": null,
  "subjective_score": null,
  "notes": null
}
```

## Error Handling
- If no identity reference exists, stop before generation and ask Yang to provide or register one.
- If copy is not approved, do not write the final prompt.
- If an approved child skill or internal paradigm is missing, do not write the
  execution packet.
- If the execution packet is missing, do not write or use a final prompt.
- If the runtime cannot explicitly pass a required identity reference image,
  output the final prompt and state the missing condition instead of generating a
  final cover.
- If generated dimensions are wrong, do not mark the project complete.
- If the character identity drifts, mark output as rejected and propose a correction prompt.
