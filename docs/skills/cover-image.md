# cover-image

## Purpose

Generate a polished article cover image aligned with the package's article workflow.

## Use Cases

- cover generation for a completed article
- reference-photo-based thumbnail composition

## Trigger Examples

- `生成封面`
- `文章封面`
- `cover image`

## Inputs

- article path or slug
- optional explicit title
- reference image path

## Outputs

- final cover image in `output/images/wechat/`

## Artifact Convention

Prefer the same slug family as the brief and article draft, for example `output/images/wechat/{slug}-cover-final.png`.

If a brief or draft already exists, inherit its slug exactly.

## Boundary

This skill is for the hero cover image, not for inline article illustrations.
