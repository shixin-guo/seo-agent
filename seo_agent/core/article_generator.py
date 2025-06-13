"""Article generation service that integrates with existing SEO tools.

This module provides functionality to generate SEO-optimized articles
using keyword research and content optimization capabilities.
"""

import tempfile
from typing import Any, Dict, List, Optional

from .advanced_content_optimizer import AdvancedContentOptimizer
from .keyword_engine import KeywordEngine
from .database import Article


class ArticleGenerator:
    """Service for generating SEO-optimized articles from keywords."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the article generator.

        Args:
            config: Configuration dictionary containing API keys and settings.
        """
        self.config = config
        self.keyword_engine = KeywordEngine(config)
        self.content_optimizer = AdvancedContentOptimizer(config)

    def generate_article_from_keywords(
        self,
        seed_keyword: str,
        industry: Optional[str] = None,
        title: Optional[str] = None,
        min_length: int = 800,
    ) -> Article:
        """Generate a complete SEO article from a seed keyword.

        Args:
            seed_keyword: The main keyword to build the article around.
            industry: Optional industry context for better targeting.
            title: Optional custom title, otherwise generated from keyword.
            min_length: Minimum word count for the article.

        Returns:
            Generated article with SEO optimization.
        """
        keyword_data = self.keyword_engine.generate_keywords(seed_keyword, industry)
        keywords = [kw["keyword"] for kw in keyword_data["keywords"][:10]]

        article_title = title or self._generate_title(seed_keyword, industry)
        initial_content = self._create_initial_content(
            article_title, seed_keyword, keywords, industry, min_length
        )

        optimized_content = self._optimize_content(initial_content, keywords)

        meta_description = self._generate_meta_description(
            article_title, seed_keyword, optimized_content
        )

        return Article(
            title=article_title,
            content=optimized_content,
            keywords=keywords,
            meta_description=meta_description,
            status="draft",
        )

    def regenerate_article_with_new_keywords(
        self, existing_article: Article, new_keywords: List[str]
    ) -> Article:
        """Regenerate an existing article with new keywords.

        Args:
            existing_article: The article to update.
            new_keywords: New keywords to incorporate.

        Returns:
            Updated article with new keywords integrated.
        """
        all_keywords = list(set(existing_article.keywords + new_keywords))

        optimized_content = self._optimize_content(
            existing_article.content, all_keywords
        )

        meta_description = self._generate_meta_description(
            existing_article.title, all_keywords[0], optimized_content
        )

        return Article(
            id=existing_article.id,
            title=existing_article.title,
            content=optimized_content,
            keywords=all_keywords,
            meta_description=meta_description,
            status=existing_article.status,
            created_at=existing_article.created_at,
        )

    def _generate_title(self, seed_keyword: str, industry: Optional[str]) -> str:
        """Generate an SEO-friendly title from the seed keyword.

        Args:
            seed_keyword: Main keyword for the article.
            industry: Optional industry context.

        Returns:
            Generated title string.
        """
        title_templates = [
            f"The Complete Guide to {seed_keyword.title()}",
            f"How to Master {seed_keyword.title()}: A Comprehensive Guide",
            f"{seed_keyword.title()}: Everything You Need to Know",
            f"Ultimate {seed_keyword.title()} Guide for Beginners",
            f"Advanced {seed_keyword.title()} Strategies That Work",
        ]

        if industry:
            title_templates.extend(
                [
                    f"{seed_keyword.title()} in {industry.title()}: Best Practices",
                    f"How {industry.title()} Professionals Use {seed_keyword.title()}",
                ]
            )

        title_index = hash(seed_keyword + (industry or "")) % len(title_templates)
        return title_templates[title_index]

    def _create_initial_content(
        self,
        title: str,
        seed_keyword: str,
        keywords: List[str],
        industry: Optional[str],
        min_length: int,
    ) -> str:
        """Create initial content structure.

        Args:
            title: Article title.
            seed_keyword: Main keyword.
            keywords: List of related keywords.
            industry: Optional industry context.
            min_length: Minimum word count target.

        Returns:
            Initial content string.
        """
        content_sections = [
            f"# {title}",
            "",
            "## Introduction",
            f"In today's competitive landscape, understanding {seed_keyword} is crucial for success.",
            f"This comprehensive guide will explore everything you need to know about {seed_keyword}.",
            "",
            f"## What is {seed_keyword.title()}?",
            f"{seed_keyword.title()} refers to the practice and strategies involved in optimizing your approach.",
            "Understanding the fundamentals is the first step toward mastery.",
            "",
            f"## Key Benefits of {seed_keyword.title()}",
            f"Implementing effective {seed_keyword} strategies can provide numerous advantages:",
            "- Improved performance and results",
            "- Better resource utilization",
            "- Enhanced competitive positioning",
            "- Increased efficiency and effectiveness",
            "",
            f"## Best Practices for {seed_keyword.title()}",
            f"To maximize your {seed_keyword} efforts, consider these proven strategies:",
        ]

        for i, keyword in enumerate(keywords[:5]):
            content_sections.extend(
                [
                    f"### {keyword.title()}",
                    f"When implementing {keyword}, it's important to consider the specific requirements and context.",
                    f"This approach to {keyword} can significantly impact your overall {seed_keyword} strategy.",
                    "",
                ]
            )

        content_sections.extend(
            [
                "## Common Challenges and Solutions",
                f"While working with {seed_keyword}, you may encounter various challenges.",
                "Here are some common issues and their solutions:",
                "",
                "## Conclusion",
                f"Mastering {seed_keyword} requires dedication, practice, and continuous learning.",
                f"By following the strategies outlined in this guide, you'll be well-equipped to succeed with {seed_keyword}.",
                "",
            ]
        )

        initial_content = "\n".join(content_sections)

        word_count = len(initial_content.split())
        if word_count < min_length:
            additional_sections = [
                f"## Advanced {seed_keyword.title()} Techniques",
                f"For those looking to take their {seed_keyword} skills to the next level, these advanced techniques can provide significant advantages.",
                "",
                "## Tools and Resources",
                f"Having the right tools can make a significant difference in your {seed_keyword} success.",
                "Consider these recommended resources and platforms.",
                "",
                f"## Future Trends in {seed_keyword.title()}",
                f"The landscape of {seed_keyword} continues to evolve rapidly.",
                "Staying ahead of trends is crucial for long-term success.",
                "",
            ]
            initial_content += "\n" + "\n".join(additional_sections)

        return initial_content

    def _optimize_content(self, content: str, keywords: List[str]) -> str:
        """Optimize content using the advanced content optimizer.

        Args:
            content: Initial content to optimize.
            keywords: Keywords to incorporate.

        Returns:
            Optimized content string.
        """
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False
            ) as content_file:
                content_file.write(content)
                content_file_path = content_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            ) as keywords_file:
                keywords_data = {
                    "keywords": [
                        {
                            "keyword": kw,
                            "intent": "informational",
                            "competition": "medium",
                        }
                        for kw in keywords
                    ]
                }
                import json

                json.dump(keywords_data, keywords_file)
                keywords_file_path = keywords_file.name

            optimized_content = self.content_optimizer.fully_optimize_content(
                content_file_path, keywords_file_path
            )

            import os

            os.unlink(content_file_path)
            os.unlink(keywords_file_path)

            return optimized_content

        except Exception as e:
            print(f"Content optimization failed: {e}")
            return content

    def _generate_meta_description(
        self, title: str, main_keyword: str, content: str
    ) -> str:
        """Generate SEO meta description.

        Args:
            title: Article title.
            main_keyword: Primary keyword.
            content: Article content.

        Returns:
            Meta description string (max 160 characters).
        """
        lines = content.split("\n")
        description_text = ""

        for line in lines:
            if line.strip() and not line.startswith("#") and len(line.strip()) > 20:
                description_text = line.strip()
                break

        if not description_text:
            description_text = f"Learn everything about {main_keyword} with our comprehensive guide. Discover best practices, strategies, and expert tips."

        if main_keyword.lower() not in description_text.lower():
            description_text = f"{main_keyword.title()}: {description_text}"

        if len(description_text) > 160:
            description_text = description_text[:157] + "..."

        return description_text
