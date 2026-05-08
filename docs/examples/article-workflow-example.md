# End-to-End Article Workflow Example

This example shows how one article can move through the package from topic discovery to artifact-family audit.

## Scenario

Assume the working topic is:

- `Claude Code workflow shift`

Assume the chosen slug is:

- `claude-code-workflow-shift`

## Step 1 - Topic Discovery

Use `hot-topics` to discover whether the topic is timely and interesting enough to continue.

Expected outcome:

- topic signal exists
- source quality is at least usable
- the topic can seed a brief

## Step 2 - Research Brief

Use `research-brief` to deepen the topic and produce a reusable brief file.

Expected artifact:

- `output/briefs/claude-code-workflow-shift-brief.yaml`

Expected brief contents:

- angle
- audience
- HKR notes
- archetype
- hook
- source set
- risk notes

## Step 3 - Pattern Enrichment

Use `viral-patterns` to attach:

- title formulas
- emotional triggers
- structure suggestions

These findings should enrich the existing brief instead of becoming an isolated note.

## Step 4 - Draft Creation

Use `write-article` with the brief-first workflow.

Expected artifact:

- `output/wechat/claude-code-workflow-shift-article.md`

Expected relationship:

- the article draft reuses the same slug established by the brief
- the brief remains the source of truth for angle and structure

## Step 5 - Inline Illustrations

Use `article-illustrate` if the article should contain section visuals.

Expected artifacts:

- `output/images/wechat/claude-code-workflow-shift-01.png`
- `output/images/wechat/claude-code-workflow-shift-02.png`
- `output/images/wechat/claude-code-workflow-shift-03.png`

The exact number of images can vary, but the slug family should stay stable.

## Step 6 - Cover Image

Use `cover-image` to generate the cover.

Expected artifact:

- `output/images/wechat/claude-code-workflow-shift-cover-final.png`

## Step 7 - Article Audit

Use `article-audit` with the slug:

- `claude-code-workflow-shift`

Expected checks:

- brief exists
- article draft exists
- cover exists
- inline images exist if the workflow required them
- all files use the same slug family

Expected readiness result:

- `A4 - Publish Ready` if all required artifacts exist and are consistently named

## Summary Of Final Artifact Family

```text
output/briefs/claude-code-workflow-shift-brief.yaml
output/wechat/claude-code-workflow-shift-article.md
output/images/wechat/claude-code-workflow-shift-01.png
output/images/wechat/claude-code-workflow-shift-02.png
output/images/wechat/claude-code-workflow-shift-03.png
output/images/wechat/claude-code-workflow-shift-cover-final.png
```

## Why This Example Matters

This is the intended package shape:

- one topic
- one stable slug
- one brief-first workflow
- one article artifact family
- one audit step before calling the article publish-ready
