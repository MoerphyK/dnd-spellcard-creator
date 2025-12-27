# Text Rendering Algorithm Documentation

## Overview

The text rendering system dynamically sizes and positions text to fit within specified bounds while maximizing readability. It handles multi-paragraph text, preserves formatting, and ensures all content fits on the card.

## Core Components

### 1. TextRenderer Class (`src/text_renderer.py`)

The main class responsible for all text rendering operations.

#### Key Methods

1. **`measure_text(text, font_size)`** - Measures pixel dimensions of text
2. **`calculate_wrap_width(font_size, max_width)`** - Calculates character wrap width
3. **`wrap_text(text, wrap_width)`** - Wraps text preserving paragraphs
4. **`calculate_text_height(lines, font_size, line_spacing, paragraph_spacing)`** - Calculates total height
5. **`find_optimal_font_size(...)`** - Binary search for best font size
6. **`render_text_left_aligned(...)`** - Renders text on image
7. **`render_text_centered(...)`** - Renders centered text on image

## Algorithm Flow

### High-Level Process

```
Input: Text + Constraints (max_width, max_height, font_size_range)
    ↓
1. Find Optimal Font Size (binary search)
    ↓
2. Wrap Text (preserve paragraphs)
    ↓
3. Calculate Layout (positions for each line)
    ↓
4. Render Text (draw on image)
    ↓
Output: Text rendered on card
```

## Detailed Algorithm Breakdown

### Step 1: Find Optimal Font Size

**Goal**: Find the largest font size that fits all text within bounds.

**Method**: Binary search between `min_size` and `max_size`

```python
def find_optimal_font_size(text, min_size, max_size, max_width, max_height, 
                          line_spacing, paragraph_spacing):
    """
    Binary search algorithm to find optimal font size.
    
    Algorithm:
    1. Start with range [min_size, max_size]
    2. Test middle value (mid)
    3. If text fits at mid:
       - Save mid as best
       - Try larger (search upper half)
    4. If text doesn't fit:
       - Try smaller (search lower half)
    5. Repeat until range exhausted
    6. Return best (largest size that fits)
    """
```

**Example**:
```
Range: [10, 32]
Iteration 1: Test 21 → Fits → Best=21, try [22, 32]
Iteration 2: Test 27 → Doesn't fit → try [22, 26]
Iteration 3: Test 24 → Fits → Best=24, try [25, 26]
Iteration 4: Test 25 → Doesn't fit → try [25, 24]
Done: Best = 24pt
```

**Time Complexity**: O(log n) where n = (max_size - min_size)

### Step 2: Calculate Wrap Width

**Goal**: Determine how many characters fit per line at given font size.

**Method**: Measure widest character ('M') and calculate capacity.

```python
def calculate_wrap_width(font_size, max_width):
    """
    Calculate character wrap width.
    
    Algorithm:
    1. Measure width of 'M' (typically widest character)
    2. Divide max_width by char_width
    3. Return integer character count
    
    Example:
    - max_width = 574px
    - 'M' at 12pt = 10px wide
    - wrap_width = 574 / 10 = 57 characters
    """
```

**Why 'M'?**: 
- 'M' is typically the widest character in most fonts
- Using widest character ensures all text fits
- Conservative estimate prevents overflow

### Step 3: Wrap Text

**Goal**: Break text into lines while preserving paragraph structure.

**Method**: Use Python's `textwrap` module with paragraph awareness.

```python
def wrap_text(text, wrap_width):
    """
    Wrap text preserving paragraphs.
    
    Algorithm:
    1. Split text by newlines (paragraphs)
    2. For each paragraph:
       a. If empty → add None (paragraph break marker)
       b. If not empty → wrap to wrap_width
    3. Return list of lines (None = paragraph break)
    
    Example Input:
    "First paragraph.\n\nSecond paragraph."
    
    Example Output:
    ["First paragraph.", None, "Second paragraph."]
    """
```

**Paragraph Handling**:
- Empty lines become `None` markers
- `None` markers trigger extra spacing when rendering
- Preserves original paragraph structure

