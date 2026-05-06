#!/usr/bin/env python3
"""
On-site viral scoring and ingestion from hot-topics result files.
Filters hot-topic results by engagement/score threshold, extracts viral patterns,
and ingests qualifying items into ViralKB — without re-running full multi-platform
viral-mining searches.
"""

import json
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List

EMOTIONAL_WORDS = [
    "震惊", "炸裂", "暴涨", "崩盘", "爆款", "秘密", "揭秘", "真相",
    "免费", "限时", "错过", "独家", "必看", "绝了", "神器", "恐怖",
    "疯了", "完蛋", "颠覆", "革命", "终极", "史上", "永远", "never",
    "best", "worst", "shocking", "secret", "ultimate", "killer",
    "mind-blowing", "game-changing", "insane", "crazy", "amazing",
    "you won't believe", "hack", "trick", "must-see",
]


def _extract_title_formula(title: str) -> str:
    title = title.strip()

    if re.search(r"\d+", title):
        if re.search(r"(个|招|种|条|步|款|件)($|\s|，)", title):
            return "数字清单: 数字 + 量词 + 价值承诺"
        if re.search(r"[¥$€]?\d+[万亿千百]?(元|美元|美金|美金|亿|万|倍|%)", title):
            return "数字冲击: 数据 + 结论"
        return f"数字型: 数字 + 信息点"

    if re.search(r"^(how|How)\s+(to|To|I|we|you)\b", title):
        return "How-to教程: How + 目标 + 方法"
    if re.search(r"^(为什么|为啥|Why)\b", title):
        return "原因分析: 为什么 + 现象 + 解答"
    if re.search(r"^(揭秘|解密|拆解|深度|内部|独家)", title):
        return "揭秘型: 揭秘/拆解 + 内幕/方法"
    if re.search(r"[？?]$", title):
        return "提问式: 疑问句引出好奇心"
    if re.search(r"\bvs\b\.?", title, re.IGNORECASE):
        return "对比型: A vs B + 结论"
    if re.search(r"(暴涨|崩盘|暴跌|炸裂|突破|碾压)", title):
        return "情绪冲击: 强情绪词 + 事件"
    if re.search(r"(排名|排名|推荐|盘点|合集|汇总)", title):
        return "合集型: 排名/盘点 + 清单"

    return "陈述型: 事实 + 观点"


def _extract_emotional_triggers(title: str) -> List[str]:
    found = []
    title_lower = title.lower()
    for word in EMOTIONAL_WORDS:
        if word.lower() in title_lower:
            found.append(word)
    return found[:5]


def _extract_opening_hook(title: str) -> str:
    if "?" in title or "？" in title:
        return title
    return f"{title} —— 你知道吗？"


def _categorize(title: str) -> List[str]:
    tags = []
    title_lower = title.lower()

    category_map = {
        "AI工具": ["工具", "平台", "软件", "tool", "app", "platform", "product"],
        "模型更新": ["模型", "model", "gpt", "llm", "claude", "gemini", "开源", "release"],
        "AI应用": ["落地", "应用", "部署", "案例", "赚钱", "变现", "deploy", "build"],
        "算法突破": ["突破", "算法", "论文", "研究", "research", "paper", "benchmark"],
        "AI出海": ["出海", "全球化", "海外", "global", "international"],
    }

    for tag, keywords in category_map.items():
        if any(kw in title_lower for kw in keywords):
            tags.append(tag)

    return tags or ["AI工具"]


def ingest_hot_topics(
    source_files: List[str],
    kb_dir: str,
    min_score: int = 50,
) -> Dict[str, int]:
    kb_path = Path(kb_dir)
    kb_path.mkdir(parents=True, exist_ok=True)
    patterns_file = kb_path / "patterns.jsonl"

    known_urls: set[str] = set()
    if patterns_file.exists():
        for line in patterns_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                url = record.get("url") or record.get("source_url", "")
                if url:
                    known_urls.add(url)
            except json.JSONDecodeError:
                pass

    total = 0
    ingested = 0
    skipped_low_score = 0
    skipped_duplicates = 0

    for file_path in source_files:
        raw = Path(file_path).read_text(encoding="utf-8")
        try:
            items = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(items, list):
            items = [items]

        for item in items:
            total += 1
            score = item.get("score", 0)
            if score < min_score:
                skipped_low_score += 1
                continue

            url = item.get("url", "")
            if url and url in known_urls:
                skipped_duplicates += 1
                continue

            title = item.get("title", "Untitled")
            pattern = {
                "title": title,
                "source_url": url,
                "url": url,
                "platform": item.get("source", item.get("platform", "unknown")),
                "topic_tags": _categorize(title),
                "viral_elements": {
                    "title_formula": _extract_title_formula(title),
                    "structure": "痛点 → 数据 → 解决方案 → CTA",
                    "emotional_triggers": _extract_emotional_triggers(title),
                    "opening_hook": _extract_opening_hook(title),
                    "cta_pattern": "引导评论/点赞/转发",
                },
                "engagement": score,
                "viral_cycle_count": 1,
                "first_seen": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "created_at": datetime.now(timezone.utc).isoformat(),
            }

            with open(patterns_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(pattern, ensure_ascii=False) + "\n")

            if url:
                known_urls.add(url)
            ingested += 1

    return {
        "total": total,
        "ingested": ingested,
        "skipped_low_score": skipped_low_score,
        "skipped_duplicates": skipped_duplicates,
    }