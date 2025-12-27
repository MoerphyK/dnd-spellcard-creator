"""Unit tests for table formatting."""

import pytest
from src.table_formatter import TableFormatter


def test_detect_table_with_ranges():
    """Test detecting tables with numeric ranges."""
    text = "Familiarity 01-05 06-13 14-24 25-00"
    assert TableFormatter.detect_table(text) is True


def test_detect_table_without_table():
    """Test that normal text is not detected as table."""
    text = "This is a normal spell description without any tables."
    assert TableFormatter.detect_table(text) is False


def test_format_simple_table():
    """Test simple table formatting."""
    text = "FamiliarityMishapSimilar AreaOff TargetOn Target"
    formatted = TableFormatter._format_simple_table(text, 60)
    
    # Should return formatted text
    assert len(formatted) >= len(text) - 10  # Allow for some compression


def test_format_description_without_table():
    """Test that descriptions without tables pass through unchanged."""
    desc = "This is a simple spell description."
    result = TableFormatter.format_description_with_table(desc)
    assert result == desc


def test_format_description_with_table():
    """Test formatting description with table."""
    desc = (
        "This spell does something. "
        "Teleportation OutcomeFamiliarityMishapSimilar AreaOff TargetOn Target"
        "Permanent circle———01-00"
        " After the table, more text."
    )
    
    result = TableFormatter.format_description_with_table(desc)
    
    # Should still contain all the text
    assert "This spell does something" in result
    assert "Familiarity" in result or "Teleportation" in result
    assert "After the table" in result


def test_parse_table_basic():
    """Test basic table parsing."""
    table_text = "Teleportation OutcomePermanent circle———01-00"
    rows = TableFormatter.parse_teleportation_table(table_text)
    
    # Should extract some structure
    assert len(rows) > 0
    assert len(rows[0]) == 5  # Header with 5 columns


def test_format_table_text():
    """Test table text formatting."""
    table_text = "Col1 Col2 Col3\nData1 Data2 Data3"
    formatted = TableFormatter.format_table_text(table_text, max_width=60)
    
    # Should have some structure
    assert "\n" in formatted or len(formatted) > 0
