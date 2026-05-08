# Topic Scoring

Rank topics using a blended view of:

- engagement signal
- source quality
- topical relevance to configured interests
- freshness

## Practical Heuristics

- Prefer topics that are both timely and specific
- Prefer topics with a clear downstream writing angle
- Down-rank vague hype without concrete product, company, or user behavior details
- Ingest to ViralKB only when the score crosses the package threshold

If scoring is uncertain, return the candidate with an explanation instead of pretending the ranking is precise.
