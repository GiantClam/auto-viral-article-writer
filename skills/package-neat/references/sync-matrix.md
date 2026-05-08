# Sync Matrix

Use this matrix when something in `skill-packaging/` changes.

## New Skill Added

Update:

- `skills/index.md`
- `README.md`
- `README.en.md`
- `docs/skills/README.md`
- `docs/skills/<name>.md`
- `MANIFEST.txt`

## Skill Structure Changed

Update:

- `README.md` repository structure section
- `README.en.md` repository structure section
- `docs/overview/skill-package-overview.md`
- `MANIFEST.txt`

## New Reference Files Added

Update:

- `MANIFEST.txt`
- possibly `docs/overview/skill-package-overview.md` if the package organization changed materially

## New Provider Or Toolchain Rule

Update:

- relevant `SKILL.md`
- relevant `references/`
- install docs if environment expectations changed
- `.env.example` if configuration changed
