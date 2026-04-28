# NanoBanana Skills

AI article writing pipeline for agents: hot topics → viral patterns → article drafting → illustrations → cover image.

For: Codex, Claude Code, OpenCode, OpenClaw, Hermes.

---

## Setup (Agent Instructions)

### Step 1 — Install Dependencies

```bash
pip install python-dotenv requests feedparser numpy
```

### Step 2 — Configure API Keys

```bash
cp config/.env.example config/.env
```

Edit `config/.env`, fill in at least one key:

```bash
# Image generation (required for cover + illustrations)
AIBERM_API_KEY=your_aiberm_key_here        # Recommended (faster, reference image support)
# OR
GOOGLE_AI_API_KEY=your_google_key_here      # Fallback

# Content research
JINA_API_KEY=your_jina_key_here            # Optional but recommended
```

**aiberm vs Google:**
- aiberm supports reference images (`--ref`) → use for cover image with personal photo
- Google Gemini does not support reference images
- Both work for article illustrations

Get keys:
- aiberm: https://aiberm.com (registration required)
- Google AI Studio: https://aistudio.google.com
- Jina Reader: https://jina.ai/reader (free tier available)

### Step 3 — Create Output Directories

```bash
mkdir -p output/wechat output/images/wechat data/viralkb
```

### Step 4 — Verify Installation

```bash
python tools/config_loader.py
```

Should print "Configuration valid!" if keys are configured.

---

## Quick Test

```bash
# Test image generation (requires AIBERM_API_KEY or GOOGLE_AI_API_KEY)
python tools/nanobanana_client.py --gemini-image --use-curl \
  --prompt "A warm orange gradient background" \
  --output output/images/test.png
```

If this succeeds, the tool chain is working.

---

## Skill Index

| Skill | Triggers | What It Does |
|-------|----------|--------------|
| **hot-topics** | 今日热榜, AI热榜, 热门话题 | Collects AI trending from HN, Reddit, RSS |
| **viral-patterns** | 爆款模式, 查找爆款, 找标题公式 | Searches ViralKB for viral patterns |
| **viral-mining** | 挖掘爆款, viral mining | Discovers viral content → ViralKB |
| **write-article** | 写文章, 生成文章, 公众号 | Full pipeline: research → draft → illustrate |
| **cover-image** | 生成封面, cover image | YouTube thumbnail cover (needs `--ref` photo) |
| **article-illustrate** | 生成插图, 文章配图 | Auto-generates + inserts illustrations |
| **image-generation** | 生成图片, create image | Direct image generation (baoyu-imagine) |

### Pipeline Flow

```
hot-topics → viral-patterns → write-article → cover-image
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
│   ├── index.md              ← Skill directory (load this first)
│   ├── hot-topics.md
│   ├── viral-patterns.md
│   ├── viral-mining.md
│   ├── write-article.md
│   ├── cover-image.md
│   ├── article-illustrate.md
│   └── image-generation.md
├── tools/
│   ├── nanobanana_client.py    ← Image gen: baoyu-imagine CLI (--gemini-image --use-curl)
│   ├── article_illustrate.py    ← Auto-illustrate: analyze → generate → insert
│   ├── config_loader.py        ← Load .env, validate API keys
│   ├── jina_reader.py          ← URL → markdown (research)
│   └── viral_kb.py             ← ViralKB interface (patterns.jsonl + embeddings)
├── config/
│   ├── .env.example             ← API key template
│   └── EXTEND.md                ← baoyu-imagine default settings
└── scripts/
    └── example_workflow.py      ← Demo of the full pipeline
```

---

## Core Tool Usage

### nanobanana_client.py (Image Generation)

```bash
# Windows PowerShell: ALWAYS use --gemini-image --use-curl
python tools/nanobanana_client.py --gemini-image --use-curl \
  --prompt "Your image description" \
  --output "output/images/xxx.png"

# With reference photo (aiberm only, --ref is your photo path)
python tools/nanobanana_client.py --gemini-image --use-curl \
  --ref "./your-photo.jpg" \
  --prompt "Professional portrait, warm tones" \
  --output "output/images/portrait.png"
```

Key args:
- `--gemini-image` — Required flag
- `--use-curl` — Required on Windows (avoids PowerShell curl alias)
- `--prompt` — Image description
- `--ref` — Your reference photo path (optional, aiberm supports it)
- `--output` — Output file path
- `--aspect-ratio` — 16:9 / 1:1 / 4:3 / 3:4 / 9:16
- `--quality` — normal / 2k (default: 2k)

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

---

## Skills Detail

### hot-topics

Collects AI trending from: HN, Reddit (r/MachineLearning, r/artificial, r/singularity), RSS feeds.

5 categories: OpenClaw ecosystem, model updates, AI applications, algorithm breakthroughs, AI global expansion.

Output:
```
## [AI应用] Claude Code new features
- Signal: ▲ 1234
- Summary: 1-2 sentence description
- Link: URL
- Source: HN
```

### viral-patterns

Searches `data/viralkb/` (patterns.jsonl) for viral title formulas by keyword.

Run `viral-mining` skill first to populate ViralKB.

### viral-mining

Parallel RSS/HN crawler → discovers viral content → ingests into ViralKB.

Signal score: `votes + comments * 0.5 + recency_bonus`

### write-article

Full pipeline:
1. hot-topics research
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
python tools/nanobanana_client.py --gemini-image --use-curl ...
```
(`--use-curl` flag tells the tool to use Python requests, not subprocess)

---

## Troubleshooting

### "No API key provided"

Edit `config/.env` and add at least one key:
```bash
AIBERM_API_KEY=your_key_here
# OR
GOOGLE_AI_API_KEY=your_key_here
```

### "curl: command not found" or curl acts weird

Always use `--use-curl` flag: `python tools/nanobanana_client.py --gemini-image --use-curl ...`

### "Reference image not found"

Cover image requires you to provide `--ref ./your-photo.jpg`. No default photo is bundled.

### viral-patterns returns nothing

Run `viral-mining` skill first to populate `data/viralkb/patterns.jsonl`.

### article_illustrate.py generates but no images appear

Check that your article has `**bold section headings**` after the `---` divider. The tool only processes post-divider content.

---

## Agent Usage Pattern

1. Load `skills/index.md` — see available skills
2. Identify skill by trigger word
3. Load that skill file — follow workflow steps
4. Execute using tools in `tools/` directory
5. All paths are relative to skill-packaging root