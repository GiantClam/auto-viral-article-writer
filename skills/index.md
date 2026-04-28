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
| **article-illustrate** | 生成插图, 文章配图, insert images, illustrate article | Auto-analyze + insert illustrations (baoyu-imagine via direct requests) |
| **image-generation** | 生成图片, create image, generate image, AI画图, draw | baoyu-imagine compatible multi-provider image gen |

## Skill Orchestration

```
user: I want to write a WeChat article about Claude Code

→ hot-topics: Research latest Claude Code trends
→ viral-patterns: Look up Claude-related viral title patterns
→ write-article: Generate full article (with illustrations via baoyu-imagine)
→ cover-image: Generate cover image via baoyu-imagine
```

## Core Tools

- `tools/nanobanana_client.py` — Image generation CLI (supports `--ref` reference photo, multi-provider: aiberm/Gemini/OpenAI/etc.)
- `tools/article_illustrate.py` — Auto-illustration for markdown articles (calls baoyu-imagine internally)
- `tools/viral_kb.py` — ViralKB database interface
- `tools/jina_reader.py` — URL → markdown fetcher
- `data/viralkb/` — ViralKB storage (patterns.jsonl + embeddings.npy)

## Provider Configuration (baoyu-imagine)

Set any of these in `config/.env`:

| Provider | Env Variable |
|----------|-------------|
| aiberm (default) | `AIBERM_API_KEY` |
| Google Gemini | `GOOGLE_AI_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| DashScope | `DASHSCOPE_API_KEY` |
| MiniMax | `MINIMAX_API_KEY` |

Default: aiberm > Google Gemini > OpenAI