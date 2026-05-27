# SPEC: Distilled Skill Router

## Purpose
Route a user's draft to the most suitable distilled creator-cover skills before
cover generation.

This is the core product layer. The router should recommend a specific
distilled blogger/creator child skill before proposing visual execution. It must
not produce a generic cover direction when an existing child skill provides a
stronger visual decision engine. The router's user-facing output is a
child-skill recommendation packet: each card starts with the recommended child
skill, then explains why that skill fits and what design scheme it would use.

## Inputs
- Article title
- Summary or full draft
- Publishing platform and canvas
- Required identity reference
- Optional user constraints

## Engine Inventory
Each child skill is treated as an internal design engine with:

- engine name
- best-fit article types
- hook families
- topic translation rules
- storyboard rules
- layout rules
- copy hierarchy rules
- drift risks
- final-prompt firewall terms

## Routing Questions
For every draft, answer:

- What is the article's main reader pain or desire?
- Is the hook a thesis, warning, proof object, hidden mechanism, transformation,
  visible stakes, identity reframe, or aesthetic mood?
- Does the article need authority, maker proof, documentary evidence, spectacle,
  or utility clarity?
- Which child skill would make the article legible in one second?
- Which child skill would distort the article?

## Current Engine Routing Guide
- `pigeonyang-cover-style-dan-koe`: thesis, warning, identity reframe, creator
  psychology, belief correction, high-authority text+face covers.
- `pigeonyang-cover-style-he-tongxue`: AI tools, workflows, prototypes,
  inventions, proof objects, maker-demonstrator covers.
- `pigeonyang-cover-style-yingshijufeng`: hidden mechanisms, documentary proof,
  real scenes, serious tech/social investigation, credible evidence.
- `pigeonyang-cover-style-mrbeast`: extreme stakes, physicalized outcomes,
  visible scale, challenges, absurd proof, high contrast result gaps.

## Output
Create `engine-routing.md` as an internal routing record in the private project:

```markdown
# Engine Routing

## Article Diagnosis

## Candidate Engines

### Candidate 1
- Child skill:
- Fit score:
- Why it fits:
- What visual promise it creates:
- Risk:
- Recommendation reason:
- Proposed design scheme:

### Candidate 2
...

### Candidate 3
...

## Rejected Engines

## Recommendation
```

Then create `directions.md` as the user-facing skill recommendation packet. The
file name stays `directions.md` for current script compatibility, but the content
must be skill-first:

```markdown
# Skill Recommendation Packet

## Recommendation 1
- Recommended child skill:
- Fit score:
- Why this skill is recommended:
- Proposed on-cover copy:
- Main visual promise:
- Proposed design scheme:
- Risk or possible misread:
- Platform/canvas:

## Recommendation 2
...

## Recommendation 3
...
```

## Rules
- Recommend 3 engines when possible.
- Present child skill plus design scheme plus reason together.
- The approval object is the child skill, not an abstract direction label.
- Do not require low-fidelity mock images for skill approval; poor mock images
  can degrade judgment. Generate images only after one child skill is approved,
  unless the user explicitly asks for visual comparisons.
- Public creator names may appear in internal routing notes, but generated image
  prompts must translate the engine into concrete design rules.
- Final prompts must pass `scripts/verify_prompt_firewall.py`.
- If no current child skill fits, say so and propose a new distillation target
  instead of forcing a bad engine.
- Every final or user-requested preview prompt must explicitly include
  `WeChat public account article main cover`, `2.35:1`,
  `target canvas 2350x1000 pixels`, and central square-safe zone `x=675..1675`.
