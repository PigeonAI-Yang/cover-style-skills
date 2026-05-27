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
Use this standard for covers where the user's topic already has, or can honestly
show, a real object, product, interface, experiment, prototype, device state,
physical action, or hand-built artifact.

Best-fit topics:

- built products, prototypes, tools, rigs, keyboards, desks, devices, apps, or
  visible interfaces
- real experiments with phones, screens, measurements, prices, quantities, or
  comparison states
- product reviews where one physical product detail or price creates curiosity
- absurd utility actions where a real object is being used, ridden, held, tested,
  opened, or compared

Do not use this standard for abstract essays, broad methodology, conceptual
systems, personal opinions, pure AI workflow explanations, or article-first
knowledge covers unless the user can provide a real object/interface/result that
truthfully proves the claim. Do not invent a fake concept machine just to make an
abstract topic look tangible.

Do not copy 何同学's likeness, channel identity, logos, exact thumbnails, or
private studio assets. Use the user's own portrait, product, interface, or a
neutral subject.

## Evidence Summary
- Cover samples: 15 public Bilibili covers from `老师好我叫何同学`, re-audited in
  `research-runs/he-tongxue/20260527-redistill`.
- Process sources: 5 archived sources reused from the managed research workspace,
  including selected Bilibili API data, a Feishu article about the studio system,
  and media profiles around 5G, AirDesk, and creator influence.
- Research run: `he-tongxue/20260527-redistill`.
- Confidence: high for object-first, experiment-first, and comparison covers;
  medium for broad studio-process inference; low for applying this engine to
  abstract article concepts without real visible evidence.

## Core Design DNA
1. The cover is a one-frame proof, not a conceptual poster.
2. One real object, screen, product, experiment state, sketch, or action must
   dominate the viewer's first read.
3. The frame should make the viewer ask: "What is this real thing, and what did
   they do with it?"
4. The subject supports the proof as operator, holder, scale reference, tester,
   or demonstrator. The subject is not the whole hook.
5. Text is usually embedded in the object world: screen UI, product name, price,
   binary labels, huge object-bound words, or natural writing on a sketch.
6. Strong covers often use one of four devices: extreme close-up, oversized
   physical object, binary comparison, or absurd action.
7. The image can be clean, but it should not be tasteful emptiness. It needs one
   tactile, specific, slightly strange proof detail.
8. If the picture needs a long title to explain why it matters, the visual proof
   is not strong enough for this engine.

## Cover Generation Engine
- Engine type: `One-Frame Proof Engine` with `Utility Clarity` and `Curiosity
  Gap` support.
- Viewer decision compressed: "There is a real thing here. What is it, why did
  they build/test it, and what happens if I click?"
- Topic-to-cover mechanism: identify the single visible proof unit first, then
  choose the sharpest evidence frame: macro device state, hand interaction,
  product internals, binary test, price reveal, impossible-looking object, or
  motion/action use.
- Subject role: operator, holder, tester, rider, witness, or scale marker. The
  subject's face should validate that the object/action is real, not replace the
  object.
- Pre-visual decision: decide what real proof can be photographed or simulated
  honestly. If the answer is only "a metaphorical machine" or "a workflow
  diagram", reject this engine.
- Drift risk: fake concept machines, generic AI dashboards, architecture diagrams,
  SaaS launch posters, Dan Koe text-first claims, MrBeast stakes, or cinematic
  documentary stills.

## Popular Paradigms
### Paradigm 1: Macro Proof State
- Evidence count: baseline support from the current 15-cover redistill sample;
  exact frequency pending expanded audit.
- Representative samples: 5G status bar, typewriter key close-up, screen-time
  UI, price/product detail.
- Best-fit topics: screen states, device details, measurable product facts,
  prices, UI proof, small mechanisms.
- Click promise: "This one visible detail proves the invisible technology or
  result."
- Topic translation: convert the topic into one close-up proof state.
- One-frame story: the proof detail is pushed close enough to judge.
- First read: screen/object/detail.
- Second read: hand, device edge, or subject scale.
- Text behavior: native screen/object text or one attached label.
- Composition: macro close-up with optional secondary subject.
- Failure mode: floating headline explaining a detail that is not visible.
- Prompt contract: choose the real proof detail before adding subject or title.

### Paradigm 2: Oversized Object Demonstration
- Evidence count: baseline support from the current 15-cover redistill sample;
  exact frequency pending expanded audit.
- Representative samples: self-typing keyboard, AirDesk, assembly-line machine,
  large device/product builds.
- Best-fit topics: prototypes, built products, physical rigs, strange device
  scale, productized experiments.
- Click promise: "They actually built a strange thing."
- Topic translation: convert the topic into one physically large or visually
  strange object.
