---
name: hot-topics
description: This skill should be used when the user asks for "今日热榜", "AI热榜", "热门话题", "热点追踪", "今日话题", "热榜", or wants to collect AI trending topics from multiple sources. Collects trending content from HN, Reddit, RSS, 小红书, 知乎, B站, Twitter.
version: 1.0.0
metadata:
  platforms: [opencode, codex, claudecode]
---

# Hot Topics Collector

Collect trending AI topics from multiple sources simultaneously, filtered by user preferences.

## Triggers

`今日热榜`, `AI热榜`, `热门话题`, `热点追踪`, `今日话题`, `热榜`

## Input

- keyword: Optional search keyword (default: uses user's configured hot_topics preferences)
- platforms: xiaohongshu / zhihu / bilibili / twitter / hackernews / reddit (default: user's configured platforms)
- limit: Number of results per platform (default: 10)

## Workflow

### Step 1 — Load User Preferences

Read user preferences to determine search keywords and platforms:

```python
import json
from pathlib import Path

def load_preferences():
    config_path = Path('config/user_preferences.json')
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

preferences = load_preferences()
if preferences:
    topics = preferences.get('hot_topics', ['AI', 'AI工具', 'SaaS'])
    platforms = preferences.get('default_platforms', ['xiaohongshu', 'zhihu', 'bilibili', 'twitter'])
else:
    topics = ['AI', 'AI工具', 'SaaS']
    platforms = ['xiaohongshu', 'zhihu', 'bilibili', 'twitter']

print(f"Using topics: {topics}")
print(f"Using platforms: {platforms}")
```

### Step 2 — Parallel Multi-Source Fetch

Run **both channels in parallel** for maximum coverage:

#### Channel A: opencli (Chinese platforms + Twitter)

```bash
# Run each platform in parallel
opencli xiaohongshu search "AI工具" --limit 10 -f json
opencli zhihu hot --limit 10 -f json
opencli bilibili hot --limit 10 -f json
opencli twitter trending --limit 10 -f json
```

Or use the wrapper script:
```bash
python tools/opencli_fetcher.py --platform xiaohongshu --limit 10
python tools/opencli_fetcher.py --platform zhihu --limit 10
python tools/opencli_fetcher.py --platform bilibili --limit 10
python tools/opencli_fetcher.py --platform twitter --limit 10
```

#### Channel B: RSS (HN + Reddit)

```python
import requests
import concurrent.futures

RSS_SOURCES = {
    'HN': 'https://news.ycombinator.com/rss',
    'Reddit-ML': 'https://www.reddit.com/r/MachineLearning/.rss',
    'Reddit-AI': 'https://www.reddit.com/r/artificial/.rss',
    'Reddit-Singularity': 'https://www.reddit.com/r/singularity/.rss',
}

def fetch_rss(name, url):
    try:
        r = requests.get(url, timeout=15)
        return (name, r.text)
    except:
        return (name, None)

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(fetch_rss, name, url) for name, url in RSS_SOURCES.items()]
    results = [f.result() for f in futures]
```

### Step 3 — Filter by User Topics

Filter results based on user's configured hot_topics:

```python
def matches_topic(item_title, topics):
    title_lower = item_title.lower()
    return any(topic.lower() in title_lower for topic in topics)

filtered = [item for item in all_items if matches_topic(item['title'], topics)]
```

### Step 4 — Merge and Sort

Combine results, deduplicate, sort by engagement score:

```python
all_items = []

# Add opencli results
for platform in platforms:
    items = collect_via_opencli(platform, limit=limit)
    for item in items:
        item['channel'] = 'opencli'
        item['platform'] = platform
        all_items.append(item)

# Add RSS results
for name, xml in rss_results:
    items = parse_rss(xml, source=name)
    for item in items:
        item['channel'] = 'rss'
        all_items.append(item)

# Filter by topics
filtered = [item for item in all_items if matches_topic(item.get('title', ''), topics)]

# Sort by engagement score
filtered.sort(key=lambda x: x.get('score', 0), reverse=True)
```

### Step 5 — Category Tagging

Tag each item with one of 5 categories:
1. **AI工具 / AI Tools** — AI software, productivity tools, SaaS
2. **模型更新 / Model Updates** — New model releases
3. **AI应用 / AI Applications** — Real-world deployment cases
4. **算法突破 / Algorithm Breakthroughs** — Research progress
5. **AI出海 / AI Global Expansion** — Chinese AI products going global

### Step 6 — Output Format

```
## 今日热榜 [AI工具, SaaS, AI出海]

### 小红书
1. **[标题]** ▲ 1234 likes
   摘要... | 来源: @作者

### 知乎
1. **[标题]** 热度: 4183万 | 回答: 150
   链接

### Twitter/X
1. **#话题** 分类

### Hacker News
1. **[标题]** ▲ 871 points
   链接
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
opencli doctor
```

## First-Time Setup

If this is your first time using hot-topics, run the `setup` skill first:

```
Use the setup skill to configure your hot topic preferences and verify opencli connection.
```

## Notes

- **Run both channels in parallel** — opencli for Chinese platforms + RSS for HN/Reddit
- opencli and RSS are complementary channels, not substitutes
- Windows PowerShell: `--use-curl` flag only needed for `nanobanana_client.py`, not for opencli or RSS