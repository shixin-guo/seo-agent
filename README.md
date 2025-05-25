# SEO AI Agent

A comprehensive SEO automation tool with both API server and CLI interface that focuses on core AI-powered SEO tasks.

## Overview

SEO AI Agent is a versatile SEO automation tool that uses AI to automate common SEO tasks like keyword research, content optimization, site auditing, and backlink analysis. It provides both a RESTful API for integration with your applications and a command-line interface for direct usage.

## Features

- 🚀 **RESTful API**: Complete FastAPI server with automatic documentation and OpenAPI schema
- 💻 **CLI Interface**: Command-line tools for automation and scripting
- 🔍 **Keyword Research Engine**: Expand seed keywords using DSPy AI, analyze competition via free APIs
- ✍️ **Content Optimizer**: Analyze and score content, get AI-powered optimization suggestions
- 🔗 **Backlink Analyzer**: Analyze backlink profiles, identify opportunities, and generate outreach templates
- 🔧 **Site Auditor**: Perform technical SEO crawling, detect common issues, and get prioritized recommendations
- 🖥️ **Modern Web UI**: Access all features through an intuitive web interface built with Next.js and React
- 🐳 **Docker Support**: Deploy the entire stack with Docker Compose for easy setup

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

# CLI Usage
poetry run python cli.py keyword-research --seed "digital marketing" --industry "saas"

# API Server Usage
poetry run python api.py
```

## Usage

### CLI Interface

#### Keyword Research
```bash
poetry run python cli.py keyword-research --seed "digital marketing" --industry "saas"
```

#### Content Optimization
```bash
poetry run python cli.py optimize-content --file "blog_post.txt" --keywords "keywords.json"
```

#### Site Audit
```bash
poetry run python cli.py audit-site --domain "example.com" --depth 50
```

#### Backlink Research
```bash
poetry run python cli.py backlink-research --domain "example.com" --competitors "comp1.com,comp2.com"
```

#### Start API Server via CLI
```bash
poetry run python cli.py serve --host 0.0.0.0 --port 8000 --reload
```

### API Server

Start the FastAPI server directly:

```bash
# Start the API server (default: http://0.0.0.0:8000)
poetry run python api.py

# Or use CLI command
poetry run python cli.py serve

# Custom host and port
poetry run python cli.py serve --host 127.0.0.1 --port 9000

# Enable auto-reload for development
poetry run python cli.py serve --reload
```

### API Endpoints

The API provides the following endpoints:

#### Health Check
- `GET /` - Server health check

#### Keyword Research
- `POST /api/keywords`
  ```json
  {
    "seed": "digital marketing",
    "industry": "saas"
  }
  ```

#### Content Optimization
- `POST /api/optimize-content`
  - Form data with `content_file` (required)
  - Optional `keywords_file`
  - `use_advanced`: boolean (default: true)
  - `creative`: boolean (default: false)

#### Site Audit
- `POST /api/audit-site`
  ```json
  {
    "domain": "example.com",
    "max_pages": 50
  }
  ```

#### Backlink Analysis
- `POST /api/backlink-analysis`
  ```json
  {
    "domain": "example.com",
    "competitors": ["competitor1.com", "competitor2.com"],
    "generate_templates": false
  }
  ```

### API Documentation

Access the interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Example API Response

Keyword research endpoint response:
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
    }
  ],
  "intent_groups": {
    "informational": [
      "Digital marketing strategies for SaaS",
      "SaaS digital marketing agency"
    ]
  }
}
```

### Testing Without API Keys

You can enable mock data mode for testing without consuming API credits:

```yaml
# In config.yaml
testing:
  use_mock_data: true
```

This will make all API endpoints use mock data instead of making real API calls.

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

Required API keys depend on the endpoints you use:
- **Keyword Research**: OpenAI API key, SerpAPI key (optional)
- **Content Optimization**: OpenAI API key
- **Backlink Analysis**: OpenAI API key, Ahrefs API key (optional)
- **Site Auditing**: OpenAI API key

> **Important:** The API will return HTTP 500 errors if required API keys are missing, unless mock mode is enabled in configuration.

### Configuration File

Edit the `config.yaml` file to customize your settings:

```yaml
# Default Settings
defaults:
  max_keywords: 100
  crawl_depth: 50

# AI Settings
ai:
  model: "gpt-4-turbo-preview"
  max_tokens: 2000
  temperature: 0.3

# API Keys (will be overridden by environment variables if present)
apis:
  openai_key: ""
  serpapi_key: ""
  ahrefs_key: ""
  semrush_key: ""

# Testing Settings
testing:
  # Set to true to use mock data instead of real API calls
  use_mock_data: false

# Fallback Settings
fallbacks:
  # Controls whether to fall back to mock data on API errors
  allow_mock_on_error: false
```

Key configuration options:
- **`testing.use_mock_data`**: Enable mock mode for testing without API calls
- **`fallbacks.allow_mock_on_error`**: Whether to use mock data when API calls fail
- **`ai.temperature`**: Controls AI response creativity (0.0-1.0)

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

The project uses pytest for testing with a comprehensive test suite covering all core modules and API endpoints. The test suite includes unit tests for all functionality with proper mocking of external dependencies.

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

## Using the Web UI

The SEO Agent includes a modern web UI built with Next.js, React, and shadcn/ui. It provides a user-friendly interface to all core SEO features.

### UI Features

- **Responsive Design**: Works on desktop and mobile devices
- **Dark Mode Support**: Toggle between light and dark themes
- **Interactive Dashboards**: Visualize your SEO data
- **Progress Tracking**: Monitor long-running tasks like site audits
- **Export Options**: Download reports in multiple formats

### Starting the UI

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

Then open your browser to `http://localhost:3000` to access the UI.

## Docker Deployment

SEO Agent can be easily deployed using Docker Compose, which sets up both the integrated API server and the web UI.

### Prerequisites

- Docker and Docker Compose installed
- API keys (set in environment variables or .env file)

### Deployment Steps

```bash
# Clone the repository
git clone https://github.com/yourusername/seo-agent.git
cd seo-agent

# Create .env file with your API keys
touch .env
# Edit .env with your API keys

# Start the containers
docker-compose up -d
```

This will start:
- The integrated API server on port 8000
- The web UI on port 3000

You can then access:
- Web UI at `http://localhost:3000`
- API documentation at `http://localhost:8000/docs`

## Recent Updates

### Modular Architecture

- **Separated API and CLI**: Clean separation between `api.py` (FastAPI server) and `cli.py` (command-line interface)
- **Shared Utilities**: Common functionality in `utils.py` for both API and CLI components
- **Direct Entry Points**: Use `python api.py` for server or `python cli.py` for CLI commands

### Enhanced Development Experience

- **Interactive API Documentation**: Swagger UI and ReDoc for easy API exploration
- **Command-Line Tools**: Full-featured CLI for automation and scripting
- **Comprehensive Error Handling**: Clear HTTP status codes and error messages

### Modern Tech Stack

- **FastAPI**: High-performance async API framework with automatic validation
- **Click**: Powerful CLI framework with command grouping and options
- **Pydantic**: Type-safe request/response models
- **Next.js Web UI**: Modern React-based interface for direct usage
- **Docker Support**: Easy deployment with Docker Compose

## License

This project is licensed under the MIT License - see the LICENSE file for details.
