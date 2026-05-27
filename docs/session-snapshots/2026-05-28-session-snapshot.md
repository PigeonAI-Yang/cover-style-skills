# Session Snapshot: 2026-05-28

## Current Product Position
- Product name/position: Creator Cover Paradigm Distiller.
- Repo root: `J:\PigeonYang\cover-style-distiller\product`.
- Workspace root: `J:\PigeonYang\cover-style-distiller`.
- Canonical Git remote: `https://github.com/PigeonAI-Yang/cover-style-skills.git`.
- `product` remains the code repo. Raw research and production artifacts stay
  outside Git.

## Repository Boundaries
- `product/`: reusable product code, design standards, child skills, scripts,
  docs, templates, tests, and MCP server.
- `research-runs/`: managed creator research runs, raw covers, source captures,
  contact sheets, and research notes. Not tracked by Git.
- `cover-projects/`: private cover production projects and generated outputs.
  Not tracked by Git.

## Git State At Snapshot
- Local branch at snapshot creation: `main`.
- `main`, `origin/main`, and `origin/codex/phase-2-feedback-loop` were aligned
  at `24299e5 Add Bilibili CDP capture script` before this snapshot commit.
- Remote `main` was intentionally force-updated from local product history per
  user instruction: local is source of truth.
- Working tree was clean before creating this snapshot.

## Completed Work
- Reframed the product away from a PigeonYang-only workflow and toward a reusable
  creator-cover paradigm distiller.
- Moved raw research discipline outside the repo through managed
  `research-runs`.
- Added internal `Popular Paradigms` as a required design-standard structure.
- Added MCP package support:
  - installable command: `pigeonyang-cover-mcp`
  - source server: `mcp-server/cover_project_server.py`
  - deterministic gates through `scripts/coverctl.py`
- Added healthcheck:
  - reports child skills
  - research runs
  - MCP status
  - cover project status
  - Git dirty files
- Added Bilibili CDP capture script:
  - `scripts/capture_bilibili_space.py`
  - captures rendered Bilibili creator upload pages through web-access Chrome
    CDP
  - supports `latest`, `most-played`, and `most-faved`
  - writes managed research source JSON
  - downloads and registers covers
  - generates contact sheets when Pillow is available

## He Tongxue Distillation Result
- Status: usable distilled version complete.
- Child skill: `child-skills/pigeonyang-cover-style-he-tongxue`.
- Child skill version: `0.7.0`.
- Canonical standard:
  `design-standards/he-tongxue/design-standard.md`.
- Current full research run:
  `J:\PigeonYang\cover-style-distiller\research-runs\he-tongxue\20260527-bilibili-cdp-current-all-videos`.
- Sample source: Bilibili rendered upload page via Chrome CDP.
- Sample count: 93 public video cards, ordered by Bilibili `最多播放`.
- Contact sheet:
  `distillation/sample-contact-sheet.jpg`.
- Core engine: `Evidence-First Curiosity Engine`.

## He Tongxue Popular Paradigms
1. `Macro / Screen Proof State` - close proof detail, screen state, UI, number,
   or document.
2. `Prototype / Built Object Hero` - a real built object, prototype, rig, or
   interface artifact proves the story.
3. `Product Curiosity / Tech Object Reveal` - dominant class; product object
   plus price, flaw, history, form factor, or future signal.
4. `Measured / Scale Test` - count, distance, price range, participant scale,
   result surface, or visible comparison.
5. `Absurd Utility Action` - ordinary problem solved by a strange real action or
   overbuilt object.
6. `Craft / Visual Spectacle` - material, camera, performance, animation, or
   visual experiment as inspectable proof.
7. `Personal / Process Documentary` - personal or process claim grounded in a
   concrete scene, artifact, room, workspace, letter, interview, or milestone.

## Operational Rule For He Tongxue Skill
- Do not treat every topic as a product/build cover.
- First choose one internal paradigm.
- If the topic has no real proof unit, process scene, product, interface,
  experiment, artifact, or personal object, route away from this child skill.
- Final image prompts must not name or imitate the public creator.

## MCP Status
- `python scripts\healthcheck.py` reports `MCP: OK`.
- MCP is currently a workflow/state/filesystem gate, not a creative engine.
- MCP tools cover project creation, state computation, routing artifact saves,
  approval recording, execution packet save, final prompt save, prompt firewall,
  generation preflight, generation output registration, dimension checks, final
  marking, metrics, and project path validation.

## Current Healthcheck Notes
- Child skills OK:
  - `pigeonyang-cover-style-dan-koe` `0.5.0`
  - `pigeonyang-cover-style-he-tongxue` `0.7.0`
  - `pigeonyang-cover-style-mrbeast` `0.5.0`
  - `pigeonyang-cover-style-yingshijufeng` `0.5.0`
- Design standards OK:
  - `dan-koe`
  - `he-tongxue`
  - `mrbeast`
  - `yingshijufeng`
- Legacy `product/research` does not exist.
- Known non-blocking historical issue: two old `cover-projects` entries have
  incomplete routing/recommendation artifacts under the newer gate rules.

## Recommended Next Moves
- Switch daily work to `main` now that remote `main` has been overwritten with
  the local product history.
- Add a small doc for how to install and register the MCP server in the user's
  actual client.
- Decide whether the remote repository should keep the old install-oriented
  `skills/` package layout, or whether the new `product` layout is now the only
  source of truth.
- Use `scripts/capture_bilibili_space.py` for future Bilibili creator sample
  expansion instead of hand-written CDP snippets.
