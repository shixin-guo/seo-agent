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
# Clone the repository
git clone https://github.com/yourusername/seo-agent.git
cd seo-agent

# Install dependencies
pip install -r requirements.txt

# For development, install dev dependencies
pip install -r requirements-dev.txt
```

## Usage

### Keyword Research

```bash
python main.py keyword-research --seed "digital marketing" --industry "saas"
```

### Content Optimization

```bash
python main.py optimize-content --file "blog_post.txt" --keywords "keywords.json"
```

### Site Audit

```bash
python main.py audit-site --domain "example.com" --depth 50
```

### Backlink Research

```bash
python main.py backlink-research --domain "example.com" --competitors "comp1.com,comp2.com"
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
# API Keys (optional)
apis:
  openai_key: "your-key-here"
  serpapi_key: "optional-for-better-data"

# Default Settings
defaults:
  max_keywords: 100
  crawl_depth: 50
  approval_required: true
  export_format: "json"
```

## Development

### Code Quality Tools

This project uses several tools to maintain code quality:

- **Black**: Code formatter
- **isort**: Import statement organizer
- **Flake8**: Linter
- **MyPy**: Static type checker
- **pre-commit**: Git hooks for automated checks

### Setup Development Environment

1. Run the setup script:
   ```bash
   ./setup_dev.sh
   ```
   This will:
   - Create a virtual environment
   - Install dependencies
   - Set up pre-commit hooks
   - Create a template .env file

   Alternatively, you can set up manually:
   ```bash
   pip install -r requirements-dev.txt
   pre-commit install
   ```

### Running Linting Tools

You can use the provided Makefile to run various code quality checks:

```bash
# Format code with Black and isort
make format

# Run linting with Flake8
make lint

# Run type checking with MyPy
make typecheck

# Run all checks
make all
```

Alternatively, you can run individual tools directly:

```bash
# Format code
black seo_agent main.py
isort seo_agent main.py

# Lint code
flake8 seo_agent main.py

# Type check
mypy seo_agent main.py
```

## Output

All reports and exports are saved to the `data/exports` directory by default. The tool generates various output formats:

- JSON for programmatic use
- CSV for spreadsheet analysis
- HTML for readable reports
- Markdown for documentation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

Before submitting a PR, please make sure your code passes all quality checks:

```bash
make all
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
