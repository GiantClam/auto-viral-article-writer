# Contributing

Thanks for considering a contribution.

## Scope

This repository packages a content-production workflow as reusable skills. Good contributions usually improve one of these layers:

- skill instructions in `skills/<name>/SKILL.md`
- supporting references under `skills/<name>/references/`
- deterministic tooling under `tools/`
- repository-facing docs under `README.md`, `README.en.md`, or `docs/`

## Contribution Guidelines

1. Keep skill instructions focused and readable.
2. Put detailed rules into `references/` instead of bloating `SKILL.md`.
3. Do not hardcode secrets, private gateways, or personal credentials.
4. Preserve output path conventions unless there is a strong reason to change them.
5. Update public-facing docs when behavior or structure changes.

## Suggested Workflow

1. Make the smallest correct change.
2. Update any affected skill docs.
3. Update `MANIFEST.txt` when package contents change.
4. Verify that internal paths still point to real files.

## Areas That Need Care

- provider-specific image generation behavior
- ViralKB schema assumptions
- relative path assumptions across agent platforms
- generated output conventions used by downstream flows
