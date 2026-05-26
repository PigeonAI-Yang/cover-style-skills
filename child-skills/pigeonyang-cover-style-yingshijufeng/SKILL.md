---
name: pigeonyang-cover-style-yingshijufeng
description: "PigeonYang-branded skill that uses the distilled 影视飓风 video cover and thumbnail design pattern to write GPT Image 2-ready prompts for original user covers. Trigger when the user asks for a cover in 影视飓风's style, references 影视飓风 thumbnails, or asks to apply this creator cover formula."
---

# PigeonYang 影视飓风 Cover Style

## Role

Use this distilled creator-cover pattern to write original, GPT Image 2-ready cover prompts for the user's video.

Do not copy existing 影视飓风 thumbnails. Apply the transferable design strategy to the user's own topic, brand, face, product, and constraints.

## Identity And Final Prompt Firewall

The distilled creator name is an internal routing and analysis label only.

Never put `影视飓风`, `影视飓风-inspired`, `in the style of 影视飓风`, `like 影视飓风`, or equivalent creator-name shortcuts in the final GPT Image 2 generation prompt. Rewrite the pattern into concrete design rules: subject role, story moment, proof object, composition, typography, color, lighting, and negative constraints.

If the user supplies a portrait/reference image, that reference controls identity. Preserve the user's face, hair, glasses, clothing cues, body type, and other supplied identity traits. Redesign only the pose/action for the thumbnail hook unless the user explicitly asks to preserve the original pose. The final generation prompt must say the subject must not resemble any public creator, without naming 影视飓风.

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
13. Save the exact final generation prompt to a prompt file and run the mother skill's `scripts/verify_prompt_firewall.py` with `影视飓风` and common aliases passed as `--forbid`. If a portrait/reference image is supplied, pass `--require-identity-reference`. Do not generate if the script fails.
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

# PigeonYang Cover Design Standard: 影视飓风

## Scope

Use this standard for original covers that should feel like 影视飓风's public-facing cover logic: cinematic documentary access, hard-core topics wrapped in a clickable shell, real-world proof objects, restrained but bold Bilibili typography, and host-as-guide credibility.

Do not use it to copy Tim's likeness, the 影视飓风 logo, exact covers, exact recurring layouts, or protected material. Do not use it when the user's content is pure entertainment challenge, SaaS feature marketing, course selling, or abstract business diagrams unless the topic can truthfully become a real-world proof scene.

## Evidence Summary

- Cover samples: 12 main-account Bilibili covers archived in the managed research workspace for run `yingshijufeng/20260525-053030`.
- Process sources: 6 saved process/data sources archived in the managed research workspace for run `yingshijufeng/20260525-053030`.
- Research run: `yingshijufeng/20260525-053030`.
- Confidence: high for shell-first topic packaging, cinematic proof objects, short Bilibili text, host-as-guide role, and documentary/tech hybrid. Medium for exact top-video ranking because direct Bilibili space API was blocked and a public dashboard API was used.

## Core Design DNA

1. Start from a clickable public shell, not from the technical nucleus.
2. Make the shell visible as a real person, place, object, number, taboo, famous name, strange question, or proof scene.
3. Make the cover feel like a real frame from a documentary, experiment, interview, trip, or industry visit.
4. Use the host as guide, witness, tester, presenter, or participant; not as a detached influencer face.
5. Keep on-cover text short: one noun, number, name, question marker, or proof label.
6. Combine cinematic realism with phone-readable Bilibili typography.
7. Let image evidence carry the premise whenever possible.

## Cover Generation Engine

- Engine type: `Shell-Theory Documentary Engine`, a hybrid of `Narrative Suspense Engine`, `Utility Clarity Engine`, and `Authority/Proof Engine`.
- Viewer decision compressed: "Is this real, unusual, useful, hidden, or credible enough that I want to see what they found?"
- Topic-to-cover mechanism: convert the raw topic into a public-facing shell, then prove that shell with one visible object, person, place, number, or scene.
- Subject role: host/witness/guide/tester/presenter; guest as authority proof; object/location as evidence.
- Pre-visual decision: choose the shell and proof object before choosing composition or style.
- Drift risk: if the cover becomes a MrBeast extreme challenge, SaaS dashboard, lecture slide, flowchart, generic tech poster, or clean product ad, it has left the 影视飓风 engine.

