# write-article — Writing Pipeline: Research → Outline → Draft → Illustrate

## Triggers
`写文章`, `生成文章`, `create-article`, `写篇`, `公众号`, `小红书`

## Input
- topic: Article topic
- platform: wechat / xiaohongshu (determines format and style)
- ref_photo: Optional reference photo path

## Workflow

### Step 1 — Hot Topics Research (call hot-topics skill)

Parallel fetch Reddit/Hacker News/RSS, collect latest trends related to topic.

### Step 2 — Viral Pattern Research (call viral-patterns skill)

Search ViralKB for same-topic viral title formulas and structure patterns.

### Step 3 — Research Data Collection

Use Jina Reader to fetch authoritative sources:

```python
import requests

def jina_read(url):
    return requests.get(
        f'https://r.jina.ai/{url}',
        headers={'X-Return-Format': 'markdown'},
        timeout=30
    ).text
```

### Step 4 — Generate Article Outline

Call Gemini (via aiberm API) to generate structured outline:

```
# 【5 Title Candidates】

---

## Section Structure
```

Title candidates use `【】`, sections use `**bold**` format.

### Step 5 — Write Complete Article

Expand outline into full article, save to `output/wechat/{slug}-{date}.md`.

### Step 6 — Generate Article Illustrations (call article-illustrate skill)

Use `article_illustrate.py` to auto-generate and insert illustrations:

```python
from tools.article_illustrate import generate_and_insert_images

generate_and_insert_images(
    article_path='output/wechat/{slug}-{date}.md',
    api_key=os.getenv('AIBERM_API_KEY'),
    style='tech Illustration',
    count=3
)
```

Insert location: exact `**heading**` match below.

## Tools

- `hot-topics.md` skill — Multi-source trending fetch
- `viral-patterns.md` skill — Viral pattern search
- `tools/nanobanana_client.py` — Image generation
- `tools/article_illustrate.py` — Auto-illustration

## Output

Final article saved to `output/wechat/{slug}-{date}.md`, containing:
- 5 title candidates
- `---` divider
- Complete article body (with illustrations)

## Format Specification

- Title candidates: `# 【Title】`
- Sections: `**Section Name**` (bold)
- Images: `![alt](image path)`