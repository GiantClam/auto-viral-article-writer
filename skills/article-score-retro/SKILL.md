---
name: article-score-retro
description: Use when a platform draft already exists and you need pre-publish scoring, blind prediction, or post-publish retrospective for WeChat, Xiaohongshu, X, TikTok, Facebook, Reddit, or dev.to.
version: 1.0.0
---

# Article Score Retro

Use this skill when a draft is already written and the next step is to evaluate it before publishing or learn from it after publishing.

## Use This For

- scoring a draft before publish
- making a blind prediction before publish
- running a T+3 or T+7 retrospective after publish
- comparing expected performance with actual performance

## Do Not Use This For

- topic research
- first-pass writing
- platform rewriting
- cover image generation

## Inputs

- article or post path
- target platform
- optional goal
- optional actual metrics for retro

## Outputs

- structured score summary
- structured blind prediction
- structured retrospective notes
- short list of rubric update suggestions when useful
- persisted experiment ledger files for score, prediction, and retro

## Modes

### 1. Score

Use when the draft is not yet published.

Output should include:

- overall judgment
- 4-6 dimension scores
- top strengths
- top risks
- concrete revision advice

### 2. Predict

Use when the draft is about to be published.

Output should include:

- expected performance band
- what the post is likely to do well
- what may underperform
- why this prediction is being made

This prediction should be written before results are known.

The prediction must be saved as a file before publish.

### 3. Retro

Use when results are already available.

Output should include:

- what worked
- what missed
- where the original prediction was right
- where the original prediction was wrong
- what should change next time

Retro must explicitly reference the earlier saved prediction.

If repeated misses or repeated wins appear, hand the findings to `platform-rubric-manager`.

## Ledger Contract

Every scored or published content unit should have a stable content folder.

Recommended structure:

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

Minimum rule set:

1. `score` writes a structured score file.
2. `predict` writes a blind prediction file before publish.
3. `retro` reads the original prediction file before writing conclusions.
4. Do not overwrite old prediction files after results are known.

## File Expectations

### Score File

Should include at minimum:

- platform
- date
- overall judgment
- dimension scores
- strengths
- risks
- revision advice

### Prediction File

Should include at minimum:

- platform
- date
- expected performance band
- why this outcome is expected
- main upside
- main risk

### Retro File

Should include at minimum:

- platform
- date
- actual result summary
- where the prediction was right
- where the prediction was wrong
- what changes next time
- rubric update suggestion if applicable

## Platform Lens

- WeChat: title strength, opening depth, section rhythm, authority, insight.
- Xiaohongshu: cover promise, first-screen hook, saveability, scannability, emotional resonance.
- X: first-line sharpness, point density, repost potential, discussion energy.
- TikTok: first-3-second hook, spoken rhythm, retention potential, simplicity.
- Facebook: readability, social tone, commentability, low-friction sharing.
- Reddit: authenticity, discussion fit, anti-marketing tone, information value.
- dev.to: technical clarity, credibility, example quality, implementation usefulness.

## Core Pattern

1. Identify the platform first.
2. Judge the draft by that platform's native logic.
3. Write the score file before publish.
4. Write the blind prediction file before publish.
5. Do not reuse another platform's rubric blindly.
6. Keep prediction separate from retrospective.
7. Use the saved prediction during retro.

## Common Mistakes

- Scoring all platforms with one universal standard.
- Writing vague praise instead of concrete revision advice.
- Doing retro without recording the original prediction.
- Confusing traffic results with content quality alone.
- Editing a prediction after seeing results.
- Skipping file persistence and leaving the process as chat-only advice.

## Quick Rules

- Publish-time judgment and post-publish learning are separate steps.
- Platform fit matters as much as writing quality.
- Short feedback beats generic feedback.
- Retro should improve the next draft, not just explain the last one.
- If it is not written to the ledger, it does not count as part of the workflow.
