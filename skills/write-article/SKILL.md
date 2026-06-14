---
name: write-article
description: This skill should be used when the user asks to "写文章", "生成文章", "写篇", "公众号文章", "create article", "write a draft", or wants a full article workflow from research to markdown output. It combines topic research, viral pattern lookup, drafting, and illustration-ready structure.
version: 1.0.0
---

# Write Article

Use this skill for the full article production flow, especially when the user wants a structured markdown draft rather than isolated research notes.

## Use This For

- WeChat article drafting
- topic-to-draft workflows
- pattern-assisted article production
- illustration-ready markdown generation

## Do Not Use This For

- one-off hot topic collection with no writing step
- retrieving only title formulas
- direct image-only requests

## Inputs

- topic or source material
- target platform, usually `wechat` or `xiaohongshu`
- optional reference links or notes
- optional article brief assembled from `hot-topics` and `viral-patterns`

## Outputs

- article markdown saved to `output/`
- title candidates
- section structure ready for illustration insertion
- clear handoff to `cover-image` first, then `article-illustrate`
- optional handoff to `repurpose-content` for platform-native rewrites after the mother draft is complete
- a completed or refined article brief when needed for downstream editing
- a stable relationship between the draft and `output/briefs/{slug}-brief.yaml` when brief-first workflow is used
- article drafts should prefer `output/wechat/{slug}-article.md` when a stable family slug is available

## Workflow

1. **Run a topic viability check** before drafting (HKR gate).
2. **Run `hot-topics`** when the topic still needs research or current framing.
3. **Decide if deep research is needed.** If the topic is:
   - A named entity (person, company, product, project)
   - An investigation/experiment archetype
   - Complex enough that hot-topics surface signals are insufficient
   → Run `last30days` for comprehensive 30-day picture before continuing
4. **Run `viral-patterns`** to retrieve structure and title patterns.
5. Collect any needed authoritative source material.
6. Classify the article into a working archetype.
7. Assemble or refine the article brief.
8. Draft a structured outline from the article brief.
9. Expand the outline into the full article.
10. Run the quality checklist before calling it complete.
11. Save to the correct output path.
12. Generate the article cover via `cover-image` using the same slug family and the approved cover title.
13. Hand off to `article-illustrate` when visuals are needed.

## Post-Draft Order

For WeChat article production, keep the generation order fixed:

1. Confirm topic and article angle.
2. Generate the article draft.
3. Generate the cover image.
4. Prompt for illustration generation.

## When to Trigger `last30days`

`last30days` is triggered **inside `write-article`** (not as a separate manual step) when:

| Condition | Why |
|---|---|
| Topic is a named entity (person/company/product) | hot-topics only gives surface trending; last30days gives full 30-day community picture including GitHub activity, X timeline, Reddit deep-dives |
| Article archetype is investigation or experiment | Needs depth beyond what hot-topics surfaces |
| User asks for "深度研究" or "全面调研" | Automatic trigger |
| hot-topics output is thin but topic seems important | last30days may find signals hot-topics missed |

**How it integrates into write-article:**
- Step 3: invoke `last30days` via Bash (Python engine) with entity resolution flags
- last30days output (synthesis + evidence) becomes part of `source_set` in the article brief
- The synthesis paragraphs directly feed the article body
- Citation format from last30days (inline `[name](url)`) preserved in article

**How to invoke last30days inside write-article:**
```bash
SKILL_DIR="D:\OpenCode\writer\.opencode\skills\last30days\skills\last30days"
if [ -f "$SKILL_DIR/scripts/last30days.py" ]; then
  LAST30DAYS_PYTHON=$(for py in python3.14 python3.13 python3.12 python3; do command -v $py 2>/dev/null && $py -c 'import sys; raise SystemExit(0 if sys.version_info>=(3,12) else 1)' 2>/dev/null && echo $py && break; done)
  $LAST30DAYS_PYTHON "$SKILL_DIR/scripts/last30days.py" "{TOPIC}" --emit=compact 2>&1
fi
```

**Output convention:** last30days badge + synthesis becomes `source_set.last30days_synthesis` in the article brief. Cite with `[author/platform]` inline markdown links per LAW 8.

## Article Brief Handoff

Prefer to write from a structured article brief instead of from loose notes alone. The brief should combine:

- topic framing from `hot-topics`
- reusable pattern notes from `viral-patterns`
- source-backed angle and risk notes
- chosen archetype, hook, and section plan

When a reusable intermediate artifact is needed, start from `templates/article-brief.yaml` and fill it before drafting.

If a persistent brief file exists, prefer reading from `output/briefs/{slug}-brief.yaml` rather than re-assembling the brief from scattered notes.

When possible, keep the resulting draft under the same slug family, for example `output/wechat/{slug}-article.md`.

Do not invent a new slug at draft time if the brief already established one.

## Topic Viability Gate

Before writing, evaluate whether the topic has enough article potential using HKR:

- `H` - Happy: is there enough curiosity, novelty, surprise, or story value to make someone want to click?
- `K` - Knowledge: will the piece teach the reader something concrete?
- `R` - Resonance: is there an emotional, social, or identity-level reason the topic will matter?

Use this rule of thumb:

- 3 hits: strong article candidate
- 2 hits: usable topic, proceed with a sharper angle
- 1 hit: likely too weak for a full article, downgrade to notes or a short brief unless the user insists

## Article Archetypes

Choose a working article archetype before drafting. This determines the opening, the evidence shape, and the ending style.

- investigation or experiment
- product experience
- phenomenon analysis
- tool sharing
- methodology or lessons learned

## AI Boundary Rules

AI may help with:

- structuring the brief
- comparing pattern options
- summarizing source material
- drafting title candidates
- expanding validated sections into a coherent article

AI must not invent:

- first-hand experience that did not happen
- fabricated interviews or quotes
- unverified factual claims presented as certain
- fake measurements, user feedback, or experiment results

## Default Output Pattern

```text
# 【Title Candidate】
# 【Title Candidate】
---
**Section Heading**
Body content...
```

## Fallback Guidance

- If live topic research is unavailable, continue from user-provided material and explain the reduced freshness.
- If ViralKB is thin, use the strongest available pattern examples rather than blocking the draft.
- If image generation is unavailable, still produce a complete markdown article.

## References

- `references/article-brief-schema.md` - shared schema between research, pattern lookup, and drafting
- `references/article-archetypes.md` - article type selection and structure guidance
- `references/editorial-boundaries.md` - what AI may and may not invent in article workflows
- `references/platform-output-spec.md` - output expectations by platform
- `references/quality-checklist.md` - article completion checks
- `references/editorial-quality-checklist.md` - four-layer editorial quality review
- `../../docs/overview/article-artifact-family.md` - recommended file family for brief, draft, cover, and inline images
- `../../docs/overview/slug-rules.md` - how to generate and reuse a stable slug
