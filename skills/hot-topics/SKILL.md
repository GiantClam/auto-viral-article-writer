---
name: hot-topics
description: This skill should be used when the user asks for "今日热榜", "AI热榜", "热门话题", "热点追踪", "今日话题", "热榜", "what's trending today", "find hot AI topics", or wants current topics from multiple sources. Use it for source-aware trend collection where ranking must balance raw discussion heat with important product releases, model launches, and capability updates.
version: 1.2.0
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
- deep single-topic research (use `last30days` instead)

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

---

## Workflow

### Step 1: Topic Quality Pre-Flight — detect keyword traps BEFORE running searches

**Mandatory.** Check the topic for known failure classes. Running searches on a keyword-trap topic burns time and produces junk. Detecting the trap upfront costs one turn.

**Known trap classes:**

| Class | Pattern | Why it fails | Action |
|-------|---------|--------------|--------|
| **Demographic shopping** | `gift for {age} year old {gender}`, `present for {demographic}` | Real posts use relationship + hobbies, not literal age | Ask for hobbies/relationship/budget |
| **Numeric keyword trap** | Topic contains a number that collides with unrelated content (42 = Jackie Robinson, 40 = 40th anniversary) | Number dominates retrieval, pulls unrelated content | Strip the number unless semantically load-bearing |
| **Overly-literal concept** | `how to use X`, `what is Y tutorial` | Social posts use different vocabulary ("my Docker setup", not "how to use Docker") | Reframe to discussion phrasing |
| **Generic single-noun** | `bread`, `sneakers`, `coffee` with no specific hook | Infinite corpus, signal is noise | Ask for specificity |

**If topic matches a trap class:** emit a visible one-liner and either ask a clarifying question OR reframe before proceeding.

**If topic does NOT match any class:** emit `Pre-Flight: {topic type} - proceeding.` Then proceed to Step 2.

---

### Step 2: Entity Pre-Resolution — resolve who matters BEFORE searching

Before running searches on a named entity topic (person, brand, product, company):

1. **Resolve X/Twitter handles** (if platform is available):
   ```
   WebSearch("{TOPIC} X twitter handle site:x.com")
   WebSearch("{TOPIC} CEO/founder X twitter site:x.com")  # for companies
   WebSearch("{TOPIC} creator founder X twitter site:x.com")  # for products
   ```
   Extract handles and pass them to the search commands.

2. **Resolve GitHub repos** (if topic is a product/project):
   ```
   WebSearch("{TOPIC} github repo site:github.com")
   ```
   Extract `owner/repo` for project-mode data.

3. **Resolve related subreddits / communities:**
   ```
   WebSearch("{TOPIC} subreddit site:reddit.com")
   ```
   Find active communities discussing this topic.

**Why this matters:** keyword search is shallow. "DeepSeek" as a bare keyword matches everything containing "DeepSeek." Resolving `@deepseek-ai`, `deepseek-ai/deepseek`, and `r/LocalLLaMA` first gives you precise targeting that bare search cannot achieve.

**Skip this step if:**
- Topic is a generic concept (no specific entity)
- User provided handles/repos directly
- Using `--quick` depth

---

### Step 3: Collect Data — parallel channels

Collect from two channels in parallel:

**A. opencli sources** (if available):
- 小红书 (xiaohongshu)
- 知乎 (zhihu)
- B站 (bilibili)
- Twitter/X (twitter)
- GitHub Trending

**B. RSS / API sources**:
- Hacker News (front page RSS)
- Reddit (subreddit feeds)
- BBC News (tech RSS)

**Failover behavior:**
- If opencli is unavailable for a source, mark it as `unavailable` and continue with remaining sources
- Do not block on a single failing source; run all channels in parallel and merge results

---

### Step 4: Cross-Source Deduplication — merge same story from different platforms

When the same story appears in multiple places:
- Merge into one entry, not three separate items
- Track which platforms confirmed it
- Attribution: `[Platform1] · [Platform2] · +N more`

