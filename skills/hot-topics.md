# hot-topics — Collect Today's AI Trending Topics

## Triggers
`今日热榜`, `AI热榜`, `热门话题`, `热点追踪`, `今日话题`, `热榜`

## Input
- Sources: Reddit, Hacker News, official blogs, RSS
- Categories: OpenClaw ecosystem, model updates, AI applications, algorithm breakthroughs, AI global expansion

## Workflow

### Step 1 — Multi-Source Fetch

Use Python `requests` to fetch these sources in parallel:

```
https://news.ycombinator.com/news
https://www.reddit.com/r/MachineLearning/.rss
https://www.reddit.com/r/artificial/.rss
https://www.reddit.com/r/singularity/.rss
```

### Step 2 — Content Parsing

Parse RSS/HTML, extract:
- Title, URL, votes/comment count
- Publication date
- Signal strength (weighted by votes + comments + recency)

### Step 3 — Category Tagging

Tag each item with one of 5 categories:
1. **OpenClaw ecosystem** — Claude Code, OpenCode plugin/features
2. **Model updates** — New model releases, version iterations
3. **AI applications** — Real-world deployment cases, product launches
4. **Algorithm breakthroughs** — Research progress, technical papers
5. **AI global expansion** — Chinese AI product internationalization

### Step 4 — Output Format

Formatted trending list, each item:

```
## [AI应用] Title
- Signal: ▲ 1234
- Summary: 1-2 sentence description
- Link: URL
- Source: Platform name
```

## Tools

Use `viral-mining` skill to fetch multiple RSS sources in parallel.

## Notes

- No special configuration required
- Output directly to terminal
- Windows PowerShell: use `requests` instead of `curl` subprocess