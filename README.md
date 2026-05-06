# Auto Viral Article Writer

AI article writing pipeline for agents: hot topics → viral patterns → article drafting → illustrations → cover image.

**Supported Platforms:** OpenCode, Codex, Claude Code, OpenClaw, Hermes

---

## First-Time Setup

### Step 1 — Run Setup Wizard

After installing, say "配置" or "setup" to start the setup wizard:

```bash
python scripts/setup.py
```

This will:
1. Prompt you to select hot topic directions (AI工具, SaaS, AI出海, etc.)
2. Choose which platforms to monitor (小红书, 知乎, B站, Twitter)
3. Verify opencli connection
4. Test all skills

### Step 2 — Install Dependencies

```bash
pip install python-dotenv requests feedparser numpy
```

### Step 3 — Configure API Keys

```bash
cp config/.env.example config/.env
```

Edit `config/.env`, fill in at least one key:

```bash
# Image generation (required for cover + illustrations)
OPENAI_COMPATIBLE_API_KEY=your_key_here
OPENAI_COMPATIBLE_BASE_URL=https://your-openai-compatible-base-url
# OR
OPENAI_API_KEY=your_openai_key_here
# OR
GOOGLE_AI_API_KEY=your_google_key_here

# Content research
JINA_API_KEY=your_jina_key_here            # Optional but recommended
```

Get keys:
- OpenAI: https://platform.openai.com/api-keys
- Google AI Studio: https://aistudio.google.com
- Jina Reader: https://jina.ai/reader (free tier available)

### Step 4 — Create Output Directories

```bash
mkdir -p output/wechat output/images/wechat data/viralkb
```

### Step 5 — Verify Installation

```bash
python tools/config_loader.py
```

Should print "Configuration valid!" if keys are configured.

Or check opencli connection:

```bash
python tools/opencli_fetcher.py --check
```

---

## Quick Test

```bash
# Test image generation (requires OpenAI-compatible, OpenAI, or Gemini credentials)
python tools/nanobanana_client.py --openai-compatible-image \
  --prompt "A warm orange gradient background" \
  --output output/images/test.png
```

If this succeeds, the tool chain is working.

---

## Skill Index

| Skill | Triggers | What It Does |
|-------|----------|--------------|
| **setup** | 配置, setup, 设置 | First-time setup wizard, configure hot topics, verify dependencies |
| **hot-topics** | 今日热榜, AI热榜, 热门话题 | Collects trending from HN, Reddit, 小红书, 知乎, B站, Twitter |
| **viral-patterns** | 爆款模式, 查找爆款, 找标题公式 | Searches ViralKB for viral patterns |
| **viral-mining** | 挖掘爆款, viral mining | Discovers viral content → ViralKB |
| **write-article** | 写文章, 生成文章, 公众号 | Full pipeline: research → draft → illustrate |
| **cover-image** | 生成封面, cover image | YouTube thumbnail cover (needs `--ref` photo) |
| **article-illustrate** | 生成插图, 文章配图 | Auto-generates + inserts illustrations |
| **image-generation** | 生成图片, create image | Direct image generation |
| **baoyu-imagine** | baoyu-imagine, 生成图片 | Compatibility alias for image-generation |

### Pipeline Flow

```
setup (first time) → hot-topics → viral-patterns → write-article → cover-image
                              ↓
                       article-illustrate (插图自动插入正文)
```

---

## Directory Structure

```
skill-packaging/
├── README.md
├── MANIFEST.txt
├── skills/
│   ├── index.md              ← Skill directory overview
│   ├── setup.md              ← First-time setup wizard
│   ├── hot-topics.md         ← Trending topic collector (reads user_preferences.json)
│   ├── viral-patterns.md     ← ViralKB pattern lookup
│   ├── viral-mining.md       ← Viral content discovery → ViralKB
│   ├── write-article.md      ← Full article pipeline
│   ├── cover-image.md        ← YouTube thumbnail cover generator
│   ├── article-illustrate.md ← Auto-illustration for articles
│   ├── image-generation.md   ← Direct image generation
│   └── baoyu-imagine.md      ← Compatibility alias for image-generation
├── tools/
│   ├── nanobanana_client.py    ← Image gen: OpenAI/Gemini/OpenAI-compatible CLI
│   ├── article_illustrate.py   ← Auto-illustrate: analyze → generate → insert
│   ├── config_loader.py        ← Load .env, validate API keys
│   ├── jina_reader.py          ← URL → markdown (research)
│   ├── viral_kb.py             ← ViralKB interface (patterns.jsonl + embeddings)
│   └── opencli_fetcher.py      ← Social media fetcher (--check to verify connection)
├── config/
│   ├── .env.example             ← API key template
│   ├── EXTEND.md                ← Image generation default settings
│   └── user_preferences.json.example  ← User preferences template
├── scripts/
│   ├── setup.py               ← Interactive first-time setup wizard
│   └── example_workflow.py     ← Demo of the full pipeline
└── data/
    └── viralkb/                ← ViralKB storage (created on first run)
```

