"""Tests for utility functions."""
import pytest
from utils import load_config

def test_load_config():
    """Test that load_config returns a dictionary."""
    config = load_config()
    assert isinstance(config, dict), "load_config should return a dictionary"

def test_load_config_has_expected_structure():
    """Test that load_config returns expected configuration structure."""
    config = load_config()
    assert "apis" in config, "config should contain 'apis' section"
    assert isinstance(config["apis"], dict), "apis section should be a dictionary"
