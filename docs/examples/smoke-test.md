# Smoke Test

This is the fastest reasonable path to confirm that the package is installed correctly and that the core workflow is usable.

## Goal

Prove that the package can:

- read configuration
- discover or accept a topic
- create a reusable brief artifact
- produce a draft path convention
- support at least one image-producing step if credentials exist

## Prerequisites

1. Dependencies installed
2. `config/.env` configured with at least one image provider
3. `output/briefs/`, `output/wechat/`, and `output/images/wechat/` created
4. `python tools/config_loader.py` succeeds

## Minimal Smoke Path

### Step 1 - Run setup

Trigger:

- `setup`

Expected result:

- preferences can be created or read
- package configuration is recognized

### Step 2 - Create or refine a topic

Use either:

- `hot-topics`
- or a direct user-provided topic if live topic discovery is not available

Expected result:

- one candidate topic with enough signal to continue

### Step 3 - Produce a brief

Use:

- `research-brief`

Expected artifact:

- `output/briefs/{slug}-brief.yaml`

### Step 4 - Produce a draft

Use:

- `write-article`

Expected artifact:

- `output/wechat/{slug}-article.md`

### Step 5 - Produce at least one visual artifact

Use either:

- `cover-image`
- or `image-generation`

Expected artifact:

- `output/images/wechat/{slug}-cover-final.png`
  or
- another valid image output proving the image toolchain works

### Step 6 - Run audit

Use:

- `article-audit`

Expected result:

- artifact family status summary
- clear report on what exists and what is still missing

## Minimum Pass Condition

Treat the smoke test as passed when all of these are true:

- configuration loads successfully
- one brief file exists
- one draft file exists
- one image-producing path succeeds
- `article-audit` can report on the slug family without ambiguity

## If The Smoke Test Fails

Check these first:

- missing API keys
- missing output directories
- `opencli` unavailable for live topic collection
- inconsistent slug naming across brief and draft
- image provider misconfiguration

Use this document together with:

- `docs/examples/article-workflow-example.md`
- `docs/overview/article-artifact-family.md`
- `docs/overview/slug-rules.md`
- `python tools/repo_consistency.py`
