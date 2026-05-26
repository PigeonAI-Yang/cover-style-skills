# SPEC: Distilled Skill Router

## Purpose
Route a user's draft to the most suitable distilled creator-cover skills before
cover generation.

This is the core product layer. The router should not produce a generic cover
direction when an existing child skill provides a stronger visual decision
engine.

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
- What visual engine would make the article legible in one second?
- Which engine would distort the article?

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
Create `engine-routing.md` in the private project:

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
- Direction reference prompt:

### Candidate 2
...

### Candidate 3
...

## Rejected Engines

## Recommendation
```

## Rules
- Recommend 3 engines when possible.
- Use visual direction references for approval; never ask the user to choose
  from text-only routing.
- Public creator names may appear in internal routing notes, but generated image
  prompts must translate the engine into concrete design rules.
- Final prompts must pass `scripts/verify_prompt_firewall.py`.
- If no current child skill fits, say so and propose a new distillation target
  instead of forcing a bad engine.
