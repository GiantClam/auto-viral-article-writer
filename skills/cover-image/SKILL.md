---
name: cover-image
description: This skill should be used when the user asks to "生成封面", "文章封面", "create cover", "cover image", or wants a polished article cover image for an existing draft. It builds cover prompts and output paths around the package's article workflow.
version: 1.1.0
---

# Cover Image

Use this skill to generate a polished article cover image that matches the package's writing workflow and output conventions.

## Use This For

- cover generation for a drafted article
- thumbnail-style personal brand covers
- reference-photo-based cover composition
- WeChat article cover with 10 composition style options
- personal IP cover with 5-dimension customization (type, palette, rendering, text, mood)

## Do Not Use This For

- generic illustration generation inside article sections
- full article drafting
- open-ended visual experimentation with no article context

## Inputs

- article slug or article path
- optional explicit title
- required or recommended reference photo path
- optional style direction

## Outputs

- generated cover image saved to `output/images/wechat/`
- prompt composition based on article title, layout rules, and selected style
- cover output should reuse the same slug family as the brief and article draft when available

## 5 Dimensions Customization

This skill supports 5-dimensional customization for personalized IP covers:

| Dimension | Values | Default |
|-----------|--------|---------|
| **Type** | hero, conceptual, typography, metaphor, scene, minimal | auto |
| **Palette** | warm, elegant, cool, dark, earth, vivid, pastel, mono, retro, duotone, macaron | auto |
| **Rendering** | flat-vector, hand-drawn, painterly, digital, pixel, chalk, screen-print | auto |
| **Text** | none, title-only, title-subtitle, text-rich | title-only |
| **Mood** | subtle, balanced, bold | balanced |
| **Font** | clean, handwritten, serif, display | clean |

### Palette Descriptions

| Palette | Description |
|---------|-------------|
| warm | Orange/amber/golden tones, inviting and energetic |
| elegant | Muted, sophisticated, refined |
| cool | Blue/gray/teal tones, calm and professional |
| dark | Deep shadows, dramatic |
| earth | Brown/green/nature tones |
| vivid | Saturated, high-impact colors |
| pastel | Soft, light, gentle |
| mono | Black/white/grayscale |
| retro | Vintage-inspired hues |
| duotone | Two-tone contrast |
| macaron | Pastel with a modern twist |

### Rendering Descriptions

| Rendering | Description |
|-----------|-------------|
| flat-vector | Clean, graphic, no textures |
| hand-drawn | Sketchy, organic strokes |
| painterly | Artistic, brush-stroke feel |
| digital | Modern, clean digital art |
| pixel | Retro pixel art style |
| chalk | Chalk-like texture on dark background |
| screen-print | Halftone dots, bold colors |

## Underlying Tool (Unified)

All cover images call `tools/nanobanana_client.py`:

```bash
python tools/nanobanana_client.py --openai-compatible-image \
  --ref "img/20260423-140003.jpg" \
  --prompt "..." \
  --image-size 1536x1024 \
  --output "output/images/wechat/cover.png"
```

**Important**:
- Never write real API keys or specific relay platform names in skill or public configs
- Default: OpenAI-compatible Images API; also supports OpenAI official and Gemini official
- Default Images API model: `gpt-image-2`

## Workflow

### Step 1: Select Style

Ask the user to choose one of the 10 composition styles below:

| # | Style Name | Best For |
|---|------------|---------|
| 1 | **深色渐变风** | 人物居中，大字覆盖后方，深色渐变背景，高对比强冲击 |
| 2 | **纯色扁平风** | 干净清爽，人物+道具+纯色背景，主体高饱和 |
| 3 | **产品主视觉风** | 有 UI 截图或产品图时，截图占主体，人物做引导 |
| 4 | **对比卡片风** | 前后对比、好坏对比类内容，人物手持两张卡片推向镜头 |
| 5 | **极简留白风** | 大留白，标题是唯一焦点，克制感强 |
| 6 | **海报拼贴风** | 多张素材叠加，有前中后景纵深，叙事丰富 |
| 7 | **人物侧置留白风** | 人物偏一侧，另一边全给标题，版面大气 |
| 8 | **背影构图风** | 人物背对镜头，适合励志、启发类内容 |
| 9 | **局部出镜风** | 只露手或半张脸，产品是绝对主角 |
| 10 | **正面对视风** | 人物直视镜头，眼神接触，情绪直接强烈 |

**一次只问一个问题，等用户回答后再问下一个。**

### Step 2: Reference Photo

Ask the user if they have a face reference photo:
- **有** → let them provide the path; the prompt will include "reference photo preserves identical facial features"
- **没有** → ask them to describe the person (gender, approximate appearance); the prompt will describe directly

