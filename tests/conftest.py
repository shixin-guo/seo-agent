"""Pytest configuration for SEO Agent tests.

This module contains fixtures and configuration for pytest.
"""

import os
import sys
from typing import Any

import pytest

# Add the project root to the path so we can import the seo_agent package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def sample_config() -> dict[str, Any]:
    """Return a sample configuration dictionary for testing."""
    return {
        "defaults": {"max_keywords": 10, "crawl_depth": 20},
        "ai": {"model": "gpt-4-turbo-preview", "max_tokens": 2000, "temperature": 0.3},
        "apis": {"openai_key": "test_api_key"},
    }


@pytest.fixture
def sample_keywords() -> list[dict[str, Any]]:
    """Return sample keywords for testing."""
    return [
        {"keyword": "seo tools", "intent": "commercial", "competition": "high"},
        {
            "keyword": "best seo practices",
            "intent": "informational",
            "competition": "medium",
        },
        {
            "keyword": "how to improve seo",
            "intent": "informational",
            "competition": "medium",
        },
        {"keyword": "seo software", "intent": "transactional", "competition": "high"},
        {"keyword": "seo tutorial", "intent": "informational", "competition": "low"},
    ]


@pytest.fixture
def sample_content() -> str:
    """Return sample content for testing content optimization."""
    return """
# SEO Best Practices

Search Engine Optimization is essential for website visibility.

Some key strategies include:
- Keyword research
- Quality content creation
- Technical optimization
- Link building

## Technical SEO

Technical SEO focuses on improving site infrastructure.
    """


@pytest.fixture
def sample_backlink_data() -> dict[str, Any]:
    """Return sample backlink data for testing."""
    return {
        "domain": "example.com",
        "links": [
            {
                "source": "blog.example.org",
                "target": "example.com/page1",
                "anchor_text": "useful resource",
            },
            {
                "source": "news.example.net",
                "target": "example.com",
                "anchor_text": "industry leader",
            },
        ],
    }


@pytest.fixture
def sample_crawl_results() -> dict[str, Any]:
    """Return sample crawl results for testing site auditor."""
    return {
        "domain": "example.com",
        "pages": [
            {
                "url": "example.com/page1",
                "status_code": 200,
                "title": "Page 1",
                "meta_description": "This is page 1",
                "h1": "Page 1 Heading",
                "issues": ["missing_alt_text"],
            },
            {
                "url": "example.com/page2",
                "status_code": 200,
                "title": "Page 2",
                "meta_description": "",
                "h1": "Page 2 Heading",
                "issues": ["missing_meta_description"],
            },
            {
                "url": "example.com/page3",
                "status_code": 404,
                "title": "Not Found",
                "meta_description": "",
                "h1": "",
                "issues": ["broken_page"],
            },
        ],
    }
