#!/usr/bin/env python3
"""
Article Illustrator
自动为文章生成配图：分析文章结构 → 识别配图位置 → 生成图像 → 插入Markdown

Usage:
    python tools/article_illustrate.py output/wechat/article.md
    python tools/article_illustrate.py output/wechat/article.md --density balanced --max-images 3
"""

import argparse
import json
import os
import re
import sys
import base64
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from config_loader import load_config


def analyze_article(content: str) -> list[dict]:
    """分析文章结构，找出适合插图的位置"""
    lines = content.split("\n")

    # 文章格式：标题候选 → --- → 正文
    # 找到第一个 --- 作为正文起始标记
    first_divider_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "---":
            first_divider_idx = i
            break

    if first_divider_idx is not None:
        # 正文从 --- 之后开始
        article_lines = lines[first_divider_idx + 1:]
    else:
        article_lines = lines

    article_text = "\n".join(article_lines).strip()

    # 按 ## 章节分割
    sections = []
    parts = re.split(r"(?=^##\s+)", article_text, flags=re.MULTILINE)
    for i, part in enumerate(parts):
        if not part.strip():
            continue
        body = "\n".join(part.split("\n")[1:]).strip()
        # 跳过标题行后面没有正文的部分（这通常是文章标题本身，不是章节）
        if not body:
            continue
        first_line = part.split("\n")[0].strip()
        # 跳过以 # 开头的标题（文章标题，不是章节）
        if first_line.startswith("#"):
            continue
        sections.append({
            "heading": first_line,
            "content": body,
            "idx": i,
        })

    # 也检查 **发现** 等加粗章节
    bold_sections = re.split(r"(?=^\*\*[^\n]+)", article_text, flags=re.MULTILINE)
    for part in bold_sections:
        if not part.strip() or part.startswith("##"):
            continue
        first_line = part.split("\n")[0].strip()
        if first_line:
            # 去掉首尾的 **
            heading = first_line.strip("*").strip()
            # 跳过文章标题（以 # 开头的内容）
            if heading.startswith("#"):
                continue
            # 跳过结论部分的编号条目（如 **1. xxx** → heading "1. xxx"）
            if re.match(r"^\d+\.", heading):
                continue
            sections.append({
                "heading": heading,
                "content": "\n".join(part.split("\n")[1:]),
                "idx": 99,
            })

    # 识别需要配图的场景
    illustration_spots = []
    seen_headings = set()
    for s in sections:
        heading = s["heading"]
        if not heading or heading in seen_headings:
            continue
        seen_headings.add(heading)

        content_lower = s["content"].lower()
        combined = heading.lower() + " " + content_lower[:300]

        illustration_type = "scene"
        needs_image = False

        # 数据/图表类 → infographic
        if any(kw in combined for kw in ["数据", "数字", "%", "率", "调查", "报告", "发现", "percent", "rate", "survey", "figure"]):
            illustration_type = "infographic"
            needs_image = True
        # 对比/比较类 → comparison
        elif any(kw in combined for kw in ["相比", "对比", "不同", "两个", "一方", "另一方", "vs", "versus", "比较", "然而"]):
            illustration_type = "comparison"
            needs_image = True
        # 流程/步骤类 → flowchart
        elif any(kw in combined for kw in ["步骤", "流程", "首先", "然后", "最后", "过程", "step", "process", "flow"]):
            illustration_type = "flowchart"
            needs_image = True
        # 框架/架构类 → framework
        elif any(kw in combined for kw in ["框架", "模型", "架构", "体系", "framework", "model", "architecture"]):
            illustration_type = "framework"
            needs_image = True
        # 时间/历史类 → timeline
        elif any(kw in combined for kw in ["历史", "时间线", "演变", "发展", "timeline", "history", "evolution"]):
            illustration_type = "timeline"
            needs_image = True
        # 场景叙事类 → scene
        elif any(kw in combined for kw in ["案例", "故事", "工程师", "司机", "设计师", "律师", "会计师", "case", "story"]):
            illustration_type = "scene"
            needs_image = True

        if needs_image and s["content"].strip():
            illustration_spots.append({
                "section": heading,
                "content": s["content"][:500],
                "type": illustration_type,
                "idx": s["idx"],
            })

    return illustration_spots


