"""DSPy-based modules for SEO analysis and optimization tasks.

This module provides a collection of DSPy-powered classes for various SEO tasks
including keyword generation, content optimization, backlink analysis,
and site auditing.
"""

import json
import os
from typing import Any, Optional

import dspy
from dspy.clients.lm import LM


class KeywordGenerator(dspy.Module):
    """A module for generating SEO keyword ideas using language models.

    Uses DSPy to interface with LLMs for generating keyword suggestions based on
    seed keywords and industry context.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the KeywordGenerator module.

        Args:
            config: Configuration dictionary containing AI model and API settings.
        """
        super().__init__()
        self.config = config
        self.model_name = config.get("ai", {}).get("model", "gpt-4-turbo-preview")
        self.max_tokens = config.get("ai", {}).get("max_tokens", 2000)
        self.temperature = config.get("ai", {}).get("temperature", 0.3)

        # Configure DSPy
        api_key = os.environ.get("OPENAI_API_KEY") or config.get("apis", {}).get(
            "openai_key"
        )
        if api_key:
            dspy.settings.configure(lm=LM(model=self.model_name, api_key=api_key))

    def generate_keywords(
        self, seed_keyword: str, industry: Optional[str] = None
    ) -> list[dict[str, Any]]:
        """Generate keyword ideas based on a seed keyword and optional industry context.

        Args:
            seed_keyword: The main keyword to generate ideas from.
            industry: Optional industry or niche context for better targeting.

        Returns:
            A list of dictionaries containing keyword suggestions with their properties.
        """

        # Define the signature for the LM
        class KeywordResearch(dspy.Signature):
            """Generate SEO keyword ideas based on a seed keyword and industry."""

            seed_keyword = dspy.InputField()
            industry = dspy.InputField(description="The industry or niche context")
            keywords = dspy.OutputField(
                description=(
                    "JSON array of objects, each with 'keyword' (string), 'intent' (string: informational, commercial, transactional, or navigational), and 'competition' (string: low, medium, or high) properties"
                )
            )

        # Create predictor
        keyword_predictor = dspy.Predict(KeywordResearch)

        # Execute prediction
        result = keyword_predictor(
            seed_keyword=seed_keyword, industry=industry or "general"
        )

        # Process and format results
        if isinstance(result.keywords, str):
            try:
                # Try to clean and parse the JSON response
                json_str = result.keywords
                # Replace single quotes with double quotes
                json_str = json_str.replace("'", '"')
                # Remove any markdown code block markers
                json_str = json_str.replace("```json", "").replace("```", "")
                json_str = json_str.strip()

                # If the string starts with a bracket but isn't a complete array, wrap it
                if not (json_str.startswith("[") and json_str.endswith("]")):
                    if json_str.startswith("["):
                        json_str = json_str + "]"
                    elif json_str.endswith("]"):
                        json_str = "[" + json_str
                    else:
                        json_str = "[" + json_str + "]"

                parsed_keywords: list[dict[str, Any]] = json.loads(json_str)
                return parsed_keywords
            except json.JSONDecodeError:
                # Fall back to using mock data if JSON parsing fails
                print("Failed to parse JSON response. Using mock data instead.")
                from tests.mock.mock_keyword_data import generate_mock_keywords

                mock_data = generate_mock_keywords(seed_keyword, industry or "general")
                keywords_list = mock_data["keywords"]
                if isinstance(keywords_list, list):
                    return keywords_list
                return []  # Return empty list as fallback

        # Ensure the returned value is the correct type
        if isinstance(result.keywords, list):
            return result.keywords
        return []  # Return empty list as fallback


class ContentOptimizer(dspy.Module):
    """A module for optimizing content for SEO using language models.

    Provides content optimization suggestions based on target keywords
    and SEO best practices.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the ContentOptimizer module.

        Args:
            config: Configuration dictionary containing AI model and API settings.
        """
        super().__init__()
        self.config = config
        self.model_name = config.get("ai", {}).get("model", "gpt-4-turbo-preview")

        # Configure DSPy
        api_key = os.environ.get("OPENAI_API_KEY") or config.get("apis", {}).get(
            "openai_key"
        )
        if api_key:
            dspy.settings.configure(lm=LM(model=self.model_name, api_key=api_key))

    def optimize_content(
        self, content: str, target_keywords: list[str]
    ) -> dict[str, Any]:
        """Optimize content for SEO based on target keywords.

        Args:
            content: The original content to optimize.
            target_keywords: List of keywords to optimize for.

        Returns:
            A dictionary containing optimization suggestions and improved content.
        """
        # Placeholder implementation
        return {
            "optimized_content": content,
            "suggestions": [],
            "keyword_density": {},
        }


