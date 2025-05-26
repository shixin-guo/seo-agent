"""Module for analyzing backlinks and identifying opportunities.

This module provides functionality for analyzing backlink profiles and
generating insights for backlink strategy.
"""

from typing import Any, Dict, List, Optional, Set, TypeVar, cast

import requests

# Default User-Agent to mimic a standard browser
USER_AGENT = "Mozilla/5.0 (compatible; SEOAgentBot/1.0; +https://github.com/yourusername/seo-agent)"


class BacklinkAnalyzer:
    """Main engine for backlink analysis and opportunity identification."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the backlink analyzer with configuration.

        Args:
            config: Dictionary containing API keys and settings.
        """
        self.config = config
        self.timeout = config.get("backlink", {}).get(
            "timeout", 10
        )  # Default 10 seconds
        self.user_agent = config.get("backlink", {}).get("user_agent", USER_AGENT)
        self.max_results = config.get("backlink", {}).get("max_results", 100)

        # Setup API keys
        self.ahrefs_key = config.get("apis", {}).get("ahrefs_key")
        self.semrush_key = config.get("apis", {}).get("semrush_key")

        # Setup session for HTTP requests
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})

        # Initialize results structure
        # Type annotation for self.results
        self.results: Dict[str, Any] = {
            "domain": "",
            "backlinks": [],
            "competitors": {},
            "opportunities": [],
            "metrics": {},
            "summary": {},
        }

    def analyze_backlinks(
        self, domain: str, competitors: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Analyze backlinks and identify opportunities.

        Args:
            domain: The primary domain to analyze
            competitors: Optional list of competitor domains

        Returns:
            Dictionary containing backlink analysis and opportunities
        """
        # Ensure domain is properly formatted
        domain = self._normalize_domain(domain)

        # Setup results structure for this analysis
        self.results = {
            "domain": domain,
            "backlinks": [],
            "competitors": {},
            "opportunities": [],
            "metrics": {},
            "summary": {},
        }

        # Get backlinks for the main domain
        backlinks = self._get_backlinks(domain)
        self.results["backlinks"] = backlinks

        # Analyze competitors if provided
        if competitors:
            for competitor in competitors:
                comp_domain = self._normalize_domain(competitor)
                comp_backlinks = self._get_backlinks(comp_domain)
                comp_metrics = self._get_domain_metrics(comp_domain)
                self.results["competitors"][comp_domain] = {
                    "backlinks": comp_backlinks,
                    "metrics": comp_metrics,
                }

            # Find opportunities based on competitor backlinks
            opportunities = self._find_opportunities(domain, competitors)
            self.results["opportunities"] = opportunities

        # Get domain metrics
        self.results["metrics"] = self._get_domain_metrics(domain)

        # Generate summary
        self._generate_summary()

        return self.results

    def _normalize_domain(self, domain: str) -> str:
        """Normalize domain by removing protocol and trailing slashes.

        Args:
            domain: Domain to normalize

        Returns:
            Normalized domain
        """
        # Remove protocol if present
        if "://" in domain:
            domain = domain.split("://")[1]

        # Remove path, query, etc.
        domain = domain.split("/")[0]

        # Remove www. if present
        if domain.startswith("www."):
            domain = domain[4:]

        return domain.lower()

    def _get_backlinks(self, domain: str) -> List[Dict[str, Any]]:
        """Get backlinks for a domain.

        Args:
            domain: Domain to get backlinks for

        Returns:
            List of backlinks
        """
        backlinks = []

        # Use Ahrefs API if available
        if self.ahrefs_key:
            backlinks = self._get_backlinks_from_ahrefs(domain)
        # Use Semrush API if available
        elif self.semrush_key:
            backlinks = self._get_backlinks_from_semrush(domain)
        else:
            # No API keys available - return empty list or raise error
            raise ValueError(
                "No backlink API keys available. Please add AHREFS_API_KEY or SEMRUSH_API_KEY to your environment."
            )

        return backlinks[: self.max_results]

    def _get_backlinks_from_ahrefs(self, domain: str) -> List[Dict[str, Any]]:
        """Get backlinks from Ahrefs API.

        Args:
            domain: Domain to get backlinks for

        Returns:
            List of backlinks
        """
        # TODO: Implement Ahrefs API integration
        # For now, this is a placeholder that would make actual API calls
        raise NotImplementedError(
            "Ahrefs API integration not yet implemented. Please use Semrush API or implement Ahrefs integration."
        )

    def _get_backlinks_from_semrush(self, domain: str) -> List[Dict[str, Any]]:
        """Get backlinks from Semrush API.

        Args:
            domain: Domain to get backlinks for

        Returns:
            List of backlinks
        """
        # TODO: Implement Semrush API integration
        # For now, this is a placeholder that would make actual API calls
        raise NotImplementedError(
            "Semrush API integration not yet implemented. Please use Ahrefs API or implement Semrush integration."
        )

    def _get_domain_metrics(self, domain: str) -> Dict[str, Any]:
        """Get domain metrics like authority, trust, etc.

        Args:
            domain: Domain to get metrics for

        Returns:
            Dictionary of domain metrics
        """
        # TODO: Implement actual domain metrics API integration
        # This would use Ahrefs, Semrush, or Moz APIs in a real implementation
        raise NotImplementedError("Domain metrics API integration not yet implemented.")

    def _find_opportunities(
        self, domain: str, competitors: List[str]
    ) -> List[Dict[str, Any]]:
        """Find backlink opportunities based on competitor analysis.

        Args:
            domain: Main domain
            competitors: List of competitor domains

        Returns:
            List of backlink opportunities
        """
        opportunities = []

        # Normalize domain and competitors
        domain = self._normalize_domain(domain)
        normalized_competitors = [self._normalize_domain(comp) for comp in competitors]

        # Get your existing backlinks (source domains only)
        your_backlink_domains: Set[str] = set()
        for bl in self.results["backlinks"]:
            if isinstance(bl, dict) and "source_domain" in bl:
                your_backlink_domains.add(bl["source_domain"])

        # Check each competitor's backlinks
        for comp_domain in normalized_competitors:
            competitors_dict = self.results.get("competitors", {})
            if not isinstance(competitors_dict, dict):
                competitors_dict = {}

            comp_data = competitors_dict.get(comp_domain, {})
            if not isinstance(comp_data, dict):
                comp_data = {}

            comp_backlinks = comp_data.get("backlinks", [])
            if not isinstance(comp_backlinks, list):
                comp_backlinks = []

            for backlink in comp_backlinks:
                if not isinstance(backlink, dict) or "source_domain" not in backlink:
                    continue
                source_domain = backlink["source_domain"]

                # If this source doesn't link to you but links to the competitor,
                # it's an opportunity
                if source_domain not in your_backlink_domains:
                    opportunity = backlink.copy()
                    opportunity["competitor"] = comp_domain
                    opportunity["opportunity_type"] = "competitor_backlink"
                    opportunity[
                        "opportunity_score"
                    ] = self._calculate_opportunity_score(backlink)
                    opportunities.append(opportunity)

        # Sort opportunities by score (descending)
        # Define a proper key function for sorting
        T = TypeVar("T", bound=Dict[str, Any])

        def get_score(x: T) -> int:
            if not isinstance(x, dict):
                return 0
            score = x.get("opportunity_score")
            return score if isinstance(score, int) else 0

        opportunities.sort(key=get_score, reverse=True)

        return opportunities

    def _calculate_opportunity_score(self, backlink: Dict[str, Any]) -> int:
        """Calculate an opportunity score for a backlink.

        Args:
            backlink: Backlink data

        Returns:
            Opportunity score (higher is better)
        """
        score = 0

        # Higher domain authority is better
        da = backlink.get("domain_authority", 0)
        if da >= 70:
            score += 30
        elif da >= 50:
            score += 20
        elif da >= 30:
            score += 10

        # Dofollow links are better than nofollow
        if backlink.get("link_type") == "dofollow":
            score += 15

        # Prefer relevant categories
        relevant_categories = ["technology", "business", "marketing"]
        if backlink.get("category") in relevant_categories:
            score += 10

        return score

    def _generate_summary(self) -> None:
        """Generate a summary of the backlink analysis."""
        backlinks = self.results["backlinks"]
        opportunities = self.results["opportunities"]

        # Count backlink types
        dofollow_count = len(
            [
                bl
                for bl in backlinks
                if isinstance(bl, dict) and bl.get("link_type") == "dofollow"
            ]
        )
        nofollow_count = len(
            [
                bl
                for bl in backlinks
                if isinstance(bl, dict) and bl.get("link_type") == "nofollow"
            ]
        )

        # Count domains
        unique_domains: Set[str] = set()
        for bl in backlinks:
            if isinstance(bl, dict) and "source_domain" in bl:
                unique_domains.add(bl["source_domain"])

        # Count opportunity types
        opportunity_types: Dict[str, int] = {}
        for opp in opportunities:
            if isinstance(opp, dict):
                opp_type = opp.get("opportunity_type", "unknown")
                if isinstance(opp_type, str):
                    opportunity_types[opp_type] = opportunity_types.get(opp_type, 0) + 1

        # Build summary
        self.results["summary"] = {
            "total_backlinks": len(backlinks),
            "dofollow_count": dofollow_count,
            "nofollow_count": nofollow_count,
            "unique_domains": len(unique_domains),
            "domain_metrics": self.results["metrics"],
            "total_opportunities": len(opportunities),
            "opportunity_types": opportunity_types,
        }

    def generate_outreach_templates(self) -> Dict[str, str]:
        """Generate outreach email templates for backlink opportunities.

        Returns:
            Dictionary of template types and their content
        """
        domain = self.results["domain"]

        templates = {
            "broken_link": f"""
Subject: Broken link found on your website

Hello,

I was browsing your website and noticed a broken link on one of your pages.
The link was supposed to point to [broken page], but it seems the page no longer exists.

I have a similar resource on {domain} that might be a good replacement: [your URL]

It covers [brief description of your content] and might be valuable to your visitors.

Let me know if you have any questions!

Best regards,
[Your Name]
            """.strip(),
            "resource_suggestion": f"""
Subject: Resource suggestion for your [Topic] page

Hello,

I recently came across your excellent article on [Topic] and found it very informative.

I wanted to suggest an additional resource that might be valuable to your readers.
We've published a comprehensive guide on [related topic] at {domain}, which complements
your content well.

You can check it out here: [your URL]

I believe your audience would benefit from this resource, as it covers [brief value proposition].

Thank you for considering my suggestion.

Best regards,
[Your Name]
            """.strip(),
            "competitor_mention": f"""
Subject: Additional resource for your article mentioning [Competitor]

Hello,

I noticed your article where you mention [Competitor], and I thought I'd reach out.

We offer a similar [product/service/tool] at {domain} with some unique features such as
[list 1-2 differentiating features]. Many users find our solution particularly helpful for
[specific use case].

If you're updating your article in the future, we'd appreciate being included as an alternative.
You can learn more about us here: [your URL]

I'm happy to provide any additional information you might need.

Best regards,
[Your Name]
            """.strip(),
        }

        return templates

    def get_top_opportunities(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the top backlink opportunities.

        Args:
            limit: Maximum number of opportunities to return

        Returns:
            List of top backlink opportunities
        """
        opportunities = self.results.get("opportunities", [])

        # Type checking: ensure we have a list of dictionaries
        dict_opportunities = [x for x in opportunities if isinstance(x, dict)]
        typed_opportunities: List[Dict[str, Any]] = cast(
            List[Dict[str, Any]], dict_opportunities
        )

        # Sort by opportunity score
        def get_score(x: Dict[str, Any]) -> int:
            score = x.get("opportunity_score")
            return score if isinstance(score, int) else 0

        sorted_opps = sorted(typed_opportunities, key=get_score, reverse=True)

        return sorted_opps[:limit]
