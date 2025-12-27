# Command-Line Interface Guide

**D&D Spell Card Generator V2 - CLI Documentation**

## Quick Start

```bash
# Optimal defaults (2×4 landscape cut-ready, 8 cards/page)
python spell-cards.py --csv spells.csv

# Grid layout mode (flexible scaling)
python spell-cards.py --csv spells.csv --pdf-mode grid --grid 3x3

# Single-card A7 pages (no cutting needed)
python spell-cards.py --csv spells.csv --pdf-mode single-card

# Generate cards only (no PDF)
python spell-cards.py --csv spells.csv --no-pdf
```

## Installation

No installation required! Just run the script:

```bash
cd v2
python spell-cards.py --help
```

Or use as a Python module:

```bash
python -m src --csv spells.csv
```

## Command-Line Options

### Required Arguments

| Option | Description |
|--------|-------------|
| `--csv FILE` | Path to CSV file containing spell data (required) |

### Input/Output Options

| Option | Default | Description |
|--------|---------|-------------|
| `--assets DIR` | `../assets` | Path to assets directory |
| `--output DIR` | `output` | Output directory for generated files |

### PDF Generation Options

| Option | Default | Description |
|--------|---------|-------------|
| `--pdf-mode MODE` | `cut-ready` | PDF generation mode: `grid`, `single-card`, or `cut-ready` |
| `--no-pdf` | - | Generate card images only, skip PDF generation |
| `--pdf-name NAME` | `cards_<mode>.pdf` | Custom PDF filename |
| `--keep-images` | - | Keep PNG files after PDF generation (default: auto-cleanup) |

### Grid Layout Options

(For `grid` and `cut-ready` modes)

| Option | Default | Description |
|--------|---------|-------------|
| `--grid RxC` | `2x4` | Grid size as ROWSxCOLS (e.g., `2x2`, `3x3`, `2x4`) |
| `--orientation ORIENT` | `landscape` | Page orientation: `portrait` or `landscape` |
| `--margin POINTS` | 20 (grid)<br>5 (cut-ready) | Page margin in points |
| `--gap POINTS` | 10 (grid)<br>5 (cut-ready) | Gap between cards in points |

### Display Options

| Option | Description |
|--------|-------------|
| `--verbose`, `-v` | Show detailed progress information |
| `--quiet`, `-q` | Suppress all output except errors |
| `--version` | Show program version |
| `--help`, `-h` | Show help message |

## PDF Modes

### Grid Layout Mode (`--pdf-mode grid`)

**Best for**: Home printing, maximum cards per page

**Features**:
- Cards scale to fit page
- Configurable grid size (any rows × cols)
- Portrait or landscape orientation
- Double-sided alignment

**Example**:
```bash
python spell-cards.py --csv spells.csv --pdf-mode grid --grid 3x3
```

**Recommended grids**:
- Portrait: 3×3, 4×2, 2×3
- Landscape: 2×4, 3×3

### Single-Card Mode (`--pdf-mode single-card`)

**Best for**: Individual cards, no cutting required

**Features**:
- One card per A7 page (74.25mm × 105mm)
- Alternates front/back for each spell
- No cutting needed
- Easy assembly

**Example**:
```bash
python spell-cards.py --csv spells.csv --pdf-mode single-card
```

**Note**: Grid options are ignored in this mode.

### Cut-Ready Mode (`--pdf-mode cut-ready`)

**Best for**: Professional printing and cutting

**Features**:
- Fixed card dimensions (63.5mm × 88.5mm - poker card size)
- Cut guidelines (dashed lines)
- 1.5mm bleed borders
- Black fill between cards
- Perfect double-sided alignment

**Example**:
```bash
python spell-cards.py --csv spells.csv --pdf-mode cut-ready --grid 2x3 --orientation landscape
```

**Recommended grids**:
- Portrait: 2×2, 3×2
- Landscape: 2×3, 2×4

**Note**: Grid size is limited by fixed card dimensions. The CLI will error if the grid doesn't fit.

## Usage Examples

### Example 1: Quick Start (Optimal Defaults)

Generate cards with optimal settings (2×4 landscape cut-ready):

```bash
python spell-cards.py --csv my_spells.csv
```

Output:
- `output/cards_cut_ready.pdf` with 8 cards per page
- PNG files automatically cleaned up
- Perfect for professional printing
- `output/cards_grid.pdf` with 3×3 grid layout

### Example 2: Professional Printing

Generate cut-ready PDF for print shop:

