# SEO AI Agent

A command-line/API-first SEO automation tool that focuses on core AI-powered SEO tasks with minimal infrastructure dependencies.

## Overview

SEO AI Agent is a simplified SEO automation tool designed for technical users who need effective SEO assistance without complex UIs or infrastructure. It uses AI to automate common SEO tasks like keyword research, content optimization, site auditing, and backlink analysis.

## Features

- 🔍 **Keyword Research Engine**: Expand seed keywords using DSPy AI, analyze competition via free APIs, and export to CSV/JSON.
- ✍️ **Content Optimizer**: Analyze and score content, get AI-powered optimization suggestions, and generate meta tags.
- 🔗 **Backlink Analyzer**: Analyze backlink profiles, identify opportunities, and generate outreach templates.
- 🔧 **Site Auditor**: Perform technical SEO crawling, detect common issues, and get prioritized recommendations.

## Installation

```bash
# Install Poetry if you don't have it
curl -sSL https://install.python-poetry.org | python3 -

# Clone the repository
git clone https://github.com/yourusername/seo-agent.git
cd seo-agent

# Install dependencies
poetry install

# For development, install dev dependencies
poetry install --with dev

# Run the application
poetry run python main.py keyword-research --seed "digital marketing" --industry "saas"

# Or using the installed script (after poetry install)
poetry run seo-agent keyword-research --seed "digital marketing" --industry "saas"
```

## Usage

### Keyword Research

```bash
poetry run python main.py keyword-research --seed "digital marketing" --industry "saas"
```

Example output (keywords_report_[date].json):
```json
{
  "seed_keyword": "digital marketing",
  "industry": "saas",
  "total_keywords": 15,
  "keywords": [
    {
      "keyword": "Digital marketing strategies for SaaS",
      "intent": "informational",
      "competition": "medium"
    },
    {
      "keyword": "SaaS digital marketing agency",
      "intent": "informational",
      "competition": "medium"
    },
    {
      "keyword": "Best digital marketing tools for SaaS",
      "intent": "informational",
      "competition": "medium"
    }
  ],
  "intent_groups": {
    "informational": [
      "Digital marketing strategies for SaaS",
      "SaaS digital marketing agency",
      "Best digital marketing tools for SaaS"
      // ... more keywords
    ]
  }
}
```

The tool generates comprehensive keyword reports with search intent analysis and competition metrics. Reports are saved in the `data/exports` directory.

### Running Without API Keys

There are two ways to run the tool without real API keys:

#### 1. Demo Mode (Explicit Mock Data)

For testing without API keys, you can use the mock keyword demo script:

```bash
# Run directly with Poetry
poetry run python tests/mock/simple_keyword_demo.py --seed "digital marketing" --industry "saas" --auto-csv

# Or use the Makefile
make mock
```

This will generate mock keyword data and save it to both JSON and CSV formats in the `data/exports` directory.

#### 2. Configuring Testing Mode in config.yaml

Alternatively, you can explicitly enable mock data usage in your configuration:

```yaml
# Testing Settings
testing:
  use_mock_data: true
```

This will make all modules use mock data instead of making real API calls. It's useful for development and testing without consuming API credits.

#### New Example Script

A new example script is available that demonstrates proper error handling and the improved keyword generation process:

```bash
# Run the new example script
poetry run python examples/keyword_generator_demo.py --seed "digital marketing" --industry "saas"
```

This script provides detailed logging about the keyword generation process and will raise clear errors if API keys are missing.

### Content Optimization

```bash
poetry run python main.py optimize-content --file "blog_post.txt" --keywords "keywords.json"
```

### Site Audit

```bash
poetry run python main.py audit-site --domain "example.com" --depth 50
```

### Backlink Research

```bash
poetry run python main.py backlink-research --domain "example.com" --competitors "comp1.com,comp2.com"
```

## Configuration

### API Keys Setup

1. Create a `.env` file in the project root:
   ```bash
   touch .env
   ```

2. Edit `.env` and add your API keys:
   ```
   # Required for AI-powered features
   OPENAI_API_KEY=your_openai_api_key_here

   # Optional keys for additional functionality
   SERPAPI_KEY=your_serpapi_key_here
   AHREFS_API_KEY=your_ahrefs_api_key_here
   SEMRUSH_API_KEY=your_semrush_api_key_here
   ```

