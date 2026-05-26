# Design Standard Template

Every distilled creator must have:

```text
distillation\research.md
distillation\design-standard.md
```

`research.md` stores evidence, source notes, sample tables, and reasoning.

`design-standard.md` is the stable reusable contract embedded into the generated child skill. It should be concise, operational, and suitable for prompt generation.

## Required Structure

```markdown
# PigeonYang Cover Design Standard: <Creator>

## Scope
<What this standard applies to and does not apply to.>

## Evidence Summary
- Cover samples:
- Process sources:
- Research run:
- Confidence:

## Core Design DNA
1. <Rule>
2. <Rule>

## Cover Generation Engine
- Engine type:
- Viewer decision compressed:
- Topic-to-cover mechanism:
- Subject role:
- Pre-visual decision:
- Drift risk:

## Topic Translation Rules
- Abstract topics:
- Concrete topics:
- Required translation variables:
- Forbidden translation moves:
- Example translation:

## Cover Storyboard Rules
- Story moment:
- Visible conflict:
- Subject task/action:
- Proof object:
- Viewer question:
- Forbidden static compositions:
- Example storyboard:

## Design Layout Brief Rules
- First read:
- Second read:
- Third read:
- Layout zones:
- Visual weight:
- Reading path:
- Negative space:
- Forbidden layouts:

## Copy Hierarchy Rules
- Main title:
- Subtitle:
- State labels:
- Object/zone binding:
- Isolation rules:
- Forbidden adjacency:
- Removal rule:

## Platform Adaptation
| Platform/mode | Ratio | Composition rule |
|---|---:|---|

## Layout Patterns
### Pattern 1: <name>
- Use when:
- Composition:
- Text:
- Avoid:

## Subject Rules
## Reference Image Handling
## Identity And Final Prompt Firewall
## Text Rules
## Typography Layout System
## Color And Lighting Rules
## Hook Mechanics
## GPT Image 2 Prompt Contract
## Negative Constraints
## User Intake Questions
## Quality Checklist
```

## Rules

- Keep the standard independent from raw images. Link to source paths and URLs only when useful.
- Do not include the full sample table unless it is tiny; keep detailed evidence in `research.md`.
- Include platform adaptation rules, especially if a wide creator format must be adapted to Bilibili, Douyin, Xiaohongshu, or vertical short video formats.
- Use imperative, prompt-ready language.
- Child skills should embed this design standard, not the full research artifact, unless the user asks for audit details.
- Include a `Cover Generation Engine` section. It must classify the creator's actual engine from evidence instead of assuming every creator uses a stakes/challenge model.
- Include a `Topic Translation Rules` section. It must define how user topics are transformed before visual composition. For MrBeast-like creators, abstract topics usually become physical stakes, giant machines, extreme outcomes, rewards, loss, or challenge scenes. For other creators, the translation may be authority, transformation, aesthetic identity, suspense, or utility clarity.
- Include a `Cover Storyboard Rules` section. It must force title-to-one-frame-story work before prompt writing: visible conflict, subject action, proof object, viewer question, and forbidden static compositions.
- Include a `Design Layout Brief Rules` section. It must force flat-design planning before prompt writing: information hierarchy, layout zones, reading path, visual weight, negative space, and forbidden layouts.
- Include a `Copy Hierarchy Rules` section. It must define main title, subtitle, labels, object binding, isolation, forbidden adjacency, and removal rules. It must prevent accidental phrases caused by nearby text blocks.
- Include a `Reference Image Handling` section. It must distinguish identity traits from pose/action. Reference images should lock identity, clothing, face traits, product appearance, or brand assets, but should not lock the pose unless the user explicitly asks.
- Include an `Identity And Final Prompt Firewall` section. It must state that user-provided portrait identity outranks creator-style transfer, and that final GPT Image 2 prompts must not contain the distilled creator's name, "inspired by", "in the style of", or similar creator-name shortcuts.
- Include a `Typography Layout System` section. It must define protected text zones, hierarchy, backing shapes/badges, background isolation, platform-safe placement, and what to do when the background is cluttered.

