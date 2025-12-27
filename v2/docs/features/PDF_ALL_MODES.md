# PDF Generation - All Modes Complete

**Status**: ✅ Complete (Tasks 8, 9, 10)  
**Date**: December 27, 2024  
**Tests**: 77 passing (29 PDF tests)

## Overview

Implemented three PDF generation modes for different use cases:
1. **Grid Layout** - Flexible scaling, maximum cards per page
2. **Single-Card A7** - One card per page, easy assembly
3. **Cut-Ready** - Professional printing with guidelines and bleed

All modes support perfect double-sided alignment for printing.

## Mode 1: Grid Layout (Task 8)

### Purpose
Home printing with maximum flexibility. Cards scale to fit the page.

### Features
- Configurable grid size (any rows × cols)
- Portrait and landscape orientation
- Cards automatically scale to fit
- Centered grid with configurable margins and gaps
- Double-sided alignment (horizontal mirroring per row)

### Best For
- Home printing
- Quick prototypes
- Maximum cards per page
- Flexible layouts

### Usage
```python
from src.pdf_generator import PDFGenerator, GridConfig

config = GridConfig(rows=3, cols=3, orientation="portrait")
generator = PDFGenerator(config)
result = generator.generate_pdf(
    card_names=["spell1", "spell2", ...],
    output_path=Path("cards_grid.pdf"),
    image_dir=Path("output/")
)
```

### Configuration Options
```python
GridConfig(
    rows=3,              # Number of rows
    cols=3,              # Number of columns
    orientation="portrait",  # "portrait" or "landscape"
    margin=20,           # Page margin in points
    gap_x=10,            # Horizontal gap between cards
    gap_y=10             # Vertical gap between cards
)
```

## Mode 2: Single-Card A7 (Task 9)

### Purpose
Individual card printing on A7-sized pages (74.25mm × 105mm).

### Features
- One card per A7 page
- Alternates front/back for each spell
- No scaling - cards at original size
- Simple assembly

### Best For
- Individual cards
- Easy assembly
- No cutting required
- Testing/prototyping

### Usage
```python
from src.pdf_generator import SingleCardPDFGenerator

generator = SingleCardPDFGenerator()
result = generator.generate_pdf(
    card_names=["spell1", "spell2", ...],
    output_path=Path("cards_a7.pdf"),
    image_dir=Path("output/")
)
```

### Page Order
For 3 spells:
- Page 1: Spell 1 Front
- Page 2: Spell 1 Back
- Page 3: Spell 2 Front
- Page 4: Spell 2 Back
- Page 5: Spell 3 Front
- Page 6: Spell 3 Back

## Mode 3: Cut-Ready (Task 10)

### Purpose
Professional printing with fixed dimensions, cut guidelines, and bleed.

### Features
- **Fixed card dimensions**: 63.5mm × 88.5mm (standard poker card size)
- **Cut guidelines**: Dashed lines showing where to cut
- **Bleed borders**: 1.5mm extension beyond cut lines
- **Black fill**: Gaps between cards filled with black
- **Perfect alignment**: Double-sided printing with horizontal mirroring
- **Grid validation**: Ensures grid fits on page before generation

### Best For
- Professional printing
- Bulk production
- Clean cuts
- High-quality finish

### Usage
```python
from src.pdf_generator import CutReadyPDFGenerator, GridConfig

# Use smaller margins for cut-ready mode
config = GridConfig(
    rows=2,
    cols=2,
    orientation="portrait",
    margin=5,    # Smaller margins
    gap_x=5,     # Smaller gaps
    gap_y=5
)

generator = CutReadyPDFGenerator(config)
result = generator.generate_pdf(
    card_names=["spell1", "spell2", ...],
    output_path=Path("cards_cut_ready.pdf"),
    image_dir=Path("output/")
)
```

### Grid Size Recommendations

**Portrait A4**:
- 2×2: ✅ Fits comfortably
- 2×3: ❌ Too wide
- 3×2: ✅ Fits with small margins

**Landscape A4**:
- 2×3: ✅ Fits comfortably
- 2×4: ⚠️ Tight fit, use margin=5
- 3×3: ❌ Too large

