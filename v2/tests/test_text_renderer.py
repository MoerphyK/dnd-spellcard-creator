"""Unit tests for text rendering functionality."""

import pytest
from pathlib import Path
from PIL import Image, ImageFont
from src.text_renderer import TextRenderer


@pytest.fixture
def font_path(tmp_path):
    """Create a temporary font file path."""
    # For testing, we'll use a system font or create a dummy path
    # In real tests, you'd want to include a test font
    font_file = tmp_path / "test.ttf"
    
    # Try to find a system font for testing
    system_fonts = [
        "/System/Library/Fonts/Helvetica.ttc",  # macOS
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
        "C:\\Windows\\Fonts\\arial.ttf"  # Windows
    ]
    
    for font in system_fonts:
        if Path(font).exists():
            return Path(font)
    
    # If no system font found, skip tests that need real fonts
    pytest.skip("No system font available for testing")


@pytest.fixture
def renderer(font_path):
    """Create a TextRenderer instance."""
    return TextRenderer(font_path)


def test_text_renderer_init(font_path):
    """Test TextRenderer initialization."""
    renderer = TextRenderer(font_path)
    assert renderer.font_path == font_path
    assert len(renderer._font_cache) == 0


def test_get_font_caching(renderer):
    """Test that fonts are cached."""
    font1 = renderer.get_font(24)
    font2 = renderer.get_font(24)
    
    # Should return same cached object
    assert font1 is font2
    assert 24 in renderer._font_cache


def test_measure_text(renderer):
    """Test text measurement."""
    width, height = renderer.measure_text("Hello", 24)
    
    assert width > 0
    assert height > 0
    
    # Longer text should be wider
    width2, _ = renderer.measure_text("Hello World", 24)
    assert width2 > width


def test_measure_text_empty(renderer):
    """Test measuring empty text."""
    width, height = renderer.measure_text("", 24)
    assert width >= 0
    assert height >= 0


def test_calculate_wrap_width(renderer):
    """Test wrap width calculation."""
    wrap_width = renderer.calculate_wrap_width(24, 200)
    
    assert wrap_width > 0
    assert isinstance(wrap_width, int)
    
    # Larger max_width should allow more characters
    wrap_width2 = renderer.calculate_wrap_width(24, 400)
    assert wrap_width2 > wrap_width


def test_wrap_text_single_line(renderer):
    """Test wrapping text that fits in one line."""
    lines = renderer.wrap_text("Short text", 50)
    
    assert len(lines) == 1
    assert lines[0] == "Short text"


def test_wrap_text_multiple_lines(renderer):
    """Test wrapping long text."""
    text = "This is a very long line of text that should be wrapped into multiple lines"
    lines = renderer.wrap_text(text, 20)
    
    assert len(lines) > 1
    assert all(len(line) <= 25 for line in lines if line)  # Allow some flexibility


def test_wrap_text_with_paragraphs(renderer):
    """Test wrapping text with paragraph breaks."""
    text = "First paragraph.\n\nSecond paragraph."
    lines = renderer.wrap_text(text, 50)
    
    # Should have None for paragraph break
    assert None in lines
    assert len([l for l in lines if l is not None]) >= 2


def test_calculate_text_height(renderer):
    """Test text height calculation."""
    lines = ["Line 1", "Line 2", "Line 3"]
    height = renderer.calculate_text_height(lines, 24)
    
    assert height > 0
    
    # More lines should be taller
    lines2 = ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"]
    height2 = renderer.calculate_text_height(lines2, 24)
    assert height2 > height


def test_calculate_text_height_with_paragraphs(renderer):
    """Test height calculation with paragraph breaks."""
    lines = ["Line 1", None, "Line 2"]
    height = renderer.calculate_text_height(lines, 24, paragraph_spacing=20)
    
    # Should include paragraph spacing
    assert height > 0


def test_find_optimal_font_size(renderer):
    """Test finding optimal font size."""
    text = "This is some text that needs to fit"
    
    size = renderer.find_optimal_font_size(
        text,
        min_size=10,
        max_size=30,
        max_width=200,
        max_height=100
    )
    
    assert 10 <= size <= 30


def test_find_optimal_font_size_very_long_text(renderer):
    """Test font sizing with very long text."""
    text = "This is a very long piece of text " * 20
    
    size = renderer.find_optimal_font_size(
        text,
        min_size=8,
        max_size=24,
        max_width=300,
        max_height=200
    )
    
    # Should find a small size that fits
    assert 8 <= size <= 24


def test_find_optimal_font_size_short_text(renderer):
    """Test font sizing with short text."""
    text = "Hi"
    
    size = renderer.find_optimal_font_size(
        text,
        min_size=10,
        max_size=50,
        max_width=500,
        max_height=500
    )
    
    # Should use maximum size since text is short
    assert size == 50


def test_render_text_centered(renderer):
    """Test centered text rendering."""
    img = Image.new('RGB', (400, 200), 'white')
    
    renderer.render_text_centered(
        img,
        "Centered Text",
        center=(200, 100),
        max_width=300,
        max_height=150,
        max_font_size=36
    )
    
    # Image should be modified (not all white)
    pixels = list(img.getdata())
    assert not all(p == (255, 255, 255) for p in pixels)


def test_render_text_left_aligned(renderer):
    """Test left-aligned text rendering."""
    img = Image.new('RGB', (400, 300), 'white')
    
    renderer.render_text_left_aligned(
        img,
        "Left aligned text that might wrap to multiple lines",
        top_left=(20, 20),
        max_width=360,
        max_height=260,
        max_font_size=24
    )
    
    # Image should be modified
    pixels = list(img.getdata())
    assert not all(p == (255, 255, 255) for p in pixels)


def test_render_text_with_paragraphs(renderer):
    """Test rendering text with paragraph breaks."""
    img = Image.new('RGB', (400, 400), 'white')
    
    text = "First paragraph with some text.\n\nSecond paragraph with more text."
    
    renderer.render_text_left_aligned(
        img,
        text,
        top_left=(20, 20),
        max_width=360,
        max_height=360,
        max_font_size=20
    )
    
    # Image should be modified
    pixels = list(img.getdata())
    assert not all(p == (255, 255, 255) for p in pixels)


def test_render_empty_text(renderer):
    """Test rendering empty text doesn't crash."""
    img = Image.new('RGB', (400, 200), 'white')
    
    # Should not crash
    renderer.render_text_centered(
        img,
        "",
        center=(200, 100),
        max_width=300,
        max_height=150,
        max_font_size=36
    )
