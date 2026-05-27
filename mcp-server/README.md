# PigeonYang Cover Project MCP Prototype

This prototype exposes deterministic cover-project operations as local MCP-style
tools. It deliberately does not call GPT Image 2 and does not choose creative
directions. The Agent remains responsible for cover reasoning, but the MCP layer
now gates workflow state transitions through `scripts/coverctl.py`.

## Installable Server

From the product repo:

```powershell
pipx install .
```

or:

```powershell
uv tool install .
```

Run the installed MCP stdio server:

```powershell
pigeonyang-cover-mcp --product-root J:\PigeonYang\cover-style-distiller\product
```

Smoke check:

```powershell
pigeonyang-cover-mcp --product-root J:\PigeonYang\cover-style-distiller\product --print-config
```

## Client Config

Use the same command shape for Claude Code, Codex CLI, Cursor, or any local MCP
client that accepts stdio servers:

```json
{
  "mcpServers": {
    "pigeonyang-cover": {
      "command": "pigeonyang-cover-mcp",
      "args": [
        "--product-root",
        "J:\\PigeonYang\\cover-style-distiller\\product"
      ]
    }
  }
}
```

If a client supports environment variables but not args, set:

```powershell
$env:PIGEONYANG_COVER_PRODUCT_ROOT = "J:\PigeonYang\cover-style-distiller\product"
```

and configure:

```json
{
  "mcpServers": {
    "pigeonyang-cover": {
      "command": "pigeonyang-cover-mcp",
      "args": []
    }
  }
}
```

## Source Server

```powershell
python mcp-server\cover_project_server.py
```

The source server remains available for development. The installable command is
the preferred integration path for MCP clients.

## Tools

- `create_cover_project`: create a private project under
  `J:\PigeonYang\cover-style-distiller\cover-projects`.
- `get_project_state`: compute the current workflow state from files.
- `save_engine_routing`: save validated `engine-routing.md`.
- `save_skill_recommendations`: save validated child-skill recommendation cards.
- `set_approved_direction`: record the approved child skill and exact cover copy.
- `save_execution_packet`: save a validated execution design packet.
- `save_final_prompt`: save a validated final prompt.
- `verify_prompt_firewall`: persist `firewall-result.json`.
- `preflight_generation`: decide whether final generation is allowed or
  prompt-only blocked.
- `record_generation_output`: copy generated images into `outputs/` and persist
  `generation-manifest.json`.
- `verify_image_dimensions`: persist `dimension-check.json`.
- `mark_final`: mark a registered output final after exact dimension pass.
- `save_artifact`: save legacy non-gated artifacts such as `source.md` and
  `review.md`; gated artifacts are redirected through `coverctl`.
- `update_metrics`: update `metrics.json` after publishing.
- `validate_project_path`: prove a project path is inside the private root and
  outside the product repo.
- `resolve_platform_canvas`: return the supported WeChat cover canvas presets.

## Boundary

Private production artifacts stay outside this product repo. The MCP layer is a
filesystem, validation, and workflow-state boundary; it is not a creative engine
and it does not replace the child skills.
