# Creator Cover Style: 影视飓风

## Source Log

- Covers: 12 main-account Bilibili covers archived under `covers/`.
- Process sources: 6 saved sources under `sources/`.
- Managed run: `J:\PigeonYang\cover-style-distiller\product\research\yingshijufeng\20260525-053030`.
- Manifest: `manifest.json`.
- Limitation: Bilibili space search API returned rate-limit/security responses, so the sample ranking uses a public Bilibili data dashboard API plus per-video public cover URLs. Main account samples were filtered by `owner_name = 影视飓风`.

## Sample Table

| # | Video title | URL | Local file | Why selected | Visible subjects | On-cover text | Composition | Colors/light | Hook mechanic | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 在性产业“合法”的地方，我们看到了... | https://www.bilibili.com/video/BV1k9wDzKEvS | covers/001-cover-001.jpg | Main account top-view sample, 10,232,544 views | Back-view person in red light district, shadow figures | 性工作者 | Cinematic street still, giant vertical word, small label | muted green/gray with orange-red title | taboo investigation | Serious documentary cover, not host-led. |
| 2 | 3台高速机VS刘谦手速！谁更胜一筹？ | https://www.bilibili.com/video/BV1XY546vE1o | covers/002-3-vs.jpg | Main account top-view sample, 9,494,886 views | Tim and Liu Qian reacting to action | 3台高速机 / VS刘谦 | Two-person foreground, large top text, motion background | warm studio, white/orange text | test/challenge | Uses large literal comparison but still grounded in real people. |
| 3 | 带着100万，我们揭开了赌场的秘密… | https://www.bilibili.com/video/BV1Nn9TBhEYR | covers/003-100.jpg | Main account top-view sample, 8,560,075 views | Tim and colleague holding money label, casino light streak | ¥100万 | Two-person close-up on right, money label center-left | gold/yellow casino glow | money + hidden truth | The amount is the proof object. |
| 4 | 收集了100个人的梦，我们发现了奇怪的关联… | https://www.bilibili.com/video/BV1PyQzB7ER5 | covers/004-100.jpg | Main account top-view sample, 8,274,341 views | Tim floating/falling over software-like grid | none visible | Wide surreal top-down story frame | cold blue/gray, motion blur | weird discovery | Abstract topic is physicalized as a strange scene. |
| 5 | 这个公司…好奇怪啊 | https://www.bilibili.com/video/BV1BbFkzYEgr | covers/005-cover-005.jpg | Main account top-view sample, 8,135,273 views | Two cutout host faces, location signage, huge question mark | ? / 阳光之桥 | Cutout collage over location background | bright sky, yellow outline | curiosity trip | Lightweight travel-investigation variant. |
| 6 | 能卖上亿美金？国产短剧如何征服世界？ | https://www.bilibili.com/video/BV1ABcsztEcY | covers/006-cover-006.jpg | Main account top-view sample, 7,966,350 views | Tim holding phone showing poster, edit screens behind | phone poster text only | Phone proof object foreground, host side-smile | studio screens, phone glow | industry explanation through object | The phone screen is the proof object. |
| 7 | 一匹马身价上百万，赛马究竟在看什么？ | https://www.bilibili.com/video/BV12Q6TBwE2J | covers/007-cover-007.jpg | Main account top-view sample, 7,484,828 views | Tim and guest cutouts, racing horse motion | 赛马 | Oversized word left, host/guest right, race behind | outdoor green + white/black text | expensive world explained | Uses big topic label plus human curiosity. |
| 8 | 改变视频行业的AI，快来了(但有点恐怖) | https://www.bilibili.com/video/BV1A3cczZEf6 | covers/008-ai.jpg | Main account top-view sample, 7,252,069 views | Tim centered in white room, green code panels | none visible | Symmetric top-down containment, host as subject | white/green tech but not cyberpunk | coming technology + unease | Clean, restrained, high-tech proof room. |
| 9 | 24小时不间断？港口都在运些什么 | https://www.bilibili.com/video/BV1hAcUzzETk | covers/009-24.jpg | Main account top-view sample, 6,593,386 views | Tim pointing down from container stack | none visible | Giant real-world environment, small host action | sunlit industrial orange/blue | behind-the-scenes access | Scale comes from location, not text. |
| 10 | 关于“活着”，我们问了问余华 | https://www.bilibili.com/video/BV14XLq64EQf | covers/010-cover-010.jpg | Main account top-view sample, 6,573,800 views | Yu Hua and Tim cutouts | 余华 | Interview proof, arrow + name label | soft indoor background, white/yellow text | authority encounter | The guest is the proof object. |
| 11 | 高一的笨豆，做出的视频让我惊呆了… | https://www.bilibili.com/video/BV1TFd3BEEB3 | covers/011-cover-011.jpg | Main account top-view sample, 6,159,875 views | Teen creator, Tim reacting, phone proof | 16岁 / 1亿+全网播放量 | Phone proof in foreground, age label top | bright outdoor blue/yellow | young creator proof | Strong number label and creator identity. |
| 12 | 全新工作楼！ | https://www.bilibili.com/video/BV1qc6iBfEPT | covers/012-cover-012.jpg | Main account top-view sample, 6,143,973 views | Tim presenting Storm Base building | 新的 | Building as proof object, host cutout lower-right | clean blue sky, white outlined text | reveal / milestone | Brand-space reveal; simple label. |

