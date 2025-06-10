#!/usr/bin/env python

"""FastAPI server for the SEO Agent tool.

This module provides a RESTful API for various SEO operations
including keyword research, content optimization, site auditing, and backlink analysis.
"""

import os
import sys
import time
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import core modules and utilities
from seo_agent.core.keyword_engine import KeywordEngine
from seo_agent.core.database import Article, ArticleDatabase
from seo_agent.core.article_generator import ArticleGenerator
from utils import load_config

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


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


class ArticleRequest(BaseModel):
    title: str
    content: str
    keywords: List[str] = []
    meta_description: Optional[str] = None
    status: str = "draft"


class ArticleGenerateRequest(BaseModel):
    seed_keyword: str
    industry: Optional[str] = None
    title: Optional[str] = None
    min_length: int = 800


class ArticleUpdateRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    keywords: Optional[List[str]] = None
    meta_description: Optional[str] = None
    status: Optional[str] = None


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
            from seo_agent.core.advanced_content_optimizer import (
                AdvancedContentOptimizer,
            )

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
            from seo_agent.core.content_optimizer import ContentOptimizer

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
        from seo_agent.core.site_auditor_improved import SiteAuditorImproved

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
        from seo_agent.core.backlink_analyzer_improved import BacklinkAnalyzer

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


config = load_config()
article_db = ArticleDatabase(config)
article_generator = ArticleGenerator(config)


@app.get("/api/articles")
async def get_articles(limit: int = 100, offset: int = 0, status: Optional[str] = None):
    """Get list of articles with pagination."""
    try:
        articles = article_db.get_articles(limit=limit, offset=offset, status=status)
        return {"articles": articles, "total": len(articles)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/articles/{article_id}")
async def get_article(article_id: int):
    """Get a specific article by ID."""
    try:
        article = article_db.get_article(article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return article
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/articles")
async def create_article(request: ArticleRequest):
    """Create a new article."""
    try:
        article = Article(
            title=request.title,
            content=request.content,
            keywords=request.keywords,
            meta_description=request.meta_description,
            status=request.status
        )
        created_article = article_db.create_article(article)
        return created_article
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/articles/{article_id}")
async def update_article(article_id: int, request: ArticleUpdateRequest):
    """Update an existing article."""
    try:
        existing_article = article_db.get_article(article_id)
        if not existing_article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        updated_data = existing_article.dict()
        for field, value in request.dict(exclude_unset=True).items():
            if value is not None:
                updated_data[field] = value
        
        updated_article = Article(**updated_data)
        result = article_db.update_article(article_id, updated_article)
        
        if not result:
            raise HTTPException(status_code=404, detail="Article not found")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/articles/{article_id}")
async def delete_article(article_id: int):
    """Delete an article."""
    try:
        deleted = article_db.delete_article(article_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Article not found")
        return {"message": "Article deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/articles/generate")
async def generate_article(request: ArticleGenerateRequest):
    """Generate a new article from keywords."""
    try:
        article = article_generator.generate_article_from_keywords(
            seed_keyword=request.seed_keyword,
            industry=request.industry,
            title=request.title,
            min_length=request.min_length
        )
        created_article = article_db.create_article(article)
        return created_article
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/articles/search")
async def search_articles(q: str, limit: int = 50):
    """Search articles by title or content."""
    try:
        articles = article_db.search_articles(query=q, limit=limit)
        return {"articles": articles, "total": len(articles)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run app with uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
