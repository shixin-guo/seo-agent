"""Shared utilities for SEO Agent.

This module provides common functionality used by both CLI and API components.
"""

import os
from typing import Any, Dict, cast

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def load_config() -> Dict[str, Any]:
    """Load and merge configuration from YAML file and environment variables.

    Returns:
        Dict[str, Any]: Configuration dictionary with API keys and settings.
    """
    config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "config.yaml"
    )
    with open(config_path) as f:
        config = yaml.safe_load(f)
        if config is None:
            config = {}
        config = dict(config)

    # Add API keys from environment variables
    api_keys = {
        "openai_key": os.getenv("OPENAI_API_KEY"),
        "serpapi_key": os.getenv("SERPAPI_KEY"),
        "ahrefs_key": os.getenv("AHREFS_API_KEY"),
        "semrush_key": os.getenv("SEMRUSH_API_KEY"),
    }

    # Remove None values
    api_keys = {k: v for k, v in api_keys.items() if v is not None}

    # Merge with config
    if "apis" not in config:
        config["apis"] = {}
    config["apis"].update(api_keys)

    return cast(Dict[str, Any], config)
