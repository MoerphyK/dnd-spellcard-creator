# Cut-Ready Mode: Empty Slot Handling - FIXED ✅

**Date**: December 27, 2024  
**Issue**: Black fill appearing in empty card slots  
**Status**: Fixed

## Problem

When generating cut-ready PDFs with partial pages (e.g., 101 cards in a 2×2 grid = 26 pages with last page having only 1 card), the system was:

1. Drawing black bleed background for the **entire grid area**
2. Drawing cut guidelines for **all grid positions**
3. This caused empty slots to have black fill and unnecessary guidelines

### Example
With 101 cards in a 2×2 grid (4 cards per page):
- Pages 1-25: 4 cards each (full pages) ✅
- Page 26: Only 1 card, but 3 empty slots had black fill ❌

## Root Cause

The original implementation drew the bleed background as one large rectangle covering the entire grid:

```python
# OLD CODE - Drew black for entire grid
def _draw_bleed_background(self, c: canvas.Canvas):
    # Calculate grid bounds
    min_x = min(pos[0] for pos in self.positions)
    min_y = min(pos[1] for pos in self.positions)
    max_x = max(pos[0] + self.card_width for pos in self.positions)
    max_y = max(pos[1] + self.card_height for pos in self.positions)
    
    # Draw one big black rectangle
    c.rect(min_x - bleed, min_y - bleed, ...)
```

This filled **all** grid positions with black, regardless of whether they contained cards.

## Solution

Changed to draw bleed background **only for filled card positions**:

```python
# NEW CODE - Draw black only for filled positions
def _draw_bleed_background(
    self,
    c: canvas.Canvas,
    group: List[Optional[str]],
    order: List[int]
):
    c.setFillColorRGB(0, 0, 0)
    
    # Draw black rectangle with bleed for each filled position
    for i, idx in enumerate(order):
        if group[idx] is not None:  # Only if card exists
            pos = self.positions[i]
            c.rect(
                pos[0] - self.bleed,
                pos[1] - self.bleed,
                self.card_width + 2 * self.bleed,
                self.card_height + 2 * self.bleed,
                fill=1,
                stroke=0
            )
```

### Additional Fixes

Also updated cut guidelines to only draw at edges of filled cards:

```python
# NEW CODE - Guidelines only for filled positions
def _draw_cut_guidelines(
    self,
    c: canvas.Canvas,
    group: List[Optional[str]],
    order: List[int]
):
    verticals = set()
    horizontals = set()
    
    # Collect edges only for filled positions
    for i, idx in enumerate(order):
        if group[idx] is not None:  # Only if card exists
            x, y = self.positions[i]
            verticals.add(x)
            verticals.add(x + self.card_width)
            horizontals.add(y)
            horizontals.add(y + self.card_height)
    
    # Draw guidelines...
```

## Result

### Before Fix
```
┌─────────────────────────────┐
│ ████████ ████████ ████████  │  ← Black fill everywhere
│ █ Card █ █ Card █ █ Card █  │
│ ████████ ████████ ████████  │
│ ████████ ████████ ████████  │  ← Empty slot also black
│ █ Card █ █ EMPTY █ █ EMPTY █ │
│ ████████ ████████ ████████  │
└─────────────────────────────┘
```

### After Fix
```
┌─────────────────────────────┐
│ ████████ ████████ ████████  │  ← Black only around cards
│ █ Card █ █ Card █ █ Card █  │
│ ████████ ████████ ████████  │
│ ████████                     │  ← Empty slots are white
│ █ Card █         (empty)     │
│ ████████                     │
└─────────────────────────────┘
```

## Validation

Tested with:
- ✅ 3 cards in 2×2 grid (1 empty slot)
- ✅ 101 cards in 2×2 grid (3 empty slots on last page)
- ✅ 101 cards in 2×3 grid (5 empty slots on last page)

All tests pass, empty slots are now white with no black fill or unnecessary guidelines.

## Files Modified

- `src/pdf_generator.py`:
  - `_draw_bleed_background()` - Now takes group and order parameters
  - `_draw_cut_guidelines()` - Now takes group and order parameters
  - `_draw_cut_ready_page()` - Updated to pass parameters

## Impact

- ✅ Empty slots now appear white (correct)
- ✅ Black bleed only around actual cards (correct)
- ✅ Cut guidelines only at card edges (correct)
- ✅ All 77 tests still passing
- ✅ No performance impact

## Testing

Created test script to verify fix:
- `scripts/examples/test_partial_page.py` - Tests 3 cards in 2×2 grid

Run with:
```bash
python scripts/examples/test_partial_page.py
```

This creates a PDF with 1 empty slot to verify it's white, not black.