## Topic Translation Rules

- Abstract topics: wrap them in a public shell and a visible proof scene. The shell can be a question, hidden world, person, object, number, location, or unsettling result.
- Concrete topics: dramatize the real proof without faking spectacle. Show the device, place, guest, money amount, data object, animal/person, or physical test.
- Technical topics: use real screens, machines, rooms, devices, tests, or controlled lab scenes; avoid generic neon AI.
- Social topics: use documentary atmosphere, real environment, human silhouette, taboo/hidden-world text, or a serious proof object.
- Interview/person topics: guest face or name is the proof object; host appears as companion/witness.
- Required translation variables: raw topic, hard-core nucleus, public shell, proof object, host role, one-frame question, exact short on-cover text.
- Forbidden translation moves: pure abstract metaphor, dense explanatory poster, fake luxury, random dramatic background, MrBeast-style cash spectacle, and full-title text pasted onto the image.
- Example translation: "AI content flywheel" should not become a flowchart. It should become "AI正在改变内容生产" as the shell, with a real studio/lab, screens, machines, scripts/cards, and the host witnessing or operating the system.

## Cover Storyboard Rules

- Story moment: show the second where the viewer can tell the creator really went there, tested it, met them, found it, or built it.
- Visible conflict: hidden truth, strange rule, expensive object, industry secret, test result, surprising age/result, new technology, or impossible-looking place.
- Subject task/action: the host points, holds proof, reacts, operates equipment, stands inside the place, presents the object, or compares with a guest.
- Proof object: phone screen, location, guest, machine, money tag, room, building, animal, industrial site, data screen, or physical artifact.
- Viewer question: "What did they see?", "How does this work?", "Is it real?", "Why is this place/person/object special?", "What is behind it?"
- Forbidden static compositions: no calm presenter beside a large title, no pure PPT comparison, no diagram, no generic SaaS UI, no unrelated face pasted over a decorative background.
- Example storyboard: the user stands in a real studio/control room, holding or pointing to a physical proof object while the background reveals the hidden system or strange result.

## Design Layout Brief Rules

- First read: the shell or proof object, often a large word, number, name, question marker, or visually shocking scene.
- Second read: host/guest face or body action.
- Third read: environment detail that proves the story.
- Layout zones: one dominant proof zone; one host/guest zone; one protected text zone; one contextual environment zone.
- Visual weight: proof object and host/guest face must read at phone size. Text is bold but sparse.
- Reading path: shell/proof text -> host/guest action -> environment clue -> unresolved question.
- Negative space: use sky, wall, screen, dark street, blurred background, or clean plate behind text.
- Forbidden layouts: no three equal text blocks, no crowded labels, no accidental phrase joining, no tiny subtitle, no pure left/right comparison unless the content is truly a direct test.

## Copy Hierarchy Rules

- Main title: one short shell phrase, noun, number, guest name, object label, or question marker.
- Subtitle: usually none.
- State labels: optional and lower priority; use only when bound to the object/person/zone they describe.
- Object/zone binding: number labels attach to money/device/phone/result; name labels attach to guest; question marks attach to strange place/object.
- Isolation rules: main text must have stroke, shadow, plate, or clean background. Secondary labels must be smaller and visually bound.
- Forbidden adjacency: never place two unrelated short labels close enough that they read as one wrong sentence.
- Removal rule: if the image clearly communicates the shell, remove secondary labels and keep only the strongest text.

## Platform Adaptation

