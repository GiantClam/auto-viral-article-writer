---
name: package-neat
description: This skill should be used when the user asks to "整理一下", "同步文档", "收尾", "release audit", "skill audit", "sync the package", or wants to reconcile package docs, indexes, manifests, and public-facing metadata after changing the skill package. It checks repository consistency and updates the package-facing knowledge layer.
version: 1.0.0
---

# Package Neat

Use this skill when work on `skill-packaging/` is functionally done and the package needs a consistency pass before handoff or release.

## Use This For

- syncing README, indexes, manifests, and showcase docs
- checking whether a new skill is reflected everywhere it should be
- final package cleanup before release or handoff

## Do Not Use This For

- writing a new feature from scratch
- generating article content
- replacing normal test or tool verification

## Workflow

1. Enumerate package-facing docs and indexes.
2. Compare actual skill directories with public docs.
3. Check manifest and overview files for missing entries.
4. Update release-facing docs when structure changed.
5. Summarize what was synced and what still needs human confirmation.

## References

- `references/sync-matrix.md` - which package files should change for each kind of repository change
- `references/release-checklist.md` - public-release consistency checklist
