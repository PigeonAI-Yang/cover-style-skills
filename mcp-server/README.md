# PigeonYang Cover Project MCP Prototype

This prototype exposes deterministic cover-project operations as local MCP-style
tools. It deliberately does not call GPT Image 2 and does not choose creative
directions. The Agent remains responsible for cover reasoning, directions,
execution packets, and final prompt writing.

## Server

```powershell
python mcp-server\cover_project_server.py
```

The server is a dependency-free JSON-RPC stdio prototype for local validation.
It wraps `scripts/manage_cover_project.py`.

## Tools

- `create_cover_project`: create a private project under
  `J:\PigeonYang\cover-style-distiller\cover-projects`.
- `save_artifact`: save `directions.md`, `execution-packet.md`,
  `prompt-final.txt`, or another known project artifact.
- `set_approved_direction`: record the approved direction and exact cover copy.
- `update_metrics`: update `metrics.json` after publishing.
- `validate_project_path`: prove a project path is inside the private root and
  outside the product repo.
- `resolve_platform_canvas`: return the supported WeChat cover canvas presets.

## Boundary

Private production artifacts stay outside this product repo. The MCP layer is
only a stable filesystem and validation boundary; it is not a creative engine.
