---
name: image-generation
description: This skill should be used when the user asks to "生成图片", "create image", "generate image", "AI画图", "draw", or wants direct image generation outside the article workflow. It uses the local image generation CLI and supports OpenAI-compatible, OpenAI official, and Gemini image providers.
version: 1.0.0
---

# Image Generation

Use this skill for direct image creation or image edits when the user is not asking for the full article workflow.

## Use This For

- standalone image generation
- reference-image-based restyling
- provider-specific image runs using the local CLI

## Do Not Use This For

- full article production by itself
- ViralKB research
- hot topic collection

## Inputs

- prompt
- output path
- optional provider flags
- optional reference image path
- optional size, quality, and format overrides

## Outputs

- saved image file
- provider-used summary
- output path confirmation

## Workflow

1. Validate required inputs.
2. Confirm any reference files exist.
3. Choose the provider in this order unless the user overrides it:
   - OpenAI-compatible
   - OpenAI official
   - Gemini official
4. Run `tools/nanobanana_client.py` with the minimal correct arguments.
5. Return the saved image path.

## Fallback Guidance

- If one provider is unavailable, fall back to another configured provider when possible.
- If no provider is configured, stop and ask for environment setup rather than guessing.
- Do not hardcode private gateways, API keys, or provider-specific secrets in committed files.

## References

- `references/provider-capabilities.md` - provider differences and recommended usage