- One-frame story: subject demonstrates or stands behind the object as proof.
- First read: oversized object.
- Second read: subject/operator.
- Text behavior: product name, price, or function word attached to object.
- Composition: object fills most of frame; subject validates scale.
- Failure mode: balanced workbench with many small parts.
- Prompt contract: make the object dominant enough to prove the build.

### Paradigm 3: Binary Test
- Evidence count: baseline support from the current 15-cover redistill sample;
  exact frequency pending expanded audit.
- Representative samples: phone fast/slow, fake/real app, visible/invisible or
  charged/degraded comparison states.
- Best-fit topics: before/after, real/fake, old/new, fast/slow, expensive/cheap,
  measured tests.
- Click promise: "Which side is true or better?"
- Topic translation: convert the topic into two real states that can be judged.
- One-frame story: subject holds or frames two objects/screens toward the viewer.
- First read: the two proof states.
- Second read: short labels or subject action.
- Text behavior: one short object-bound label per side.
- Composition: two clear objects or states, not a table.
- Failure mode: abstract comparison diagram with no real objects.
- Prompt contract: only use this when both states have visible proof.

### Paradigm 4: Absurd Utility Action
- Evidence count: baseline support from the current 15-cover redistill sample;
  exact frequency pending expanded audit.
- Representative samples: water utility object, powered chair, cow-service
  intervention, overbuilt everyday solution.
- Best-fit topics: playful utility, everyday problem solved by a strange object,
  action-driven invention.
- Click promise: "Why did they solve this ordinary problem in such an overbuilt
  way?"
- Topic translation: convert utility into a real action already happening.
- One-frame story: subject uses, rides, launches, opens, presses, or tests the
  invention.
- First read: action.
- Second read: strange object.
- Text behavior: optional short function label.
- Composition: action frame, not beauty shot.
- Failure mode: static product render with no use.
- Prompt contract: show the object performing its function.

### Paradigm 5: Internal Reveal
- Evidence count: baseline support from the current 15-cover redistill sample;
  exact frequency pending expanded audit.
- Representative samples: AirDesk internals, sketch plan, transparent TV,
  assembly and wiring views.
- Best-fit topics: hidden mechanisms, product internals, making process, design
  proof, transparent or opened devices.
- Click promise: "What is inside this thing, and how did they make it work?"
- Topic translation: convert the topic into an opened, sketched, transparent, or
  partially assembled proof.
- One-frame story: the object is opened or revealed at the moment of proof.
- First read: internal structure.
- Second read: subject/hand/label as witness.
- Text behavior: product name or one large object-bound label.
- Composition: overhead or oblique internal reveal.
- Failure mode: generic exploded-view diagram.
- Prompt contract: reveal real structure, not a decorative diagram.

## Topic Translation Rules
- Abstract topics: use this engine only if they can be grounded in a real
  artifact: a working interface, an actual generated output, a physical prototype,
  a measurement screen, a before/after comparison, a real document pile, or a
  visible test. If not, route to another child skill.
- Concrete topics: push the real object closer, larger, stranger, more readable,
  or more testable. Show hand, face, scale, screen state, price, internals, or
  motion.
- Required translation variables: real proof unit, why it is surprising, subject
  interaction, one-second viewer question, object-bound text if needed, and what
  must stay out of frame.
- Forbidden translation moves: inventing a decorative machine for an abstract
  system, floating icons, holograms, AI robots, dashboard collages, PPT diagrams,
  product-ad beauty shots without use, and large detached thesis titles.
- Example translation: "I built a keyboard that types itself" becomes a huge
  keyboard close to the camera, a finger pressing one key, and the subject's face
  behind it. "AI content flywheel" is rejected unless there is a real interface,
  printed output, or physical workflow artifact to show.

## Cover Storyboard Rules
- Story moment: freeze the instant of proof: the button is being pressed, the
  screen shows the result, the product is held up, the machine is opened, two
  objects are compared, or the strange invention is being used.
- Visible conflict: real vs fake, fast vs slow, hidden internals vs polished
  product, absurd solution vs ordinary problem, expensive number vs object,
  invisible function vs visible proof.
- Subject task/action: hold two objects toward the camera, point at an oversized
  device, operate a control, ride/use the invention, stand above a product, or
  present a screen close to the lens.
- Proof object: phone status bar, huge keyboard, AirDesk internals, typewriter
  keys, assembly line, phone comparison, screen-time UI, fake app, light device,
  sketch plan, powered chair, cow service device, transparent TV, price tag.
