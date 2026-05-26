# Direction Reference Prompts

Project: `{{PROJECT_ID}}`
Platform: WeChat public account article cover
Target: `{{TARGET_CANVAS}}`
Preset: `{{COVER_MODE}}`

## Purpose
Generate three rough visual direction references before asking for approval.

These are decision images, not final covers. They should test composition,
visual metaphor, title treatment, and overall taste. They do not need to preserve
every final detail, but they must be close enough for Yang to judge which visual
direction is worth developing.

## Rules
- Select one internal child-skill design engine for each direction.
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

## Direction 1 Prompt

## Direction 2 Prompt

## Direction 3 Prompt
