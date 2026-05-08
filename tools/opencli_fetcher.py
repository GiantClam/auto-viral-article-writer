#!/usr/bin/env python3
"""
OpenCLI Fetcher - Use opencli to collect viral content from multiple platforms
Supports: xiaohongshu, zhihu, reddit, bilibili, twitter, etc.
"""

import json
import argparse
import subprocess
import sys
import shutil
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


PLATFORM_COMMANDS = {
    "xiaohongshu": "xiaohongshu",
    "zhihu": "zhihu",
    "reddit": "reddit",
    "bilibili": "bilibili",
    "twitter": "twitter",
    "hackernews": "hackernews",
}


def resolve_opencli_command() -> Optional[List[str]]:
    executable = shutil.which("opencli")
    if executable:
        return [executable]

    if os.name != "nt":
        return None

    for candidate in ("opencli.cmd", "opencli.exe", "opencli.bat"):
        executable = shutil.which(candidate)
        if executable:
            return [executable]

    powershell_script = shutil.which("opencli.ps1")
    if powershell_script:
        return [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            powershell_script,
        ]

    return None


def emit_text(text: str) -> None:
    try:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")
    except UnicodeEncodeError:
        encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
        safe_text = text.encode(encoding, errors="replace")
        buffer = getattr(sys.stdout, "buffer", None)
        if buffer is not None:
            buffer.write(safe_text)
            if not text.endswith("\n"):
                buffer.write(os.linesep.encode(encoding, errors="replace"))
        else:
            sys.stdout.write(safe_text.decode(encoding, errors="replace"))
            if not text.endswith("\n"):
                sys.stdout.write("\n")

    flush = getattr(sys.stdout, "flush", None)
    if callable(flush):
        flush()


def run_opencli(command: List[str], verbose: bool = False) -> Optional[Dict]:
    try:
        opencli_command = resolve_opencli_command()
        if not opencli_command:
            return {
                "success": False,
                "error": "opencli executable not found in PATH for Python subprocess",
            }

        if verbose:
            emit_text(f"Running: {' '.join(opencli_command + command)}")

        result = subprocess.run(
            opencli_command + command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )

        if result.returncode == 0:
            return {"success": True, "output": result.stdout}
        else:
            emit_text(f"Error: {result.stderr}")
            return {"success": False, "error": result.stderr}

    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timeout"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def search_xiaohongshu(
    query: str, limit: int = 10, verbose: bool = False
) -> List[Dict]:
    result = run_opencli(
        ["xiaohongshu", "search", query, "--limit", str(limit), "-f", "json"], verbose
    )

    if result and result.get("success"):
        try:
            data = json.loads(result["output"])
            return data if isinstance(data, list) else [data]
        except:
            return []
    return []


def get_xiaohongshu_feed(limit: int = 10, verbose: bool = False) -> List[Dict]:
    result = run_opencli(
        ["xiaohongshu", "feed", "--limit", str(limit), "-f", "json"], verbose
    )

    if result and result.get("success"):
        try:
            data = json.loads(result["output"])
            return data if isinstance(data, list) else [data]
        except:
            return []
    return []


def search_zhihu(query: str, limit: int = 10, verbose: bool = False) -> List[Dict]:
    result = run_opencli(
        ["zhihu", "search", query, "--limit", str(limit), "-f", "json"],
        verbose,
    )

    if result and result.get("success"):
        try:
            data = json.loads(result["output"])
            return data if isinstance(data, list) else [data]
        except:
            return []
    return []


def search_reddit(query: str, limit: int = 10, verbose: bool = False) -> List[Dict]:
    result = run_opencli(
        ["reddit", "search", query, "--limit", str(limit), "-f", "json"], verbose
    )

    if result and result.get("success"):
        try:
            data = json.loads(result["output"])
            return data if isinstance(data, list) else [data]
        except:
            return []
    return []


def get_reddit_hot(limit: int = 10, verbose: bool = False) -> List[Dict]:
    result = run_opencli(
        ["reddit", "hot", "--limit", str(limit), "-f", "json"], verbose
    )

    if result and result.get("success"):
        try:
            data = json.loads(result["output"])
            return data if isinstance(data, list) else [data]
        except:
            return []
    return []


def search_bilibili(query: str, limit: int = 10, verbose: bool = False) -> List[Dict]:
    result = run_opencli(
        ["bilibili", "search", query, "--limit", str(limit), "-f", "json"], verbose
    )

    if result and result.get("success"):
        try:
            data = json.loads(result["output"])
            return data if isinstance(data, list) else [data]
        except:
            return []
    return []


