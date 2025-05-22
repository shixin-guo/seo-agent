#!/usr/bin/env python

"""Main CLI interface for the SEO Agent tool.

This module provides command-line interface functionality for various SEO operations
including keyword research, content optimization, site auditing, and backlink analysis.
"""

import json
import os
import sys
from datetime import datetime
from typing import Any, Optional

import click
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import core modules - must be after adding to path
from seo_agent.core.keyword_engine import KeywordEngine  # noqa: E402


# Load configuration
def load_config() -> dict[str, Any]:
    """Load and merge configuration from YAML file and environment variables.

    Returns:
        dict[str, Any]: Configuration dictionary with API keys and settings.
    """
    config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "config.yaml"
    )
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Add API keys from environment variables
    api_keys = {
        "openai_key": os.getenv("OPENAI_API_KEY"),
        "serpapi_key": os.getenv("SERPAPI_KEY"),
        "ahrefs_key": os.getenv("AHREFS_API_KEY"),
        "semrush_key": os.getenv("SEMRUSH_API_KEY"),
    }

    # Remove None values
    api_keys = {k: v for k, v in api_keys.items() if v is not None}

    # Merge with config
    if "apis" not in config:
        config["apis"] = {}
    config["apis"].update(api_keys)

    return config  # type: ignore[no-any-return]


def validate_api_keys(config: dict[str, Any], required_apis: list[str]) -> None:
    """Validate that required API keys are present"""
    missing_keys = []
    for api in required_apis:
        if not config.get("apis", {}).get(api):
            missing_keys.append(api)

    if missing_keys:
        click.echo(f"❌ Missing required API keys: {', '.join(missing_keys)}")
        click.echo("Please add them to your .env file")
        sys.exit(1)


# Approval system
def require_approval(operation: str, details: str, config: dict[str, Any]) -> bool:
    """Ask for user approval before proceeding with an operation.

    Args:
        operation: Description of the operation to perform
        details: Additional details about the operation
        config: Configuration dictionary that may contain approval settings

    Returns:
        True if approved, False otherwise
    """
    # Skip approval if disabled in config
    if not config.get("defaults", {}).get("approval_required", True):
        return True

    # Ask for approval
    click.echo(f"\n📋 {operation}")
    click.echo(f"Details: {details}")

    # Auto-approve for non-interactive environments (CI/CD)
    if os.environ.get("CI") or os.environ.get("NONINTERACTIVE"):
        click.echo("Auto-approving in non-interactive mode.")
        return True

    try:
        while True:
            response = click.prompt("Proceed? (y/n/details)", type=str, default="y")
            if response.lower() == "details":
                click.echo("Detailed preview not implemented yet.")
                continue
            elif response.lower() in ["y", "yes"]:
                return True
            else:
                return False
    except (KeyboardInterrupt, EOFError):
        # Handle keyboard interrupt (Ctrl+C) or pipe errors
        click.echo("\nOperation aborted by user.")
        return False


# CLI commands
@click.group()
def cli() -> None:
    """SEO Agent - AI-powered SEO automation tool"""
    pass


@cli.command("keyword-research")
@click.option("--seed", required=True, help="Seed keyword to expand from")
@click.option("--industry", help="Industry for context")
@click.option("--output", default=None, help="Output file path")
def keyword_research(seed: str, industry: Optional[str], output: Optional[str]) -> None:
    """Generate keyword research based on seed keywords."""
    config = load_config()

    # Validate required API keys
    validate_api_keys(config, ["openai_key", "serpapi_key"])

    click.echo(f"🔍 Performing keyword research for: {seed}")

    # Initialize engine
    engine = KeywordEngine(config)

    # Generate keywords
    try:
        results = engine.generate_keywords(seed, industry)
        click.echo(f"Generated {results['total_keywords']} keywords.")
    except Exception as e:
        click.echo(f"Error generating keywords: {str(e)}")
        # Use mock data as fallback
        from tests.mock.mock_keyword_data import generate_mock_keywords

        results = generate_mock_keywords(seed, industry or "general")

    # Generate default output filename if not provided
    if not output:
        timestamp = datetime.now().strftime("%Y_%m_%d")
        output = f"keywords_report_{timestamp}.json"
        output_path = os.path.join(config["output"]["reports_folder"], output)
    else:
        output_path = output

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save results
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    click.echo(f"✅ Keyword research complete. Results saved to: {output_path}")

    # Approval for export to CSV
    if require_approval(
        "Export to CSV for use in other tools",
        f"{len(results['keywords'])} keywords",
        config,
    ):
        csv_path = output_path.replace(".json", ".csv")
        # Export to CSV
        with open(csv_path, "w") as f:
            f.write("keyword,intent,competition\n")
            for kw in results["keywords"]:
                keyword = kw.get("keyword", "").replace(
                    ",", " "
                )  # Remove commas from keywords
                intent = kw.get("intent", "informational")
                competition = kw.get("competition", "medium")
                f.write(f"{keyword},{intent},{competition}\n")
        click.echo(f"📤 Exported to: {csv_path}")