- Viewer question: "What exactly am I seeing, and why did they do this?"
- Forbidden static compositions: balanced concept workbench, central portrait
  with title, abstract workflow diagram, decorative prototype, UI-card collage,
  clean metaphor object, or a machine that exists only as visual symbolism.
- Example storyboard: a real screen/result is pushed near the camera; the subject
  is slightly behind it, focused on the proof, with one short label on the screen
  or beside the object.

## Design Layout Brief Rules
- First read: the proof object, screen state, comparison label, product name, or
  price.
- Second read: the subject's action or face confirming use/scale.
- Third read: one clue such as a number, internal mechanism, small sketch mark,
  cable, reflection, hand, motion blur, or object label.
- Layout zones: use one dominant foreground proof zone. Put the subject behind,
  beside, above, or partially obscured by the object.
- Visual weight: proof object 60-85%; subject 10-35%; background mostly
  isolation. Avoid equal-weight panels.
- Reading path: object first, action/face second, clue third.
- Negative space: black studio void, clean wall, blurred background, product
  surface, or empty screen area used to isolate the proof.
- Forbidden layouts: symmetrical article-header diagram, many input/output cards,
  three-column process explanation, decorative flywheel, detached title block,
  and "productivity system" collage.

## Copy Hierarchy Rules
- Main title: usually none. If needed, use one object-bound phrase, price, number,
  product name, binary label, or function label.
- Subtitle: avoid.
- State labels: use only for visible comparison states, such as `快 / 慢`, `真的 /
  假的`, `自动开灯`, `5G`, `¥49999`, or a product name.
- Object/zone binding: text must sit on the screen, product, label plate, or
  directly above the corresponding object/side.
- Isolation rules: labels must be visually fused to their object through distance,
  color, plate, screen placement, or perspective.
- Forbidden adjacency: never combine a detached main title with object labels so
  the viewer reads a confusing sentence.
- Removal rule: if text explains a concept rather than naming visible proof,
  remove it or route away from this engine.

## Platform Adaptation
| Platform/mode | Ratio | Composition rule |
|---|---:|---|
| YouTube long video | 16:9 | Use wide product-proof composition; one oversized foreground object and subject behind/side. |
| Bilibili native upload | 1146:717 | Native fit. Keep proof object and key text in center-safe area. |
| Bilibili cross-platform | 16:9 | Keep the object large enough for both Bilibili and YouTube feed sizes. |
| Bilibili 4:3-safe | 4:3 | Crop toward proof object and subject face; remove side labels. |
| Douyin horizontal | 4:3 | Use tighter foreground proof; avoid tiny edge details. |
| Douyin vertical | 3:4 | Stack proof object and subject action; keep one central label. |
| Xiaohongshu | 3:4 | Use clean product proof or comparison object, not a wide machine scene. |
| Xiaohongshu square | 1:1 | One central object plus hand/face scale; no secondary narrative. |
| TikTok / Reels / Shorts | 9:16 | Use a vertical action moment or screen proof; avoid wide workbench logic. |
| WeChat article main | 2.35:1 | Use only when a single proof object can remain large in the central square-safe zone. Do not turn this into a process diagram. |

## Layout Patterns
### Pattern 1: Macro Proof State
- Use when: one screen, button, key, UI metric, price, or product detail proves
  the hook.
- Composition: extreme close-up; hand or device edge visible; subject optional
  and secondary.
- Text: native screen/object text or one attached label.
- Avoid: explaining the detail with a large floating title.

### Pattern 2: Oversized Object Demonstration
- Use when: a real prototype or product has a visually strange scale or form.
- Composition: object fills most of the frame; subject behind or beside it as
  operator/scale.
- Text: product name, price, or function word attached to object.
- Avoid: balanced workbench layouts and tiny object proof.

### Pattern 3: Binary Test
- Use when: the story is real/fake, fast/slow, old/new, charged/dead, expensive/
  cheap, visible/invisible.
- Composition: subject holds two objects/screens toward the camera, or the frame
  splits around two real states.
- Text: one short label per object/side.
- Avoid: abstract before/after diagrams with no objects.

### Pattern 4: Absurd Utility Action
- Use when: the object solves an everyday problem in a playful or overbuilt way.
- Composition: action is already happening: riding, launching, drinking, opening,
  testing, pressing, holding, or chasing.
- Text: optional short function label if the action is not self-evident.
- Avoid: static beauty shot of the invention.

### Pattern 5: Internal Reveal
- Use when: internals, wiring, sketches, assembly, or transparent structure are
  the surprising proof.
- Composition: overhead or oblique view; internal parts are readable; subject is
  witness or scale.
- Text: product name or one large label can overlay the object if it behaves like
  product typography.
- Avoid: generic exploded-view diagram.