Required API keys depend on the features you use:
- Keyword Research: OpenAI API key, SerpAPI key (optional)
- Content Optimization: OpenAI API key
- Backlink Analysis: OpenAI API key, Ahrefs API key (optional)
- Site Auditing: OpenAI API key

> **Important:** The new error handling system will now raise clear errors if required API keys are missing, instead of silently falling back to mock data. This helps ensure you're getting real AI-generated results.

### Configuration File

Edit the `config.yaml` file to customize your settings:

```yaml
# Default Settings
defaults:
  max_keywords: 100
  crawl_depth: 50
  approval_required: true
  export_format: "json"

# Output Preferences
output:
  reports_folder: "./data/exports"
  auto_timestamp: true
  email_reports: false

# AI Settings
ai:
  model: "gpt-4-turbo-preview"
  max_tokens: 2000
  temperature: 0.3

# API Keys (will be overridden by environment variables if present)
apis:
  # OpenAI API key can also be set in .env file as OPENAI_API_KEY
  openai_key: ""
  # Other API keys can be added here

# Testing Settings
testing:
  # Set to true to explicitly use mock data instead of real API calls
  use_mock_data: false

# Fallback Settings
fallbacks:
  # Controls whether to fall back to mock data on API errors
  # Set to false to prevent silent fallbacks to mock data
  allow_mock_on_error: false
```

The newly added testing and fallback settings help control when mock data is used:

- `testing.use_mock_data`: When set to `true`, the system will explicitly use mock data instead of making API calls
- `fallbacks.allow_mock_on_error`: When set to `true`, the system will fall back to mock data if API calls fail; when `false`, it will raise errors instead

## Development

### Code Quality Tools

This project uses the following tools to maintain code quality:

- **Ruff**: Fast Python linter and formatter (replaces Black, isort, and Flake8)
- **MyPy**: Static type checker
- **pre-commit**: Git hooks for automated checks
- **pytest**: Testing framework
- **pytest-cov**: Test coverage reporting
- **pytest-mock**: Mocking support for tests

### Setup Development Environment

```bash
# Install development dependencies
poetry install --with dev

# Set up pre-commit hooks
poetry run pre-commit install
```

### Running Linting Tools

```bash
# Format code with Ruff
poetry run ruff format seo_agent

# Run linting with Ruff
poetry run ruff check seo_agent

# Run type checking with MyPy
poetry run mypy seo_agent
```

Or use the provided Makefile:
```bash
make format
make lint
make typecheck
make all  # Run all checks
```

### Running Tests

The project uses pytest for testing with a comprehensive test suite covering all core modules. The test suite includes unit tests for all functionality with proper mocking of external dependencies.

#### Test Structure

- **Unit Tests**: Tests for individual components in isolation
- **Integration Tests**: Tests for component interactions
- **Mock Tests**: Separate tests using mock data for development without API keys

#### Test Command Reference

```bash
# Run all tests
poetry run pytest

# Run only unit tests
poetry run pytest -m unit

# Run only integration tests
poetry run pytest -m integration

# Run with coverage report
poetry run pytest --cov=seo_agent

# Run tests for a specific module
poetry run pytest tests/core/test_keyword_engine.py

# Run a specific test
poetry run pytest tests/core/test_keyword_engine.py::TestKeywordEngine::test_init
```

Or use the provided Makefile:
```bash
make test
make test-unit
make test-integration
make test-cov
```

#### Writing New Tests

When adding new features, please include tests that verify the functionality. For examples of how to write tests, see the existing test files in the `tests/core/` directory.

```python
# Example of a simple test
def test_my_feature(sample_config):
    # Arrange
    my_component = MyComponent(sample_config)

    # Act
    result = my_component.my_feature("test input")

    # Assert
    assert "expected output" in result
    assert result["status"] == "success"
```

## Output

All reports and exports are saved to the `data/exports` directory by default. The tool generates various output formats:

- JSON for programmatic use
- CSV for spreadsheet analysis
- HTML for readable reports
- Markdown for documentation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

Before submitting a PR, please make sure your code passes all quality checks and tests:

```bash
# Run all code quality checks and tests
make all

# Run specific checks
make format  # Format code with Ruff
make lint    # Check code style with Ruff
make typecheck  # Check types with MyPy
make test    # Run all tests
```

The project uses GitHub Actions for CI/CD, which will automatically run all checks and tests on your PR. To ensure your PR is accepted smoothly, make sure all tests pass locally before submitting.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
