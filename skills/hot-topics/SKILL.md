---
name: hot-topics
description: This skill should be used when the user asks for "今日热榜", "AI热榜", "热门话题", "热点追踪", "今日话题", "热榜", "what's trending today", "find hot AI topics", or wants current topics from multiple sources. It collects AI trending content from opencli-supported social platforms and RSS feeds, then filters and ranks the results.
version: 1.0.0
---

# Hot Topics

Use this skill to collect current topics across Chinese and global sources, then filter them by the user's configured preferences.

## Use This For

- daily topic discovery
- source-aware trend collection
- pre-writing topic research
- feeding high-signal items into ViralKB

## Do Not Use This For

- retrieving title formulas from ViralKB
- drafting articles directly
- generating images

## Inputs

- optional keyword override
- optional source or platform override
- optional result limit

## Outputs

- ranked topic list grouped by source
- tagged categories for each topic
- optional ViralKB ingestion summary
- optional topic framing that can seed an article brief

## Workflow

1. Load `config/user_preferences.json` if present.
2. Collect data from two channels in parallel:
   - `opencli` sources such as 小红书, 知乎, B站, Twitter/X
   - RSS sources such as Hacker News and Reddit feeds
3. Filter results by configured or requested topic directions.
4. Rank and deduplicate results.
5. Apply source-priority and source-quality discipline.
6. Tag results by category.
7. Optionally ingest qualifying items into ViralKB.

## Article Brief Seeding

When a topic is strong enough for downstream writing, return enough structure to seed an article brief:

- topic
- possible angle
- likely audience
- HKR viability notes
- candidate hook
- source set summary
- risk notes if the topic is still thin

## Source Discipline

When the same story appears in multiple places:

- prefer the original source over repeated summaries
- do not count repeated reposts as independent confirmation
- separate raw attention from source quality

If a topic is based only on weak secondary chatter, return it with a confidence caveat.

## Research Sufficiency Check

Before surfacing a topic as especially strong, confirm at least one of these is true:

- there is a clear original source
- there are multiple independent signals pointing to the same event
- there is enough concrete detail to support a writing angle

## Categories

- AI工具 / AI Tools
- 模型更新 / Model Updates
- AI应用 / AI Applications
- 算法突破 / Algorithm Breakthroughs
- AI出海 / AI Global Expansion

## Fallback Guidance

- If `opencli` is unavailable, continue with RSS and make the reduced coverage explicit.
- If user preferences are missing, use sane defaults and suggest running `setup` later.
- If ViralKB ingestion fails, still return the ranked topic list instead of failing the whole workflow.

## References

- `references/article-brief-seeding.md` - how to turn a trend result into a draftable brief seed
- `references/source-priority.md` - source quality and channel strategy
- `references/research-sufficiency.md` - what is strong enough to escalate into an article lead
- `references/topic-scoring.md` - ranking and ingestion heuristics
