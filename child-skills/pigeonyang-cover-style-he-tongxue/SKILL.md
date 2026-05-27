---
name: pigeonyang-cover-style-he-tongxue
description: "PigeonYang-branded skill that uses the distilled 何同学 video cover and thumbnail design pattern to write GPT Image 2-ready prompts for original user covers. Trigger when the user asks for a cover in 何同学's style, references 何同学 thumbnails, or asks to apply this creator cover formula."
---

# PigeonYang 何同学 Cover Style

## Role

Use this distilled creator-cover pattern to write original, GPT Image 2-ready cover prompts for the user's video.

Do not copy existing 何同学 thumbnails. Apply the transferable design strategy to the user's own topic, brand, face, product, and constraints.

## Identity And Final Prompt Firewall

The distilled creator name is an internal routing and analysis label only.

Never put `何同学`, `何同学-inspired`, `in the style of 何同学`, `like 何同学`, or equivalent creator-name shortcuts in the final GPT Image 2 generation prompt. Rewrite the pattern into concrete design rules: subject role, story moment, proof object, composition, typography, color, lighting, and negative constraints.

If the user supplies a portrait/reference image, that reference controls identity. Preserve the user's face, hair, glasses, clothing cues, body type, and other supplied identity traits. Redesign only the pose/action for the thumbnail hook unless the user explicitly asks to preserve the original pose. The final generation prompt must say the subject must not resemble any public creator, without naming 何同学.

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
14. Save the exact final generation prompt through the mother skill's workflow gate, preferably `scripts/coverctl.py save-final-prompt`, then run `scripts/coverctl.py verify-prompt-firewall` with `何同学` and common aliases passed as `--forbid`. If a portrait/reference image is supplied, require identity-reference handling. Do not generate if the firewall fails.
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

# PigeonYang Cover Design Standard: 何同学

## Scope
Use this standard for covers where the user's topic can honestly show a concrete
proof unit: object, product, interface, experiment, prototype, device state,
physical action, made artifact, behavior result, human-scale test, or visible
data.

Best-fit topics:

- built products, prototypes, tools, rigs, keyboards, desks, devices, apps, or
  visible interfaces
- product reviews where one physical product detail, price, old/new contrast, or
  named object creates curiosity
- real experiments with phones, screens, measurements, people counts, behavior
  data, taste tests, or comparison states
- absurd utility actions where a real object or service is being used, ridden,
  held, tested, opened, or compared
- craft, material, or visual experiments where the made artifact or visual
  effect is itself inspectable

Do not use this standard for abstract essays, broad methodology, conceptual
systems, personal opinions, pure AI workflow explanations, or article-first
knowledge covers unless the user can provide a real object/interface/result,
human experiment, data screen, or physical workflow artifact that truthfully
proves the claim. Do not invent a fake concept machine just to make an abstract
topic look tangible.

Do not copy 何同学's likeness, channel identity, logos, exact thumbnails, or
private studio assets. Use the user's own portrait, product, interface, proof
object, or a neutral subject.

## Evidence Summary
- Cover samples: 30 high-performing public Bilibili covers from `老师好我叫何同学`,
  selected by archived Bilibili API view count from a 35-video candidate pool.
- View range: 33,740,644 to 3,684,554.
- Research run: `he-tongxue/20260527-30-sample-expansion`.
- Process sources: 2 data sources archived in the expansion run; prior media and
  studio-process sources remain in `he-tongxue/20260527-redistill`.
- Confidence: high for product curiosity, prototype/build proof, macro proof
  states, absurd utility action, and measured comparison covers; medium for
  craft/visual experiment and human/mass experiment because those have fewer
  primary assignments; low for abstract topics without real proof.

## Core Design DNA
1. The shared engine is evidence-first curiosity, not a single layout.
2. A high-performing cover shows a concrete proof unit before it explains a
   concept.
3. The proof unit can be an object, screen, product, machine, action, visual
   artifact, behavior result, people-count experiment, or visible data.
4. The subject supports the proof as operator, holder, scale reference, tester,
   witness, rider, presenter, or demonstrator. The subject is not the whole hook.
5. Text is usually proof-bound: screen UI, product name, price, number, binary
   label, object label, or function word.
6. The viewer question is concrete: what is this, how did they build/test it,
   what result did it show, or why is this ordinary thing solved so strangely?
7. If the cover needs a long detached title to explain why it matters, the proof
   unit is not strong enough for this engine.

## Cover Generation Engine
- Engine type: `Evidence-First Curiosity Engine`.
- Viewer decision compressed: "There is a concrete thing, result, action, or
  test here. What is it, how did they make/test it, and why does it matter?"
