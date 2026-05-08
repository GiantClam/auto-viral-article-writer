# Release Process

This document describes the recommended release path for `skill-packaging`.

## Goal

Make sure the repository is internally consistent, the public docs still reflect reality, and the example workflows are still valid before treating a version as release-ready.

## Release Flow

### 1. Sync Package Docs

Run the package-level consistency pass conceptually covered by `package-neat`.

Check:

- `README.md`
- `README.en.md`
- `skills/index.md`
- `docs/skills/`
- `MANIFEST.txt`
- `docs/overview/`

### 2. Verify Workflow Docs

Confirm that these still reflect the actual package shape:

- `docs/examples/article-workflow-example.md`
- `docs/examples/smoke-test.md`
- `docs/overview/article-artifact-family.md`
- `docs/overview/slug-rules.md`

### 3. Verify Core Artifacts

Make sure the package still clearly supports these concepts:

- brief template
- brief-first workflow
- article artifact family
- article audit path

### 4. Run Smoke Path

Use `docs/examples/smoke-test.md` as the minimum release check path.

### 5. Run Repository Consistency Check

Run:

```bash
python tools/repo_consistency.py
```

This catches common repository drift such as skill count mismatches, missing showcase docs, or stale manifest entries.

### 6. Confirm Public Metadata

Check:

- `LICENSE`
- `CONTRIBUTING.md`
- `.gitignore`
- `CHANGELOG.md`

### 7. Update Changelog

Add a new section to `CHANGELOG.md` summarizing:

- new skills
- major documentation changes
- workflow changes
- output convention changes

## Release Readiness Standard

Treat the repository as release-ready only when:

- public docs are consistent
- skill count and skill list match reality
- no stale paths remain
- smoke-test still makes sense
- artifact family and slug rules still match current outputs
