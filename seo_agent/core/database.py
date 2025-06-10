"""Database models and connection layer for article storage.

This module provides database connectivity and CRUD operations for SEO articles
using SQLite (with future Cloudflare D1 support).
"""

import json
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path

from pydantic import BaseModel


class Article(BaseModel):
    """Article model for database operations."""

    id: Optional[int] = None
    title: str
    content: str
    keywords: List[str] = []
    meta_description: Optional[str] = None
    status: str = "draft"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ArticleDatabase:
    """Database manager for article operations."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize database connection.

        Args:
            config: Configuration dictionary containing database settings.
        """
        self.config = config
        db_config = config.get("database", {})
        self.db_url = db_config.get("url", "./data/articles.db")

        db_path = Path(self.db_url)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        self._init_database()

    def _init_database(self) -> None:
        """Initialize database schema."""
        with sqlite3.connect(self.db_url) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    keywords TEXT,
                    meta_description TEXT,
                    status TEXT DEFAULT 'draft',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def create_article(self, article: Article) -> Article:
        """Create a new article.

        Args:
            article: Article data to create.

        Returns:
            Created article with ID assigned.
        """
        with sqlite3.connect(self.db_url) as conn:
            cursor = conn.execute(
                """
                INSERT INTO articles (title, content, keywords, meta_description, status)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    article.title,
                    article.content,
                    json.dumps(article.keywords),
                    article.meta_description,
                    article.status,
                ),
            )
            article_id = cursor.lastrowid
            conn.commit()

        if article_id is None:
            raise ValueError("Failed to create article - no ID returned")

        result = self.get_article(article_id)
        if result is None:
            raise ValueError("Failed to retrieve created article")

        return result

    def get_article(self, article_id: int) -> Optional[Article]:
        """Get article by ID.

        Args:
            article_id: ID of the article to retrieve.

        Returns:
            Article if found, None otherwise.
        """
        with sqlite3.connect(self.db_url) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT * FROM articles WHERE id = ?
            """,
                (article_id,),
            )
            row = cursor.fetchone()

        if not row:
            return None

        return Article(
            id=row["id"],
            title=row["title"],
            content=row["content"],
            keywords=json.loads(row["keywords"] or "[]"),
            meta_description=row["meta_description"],
            status=row["status"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    def get_articles(
        self, limit: int = 100, offset: int = 0, status: Optional[str] = None
    ) -> List[Article]:
        """Get list of articles with pagination.

        Args:
            limit: Maximum number of articles to return.
            offset: Number of articles to skip.
            status: Filter by status if provided.

        Returns:
            List of articles.
        """
        with sqlite3.connect(self.db_url) as conn:
            conn.row_factory = sqlite3.Row

            if status:
                cursor = conn.execute(
                    """
                    SELECT * FROM articles WHERE status = ?
                    ORDER BY updated_at DESC LIMIT ? OFFSET ?
                """,
                    (status, limit, offset),
                )
            else:
                cursor = conn.execute(
                    """
                    SELECT * FROM articles
                    ORDER BY updated_at DESC LIMIT ? OFFSET ?
                """,
                    (limit, offset),
                )

            rows = cursor.fetchall()

        articles = []
        for row in rows:
            articles.append(
                Article(
                    id=row["id"],
                    title=row["title"],
                    content=row["content"],
                    keywords=json.loads(row["keywords"] or "[]"),
                    meta_description=row["meta_description"],
                    status=row["status"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    updated_at=datetime.fromisoformat(row["updated_at"]),
                )
            )

        return articles

    def update_article(self, article_id: int, article: Article) -> Optional[Article]:
        """Update an existing article.

        Args:
            article_id: ID of the article to update.
            article: Updated article data.

        Returns:
            Updated article if found, None otherwise.
        """
        with sqlite3.connect(self.db_url) as conn:
            cursor = conn.execute(
                """
                UPDATE articles 
                SET title = ?, content = ?, keywords = ?, meta_description = ?, 
                    status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """,
                (
                    article.title,
                    article.content,
                    json.dumps(article.keywords),
                    article.meta_description,
                    article.status,
                    article_id,
                ),
            )

            if cursor.rowcount == 0:
                return None

            conn.commit()

        return self.get_article(article_id)

    def delete_article(self, article_id: int) -> bool:
        """Delete an article.

        Args:
            article_id: ID of the article to delete.

        Returns:
            True if article was deleted, False if not found.
        """
        with sqlite3.connect(self.db_url) as conn:
            cursor = conn.execute("DELETE FROM articles WHERE id = ?", (article_id,))
            deleted = cursor.rowcount > 0
            conn.commit()

        return deleted

    def search_articles(self, query: str, limit: int = 50) -> List[Article]:
        """Search articles by title or content.

        Args:
            query: Search query string.
            limit: Maximum number of results to return.

        Returns:
            List of matching articles.
        """
        with sqlite3.connect(self.db_url) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT * FROM articles 
                WHERE title LIKE ? OR content LIKE ?
                ORDER BY updated_at DESC LIMIT ?
            """,
                (f"%{query}%", f"%{query}%", limit),
            )

            rows = cursor.fetchall()

        articles = []
        for row in rows:
            articles.append(
                Article(
                    id=row["id"],
                    title=row["title"],
                    content=row["content"],
                    keywords=json.loads(row["keywords"] or "[]"),
                    meta_description=row["meta_description"],
                    status=row["status"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    updated_at=datetime.fromisoformat(row["updated_at"]),
                )
            )

        return articles
