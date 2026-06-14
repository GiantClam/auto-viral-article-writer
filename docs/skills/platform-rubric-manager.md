# platform-rubric-manager

## Purpose

Maintain one scoring rubric per platform and update it only when repeated retro signals justify a change.

## Use Cases

- creating a WeChat, X, Xiaohongshu, TikTok, Reddit, dev.to, or Facebook rubric
- updating a rubric after repeated misses or wins
- comparing old and proposed rubric versions

## Trigger Examples

- `update wechat rubric`
- `compare old and new x rubric`
- `review xiaohongshu scoring rules`

## Inputs

- platform name
- optional retro findings
- optional existing rubric file

## Outputs

- platform rubric revision
- change summary
- tighter scoring rules for later content evaluation

## Boundary

This skill manages standards. It does not write content or score a live draft directly.
