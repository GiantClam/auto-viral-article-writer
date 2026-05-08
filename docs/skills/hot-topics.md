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

## Outputs

- ranked topic lists
- source grouping
- optional ViralKB ingestion summary
- optional article brief seed

## Boundary

Use `hot-topics` to discover what is happening now. Use `viral-patterns` to reuse what already worked.

When the topic is strong, the result should be rich enough to seed `templates/article-brief.yaml`.

For a stronger draft-ready brief, hand the seed into `research-brief` before moving to writing.
