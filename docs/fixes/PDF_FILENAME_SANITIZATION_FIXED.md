# PDF Generation: Filename Sanitization - FIXED ✅

**Date**: December 27, 2024  
**Issue**: PDF generators couldn't find card images due to filename mismatch  
**Status**: Fixed

## Problem

When generating PDFs, the system was looking for card images using the original spell names (e.g., "Arcane Gate_front.png"), but the batch processor saves files with sanitized names (e.g., "arcane_gate_front.png").

This caused:
1. **Missing images**: PDF generators reported missing files
2. **Black rectangles**: Cut-ready mode drew bleed borders but no card images
3. **Empty pages**: Pages with only black rectangles and no content

### Example
For spell "Arcane Gate":
- **Batch processor saves**: `arcane_gate_front.png` (lowercase, underscores)
- **PDF generator looked for**: `Arcane Gate_front.png` (original case, spaces)
- **Result**: File not found, black rectangle drawn but no image

## Root Cause

The batch processor has filename sanitization logic:

```python
def _sanitize_filename(name: str) -> str:
    safe = name.replace(" ", "_")  # Spaces → underscores
    # Remove unsafe characters
    for char in '<>:"/\\|?*\'':
        safe = safe.replace(char, "")
    safe = safe.lower()  # Convert to lowercase
    return safe
```

But the PDF generators were using the original card names directly without sanitization.

## Solution

Added the same `_sanitize_filename()` method to all three PDF generator classes:
- `PDFGenerator` (grid layout)
- `SingleCardPDFGenerator` (A7 pages)
- `CutReadyPDFGenerator` (cut-ready mode)

### Implementation

```python
class PDFGenerator:
    # ... existing code ...
    
    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Convert spell name to safe filename (matches batch processor logic)."""
        safe = name.replace(" ", "_")
        unsafe_chars = '<>:"/\\|?*\''
        for char in unsafe_chars:
            safe = safe.replace(char, "")
        safe = safe.lower()
        return safe
    
    def _draw_page(self, ...):
        # OLD: image_path = image_dir / f"{card_name}_{side}.png"
        # NEW:
        safe_name = self._sanitize_filename(card_name)
        image_path = image_dir / f"{safe_name}_{side}.png"
```

Applied to all three generators in their respective image loading code.

## Files Modified

- `src/pdf_generator.py`:
  - Added `_sanitize_filename()` to `PDFGenerator` class
  - Added `_sanitize_filename()` to `SingleCardPDFGenerator` class
  - Added `_sanitize_filename()` to `CutReadyPDFGenerator` class
  - Updated all image path construction to use sanitized names

## Validation

### Before Fix
```bash
python scripts/examples/debug_cut_ready.py
# Result: Missing files: 8 (all images not found)
```

### After Fix
```bash
python scripts/examples/debug_cut_ready.py
# Result: Missing files: 0 (all images found)
```

### Test Results
- ✅ All 77 tests passing
- ✅ 101 warlock spells processed successfully
- ✅ All 5 PDF modes working correctly
- ✅ No missing files reported

## Impact

- ✅ PDF generators now find all card images
- ✅ No more black rectangles without content
- ✅ No more empty pages
- ✅ Cut-ready mode works correctly with partial pages
- ✅ All PDF modes consistent with batch processor

## Related Fixes

This fix works together with the empty slot fix:
1. **Filename sanitization** (this fix): Ensures images are found
2. **Empty slot handling**: Ensures empty slots stay white

Both fixes were needed to fully resolve the cut-ready PDF issues.

## Testing

Run the debug script to verify:
```bash
cd v2
python scripts/examples/debug_cut_ready.py
```

Should show:
- Missing files: 0
- All cards rendered correctly
- Empty slots white (no black fill)
