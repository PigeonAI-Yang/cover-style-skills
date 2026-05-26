---
name: pigeonyang-cover-style-distiller
description: PigeonYang-branded mother skill for researching creator cover patterns, distilling reusable child skills, and running PigeonYang's Agent-native cover workflows for WeChat public account article covers, video covers, Xiaohongshu note covers, and GPT Image 2-ready prompts. Use when the user asks for a cover in a creator's style, wants to distill a YouTube/Bilibili/Xiaohongshu/TikTok creator's thumbnail formula, wants reusable PigeonYang prompt skills for creator-specific cover design patterns, or wants a PigeonYang-branded WeChat article cover workflow.
---

# PigeonYang Cover Style Distiller

## Purpose

Turn a creator's public thumbnail practice into a reusable cover-prompt skill.

Do not write a one-off imitation prompt from memory. First research real cover samples and creator/team commentary, then distill the creator's cover generation engine, create a top-level child skill, and only then write GPT Image 2 prompts.

For PigeonYang's own WeChat public account article covers, do not force a creator-style imitation workflow. Use the product workflow in `PigeonYang WeChat Article Cover Workflow`: extract the article hook, propose three differentiated cover directions, get copy and direction approval, preserve the fixed PigeonYang anime identity, and save production artifacts outside the product git repo.

## Non-Negotiables

