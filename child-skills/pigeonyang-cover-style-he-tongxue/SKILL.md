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

Never put `何同学`, `He Tongxue`, `何同学-inspired`, `He Tongxue-inspired`, `in the style of 何同学`, `like 何同学`, or equivalent creator-name shortcuts in the final GPT Image 2 generation prompt. Rewrite the pattern into concrete design rules: subject role, story moment, proof object, composition, typography, color, lighting, and negative constraints.

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
13. Save the exact final generation prompt to a prompt file and run the mother skill's `scripts/verify_prompt_firewall.py` with `何同学`, `He Tongxue`, and common aliases passed as `--forbid`. If a portrait/reference image is supplied, pass `--require-identity-reference`. Do not generate if the script fails.
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

# PigeonYang Cover Design Standard: 何同学

## Scope
Use this standard to create original video covers that apply 何同学's transferable cover logic: make an abstract technology or creator-workflow topic feel like a real built object, prototype, experiment, or visible device state. It is best for topics about technology products, AI workflows, maker projects, experiments, productivity systems, strange utility tools, and "I built this" stories.

Do not copy 何同学's likeness, channel identity, logos, exact thumbnails, or private studio assets. Use the user's own portrait, product, interface, or a neutral subject.

## Evidence Summary
- Cover samples: 15 public Bilibili covers from `老师好我叫何同学`, archived in the managed research run under `covers/`.
- Process sources: 5 archived sources, including Bilibili selected video API data, a Feishu article about 何同学工作室's production system, and media profiles/articles about 何同学, 5G, and AirDesk.
- Research run: `he-tongxue/20260525-203702` in the user's configured research workspace.
- Confidence: High for the "physical proof object / maker demonstrator" engine; medium for exact current studio process because public process sources describe workflow broadly, not a dedicated cover-design manual.

## Core Design DNA
1. Turn the topic into a visible object before designing style: invention, prototype, device, experiment, data screen, product, sketch, or mechanical system.
2. Make the proof object the first read. The viewer should see "there is a real thing here" before reading any title.
3. Use the person as maker, demonstrator, witness, or scale reference; the face supports the object instead of replacing it.
4. Bind text to the object: screen label, product name, comparison tag, price, number, or function word. Avoid long floating titles.
5. Use real-camera studio/product photography: macro detail, wide-angle machine depth, overhead workbench, clean black/white lab backgrounds, and tactile parts.
6. Keep the tone curious, clever, and maker-like. It should feel engineered and slightly romantic, not loud challenge spectacle or pure lecture authority.

## Cover Generation Engine
- Engine type: Hybrid `Utility Clarity Engine` + `Narrative Suspense Engine` + `Aesthetic Identity Engine`.
- Viewer decision compressed: "Is there a real, clever, visually interesting thing here that solves or tests a problem I recognize?"
- Topic-to-cover mechanism: Convert the raw topic into a physical proof object first, then choose the strongest reveal moment: finished prototype, open internals, comparison test, strange action, visible data, hand-drawn plan, or product close-up.
- Subject role: Maker-demonstrator-witness. The subject points, holds, operates, rides, opens, or stands beside the object to prove ownership and scale.
- Pre-visual decision: Decide the one physical proof the viewer can understand in one second. If no object, experiment state, or "we made this" moment exists, redesign the concept before prompting.
- Drift risk: MrBeast extreme stakes, Dan Koe text authority, 影视飓风 cinematic documentary stills, generic AI dashboards, product-ad beauty shots with no maker proof, or abstract icons.

## Topic Translation Rules
- Abstract topics: translate into a buildable or observable thing: a machine, workflow desk, prototype device, robotic rig, physical dashboard, screen array, experiment table, sketch, or before/after data object.
- Concrete topics: make the real object closer, bigger, more interactive, or more mechanically legible through internals, hands, scale, comparison, or screen data.
- Required translation variables: viewer problem, invented solution, proof object, physical form, subject action, one-second mystery, optional object-bound label.
- Forbidden translation moves: floating AI icons, holographic dashboards, cyberpunk robots, PPT diagrams, generic app screenshots, long slogan beside a portrait, or pure aesthetic tech background.
- Example translation: Raw topic "I built a skill that distills any creator's video cover style" becomes "a workbench machine that eats a wall of creator covers and outputs a new approved cover prompt, with the subject operating the machine."

