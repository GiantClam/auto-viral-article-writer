#!/usr/bin/env python3
"""
Viral Knowledge Base - JSONL storage + BGE-M3 embeddings + semantic search.
Stores viral article patterns, retrieves relevant patterns during generation.
"""

import json
import os
import sys
import time
import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict

sys.path.insert(0, str(Path(__file__).parent))

from config_loader import load_config

try:
    import numpy as np
except ImportError:
    print("Error: numpy not installed. Run: pip install numpy")
    sys.exit(1)


class ViralKB:
    """Viral content knowledge base with semantic retrieval."""

    DEFAULT_DIR = Path(__file__).parent.parent / "data" / "viral_kb"

    def __init__(
        self, kb_dir: str = None, model_name: str = None, verbose: bool = False
    ):
        self.verbose = verbose
        self.kb_dir = Path(kb_dir) if kb_dir else self.DEFAULT_DIR
        self.kb_dir.mkdir(parents=True, exist_ok=True)

        self.patterns_file = self.kb_dir / "patterns.jsonl"
        self.index_file = self.kb_dir / "embeddings.npy"
        self.meta_file = self.kb_dir / "meta.json"

        self.patterns: List[Dict] = []
        self.embeddings: Optional[np.ndarray] = None
        self.encoder = None

        self._load_patterns()
        self._load_or_build_index(model_name)

    def _load_patterns(self):
        if not self.patterns_file.exists():
            return
        with open(self.patterns_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        self.patterns.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        if self.verbose:
            print(f"Loaded {len(self.patterns)} patterns from {self.patterns_file}")

    def _load_or_build_index(self, model_name: str = None):
        if model_name is None:
            config = load_config()
            model_name = config.get("embedding_model", "BAAI/bge-small-zh-v1.5")

        self._init_encoder(model_name)

        if self.index_file.exists() and self.embeddings is not None:
            try:
                self.embeddings = np.load(self.index_file)
                if self.verbose:
                    print(f"Loaded index: {self.embeddings.shape}")
                return
            except Exception:
                pass

        if self.patterns:
            self._build_index()

    def _init_encoder(self, model_name: str):
        try:
            from sentence_transformers import SentenceTransformer

            self.encoder = SentenceTransformer(model_name)
            if self.verbose:
                print(f"Encoder loaded: {model_name}")
        except ImportError:
            if self.verbose:
                print("sentence-transformers not installed, using fallback encoder")
            self.encoder = None

    def _build_index(self):
        if not self.encoder or not self.patterns:
            return

        texts = [self._pattern_to_search_text(p) for p in self.patterns]
        raw_embeddings = self.encoder.encode(texts, show_progress_bar=False)

        norms = np.linalg.norm(raw_embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)
        self.embeddings = raw_embeddings / norms

        np.save(self.index_file, self.embeddings)
        if self.verbose:
            print(f"Built index: {self.embeddings.shape}")

    def _pattern_to_search_text(self, pattern: Dict) -> str:
        parts = []
        ve = pattern.get("viral_elements", {})
        parts.append(ve.get("title_formula", ""))
        parts.append(ve.get("structure", ""))
        parts.append(" ".join(ve.get("emotional_triggers", [])))
        parts.append(ve.get("opening_hook", ""))
        parts.append(pattern.get("title", ""))
        parts.append(" ".join(pattern.get("topic_tags", [])))
        return " ".join(p for p in parts if p)

    def add(self, pattern: Dict):
        if "id" not in pattern:
            pattern["id"] = self._gen_id(pattern)
        if "created_at" not in pattern:
            pattern["created_at"] = datetime.now(timezone.utc).isoformat()
        if "first_seen" not in pattern:
            pattern["first_seen"] = pattern["created_at"][:10]
        if "viral_cycle_count" not in pattern:
            pattern["viral_cycle_count"] = 1

        self.patterns.append(pattern)

        with open(self.patterns_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(pattern, ensure_ascii=False) + "\n")

        if self.encoder:
            text = self._pattern_to_search_text(pattern)
            vec = self.encoder.encode([text])
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            if self.embeddings is None:
                self.embeddings = vec
            else:
                self.embeddings = np.vstack([self.embeddings, vec])
            np.save(self.index_file, self.embeddings)

        if self.verbose:
            print(f"Added pattern: {pattern.get('title', '')[:40]}")

    def retrieve(
        self,
        query: str,
        platform: str = None,
        topic_tags: List[str] = None,
        top_k: int = 5,
        min_score: float = 0.0,
    ) -> List[Dict]:
        if not self.patterns or self.embeddings is None:
            return []

        if not self.encoder:
            return self._retrieve_keyword(query, platform, topic_tags, top_k)

        query_vec = self.encoder.encode([query])
        norm = np.linalg.norm(query_vec)
        if norm > 0:
            query_vec = query_vec / norm

        scores = np.dot(self.embeddings, query_vec.T).flatten()

        candidates = []
        for i, score in enumerate(scores):
            pattern = self.patterns[i]
            if platform and pattern.get("platform") != platform:
                continue
            if topic_tags:
                p_tags = set(t.lower() for t in pattern.get("topic_tags", []))
                if not any(t.lower() in p_tags for t in topic_tags):
                    continue
            if score < min_score:
                continue
            candidates.append({"score": float(score), "pattern": pattern})

        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates[:top_k]

    def _retrieve_keyword(
        self,
        query: str,
        platform: str = None,
        topic_tags: List[str] = None,
        top_k: int = 5,
    ) -> List[Dict]:
        query_lower = query.lower()
        candidates = []
        for pattern in self.patterns:
            if platform and pattern.get("platform") != platform:
                continue
            if topic_tags:
                p_tags = set(t.lower() for t in pattern.get("topic_tags", []))
                if not any(t.lower() in p_tags for t in topic_tags):
                    continue
            text = self._pattern_to_search_text(pattern).lower()
            score = sum(1 for w in query_lower.split() if w in text) / max(
                len(query_lower.split()), 1
            )
            candidates.append({"score": score, "pattern": pattern})
        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates[:top_k]

    def update_cycle(self, pattern_id: str):
        for p in self.patterns:
            if p.get("id") == pattern_id:
                p["last_seen"] = datetime.now(timezone.utc).isoformat()[:10]
                p["viral_cycle_count"] = p.get("viral_cycle_count", 1) + 1

                with open(self.patterns_file, "w", encoding="utf-8") as f:
                    for pat in self.patterns:
                        f.write(json.dumps(pat, ensure_ascii=False) + "\n")
                return True
        return False

    def get_cycle_info(self, topic: str) -> Dict:
        topic_lower = topic.lower()
        events = []
        for p in self.patterns:
            tags = [t.lower() for t in p.get("topic_tags", [])]
            if topic_lower in tags or topic_lower in p.get("title", "").lower():
                events.append(
                    {
                        "date": p.get("first_seen", ""),
                        "title": p.get("title", ""),
                        "id": p.get("id", ""),
                    }
                )
        events.sort(key=lambda x: x["date"])
        if len(events) >= 2:
            dates = [datetime.fromisoformat(e["date"]) for e in events if e["date"]]
            if len(dates) >= 2:
                gaps = [(dates[i + 1] - dates[i]).days for i in range(len(dates) - 1)]
                avg_cycle = sum(gaps) / len(gaps)
                last_date = max(dates)
                next_pred = last_date + __import__("datetime").timedelta(days=avg_cycle)
                return {
                    "topic": topic,
                    "viral_events": events,
                    "cycle_months": round(avg_cycle / 30, 1),
                    "next_predicted": next_pred.strftime("%Y-%m"),
                }
        return {"topic": topic, "viral_events": events, "cycle_months": None}

    def stats(self) -> Dict:
        platforms = {}
        topics = {}
        for p in self.patterns:
            plat = p.get("platform", "unknown")
            platforms[plat] = platforms.get(plat, 0) + 1
            for tag in p.get("topic_tags", []):
                topics[tag] = topics.get(tag, 0) + 1
        return {
            "total_patterns": len(self.patterns),
            "by_platform": platforms,
            "top_topics": sorted(topics.items(), key=lambda x: x[1], reverse=True)[:10],
        }

    def _gen_id(self, pattern: Dict) -> str:
        title = pattern.get("title", "")
        url = pattern.get("source_url", "")
        raw = f"{title}{url}{time.time()}"
        return f"viral_{datetime.now().strftime('%Y%m%d')}_{hashlib.md5(raw.encode()).hexdigest()[:6]}"

    def format_for_prompt(self, results: List[Dict], max_items: int = 3) -> str:
        if not results:
            return "（暂无相关爆款模式参考）"

        parts = []
        for i, item in enumerate(results[:max_items]):
            p = item["pattern"]
            ve = p.get("viral_elements", {})
            score = item.get("score", 0)

            part = f"""<pattern id="{p.get("id", "")}" relevance="{score:.2f}">
<platform>{p.get("platform", "")}</platform>
<title>{p.get("title", "")}</title>
<title_formula>{ve.get("title_formula", "")}</title_formula>
<structure>{ve.get("structure", "")}</structure>
<emotional_triggers>{", ".join(ve.get("emotional_triggers", []))}</emotional_triggers>
<opening_hook>{ve.get("opening_hook", "")}</opening_hook>
<cta_pattern>{ve.get("cta_pattern", "")}</cta_pattern>
<topic_tags>{", ".join(p.get("topic_tags", []))}</topic_tags>
<viral_cycle>{p.get("viral_cycle_count", 1)}次复热</viral_cycle>
</pattern>"""
            parts.append(part)

        return "\n\n".join(parts)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Viral Knowledge Base")
    parser.add_argument("command", choices=["stats", "search", "add", "cycle"])
    parser.add_argument("--query", "-q", help="Search query")
    parser.add_argument("--platform", "-p", help="Filter by platform")
    parser.add_argument("--topic", "-t", help="Topic tag filter")
    parser.add_argument("--top-k", "-k", type=int, default=5)
    parser.add_argument("--kb-dir", help="Knowledge base directory")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    kb = ViralKB(kb_dir=args.kb_dir, verbose=args.verbose)

    if args.command == "stats":
        s = kb.stats()
        print(json.dumps(s, ensure_ascii=False, indent=2))

    elif args.command == "search":
        if not args.query:
            print("Error: --query required")
            return
        topic_tags = [args.topic] if args.topic else None
        results = kb.retrieve(args.query, args.platform, topic_tags, args.top_k)
        for item in results:
            p = item["pattern"]
            print(
                f"[{item['score']:.3f}] {p.get('title', '')} ({p.get('platform', '')})"
            )
            print(f"  Tags: {', '.join(p.get('topic_tags', []))}")
            ve = p.get("viral_elements", {})
            print(f"  Formula: {ve.get('title_formula', '')}")
            print()

    elif args.command == "cycle":
        if not args.topic:
            print("Error: --topic required")
            return
        info = kb.get_cycle_info(args.topic)
        print(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
