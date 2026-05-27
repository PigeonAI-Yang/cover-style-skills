# Phase 4 Tasks: Internal Paradigm Cards

## Goal

Upgrade Creator Cover Paradigm Distiller from `one creator = one cover engine`
to `one creator = one child skill with multiple evidence-backed popular
paradigms`.

The product is not trying to fully copy a public creator's style. It is trying
to distill the repeatable cover decisions behind that creator's high-performing
covers, then route a user task to the most suitable internal paradigm without
copying public likeness, logos, or exact thumbnails.

## Architecture Decision

Use this structure:

```text
user article/video
  -> creator child skill
    -> selected internal paradigm card
      -> execution design packet
        -> final prompt
```

Keep one child skill per creator by default. Do not split every creator paradigm
into separate top-level skills unless a paradigm proves useful across creators.

## Required Contract

Each design standard must include `Popular Paradigms`.

Each paradigm card must include:

- evidence count
- representative samples
- best-fit topics
- click promise
- topic translation
- one-frame story
- first read and second read
- text behavior
- composition
- failure mode
- prompt contract

Routing and approval must select both:

- child skill
- internal paradigm

## Todo

- [x] Record the Phase 4 architecture decision.
- [x] Add `Popular Paradigms` to the research framework and research artifact
  template.
- [x] Add `Popular Paradigms` to the canonical design standard template.
- [x] Update the mother skill contract so distillation and prompt execution
  choose an internal paradigm before final prompting.
- [x] Update `scripts/create_child_skill.py` so generated child skills require
  and use `Popular Paradigms`.
- [x] Update router and MCP specs so recommendation cards include
  `Selected internal paradigm`.
- [x] Update `scripts/coverctl.py` to validate selected internal paradigms in
  recommendation, approval, and execution packet gates.
- [x] Update tests for the new gate fields.
- [x] Run pytest, healthcheck, and child skill validation.

## He Tongxue Follow-Up

After the architecture gate is in place, open a new evidence expansion run for
`he-tongxue`. Keep the current `0.4.1` as a baseline guardrail, then add more
high-performing samples and rewrite the standard around multiple popular
paradigm cards instead of one over-broad engine.
