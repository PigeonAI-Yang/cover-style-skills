# SPEC: Installable MCP Package

## Purpose
Package the PigeonYang cover workflow gate as a local MCP stdio server that can
be installed once and configured in MCP-capable CLIs.

## Package
- Distribution name: `pigeonyang-cover-mcp`
- Console command: `pigeonyang-cover-mcp`
- Runtime: Python 3.11+
- Transport: MCP stdio JSON-RPC
- Core gate: `scripts/coverctl.py`
- Project operations: `scripts/manage_cover_project.py`

## Product Root
The installed command is stable, but the product repo remains the source of
skill docs, templates, scripts, and private project policy.

Resolve product root in this order:

1. `--product-root <path>`
2. `PIGEONYANG_COVER_PRODUCT_ROOT`
3. Source checkout auto-detection

The command must fail before MCP initialization if the product root, source MCP
server, or `coverctl.py` cannot be found.

## Install
From `J:\PigeonYang\cover-style-distiller\product`:

```powershell
pipx install .
```

or:

```powershell
uv tool install .
```

Development mode:

```powershell
python -m pip install -e .
```

## Client Configuration

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

## Required Tools
The installed MCP command must expose:

- `create_cover_project`
- `get_project_state`
- `save_engine_routing`
- `save_skill_recommendations`
- `set_approved_direction`
- `save_execution_packet`
- `save_final_prompt`
- `verify_prompt_firewall`
- `preflight_generation`
- `record_generation_output`
- `verify_image_dimensions`
- `mark_final`

## Acceptance
- `pigeonyang-cover-mcp --product-root <product> --print-config` prints resolved
  paths and exits zero.
- MCP `tools/list` returns the workflow-gate tools.
- An installed editable package can start the same MCP server as the source
  `mcp-server/cover_project_server.py`.
- Product workflow gates remain in `coverctl.py`; the package entrypoint must not
  duplicate creative logic.
