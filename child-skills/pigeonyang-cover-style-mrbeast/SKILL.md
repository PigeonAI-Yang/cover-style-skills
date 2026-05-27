---
name: pigeonyang-cover-style-mrbeast
description: "PigeonYang-branded skill that uses the distilled MrBeast video cover and thumbnail design pattern to write GPT Image 2-ready prompts for original user covers. Trigger when the user asks for a cover in MrBeast's style, references MrBeast thumbnails, or asks to apply this creator cover formula."
---

# PigeonYang MrBeast Cover Style

## Role

Use this distilled creator-cover pattern to write original, GPT Image 2-ready cover prompts for the user's video.

Do not copy existing MrBeast thumbnails. Apply the transferable design strategy to the user's own topic, brand, face, product, and constraints.

## Identity And Final Prompt Firewall

The distilled creator name is an internal routing and analysis label only.

Never put `MrBeast`, `MrBeast-inspired`, `in the style of MrBeast`, `like MrBeast`, or equivalent creator-name shortcuts in the final GPT Image 2 generation prompt. Rewrite the pattern into concrete design rules: subject role, story moment, proof object, composition, typography, color, lighting, and negative constraints.

If the user supplies a portrait/reference image, that reference controls identity. Preserve the user's face, hair, glasses, clothing cues, body type, and other supplied identity traits. Redesign only the pose/action for the thumbnail hook unless the user explicitly asks to preserve the original pose. The final generation prompt must say the subject must not resemble any public creator, without naming MrBeast.

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
14. Save the exact final generation prompt through the mother skill's workflow gate, preferably `scripts/coverctl.py save-final-prompt`, then run `scripts/coverctl.py verify-prompt-firewall` with `MrBeast` and common aliases passed as `--forbid`. If a portrait/reference image is supplied, require identity-reference handling. Do not generate if the firewall fails.
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

# PigeonYang Cover Design Standard: MrBeast

## Scope
Use this standard when the user's topic can truthfully become a visible stake:
money, time, danger, quantity, prize, crowd, rule, endurance condition,
transformation, destruction, impossible object, or concrete consequence.

Best-fit topics:

- extreme comparisons: cheap vs expensive, small vs huge, weak vs powerful,
  before vs after, low value vs absurd value
- challenges with one visible rule: last to leave, press a button, keep a hand
  on an object, fit something into a shape, cross a boundary, hit a target
- survival/endurance: days, hours, isolation, wilderness, prison, desert,
  bunker, island, mountain, sky, water, or other visible containment
- crowd competitions: many people, ages, teams, countries, creators, groups, or
  public participants fighting for one prize
- prize/giveaway fantasies: cash, house, car, island, vacation, store, restaurant
  or object the viewer instantly understands as desirable
- danger/fear trials: predators, chase, traps, escape rooms, military/FBI/bounty
  hunter pressure, drowning, sharks, falling, fire, explosion, or other truthful
  risk frame
- philanthropic/transformation proof: blind/deaf people helped, wells, houses,
  animals rescued, weight change, life-changing donation, or other visible
  before/after impact

Do not use this standard for quiet thought leadership, subtle product taste,
abstract essays, SaaS dashboards, workflow diagrams, pure AI concepts, or calm
expert portraits unless the topic can honestly become one large visible stake.
Do not fake money, danger, charity, crowds, or prizes that the content cannot
deliver.

Do not copy MrBeast's likeness, channel identity, logos, exact thumbnails, fonts,
or protected franchise/IP cues. Use the user's own portrait, neutral subjects,
or original scene elements.

## Evidence Summary
- Cover samples: 120 popular public YouTube long-form MrBeast video cards.
- Capture method: YouTube channel HTML plus `youtubei/v1/browse` continuation
  for the `Popular` chip.
