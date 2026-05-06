#!/usr/bin/env python3
"""
Setup script for skill-package
Guides users through initial configuration and verifies all dependencies
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def print_banner():
    print("=" * 50)
    print("  Skill Package Setup")
    print("  内容创作技能包配置")
    print("=" * 50)
    print()


def load_current_preferences():
    config_path = Path('config/user_preferences.json')
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def save_preferences(preferences):
    config_dir = Path('config')
    config_dir.mkdir(exist_ok=True)
    config_path = config_dir / 'user_preferences.json'
    preferences['updated_at'] = datetime.now().isoformat()
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(preferences, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 配置已保存到: {config_path}")


def get_hot_topics_input():
    print("\n📌 请选择你感兴趣的热门话题方向 (可多选，选3-5个):")
    print()
    options = [
        ("1", "AI / AI工具站", "AI tools, productivity software, AI startups"),
        ("2", "科技 / Tech", "Technology trends, gadgets, software"),
        ("3", "编程 / Programming", "Coding, developer tools, frameworks"),
        ("4", "商业 / Business", "Startups, entrepreneurship, marketing"),
        ("5", "AI出海 / Global Expansion", "Chinese AI products going global"),
        ("6", "效率工具 / Productivity", "Tools that improve efficiency"),
        ("7", "AI创业 / AI Startups", "Building AI companies"),
        ("8", "全部 / All", "Follow all topics"),
    ]

    for num, name, desc in options:
        print(f"  {num}. {name}")
        print(f"     {desc}")
        print()

    while True:
        choice = input("请输入编号 (如 1,3,5): ").strip()
        if not choice:
            print("请输入编号!")
            continue

        selected = [c.strip() for c in choice.split(',')]
        valid = True
        topics = []

        for s in selected:
            if s == '8':
                topics = ['AI', 'AI工具', 'SaaS', '科技', '编程', '商业', 'AI出海', '效率工具', 'AI创业']
                break
            elif s in ['1', '2', '3', '4', '5', '6', '7']:
                topic_map = {
                    '1': 'AI工具',
                    '2': '科技',
                    '3': '编程',
                    '4': '商业',
                    '5': 'AI出海',
                    '6': '效率工具',
                    '7': 'AI创业',
                }
                topics.append(topic_map[s])
            else:
                print(f"无效编号: {s}")
                valid = False
                break

        if valid and topics:
            return topics[:5] if len(topics) > 5 else topics

        print("请输入有效的编号组合，如 1,3,5")


def get_platforms_input():
    print("\n📌 请选择要抓取的平台 (可多选):")
    print()
    options = [
        ("1", "小红书 / Xiaohongshu", "中国生活方式平台"),
        ("2", "知乎 / Zhihu", "中国问答社区"),
        ("3", "B站 / Bilibili", "中国视频平台"),
        ("4", "Twitter/X", "国际社交媒体"),
    ]

    for num, name, desc in options:
        print(f"  {num}. {name} - {desc}")

    print()
    while True:
        choice = input("请输入编号 (如 1,2,3,4) 或直接回车默认全部: ").strip()

        if not choice:
            return ['xiaohongshu', 'zhihu', 'bilibili', 'twitter']

        selected = [c.strip() for c in choice.split(',')]
        platform_map = {
            '1': 'xiaohongshu',
            '2': 'zhihu',
            '3': 'bilibili',
            '4': 'twitter',
        }

        platforms = []
        valid = True
        for s in selected:
            if s in platform_map:
                platforms.append(platform_map[s])
            else:
                print(f"无效编号: {s}")
                valid = False
                break

        if valid and platforms:
            return platforms


def check_opencli():
    print("\n🔍 检查 opencli 连接...")
    try:
        import subprocess
        result = subprocess.run(
            ['opencli', 'doctor'],
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout + result.stderr

        if '[OK]' in output and 'connected' in output.lower():
            print("✅ opencli 连接正常!")
            return True
        else:
            print("⚠️ opencli 连接有问题:")
            print(output)
            return False
    except FileNotFoundError:
        print("❌ opencli 未安装。请先安装 opencli:")
        print("   npm install -g @jackwener/opencli")
        return False
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False


def test_skills():
    print("\n🧪 测试 Skills...")
    print()

    print("1. 测试 hot-topics (小红书)...")
    try:
        import subprocess
        result = subprocess.run(
            ['opencli', 'xiaohongshu', 'search', 'AI', '--limit', '3', '-f', 'json'],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.stdout and 'rank' in result.stdout:
            print("   ✅ hot-topics 正常")
        else:
            print("   ⚠️ hot-topics 返回格式异常")
    except Exception as e:
        print(f"   ⚠️ hot-topics 测试失败: {e}")

    print("2. 测试 viral-patterns (ViralKB)...")
    kb_dir = Path('data/viralkb')
    if kb_dir.exists():
        patterns_file = kb_dir / 'patterns.jsonl'
        if patterns_file.exists():
            print("   ✅ ViralKB 已初始化")
        else:
            print("   ⚠️ ViralKB 未初始化 (运行 viral-mining skill 来填充)")
    else:
        print("   ⚠️ ViralKB 未初始化 (运行 viral-mining skill 来填充)")

    print("\n3. 测试 image-generation (nanobanana_client)...")
    try:
        result = subprocess.run(
            ['python', 'tools/nanobanana_client.py', '--gemini-image', '--use-curl',
             '--prompt', 'test', '--output', 'output/images/test_setup.png'],
            capture_output=True,
            text=True,
            timeout=120
        )
        if 'Image saved' in result.stdout or result.returncode == 0:
            print("   ✅ image-generation 正常")
        else:
            print("   ⚠️ image-generation 需要配置 API key")
    except Exception as e:
        print(f"   ⚠️ image-generation 测试失败: {e}")


def main():
    print_banner()

    print("🚀 欢迎使用内容创作技能包!")
    print("=" * 50)
    print()

    existing = load_current_preferences()

    if existing and existing.get('hot_topics'):
        print(f"📋 当前配置: {existing.get('hot_topics', [])}")
        choice = input("\n是否要重新配置? (y/N): ").strip().lower()
        if choice != 'y':
            print("\n✅ 使用现有配置")
            return

    hot_topics = get_hot_topics_input()
    platforms = get_platforms_input()

    print(f"\n📝 你选择的话题: {hot_topics}")
    print(f"📝 你选择的平台: {platforms}")

    confirm = input("\n确认保存配置? (Y/n): ").strip().lower()
    if confirm == 'n':
        print("取消配置")
        return

    preferences = {
        "hot_topics": hot_topics,
        "default_platforms": platforms,
        "output_dir": "output",
        "created_at": datetime.now().isoformat(),
        "opencli_configured": False,
        "preferred_language": "zh"
    }

    save_preferences(preferences)

    opencli_ok = check_opencli()
    if opencli_ok:
        preferences['opencli_configured'] = True
        save_preferences(preferences)

    test_skills()

    print()
    print("=" * 50)
    print("✅ 配置完成!")
    print("=" * 50)
    print()
    print("可用 Skills:")
    print("  - hot-topics: 今日热榜, AI热榜, 热门话题...")
    print("  - viral-patterns: 爆款模式, 查找爆款...")
    print("  - viral-mining: 挖掘爆款, 发现爆款...")
    print("  - write-article: 写文章, 生成文章...")
    print("  - cover-image: 生成封面, create cover...")
    print("  - article-illustrate: 生成插图, 文章配图...")
    print("  - image-generation: 生成图片, AI画图...")
    print()
    print("开始创作吧! 🚀")


if __name__ == '__main__':
    main()