### Step 3: Expression (skip for 背影构图风 Style 8)

Ask them to choose one:

1. 捂嘴惊讶 — 双手捂嘴，眼睛睁大，震惊感
2. 张嘴震惊 — 嘴巴微张，眼神放大，强烈惊讶
3. 开心大笑 — 嘴角上扬，眼睛弯起，真实喜悦
4. 兴奋雀跃 — 眉飞色舞，身体前倾，藏不住的激动
5. 自信得意 — 嘴角微扬，眼神笃定
6. 托腮思考 — 单手托腮，眼神若有所思
7. 推荐种草感 — 微笑点头，眼神看向镜头
8. 交给模型决定

### Step 4: Extra Materials

Ask if they have any additional materials (product screenshots, UI images, brand assets) as 图2, 图3 etc:
- **有** → ask how many and what each one is
- **没有** → skip

### Step 5: Background Color

1. 浅色系 — 白/米白/浅灰，干净清爽
2. 深色系 — 深灰/墨黑，沉稳有力
3. 暖色调 — 米黄/暖棕/柔橙，温暖感
4. 冷色调 — 浅蓝灰/青灰，冷静专业
5. 高饱和撞色 — 模型根据选题自选高对比色
6. 交给模型决定

Note: 极简留白风(5) and 人物侧置留白风(7) default to light backgrounds; this step can be skipped or simplified for those.

### Step 6: Font Style

1. 超粗黑体 — 粗壮有力，干货/科技类首选
2. 柔和圆体 — 圆角笔画，温暖亲切
3. 手写涂鸦体 — 笔触自然，个性感强
4. 极简无衬线 — 笔画均匀，国际范
5. 复古宋体 — 有衬线，古典怀旧感
6. 交给模型决定

### Step 7: Font Color Effect

1. 纯白 — 深色背景首选，干净清晰
2. 纯黑 — 浅色背景首选，沉稳有力
3. 渐变色 — 模型根据背景色调自选
4. 描边效果 — 字体加轮廓，增加层次感
5. 交给模型决定

### Step 8: Cover Title

Extract 1-3 candidate titles from the article (4-8 characters each), present them to the user for confirmation or modification.

---

### Step 9: Generate Prompt

After collecting all answers, generate the prompt using the appropriate style template (see Prompt Templates section below).

**Core requirements for all prompts:**
- **Person pose specific**: describe body position, hand placement, action details — no vague descriptions like "she made a gesture"
- **Subject elements detailed**: what the main visual element looks like, what's on it, size ratio, static or dynamic
- **Spatial relationships clear**: foreground / midground / background, who overlaps whom
- **Each style has its own background and font logic**: do not reuse the same color/font across all styles

---

### Step 10: Generate Image

1. Call `tools/nanobanana_client.py` with `--openai-compatible-image --ref <path>` (reference photo if available)
2. If provider call fails with 429 or network error, report failure clearly. **Do not silently replace with a local pasted-photo composition.**
3. Save output to `output/images/wechat/{slug}-cover-final.png`

---

## Fallback Guidance

- If no reference image is available, tell the user the cleanest personal-brand result still depends on a user-supplied portrait.
- If no article exists yet, ask for a title or article path before generating the cover.
- If user explicitly asked for reference-photo-based generation and the provider call fails, report that failure clearly. Do not silently replace it with a local pasted-photo composition and call it generated.
- If the provider is unavailable or rate-limited, wait for reset rather than falling back to local composition.

---

## Prompt Rule For Reference Photos

When a reference photo is used, write prompts that ask the model to:

- preserve the same person's identity
- recompose the subject into an editorial portrait
- integrate the subject naturally into the scene
- avoid collage / cutout / sticker-like results

Avoid prompts that merely describe "put a person on the right side" because they encourage pasted-subject composition.

The reference photo is used to give the AI model a facial identity to maintain, not to paste that exact photo into the scene.

---

## Prompt Templates

### Style 1: 深色渐变风 (Dark Gradient)

```
[Gender] figure, reference photo preserves identical facial features, bust/half-body shot.

[Expression description], [body position and pose], [specific hand action: right hand / left hand],
[main visual element's narrative behavior — describe clearly what is happening between person and element],
[main visual element detailed description: shape / content / size / dynamic],
(if additional refs: [ref编号] as [specific presentation and position])

Massive Chinese text "[Cover Title]" overlaid behind the figure, [font style], [color effect], partially obscured by figure and main elements, creating visual hierarchy

Background: [dark gradient — deep purple-gray / dark blue-black / charcoal], smooth gradient transition

All elements concentrated in central area, margins preserved top and bottom, within safe zone

Foreground: scattered extremely small [theme-related icons], minimal quantity, purely decorative, partially overlapping text edges

Floating elements with soft shadows, layered depth, high saturation, organized chaos aesthetic
```

