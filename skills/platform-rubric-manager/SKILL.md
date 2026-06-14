---
name: platform-rubric-manager
description: Use when a content system needs platform-specific scoring rules, or when retro results should update the rubric for WeChat, Xiaohongshu, X, TikTok, Facebook, Reddit, or dev.to.
version: 1.0.0
---

# Platform Rubric Manager

Use this skill when platform-level judgment standards need to be created, reviewed, compared, or updated.

## Use This For

- creating one rubric per platform
- reviewing the current rubric before scoring content
- updating a rubric after repeated retro signals
- comparing old and new rubric versions

## Do Not Use This For

- writing the source article
- rewriting platform drafts
- scoring a specific draft directly
- publishing content

## Inputs

- platform name
- optional existing rubric file
- optional retro findings
- optional benchmark examples

## Outputs

- platform rubric draft or revision
- concise change summary
- explicit notes on what was added, removed, or tightened

## Recommended File Layout

```text
rubrics/
  wechat.yaml
  xiaohongshu.yaml
  x.yaml
  tiktok.yaml
  facebook.yaml
  reddit.yaml
  devto.yaml
```

## Rubric Structure

Each platform rubric should define at minimum:

- platform goal
- audience expectation
- scoring dimensions
- strong signals
- risk signals
- tone rules
- CTA rules when relevant

Example shape:

```yaml
platform: wechat
goal: build authority and complete an argument
dimensions:
  - title_strength
  - opening_grab
  - structure_depth
  - information_density
  - insight_strength
strong_signals:
  - result-first opening
  - clear section rhythm
  - concrete examples supporting a judgment
risk_signals:
  - opening too slow
  - generic conclusion
  - weak title promise
```

## Modes

### 1. View

Use when a platform draft is about to be scored and the current rubric must be checked first.

### 2. Update

Use when retro results show repeated misses or repeated wins that should change future judgment.

### 3. Diff

Use when comparing an old rubric and a proposed new rubric.

### 4. Promote

Use when a revised rubric is judged better and should replace the working version.

## Core Pattern

1. Keep one rubric per platform.
2. Do not merge all platforms into one universal scoring file.
3. Update a rubric only after repeated evidence, not one random outlier.
4. Prefer small explicit changes over full rewrites.

## Common Mistakes

- Using one rubric across all platforms.
- Updating the rubric after a single surprising result.
- Letting tone rules stay vague.
- Keeping old dimensions that no longer explain results.

## Quick Rules

- Platform logic is local, not universal.
- Retro data should refine the rubric, not replace judgment.
- Small repeated misses matter more than one lucky hit.
- Rubrics should become sharper over time, not longer by default.
