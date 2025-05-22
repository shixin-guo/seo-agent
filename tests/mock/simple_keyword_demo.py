#!/usr/bin/env python3

"""Simplified standalone keyword research demo for SEO Agent.

This script doesn't require any external dependencies or API keys.
"""

import argparse
import json
import os
from datetime import datetime
from typing import Any, Optional


def generate_keywords(
    seed_keyword: str, industry: Optional[str] = None
) -> dict[str, Any]:
    """Generate mock keywords for a seed keyword and industry."""
    industry = industry or "general"

    # Create some mock keyword data
    keywords = [
        {
            "keyword": f"Digital marketing strategies for {industry}",
            "intent": "informational",
            "competition": "medium",
        },
        {
            "keyword": f"{industry} digital marketing agency",
            "intent": "commercial",
            "competition": "high",
        },
        {
            "keyword": f"Best digital marketing tools for {industry}",
            "intent": "informational",
            "competition": "medium",
        },
        {
            "keyword": f"{industry} digital marketing trends",
            "intent": "informational",
            "competition": "low",
        },
        {
            "keyword": f"How to market {industry} products online",
            "intent": "informational",
            "competition": "medium",
        },
        {
            "keyword": f"{industry} digital marketing certification",
            "intent": "transactional",
            "competition": "high",
        },
        {
            "keyword": f"{industry} social media marketing",
            "intent": "informational",
            "competition": "medium",
        },
        {
            "keyword": f"Email marketing for {industry} companies",
            "intent": "informational",
            "competition": "low",
        },
        {
            "keyword": f"{industry} content marketing",
            "intent": "informational",
            "competition": "medium",
        },
        {
            "keyword": f"Digital marketing budget for {industry}",
            "intent": "informational",
            "competition": "low",
        },
        {
            "keyword": f"ROI digital marketing {industry}",
            "intent": "informational",
            "competition": "medium",
        },
        {
            "keyword": f"Digital marketing consultant for {industry}",
            "intent": "commercial",
            "competition": "high",
        },
        {
            "keyword": f"{industry} marketing analytics",
            "intent": "informational",
            "competition": "medium",
        },
        {
            "keyword": f"Digital marketing plan {industry}",
            "intent": "informational",
            "competition": "medium",
        },
        {
            "keyword": f"Lead generation for {industry}",
            "intent": "commercial",
            "competition": "high",
        },
    ]

    # Group by intent
    intent_groups = {}
    for kw in keywords:
        intent = kw["intent"]
        if intent not in intent_groups:
            intent_groups[intent] = []
        intent_groups[intent].append(kw["keyword"])

    # Create the final result
    result = {
        "seed_keyword": seed_keyword,
        "industry": industry,
        "total_keywords": len(keywords),
        "keywords": keywords,
        "intent_groups": intent_groups,
    }

    return result


def save_results(results: dict[str, Any], output: Optional[str] = None) -> str:
    """Save results to a file."""
    # Create exports directory if it doesn't exist
    os.makedirs("data/exports", exist_ok=True)

    # Generate filename if not provided
    if not output:
        timestamp = datetime.now().strftime("%Y_%m_%d")
        output = f"data/exports/keywords_report_{timestamp}.json"

    # Save the file
    with open(output, "w") as f:
        json.dump(results, f, indent=2)

    return output


def export_to_csv(results: dict[str, Any], json_path: str) -> str:
    """Export results to CSV format."""
    csv_path = json_path.replace(".json", ".csv")

    # Simple CSV export
    with open(csv_path, "w") as f:
        # Write header
        f.write("keyword,intent,competition\n")
        # Write data
        for kw in results["keywords"]:
            f.write(f"{kw['keyword']},{kw['intent']},{kw['competition']}\n")

    return csv_path


def main() -> None:
    """Run the keyword research demo."""
    parser = argparse.ArgumentParser(description="SEO Agent Keyword Research Demo")
    parser.add_argument("--seed", required=True, help="Seed keyword to expand from")
    parser.add_argument("--industry", help="Industry for context")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument(
        "--auto-csv", action="store_true", help="Automatically export to CSV"
    )

    args = parser.parse_args()

    print(f"🔍 Performing keyword research for: {args.seed}")
    if args.industry:
        print(f"🏢 Industry context: {args.industry}")

    # Generate keywords
    results = generate_keywords(args.seed, args.industry)

    # Save results
    output_path = save_results(results, args.output)

    # Display summary
    print(f"✅ Keyword research complete. Found {results['total_keywords']} keywords.")
    print("📊 Intent breakdown:")
    for intent, keywords in results["intent_groups"].items():
        print(f"   - {intent}: {len(keywords)} keywords")
    print(f"💾 Results saved to: {output_path}")

    # Export to CSV if requested
    if args.auto_csv:
        csv_path = export_to_csv(results, output_path)
        print(f"📤 Exported to: {csv_path}")


if __name__ == "__main__":
    main()
