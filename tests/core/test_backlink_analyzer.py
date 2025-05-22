"""Tests for the BacklinkAnalyzer module."""

from typing import Any
from unittest.mock import MagicMock

from seo_agent.core.backlink_analyzer import BacklinkAnalyzer

# Constants for test configuration
EXPECTED_COMPETITOR_COUNT = 2
EXPECTED_TOTAL_DOMAINS = 3  # main domain + competitors
EXPECTED_BACKLINKS = 1  # Number of backlinks in mock data


class TestBacklinkAnalyzer:
    """Test suite for BacklinkAnalyzer class."""

    def test_init(self, sample_config: dict[str, Any]) -> None:
        """Test BacklinkAnalyzer initialization."""
        analyzer = BacklinkAnalyzer(sample_config)
        assert analyzer.config == sample_config

    def test_analyze_backlinks_without_competitors(
        self, sample_config: dict[str, Any]
    ) -> None:
        """Test analyze_backlinks without competitor domains."""
        # Setup
        analyzer = BacklinkAnalyzer(sample_config)
        analyzer._fetch_backlink_data = MagicMock(
            return_value={"domain": "example.com", "links": []}
        )
        analyzer._find_opportunities = MagicMock(return_value=[])

        # Execute
        result = analyzer.analyze_backlinks("example.com")

        # Verify
        analyzer._fetch_backlink_data.assert_called_once_with("example.com")
        analyzer._find_opportunities.assert_called_once()

        assert result["domain"] == "example.com"
        assert result["backlinks"] == 0
        assert result["competitors_analyzed"] == 0
        assert "opportunities" in result

    def test_analyze_backlinks_with_competitors(
        self, sample_config: dict[str, Any]
    ) -> None:
        """Test analyze_backlinks with competitor domains."""
        # Setup
        analyzer = BacklinkAnalyzer(sample_config)
        analyzer._fetch_backlink_data = MagicMock()
        analyzer._fetch_backlink_data.side_effect = [
            {"domain": "example.com", "links": [{"url": "link1.com"}]},
            {"domain": "competitor1.com", "links": [{"url": "link2.com"}]},
            {"domain": "competitor2.com", "links": [{"url": "link3.com"}]},
        ]

        analyzer._find_opportunities = MagicMock(
            return_value=[
                {
                    "source": "opportunity1.com",
                    "opportunity_type": "competitor_backlink",
                },
                {
                    "source": "opportunity2.com",
                    "opportunity_type": "competitor_backlink",
                },
            ]
        )

        # Execute
        result = analyzer.analyze_backlinks(
            "example.com", ["competitor1.com", "competitor2.com"]
        )

        # Verify
        assert analyzer._fetch_backlink_data.call_count == EXPECTED_TOTAL_DOMAINS
        analyzer._find_opportunities.assert_called_once()

        assert result["domain"] == "example.com"
        assert result["backlinks"] == EXPECTED_BACKLINKS
        assert result["competitors_analyzed"] == EXPECTED_COMPETITOR_COUNT
        assert len(result["opportunities"]) == 2

    def test_fetch_backlink_data(self, sample_config: dict[str, Any]) -> None:
        """Test _fetch_backlink_data method."""
        analyzer = BacklinkAnalyzer(sample_config)

        # Execute
        result = analyzer._fetch_backlink_data("example.com")

        # Verify
        assert result["domain"] == "example.com"
        assert "links" in result

    def test_find_opportunities(
        self, sample_config: dict[str, Any], sample_backlink_data: dict[str, Any]
    ) -> None:
        """Test _find_opportunities method."""
        analyzer = BacklinkAnalyzer(sample_config)
        competitor_data = {
            "competitor1.com": {
                "domain": "competitor1.com",
                "links": [{"source": "unique-site.com"}],
            },
            "competitor2.com": {"domain": "competitor2.com", "links": []},
        }

        # Execute
        opportunities = analyzer._find_opportunities(
            "example.com", sample_backlink_data, competitor_data
        )

        # Verify
        assert isinstance(opportunities, list)
        assert len(opportunities) > 0
        assert all(isinstance(o, dict) for o in opportunities)
        assert all("source" in o for o in opportunities)

    def test_generate_outreach_templates(self, sample_config: dict[str, Any]) -> None:
        """Test generate_outreach_templates method."""
        analyzer = BacklinkAnalyzer(sample_config)
        opportunities = [
            {"source": "opportunity1.com", "opportunity_type": "competitor_backlink"},
            {"source": "opportunity2.com", "opportunity_type": "broken_link"},
        ]

        # Execute
        templates = analyzer.generate_outreach_templates(opportunities)

        # Verify
        assert isinstance(templates, dict)
        assert len(templates) == len(opportunities)
        assert all("template_" in key for key in templates.keys())
        assert all(isinstance(value, str) for value in templates.values())
        assert all("Subject:" in value for value in templates.values())
