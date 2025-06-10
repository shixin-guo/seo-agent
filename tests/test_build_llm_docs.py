"""Tests for LLM documentation generation script."""
import pytest
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

def test_llm_files_exist():
    """Test that LLM documentation files are generated and exist."""
    root_dir = Path(__file__).parent.parent
    assert (root_dir / "llm.txt").exists(), "llm.txt should exist"
    assert (root_dir / "llm-full.txt").exists(), "llm-full.txt should exist"

def test_llm_files_not_empty():
    """Test that LLM documentation files contain content."""
    root_dir = Path(__file__).parent.parent
    llm_txt = root_dir / "llm.txt"
    llm_full_txt = root_dir / "llm-full.txt"
    
    assert llm_txt.stat().st_size > 0, "llm.txt should not be empty"
    assert llm_full_txt.stat().st_size > 0, "llm-full.txt should not be empty"

def test_llm_txt_contains_project_info():
    """Test that llm.txt contains expected project information."""
    root_dir = Path(__file__).parent.parent
    llm_txt = root_dir / "llm.txt"
    content = llm_txt.read_text(encoding='utf-8')
    
    assert "SEO Agent" in content, "llm.txt should contain project name"
    assert "AI-powered SEO automation tool" in content, "llm.txt should contain project description"
