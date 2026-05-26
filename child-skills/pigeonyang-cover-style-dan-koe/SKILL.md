---
name: pigeonyang-cover-style-dan-koe
description: "PigeonYang-branded skill that uses the distilled Dan Koe video cover and thumbnail design pattern to write GPT Image 2-ready prompts for original user covers. Trigger when the user asks for a cover in Dan Koe's style, references Dan Koe thumbnails, or asks to apply this creator cover formula."
---

# PigeonYang Dan Koe Cover Style

## Role

Use this distilled creator-cover pattern to write original, GPT Image 2-ready cover prompts for the user's video.

Do not copy existing Dan Koe thumbnails. Apply the transferable design strategy to the user's own topic, brand, face, product, and constraints.

## Identity And Final Prompt Firewall

The distilled creator name is an internal routing and analysis label only.

Never put `Dan Koe`, `Dan Koe-inspired`, `in the style of Dan Koe`, `like Dan Koe`, or equivalent creator-name shortcuts in the final GPT Image 2 generation prompt. Rewrite the pattern into concrete design rules: subject role, story moment, proof object, composition, typography, color, lighting, and negative constraints.

If the user supplies a portrait/reference image, that reference controls identity. Preserve the user's face, hair, glasses, clothing cues, body type, and other supplied identity traits. Redesign only the pose/action for the thumbnail hook unless the user explicitly asks to preserve the original pose. The final generation prompt must say the subject must not resemble any public creator, without naming Dan Koe.

## Required User Inputs

Ask the publishing platform first, then ask only for missing production fields.

Platform guidance:

| Platform | Recommended cover ratio | Target canvas | Notes |
|---|---:|---:|---|
| YouTube long video | 16:9 | 1280x720 | Best fit for wide comparison, crowd, and spectacle layouts. |
| Bilibili native upload | 1146:717, approx 16:10 | 1146x717 | Use when the cover is Bilibili-only; keep face/text in a 16:9 and 4:3 safe center area. |
| Bilibili cross-platform | 16:9 | 1920x1080 | Use when reusing with YouTube or wide feeds; preserve Bilibili-safe center crop. |
| Bilibili 4:3-safe | 4:3 | 1440x1080 | Use when the user cares about Bilibili card/homepage crop safety. |
| Douyin horizontal video | 4:3 | 1440x1080 | Compress wide logic; avoid critical side-edge text. |
| Douyin vertical video | 3:4 | 1080x1440 | Use portrait cover composition; keep face/text central and avoid edge-critical details. |
| Xiaohongshu | 3:4 | 1080x1440 | Use note/card style portrait composition. |
| Xiaohongshu square | 1:1 | 1080x1080 | Use central subject plus two contrast cues. |
| TikTok / Reels / Shorts | 9:16 | 1080x1920 | Use vertical poster logic; avoid YouTube-style split-screen. |
| WeChat video account | 6:7 or 3:4 | 1080x1260 or 1080x1440 | Ask for account preference if uncertain. |

Missing fields:

- video topic or title
- exact on-cover text, if any
- target platform, orientation, aspect ratio, and target canvas
- user's own portrait/reference image, if identity matters
- whether the reference pose should be preserved; default to redesigning the pose for the thumbnail hook
- must-include elements
- must-avoid elements
- brand or legal constraints

## Prompt Workflow

