# Ranking Examples

Use these examples to avoid overfitting to raw HN or Reddit comment volume.

## Example 1: Important Product Update vs Loud Discussion Thread

Scenario:

- Topic A: a research or opinion thread is getting more comments on HN or Reddit
- Topic B: a major AI product just gained support for an important workflow surface such as Office, Chrome, IDE integration, or enterprise operations

Preferred handling:

- Treat Topic A as hotter by discussion volume
- Treat Topic B as hotter by industry importance
- In a general "today's hot topics" answer, allow Topic B to rank above Topic A if the capability expansion materially changes what users can do

Reason:

- product-surface expansion often matters more to real users than short-lived community debate

## Example 2: Claude Supports Office

Signal pattern:

- official release note or product announcement exists
- secondary discussion appears on X, community chats, or reposted summaries
- RSS discussion may be modest compared with research arguments or alignment threads

Ranking decision:

- include it as a major topic
- do not omit it just because HN or Reddit engagement is lower than a research discussion thread

Why it matters:

- it expands Claude into mainstream office productivity workflows
- it changes the practical adoption story for knowledge workers and enterprise usage

## Example 3: Codex Supports Chrome

Signal pattern:

- official source or credible product update shows Codex can now operate through Chrome or a browser surface
- community discussion may initially be fragmented across X, product circles, and automation communities

Ranking decision:

- treat it as a major capability update
- rank it above generic opinion posts if the new browser support expands real task coverage

Why it matters:

- browser control moves the product closer to end-to-end workflow execution
- it affects testing, browsing, operations, research, and agent automation use cases

## Example 4: Reduced Coverage Day

Scenario:

- `opencli` sources fail or are partially unavailable
- RSS still returns strong research and discussion topics

Required behavior:

- explicitly say that Chinese social and X coverage is reduced
- avoid presenting the RSS-only ranking as fully representative of the day's overall AI conversation
- manually preserve obviously important product launches if reliable primary sources are known

## Example 5: Reposts Are Not Independent Confirmation

Scenario:

- the same product announcement appears on HN, Reddit, X reposts, and Chinese summaries

Required behavior:

- prefer the original announcement as the anchor source
- count reposts as attention, not as independent confirmation
- describe the topic as strong because of both primary-source credibility and cross-platform pickup
