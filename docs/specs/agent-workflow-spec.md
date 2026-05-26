# SPEC: Agent Cover Workflow

## Runtime
The workflow runs in Codex. Skills handle reasoning and prompt design. Scripts or MCP tools handle deterministic project operations.

Deterministic project operations are implemented in:

- `scripts/manage_cover_project.py`
- `schemas/cover-project/brief.schema.json`
- `schemas/cover-project/metrics.schema.json`
- `templates/cover-project/`

## Inputs
The Agent accepts any of:

- Article title only
- Title plus summary
- Full article Markdown
- Existing draft file path

When input is weak, the Agent should still produce directions, but must mark assumptions explicitly.

## Workflow
1. Create or select a private cover project under `cover-projects` with `scripts/manage_cover_project.py create`.
2. Save the raw input as project source material.
3. Extract article promise, reader pain, contradiction, stakes, and strongest open-rate hook.
4. Generate three differentiated cover directions.
5. Ask Yang to approve one direction and final cover copy.
6. Build an execution design packet.
7. Write the final GPT Image 2 prompt.
8. Run prompt firewall checks.
9. Generate the image through Codex's native GPT Image 2 path.
10. Verify image dimensions and obvious identity drift.
11. Save output, selected prompt, and generation notes.
12. After publishing, record metrics with `scripts/manage_cover_project.py update-metrics`.

## Direction Packet
Each of the three direction options must include:

- Hook angle
- Proposed cover copy
- Visual premise
- Character pose / expression
- Background or proof object
- Text hierarchy
- Why it may improve open rate
- Risk or possible misread

## Approval Gates
- Copy Approval Gate: final on-cover text requires Yang's approval.
- Direction Approval Gate: generation only happens after Yang chooses one direction.
- Identity Gate: final prompt must require the fixed PigeonYang character identity.
- Style Gate: final prompt must keep anime / refined illustration style and forbid photorealistic person replacement.
- Privacy Gate: project artifacts must not be written inside the product repo.

## Private Project Structure
Use this structure for each real production task:

```text
cover-projects/
  YYYYMMDD-slug/
    brief.json
    source.md
    directions.md
    approved-direction.md
    execution-packet.md
    prompt-final.txt
    outputs/
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

Approve one direction and exact cover copy:

```powershell
python scripts\manage_cover_project.py set-approved --project-path <project-path> --direction-id direction-2 --approved-copy "<copy>"
```

Update metrics:

```powershell
python scripts\manage_cover_project.py update-metrics --project-path <project-path> --open-rate 0.18 --reads 1000
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
- If generated dimensions are wrong, do not mark the project complete.
- If the character identity drifts, mark output as rejected and propose a correction prompt.
