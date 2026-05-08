# article-illustrate

## Purpose

Analyze an existing article draft and insert generated illustrations into the markdown body.

## Use Cases

- turning section headings into image slots
- enriching a finished article draft with visuals

## Trigger Examples

- `生成插图`
- `文章配图`
- `illustrate article`

## Inputs

- article markdown path
- optional style hint
- optional image count limit

## Outputs

- generated image files
- updated article markdown

## Artifact Convention

Prefer inline image names that stay in the same article slug family, such as `output/images/wechat/{slug}-01.png`.

## Boundary

This skill works on an existing article. It does not create the article itself.