- Source channel: `@MrBeast`, channel id `UCX6OQ3DkcsbYNE6H8uQQuVA`.
- Research run: `mrbeast/20260528-youtube-popular-top120`.
- Source artifact: `sources/datas/mrbeast-youtube-popular-top-120-video-cards.json`.
- Contact sheet: `distillation/sample-contact-sheet.jpg`.
- Prior process sources remain in `mrbeast/20260524-203206`.
- Confidence: high for visible stakes, price ladders, endurance containers,
  crowd competition, prize fantasy, danger trials, giant stunts, and
  philanthropy/transformation proof. Medium for platform adaptation outside
  YouTube because the evidence is YouTube-native. Low for abstract topics with
  no truthful stake.

## Core Design DNA
1. Convert the topic into one visible event, not a concept poster.
2. The first read must be a stake: money, price gap, timer/day count, prize,
   crowd, danger, rule shape, giant object, or before/after consequence.
3. The subject is inside the event as host, participant, survivor, winner, loser,
   referee, rescuer, witness, or prize presenter.
4. The premise must be child-legible in under one second.
5. Text is sparse and usually numeric: `$1`, `$100M`, `DAY 100`, `#1`, `1000`,
   `BEFORE/AFTER`, or one rule label.
6. Faces, hands, arrows, red shapes, cash, crowds, vehicles, islands, boxes, and
   hazard colors are used as legibility devices, not decoration.
7. The title, thumbnail, and first video seconds should make one truthful
   promise. If the image promises a bigger stake than the content can prove, it
   fails.

## Cover Generation Engine
- Engine type: `Visible Stakes Engine`.
- Viewer decision compressed: "This premise is extreme, valuable, risky,
  generous, competitive, or absurdly clear. I need to see the outcome."
- Topic-to-cover mechanism: choose the stake first, then choose one internal
  paradigm: value gap, endurance container, crowd contest, prize/giveaway,
  danger trial, physical stunt/destruction, transformation proof, or simple rule
  object.
- Subject role: host, competitor, survivor, prize witness, challenger, rescuer,
  referee, winner, loser, or transformation proof.
- Pre-visual decision: define the single visible stake before choosing color,
  face expression, layout, or text.
- Drift risk: fake stakes, fake charity, fake danger, flowcharts, course posters,
  calm expert portraits, product ads, generic tech UI, abstract neon concepts,
  and multi-step process diagrams.

## Popular Paradigms
### Paradigm 1: Value Ladder / Extreme Comparison
- Evidence count: 16/120 primary assignments.
- Representative samples: 2, 3, 5, 11, 12, 15, 19, 36, 47, 51, 61, 78, 99,
  116.
- Best-fit topics: budget tiers, quality gaps, output scale, manual vs
  automated, small vs huge, cheap vs expensive, low value vs high value.
- Click promise: how different are the two extremes?
- Topic translation: convert the topic into two visible endpoints with one
  measurable gap.
- One-frame story: subject stands between, compares, or reacts to the extremes.
- First read: the gap.
- Second read: subject face/action.
- Text behavior: huge numeric labels only when they sharpen the gap.
- Composition: two extremes, no middle steps.
- Failure mode: feature matrix, dashboard comparison, or subtle product ad.
- Prompt contract: show two physical endpoints and make the gap judgeable in one
  second.

### Paradigm 2: Survival / Endurance Container
- Evidence count: 25/120 primary assignments.
- Representative samples: 4, 6, 7, 10, 14, 16, 21, 25, 28, 30, 38, 42, 46, 57,
  68, 72, 80, 81, 85, 87, 91, 107, 111, 114, 117.
- Best-fit topics: time pressure, isolation, hard constraints, long tests,
  persistence, stress tests, endurance experiments.
- Click promise: can they last under this visible condition?
- Topic translation: convert the topic into a physical container, environment,
  timer, day count, or harsh rule.