def extract_title(content: str, fallback: str) -> str:
    """提取文章标题（--- 之后的首个 # 标题）"""
    lines = content.split("\n")
    first_divider_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "---":
            first_divider_idx = i
            break
    start = first_divider_idx + 1 if first_divider_idx is not None else 0
    for line in lines[start:]:
        stripped = line.strip()
        if stripped.startswith("# ") and "【5个标题" not in stripped:
            return stripped.lstrip("#").strip()
    return fallback


def build_prompt(spot: dict, article_title: str = "") -> str:
    """为配图位置构建 prompt"""
    ill_type = spot["type"]
    section = spot["section"]
    content = spot["content"]

    prompts = {
        "infographic": (
            f"Professional infographic illustration for section: {section}. "
            f"Data visualization with charts, metrics, clean typography. "
            f"Content: {content[:200]}. "
            f"Modern flat design, corporate style. 16:9 aspect ratio."
        ),
        "comparison": (
            f"Side-by-side comparison illustration for: {section}. "
            f"Two-column layout showing contrast. "
            f"Content: {content[:200]}. "
            f"Clean vector style with clear visual separation. 16:9 aspect ratio."
        ),
        "flowchart": (
            f"Process flow diagram for section: {section}. "
            f"Step-by-step workflow with arrows and nodes. "
            f"Content: {content[:200]}. "
            f"Technical schematic style. 16:9 aspect ratio."
        ),
        "framework": (
            f"Conceptual framework diagram for: {section}. "
            f"Architecture or model with connected components. "
            f"Content: {content[:200]}. "
            f"Technical blueprint style. 16:9 aspect ratio."
        ),
        "timeline": (
            f"Timeline visualization for: {section}. "
            f"Chronological progression with milestone markers. "
            f"Content: {content[:200]}. "
            f"Modern editorial infographic style. 16:9 aspect ratio."
        ),
        "scene": (
            f"Editorial illustration for section: {section}. "
            f"Atmospheric human-centric scene: {content[:200]}. "
            f"Clean magazine illustration style, warm tones. 16:9 aspect ratio."
        ),
    }
    return prompts.get(ill_type, prompts["scene"])


def generate_image(
    prompt: str,
    output_path: str,
    aspect: str = "16:9",
    quality: str = "2k",
) -> bool:
    """通过 Aiberm/Gemini API 生成图像"""
    try:
        import requests

        api_key = os.getenv("AIBERM_API_KEY") or os.getenv("GOOGLE_AI_API_KEY")
        if not api_key:
            print("Error: AIBERM_API_KEY / GOOGLE_AI_API_KEY not set")
            return False

        base_url = "https://aiberm.com/v1beta/models"
        model = "gemini-3.1-flash-image-preview"

        size_map = {
            "16:9": ("1024", "576"),
            "1:1": ("1024", "1024"),
            "4:3": ("1024", "768"),
            "9:16": ("576", "1024"),
        }
        image_size_map = {"normal": "1K", "2k": "2K"}
        image_size = image_size_map.get(quality, "2K")

        resp = requests.post(
            f"{base_url}/{model}:generateContent",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "contents": [{"parts": [{"text": f"Generate an image of: {prompt}"}]}],
                "generationConfig": {
                    "responseModalities": ["TEXT", "IMAGE"],
                    "imageSize": image_size,
                },
            },
            timeout=180,
        )
        resp.raise_for_status()
        data = resp.json()

        for candidate in data.get("candidates", []):
            for part in candidate.get("content", {}).get("parts", []):
                if "inlineData" in part:
                    b64 = part["inlineData"]["data"]
                    img_bytes = base64.b64decode(b64)
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(img_bytes)
                    return True

        print(f"No image in response for: {output_path}")
        return False

    except Exception as e:
        print(f"Image generation failed for {output_path}: {e}")
        return False


def _normalize_heading(text: str) -> str:
    """标准化章节标题用于匹配：去掉 ** # 空格，转小写"""
    return text.strip().strip("*").strip("#").strip().lower()


