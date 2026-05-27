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
3. Select one internal paradigm from `Popular Paradigms`. Record why it fits and why the other internal paradigms were rejected. If no paradigm fits, route away from this child skill.
4. Build a one-frame cover storyboard: visible conflict, subject action, proof object, emotional beat, viewer question, and forbidden static-poster failure mode.
5. Build a design layout brief: first-read, second-read, third-read, layout zones, visual weight, reading path, negative space, and forbidden layouts.
6. Build a copy hierarchy: main title, subtitle if any, state labels if any, object/zone binding, isolation rules, forbidden adjacency, and text removal rule.
7. Select the platform ratio and target canvas, then adapt the layout before writing the visual concept.
8. If a reference image is provided, split it into identity traits to preserve and pose/action traits to ignore unless the user explicitly asks to preserve them.
9. If the exact on-cover text is not supplied, or if the user's title is shortened or rewritten, run the Copy Approval Gate and wait for explicit approval of the exact on-cover text.
10. Produce an Execution Design Packet with copy approval, selected internal paradigm, rejected internal paradigms, topic translation, cover storyboard, design layout brief, copy hierarchy, reference handling, identity and final-prompt firewall, and pre-generation self-check.
11. If any self-check item fails, revise the Execution Design Packet before writing the final image prompt.
12. Map the approved storyboard and layout brief to one clear cover concept and choose the subject role/action required by the selected internal paradigm.
13. Write a GPT Image 2 prompt packet with platform adaptation, reference handling, identity preservation, composition, subject, typography layout system, lighting, readability, and negative constraints.
14. Save the exact final generation prompt through the mother skill's workflow gate, preferably `scripts/coverctl.py save-final-prompt`, then run `scripts/coverctl.py verify-prompt-firewall` with `Dan Koe` and common aliases passed as `--forbid`. If a portrait/reference image is supplied, require identity-reference handling. Do not generate if the firewall fails.
15. Run `scripts/coverctl.py preflight-generation`. If it returns `generate`, generate directly without asking for another approval. If it returns `prompt_only`, output the exact final prompt and the missing generation condition.
16. Register any generated output, verify dimensions, and mark final only through the workflow gate.

## Execution Gate

Do not write the final GPT Image 2 prompt, and do not generate an image, unless the current turn contains a concrete Execution Design Packet.

Required packet fields:

- Copy approval: exact approved on-cover text, or "no text". If the user's title was shortened or rewritten, include the approved candidate. Permission to shorten is not approval of a specific title.
- Selected internal paradigm: the chosen `Popular Paradigms` card and why it fits this task.
- Rejected internal paradigms: which other internal paradigms were considered and why they were not chosen.
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
Selected internal paradigm:
Rejected internal paradigms:
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