- One-frame story: subject is visibly trapped, waiting, surviving, or enduring.
- First read: container, timer/day label, or harsh condition.
- Second read: subject under pressure.
- Text behavior: one day/hour/progress label.
- Composition: subject physically contained by rule, place, or condition.
- Failure mode: dramatic background without a visible rule.
- Prompt contract: make the endurance condition visible before styling.

### Paradigm 3: Mass Competition / Crowd Geometry
- Evidence count: 15/120 primary assignments.
- Representative samples: 1, 8, 9, 29, 34, 40, 53, 60, 66, 77, 90, 105, 106,
  108, 119.
- Best-fit topics: people-count tests, creator competitions, teams, age groups,
  audience experiments, public participation, cohort comparisons.
- Click promise: who wins when many people face one simple rule?
- Topic translation: convert the topic into organized participants plus one
  shared prize/rule.
- One-frame story: crowd geometry proves scale while the subject anchors or
  referees the contest.
- First read: crowd scale, teams, or numbered groups.
- Second read: prize/rule/host.
- Text behavior: usually no text or one count/prize label.
- Composition: crowd simplified into lines, circles, teams, or color blocks.
- Failure mode: noisy group photo with no rule or prize.
- Prompt contract: people must be the proof of scale, not background texture.

### Paradigm 4: Prize / Giveaway Fantasy
- Evidence count: 18/120 primary assignments.
- Representative samples: 18, 22, 24, 31, 39, 41, 49, 58, 59, 71, 73, 94, 95,
  98, 101, 102, 103, 115.
- Best-fit topics: reward, gift, desired object, productized promise, generosity,
  abundance, one-minute spending, cash prize, winner-takes-object.
- Click promise: can someone really get or keep this thing?
- Topic translation: turn the value proposition into one desirable object or
  reward scene.
- One-frame story: subject presents the prize, someone reaches for it, or the
  prize fills the frame.
- First read: prize object.
- Second read: subject/winner reaction.
- Text behavior: optional value, price, or prize label.
- Composition: prize dominates; subject validates scale and desirability.
- Failure mode: generic luxury mood or unearned cash pile.
- Prompt contract: make the prize physically present and instantly legible.

### Paradigm 5: Fear / Chase / Danger Trial
- Evidence count: 17/120 primary assignments.
- Representative samples: 13, 17, 20, 27, 33, 37, 45, 52, 55, 63, 74, 82, 84,
  93, 96, 97, 100.
- Best-fit topics: fear exposure, chase, predator, trap, escape, military/police
  pursuit, drowning, speed danger, obstacle courses, risk-for-reward.
- Click promise: will the subject survive, escape, or face the danger for the
  reward?
- Topic translation: convert the topic into one visible threat plus one subject
  reaction/action.
- One-frame story: danger is close enough to matter.
- First read: threat object, predator, weapon, trap, vehicle, or hazard.
- Second read: subject fear/focus/action.
- Text behavior: optional reward or danger label.
- Composition: threat and subject share the frame with clear distance/impact.
- Failure mode: vague cinematic danger with no rule or reward.
- Prompt contract: danger must be specific and truthful, not generic drama.

### Paradigm 6: Giant Physical Stunt / Destruction
- Evidence count: 15/120 primary assignments.
- Representative samples: 23, 32, 35, 43, 48, 50, 56, 62, 65, 69, 83, 88, 89,
  109, 113, 118.
- Best-fit topics: giant objects, machines, destruction, absurd physical scale,
  construction, obstacle mechanics, huge food, trains, cars, diamonds, towers,
  backyard transformations.
- Click promise: this physical object/event is too big or absurd to ignore.
- Topic translation: make the abstract result a massive object, destructive
  action, or impossible-looking physical scene.
- One-frame story: an object is about to collide, crush, spill, explode, tower,
  fill, or be won.
- First read: giant physical object or action.
- Second read: subject scale or reaction.
- Text behavior: optional size, price, or arrow.
- Composition: object dominates; subject proves scale.
- Failure mode: static object render with no event.
- Prompt contract: show a physical event, not a prop.