| Platform/mode | Ratio | Composition rule |
|---|---:|---|
| Bilibili cross-platform | 16:9 | Native fit. Use cinematic wide frame, large proof object, face/host in center-safe area, short text away from edges. |
| Bilibili native upload | 1146:717, approx 16:10 | Slightly taller master; keep text, face, and proof in 16:9/4:3 safe center. |
| Bilibili 4:3-safe | 4:3 | Compress to host + proof object + one short shell label. Avoid wide environment-only clues. |
| Douyin horizontal | 4:3 | Use one close proof object and one host action. Reduce background subtlety. |
| Douyin vertical | 3:4 | Stack shell text, host, and proof object vertically; keep documentary environment but simplify labels. |
| Xiaohongshu | 3:4 | More portrait-card friendly: host/object large, short text, clean background, less dark cinematic space. |
| TikTok/Reels/Shorts | 9:16 | Use vertical poster logic; do not force wide documentary frame unless cropping is safe. |
| YouTube long video | 16:9 | Use the same wide cinematic proof frame; reduce Bilibili-specific large Chinese text if title already carries meaning. |

## Layout Patterns

### Pattern 1: Hidden World Proof

- Use when: the topic is an investigation, unusual place, taboo, secret industry, or rare access.
- Composition: cinematic location dominates; host may be small or absent; one huge word/name or no text.
- Text: one noun, one taboo label, or no text.
- Avoid: smiling host cutout that weakens seriousness.

### Pattern 2: Test / Comparison With Real People

- Use when: device vs person, old vs new, human vs machine, result comparison.
- Composition: host and guest/subject foreground, action or test object behind/center.
- Text: short comparison phrase, number, or `VS`.
- Avoid: sterile spec-table comparison.

### Pattern 3: Money / Number As Proof

- Use when: amount, age, view count, price, output, or scale is the hook.
- Composition: number label attached to money, phone, product, person, or object.
- Text: huge number with unit.
- Avoid: floating number that is not physically tied to proof.

### Pattern 4: Tech Arrival / Controlled Room

- Use when: AI, camera gear, software, workflow, future tech.
- Composition: real room, devices, screens, lab/studio, host inside the system.
- Text: optional; keep it short and uneasy or factual.
- Avoid: neon hologram, abstract blue grid, sci-fi tunnel.

### Pattern 5: Guest / Authority Encounter

- Use when: famous person, expert, creator, artist, or guest is the hook.
- Composition: guest and host as cutouts or realistic portrait pair; label/name/arrow binds to guest.
- Text: guest name or one emotional phrase.
- Avoid: generic podcast cover or two heads without a visual question.

### Pattern 6: Brand / Place Reveal

- Use when: office, studio, company, base, new building, internal process.
- Composition: place/building as proof object; host presents or reacts.
- Text: one reveal label such as `新的`.
- Avoid: real-estate brochure or corporate slide.

## Subject Rules

- Use the user's portrait if provided; preserve identity, clothing, face traits, and recognizable accessories.
- Do not preserve a calm reference pose by default. Redesign pose as guide, witness, tester, presenter, or participant.
- Expression should be curious, focused, surprised, amused, or quietly unsettled; avoid MrBeast-level exaggerated yelling unless the topic is comedic.
- If the proof object is stronger than the person, let the object or location dominate.

## Reference Image Handling

- Preserve identity traits from the reference image: face structure, hair, glasses, clothing, silhouette, brand colors, recognizable accessories.
- Do not copy the reference pose unless the user explicitly asks.
- Use a new hook-driven action: pointing to proof, holding device/phone/card, standing inside real scene, reacting to result, guiding viewer through place, or operating equipment.
- If the user provides a product/device/location reference, keep its key shape and visible function but adapt lighting and composition to the shell.
- The final image subject must resemble the user's supplied reference and must not resemble any public creator.

## Identity And Final Prompt Firewall

- Internal skill routing may name 影视飓风, but the final GPT Image 2 prompt must not contain `影视飓风`, `影视飓风-inspired`, `in the style of 影视飓风`, `like 影视飓风`, or any equivalent creator-name shortcut.
- Express the pattern through concrete cover mechanics: real-world proof scene, documentary shell, subject-location-object relationship, restrained cinematic lighting, and clean reveal hierarchy.
- If a portrait reference is supplied, identity preservation outranks all creator-pattern rules. The subject must preserve the user's face, hair, glasses, clothing cues, body type, and supplied identity traits.
- Add a negative constraint that the generated subject must not resemble any public creator, without naming 影视飓风 in the final prompt.

## Text Rules

