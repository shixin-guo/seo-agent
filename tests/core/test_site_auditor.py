"""Tests for the SiteAuditor module."""

from typing import Any
from unittest.mock import MagicMock

from seo_agent.core.site_auditor import SiteAuditor

# Constants for test configuration
SAMPLE_ISSUE_COUNT = 2


class TestSiteAuditor:
    """Test suite for SiteAuditor class."""

    def test_init(self, sample_config: dict[str, Any]) -> None:
        """Test SiteAuditor initialization."""
        auditor = SiteAuditor(sample_config)
        assert auditor.config == sample_config
        assert auditor.max_pages == sample_config["defaults"]["crawl_depth"]

    def test_audit_site_with_default_max_pages(
        self, sample_config: dict[str, Any], sample_crawl_results: dict[str, Any]
    ) -> None:
        """Test audit_site with default max_pages from config."""
        # Setup
        auditor = SiteAuditor(sample_config)
        auditor._crawl_site = MagicMock(return_value=sample_crawl_results)
        auditor._analyze_issues = MagicMock(
            return_value=[
                {
                    "type": "missing_meta_description",
                    "severity": "medium",
                    "affected_pages": ["example.com/page2"],
                }
            ]
        )
        auditor._generate_recommendations = MagicMock(
            return_value=[
                {
                    "issue_type": "missing_meta_description",
                    "priority": "medium",
                    "recommendation": "Add meta descriptions",
                    "affected_pages": ["example.com/page2"],
                }
            ]
        )

        # Execute
        result = auditor.audit_site("example.com")

        # Verify
        auditor._crawl_site.assert_called_once_with(
            "example.com", sample_config["defaults"]["crawl_depth"]
        )
        auditor._analyze_issues.assert_called_once_with(sample_crawl_results)
        auditor._generate_recommendations.assert_called_once()

        assert result["domain"] == "example.com"
        assert result["pages_crawled"] == len(sample_crawl_results["pages"])
        assert result["total_issues"] == 1
        assert "issues_by_severity" in result
        assert "issues" in result
        assert "recommendations" in result

    def test_audit_site_with_custom_max_pages(
        self, sample_config: dict[str, Any], sample_crawl_results: dict[str, Any]
    ) -> None:
        """Test audit_site with custom max_pages parameter."""
        # Setup
        auditor = SiteAuditor(sample_config)
        auditor._crawl_site = MagicMock(return_value=sample_crawl_results)
        auditor._analyze_issues = MagicMock(
            return_value=[
                {
                    "type": "missing_meta_description",
                    "severity": "medium",
                    "affected_pages": ["example.com/page2"],
                }
            ]
        )
        auditor._generate_recommendations = MagicMock(
            return_value=[
                {
                    "issue_type": "missing_meta_description",
                    "priority": "medium",
                    "recommendation": "Add meta descriptions",
                    "affected_pages": ["example.com/page2"],
                }
            ]
        )

        custom_max_pages = 30

        # Execute
        result = auditor.audit_site("example.com", custom_max_pages)

        # Verify
        auditor._crawl_site.assert_called_once_with("example.com", custom_max_pages)
        assert result["domain"] == "example.com"
        assert result["pages_crawled"] == len(sample_crawl_results["pages"])

    def test_crawl_site(self, sample_config: dict[str, Any]) -> None:
        """Test _crawl_site method."""
        auditor = SiteAuditor(sample_config)

        # Execute
        result = auditor._crawl_site("example.com", 20)

        # Verify
        assert result["domain"] == "example.com"
        assert "pages" in result

    def test_analyze_issues(
        self, sample_config: dict[str, Any], sample_crawl_results: dict[str, Any]
    ) -> None:
        """Test _analyze_issues method."""
        auditor = SiteAuditor(sample_config)

        # Execute
        issues = auditor._analyze_issues(sample_crawl_results)

        # Verify
        assert isinstance(issues, list)
        assert len(issues) > 0
        assert all(isinstance(i, dict) for i in issues)
        assert all("type" in i and "severity" in i for i in issues)

    def test_generate_recommendations(self, sample_config: dict[str, Any]) -> None:
        """Test _generate_recommendations method."""
        auditor = SiteAuditor(sample_config)
        issues = [
            {
                "type": "missing_meta_description",
                "severity": "medium",
                "affected_pages": ["page1.html"],
            },
            {
                "type": "broken_link",
                "severity": "high",
                "affected_pages": ["page2.html"],
            },
        ]

        # Execute
        recommendations = auditor._generate_recommendations(issues)

        # Verify
        assert isinstance(recommendations, list)
        assert len(recommendations) == len(issues)
        assert all(isinstance(r, dict) for r in recommendations)
        assert all(
            "issue_type" in r and "priority" in r and "recommendation" in r
            for r in recommendations
        )

        # High severity issues should have high priority
        high_severity_recs = [
            r for r in recommendations if r["issue_type"] == "broken_link"
        ]
        assert high_severity_recs[0]["priority"] == "high"

    def test_group_by_severity(self, sample_config: dict[str, Any]) -> None:
        """Test _group_by_severity method."""
        auditor = SiteAuditor(sample_config)
        issues = [
            {"type": "missing_meta_description", "severity": "medium"},
            {"type": "broken_link", "severity": "high"},
            {"type": "duplicate_content", "severity": "medium"},
            {"type": "slow_page", "severity": "low"},
        ]

        # Execute
        grouped = auditor._group_by_severity(issues)

        # Verify
        assert grouped["high"] == 1
        assert grouped["medium"] == SAMPLE_ISSUE_COUNT
        assert grouped["low"] == 1

    def test_generate_action_plan(self, sample_config: dict[str, Any]) -> None:
        """Test generate_action_plan method."""
        auditor = SiteAuditor(sample_config)
        audit_result = {
            "domain": "example.com",
            "recommendations": [
                {"priority": "high", "recommendation": "Fix broken links"},
                {"priority": "medium", "recommendation": "Add meta descriptions"},
                {"priority": "high", "recommendation": "Fix server errors"},
            ],
        }

        # Execute
        action_plan = auditor.generate_action_plan(audit_result)

        # Verify
        assert isinstance(action_plan, str)
        assert "# SEO Action Plan" in action_plan
        assert "## High Priority Items" in action_plan
        assert "## Medium Priority Items" in action_plan

        # Check that high priority items come before medium priority
        high_priority_pos = action_plan.find("## High Priority Items")
        medium_priority_pos = action_plan.find("## Medium Priority Items")
        assert high_priority_pos < medium_priority_pos
