# Multi-Platform Content Demo Runbook

This runbook shows how to run one complete content experiment through the writer system.

It is designed for the current skill stack:

- `write-article`
- `cover-image`
- `repurpose-content`
- `article-score-retro`
- `platform-rubric-manager`

## Goal

Take one topic and turn it into:

1. one WeChat mother draft
2. several platform-native variants
3. pre-publish score and prediction files
4. post-publish retro files

## Recommended First Demo Platforms

Run the first demo on:

- WeChat
- X
- Xiaohongshu

These three give the clearest contrast in format and platform logic.

## Step 1 - Choose One Real Topic

Pick one topic that is already worth publishing.

Good demo topics:

- a new model release
- a product workflow you tested
- a clear engineering lesson
- a tool comparison with practical conclusions

Avoid a vague topic for the first run.

## Step 2 - Create the Mother Draft

Use `write-article` to create the WeChat source article.

Output target:

```text
output/wechat/{slug}-article.md
```

The mother draft should be the most complete version of the idea.

## Step 3 - Create the Cover

Use `cover-image` after the mother draft is complete.

Output target:

```text
output/images/wechat/{slug}-cover.png
```

## Step 4 - Create the Content Ledger Folder

Create one shared folder for this topic:

```text
output/content/{slug}/
```

Recommended contents after setup:

```text
output/content/{slug}/
  source.md
  wechat.md
  x.md
  xiaohongshu.md
  score-wechat.json
  score-x.json
  score-xiaohongshu.json
  predict-wechat.json
  predict-x.json
  predict-xiaohongshu.json
  retro-wechat-t3.json
  retro-x-t3.json
  retro-xiaohongshu-t3.json
```

Copy or save the WeChat mother draft into:

```text
output/content/{slug}/source.md
output/content/{slug}/wechat.md
```

## Step 5 - Repurpose for Each Platform

Use `repurpose-content` to create:

- `x.md`
- `xiaohongshu.md`

Principle:

- keep the same core idea
- change the packaging for the platform
- do not copy the WeChat draft verbatim

## Step 6 - Score Before Publish

Use `article-score-retro` in `score` mode for each platform draft.

Use these matching rubric files:

- WeChat: `rubrics/wechat.yaml`
- X: `rubrics/x.yaml`
- Xiaohongshu: `rubrics/xiaohongshu.yaml`

Save files to:

- `score-wechat.json`
- `score-x.json`
- `score-xiaohongshu.json`

Do not publish before score files exist.

## Step 7 - Predict Before Publish

Use `article-score-retro` in `predict` mode for each platform draft.

Save files to:

- `predict-wechat.json`
- `predict-x.json`
- `predict-xiaohongshu.json`

Rules:

- prediction must be written before results are known
- prediction files should not be edited after publish

## Step 8 - Publish

Publish the content to the selected platforms.

At minimum, record:

- publish date
- platform
- post URL

You may store these in your own notes or inside each retro file later.

## Step 9 - Run T+3 Retro

After three days, collect the real signals.

Examples:

- WeChat: reads, shares, saves, comments, follows, inquiries
- X: impressions, likes, reposts, replies, bookmarks
- Xiaohongshu: reads, likes, saves, comments, follows

Use `article-score-retro` in `retro` mode and save:

- `retro-wechat-t3.json`
- `retro-x-t3.json`
- `retro-xiaohongshu-t3.json`

Each retro must reference its original prediction file.

## Step 10 - Update Rubric Only If Signals Repeat

Do not change a rubric because of one random result.

Only use `platform-rubric-manager` if:

- the same weakness repeats
- the same strength repeats
- an existing dimension stops explaining outcomes

Example:

- weak WeChat read-through on multiple posts -> review `opening_grab`
- strong X impressions but weak reposts on multiple posts -> review `repost_potential`
- strong Xiaohongshu clicks but weak saves on multiple posts -> review `saveability`

## What A Good First Demo Looks Like

Success does not mean every post performs well.

Success means:

1. the mother draft exists
2. the platform variants exist
3. the score files exist
4. the prediction files exist before publish
5. the retro files exist after results
6. you can explain what changed across platforms

## Anti-Patterns

Avoid these in the first demo:

- writing one draft and posting it unchanged everywhere
- publishing before prediction is saved
- doing retro from memory instead of from files
- rewriting a rubric after one lucky hit
- choosing too many platforms at once

## Recommended First Iteration Scope

For your first full run:

- 1 mother draft
- 2 repurposed variants
- 3 score files
- 3 prediction files
- 3 retro files

That is enough to validate the system.
