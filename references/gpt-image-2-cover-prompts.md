# GPT Image 2 Cover Prompt Rules

## Goal

Write production prompts for video covers, not moodboard prompts.

The prompt must specify:

- final artifact type: finished video thumbnail or cover
- target platform and aspect ratio
- target canvas in pixels
- subject and relationship between elements
- creator cover generation engine and topic translation decision
- selected internal paradigm and rejected internal paradigms
- one-frame cover storyboard
- design layout brief and copy hierarchy
- composition and focal hierarchy
- exact on-image text, or explicitly no text
- color, lighting, typography, and finish
- identity preservation and final-prompt creator-name firewall
- constraints that protect readability and avoid unwanted copying

## Prompt Packet

Use this structure:

```markdown
Execution Design Packet:

Copy approval:
<exact approved on-cover text, or "no text"; if rewritten from the user's title, include the approved candidate and why it preserves the intended meaning>

Topic translation:
<raw topic -> creator-engine translation; name the click promise, visible stake, proof object, and forbidden drift>

Selected internal paradigm:
<chosen paradigm card from the child skill, why it fits, and why other internal paradigms were rejected>

Cover storyboard:
<one-frame story: story moment, visible conflict, subject action, proof object, emotional beat, viewer question, and why this is not a static poster>

Design layout brief:
<first-read, second-read, third-read, layout zones, visual weight, reading path, negative space, platform safe area, and forbidden layouts>

Copy hierarchy:
<main title, subtitle if any, state labels if any, object/zone binding, isolation rules, forbidden adjacency, and text removal rule>

Reference handling:
<identity traits to preserve, pose/action traits to ignore, and the new hook-driven action>

Identity and final-prompt firewall:
<who the generated subject must look like; which supplied reference controls identity; which creator names, style labels, and "inspired by" phrases are forbidden in the final generation prompt; how the creator pattern is rewritten as concrete design rules>

Pre-generation self-check:
- Engine match:
- Story clarity:
- Flat design hierarchy:
- Copy isolation:
- Platform safe area:
- Target canvas:
- Reference handling:
- Identity firewall:
- Drift risk:

Final GPT Image 2 Prompt:

Create a finished <platform> video thumbnail in <aspect ratio>, target canvas <width>x<height> pixels.

Platform adaptation:
<why this ratio and target canvas fit the platform and how composition changes for this platform>

Topic:
<what the video is about>

Cover generation engine:
<engine type and why this creator uses it for this topic>

Selected internal paradigm:
<internal paradigm card chosen for this cover; include rejected internal paradigms if they affected the decision>

Topic translation:
<how the raw topic was transformed before visual design; for abstract topics, state whether it became a physical event, concept label, transformation proof, suspense gap, utility result, or aesthetic atmosphere>

Cover storyboard:
<one-frame story: visible conflict, subject action, proof object, emotional beat, viewer question, and why this is not a static poster>

Design layout brief:
<first-read, second-read, third-read, layout zones, visual weight, reading path, negative space, and forbidden layouts>

Copy hierarchy:
<main title, subtitle if any, state labels if any, object/zone binding, isolation rules, forbidden adjacency, and text removal rule>

Thumbnail concept:
<one-sentence click promise>

Composition:
<where each major element goes, scale, camera distance, negative space>

Main subject:
<person/object/scene details; use user's own reference image if supplied>

Reference handling:
<what to preserve from references, what not to copy, and what new action/pose is required>

Identity preservation:
<if a portrait reference is supplied, state that the generated person must preserve the user's identity from that reference and must not resemble the distilled creator or any public creator>

Text:
Exact on-image text: "<text>"
Typography: <font category, weight, stroke/shadow, placement>

Typography layout system:
<main title zone, label zones, badge/backing shapes, padding, background isolation, safe-area rules>

Visual style:
<distilled creator-pattern rules translated into original design strategy; do not name the creator or write "inspired by">

Color and lighting:
<palette, contrast, rim light, background treatment>

Readability constraints:
<mobile readability, large face/object, simple background, no clutter>

Do not:
<negative constraints>
```

