#!/usr/bin/env python3
"""
Example Workflow — NanoBanana Skills Pipeline
Demonstrates the full article writing pipeline:
1. Hot topics research
2. Viral pattern lookup
3. Article drafting
4. Cover image generation

Usage:
    python scripts/example_workflow.py
"""

import os
import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from config_loader import load_config


def example_hot_topics():
    """Example: Collect AI trending topics"""
    import requests

    SOURCES = {
        'HN': 'https://news.ycombinator.com/rss',
        'Reddit-ML': 'https://www.reddit.com/r/MachineLearning/.rss',
    }

    print("\n=== Step 1: Hot Topics Research ===")
    for name, url in SOURCES.items():
        try:
            resp = requests.get(url, timeout=15)
            print(f"[{name}] Status: {resp.status_code}, Size: {len(resp.content)} bytes")
        except Exception as e:
            print(f"[{name}] Error: {e}")


def example_viral_patterns():
    """Example: Search ViralKB for patterns"""
    import json

    patterns_file = Path(__file__).parent.parent / "data" / "viralkb" / "patterns.jsonl"
    if not patterns_file.exists():
        print("\n=== Step 2: Viral Patterns ===")
        print("ViralKB not found (data/viralkb/patterns.jsonl)")
        return

    print("\n=== Step 2: Viral Pattern Lookup ===")
    keyword = "AI"
    matches = []
    with open(patterns_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                p = json.loads(line)
                if keyword.lower() in p.get('keyword', '').lower():
                    matches.append(p)
            except:
                pass

    print(f"Found {len(matches)} patterns for '{keyword}'")
    for m in matches[:3]:
        print(f"  - {m.get('title', 'N/A')}")


def example_image_generation():
    """Example: Generate image with nanobanana_client"""
    print("\n=== Step 3: Image Generation ===")
    print("Note: Requires API key in config/.env")
    print("Command: python tools/nanobanana_client.py --prompt 'a warm portrait' --output output.png")


def example_article_illustrate():
    """Example: Auto-illustrate article"""
    print("\n=== Step 4: Article Illustration ===")
    print("Command: python tools/article_illustrate.py output/wechat/article.md")


def main():
    print("NanoBanana Skills — Example Workflow")
    print("=" * 50)

    config = load_config()
    has_key = config.get('google_ai_api_key') or config.get('aiberm_api_key')
    print(f"API key configured: {'Yes' if has_key else 'No (run: cp config/.env.example config/.env)'}")

    example_hot_topics()
    example_viral_patterns()
    example_image_generation()
    example_article_illustrate()

    print("\n" + "=" * 50)
    print("Workflow complete. See README.md for detailed usage.")


if __name__ == "__main__":
    main()