### Cut-Ready Features Explained

#### 1. Fixed Dimensions
Unlike grid mode which scales cards, cut-ready uses exact poker card dimensions (63.5×88.5mm). This ensures consistency across prints.

#### 2. Bleed Borders
Content extends 1.5mm beyond the cut line. This prevents white edges if cutting is slightly off.

#### 3. Cut Guidelines
Dashed gray lines extend across the entire page, showing exactly where to cut. They mark the boundaries between cards.

#### 4. Black Fill
The gaps between cards and the bleed area are filled with black, creating a professional look and hiding any cutting imperfections.

#### 5. Double-Sided Alignment
Critical for cut-ready mode! Each row is horizontally mirrored on the back page:

```
Front page (looking at it):
┌─────┬─────┬─────┐
│  0  │  1  │  2  │
├─────┼─────┼─────┤
│  3  │  4  │  5  │
└─────┴─────┴─────┘

Back page (looking at it):
┌─────┬─────┬─────┐
│  2  │  1  │  0  │  ← Row reversed
├─────┼─────┼─────┤
│  5  │  4  │  3  │  ← Row reversed
└─────┴─────┴─────┘

When you flip the paper horizontally and hold it up to light,
the fronts and backs align perfectly!
```

## Printing Instructions

### Grid & Cut-Ready Modes
1. **Print fronts**: Print odd pages (1, 3, 5, ...)
2. **Flip horizontally**: Take the printed stack and flip it horizontally (not vertically!)
3. **Print backs**: Put the paper back in the printer and print even pages (2, 4, 6, ...)
4. **Cut** (cut-ready only): Cut along the dashed guidelines

### Single-Card Mode
1. **Print all pages**: Pages alternate front/back automatically
2. **Pair them up**: Page 1 with page 2, page 3 with page 4, etc.
3. **Done**: No cutting needed!

## Comparison Table

| Feature | Grid Layout | Single-Card A7 | Cut-Ready |
|---------|-------------|----------------|-----------|
| **Cards per page** | 4-9 (configurable) | 1 | 4-6 (typical) |
| **Card size** | Scaled to fit | Fixed (A7) | Fixed (63.5×88.5mm) |
| **Cutting required** | Yes | No | Yes |
| **Guidelines** | No | No | Yes (dashed lines) |
| **Bleed** | No | No | Yes (1.5mm) |
| **Best for** | Home printing | Individual cards | Professional printing |
| **Complexity** | Low | Very low | Medium |
| **Quality** | Good | Good | Excellent |

## Test Coverage

**29 PDF tests, all passing**:

### Grid Layout (18 tests)
- Configuration validation
- Page size calculation
- Card dimension calculation
- Position calculation
- Back order calculation
- PDF generation

### Single-Card A7 (4 tests)
- Initialization
- PDF creation
- Front/back alternation
- Missing image handling

### Cut-Ready (7 tests)
- Initialization
- Fixed dimensions
- Grid validation
- Back order calculation
- PDF creation
- Orientation support
- Bleed calculation

## Performance

- **Grid Layout**: O(n) where n = number of cards
- **Single-Card**: O(n) where n = number of cards
- **Cut-Ready**: O(n) where n = number of cards
- All modes process one page at a time (memory efficient)

## Files

- `src/pdf_generator.py` - All three PDF generators (580 lines)
- `tests/test_pdf_generator.py` - Comprehensive tests (29 tests)
- `scripts/examples/test_all_pdf_modes.py` - Usage example

## Requirements Satisfied

From specification:
- ✅ 5.1: Grid layout with configurable rows/columns
- ✅ 5.2: Double-sided alignment
- ✅ 5.4: Centered grid with margins
- ✅ 5.5: Handles partial pages
- ✅ 6.2: A7-sized single-card pages
- ✅ 6.3: Cut-ready with guidelines and bleed
- ✅ 6.4: Portrait and landscape orientation
- ✅ 10.1: Fixed card dimensions (63.5×88.5mm)

## Next Steps

- Task 11: Implement command-line interface
- Task 12: Final checkpoint
- Optional: AI illustration generation
- Optional: GUI with preview
