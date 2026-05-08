# Article Brief Schema

Use this schema as the shared handoff object between `hot-topics`, `viral-patterns`, and `write-article`.

Concrete templates are available at:

- `templates/article-brief.yaml`
- `templates/article-brief.example.yaml`

## Core Fields

- `topic` - the concrete subject being written about
- `angle` - the specific lens that makes the article worth writing
- `audience` - who the article is for
- `platform` - usually `wechat` or another target output channel
- `hkr` - topic viability notes for Happy, Knowledge, Resonance
- `archetype` - chosen article type
- `hook` - the opening promise or tension
- `title_patterns` - candidate title formulas or titles
- `emotional_triggers` - which emotional levers are active
- `source_set` - the source material that supports the article
- `pattern_summary` - the reusable structures drawn from ViralKB
- `section_plan` - the planned sections for the article
- `risk_notes` - weak spots, unsupported areas, or caveats

## Minimal Example

```yaml
topic: Claude Code trend shift
angle: Why the current wave is less about tools and more about workflow standardization
audience: AI practitioners and content readers who follow agent tooling
platform: wechat
hkr:
  happy: strong
  knowledge: strong
  resonance: medium
archetype: phenomenon analysis
hook: Everyone is talking about the tool, but the real change is the workflow it normalizes.
title_patterns:
  - "[Phenomenon] is not really about [surface topic]"
  - "Why [current trend] matters more than it looks"
emotional_triggers:
  - curiosity
  - urgency
source_set:
  - official launch note
  - high-signal user discussion
  - comparison article
pattern_summary:
  title_formulas:
    - contrast formula
  structure:
    - observation -> tension -> explanation -> implication
section_plan:
  - what happened
  - why people are reading it wrong
  - what the deeper shift actually is
risk_notes:
  - avoid overstating the size of the trend without direct metrics
```

## Practical Rule

If the article brief is weak, the article will be weak. Fix the brief before forcing a draft.
