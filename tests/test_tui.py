"""Tests for terminal-browser setup paths that do not require Textual."""

import pytest

from PyOptik.tui import run_browser


def test_browser_requires_local_catalog(tmp_path):
    """A missing snapshot should produce an actionable error."""
    with pytest.raises(FileNotFoundError, match="pyoptik setup"):
        run_browser(tmp_path)
