# Optimal Grid Configurations for Cut-Ready Mode

**Date**: December 27, 2024

## Overview

This document describes the optimal grid configurations for cut-ready PDF mode, which uses fixed poker card dimensions (63.5mm × 88.5mm).

## Card Dimensions

- **Card Size**: 63.5mm × 88.5mm (standard poker card)
- **Bleed**: 1.5mm extension beyond cut lines
- **Page Size**: A4 (210mm × 297mm)

## Supported Grid Configurations

### Portrait Orientation

| Grid | Cards/Page | Status | Notes |
|------|------------|--------|-------|
| 2×2  | 4          | ✅ Recommended | Good balance, easy cutting |
| 3×2  | 6          | ✅ Recommended | Maximum for portrait |
| 3×3  | 9          | ❌ Too large | Doesn't fit on A4 portrait |

### Landscape Orientation

| Grid | Cards/Page | Status | Notes |
|------|------------|--------|-------|
| 2×3  | 6          | ✅ Recommended | Good balance |
| 2×4  | 8          | ✅ **OPTIMAL** | **Maximum cards per page** |
| 3×3  | 9          | ❌ Too large | Doesn't fit on A4 landscape |

## Optimal Configuration

**For maximum efficiency, use 2×4 landscape:**

```bash
python spell-cards.py \
  --csv spells.csv \
  --pdf-mode cut-ready \
  --grid 2x4 \
  --orientation landscape
```

**Benefits**:
- 8 cards per page (most efficient)
- Perfect double-sided alignment
- Fits comfortably on A4 landscape
- Efficient paper usage for large spell collections

## Comparison

### Paper Usage for 101 Warlock Spells

| Configuration | Cards/Page | Pages Needed | Paper Sheets |
|---------------|------------|--------------|--------------|
| 2×2 portrait  | 4          | 26 (13 front + 13 back) | 13 sheets |
| 3×2 portrait  | 6          | 18 (9 front + 9 back) | 9 sheets |
| 2×3 landscape | 6          | 18 (9 front + 9 back) | 9 sheets |
| **2×4 landscape** | **8** | **14 (7 front + 7 back)** | **7 sheets** |

**Savings**: 2×4 landscape uses 46% less paper than 2×2 portrait!

## Validation

The system automatically validates that the grid fits on the page:

```python
# This will succeed
python spell-cards.py --csv spells.csv --pdf-mode cut-ready --grid 2x4 --orientation landscape

# This will fail with clear error message
python spell-cards.py --csv spells.csv --pdf-mode cut-ready --grid 3x3 --orientation landscape
# Error: Grid with fixed card dimensions (3×3) doesn't fit on landscape page
```

## Margins and Gaps

Default values work well for all supported grids:
- **Margin**: 5 points (minimal, allows maximum cards)
- **Gap**: 5 points (enough space for cut guidelines)

You can adjust these if needed:

```bash
python spell-cards.py \
  --csv spells.csv \
  --pdf-mode cut-ready \
  --grid 2x4 \
  --orientation landscape \
  --margin 10 \
  --gap 8
```

**Note**: Increasing margins/gaps may cause larger grids to not fit.

## Recommendations by Use Case

### Small Collections (< 20 spells)
- **2×2 portrait** - Easy to cut, good for beginners

### Medium Collections (20-50 spells)
- **2×3 landscape** - Good balance of efficiency and ease

### Large Collections (50+ spells)
- **2×4 landscape** - Maximum efficiency, saves paper

### Professional Printing
- **2×4 landscape** - Most cost-effective for bulk printing

## Testing

All configurations have been tested with:
- ✅ 3 test spells (validation)
- ✅ 101 warlock spells (real-world)
- ✅ Perfect double-sided alignment verified
- ✅ Cut guidelines visible in white gaps only
- ✅ Black bleed fills gaps between cards

## Conclusion

**For most users, 2×4 landscape is the optimal choice**, offering:
- Maximum cards per page (8)
- Minimum paper usage
- Perfect alignment
- Professional results

Use smaller grids (2×2, 2×3) if you prefer easier cutting or have fewer cards.
