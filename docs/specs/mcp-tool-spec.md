# SPEC: Local MCP Workflow Engine

## Purpose
The MCP should make the cover workflow stable. It should not replace Agent design judgment.

Prototype implementation:

- `mcp-server/cover_project_server.py`
- `mcp-server/README.md`

The prototype wraps `scripts/manage_cover_project.py` and uses dependency-free
JSON-RPC stdio for local validation. Treat it as an implementation scaffold, not
as a replacement for Codex's creative/runtime image path.

## Responsibility Split
Skill responsibilities:
- Interpret article meaning.
- Choose cover hooks.
- Design three cover directions.
- Write execution packets and final prompts.
- Judge creative fit and iteration direction.

MCP responsibilities:
- Create private project folders.
- Save and read project artifacts.
- Resolve platform cover specs.
- Run deterministic validation.
- Record outputs and metrics.
- Prevent accidental writes to the product repo.

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
Writes `directions.md` containing the three candidate cover directions.

Implementation: `scripts/manage_cover_project.py save-artifact --artifact directions`.

### `save_approved_direction`
Writes the selected direction and approved copy.

Implementation: `scripts/manage_cover_project.py set-approved`.

### `save_execution_packet`
Writes `execution-packet.md`.

Implementation: `scripts/manage_cover_project.py save-artifact --artifact execution-packet`.

### `save_final_prompt`
Writes `prompt-final.txt`.

Implementation: `scripts/manage_cover_project.py save-artifact --artifact prompt-final`.

### `verify_prompt_firewall`
Checks for forbidden creator names, missing identity requirements, unsupported photorealistic drift, and missing platform canvas.

### `resolve_platform_canvas`
Returns platform dimensions, ratio, and safe-area guidance. First required platform: WeChat public account cover.

Implementation: `mcp-server/cover_project_server.py` static resolver.

### `record_generation_output`
Copies or registers the generated image under `outputs/`.

### `verify_image_dimensions`
Checks output dimensions and aspect ratio.

### `update_metrics`
Updates `metrics.json` after publishing.

Implementation: `scripts/manage_cover_project.py update-metrics`.

## Non-Goals
- MCP does not call GPT Image 2 in MVP.
- MCP does not publish to WeChat.
- MCP does not decide creative direction.

## Safety Rules
- Refuse project paths inside the product repo.
- Refuse writes outside the configured private project root unless explicitly allowed.
- Use JSON schemas for machine-written files.
- Keep every write idempotent or versioned.
