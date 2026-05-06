# article-illustrate — Auto-Generate and Insert Illustrations into Article

## Triggers
`生成插图`, `文章配图`, `insert images`, `illustrate article`

## Input
- article_path: Article markdown file path
- style: Illustration style (e.g., "tech Illustration", "flat design")
- count: Number of images to generate (default: 3)

## Workflow

### Step 1 — Analyze Article Structure

Use `analyze_article(article_path)` to extract:
- All `**bold section**` headings
- Filter rules:
  - Exclude lines starting with `#` (title candidates)
  - Exclude sections with empty body
  - Exclude numbered items like `**1. xxx**`

```python
from tools.article_illustrate import analyze_article

spots = analyze_article(article_path)
# Returns: [{'section': 'Product Paradox', 'content': '...', 'type': 'scene'}, ...]
```

### Step 2 — Determine Illustration Positions

Each bold section heading below (exact match, not sequential insertion).

### Step 3 — Generate Image for Each Position

Call `generate_image()` to create illustration:

```python
from tools.article_illustrate import generate_image

for spot in spots:
    img_path = generate_image(
        prompt=f"{spot['type']} illustration for: {spot['section']}. {spot['content'][:200]}",
        output_path=f"output/images/wechat/{slug}-{idx}.png",
        aspect="16:9",
        quality="2k"
    )
    spot['image_path'] = img_path
```

Image generation uses requests directly to an Images API:
- Endpoint: `{base_url}/v1/images/generations`
- Model: `gpt-image-2` by default
- Auth: `Bearer {OPENAI_COMPATIBLE_API_KEY}` or `Bearer {OPENAI_API_KEY}`
- Params: `size`, `quality`, `background`, `output_format`, `moderation`, `n`

Illustration types mapped to prompts:
- `infographic` — data/figure content
- `comparison` — vs/versus content
- `flowchart` — step/process content
- `framework` — model/architecture content
- `timeline` — historical/chronological content
- `scene` — case study/story content

### Step 4 — Insert Images into Markdown

Use `insert_images_into_article()` to write image paths into file:

```python
from tools.article_illustrate import insert_images_into_article

insert_images_into_article(article_path, spots)
```

### Step 5 — Save Updated Article

Modification done in-place on original file.

## Core Functions

### `analyze_article(article_path)`
Returns section list, each containing `section`, `content`, `type`.

### `generate_image(prompt, output_path, aspect, quality)`
Direct requests to OpenAI-compatible or OpenAI official Images API using `gpt-image-2` by default. Supports aspect: 16:9 / 1:1 / 4:3 / 3:4 / 9:16.

### `insert_images_into_article(article_path, spots)`
Exact match `**section**` then insert `![alt](path)`.

## Notes

- Images only inserted into body after `---` divider
- Title lines (like `# 【Title】`) not matched
- One image per position
- Alt text from section's own section name
- No `--use-curl` needed (uses Python `requests` directly, not subprocess)

## Tool Dependencies

- `tools/article_illustrate.py` — Contains `analyze_article`, `generate_image`, `insert_images_into_article`
- `tools/nanobanana_client.py` — Not used by article_illustrate.py (generates images via direct requests instead)
- Both tools share the same OpenAI-compatible/OpenAI official Images API configuration