1. Extract the relevant design rules from the distilled research below.
2. Use the cover generation engine and topic translation rules to convert the user's raw topic into this creator's cover logic before choosing visual style.
3. Build a one-frame cover storyboard: visible conflict, subject action, proof object, emotional beat, viewer question, and forbidden static-poster failure mode.
4. Build a design layout brief: first-read, second-read, third-read, layout zones, visual weight, reading path, negative space, and forbidden layouts.
5. Build a copy hierarchy: main title, subtitle if any, state labels if any, object/zone binding, isolation rules, forbidden adjacency, and text removal rule.
6. Select the platform ratio and target canvas, then adapt the layout before writing the visual concept.
7. If a reference image is provided, split it into identity traits to preserve and pose/action traits to ignore unless the user explicitly asks to preserve them.
8. If the exact on-cover text is not supplied, or if the user's title is shortened or rewritten, run the Copy Approval Gate and wait for explicit approval of the exact on-cover text.
9. Produce an Execution Design Packet with copy approval, topic translation, cover storyboard, design layout brief, copy hierarchy, reference handling, identity and final-prompt firewall, and pre-generation self-check.
10. If any self-check item fails, revise the Execution Design Packet before writing the final image prompt.
11. Map the approved storyboard and layout brief to one clear cover concept and choose the subject role/action required by the engine.
12. Write a GPT Image 2 prompt packet with platform adaptation, reference handling, identity preservation, composition, subject, typography layout system, lighting, readability, and negative constraints.
13. Save the exact final generation prompt to a prompt file and run the mother skill's `scripts/verify_prompt_firewall.py` with `Dan Koe` and common aliases passed as `--forbid`. If a portrait/reference image is supplied, pass `--require-identity-reference`. Do not generate if the script fails.
14. Ask whether the user wants direct generation.
15. Generate only after confirmation and only after the prompt firewall has passed.

## Execution Gate

Do not write the final GPT Image 2 prompt, and do not generate an image, unless the current turn contains a concrete Execution Design Packet.

Required packet fields:

- Copy approval: exact approved on-cover text, or "no text". If the user's title was shortened or rewritten, include the approved candidate. Permission to shorten is not approval of a specific title.
- Topic translation: raw topic, creator-engine translation, click promise, visible stake, proof object, and forbidden drift.
- Cover storyboard: story moment, conflict, subject action, proof object, emotional beat, viewer question, and why it is not a static poster.
- Design layout brief: first-read, second-read, third-read, layout zones, visual weight, reading path, negative space, platform safe area, and forbidden layouts.
- Copy hierarchy: main title, subtitle if any, labels if any, object/zone binding, isolation rules, forbidden adjacency, and removal rule.
- Reference handling: identity traits to preserve, pose/action traits to ignore, and new hook-driven action.
- Identity and final-prompt firewall: who the subject must look like, which reference controls identity, which creator/style words are forbidden in the final prompt, how the creator pattern is rewritten without naming the creator, and the exact `verify_prompt_firewall.py` command that must pass before generation.
- Pre-generation self-check: engine match, story clarity, flat design hierarchy, copy isolation, platform safe area, reference handling, and drift risk.
- Post-generation dimension check: after image generation, verify actual pixel dimensions against the requested target canvas or aspect ratio before reporting success. Use the mother skill's `scripts/verify_image_dimensions.py` when a local generated file is available.

If the packet is weak, fix the packet first. Do not compensate by adding more visual adjectives to the final prompt.

## Copy Approval Gate

If changing the user's title, stop before final prompt writing and provide:

- 3-5 candidate on-cover titles
- the semantic meaning each candidate preserves
- the meaning each candidate drops or weakens
- one recommendation

Continue only after the user approves one exact title or provides replacement text.

## Output Format

```markdown
## Execution Design Packet
Copy approval:
Topic translation:
Cover storyboard:
Design layout brief:
Copy hierarchy:
Reference handling:
Identity and final-prompt firewall:
Pre-generation self-check:

## Cover Prompt
<final GPT Image 2 prompt>

## Generation Settings
model: gpt-image-2
platform:
aspect_ratio:
target_canvas:
quality:
post_generation_check:

## Negative Constraints
<constraints>

## Iteration Plan
<2-3 likely improvements after first image>

是否需要我直接生成？
```

## Design Standard

# PigeonYang Cover Design Standard: Dan Koe

## Scope
Use this standard to create original video covers that apply Dan Koe's transferable cover logic: serious creator authority, a blunt intellectual claim, minimal studio composition, and strong typography. It is best for topics about personal transformation, creator economy, writing, focus, AI workflows, one-person business, thinking, and future-of-work arguments.

Do not copy Dan Koe's likeness, exact recurring cover, channel identity, or private brand assets. Use the user's own portrait or a neutral subject.

