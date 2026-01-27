"""Basic tests for animaid package."""

import animaid


def test_version():
    """Test that version is defined and follows semver pattern."""
    assert animaid.__version__
    parts = animaid.__version__.split(".")
    assert len(parts) == 3
    assert all(part.isdigit() for part in parts)
