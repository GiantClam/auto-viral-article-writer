# cover-image — Article Cover Generator (baoyu-cover-image compatible)

## Triggers
`生成封面`, `create cover`, `文章封面`, `cover image`

## Input
- article_slug: Article slug (extracted from filename)
- ref_photo: Reference photo path (optional — pass your own)
- style: personal_brand / cinematic / minimalist (default: personal_brand)

## Workflow

### Step 1 — Determine Reference Photo

Provide your own reference photo via `--ref`. No default ref image is bundled.

### Step 2 — Determine Title and Badge

Read first `# 【】` title from `output/wechat/{slug}-{date}.md`.
If user provided title, use directly.

Badge generated from title emotional words:
- "效率翻倍，岗位减半？" → badge: "真实访谈数据"

### Step 3 — Build Prompt

YouTube thumbnail style (personal brand version):

```
A person sits or stands on the right side of the frame (40-45% of frame),
warm orange gradient background fading to deep amber on the left,
text space on left (55-60% of frame), ultra-clean professional photo.
Amber rim light on person's hair and shoulders, cinematic warmth.
Person's face: idealized version of reference, confident expression.

Left side text space (no actual text in image — text is added later as overlay):
[Generative placeholder — keep this area clean and uncluttered]

Style: YouTube thumbnail, high contrast, bold professional aesthetic,
warm color grading, clean composition. No watermark. No signature.
```

### Step 4 — Call nanobanana_client

```bash
python tools/nanobanana_client.py --gemini-image --use-curl \
  --ref "./your-photo.jpg" \
  --prompt "YouTube thumbnail cover. Person on right (40-45% frame), half-body, amber rim light. Warm orange-to-amber gradient. Left area clean for text overlay. No watermark." \
  --aspect-ratio 16:9 \
  --output "output/images/wechat/{slug}-cover-final.png"
```

### Step 5 — Save Cover

Output path: `output/images/wechat/{slug}-cover-final.png`

## Cover Design Rules

- **Composition**: Person on right (40-45%), text area on left (55-60%)
- **Background**: Warm orange gradient → deep amber
- **Lighting**: Amber rim light (hair & shoulders)
- **Text area**: Keep clean (text added as overlay later)
- **Style**: YouTube thumbnail, high contrast, professional
- **Prohibited**: Watermark, signature, stray elements

## 5 Dimension Customization

| Dimension | Values | Default |
|-----------|--------|---------|
| **Type** | hero, conceptual, typography, metaphor, scene, minimal | auto |
| **Palette** | warm, elegant, cool, dark, earth, vivid, pastel, mono, retro, duotone, macaron | warm |
| **Rendering** | flat-vector, hand-drawn, painterly, digital, pixel, chalk, screen-print | auto |
| **Text** | none, title-only, title-subtitle, text-rich | title-only |
| **Mood** | subtle, balanced, bold | balanced |

## EXTEND.md Configuration

`config/EXTEND.md` (for baoyu-cover-image):

```yaml
# Cover image preferences
preferred_image_backend: baoyu-imagine
quick_mode: true
default_aspect: 16:9
language: zh
watermark:
  enabled: false
```

## Tools

`tools/nanobanana_client.py` — Always use `--gemini-image --use-curl`