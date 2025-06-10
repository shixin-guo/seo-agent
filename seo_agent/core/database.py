"""Database models and connection layer for article and image storage.

This module provides database connectivity and CRUD operations for SEO articles
and images using SQLite (with future Cloudflare D1 support).
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


class Image(BaseModel):
    """Image model for database operations."""

    id: Optional[int] = None
    filename: str
    original_name: str
    alt_text: Optional[str] = None
    file_path: str
    file_size: int
    mime_type: str
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

            conn.execute("""
                CREATE TABLE IF NOT EXISTS images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    original_name TEXT NOT NULL,
                    alt_text TEXT,
                    file_path TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    mime_type TEXT NOT NULL,
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

    def create_image(self, image: Image) -> Image:
        """Create a new image record.

        Args:
            image: Image data to create.

        Returns:
            Created image with ID assigned.
        """
        with sqlite3.connect(self.db_url) as conn:
            cursor = conn.execute(
                """
                INSERT INTO images (filename, original_name, alt_text, file_path, file_size, mime_type)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    image.filename,
                    image.original_name,
                    image.alt_text,
                    image.file_path,
                    image.file_size,
                    image.mime_type,
                ),
            )
            image_id = cursor.lastrowid
            conn.commit()

        if image_id is None:
            raise ValueError("Failed to create image - no ID returned")

        result = self.get_image(image_id)
        if result is None:
            raise ValueError("Failed to retrieve created image")

        return result

    def get_image(self, image_id: int) -> Optional[Image]:
        """Get image by ID.

        Args:
            image_id: ID of the image to retrieve.

        Returns:
            Image if found, None otherwise.
        """
        with sqlite3.connect(self.db_url) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT * FROM images WHERE id = ?
            """,
                (image_id,),
            )
            row = cursor.fetchone()

        if not row:
            return None

        return Image(
            id=row["id"],
            filename=row["filename"],
            original_name=row["original_name"],
            alt_text=row["alt_text"],
            file_path=row["file_path"],
            file_size=row["file_size"],
            mime_type=row["mime_type"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    def get_images(self, limit: int = 100, offset: int = 0) -> List[Image]:
        """Get list of images with pagination.

        Args:
            limit: Maximum number of images to return.
            offset: Number of images to skip.

        Returns:
            List of images.
        """
        with sqlite3.connect(self.db_url) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT * FROM images
                ORDER BY created_at DESC LIMIT ? OFFSET ?
            """,
                (limit, offset),
            )

            rows = cursor.fetchall()

        images = []
        for row in rows:
            images.append(
                Image(
                    id=row["id"],
                    filename=row["filename"],
                    original_name=row["original_name"],
                    alt_text=row["alt_text"],
                    file_path=row["file_path"],
                    file_size=row["file_size"],
                    mime_type=row["mime_type"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    updated_at=datetime.fromisoformat(row["updated_at"]),
                )
            )

        return images

    def update_image_alt_text(self, image_id: int, alt_text: str) -> Optional[Image]:
        """Update alt text for an image.

        Args:
            image_id: ID of the image to update.
            alt_text: New alt text.

        Returns:
            Updated image if found, None otherwise.
        """
        with sqlite3.connect(self.db_url) as conn:
            cursor = conn.execute(
                """
                UPDATE images 
                SET alt_text = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """,
                (alt_text, image_id),
            )

            if cursor.rowcount == 0:
                return None

            conn.commit()

        return self.get_image(image_id)

    def delete_image(self, image_id: int) -> bool:
        """Delete an image record.

        Args:
            image_id: ID of the image to delete.

        Returns:
            True if image was deleted, False if not found.
        """
        with sqlite3.connect(self.db_url) as conn:
            cursor = conn.execute("DELETE FROM images WHERE id = ?", (image_id,))
            deleted = cursor.rowcount > 0
            conn.commit()

        return deleted

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
