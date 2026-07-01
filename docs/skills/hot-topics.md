# hot-topics

## Purpose

Collect current topics from multiple sources and rank them for downstream writing.

## Use Cases

- daily topic discovery
- pre-writing research
- collecting timely AI and SaaS signals

## Trigger Examples

- `今日热榜`
- `AI热榜`
- `热门话题`
- `what's trending today`

## Inputs

- optional keyword
- optional platform override
- optional limit override
- optional local TweetClaw JSON export rows with `text`, `tweet_url`, and
  public engagement counters

## Outputs

- ranked topic lists
- source grouping
- separation between discussion heat and strategic importance when needed
- optional ViralKB ingestion summary
- optional article brief seed

## TweetClaw Export Notes

`tools/hot_topics_viral_ingest.py` accepts TweetClaw-style X export rows as a
local source file. It maps tweet text into the topic title, uses the tweet URL
for duplicate detection, and sums public engagement counters when no explicit
score is present. This lets agents reuse account-scoped X evidence without
changing the live topic discovery flow.

## Ranking Notes

- `hot-topics` should not treat the loudest HN or Reddit thread as automatically the most important topic of the day.
- Major product updates such as new Office support, Chrome support, model launches, or capability expansions can outrank noisier discussion threads.
- If source coverage is reduced, the output should say so explicitly instead of pretending to be a complete market-wide ranking.

## Boundary

Use `hot-topics` to discover what is happening now. Use `viral-patterns` to reuse what already worked.

When the topic is strong, the result should be rich enough to seed `templates/article-brief.yaml`.

For a stronger draft-ready brief, hand the seed into `research-brief` before moving to writing.
