"""Tests for the KeywordEngine module."""

from typing import Any
from unittest.mock import MagicMock, patch

from seo_agent.core.keyword_engine import KeywordEngine

# Constants for test configuration
MAX_TEST_KEYWORDS = 3


class TestKeywordEngine:
    """Test suite for KeywordEngine class."""

    def test_init(self, sample_config: dict[str, Any]) -> None:
        """Test KeywordEngine initialization."""
        engine = KeywordEngine(sample_config)

        assert engine.config == sample_config
        assert engine.max_keywords == sample_config["defaults"]["max_keywords"]
        assert hasattr(engine, "keyword_generator")

    @patch("seo_agent.core.keyword_engine.KeywordGenerator")
    def test_generate_keywords_with_limit(
        self,
        mock_generator: MagicMock,
        sample_config: dict[str, Any],
        sample_keywords: list[dict[str, Any]],
    ) -> None:
        """Test generate_keywords with keyword limit applied."""
        # Setup
        mock_instance = mock_generator.return_value
        mock_instance.generate_keywords.return_value = sample_keywords

        # Ensure our sample config has a max_keywords less than len(sample_keywords)
        test_config = sample_config.copy()
        test_config["defaults"]["max_keywords"] = MAX_TEST_KEYWORDS

        engine = KeywordEngine(test_config)

        # Execute
        result = engine.generate_keywords("seo", "digital marketing")

        # Verify
        mock_instance.generate_keywords.assert_called_once_with(
            "seo", "digital marketing"
        )
        assert result["seed_keyword"] == "seo"
        assert result["industry"] == "digital marketing"
        assert result["total_keywords"] == MAX_TEST_KEYWORDS
        assert len(result["keywords"]) == MAX_TEST_KEYWORDS
        assert "intent_groups" in result

    @patch("seo_agent.core.keyword_engine.KeywordGenerator")
    def test_generate_keywords_without_limit(
        self,
        mock_generator: MagicMock,
        sample_config: dict[str, Any],
        sample_keywords: list[dict[str, Any]],
    ) -> None:
        """Test generate_keywords without hitting the keyword limit."""
        # Setup
        mock_instance = mock_generator.return_value
        mock_instance.generate_keywords.return_value = sample_keywords

        # Ensure our sample config has a max_keywords more than len(sample_keywords)
        test_config = sample_config.copy()
        test_config["defaults"]["max_keywords"] = 100

        engine = KeywordEngine(test_config)

        # Execute
        result = engine.generate_keywords("seo", "digital marketing")

        # Verify
        assert result["total_keywords"] == len(sample_keywords)
        assert len(result["keywords"]) == len(sample_keywords)

    @patch("seo_agent.core.keyword_engine.KeywordGenerator")
    def test_generate_keywords_without_industry(
        self,
        mock_generator: MagicMock,
        sample_config: dict[str, Any],
        sample_keywords: list[dict[str, Any]],
    ) -> None:
        """Test generate_keywords with no industry specified."""
        # Setup
        mock_instance = mock_generator.return_value
        mock_instance.generate_keywords.return_value = sample_keywords

        engine = KeywordEngine(sample_config)

        # Execute
        result = engine.generate_keywords("seo")

        # Verify
        mock_instance.generate_keywords.assert_called_once_with("seo", None)
        assert result["industry"] == "Not specified"

    @patch("seo_agent.core.keyword_engine.KeywordGenerator")
    def test_intent_grouping(
        self,
        mock_generator: MagicMock,
        sample_config: dict[str, Any],
        sample_keywords: list[dict[str, Any]],
    ) -> None:
        """Test that keywords are properly grouped by intent."""
        # Setup
        mock_instance = mock_generator.return_value
        mock_instance.generate_keywords.return_value = sample_keywords

        engine = KeywordEngine(sample_config)

        # Execute
        result = engine.generate_keywords("seo", "digital marketing")

        # Verify
        assert "intent_groups" in result

        # Check that all intents are represented
        intents = {kw["intent"] for kw in sample_keywords}
        assert set(result["intent_groups"].keys()) == intents

        # Check that each keyword is in the right group
        for kw in sample_keywords:
            intent = kw["intent"]
            assert kw["keyword"] in result["intent_groups"][intent]

    # Negative test cases
    @patch("seo_agent.core.keyword_engine.KeywordGenerator")
    def test_generate_keywords_empty_result(
        self, mock_generator: MagicMock, sample_config: dict[str, Any]
    ) -> None:
        """Test generate_keywords when the generator returns empty results."""
        # Setup
        mock_instance = mock_generator.return_value
        mock_instance.generate_keywords.return_value = []

        engine = KeywordEngine(sample_config)

        # Execute
        result = engine.generate_keywords("seo", "digital marketing")

        # Verify
        assert result["total_keywords"] == 0
        assert len(result["keywords"]) == 0
        assert result["intent_groups"] == {}
