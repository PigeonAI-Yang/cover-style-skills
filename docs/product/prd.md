# PRD: PigeonYang Agent-Native Cover Skill Router

## Problem
Yang needs a repeatable way to turn article ideas into high-open-rate covers by
using the design intelligence already distilled from excellent creators. Current
cover generation through ad hoc prompts or generic "good-looking cover" logic is
not stable enough: it bypasses proven creator-specific visual engines, and the
user cannot judge direction quality from prose alone.

## Product Promise
Given an article title, summary, draft, or full Markdown article, the system
analyzes the article, recommends suitable distilled creator-cover skills as
internal design engines, produces visual direction references from those engines,
lets Yang choose the best direction, then generates a GPT Image 2-ready cover
while preserving PigeonYang identity, platform sizing, and prompt-firewall safety.

## Primary User
Yang, working inside Codex.

## MVP Scope
- WeChat public account cover first.
- Input can be title-only, title plus summary, or full article Markdown.
- System routes the article to 3 suitable internal design engines from the
  distilled child-skill library.
- System explains why each engine fits or does not fit the article.
- System produces three visual direction references, not text-only directions.
- Yang approves one visual direction and final cover copy before final prompt
  writing and generation.
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
- The first response recommends suitable distilled creator skills with concrete
  rationale.
- Direction choice is based on visual references, not prose imagination.
- Final cover feels like PigeonYang: refined anime identity, knowledge-media click clarity, and medium brand consistency.
- Final cover benefits from a specific distilled creator-cover engine without
  naming or copying that creator in the final prompt.
- Each project stores enough context to reconstruct decisions later.
- Published articles can be manually annotated with open-rate metrics.

## Design Engine Library
The product is expected to grow by adding more high-quality creator-cover child
skills. Each child skill is a reusable design engine, not a public style label.
The router should choose engines based on the article's content type, hook,
proof object, emotional promise, platform, and PigeonYang identity constraints.

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