```bash
python spell-cards.py \
  --csv warlock_spells.csv \
  --output warlock_cards \
  --pdf-mode cut-ready \
  --grid 2x3 \
  --orientation landscape \
  --pdf-name warlock_cut_ready
```

Output:
- `warlock_cards/` directory with 202 card images (101 spells × 2 sides)
- `warlock_cards/warlock_cut_ready.pdf` ready for professional printing

### Example 3: Individual Cards

Generate A7 pages for easy assembly:

```bash
python spell-cards.py \
  --csv my_spells.csv \
  --pdf-mode single-card \
  --pdf-name my_cards_a7
```

Output:
- Card images in `output/`
- `output/my_cards_a7.pdf` with 2 pages per spell (front, back)

### Example 4: Cards Only (No PDF)

Generate card images without PDF:

```bash
python spell-cards.py --csv spells.csv --no-pdf
```

Output:
- Only card images in `output/`
- No PDF file created
- PNG files are preserved (no cleanup)

### Example 5: Keep PNG Files for Debugging

By default, PNG files are automatically cleaned up after PDF generation. To keep them:

```bash
python spell-cards.py --csv spells.csv --keep-images
```

Output:
- Card images in `output/`
- PDF file in `output/`
- PNG files preserved for debugging or manual use

**Note**: This is useful when you want to:
- Inspect individual card images
- Use PNG files for other purposes
- Debug card generation issues

### Example 6: Custom Configuration

Full control over layout:

```bash
python spell-cards.py \
  --csv spells.csv \
  --assets my_custom_assets \
  --output my_output \
  --pdf-mode grid \
  --grid 4x2 \
  --orientation portrait \
  --margin 15 \
  --gap 8 \
  --pdf-name custom_cards \
  --verbose
```

### Example 7: Maximum Cards Per Page (2×4 Landscape)

For cut-ready mode, 2×4 landscape fits the most cards per page:

```bash
python spell-cards.py \
  --csv spells.csv \
  --pdf-mode cut-ready \
  --grid 2x4 \
  --orientation landscape
```

Output:
- 8 cards per page (2 rows × 4 columns)
- Perfect for large spell collections
- Efficient paper usage

### Example 8: Quiet Mode

Run without output (useful for scripts):

```bash
python spell-cards.py --csv spells.csv --quiet
echo "Exit code: $?"
```

## CSV Format

The CSV file must contain these columns:

| Column | Required | Description |
|--------|----------|-------------|
| `Name` | Yes | Spell name |
| `Level` | Yes | Spell level (0-9) |
| `School` | Yes | School of magic |
| `Casting Time` | Yes | Casting time |
| `Range` | Yes | Range |
| `Components` | Yes | Components (V, S, M) |
| `Duration` | Yes | Duration |
| `Classes` | Yes | Comma-separated class list |
| `Description` | Yes | Full spell description |
| `At Higher Levels` | No | Higher level effects (optional) |

**Example CSV**:
```csv
Name,Level,School,Casting Time,Range,Components,Duration,Classes,Description,At Higher Levels
Magic Missile,1,Evocation,1 action,120 feet,V S,Instantaneous,Sorcerer Wizard,"You create three glowing darts...",When you cast this spell using...
```

## Progress Output

### Normal Mode (default)

```
================================================================================
D&D Spell Card Generator V2
================================================================================

📖 Loading spell data from spells.csv...
   ✅ Loaded 101 spells

🎨 Loading assets from ../assets...
   ✅ Assets loaded successfully

🃏 Generating card images...
   Progress: 10/101 (9%)
   Progress: 20/101 (19%)
   ...
   Progress: 101/101 (100%)
   ✅ Generated 101 cards

📄 Generating PDF (cut-ready mode)...
   ✅ PDF created: output/cards_cut_ready.pdf

================================================================================
✅ COMPLETE
================================================================================
📁 Output directory: /path/to/output
🃏 Card images: 202 files
📄 PDF file: cards_cut_ready.pdf
```

### Verbose Mode (`--verbose`)

Shows each spell as it's processed:

```
🃏 Generating card images...
   [1/101] Arcane Gate
   [2/101] Armor of Agathys
   [3/101] Arms of Hadar
   ...
```

### Quiet Mode (`--quiet`)

No output (only errors). Check exit code:
- `0` = Success
- `1` = Error
- `130` = Cancelled (Ctrl+C)

## Error Handling

### CSV File Not Found

