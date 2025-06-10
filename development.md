# Development Guide

## Quick Start

```bash
# Install dependencies
poetry install --with dev

# Set up pre-commit hooks
poetry run pre-commit install

# Run development server
poetry run python main.py keyword-research --seed "test" --industry "tech"
```

## Project Structure

```
seo-agent/
├── seo_agent/                 # Core Python package
│   ├── core/                  # Main modules
│   ├── utils/                 # Helper utilities
│   └── templates/             # Templates
├── frontend/                  # Next.js web UI
├── api/                       # FastAPI backend
├── tests/                     # Test suite
└── data/exports/              # Output directory
```

## Development Workflow

### Code Quality

```bash
# Format code
make format
poetry run ruff format .

# Check linting
make lint
poetry run ruff check .

# Type checking
make typecheck
poetry run mypy seo_agent

# Run all checks
make all
```

### Testing

```bash
# Run all tests
make test
poetry run pytest

# Run with coverage
make test-cov
poetry run pytest --cov=seo_agent

# Run specific module
poetry run pytest tests/core/test_keyword_engine.py
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev        # Development server
npm run build      # Production build
npm run lint       # ESLint
npm run test       # Jest tests
```

## Configuration

### Environment Variables

Create `.env` file:
```bash
OPENAI_API_KEY=your_key_here
SERPAPI_KEY=your_key_here
AHREFS_API_KEY=your_key_here
```

### API Key Setup

```bash
# Set up API keys in .env
touch .env
echo "OPENAI_API_KEY=your_key_here" >> .env
```

## Docker Development

```bash
# Start full stack
docker-compose up -d

# Rebuild containers
docker-compose up --build

# View logs
docker-compose logs -f
```

## Adding New Features

1. Create module in `seo_agent/core/`
2. Add tests in `tests/core/`
3. Update CLI in `main.py`
4. Add UI component in `frontend/src/`
5. Run quality checks with `make all`

## Common Commands

```bash
# Run keyword research
poetry run python main.py keyword-research --seed "keyword" --industry "tech"

# Run site audit
poetry run python main.py audit-site --domain "example.com"

# Start UI development
cd frontend && npm run dev

# Start API server
cd api && poetry run uvicorn main:app --reload
```

## Debugging

### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Environment Variables
```bash
# Check API keys are set
echo $OPENAI_API_KEY
```

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run `make all` to verify quality
5. Commit and push changes
6. Create pull request

## Performance Tips

- Use async/await for API calls
- Cache expensive operations
- Implement request timeouts
- Use connection pooling for multiple requests
- Monitor memory usage with large datasets

## Documentation Generation

```bash
# Generate LLM-friendly documentation files
make docs
python scripts/build_llm_docs.py
```
