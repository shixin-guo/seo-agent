"""Basic tests for SEO Agent functionality."""

import pytest
from unittest.mock import patch, MagicMock
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import load_config


def test_load_config():
    """Test that load_config returns a dictionary."""
    with patch('builtins.open'), patch('yaml.safe_load') as mock_yaml:
        mock_yaml.return_value = {"ai": {"model": "test"}}
        config = load_config()
        assert isinstance(config, dict)
        assert "apis" in config


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"), 
    reason="OpenAI API key not available"
)
def test_image_alt_generator_import():
    """Test that ImageAltGenerator can be imported when API key is available."""
    from seo_agent.core.image_alt_generator import ImageAltGenerator
    
    config = {"apis": {"openai_key": os.getenv("OPENAI_API_KEY")}}
    generator = ImageAltGenerator(config)
    assert generator is not None


def test_database_import():
    """Test that database classes can be imported."""
    from seo_agent.core.database import Article, ArticleDatabase, Image
    
    assert Article is not None
    assert ArticleDatabase is not None
    assert Image is not None


def test_api_imports():
    """Test that API modules can be imported without errors."""
    import api
    assert hasattr(api, 'app')
