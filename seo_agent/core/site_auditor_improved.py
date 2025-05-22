"""Module for performing technical SEO audits on websites.

This module provides functionality for crawling websites and analyzing them
for technical SEO issues and opportunities.
"""

import time
from typing import Any, Dict, List, Optional, Set
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# Default User-Agent to mimic a standard browser
USER_AGENT = "Mozilla/5.0 (compatible; SEOAgentBot/1.0; +https://github.com/yourusername/seo-agent)"


class SiteAuditorImproved:
    """Main engine for technical SEO audits."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the site auditor with configuration.

        Args:
            config: Dictionary containing API keys and settings.
        """
        self.config = config
        self.timeout = config.get("audit", {}).get("timeout", 10)  # Default 10 seconds
        self.user_agent = config.get("audit", {}).get("user_agent", USER_AGENT)
        self.respect_robots = config.get("audit", {}).get("respect_robots", True)
        self.max_pages = config.get("audit", {}).get("max_pages", 50)

        # Setup requests session
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})

        # Initialize tracking sets
        self.visited_urls: Set[str] = set()
        self.found_urls: Set[str] = set()
        self.errors: Dict[str, List[Dict[str, Any]]] = {}
        self.all_pages: List[Dict[str, Any]] = []
        self.meta_tags: Dict[str, Dict[str, Any]] = {}

        # Initialize results
        self.results: Dict[str, Any] = {
            "pages_analyzed": 0,
            "issues": [],
            "recommendations": [],
            "summary": {},
        }

    def audit_site(self, domain: str, max_pages: int = 50) -> dict[str, Any]:
        """Perform a technical SEO audit on a website.

        Args:
            domain: The domain to audit
            max_pages: Maximum pages to crawl

        Returns:
            Dictionary containing audit results
        """
        # Ensure domain starts with http
        if not domain.startswith(("http://", "https://")):
            domain = "https://" + domain

        self.max_pages = min(
            max_pages, self.config.get("audit", {}).get("max_pages", 50)
        )
        start_url = domain

        # Setup results structure
        self.results = {
            "domain": urlparse(domain).netloc,
            "start_url": start_url,
            "pages_analyzed": 0,
            "issues": [],
            "redirects": [],
            "broken_links": [],
            "meta_tags": {},
            "page_speeds": {},
            "recommendations": [],
            "summary": {},
        }

        # Start crawling
        self._crawl(start_url)

        # Analyze results
        self._analyze_results()

        # Generate recommendations
        self._generate_recommendations()

        return self.results

    def _crawl(self, start_url: str) -> None:
        """Crawl the website starting from the given URL.

        Args:
            start_url: The URL to start crawling from
        """
        self.found_urls.add(start_url)

        # While we have URLs to visit and haven't hit the limit
        while self.found_urls and len(self.visited_urls) < self.max_pages:
            # Get next URL to visit
            url = self.found_urls.pop()

            if url in self.visited_urls:
                continue

            # Mark as visited
            self.visited_urls.add(url)

            # Fetch and analyze the page
            try:
                page_data = self._fetch_and_analyze_page(url)
                if page_data:
                    self.all_pages.append(page_data)

                    # Extract links
                    if "links" in page_data:
                        for link in page_data["links"]:
                            if link not in self.visited_urls and self._should_crawl(
                                link
                            ):
                                self.found_urls.add(link)
            except Exception as e:
                self.errors[url] = [{"type": "crawl_error", "message": str(e)}]

            # Respect rate limiting
            time.sleep(1)

        # Update pages analyzed count
        self.results["pages_analyzed"] = len(self.visited_urls)

    def _fetch_and_analyze_page(self, url: str) -> Optional[Dict[str, Any]]:
        """Fetch and analyze a single page.

        Args:
            url: The URL to fetch and analyze

        Returns:
            Dictionary containing page analysis data or None if error
        """
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            load_time = time.time() - start_time

            # Check for redirects
            if len(response.history) > 0:
                self.results["redirects"].append(
                    {
                        "from": url,
                        "to": response.url,
                        "status_code": response.history[0].status_code,
                    }
                )

            # Check status code
            if response.status_code != 200:
                self.results["broken_links"].append(
                    {"url": url, "status_code": response.status_code}
                )
                return None

            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract data
            page_data = {
                "url": url,
                "final_url": response.url,
                "status_code": response.status_code,
                "load_time": load_time,
                "content_type": response.headers.get("Content-Type", ""),
                "title": self._get_title(soup),
                "meta_description": self._get_meta_description(soup),
                "h1": self._get_headings(soup, "h1"),
                "h2": self._get_headings(soup, "h2"),
                "images": self._get_images(soup),
                "links": self._get_links(soup, url),
                "issues": self._analyze_page_issues(soup, url, response),
            }

            # Store meta tags
            self.meta_tags[url] = {
                "title": page_data["title"],
                "description": page_data["meta_description"],
                "h1": page_data["h1"],
            }

            # Store page speed
            self.results["page_speeds"][url] = load_time

            return page_data

        except requests.RequestException as e:
            self.results["broken_links"].append({"url": url, "error": str(e)})
            return None

    def _get_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract page title.

        Args:
            soup: BeautifulSoup object

        Returns:
            Page title or None if not found
        """
        title_tag = soup.find("title")
        return title_tag.get_text().strip() if title_tag else None

    def _get_meta_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract meta description.

        Args:
            soup: BeautifulSoup object

        Returns:
            Meta description or None if not found
        """
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag and hasattr(meta_tag, "get"):
            content = meta_tag.get("content", "")
            if isinstance(content, str):
                return content.strip()
        return None

    def _get_headings(self, soup: BeautifulSoup, heading_type: str) -> List[str]:
        """Extract headings of specified type.

        Args:
            soup: BeautifulSoup object
            heading_type: Type of heading (h1, h2, etc.)

        Returns:
            List of headings
        """
        return [h.get_text().strip() for h in soup.find_all(heading_type)]

    def _get_images(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract images and their attributes.

        Args:
            soup: BeautifulSoup object

        Returns:
            List of image data
        """
        images = []
        for img in soup.find_all("img"):
            # Handle different BeautifulSoup types
            if not hasattr(img, "get"):
                continue

            src = img.get("src", "")
            alt = img.get("alt", "")

            # Ensure we have strings
            if not isinstance(src, str):
                src = ""
            if not isinstance(alt, str):
                alt = ""

            if src:
                images.append(
                    {
                        "src": src,
                        "alt": alt,
                        "has_alt": bool(
                            alt and alt.strip()
                        ),  # Check if alt exists before stripping
                    }
                )

        return images

    def _get_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract links from the page.

        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving relative links

        Returns:
            List of absolute URLs
        """
        links = []
        base_domain = urlparse(base_url).netloc

        for a in soup.find_all("a", href=True):
            # Handle different BeautifulSoup types
            if not hasattr(a, "get"):
                continue

            href_attr = a.get("href", "")
            if not isinstance(href_attr, str):
                continue

            href = href_attr.strip()

            # Skip empty, javascript, and anchor links
            if not href or href.startswith(("javascript:", "#", "mailto:", "tel:")):
                continue

            # Resolve relative URLs
            absolute_url = urljoin(base_url, href)

            # Only include links from the same domain
            link_domain = urlparse(absolute_url).netloc
            if link_domain == base_domain:
                links.append(absolute_url)

        return links

    def _analyze_page_issues(
        self, soup: BeautifulSoup, url: str, response: requests.Response
    ) -> List[Dict[str, Any]]:
        """Analyze page for common SEO issues.

        Args:
            soup: BeautifulSoup object
            url: URL of the page
            response: HTTP response object

        Returns:
            List of issues found
        """
        issues = []

        # Check title length
        title = self._get_title(soup)
        if not title:
            issues.append(
                {
                    "type": "missing_title",
                    "severity": "high",
                    "message": "Page is missing a title tag",
                }
            )
        elif len(title) < 10:
            issues.append(
                {
                    "type": "short_title",
                    "severity": "medium",
                    "message": f"Title is too short ({len(title)} characters)",
                }
            )
        elif len(title) > 70:
            issues.append(
                {
                    "type": "long_title",
                    "severity": "medium",
                    "message": f"Title is too long ({len(title)} characters)",
                }
            )

        # Check meta description
        meta_description = self._get_meta_description(soup)
        if not meta_description:
            issues.append(
                {
                    "type": "missing_meta_description",
                    "severity": "medium",
                    "message": "Page is missing a meta description",
                }
            )
        elif len(meta_description) < 50:
            issues.append(
                {
                    "type": "short_meta_description",
                    "severity": "low",
                    "message": f"Meta description is too short ({len(meta_description)} characters)",
                }
            )
        elif len(meta_description) > 160:
            issues.append(
                {
                    "type": "long_meta_description",
                    "severity": "low",
                    "message": f"Meta description is too long ({len(meta_description)} characters)",
                }
            )

        # Check H1
        h1_tags = self._get_headings(soup, "h1")
        if not h1_tags:
            issues.append(
                {
                    "type": "missing_h1",
                    "severity": "medium",
                    "message": "Page is missing an H1 heading",
                }
            )
        elif len(h1_tags) > 1:
            issues.append(
                {
                    "type": "multiple_h1",
                    "severity": "low",
                    "message": f"Page has multiple H1 headings ({len(h1_tags)})",
                }
            )

        # Check images
        images = self._get_images(soup)
        missing_alt = [img for img in images if not img["has_alt"]]
        if missing_alt:
            issues.append(
                {
                    "type": "images_missing_alt",
                    "severity": "medium",
                    "message": f"{len(missing_alt)} of {len(images)} images missing alt text",
                    "details": str(missing_alt),
                }
            )

        # Check page size
        content_length = len(response.text)
        if content_length > 1024 * 1024:  # 1 MB
            issues.append(
                {
                    "type": "large_page_size",
                    "severity": "medium",
                    "message": f"Page size is large: {content_length / 1024:.1f} KB",
                }
            )

        # Add to global issues list
        for issue in issues:
            issue_with_url = issue.copy()
            issue_with_url["url"] = url
            self.results["issues"].append(issue_with_url)

        return issues

    def _should_crawl(self, url: str) -> bool:
        """Check if the URL should be crawled.

        Args:
            url: URL to check

        Returns:
            Boolean indicating if the URL should be crawled
        """
        # Parse URL
        parsed = urlparse(url)

        # Skip non-HTTP URLs
        if parsed.scheme not in ("http", "https"):
            return False

        # Skip certain file types
        extensions = [".pdf", ".jpg", ".jpeg", ".png", ".gif", ".css", ".js"]
        if any(parsed.path.lower().endswith(ext) for ext in extensions):
            return False

        # Skip URLs with query parameters if option is set
        if self.config.get("audit", {}).get("skip_query_urls", False) and parsed.query:
            return False

        return True

    def _analyze_results(self) -> None:
        """Analyze the crawling results and generate a summary."""
        # Count issue types
        issue_counts: Dict[str, int] = {}
        for issue in self.results["issues"]:
            if isinstance(issue, dict) and "type" in issue:
                issue_type = issue["type"]
                if isinstance(issue_type, str):
                    issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1

        # Generate summary
        self.results["summary"] = {
            "total_pages": len(self.visited_urls),
            "total_issues": len(self.results["issues"]),
            "issue_counts": issue_counts,
            "broken_links_count": len(self.results["broken_links"]),
            "redirects_count": len(self.results["redirects"]),
            "average_page_speed": sum(self.results["page_speeds"].values())
            / max(1, len(self.results["page_speeds"])),
        }

        # Count severity levels
        severity_counts = {"high": 0, "medium": 0, "low": 0}
        for issue in self.results["issues"]:
            severity = issue.get("severity", "medium")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        self.results["summary"]["severity_counts"] = severity_counts

    def _generate_recommendations(self) -> None:
        """Generate recommendations based on the issues found."""
        recommendations = []

        # Title and meta description issues
        if any(
            issue["type"] in ["missing_title", "short_title", "long_title"]
            for issue in self.results["issues"]
        ):
            recommendations.append(
                {
                    "type": "title_optimization",
                    "priority": "high",
                    "message": "Optimize page titles to be between 10-70 characters and include relevant keywords.",
                }
            )

        if any(
            issue["type"]
            in [
                "missing_meta_description",
                "short_meta_description",
                "long_meta_description",
            ]
            for issue in self.results["issues"]
        ):
            recommendations.append(
                {
                    "type": "meta_description_optimization",
                    "priority": "high",
                    "message": "Add or optimize meta descriptions to be between 50-160 characters and entice clicks.",
                }
            )

        # Heading issues
        if any(
            issue["type"] in ["missing_h1", "multiple_h1"]
            for issue in self.results["issues"]
        ):
            recommendations.append(
                {
                    "type": "heading_structure",
                    "priority": "medium",
                    "message": "Ensure each page has exactly one H1 tag that clearly describes the page content.",
                }
            )

        # Image issues
        if any(
            issue["type"] == "images_missing_alt" for issue in self.results["issues"]
        ):
            recommendations.append(
                {
                    "type": "image_optimization",
                    "priority": "medium",
                    "message": "Add descriptive alt text to all images to improve accessibility and SEO.",
                }
            )

        # Broken links
        if self.results["broken_links"]:
            recommendations.append(
                {
                    "type": "fix_broken_links",
                    "priority": "high",
                    "message": f"Fix {len(self.results['broken_links'])} broken links found during the audit.",
                }
            )

        # Page speed
        if self.results["summary"]["average_page_speed"] > 3.0:  # More than 3 seconds
            recommendations.append(
                {
                    "type": "improve_page_speed",
                    "priority": "high",
                    "message": f"Improve page load speed, currently averaging {self.results['summary']['average_page_speed']:.2f} seconds.",
                }
            )

        # Add recommendations to results
        self.results["recommendations"] = recommendations

    def generate_action_plan(self) -> str:
        """Generate a prioritized action plan based on audit results.

        Returns:
            Action plan in markdown format
        """
        action_plan = "# SEO Action Plan\n\n"

        # Add high priority items
        action_plan += "## High Priority Items\n\n"
        for rec in self.results.get("recommendations", []):
            if rec.get("priority") == "high":
                action_plan += f"- {rec['message']}\n"

        # Add medium priority items
        action_plan += "\n## Medium Priority Items\n\n"
        for rec in self.results.get("recommendations", []):
            if rec.get("priority") == "medium":
                action_plan += f"- {rec['message']}\n"

        # Add statistics
        action_plan += "\n## Audit Statistics\n\n"
        action_plan += (
            f"- Total pages analyzed: {self.results['summary']['total_pages']}\n"
        )
        action_plan += (
            f"- Total issues found: {self.results['summary']['total_issues']}\n"
        )
        action_plan += (
            f"- Broken links: {self.results['summary']['broken_links_count']}\n"
        )
        action_plan += f"- Redirects: {self.results['summary']['redirects_count']}\n"
        action_plan += f"- Average page speed: {self.results['summary']['average_page_speed']:.2f} seconds\n"

        return action_plan
