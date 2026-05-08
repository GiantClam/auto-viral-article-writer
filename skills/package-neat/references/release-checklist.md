# Release Checklist

Before treating the package as release-ready, confirm:

- all skills listed in `skills/index.md` exist
- `README.md` and `README.en.md` describe the current structure
- `docs/skills/` contains a page for every public skill
- `MANIFEST.txt` includes all packaged docs and skill files
- `LICENSE`, `CONTRIBUTING.md`, and `.gitignore` are present
- no stale flat-file paths remain after directory migrations
- no secrets or private gateway details are present in committed docs
- `docs/examples/smoke-test.md` still matches the current package workflow
- `CHANGELOG.md` is present and recent changes are reflected there when needed
- `docs/release/release-process.md` still matches the current release expectations
- `python tools/repo_consistency.py` passes on the current repository state
