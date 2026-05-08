# Skill Package Overview

`skill-packaging/` is organized as a public-facing skill repository rather than a loose prompt dump.

## Design Goals

- make the package easy to understand before installation
- keep complex skill instructions in `SKILL.md`
- move detailed guidance into `references/`
- keep deterministic work in Python tools
- preserve a stable output layout for downstream automation

## Package Layers

### 1. Skills

Each skill lives under `skills/<name>/` and exposes a `SKILL.md` entry point.

### 2. References

Detailed rules, scoring notes, and output specs live under `skills/<name>/references/`.

### 3. Tools

Deterministic execution lives in `tools/`, including:

- `nanobanana_client.py`
- `article_illustrate.py`
- `opencli_fetcher.py`
- `viral_kb.py`

### 4. Config

Environment and user preference files live in `config/`.

### 5. Outputs

Generated content is written under `output/`.

Notable subpaths:

- `output/briefs/` for reusable article brief files
- `output/wechat/` for draft articles
- `output/images/` for generated visuals

See `docs/overview/article-artifact-family.md` for the naming convention that ties a brief, article draft, cover image, and inline images to the same slug.

See `docs/overview/slug-rules.md` for how that slug should be generated and reused.

See `docs/examples/article-workflow-example.md` for a concrete end-to-end path through the package.

See `docs/examples/smoke-test.md` for the fastest practical test path through the package.

## Main Workflows

### Topic Discovery

`setup` -> `hot-topics`

### Brief Development

`hot-topics` -> `research-brief`

### Pattern Reuse

`research-brief` -> `viral-patterns`

### Article Production

`write-article` -> `article-illustrate` -> `cover-image`

### Article Readiness Audit

`article-audit`

## Shared Handoff Object

The package now uses an article brief concept as the structured handoff between:

- `hot-topics` topic framing
- `research-brief` source-backed angle development
- `viral-patterns` pattern reuse
- `write-article` drafting

See `skills/write-article/references/article-brief-schema.md` for the current shared schema.

Concrete reusable templates live at:

- `templates/article-brief.yaml`
- `templates/article-brief.example.yaml`

## Public Repository Intent

This package is structured so it can be understood by:

- someone evaluating the repo for the first time
- someone installing the skills into an agent platform
- someone extending the package with new content-production skills