- Initialize a user-chosen managed research workspace before collecting covers. Do not save downloaded covers into random project folders, Downloads, Desktop, the skill folder, or any implicit C drive default.
- If no workspace root is configured, stop and ask the user for one path, then persist it with `manage_research_workspace.py set-root`.
- Store every run under `<configured-workspace-root>\<creator-id>\<run-id>\`.
- Maintain `manifest.json` for every run. The manifest is the source of truth for source URLs, local file paths, retention class, and cleanup dates.
- Run workspace cleanup before starting a new research run. Raw cover files default to 30-day retention unless the user explicitly asks to preserve them.
- Collect at least 10 public cover samples before distilling a creator style. Prefer the creator's most-viewed, highest-performing, or most representative videos.
- Search for first-party or team-adjacent explanations of the creator's thumbnail process. For MrBeast, prioritize public explanations from Jimmy Donaldson, his team, interviews, talks, podcasts, or credible writeups that quote them.
- Record source URLs for covers and articles. Do not present unsourced memory as research.
- Distill strategy, not a literal copy. Avoid instructions that duplicate a living creator's exact recurring layout, face, logo, trademarked marks, or protected likeness unless the user owns the rights or provides their own references.
- Creator names are internal routing and research labels only. Do not put the distilled creator's name, `inspired by <creator>`, `in the style of <creator>`, or equivalent wording in the final GPT Image 2 generation prompt. Translate the creator pattern into concrete design rules instead.
- If the user supplies a portrait/reference image, user identity is a hard priority over creator-style transfer. The final prompt must preserve the user's face, hair, glasses, clothing cues, body type, and other supplied identity traits, while only redesigning pose/action for the cover hook. Never let the generated subject resemble the distilled creator unless the user explicitly supplied and authorized that likeness.
- Create child skills as top-level folders under the skills root, not nested inside this skill. Top-level folders are discoverable; nested folders may not be indexed.
- Name every generated child skill with the `pigeonyang-` prefix, for example `pigeonyang-cover-style-mrbeast`.
- Every generated child skill must include `skill.json` with name, semantic version, kind, package, and package_version metadata.
- Produce two distillation artifacts for every creator: `distillation\research.md` and `distillation\design-standard.md`. The research file stores evidence and reasoning; the design standard is the stable reusable contract used by child skills.
- Distill the creator's cover generation engine before distilling surface style. The engine explains how a video topic becomes a clickable cover promise, visual event, subject role, text system, and composition.
- Do not assume every creator uses a MrBeast-style stakes engine. Classify the engine from evidence. Common engines include `Stakes Engine`, `Authority Engine`, `Transformation Engine`, `Aesthetic Identity Engine`, `Narrative Suspense Engine`, and `Utility Clarity Engine`.
- Every design standard must include `Cover Generation Engine` and `Topic Translation Rules`. These sections explain how to translate a user's topic into that creator's cover logic before writing image prompts.
- Every design standard must include `Cover Storyboard Rules`. Prompt writing must build a one-frame cover storyboard before writing final image instructions. The storyboard defines the story moment, conflict, subject task, visible proof, emotional beat, and composition.
- Every design standard must include `Design Layout Brief Rules` and `Copy Hierarchy Rules`. Prompt writing must define information hierarchy, reading path, text blocks, semantic grouping, and forbidden text adjacency before final image instructions.
- Research and standardize typography as a protected layout system, not as loose text styling. Every creator standard must define text hierarchy, protected text zones, backing shapes or badges, background isolation, platform-safe placement, and clutter-handling rules.
- Treat prompt execution as a gated design process, not a memory task. Before writing the final GPT Image 2 prompt or generating an image, produce an `Execution Design Packet` with topic translation, cover storyboard, design layout brief, copy hierarchy, reference handling, and a pre-generation self-check.
- Every `Execution Design Packet` must include an identity and final-prompt firewall check: who the subject must look like, what creator/style words are forbidden in the final prompt, and how the creator pattern will be expressed without naming the creator.
- The final prompt firewall is not optional. Before direct generation, save the exact final GPT Image 2 prompt to a prompt file and run `scripts/verify_prompt_firewall.py` with the distilled creator's forbidden names/aliases. If a portrait/reference image is supplied, also pass `--require-identity-reference`. Do not generate if the script fails.
- Do not generate from only a raw topic, title, or user requirements. If the `Execution Design Packet` is missing or fails the self-check, revise the packet first instead of generating.
- Treat on-cover copy as user-approved product language, not a free assistant rewrite. If the user allows shortening, that permission only allows copy proposals; it does not approve a final title. When changing the user's title, show 3-5 candidate titles with semantic tradeoffs and wait for explicit user approval before final prompt writing or generation.
- Select both an aspect ratio and a target pixel canvas from `references/platform-cover-standards.md`. Prompts must include the target canvas, and generated outputs must be dimension-checked before delivery.
- Default to prompt writing only. Ask whether the user wants direct generation after showing the prompt packet.
- For PigeonYang WeChat article covers, the first-generation target is open rate, not style mimicry. Use high-click knowledge-media cover logic with medium brand consistency.
- For PigeonYang WeChat article covers, always use the private identity reference unless the user explicitly overrides it: `J:\PigeonYang\cover-style-distiller\cover-projects\_identity\pigeonyang-character-reference.png`.
- For PigeonYang WeChat article covers, production project files must be written under `J:\PigeonYang\cover-style-distiller\cover-projects`, never under the product repo.
- For PigeonYang WeChat article covers, produce three differentiated directions before final prompt writing. Each direction must vary hook, copy, and visual strategy.
- For PigeonYang WeChat article covers, do not generate until the user approves one direction and the exact on-cover text.

## Workflow

### 1. Identify the Creator

Resolve:

- Creator display name
- Stable creator id, lowercase kebab-case, such as `mrbeast`, `dan-koe`, `heygen`, `yingshijufeng`
- Platform and channel URL when available
- Target platform for the user's future cover: YouTube 16:9, Bilibili 16:9, Xiaohongshu 3:4/1:1, TikTok/Reels 9:16, or other

If the creator is ambiguous, ask one clarifying question.

### 2. Research

First initialize a managed run:

```powershell
python <CODEX_SKILLS_ROOT>\pigeonyang-cover-style-distiller\scripts\manage_research_workspace.py show-config
python <CODEX_SKILLS_ROOT>\pigeonyang-cover-style-distiller\scripts\manage_research_workspace.py cleanup
python <CODEX_SKILLS_ROOT>\pigeonyang-cover-style-distiller\scripts\manage_research_workspace.py init `
  --creator-id mrbeast `
  --creator-name "MrBeast"
```

If `show-config`, `cleanup`, or `init` reports that no workspace root is configured, ask the user for the workspace path and run:

```powershell
python <CODEX_SKILLS_ROOT>\pigeonyang-cover-style-distiller\scripts\manage_research_workspace.py set-root `
  --workspace-root <user-provided-workspace-root>
```

Use the returned run directory for all downloaded files and research artifacts.

Then use `references/cover-research-framework.md` and `references/workspace-management.md`.

Minimum evidence:

- 10+ cover samples with source URLs
- titles, rough topics, and visible text on the cover
- if available, performance signals such as view count or ranking reason
- 3+ creator/team/process sources when available
- each downloaded file recorded in `manifest.json`

