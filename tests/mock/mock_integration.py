#!/usr/bin/env python3

"""Module to patch SEO Agent components with mock data for testing.

This lets you test the application without needing real API keys.
"""

from typing import Any, Optional


class MockKeywordGenerator:
    """Mock implementation of KeywordGenerator that doesn't require API keys."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the mock generator."""
        self.config = config

    def generate_keywords(
        self, seed_keyword: str, industry: Optional[str] = None
    ) -> list[dict[str, Any]]:
        # Note: This is a mock implementation that returns a list of dictionaries
        """Generate mock keywords without using APIs."""
        from mock_keyword_data import generate_mock_keywords

        # Generate mock data
        mock_data = generate_mock_keywords(seed_keyword, industry or "general")

        # Return just the keywords list
        return mock_data["keywords"]


def patch_keyword_engine():
    """Patch the KeywordEngine to use mock data."""
    from seo_agent.core.keyword_engine import KeywordEngine

    # Save the original init method
    original_init = KeywordEngine.__init__

    def patched_init(self, config: dict[str, Any]) -> None:
        """Patched init that uses mock generator."""
        # Call original init
        original_init(self, config)

        # Replace the keyword generator with our mock
        self.keyword_generator = MockKeywordGenerator(config)

    # Apply the patch
    KeywordEngine.__init__ = patched_init
    print("✅ KeywordEngine patched to use mock data")


if __name__ == "__main__":
    # Patch everything
    patch_keyword_engine()

    # Now run the main application
    import subprocess
    import sys

    # Forward all command-line arguments to the main application
    cmd = [sys.executable, "main.py"] + sys.argv[1:]
    result = subprocess.run(cmd, check=True)
    sys.exit(result.returncode)