```bash
$ python spell-cards.py --csv missing.csv
Error: CSV file not found: missing.csv
```

Exit code: `1`

### Assets Directory Not Found

```bash
$ python spell-cards.py --csv spells.csv --assets missing_assets
Error: Assets directory not found: missing_assets
```

Exit code: `1`

### Invalid Grid Size

```bash
$ python spell-cards.py --csv spells.csv --pdf-mode cut-ready --grid 10x10
Error: Grid with fixed card dimensions (10×10) doesn't fit on portrait page.
```

Exit code: `1`

### Cancelled by User

Press `Ctrl+C` during execution:

```
^C
Operation cancelled by user.
```

Exit code: `130`

## Tips & Best Practices

### 1. Test with Small Dataset First

```bash
# Create test CSV with 3-5 spells
python spell-cards.py --csv test_spells.csv --verbose
```

### 2. Use Appropriate PDF Mode

- **Home printing**: `--pdf-mode grid --grid 3x3`
- **Professional printing**: `--pdf-mode cut-ready --grid 2x3 --orientation landscape`
- **Individual cards**: `--pdf-mode single-card`

### 3. Check Grid Fit for Cut-Ready

Cut-ready mode has size limits. If you get an error:
- Try smaller grid (2×2 instead of 3×3)
- Try landscape orientation
- Reduce margins: `--margin 5 --gap 5`

### 4. Custom Output Organization

```bash
# Organize by class
python spell-cards.py --csv warlock_spells.csv --output output/warlock
python spell-cards.py --csv wizard_spells.csv --output output/wizard
```

### 5. Batch Processing

```bash
#!/bin/bash
# Generate PDFs for all classes
for class in warlock wizard sorcerer; do
  python spell-cards.py \
    --csv "${class}_spells.csv" \
    --output "output/${class}" \
    --pdf-name "${class}_cards" \
    --quiet
done
```

## Troubleshooting

### Problem: "CSV file not found"

**Solution**: Check file path is correct relative to current directory.

```bash
# If CSV is in parent directory
python spell-cards.py --csv ../spells.csv

# If CSV is in csv/ subdirectory
python spell-cards.py --csv csv/spells.csv
```

### Problem: "Assets directory not found"

**Solution**: Specify correct assets path.

```bash
# If running from v2/ directory
python spell-cards.py --csv spells.csv --assets ../assets

# If assets are elsewhere
python spell-cards.py --csv spells.csv --assets /path/to/assets
```

### Problem: Grid doesn't fit (cut-ready mode)

**Solution**: Use smaller grid or landscape orientation.

```bash
# Try 2×2 instead of 3×3
python spell-cards.py --csv spells.csv --pdf-mode cut-ready --grid 2x2

# Or use landscape
python spell-cards.py --csv spells.csv --pdf-mode cut-ready --grid 2x3 --orientation landscape
```

### Problem: Missing card images in PDF

**Solution**: Ensure card images were generated successfully. Check output directory.

```bash
# Generate cards first, then check
python spell-cards.py --csv spells.csv --no-pdf
ls output/*.png

# Then generate PDF
python spell-cards.py --csv spells.csv
```

## Advanced Usage

### Using as Python Module

```python
from src.cli import SpellCardCLI

cli = SpellCardCLI()
exit_code = cli.run(['--csv', 'spells.csv', '--pdf-mode', 'grid'])
```

### Programmatic Access

```python
from pathlib import Path
from src.data_loader import load_spell_data, load_assets
from src.card_generator import CardGenerator
from src.batch_processor import BatchProcessor
from src.pdf_generator import PDFGenerator, GridConfig

# Load and generate
spells = load_spell_data(Path('spells.csv'))
assets = load_assets(Path('../assets'))
generator = CardGenerator(assets)
processor = BatchProcessor(generator, Path('output'))
processor.process_spells(spells)

# Create PDF
config = GridConfig(rows=3, cols=3)
pdf_gen = PDFGenerator(config)
pdf_gen.generate_pdf(
    [s.name for s in spells],
    Path('output/cards.pdf'),
    Path('output')
)
```

## Getting Help

```bash
# Show full help
python spell-cards.py --help

# Show version
python spell-cards.py --version

# Test with verbose output
python spell-cards.py --csv test.csv --verbose
```

## See Also

- [README.md](../README.md) - Project overview
- [PDF_ALL_MODES.md](features/PDF_ALL_MODES.md) - PDF mode details
- [STATUS.md](project/STATUS.md) - Project status