If current public data is needed, browse the web. If the platform blocks direct cover access, use search results, video pages, screenshots, or user-provided image files and state the limitation.

When a cover or source is downloaded to a temporary location, immediately archive it with `manage_research_workspace.py add-cover` or `add-source`. Do not proceed with analysis from untracked files.

### 3. Distill

Produce `distillation\research.md` with these sections:

```markdown
# Creator Cover Style: <creator name>

## Source Log
## Sample Table
## Process Sources
## Design DNA
## Cover Generation Engine
## Topic Translation Rules
## Cover Storyboard Rules
## Design Layout Brief Rules
## Copy Hierarchy Rules
## Composition Rules
## Subject Rules
## Identity And Final Prompt Firewall
## Text Rules
## Typography Layout System
## Color And Lighting Rules
## Hook Mechanics
## GPT Image 2 Prompt Rules
## Avoid
## User Input Questions
```

Design DNA must separate:

- stable repeatable rules
- context-dependent rules
- weak or uncertain observations

Cover Generation Engine must answer:

- What viewer decision is the cover trying to compress?
- What engine type best describes the creator: stakes, authority, transformation, aesthetic identity, narrative suspense, utility clarity, or a hybrid?
- How does the creator turn a topic into a click promise?
- What is the subject's role: host, proof, witness, prize, victim, guide, expert, object, or atmosphere?
- What must happen before visual style is selected?

Topic Translation Rules must answer:

- How abstract topics are translated for this creator.
- What must be made physical, named, quantified, simplified, dramatized, or aesthetically restrained.
- What translation moves are forbidden because they would drift into another creator category.

Cover Storyboard Rules must answer:

- What one-frame story should this title become?
- What is the visible conflict, rule, risk, reward, or transformation?
- What is the subject actively doing in that moment?
- What proof object makes the promise believable?
- What should the viewer wonder after seeing the cover?
- What composition is forbidden because it would become a static poster, product ad, dashboard, or PPT comparison?

Design Layout Brief Rules must answer:

- What is the information hierarchy: first read, second read, third read?
- What are the fixed zones for title, subject, conflict area, proof object, and optional labels?
- What is the visual weight of each zone?
- What is the intended reading path?
- Where must negative space be preserved?
- What layouts are forbidden because they create weak hierarchy or poster-like clutter?

Copy Hierarchy Rules must answer:

- What is the main title, and is there a subtitle?
- Are state labels needed, or should the image carry the contrast?
- If labels are used, what object/zone are they bound to?
- What text blocks must be isolated from each other?
- What text adjacency or reading order would create the wrong meaning?
- What text should be removed if it competes with the main title?

Then produce `distillation\design-standard.md` using `references/design-standard-template.md`. This file is the canonical reusable standard. It should cite the evidence summary but not include the full sample table or long research notes.

### 4. Create The Child Skill

Run `scripts/create_child_skill.py` from this skill:

```powershell
python <CODEX_SKILLS_ROOT>\pigeonyang-cover-style-distiller\scripts\create_child_skill.py `
  --creator-id mrbeast `
  --creator-name "MrBeast" `
  --source <configured-workspace-root>\mrbeast\<run-id>\distillation\design-standard.md `
  --output-root <CODEX_SKILLS_ROOT>
```

The created folder should be named `pigeonyang-cover-style-<creator-id>`, for example `pigeonyang-cover-style-mrbeast`.
The created folder must include both `SKILL.md` and `skill.json`.

After creation, run:

```powershell
python <CODEX_SKILLS_ROOT>\.system\skill-creator\scripts\quick_validate.py <CODEX_SKILLS_ROOT>\pigeonyang-cover-style-<creator-id>
```

### 5. Use The Child Skill

When the user asks for a cover in a distilled creator style:

1. Load the matching child skill, such as `pigeonyang-cover-style-mrbeast`.
2. Ask the publishing platform first and recommend a ratio using `references/platform-cover-standards.md`.
3. Ask only for remaining missing production inputs:
   - cover topic or video title
   - exact on-cover text, if any
   - target platform, orientation, aspect ratio, and target canvas
   - user's own portrait/reference image, if required
   - must-include or must-avoid elements
   - brand constraints
