---
name: cover-image
description: This skill should be used when the user asks to "生成封面", "文章封面", "create cover", "cover image", or wants a polished article cover image for an existing draft. It builds cover prompts and output paths around the package's article workflow.
version: 1.0.0
---

# Cover Image

Use this skill to generate a polished article cover image that matches the package's writing workflow and output conventions.

## Use This For

- cover generation for a drafted article
- thumbnail-style personal brand covers
- reference-photo-based cover composition

## Do Not Use This For

- generic illustration generation inside article sections
- full article drafting
- open-ended visual experimentation with no article context

## Inputs

- article slug or article path
- optional explicit title
- required or recommended reference photo path
- optional style direction

## Outputs

- generated cover image saved to `output/images/wechat/`
- prompt composition based on article title and layout rules
- cover output should reuse the same slug family as the brief and article draft when available

## Workflow

1. Determine the source article or article slug.
2. Read the first article title candidate if needed.
3. Build the cover prompt from the package's composition rules.
4. Call `tools/nanobanana_client.py` with the configured provider.
5. Save the image to the package's cover output path using the article slug family.

If the brief or article draft already established the slug, reuse it exactly.

## Fallback Guidance

- If no reference image is available, tell the user that the cleanest personal-brand result still depends on a user-supplied portrait.
- If no article exists yet, ask for a title or article path before generating the cover.

## References

- `references/cover-rules.md` - composition, palette, and output conventions
- `../../docs/overview/article-artifact-family.md` - recommended file family for brief, draft, cover, and inline images
- `../../docs/overview/slug-rules.md` - how to generate and reuse a stable slug
