# article-score-retro

## Purpose

Score, predict, and retro platform drafts with a persistent experiment ledger.

## Use Cases

- pre-publish scoring
- blind prediction before publish
- T+3 or T+7 retrospective after publish

## Trigger Examples

- `score this post for X`
- `predict this Xiaohongshu post`
- `retro this WeChat article`

## Inputs

- draft path
- platform
- optional actual metrics for retro

## Outputs

- score summary
- blind prediction
- retrospective notes
- ledger files in `output/content/{slug}/`

## Ledger Contract

This skill is only useful when the judgment is written to files.

Expected file family:

- `score-{platform}.json`
- `predict-{platform}.json`
- `retro-{platform}-t3.json`
- `retro-{platform}-t7.json`

Prediction must be saved before publish. Retro must reference the saved prediction.