4. Use the child skill's `Cover Generation Engine` and `Topic Translation Rules` to translate the raw topic into the creator's cover logic.
5. Build a one-frame `Cover Storyboard` before final prompting. Do not skip it. If the storyboard is weak, revise the story instead of decorating the frame.
6. Build a `Design Layout Brief` and `Copy Hierarchy` before final prompting. Do not skip them. If text blocks can be misread as one phrase, remove or reposition the lower-priority text before generating.
7. If the exact on-cover text is not supplied, or if you shorten/rewrite the user's title, run a `Copy Approval Gate` before final prompt writing:
   - propose 3-5 candidate titles
   - explain what each preserves and what it drops
   - recommend one
   - ask the user to approve one exact title or provide their own
   - do not generate until the exact title is approved
8. Produce an `Execution Design Packet` using `references/gpt-image-2-cover-prompts.md`. The packet must include:
   - topic translation
   - cover storyboard
   - design layout brief
   - copy hierarchy
   - reference handling
   - identity and final-prompt firewall
   - pre-generation self-check
9. If any self-check item fails, revise the packet before writing the final image prompt.
10. Write a GPT Image 2 prompt packet using `references/gpt-image-2-cover-prompts.md`; include the exact target canvas in pixels. Before generation, remove the distilled creator's name and any style/inspired-by wording from the final prompt.
11. Save the exact final prompt text to a prompt file and run `scripts/verify_prompt_firewall.py`. Use `--forbid` for the distilled creator display name and common aliases; use `--require-identity-reference` when the user supplied a portrait/reference image. Do not continue if the script fails.
12. Show the prompt packet and ask whether to generate.
13. If the user confirms and the prompt firewall passed, use the available image generation backend. Prefer a runtime-native image tool; if using `baoyu-imagine`, use provider `openai` and model `gpt-image-2` when configured.
14. After generation, verify the output dimensions with `scripts/verify_image_dimensions.py`. If the result does not match the requested ratio/canvas, do not report it as complete; regenerate or ask whether to crop/resize.

### 6. PigeonYang WeChat Article Cover Workflow

Use this workflow when the user asks for a PigeonYang-branded WeChat public account article cover, a WeChat article header image, or a cover for Yang's article-first publishing pipeline.

This is a product workflow, not a creator-style distillation workflow.

#### 6.1 Inputs

Accept any of:

- article title only
- title plus summary
- full article Markdown
- local draft file path
- rough topic plus desired publishing angle

If the input is weak, proceed with explicit assumptions instead of asking many questions. Ask only when the missing information blocks the cover decision.

#### 6.2 Default Platform Standard

Default to `WeChat public account article main cover`:

- ratio: `2.35:1`
- target canvas: `2350x1000`
- square-safe zone: central `1000x1000` area, approximately `x=675` to `x=1675`

Ask only whether the user also needs a square sharing or secondary-article cover. If yes, generate a separate `1:1 1080x1080` layout from the same approved concept instead of cropping blindly.

Use `references/platform-cover-standards.md` for WeChat safe-area, text density, and readability rules.

#### 6.3 Identity Reference

The default identity reference is:

```text
J:\PigeonYang\cover-style-distiller\cover-projects\_identity\pigeonyang-character-reference.png
```

Preserve these traits:

- refined anime / illustration character style
- silver-gray short hair
- glasses
- black suit or all-black refined clothing
- calm, confident, intelligent, composed expression
- PigeonYang personal IP presence

Do not turn the subject into a photorealistic person. Do not copy the static reference pose unless it serves the cover hook.

#### 6.4 Private Project Records

Real production artifacts must be saved under:

```text
J:\PigeonYang\cover-style-distiller\cover-projects\<YYYYMMDD-slug>\
```

Use this structure when possible:

```text
brief.json
source.md
directions.md
approved-direction.md
execution-packet.md
prompt-final.txt
outputs\
metrics.json
review.md
```

Do not save private production artifacts under `J:\PigeonYang\cover-style-distiller\product`.

Use the deterministic project script when possible:

```powershell
python J:\PigeonYang\cover-style-distiller\product\scripts\manage_cover_project.py create `
  --title "<article title>" `
  --summary "<optional summary>" `
  --cover-mode wechat-article-main
```

Before writing or updating a production record, validate the path:

```powershell
python J:\PigeonYang\cover-style-distiller\product\scripts\manage_cover_project.py validate-path `
  --project-path J:\PigeonYang\cover-style-distiller\cover-projects\<project-id>
```

#### 6.5 Direction Generation

Before final prompt writing, produce three candidate directions. Each direction must include:

