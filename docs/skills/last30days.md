# last30days

深度研究 skill：在 Reddit、X、YouTube、Hacker News、Polymarket、GitHub 等平台检索任意话题，AI 合并总结为一份结构化简报。

## 触发词

`last30days`, `/last30days`, `深度研究`, `research topic`, `过去30天`, `全面调研`

## 核心能力

**12+ 信源并行搜索：**
- Reddit（免费公开 JSON，含评论和 upvotes）
- X / Twitter（含创始人/专家 timeline）
- YouTube（全文字幕检索）
- TikTok + Instagram + Threads（需 ScrapeCreators key）
- Hacker News（points + comments）
- Polymarket（真金白银赔率，非讨论热度）
- GitHub（repo stars / PR velocity / releases）
- Digg（AI 1000 高信号账号精选）
- Bluesky / Perplexity Sonar / Web

**智能预研（Pre-research brain）：**
搜索前先解析实体关联——人 ↔ 公司 ↔ 产品 ↔ 创始人 → 再执行精确搜索。

**交叉来源合并：**
同一事件在多平台出现 = 一个 cluster，不重复展示。

**双判决评分：**
- 相关性评分
- 幽默/洞察力评分 → "Best Takes" 精选

## 与 hot-topics 的区别

| | hot-topics | last30days |
|---|---|---|
| 用途 | 日常发现 | 深度研究 |
| 时效 | 今日 | 过去30天 |
| 深度 | 宽而浅 | 深而窄 |
| 输出 | 热榜罗列 | 结构化简报 |
| 比较 | 单话题 | 支持多实体对比 |

## 适用场景

- `/last30days DeepSeek` — DeepSeek 过去30天的完整舆情图谱
- `/last30days Claude Code vs Cursor` — 两者深度对比
- `/last30days Peter Steinberger` — 某个人物的最近动态（GitHub PRs + X posts + Reddit 讨论）

## 输出格式

```
🌐 last30days v3.3.0 · synced 2026-05-10

What I learned:
[合成段落，基于真实数据]

KEY PATTERNS from the research:
1. [pattern with citations]
2. [...]

✅ All agents reported back!
[信源覆盖树状图]
```

## 安装需求

- Python 3.12+
- Reddit / HN / Polymarket / GitHub：免费，立即可用
- X/Twitter：免费（需登录状态）
- YouTube：`yt-dlp`
- TikTok/Instagram/Threads：`SCRAPECREATORS_API_KEY`
- Polymarket 无需 key

## 官方文档

- SKILL.md：`skills/last30days/skills/last30days/SKILL.md`
- 完整说明：https://github.com/mvanhorn/last30days-skill