## Generation Gate
<generate directly if preflight passes; otherwise output prompt_only with blocker>
```

## Design Standard

# PigeonYang Cover Design Standard: Dan Koe

## Scope

Use this standard when the user's topic can become a quiet but forceful
belief-level claim: one-person business, personal reinvention, deep work,
high-income skills, thinking, writing/content systems, future-of-work shifts,
or society-trap diagnosis.

Best-fit topics:

- solo creator business, knowledge products, micro education, productized
  expertise, niche-of-one positioning, and value creation
- life reset, identity rebuild, getting ahead, twenties, comeback, self-directed
  work, and hard personal standards
- deep work, focus, dopamine detox, routine design, discipline, walking,
  minimalist productivity, and attention control
- high-income skills, AI skill use, generalist careers, networking, fast
  learning, and future-proof skill stacks
- mental models, intelligence, reading, articulation, strategic thinking, and
  reprogramming the mind
- writing, essays, audience growth, content systems, personal brand, and
  creator economy shifts
- category death, future of work, AI-first careers, new economy paths, and the
  decline of old work models
- wage slavery, matrix/autopilot framing, NPC behavior, social conformity, and
  escape from modern traps

Do not use this standard for topics that need spectacle, documentary field
proof, huge objects, fake danger, crowd competition, cash-prize fantasy, product
beauty shots, or dense software dashboards. Do not copy Dan Koe's likeness,
exact thumbnails, channel identity, recurring private brand assets, or protected
marks. Use the user's own portrait, a neutral subject, or legally supplied
references.

## Evidence Summary

- Cover samples: 120 popular public YouTube video cards from Dan Koe's channel.
- Capture method: YouTube channel HTML plus `youtubei/v1/browse` continuation
  pages for the `Popular` chip.
- Source channel id: `UCWXYDYv5STLk-zoxMP2I1Lw`.
- Research run: `dan-koe/20260528-youtube-popular-top120`.
- Source artifact: `generated/youtube-popular-top120.json`.
- Contact sheet: `distillation/sample-contact-sheet.jpg`.
- Process sources: 6 saved sources in the run, including the current YouTube
  Popular capture, channel RSS feed, Dan Koe's own content/business writing,
  and two third-party content-system breakdowns.
- Prior baseline: the old standard used 12 samples and grouped the style into 4
  generic paradigms. The expanded 120-sample audit shows a more specific system:
  one stable authority-text surface and 8 recurring topic-lane paradigms.
- Confidence: high for YouTube-native covers about one-person business,
  reinvention, focus, skills, thinking, creator systems, future work, and
  society-trap framing. Medium for vertical/mobile platform adaptation because
  the evidence is YouTube-native. Low for topics with no belief-level claim or
  no credible human authority.

## Core Design DNA

1. Start from a belief-level claim, not a scene idea.
2. The first read is the claim: short, blunt, high-contrast typography.
3. The second read is the authority portrait: close face, direct or near-direct
   eye contact, serious expression, restrained gesture.
4. The third read is one accent or proof cue: teal/yellow phrase, red underline,
   white plate, book, laptop, diagram, or muted screen glow.
5. The background stays quiet: black, charcoal, gray, muted studio, desk blur,
   or soft abstract texture.
6. The cover promises a sharper rule, not spectacle.
7. Topic lane controls the promise. Business, reinvention, focus, skill,
   thinking, content, future work, and trap diagnosis should not collapse into
   one generic diagnosis template.

## Cover Generation Engine

- Engine type: `Belief-Level Authority Engine`, a hybrid of `Authority Engine`,
  `Transformation Engine`, and `Utility Clarity Engine`.
- Viewer decision compressed: "Does this person understand the hidden rule that
  explains my stalled life, work, thinking, skill path, or creator business?"
- Topic-to-cover mechanism: first route the topic to one internal paradigm, then
  compress it into a blunt claim, warning, command, paradox, identity reframe,
  or protocol.
- Subject role: expert, guide, witness, challenger, or lived proof. The subject
  is credible because they seem to have used the rule, not because the image is
  loud.
- Pre-visual decision: define the topic lane, one-sentence belief claim,
  subject role, proof cue, first read, second read, and forbidden drift before
  choosing pose, color, or typography.
- Drift risk: quote-card portraits, motivational posters, course ads, product
  dashboards, neon AI scenes, social-logo collages, MrBeast-style stakes, or
  Yingshijufeng-style documentary proof scenes.

## Popular Paradigms

### Paradigm 1: One-Person Business / Productized Self

- Evidence count: 28/120 primary assignments.
- Representative samples: 3, 9, 24, 26, 29, 30, 34, 36, 42, 43, 44, 45, 46,
  55, 57, 59, 65, 66, 69, 71, 84, 85, 87, 97, 99, 101, 102, 120.
- Best-fit topics: solo business, creator business, knowledge products, niche,
  digital writing, micro education, productized expertise, consulting,
  monetizing solved problems.
- Click promise: "My knowledge, taste, experience, or solved problem can become
  a business."
- Topic translation: turn the topic into productized self, productized
  knowledge, value creation, niche-of-one, or solo-business path.
- One-frame story: a calm authority figure points the viewer from their mind,
  skill, or problem into a credible business path.
- First read: business claim or productization phrase.
- Second read: serious creator portrait as proof that the model is lived.
- Text behavior: large white text with one teal/yellow emphasis phrase, a white
  plate, or a boxed imperative such as "productize yourself".
- Composition: text block and portrait dominate; diagrams or screens stay
  background proof.
- Failure mode: money-flex entrepreneur poster, SaaS dashboard, hustle quote,
  generic startup pitch, or fake luxury outcome.
- Prompt contract: show authority plus a clean productization claim; do not add
  fake cash, cars, luxury, or business-collage clutter.

### Paradigm 2: Life Reinvention / Identity Rebuild

- Evidence count: 22/120 primary assignments.
- Representative samples: 1, 6, 8, 10, 13, 17, 23, 27, 39, 64, 70, 72, 73, 76,
  83, 91, 96, 100, 103, 109, 111, 112.
- Best-fit topics: changing your life, rebuilding identity, hard resets,
  twenties, comeback stories, feeling lost, becoming a different person,
  escaping mediocrity.
- Click promise: "A severe but realistic rule can rebuild who I become."
- Topic translation: convert utility into a personal time-bound identity shift:
  reset, recreate, become unrecognizable, build, disappear, or come back.
- One-frame story: the subject confronts the viewer with the identity standard
  they are avoiding.
- First read: identity or life-change command.
- Second read: direct face, stillness, and seriousness.
- Text behavior: short hard phrases, sometimes time-boxed: 6 months, 7 days,
  12 months, 30 minutes.
- Composition: high-contrast text field plus close portrait, rarely more than
  one proof cue.
- Failure mode: motivational quote poster, gym-transformation before/after,
  sentimental self-help image, or vague aspirational typography.
- Prompt contract: make the identity rule concrete and severe; keep the visual
  calm enough to feel like counsel, not hype.

### Paradigm 3: Deep Work / Focus Protocol

- Evidence count: 18/120 primary assignments.
- Representative samples: 2, 4, 5, 7, 21, 41, 47, 51, 52, 62, 68, 75, 80, 106,
  108, 116, 118, 119.
- Best-fit topics: deep work, focus, routine, dopamine detox, discipline,
  walking, workday design, monk mode, minimalist productivity, attention
  control.
- Click promise: "A repeatable protocol can restore focus and compound results."
- Topic translation: turn the topic into a ritual, time block, detox, routine,
  protocol, or concentration rule.
- One-frame story: the authority figure reveals the disciplined operating rule
  behind uncommon output.
- First read: focus command, time block, or protocol title.
- Second read: concentrated face or restrained work gesture.
- Text behavior: time counts and protocol phrases work better than broad
  productivity slogans.
- Composition: text and portrait first; desk, book, screen, or room glow as
  muted proof.
- Failure mode: wellness routine board, calendar app screenshot, productivity
  dashboard, cozy lifestyle photo, or app-feature graphic.
- Prompt contract: show one hard focus rule and one credible human operator;
  keep tools secondary.

### Paradigm 4: High-Income Skill Stack / Future-Proof Skill

- Evidence count: 16/120 primary assignments.
- Representative samples: 16, 18, 20, 25, 37, 38, 50, 53, 58, 61, 81, 95, 107,
  110, 113, 115.
- Best-fit topics: learning, skill acquisition, AI use, generalist careers,
  networking, high-income skills, skill stacks, relevance over the next decade.
- Click promise: "There is a scarce skill path I should learn before the market
  moves."
- Topic translation: compress the topic into one named skill, stack, order, or
  future-proof learning command.
- One-frame story: the expert points to the skill that separates the viewer from
  the average crowd.
- First read: named skill, "learn this" claim, or future-proof warning.
- Second read: face credibility.
- Text behavior: imperative phrases, one number, or one time horizon; never a
  full curriculum map.
- Composition: portrait and text; optional minimal screen, list, or abstract
  opportunity signal behind the subject.
- Failure mode: course sales page, certificate ad, feature matrix, noisy AI
  dashboard, or "learn these 17 things" clutter.
- Prompt contract: make the skill feel scarce and urgent without visual hype.

### Paradigm 5: Thinking / Intelligence / Mental Model

- Evidence count: 10/120 primary assignments.
- Representative samples: 11, 14, 22, 32, 40, 67, 78, 86, 93, 94.
- Best-fit topics: intelligence, mental models, reading, articulation,
  strategic thinking, reprogramming the mind, gamified thinking, decision
  quality.
- Click promise: "A better mental model changes how I think and decide."
- Topic translation: turn abstract thinking into one mental action: articulate,
  reprogram, read, strategize, gamify, or think like a genius.
- One-frame story: the subject is not posing; they are showing a cognitive rule.
- First read: mental model claim.
- Second read: intense thinking face or subtle mind/diagram cue.
- Text behavior: tight phrase with one cognitive verb; avoid long philosophy.
- Composition: face and typography dominate; mind maps, game HUDs, book stacks,
  or diagrams are restrained accents.
- Failure mode: neon brain poster, dense mind map, academic slide, mystical
  spirituality image, or philosophical quote card.
- Prompt contract: make intelligence visible through hierarchy and gesture, not
  decorative brain effects.

### Paradigm 6: Creator Content System / Audience Growth

- Evidence count: 9/120 primary assignments.
- Representative samples: 19, 28, 31, 48, 56, 60, 63, 77, 98.
- Best-fit topics: writing, essays, digital writing, audience building, social
  media, content systems, creator economy, personal brand, newsletter flywheels.
- Click promise: "There is a writing/content system that still works after the
  old platform game breaks."
- Topic translation: convert the topic into a writing command, authentic content
  rule, audience-from-zero path, or old-channel death warning.
- One-frame story: the authority figure turns writing and ideas into audience
  leverage.
- First read: writing/content claim.
- Second read: creator portrait or writing proof.
- Text behavior: blunt command or warning, not a multi-step content calendar.
- Composition: text and face first; notebook, laptop, essay page, or social
  feed stays secondary.
- Failure mode: social media logo collage, funnel diagram, marketing dashboard,
  platform-growth infographic, or viral-hack poster.
- Prompt contract: make writing or content discipline feel like an operating
  system, not a platform hack.

### Paradigm 7: Future Of Work / Category Death

- Evidence count: 9/120 primary assignments.
- Representative samples: 12, 15, 74, 82, 88, 90, 105, 114, 117.
- Best-fit topics: future of work, AI disruption, career path shifts, personal
  brand decline, creator work, new economy, self-improver careers.
- Click promise: "An old category is dying, and there is a new path I need to
  understand before it is late."
- Topic translation: turn the topic into a category-death phrase,
  future-of-work claim, time-window warning, or new-path announcement.
- One-frame story: the expert acts as witness to a market shift.
- First read: death/future/new-path warning.
- Second read: severe portrait or small symbolic proof.
- Text behavior: short declarative warnings with strong nouns: death, future,
  work, career path, AI-first.
- Composition: dark or muted background, clean text, close subject, optional
  subtle tech/future cue.
- Failure mode: apocalyptic news poster, cyberpunk AI spectacle, trend report
  slide, or generic business forecast.
- Prompt contract: urgency must come from the claim and face, not from chaos.

### Paradigm 8: Modern Slavery / Society Trap Diagnosis

- Evidence count: 8/120 primary assignments.
- Representative samples: 33, 35, 49, 54, 79, 89, 92, 104.
- Best-fit topics: wage slavery, social traps, NPC/autopilot, matrix metaphor,
  autonomy, control, anti-conformity, escape narratives.
- Click promise: "The system trapping me has a name, and there is an escape."
- Topic translation: frame the topic as trap, pyramid, matrix, wage slavery,
  autopilot, modern slavery, or social conditioning.
- One-frame story: the authority figure calls out the trap the viewer is living
  inside.
- First read: provocative trap diagnosis.
- Second read: severe portrait, often more monochrome and confrontational.
- Text behavior: short charged nouns work better than long explanations.
- Composition: high-contrast text plus portrait; abstract cage/matrix/pyramid
  cues must stay minimal.
- Failure mode: conspiracy board, doomer poster, political propaganda, or
  over-dark horror image.
- Prompt contract: diagnose the trap sharply while keeping the visual clean and
  intellectually controlled.

## Topic Translation Rules

1. Pick the internal paradigm before writing copy or prompt details.
2. Convert the raw topic into one belief-level claim the viewer can understand
   in under one second.
3. Business topics become productized knowledge, niche-of-one, value creation,
   or one-person business paths.
4. Reinvention topics become identity standards, hard resets, time-boxed change,
   or severe rules.
5. Focus topics become protocols, routines, time blocks, detox rules, or deep
   work constraints.
6. Skill topics become scarce skill, future-proof stack, learning order, or time
   horizon.
7. Thinking topics become mental model, reprogramming, articulation, strategic
   thinking, or reading/intelligence action.
8. Content topics become writing command, audience-from-zero path, creator
   system, or old-platform death warning.
9. Future-work topics become category death, new path, AI-first shift, or
   career-window warning.
10. Society-trap topics become named trap, matrix, autopilot, pyramid, wage
    slavery, or escape frame.
11. Forbidden translation moves: giant money props, fake danger, crowd
    competition, documentary field proof, busy UI screenshots, platform-logo
    collage, or abstract neon AI spectacle.

## Cover Storyboard Rules

- Story moment: the authority figure names the hidden rule, trap, protocol, or
  path the viewer has missed.
- Visible conflict: old belief vs sharper belief, passive life vs intentional
  rebuild, distracted mind vs focus protocol, old work path vs new economy,
  trapped self vs autonomous self.
- Subject task/action: direct stare, slight lean-in, restrained pointing,
  hand-to-temple, hands together, holding a notebook, or explaining with one
  hand.
- Proof object: usually the text plus human authority. Use document, book,
  laptop, diagram, screen glow, or abstract system cue only when it clarifies
  the claim.
- Emotional beat: serious, challenging, calm, mildly urgent, never shocked or
  goofy.
- Viewer question: "Is this the rule I missed?" or "Am I living inside this
  mistake?"
- Forbidden static composition: generic portrait with pasted title, quote card,
  product ad, lecture slide, dashboard hero, multi-card carousel, or noisy
  before/after board.

## Design Layout Brief Rules

- First read: blunt claim, warning, command, named protocol, or category-death
  phrase.
- Second read: serious human authority portrait.
- Third read: one accent, proof object, or context cue.
- Text zone: 40-60% of canvas, protected by dark field or solid backing.
- Subject zone: 35-50% of canvas, close portrait or upper body.
- Proof zone: 0-20% of canvas, always behind the text/subject hierarchy.
- Reading path: title claim, face, accent/proof cue.
- Negative space: preserve clean dark or gray space around the title; do not
  fill unused space with icons.
- Forbidden layouts: equal-weight cards, dense comparison boards, screenshot
  walls, full-width quote posters, centered title over busy face, and decorative
  split layouts with no claim hierarchy.

## Copy Hierarchy Rules

- Main title: one blunt claim, usually 2-7 words on cover.
- Subtitle: optional; only if it is shorter than the main title and visually
  subordinate.
- State labels: use only when bound to a visual object or topic lane, such as
  "old path", "new path", "anti-vision", "focus", or "deep work".
- Text isolation: separate the main claim from small context text; never place
  two competing slogans side by side.
- Forbidden adjacency: do not put a secondary label so close to the title that
  the viewer reads it as one confusing sentence.
- Text removal rule: if the portrait and claim already explain the promise, cut
  subtitles and labels.

## Platform Adaptation

- YouTube long video: default fit. Use 16:9, 1280x720 or 1920x1080. Keep the
  main text large enough to read in the subscription feed.
- Bilibili cross-platform: use 16:9 or Bilibili-safe wide layout. Increase text
  size and avoid tiny English-only copy if the audience is Chinese.
- Bilibili 4:3-safe: keep the face and main claim in the central area; remove
  third-read proof objects first.
- Xiaohongshu 3:4 or square: stack the claim above or beside the face, keep one
  proof cue, and avoid tiny subtitles.
- TikTok/Reels/Shorts 9:16: use vertical portrait poster logic with title in the
  upper or middle protected zone and face below/alongside it.
- WeChat article cover: use the child skill only as an internal design engine;
  preserve PigeonYang identity and WeChat 2.35:1 safe-area rules from the mother
  workflow.

## Layout Patterns

### Pattern A: Text Left / Authority Right

- Best for: business, reinvention, focus, skills, trap diagnosis.
- First read: large claim on left.
- Second read: close portrait on right.
- Proof cue: tiny screen, book, line, plate, or accent word.
- Failure: face too small or text too close to face.

### Pattern B: Authority Left / Text Right

- Best for: interview, guest, direct challenge, or when subject gaze points into
  the claim.
- First read: claim on right in a clean field.
- Second read: face on left.
- Proof cue: subdued background object behind the text.
- Failure: subject becomes a decorative headshot.

### Pattern C: Central Claim With Split Presence

- Best for: category death, future work, thinking, or trap framing.
- First read: central or near-central claim.
- Second read: severe face adjacent to the claim.
- Proof cue: minimal abstract shape or dim symbolic cue.
- Failure: generic quote poster.

### Pattern D: White Plate / Accent Word

- Best for: productization phrases, focus commands, category warnings.
- First read: one key phrase isolated on white or accented plate.
- Second read: portrait and dark field.
- Proof cue: none or one small object.
- Failure: too many plates or sticker-like clutter.

## Subject Rules

- Subject role: expert, guide, witness, challenger, or lived proof.
- Expression: serious, calm, direct, skeptical, focused, or mildly urgent.
- Gesture: restrained explaining gesture, pointing, thinking pose, hands clasped,
  holding a notebook, or still stare.
- Clothing: simple dark or neutral top; no costume, luxury flex, or loud brand
  styling.
- Framing: close-up, head and shoulders, or upper body. Face must be readable.
- Skin/face treatment: realistic, not over-smoothed, not caricatured.
- Do not make the subject resemble Dan Koe unless the user explicitly owns and
  supplies that authorized likeness.

## Reference Image Handling

- If the user supplies a portrait/reference image, preserve the user's identity:
  face, hair, glasses, clothing cues, body type, age range, and other explicit
  traits.
- Redesign pose/action only to match the selected paradigm unless the user asks
  to preserve the original pose.
- If no portrait is supplied, use a neutral original subject or non-likeness
  figure.
- Do not infer Dan Koe's face, hair, or body as the subject model.
- If a brand reference is supplied, use only authorized colors/logos and keep
  them subordinate to the claim/portrait hierarchy.

## Identity And Final Prompt Firewall

- Dan Koe is an internal routing and research label only.
- Final GPT Image 2 prompts must not include `Dan Koe`, `Dan Koe-inspired`, `in
  the style of Dan Koe`, `like Dan Koe`, or creator-name shortcuts.
- Translate the pattern into concrete rules: serious authority portrait, blunt
  belief-level text, protected text zone, muted studio background, one accent,
  and selected internal paradigm.
- If the user supplies a portrait/reference image, the prompt must state that
  this reference controls identity and that the subject must not resemble any
  public creator.
- Before generation, save the final prompt and run the mother skill firewall
  with Dan Koe aliases forbidden.

## Text Rules

1. Text is the hook, not decoration.
2. Prefer 2-7 word cover copy; longer ideas must be compressed.
3. Use all caps or strong title case; avoid thin fonts.
4. Isolate one hinge phrase with color, underline, or backing plate.
5. Avoid three or more independent text blocks.
6. Avoid long subtitles unless platform crop demands extra explanation.
7. Keep text off the subject's face.
8. If the user's title is rewritten or shortened, get exact copy approval before
   final prompt writing or generation.

## Typography Layout System

- Type weight: heavy sans-serif, extra bold or black.
- Hierarchy: one dominant block, optional tiny support label.
- Alignment: left-aligned or centered within a protected field.
- Line breaks: break by meaning, not by equal line length.
- Backing: dark field, white plate, or solid rectangle only when it improves
  legibility.
- Accent: teal/cyan, pale yellow, muted red underline, or white plate; one
  accent family per cover.
- Safe area: keep type away from platform edges and subject face.
- Clutter handling: delete objects before shrinking type.

## Color And Lighting Rules

- Base palette: black, charcoal, cool gray, white, desaturated skin tone.
- Accent palette: cyan, teal, pale yellow, muted red, or cool screen glow.
- Lighting: soft studio key light, directional face light, mild rim light, low
  contrast background separation.
- Mood: serious, quiet, intellectual, not cinematic spectacle.
- Background: muted studio, desk, screen glow, wall gradient, abstract dark
  texture, or simple proof object.
- Avoid: saturated rainbow gradients, neon cyberpunk, warm luxury gold, busy
  stock-photo backgrounds, and over-lit corporate headshots.

## Hook Mechanics

1. Belief correction: "you are doing this wrong".
2. Identity promise: "you can become a different person".
3. Protocol promise: "this routine creates the result".
4. Scarcity warning: "this skill/path matters before it is late".
5. Category death: "the old game is ending".
6. Trap diagnosis: "the system keeping you stuck has a name".
7. Productized self: "your knowledge/problem/experience is the product".
8. Time compression: "6 months", "7 days", "30 minutes", "next 10 years", or
   another truthful time window.

## GPT Image 2 Prompt Contract

Every final image prompt must include:

- platform, aspect ratio, and target canvas
- selected internal paradigm and translated claim, without naming Dan Koe
- exact approved on-cover text or "no text"
- subject identity source and preservation rules
- subject role, expression, gesture, and framing
- first read, second read, and third read
- typography placement, protected text zone, line-break behavior, and accent
  treatment
- background, lighting, palette, and proof object
- negative constraints: no creator name, no public-creator resemblance, no exact
  thumbnail copy, no busy collage, no fake stakes, no thin/low-contrast text
- post-generation dimension check requirement

## Negative Constraints

- Do not copy Dan Koe's likeness, face, hair, exact thumbnails, channel identity,
  or private brand assets.
- Do not put creator/style shortcut wording in final generation prompts.
- Do not make a generic quote-card portrait.
- Do not use motivational-poster language without a sharp belief claim.
- Do not add fake luxury, cash, challenge, crowd, danger, charity, or prize
  stakes.
- Do not use course-sales graphics, certificate badges, SaaS dashboard hero
  shots, dense UI, feature matrices, or funnel diagrams.
- Do not use neon AI backgrounds, cyberpunk future scenes, platform-logo
  collages, or documentary field scenes unless another skill is selected.
- Do not place multiple unconnected claims on the same cover.
- Do not allow tiny text, thin text, low-contrast text, or text over the face.

## User Intake Questions

Ask only for missing production information:

1. What platform and target ratio/canvas is this cover for?
2. What is the raw topic, video title, article hook, or core claim?
3. Which topic lane is intended: business, reinvention, focus, skill, thinking,
   content, future work, or society trap?
4. What exact on-cover text is already approved? If none, propose 3-5 short
   options and wait for approval.
5. Is there a user portrait/reference image that must control identity?
6. What must be included or avoided for brand, legal, or factual reasons?

## Quality Checklist

- The selected internal paradigm is named and justified.
- The first read is a short belief-level claim, not a vague title.
- The second read is a credible authority portrait or authorized user identity.
- The cover has one accent or proof cue, not many.
- Text is phone-readable and isolated from the face.
- The visual does not promise fake spectacle, fake money, fake danger, or fake
  documentary proof.
- The final prompt does not include Dan Koe or style-name shortcuts.
- If a reference image is supplied, identity preservation is explicit.
- Platform ratio, target canvas, and safe areas are specified.
- The generated output is dimension-checked before delivery.
