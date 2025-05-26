"""DSPy-based modules for SEO analysis and optimization tasks.

This module provides a collection of DSPy-powered classes for various SEO tasks
including keyword generation, content optimization, backlink analysis,
and site auditing.
"""

import json
import os
import logging
from typing import Any, Optional, List, Dict, TypedDict, Protocol, cast

import dspy
from dspy.clients.lm import LM

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("seo_agent")


# Define typed structures for keyword data
class KeywordData(TypedDict):
    """Type definition for keyword data structure."""

    keyword: str
    intent: str  # informational, commercial, transactional, or navigational
    competition: str  # low, medium, or high


# Define protocol for DSPy output that contains keywords
class KeywordResearchOutput(Protocol):
    """Protocol defining the structure of keyword research output from DSPy."""

    keywords: str | List[KeywordData]


class KeywordGenerator(dspy.Module):
    """A module for generating SEO keyword ideas using language models.

    Uses DSPy to interface with LLMs for generating keyword suggestions based on
    seed keywords and industry context.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
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

        if not api_key:
            logger.error("No OpenAI API key found in environment variables or config!")
            logger.warning(
                "Set OPENAI_API_KEY environment variable or add 'openai_key' to config.yaml"
            )
            raise ValueError(
                "OpenAI API key is required for KeywordGenerator. Add it to .env file or config."
            )

        if api_key:
            logger.info(f"Configuring DSPy with model: {self.model_name}")
            dspy.settings.configure(lm=LM(model=self.model_name, api_key=api_key))

    def generate_keywords(
        self, seed_keyword: str, industry: Optional[str] = None
    ) -> List[KeywordData]:
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

        logger.info(
            f"Generating keywords for seed: '{seed_keyword}', industry: '{industry or 'general'}'"
        )

        try:
            # Execute prediction
            dspy_result = cast(
                KeywordResearchOutput,
                keyword_predictor(
                    seed_keyword=seed_keyword, industry=industry or "general"
                ),
            )

            # Process and format results
            if isinstance(dspy_result.keywords, str):
                try:
                    # Try to clean and parse the JSON response
                    json_str = dspy_result.keywords
                    # Replace single quotes with double quotes
                    json_str = json_str.replace("'", '"')
                    # Remove any markdown code block markers
                    json_str = json_str.replace("```json", "").replace("```", "")
                    json_str = json_str.strip()

                    logger.debug(f"Received raw JSON response: {json_str[:100]}...")

                    # If the string starts with a bracket but isn't a complete array, wrap it
                    if not (json_str.startswith("[") and json_str.endswith("]")):
                        if json_str.startswith("["):
                            json_str = json_str + "]"
                            logger.warning(
                                "Had to add closing bracket to JSON response"
                            )
                        elif json_str.endswith("]"):
                            json_str = "[" + json_str
                            logger.warning(
                                "Had to add opening bracket to JSON response"
                            )
                        else:
                            json_str = "[" + json_str + "]"
                            logger.warning("Had to wrap JSON response in brackets")

                    parsed_keywords: List[KeywordData] = json.loads(json_str)
                    logger.info(
                        f"Successfully parsed {len(parsed_keywords)} keywords from API response"
                    )
                    return parsed_keywords

                except json.JSONDecodeError as e:
                    # Log detailed error info and raise error
                    logger.error(f"JSON decode error: {str(e)}")
                    logger.error(f"Problematic JSON: {json_str[:500]}...")
                    logger.error("Failed to parse keywords from API response")
                    raise ValueError(
                        f"Failed to parse keyword data from API response: {str(e)}"
                    )

            # Ensure the returned value is the correct type
            if isinstance(dspy_result.keywords, list):
                logger.info(
                    f"Got {len(dspy_result.keywords)} keywords directly as list object"
                )
                return cast(List[KeywordData], dspy_result.keywords)

            logger.error(f"Unexpected response type: {type(dspy_result.keywords)}")
            raise TypeError(
                f"Expected list or JSON string, got {type(dspy_result.keywords)}"
            )

        except Exception as e:
            logger.error(f"Error generating keywords: {str(e)}")
            # Re-raise the exception
            raise


# Define type structures for other modules
class OptimizationResult(TypedDict):
    """Type definition for content optimization results."""

    optimized_content: str
    suggestions: List[str]
    keyword_density: Dict[str, float]


class BacklinkAnalysisResult(TypedDict):
    """Type definition for backlink analysis results."""

    domain: str
    opportunities: List[Dict[str, Any]]
    competitor_analysis: Dict[str, Any]


class SiteAuditResult(TypedDict):
    """Type definition for site audit results."""

    domain: str
    pages_analyzed: int
    issues: List[Dict[str, Any]]
    recommendations: List[str]


class ContentOptimizer(dspy.Module):
    """A module for optimizing content for SEO using language models.

    Provides content optimization suggestions based on target keywords
    and SEO best practices.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
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
        self, content: str, target_keywords: List[str]
    ) -> OptimizationResult:
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

    def __init__(self, config: Dict[str, Any]) -> None:
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
        self, domain: str, competitors: Optional[List[str]] = None
    ) -> BacklinkAnalysisResult:
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

    def __init__(self, config: Dict[str, Any]) -> None:
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

    def audit_site(self, domain: str, max_pages: int = 50) -> SiteAuditResult:
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


# Define protocol for content generation output
class ContentOptimizationOutput(Protocol):
    """Protocol defining the structure of content optimization output from DSPy."""

    optimized_content: Optional[str]


class AIContentGenerator(dspy.Module):
    """A module for generating optimized content using language models.

    Uses DSPy to interface with LLMs for creating SEO-friendly content based on
    original content and optimization instructions.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
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
            lm_config: Dict[str, Any] = {
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
        dspy_result = cast(
            ContentOptimizationOutput,
            content_optimizer(
                original_content=original_content, optimization_guidelines=instructions
            ),
        )

        # Return the optimized content
        if hasattr(dspy_result, "optimized_content") and dspy_result.optimized_content:
            optimized = dspy_result.optimized_content
            if isinstance(optimized, str):
                return optimized
            return original_content  # Return original if wrong type

        # Fallback to original content if optimization fails
        return original_content
