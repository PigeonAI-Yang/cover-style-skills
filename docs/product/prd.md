# PRD: PigeonYang Agent-Native Cover System

## Problem
Yang needs a repeatable way to turn article ideas into high-open-rate WeChat covers. Current cover generation through ad hoc prompts is not stable enough: strategy, copy, identity, platform sizing, and output records can drift between runs.

## Product Promise
Given an article title, summary, draft, or full Markdown article, the system helps Codex produce three differentiated WeChat cover directions, get Yang's copy and direction approval, generate a GPT Image 2-ready prompt, create the cover, verify the output, and save a private project record for later open-rate review.

## Primary User
Yang, working inside Codex.

## MVP Scope
- WeChat public account cover first.
- Input can be title-only, title plus summary, or full article Markdown.
- System proposes three cover directions with different hooks, copy, and visual strategies.
- Yang approves one direction and final cover copy before generation.
- Generated covers must preserve the fixed PigeonYang character identity.
- Project records are saved outside the product repo.
- Metrics are manually recorded after publishing.

## Non-Goals
- No standalone SaaS or web UI in MVP.
- No external customer workflow in MVP.
- No direct MCP image generation wrapper in MVP.
- No automatic publishing to WeChat in MVP.
- No fully automatic one-shot generation without approval gates.

## Success Criteria
- Yang can produce a usable WeChat cover from an article draft inside Codex.
- The first response gives useful strategic choices, not only image prompts.
- Final cover feels like PigeonYang: refined anime identity, knowledge-media click clarity, and medium brand consistency.
- Each project stores enough context to reconstruct decisions later.
- Published articles can be manually annotated with open-rate metrics.

## Private Project Location
Private cover projects live under:

```text
J:\PigeonYang\cover-style-distiller\cover-projects
```

This directory is outside the product git repo and must remain private.

## Default Identity Reference
The default identity reference should be stored privately as:

```text
J:\PigeonYang\cover-style-distiller\cover-projects\_identity\pigeonyang-character-reference.png
```

The identity must preserve: silver-gray short hair, glasses, black suit, calm confident intellectual expression, refined all-black styling, and anime character-design-sheet continuity.
