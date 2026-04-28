#!/usr/bin/env python3
"""
Jina AI Reader Client
Convert web URLs to LLM-friendly Markdown format
"""

import argparse
import sys
from pathlib import Path
from urllib.parse import urlparse

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config_loader import load_config

try:
    import requests
except ImportError:
    print("Error: requests not installed")
    print("Run: pip install requests")
    sys.exit(1)


def extract_content(api_key, url, verbose=False):
    """Extract web page content using Jina Reader API

    Args:
        api_key: Jina API key (optional, but recommended for higher quota)
        url: URL to extract content from
        verbose: Print verbose output
    """

    if verbose:
        print(f"Extracting content: {url}")

    # Jina Reader API endpoint
    jina_url = f"https://r.jina.ai/{url}"

    headers = {"Accept": "text/markdown"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        response = requests.get(jina_url, headers=headers, timeout=30)
        response.raise_for_status()

        markdown_content = response.text.strip()

        print(f"Content extracted: {len(markdown_content)} chars")

        if verbose:
            print(f"  Preview (first 300 chars):")
            print(f"  {markdown_content[:300]}...")

        return markdown_content

    except requests.exceptions.Timeout:
        print(f"Timeout: {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Extraction failed: {str(e)}")
        return None


def batch_extract(urls_file, api_key=None, output_dir=None, verbose=False):
    """Extract content from multiple URLs"""

    urls = Path(urls_file).read_text(encoding="utf-8").strip().split("\n")
    valid_urls = [
        url.strip()
        for url in urls
        if url.strip() and url.strip().startswith(("http://", "https://"))
    ]

    if not valid_urls:
        print("Error: No valid URLs found")
        return 0

    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    all_content = []

    for i, url in enumerate(valid_urls, 1):
        if verbose:
            print(f"\n[{i}/{len(valid_urls)}]", end=" ")

        content = extract_content(api_key, url, verbose)

        if content:
            all_content.append({"url": url, "content": content})

            if output_dir:
                # Generate safe filename from URL
                parsed = urlparse(url)
                domain = parsed.netloc.replace(".", "_")
                filename = f"extracted_{i:02d}_{domain}.md"
                output_path = output_dir / filename

                output_path.write_text(content, encoding="utf-8")

                if verbose:
                    print(f"  Saved: {output_path}")

            success_count += 1

    print(f"\nExtracted {success_count}/{len(valid_urls)} pages")
    return success_count, all_content


def format_for_findings(url, content, max_length=5000):
    """Format extracted content for findings.md"""

    parsed = urlparse(url)
    domain = parsed.netloc

    # Truncate if too long
    if len(content) > max_length:
        content = content[:max_length] + "\n\n... [Content truncated]"

    return f"""## Source: {domain}

**URL:** {url}

### Extracted Content

{content}

---
"""


def main():
    parser = argparse.ArgumentParser(
        description="Jina Reader - Web Content Extractor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract single URL
  python3 jina_reader.py --url "https://example.com/article"
  
  # Extract and save to file
  python3 jina_reader.py --url "https://example.com/article" --output article.md
  
  # Batch extract from file
  python3 jina_reader.py --urls-file urls.txt --output extracted/
  
  # Format for findings.md
  python3 jina_reader.py --url "https://example.com/article" --findings
""",
    )

    parser.add_argument("--url", help="Single URL to extract")
    parser.add_argument("--urls-file", help="File with multiple URLs (one per line)")
    parser.add_argument("--api-key", help="Jina API Key (optional, higher quota)")
    parser.add_argument("--output", help="Output file or directory")
    parser.add_argument(
        "--findings", action="store_true", help="Format output for findings.md"
    )
    parser.add_argument(
        "--env", action="store_true", help="Load API key from environment"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Load API key (optional for Jina)
    api_key = args.api_key
    if args.env and not api_key:
        config = load_config()
        api_key = config.get("jina_api_key")
        if api_key and args.verbose:
            print("Loaded Jina API key from environment")

    # Execute extraction
    if args.urls_file:
        output_dir = args.output if args.output else None
        success, contents = batch_extract(
            args.urls_file, api_key, output_dir, verbose=args.verbose
        )

        if args.findings and contents:
            print("\n" + "=" * 60)
            print("# Research Findings\n")
            for item in contents:
                print(format_for_findings(item["url"], item["content"]))

    elif args.url:
        content = extract_content(api_key, args.url, verbose=args.verbose)

        if content:
            if args.output:
                Path(args.output).parent.mkdir(parents=True, exist_ok=True)
                Path(args.output).write_text(content, encoding="utf-8")
                print(f"Saved to: {args.output}")
            elif args.findings:
                print(format_for_findings(args.url, content))
            else:
                print("\n" + "=" * 60)
                print(content)
                print("=" * 60)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
