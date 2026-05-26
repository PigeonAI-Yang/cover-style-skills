# PLAN: Phase 1

## Goal
Turn the existing cover-style distiller into a Codex-native product for Yang's WeChat article covers.

## Phase 1 Deliverable
From a title, summary, or article draft, Codex can produce three differentiated WeChat cover directions, wait for Yang's approval, generate a final GPT Image 2 prompt, save the private project record, and leave room for post-publish metrics.

## Work Sequence
1. Stabilize repository structure and documentation.
2. Add private project protocol and templates.
3. Extend platform standards for WeChat public account covers.
4. Add a WeChat cover workflow section to the mother skill.
5. Add identity reference handling rules.
6. Add deterministic scripts for project creation and metrics updates.
7. Later: wrap deterministic scripts as a local MCP.

## Acceptance
- Product repo remains under `product`.
- Private projects remain under sibling `cover-projects`.
- Active skill entrypoints are junctions to `product` or `product\child-skills`.
- Skill validation passes.
- A dry-run WeChat cover project can be created without writing private data to git.