---

## User Preferences

After running setup, your preferences are saved to `config/user_preferences.json`:

```json
{
  "hot_topics": ["AI工具", "SaaS", "AI出海"],
  "default_platforms": ["xiaohongshu", "zhihu", "bilibili", "twitter"],
  "output_dir": "output",
  "opencli_configured": true
}
```

hot-topics skill reads these preferences to filter content by your selected topics.

---

## Core Tool Usage

### nanobanana_client.py (Image Generation)

```bash
# OpenAI-compatible Images API
python tools/nanobanana_client.py --openai-compatible-image \
  --prompt "Your image description" \
  --output "output/images/xxx.png"

# With reference photo via OpenAI-compatible edits API
python tools/nanobanana_client.py --openai-compatible-image \
  --ref "./your-photo.jpg" \
  --prompt "Professional portrait, warm tones" \
  --output "output/images/portrait.png"
```

Key args:
- `--openai-compatible-image` — Use OpenAI-compatible Images API
- `--openai-image` — Use official OpenAI Images API
- `--gemini-image` — Use official Gemini image generation
- `--prompt` — Image description
- `--ref` — Reference photo path for supported providers
- `--output` — Output file path
- `--image-size` — 1024x1024 / 1536x1024 / 1024x1536 / auto
- `--image-quality` — low / medium / high / auto

### article_illustrate.py (Auto-Illustrate)

```bash
python tools/article_illustrate.py output/wechat/article.md
python tools/article_illustrate.py output/wechat/article.md --density balanced --max-images 3
```

This generates images for each `**bold section**` in the article and inserts them below the matching heading.

### jina_reader.py (URL → Markdown)

```python
from jina_reader import extract_content

markdown = extract_content(api_key=None, url="https://example.com/article", verbose=True)
```

### viral_kb.py (ViralKB Search)

```python
from viral_kb import ViralKB
kb = ViralKB()
results = kb.search("Claude Code", limit=10)
```

### opencli_fetcher.py (Social Media Fetcher)

Requires `opencli` CLI + Chrome extension. Fetches real-time viral content.

```bash
# Check if opencli is available
python tools/opencli_fetcher.py --check

# Xiaohongshu viral feed
python tools/opencli_fetcher.py --platform xiaohongshu --limit 10

# Zhihu hot search
python tools/opencli_fetcher.py --platform zhihu --limit 10

# Bilibili hot
python tools/opencli_fetcher.py --platform bilibili --limit 10

# Twitter trending
python tools/opencli_fetcher.py --platform twitter --limit 10

# Reddit hot posts
python tools/opencli_fetcher.py --platform reddit --limit 10

# HackerNews
python tools/opencli_fetcher.py --platform hackernews --limit 10
```

Requirements: Chrome browser with OpenCLI Browser Bridge extension installed and enabled.

---

## Skills Detail

### setup

First-time setup wizard that:
1. Prompts user to select hot topic directions (3-5 from: AI工具, 科技, 编程, 商业, AI出海, 效率工具, AI创业, 全部)
2. Chooses default platforms (小红书, 知乎, B站, Twitter)
3. Verifies opencli connection
4. Tests core functionality
5. Saves preferences to `config/user_preferences.json`

### hot-topics

Collects AI trending from:
- **opencli**: 小红书, 知乎, B站, Twitter (requires Chrome + extension)
- **RSS**: HN, Reddit (r/MachineLearning, r/artificial, r/singularity)

Reads `config/user_preferences.json` to filter by user's selected hot_topics.

5 categories: AI工具, 模型更新, AI应用, 算法突破, AI出海.

