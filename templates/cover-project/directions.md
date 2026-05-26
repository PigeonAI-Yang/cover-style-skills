# Cover Directions

Project: `{{PROJECT_ID}}`
Platform: WeChat public account article cover
Target: `{{TARGET_CANVAS}}`
Preset: `{{COVER_MODE}}`

## Direction Preview Rule
Do not ask Yang to choose from text-only directions.

Each direction must have a visual reference image or low-fidelity direction
preview saved under `outputs/direction-references/`. The text below only explains
what the image is trying to test.

Every direction reference prompt must explicitly include:

- `WeChat public account article main cover`
- `2.35:1`
- `target canvas 2350x1000 pixels`
- central square-safe zone `x=675..1675`

After generation, verify each direction reference with
`scripts/verify_image_dimensions.py --preset wechat-article-main --ratio-only`.
If the exact canvas is not `2350x1000`, mark it as a reference only, not a final
cover candidate.

## Direction 1
- Visual reference:
- Target canvas:
- Hook angle:
- Proposed on-cover copy:
- Visual premise:
- PigeonYang character pose / expression:
- Background, object, or proof cue:
- Text hierarchy:
- Why it may improve open rate:
- Risk or possible misread:

## Direction 2
- Visual reference:
- Target canvas:
- Hook angle:
- Proposed on-cover copy:
- Visual premise:
- PigeonYang character pose / expression:
- Background, object, or proof cue:
- Text hierarchy:
- Why it may improve open rate:
- Risk or possible misread:

## Direction 3
- Visual reference:
- Target canvas:
- Hook angle:
- Proposed on-cover copy:
- Visual premise:
- PigeonYang character pose / expression:
- Background, object, or proof cue:
- Text hierarchy:
- Why it may improve open rate:
- Risk or possible misread:

## Approval Gate
Stop here until Yang has seen the three visual references and approves one
direction plus exact on-cover copy.