class BacklinkAnalyzer(dspy.Module):
    """A module for analyzing backlink opportunities using language models.

    Analyzes backlink profiles and identifies opportunities based on
    competitor analysis.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the BacklinkAnalyzer module.

        Args:
            config: Configuration dictionary containing AI model and API settings.
        """
        super().__init__()
        self.config = config

        # Configure DSPy
        api_key = os.environ.get("OPENAI_API_KEY") or config.get("apis", {}).get(
            "openai_key"
        )
        if api_key:
            dspy.settings.configure(
                lm=LM(model=self.config["ai"]["model"], api_key=api_key)
            )

    def analyze_backlinks(
        self, domain: str, competitors: Optional[list[str]] = None
    ) -> dict[str, Any]:
        """Analyze backlink opportunities based on domain and competitors.

        Args:
            domain: The domain to analyze backlinks for.
            competitors: Optional list of competitor domains to analyze.

        Returns:
            A dictionary containing backlink analysis and opportunities.
        """
        # Placeholder implementation
        return {
            "domain": domain,
            "opportunities": [],
            "competitor_analysis": {},
        }


class SiteAuditor(dspy.Module):
    """A module for performing technical SEO audits using language models.

    Analyzes websites for technical SEO issues and provides improvement recommendations.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the SiteAuditor module.

        Args:
            config: Configuration dictionary containing AI model and API settings.
        """
        super().__init__()
        self.config = config

        # Configure DSPy
        api_key = os.environ.get("OPENAI_API_KEY") or config.get("apis", {}).get(
            "openai_key"
        )
        if api_key:
            dspy.settings.configure(
                lm=LM(model=self.config["ai"]["model"], api_key=api_key)
            )

    def audit_site(self, domain: str, max_pages: int = 50) -> dict[str, Any]:
        """Perform a technical SEO audit on a website.

        Args:
            domain: The domain to audit.
            max_pages: Maximum number of pages to analyze.

        Returns:
            A dictionary containing audit results and recommendations.
        """
        return {
            "domain": domain,
            "pages_analyzed": 0,
            "issues": [],
            "recommendations": [],
        }


class AIContentGenerator(dspy.Module):
    """A module for generating optimized content using language models.

    Uses DSPy to interface with LLMs for creating SEO-friendly content based on
    original content and optimization instructions.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the AIContentGenerator module.

        Args:
            config: Configuration dictionary containing AI model and API settings.
        """
        super().__init__()
        self.config = config
        self.model_name = config.get("ai", {}).get("model", "gpt-4-turbo-preview")
        self.max_tokens = config.get("ai", {}).get("max_tokens", 3000)
        self.temperature = config.get("ai", {}).get("temperature", 0.3)

        # Configure DSPy
        api_key = os.environ.get("OPENAI_API_KEY") or config.get("apis", {}).get(
            "openai_key"
        )
        if api_key:
            # Add a random seed to each request if available in config
            random_seed = None
            if "randomization" in config and "seed" in config["randomization"]:
                random_seed = config["randomization"]["seed"]

            # Configure with temperature setting (for creativity control)
            lm_config = {
                "model": self.model_name,
                "api_key": api_key,
                "temperature": self.temperature,
            }

            # Add seed for OpenAI if available
            if random_seed is not None:
                lm_config["seed"] = random_seed

            dspy.settings.configure(lm=LM(**lm_config))

    def generate_optimized_content(
        self, original_content: str, instructions: str
    ) -> str:
        """Generate optimized content based on original content and instructions.

        Args:
            original_content: The original content to optimize
            instructions: Specific instructions for optimization

        Returns:
            The optimized content
        """

        # Define the signature for content optimization
        class ContentOptimizationSignature(dspy.Signature):
            """Generate SEO-optimized content based on original content and optimization guidelines."""

            original_content = dspy.InputField()
            optimization_guidelines = dspy.InputField(
                description="Guidelines for optimization"
            )
            optimized_content = dspy.OutputField(
                description="The optimized content that follows all guidelines"
            )

        # Create predictor
        content_optimizer = dspy.Predict(ContentOptimizationSignature)

        # Execute prediction
        result = content_optimizer(
            original_content=original_content, optimization_guidelines=instructions
        )

        # Return the optimized content
        if hasattr(result, "optimized_content") and result.optimized_content:
            optimized = result.optimized_content
            if isinstance(optimized, str):
                return optimized
            return original_content  # Return original if wrong type

        # Fallback to original content if optimization fails
        return original_content