@cli.command("optimize-content")
@click.option("--file", required=True, help="Content file to optimize")
@click.option("--keywords", help="Keywords JSON file to use for optimization")
@click.option("--output", help="Output file path for optimized content")
@click.option(
    "--basic",
    is_flag=True,
    help="Use basic optimization instead of advanced AI-powered optimization",
)
@click.option(
    "--creative", is_flag=True, help="Use higher creativity for more varied output"
)
def optimize_content(
    file: str,
    keywords: Optional[str],
    output: Optional[str],
    basic: bool = False,
    creative: bool = False,
) -> None:
    """Optimize content for SEO."""
    config = load_config()

    # Validate required API keys
    validate_api_keys(config, ["openai_key"])

    # Check if the file exists
    if not os.path.exists(file):
        click.echo(f"❌ Error: File {file} not found.")
        sys.exit(1)

    # Check if keywords file exists if provided
    if keywords and not os.path.exists(keywords):
        click.echo(f"❌ Error: Keywords file {keywords} not found.")
        sys.exit(1)

    click.echo(f"✍️ Optimizing content: {file}")

    try:
        # Generate default output filename if not provided
        if not output:
            # Get base filename without extension
            base_name = os.path.basename(file)
            name_parts = os.path.splitext(base_name)
            file_name = name_parts[0]

            # Create a standard filename with _optimized suffix (no timestamp)
            output = f"{file_name}_optimized.md"

            # Make sure we're using an absolute path
            if not os.path.isabs(output):
                output = os.path.join(os.path.dirname(os.path.abspath(file)), output)

            # Check if file exists
            if os.path.exists(output):
                click.echo(
                    f"Output file {output} already exists and will be overwritten."
                )
            else:
                click.echo(f"Output file will be saved to: {output}")

        if basic:
            # Use the standard optimizer
            from seo_agent.core.content_optimizer import ContentOptimizer

            # Initialize optimizer
            optimizer = ContentOptimizer(config)

            # Perform optimization
            result = optimizer.optimize_content(file, keywords)

            # Display summary of analysis
            click.echo("\n📊 Content Analysis:")
            click.echo(f"- Word count: {result['analysis'].get('word_count', 0)}")
            click.echo(
                f"- Readability: {result['analysis'].get('readability', 'unknown')}"
            )

            # Display suggestions
            suggestions = result.get("suggestions", [])
            if suggestions:
                click.echo("\n💡 Optimization Suggestions:")
                for idx, suggestion in enumerate(suggestions, 1):
                    click.echo(
                        f"{idx}. {suggestion.get('type', 'general')}: {suggestion.get('suggestion', '')}"
                    )
            else:
                click.echo(
                    "\n💡 Optimization Suggestions: None - content is already well-optimized!"
                )

            # Save optimized content
            with open(output, "w") as f:
                f.write(result["optimized_content"])
            click.echo(f"\n✅ Optimized content saved to: {output}")
        else:
            # Use the advanced AI-powered optimizer
            from seo_agent.core.advanced_content_optimizer import (
                AdvancedContentOptimizer,
            )

            # Adjust config for creativity if requested
            if creative:
                # Make a copy of the config to avoid modifying the original
                creative_config = config.copy()
                if "ai" not in creative_config:
                    creative_config["ai"] = {}

                # Set higher temperature for more creative results
                creative_config["ai"]["temperature"] = 0.9

                # Add timestamp to seed random variation
                import time

                timestamp = int(time.time())
                if "randomization" not in creative_config:
                    creative_config["randomization"] = {}
                creative_config["randomization"]["seed"] = timestamp

                click.echo(
                    f"\n🎨 Using higher creativity for unique output (seed: {timestamp})..."
                )

                # Initialize advanced optimizer with creative config
                advanced_optimizer = AdvancedContentOptimizer(creative_config)
            else:
                # Initialize advanced optimizer with standard config
                advanced_optimizer = AdvancedContentOptimizer(config)

            # Start the full optimization process
            click.echo("\n🧠 Using advanced AI-powered optimization...")

            # Fully optimize the content
            # Ensure keywords is a string or None
            keywords_path = keywords if keywords else ""
            optimized_content = advanced_optimizer.fully_optimize_content(
                file, keywords_path
            )

            # Save the optimized content to the output file
            with open(output, "w") as f:
                f.write(optimized_content)
            click.echo(f"\n✅ Fully optimized content saved to: {output}")
    except Exception as e:
        click.echo(f"❌ Error optimizing content: {str(e)}")
        import traceback

        click.echo(traceback.format_exc())
        sys.exit(1)


