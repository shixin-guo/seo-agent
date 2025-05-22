#!/usr/bin/env python3

import yaml
import json
from seo_agent.core.keyword_engine import KeywordEngine

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Initialize engine
engine = KeywordEngine(config)

# Create mock data
print('Testing mock keyword generation...')
mock_keywords = [
    {'keyword': 'seo tools', 'intent': 'commercial', 'competition': 'high'},
    {'keyword': 'seo strategies', 'intent': 'informational', 'competition': 'medium'},
    {'keyword': 'how to improve seo', 'intent': 'informational', 'competition': 'low'}
]

# Create mock generator
class MockGenerator:
    def generate_keywords(self, seed, industry):
        return mock_keywords

# Replace generator with mock
engine.keyword_generator = MockGenerator()

# Generate keywords
results = engine.generate_keywords('seo', 'marketing')

# Print results
print(json.dumps(results, indent=2))