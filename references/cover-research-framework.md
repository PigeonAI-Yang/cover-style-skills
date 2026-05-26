# Cover Research Framework

## Evidence Rules

Use evidence before taste. A creator style is valid only when it is visible across multiple covers or described by the creator/team.

The primary research target is the creator's cover generation engine, not surface style. The engine explains how a video topic becomes a clickable cover promise, visual event, subject role, text system, and composition.

Before collecting evidence, initialize a managed run using `scripts/manage_research_workspace.py`. Store downloaded files only in the returned run directory and update `manifest.json`.

Minimum source set:

- 10+ public covers
- 3+ process sources when available
- source URL for every sample and process source
- manifest entry for every downloaded cover or copied source

Prefer:

- most-viewed videos
- recent high-performing videos
- recurring formats across time
- thumbnails discussed by the creator or team

Avoid:

- single-cover overfitting
- copying a person's exact face, pose, branding, or logo
- treating generic YouTube tactics as creator-specific DNA

## Sample Table

Use this table while researching:

```markdown
| # | Video title | URL | Local file | Why selected | Visible subjects | On-cover text | Composition | Colors/light | Hook mechanic | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
```

## Analysis Dimensions

### Cover Generation Engine

Classify the creator's dominant engine from evidence. Do not force a creator into MrBeast logic.

Common engine types:

- `Stakes Engine`: extreme cost, reward, danger, challenge, quantity, time, win/loss.
- `Authority Engine`: personal authority, conceptual naming, intellectual confidence, sparse hierarchy.
- `Transformation Engine`: before/after gap, proof of change, path to result.
- `Aesthetic Identity Engine`: stable taste, atmosphere, lifestyle signal, recognizable visual world.
- `Narrative Suspense Engine`: unresolved question, threat, hidden truth, story gap.
- `Utility Clarity Engine`: problem/solution clarity, tutorial value, tool result, scannable promise.

For each creator, answer:

- What viewer decision is compressed into the cover?
- What is the creator promising: spectacle, authority, transformation, beauty, suspense, utility, or a hybrid?
- What must happen to the raw video topic before it becomes a cover?
- What is the subject's role: host, expert, proof, witness, prize, victim, guide, object, atmosphere?
- What would make the cover drift into a different creator's engine?

### Topic Translation Rules

Identify how this creator converts topics into cover concepts:

- Abstract topics: are they made physical, named, quantified, simplified, metaphorized, or left restrained?
- Concrete topics: are they dramatized, compared, beautified, clarified, or framed as proof?
- Does the creator prefer a visual event, a concept label, a person, a product, a result, or an atmosphere?
- What input variables matter before prompting: viewer pain, promise, stakes, authority claim, transformation gap, object, result, scene, mood?
- What translations are forbidden for this creator?

### Cover Storyboard Rules

Analyze how the creator turns a title into a one-frame story, not just a layout.

For each creator, answer:

- What is the story moment shown in the thumbnail?
- What conflict, rule, risk, reward, transformation, or mystery is visible?
- What is the subject doing, and why does that action matter?
- What proof object makes the title believable?
- What should the viewer wonder after seeing the frame?
- What static compositions would fail for this creator?

### Design Layout Brief Rules

Analyze how the creator organizes the thumbnail as a flat design object.

- What is the first-read element, second-read element, and third-read element?
- Where are title, subject, proof object, conflict area, labels, and negative space placed?
- What scale relationship exists between text, face/body, and proof object?
- What reading path does the layout create?
- How does the creator avoid accidental text grouping or semantic misreads?
- What layout patterns weaken the cover even if the story is good?

### Copy Hierarchy Rules

Analyze the creator's on-cover copy as a hierarchy, not a list of text elements.

- What counts as main title, state label, number, progress marker, or badge?
- When does the creator use no text because the image carries the meaning?
- How are labels visually bound to objects or zones?
- What text should not appear together because it creates an unwanted phrase?
- How much distance, scale difference, or backing is needed between text groups?

### Subject

- human face, object, product, environment, money, danger, before/after, social proof
- expression intensity
- body scale: extreme close-up, waist-up, full body
- relationship between subjects: competition, contrast, rescue, reveal, transformation

### Composition

- one dominant focal point or split-screen contrast
- face placement
- object scale exaggeration
- foreground/background depth
- negative space reserved for text
- left/right reading path

### Text

- exact words on cover
- word count
- font category
- outline, shadow, glow, stroke
- placement
- whether text repeats or contradicts the title

### Typography Layout System

- text hierarchy: main title, state labels, numeric/progress badges, optional annotations
- protected text zones: clean negative space, safe bands, corner zones, center-safe placement
- backing system: solid plates, semi-transparent plates, stickers, badges, high-contrast bands
- clutter handling: whether text appears on clean background or first creates a clean plate
- paired-label behavior: whether left/right labels share size, padding, alignment, and visual weight
- platform crop safety: whether text survives 16:9, 16:10, 4:3, 3:4, or 9:16 adaptation

### Color And Lighting

- dominant palette
- accent color
- saturation
- contrast
- rim light, glow, spotlight, cutout, vignette

### Hook Mechanics

Classify each cover's click promise:

- stakes: win/lose, danger, money, time limit
- contrast: cheap vs expensive, before vs after, tiny vs huge
- curiosity gap: hidden result, impossible object, unexplained scene
- identity: "I did X", face-driven emotion, social challenge
- utility/status: lesson, transformation, aspiration

## Distillation Rules

Separate observations into:

- `core`: appears repeatedly and affects recognition
- `conditional`: useful only for certain video topics
- `weak`: plausible but not yet proven

Design DNA should be 3-7 rules. If there are more, compress them.

## Research Artifact Template

```markdown
# Creator Cover Style: <creator name>

## Source Log
- Covers:
- Process sources:
- Managed run:
- Manifest:

## Sample Table
| # | Video title | URL | Local file | Why selected | Visible subjects | On-cover text | Composition | Colors/light | Hook mechanic | Notes |
|---|---|---|---|---|---|---|---|---|---|---|

## Process Sources
- <source>: <what it says about thumbnail design>

## Design DNA
### Core
### Conditional
### Weak

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

After writing this research artifact, write `distillation/design-standard.md` from `references/design-standard-template.md`.

