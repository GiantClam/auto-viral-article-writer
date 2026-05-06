#!/usr/bin/env python3
"""
Configuration Loader
Load environment variables from .env file
"""

import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("Warning: python-dotenv not installed. Run: pip install python-dotenv")
    load_dotenv = None


def find_env_file():
    """Find .env file in config directory or parent directories"""
    current = Path(__file__).parent.parent

    # Check config/.env first
    env_path = current / "config" / ".env"
    if env_path.exists():
        return env_path

    # Check root .env
    env_path = current / ".env"
    if env_path.exists():
        return env_path

    return None


def load_extend_config():
    """Load optional YAML configuration from config/EXTEND.md."""
    extend_path = Path(__file__).parent.parent / "config" / "EXTEND.md"
    if not extend_path.exists():
        return {}

    try:
        import yaml
    except ImportError:
        return {}

    try:
        content = extend_path.read_text(encoding="utf-8")
        return yaml.safe_load(content) or {}
    except Exception:
        return {}


def load_config():
    """Load configuration from environment variables"""

    if load_dotenv:
        env_file = find_env_file()
        if env_file:
            load_dotenv(env_file)

    extend_config = load_extend_config()
    openai_compatible_extend = extend_config.get("openai_compatible", {}) if extend_config else {}

    config = {
        "google_ai_api_key": os.getenv("GOOGLE_AI_API_KEY"),
        "google_search_api_key": os.getenv("GOOGLE_SEARCH_API_KEY"),
        "google_search_engine_id": os.getenv("GOOGLE_SEARCH_ENGINE_ID"),
        "jina_api_key": os.getenv("JINA_API_KEY"),
        "openrouter_api_key": os.getenv("OPENROUTER_API_KEY"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "openai_base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com"),
        "dify_api_url": os.getenv("DIFY_API_URL"),
        "dify_api_key": os.getenv("DIFY_API_KEY"),
        "notion_api_key": os.getenv("NOTION_API_KEY"),
        "notion_database_id": os.getenv("NOTION_DATABASE_ID"),
        "google_sheets_api_key": os.getenv("GOOGLE_SHEETS_API_KEY"),
        "google_sheet_id": os.getenv("GOOGLE_SHEET_ID"),
        "wechat_app_id": os.getenv("WECHAT_APP_ID"),
        "wechat_app_secret": os.getenv("WECHAT_APP_SECRET"),
        "serper_api_key": os.getenv("SERPER_API_KEY"),
        "rsshub_base": os.getenv("RSSHUB_BASE", "https://rsshub.app"),
        "wewe_rss_base": os.getenv("WEWE_RSS_BASE"),
        "wewe_auth_code": os.getenv("WEWE_AUTH_CODE"),
        "openai_compatible": {
            "api_key": os.getenv("OPENAI_COMPATIBLE_API_KEY"),
            "base_url": os.getenv("OPENAI_COMPATIBLE_BASE_URL") or openai_compatible_extend.get("base_url", ""),
            "default_size": openai_compatible_extend.get("default_size", "1536x1024"),
            "default_quality": openai_compatible_extend.get("default_quality", "high"),
            "default_n": openai_compatible_extend.get("default_n", 1),
        },
    }

    return config


def validate_config(config, verbose=True):
    """Validate required configuration items"""
    # Either official Gemini, official OpenAI, or OpenAI-compatible credentials are required.
    openai_compatible_config = config.get("openai_compatible", {})
    has_ai_key = (
        config.get("google_ai_api_key")
        or config.get("openai_api_key")
        or (openai_compatible_config and openai_compatible_config.get("api_key"))
    )

    if not has_ai_key:
        if verbose:
            print(
                "Missing required config: GOOGLE_AI_API_KEY, OPENAI_API_KEY, or OPENAI_COMPATIBLE_API_KEY"
            )
            print("Please configure at least one in config/.env")
        return False

    if verbose:
        # Check optional configurations
        optional_keys = {
            "openai_compatible": "OpenAI-compatible image API",
            "openai_api_key": "OpenAI official API",
            "google_ai_api_key": "Google AI (direct)",
            "google_search_api_key": "Google Search",
            "google_search_engine_id": "Google Search Engine ID",
            "jina_api_key": "Jina Reader",
        }

        configured = []
        not_configured = []

        for key, name in optional_keys.items():
            value = config.get(key)
            if key == "openai_compatible":
                value = value and value.get("api_key")
            if value:
                configured.append(name)
            else:
                not_configured.append(name)

        if configured:
            print(f"Configured: {', '.join(configured)}")
        if not_configured:
            print(f"Not configured (optional): {', '.join(not_configured)}")

    return True


def get_api_key(key_name):
    """Get a specific API key"""
    config = load_config()
    return config.get(key_name)


if __name__ == "__main__":
    print("Checking configuration...")
    config = load_config()

    if validate_config(config, verbose=True):
        print("\nConfiguration valid!")
    else:
        print("\nConfiguration incomplete!")
        sys.exit(1)
