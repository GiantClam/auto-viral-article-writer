# viral-mining — Discover Viral Articles from Multiple Sources, Ingest to ViralKB

## Triggers
`挖掘爆款`, `viral mining`, `发现爆款`, `爆款挖掘`

## Input
- keyword: Topic keyword to search across platforms
- sources: Platform list (default: xiaohongshu, zhihu, reddit, bilibili, twitter, hackernews)

## Workflow

### Step 1 — Check opencli Availability

```bash
opencli --version
opencli doctor
```

If opencli is installed with Chrome + extension active, use Step 2.
Otherwise, fall back to Step 3.

### Step 2 — Multi-Platform Search via opencli

Use `tools/opencli_fetcher.py` to search viral content by keyword across platforms:

```bash
# Search each platform for the keyword
python tools/opencli_fetcher.py --platform xiaohongshu --query "AI" --limit 20
python tools/opencli_fetcher.py --platform zhihu --query "AI工具" --limit 20
python tools/opencli_fetcher.py --platform bilibili --query "AI" --limit 20
python tools/opencli_fetcher.py --platform reddit --query "AI" --limit 20
```

Parse JSON output, extract viral articles:
```python
import json
from pathlib import Path

def collect_viral(keyword, platforms, limit=20):
    results = []
    for platform in platforms:
        output_file = f'/tmp/{platform}_viral.json'
        subprocess.run([
            'python', 'tools/opencli_fetcher.py',
            '--platform', platform,
            '--query', keyword,
            '--limit', str(limit),
            '--output', output_file
        ], capture_output=True)

        if Path(output_file).exists():
            with open(output_file) as f:
                data = json.load(f)
                for item in data.get('items', []):
                    item['platform'] = platform
                    results.append(item)
    return results
```

### Step 3 — Fallback: RSS (no opencli)

If opencli is not available:

```python
import requests

SOURCES = {
    'HN': 'https://news.ycombinator.com/rss',
    'Reddit-ML': 'https://www.reddit.com/r/MachineLearning/.rss',
    'Reddit-AI': 'https://www.reddit.com/r/artificial/.rss',
    'Reddit-Singularity': 'https://www.reddit.com/r/singularity/.rss',
}
```

### Step 4 — Signal Calculation

Calculate engagement score per item:

```python
def calc_score(item, platform):
    if platform == 'xiaohongshu':
        return int(item.get('liked_count', 0))
    elif platform == 'zhihu':
        return int(item.get('vote_count', 0))
    elif platform == 'reddit':
        return int(item.get('score', 0))
    elif platform == 'bilibili':
        return int(item.get('view', 0))
    else:
        return 0
```

### Step 5 — Category Tagging

Tag each item with one of 5 categories:
1. OpenClaw ecosystem
2. Model updates
3. AI applications
4. Algorithm breakthroughs
5. AI global expansion

### Step 6 — Ingest to ViralKB

```python
import json
from pathlib import Path

kb_dir = Path('data/viralkb')
kb_dir.mkdir(parents=True, exist_ok=True)
patterns_file = kb_dir / 'patterns.jsonl'

with open(patterns_file, 'a', encoding='utf-8') as f:
    f.write(json.dumps({
        'keyword': keyword,
        'title': item.get('title', 'N/A'),
        'title_pattern': analyze_title_pattern(item['title']),
        'structure': 'Pain point → Data → Solution → CTA',
        'emotional_triggers': extract_emotions(item['title']),
        'engagement': score,
        'source': platform
    }, ensure_ascii=False) + '\n')
```

### Step 7 — Output Trending List

```
## Trending Viral Content

### [AI应用] Claude Code New Features
▲ 1234 likes | Summary: ... | Source: 小红书 | Link: ...
...
```

## Tool: opencli_fetcher.py

Requirements:
- `opencli` CLI installed
- Chrome browser with target site logged in
- OpenCLI Browser Bridge extension enabled

## Notes

- **opencli is the primary source** — provides rich engagement data from Chinese platforms
- Windows PowerShell: opencli works fine, `nanobanana_client.py` needs `--use-curl` only