## Subject Rules
Preserve the user's identity from reference images, but redesign pose and
expression around the proof action. Good subject roles: holder, operator, tester,
rider, watcher, scale reference. Good expressions: focused curiosity, calm proof,
slight mischievous smile, or serious comparison. Avoid arms-crossed authority,
default thinking pose, detached presenter, and exaggerated shock without object
evidence.

## Reference Image Handling
Reference images lock identity, face traits, hair, glasses, clothing cues,
product appearance, interface appearance, or brand assets. They do not lock pose,
crop, lighting, or background unless the user explicitly says so. For this
engine, convert static portraits into an active object interaction. If the user
only supplies a portrait and no real proof object/interface/result, ask for proof
or route to another engine.

## Identity And Final Prompt Firewall
- Internal routing may name 何同学, but the final GPT Image 2 prompt must not
  contain `何同学`, `He Tongxue`, `何同学-inspired`, `He Tongxue-inspired`, `in
  the style of 何同学`, `like 何同学`, or equivalent creator-name shortcuts.
- Express the pattern through concrete mechanics: one-frame proof, oversized
  object or screen, subject-as-operator, object-bound labels, realistic product
  lighting, and specific interaction.
- If a portrait reference is supplied, identity preservation outranks all
  creator-pattern rules. The subject must preserve the user's identity traits and
  must not resemble any public creator.
- Add a final negative constraint that the generated subject must not resemble
  any public creator, without naming 何同学.

## Text Rules
Use text as proof, not explanation. Good text is a visible screen state, product
name, price, short binary label, or function word. Keep Chinese labels short and
bold. Avoid article headlines, slogans, thesis claims, and multi-label process
maps. If the text could be removed without weakening the real object, remove it.

## Typography Layout System
Protected text zones are object-bound: phone screens, device surfaces, giant
product-name overlays on the object, price labels on a product, or labels above
two compared objects. Use bold, high-contrast, feed-readable type. Backing shapes
are allowed only when they behave like stickers, screens, or label plates.
When the frame is cluttered, either move text onto the object/screen or remove it.

## Color And Lighting Rules
Use real-camera product or studio lighting. Common palettes: black/white product
contrast, phone-screen blue, red/blue test polarity, yellow utility object,
graphite machinery, transparent product glow. Saturation can be strong when it
belongs to the product or comparison state. Avoid generic AI purple, cyberpunk
glow, fictional holograms, and soft editorial gradients.

## Hook Mechanics
- A real detail makes an invisible technology visible.
- A physical object proves "we built this".
- A comparison makes the result instantly judgeable.
- A price or number creates a concrete curiosity gap.
- A strange action proves the invention's function.
- Internal structure shows hidden effort and credibility.
- A screen state converts behavior or data into visible proof.

## GPT Image 2 Prompt Contract
Every prompt must include:
- target platform, aspect ratio, and exact pixel canvas
- the real proof object/interface/result to show
- subject role and physical interaction with the proof
- camera distance and perspective: macro close-up, held-to-camera, overhead,
  oblique internal reveal, or action frame
- exact on-cover text, or "no text"
- where each text element is attached in the object world
- realistic product/studio lighting and material detail
- platform crop-safe zones
- explicit rejection of fake concept machines, abstract workflow diagrams,
  detached titles, generic AI dashboards, and public creator likeness

## Negative Constraints
No 何同学 likeness replication. No channel logo imitation. No invented concept
machine for abstract topics. No generic AI robot, hologram dashboard, floating
icons, process diagram, article-title poster, text-first authority cover, dense
architecture, or decorative workflow flywheel. No object so small that it only
acts as background decoration. No labels detached from their objects. No public
creator names in final prompts.

## User Intake Questions
1. 你要发哪个平台？横版、竖版还是都要？
2. 这个主题里真实可展示的物件、界面、数据、实验结果是什么？
3. 是否有产品图、界面图、样机图、截图、手稿、输出样例或实拍参考？
4. 封面文字是否可以不用完整标题，只保留产品名、数字、价格或状态标签？
5. 你希望画面是极近景、手持对比、产品内构、动作瞬间，还是屏幕证据？
6. 如果没有真实证明物，是否改用更适合抽象观点/机制解释的 child skill？

## Quality Checklist
- A real proof unit is named before style is chosen.
- The first read is an object, screen, product, comparison, price, or action.
- The subject is physically interacting with proof or acting as scale.
- Text is short, object-bound, and not a detached thesis.
- The frame is not a balanced workflow diagram or concept workbench.
- The object/action creates a one-second viewer question.
- Platform ratio and target canvas are explicit.
- Reference image preserves identity but not weak source pose.
- Final prompt avoids creator-name shortcuts and public creator likeness.
