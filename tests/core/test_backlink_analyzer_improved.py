"""Tests for the improved BacklinkAnalyzer module."""

from typing import Any, Dict, List
from unittest.mock import MagicMock


from seo_agent.core.backlink_analyzer_improved import BacklinkAnalyzer


class TestBacklinkAnalyzerImproved:
    """Test suite for the improved BacklinkAnalyzer class."""

    def test_init(self, sample_config: Dict[str, Any]) -> None:
        """Test BacklinkAnalyzer initialization."""
        analyzer = BacklinkAnalyzer(sample_config)
        assert analyzer.config == sample_config
        assert hasattr(analyzer, "session")
        assert hasattr(analyzer, "max_results")
        assert hasattr(analyzer, "results")

    def test_normalize_domain(self) -> None:
        """Test domain normalization logic."""
        analyzer = BacklinkAnalyzer({})

        # Test with different domain formats
        assert analyzer._normalize_domain("example.com") == "example.com"
        assert analyzer._normalize_domain("www.example.com") == "example.com"
        assert analyzer._normalize_domain("https://www.example.com") == "example.com"
        assert analyzer._normalize_domain("http://example.com/page") == "example.com"
        assert analyzer._normalize_domain("EXAMPLE.com") == "example.com"

    def test_get_mock_backlinks(self) -> None:
        """Test mock backlink generation."""
        analyzer = BacklinkAnalyzer({})

        # Test with different domains
        backlinks1 = analyzer._get_mock_backlinks("example.com")
        backlinks2 = analyzer._get_mock_backlinks("test.org")

        # Check backlink structure
        assert isinstance(backlinks1, list)
        assert len(backlinks1) > 0

        # Check required fields
        for link in backlinks1:
            assert "source_domain" in link
            assert "source_url" in link
            assert "target_url" in link
            assert "anchor_text" in link
            assert "link_type" in link
            assert "domain_authority" in link

        # Check that different domains produce different results
        assert backlinks1 != backlinks2

    def test_find_opportunities(self) -> None:
        """Test opportunity finding logic."""
        analyzer = BacklinkAnalyzer({})

        # Setup test data
        domain = "example.com"
        competitors = ["competitor1.com", "competitor2.com"]

        # Setup mock backlinks
        analyzer.results = {
            "domain": domain,
            "backlinks": [
                {"source_domain": "common.com", "source_url": "https://common.com/1"},
                {
                    "source_domain": "yourlink.com",
                    "source_url": "https://yourlink.com/1",
                },
            ],
            "competitors": {
                "competitor1.com": {
                    "backlinks": [
                        {
                            "source_domain": "common.com",
                            "source_url": "https://common.com/1",
                        },
                        {
                            "source_domain": "unique1.com",
                            "source_url": "https://unique1.com/1",
                            "domain_authority": 50,
                            "link_type": "dofollow",
                        },
                    ]
                },
                "competitor2.com": {
                    "backlinks": [
                        {
                            "source_domain": "unique2.com",
                            "source_url": "https://unique2.com/1",
                            "domain_authority": 30,
                            "link_type": "nofollow",
                        },
                    ]
                },
            },
        }

        # Test opportunity finding
        opportunities = analyzer._find_opportunities(domain, competitors)

        # Verify opportunities are found
        assert len(opportunities) == 2

        # Check that opportunities are properly identified
        domains = {opp["source_domain"] for opp in opportunities}
        assert "unique1.com" in domains
        assert "unique2.com" in domains

        # Check that scoring is working
        for opp in opportunities:
            assert "opportunity_score" in opp

        # Verify opportunities are sorted by score
        assert (
            opportunities[0]["opportunity_score"]
            >= opportunities[1]["opportunity_score"]
        )

    def test_analyze_backlinks(self, sample_config: Dict[str, Any]) -> None:
        """Test full backlink analysis process."""
        analyzer = BacklinkAnalyzer(sample_config)

        # Mock key methods to isolate test
        analyzer._get_backlinks = MagicMock(
            return_value=[
                {
                    "source_domain": "example-source.com",
                    "source_url": "https://example-source.com/page",
                    "target_url": "https://example.com/target",
                    "anchor_text": "example anchor",
                    "link_type": "dofollow",
                    "domain_authority": 40,
                }
            ]
        )

        analyzer._get_domain_metrics = MagicMock(
            return_value={
                "domain_authority": 50,
                "referring_domains": 100,
            }
        )

        # Test with no competitors
        results = analyzer.analyze_backlinks("example.com")

        # Verify result structure
        assert "domain" in results
        assert "backlinks" in results
        assert "metrics" in results
        assert "summary" in results

        # Test with competitors
        competitors = ["competitor1.com", "competitor2.com"]
        results = analyzer.analyze_backlinks("example.com", competitors)

        # Verify competitor data
        assert "competitors" in results
        assert len(results["competitors"]) == len(competitors)
        assert "opportunities" in results

    def test_analyze_backlinks_with_sample_data(
        self,
        sample_config: Dict[str, Any],
        sample_improved_backlink_data: Dict[str, Any],
    ) -> None:
        """Test analyze_backlinks with sample data."""
        analyzer = BacklinkAnalyzer(sample_config)

        # Replace internal methods with mocks that return our sample data
        def mock_get_backlinks(domain: str) -> List[Dict[str, Any]]:
            if domain == "example.com":
                return sample_improved_backlink_data["backlinks"]
            elif domain == "competitor1.com":
                return sample_improved_backlink_data["competitors"]["competitor1.com"][
                    "backlinks"
                ]
            return []

        def mock_get_domain_metrics(domain: str) -> Dict[str, Any]:
            if domain == "example.com":
                return sample_improved_backlink_data["metrics"]
            elif domain == "competitor1.com":
                return sample_improved_backlink_data["competitors"]["competitor1.com"][
                    "metrics"
                ]
            return {"domain_authority": 30}

        analyzer._get_backlinks = MagicMock(side_effect=mock_get_backlinks)
        analyzer._get_domain_metrics = MagicMock(side_effect=mock_get_domain_metrics)

        # Test with one competitor
        results = analyzer.analyze_backlinks("example.com", ["competitor1.com"])

        # Verify result matches our sample data structure
        assert results["domain"] == "example.com"
        assert len(results["backlinks"]) == len(
            sample_improved_backlink_data["backlinks"]
        )
        assert "competitors" in results
        assert "competitor1.com" in results["competitors"]
        assert "opportunities" in results

    def test_generate_outreach_templates(self) -> None:
        """Test email template generation."""
        analyzer = BacklinkAnalyzer({"domain": "example.com"})
        analyzer.results = {"domain": "example.com"}

        templates = analyzer.generate_outreach_templates()

        # Verify templates exist
        assert "broken_link" in templates
        assert "resource_suggestion" in templates
        assert "competitor_mention" in templates

        # Check template content
        for template_name, content in templates.items():
            assert "Subject:" in content
            assert "example.com" in content  # Domain should be in template

    def test_get_top_opportunities(self) -> None:
        """Test retrieval of top opportunities."""
        analyzer = BacklinkAnalyzer({})

        # Setup test data with varied scores
        analyzer.results = {
            "opportunities": [
                {"source_domain": "high.com", "opportunity_score": 50},
                {"source_domain": "medium.com", "opportunity_score": 30},
                {"source_domain": "low.com", "opportunity_score": 10},
            ]
        }

        # Test with default limit
        top_opps = analyzer.get_top_opportunities()
        assert len(top_opps) == 3
        assert top_opps[0]["source_domain"] == "high.com"

        # Test with custom limit
        top_opps = analyzer.get_top_opportunities(limit=2)
        assert len(top_opps) == 2
        assert top_opps[0]["source_domain"] == "high.com"
        assert top_opps[1]["source_domain"] == "medium.com"
