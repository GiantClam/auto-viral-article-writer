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


def load_config():
    """Load configuration from environment variables"""

    if load_dotenv:
        env_file = find_env_file()
        if env_file:
            load_dotenv(env_file)

    config = {
        "google_ai_api_key": os.getenv("GOOGLE_AI_API_KEY"),
        "google_search_api_key": os.getenv("GOOGLE_SEARCH_API_KEY"),
        "google_search_engine_id": os.getenv("GOOGLE_SEARCH_ENGINE_ID"),
        "jina_api_key": os.getenv("JINA_API_KEY"),
        "openrouter_api_key": os.getenv("OPENROUTER_API_KEY"),
        "dify_api_url": os.getenv("DIFY_API_URL"),
        "dify_api_key": os.getenv("DIFY_API_KEY"),
        "notion_api_key": os.getenv("NOTION_API_KEY"),
        "notion_database_id": os.getenv("NOTION_DATABASE_ID"),
        "google_sheets_api_key": os.getenv("GOOGLE_SHEETS_API_KEY"),
        "google_sheet_id": os.getenv("GOOGLE_SHEET_ID"),
        "aiberm_api_key": os.getenv("AIBERM_API_KEY"),
        "wechat_app_id": os.getenv("WECHAT_APP_ID"),
        "wechat_app_secret": os.getenv("WECHAT_APP_SECRET"),
        "serper_api_key": os.getenv("SERPER_API_KEY"),
        "rsshub_base": os.getenv("RSSHUB_BASE", "https://rsshub.app"),
        "wewe_rss_base": os.getenv("WEWE_RSS_BASE"),
        "wewe_auth_code": os.getenv("WEWE_AUTH_CODE"),
    }

    return config


def validate_config(config, verbose=True):
    """Validate required configuration items"""
    # Either google_ai_api_key, aiberm_api_key, or openrouter_api_key is required
    has_ai_key = (
        config.get("google_ai_api_key")
        or config.get("aiberm_api_key")
        or config.get("openrouter_api_key")
    )

    if not has_ai_key:
        if verbose:
            print(
                "Missing required config: GOOGLE_AI_API_KEY, AIBERM_API_KEY, or OPENROUTER_API_KEY"
            )
            print("Please configure at least one in config/.env")
        return False

    if verbose:
        # Check optional configurations
        optional_keys = {
            "google_ai_api_key": "Google AI (direct)",
            "aiberm_api_key": "Aiberm (for images)",
            "openrouter_api_key": "OpenRouter",
            "google_search_api_key": "Google Search",
            "google_search_engine_id": "Google Search Engine ID",
            "jina_api_key": "Jina Reader",
        }

        configured = []
        not_configured = []

        for key, name in optional_keys.items():
            if config.get(key):
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
