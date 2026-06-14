# Skills Index

All skills are located in the `skills/` directory and trigger on specific keywords. The most complex skills use directory-style packaging with `SKILL.md` and optional `references/` files.

## Skill List

| Skill | Triggers | Description |
|-------|----------|-------------|
| **hot-topics** | 今日热榜, AI热榜, 热门话题, 热点追踪, 今日话题, 热榜 | Multi-source trending collector with source ranking and optional ViralKB ingestion |
| **last30days** | last30days, /last30days, 深度研究, research topic, 过去30天 | Deep research across Reddit/X/YouTube/HN/Polymarket/GitHub, synthesized into one brief |
| **research-brief** | 先研究一下, 帮我先梳理这个题, research brief, deep brief | Converts a promising topic into a source-backed article brief before drafting |
| **viral-patterns** | viral-patterns, 爆款模式, 查找爆款, 找标题公式, 参考爆款, check article structure | ViralKB pattern lookup by keyword |
| **viral-mining** | 挖掘爆款, viral mining, 发现爆款, 爆款挖掘 | Multi-source discovery + ViralKB ingestion |
| **write-article** | 写文章, 生成文章, create-article, 写篇, 公众号, 小红书 | Full pipeline: research -> outline -> draft -> illustrate |
| **repurpose-content** | 改写成 X 版本, 改成小红书, repurpose this article | Turn one mother draft into multiple native platform versions |
| **article-score-retro** | score this post, predict this, retro this post | Pre-publish scoring, blind prediction, and post-publish retrospective |
| **platform-rubric-manager** | update wechat rubric, review x rubric | Manage and evolve one scoring rubric per platform |
| **multi-platform-content** | 做一套多平台内容包, run the multi-platform workflow | Orchestrate article drafting, repurposing, scoring, prediction, and retro |
| **article-audit** | 检查这篇文章是否齐全, 审计这篇文章, article audit, publish ready | Audits one article slug across brief, draft, cover, and inline image artifacts |
| **cover-image** | 生成封面, create cover, 文章封面, cover image | YouTube thumbnail style personal brand cover |
| **article-illustrate** | 生成插图, 文章配图, insert images, illustrate article | Auto-analyze + insert illustrations via Images API |
| **image-generation** | 生成图片, create image, generate image, AI画图, draw | Direct image generation across configured providers |
| **baoyu-imagine** | baoyu-imagine, 生成图片, create image, generate image | Compatibility alias for image-generation |
| **package-neat** | 整理一下, 同步文档, 收尾, release audit, skill audit | Syncs package docs, manifests, and public-facing repository metadata |

## Skill Orchestration

```
user: I want to write a WeChat article about Claude Code

→ hot-topics: Research latest Claude Code trends (daily discovery)
→ last30days: Deep research on Claude Code ecosystem (deep investigation)
→ research-brief: Turn the topic into a stronger article brief
→ viral-patterns: Look up Claude-related viral title patterns
→ write-article: Generate full mother draft
→ repurpose-content: Create native platform variants
→ article-score-retro: Score and predict before publish; retro after publish
→ platform-rubric-manager: Update platform judgment standards from repeated signals
→ article-audit: Check whether the article family is publish-ready
→ cover-image: Generate cover image via image-generation
```

**hot-topics vs last30days:**
- `hot-topics` — daily discovery: what's trending today across AI?
- `last30days` — deep research: what's the complete picture of one topic over 30 days?

The two are complementary: `hot-topics` feeds the discovery layer; `last30days` handles the investigation layer.

## Core Tools

- `tools/nanobanana_client.py` — Image generation CLI (OpenAI official, Gemini official, OpenAI-compatible)
- `tools/article_illustrate.py` — Auto-illustration for markdown articles (uses Images API internally)
- `tools/viral_kb.py` — ViralKB database interface
- `tools/jina_reader.py` — URL → markdown fetcher
- `data/viralkb/` — ViralKB storage (patterns.jsonl + embeddings.npy)

## Layout Conventions

- `skills/<name>/SKILL.md` - canonical skill entry point for complex skills
- `skills/<name>/references/` - extra guidance loaded only when needed
- all package skills now use directory-style entries with `SKILL.md`

## Provider Configuration

Set any of these in `config/.env`:

| Provider | Env Variable |
|----------|-------------|
| OpenAI-compatible Images API | `OPENAI_COMPATIBLE_API_KEY`, `OPENAI_COMPATIBLE_BASE_URL` |
| OpenAI official Images API | `OPENAI_API_KEY`, optional `OPENAI_BASE_URL` |
| Google Gemini | `GOOGLE_AI_API_KEY` |

Default: OpenAI-compatible > OpenAI official > Google Gemini
