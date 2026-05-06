# baoyu-imagine — Compatibility Alias for Image Generation

## Triggers
`baoyu-imagine`, `生成图片`, `create image`, `generate image`, `AI画图`, `draw`

## Purpose

This is a compatibility alias for users familiar with the original baoyu-imagine workflow.

The canonical implementation is `image-generation.md`.

## Backend Policy

This package only supports:
- Gemini official API
- OpenAI official Images API
- OpenAI-compatible Images API

Do not hardcode intermediary platform names, private gateways, or API keys in this skill or committed config.

## Workflow

Follow `image-generation.md`.

Recommended command:

```bash
python tools/nanobanana_client.py --openai-compatible-image \
  --prompt "Your image description" \
  --image-size 1536x1024 \
  --output "output/images/xxx.png"
```

## Upgrade Policy

When upstream baoyu-imagine changes:
- Sync trigger wording and generic usage examples here if useful.
- Add new provider-neutral features to `image-generation.md` and `tools/nanobanana_client.py`.
- Do not sync provider-specific names, private gateways, or API keys.
- Keep this file as a thin alias; avoid duplicating implementation details.

## Provider Configuration

Use `config/.env`:

| Provider | Env Variable |
|----------|-------------|
| OpenAI-compatible Images API | `OPENAI_COMPATIBLE_API_KEY`, `OPENAI_COMPATIBLE_BASE_URL` |
| OpenAI official Images API | `OPENAI_API_KEY`, optional `OPENAI_BASE_URL` |
| Gemini official API | `GOOGLE_AI_API_KEY` |
