<div align="center">

**中文** · [English](./README.en.md)

# Auto Viral Article Writer

为 Agent 提供的内容生产 auto viral article writer：热点采集 -> 爆款模式 -> 文章起草 -> 正文插图 -> 封面生成。

![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)
![Skills](https://img.shields.io/badge/Skills-12-10B981?style=for-the-badge)
![Platforms](https://img.shields.io/badge/Platforms-5-F59E0B?style=for-the-badge)

**支持平台：** OpenCode、Codex、Claude Code、OpenClaw、Hermes

</div>

---

## 这是什么

这是一个面向内容工作流的 Auto Viral Article Writer。它不是单一工具，也不是纯 prompt 集合，而是一套可以被 Agent 直接加载和复用的技能包。

它要解决的是这件事：

- 先找到值得写的话题
- 再复用高信号的爆款结构
- 然后产出可继续加工的文章草稿
- 最后补齐插图和封面

如果你想让 Agent 按稳定流程做内容，而不是每次从零开始，这个包就是为这个场景设计的。

## 适合谁

- 写公众号长文的人
- 做 AI / SaaS / 内容研究的人
- 想把选题、结构、成稿、配图串成一个流程的人
- 想把内容生产沉淀成可安装 skill 的团队

## 不适合谁

- 只想要一个独立画图工具的人
- 不需要热点研究、只想随便写点博客的人
- 不接受本地 `output/`、`config/`、`data/viralkb/` 文件结构的人
- 想要云端托管产品而不是本地 skill 包的人

---

## Skills

| Skill | 一句话说明 | 触发示例 |
|---|---|---|
| `setup` | 首次配置、依赖检查、连接验证 | `setup`, `配置`, `设置` |
| `hot-topics` | 多源抓取今日热点 | `今日热榜`, `AI热榜`, `热门话题` |
| `research-brief` | 把可写的话题整理成更强的结构化 brief | `先研究一下`, `帮我先梳理这个题`, `research brief` |
| `viral-patterns` | 从 ViralKB 里取爆款标题和结构模式 | `爆款模式`, `找标题公式`, `参考爆款` |
| `viral-mining` | 从外部发现高信号内容并入库 ViralKB | `挖掘爆款`, `发现爆款`, `viral mining` |
| `write-article` | 从研究到草稿的完整写作流程 | `写文章`, `生成文章`, `公众号文章` |
| `article-audit` | 审计单篇文章的 brief、draft、cover 和 inline images 是否齐全 | `检查这篇文章是否齐全`, `审计这篇文章`, `article audit` |
| `article-illustrate` | 给现有文章自动插图 | `生成插图`, `文章配图` |
| `cover-image` | 生成文章封面图 | `生成封面`, `文章封面` |
| `image-generation` | 独立图片生成 | `生成图片`, `create image`, `draw` |
| `baoyu-imagine` | `image-generation` 的兼容别名 | `baoyu-imagine` |
| `package-neat` | 同步 skill 包文档、索引、清单和发布元数据 | `整理一下`, `同步文档`, `release audit` |

完整技能总览见 `skills/index.md`。

单 skill 展示页见 `docs/skills/README.md`。

---

## 典型流程

```text
setup
  -> hot-topics
  -> research-brief
  -> viral-patterns
  -> write-article
       -> article-illustrate
  -> cover-image
```

典型产物：

- 按平台归类的热点清单
- 区分“讨论热度”和“行业重要性”的热点排序
- `output/briefs/` 下的结构化 article brief
- 本地 ViralKB 模式结果
- `output/wechat/{slug}-article.md` 形式的文章草稿
- `output/images/wechat/{slug}-01.png` 这类 inline images
- `output/images/wechat/{slug}-cover-final.png` 形式的封面图
- 可审计的 article artifact family 状态

---

## 安装方式

### 依赖安装

```bash
pip install python-dotenv requests feedparser numpy
```

### 配置 API Key

```bash
cp config/.env.example config/.env
```

至少填一个图片生成 provider：

```bash
OPENAI_COMPATIBLE_API_KEY=your_key_here
OPENAI_COMPATIBLE_BASE_URL=https://your-openai-compatible-base-url
# OR
OPENAI_API_KEY=your_openai_key_here
# OR
GOOGLE_AI_API_KEY=your_google_key_here

JINA_API_KEY=your_jina_key_here
```

### 创建输出目录

```bash
mkdir -p output/briefs output/wechat output/images/wechat data/viralkb
```

### 首次运行 setup

可以直接对 Agent 说 `配置`、`设置`、`setup`，也可以手动执行：

```bash
python scripts/setup.py
```

### 验证配置

```bash
python tools/config_loader.py
python tools/opencli_fetcher.py --check
```

---

## 平台安装

平台化安装说明见：`docs/install/README.md`

包括：

- OpenCode
- Claude Code
- Codex
- OpenClaw
- Hermes

---

## 仓库结构

```text
skill-packaging/
├── README.md
├── README.en.md
├── MANIFEST.txt
├── docs/
│   ├── install/
│   └── overview/
├── skills/
│   ├── index.md
│   ├── setup/
│   ├── hot-topics/
│   ├── viral-patterns/
│   ├── viral-mining/
│   ├── write-article/
│   ├── article-illustrate/
│   ├── cover-image/
│   ├── image-generation/
│   └── baoyu-imagine/
├── tools/
├── config/
├── scripts/
├── templates/
└── data/
```

---

## 进一步阅读

- 技能总览：`skills/index.md`
- 技能展示页：`docs/skills/README.md`
- 仓库总览：`docs/overview/skill-package-overview.md`
- 文章产物族规范：`docs/overview/article-artifact-family.md`
- slug 命名规则：`docs/overview/slug-rules.md`
- 端到端工作流示例：`docs/examples/article-workflow-example.md`
- 快速试跑 smoke test：`docs/examples/smoke-test.md`
- 仓库一致性检查：`python tools/repo_consistency.py`
- 版本变更记录：`CHANGELOG.md`
- 发布流程：`docs/release/release-process.md`
- 平台安装说明：`docs/install/README.md`
- Article brief 模板：`templates/article-brief.yaml`
- Article brief 示例：`templates/article-brief.example.yaml`

---

## 故障排查

### 没有 API key

检查 `config/.env` 是否至少配置了一个图片 provider。

### `viral-patterns` 没有结果

先运行 `viral-mining`，或者先让 `hot-topics` 自动入库一批数据。

### `article_illustrate.py` 没插入图片

确认文章在 `---` 后包含 `**加粗章节标题**`。

### `opencli` 无结果

确认：

- Chrome 正在运行
- 目标站点已登录
- OpenCLI Browser Bridge 扩展已启用
- `python tools/opencli_fetcher.py --check` 能通过

补充说明：

- `tools/opencli_fetcher.py` 现在会在 Linux 和 macOS 上直接解析 `opencli`
- 在 Windows 上会优先解析 `opencli.cmd` / `opencli.exe` / `opencli.bat`
- 如果只有 `opencli.ps1`，会自动通过 PowerShell 调用，避免 Python 子进程找不到命令
- Windows 控制台若不支持部分 Unicode 字符，脚本会回退到安全输出而不是直接崩溃

### 封面图缺少参考图

`cover-image` 默认期望用户提供 `--ref` 肖像或参考图路径。

---

## Agent 使用方式

1. 先运行 `setup`
2. 查看 `skills/index.md`
3. 用自然语言触发对应 skill
4. 按 `SKILL.md` 和 `references/` 执行
5. 需要确定性执行时调用 `tools/` 里的 Python 工具
