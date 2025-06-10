#!/usr/bin/env python3
"""Test script to verify article generator functionality."""

from seo_agent.core.article_generator import ArticleGenerator
from utils import load_config


def test_article_generator() -> bool:
    """Test article generation functionality."""
    print("Testing article generator functionality...")

    config = load_config()
    generator = ArticleGenerator(config)
    print("✓ Article generator initialized successfully")

    try:
        article = generator.generate_article_from_keywords(
            seed_keyword="digital marketing", industry="technology", min_length=500
        )

        print("✓ Article generated successfully")
        print(f"  Title: {article.title}")
        print(f"  Keywords: {', '.join(article.keywords[:3]) if article.keywords else 'None'}...")
        print(f"  Content length: {len(article.content)} characters")
        print(f"  Meta description: {(article.meta_description or '')[:50]}...")

        if not article.title:
            print("✗ Article missing title")
            return False

        if not article.content:
            print("✗ Article missing content")
            return False

        if len(article.keywords) == 0:
            print("✗ Article missing keywords")
            return False

        print("✓ Article generation test completed successfully!")
        return True

    except Exception as e:
        print(f"✗ Article generation failed: {e}")
        return False


if __name__ == "__main__":
    test_article_generator()