## Cover Storyboard Rules
- Story moment: show the instant the maker reveals, tests, operates, opens, or uses the built thing.
- Visible conflict: everyday problem vs over-engineered solution; real vs fake; slow vs fast; hidden internal mechanism vs polished product; messy input vs clean output.
- Subject task/action: point to the machine, hold two comparison objects, press a button, operate a rig, open internals, ride/use the prototype, or look through/behind the object.
- Proof object: invention, close-up component, experiment array, phone screen, sketch, product name, price label, output sample, or object-bound comparison tags.
- Viewer question: "What is that thing, and why did they build it?"
- Forbidden static compositions: ordinary portrait with pasted title, floating UI collage, text-first poster, beautiful but nonfunctional tech scene, diagram-only frame, or metaphor with no real object.
- Example storyboard: The user's portrait appears at the right edge, one hand operating a white desktop machine; the machine pulls in messy thumbnail cards on the left and ejects one polished cover on the right; a small object-bound label reads `封面机器`.

## Design Layout Brief Rules
- First read: the proof object or the object-bound label.
- Second read: the subject's action, face, or the comparison state.
- Third read: a small clue such as screen data, price, number, product name, sketch detail, or color polarity.
- Layout zones: give 55-75% visual weight to the proof object; place the subject at an edge, behind, above, or between objects as scale/ownership proof.
- Visual weight: object dominates, subject supports, text labels stay short and attached.
- Reading path: object first, action/face second, label/detail third.
- Negative space: use black void, clean workbench, white machine surface, phone-screen area, or simple studio wall to isolate object and labels.
- Forbidden layouts: central portrait plus title, three unrelated props, floating slogan, dashboard collage, decorative icon field, or object so small that it becomes background decoration.

## Copy Hierarchy Rules
- Main title: usually no full sentence. If text is needed, use one product name, function word, number, price, or binary state label.
- Subtitle: usually none. Let the video title outside the image carry nuance.
- State labels: only when the image truly compares states or objects, such as `快充/慢充`, `真的/假的`, `自动开灯`, `¥49999`, `输入/输出`.
- Object/zone binding: every label must attach to a screen, product surface, side of a comparison, or clean label plate near the object.
- Isolation rules: keep each label visually connected to its object with distance, color, screen placement, or backing plate.
- Forbidden adjacency: never place object labels near a main title where they read as one accidental sentence.
- Removal rule: if text competes with the proof object, remove the lower-priority text and make the object/action carry the meaning.

## Platform Adaptation
| Platform/mode | Ratio | Composition rule |
|---|---:|---|
| YouTube long video | 16:9 | Use native wide product-proof composition: large object across 55-75%, subject at edge or behind object. |
| Bilibili native upload | 1146:717, approx 16:10 | Keep the proof object and subject inside a center-safe wide frame; avoid edge-critical labels. |
| Bilibili cross-platform | 16:9 | Use clean wide composition; keep object label readable at feed size. |
| Bilibili 4:3-safe | 4:3 | Move subject closer to object, reduce side spread, and keep labels central. |
| Douyin horizontal | 4:3 | Compress wide machinery into a tighter workbench or two-object comparison; avoid tiny side details. |
| Douyin vertical | 3:4 | Stack object and face vertically; keep the proof object large in the center or lower center, with one short label. |
| Xiaohongshu | 3:4 | Use a cleaner maker-product card: object hero, subject edge, minimal label. |
| Xiaohongshu square | 1:1 | Use one central object plus face/hand as scale; remove secondary details. |
| TikTok / Reels / Shorts | 9:16 | Use vertical poster logic only if the user asks for a short-video frame; keep object and label central. |

## Layout Patterns
### Pattern 1: Built Thing Reveal
- Use when: the title says "I built/made a tool, machine, product, or workflow."
- Composition: large device or prototype in foreground/middle, subject at right/behind/above, hand operating or pointing.
- Text: optional product name or function label attached to the device.
- Avoid: portrait plus slogan, icon metaphor, clean app mockup with no physical proof.

### Pattern 2: Experiment Comparison
- Use when: the topic tests two states, methods, products, or outcomes.
- Composition: subject centered or slightly behind two objects; labels sit on each object or side.
- Text: two short object-bound labels, balanced in size and color.
- Avoid: floating before/after labels detached from the proof objects.

### Pattern 3: Macro Proof Detail
- Use when: one detail proves the whole topic, such as a screen, status, mechanical part, sketch, keyboard, or UI metric.
- Composition: extreme close-up, hands or finger for interaction, shallow depth.
- Text: none unless it appears naturally on the screen/object.
- Avoid: explaining the detail with long overlay text.

### Pattern 4: Absurd Utility Action
- Use when: the topic solves an everyday pain in a playful or over-engineered way.
- Composition: subject actively uses the prototype; motion or awkward physicality proves the function.
- Text: optional short function label.
- Avoid: static product shot that hides the absurd action.

## Subject Rules
Preserve the user's identity from reference images, but redesign pose and expression around the prototype. Preferred expressions are focused curiosity, maker confidence, subtle smile, or calm seriousness. Preferred actions are presenting, pointing, holding, operating, opening internals, using, riding, or comparing. Avoid default thinking poses, influencer poses, crossed-arm authority, or exaggerated shock without a proof object.

