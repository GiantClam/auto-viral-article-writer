---
name: article-audit
description: This skill should be used when the user asks to "检查这篇文章是否齐全", "审计这篇文章", "article audit", "publish ready", or wants to verify that one article's brief, draft, cover, and inline images exist and follow the artifact-family naming convention. It audits a single article slug across the package output directories.
version: 1.0.0
---

# Article Audit

Use this skill to inspect whether one article's artifact family is complete, coherent, and named consistently.

## Use This For

- checking whether an article is publish-ready
- verifying that brief, draft, cover, and inline images belong to the same slug family
- identifying missing or misnamed artifacts for a specific article

## Do Not Use This For

- repository-wide documentation sync
- generating content from scratch
- replacing normal article writing or research steps

## Inputs

- article slug
- optional article path
- optional expectation about whether inline images should exist

## Outputs

- artifact presence summary
- naming consistency summary
- missing-file warnings
- publish-readiness decision for the article family

## Workflow

1. Determine the target slug.
2. Check for the expected brief file.
3. Check for the expected draft file.
4. Check for the expected cover image.
5. Check for inline image files if the article should already be illustrated.
6. Compare naming consistency across all discovered files.
7. Report gaps, mismatches, and overall readiness.

If a naming mismatch exists, prefer the slug established by the earliest durable artifact, usually the brief file.

## Expected Artifact Family

- `output/briefs/{slug}-brief.yaml`
- `output/wechat/{slug}-article.md`
- `output/images/wechat/{slug}-cover-final.png`
- `output/images/wechat/{slug}-01.png`, `output/images/wechat/{slug}-02.png`, `output/images/wechat/{slug}-03.png`

## References

- `references/audit-checklist.md` - what to verify for one article family
- `references/status-levels.md` - how to classify article readiness
- `../../docs/overview/article-artifact-family.md` - canonical artifact-family naming convention
- `../../docs/overview/slug-rules.md` - slug generation and stability rules
