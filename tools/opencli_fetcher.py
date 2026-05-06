#!/usr/bin/env python3
"""
OpenCLI Fetcher - Use opencli to collect viral content from multiple platforms
Supports: xiaohongshu, zhihu, bilibili, twitter, reddit, hackernews

This script wraps opencli CLI commands. Make sure:
1. opencli is installed: npm install -g @jackwener/opencli
2. Chrome browser is running with target site logged in
3. OpenCLI Browser Bridge extension is installed and enabled
4. Run 'opencli doctor' to verify connection
"""

import json
import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


def run_opencli(command: List[str], verbose: bool = False) -> Optional[Dict]:
    """Run opencli command and return parsed result"""
    try:
        if verbose:
            print(f"Running: opencli {' '.join(command)}")

        result = subprocess.run(
            ["opencli"] + command,
            capture_output=True,
            text=True,
            timeout=90,
            encoding='utf-8',
            errors='replace'
        )

        if result.returncode == 0:
            return {"success": True, "output": result.stdout}
        else:
            stderr = result.stderr or ""
            stdout = result.stdout or ""
            error_msg = stderr if stderr else (stdout if "Error" in stdout else "Unknown error")
            return {"success": False, "error": error_msg}

    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timeout (90s)"}
    except FileNotFoundError:
        return {"success": False, "error": "opencli not found. Install with: npm install -g @jackwener/opencli"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_platform_command(platform: str, query: str = None, limit: int = 10) -> List[str]:
    """Build opencli command for platform"""
    if platform == "xiaohongshu":
        cmd = ["xiaohongshu", "search", query or "AI", "--limit", str(limit), "-f", "json"]
    elif platform == "zhihu":
        if query:
            cmd = ["zhihu", "search", query, "--limit", str(limit), "-f", "json"]
        else:
            cmd = ["zhihu", "hot", "--limit", str(limit), "-f", "json"]
    elif platform == "bilibili":
        if query:
            cmd = ["bilibili", "search", query, "--limit", str(limit), "-f", "json"]
        else:
            cmd = ["bilibili", "hot", "--limit", str(limit), "-f", "json"]
    elif platform == "twitter":
        cmd = ["twitter", "trending", "--limit", str(limit), "-f", "json"]
    elif platform == "reddit":
        if query:
            cmd = ["reddit", "search", query, "--limit", str(limit), "-f", "json"]
        else:
            cmd = ["reddit", "hot", "--limit", str(limit), "-f", "json"]
    elif platform == "hackernews":
        cmd = ["hackernews", "top", "--limit", str(limit), "-f", "json"]
    else:
        cmd = []
    return cmd


def collect_viral_articles(
    platform: str, query: str = None, limit: int = 10, verbose: bool = False
) -> List[Dict]:
    """Collect viral articles from specified platform using opencli"""

    cmd = get_platform_command(platform, query, limit)

    if not cmd:
        if verbose:
            print(f"Unknown platform: {platform}")
        return []

    result = run_opencli(cmd, verbose)

    if not result or not result.get("success"):
        error_msg = result.get("error", "Unknown error") if result else "No result"
        if verbose:
            print(f"Error for {platform}: {error_msg}")
        return []

    try:
        output = result["output"].strip()

        if not output:
            if verbose:
                print(f"No output from {platform}")
            return []

        data = json.loads(output)

        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            if "data" in data:
                return data["data"] if isinstance(data["data"], list) else [data["data"]]
            elif "items" in data:
                return data["items"] if isinstance(data["items"], list) else [data["items"]]
            elif "results" in data:
                return data["results"] if isinstance(data["results"], list) else [data["results"]]
            else:
                return [data]
        else:
            return []

    except json.JSONDecodeError as e:
        if verbose:
            print(f"JSON parse error for {platform}: {e}")
            print(f"Raw output: {result['output'][:200]}")
        return []


def check_opencli_connection(verbose: bool = False) -> Dict:
    """Check if opencli is properly connected"""
    result = run_opencli(["doctor"], verbose)

    if result and result.get("success"):
        output = result["output"].lower()
        if "ok" in output and "connected" in output:
            return {"status": "connected", "output": result["output"]}
        elif "error" in output:
            return {"status": "error", "output": result["output"]}

    return {"status": "unknown", "output": result.get("error", "Connection check failed")}


def format_results(results: List[Dict], platform: str) -> str:
    """Format results as markdown"""
    if not results:
        return f"No results found for {platform}"

    platform_names = {
        "xiaohongshu": "小红书",
        "zhihu": "知乎",
        "bilibili": "B站",
        "twitter": "Twitter/X",
        "reddit": "Reddit",
        "hackernews": "Hacker News"
    }

    lines = [f"## {platform_names.get(platform, platform)}", f"**Total:** {len(results)}", ""]

    for i, item in enumerate(results, 1):
        if platform == "xiaohongshu":
            title = item.get("title", item.get("desc", "N/A"))
            author = item.get("author", item.get("user", item.get("nickname", "N/A")))
            likes = item.get("likes", item.get("liked_count", "N/A"))
            lines.append(f"### {i}. {title}")
            lines.append(f"**Author:** {author} | **Likes:** {likes}")
            if item.get("url"):
                lines.append(f"**Link:** {item['url']}")

        elif platform == "zhihu":
            title = item.get("title", "N/A")
            heat = item.get("heat", item.get("hot", "N/A"))
            answers = item.get("answers", item.get("answer_count", "N/A"))
            lines.append(f"### {i}. {title}")
            lines.append(f"**Heat:** {heat} | **Answers:** {answers}")
            if item.get("url"):
                lines.append(f"**Link:** {item['url']}")

        elif platform == "bilibili":
            title = item.get("title", "N/A")
            author = item.get("author", "N/A")
            play = item.get("play", item.get("views", "N/A"))
            lines.append(f"### {i}. {title}")
            lines.append(f"**UP主:** {author} | **播放:** {play}")
            if item.get("url"):
                lines.append(f"**Link:** {item['url']}")

        elif platform == "twitter":
            topic = item.get("topic", item.get("name", "N/A"))
            category = item.get("category", "")
            lines.append(f"### {i}. {topic}")
            if category:
                lines.append(f"**Category:** {category}")

        elif platform == "reddit":
            title = item.get("title", "N/A")
            score = item.get("score", item.get("upvotes", "N/A"))
            lines.append(f"### {i}. {title}")
            lines.append(f"**Score:** {score}")

        elif platform == "hackernews":
            title = item.get("title", "N/A")
            score = item.get("score", item.get("points", "N/A"))
            lines.append(f"### {i}. {title}")
            lines.append(f"**Score:** {score}")
            if item.get("url"):
                lines.append(f"**Link:** {item['url']}")

        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="OpenCLI Viral Content Fetcher - Collect trending content from social platforms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search Xiaohongshu for AI related viral notes
  python opencli_fetcher.py --platform xiaohongshu --query "AI工具" --limit 10

  # Get Zhihu hot topics
  python opencli_fetcher.py --platform zhihu --limit 10

  # Get Bilibili hot videos
  python opencli_fetcher.py --platform bilibili --limit 10

  # Get Twitter trending topics
  python opencli_fetcher.py --platform twitter --limit 10

  # Check opencli connection status
  python opencli_fetcher.py --check

  # Output to JSON file
  python opencli_fetcher.py --platform xiaohongshu --output viral.json

Prerequisites:
  1. Install opencli: npm install -g @jackwener/opencli
  2. Chrome browser running with target site logged in
  3. OpenCLI Browser Bridge extension installed and enabled
  4. Run 'opencli doctor' to verify connection
        """,
    )

    parser.add_argument(
        "--platform", "-p",
        choices=["xiaohongshu", "zhihu", "bilibili", "twitter", "reddit", "hackernews"],
        help="Platform to collect from"
    )
    parser.add_argument("--query", "-q", help="Search query (optional)")
    parser.add_argument(
        "--limit", "-l", type=int, default=10,
        help="Number of results per platform (default: 10)"
    )
    parser.add_argument("--output", "-o", help="Output JSON file (optional)")
    parser.add_argument(
        "--markdown", "-m", action="store_true",
        help="Output results as formatted Markdown"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "--check", action="store_true",
        help="Check opencli connection status"
    )

    args = parser.parse_args()

    if args.check:
        print("🔍 Checking opencli connection...")
        status = check_opencli_connection(args.verbose)
        print(f"Status: {status['status']}")
        print(status['output'])
        return

    if not args.platform:
        parser.print_help()
        print("\n❌ Error: --platform is required (or use --check to verify connection)")
        return

    print(f"📡 Collecting {args.platform} viral content...")

    results = collect_viral_articles(
        platform=args.platform,
        query=args.query,
        limit=args.limit,
        verbose=args.verbose
    )

    if not results:
        print("⚠️ No results found. Please ensure:")
        print("   1. Chrome browser is running with the target site logged in")
        print("   2. OpenCLI Browser Bridge extension is installed and enabled")
        print("   3. Run 'opencli doctor' to verify connection")
        return

    print(f"✅ Found {len(results)} items")

    if args.markdown:
        print()
        print(format_results(results, args.platform))

    if args.output:
        output_dir = Path(args.output).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        output_data = {
            "platform": args.platform,
            "query": args.query,
            "collected_at": datetime.now().isoformat(),
            "count": len(results),
            "items": results,
        }
        Path(args.output).write_text(
            json.dumps(output_data, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        print(f"💾 Saved to: {args.output}")
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()