#!/usr/bin/env python3

"""Mock data generator for testing the SEO Agent without API keys.

This script creates sample keyword data that can be used for testing.
"""

import json
import os
from datetime import datetime
from typing import Any, Optional


# Create mock keyword data
def generate_mock_keywords(seed_keyword: str, industry: str) -> dict[str, Any]:
    """Generate mock keyword data for testing."""
    mock_data = {
        "seed_keyword": seed_keyword,
        "industry": industry or "Not specified",
        "total_keywords": 15,
        "keywords": [
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
        ],
    }

    # Add intent groups
    intent_groups = {}
    for kw in mock_data["keywords"]:
        intent = kw.get("intent", "informational")
        if intent not in intent_groups:
            intent_groups[intent] = []
        intent_groups[intent].append(kw["keyword"])

    mock_data["intent_groups"] = intent_groups

    return mock_data


def save_mock_data(data: dict[str, Any], output_path: Optional[str] = None) -> str:
    """Save mock data to a file."""
    if not output_path:
        timestamp = datetime.now().strftime("%Y_%m_%d")
        output = f"data/exports/keywords_report_{timestamp}.json"
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output), exist_ok=True)
    else:
        output = output_path

    with open(output, "w") as f:
        json.dump(data, f, indent=2)

    return output


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate mock keyword data for testing"
    )
    parser.add_argument("--seed", required=True, help="Seed keyword")
    parser.add_argument("--industry", default="saas", help="Industry for context")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    data = generate_mock_keywords(args.seed, args.industry)
    file_path = save_mock_data(data, args.output)

    print(f"✅ Mock keyword data generated and saved to: {file_path}")
    print(f"📊 Total keywords: {data['total_keywords']}")
    print(f"🔍 Intent groups: {', '.join(data['intent_groups'].keys())}")
