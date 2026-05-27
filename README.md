# Creator Cover Paradigm Distiller

Creator Cover Paradigm Distiller turns real creator cover practice into reusable
cover design engines.

The product has three layers:

1. Distillation: research a creator's real covers and process sources, then
   produce a stable `design-standard.md` and child skill.
2. Router: diagnose a user's article or video and choose the best distilled
   creator-cover engine for the hook.
3. Production: turn the chosen engine into a concrete cover prompt and generated
   output, with filesystem, prompt, reference-image, and dimension gates.

PigeonYang WeChat article covers are the first application of the system, not
the product center. MCP and `coverctl.py` are infrastructure gates, not the
creative engine.

## Repository Boundaries

- `product/`: Git repo for reusable product code, skills, standards, templates,
  specs, and tests.
- `../research-runs/`: managed research runs, raw covers, source captures, and
  full research notes. This stays outside Git.
- `../cover-projects/`: private production projects and generated cover outputs.
  This stays outside Git.
- `../_archive/`: historical backups.

## Core Assets

- `child-skills/`: reusable creator-cover design engines.
- `design-standards/`: canonical distilled design standards kept in Git.
- `references/`: research, prompt, platform, and workspace rules.
- `scripts/create_child_skill.py`: creates a child skill from a design standard.
- `scripts/manage_research_workspace.py`: manages raw research runs outside Git.
- `scripts/capture_bilibili_space.py`: captures a creator's rendered Bilibili
  upload page through the local Chrome CDP proxy and archives video cards,
  source JSON, covers, and contact sheets into a managed research run.
- `scripts/coverctl.py`: deterministic production workflow gate.

## Bilibili CDP Capture

Use this when direct Bilibili APIs are blocked or rate-limited. First make sure
`web-access` CDP is ready, then run from `product/`:

```powershell
python scripts\capture_bilibili_space.py `
  --creator-id he-tongxue `
  --creator-name "何同学" `
  --mid 163637592 `
  --order most-played
```

Useful bounded capture for verification:

```powershell
python scripts\capture_bilibili_space.py `
  --creator-id he-tongxue `
  --creator-name "何同学" `
  --mid 163637592 `
  --order most-played `
  --max-pages 1 `
  --max-videos 5 `
  --no-download-covers
```

## Health Check

Run from `product/`:

```powershell
python scripts\healthcheck.py
```

Use JSON output for automation:

```powershell
python scripts\healthcheck.py --json
```
