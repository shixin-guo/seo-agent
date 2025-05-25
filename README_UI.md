# SEO Agent UI

A complete UI solution for the SEO Agent tool, built with React, Next.js, shadcn/ui, and FastAPI.

![SEO Agent UI](https://placekitten.com/800/400)

## Overview

The SEO Agent UI is a modern web application that provides a user-friendly interface for the powerful SEO Agent tool. It enables users to perform SEO tasks through an intuitive GUI, including keyword research, content optimization, site auditing, and backlink analysis.

## Features

### Keyword Research

- Generate keyword ideas from seed keywords
- Filter by search intent (informational, commercial, transactional, navigational)
- View competition metrics for each keyword
- Export results to CSV or JSON formats

### Content Optimization

- Upload content files or enter content directly
- Basic and advanced AI-powered optimization options
- Detailed content analysis with readability scores
- Specific optimization suggestions
- Download optimized content

### Site Auditor

- Technical SEO site crawling and analysis
- Issue detection and prioritization
- Comprehensive recommendations
- Downloadable action plans
- Progress tracking during audits

### Backlink Analyzer

- Analyze backlink profiles
- Compare with competitors
- Identify high-value backlink opportunities
- Generate outreach email templates
- Export opportunities to CSV or JSON

## Architecture

The application follows a modern web architecture:

- **Frontend**: React + Next.js + shadcn/ui
  - Type-safe with TypeScript
  - Component-based architecture
  - Responsive design with dark mode support
  - Client-side and server-side rendering

- **Backend**: Python + FastAPI
  - RESTful API endpoints
  - Asynchronous request handling
  - API documentation with Swagger UI
  - Integration with core SEO Agent functionality

## Getting Started

See the [frontend README](./frontend/README.md) and [API README](./api/README.md) for detailed setup instructions.

### Quick Start

1. Clone this repository
2. Set up environment variables
3. Install dependencies:

```bash
# Backend
cd api
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

4. Start the backend:

```bash
cd api
uvicorn main:app --reload
```

5. Start the frontend:

```bash
cd frontend
npm run dev
```

6. Open your browser and go to `http://localhost:3000`

## Testing

The project includes comprehensive testing infrastructure:

- Backend: pytest for API endpoint testing
- Frontend: Jest and React Testing Library for component testing

## License

This project is licensed under the terms of the MIT license.