- Topic-to-cover mechanism: choose the proof unit and internal paradigm first,
  then pick the sharpest evidence frame: macro state, product reveal, built
  object, binary test, price reveal, absurd action, craft spectacle, or
  human-scale experiment.
- Subject role: operator, holder, tester, rider, witness, presenter,
  demonstrator, or scale marker. The face validates reality, authorship, or
  reaction; it does not replace proof.
- Pre-visual decision: decide what real proof can be shown honestly. If the
  answer is only "a metaphorical machine" or "a workflow diagram", reject this
  engine.
- Drift risk: fake concept machines, generic AI dashboards, architecture
  diagrams, SaaS launch posters, text-first authority covers, MrBeast stakes
  without truthful scale, or documentary stills with no inspectable proof.

## Popular Paradigms
### Paradigm 1: Macro Proof State
- Evidence count: 4/30 primary assignments.
- Representative samples: 1, 6, 11, 21.
- Best-fit topics: invisible tech, phone state, UI result, measurements,
  screen-time data, tiny device details, close physical controls.
- Click promise: one close detail proves the whole story.
- Topic translation: convert the topic into a single readable proof state.
- One-frame story: the proof detail is pushed close enough to judge.
- First read: screen, object detail, key, number, UI state, or measured value.
- Second read: hand, device edge, subject blur, or scale cue.
- Text behavior: native screen/object text or one attached label.
- Composition: macro close-up; subject optional and secondary.
- Failure mode: detached headline explains a detail that is not visible.
- Prompt contract: choose the real proof detail before adding title, face, or
  background.

### Paradigm 2: Prototype / Built Object Hero
- Evidence count: 4/30 primary assignments.
- Representative samples: 2, 3, 5, 15.
- Best-fit topics: prototypes, built products, physical rigs, internals,
  assembly, machines, sketches, keyboards, desks, hand-built artifacts.
- Click promise: they actually built this thing.
- Topic translation: convert the topic into one built object, internal reveal,
  process proof, or working rig.
- One-frame story: subject demonstrates, presents, opens, or stands behind the
  object as proof.
- First read: prototype, machine, internal structure, or sketch.
- Second read: subject/hand as operator or scale reference.
- Text behavior: product name, function word, or object-native label.
- Composition: object dominates; subject validates scale or authorship.
- Failure mode: balanced workbench with many small parts and no decisive object.
- Prompt contract: make the built object large enough to prove the claim.

### Paradigm 3: Product Curiosity / Tech Object Reveal
- Evidence count: 8/30 primary assignments.
- Representative samples: 7, 9, 17, 18, 19, 22, 28, plus product-heavy parts of
  sample 3.
- Best-fit topics: product reviews, retro devices, new phones, transparent
  products, AR/VR, price reveals, product identity, favorite-device stories.
- Click promise: this object has a surprising property, price, history, or
  future signal.
- Topic translation: choose the product's curiosity anchor: old/new aura, price,
  transparency, UI implication, form factor, hidden function, or named identity.
- One-frame story: the product is revealed as the object worth inspecting.
- First read: product body, name, price, or impossible-looking feature.
- Second read: subject as witness, holder, or scale cue.
- Text behavior: product name, price, short object label, or no text.
- Composition: product hero, held object, object wall, or clean device lineup.
- Failure mode: generic product ad with no curiosity gap.
- Prompt contract: identify the product curiosity before choosing beauty-shot
  lighting.

### Paradigm 4: Binary / Measured Test
- Evidence count: 3/30 primary assignments.
- Representative samples: 10, 13, 16.
- Best-fit topics: real/fake, fast/slow, old/new, charged/degraded,
  before/after, measured outcomes, comparison experiments.
- Click promise: the visible test decides which side wins.
- Topic translation: convert the topic into two real states that can be judged.
- One-frame story: subject holds or frames two objects/screens toward the viewer.
- First read: two compared proof states.
- Second read: short labels, result cue, or subject action.
- Text behavior: one short label per side, bound to the object/zone.
- Composition: two clear objects or states; not a table or diagram.
- Failure mode: abstract before/after with no real proof objects.
- Prompt contract: use this only when both sides have visible evidence.

### Paradigm 5: Absurd Utility Action
- Evidence count: 7/30 primary assignments.
- Representative samples: 4, 8, 12, 24, 25, 27, 29.
- Best-fit topics: everyday problems solved by strange overbuilt products,
  utility devices, playful services, physical interventions, functional gags.
- Click promise: why did they solve this ordinary problem like that?
- Topic translation: turn the practical benefit into a real action already
  happening.
- One-frame story: subject uses, rides, launches, opens, presses, tastes,
  operates, or tests the invention.