## Process Sources

- `sources/articles/ai-ip.html`: reports Tim/影视飓风's AI-era content method. Key points: start from a clickable "shell"; if people do not click, they will not watch; the shell is often title-driven; teams submit title and picture ideas; AI is used to generate cover alternatives; after the shell is set, production shifts from pure resolution worship to interesting images; publishing is data-monitored.
- `sources/data-apis/bilibili-api-metadata-tim-2.json`: Liu Run interview page metadata states the interview discusses Tim's "HKRR" viral creation method, business model, team management, and self-media停更 crisis.
- `sources/interview-video-pages/tim.html`: saved page for Liu Run's Tim interview. Used as process-source locator, with API metadata above as the reliable readable record.
- `sources/interview-summarys/tim-4-500.html`: Podwise summary/transcript page for Luo Yonghao's Tim interview. Supports broader evidence that Tim frames the team as image-world builders with content, business, and organization discipline. Less directly about covers; treated as medium-confidence process context.
- `sources/creator-process-video-pages/tim.html` and `sources/data-apis/bilibili-api-metadata-tim.json`: Tim writing/rhythm process page and API metadata. Supports the idea that cover/story promise should map to pacing and script rhythm, not just a static poster.
- `sources/data-apis/b-api.json`: public dashboard API used to select main-account high-view samples and record cover URLs.

## Design DNA

### Core

1. Use a popular "shell" to package a hard-core or niche topic: taboo, money, famous person, impossible age/result, strange place, rare industry, new technology, or direct question.
2. Make the cover feel like a real frame from a documentary/adventure/experiment, not a graphic poster.
3. Put a proof object in the frame: real person, phone, money label, location, building, machine, code room, horse, container yard, famous guest.
4. Use Tim/host as guide, witness, presenter, or participant; the host explains access and credibility, not just celebrity expression.
5. Keep text short and large. Typical text is a noun, number, name, or question marker, not a full sentence.
6. Combine cinematic realism with Bilibili-friendly bold text/cutout clarity.

### Conditional

- For social or investigative topics, the host may disappear and the scene/proof object takes over.
- For tech topics, use clean white/green labs, real screens, devices, or controlled rooms; avoid generic neon AI.
- For guest/interview topics, guest face/name becomes the proof object.
- For brand/company topics, location/building/office becomes the proof object.

### Weak

- Exact typography varies by video, but white heavy text with black outline and occasional yellow/orange emphasis recurs strongly enough to standardize.
- View-ranking data comes from a public dashboard, not official Bilibili space API export, because the direct space API was blocked.