def get_bilibili_hot(limit: int = 10, verbose: bool = False) -> List[Dict]:
    result = run_opencli(
        ["bilibili", "hot", "--limit", str(limit), "-f", "json"], verbose
    )

    if result and result.get("success"):
        try:
            data = json.loads(result["output"])
            return data if isinstance(data, list) else [data]
        except:
            return []
    return []


def collect_viral_articles(
    platform: str, query: str = None, limit: int = 10, verbose: bool = False
) -> List[Dict]:
    if platform == "xiaohongshu":
        if query:
            return search_xiaohongshu(query, limit, verbose)
        else:
            return get_xiaohongshu_feed(limit, verbose)

    elif platform == "zhihu":
        if query:
            return search_zhihu(query, limit, verbose)
        result = run_opencli(["zhihu", "hot", "--limit", str(limit), "-f", "json"], verbose)
        if result and result.get("success"):
            try:
                data = json.loads(result["output"])
                return data if isinstance(data, list) else [data]
            except:
                return []
        return []

    elif platform == "reddit":
        if query:
            return search_reddit(query, limit, verbose)
        else:
            return get_reddit_hot(limit, verbose)

    elif platform == "bilibili":
        if query:
            return search_bilibili(query, limit, verbose)
        else:
            return get_bilibili_hot(limit, verbose)

    elif platform == "twitter":
        result = run_opencli(
            ["twitter", "trending", "--limit", str(limit), "-f", "json"], verbose
        )
        if result and result.get("success"):
            try:
                return json.loads(result["output"])
            except:
                return []
        return []

    return []


def format_results(results: List[Dict], platform: str) -> str:
    if not results:
        return f"No results found for {platform}"

    lines = [f"## {platform.upper()} Viral Content", f"**Total:** {len(results)}", ""]

    for i, item in enumerate(results, 1):
        if platform == "xiaohongshu":
            title = item.get("title", item.get("desc", "N/A"))
            author = item.get("user", item.get("nickname", "N/A"))
            likes = item.get("liked_count", item.get("likes", "N/A"))
            lines.append(f"### {i}. {title}")
            lines.append(f"**Author:** {author} | **Likes:** {likes}")

        elif platform == "zhihu":
            title = item.get("title", "N/A")
            excerpt = item.get("excerpt", item.get("content", ""))[:100]
            lines.append(f"### {i}. {title}")
            lines.append(f"**Excerpt:** {excerpt}...")

        elif platform == "reddit":
            title = item.get("title", "N/A")
            score = item.get("score", item.get("upvotes", "N/A"))
            lines.append(f"### {i}. {title}")
            lines.append(f"**Score:** {score}")

        elif platform == "bilibili":
            title = item.get("title", "N/A")
            views = item.get("view", item.get("views", "N/A"))
            lines.append(f"### {i}. {title}")
            lines.append(f"**Views:** {views}")

        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="OpenCLI Viral Content Fetcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search Xiaohongshu for viral notes
  python3 opencli_fetcher.py --platform xiaohongshu --query "AI工具"
  
  # Get Xiaohongshu feed
  python3 opencli_fetcher.py --platform xiaohongshu
  
  # Get Reddit hot posts
  python3 opencli_fetcher.py --platform reddit
  
  # Search Reddit
  python3 opencli_fetcher.py --platform reddit --query "programming"
  
  # Get Bilibili hot
  python3 opencli_fetcher.py --platform bilibili
  
  # Output to file
  python3 opencli_fetcher.py --platform reddit --output viral.json
        """,
    )

    parser.add_argument(
        "--platform",
        "-p",
        required=True,
        choices=["xiaohongshu", "zhihu", "reddit", "bilibili", "twitter"],
        help="Platform to collect from",
    )
    parser.add_argument("--query", "-q", help="Search query (optional)")
    parser.add_argument(
        "--limit", "-l", type=int, default=10, help="Number of results (default: 10)"
    )
    parser.add_argument("--output", "-o", help="Output JSON file")
    parser.add_argument(
        "--markdown", "-m", action="store_true", help="Output as Markdown"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    print(f"Collecting {args.platform} viral content...")

    results = collect_viral_articles(
        platform=args.platform, query=args.query, limit=args.limit, verbose=args.verbose
    )

    if not results:
        emit_text("No results found. Make sure:")
        emit_text("1. Chrome browser is running with the target site logged in")
        emit_text("2. OpenCLI Browser Bridge extension is installed and enabled")
        emit_text("3. Run 'opencli doctor' to verify connection")
        return

    emit_text(f"Found {len(results)} items")

    if args.markdown:
        emit_text(format_results(results, args.platform))

    if args.output:
        output_data = {
            "platform": args.platform,
            "query": args.query,
            "collected_at": datetime.now().isoformat(),
            "count": len(results),
            "items": results,
        }
        Path(args.output).write_text(
            json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        emit_text(f"Saved to: {args.output}")
    else:
        emit_text(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