### Style 2: 纯色扁平风 (Flat Solid Color)

```
[Gender] figure, reference photo preserves identical facial features, bust/half-body shot.

[Expression], [body pose], [hand action: pushing / lifting / displaying],
[main prop] occupies large area of the frame, strong motion blur, intense near-large-far-small perspective,
[main prop detailed description: appearance / content / material],
(if ref2: [prop/interface] displaying ref2 content, minimal and clean)

Background: [solid flat color — teal / coral / purple], pure flat, no gradient

Massive Chinese "[Cover Title]" at [top/center], [font style], [color effect],
font partially obscured by main subject, creating visual hierarchy

Foreground: scattered tiny [theme-related icons], soft shadows, partially overlapping text edges

Main subject high saturation, background low saturation, clear contrast
```

### Style 3: 产品主视觉风 (Product Hero)

```
[Gender] figure, reference photo preserves identical facial features, bust/half-body, figure smaller in proportion.

Figure positioned at [left/right] lower portion, ~25% of frame, [specific guiding gesture: right hand pointing toward / body turned toward],
[expression], eyes directed toward main visual,

Ref2 as the main visual of the frame, ~65% of frame, [specific presentation: floating in air / unfolding beside figure / filling background],
[ref2 content detailed description: which parts of interface are clearly visible, white base or dark base, content layout],
(if ref3: ref3 as [specific position and presentation])

"[Cover Title]", [font style], [color effect],压在产品[顶部/一侧]边缘，形成层次感

Background: [light / neutral tone, making product the absolute protagonist]

All elements within central area, safe zone, soft shadows, layered depth
```

### Style 4: 对比卡片风 (Contrast Cards)

```
[Gender] figure, reference photo preserves identical facial features, bust/half-body shot.

[Expression — must have strong contrast feeling: triumphant / shocked / promotional], centered,
left hand holding a [small/dim/worn-looking] card, distant perspective,
card displays "[Card B content — represents before/bad side]", [card B visual description],
right hand thrusting a [large/bright/glowing] card hard toward camera lens,
card displays "[Card A content — represents after/good side]", [card A visual description],
foreground card occupies large area, strong motion blur, intense near-large-far-small perspective,
the two cards [specific contrast relationship], strong contrast,

Massive Chinese "[Cover Title]" overlaid behind figure, [font style], [color effect], forming visual hierarchy

Background: [tone — dark to make card contrast stand out]

All elements within central area, safe zone

Floating elements with soft shadows, foreground small elements partially overlapping text edges
```

### Style 5: 极简留白风 (Minimalist White Space)

```
[Gender] figure, reference photo preserves identical facial features, bust/half-body, smaller proportion.

Figure positioned at [lower-left / lower-right / side], ~20% of frame, [simple pose],
[light expression — not over-the-top], eyes/body directed toward white space area,

[Opposite side of frame] ~65% is large [white/cream/light gray] white space,
massive Chinese "[Cover Title]" occupying the white space area, [font style — thin to medium weight], [dark color],
character spacing open, breathing room,
(if subtitle: one line small gray text below, as supplementary info),

Background: overall [light tone], minimal, no decoration

Composition restrained, white space is part of the design, within safe zone
```

### Style 6: 海报拼贴风 (Poster Collage)

```
[Gender] figure, reference photo preserves identical facial features, bust/half-body shot.

[Expression], [pose and body position],

Foreground: [foreground element detailed description — size, position, visual details], ~[ratio] of frame, with slight shadow and floating feel,
Midground: main figure, with overlapping relationship with foreground element, [which part of figure is overlapped by foreground],
Background: [background element description — lightly blurred, content summarized], [count] pieces, staggered arrangement, as background layer,
all elements have front-back overlap relationships, creating layers and depth,

Massive Chinese "[Cover Title]", [font style], [color — white or white with outline recommended],
positioned between figure and foreground elements, forming overlap relationship with multiple layers,

Background: [deep steady tone — dark navy / charcoal], making each layer stand out

All elements within central area, safe zone, floating elements with slight shadows, strong layering
```

### Style 7: 人物侧置留白风 (Figure Offset White Space)

