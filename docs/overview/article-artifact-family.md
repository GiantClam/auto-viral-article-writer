# Article Artifact Family

This package treats all deliverables for a single article as one artifact family keyed by the same slug.

## Core Convention

For a given article slug, keep related outputs aligned by name and path.

See `docs/overview/slug-rules.md` for how the slug itself should be generated and reused.

## Recommended Files

- brief: `output/briefs/{slug}-brief.yaml`
- article draft: `output/wechat/{slug}-article.md`
- content ledger folder: `output/content/{slug}/`
- cover image: `output/images/wechat/{slug}-cover-final.png`
- inline images: `output/images/wechat/{slug}-01.png`, `output/images/wechat/{slug}-02.png`, `output/images/wechat/{slug}-03.png`

## Why This Matters

- easier handoff between skills
- easier release review
- easier cleanup and regeneration
- less ambiguity about which files belong to which article

## Practical Rule

If a brief exists, the article and image artifacts should reuse the same slug family whenever possible.

Use `article-audit` to verify this family for a specific slug before treating the article as publish-ready.
