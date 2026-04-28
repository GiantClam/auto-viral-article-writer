# hot-topics — Collect Today's AI Trending Topics

## Triggers
`今日热榜`, `AI热榜`, `热门话题`, `热点追踪`, `今日话题`, `热榜`

## Input
- keyword: Optional search keyword (default: collect general AI trending)
- platforms: xiaohongshu / zhihu / reddit / bilibili / twitter / hackernews (default: all)

## Workflow

### Step 1 — Parallel Multi-Source Fetch

Fetch from **all available sources simultaneously** — opencli for social media + requests RSS for HN/Reddit. Combining both gives the most complete picture.

#### Channel A: opencli (Social Media — Chinese platforms)

```bash
# Xiaohongshu viral notes
python tools/opencli_fetcher.py --platform xiaohongshu --limit 20

# Zhihu hot search
python tools/opencli_fetcher.py --platform zhihu --limit 20

# Bilibili hot
python tools/opencli_fetcher.py --platform bilibili --limit 20

# Twitter trending
python tools/opencli_fetcher.py --platform twitter --limit 20
```

#### Channel B: requests RSS (HN + Reddit — Western platforms)

```python
import requests

RSS_SOURCES = {
    'HN': 'https://news.ycombinator.com/rss',
    'Reddit-ML': 'https://www.reddit.com/r/MachineLearning/.rss',
    'Reddit-AI': 'https://www.reddit.com/r/artificial/.rss',
    'Reddit-Singularity': 'https://www.reddit.com/r/singularity/.rss',
}

import concurrent.futures

def fetch_rss(name, url):
    r = requests.get(url, timeout=15)
    return (name, r.text)

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(fetch_rss, name, url) for name, url in RSS_SOURCES.items()]
    results = [f.result() for f in futures]
```

### Step 2 — Merge and Deduplicate

Combine results from both channels, deduplicate by URL/title.

```python
all_items = []

# Add opencli results
for platform in ['xiaohongshu', 'zhihu', 'bilibili', 'reddit', 'twitter', 'hackernews']:
    items = collect_via_opencli(platform, limit=20)
    for item in items:
        item['channel'] = 'opencli'
        all_items.append(item)

# Add RSS results
for name, xml in rss_results:
    items = parse_rss(xml, source=name)
    for item in items:
        item['channel'] = 'rss'
        all_items.append(item)

# Sort by signal score
all_items.sort(key=lambda x: x.get('score', 0), reverse=True)
```

### Step 3 — Category Tagging

Tag each item with one of 5 categories:
1. **OpenClaw ecosystem** — Claude Code, OpenCode plugin/features
2. **Model updates** — New model releases, version iterations
3. **AI applications** — Real-world deployment cases, product launches
4. **Algorithm breakthroughs** — Research progress, technical papers
5. **AI global expansion** — Chinese AI product internationalization

### Step 4 — Output Format

```
## [AI应用] 小红书笔记标题
- Signal: ▲ 1234
- Summary: 1-2 sentence description
- Link: URL
- Source: 小红书
- Channel: opencli

## [模型更新] HackerNews标题
- Signal: ▲ 871
- Summary: ...
- Link: URL
- Source: HN
- Channel: RSS
```

## Data Sources Summary

| Platform | Channel | Data Available |
|----------|---------|----------------|
| 小红书 | opencli | 标题、作者、点赞数、评论数 |
| 知乎 | opencli | 标题、摘要、投票数、回答数 |
| Bilibili | opencli | 标题、播放量、弹幕数、点赞数 |
| Twitter/X | opencli | trending topics、转发数 |
| Reddit | opencli + RSS | 标题、score、评论数 |
| HackerNews | opencli + RSS | 标题、分数、评论数 |

## Tool: opencli_fetcher.py

`tools/opencli_fetcher.py` — wraps `opencli` CLI for social media data.

Requirements:
- `opencli` CLI installed
- Chrome browser running with target site logged in
- OpenCLI Browser Bridge extension enabled

Check availability:
```bash
opencli --version
opencli doctor
```

## Notes

- **Run both channels in parallel** — opencli for Chinese platforms + RSS for HN/Reddit
- opencli and RSS are complementary channels, not substitutes
- Windows PowerShell: `--use-curl` flag only needed for `nanobanana_client.py`, not for opencli or RSS