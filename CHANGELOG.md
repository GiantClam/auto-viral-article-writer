# Changelog

All notable repository-level changes to `skill-packaging` should be recorded here.

## 2026-05-29

### Added

- multi-platform content workflow skills: `repurpose-content`, `article-score-retro`, `platform-rubric-manager`, `multi-platform-content`
- platform rubric files under `rubrics/` for WeChat, Xiaohongshu, X, TikTok, Reddit, dev.to, and Facebook
- `docs/runbooks/multi-platform-content-demo-runbook.md` for a full content-package demo path
- `docs/skills/` showcase pages for the new multi-platform skills
- `docs/skills/last30days.md` as the public-facing overview page for the bundled `last30days` skill
- `skills/last30days` as a Git submodule pointing at the upstream `mvanhorn/last30days-skill` repository

### Changed

- `write-article` now explicitly hands off to `cover-image` before `article-illustrate`, and optionally to `repurpose-content` after the mother draft is complete
- `README.md` and `README.en.md` now describe the package as a multi-platform content system, not only a single article workflow
- `skills/index.md` now exposes the multi-platform workflow chain and the new skills
- `docs/skills/README.md` now includes the new skills in the public showcase index
- `docs/overview/skill-package-overview.md` now documents the multi-platform distribution path
- `docs/overview/article-artifact-family.md` now recognizes `output/content/{slug}/` as part of the article artifact family
- `docs/install/README.md` now documents submodule initialization for bundled external skills

### Repository Outcome

- the package now behaves like a content middle layer: mother draft -> native rewrites -> scoring/prediction/retro -> rubric evolution
- the repository now keeps the external `last30days` skill as a submodule instead of flattening it into the main tree
- public docs and manifest files now reflect the expanded multi-platform workflow

## 2026-05-08

### Added

- bilingual repository entry with `README.md` and `README.en.md`
- platform installation guide under `docs/install/README.md`
- package overview docs under `docs/overview/`
- per-skill public showcase docs under `docs/skills/`
- article brief schema, templates, and brief-first workflow guidance
- `research-brief` skill for source-backed brief development
- `package-neat` skill for package-level sync and release readiness
- `article-audit` skill for artifact-family auditing
- end-to-end workflow example and smoke-test docs
- article artifact family rules and slug rules
- `cover-image` skill: `--article-title` injection for generations endpoint, `--ref` for img2img (edits) endpoint; title-only path renders text more cleanly
- `--article-title` argument in `nanobanana_client.py`: auto-injects article title into built-in portrait prompt

### Changed

- migrated all major skills to directory-style `SKILL.md` packaging
- rewrote the README to be product-first instead of tool-first
- expanded `write-article` with HKR gating, article archetypes, editorial boundaries, and stronger quality checks
- expanded `hot-topics` and `viral-mining` with source-discipline and research-sufficiency guidance
- aligned package outputs around reusable brief, draft, cover, and inline-image conventions
- `cover-image` skill: updated generation pathway documentation to clarify generations vs. edits endpoint selection
- `nanobanana_client.py`: `--article-title` without `--ref` now uses generations endpoint for cleaner text rendering; `--ref` enables img2img for higher subject likeness
- `docs/skills/cover-image.md`: added generation pathway table

### Repository Outcome

- the package now behaves more like a public skill repository than a local prompt bundle
- the content workflow now has a clearer research -> brief -> pattern -> draft -> image -> audit path
