# viral-mining — Discover Viral Articles from Multiple Sources, Ingest to ViralKB

## Triggers
`挖掘爆款`, `viral mining`, `发现爆款`, `爆款挖掘`

## Input
- keyword: Topic keyword
- sources: RSS URL list (default sources provided)

## Workflow

### Step 1 — Parallel Multi-Source Fetch

Built-in default sources:
```python
SOURCES = {
    'HN': 'https://news.ycombinator.com/rss',
    'Reddit-ML': 'https://www.reddit.com/r/MachineLearning/.rss',
    'Reddit-AI': 'https://www.reddit.com/r/artificial/.rss',
    'Reddit-Singularity': 'https://www.reddit.com/r/singularity/.rss',
}
```

Use `requests` + `feedparser` in parallel (avoid PowerShell curl alias).

### Step 2 — Content Parsing & Signal Calculation

Signal strength per item:
```python
score = votes * 1.0 + comments * 0.5 + recency_bonus
```

Higher recency_bonus for newer content.

### Step 3 — Category Tagging

5 categories:
1. OpenClaw ecosystem
2. Model updates
3. AI applications
4. Algorithm breakthroughs
5. AI global expansion

### Step 4 — Ingest to ViralKB

```python
# Append to patterns.jsonl
with open(r'data/viralkb/patterns.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps({
        'keyword': keyword,
        'title': title,
        'title_pattern': pattern,
        'structure': structure,
        'emotional_triggers': triggers,
        'engagement': score,
        'source': source
    }, ensure_ascii=False) + '\n')
```

### Step 5 — Output Trending List

Sorted by signal strength, top 20:

```
## Trending Viral Content

### [AI应用] Claude Code New Features
▲ 1234 | Summary: ... | Source: HN | Link: ...
...
```

## Tools

Python `requests` + `feedparser` (optional).

## Notes

- Do NOT use `subprocess.run(['curl', ...])` — Windows PowerShell intercepts it
- Use `requests.get()` directly for HTTP requests
- Supports custom sources parameter to override defaults