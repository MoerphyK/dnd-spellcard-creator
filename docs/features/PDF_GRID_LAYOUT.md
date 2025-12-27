# PDF Grid Layout Mode - Task 8 Complete

**Status**: ✅ Complete  
**Date**: December 27, 2024

## Overview

Implemented PDF generation with configurable grid layouts for double-sided printing. The system arranges spell card images into PDF pages with proper alignment for front and back pages.

## Features Implemented

### 1. Grid Positioning Algorithm (Task 8.1)
- Calculates optimal card positions for any grid size (rows × cols)
- Centers grid on page with configurable margins
- Maintains A7 card aspect ratio (210:298)
- Automatically scales cards to fit available space
- Supports configurable gaps between cards

**Algorithm**:
1. Calculate available space (page size - margins - gaps)
2. Determine card width from available width
3. Calculate card height from width using aspect ratio
4. If total height exceeds available space, scale down proportionally
5. Center the grid on the page

### 2. Double-Sided Alignment (Task 8.2)
- Implements horizontal mirroring per row for back pages
- Ensures fronts and backs align when printed double-sided
- Works with any grid configuration

**Example** (3×3 grid):
```
Front page:  [0, 1, 2, 3, 4, 5, 6, 7, 8]
Back page:   [2, 1, 0, 5, 4, 3, 8, 7, 6]
```

Each row is reversed to create the mirror effect needed for double-sided printing.

### 3. PDF Page Generation (Task 8.4)
- Creates front and back pages for each group of cards
- Handles partial pages (unfilled grids) gracefully
- Reports missing image files
- Creates output directories automatically

### 4. Portrait and Landscape Orientation (Task 8.6)
- Supports both portrait and landscape page orientations
- Adjusts grid calculations based on orientation
- Maintains proper card aspect ratio in both modes

## API

### GridConfig
```python
@dataclass
class GridConfig:
    rows: int = 3              # Number of rows
    cols: int = 3              # Number of columns
    orientation: str = "portrait"  # "portrait" or "landscape"
    margin: float = 20         # Page margin in points
    gap_x: float = 10          # Horizontal gap in points
    gap_y: float = 10          # Vertical gap in points
```

### PDFGenerator
```python
generator = PDFGenerator(config)
result = generator.generate_pdf(
    card_names=["spell1", "spell2", ...],
    output_path=Path("output.pdf"),
    image_dir=Path("images/")
)
```

**Returns**:
```python
{
    "total_cards": 3,
    "total_pages": 2,
    "missing_files": []
}
```

## Usage Examples

### Example 1: Standard 3×3 Portrait Grid
```python
from src.pdf_generator import PDFGenerator, GridConfig

config = GridConfig(rows=3, cols=3, orientation="portrait")
generator = PDFGenerator(config)
result = generator.generate_pdf(
    card_names=["spell1", "spell2", "spell3"],
    output_path=Path("cards_3x3.pdf"),
    image_dir=Path("output/")
)
```

### Example 2: Landscape 2×4 Grid
```python
config = GridConfig(rows=2, cols=4, orientation="landscape")
generator = PDFGenerator(config)
result = generator.generate_pdf(
    card_names=spell_names,
    output_path=Path("cards_2x4_landscape.pdf"),
    image_dir=Path("output/")
)
```

### Example 3: Custom Margins and Gaps
```python
config = GridConfig(
    rows=4,
    cols=2,
    orientation="portrait",
    margin=30,    # Larger margins
    gap_x=15,     # More horizontal space
    gap_y=15      # More vertical space
)
generator = PDFGenerator(config)
```

## Test Coverage

**18 tests, all passing**:

### GridConfig Tests (5)
- Default configuration
- Custom configuration
- Validation (rows, cols, orientation)

### PDFGenerator Tests (13)
- Initialization
- Page size calculation (portrait/landscape)
- Card dimension calculation (3×3, 2×4)
- Position calculation and ordering
- Back order calculation (3×3, 2×4)
- PDF file creation
- Multiple pages
- Missing images handling
- Output directory creation

## Performance

- **Grid Calculation**: O(rows × cols) - linear in number of cards
- **PDF Generation**: O(n) where n = number of cards
- **Memory**: Minimal - processes one page at a time

## Printing Instructions

1. Generate PDF with desired grid configuration
2. Print front pages (odd pages: 1, 3, 5, ...)
3. Flip paper stack horizontally (not vertically!)
4. Print back pages (even pages: 2, 4, 6, ...)
5. Cut along card boundaries

The horizontal mirroring ensures perfect alignment when the paper is flipped horizontally for double-sided printing.

## Files

- `src/pdf_generator.py` - PDF generation implementation (237 lines)
- `tests/test_pdf_generator.py` - Comprehensive tests (18 tests)
- `scripts/examples/test_pdf_generation.py` - Usage example

## Requirements Satisfied

From specification:
- ✅ 5.1: Grid layout with configurable rows/columns
- ✅ 5.2: Double-sided alignment with horizontal mirroring
- ✅ 5.4: Centered grid with margins
- ✅ 5.5: Handles partial pages
- ✅ 6.4: Portrait and landscape orientation

## Next Steps

- Task 9: Implement PDF single-card layout mode (A7 pages)
- Task 10: Implement PDF cut-ready layout mode (guidelines, bleed)
- Task 11: Implement command-line interface
