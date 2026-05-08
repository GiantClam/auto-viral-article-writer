---
name: hot-topics
description: This skill should be used when the user asks for "今日热榜", "AI热榜", "热门话题", "热点追踪", "今日话题", "热榜", "what's trending today", "find hot AI topics", or wants current topics from multiple sources. Use it for source-aware trend collection where ranking must balance raw discussion heat with important product releases, model launches, and capability updates.
version: 1.1.0
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
- explicit separation between discussion heat and strategic importance when needed
- optional ViralKB ingestion summary
- optional topic framing that can seed an article brief

## Workflow

1. Load `config/user_preferences.json` if present.
2. Collect data from two channels in parallel:
   - `opencli` sources such as 小红书, 知乎, B站, Twitter/X
   - RSS sources such as Hacker News and Reddit feeds
3. Filter results by configured or requested topic directions.
4. Deduplicate repeated stories and collapse reposts under the strongest available source.
5. Rank results using two lenses:
   - discussion heat: how much active attention the topic is getting right now
   - strategic importance: whether the topic represents a meaningful product release, model launch, capability expansion, platform integration, pricing move, or ecosystem shift
6. Elevate major product updates even when social discussion volume is temporarily lower than research or opinion threads.
7. Apply source-priority and source-quality discipline.
8. Tag results by category.
9. Optionally ingest qualifying items into ViralKB.

## Ranking Rules

Do not treat the highest-commented RSS item as automatically the most important topic.

Use `discussion heat` to capture what people are actively talking about.

Use `strategic importance` to capture updates such as:

- new support for major surfaces like Office, Chrome, IDEs, or enterprise workflows
- new model releases or API capabilities
- meaningful pricing, rate-limit, or availability changes
- major partnerships, acquisitions, or platform distribution changes
- capability expansions that change what users can now do in practice

When producing a general "today's hot topics" answer rather than a pure engagement leaderboard, allow strategically important product updates to outrank noisier but less consequential discussion threads.

If needed, explicitly label the output as a mix of:

- hot by discussion volume
- hot by industry importance

Do not hide major capability updates just because they are underrepresented in HN or Reddit comments.

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
- separate raw attention from product importance

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
- If `opencli` is unavailable, do not let RSS-only discussion volume suppress clearly important product-release topics that are likely hotter on X or Chinese social platforms.
- If coverage is reduced, say so and frame the output as partial rather than fully representative.
- If user preferences are missing, use sane defaults and suggest running `setup` later.
- If ViralKB ingestion fails, still return the ranked topic list instead of failing the whole workflow.

## References

- `references/article-brief-seeding.md` - how to turn a trend result into a draftable brief seed
- `references/ranking-examples.md` - examples showing when important product updates should outrank noisier discussion threads
- `references/source-priority.md` - source quality and channel strategy
- `references/research-sufficiency.md` - what is strong enough to escalate into an article lead
- `references/topic-scoring.md` - ranking and ingestion heuristics