### Paradigm 7: Philanthropic / Transformation Proof
- Evidence count: 8/120 primary assignments.
- Representative samples: 64, 67, 70, 75, 86, 90, 92, 110, 112.
- Best-fit topics: life-change proof, charity, access, rescue, health change,
  education, housing, wells, sensory restoration, animal rescue.
- Click promise: a real life changed visibly.
- Topic translation: convert generosity into before/after or beneficiary proof,
  not a self-congratulatory portrait.
- One-frame story: the beneficiary/result is visible, with the subject as
  witness or helper.
- First read: transformation result or beneficiary scale.
- Second read: subject/beneficiary emotion.
- Text behavior: count, before/after, or no text.
- Composition: result first; giver second.
- Failure mode: fake charity optics or generic smiling portrait.
- Prompt contract: show the impact, not just the gift.

### Paradigm 8: Simple Rule / Choice Object
- Evidence count: 6/120 primary assignments.
- Representative samples: 24, 47, 54, 71, 88, 104.
- Best-fit topics: binary choices, one button, one object to hold, fit-in-shape,
  hit target, keep hand on object, one mystery key.
- Click promise: what happens if this simple rule is followed?
- Topic translation: convert the topic into one rule object.
- One-frame story: subject is one action away from reward/loss.
- First read: button, key, target, shape, hand-on-object rule, or boundary.
- Second read: prize or consequence.
- Text behavior: optional short rule/prize label.
- Composition: rule object large and central.
- Failure mode: rule only explained in title.
- Prompt contract: draw the rule as a physical object or boundary.

## Topic Translation Rules
- First choose the stake type and internal paradigm.
- Abstract topics must become physical stakes: arena, prize, choice, boundary,
  timer, crowd, object, transformation, or consequence.
- Concrete topics should exaggerate one truthful dimension: cost, quantity,
  risk, reward, duration, participant count, physical size, or before/after
  consequence.
- Required translation variables: selected paradigm, visible stake, proof object,
  subject role/action, rule/reward/danger, one-second viewer question, text
  label if needed, and what would be misleading if exaggerated.
- Forbidden moves: fake cash, fake charity, fake danger, fake crowd, AI robot,
  hologram dashboard, flowchart, lecture slide, calm productivity poster,
  product-ad beauty shot, and title-only concept poster.

## Cover Storyboard Rules
- Story moment: freeze the exact instant the stake becomes undeniable: before
  choosing, inside survival, during chase, at prize reveal, after
  transformation, before collision, or when crowd scale is visible.
- Visible conflict: cheap vs expensive, safe vs dangerous, alone vs crowd,
  trapped vs free, before vs after, winner vs loser, small object vs giant scale,
  ordinary action vs absurd reward.
- Subject task/action: survive, choose, hold, run, react, referee, rescue,
  present prize, protect object, trigger machine, stand inside the rule, or
  witness the transformation.
- Proof object: cash, prize, timer, day label, circle, triangle, button, crowd,
  car, island, house, dog, well, bunker, train, target, diamond, danger object,
  or before/after environment.
- Viewer question: "Who wins, can they survive, how different is it, would I do
  this, or is the transformation real?"
- Forbidden static compositions: neutral host pointing at text, feature matrix,
  software dashboard, calm portrait, subtle product display, and abstract
  metaphor object.

## Design Layout Brief Rules
- First read: visible stake.
- Second read: subject action or expression.
- Third read: scale cue, label, timer, prize, danger, or consequence.
- Layout zones: one dominant stake zone, one subject anchor, optional secondary
  consequence zone.
- Visual weight: stake 45-75%; subject 20-45%; labels only as support.
- Reading path: stake -> subject -> consequence/label.
- Negative space: preserve clear room around numeric labels and face.
- Forbidden layouts: many equal panels, three unrelated text blocks, noisy crowd
  without grouping, or small prize hidden behind a face.

