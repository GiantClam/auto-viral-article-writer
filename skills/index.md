# Skills Index

All skills are located in the `skills/` directory and trigger on specific keywords.

## Skill List

| Skill | Triggers | Description |
|-------|----------|-------------|
| **hot-topics** | 今日热榜, AI热榜, 热门话题, 热点追踪, 今日话题, 热榜 | Multi-source (HN, Reddit, RSS) AI trending collector |
| **viral-patterns** | viral-patterns, 爆款模式, 查找爆款, 找标题公式, 参考爆款, check article structure | ViralKB pattern lookup by keyword |
| **viral-mining** | 挖掘爆款, viral mining, 发现爆款, 爆款挖掘 | Multi-source discovery + ViralKB ingestion |
| **write-article** | 写文章, 生成文章, create-article, 写篇, 公众号, 小红书 | Full pipeline: research → outline → draft → illustrate |
| **cover-image** | 生成封面, create cover, 文章封面, cover image | YouTube thumbnail style personal brand cover |
| **article-illustrate** | 生成插图, 文章配图, insert images, illustrate article | Auto-analyze + insert illustrations via Images API |
| **image-generation** | 生成图片, create image, generate image, AI画图, draw | OpenAI/Gemini/OpenAI-compatible image generation |
| **baoyu-imagine** | baoyu-imagine, 生成图片, create image, generate image | Compatibility alias for image-generation |

## Skill Orchestration

```
user: I want to write a WeChat article about Claude Code

→ hot-topics: Research latest Claude Code trends
→ viral-patterns: Look up Claude-related viral title patterns
→ write-article: Generate full article (with illustrations via image-generation)
→ cover-image: Generate cover image via image-generation
```

## Core Tools

- `tools/nanobanana_client.py` — Image generation CLI (OpenAI official, Gemini official, OpenAI-compatible)
- `tools/article_illustrate.py` — Auto-illustration for markdown articles (uses Images API internally)
- `tools/viral_kb.py` — ViralKB database interface
- `tools/jina_reader.py` — URL → markdown fetcher
- `data/viralkb/` — ViralKB storage (patterns.jsonl + embeddings.npy)

## Provider Configuration

Set any of these in `config/.env`:

| Provider | Env Variable |
|----------|-------------|
| OpenAI-compatible Images API | `OPENAI_COMPATIBLE_API_KEY`, `OPENAI_COMPATIBLE_BASE_URL` |
| OpenAI official Images API | `OPENAI_API_KEY`, optional `OPENAI_BASE_URL` |
| Google Gemini | `GOOGLE_AI_API_KEY` |

Default: OpenAI-compatible > OpenAI official > Google Gemini