```
[Gender] figure, reference photo preserves identical facial features, bust/half-body shot.

Figure positioned at [left/right] side of frame, ~30% width, [specific pose],
[expression], eyes and body naturally facing [opposite white space area],

[Opposite side] ~65% is large white space,
massive Chinese "[Cover Title]" filling the white space area, [font style], [dark color],
[arrangement: vertical top-to-bottom / horizontal split-two-lines / main large + secondary small],
(if supplementary info: one line small gray text below title),

Background: [neutral or light tone, soft overall]

Figure and text retain sufficient breathing room, not cramped, within safe zone
```

### Style 8: 背影构图风 (Back View Composition)

```
[Gender] figure from behind, only back of head, shoulders, and back visible, hair strands clear, no face shown,

[specific action: looking up toward front / arms spread / walking slowly forward], [body pose description — sense of motion],
in front of [or above] figure is [main visual element detailed description: content / size / state / dynamic],
[spatial relationship between main visual element and figure],

Massive Chinese "[Cover Title]" at [above / left-right sides of] figure, [font style], [color effect],
generous character spacing, sufficient contrast with background,

Background: [grand deep gradient — sense of breadth and depth], creating expansive depth

Frame has [narrative feeling: release / departure / arrival], strong immersion, within safe zone
```

### Style 9: 局部出镜风 (Partial Appearance)

```
Main subject is [product/screenshot/card detailed description: content layout / color / key information],
~[ratio] of frame, [white base or color], clear and sharp,
(if ref2: main content is ref2, [ref2 display method])

[Lower-right corner / left edge / bottom edge] partially appears:
reference photo [hand close-up / half face / side profile],
[specific partial action: index finger lightly touching / picking up / pointing at a location],
[partial appearance details: hand pose / face direction / distance relationship with main subject],

"[Cover Title]", [font style], [color effect], pressed at [top / left / bottom] of main subject

Background: [light / neutral — making main subject the absolute focus]

Product is the focus, figure is merely the witness, within safe zone
```

### Style 10: 正面对视风 (Direct Eye Contact)

```
[Gender] figure, reference photo preserves identical facial features, bust/half-body, facing camera directly.

[Expression — must be strong and clear], [hand/body coordinated pose], forming strong eye contact with viewer,

"[Cover Title — first half]" [count] characters above figure's face, [font style], [color effect], very large,
"[Cover Title — second half]" [count] characters below figure's face, [font style], [color effect], slightly smaller,
two lines of text above and below the face, forming a natural frame, not obscuring eyes or mouth,
text has breathing room from the face,
(if decoration: one extremely small [theme icon] floating on each side of the face, slight shadow)

Background: [tone — high saturation solid color or dark gradient, high contrast with figure]

Figure is absolute focus, frame direct and powerful, emotion overflowing, within safe zone
```

---

## Quick Generation Commands (Person IP Cover)

```bash
# With reference photo (default), generate person IP cover
python tools/nanobanana_client.py --openai-compatible-image \
  --ref "img/20260423-140003.jpg" \
  --prompt "Photorealistic WeChat cover. Person on right side (40-45% frame), half-body, confident smile, amber rim light. Left side: large orange Chinese headline '效率翻倍，岗位减半？' with three icon tags. Warm orange-to-amber gradient background. NO watermark." \
  --image-size 1536x1024 \
  --output "output/images/wechat/article-cover.png"

# Without reference photo (pure AI imagination)
python tools/nanobanana_client.py --openai-compatible-image \
  --prompt "..." \
  --image-size 1536x1024 \
  --output "output/images/wechat/cover-no-ref.png"
```

**Note**: When title is long, do not rely on `--article-title` (it bypasses ref image and uses generations interface, reducing person similarity). Write all text information directly into `--prompt` with `--ref` to use img2img interface.

## Confirmation Strategy

When `quick_mode: true` is set in EXTEND.md, skip all confirmation steps and generate directly.

When confirmation is needed each time, use this tool call order:
1. Caller first confirms dimensions / aspect ratio / copy / backend selection
2. Only skip when caller explicitly says "generate directly" or "--quick"

## EXTEND.md Configuration Example

To apply default settings, create `EXTEND.md` in the skill root:

```yaml
preferred_image_backend: openai-compatible
quick_mode: false
default_aspect: 16:9
language: zh
cover_mode: personal_brand
brand_name: Your Name
brand_palette:
  primary: "#0E1A2B"
  accent: "#F59E0B"
layout_style: youtube-thumbnail
watermark:
  enabled: false
```

## References

- `references/cover-rules.md` - composition, palette, and output conventions
- `../../docs/overview/article-artifact-family.md` - recommended file family for brief, draft, cover, and inline images
- `../../docs/overview/slug-rules.md` - how to generate and reuse a stable slug