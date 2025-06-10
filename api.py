#!/usr/bin/env python

"""FastAPI server for the SEO Agent tool.

This module provides a RESTful API for various SEO operations
including keyword research, content optimization, site auditing, and backlink analysis.
"""

import os
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Import core modules and utilities
from seo_agent.core.keyword_engine import KeywordEngine
from seo_agent.core.database import ArticleDatabase, Image
from seo_agent.core.image_alt_generator import ImageAltGenerator
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

config = load_config()
db = ArticleDatabase(config)
image_generator = None

try:
    image_generator = ImageAltGenerator(config)
except ValueError:
    pass


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


class ImageUploadResponse(BaseModel):
    id: int
    filename: str
    original_name: str
    alt_text: Optional[str]
    file_size: int
    mime_type: str
    created_at: str


class ImageListResponse(BaseModel):
    images: List[ImageUploadResponse]
    total: int


class AltTextUpdateRequest(BaseModel):
    alt_text: str


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


@app.post("/api/images/upload", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...)) -> ImageUploadResponse:
    """Upload an image and generate alt text."""
    if not image_generator:
        raise HTTPException(
            status_code=503,
            detail="Image processing service unavailable - OpenAI API key required",
        )

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported image type. Allowed: {', '.join(allowed_types)}",
        )

    images_dir = Path("./data/images")
    images_dir.mkdir(parents=True, exist_ok=True)

    file_extension = Path(file.filename or "image").suffix or ".jpg"
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = images_dir / unique_filename

    try:
        content = await file.read()

        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400, detail="File size too large (max 10MB)"
            )

        with open(file_path, "wb") as f:
            f.write(content)

        validation = image_generator.validate_image(str(file_path))
        if not validation["valid"]:
            file_path.unlink(missing_ok=True)
            raise HTTPException(
                status_code=400, detail=f"Invalid image: {validation['error']}"
            )

        alt_text = image_generator.generate_alt_text(str(file_path))

        image_record = Image(
            filename=unique_filename,
            original_name=file.filename or "unknown",
            alt_text=alt_text,
            file_path=str(file_path),
            file_size=len(content),
            mime_type=file.content_type,
        )

        created_image = db.create_image(image_record)

        return ImageUploadResponse(
            id=created_image.id or 0,
            filename=created_image.filename,
            original_name=created_image.original_name,
            alt_text=created_image.alt_text,
            file_size=created_image.file_size,
            mime_type=created_image.mime_type,
            created_at=created_image.created_at.isoformat()
            if created_image.created_at
            else "",
        )

    except HTTPException:
        file_path.unlink(missing_ok=True)
        raise
    except Exception as e:
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to process image: {str(e)}"
        )


@app.get("/api/images", response_model=ImageListResponse)
async def list_images(limit: int = 50, offset: int = 0) -> ImageListResponse:
    """List uploaded images with pagination."""
    images = db.get_images(limit=limit, offset=offset)

    image_responses = []
    for img in images:
        image_responses.append(
            ImageUploadResponse(
                id=img.id or 0,
                filename=img.filename,
                original_name=img.original_name,
                alt_text=img.alt_text,
                file_size=img.file_size,
                mime_type=img.mime_type,
                created_at=img.created_at.isoformat() if img.created_at else "",
            )
        )

    return ImageListResponse(images=image_responses, total=len(image_responses))


@app.get("/api/images/{image_id}")
async def get_image(image_id: int) -> ImageUploadResponse:
    """Get specific image details."""
    image = db.get_image(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    return ImageUploadResponse(
        id=image.id or 0,
        filename=image.filename,
        original_name=image.original_name,
        alt_text=image.alt_text,
        file_size=image.file_size,
        mime_type=image.mime_type,
        created_at=image.created_at.isoformat() if image.created_at else "",
    )


@app.get("/api/images/{image_id}/file")
async def get_image_file(image_id: int) -> FileResponse:
    """Serve the actual image file."""
    image = db.get_image(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    file_path = Path(image.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image file not found")

    return FileResponse(
        path=str(file_path),
        media_type=image.mime_type,
        filename=image.original_name,
    )


@app.put("/api/images/{image_id}/alt-text", response_model=ImageUploadResponse)
async def update_image_alt_text(
    image_id: int, request: AltTextUpdateRequest
) -> ImageUploadResponse:
    """Update alt text for an image."""
    updated_image = db.update_image_alt_text(image_id, request.alt_text)
    if not updated_image:
        raise HTTPException(status_code=404, detail="Image not found")

    return ImageUploadResponse(
        id=updated_image.id or 0,
        filename=updated_image.filename,
        original_name=updated_image.original_name,
        alt_text=updated_image.alt_text,
        file_size=updated_image.file_size,
        mime_type=updated_image.mime_type,
        created_at=updated_image.created_at.isoformat()
        if updated_image.created_at
        else "",
    )


@app.delete("/api/images/{image_id}")
async def delete_image(image_id: int) -> Dict[str, str]:
    """Delete an image."""
    image = db.get_image(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    file_path = Path(image.file_path)
    file_path.unlink(missing_ok=True)

    deleted = db.delete_image(image_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Image not found")

    return {"message": "Image deleted successfully"}


# Run app with uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
