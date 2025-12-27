# Table Handling in Spell Descriptions

## Current Implementation

The V2 spell card generator currently handles tables as **plain text**. When a spell description contains tabular data (like the Teleportation Outcome table in the "Teleport" spell), it is rendered as continuous text with the dynamic font sizing algorithm.

### Example: Teleport Spell

**Description length**: 2,622 characters  
**Contains**: Teleportation Outcome table with columns for Familiarity, Mishap, Similar Area, Off Target, and On Target

**Current behavior**:
- ✅ All text is preserved and rendered
- ✅ Dynamic font sizing ensures everything fits on the card
- ✅ Text wrapping maintains readability
- ⚠️ Table structure is lost (rendered as continuous text)

## Test Results

```
Spell: Teleport
Front: 15.3KB (750x1045)
Back: 113.7KB (750x1045)
Status: ✅ Generated successfully
```

The larger back file size (113.7KB vs typical 60-90KB) reflects the extensive text content.

## Potential Improvements

### Option 1: Keep as Plain Text (Current)
**Pros**:
- Simple, works for all cases
- No special parsing needed
- Dynamic sizing handles any length
- Consistent with other text

**Cons**:
- Table structure not visually preserved
- Harder to read tabular data

### Option 2: Detect and Format Tables
**Implementation ideas**:
1. Detect table markers (e.g., "Outcome", "Familiarity", column headers)
2. Parse table structure from text
3. Render as formatted table with borders/columns
4. Use smaller font for table sections

**Pros**:
- Better visual representation
- Easier to reference during gameplay
- More professional appearance

**Cons**:
- Complex parsing logic needed
- May not fit on card if table is large
- Requires table detection heuristics
- Different CSV sources may format tables differently

### Option 3: Hybrid Approach
**Implementation**:
1. Render tables as plain text (current behavior)
2. Add optional table detection and formatting
3. Allow users to choose rendering mode
4. Provide manual table markup in CSV (e.g., `[TABLE]...[/TABLE]`)

**Pros**:
- Flexible for different use cases
- Backwards compatible
- Users can optimize per spell

**Cons**:
- More complex configuration
- Requires user intervention for best results

## Recommendation

For V2.0, **keep the current plain text approach** because:

1. ✅ It works reliably for all cases
2. ✅ No special parsing or detection needed
3. ✅ Dynamic sizing ensures readability
4. ✅ Consistent behavior across all spells
5. ✅ Users can still read the information

For future versions (V2.1+), consider adding **optional table detection** as an enhancement:
- Add a `--format-tables` flag
- Detect common table patterns
- Render with basic formatting (indentation, spacing)
- Fall back to plain text if detection fails

## Current Status

✅ **Working**: Tables render as plain text with proper text fitting  
📋 **Future Enhancement**: Optional table formatting (not blocking V2.0 release)

## Testing

To test table handling:
```bash
cd v2
./venv/bin/python test_table_spell.py
```

This generates the Teleport spell card with its complex table structure.
