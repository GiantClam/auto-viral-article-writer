# viral-mining — Discover Viral Articles from Multiple Sources, Ingest to ViralKB

## Triggers
`挖掘爆款`, `viral mining`, `发现爆款`, `爆款挖掘`

## Input
- keyword: Topic keyword to search across platforms
- sources: Platform list (default: all available — xiaohongshu, zhihu, reddit, bilibili, twitter, hackernews + HN/Reddit RSS)

## Workflow

### Step 1 — Parallel Multi-Source Search

Search keyword across **all available sources simultaneously** — opencli for social media + requests RSS for HN/Reddit. Both channels run in parallel, results are merged.

#### Channel A: opencli (Social Media — Chinese platforms)

```bash
python tools/opencli_fetcher.py --platform xiaohongshu --query "AI" --limit 20
python tools/opencli_fetcher.py --platform zhihu --query "AI工具" --limit 20
python tools/opencli_fetcher.py --platform bilibili --query "AI" --limit 20
python tools/opencli_fetcher.py --platform reddit --query "AI" --limit 20
python tools/opencli_fetcher.py --platform twitter --query "AI" --limit 20
```

#### Channel B: requests RSS (HN + Reddit — Western platforms)

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
    r = requests.get(url, timeout=15)
    return (name, r.text)

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(fetch_rss, name, url) for name, url in RSS_SOURCES.items()]
    rss_results = [f.result() for f in futures]
```

### Step 2 — Merge Results and Calculate Signal

```python
all_items = []

# Add opencli results
for platform in ['xiaohongshu', 'zhihu', 'bilibili', 'reddit', 'twitter', 'hackernews']:
    items = collect_via_opencli(platform, keyword, limit=20)
    for item in items:
        item['platform'] = platform
        item['channel'] = 'opencli'
        all_items.append(item)

# Add RSS results
for source_name, xml in rss_results:
    items = parse_rss_by_keyword(xml, keyword, source=source_name)
    for item in items:
        item['source'] = source_name
        item['channel'] = 'rss'
        all_items.append(item)

# Calculate engagement score
def calc_score(item):
    channel = item.get('channel')
    if channel == 'opencli':
        platform = item.get('platform', '')
        if platform == 'xiaohongshu':
            return int(item.get('liked_count', 0))
        elif platform == 'zhihu':
            return int(item.get('vote_count', 0))
        elif platform == 'bilibili':
            return int(item.get('view', 0))
        elif platform == 'reddit':
            return int(item.get('score', 0))
        elif platform == 'hackernews':
            return int(item.get('points', 0))
    elif channel == 'rss':
        return int(item.get('score', 0))
    return 0

for item in all_items:
    item['engagement'] = calc_score(item)

all_items.sort(key=lambda x: x['engagement'], reverse=True)
```

### Step 3 — Category Tagging

Tag each item with one of 5 categories:
1. OpenClaw ecosystem
2. Model updates
3. AI applications
4. Algorithm breakthroughs
5. AI global expansion

### Step 4 — Ingest to ViralKB

```python
import json
from pathlib import Path

kb_dir = Path('data/viralkb')
kb_dir.mkdir(parents=True, exist_ok=True)
patterns_file = kb_dir / 'patterns.jsonl'

for item in all_items[:50]:  # Top 50
    with open(patterns_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps({
            'keyword': keyword,
            'title': item.get('title', 'N/A'),
            'title_pattern': analyze_title_pattern(item['title']),
            'structure': 'Pain point → Data → Solution → CTA',
            'emotional_triggers': extract_emotions(item['title']),
            'engagement': item['engagement'],
            'source': item.get('platform') or item.get('source', 'unknown'),
            'url': item.get('url', ''),
            'channel': item.get('channel', 'unknown')
        }, ensure_ascii=False) + '\n')
```

### Step 5 — Output Trending List

```
## Trending Viral Content for "AI"

### [AI应用] 小红书笔记 ▲ 1234 likes
Summary: ... | Link: ... | Source: 小红书 | Channel: opencli

### [模型更新] HN文章 ▲ 871 points
Summary: ... | Link: ... | Source: HN | Channel: RSS
...
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

Requirements:
- `opencli` CLI installed
- Chrome browser with target site logged in
- OpenCLI Browser Bridge extension enabled

## Notes

- **Both channels run in parallel** — opencli (Chinese platforms) + RSS (HN/Reddit)
- Results are merged, deduplicated, sorted by engagement score
- For Reddit/HN, both opencli AND RSS are queried separately for maximum coverage
- Windows PowerShell: `--use-curl` only needed for `nanobanana_client.py`