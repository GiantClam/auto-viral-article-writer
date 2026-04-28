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

Uses SQLite-compatible pattern storage (patterns.jsonl + embeddings.npy).

### Step 2 — Search ViralKB

Search by keyword for title patterns, structure patterns, emotional triggers:

```python
import json

# Search patterns.jsonl
with open(r'data/viralkb/patterns.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        pattern = json.loads(line)
        if keyword.lower() in pattern.get('keyword', '').lower():
            # yield pattern
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

Direct Python JSON reading, no external dependencies.