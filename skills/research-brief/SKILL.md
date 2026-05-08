---
name: research-brief
description: This skill should be used when the user asks to "先研究一下", "先帮我梳理这个题", "research brief", "deep brief", "帮我先摸清楚这个题", or wants a stronger structured brief before article drafting. It sits between topic discovery and writing, turning a promising topic into a source-backed article brief.
version: 1.0.0
---

# Research Brief

Use this skill when a topic is interesting enough to pursue, but still needs stronger framing, source organization, and risk notes before drafting the article.

## Use This For

- deepening a promising topic before writing
- turning topic discovery into a stronger article brief
- gathering source-backed angle options
- preparing the handoff object for `write-article`

## Do Not Use This For

- broad hot-topic scanning
- direct article drafting
- pure title-pattern lookup with no deeper research step

## Inputs

- topic, trend, or candidate article idea
- optional hot-topics result seed
- optional platform target

## Outputs

- a stronger article brief
- clearer angle options
- source set summary
- risk notes and unsupported areas
- a brief file saved under `output/briefs/` when a durable artifact is needed

## Workflow

1. Start from a topic or a hot-topics brief seed.
2. Gather stronger source material around the topic.
3. Evaluate whether the topic is article-ready or still exploratory.
4. Propose one or more viable angles.
5. Fill or refine the article brief.
6. Save the brief to `output/briefs/{slug}-brief.yaml` when a reusable file is needed.
7. Hand the brief to `viral-patterns` and `write-article`.

## Research Discipline

- prefer original or primary sources when available
- separate confirmed facts from strong hypotheses
- record where the brief is still thin instead of pretending certainty
- keep the output structured enough for downstream drafting

## Output Convention

When the brief should persist as a reusable artifact, write it under:

- `output/briefs/{slug}-brief.yaml`

Use the shared template at `templates/article-brief.yaml` as the starting structure.

Generate the slug once and keep it stable for all later article artifacts.

Prefer to treat this brief as the first artifact in the article artifact family for the chosen slug.

## References

- `references/brief-strength-levels.md` - how to classify brief maturity
- `references/source-matrix.md` - source priorities by content type
- `references/angle-selection.md` - how to choose a useful angle from the research
- `../../docs/overview/article-artifact-family.md` - recommended file family for brief, draft, cover, and inline images
- `../../docs/overview/slug-rules.md` - how to generate and reuse a stable slug