- hook angle
- proposed on-cover copy
- visual premise
- PigeonYang character pose / expression
- background, object, or proof cue
- text hierarchy
- why it may improve open rate
- risk or possible misread

The three options should not be minor style variants. They should differ in hook, copy, and visual strategy.

Recommended hook families:

- contradiction / anti-common-sense
- painful truth / warning
- direct benefit / outcome
- hidden mechanism / behind-the-scenes
- identity challenge
- numbered system or method

#### 6.6 Copy Decision Rules

The system may propose cover copy, but the user must approve exact final on-cover text before final prompt writing.

For WeChat main covers:

- use a large title when the click promise depends on a sharp claim, contradiction, warning, or benefit
- use a short keyword or label when the visual carries the story
- use no text only when the visual premise is unusually self-explanatory
- keep first-read Chinese text short, preferably 4-10 characters and no more than 14 characters across 1-2 lines
- avoid more than two independent text blocks

If the user has not approved exact text, stop at the direction packet and ask for approval.

#### 6.7 Execution Packet

After the user approves one direction, produce an `Execution Design Packet` with:

- approved copy
- article hook translation
- one-frame cover storyboard
- design layout brief
- copy hierarchy
- WeChat safe-area plan
- identity reference handling
- final-prompt firewall
- pre-generation self-check

The layout brief must state whether the cover is `2.35:1 2350x1000`, `1:1 1080x1080`, or both.

#### 6.8 Final Prompt Rules

The final GPT Image 2 prompt must:

- specify `WeChat public account article main cover`
- specify `2.35:1, target canvas 2350x1000 pixels`
- include central square-safe composition rules
- preserve PigeonYang anime identity from the private reference image
- state exact approved text once, or explicitly say no on-image text
- forbid photorealistic identity drift
- forbid small unreadable text, crowded subtitles, and text over the face or glasses

Before generation, save the exact final prompt to `prompt-final.txt` in the private project folder and run `scripts/verify_prompt_firewall.py`. Use `--require-identity-reference`.

#### 6.9 Output And Metrics

After generation:

- save output under the private project `outputs\` folder
- verify dimensions using `scripts/verify_image_dimensions.py`
- create or update `metrics.json` with fields for article URL, published time, selected output, open rate, reads, shares, subjective score, and notes
- do not call the project complete if dimensions are wrong or identity has drifted

Metrics update example:

```powershell
python J:\PigeonYang\cover-style-distiller\product\scripts\manage_cover_project.py update-metrics `
  --project-path J:\PigeonYang\cover-style-distiller\cover-projects\<project-id> `
  --article-url "<published article URL>" `
  --open-rate 0.18 `
  --reads 1000 `
  --shares 20 `
  --subjective-score 4
```

Dimension verification example:

```powershell
python <CODEX_SKILLS_ROOT>\pigeonyang-cover-style-distiller\scripts\verify_image_dimensions.py <generated-image.png> --preset douyin-vertical --ratio-only
```

Prompt firewall example:

```powershell
python <CODEX_SKILLS_ROOT>\pigeonyang-cover-style-distiller\scripts\verify_prompt_firewall.py <final-prompt.txt> `
  --forbid "He Tongxue" `
  --forbid "何同学" `
  --require-identity-reference
```

## Output Contract

For prompt-only output, return:

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
<final prompt>

## Reference Inputs
<required reference images or "none">

## Generation Settings
model: gpt-image-2
platform:
aspect_ratio:
target_canvas:
quality:
post_generation_check:

## Negative Constraints
<what to avoid>

## Iteration Plan
<2-3 likely fixes after first image>

是否需要我直接生成？
```

For child-skill creation, return:

1. Key files read
2. Child skill path
3. Managed research run path
4. Research artifact path
5. Design standard path
6. Evidence count: cover samples and process sources
7. Retention status for raw covers
8. Validation result
9. Risks or weak evidence

## References

- `references/cover-research-framework.md`: research and distillation rubric.
- `references/gpt-image-2-cover-prompts.md`: prompt packet format for GPT Image 2-ready cover generation.
- `references/workspace-management.md`: storage layout, manifest schema, and retention rules.
- `references/platform-cover-standards.md`: platform-specific cover ratios and composition adaptation rules.
- `references/design-standard-template.md`: canonical design standard structure required for each distilled creator.
- `scripts/verify_image_dimensions.py`: post-generation pixel and aspect-ratio verification.