@cli.command("audit-site")
@click.option("--domain", required=True, help="Domain to audit")
@click.option("--depth", default=50, help="Maximum pages to crawl")
@click.option("--output", help="Output file path for audit results")
def audit_site(domain: str, depth: int, output: Optional[str] = None) -> None:
    """Perform a technical SEO audit on a website."""
    config = load_config()

    # No API key required for basic audit
    # validate_api_keys(config, ["openai_key"])

    click.echo(f"🔧 Auditing site: {domain} (max {depth} pages)")

    try:
        # Import the improved auditor
        from seo_agent.core.site_auditor_improved import SiteAuditorImproved

        # Initialize auditor
        auditor = SiteAuditorImproved(config)

        # Start the audit
        click.echo("\n🔍 Crawling website... (this may take a few minutes)")

        # Perform the audit
        results = auditor.audit_site(domain, depth)

        # Display summary
        click.echo("\n📊 Audit Summary:")
        click.echo(f"- Pages analyzed: {results['summary']['total_pages']}")
        click.echo(f"- Issues found: {results['summary']['total_issues']}")

        # Display severity breakdown
        severity_counts = results["summary"].get("severity_counts", {})
        click.echo(f"- High severity issues: {severity_counts.get('high', 0)}")
        click.echo(f"- Medium severity issues: {severity_counts.get('medium', 0)}")
        click.echo(f"- Low severity issues: {severity_counts.get('low', 0)}")

        # Display broken links
        if results.get("broken_links"):
            click.echo(f"- Broken links: {len(results['broken_links'])}")

        # Display recommendations
        if results.get("recommendations"):
            click.echo("\n💡 Top Recommendations:")
            for idx, rec in enumerate(results["recommendations"][:5], 1):
                click.echo(f"{idx}. {rec['message']}")

        # Generate action plan
        action_plan = auditor.generate_action_plan()

        # Save results if output file provided
        if output:
            # Save action plan to file
            with open(output, "w") as f:
                f.write(action_plan)
            click.echo(f"\n✅ Audit results saved to: {output}")
        else:
            # Display action plan summary
            click.echo("\n📝 SEO Action Plan:")
            click.echo("-------------------")
            # Display first 20 lines of action plan
            action_plan_lines = action_plan.split("\n")
            for line in action_plan_lines[:20]:
                click.echo(line)
            if len(action_plan_lines) > 20:
                click.echo("... (use --output to save the full action plan)")

    except Exception as e:
        click.echo(f"❌ Error during site audit: {str(e)}")
        import traceback

        click.echo(traceback.format_exc())
        sys.exit(1)


