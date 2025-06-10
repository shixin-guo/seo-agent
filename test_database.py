#!/usr/bin/env python3
"""Test script to verify database functionality."""

from seo_agent.core.database import ArticleDatabase, Article
from utils import load_config


def test_database() -> bool:
    """Test database operations."""
    print("Testing database functionality...")

    config = load_config()
    db = ArticleDatabase(config)
    print("✓ Database initialized successfully")

    test_article = Article(
        title="Test SEO Article",
        content="This is a test article about SEO optimization.",
        keywords=["seo", "optimization", "test"],
        meta_description="A test article for SEO",
        status="draft",
    )

    created = db.create_article(test_article)
    print(f"✓ Article created with ID: {created.id}")

    if created.id is None:
        print("✗ Created article has no ID")
        return False
        
    retrieved = db.get_article(created.id)
    if retrieved and retrieved.title == test_article.title:
        print("✓ Article retrieved successfully")
    else:
        print("✗ Failed to retrieve article")
        return False
    
    retrieved.status = "published"
    updated = db.update_article(created.id, retrieved)
    if updated and updated.status == "published":
        print("✓ Article updated successfully")
    else:
        print("✗ Failed to update article")
        return False

    articles = db.get_articles(limit=10)
    if len(articles) > 0:
        print(f"✓ Found {len(articles)} articles")
    else:
        print("✗ No articles found")

    search_results = db.search_articles("SEO")
    if len(search_results) > 0:
        print(f"✓ Search found {len(search_results)} articles")
    else:
        print("✗ Search returned no results")

    deleted = db.delete_article(created.id)
    if deleted:
        print("✓ Test article deleted successfully")
    else:
        print("✗ Failed to delete test article")

    print("Database test completed successfully!")
    return True


if __name__ == "__main__":
    test_database()
