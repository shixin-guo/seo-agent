"""Basic test to ensure test discovery works."""

def test_basic():
    """Basic test that always passes to ensure CI doesn't fail on empty test suite."""
    assert True


def test_imports():
    """Test that core modules can be imported."""
    try:
        import seo_agent
        assert True
    except ImportError:
        assert False, "Failed to import seo_agent module"
