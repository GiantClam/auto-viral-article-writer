---
name: multi-platform-content
description: Use when one topic should become a mother draft plus native posts for multiple platforms, with scoring, prediction, and retrospective built into the workflow.
version: 1.0.0
---

# Multi Platform Content

Use this skill when one core idea needs to become a complete multi-platform content package.

## Use This For

- turning one topic into a WeChat mother draft and multiple platform-native variants
- running a controlled content workflow from draft to distribution to retro
- keeping article production, repurposing, scoring, and rubric evolution in one sequence

## Do Not Use This For

- one-off article drafting with no distribution plan
- isolated cover-only work
- isolated image-only work

## Inputs

- topic or source material
- target platforms
- optional audience
- optional launch goal

## Outputs

- a WeChat mother draft
- platform-native content variants
- score and prediction files
- retro files after publish
- rubric update candidates when repeated patterns appear

## Workflow

1. Use `write-article` to create the WeChat mother draft.
2. Use `cover-image` to create the article cover.
3. Use `repurpose-content` to create platform-native versions.
4. Use `article-score-retro` in `score` mode before publish.
5. Use `article-score-retro` in `predict` mode before publish.
6. Publish the content.
7. Use `article-score-retro` in `retro` mode at T+3 or T+7.
8. If repeated misses or wins appear, use `platform-rubric-manager` to update the platform rubric.

## Recommended Platform Order

- WeChat first as the mother draft
- X and Xiaohongshu next for highest-value repurposing
- TikTok, Reddit, dev.to, and Facebook after the core text workflow is stable

## Content Ledger

Prefer using one shared content folder per topic:

```text
output/content/{slug}/
```

Store:

- the source article
- platform variants
- score files
- prediction files
- retro files

## Core Principle

Do not treat multi-platform publishing as copy-paste distribution.

Treat it as:

- one core idea
- multiple native packages
- separate judgment per platform
- shared learning across time

## Common Mistakes

- publishing the mother draft everywhere unchanged
- skipping score and going straight to publish
- doing retro without a saved prediction
- updating rubric from one random outlier

## Quick Rules

- One source idea, many native versions.
- Score before publish.
- Predict before results.
- Retro after real data.
- Update rubric only from repeated signals.
