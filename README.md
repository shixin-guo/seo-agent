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

### Running Without API Keys (Demo Mode)

For testing without API keys, use the mock keyword demo script:

```bash
# Run directly with Poetry
poetry run python tests/mock/simple_keyword_demo.py --seed "digital marketing" --industry "saas" --auto-csv

# Or use the Makefile
make mock
```

This will generate mock keyword data and save it to both JSON and CSV formats in the `data/exports` directory.

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

1. Copy the template environment file:
   ```bash
   cp .env.template .env
   ```

2. Edit `.env` and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SERPAPI_KEY=your_serpapi_key_here
   AHREFS_API_KEY=your_ahrefs_api_key_here  # Optional
   SEMRUSH_API_KEY=your_semrush_api_key_here  # Optional
   ```

Required API keys depend on the features you use:
- Keyword Research: OpenAI API key, SerpAPI key
- Content Optimization: OpenAI API key
- Backlink Analysis: OpenAI API key, Ahrefs API key
- Site Auditing: OpenAI API key

### Configuration File

Edit the `config.yaml` file to customize your settings:

```yaml
# Default Settings
defaults:
  max_keywords: 100
  crawl_depth: 50
  approval_required: true
  export_format: "json"
```

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
