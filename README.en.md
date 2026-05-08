# Auto Viral Article Writer

AI content creation skill package for agents: hot topics -> viral patterns -> article drafting -> illustrations -> cover image.

![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)
![Skills](https://img.shields.io/badge/Skills-12-10B981?style=for-the-badge)
![Platforms](https://img.shields.io/badge/Platforms-5-F59E0B?style=for-the-badge)

**Supported Platforms:** OpenCode, Codex, Claude Code, OpenClaw, Hermes

This repository packages a repeatable content workflow as installable skills. It is meant for people who want an agent to discover timely topics, reuse proven viral structures, draft long-form articles, and generate matching visuals with predictable local outputs.

---

## What It Solves

- Finds current topics across Chinese and global sources
- Reuses proven viral structures instead of starting from zero every time
- Produces article drafts with a stable markdown format
- Generates illustrations and cover images through the same toolchain
- Keeps the workflow portable across multiple agent platforms

## Good Fit

- WeChat article production
- AI and SaaS topic research
- Pattern-based long-form drafting
- Teams that want reusable content-production skills

## Not A Good Fit

- General-purpose blogging with no topic research step
- Users who only want a standalone image generator
- Users who want a hosted product instead of a local skill package
- Workflows that do not want local `output/`, `config/`, and `data/viralkb/` directories

---

## Skills

| Skill | What It Does | Trigger Examples |
|---|---|---|
| `setup` | First-time configuration and verification | `setup`, `configure`, `set this up` |
| `hot-topics` | Collects current topics from multiple sources | `今日热榜`, `AI热榜`, `what's trending today` |
| `research-brief` | Turns a promising topic into a stronger source-backed brief | `research brief`, `deep brief`, `help me frame this topic first` |
| `viral-patterns` | Retrieves reusable title and structure patterns from ViralKB | `viral patterns`, `find title formulas`, `check article structure` |
| `viral-mining` | Discovers and ingests high-signal content into ViralKB | `viral mining`, `discover viral content` |
| `write-article` | Runs the full article workflow from research to draft | `write article`, `create article`, `公众号文章` |
| `article-audit` | Audits whether one article family is complete and consistently named | `article audit`, `publish ready`, `check this article family` |
| `article-illustrate` | Inserts illustrations into an existing article | `illustrate article`, `insert images` |
| `cover-image` | Creates article cover images | `create cover`, `cover image` |
| `image-generation` | Direct image generation outside the article pipeline | `create image`, `generate image`, `draw` |
| `baoyu-imagine` | Compatibility alias for `image-generation` | `baoyu-imagine` |
| `package-neat` | Syncs package docs, manifests, and public-facing metadata | `sync the package`, `release audit`, `skill audit` |

See `skills/index.md` for the package-level skill index.

See `docs/skills/README.md` for public-facing skill showcase pages.

---

## Typical Flow

```text
setup
  -> hot-topics
  -> research-brief
  -> viral-patterns
  -> write-article
       -> article-illustrate
  -> cover-image
```

Expected outputs:

- topic summaries grouped by platform and category
- structured article briefs under `output/briefs/`
- local ViralKB pattern lookups
- markdown drafts such as `output/wechat/{slug}-article.md`
- inline images such as `output/images/wechat/{slug}-01.png`
- final cover images such as `output/images/wechat/{slug}-cover-final.png`
- auditable article artifact family status

---

## Installation

### Install dependencies

```bash
pip install python-dotenv requests feedparser numpy
```

### Configure API keys

```bash
cp config/.env.example config/.env
```

Fill in at least one image provider:

```bash
OPENAI_COMPATIBLE_API_KEY=your_key_here
OPENAI_COMPATIBLE_BASE_URL=https://your-openai-compatible-base-url
# OR
OPENAI_API_KEY=your_openai_key_here
# OR
GOOGLE_AI_API_KEY=your_google_key_here

JINA_API_KEY=your_jina_key_here
```

### Create output directories

```bash
mkdir -p output/briefs output/wechat output/images/wechat data/viralkb
```

### Run first-time setup

Say `setup`, `配置`, or `设置` to the agent, or run:

```bash
python scripts/setup.py
```

### Verify configuration

```bash
python tools/config_loader.py
python tools/opencli_fetcher.py --check
```

---

## Platform Installation

See `docs/install/README.md` for platform-specific guidance for:

- OpenCode
- Claude Code
- Codex
- OpenClaw
- Hermes

---

## Repository Structure

```text
skill-packaging/
├── README.md
├── README.en.md
├── MANIFEST.txt
├── docs/
│   ├── install/
│   └── overview/
├── skills/
├── tools/
├── config/
├── scripts/
├── templates/
└── data/
```

---

## Additional Docs

- Skill index: `skills/index.md`
- Skill showcase pages: `docs/skills/README.md`
- Package overview: `docs/overview/skill-package-overview.md`
- Article artifact family: `docs/overview/article-artifact-family.md`
- Slug rules: `docs/overview/slug-rules.md`
- End-to-end workflow example: `docs/examples/article-workflow-example.md`
- Smoke test: `docs/examples/smoke-test.md`
- Repository consistency check: `python tools/repo_consistency.py`
- Changelog: `CHANGELOG.md`
- Release process: `docs/release/release-process.md`
- Platform install guide: `docs/install/README.md`
- Article brief template: `templates/article-brief.yaml`
- Article brief example: `templates/article-brief.example.yaml`

---

## Troubleshooting

### No API key provided

Make sure `config/.env` contains at least one configured image provider.

### `viral-patterns` returns nothing

Populate ViralKB with `viral-mining`, or let `hot-topics` auto-ingest qualifying results first.

### `article_illustrate.py` inserts nothing

Make sure the article contains `**bold section headings**` after the `---` divider.

### `opencli` returns no results

Check that Chrome is running, the target site is logged in, the OpenCLI Browser Bridge extension is enabled, and `python tools/opencli_fetcher.py --check` succeeds.

### Cover image reference missing

`cover-image` expects a user-provided `--ref` portrait or reference image path.
