---
name: article-illustrate
description: This skill should be used when the user asks to "生成插图", "文章配图", "insert images", "illustrate article", or wants images inserted into an existing article draft. It analyzes article structure, generates matching visuals, and inserts them into markdown.
version: 1.0.0
---

# Article Illustrate

Use this skill when a markdown article already exists and the next step is to add illustrations into the body.

## Use This For

- adding illustrations to a generated article
- converting section headings into image insertion points
- in-place markdown enhancement for article outputs

## Do Not Use This For

- creating a cover image
- creating a full article from scratch
- generating unrelated standalone images

## Inputs

- article markdown path
- optional style hint
- optional max image count

## Outputs

- generated image files under `output/images/`
- updated article markdown with inserted `![alt](path)` blocks
- inline images should prefer the same slug family as the source article when possible

## Workflow

1. Analyze the article for eligible `**bold section**` headings.
2. Filter out title lines, numbered list-style headings, and empty sections.
3. Generate one image prompt per selected section.
4. Save generated images to the output directory using the article slug family when possible.
5. Insert image markdown below the matching headings.

## Fallback Guidance

- If no eligible section headings exist, report that the article is not illustration-ready yet.
- If image generation fails, preserve the article content and return a partial-completion summary.

## References

- `references/insertion-rules.md` - article spot detection and insertion behavior
- `../../docs/overview/article-artifact-family.md` - recommended file family for brief, draft, cover, and inline images