## Cover Generation Engine

Engine type: `Shell-Theory Documentary Engine`, a hybrid of `Narrative Suspense Engine`, `Utility Clarity Engine`, and `Authority/Proof Engine`.

Viewer decision compressed: "Is this real, unusual, useful, or close enough to a hidden world that I want to see what they found?"

The creator promises access and understanding: a hard or unfamiliar subject is wrapped in a concrete shell that ordinary viewers can instantly care about.

Topic-to-cover mechanism:

1. Choose the shell before choosing style.
2. The shell must be a person, place, money amount, visible object, strange question, famous name, impossible result, or sensory scene.
3. Then stage a one-frame documentary proof: host/guest/object in a real environment.
4. Use short text to name the shell or proof, not to explain the whole video.

Subject role:

- Tim/host: guide, witness, explainer, tester, presenter, participant.
- Guest: authority proof or contrast partner.
- Object/location: evidence.
- Environment: atmosphere and scale.

Pre-visual decision:

- Decide the "shell" and proof object first.
- Decide whether this is investigation, experiment, explanation, journey, reveal, or interview.
- Only then choose text, pose, lighting, and layout.

Drift risk:

- If the cover becomes a MrBeast-style extreme challenge, SaaS dashboard, pure flowchart, generic AI neon poster, course cover, or clean product ad, it has left the 影视飓风 engine.

## Topic Translation Rules

- Abstract topics: translate into a public-facing shell. For example, "AI workflow" becomes "AI正在改变视频行业", a visible white/green lab, Tim inside the machine/room, and one eerie proof object.
- Technical topics: make the device, experiment, screen, failure, or real test scene visible.
- Social topics: make the place, group, rule, money, taboo, or real person visible; use cinematic distance and serious atmosphere.
- Creator/business topics: use the person, office, phone result, million-level number, or backstage scene as proof.
- Interview topics: guest face/name plus a single emotional or intellectual hook.
- Required translation variables: raw topic, public shell, hidden hard-core nucleus, proof object, host role, one-frame question, exact short cover text.
- Forbidden moves: generic keynote slide, UI dashboard, abstract concept card, dense text explanation, fake luxury, unearned danger, MrBeast money spectacle unless the source topic truly involves money.

## Cover Storyboard Rules

- Story moment: capture the moment the viewer can tell "they really went there / tested it / met them / found something."
- Visible conflict: hidden world, strange rule, real proof, money scale, technology arriving, before/after surprise, or "why is this happening?"
- Subject action: host points, holds proof, reacts, stands inside the environment, presents a location, compares with guest, or is physically placed inside the concept.
- Proof object: phone screen, real location, guest, machine, room, building, money tag, data panel, industry scene, or strong environmental clue.
- Viewer question: "What did they see?", "Is this true?", "How does this work?", "Why is it like this?", "What is behind it?"
- Forbidden static compositions: no generic presenter next to title, no plain PPT title card, no decorative tech background, no balanced dashboard layout, no unrelated host face pasted over vague background.

## Design Layout Brief Rules

- First read: the shell or proof, often a large word/number/name or a shocking visual object.
- Second read: host/guest face or body action.
- Third read: environment and story detail.
- Layout zones: one dominant proof zone; one host/guest zone; one protected text zone; background must carry context, not random texture.
- Visual weight: proof object and face must be phone-readable. Text should be big but not overcrowd the real-world frame.
- Reading path: text/proof -> face/action -> environment clue -> title curiosity.
- Negative space: preserve clean space around text; use sky, wall, screen, dark street, or blurred background for text.
- Forbidden layouts: no three equal text blocks, no label touching main title in a way that makes a wrong sentence, no tiny captions, no pure left/right feature comparison unless the video is a direct test.

## Copy Hierarchy Rules

