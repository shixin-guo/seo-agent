#!/usr/bin/env python3
"""Test script to verify article generator functionality."""

import os
import pytest
from seo_agent.core.article_generator import ArticleGenerator
from utils import load_config


@pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY") and not load_config().get("apis", {}).get("openai_key"),
    reason="OpenAI API key not available - skipping AI-dependent test"
)
def test_article_generator() -> None:
    """Test article generation functionality."""
    print("Testing article generator functionality...")

    config = load_config()
    generator = ArticleGenerator(config)
    print("✓ Article generator initialized successfully")

    article = generator.generate_article_from_keywords(
        seed_keyword="digital marketing", industry="technology", min_length=500
    )

    print("✓ Article generated successfully")
    print(f"  Title: {article.title}")
    print(f"  Keywords: {', '.join(article.keywords[:3]) if article.keywords else 'None'}...")
    print(f"  Content length: {len(article.content)} characters")
    print(f"  Meta description: {(article.meta_description or '')[:50]}...")

    assert article.title, "Article missing title"
    assert article.content, "Article missing content"
    assert len(article.keywords) > 0, "Article missing keywords"

    print("✓ Article generation test completed successfully!")


def test_article_generator_without_api_key() -> None:
    """Test that article generator fails gracefully without API key."""
    config = load_config()
    
    if "apis" in config:
        config["apis"].pop("openai_key", None)
    
    original_key = os.environ.pop("OPENAI_API_KEY", None)
    
    try:
        with pytest.raises(ValueError, match="OpenAI API key is required"):
            ArticleGenerator(config)
    finally:
        if original_key:
            os.environ["OPENAI_API_KEY"] = original_key


if __name__ == "__main__":
    test_article_generator()