## GPT Image 2-Specific Guidance

- If the user supplies a long title and permits shortening, do not treat that as approval of your rewritten title. First propose 3-5 copy candidates, explain the semantic tradeoff of each, recommend one, and wait for explicit approval.
- The final prompt may contain only the approved exact on-image text. If no title has been approved, stop before final prompt writing and ask for copy approval.
- Do not write the final GPT Image 2 prompt until the `Execution Design Packet` is complete.
- Do not generate an image if any `Pre-generation self-check` item fails. Revise the topic translation, storyboard, layout brief, or copy hierarchy first.
- The self-check must be concrete, not a generic checklist. Each item should state the actual design decision for this cover.
- Use direct layout instructions instead of vague adjective stacks.
- Include the exact target canvas in the final prompt, for example `target canvas 1440x1080 pixels` for Douyin horizontal 4:3 or `target canvas 1080x1440 pixels` for Douyin vertical 3:4.
- After generation, check the actual output dimensions. If the output ratio or canvas is wrong, do not call the task complete.
- Use `scripts/verify_image_dimensions.py` for the post-generation check when a local generated file is available.
- Before generation, save the exact final prompt to a prompt file and run `scripts/verify_prompt_firewall.py`. Use `--forbid` for the distilled creator's name and aliases. If a portrait/reference image is supplied, use `--require-identity-reference`.
- If `verify_prompt_firewall.py` fails, do not generate. Rewrite the final prompt until the script passes.
- Do not jump directly from a raw topic to visual style. First translate the topic through the child skill's cover generation engine.
- Do not use a child skill as one undifferentiated style. Select one internal
  paradigm from the child skill's `Popular Paradigms` before storyboard and
  composition. If no internal paradigm fits, route to another child skill.
