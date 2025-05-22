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

    while True:
        response = click.prompt("Proceed? (y/n/details)", type=str, default="y")
        if response.lower() == "details":
            click.echo("Detailed preview not implemented yet.")
            continue
        elif response.lower() in ["y", "yes"]:
            return True
        else:
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
    results = engine.generate_keywords(seed, industry)

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
                intent = kw.get("intent", "informational")
                competition = kw.get("competition", "medium")
                f.write(f"{kw['keyword']},{intent},{competition}\n")
        click.echo(f"📤 Exported to: {csv_path}")


@cli.command("optimize-content")
@click.option("--file", required=True, help="Content file to optimize")
@click.option("--keywords", help="Keywords JSON file to use for optimization")
def optimize_content(file: str, keywords: Optional[str]) -> None:
    """Optimize content for SEO."""
    config = load_config()

    # Validate required API keys
    validate_api_keys(config, ["openai_key"])

    click.echo(f"✍️ Optimizing content: {file}")

    # Import the module only when needed to avoid circular imports

    # Future implementation
    click.echo("Not implemented yet. Coming soon!")


@cli.command("audit-site")
@click.option("--domain", required=True, help="Domain to audit")
@click.option("--depth", default=50, help="Maximum pages to crawl")
def audit_site(domain: str, depth: int) -> None:
    """Perform a technical SEO audit on a website."""
    config = load_config()

    # Validate required API keys
    validate_api_keys(config, ["openai_key"])

    click.echo(f"🔧 Auditing site: {domain} (max {depth} pages)")

    # Import the module only when needed to avoid circular imports

    # Future implementation
    click.echo("Not implemented yet. Coming soon!")


@cli.command("backlink-research")
@click.option("--domain", required=True, help="Domain to research")
@click.option("--competitors", help="Comma-separated list of competitor domains")
def backlink_research(domain: str, competitors: Optional[str]) -> None:
    """Research backlink opportunities."""
    config = load_config()

    # Validate required API keys
    validate_api_keys(config, ["openai_key", "ahrefs_key"])

    comp_list = competitors.split(",") if competitors else []
    click.echo(f"🔗 Researching backlink opportunities for: {domain}")
    if comp_list:
        click.echo(f"Comparing against competitors: {', '.join(comp_list)}")

    # Import the module only when needed to avoid circular imports
    # Commented out to avoid unused variable warning until implementation is complete
    # from seo_agent.core.backlink_analyzer import BacklinkAnalyzer
    # analyzer = BacklinkAnalyzer(config)

    # Future implementation
    click.echo("Not implemented yet. Coming soon!")


if __name__ == "__main__":
    cli()
