import os

# json is imported in optimize_content when needed
from typing import Any, Optional


class ContentOptimizer:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def optimize_content(
        self, content_file: str, keywords: Optional[str] = None
    ) -> dict[str, Any]:
        """Optimize content for SEO"""
        # Read content file
        with open(content_file, "r") as f:
            content = f.read()

        # Load keywords if provided
        keyword_list = []
        if keywords and os.path.exists(keywords):
            import json

            with open(keywords, "r") as f:
                keyword_data = json.load(f)
                if "keywords" in keyword_data:
                    keyword_list = [
                        kw.get("keyword") for kw in keyword_data["keywords"]
                    ]

        # Perform content analysis (placeholder implementation)
        analysis = self._analyze_content(content, keyword_list)

        # Generate optimization suggestions
        suggestions = self._generate_suggestions(content, analysis)

        # Create optimized version
        optimized_content = self._apply_suggestions(content, suggestions)

        # Prepare result
        result = {
            "original_content": content,
            "optimized_content": optimized_content,
            "analysis": analysis,
            "suggestions": suggestions,
        }

        return result

    def _analyze_content(self, content: str, keywords: list[str]) -> dict[str, Any]:
        """Analyze content for SEO factors"""
        """Analyze content for SEO factors"""
        # Calculate word count
        words = content.split()
        word_count = len(words)

        # Calculate keyword density
        keyword_density = {}
        if keywords:
            content_lower = content.lower()
            for keyword in keywords:
                if not keyword:
                    continue
                keyword_lower = keyword.lower()
                # Count occurrences
                count = content_lower.count(keyword_lower)
                if count > 0:
                    density = (
                        (count * len(keyword_lower.split())) / max(1, word_count) * 100
                    )
                    keyword_density[keyword] = {
                        "count": count,
                        "density": round(density, 2),
                    }

        # Simple readability estimate based on word length
        avg_word_length = sum(len(word) for word in words) / max(1, word_count)
        if avg_word_length > 7:
            readability = "complex"
        elif avg_word_length > 5:
            readability = "medium"
        else:
            readability = "simple"

        # Count headings (markdown style)
        heading_count = 0
        for line in content.split("\n"):
            if line.strip().startswith("#"):
                heading_count += 1

        return {
            "word_count": word_count,
            "keyword_density": keyword_density,
            "readability": readability,
            "headings": heading_count,
            "meta_tags": {},
            "avg_word_length": round(avg_word_length, 2),
        }

    def _generate_suggestions(
        self, content: str, analysis: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Generate optimization suggestions"""
        suggestions = []

        # Check word count
        word_count = analysis.get("word_count", 0)
        if word_count < 300:
            suggestions.append(
                {
                    "type": "length",
                    "suggestion": f"Content is too short ({word_count} words). Aim for at least 300 words for better SEO.",
                }
            )

        # Check headings
        heading_count = analysis.get("headings", 0)
        if heading_count == 0:
            suggestions.append(
                {
                    "type": "heading",
                    "suggestion": "Add headings (using # in markdown) to structure your content and improve readability.",
                }
            )
        elif word_count > 300 and heading_count < 2:
            suggestions.append(
                {
                    "type": "heading",
                    "suggestion": f"Add more headings. For {word_count} words, aim for at least 3-4 headings.",
                }
            )

        # Check keyword usage
        keyword_density = analysis.get("keyword_density", {})
        if not keyword_density:
            suggestions.append(
                {
                    "type": "keyword",
                    "suggestion": "No target keywords found in content. Include relevant keywords to improve SEO.",
                }
            )
        else:
            # Suggest optimization for low-density keywords
            low_density_keywords = []
            for keyword, data in keyword_density.items():
                if data.get("density", 0) < 0.5:
                    low_density_keywords.append(keyword)

            if low_density_keywords:
                suggestions.append(
                    {
                        "type": "keyword",
                        "suggestion": f"Increase usage of these keywords: {', '.join(low_density_keywords[:3])}",
                    }
                )

            # Check for overly dense keywords
            high_density_keywords = []
            for keyword, data in keyword_density.items():
                if data.get("density", 0) > 5.0:
                    high_density_keywords.append(keyword)

            if high_density_keywords:
                suggestions.append(
                    {
                        "type": "keyword_stuffing",
                        "suggestion": f"Keyword stuffing detected. Reduce usage of: {', '.join(high_density_keywords)}",
                    }
                )

        # Readability suggestions
        readability = analysis.get("readability", "medium")
        if readability == "complex":
            suggestions.append(
                {
                    "type": "readability",
                    "suggestion": "Content is complex. Consider simplifying language for better readability.",
                }
            )

        return suggestions

    def _apply_suggestions(
        self, content: str, suggestions: list[dict[str, Any]]
    ) -> str:
        """Apply suggestions to create optimized content"""
        # Note: This is a simplified implementation.
        # In a real-world scenario, you would integrate with a language model like GPT
        # to intelligently rewrite content based on suggestions.

        # If there are no suggestions, the content is already optimized
        if not suggestions:
            return content

        # For now, we'll just add optimization notes at the top of the content
        optimization_notes = []
        optimization_notes.append("# SEO OPTIMIZATION NOTES")
        optimization_notes.append(
            "The following suggestions should be applied to improve SEO:"
        )

        for idx, suggestion in enumerate(suggestions, 1):
            suggestion_type = suggestion.get("type", "general")
            suggestion_text = suggestion.get("suggestion", "")
            optimization_notes.append(
                f"{idx}. [{suggestion_type.upper()}] {suggestion_text}"
            )

        # Only include the notes if there are suggestions
        if suggestions:
            return "\n".join(optimization_notes)
        else:
            return content