## Evidence Summary
- Cover samples: 12 public YouTube thumbnails from Dan Koe's channel, archived in the managed research run under `covers/`.
- Process sources: 5 archived sources, including Dan Koe's YouTube RSS feed, Dan Koe's own content-system writing, and third-party content-system breakdowns.
- Research run: `dan-koe/20260525-181547` in the user's configured research workspace.
- Confidence: High for 2025-2026 talking-head authority thumbnails; medium for older visual-explainer variants because the current sample set favors text-left/face-right covers.

## Core Design DNA
1. Turn the topic into one blunt belief-level claim before designing the image.
2. Make the person the authority proof: close face, direct eye contact, serious expression, restrained gesture.
3. Let typography carry the story: huge bold sans-serif text, clean line breaks, one emphasized hinge phrase.
4. Keep the visual world quiet: gray/black/white studio background, shallow depth, no decorative clutter.
5. Use contrast in meaning, not spectacle: wrong belief vs better belief, current self vs future self, outdated skill vs new skill.
6. Use one accent at most: white plate, pale yellow word, or red underline.

## Cover Generation Engine
- Engine type: Hybrid `Authority Engine` + `Transformation Engine` + `Utility Clarity Engine`.
- Viewer decision compressed: "Does this creator understand the hidden rule behind my stalled growth, thinking, work, or identity?"
- Topic-to-cover mechanism: Convert the raw topic into a hard claim, warning, command, paradox, identity reframe, or shortcut. The claim must feel like a diagnosis.
- Subject role: Expert and witness. The subject looks like they have seen the pattern and are telling the viewer directly.
- Pre-visual decision: Decide the one sentence the viewer must believe after seeing the cover. If this sentence is weak, fix the sentence before designing.
- Drift risk: Giant props, money, shock faces, colorful AI visuals, busy screenshots, dashboard collages, or comparison boards move the cover away from Dan Koe.

## Topic Translation Rules
- Abstract topics: translate into a viewer belief, mistake, identity shift, or mental model. Do not literalize into a complicated diagram unless the user explicitly asks for a visual explainer variant.
- Concrete topics: translate into a simple shortcut, command, proof claim, or number-backed utility.
- Required translation variables: viewer pain, wrong belief, better belief, one-sentence claim, topic lane, proof object if any, subject authority action, exact on-cover text.
- Forbidden translation moves: physical spectacle, prize/reward scenes, multiple feature cards, tool screenshots as the hero, neon AI backgrounds, cute metaphors, busy before/after boards.
- Example translation: Raw topic "I built an AI content flywheel" becomes "your content system is backwards" or "your ideas need a system" depending on whether the hook is diagnosis or transformation.

## Cover Storyboard Rules
- Story moment: the expert catches the viewer in a mistaken assumption and names the sharper rule.
- Visible conflict: wrong belief vs better belief, scattered behavior vs clear system, outdated skill vs future skill, passive consumption vs deliberate creation.
- Subject task/action: direct stare, lean-in, finger-to-temple, hands together, or restrained explaining gesture. The action should support the claim.
- Proof object: usually the claim plus subject authority. Use a blurred UI, document, notes, or prompt canvas only when it makes a workflow/software claim more believable.
- Viewer question: "Am I making this mistake?" or "What does this person know that I don't?"
- Forbidden static compositions: ordinary portrait with title pasted on it, product dashboard hero shot, icon collage, slide-deck comparison, or generic AI illustration.
- Example storyboard: A serious creator leans toward camera on the right, one hand raised in a contained explanation; the left side says `your content system is backwards`, with `backwards` isolated on a white plate; behind the text is a blurred writing/workflow canvas.