### Step 4: Calculate Text Height

**Goal**: Calculate total vertical space needed for wrapped text.

**Method**: Sum line heights plus spacing.

```python
def calculate_text_height(lines, font_size, line_spacing, paragraph_spacing):
    """
    Calculate total height of text block.
    
    Algorithm:
    1. Get font metrics (ascent + descent)
    2. For each line:
       a. If None (paragraph break):
          - Add paragraph_spacing
       b. If text line:
          - Add line_height + line_spacing
    3. Subtract final line_spacing (no space after last line)
    4. Return total height
    
    Example (3 lines, 1 paragraph break):
    Line 1: 20px (font) + 4px (spacing) = 24px
    Break:  25px (paragraph spacing)
    Line 2: 20px (font) + 4px (spacing) = 24px
    Line 3: 20px (font) + 0px (no spacing after) = 20px
    Total: 93px
    """
```

**Spacing Types**:
- **line_spacing**: Extra pixels between consecutive lines
- **paragraph_spacing**: Extra pixels between paragraphs
- **Font height**: Ascent + descent (built into font)

### Step 5: Render Text

**Goal**: Draw text on image at calculated positions.

**Method**: Position each line and draw with PIL.

```python
def render_text_left_aligned(image, text, top_left, max_width, max_height, ...):
    """
    Render text on image.
    
    Algorithm:
    1. Find optimal font size
    2. Wrap text
    3. Calculate starting Y position
    4. For each line:
       a. If None → advance Y by paragraph_spacing
       b. If text:
          - Draw text at (x, y)
          - Advance Y by line_height + line_spacing
    5. Done
    
    Positioning:
    - X: Fixed at top_left[0]
    - Y: Starts at top_left[1], increments for each line
    """
```

## Visual Example

### Input
```
Text: "First paragraph.\n\nSecond paragraph with more text."
max_width: 574px
max_height: 588px
font_size_range: 10-32pt
line_spacing: 4px
paragraph_spacing: 25px
```

### Process

**Step 1: Find Optimal Font Size**
```
Binary search: [10, 32]
Test 21pt → Fits
Test 27pt → Doesn't fit
Test 24pt → Fits
Result: 24pt
```

**Step 2: Calculate Wrap Width**
```
'M' at 24pt = 16px wide
wrap_width = 574 / 16 = 35 characters
```

**Step 3: Wrap Text**
```
Input paragraphs:
1. "First paragraph."
2. "" (empty line)
3. "Second paragraph with more text."

Wrapped lines:
1. "First paragraph."
2. None (paragraph break)
3. "Second paragraph with more"
4. "text."
```

**Step 4: Calculate Height**
```
Font height at 24pt: 28px

Line 1: 28px + 4px = 32px
Break:  25px
Line 2: 28px + 4px = 32px
Line 3: 28px + 0px = 28px
Total: 117px (fits in 588px ✓)
```

**Step 5: Render**
```
Y positions:
Line 1: y=384 (start)
Break:  y=416 (384 + 32)
Line 2: y=441 (416 + 25)
Line 3: y=473 (441 + 32)
```

## Key Design Decisions

### 1. Binary Search for Font Size

**Why?**: 
- Efficient: O(log n) vs O(n) linear search
- Guaranteed to find optimal size
- Fast even with large font ranges

**Alternative Considered**: Linear search from max down
- Slower for large ranges
- Same result but worse performance

### 2. Character-Based Wrapping

**Why?**:
- Simple and predictable
- Works with textwrap module
- Conservative (ensures fit)

**Alternative Considered**: Pixel-perfect wrapping
- More complex
- Minimal benefit (character-based works well)
- Harder to maintain

### 3. Paragraph Preservation

**Why?**:
- Maintains author's intent
- Better readability
- Professional appearance

**Implementation**: Use `None` markers
- Simple to implement
- Easy to handle in rendering
- Clear semantic meaning

### 4. Spacing Parameters

**Why separate line_spacing and paragraph_spacing?**:
- Different semantic purposes
- Allows fine-tuning readability
- Industry standard approach

