# SEO Agent UI

A modern web interface for the SEO Agent tool, built with Next.js, React, shadcn/ui, and FastAPI.

## Features

- Keyword Research
- Content Optimization
- Site Auditing
- Backlink Analysis
- Modern, responsive UI with dark mode support

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Poetry (for Python dependency management)

### Installation

1. Clone the repository
2. Set up the backend:

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

3. Set up the frontend:

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install
```

### Running the Application

1. Start the FastAPI backend:

```bash
# From the project root
cd api
uvicorn main:app --reload
```

2. Start the Next.js frontend:

```bash
# From the frontend directory
npm run dev
```

3. Open your browser and navigate to `http://localhost:3000`

## API Integration

The frontend communicates with the FastAPI backend using RESTful API calls. The API client is located at `src/lib/api/api-client.ts`.

You can configure the API URL by setting the `NEXT_PUBLIC_API_URL` environment variable.

## Testing

The application includes tests for both frontend components and backend functionality.

### Frontend Tests

```bash
# From the frontend directory
npm run test
```

### Backend Tests

```bash
# From the project root
pytest
```

## Deployment

1. Build the frontend:

```bash
# From the frontend directory
npm run build
```

2. Deploy the FastAPI backend using your preferred method (e.g., Docker, serverless, etc.)
3. Ensure the frontend is configured to communicate with your deployed backend API

## License

See the LICENSE file for details.
