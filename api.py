#!/usr/bin/env python

"""FastAPI server for the SEO Agent tool.

This module provides a RESTful API for various SEO operations
including keyword research, content optimization, site auditing, and backlink analysis.
"""

import os
import sys
import time
from typing import Any, Dict, List, Optional
import sqlite3
import jwt
from datetime import datetime

from fastapi import FastAPI, File, Form, HTTPException, UploadFile, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import core modules and utilities
from seo_agent.core.keyword_engine import KeywordEngine
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


def get_user_subscription_status(user_id: str) -> Dict[str, Any]:
    """Get user subscription status from database."""
    try:
        db_path = os.path.join(os.path.dirname(__file__), "frontend", "dev.db")
        if not os.path.exists(db_path):
            return {"planType": "FREE", "subscriptionStatus": None}
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT planType, subscriptionStatus, planEndDate, monthlyCredits, usedCredits
            FROM user WHERE id = ?
        """, (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return {"planType": "FREE", "subscriptionStatus": None}
        
        plan_type, subscription_status, plan_end_date, monthly_credits, used_credits = result
        
        if plan_end_date and datetime.now().timestamp() * 1000 > plan_end_date:
            return {"planType": "FREE", "subscriptionStatus": "expired"}
        
        return {
            "planType": plan_type or "FREE",
            "subscriptionStatus": subscription_status,
            "monthlyCredits": monthly_credits or 0,
            "usedCredits": used_credits or 0
        }
    except Exception as e:
        print(f"Error checking subscription status: {e}")
        return {"planType": "FREE", "subscriptionStatus": None}


def verify_session_token(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """Verify NextAuth session token and return user ID."""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    try:
        token = authorization.replace("Bearer ", "")
        decoded = jwt.decode(token, options={"verify_signature": False})
        user_id = decoded.get("sub")
        return user_id if isinstance(user_id, str) else None
    except Exception as e:
        print(f"Error verifying session token: {e}")
        return None


def require_subscription(user_id: Optional[str] = Depends(verify_session_token)) -> str:
    """Dependency to require active subscription for advanced features."""
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    subscription_info = get_user_subscription_status(user_id)
    
    if subscription_info["planType"] == "FREE":
        raise HTTPException(
            status_code=403, 
            detail="This feature requires a paid subscription. Please upgrade your plan."
        )
    
    if subscription_info["subscriptionStatus"] not in ["active", "trialing"]:
        raise HTTPException(
            status_code=403,
            detail="Your subscription is not active. Please check your billing status."
        )
    
    return user_id


# API routes
@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {"message": "SEO Agent API is running"}


@app.get("/api/validate-subscription")
async def validate_subscription(
    user_id: Optional[str] = Depends(verify_session_token)
) -> Dict[str, Any]:
    """Validate user subscription status."""
    if not user_id:
        return {
            "authenticated": False,
            "planType": "FREE",
            "subscriptionStatus": None,
            "canUseAdvanced": False
        }
    
    subscription_info = get_user_subscription_status(user_id)
    can_use_advanced = (
        subscription_info["planType"] != "FREE" and 
        subscription_info["subscriptionStatus"] in ["active", "trialing"]
    )
    
    return {
        "authenticated": True,
        "userId": user_id,
        "planType": subscription_info["planType"],
        "subscriptionStatus": subscription_info["subscriptionStatus"],
        "monthlyCredits": subscription_info.get("monthlyCredits", 0),
        "usedCredits": subscription_info.get("usedCredits", 0),
        "canUseAdvanced": can_use_advanced
    }


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
    user_id: Optional[str] = Depends(verify_session_token),
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
            if user_id:
                subscription_info = get_user_subscription_status(user_id)
                if subscription_info["planType"] == "FREE":
                    raise HTTPException(
                        status_code=403,
                        detail="Advanced content optimization requires a paid subscription. Please upgrade your plan."
                    )
                if subscription_info["subscriptionStatus"] not in ["active", "trialing"]:
                    raise HTTPException(
                        status_code=403,
                        detail="Your subscription is not active. Please check your billing status."
                    )
            else:
                # No authentication provided, but advanced features requested
                raise HTTPException(
                    status_code=401,
                    detail="Authentication required for advanced content optimization."
                )
            
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


# Run app with uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