## Reference Image Handling
Reference images lock identity traits, face traits, hairstyle, clothing preference, product/interface appearance, or brand assets. They do not lock pose, expression, crop, lighting, or background unless the user explicitly says so. For this pattern, convert a static portrait into an active maker-demonstrator moment. The final image subject must resemble the user's supplied reference and must not resemble any public creator.

## Identity And Final Prompt Firewall

- Internal skill routing may name 何同学, but the final GPT Image 2 prompt must not contain `何同学`, `He Tongxue`, `何同学-inspired`, `He Tongxue-inspired`, `in the style of 何同学`, `like 何同学`, or any equivalent creator-name shortcut.
- Express the pattern through concrete cover mechanics: real physical proof object, maker-demonstrator subject role, object-bound short label, product/studio photography, visible mechanism, and clean black/white lab environment.
- If a portrait reference is supplied, identity preservation outranks all creator-pattern rules. The subject must preserve the user's face, hair, glasses, clothing cues, body type, and supplied identity traits.
- Add a negative constraint that the generated subject must not resemble any public creator, without naming 何同学 in the final prompt.

## Text Rules
Use clean, heavy sans-serif Chinese or Latin text only when it behaves like product typography, screen UI, price, number, or comparison label. Keep text short and object-bound. A good label is usually 1-4 Chinese characters or one product name. Do not use long title blocks unless the visual proof cannot be understood without one.

## Typography Layout System
Protected text zones are object-bound zones: phone screens, device surface, label plate above an object, white machine surface, or clean negative space next to the proof object. Use thick white text for product names on dark machinery, red/blue for binary tests, pink/white outlines for playful real/fake app comparisons, and price/number labels only when they are part of the hook. If background is busy, move the label onto the screen/object or create a clean plate.

## Color And Lighting Rules
Use clean black, white, graphite, lab gray, metal, glass, phone-screen glow, and product-specific accents. Good accent colors: cyan/blue, red, yellow, pink, or one strong object color. Use realistic studio/product lighting, crisp highlights, high local contrast, controlled shadows, and real-camera depth. Avoid generic neon AI purple-blue, cyberpunk glow, flat vector art, or cartoon saturation.

## Hook Mechanics
- "I/we made this": a real thing exists.
- Everyday problem becomes an oddly specific device.
- Product internals or prototype process reveal the hidden work.
- Real vs fake, fast vs slow, or old vs new comparison.
- Visible experiment proof: time, quantity, price, data, screen state, or repeated objects.
- Absurd utility: the invention looks slightly unnecessary but undeniably tangible.

## GPT Image 2 Prompt Contract
Every prompt must include:
- target platform, aspect ratio, and exact pixel canvas
- exact approved on-cover text, or "no text"
- one-sentence topic translation into a physical proof object
- proof object description with physical parts, materials, scale, and interaction
- subject placement, action, and expression
- object-bound typography location and hierarchy
- camera perspective: macro, wide-angle, overhead, product hero, or comparison
- real-camera studio/product lighting
- platform crop-safe zones
- negative constraints against copied 何同学 likeness, generic AI visuals, text-first posters, weak object proof, and detached labels

## Negative Constraints
No 何同学 likeness replication. No Bilibili logo imitation unless the user owns/provides it. No MrBeast challenge stakes, no Dan Koe text-first authority cover, no 影视飓风 cinematic documentary still as the main frame. No generic AI robot, hologram dashboard, floating icons, long slogan beside a portrait, unbuilt-looking fantasy machine, tiny unreadable labels, or labels detached from their objects.

## User Intake Questions
1. 你要发哪个平台？横版、竖版还是都要？
2. 原始标题或视频主题是什么？
3. 是否允许我把封面文字改短？如果允许，我会先给候选文案让你确认。
4. 是否放你的真人形象、产品图、界面图或其他参考图？
5. 这个主题要做成机器、实验、产品、工具、屏幕、对比，还是让我先翻译成一个可视化物件？
6. 有哪些必须出现或必须避免的物件、品牌、文案、颜色？

## Quality Checklist
- The raw topic has been translated into a physical proof object.
- The proof object is the first read.
- The subject has an active maker-demonstrator role, not a passive portrait pose.
- Any text is short, approved, and object-bound.
- No text block can be misread as part of another text block.
- The frame looks like real product/studio photography, not illustration or cyberpunk AI art.
- The object includes physical details that make it believable.
- Platform ratio and target canvas are explicit.
- Reference image preserves identity but not weak source pose.
- The concept avoids copying 何同学's likeness, logos, and exact existing covers.
