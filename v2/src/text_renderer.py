"""
Text rendering engine for spell cards with dynamic font sizing.

This module provides the core text rendering functionality for the spell card
generator. It handles automatic font sizing, text wrapping, paragraph preservation,
and optimal space utilization.

Key Features:
- Dynamic font sizing: Automatically finds largest font that fits
- Paragraph preservation: Maintains original paragraph structure
- Optimal space usage: Maximizes readability while fitting constraints
- Efficient algorithm: Binary search for O(log n) performance

Main Classes:
- TextRenderer: Core rendering engine with all text operations

Algorithm Overview:
1. Find optimal font size (binary search)
2. Wrap text to fit width (preserving paragraphs)
3. Calculate layout (line positions with spacing)
4. Render text on image (using PIL)

Example Usage:
    >>> from text_renderer import TextRenderer
    >>> renderer = TextRenderer("path/to/font.ttf")
    >>> 
    >>> # Render description on card back
    >>> renderer.render_text_left_aligned(
    ...     image=card,
    ...     text="Spell description with\\n\\nmultiple paragraphs.",
    ...     top_left=(90, 384),
    ...     max_width=574,
    ...     max_height=588,
    ...     max_font_size=32,
    ...     min_font_size=10,
    ...     color="black",
    ...     line_spacing=4,
    ...     paragraph_spacing=25
    ... )

For detailed algorithm documentation, see TEXT_RENDERING_ALGORITHM.md

Author: D&D Spell Card Generator V2
"""

import textwrap
from typing import Tuple, List, Optional
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


