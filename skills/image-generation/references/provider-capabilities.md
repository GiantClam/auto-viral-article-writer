# Provider Capabilities

## OpenAI-compatible Images API

- best default when the package is configured for it
- supports generation and edit-style flows used by this package
- requires `OPENAI_COMPATIBLE_API_KEY` and `OPENAI_COMPATIBLE_BASE_URL`

## OpenAI Official Images API

- good fallback when OpenAI-compatible routing is not configured
- requires `OPENAI_API_KEY`

## Gemini Official Image Generation

- useful as another configured fallback
- requires `GOOGLE_AI_API_KEY`

## Selection Guidance

- use the user-requested provider if explicitly stated
- otherwise prefer the configured default order from the package
- keep prompts provider-neutral in skill docs whenever possible
