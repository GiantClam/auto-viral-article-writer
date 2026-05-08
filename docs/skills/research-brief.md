# research-brief

## Purpose

Turn a promising topic into a stronger structured brief before article drafting.

## Use Cases

- deepening a topic after discovery
- preparing a source-backed article brief
- testing whether a topic is really ready to draft

## Trigger Examples

- `先研究一下`
- `帮我先梳理这个题`
- `research brief`
- `deep brief`

## Inputs

- topic
- hot-topics seed
- optional platform target

## Outputs

- stronger article brief
- angle candidates
- source summary
- risk notes
- optional persisted brief file under `output/briefs/`

## Boundary

This skill stops before full drafting. It prepares the brief that `write-article` should consume.

When the workflow needs a reusable intermediate artifact, save it as `output/briefs/{slug}-brief.yaml`.

That brief should become the first artifact in the article's shared slug family.

The brief is also the best place to establish the slug that later artifacts should inherit.
