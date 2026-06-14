---
name: repurpose-content
description: Use when turning one source article into native versions for WeChat, Xiaohongshu, X, TikTok, Facebook, Reddit, or dev.to, or when a mother draft needs platform-specific rewriting.
version: 1.0.0
---

# Repurpose Content

Use this skill when a source draft already exists and the next step is to adapt it for multiple platforms.

## Use This For

- turning a WeChat mother draft into platform-native posts
- rewriting one core idea for X, Xiaohongshu, TikTok, Facebook, Reddit, or dev.to
- keeping a single content source while changing tone, length, and hook per platform

## Do Not Use This For

- topic research
- first-pass article drafting
- scoring, prediction, or retro
- cover image generation

## Inputs

- source article path or draft text
- target platform
- optional platform goal
- optional tone or audience

## Outputs

- platform-native rewritten draft
- platform title options when useful
- concise notes on what changed from the source
- drafts should prefer a shared content folder such as `output/content/{slug}/`

## Core Pattern

1. Read the mother draft once.
2. Keep the core claim.
3. Rewrite for the target platform's format.
4. Tighten length, hook, and CTA for that platform.
5. Hand off the rewritten platform draft to `article-score-retro` before publish.

## Platform Guide

- WeChat: complete argument, sectioned, authority-oriented.
- Xiaohongshu: first-screen hook, scannable, saveable, practical.
- X: short, sharp, opinion-heavy, thread-friendly.
- TikTok: spoken cadence, strong opening, one idea per beat.
- Facebook: readable, conversational, low-friction.
- Reddit: honest, discussion-friendly, low-marketing tone.
- dev.to: technical clarity, examples, implementation bias.

## Common Mistakes

- Copying the mother draft too closely.
- Keeping the same title across platforms.
- Using the same CTA everywhere.
- Writing for the source platform instead of the target platform.

## Quick Rules

- Keep the core idea, change the packaging.
- Match each platform's native rhythm.
- Shorten aggressively where attention is scarce.
- Avoid platform-inappropriate marketing tone.