## Copy Hierarchy Rules
- Main title: usually not needed inside the image unless user-approved.
- Good text: `$1`, `$100M`, `DAY 100`, `500 PEOPLE`, `BEFORE`, `AFTER`, `#1`,
  `#100`, one prize amount, or one rule label.
- Subtitle: avoid.
- Object/zone binding: labels must sit directly on or beside the thing they
  describe.
- Isolation rules: never let price labels and title merge into a confusing
  sentence.
- Removal rule: if the event is readable without text, remove text.

## Platform Adaptation
| Platform/mode | Ratio | Target canvas | Composition rule |
|---|---:|---:|---|
| YouTube long video | 16:9 | 1280x720 | Native fit: wide stake, large face/action, sparse labels. |
| Bilibili cross-platform | 16:9 | 1920x1080 | Keep face, stake, and labels center-safe; avoid tiny edge text. |
| Bilibili native upload | 1146:717 | 1146x717 | Slightly taller frame; keep rule/prize central. |
| Bilibili 4:3-safe | 4:3 | 1440x1080 | Compress to one subject plus one stake object. |
| Douyin horizontal | 4:3 | 1440x1080 | Use central action and one large label. |
| Douyin vertical | 3:4 | 1080x1440 | Stack subject, stake, and prize/danger. |
| Xiaohongshu | 3:4 | 1080x1440 | Reduce chaos; one large stake and one subject. |
| Xiaohongshu square | 1:1 | 1080x1080 | Center subject and stake; remove side labels. |
| TikTok/Reels/Shorts | 9:16 | 1080x1920 | Vertical action frame; keep face and stake large. |
| WeChat article main | 2.35:1 | 2350x1000 | Use only when the stake remains clear in the central square-safe zone. |

## Layout Patterns
### Pattern 1: Two Extremes
- Use for value ladder and before/after.
- Composition: two endpoints only; subject bridges or reacts.
- Text: one label per endpoint.
- Avoid: multi-step comparison.

### Pattern 2: Contained Survivor
- Use for endurance, isolation, and pressure.
- Composition: subject inside visible container/environment with timer/day label.
- Text: one progress label.
- Avoid: generic drama without a rule.

### Pattern 3: Crowd Arena
- Use for mass competition and people-count tests.
- Composition: grouped crowd plus simple rule/prize.
- Text: count or prize only.
- Avoid: unstructured crowd noise.

### Pattern 4: Prize Reveal
- Use for giveaways and wish fulfillment.
- Composition: prize object dominates, subject validates.
- Text: value label if needed.
- Avoid: luxury mood without a rule.

### Pattern 5: Danger Near Subject
- Use for fear/chase/risk.
- Composition: threat and subject share the same immediate frame.
- Text: reward or danger label only if needed.
- Avoid: vague danger background.

### Pattern 6: Giant Physical Event
- Use for destruction, absurd machines, and massive objects.
- Composition: object/action dominates; subject proves scale.
- Text: arrow, price, or size cue.
- Avoid: static prop render.

### Pattern 7: Transformation Proof
- Use for philanthropy and life-change results.
- Composition: result/beneficiary first, subject second.
- Text: before/after or count.
- Avoid: self-congratulatory portrait.

## Subject Rules
Preserve the user's identity from reference images, but redesign pose and
expression around the stake. Good roles: participant, witness, referee, rescuer,
winner, loser, survivor, prize presenter, or challenger. Good expressions:
surprise, fear, joy, focus, disbelief, urgency, or warm proof for philanthropic
scenes. Avoid detached expert poses, arms-crossed authority, and face-only
thumbnails with no stake.

## Reference Image Handling
Reference images lock user identity, face traits, hair, clothing cues, product
appearance, or brand assets. They do not lock pose, scale, background, or
expression unless explicitly requested. Convert static portraits into event
participation. If no real stake/proof object exists, ask for one or route away.

