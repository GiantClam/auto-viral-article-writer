---
name: setup
description: This skill should be used when the user asks to "setup", "configure", "配置", "设置", "初始化", "set this up", or when first installing the skill package. It configures user preferences, checks dependencies, verifies opencli connectivity, and confirms the package is ready to use.
version: 1.0.0
---

# Setup

Use this skill for first-time package setup and later preference updates.

## Use This For

- first install of the package
- updating `hot_topics` preferences
- checking whether `opencli` is connected
- verifying the package can run end-to-end

## Do Not Use This For

- daily topic collection after setup is already complete
- article drafting
- image generation requests

## Inputs

- preferred hot topic directions
- preferred platforms
- optional request to re-run verification

## Outputs

- updated `config/user_preferences.json`
- confirmation of dependency and connectivity state
- clear next-step guidance

## Workflow

1. Check whether `config/user_preferences.json` already exists.
2. Ask the user to confirm or update preferred hot topics.
3. Save the preferences file if needed.
4. Verify `opencli` using `python tools/opencli_fetcher.py --check` or `opencli doctor`.
5. Verify config with `python tools/config_loader.py`.
6. Summarize readiness and recommend the next skill.

## Default Preference Shape

```json
{
  "hot_topics": ["AI工具", "SaaS", "AI出海"],
  "default_platforms": ["xiaohongshu", "zhihu", "bilibili", "twitter"],
  "output_dir": "output"
}
```

## Fallback Guidance

- If `user_preferences.json` is missing, create it.
- If `opencli` is unavailable, continue with RSS-capable flows and explain which social sources are unavailable.
- If image provider keys are missing, explain that writing and pattern lookup can still proceed, but image-producing skills will fail.
