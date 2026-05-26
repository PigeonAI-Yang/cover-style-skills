# Platform Cover Standards

## Rule

Ask the publishing platform before writing the image prompt. Aspect ratio changes composition, text placement, and whether a MrBeast-style layout can survive cropping.

If the user names a platform but not orientation, recommend a default and ask for confirmation only when the choice materially changes the cover.

## Practical Defaults

Use both the ratio and the target canvas. Do not prompt with only `horizontal`, `vertical`, or a ratio label when a fixed canvas is available.

| Platform | Recommended cover ratio | Target canvas | Use when | Notes |
|---|---:|---:|---|---|
| YouTube long video | 16:9 | 1280x720 | Standard YouTube thumbnail | Best fit for MrBeast-style wide comparison, crowd, and spectacle layouts. |
| Bilibili upload master | 1146:717, approx 16:10 | 1146x717 | Bilibili-native video cover upload | Commonly cited Bilibili cover canvas. Design with center-safe layout because display surfaces may crop differently. |
| Bilibili 16:9-safe | 16:9 | 1920x1080 | Reuse with YouTube or wide Bilibili feed surfaces | Keep critical face/text away from the top/bottom and side edges. |
| Bilibili 4:3-safe | 4:3 | 1440x1080 | Bilibili surfaces or templates that crop toward 4:3 | Use a tighter central composition; avoid far-left/far-right labels. |
| Douyin horizontal video | 4:3 | 1440x1080 | User publishes horizontal video on Douyin | Safer than 16:9 for Douyin cover surfaces; reduce side-by-side complexity. |
| Douyin vertical video | 3:4 | 1080x1440 | User publishes vertical video on Douyin | Use portrait cover composition; keep face/text central and avoid edge-critical details. |
| Xiaohongshu | 3:4 | 1080x1440 | Note/card style cover | Use portrait composition; one large subject and short text. |
| Xiaohongshu square | 1:1 | 1080x1080 | User asks for square feed cover | Avoid long left/right comparisons; use stacked or diagonal contrast. |
| TikTok / Reels / Shorts | 9:16 | 1080x1920 | Full vertical short-video cover | Keep text and face in the center; avoid tiny side labels. |
| WeChat video account | 6:7 or 3:4 | 1080x1260 or 1080x1440 | User targets feed-style video cover | Ask if the account has a preferred ratio; keep center-safe. |
| WeChat public account article main cover | 2.35:1 | 2350x1000 | First article in a WeChat public account push | Use a wide master that can downsample to common 900x383 display surfaces; design for phone-size title readability. |
| WeChat public account square cover | 1:1 | 1080x1080 | Sharing thumbnail, secondary articles, or when a square crop is required | Use a self-contained square composition; do not rely on far-left or far-right details from the wide cover. |

## Adaptation Rules

- 16:9: use wide MrBeast layouts: three-zone comparison, huge object vs tiny object, teams facing each other, large foreground host plus giant prize.
- Bilibili native: prefer a 1146:717 / approx 16:10 master when the user specifically says Bilibili and has no cross-platform requirement. Keep a 4:3 and 16:9 safe center area because Bilibili covers may be displayed or cropped differently across surfaces.
- Bilibili cross-platform: if the same cover must also fit YouTube, generate 16:9 first and keep the Bilibili-safe center crop; if the cover is only for Bilibili feed/card use, consider 4:3-safe composition.
- 4:3: keep the wide logic but compress spacing; avoid putting critical text at the far left/right edge.
- 3:4: switch from side-by-side to top/bottom or diagonal contrast; make one face/object dominate the upper half and put short text in the top or lower safe band. Use as the default Douyin vertical ratio and for Xiaohongshu portrait covers.
- 1:1: use one central subject plus two contrast cues; avoid crowd detail.
- 9:16: use full vertical short-video cover logic; stack subject, stake, and prize. Use for TikTok/Reels/Shorts or explicit full vertical poster requests. Do not substitute it for Douyin 3:4 vertical cover requests.
- WeChat public account article main cover: use 2.35:1 as the default wide cover. The canvas is shallow, so create one dominant horizontal reading path: hook text -> PigeonYang character -> proof object or conflict. Keep the main face, core symbol, and brand cue inside the center square-safe zone so the cover can survive sharing or square previews.
- WeChat public account square cover: use a separate 1:1 composition when the user needs a share thumbnail or secondary article cover. Do not simply crop the wide cover if the title, face, or proof object would be cut off.

