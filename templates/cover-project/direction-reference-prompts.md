# Direction Reference Prompts

Project: `{{PROJECT_ID}}`
Platform: WeChat public account article cover
Target: `{{TARGET_CANVAS}}`
Preset: `{{COVER_MODE}}`

## Purpose
This file is optional. Use it only when Yang explicitly asks for visual
comparisons before approving a child skill, or when a high-quality draft is
needed after child-skill approval.

Low-fidelity mock images are not the default approval gate. If previews are
generated, they should be good enough to clarify the child skill's visual
translation, not crude placeholders that make the choice harder.

## Rules
- Select one recommended child skill for each optional preview.
- Record the internal engine name in `directions.md`, but do not put public
  creator names, `inspired by`, or `in the style of` wording in generated image
  prompts.
- Every prompt must explicitly say: `WeChat public account article main cover,
  2.35:1, target canvas 2350x1000 pixels`.
- Every prompt must include the central square-safe zone: `x=675..1675`.
- Preserve PigeonYang anime identity when a character appears.
- Keep text either exact or use placeholder blocks if text rendering is not the
  evaluation target.
- Make each reference visually different, not just a color variant.
- Save outputs under `outputs/direction-references/`.
- Verify each generated reference with:
  `scripts/verify_image_dimensions.py <image> --preset wechat-article-main --ratio-only`.
- Only final accepted covers require exact `2350x1000`; direction references may
  pass ratio-only, but exact size failures must be recorded.

## Recommendation 1 Preview Prompt
- Recommended child skill:
- Selected internal paradigm:
- Recommendation reason this image should test:

## Recommendation 2 Preview Prompt
- Recommended child skill:
- Selected internal paradigm:
- Recommendation reason this image should test:

## Recommendation 3 Preview Prompt
- Recommended child skill:
- Selected internal paradigm:
- Recommendation reason this image should test:
