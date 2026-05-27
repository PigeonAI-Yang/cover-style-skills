# TASKS: Phase 2

## Task 1: First Real Article Run
Status: reroute required 2026-05-27

- Use a real title, summary, Markdown draft, or draft path.
- Create a private cover project.
- Produce a WeChat child-skill recommendation packet without default low-fidelity previews.
- Stop for direction and exact copy approval.
- Generate only after prompt firewall passes.

Current project:
`J:\PigeonYang\cover-style-distiller\cover-projects\20260526-ai-flywheel-builder-cover`

Progress: real article source has been saved, but the previous direction
approval was based on text-only directions instead of child-skill recommendation
cards and is no longer valid. The old exact
copy `这是内容飞轮` remains useful input, but the workflow must reroute the article
through child-skill recommendation before any v002 final prompt.

## Task 2: Output Verification
Status: iteration needed 2026-05-27

- Verify generated output dimensions with `scripts/verify_image_dimensions.py`.
- Check the PigeonYang anime identity against the private reference.
- Record accepted and rejected outputs under the private project.

Progress: `cover-v001-rejected.png` was generated and copied to the private
project. Ratio verification passed, exact target canvas failed (`1923x818` vs
`2350x1000`). User rejected the cover aesthetics.

Next: generate a skill recommendation packet with explicit target canvas,
safe-area requirements, recommended child skill, design scheme, and risk before
revising v002. The previous text-only direction approval is insufficient.

## Task 3: Metrics Capture
Status: blocked 2026-05-26

- After publishing, update `metrics.json`.
- Record open rate, reads, shares, selected output, subjective score, and notes.
- Keep metrics private.

Blocker: no real cover has been generated or published.

## Task 4: Review Notes
Status: started 2026-05-27

- Fill `review.md` for each real project.
- Separate design taste issues from workflow/tooling friction.
- Identify repeated failure modes.

Progress: review notes for rejected v001 were written in the private project.

## Task 5: Product Patch Batch
Status: started 2026-05-27

- After 3-5 runs, patch only repeated or high-cost friction.
- Prefer mechanical guardrails over prompt-only reminders.
- Update skill docs, schemas, scripts, or MCP tools only when evidence supports it.

Observed friction: text-only direction approval caused a bad visual choice, and
direction prompts did not explicitly carry canvas requirements. Patch direction
workflow so approval requires child-skill recommendation cards with explicit
platform, ratio, target canvas, safe-area rules, and router reasons.

Additional friction: generic PigeonYang product workflow bypassed the distilled
child-skill visual engines. Patch workflow so direction references use child
skills as internal design engines while keeping final prompts firewall-safe.

Product clarification: the target product is a router over a growing library of
distilled excellent-blogger cover skills. Given a user's draft, the system should
recommend suitable specific skills, generate visual schemes from those engines,
and use the selected skill to produce the final image.

## Task 6: Phase 2 Retrospective
Status: not ready 2026-05-26

- Summarize what improved open-rate confidence.
- Summarize what slowed production.
- Decide whether Phase 3 should focus on MCP hardening, image QA, or style-library expansion.

Reason: retrospective requires 3-5 real projects or at least one complete
published run.
