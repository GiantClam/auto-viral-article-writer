---
name: viral-patterns
description: This skill should be used when the user asks for "爆款模式", "找标题公式", "参考爆款", "viral patterns", "check article structure", or wants reusable title formulas and structure patterns from ViralKB. It looks up local viral content patterns by keyword and summarizes reusable structures.
version: 1.0.0
---

# Viral Patterns

Use this skill to retrieve title formulas, structure patterns, and emotional triggers from local ViralKB storage.

## Use This For

- title inspiration
- structure benchmarking
- pattern-assisted outlining
- topic-specific emotional trigger lookup

## Do Not Use This For

- collecting new live topics from the web
- drafting the full article by itself
- generating visuals

## Inputs

- topic keyword
- optional request for title-only or structure-only output

## Outputs

- ranked matching patterns
- reusable title formulas
- suggested structure shape
- emotional trigger summary
- pattern notes that can attach cleanly to an article brief

## Workflow

1. Read ViralKB from `data/viralkb/`.
2. Search by keyword or related topic markers.
3. Rank by engagement or stored signal quality.
4. Return patterns in a reusable output format.
5. Attach the results to an article-brief-friendly structure.

## Article Brief Attachment

When returning pattern findings for downstream writing, structure them so they can attach to the brief as:

- title patterns
- emotional triggers
- structure suggestions
- notes on what not to copy mechanically

## Fallback Guidance

- If ViralKB is missing or empty, tell the user to run `viral-mining` or `hot-topics` first.
- If direct keyword matches are sparse, broaden by topic family rather than claiming no patterns exist.

## References

- `references/article-brief-attachment.md` - how pattern findings should attach to the article brief
- `references/pattern-output-format.md` - how to present retrieved patterns for downstream article writing
