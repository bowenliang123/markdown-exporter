"""Unit tests for extract_headings covering all six HTML heading levels."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from md_exporter.utils.table_utils import extract_headings


def test_extract_headings_h1_to_h5():
    html = "<h1>One</h1><h2>Two</h2><h3>Three</h3><h4>Four</h4><h5>Five</h5>"
    assert extract_headings(html, True) == ["One", "Two", "Three", "Four", "Five"]


def test_extract_headings_includes_h6():
    html = "<h1>Top</h1><h6>Deep section</h6>"
    assert extract_headings(html, True) == ["Top", "Deep section"]


def test_extract_headings_disabled_returns_empty():
    html = "<h1>Top</h1><h6>Deep section</h6>"
    assert extract_headings(html, False) == []