## Design Layout Brief Rules
- First read: the approved on-cover claim in huge type.
- Second read: the subject's face and expression.
- Third read: one emphasized word, number, or subtle background proof.
- Layout zones: in 16:9, left 50-60% text zone and right 35-45% face zone. In vertical formats, stack title top/middle and face lower/middle while keeping both central.
- Visual weight: text and face dominate equally; proof objects stay blurred and secondary.
- Reading path: main sentence first, emphasized phrase second, face third, optional background cue last.
- Negative space: preserve a smooth dark or light field behind every text line. Create a plate before placing text on busy UI.
- Forbidden layouts: three-column comparisons, dense cards, many badges, edge-critical text, a background so detailed that the title needs shrinking, or text blocks that form the wrong sentence when read together.

## Copy Hierarchy Rules
- Main title: one concise thesis, command, warning, or identity reframe. Ideal length is 3-9 words; up to 12 if line breaks are clean.
- Subtitle: usually none. If needed, use a small secondary phrase below the main title, not another claim.
- State labels: avoid unless adapting to a comparison request. Prefer one sentence over labels.
- Object/zone binding: bind any label to a concrete blurred object or UI zone, never near the main title as a floating phrase.
- Isolation rules: keep the main claim in one protected block. Highlight only the hinge phrase.
- Forbidden adjacency: do not place a label or subtitle where it can be read as the beginning or continuation of the main sentence.
- Removal rule: if two text blocks compete, remove the lower-priority block and make the image carry that meaning.

## Platform Adaptation
| Platform/mode | Ratio | Composition rule |
|---|---:|---|
| YouTube long video | 16:9 | Use the native Dan Koe structure: left text, right face, blurred studio/UI background. |
| Bilibili native upload | 1146:717, approx 16:10 | Keep text and face inside a 16:9/4:3 safe center; avoid side-edge title endings. |
| Bilibili cross-platform | 16:9 | Keep the face slightly larger than YouTube-safe so it survives feed previews. |
| Bilibili 4:3-safe | 4:3 | Stack shorter text; use chest-up face; remove optional proof objects. |
| Douyin horizontal | 4:3 | Compress text to 2-3 lines; face occupies right or lower-right; keep central safe area. |
| Douyin vertical | 3:4 | Use top text and lower face, or face right-middle with stacked left/upper text; no 9:16 unless user asks for short-video frame, not Douyin cover. |
| Xiaohongshu | 3:4 | Use a cleaner portrait card version with one thesis and strong face; avoid dense note-style labels. |
| Xiaohongshu square | 1:1 | Put face and claim in a tight two-zone layout; use only one highlight. |
| TikTok / Reels / Shorts | 9:16 | Use vertical poster logic, but preserve Dan Koe restraint: one claim, close face, dark background. |

## Layout Patterns
### Pattern 1: Diagnosis Claim
- Use when: the topic exposes a mistake, false belief, or hidden blocker.
- Composition: text-left/face-right, direct stare, dark blurred background.
- Text: one sentence like `you are learning the wrong skills`.
- Avoid: literal mistake icons, big red X marks, or multi-point explanations.

### Pattern 2: Transformation Promise
- Use when: the topic promises identity change, skill change, or life change.
- Composition: calm face right, softer expression, left stacked sentence with one highlighted phrase.
- Text: `your life will look drastically different` or equivalent approved wording.
- Avoid: before/after split screens, fitness-style transformation, or motivational poster tone.

### Pattern 3: Tactical Shortcut
- Use when: the topic offers prompts, systems, routines, or workflows.
- Composition: face right, text left, optional blurred UI/workspace in background.
- Text: command or number-backed phrase like `steal these 6 prompts`.
- Avoid: turning the cover into a software ad or showing a readable dashboard.

### Pattern 4: Market Shift Warning
- Use when: the topic argues that an old category is dying or a new category is rising.
- Composition: serious face, large all-caps or title-case warning, one pale yellow emphasized word.
- Text: `THE DEATH OF INFO PRODUCTS` style, adapted to the user's exact approved topic.
- Avoid: apocalyptic visuals, flames, money, or news-poster graphics.

## Subject Rules
Use a close-up or chest-up portrait. Preserve the user's identity from reference images, but redesign pose and expression for the hook. Preferred expression is serious, focused, restrained, and slightly confrontational. Use hands only when they communicate thinking, explanation, or conviction. Keep clothing simple and neutral.

