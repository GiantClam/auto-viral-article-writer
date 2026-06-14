# Rubrics

This directory stores platform-specific content judgment rules for the writer system.

These rubric files are used after a source article exists and before or after platform distribution.

## Purpose

Rubrics exist to keep platform judgment local.

Do not use one universal standard for all platforms.

Each platform has different expectations for:

- title style
- opening rhythm
- tone
- scannability
- discussion value
- share/save behavior

The rubric files help the system judge drafts by the target platform's real logic instead of the source platform's logic.

## Current Files

- `wechat.yaml`
- `xiaohongshu.yaml`
- `x.yaml`
- `tiktok.yaml`
- `reddit.yaml`
- `devto.yaml`
- `facebook.yaml`

## How To Use

Recommended workflow:

1. Generate the mother draft with `write-article`.
2. Rewrite the mother draft into platform-native versions with `repurpose-content`.
3. Score each platform draft with `article-score-retro` using the matching rubric.
4. Save a blind prediction file before publish.
5. Publish the platform draft.
6. Run T+3 or T+7 retro after results are available.
7. If repeated misses or repeated wins appear, update the matching rubric with `platform-rubric-manager`.

## Update Rules

Rubrics should not change after one surprising result.

Prefer updating a rubric only when:

- the same weakness appears repeatedly
- a repeated strong pattern becomes obvious
- the old dimension no longer explains outcomes
- the platform's native format expectations clearly shifted

Good update behavior:

- small changes
- explicit wording
- remove vague or dead dimensions
- sharpen strong signals and risk signals

Bad update behavior:

- rewriting the whole rubric after one outlier
- merging multiple platform rules into one file
- adding generic advice that applies everywhere and means nothing locally

## Relationship To Ledger Files

Rubrics work together with the content ledger files created by `article-score-retro`.

Typical structure:

```text
output/content/{slug}/
  source.md
  wechat.md
  x.md
  xiaohongshu.md
  tiktok.md
  facebook.md
  reddit.md
  devto.md
  score-{platform}.json
  predict-{platform}.json
  retro-{platform}-t3.json
  retro-{platform}-t7.json
```

Rubrics define the platform logic.

Ledger files capture how real content performed against that logic.

## Practical Principle

Rubrics should become sharper over time, not longer by default.

The goal is not to create a content theory museum.

The goal is to help the next draft get judged more accurately.
