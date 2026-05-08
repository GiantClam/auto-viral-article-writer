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

## Cover Prompt Endpoint Behavior

This tool supports two image generation pathways:

| Situation | Endpoint used | Why |
|---|---|---|
| `--article-title` without `--ref` | `generations` | img2img tends to drop text from the prompt; generations preserves title text clearly |
| `--ref` (with or without `--article-title`) | `edits` (img2img) | Reference photo drives subject likeness; best when combined with title written directly in `--prompt` |
| No `--ref`, no `--article-title`, no custom `--prompt` | `generations` | Default portrait cover prompt runs without ref |

### `--article-title` Usage

`--article-title "你的标题"` auto-injects the title into the built-in portrait prompt. It is most effective when used alone (no `--ref`), because it selects the generations endpoint for cleaner text rendering.

### Best Practice for High Similarity + Title

When you need both strong person likeness AND the title rendered cleanly, write the title directly in the prompt and use `--ref` to drive likeness via img2img:

```bash
python tools/nanobanana_client.py --openai-compatible-image \
  --ref "img/20260423-140003.jpg" \
  --prompt "Same person as reference photo. Keep same face and pose, but smaller in frame (about 20-25% of image on right side). Half-body shot, not cropped. Dynamic pose - one hand gesturing enthusiastically, slight smile with personality. Warm orange rim light on hair and shoulders. Left 65% of frame dominated by Chinese title '我研究了这个 auto-viral-article-writer 后，发现它最值钱的不是写文章，而是把整条内容链跑通' in large bold white font on semi-transparent dark overlay. Warm orange amber gradient background with subtle workflow elements. Style: reference photo quality preserved, photorealistic, editorial retouched, 16:9, no watermark." \
  --image-size 1024x1024 \
  --output "output/images/wechat/{slug}-cover-final.png"
```

## Fallback Guidance

- If no reference image is available, tell the user that the cleanest personal-brand result still depends on a user-supplied portrait.
- If no article exists yet, ask for a title or article path before generating the cover.

## References

- `references/cover-rules.md` - composition, palette, and output conventions
- `../../docs/overview/article-artifact-family.md` - recommended file family for brief, draft, cover, and inline images
- `../../docs/overview/slug-rules.md` - how to generate and reuse a stable slug