**Do NOT count repeated reposts as independent confirmation.** A story appearing in 5 B站 reposts is still one story, not five.

---

### Step 5: Rank with Engagement Scoring — not just discussion volume

Rank results using TWO dimensions:

**Dimension 1 — Discussion Heat** (what people are actively talking about):
- HN: points + comment count
- Reddit: upvotes + comment count
- Twitter/X: likes + retweets + views
- 小红书: likes +收藏 +评论
- 知乎: 热度值（显示在列表中）
- B站: 播放量 + 弹幕数

**Dimension 2 — Strategic Importance** (regardless of volume):
- New model releases or API capabilities
- New enterprise/platform integrations
- Pricing or availability changes
- Major partnerships or acquisitions
- Capability expansions that change what users can do

**Key rule:** For a general "today's hot topics" answer, allow strategically important product updates to outrank noisier but less consequential discussion threads.

**Tag each entry with:**
- Primary category
- Engagement signals (e.g., "🔥 89⬆ · 11💬" for HN, "❤️ 4.1k" for 小红书)
- Source platform(s)

---

### Step 6: Research Sufficiency Check

Before surfacing a topic as especially strong, confirm at least one of:
- Clear original source exists
- Multiple independent signals point to the same event
- Enough concrete detail to support a writing angle

If a topic is thin, tag it with a confidence caveat.

---

### Step 7: Optional ViralKB Ingestion

For topics that qualify for downstream writing:
- Tag with recommended article angle
- Note likely audience
- Note HKR viability (Happy / Knowledge / Resonance)

---

## Ranking Rules Summary

| Situation | Action |
|-----------|--------|
| HN 100⬆ but a model release got 20⬆ | Model release outranks if strategically important |
| Same story on 3 platforms | Merge, tag multi-platform |
| Single-source topic with weak discussion | Add confidence caveat |
| Demographic trap query | Ask clarifying question first |

---

## Article Brief Seeding

When a topic is strong enough for downstream writing, return enough structure to seed an article brief:

- topic
- possible angle
- likely audience
- HKR viability notes
- candidate hook
- source set summary
- risk notes if the topic is still thin

---

## Output Format

Structure the ranked list as:

```
## 讨论热度优先

| 话题 | 来源 | 信号 |
|-----|------|-----|
| ... | ... | ... |

## 战略重要性优先

| 话题 | 来源 | 信号 |
|-----|------|-----|
| ... | ... | ... |
```

Tag each item with:
- `[AI工具]` / `[模型更新]` / `[AI应用]` / `[算法突破]` / `[AI出海]` category badge
- Engagement signal (🔥 ⬆ + 💬 count)
- Multi-platform indicator if applicable

---

## Categories

- AI工具 / AI Tools
- 模型更新 / Model Updates
- AI应用 / AI Applications
- 算法突破 / Algorithm Breakthroughs
- AI出海 / AI Global Expansion

---

## Fallback Guidance

- If `opencli` is unavailable, continue with RSS and make the reduced coverage explicit.
- If coverage is reduced, say so and frame output as partial rather than fully representative.
- If user preferences are missing, use sane defaults and suggest running `setup` later.
- If ViralKB ingestion fails, still return the ranked topic list.
- If the topic is a named entity and opencli is unavailable, use WebSearch to resolve handles before running structured searches.

---

## Relationship with `last30days`

Use `hot-topics` for: **daily discovery** — "what's happening today across AI?"

Use `last30days` for: **deep research** — "what is the complete picture of this specific topic over the last 30 days?"

The two skills are complementary. `hot-topics` feeds the discovery layer; `last30days` handles the investigation layer.

---

## References

- `references/article-brief-seeding.md`
- `references/ranking-examples.md`
- `references/source-priority.md`
- `references/research-sufficiency.md`
- `references/topic-scoring.md`