class TextRenderer:
    """Handles text measurement, fitting, and rendering on images."""
    
    def __init__(self, font_path: Path):
        """
        Initialize text renderer with a font.
        
        Args:
            font_path: Path to TrueType font file
        """
        self.font_path = font_path
        self._font_cache = {}
    
    def get_font(self, size: int) -> ImageFont.FreeTypeFont:
        """
        Get font at specified size (cached).
        
        Args:
            size: Font size in points
            
        Returns:
            Font object at requested size
        """
        if size not in self._font_cache:
            self._font_cache[size] = ImageFont.truetype(str(self.font_path), size)
        return self._font_cache[size]
    
    def measure_text(self, text: str, font_size: int) -> Tuple[int, int]:
        """
        Measure the dimensions of text at given font size.
        
        Args:
            text: Text to measure
            font_size: Font size in points
            
        Returns:
            Tuple of (width, height) in pixels
        """
        font = self.get_font(font_size)
        
        # Create temporary image for measurement
        temp_img = Image.new('RGB', (1, 1))
        draw = ImageDraw.Draw(temp_img)
        
        # Use textbbox for accurate measurement
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        
        return width, height
    
    def calculate_wrap_width(self, font_size: int, max_width: int) -> int:
        """
        Calculate optimal character wrap width for given font size and max pixel width.
        
        This determines how many characters can fit on a single line at the specified
        font size. We use a conservative estimate based on the widest character ('M')
        to ensure all text will fit.
        
        Algorithm:
        1. Measure the width of 'M' (typically the widest character)
        2. Divide max_width by char_width to get character capacity
        3. Return integer character count (minimum 1)
        
        Why 'M'?
        - 'M' is typically the widest character in most fonts
        - Using the widest character ensures conservative estimate
        - All other characters will fit within this width
        - Prevents text overflow
        
        Example:
        >>> renderer.calculate_wrap_width(font_size=12, max_width=574)
        57  # Approximately 57 characters fit at 12pt
        
        >>> renderer.calculate_wrap_width(font_size=24, max_width=574)
        28  # Fewer characters fit at larger font
        
        Args:
            font_size: Font size in points
            max_width: Maximum width in pixels
            
        Returns:
            Number of characters that fit in max_width (minimum 1)
        """
        # Measure a typical character (M is usually widest)
        char_width, _ = self.measure_text("M", font_size)
        
        if char_width == 0:
            return 1
        
        return max(1, int(max_width / char_width))
    
    def wrap_text(self, text: str, wrap_width: int) -> List[Optional[str]]:
        """
        Wrap text to specified character width, preserving paragraphs.
        
        This function breaks long text into lines while maintaining the original
        paragraph structure. Empty lines (paragraph breaks) are preserved as None
        markers, which trigger extra spacing during rendering.
        
        Algorithm:
        1. Split text by newlines to get paragraphs
        2. For each paragraph:
           a. If empty (just whitespace) → add None (paragraph break marker)
           b. If not empty → wrap using textwrap.wrap() to wrap_width
        3. Return list of lines where None = paragraph break
        
        Paragraph Handling:
        - Original: "Para 1.\n\nPara 2."
        - Split: ["Para 1.", "", "Para 2."]
        - Wrapped: ["Para 1.", None, "Para 2."]
        - The None marker triggers paragraph_spacing during rendering
        
        Example:
        >>> renderer.wrap_text("Short text", wrap_width=50)
        ["Short text"]
        
        >>> renderer.wrap_text("First paragraph.\\n\\nSecond paragraph.", wrap_width=20)
        ["First paragraph.", None, "Second paragraph."]
        
        >>> renderer.wrap_text("Very long text that needs wrapping...", wrap_width=20)
        ["Very long text that", "needs wrapping..."]
        
        Args:
            text: Text to wrap (may contain newlines for paragraphs)
            wrap_width: Maximum characters per line
            
        Returns:
            List of lines (None represents paragraph breaks)
        """
        paragraphs = text.splitlines()
        lines = []
        
        for para in paragraphs:
            if para.strip():
                wrapped = textwrap.wrap(para, width=wrap_width)
                lines.extend(wrapped)
            else:
                # Empty line represents paragraph break
                lines.append(None)
        
        return lines
    
    def calculate_text_height(
        self,
        lines: List[Optional[str]],
        font_size: int,
        line_spacing: int = 2,
        paragraph_spacing: int = 10
    ) -> int:
        """
        Calculate total height of wrapped text including spacing.
        
        This calculates the vertical space needed to render all lines with
        appropriate spacing between lines and paragraphs.
        
        Algorithm:
        1. Get font metrics (ascent + descent = line height)
        2. Initialize total_height = 0
        3. For each line:
           a. If None (paragraph break):
              - Add paragraph_spacing to total
           b. If text line:
              - Add line_height + line_spacing to total
        4. Subtract final line_spacing (no space after last line)
        5. Return total_height
        
        Spacing Types:
        - Font height: Built into font (ascent + descent)
        - line_spacing: Extra pixels between consecutive lines
        - paragraph_spacing: Extra pixels between paragraphs
        
        Example Calculation (font_size=20, line_spacing=4, paragraph_spacing=25):
        Lines: ["Line 1", None, "Line 2", "Line 3"]
        
        Font height at 20pt: 24px
        Line 1: 24px + 4px = 28px
        Break:  25px (paragraph spacing)
        Line 2: 24px + 4px = 28px
        Line 3: 24px + 0px = 24px (no spacing after last)
        Total: 105px
        
        Args:
            lines: List of text lines (None for paragraph breaks)
            font_size: Font size in points
            line_spacing: Extra pixels between lines (default 2)
            paragraph_spacing: Extra pixels between paragraphs (default 10)
            
        Returns:
            Total height in pixels
        """
        total_height = 0
        
        for line in lines:
            if line is None:
                total_height += paragraph_spacing
            else:
                _, line_height = self.measure_text(line, font_size)
                total_height += line_height + line_spacing
        
        # Remove trailing line spacing
        if total_height > 0 and lines and lines[-1] is not None:
            total_height -= line_spacing
        
        return total_height
    
    def find_optimal_font_size(
        self,
        text: str,
        min_size: int,
        max_size: int,
        max_width: int,
        max_height: int,
        line_spacing: int = 2,
        paragraph_spacing: int = 10
    ) -> int:
        """
        Find largest font size that fits text within bounds using binary search.
        
        This is the core algorithm for dynamic text sizing. It uses binary search
        to efficiently find the largest font size that allows all text to fit
        within the specified width and height constraints.
        
        Algorithm:
        1. Start with range [min_size, max_size]
        2. Test middle value (mid):
           - Wrap text at this font size
           - Calculate total height needed
           - Check if it fits within max_width and max_height
        3. If text fits:
           - Save mid as best candidate
           - Try larger fonts (search upper half: [mid+1, max_size])
        4. If text doesn't fit:
           - Try smaller fonts (search lower half: [min_size, mid-1])
        5. Repeat until range is exhausted
        6. Return best (largest size that fits)
        
        Time Complexity: O(log n × m) where:
        - n = (max_size - min_size) = font size range
        - m = text length (for wrapping and measuring)
        
        Example:
        >>> renderer.find_optimal_font_size(
        ...     "Short text",
        ...     min_size=10, max_size=32,
        ...     max_width=574, max_height=588
        ... )
        32  # Short text fits at maximum size
        
        >>> renderer.find_optimal_font_size(
        ...     "Very long text..." * 100,
        ...     min_size=10, max_size=32,
        ...     max_width=574, max_height=588
        ... )
        10  # Long text requires minimum size
        
        Args:
            text: Text to fit (may contain newlines for paragraphs)
            min_size: Minimum font size to try (typically 10pt)
            max_size: Maximum font size to try (typically 32pt)
            max_width: Maximum width in pixels (e.g., 574px for card back)
            max_height: Maximum height in pixels (e.g., 588px for card back)
            line_spacing: Extra pixels between consecutive lines (default 2)
            paragraph_spacing: Extra pixels between paragraphs (default 10)
            
        Returns:
            Optimal font size in points (or min_size if text doesn't fit at minimum)
        """
        # Binary search for optimal font size
        # We want the LARGEST size that fits, so we search from high to low
        low = min_size
        high = max_size
        best = low  # Start with minimum as fallback
        
        while low <= high:
            mid = (low + high) // 2  # Test middle of range
            
            # Step 1: Calculate how many characters fit per line at this font size
            wrap_width = self.calculate_wrap_width(mid, max_width)
            
            # Step 2: Wrap text to that width (preserving paragraphs)
            lines = self.wrap_text(text, wrap_width)
            
            # Step 3: Check if all lines fit within max_width
            # (wrap_width is conservative, but we verify actual pixel width)
            lines_fit_width = all(
                line is None or self.measure_text(line, mid)[0] <= max_width
                for line in lines
            )
            
            # Step 4: Calculate total height needed for all lines
            total_height = self.calculate_text_height(
                lines, mid, line_spacing, paragraph_spacing
            )
            fits_height = total_height <= max_height
            
            # Step 5: Decide which direction to search
            if lines_fit_width and fits_height:
                # Text fits! Save this size and try larger
                best = mid
                low = mid + 1  # Search upper half [mid+1, high]
            else:
                # Text doesn't fit, try smaller
                high = mid - 1  # Search lower half [low, mid-1]
        
        return best
    
    def render_text_centered(
        self,
        image: Image.Image,
        text: str,
        center: Tuple[int, int],
        max_width: int,
        max_height: int,
        max_font_size: int,
        min_font_size: int = 10,
        color: str = "black",
        wrap_width: Optional[int] = None
    ) -> None:
        """
        Render text centered at a point with dynamic sizing.
        
        Args:
            image: Image to draw on
            text: Text to render
            center: (x, y) center point
            max_width: Maximum width in pixels
            max_height: Maximum height in pixels
            max_font_size: Maximum font size to use
            min_font_size: Minimum font size to use
            color: Text color
            wrap_width: Optional fixed wrap width (otherwise calculated)
        """
        draw = ImageDraw.Draw(image)
        
        # Find optimal font size
        if wrap_width is None:
            font_size = self.find_optimal_font_size(
                text, min_font_size, max_font_size, max_width, max_height
            )
            wrap_width = self.calculate_wrap_width(font_size, max_width)
        else:
            font_size = max_font_size
            # Reduce font size until it fits
            while font_size >= min_font_size:
                lines = self.wrap_text(text, wrap_width)
                height = self.calculate_text_height(lines, font_size)
                if height <= max_height:
                    break
                font_size -= 1
        
        font = self.get_font(font_size)
        lines = self.wrap_text(text, wrap_width)
        
        # Calculate total height
        total_height = self.calculate_text_height(lines, font_size)
        
        # Start y position (centered)
        current_y = center[1] - total_height // 2
        
        # Draw each line centered
        for line in lines:
            if line is None:
                current_y += 10  # Paragraph spacing
            else:
                line_width, line_height = self.measure_text(line, font_size)
                x = center[0] - line_width // 2
                draw.text((x, current_y), line, font=font, fill=color)
                current_y += line_height + 2  # Line spacing
    
    def render_text_left_aligned(
        self,
        image: Image.Image,
        text: str,
        top_left: Tuple[int, int],
        max_width: int,
        max_height: int,
        max_font_size: int,
        min_font_size: int = 10,
        color: str = "black",
        line_spacing: int = 2,
        paragraph_spacing: int = 10
    ) -> None:
        """
        Render text left-aligned with dynamic sizing.
        
        Args:
            image: Image to draw on
            text: Text to render
            top_left: (x, y) top-left corner
            max_width: Maximum width in pixels
            max_height: Maximum height in pixels
            max_font_size: Maximum font size to use
            min_font_size: Minimum font size to use
            color: Text color
            line_spacing: Extra pixels between lines
            paragraph_spacing: Extra pixels between paragraphs
        """
        draw = ImageDraw.Draw(image)
        
        # Find optimal font size
        font_size = self.find_optimal_font_size(
            text, min_font_size, max_font_size, max_width, max_height,
            line_spacing, paragraph_spacing
        )
        
        font = self.get_font(font_size)
        wrap_width = self.calculate_wrap_width(font_size, max_width)
        lines = self.wrap_text(text, wrap_width)
        
        # Draw each line
        current_y = top_left[1]
        for line in lines:
            if line is None:
                current_y += paragraph_spacing
            else:
                _, line_height = self.measure_text(line, font_size)
                draw.text((top_left[0], current_y), line, font=font, fill=color)
                current_y += line_height + line_spacing