def insert_images_into_article(
    article_path: str,
    selected: list[dict],
    output_dir: str,
) -> str:
    """将图像路径插入文章 Markdown，按章节标题精确匹配插图位置"""
    content = Path(article_path).read_text(encoding="utf-8")
    lines = content.split("\n")

    # 建立 spot 的精确匹配表：normalized heading → (spot, img_index)
    # img index 是生成时的序号（1-based），用于找到对应图片文件
    spot_map: dict[str, tuple[dict, int]] = {}
    for i, spot in enumerate(selected):
        key = _normalize_heading(spot["section"])
        spot_map[key] = (spot, i + 1)

    # 找到第一个 --- 的行号，只在正文区域插图
    first_divider_line = None
    for idx, line in enumerate(lines):
        if line.strip() == "---":
            first_divider_line = idx
            break

    new_lines = []
    for line_idx, line in enumerate(lines):
        new_lines.append(line)

        # 只在正文区域（--- 之后）处理插图
        if first_divider_line is not None and line_idx <= first_divider_line:
            continue

        stripped = line.strip()
        is_heading = (
            stripped.startswith("## ")
            or (stripped.startswith("**") and stripped.endswith("**") and len(stripped) > 4)
        )
        if not is_heading:
            continue

        # 精确匹配：用当前行的标题文本查找对应 spot
        key = _normalize_heading(stripped)
        if key not in spot_map:
            continue

        spot, img_idx = spot_map[key]
        img_name = f"article-img-{img_idx:02d}-{spot['type']}.png"
        img_rel = f"imgs/{img_name}"
        img_full = Path(output_dir) / "imgs" / img_name

        if img_full.exists():
            desc = spot["section"]
            new_lines.append(f'\n![{desc}]({img_rel})\n')
            # 用完即删，防止同一标题重复插图
            del spot_map[key]

    return "\n".join(new_lines)


def main():
    parser = argparse.ArgumentParser(description="Article Illustrator")
    parser.add_argument("article", help="文章Markdown文件路径")
    parser.add_argument("--density", default="balanced",
                        choices=["minimal", "balanced", "per-section", "rich"])
    parser.add_argument("--aspect", default="16:9",
                        choices=["16:9", "1:1", "4:3", "9:16"])
    parser.add_argument("--quality", default="2k", choices=["normal", "2k"])
    parser.add_argument("--max-images", type=int, default=3)
    parser.add_argument("--no-insert", action="store_true", help="只生成图，不插入文章")
    args = parser.parse_args()

    load_config()

    article_path = Path(args.article)
    if not article_path.exists():
        print(f"Article not found: {article_path}")
        sys.exit(1)

    content = article_path.read_text(encoding="utf-8")
    article_title = extract_title(content, article_path.stem)
    print(f"Article: {article_title}")
    print("Analyzing structure...")

    spots = analyze_article(content)
    print(f"Found {len(spots)} illustration spots")

    if not spots:
        print("No suitable positions found.")
        sys.exit(0)

    max_map = {"minimal": 1, "balanced": 3, "per-section": len(spots), "rich": min(len(spots), 6)}
    limit = min(args.max_images, max_map.get(args.density, 3), len(spots))
    selected = spots[:limit]

    print(f"Generating {len(selected)} images...")

    # imgs 输出到文章所在目录
    img_output_dir = str(article_path.parent)
    generated = []

    for i, spot in enumerate(selected):
        img_name = f"article-img-{i+1:02d}-{spot['type']}.png"
        img_full_path = Path(img_output_dir) / "imgs" / img_name
        img_full_path.parent.mkdir(parents=True, exist_ok=True)

        prompt = build_prompt(spot, article_title)
        print(f"\n[{i+1}/{len(selected)}] type={spot['type']} section={spot['section'][:30]}")

        ok = generate_image(
            prompt=prompt,
            output_path=str(img_full_path),
            aspect=args.aspect,
            quality=args.quality,
        )

        if ok:
            rel = f"imgs/{img_name}"
            generated.append({"spot": spot, "path": rel, "full": str(img_full_path)})
            print(f"  [OK] saved image")
        else:
            print(f"  [FAIL]")

    if not generated:
        print("No images generated.")
        sys.exit(1)

    if not args.no_insert:
        updated = insert_images_into_article(
            str(article_path),
            selected,
            img_output_dir,
        )
        out_path = article_path.with_suffix(".illustrated.md")
        out_path.write_text(updated, encoding="utf-8")
        print(f"\n[DONE] Article with illustrations: {out_path}")
    else:
        print(f"\n{len(generated)} images saved to: {img_output_dir}/imgs/")

    print(f"Done: {len(generated)} images generated")
    for g in generated:
        print(f"  {g['path']}")


if __name__ == "__main__":
    main()