## WeChat Public Account Article Cover Rules

### Modes

Use two WeChat article cover modes:

| Mode | Ratio | Target canvas | Purpose |
|---|---:|---:|---|
| Main wide cover | 2.35:1 | 2350x1000 | First article / headline visual in a public account push. |
| Square cover | 1:1 | 1080x1080 | Sharing thumbnail, secondary article, or explicit square preview. |

For a 2350x1000 wide cover, treat the central `1000x1000` area as square-safe. On the wide canvas this means the horizontal zone from approximately `x=675` to `x=1675`. The square-safe zone must contain the PigeonYang identity anchor and the one visual idea that still explains the article if cropped.

### Safe-Area Rules

- Keep all critical text at least `120px` away from the wide canvas left and right edges, and at least `90px` away from the top and bottom edges.
- Keep the PigeonYang character face, glasses, and hair fully inside either the center square-safe zone or a deliberate wide-cover focal zone that can be separately adapted to square.
- Do not place the only proof object, number, or conflict cue at the far left or far right unless a separate square cover will be generated.
- Avoid putting small subtitle text near the bottom edge; WeChat feed surfaces and phone compression make thin lower text easy to lose.
- If both wide and square outputs are needed, design from a shared concept but write two layouts, not one crop instruction.

### Text Decision Rules

Choose text density by article hook:

- Use a large title when the article's click promise depends on a sharp claim, contradiction, warning, or benefit. Keep it to 4-10 Chinese characters when possible; absolute maximum is 14 Chinese characters across 1-2 lines.
- Use a short keyword or label when the image already carries the story and the article only needs a category, number, name, or conflict tag.
- Use no on-cover text only when the visual premise is unusually self-explanatory and the WeChat article title itself will carry the hook.
- Never place more than two independent text blocks on the main wide cover. If a subtitle competes with the main hook, remove it.

### Readability Rules

- The first-read text must remain legible when the wide cover is viewed at roughly phone feed size.
- Use heavy simplified Chinese typography, strong foreground/background contrast, and a protected text zone with a solid or semi-transparent backing shape when the background is busy.
- Do not place text over the character's face, glasses, hands, or dense UI.
- Avoid thin strokes, small English labels, decorative handwritten fonts, and long sentence-style text.
- The cover should be understandable in this order: main hook or visual contradiction first, PigeonYang character second, proof object or article category third.

## Generation And Verification

- Every final prompt must include `target canvas: <width>x<height>` in addition to the aspect ratio.
- After generation, verify the actual pixel dimensions before reporting success.
- If the generated image does not match the target canvas or the requested aspect ratio, do not present it as completed. Regenerate with stricter canvas wording, or crop/resize only after confirming that the crop will not damage face, text, or proof object.
- For WeChat public account main covers, verify ratio against 2.35:1 and target canvas `2350x1000` unless the user explicitly chooses another compliant 2.35:1 size.
- For WeChat square covers, verify 1:1 and target canvas `1080x1080`.

## Questions To Ask

Ask in this order:

1. Which platform will this cover be published on?
2. If the platform has multiple cover modes, ask orientation or mode: horizontal, vertical, square, long video, short video.
3. For Bilibili, ask whether this is Bilibili-only, YouTube/Bilibili reuse, or needs 4:3-safe card display.
4. For WeChat public account articles, recommend `2.35:1 2350x1000` for the main cover and ask only whether a square sharing/secondary cover is also needed.
5. Recommend the ratio and explain the tradeoff in one sentence.
6. Ask for exact override only if the user has a platform spec or template.