## Reference Image Handling
Reference images lock identity traits, face traits, hair, clothing preference, product appearance, or brand assets. They do not lock the pose, facial expression, crop, lighting, or background unless the user explicitly says so. For this pattern, convert a casual reference into a calm authority portrait with direct eye contact. The final image subject must resemble the user's supplied reference and must not resemble any public creator.

## Identity And Final Prompt Firewall

- Internal skill routing may name Dan Koe, but the final GPT Image 2 prompt must not contain `Dan Koe`, `Dan Koe-inspired`, `in the style of Dan Koe`, `like Dan Koe`, or any equivalent creator-name shortcut.
- Express the pattern through concrete cover mechanics: serious authority portrait, one blunt claim, minimal studio composition, protected title field, restrained grayscale palette, and one accent at most.
- If a portrait reference is supplied, identity preservation outranks all creator-pattern rules. The subject must preserve the user's face, hair, glasses, clothing cues, body type, and supplied identity traits.
- Add a negative constraint that the generated subject must not resemble any public creator, without naming Dan Koe in the final prompt.

## Text Rules
Use bold geometric or grotesk sans-serif typography. Use white text on dark backgrounds or black text on white plates. Keep line breaks semantic. Use lowercase for conversational claims; use all caps only for blunt warnings or market-shift claims. Never use more than one accent treatment.

## Typography Layout System
Protected text zones are mandatory. In wide layouts, reserve the left half as a clean title field; in vertical layouts, reserve the upper/middle central area. If the background contains UI, blur and darken it or place the hinge phrase on a white plate. The main title must be visually isolated from subtitles, labels, and proof objects. The final cover must not create accidental phrases through nearby text blocks.

## Color And Lighting Rules
Use grayscale, charcoal, black, white, and cool gray. Optional accent: pale yellow for one word or red for one underline. Keep saturation low. Light the face with a soft key light and mild vignette. Background should be dim, blurred, and unobtrusive.

## Hook Mechanics
- Contrarian diagnosis: viewer's current belief is wrong.
- Identity reframe: the viewer should become a different kind of person.
- Transformation promise: a simple practice changes the future self.
- Command: do this one thing now.
- Paradox: the cure is counterintuitive.
- Market shift: an old model is dying and a new model rewards the prepared.

## GPT Image 2 Prompt Contract
Every prompt must include:
- target platform, aspect ratio, and exact pixel canvas
- exact approved on-cover text
- one-sentence topic translation
- portrait placement and expression
- protected text zone
- typography hierarchy and highlight treatment
- background simplicity and optional proof object
- platform crop safety
- negative constraints against spectacle, clutter, neon, copied likeness, weak typography, and text adjacency errors

## Negative Constraints
No Dan Koe likeness replication. No MrBeast-style extreme stakes. No giant machines, money piles, neon AI robots, holographic dashboards, crowded interface screenshots, multiple title blocks, decorative icons, arrows everywhere, shock faces, or tiny unreadable text. Do not place labels near the main title if they can be misread as one sentence.

## User Intake Questions
1. 你要发哪个平台？横版、竖版还是都要？
2. 原始标题或视频主题是什么？
3. 你是否允许我改短封面文字？如果允许，我会先给候选文案让你确认。
4. 是否放你的真人形象或其他参考图？
5. 这个主题更偏身份转变、商业判断、写作创作、AI工作流、还是趋势判断？
6. 有哪些必须避免的东西：太攻击、太销售、太暗、太像本人、太抽象？

## Quality Checklist
- The topic has been translated into one Dan Koe-style belief-level claim.
- The exact on-cover text has been approved by the user if rewritten.
- The face reads as authority, not entertainer shock.
- Text is the first read and remains readable at feed size.
- Only one main claim exists.
- Highlight treatment is limited to one hinge phrase or word.
- Background is quiet enough for the title.
- Layout does not create accidental combined phrases.
- Platform ratio and target canvas are explicit.
- Reference image preserves identity but not weak source pose.