- Main title: one short shell phrase, noun, number, name, question marker, or product/guest label.
- Subtitle: usually none.
- State labels: optional. Use only when attached to person/object/zone.
- Object/zone binding: labels must point to the object or person they name, e.g. name label next to guest, number next to phone/money/device, question mark next to strange location.
- Isolation rules: main text should have stroke, shadow, or plate. Secondary labels must be smaller or physically bound.
- Forbidden adjacency: do not place unrelated short labels near the main title if they can be read as one sentence.
- Removal rule: if the scene already explains the shell, remove text and rely on the object/environment.

## Composition Rules

- Use cinematic real-world backgrounds: street, office, device room, industrial site, racecourse, interview scene, studio screen.
- Use cutout host/guest when clarity is needed, but keep the background as believable evidence.
- Use slight exaggeration: oversized phone, large amount label, large guest/name label, big question mark.
- Maintain Bilibili feed readability: high contrast, heavy text, clean face edges.

## Subject Rules

- Preserve Tim/host-like role only as functional role, not likeness. For user covers, use the user's own portrait as host/witness/guide if provided.
- Expressions are curious, surprised, focused, or amused; rarely MrBeast-level open-mouth shouting.
- If no face is needed, let the proof object or location dominate.

## Text Rules

- Prefer 0-5 Chinese characters, one number, one name, or one question mark.
- Text types: short noun, celebrity/name, price/amount, age/result, direct object label, "新的", "赛马", "¥100万", "16岁".
- Avoid full sentence cover copy unless the platform requires it.
- Use white heavy characters with black stroke; yellow/orange for emphasis; occasional red/orange when the topic is danger/taboo.

## Typography Layout System

- Text is a protected layer on clean background or plate.
- Heavy Chinese display font, white with black outline/shadow; yellow/orange secondary emphasis.
- Numbers and names can be huge; explanatory words stay minimal.
- For labels, bind with arrows, outlines, or proximity to the named subject.
- Avoid tiny annotation text; it dies in Bilibili mobile feeds.

## Color And Lighting Rules

- Use cinematic realism first: real light, real environment, strong contrast.
- Palette changes by shell:
  - investigation/taboo: muted green/gray, orange/red accent.
  - money/casino: gold/yellow.
  - tech/AI: white room, green screens, controlled lab, not cyberpunk.
  - outdoor/industry: blue sky, sunlight, industrial orange/yellow.
  - interview/guest: warm soft indoor with clear face cutouts.
- Faces and proof objects must be bright and sharp.

## Hook Mechanics

- Hidden world: "we went where you normally cannot go."
- Proof amount/result: money, age, views, expensive object, famous person.
- Test/comparison: machine vs human, device vs reality.
- Strange place/company: "this place is weird; what is inside?"
- Tech arrival: "this thing is coming and it changes an industry."
- Emotional authority: famous guest or human story as proof.

## GPT Image 2 Prompt Rules

- Prompt the transferable engine, not "copy 影视飓风".
- Always specify: shell, hard-core nucleus, proof object, one-frame story, subject role, exact on-image text, protected text zone, cinematic environment, Bilibili-safe readability, and negative constraints.
- For reference portraits, preserve identity but redesign pose/action as host/witness/guide.

## Avoid

- No exact 影视飓风 logo, Tim likeness, or copied existing thumbnail.
- No generic AI/cyberpunk background.
- No MrBeast challenge spectacle unless the user's content is truly challenge-based.
- No product ad, course poster, SaaS dashboard, flowchart, or calm expert slide.
- No long title pasted onto the image.
- No unbound labels.

## User Input Questions

1. Which platform and ratio is this for?
2. What is the raw topic/title?
3. What is the hard-core nucleus of the content?
4. What public-facing shell can ordinary viewers instantly care about?
5. What proof object, location, person, number, device, or scene can appear?
6. Should the user's own face appear? If yes, provide a reference.
7. What exact on-cover text should appear, if any?
8. What must appear?
9. What must not appear?
10. Are there brand/legal constraints?
