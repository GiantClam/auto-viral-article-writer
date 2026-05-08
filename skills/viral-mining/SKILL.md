---
name: viral-mining
description: This skill should be used when the user asks to "挖掘爆款", "发现爆款", "viral mining", "爆款挖掘", or wants to discover and ingest high-signal content into ViralKB. It performs broader multi-source discovery than `viral-patterns` and writes structured results into the local pattern store.
version: 1.0.0
---

# Viral Mining

Use this skill to discover new high-signal content across multiple sources and turn those findings into local ViralKB assets.

## Use This For

- growing ViralKB from fresh external signals
- broad topic mining across platforms
- collecting reusable examples before writing

## Do Not Use This For

- looking up already-stored patterns by keyword only
- writing the final article draft
- generating visuals

## Inputs

- keyword or topic family
- optional source restrictions
- optional limit per source

## Outputs

- ranked multi-source viral content list
- newly written or appended ViralKB entries
- ingestion summary

## Workflow

1. Search multiple sources in parallel.
2. Merge social and RSS results.
3. Score and rank the merged items.
4. Check whether the evidence is strong enough to justify ingestion.
5. Tag the winning items by category.
6. Write structured entries into ViralKB.

## Research Discipline

Use broader coverage than `viral-patterns`, but keep ingestion standards strict:

- prefer original sources over repeated summaries
- do not treat duplicated reposts as multiple proofs
- avoid polluting ViralKB with weak or unverifiable examples

## Evidence Sufficiency

Before writing into ViralKB, check whether the item has enough strength to be reusable later:

- identifiable source or origin
- enough detail to infer a title pattern or structure pattern
- signal quality that is stronger than generic hype alone

## Fallback Guidance

- If social sources are unavailable, continue with RSS and report the reduced coverage.
- If a topic yields weak signals, return the strongest candidate set with caveats instead of pretending the result is robust.

## References

- `references/ingestion-shape.md` - expected ViralKB fields and ingestion behavior
- `references/research-sufficiency.md` - what is strong enough to ingest
