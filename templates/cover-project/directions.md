# Skill Recommendation Packet

Project: `{{PROJECT_ID}}`
Platform: WeChat public account article cover
Target: `{{TARGET_CANVAS}}`
Preset: `{{COVER_MODE}}`

## Recommendation Rule
Do not ask Yang to choose from text-only skill recommendations.

Each recommendation must start with the recommended child skill and selected
internal paradigm. The approval decision is based on article diagnosis,
child-skill fit, paradigm fit, design scheme, proposed copy, and risk. Do not
require low-fidelity mock images by default.

Prefer existing child skills. The skill name is project metadata; generated
image prompts must translate it into concrete visual rules and must not contain
public creator names or style-copy wording.

Every final prompt or user-requested visual comparison prompt must explicitly include:

- `WeChat public account article main cover`
- `2.35:1`
- `target canvas 2350x1000 pixels`
- central square-safe zone `x=675..1675`

After generation, verify each final image or user-requested preview with
`scripts/verify_image_dimensions.py --preset wechat-article-main --ratio-only`.
If an optional preview's exact canvas is not `2350x1000`, mark it as a reference
only, not a final cover candidate.

## Recommendation 1
- Recommended child skill:
- Selected internal paradigm:
- Fit score:
- Why this skill is recommended:
- Why this paradigm fits:
- Rejected internal paradigms:
- Target canvas:
- Hook angle:
- Proposed on-cover copy:
- Visual premise:
- PigeonYang character pose / expression:
- Background, object, or proof cue:
- Text hierarchy:
- Why it may improve open rate:
- Risk or possible misread:

## Recommendation 2
- Recommended child skill:
- Selected internal paradigm:
- Fit score:
- Why this skill is recommended:
- Why this paradigm fits:
- Rejected internal paradigms:
- Target canvas:
- Hook angle:
- Proposed on-cover copy:
- Visual premise:
- PigeonYang character pose / expression:
- Background, object, or proof cue:
- Text hierarchy:
- Why it may improve open rate:
- Risk or possible misread:

## Recommendation 3
- Recommended child skill:
- Selected internal paradigm:
- Fit score:
- Why this skill is recommended:
- Why this paradigm fits:
- Rejected internal paradigms:
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
Stop here until Yang has seen the skill recommendation packet and approves one
child skill, one internal paradigm, and exact on-cover copy.
