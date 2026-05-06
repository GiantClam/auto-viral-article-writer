# image-generation — AI Image Generation

## Triggers
`生成图片`, `create image`, `generate image`, `AI画图`, `draw`

## Input
- `--prompt`: Image description (required)
- `--ref`: Reference image path(s), optional for OpenAI-compatible edits or Gemini refs
- `--mask`: Optional mask image for OpenAI-compatible inpainting edits
- `--openai-image`: Use official OpenAI Images API
- `--openai-compatible-image`: Use an OpenAI-compatible Images API
- `--image-model`: Images API model (default: `gpt-image-2`)
- `--image-size`: `1024x1024`, `1536x1024`, `1024x1536`, or `auto`
- `--image-quality`: `low` / `medium` / `high` / `auto`
- `--image-format`: `png` / `jpeg` / `webp`
- `--gemini-image`: Use Google Gemini official image generation
- `--gemini-image-model`: Gemini model (default: `gemini-3.1-flash-image-preview`)
- `--output`: Output file path (required)

## Workflow

### Step 1 — Validate Inputs

Reference and mask files are optional; if provided, verify they exist.

### Step 2 — Build Command

OpenAI-compatible Images API:

```bash
python tools/nanobanana_client.py --openai-compatible-image \
  --prompt "Your image description" \
  --image-size 1536x1024 \
  --output "output/images/xxx.png"
```

Official OpenAI Images API:

```bash
python tools/nanobanana_client.py --openai-image \
  --prompt "Your image description" \
  --image-size 1536x1024 \
  --output "output/images/xxx.png"
```

Google Gemini official API:

```bash
python tools/nanobanana_client.py --gemini-image \
  --prompt "Your image description" \
  --output "output/images/xxx.png"
```

Reference image edit with OpenAI-compatible API:

```bash
python tools/nanobanana_client.py --openai-compatible-image \
  --ref "./source.png" \
  --prompt "Keep the subject and composition, restyle as a clean tech poster" \
  --image-size 1536x1024 \
  --output "output/images/edit.png"
```

### Step 3 — Execute and Parse Output

Run via subprocess, parse stdout for `Image saved:` line.

## Provider Support

| Provider | Env Variable |
|----------|-------------|
| OpenAI-compatible Images API | `OPENAI_COMPATIBLE_API_KEY`, `OPENAI_COMPATIBLE_BASE_URL` |
| OpenAI official Images API | `OPENAI_API_KEY`, optional `OPENAI_BASE_URL` |
| Google Gemini official API | `GOOGLE_AI_API_KEY` |

Default priority: OpenAI-compatible > OpenAI official > Gemini official.

## Output Format

```
Image saved: output/images/xxx.png
Size: X KB
```

## Notes

- Do not hardcode provider-specific API keys or intermediary platform names in skills or committed config.
- OpenAI-compatible APIs use `/v1/images/generations` and `/v1/images/edits`.
- `--ref` with OpenAI-compatible API uses multipart `/v1/images/edits`.
- If `background=transparent`, use `png` or `webp`, not `jpeg`.
