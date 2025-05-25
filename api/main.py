"""FastAPI backend for SEO Agent.

This module provides a RESTful API for the SEO Agent, enabling frontend applications
to interact with the core SEO functionality.
"""

import os
import sys
import time
from typing import Any, Dict, List, Optional

import yaml
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add project root to Python path

# Import SEO Agent core modules
from seo_agent.core.advanced_content_optimizer import AdvancedContentOptimizer
from seo_agent.core.backlink_analyzer_improved import BacklinkAnalyzer
from seo_agent.core.content_optimizer import ContentOptimizer
from seo_agent.core.keyword_engine import KeywordEngine
from seo_agent.core.site_auditor_improved import SiteAuditorImproved

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="SEO Agent API",
    description="API for the SEO Agent tool - AI-powered SEO automation",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load configuration
def load_config() -> Dict[str, Any]:
    """Load and merge configuration from YAML file and environment variables.

    Returns:
        Dict[str, Any]: Configuration dictionary with API keys and settings.
    """
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.yaml"
    )
    with open(config_path) as f:
        config: Dict[str, Any] = yaml.safe_load(f)

    # Add API keys from environment variables
    api_keys: Dict[str, Optional[str]] = {
        "openai_key": os.getenv("OPENAI_API_KEY"),
        "serpapi_key": os.getenv("SERPAPI_KEY"),
        "ahrefs_key": os.getenv("AHREFS_API_KEY"),
        "semrush_key": os.getenv("SEMRUSH_API_KEY"),
    }

    # Remove None values
    api_keys_filtered: Dict[str, str] = {
        k: v for k, v in api_keys.items() if v is not None
    }

    # Merge with config
    if "apis" not in config:
        config["apis"] = {}
    config["apis"].update(api_keys_filtered)

    return config


# Pydantic models for API requests/responses
class KeywordRequest(BaseModel):
    seed: str
    industry: Optional[str] = None


class ContentOptimizationRequest(BaseModel):
    content: str
    keywords: Optional[List[Dict[str, Any]]] = None
    use_advanced: bool = True
    creative: bool = False


class SiteAuditRequest(BaseModel):
    domain: str
    max_pages: int = 50


class BacklinkAnalysisRequest(BaseModel):
    domain: str
    competitors: Optional[List[str]] = None
    generate_templates: bool = False


# API routes
@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {"message": "SEO Agent API is running"}


@app.post("/api/keywords")
async def generate_keywords(request: KeywordRequest) -> Dict[str, Any]:
    """Generate keyword research based on a seed keyword."""
    try:
        config = load_config()
        engine = KeywordEngine(config)
        results = engine.generate_keywords(request.seed, request.industry)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/optimize-content")
async def optimize_content(
    content_file: UploadFile = File(...),
    keywords_file: Optional[UploadFile] = None,
    use_advanced: bool = Form(True),
    creative: bool = Form(False),
) -> Dict[str, Any]:
    """Optimize content for SEO."""
    try:
        config = load_config()

        # Save uploaded content to temporary file
        content_path = f"/tmp/{content_file.filename}"
        with open(content_path, "wb") as f:
            f.write(await content_file.read())

        # Save keywords file if provided
        keywords_path: Optional[str] = None
        if keywords_file:
            keywords_path = f"/tmp/{keywords_file.filename}"
            with open(keywords_path, "wb") as f:
                f.write(await keywords_file.read())

        result: Dict[str, Any]
        if use_advanced:
            # Use advanced optimizer
            if creative:
                # Make a copy of the config to avoid modifying the original
                creative_config = config.copy()
                if "ai" not in creative_config:
                    creative_config["ai"] = {}

                # Set higher temperature for more creative results
                creative_config["ai"]["temperature"] = 0.9

                # Add timestamp to seed random variation
                timestamp = int(time.time())
                if "randomization" not in creative_config:
                    creative_config["randomization"] = {}
                creative_config["randomization"]["seed"] = timestamp

                optimizer = AdvancedContentOptimizer(creative_config)
            else:
                optimizer = AdvancedContentOptimizer(config)

            # Handle the case where keywords_path is None
            kw_path = "" if keywords_path is None else keywords_path
            optimized_content = optimizer.fully_optimize_content(content_path, kw_path)
            result = {
                "optimized_content": optimized_content,
                "analysis": {},  # Advanced optimizer doesn't provide separate analysis
                "suggestions": [],  # Advanced optimizer doesn't provide separate suggestions
            }
        else:
            # Use basic optimizer
            basic_optimizer = ContentOptimizer(config)
            result = basic_optimizer.optimize_content(content_path, keywords_path)

        # Clean up temporary files
        os.remove(content_path)
        if keywords_path:
            os.remove(keywords_path)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/audit-site")
async def audit_site(request: SiteAuditRequest) -> Dict[str, Any]:
    """Perform a technical SEO audit on a website."""
    try:
        config = load_config()
        auditor = SiteAuditorImproved(config)
        results = auditor.audit_site(request.domain, request.max_pages)

        # Generate action plan
        action_plan = auditor.generate_action_plan()

        # Add action plan to results
        results["action_plan"] = action_plan

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/backlink-analysis")
async def analyze_backlinks(request: BacklinkAnalysisRequest) -> Dict[str, Any]:
    """Research backlink opportunities."""
    try:
        config = load_config()
        analyzer = BacklinkAnalyzer(config)

        # Convert competitors list
        competitors = request.competitors if request.competitors else []

        # Analyze backlinks
        results = analyzer.analyze_backlinks(request.domain, competitors)

        # Generate outreach templates if requested
        if request.generate_templates:
            templates = analyzer.generate_outreach_templates()
            results["templates"] = templates

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run app with uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