## Identity And Final Prompt Firewall
- Internal routing may name MrBeast, but the final GPT Image 2 prompt must not
  contain `MrBeast`, `Jimmy Donaldson`, `MrBeast-inspired`, `Jimmy
  Donaldson-inspired`, `in the style of MrBeast`, `like MrBeast`, or equivalent
  creator-name shortcuts.
- Express the pattern through concrete mechanics: visible stakes, price gap,
  endurance container, crowd geometry, prize reveal, danger trial, giant physical
  event, transformation proof, sparse numeric text, and high-contrast commercial
  realism.
- If a portrait reference is supplied, identity preservation outranks all
  creator-pattern rules. The subject must preserve the user's identity traits and
  must not resemble any public creator.

## Text Rules
Use text as stake, not explanation. Good text is a price, count, day/time label,
before/after label, rank, prize amount, or one rule word. Keep it huge,
high-contrast, and isolated. Avoid sentence titles, slogans, thesis claims,
brand-copy paragraphs, and multi-label infographics.

## Typography Layout System
Protected text zones: top corners for price/day labels, before/after headers,
object-bound labels, prize tags, shape labels, or one giant central number.
Typography should be thick, white/yellow/black with strong outline or backing.
When there are multiple labels, use the same style family and keep them bound to
their zones. Delete text before shrinking it.

## Color And Lighting Rules
Use saturated commercial realism. Common color roles: red for rule/danger,
yellow/gold for money/reward, blue sky/water for scale, orange for prison/danger
suits, green for money/grass, black/yellow for hazard, clean white for prize or
medical transformation. Avoid muted editorial palettes, cyberpunk glow, generic
AI purple, and darkness that hides the stake.

## Hook Mechanics
- Price gap creates immediate value curiosity.
- Day/time count makes endurance measurable.
- Crowd geometry makes scale undeniable.
- Prize object creates wish fulfillment.
- Danger object creates risk.
- Giant physical object creates absurd proof.
- Before/after creates transformation belief.
- One rule object creates instant challenge clarity.

## GPT Image 2 Prompt Contract
Every prompt must include:
- target platform, aspect ratio, and exact pixel canvas
- selected internal paradigm
- visible stake and truthful proof object
- subject role/action inside the event
- camera distance and composition pattern
- exact text labels or "no text"
- where each label attaches
- high-contrast commercial realism and color role
- platform crop-safe zones
- explicit rejection of creator likeness, creator names, fake stakes, fake
  charity, and fake danger

## Negative Constraints
No MrBeast likeness replication. No channel logo imitation. No exact thumbnail
recreation. No protected franchise/IP imitation. No fake money, fake charity,
fake danger, fake crowd, or fake prize. No dashboard, workflow diagram, lecture
poster, subtle product ad, calm expert portrait, or abstract AI concept art. No
public creator names in final prompts.

## User Intake Questions
1. 这次真实 stake 是什么：钱、时间、危险、人数、奖品、规则、改造、还是巨大物体？
2. 哪个物体或场景能一眼证明这个 stake？
3. 主体在事件里是什么角色：参与者、见证者、裁判、幸存者、获胜者、失败者、救助者？
4. 封面文字是否只用数字、金额、天数、人数、before/after 或 no text？
5. 哪些夸张会误导观众，必须禁止？

## Quality Checklist
- One internal paradigm is selected before visual style.
- One truthful stake is visible before text.
- The first read is money, rule, danger, prize, crowd, timer, giant object, or
  transformation result.
- Subject is inside the event, not presenting a concept.
- Text is numeric, short, and stake-bound.
- The frame is understandable in one second.
- No fake charity, danger, prize, or crowd.
- Platform ratio and target canvas are explicit.
- Reference image identity is preserved.
- Final prompt avoids creator-name shortcuts and public creator likeness.
