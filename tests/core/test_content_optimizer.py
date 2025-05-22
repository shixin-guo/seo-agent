"""Tests for the ContentOptimizer module."""

from typing import Any
from unittest.mock import MagicMock, mock_open, patch
from dataclasses import dataclass

from seo_agent.core.content_optimizer import ContentOptimizer


@dataclass
class OptimizerTestContext:
    """Test context for content optimizer tests."""

    config: dict[str, Any]
    content: str
    json_loader: MagicMock
    file_exists: MagicMock
    file_mock: MagicMock


class TestContentOptimizer:
    """Test suite for ContentOptimizer class."""

    def test_init(self, sample_config: dict[str, Any]) -> None:
        """Test ContentOptimizer initialization."""
        optimizer = ContentOptimizer(sample_config)
        assert optimizer.config == sample_config

    @patch(
        "builtins.open", new_callable=mock_open, read_data="Sample content for testing"
    )
    @patch("os.path.exists")
    def test_optimize_content_without_keywords(
        self,
        mock_exists: MagicMock,
        mock_file: MagicMock,
        sample_config: dict[str, Any],
    ) -> None:
        """Test optimize_content without a keywords file."""
        # Setup
        mock_exists.return_value = False
        optimizer = ContentOptimizer(sample_config)

        # Mock the private methods
        optimizer._analyze_content = MagicMock(return_value={"word_count": 4})
        optimizer._generate_suggestions = MagicMock(
            return_value=[{"type": "heading", "suggestion": "Add more headings"}]
        )
        optimizer._apply_suggestions = MagicMock(
            return_value="Optimized sample content"
        )

        # Execute
        result = optimizer.optimize_content("sample.txt")

        # Verify
        mock_file.assert_called_once_with("sample.txt", "r")
        optimizer._analyze_content.assert_called_once_with(
            "Sample content for testing", []
        )
        optimizer._generate_suggestions.assert_called_once()
        optimizer._apply_suggestions.assert_called_once()

        assert result["original_content"] == "Sample content for testing"
        assert result["optimized_content"] == "Optimized sample content"
        assert "analysis" in result
        assert "suggestions" in result

    @patch("builtins.open")
    @patch("os.path.exists")
    @patch("json.load")
    def test_optimize_content_with_keywords(
        self,
        mock_json_load: MagicMock,
        mock_exists: MagicMock,
        mock_file: MagicMock,
        sample_config: dict[str, Any],
        sample_content: str,
    ) -> None:
        """Test optimize_content with a keywords file."""
        # Note: OptimizerTestContext can be used for more complex tests
        # but not needed for this basic test
        """Test optimize_content with a keywords file."""
        # Setup
        mock_exists.return_value = True
        mock_file.side_effect = [
            mock_open(read_data=sample_content).return_value,
            mock_open().return_value,
        ]
        mock_json_load.return_value = {
            "keywords": [{"keyword": "seo"}, {"keyword": "content optimization"}]
        }

        optimizer = ContentOptimizer(sample_config)

        # Mock the private methods
        optimizer._analyze_content = MagicMock(
            return_value={"word_count": len(sample_content.split())}
        )
        optimizer._generate_suggestions = MagicMock(
            return_value=[{"type": "keyword", "suggestion": "Add more keywords"}]
        )
        optimizer._apply_suggestions = MagicMock(return_value="Optimized content")

        # Execute
        result = optimizer.optimize_content("sample.txt", "keywords.json")

        # Verify
        optimizer._analyze_content.assert_called_once_with(
            sample_content, ["seo", "content optimization"]
        )
        assert result["original_content"] == sample_content
        assert "analysis" in result
        assert "suggestions" in result

    def test_analyze_content(
        self, sample_config: dict[str, Any], sample_content: str
    ) -> None:
        """Test _analyze_content method."""
        optimizer = ContentOptimizer(sample_config)

        # Execute
        result = optimizer._analyze_content(sample_content, ["seo", "optimization"])

        # Verify
        assert "word_count" in result
        assert "keyword_density" in result
        assert "readability" in result

    def test_generate_suggestions(self, sample_config: dict[str, Any]) -> None:
        """Test _generate_suggestions method."""
        optimizer = ContentOptimizer(sample_config)
        analysis = {"word_count": 100, "keyword_density": {}, "readability": "medium"}

        # Execute
        suggestions = optimizer._generate_suggestions("content", analysis)

        # Verify
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        assert all(isinstance(s, dict) for s in suggestions)
        assert all("type" in s and "suggestion" in s for s in suggestions)

    def test_apply_suggestions(
        self, sample_config: dict[str, Any], sample_content: str
    ) -> None:
        """Test _apply_suggestions method."""
        optimizer = ContentOptimizer(sample_config)
        suggestions = [
            {"type": "heading", "suggestion": "Add more headings"},
            {"type": "keyword", "suggestion": "Increase keyword density"},
        ]

        # Execute
        result = optimizer._apply_suggestions(sample_content, suggestions)

        # Verify
        assert (
            result == sample_content
        )  # The placeholder implementation returns the original content
