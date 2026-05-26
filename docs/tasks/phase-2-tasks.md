# TASKS: Phase 2

## Task 1: First Real Article Run
Status: prompt ready 2026-05-26

- Use a real title, summary, Markdown draft, or draft path.
- Create a private cover project.
- Produce three differentiated WeChat cover directions.
- Stop for direction and exact copy approval.
- Generate only after prompt firewall passes.

Current project:
`J:\PigeonYang\cover-style-distiller\cover-projects\20260526-ai-flywheel-builder-cover`

Progress: real article source has been saved, three differentiated WeChat cover
directions have been produced, Direction 2 has been approved, exact cover copy is
`这是内容飞轮`, execution packet and final prompt have been written, and prompt
firewall has passed.

## Task 2: Output Verification
Status: iteration needed 2026-05-27

- Verify generated output dimensions with `scripts/verify_image_dimensions.py`.
- Check the PigeonYang anime identity against the private reference.
- Record accepted and rejected outputs under the private project.

Progress: `cover-v001-rejected.png` was generated and copied to the private
project. Ratio verification passed, exact target canvas failed (`1923x818` vs
`2350x1000`). User rejected the cover aesthetics.

Next: generate three visual direction references with explicit target canvas and
safe-area requirements before revising v002. The previous text-only direction
approval is insufficient.

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
workflow so approval requires three visual references with explicit platform,
ratio, target canvas, and safe-area rules.

## Task 6: Phase 2 Retrospective
Status: not ready 2026-05-26

- Summarize what improved open-rate confidence.
- Summarize what slowed production.
- Decide whether Phase 3 should focus on MCP hardening, image QA, or style-library expansion.

Reason: retrospective requires 3-5 real projects or at least one complete
published run.