**Current Values**:
- `line_spacing=4`: Comfortable reading
- `paragraph_spacing=25`: Clear separation

## Performance Characteristics

### Time Complexity
- **find_optimal_font_size**: O(log n × m) where n=font range, m=text length
- **wrap_text**: O(m) where m=text length
- **calculate_text_height**: O(k) where k=number of lines
- **render_text**: O(k) where k=number of lines

### Space Complexity
- **Wrapped lines**: O(k) where k=number of lines
- **Font cache**: O(f) where f=number of unique font sizes used

### Optimization Techniques

1. **Font Caching**: Fonts loaded once and reused
   ```python
   self._font_cache = {}  # Avoid reloading fonts
   ```

2. **Early Exit**: Binary search stops when range exhausted
   ```python
   while low <= high:  # Exits when low > high
   ```

3. **Conservative Estimates**: Use widest character for wrapping
   ```python
   char_width = measure_text("M", font_size)  # Widest char
   ```

## Edge Cases Handled

### 1. Empty Text
```python
if not text or not text.strip():
    return  # No rendering needed
```

### 2. Text Too Long for Minimum Font
```python
# Algorithm finds min_size if nothing else fits
# Text will be rendered at minimum size
```

### 3. Single Very Long Word
```python
# textwrap.wrap handles this
# Word will be placed on its own line
# May exceed max_width (unavoidable)
```

### 4. Multiple Consecutive Empty Lines
```python
# Each empty line becomes None
# Multiple Nones = multiple paragraph breaks
# Preserves original spacing intent
```

## Testing Strategy

### Unit Tests Cover:
1. ✅ Font size finding (various text lengths)
2. ✅ Text wrapping (single/multi-paragraph)
3. ✅ Height calculation (with/without breaks)
4. ✅ Rendering (centered/left-aligned)
5. ✅ Edge cases (empty text, very long text)

### Integration Tests Cover:
1. ✅ Full card generation
2. ✅ Various spell descriptions
3. ✅ Table formatting
4. ✅ Batch processing

## Usage Examples

### Example 1: Simple Text
```python
renderer = TextRenderer(font_path)
renderer.render_text_left_aligned(
    image=card,
    text="Simple spell description.",
    top_left=(90, 384),
    max_width=574,
    max_height=588,
    max_font_size=32,
    min_font_size=10,
    color="black",
    line_spacing=4,
    paragraph_spacing=25
)
# Result: Text rendered at optimal size (likely 32pt)
```

### Example 2: Long Text with Paragraphs
```python
text = """First paragraph with spell description.

Second paragraph with additional details.

Third paragraph with even more information."""

renderer.render_text_left_aligned(
    image=card,
    text=text,
    top_left=(90, 384),
    max_width=574,
    max_height=588,
    max_font_size=32,
    min_font_size=10,
    color="black",
    line_spacing=4,
    paragraph_spacing=25
)
# Result: Text rendered at smaller size (e.g., 14pt) with clear paragraph breaks
```

### Example 3: Centered Text (Spell Name)
```python
renderer.render_text_centered(
    image=banner,
    text="Tasha's Hideous Laughter",
    center=(375, 145),
    max_width=670,
    max_height=90,
    max_font_size=36,
    color="black"
)
# Result: Spell name centered in banner at optimal size
```

## Future Enhancements

### Potential Improvements:
1. **Adaptive Spacing**: Vary spacing based on text length
2. **Hyphenation**: Break long words with hyphens
3. **Justification**: Support justified text alignment
4. **Font Fallbacks**: Handle missing characters gracefully
5. **Kerning**: Fine-tune character spacing

### Not Planned:
- Rich text formatting (bold, italic) - not needed for spell cards
- Multiple fonts per card - design uses single font
- Vertical text - not required for D&D cards

## Conclusion

The text rendering algorithm provides:
- ✅ Automatic font sizing
- ✅ Paragraph preservation
- ✅ Optimal space utilization
- ✅ Consistent appearance
- ✅ Excellent performance
- ✅ Robust edge case handling

It's production-ready and handles all spell card text rendering needs efficiently and reliably.