@cli.command("backlink-research")
@click.option("--domain", required=True, help="Domain to research")
@click.option("--competitors", help="Comma-separated list of competitor domains")
@click.option("--output", help="Output file path for backlink report")
@click.option("--limit", default=10, help="Number of top opportunities to display")
@click.option(
    "--generate-templates", is_flag=True, help="Generate outreach email templates"
)
def backlink_research(
    domain: str,
    competitors: Optional[str],
    output: Optional[str] = None,
    limit: int = 10,
    generate_templates: bool = False,
) -> None:
    """Research backlink opportunities."""
    config = load_config()

    # Validate required API keys - make ahrefs_key or semrush_key optional
    # since we have mock implementation
    api_keys_available = []
    for key in ["ahrefs_key", "semrush_key"]:
        if config.get("apis", {}).get(key):
            api_keys_available.append(key)

    if not api_keys_available:
        click.echo("⚠️ No backlink API keys found. Using mock data for demonstration.")
        click.echo(
            "For production use, add AHREFS_API_KEY or SEMRUSH_API_KEY to your .env file."
        )

    comp_list = competitors.split(",") if competitors else []
    click.echo(f"🔗 Researching backlink opportunities for: {domain}")
    if comp_list:
        click.echo(f"Comparing against competitors: {', '.join(comp_list)}")

    # Import the improved backlink analyzer
    from seo_agent.core.backlink_analyzer_improved import BacklinkAnalyzer

    analyzer = BacklinkAnalyzer(config)

    try:
        # Analyze backlinks
        click.echo("\n🔍 Analyzing backlink profile... (this may take a moment)")
        results = analyzer.analyze_backlinks(domain, comp_list)

        # Display summary
        click.echo("\n📊 Backlink Analysis Summary:")
        click.echo(f"- Domain: {results['domain']}")
        click.echo(f"- Total backlinks: {results['summary']['total_backlinks']}")
        click.echo(
            f"- Unique referring domains: {results['summary']['unique_domains']}"
        )
        click.echo(f"- Dofollow links: {results['summary']['dofollow_count']}")
        click.echo(f"- Nofollow links: {results['summary']['nofollow_count']}")

        # Show competitors analyzed
        if comp_list:
            click.echo("\n🔍 Competitor Analysis:")
            for comp_domain, comp_data in results["competitors"].items():
                comp_backlinks = len(comp_data.get("backlinks", []))
                click.echo(f"- {comp_domain}: {comp_backlinks} backlinks")

        # Show top opportunities
        opportunities = results.get("opportunities", [])
        if opportunities:
            click.echo(
                f"\n💡 Top {min(limit, len(opportunities))} Backlink Opportunities:"
            )
            for idx, opp in enumerate(opportunities[:limit], 1):
                domain_auth = opp.get("domain_authority", "N/A")
                link_type = opp.get("link_type", "unknown")
                competitor = opp.get("competitor", "N/A")
                score = opp.get("opportunity_score", 0)
                click.echo(
                    f"{idx}. {opp['source_domain']} (DA: {domain_auth}, {link_type}, via {competitor}, score: {score})"
                )

        # Generate outreach templates if requested
        if generate_templates:
            click.echo("\n✉️ Generating outreach email templates...")
            templates = analyzer.generate_outreach_templates()

            for template_type, content in templates.items():
                click.echo(f"\n📧 Template for {template_type}:")
                # Show first few lines of each template
                preview_lines = content.split("\n")[:5]
                for line in preview_lines:
                    click.echo(line)
                click.echo("...")

        # Save results if output file provided
        if output:
            # Generate default output filename if not provided with a file extension
            if not output.endswith((".json", ".csv", ".txt")):
                output = f"{output}.json"

            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)

            # Save results to output file
            with open(output, "w") as f:
                json.dump(results, f, indent=2)
            click.echo(f"\n✅ Backlink analysis saved to: {output}")

            # Offer to export top opportunities to CSV
            csv_path = output.replace(".json", ".csv")
            if require_approval(
                "Export top opportunities to CSV",
                f"{min(100, len(opportunities))} opportunities",
                config,
            ):
                # Export to CSV
                with open(csv_path, "w") as f:
                    f.write(
                        "source_domain,source_url,domain_authority,link_type,competitor,opportunity_score\n"
                    )
                    for opp in opportunities[:100]:  # Limit to top 100
                        source_domain = opp.get("source_domain", "").replace(",", " ")
                        source_url = opp.get("source_url", "").replace(",", " ")
                        domain_authority = opp.get("domain_authority", "")
                        link_type = opp.get("link_type", "unknown")
                        competitor = opp.get("competitor", "").replace(",", " ")
                        score = opp.get("opportunity_score", 0)
                        f.write(
                            f"{source_domain},{source_url},{domain_authority},{link_type},{competitor},{score}\n"
                        )
                click.echo(f"📤 Exported to: {csv_path}")

    except Exception as e:
        click.echo(f"❌ Error during backlink analysis: {str(e)}")
        import traceback

        click.echo(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    cli()
