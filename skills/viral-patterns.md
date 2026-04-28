# viral-patterns — Retrieve Viral Content Patterns from ViralKB

## Triggers
`viral-patterns`, `爆款模式`, `查找爆款`, `找标题公式`, `参考爆款`, `check article structure`

## Input
Keyword or topic provided by user to search ViralKB for viral article patterns.

## Workflow

### Step 1 — Connect ViralKB

ViralKB storage:
```
data/viralkb/
```

Format: patterns.jsonl (JSONL, one pattern per line) + embeddings.npy (optional, for semantic search).

### Step 2 — Search ViralKB

Search by keyword for title patterns, structure patterns, emotional triggers:

```python
import json
from pathlib import Path

patterns_file = Path('data/viralkb/patterns.jsonl')
keyword_lower = keyword.lower()

matches = []
with open(patterns_file, 'r', encoding='utf-8') as f:
    for line in f:
        pattern = json.loads(line)
        if keyword_lower in pattern.get('keyword', '').lower():
            matches.append(pattern)

# Sort by engagement score
matches.sort(key=lambda x: x.get('engagement', 0), reverse=True)
```

### Step 3 — Analyze Title Formulas

Extract high-frequency title elements:
- Number usage ("3 tips", "81k survey")
- Emotional words (anxiety, doubling, halving)
- Sentence structures (question, exclamation, command)

### Step 4 — Output Format

```
## Viral Title Formulas

1. [Number + Emotional Impact] — e.g., "3 Tips, 2x Efficiency"
2. [Question Format] — e.g., "Half the Jobs? Real Data Speaks"
...

## Viral Structure Pattern

Opening: Pain point scenario → Data validation → Solution → Call to action

## High-Engagement Emotional Triggers

Anxiety, doubling, halving, truth, expose, must-see
```

## Tools

Direct Python JSON reading — no external dependencies.

## Optional Enhancement: opencli_fetcher.py

For fresh social media data to compare against ViralKB patterns:

```bash
# Requires: opencli CLI + Chrome extension
python tools/opencli_fetcher.py --platform xiaohongshu --query "AI" --limit 5
python tools/opencli_fetcher.py --platform zhihu --query "AI工具" --limit 5
```

This gives you real-time viral content to validate or supplement ViralKB findings.

## Notes

- If `data/viralkb/patterns.jsonl` does not exist, run `viral-mining` skill first to populate
- No API keys required for ViralKB lookup (local file-based)