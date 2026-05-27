# PRD: Creator Cover Paradigm Distiller

## Problem

Users do not need another generic "make me a good cover" prompt. They need a
repeatable way to extract cover decision systems from excellent creators, then
apply the right system to their own article or video without copying a public
creator's identity, assets, or exact layouts.

The project drifted toward a PigeonYang WeChat cover workflow because that was
the first real application. That workflow is valuable, but it is not the product
center.

## Product Promise

Given a creator, the system distills that creator's high-performing cover
paradigms into a reusable child skill backed by real cover samples and process
sources.

Given a user's article or video, the system diagnoses the hook, routes it to the
most suitable distilled child skill and internal paradigm, explains the design
scheme that pairing would use, gets exact copy approval when needed, then
produces a GPT Image 2-ready cover prompt and generated output through
deterministic workflow gates.

## Product Layers

1. Distillation: collect evidence, write `research.md`, produce canonical
   `design-standard.md`, and generate a child skill.
2. Router: choose the best creator-cover engine and internal paradigm for a
   user's article or video.
3. Production: save project records, run prompt firewall checks, prove reference
   image handling, register generated outputs, and verify dimensions.

## Primary User

Yang inside Codex. The architecture should still be general enough to support
other users, platforms, and creators later.

## MVP Scope

- Maintain a small library of distilled child skills.
- Keep canonical `design-standard.md` files in Git.
- Keep raw research runs outside Git.
- Route article/video inputs to up to three suitable child skill and internal
  paradigm pairings.
- Produce a skill-first recommendation packet.
- Require exact on-cover copy approval before final prompt writing when copy is
  proposed or rewritten.
- Use `coverctl.py` or MCP tools for deterministic production gates.
- Treat PigeonYang WeChat article covers as the first application workflow.

## Non-Goals

- No standalone SaaS or web UI in MVP.
- No automatic publishing.
- No one-shot generation that bypasses routing and approval.
- No direct MCP image-generation wrapper until a reference-capable backend is
  explicitly implemented.
- No raw research archives inside the product repo.

## Success Criteria

- A new creator can be researched and converted into a child skill from a
  managed research run.
- A user draft can be routed to a child skill and internal paradigm with a
  concrete reason, visual premise, copy proposal, and risk.
- Final prompts translate creator patterns into concrete design rules without
  creator-name shortcuts.
- The repo contains reusable product assets, not raw research clutter.
- Private production projects stay outside Git.
- The workflow gate can explain exactly why a project is ready, blocked, or
  prompt-only.
