---
name: setup
description: This skill should be used when the user asks to "setup", "configure", "配置", "设置", or when first installing the skill-package. It guides users through initial configuration including setting hot topic preferences, verifying opencli connection, and testing all skills.
version: 1.0.0
metadata:
  platforms: [opencode, codex, claudecode]
---

# Skill Package Setup

First-time setup and configuration for the content creation skill package.

## Workflow

### Step 1 — Check Configuration File

Read `config/user_preferences.json` to determine if user has already configured preferences:

```python
import json
from pathlib import Path

config_path = Path('config/user_preferences.json')
if config_path.exists():
    with open(config_path, 'r', encoding='utf-8') as f:
        preferences = json.load(f)
    print(f"Current preferences: {preferences}")
else:
    print("No preferences found. Please configure your hot topic directions.")
```

### Step 2 — Prompt User for Hot Topic Directions

If no preferences exist or user wants to update, ask:

```
Welcome to the Content Creation Skill Package! 🎯

To personalize your experience, please select your preferred hot topic directions (choose 3-5):

1. AI / AI工具 / SaaS - AI tools, productivity software, AI startups
2. 科技 / Tech - Technology trends, gadgets, software
3. 编程 / Programming - Coding, developer tools, frameworks
4. 商业 / Business - Startups, entrepreneurship, marketing
5. AI出海 / Global Expansion - Chinese AI products going global
6. 效率工具 / Productivity - Tools that improve efficiency
7. AI创业 / AI Startups - Building AI companies
8. 全选 / All - Follow all topics

Enter numbers (e.g., "1,3,5"): _
```

### Step 3 — Save Configuration

```python
import json
from pathlib import Path

config_dir = Path('config')
config_dir.mkdir(exist_ok=True)

preferences = {
    "hot_topics": ["AI工具", "SaaS", "AI出海"],
    "default_platforms": ["xiaohongshu", "zhihu", "bilibili", "twitter"],
    "output_dir": "output",
    "created_at": datetime.now().isoformat()
}

config_path = config_dir / 'user_preferences.json'
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(preferences, f, ensure_ascii=False, indent=2)

print(f"Configuration saved to {config_path}")
```

### Step 4 — Verify opencli Connection

```bash
# Check if opencli is installed and connected
opencli doctor

# Expected output:
# [OK] Daemon: running
# [OK] Extension: connected
# [OK] Connectivity: connected
```

If connection fails, display troubleshooting steps:
```
⚠️ opencli connection issue detected. Please ensure:
1. Chrome browser is running with target site logged in
2. OpenCLI Browser Bridge extension is installed and enabled
3. Run 'opencli doctor' to verify connection
```

### Step 5 — Test All Skills

Test each skill's core functionality:

#### Test hot-topics
```bash
python tools/opencli_fetcher.py --platform xiaohongshu --limit 3
```

#### Test viral-patterns
```python
from pathlib import Path
kb_dir = Path('data/viralkb')
if not kb_dir.exists():
    print("ViralKB not initialized. Run viral-mining skill first to populate.")
else:
    print("ViralKB found at data/viralkb/")
```

#### Test image-generation
```bash
python tools/nanobanana_client.py --openai-compatible-image \
  --prompt "test image" \
  --output "output/images/test.png"
```

### Step 6 — Summary

Display setup summary:

```
✅ Setup Complete!

Your Configuration:
- Hot Topics: AI工具, SaaS, AI出海
- Platforms: 小红书, 知乎, B站, Twitter
- Output: output/

Available Skills:
- hot-topics: 今日热榜, AI热榜, 热门话题...
- viral-patterns: 爆款模式, 查找爆款...
- viral-mining: 挖掘爆款, 发现爆款...
- write-article: 写文章, 生成文章...
- cover-image: 生成封面, create cover...
- article-illustrate: 生成插图, 文章配图...
- image-generation: 生成图片, AI画图...

Ready to create content! 🚀
```