Output:
```
## 今日热榜 [AI工具, SaaS, AI出海]

### 小红书
1. **[标题]** ▲ 1234 likes

### 知乎
1. **[标题]** 热度: 4183万 | 回答: 150

### Twitter/X
1. **#话题** 分类
```

### viral-patterns

Searches `data/viralkb/` (patterns.jsonl) for viral title formulas by keyword.

Run `viral-mining` skill first to populate ViralKB.

### viral-mining

Parallel RSS/HN crawler → discovers viral content → ingests into ViralKB.

Signal score calculated from engagement metrics.

### write-article

Full pipeline:
1. hot-topics research (reads user preferences)
2. viral-patterns lookup
3. Jina Reader data collection
4. Gemini outline (5 title candidates + `**bold sections**`)
5. Full article draft
6. article-illustrate auto-illustration

Output: `output/wechat/{slug}-{date}.md`

Article format:
- `# 【标题候选】` — title candidates (H1)
- `---` — divider
- `**章节名**` — bold section headings
- `![alt](path)` — inserted images

### cover-image

YouTube thumbnail style cover:
- **Composition**: Person on right (40-45%), text area on left (55-60%)
- **Background**: Warm orange → deep amber gradient
- **Lighting**: Amber rim light on hair/shoulders
- **Prohibited**: Watermark, signature

⚠️ **You must provide `--ref ./your-photo.jpg`** — no default photo is bundled.

```bash
python tools/nanobanana_client.py --gemini-image --use-curl \
  --ref "./your-portrait.jpg" \
  --prompt "YouTube thumbnail cover. Person on right (40-45% frame)... NO watermark." \
  --output "output/images/wechat/cover.png"
```

### article-illustrate

Analyzes `**bold sections**` → generates one image per section → inserts `![alt](path)` below heading.

Image types: infographic, comparison, flowchart, framework, timeline, scene (auto-detected).

Spot detection rules:
- Matches `**section name**` (bold headings)
- Excludes `#` prefixed lines (title candidates)
- Excludes empty body sections
- Excludes numbered items `**1. xxx**`
- Only inserts into post-`---` body

### image-generation

Direct image generation without the article pipeline.

Use when you need a specific image outside the article workflow.

---

## Windows PowerShell Note

`curl` is aliased to `Invoke-WebRequest` in PowerShell. All tools in this package use Python `requests` directly to avoid this issue. **Do not call `subprocess.run(['curl', ...])`**.

The correct pattern is:
```bash
python tools/nanobanana_client.py --openai-compatible-image ...
```
The tool uses Python requests internally for OpenAI-compatible and OpenAI image calls.

---

## Troubleshooting

### "No API key provided"

Edit `config/.env` and add at least one key:
```bash
OPENAI_COMPATIBLE_API_KEY=your_key_here
OPENAI_COMPATIBLE_BASE_URL=https://your-openai-compatible-base-url
# OR
OPENAI_API_KEY=your_key_here
# OR
GOOGLE_AI_API_KEY=your_key_here
```

### "curl: command not found" or curl acts weird

Prefer OpenAI-compatible or OpenAI image calls, which use Python requests directly. If using Gemini from Windows PowerShell, pass `--use-curl` to force the requests path.

### "Reference image not found"

Cover image requires you to provide `--ref ./your-photo.jpg`. No default photo is bundled.

### viral-patterns returns nothing

Run `viral-mining` skill first to populate `data/viralkb/patterns.jsonl`.

### article_illustrate.py generates but no images appear

Check that your article has `**bold section headings**` after the `---` divider. The tool only processes post-divider content.

### opencli returns "No results found"

1. Ensure Chrome browser is running with target site logged in
2. Check OpenCLI Browser Bridge extension is installed and enabled
3. Run `opencli doctor` to verify connection
4. Run `python tools/opencli_fetcher.py --check` for detailed diagnostics

### First-time setup not prompted

Say "配置" or "setup" or "设置" to start the setup wizard manually:
```bash
python scripts/setup.py
```

---

## Agent Usage Pattern

1. Say "配置" to run first-time setup (or "配置" to update preferences)
2. Load `skills/index.md` — see available skills
3. Identify skill by trigger word
4. Load that skill file — follow workflow steps
5. Execute using tools in `tools/` directory
6. All paths are relative to skill-packaging root
