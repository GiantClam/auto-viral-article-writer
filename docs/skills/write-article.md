# write-article

## Purpose

Run the main article workflow from research to draft output.

## Use Cases

- WeChat article drafting
- topic-to-draft production
- markdown output generation for later visual enrichment

## Trigger Examples

- `写文章`
- `生成文章`
- `公众号文章`
- `create article`

## Inputs

- topic
- source material
- target platform
- optional article brief

## Outputs

- article markdown under `output/`
- title candidates
- illustration-ready section structure
- completed or refined article brief when needed
- article drafts that can trace back to `output/briefs/{slug}-brief.yaml`

## Boundary

`write-article` owns the draft. `article-illustrate` and `cover-image` handle visual completion after the text exists.

It now prefers to consume a structured article brief instead of loose research fragments whenever possible.

When available, that brief should come through `research-brief` rather than directly from raw topic discovery.

When a stable slug exists, the draft should ideally be saved as `output/wechat/{slug}-article.md` so the rest of the artifact family can follow the same naming.

Do not silently regenerate a different slug if the brief already established one.

Start from `templates/article-brief.yaml` when a concrete reusable brief file is needed.