- First read: action or strange utility object.
- Second read: subject role and result cue.
- Text behavior: optional short function label if the action is not self-evident.
- Composition: action frame, not static product render.
- Failure mode: beauty shot of the invention with no visible use.
- Prompt contract: show the object performing its function.

### Paradigm 6: Craft / Visual Experiment
- Evidence count: 3/30 primary assignments.
- Representative samples: 14, 20, 26.
- Best-fit topics: material experiments, animation tricks, time/visual illusions,
  physical craft, made scenes, one-off visual inventions.
- Click promise: this made artifact or visual effect is real enough to inspect.
- Topic translation: convert the topic into a visible material effect, document,
  miniature, or crafted scene.
- One-frame story: the made effect is visible at its most surprising moment.
- First read: visual effect or material artifact.
- Second read: subject, hand, or scale cue proving it was made.
- Text behavior: native document text, short label, or no text.
- Composition: effect/artifact dominates; keep explanation out of frame.
- Failure mode: abstract art poster with no proof of making.
- Prompt contract: make the artifact/effect inspectable, not decorative.

### Paradigm 7: Human / Mass Experiment
- Evidence count: 2/30 primary assignments.
- Representative samples: 23, 30.
- Best-fit topics: people-count experiments, taste tests, behavior research,
  focus tests, surveys, public participation, social proof.
- Click promise: a large human sample produced a result.
- Topic translation: make the participant count, test object, or result surface
  visible.
- One-frame story: people, objects, or repeated test units show scale.
- First read: count/object wall/test setup.
- Second read: subject as organizer, witness, or participant.
- Text behavior: count label, product/test object labels, or no text if the scale
  is self-evident.
- Composition: repeated objects or participants create scale without clutter.
- Failure mode: generic survey infographic or fake crowd.
- Prompt contract: show the human/test scale as physical evidence.

## Topic Translation Rules
- First choose the internal paradigm and proof unit.
- Abstract topics can use this engine only if grounded in a real artifact:
  working interface, generated output, physical prototype, data screen, before/
  after comparison, document pile, human experiment, or visible test.
- Concrete topics should become closer, larger, stranger, more judgeable, more
  product-specific, or more action-driven.
- Required translation variables: selected internal paradigm, proof unit, why it
  is surprising, subject role/action, one-second viewer question, object-bound
  text if needed, and forbidden drift.
- Forbidden translation moves: invented concept machines, floating icons,
  holograms, AI robots, dashboard collages, PPT diagrams, product-ad beauty shots
  without curiosity, and large detached thesis titles.
- Example translation: "AI content flywheel" is rejected unless there is a real
  interface, printed output, physical workflow artifact, measured result, or
  human test to show.

## Cover Storyboard Rules
- Story moment: freeze the instant of proof: the button is pressed, the screen
  shows the result, the product is held up, the machine is opened, two objects
  are compared, the strange invention is being used, or a human-scale test is
  visible.
- Visible conflict: invisible vs visible, real vs fake, fast vs slow, hidden
  internals vs polished product, absurd solution vs ordinary problem, expensive
  number vs object, large sample vs individual opinion, made effect vs ordinary
  scene.
- Subject task/action: hold, point, operate, ride, taste, compare, demonstrate,
  stand above, present a screen, or witness the result.
- Proof object: device state, product body, prototype, UI, price, comparison
  object, artifact, repeated test objects, participant count, document, sketch,
  internal mechanism, or action result.
- Viewer question: "What exactly am I seeing, and why did they do this?"
- Forbidden static compositions: central portrait with title, abstract workflow
  diagram, decorative prototype, UI-card collage, clean metaphor object, or a
  machine that exists only as visual symbolism.
- Example storyboard: a real screen/result/object/test is pushed near the camera;
  the subject is behind or beside it as operator or witness, with one short
  proof-bound label if needed.

## Design Layout Brief Rules
- First read: selected proof unit, product, screen state, comparison, price,
  action, artifact, or human-scale test.
- Second read: subject's action or face confirming use, scale, authorship, or
  result.
- Third read: clue such as number, label, internal mechanism, cable, reflection,
  hand, repeated object, participant count, motion blur, or object label.
- Layout zones: one dominant proof zone; subject behind, beside, above, or
  partially obscured by proof; optional labels bound to proof.
- Visual weight: proof unit 55-85%; subject 10-35%; environment only as context.
- Reading path: proof first, action/face second, clue third.
- Negative space: black studio void, clean wall, screen area, product surface,
  blurred background, or object-native text zone.