- Prefer 0-5 Chinese characters, one number, one name, or one question mark.
- Strong text types: object noun, guest name, amount, age, result number, short reveal word, direct question marker.
- Avoid full titles, explanatory subtitles, marketing slogans, and abstract labels like `效率系统` unless embodied by a proof scene.
- Use Chinese text only when it is short, dominant, and protected.

## Typography Layout System

- Treat text as a protected design layer.
- Use heavy Chinese display type, white fill, black stroke/shadow; use yellow/orange for emphasis or proof numbers.
- Every text block needs clean space, a backing plate, or a simple background area.
- Labels must visually attach to their proof object with proximity, arrow, outline, or shared plate.
- For paired labels, match size and visual weight; otherwise remove the weaker label.
- Keep all text, face, and proof object in platform safe area.

## Color And Lighting Rules

- Use cinematic realism before graphic decoration.
- Investigation/taboo: muted green/gray/black, orange or red emphasis, environmental haze.
- Money/industry: warm gold/yellow light, real reflective surfaces.
- Tech/AI: white/green control room, screens, data panels, practical light; not cyberpunk.
- Outdoor/industrial: blue sky, sunlight, shipping/metal/yellow-orange accents.
- Interview/guest: warm soft light, clean face cutout, background blur.
- Faces and proof objects must be bright, sharp, and separated from background.

## Hook Mechanics

- Shell theory: wrap the hard-core nucleus in something public and clickable.
- Hidden world: show access to a place/viewer normally cannot enter.
- Proof number: use money, age, views, price, time, or scale as evidence.
- Real test: show machine/person/device under comparison.
- Tech anxiety: "coming soon but a little scary" through controlled physical setting.
- Authority encounter: guest/person as the proof.
- Place reveal: new building/studio/company/location as the story object.

## GPT Image 2 Prompt Contract

Every prompt must specify:

- final artifact: finished video cover/thumbnail
- platform and ratio
- target canvas in pixels
- creator engine: Shell-Theory Documentary Engine
- raw topic and hard-core nucleus
- public shell chosen for ordinary viewers
- proof object/person/place/number
- one-frame storyboard
- host/user subject role and action
- exact on-image text or `no text`
- copy hierarchy and protected text zones
- layout pattern
- cinematic environment and lighting
- typography rules
- platform-safe area
- reference image handling
- negative constraints
- post-generation dimension verification

Do not prompt "in 影视飓风's exact style." Prompt the transferable shell/proof/cinematic documentary rules.

## Negative Constraints

- no Tim likeness
- no 影视飓风 logo
- no copied existing thumbnail
- no copied Bilibili UI or protected marks
- no generic AI/cyberpunk background
- no abstract flowchart
- no SaaS dashboard
- no course-poster layout
- no fake MrBeast challenge spectacle
- no long sentence on cover
- no tiny text
- no text over clutter without backing
- no unbound labels
- no wrong text grouping
- no edge-critical text outside safe area
- no copying reference pose unless requested

## User Intake Questions

Ask in this order:

1. Which platform will this cover be published on?
2. Which mode or orientation is needed?
3. What is the raw video topic/title?
4. What is the hard-core nucleus: what is the real knowledge, story, product, or result?
5. What public-facing shell can ordinary viewers care about immediately?
6. What proof object, person, location, number, or scene can appear?
7. What exact on-cover text should appear? If none, say no text.
8. Should the user's face appear? If yes, request a reference image.
9. Should the reference pose be preserved, or redesigned as host/witness/guide?
10. What must appear?
11. What must not appear?
12. Are there brand, legal, or platform constraints?

## Quality Checklist

- Did the prompt choose a public-facing shell before visual style?
- Does the shell wrap the hard-core nucleus without lying?
- Is there one visible proof object/person/place/number?
- Does the frame feel like a real documentary/experiment/interview/trip moment?
- Is the host acting as guide/witness/tester/presenter instead of posing generically?
- Is on-cover text short, readable, protected, and object-bound?
- Can the viewer understand the curiosity hook in under one second?
- Does the layout avoid accidental text grouping?
- Does the palette match the topic category instead of default AI neon?
- Does the selected ratio match the platform and keep face/text/proof in safe area?
- Does it avoid copying 影视飓风, Tim, logos, or specific existing thumbnails?
