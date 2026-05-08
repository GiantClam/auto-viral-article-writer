# Changelog

All notable repository-level changes to `skill-packaging` should be recorded here.

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
