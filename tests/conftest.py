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
def sample_improved_backlink_data() -> dict[str, Any]:
    """Return sample improved backlink data for testing."""
    return {
        "domain": "example.com",
        "backlinks": [
            {
                "source_domain": "blog.example.org",
                "source_url": "https://blog.example.org/post1",
                "target_url": "https://example.com/page1",
                "anchor_text": "useful resource",
                "link_type": "dofollow",
                "domain_authority": 45,
                "first_seen": "2024-01-15",
                "category": "technology",
            },
            {
                "source_domain": "news.example.net",
                "source_url": "https://news.example.net/article2",
                "target_url": "https://example.com",
                "anchor_text": "industry leader",
                "link_type": "dofollow",
                "domain_authority": 60,
                "first_seen": "2024-02-20",
                "category": "business",
            },
            {
                "source_domain": "review.example.com",
                "source_url": "https://review.example.com/tools",
                "target_url": "https://example.com/product",
                "anchor_text": "top solution",
                "link_type": "nofollow",
                "domain_authority": 35,
                "first_seen": "2024-03-10",
                "category": "marketing",
            },
        ],
        "competitors": {
            "competitor1.com": {
                "backlinks": [
                    {
                        "source_domain": "blog.example.org",
                        "source_url": "https://blog.example.org/post1",
                        "target_url": "https://competitor1.com/page1",
                        "anchor_text": "alternative solution",
                        "link_type": "dofollow",
                        "domain_authority": 45,
                        "first_seen": "2024-01-20",
                        "category": "technology",
                    },
                    {
                        "source_domain": "resource.example.com",
                        "source_url": "https://resource.example.com/list",
                        "target_url": "https://competitor1.com",
                        "anchor_text": "market leader",
                        "link_type": "dofollow",
                        "domain_authority": 55,
                        "first_seen": "2024-02-15",
                        "category": "business",
                    },
                ],
                "metrics": {
                    "domain_authority": 52,
                    "page_authority": 48,
                    "referring_domains": 230,
                    "total_backlinks": 1200,
                },
            }
        },
        "metrics": {
            "domain_authority": 48,
            "page_authority": 45,
            "trust_flow": 35,
            "citation_flow": 40,
            "referring_domains": 180,
            "total_backlinks": 950,
        },
        "opportunities": [
            {
                "source_domain": "resource.example.com",
                "source_url": "https://resource.example.com/list",
                "target_url": "https://competitor1.com",
                "anchor_text": "market leader",
                "link_type": "dofollow",
                "domain_authority": 55,
                "first_seen": "2024-02-15",
                "category": "business",
                "competitor": "competitor1.com",
                "opportunity_type": "competitor_backlink",
                "opportunity_score": 45,
            }
        ],
        "summary": {
            "total_backlinks": 3,
            "dofollow_count": 2,
            "nofollow_count": 1,
            "unique_domains": 3,
            "total_opportunities": 1,
            "opportunity_types": {"competitor_backlink": 1},
        },
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
