"""Tests for the FastAPI endpoints."""

import os
import sys
from typing import Any
from api.main import app
from fastapi.testclient import TestClient

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the FastAPI app

client = TestClient(app)


def test_root_endpoint() -> None:
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "SEO Agent API is running"}


def test_generate_keywords() -> None:
    """Test the keyword generation endpoint."""
    # Arrange
    request_data = {"seed": "digital marketing", "industry": "technology"}

    # Act
    response = client.post("/api/keywords", json=request_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "seed_keyword" in data
    assert data["seed_keyword"] == "digital marketing"
    assert "industry" in data
    assert data["industry"] == "technology"
    assert "total_keywords" in data
    assert "keywords" in data
    assert isinstance(data["keywords"], list)
    assert "intent_groups" in data
    assert isinstance(data["intent_groups"], dict)


def test_optimize_content(tmp_path: Any) -> None:
    """Test the content optimization endpoint."""
    # Arrange
    content = "This is some example content to optimize for SEO."
    content_file_path = tmp_path / "content.txt"
    with open(content_file_path, "w") as f:
        f.write(content)

    # Create a file to upload
    with open(content_file_path, "rb") as f:
        files = {"content_file": ("content.txt", f, "text/plain")}
        form_data = {"use_advanced": "false", "creative": "false"}

        # Act
        response = client.post("/api/optimize-content", files=files, data=form_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "original_content" in data
    assert "optimized_content" in data
    assert "analysis" in data
    assert "suggestions" in data


def test_audit_site() -> None:
    """Test the site audit endpoint."""
    # Arrange
    request_data = {"domain": "example.com", "max_pages": 10}

    # Act
    response = client.post("/api/audit-site", json=request_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "domain" in data
    assert data["domain"] == "example.com"
    assert "pages_crawled" in data
    assert "issues" in data
    assert "recommendations" in data
    assert "action_plan" in data


def test_analyze_backlinks() -> None:
    """Test the backlink analysis endpoint."""
    # Arrange
    request_data = {
        "domain": "example.com",
        "competitors": ["competitor1.com", "competitor2.com"],
        "generate_templates": True,
    }

    # Act
    response = client.post("/api/backlink-analysis", json=request_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "domain" in data
    assert data["domain"] == "example.com"
    assert "summary" in data
    assert "opportunities" in data
    assert "competitors" in data
    assert "templates" in data
