# SEO Agent API

A FastAPI backend for the SEO Agent tool, providing RESTful API access to all SEO features.

## Features

- Keyword Research API
- Content Optimization API
- Site Auditing API
- Backlink Analysis API

## Getting Started

### Prerequisites

- Python 3.9+
- Poetry (for Python dependency management)

### Installation

1. Clone the repository
2. Set up the environment:

```bash
# Navigate to the project root
cd /path/to/seo-agent

# Install dependencies using Poetry
poetry install

# Set up environment variables
# Create a .env file with the required API keys:
# OPENAI_API_KEY=your-openai-key
# SERPAPI_KEY=your-serpapi-key (optional)
# AHREFS_API_KEY=your-ahrefs-key (optional)
# SEMRUSH_API_KEY=your-semrush-key (optional)
```

### Running the API

Start the FastAPI backend:

```bash
# From the api directory
cd api
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

FastAPI automatically generates interactive documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Keyword Research

```
POST /api/keywords
```

Generate keyword research based on a seed keyword.

**Request Body:**
```json
{
  "seed": "digital marketing",
  "industry": "technology"
}
```

### Content Optimization

```
POST /api/optimize-content
```

Optimize content for SEO.

**Form Data:**
- `content_file`: Content file to optimize
- `keywords_file` (optional): Keywords JSON file
- `use_advanced`: Boolean flag for using advanced optimization (default: true)
- `creative`: Boolean flag for using creative mode (default: false)

### Site Auditing

```
POST /api/audit-site
```

Perform a technical SEO audit on a website.

**Request Body:**
```json
{
  "domain": "example.com",
  "max_pages": 50
}
```

### Backlink Analysis

```
POST /api/backlink-analysis
```

Research backlink opportunities.

**Request Body:**
```json
{
  "domain": "example.com",
  "competitors": ["competitor1.com", "competitor2.com"],
  "generate_templates": true
}
```

## Testing

```bash
# From the project root
pytest
```

## Deployment

The API can be deployed using various methods:

1. Docker container
2. Serverless deployment (e.g., AWS Lambda with API Gateway)
3. Traditional web server (e.g., using Gunicorn)

Example Docker deployment:

```bash
# Build Docker image
docker build -t seo-agent-api .

# Run Docker container
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key seo-agent-api
```

## License

See the LICENSE file for details.
