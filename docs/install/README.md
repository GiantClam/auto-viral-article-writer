# Platform Installation Guide

This package can be installed in multiple agent environments. The exact skill directory differs by platform, but the package layout stays the same.

## Shared Requirements

1. Copy or clone `skill-packaging/` into a workspace-accessible location.
2. If you need bundled dependencies such as `skills/last30days/`, initialize submodules.
3. Install Python dependencies.
4. Configure `config/.env`.
5. Ensure the agent can read the `skills/` directory.
6. Create output paths including `output/briefs/` if you want reusable brief artifacts.

## Submodule Initialization

If you cloned the repository fresh, initialize bundled submodules before installation:

```bash
git submodule update --init --recursive
```

Current submodule:

- `skills/last30days/` → `https://github.com/mvanhorn/last30days-skill.git`

## OpenCode

Recommended location:

- workspace-local: `.opencode/skills/`
- global: `~/.config/opencode/skills/`

Practical approach:

1. Copy skill directories from `skill-packaging/skills/` into `.opencode/skills/`.
2. Keep `tools/`, `config/`, `scripts/`, and `data/` accessible from the same workspace.
3. Trigger `setup` to verify the package is usable.

## Claude Code

Typical skill discovery locations depend on the Claude Code environment and plugin layout. The important requirement is that each skill directory contains `SKILL.md` at its root.

Practical approach:

1. Place the skill directories where your Claude Code environment loads custom skills.
2. Keep the package-relative tools and config files in the same working project.
3. Trigger `setup` after install.

## Codex

Use the platform's custom skill loading mechanism and preserve the directory-style layout.

Practical approach:

1. Copy `skills/<name>/SKILL.md` directories into the configured Codex skill location.
2. Keep the Python tools and config folder together with the working repository.
3. Trigger `setup` and verify tool access.

## OpenClaw

Install the package into the custom skills area used by the OpenClaw environment.

Practical approach:

1. Copy the `skills/` subtree into the OpenClaw skill path.
2. Keep `tools/`, `config/`, and `scripts/` in the same project or a referenced package root.
3. Run the setup flow and verify the environment.

## Hermes

Use the custom skill import or local skill directory expected by the Hermes environment.

Practical approach:

1. Preserve the directory-style skill layout.
2. Keep the package root available so skill-relative documentation and tool paths remain meaningful.
3. Trigger `setup` as the first smoke test.

## Verification Checklist

After installation:

1. Confirm the agent can see the skills.
2. Trigger `setup`.
3. Run `python tools/config_loader.py`.
4. Run `python tools/opencli_fetcher.py --check` if social source collection is needed.
5. Run one image-generation smoke test if image output is required.
