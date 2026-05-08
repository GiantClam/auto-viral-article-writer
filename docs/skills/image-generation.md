# image-generation

## Purpose

Generate standalone images outside the article pipeline.

## Use Cases

- direct prompt-to-image generation
- provider-specific image runs
- image edits with reference files

## Trigger Examples

- `生成图片`
- `create image`
- `generate image`
- `draw`

## Inputs

- prompt
- output path
- optional provider flags
- optional reference image

## Outputs

- saved image file
- provider-used summary

## Boundary

Use this when the request is image-first. Use `cover-image` or `article-illustrate` when the image belongs to the article workflow.
