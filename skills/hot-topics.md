# hot-topics — Collect Today's AI Trending Topics

## Triggers
`今日热榜`, `AI热榜`, `热门话题`, `热点追踪`, `今日话题`, `热榜`

## Input
- keyword: Optional search keyword (default: collect general AI trending)
- platforms: xiaohongshu / zhihu / reddit / bilibili / twitter / hackernews (default: all available)

## Workflow

### Step 1 — Check opencli Availability

```bash
opencli --version
```

If opencli is installed and Chrome + OpenCLI Browser Bridge extension are active, proceed to Step 2.
If opencli is not available, fall back to Step 3.

### Step 2 — Multi-Platform Fetch via opencli

Use `tools/opencli_fetcher.py` to collect viral content from multiple platforms in parallel:

```python
import subprocess
import json

platforms = ['xiaohongshu', 'zhihu', 'reddit', 'bilibili', 'hackernews']
results = {}

for platform in platforms:
    result = subprocess.run([
        'python', 'tools/opencli_fetcher.py',
        '--platform', platform,
        '--limit', '10',
        '--output', f'/tmp/{platform}_viral.json'
    ], capture_output=True)
```

Or via CLI directly:

```bash
# Xiaohongshu viral notes
python tools/opencli_fetcher.py --platform xiaohongshu --limit 20

# Zhihu hot search
python tools/opencli_fetcher.py --platform zhihu --limit 20

# Bilibili hot
python tools/opencli_fetcher.py --platform bilibili --limit 20

# Reddit hot
python tools/opencli_fetcher.py --platform reddit --limit 20

# Twitter trending
python tools/opencli_fetcher.py --platform twitter --limit 20

# HackerNews
python tools/opencli_fetcher.py --platform hackernews --limit 20
```

### Step 3 — Fallback: requests (no opencli)

If opencli is not available, use Python `requests` for HN + Reddit RSS:

```python
import requests

SOURCES = {
    'HN': 'https://news.ycombinator.com/rss',
    'Reddit-ML': 'https://www.reddit.com/r/MachineLearning/.rss',
    'Reddit-AI': 'https://www.reddit.com/r/artificial/.rss',
    'Reddit-Singularity': 'https://www.reddit.com/r/singularity/.rss',
}

for name, url in SOURCES.items():
    r = requests.get(url, timeout=15)
    # Parse RSS, extract titles/links/scores
```

### Step 4 — Category Tagging

Tag each item with one of 5 categories:
1. **OpenClaw ecosystem** — Claude Code, OpenCode plugin/features
2. **Model updates** — New model releases, version iterations
3. **AI applications** — Real-world deployment cases, product launches
4. **Algorithm breakthroughs** — Research progress, technical papers
5. **AI global expansion** — Chinese AI product internationalization

### Step 5 — Output Format

```
## [AI应用] Title
- Signal: ▲ 1234
- Summary: 1-2 sentence description
- Link: URL
- Source: 小红书 / 知乎 / HN / Reddit / Bilibili / Twitter
```

## Tool: opencli_fetcher.py

`tools/opencli_fetcher.py` — wraps `opencli` CLI for social media data collection.

Platforms supported:
| Platform | Command | Data |
|----------|---------|------|
| 小红书 | `xiaohongshu` | title, author, likes |
| 知乎 | `zhihu` | title, excerpt, votes |
| Reddit | `reddit` | title, score |
| Bilibili | `bilibili` | title, views |
| Twitter | `twitter` | trending topics |
| HackerNews | `hackernews` | title, points |

Requirements:
- `opencli` CLI installed
- Chrome browser running with target site logged in
- OpenCLI Browser Bridge extension enabled

Check setup:
```bash
opencli doctor
```

## Notes

- **Always try opencli first** — it provides richer social media data (engagement, author, etc.)
- Windows PowerShell: opencli works fine, but use `--use-curl` flag for nanobanana_client only
- If opencli fails (e.g., not logged in), fall back to requests RSS