- Do not jump from topic translation directly to composition. First build a one-frame cover storyboard. If the storyboard has no action, conflict, proof object, or viewer question, revise the story before writing image instructions.
- Do not jump from storyboard directly to image prompt. First write a design layout brief and copy hierarchy. If text blocks can be read as an unintended phrase, remove the lower-priority text or move it far away and bind it to an object/zone.
- A main title must be an isolated semantic unit. State labels must never sit close enough to the main title to be read as one sentence.
- If the picture already communicates before/after or bad/good states, prefer no state labels. Use fewer text blocks when the cover has a strong story moment.
- Avoid static presenter compositions such as a host pointing at a product, a neat before/after dashboard, a workflow diagram, or a clean product ad unless that creator's engine explicitly uses them.
- For `Stakes Engine` creators, turn abstract ideas into visible stakes: giant machines, extreme quantities, time pressure, money, danger, failure, reward, or a physical challenge. Avoid pure diagrams and course-poster logic unless the diagram is physically embodied as an object or machine.
- For AI or software topics under a `Stakes Engine`, do not default to cyberpunk, neon-blue labs, holographic UI, glowing abstract cores, or SaaS dashboards. Translate the topic into real-world props, physical studio machines, game-show contraptions, paper/cards/screens as objects, buttons, levers, belts, red tape, hazard stripes, and brightly lit practical sets.
- For `Authority Engine` creators, turn topics into concise concept names, intellectual tension, and high-trust visual hierarchy. Avoid fake spectacle that damages authority.
- For `Transformation Engine` creators, turn topics into before/after proof and a clear result gap.
- For `Aesthetic Identity Engine` creators, preserve atmosphere, taste, and recognizable visual world over exaggerated clarity.
- For `Narrative Suspense Engine` creators, build an unresolved question or threat signal without explaining everything.
- For `Utility Clarity Engine` creators, foreground the problem, tool, result, and scannable benefit.
- Keep on-image text short. Prefer 1-5 words for thumbnails.
- State exact text once and require correct spelling.
- Treat text as a separate protected design layer. Do not place text directly over clutter, faces, hands, detailed UI, or the main product unless the text has a backing shape.
- Specify a hierarchy: main title, state labels, optional numeric badges. Define exact zones such as top-center safe area, upper-left badge, upper-right badge, lower safe band.
- Use backing plates or badges for labels placed over busy backgrounds: solid or semi-transparent dark plate, colored rounded badge, sticker shape, or high-contrast band.
- Require padding around every text block. Text must not touch frame edges or overlap the host, hands, flywheel, product, or dense UI.
- For before/after thumbnails, use a matched badge system: left label and right label have the same size, style, alignment, and padding, with different semantic colors.
- Use reference images for the user's own portrait or product when identity matters.
- Ask for a reference image instead of inventing the user's likeness.
- Treat portrait/reference images as identity or asset references, not pose locks. Preserve identity traits such as face, hair, glasses, clothing, product shape, or brand colors, but explicitly choose a new pose/action that serves the cover hook.
- If the reference image has a static or thoughtful pose, explicitly say not to copy that pose unless it matches the thumbnail hook.
- When a portrait reference is supplied, the reference identity has higher priority than the distilled creator pattern. The final prompt must say that the subject should preserve the user's reference identity and must not resemble any public creator. Do not name the distilled creator in this negative constraint.
- The distilled creator's name may appear in the internal Execution Design Packet, but it must not appear in the final GPT Image 2 generation prompt. Do not write `<creator>-inspired`, `in the style of <creator>`, `like <creator>`, or similar wording in the final prompt.
- Before generation, run a final-prompt firewall pass: remove creator names, public-person likeness cues, and style-name shortcuts; replace them with concrete rules for composition, subject role, object hierarchy, typography, color, lighting, and story moment.
- For MrBeast-derived covers, the host action should be hook-driven: pointing at the reward, pushing away chaos, physically separating before/after sides, reacting with shock, straining under survival pressure, or presenting the prize.
- For MrBeast-derived covers, use prop-realistic commercial color rather than cyberpunk ambience: daylight/studio lighting, white rooms, yellow props, red tape, blue shirts/buttons, green grass, cash/gold objects, clean sky, and practical set lighting. Avoid deep blue sci-fi backgrounds unless the real physical object is space/underwater/night.
- Avoid "in the exact style of <living creator>" in the final generation prompt. Use distilled design rules instead.
- Avoid all creator-name style shortcuts in the final generation prompt, not only "exact style" wording.
- Ask the publishing platform before choosing aspect ratio. Use `references/platform-cover-standards.md` for platform defaults and adaptation rules.
- For Bilibili, do not default blindly to 16:9. Ask whether the cover is Bilibili-only, cross-posted to YouTube, or needs 4:3-safe card display. Use 1146:717 / approx 16:10 for Bilibili-native masters when the user has no stricter template.

## Negative Constraints

Always include constraints that fit the request:

- no extra text
- no misspelled text
- no unreadable small typography
- no text directly on cluttered backgrounds without a backing plate
- no inconsistent random text styling
- no copied logos or watermarks
- no exact recreation of existing thumbnails
- no use of the creator's likeness unless explicitly supplied and authorized
- no resemblance to the distilled creator when the user supplied their own portrait/reference image
- no distilled creator name, `inspired by`, or `in the style of` wording in the final generation prompt
- no cluttered background
- no unintentional copying of reference pose
- no cyberpunk default for AI/software topics
- no neon-blue holographic UI unless explicitly requested
- no dark sci-fi lab when the creator engine calls for real-world studio props

## Iteration Plan

After the first image, evaluate:

1. Does the thumbnail read at phone size?
2. Is the click promise visible without the title?
3. Is the subject hierarchy clear?
4. Is the text spelled exactly right?
5. Does every text block have a protected readable zone or backing shape?
6. Did the output drift into copying instead of original adaptation?
7. Did the output follow the creator's engine, or did it collapse into a generic infographic/poster?

