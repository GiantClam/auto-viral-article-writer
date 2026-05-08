# Source Priority

Prefer sources in this order when the same story appears across multiple places:

1. Official product, company, or release source
2. Primary long-form source such as a paper, official blog, or launch note
3. High-signal social post with strong engagement and clear attribution
4. RSS or discussion aggregation source

Use `opencli` for social and Chinese platform coverage. Use RSS for resilient fallback coverage when social automation is unavailable.

## Channel Roles

- `opencli`: best for fast-moving user sentiment, Chinese platforms, and platform-native signals
- RSS: best for stable fallback collection from HN and Reddit

Do not treat duplicate reposts as separate signals unless they represent clearly different audiences or reactions.

## Confidence Notes

- High confidence: original source or multiple independent confirmations
- Medium confidence: strong social signal with traceable attribution
- Low confidence: repeated chatter with weak sourcing

Prefer returning fewer higher-confidence items over flooding the user with thinly sourced noise.
