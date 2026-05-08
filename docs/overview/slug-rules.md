# Slug Rules

This package uses one stable slug to tie a brief, article draft, cover image, and inline images into the same article artifact family.

## Core Rule

Generate the slug once, then reuse it for all downstream artifacts.

## Recommended Slug Format

- lowercase
- words separated by hyphens
- no spaces
- no punctuation other than hyphens
- avoid dates unless the workflow explicitly needs versioned duplicates

## Good Examples

- `claude-code-workflow-shift`
- `ai-image-prompt-patterns`
- `nano-banana-cover-guide`

## Bad Examples

- `Claude Code Workflow Shift`
- `claude_code_workflow_shift`
- `claude-code-workflow-shift!!!`

## Source Of Truth

Prefer the slug from the brief file if it already exists. Do not regenerate a new slug for later artifacts unless there is a deliberate versioning reason.

## Duplicate Handling

If a topic would naturally map to the same slug as an older article, add a meaningful suffix rather than a random one.

Examples:

- `claude-code-workflow-shift-v2`
- `claude-code-workflow-shift-followup`
- `claude-code-workflow-shift-xiaohongshu`

## Practical Rule

Slug stability is more important than slug cleverness. Once a brief exists, keep the slug family stable.