- Forbidden layouts: symmetrical article-header diagram, many input/output
  cards, three-column process explanation, decorative flywheel, detached title
  block, and "productivity system" collage.

## Copy Hierarchy Rules
- Main title: usually none. If needed, use one proof-bound phrase, number, price,
  product name, binary label, count, or function word.
- Subtitle: avoid.
- State labels: use only for visible comparison states or test scale, such as
  `快 / 慢`, `真的 / 假的`, `500人`, `1000人`, `自动开灯`, `5G`, `¥49999`, or a
  product name.
- Object/zone binding: text must sit on the screen, product, label plate, or
  directly above the corresponding object/side.
- Isolation rules: labels must be visually fused to their proof through distance,
  color, plate, screen placement, perspective, or repeated-object grouping.
- Forbidden adjacency: never combine a detached main title with object labels so
  the viewer reads a confusing sentence.
- Removal rule: if text explains a concept rather than naming visible proof,
  remove it or route away from this engine.

## Platform Adaptation
| Platform/mode | Ratio | Composition rule |
|---|---:|---|
| YouTube long video | 16:9 | Use wide product/proof composition; one oversized foreground proof and subject behind/side. |
| Bilibili native upload | 1146:717 | Native fit. Keep proof object and key text in center-safe area. |
| Bilibili cross-platform | 16:9 | Keep product/proof large enough for both Bilibili and YouTube feed sizes. |
| Bilibili 4:3-safe | 4:3 | Crop toward proof unit and subject face; remove side labels. |
| Douyin horizontal | 4:3 | Use tighter foreground proof; avoid tiny edge details. |
| Douyin vertical | 3:4 | Stack proof unit and subject action; keep one central label. |
| Xiaohongshu | 3:4 | Use clean product proof, craft artifact, or comparison object; avoid wide machine scenes. |
| Xiaohongshu square | 1:1 | One central proof unit plus hand/face scale; no secondary narrative. |
| TikTok / Reels / Shorts | 9:16 | Use a vertical action moment, screen proof, product hero, or repeated-object test scale. |
| WeChat article main | 2.35:1 | Use only when one proof unit can remain large in the central square-safe zone. Do not turn this into a process diagram. |

## Layout Patterns
### Pattern 1: Macro Proof State
- Use when: one screen, button, key, UI metric, price, or product detail proves
  the hook.
- Composition: extreme close-up; hand/device edge visible; subject optional and
  secondary.
- Text: native screen/object text or one attached label.
- Avoid: explaining the detail with a large floating title.

### Pattern 2: Product / Prototype Hero
- Use when: a product, prototype, rig, or artifact has a visually strange form,
  price, internal structure, or named identity.
- Composition: proof object fills most of frame; subject behind or beside it as
  operator/witness/scale.
- Text: product name, price, function word, or no text.
- Avoid: generic product ad without a curiosity anchor.

### Pattern 3: Binary / Measured Test
- Use when: the story is real/fake, fast/slow, old/new, charged/dead, expensive/
  cheap, visible/invisible, or measured by a real test.
- Composition: subject holds two objects/screens toward camera, or frame splits
  around two real states.
- Text: one short label per object/side.
- Avoid: abstract before/after diagrams with no objects.

### Pattern 4: Absurd Utility Action
- Use when: the object solves an everyday problem in a playful or overbuilt way.
- Composition: action is happening: riding, launching, drinking, opening,
  tasting, testing, pressing, holding, aiming, erasing, or operating.
- Text: optional short function label if the action is not self-evident.
- Avoid: static beauty shot of the invention.

### Pattern 5: Human / Mass Experiment
- Use when: the claim depends on people count, public participation, taste test,
  focus test, or behavior data.
- Composition: repeated people/objects/data create scale; subject organizes or
  witnesses.
- Text: count label or test object label.
- Avoid: fake survey infographic or crowd used only as decoration.

### Pattern 6: Craft / Visual Experiment
- Use when: a made artifact, material effect, animation trick, or visual illusion
  is the click object.
- Composition: effect/artifact dominates; subject or hand proves scale/making.
- Text: native document text or none.
- Avoid: abstract art poster with no proof of making.

## Subject Rules
Preserve the user's identity from reference images, but redesign pose and
expression around the proof action. Good subject roles: holder, operator, tester,
rider, watcher, scale reference, organizer, witness, or demonstrator. Good
expressions: focused curiosity, calm proof, slight mischievous smile, or serious
comparison. Avoid arms-crossed authority, default thinking pose, detached
presenter, and exaggerated shock without object evidence.

