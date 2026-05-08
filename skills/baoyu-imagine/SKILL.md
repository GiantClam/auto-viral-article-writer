---
name: baoyu-imagine
description: This skill should be used when the user asks for "baoyu-imagine", or uses older image-generation wording from the original baoyu workflow. It acts as a compatibility alias and routes users to the package's canonical image generation skill.
version: 1.0.0
---

# Baoyu Imagine

Use this as a compatibility alias for users who know the upstream `baoyu-imagine` naming but should still run this package's local `image-generation` skill.

## Use This For

- compatibility with older wording
- redirecting image requests into the canonical package flow

## Do Not Use This For

- maintaining a separate image backend policy
- duplicating image-generation implementation details

## Inputs

- same core inputs as `image-generation`

## Outputs

- same output behavior as `image-generation`

## Workflow

1. Explain that this is an alias.
2. Follow `image-generation/SKILL.md`.
3. Keep provider examples generic and package-safe.

## Fallback Guidance

- If users reference upstream private or provider-specific details, strip those details and continue with the package-supported provider model.

## References

- `references/alias-policy.md` - what should and should not be mirrored from upstream naming
