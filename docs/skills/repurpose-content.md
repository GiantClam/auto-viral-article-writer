# repurpose-content

## Purpose

Turn one mother draft into native versions for multiple platforms without copying the source format blindly.

## Use Cases

- WeChat mother draft to X, Xiaohongshu, TikTok, Facebook, Reddit, or dev.to
- one core idea adapted to multiple native content packages

## Trigger Examples

- `改写成 X 版本`
- `把这篇公众号文章改成小红书`
- `repurpose this article`

## Inputs

- source article path
- target platform
- optional audience
- optional tone

## Outputs

- platform-native rewritten draft
- title options when useful
- suggested placement in `output/content/{slug}/`

## Boundary

This skill does not research, write the first draft, score the post, or generate visuals.

It only changes the packaging so one source idea can fit the target platform.
