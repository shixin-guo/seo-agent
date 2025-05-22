"""Advanced content optimizer using AI to rewrite and optimize content for SEO.

This module extends the basic ContentOptimizer with more sophisticated
optimization capabilities using DSPy and language models.
"""

import json
import re
from typing import Any, Dict, List, Optional, Tuple, TypedDict

from .content_optimizer import ContentOptimizer
from .dspy_modules import AIContentGenerator


class KeywordData(TypedDict):
    """Type definition for keyword metadata."""

    intent: str
    competition: str
    count: int
    priority: int


class AdvancedContentOptimizer:
    """Advanced content optimizer using AI for comprehensive content optimization."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the advanced content optimizer.

        Args:
            config: Configuration dictionary containing API keys and settings.
        """
        self.config = config
        self.basic_optimizer = ContentOptimizer(config)
        self.ai_generator = AIContentGenerator(config)

    def fully_optimize_content(
        self, content_file: str, keywords_file: str, output_file: Optional[str] = None
    ) -> str:
        """Perform a full optimization cycle on the content.

        This method:
        1. Analyzes the original content
        2. Extracts keywords from the keywords file
        3. Uses AI to rewrite content with proper structure and keywords
        4. Validates the optimized content
        5. Makes final adjustments if needed
        6. Returns the optimized content (and optionally saves to file)

        Args:
            content_file: Path to the original content file
            keywords_file: Path to the keywords JSON file
            output_file: Optional path to save the optimized content

        Returns:
            The optimized content as a string
        """
        # Step 1: Read and analyze the original content
        with open(content_file, "r") as f:
            original_content = f.read()

        # Step 2: Extract keywords from the keywords file
        target_keywords = self._extract_keywords(keywords_file)

        # Step 3: Get initial analysis of the original content
        initial_analysis = self.basic_optimizer._analyze_content(
            original_content, target_keywords["keywords"]
        )
        initial_suggestions = self.basic_optimizer._generate_suggestions(
            original_content, initial_analysis
        )

        # Step 4: Use AI to rewrite the content if there are suggestions
        if initial_suggestions:
            # Generate optimized content using AI
            optimized_content = self._generate_optimized_content(
                original_content, target_keywords, initial_analysis, initial_suggestions
            )
        else:
            # Content is already well-optimized
            optimized_content = original_content

        # Step 5: Re-analyze the optimized content
        optimized_analysis = self.basic_optimizer._analyze_content(
            optimized_content, target_keywords["keywords"]
        )
        optimized_suggestions = self.basic_optimizer._generate_suggestions(
            optimized_content, optimized_analysis
        )

        # Step 6: Make final adjustments if needed
        if optimized_suggestions:
            final_content = self._make_final_adjustments(
                optimized_content, optimized_suggestions, target_keywords
            )
        else:
            final_content = optimized_content

        # Step 7: Save to output file if provided (optional)
        if output_file:
            with open(output_file, "w") as f:
                f.write(final_content)

        # Always return the optimized content as a string
        return final_content

    def _extract_keywords(self, keywords_file: str) -> Dict[str, Any]:
        """Extract keywords and metadata from the keywords JSON file.

        Args:
            keywords_file: Path to the keywords JSON file

        Returns:
            Dictionary containing keywords and metadata
        """
        with open(keywords_file, "r") as f:
            data = json.load(f)

        # Extract the actual keyword strings
        keywords: List[str] = []
        keyword_frequencies: Dict[str, KeywordData] = {}

        for kw in data.get("keywords", []):
            keyword = kw.get("keyword", "")
            if keyword:
                keywords.append(keyword)
                keyword_frequencies[keyword] = {
                    "intent": kw.get("intent", "informational"),
                    "competition": kw.get("competition", "medium"),
                    "count": 0,
                    "priority": self._calculate_keyword_priority(kw),
                }

        return {
            "seed_keyword": data.get("seed_keyword", ""),
            "industry": data.get("industry", ""),
            "keywords": keywords,
            "keyword_data": keyword_frequencies,
            "intent_groups": data.get("intent_groups", {}),
        }

    def _calculate_keyword_priority(self, keyword_data: Dict[str, Any]) -> int:
        """Calculate a priority score for a keyword based on its metadata.

        Args:
            keyword_data: Dictionary containing keyword metadata

        Returns:
            Priority score (higher is more important)
        """
        # Base priority
        priority = 5

        # Adjust based on intent
        intent = keyword_data.get("intent", "informational").lower()
        if intent == "transactional":
            priority += 3
        elif intent == "commercial":
            priority += 2

        # Adjust based on competition
        competition = keyword_data.get("competition", "medium").lower()
        if competition == "low":
            priority += 2
        elif competition == "high":
            priority -= 1

        return priority

    def _generate_optimized_content(
        self,
        original_content: str,
        target_keywords: Dict[str, Any],
        analysis: Dict[str, Any],
        suggestions: List[Dict[str, Any]],
    ) -> str:
        """Generate optimized content using AI based on original content and suggestions.

        Args:
            original_content: The original content to optimize
            target_keywords: Dictionary containing target keywords and metadata
            analysis: Analysis of the original content
            suggestions: List of suggestions for improvement

        Returns:
            The AI-generated optimized content
        """
        # If we can't use AI (no API key, etc.), fall back to basic optimization
        if not self.config.get("apis", {}).get("openai_key"):
            return self.basic_optimizer._apply_suggestions(
                original_content, suggestions
            )

        # Extract key information from suggestions
        needs_headings = any(s.get("type") == "heading" for s in suggestions)
        needs_keywords = any(s.get("type") == "keyword" for s in suggestions)
        needs_length = any(s.get("type") == "length" for s in suggestions)

        # Format keywords for the prompt
        keywords_str = ", ".join([f'"{kw}"' for kw in target_keywords["keywords"]])

        def get_priority(item: Tuple[str, KeywordData]) -> int:
            return item[1]["priority"]

        priority_keywords = sorted(
            target_keywords["keyword_data"].items(),
            key=get_priority,
            reverse=True,
        )
        priority_keywords_str = ", ".join(
            [f'"{kw[0]}"' for kw in priority_keywords[:5]]
        )

        # Create instructions for the AI
        instructions = [
            "Rewrite the following content to optimize it for SEO.",
            f"Use these target keywords: {keywords_str}",
            f"Prioritize these important keywords: {priority_keywords_str}",
            f"Main topic: {target_keywords['seed_keyword']}",
            f"Industry context: {target_keywords['industry']}",
        ]

        # Add randomization seed if available for more varied output
        if self.config.get("randomization", {}).get("seed"):
            seed = self.config["randomization"]["seed"]
            instructions.append(
                f"Use creative variation style #{seed % 10} with unique phrasing and structure."
            )

            # Vary the tone based on the seed
            tones = [
                "professional",
                "conversational",
                "educational",
                "persuasive",
                "inspiring",
            ]
            tone_index = seed % len(tones)
            instructions.append(f"Write in a {tones[tone_index]} tone.")

            # Vary the structure based on the seed
            structures = [
                "Use short paragraphs with frequent subheadings",
                "Include bullets and lists where appropriate",
                "Use quotes and examples to illustrate points",
                "Incorporate rhetorical questions to engage readers",
                "Use data points and statistics to strengthen arguments",
            ]
            structure_index = (seed // 10) % len(structures)
            instructions.append(structures[structure_index])

        if needs_headings:
            instructions.append(
                "Use proper heading structure with H1 for title and H2 for sections."
            )

        if needs_keywords:
            instructions.append(
                "Incorporate target keywords naturally throughout the content."
            )

        if needs_length:
            instructions.append(
                "Expand the content to at least 800 words for better SEO."
            )

        instructions.append(
            "Organize the content into logical sections while maintaining the key information."
        )

        # Generate the optimized content using the AI model
        return self.ai_generator.generate_optimized_content(
            original_content, "\n".join(instructions)
        )

    def _make_final_adjustments(
        self,
        content: str,
        suggestions: List[Dict[str, Any]],
        target_keywords: Dict[str, Any],
    ) -> str:
        """Make final manual adjustments to address any remaining suggestions.

        Args:
            content: The content to adjust
            suggestions: List of remaining suggestions
            target_keywords: Dictionary containing target keywords and metadata

        Returns:
            The adjusted content
        """
        adjusted_content = content

        # Address specific keyword usage suggestions
        for suggestion in suggestions:
            if suggestion["type"] == "keyword":
                suggestion_text = suggestion.get("suggestion", "")

                # Check if we need to increase usage of specific keywords
                if "Increase usage of these keywords:" in suggestion_text:
                    keywords_to_add = re.findall(
                        r"Increase usage of these keywords: (.*?)$", suggestion_text
                    )
                    if keywords_to_add:
                        keywords_list = [
                            k.strip() for k in keywords_to_add[0].split(",")
                        ]

                        # Add these keywords in appropriate places
                        for keyword in keywords_list:
                            # Find good places to add the keyword
                            adjusted_content = self._increase_keyword_usage(
                                adjusted_content, keyword
                            )

        return adjusted_content

    def _increase_keyword_usage(self, content: str, keyword: str) -> str:
        """Increase the usage of a specific keyword in the content.

        Args:
            content: The content to modify
            keyword: The keyword to increase usage of

        Returns:
            The modified content with increased keyword usage
        """
        # Split content into paragraphs
        paragraphs = content.split("\n\n")

        # Find paragraphs that don't contain the keyword
        paragraphs_without_keyword = [
            (i, p)
            for i, p in enumerate(paragraphs)
            if keyword.lower() not in p.lower()
            and not p.strip().startswith("#")
            and len(p.split()) > 20
        ]

        # Modify up to 2 paragraphs to include the keyword
        modified_count = 0
        for i, paragraph in paragraphs_without_keyword:
            if modified_count >= 2:
                break

            # Don't modify headings or short paragraphs
            if paragraph.strip().startswith("#") or len(paragraph.split()) < 20:
                continue

            # Add the keyword near the beginning of the paragraph
            sentences = paragraph.split(". ")
            if len(sentences) > 1:
                # Add to the second sentence if possible
                target_idx = min(1, len(sentences) - 1)
                sentence = sentences[target_idx]

                # Insert the keyword naturally
                modified_sentence = self._insert_keyword_in_sentence(sentence, keyword)
                sentences[target_idx] = modified_sentence

                # Reconstruct the paragraph
                paragraphs[i] = ". ".join(sentences)
                modified_count += 1

        # Join the paragraphs back together
        return "\n\n".join(paragraphs)

    def _insert_keyword_in_sentence(self, sentence: str, keyword: str) -> str:
        """Insert a keyword into a sentence in a natural way.

        Args:
            sentence: The sentence to modify
            keyword: The keyword to insert

        Returns:
            Modified sentence with the keyword included
        """
        # Common phrases to use when inserting keywords
        templates = [
            f"using {keyword}",
            f"with {keyword}",
            f"through {keyword}",
            f"leveraging {keyword}",
            f"{keyword} can help",
            f"the {keyword} approach",
        ]

        # Select a template based on the sentence
        words = sentence.split()
        if len(words) < 4:
            return f"{keyword} {sentence}"

        # Insert after a suitable position
        insertion_point = min(len(words) // 2, 5)

        # Choose a template that fits grammatically
        template = templates[hash(sentence) % len(templates)]

        # Insert the phrase
        words.insert(insertion_point, template)
        return " ".join(words)