## Reference Image Handling
Reference images lock identity, face traits, hair, glasses, clothing cues,
product appearance, interface appearance, or brand assets. They do not lock pose,
crop, lighting, or background unless the user explicitly says so. Convert static
portraits into proof-related interaction. If the user only supplies a portrait
and no real proof object/interface/result/action/test, ask for proof or route to
another engine.

## Identity And Final Prompt Firewall
- Internal routing may name 何同学, but the final GPT Image 2 prompt must not
  contain `何同学`, `He Tongxue`, `何同学-inspired`, `He Tongxue-inspired`, `in
  the style of 何同学`, `like 何同学`, or equivalent creator-name shortcuts.
- Express the pattern through concrete mechanics: evidence-first curiosity,
  selected internal paradigm, dominant proof unit, subject-as-operator/witness,
  proof-bound labels, real product/studio lighting, and specific interaction.
- If a portrait reference is supplied, identity preservation outranks all
  creator-pattern rules. The subject must preserve the user's identity traits and
  must not resemble any public creator.
- Add a final negative constraint that the generated subject must not resemble
  any public creator, without naming 何同学.

## Text Rules
Use text as proof, not explanation. Good text is visible screen state, product
name, price, count, short binary label, function word, object label, or native
document text. Keep Chinese labels short and bold. Avoid article headlines,
slogans, thesis claims, and multi-label process maps. If text could be removed
without weakening the real proof unit, remove it.

## Typography Layout System
Protected text zones are proof-bound: phone screens, device surfaces, giant
product-name overlays on the object, price labels on products, labels above two
compared objects, count labels attached to repeated objects, or native document
text. Use bold, high-contrast, feed-readable type. Backing shapes are allowed
only when they behave like stickers, screens, label plates, or product UI.
When the frame is cluttered, either move text onto the proof unit or remove it.

## Color And Lighting Rules
Use real-camera product or studio lighting. Common palettes: black/white product
contrast, phone-screen blue, red/blue test polarity, yellow utility object,
graphite machinery, transparent product glow, product-native color, or clean
lab/studio light. Saturation can be strong when it belongs to the object or
comparison state. Avoid generic AI purple, cyberpunk glow, fictional holograms,
and soft editorial gradients.

## Hook Mechanics
- A real detail makes invisible technology visible.
- A physical object proves "we built this".
- A product property, price, or name creates curiosity.
- A comparison makes the result instantly judgeable.
- A strange action proves the invention's function.
- A made artifact or visual effect proves craft.
- A people-count test converts opinion into social proof.
- A screen state converts behavior or data into visible proof.

## GPT Image 2 Prompt Contract
Every prompt must include:
- target platform, aspect ratio, and exact pixel canvas
- selected internal paradigm
- the real proof object/interface/result/action/test/person-count to show
- subject role and physical interaction with the proof
- camera distance and perspective: macro close-up, product hero, held-to-camera,
  overhead, oblique internal reveal, action frame, or repeated-object test scale
- exact on-cover text, or "no text"
- where each text element is attached in the proof world
- realistic product/studio lighting and material detail
- platform crop-safe zones
- explicit rejection of fake concept machines, abstract workflow diagrams,
  detached titles, generic AI dashboards, and public creator likeness

## Negative Constraints
No 何同学 likeness replication. No channel logo imitation. No invented concept
machine for abstract topics. No generic AI robot, hologram dashboard, floating
icons, process diagram, article-title poster, text-first authority cover, dense
architecture, or decorative workflow flywheel. No object so small that it only
acts as background decoration. No labels detached from their proof units. No
public creator names in final prompts.

## User Intake Questions
1. 你要发哪个平台？横版、竖版还是都要？
2. 这个主题里真实可展示的物件、界面、数据、实验结果、动作或人群测试是什么？
3. 是否有产品图、界面图、样机图、截图、手稿、输出样例或实拍参考？
4. 这次更适合哪个内部范式：极近证据、样机/产品主角、产品好奇、二元测试、荒诞实用动作、手工视觉实验，还是人群实验？
5. 封面文字是否可以不用完整标题，只保留产品名、数字、价格、状态或功能标签？
6. 如果没有真实证明物，是否改用更适合抽象观点/机制解释的 child skill？

## Quality Checklist
- A selected internal paradigm is named before style is chosen.
- A real proof unit is named before composition.
- The first read is an object, screen, product, comparison, price, action,
  artifact, data, or human-scale test.
- The subject interacts with proof or acts as witness/scale.
- Text is short, proof-bound, and not a detached thesis.
- The frame is not a balanced workflow diagram or concept workbench.
- The proof unit creates a one-second viewer question.
- Platform ratio and target canvas are explicit.
- Reference image preserves identity but not weak source pose.
- Final prompt avoids creator-name shortcuts and public creator likeness.
