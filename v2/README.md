# D&D Spell Card Generator V2

A modular system for generating printable, double-sided D&D 5e spell cards from CSV data.

## Features

✅ Load spell data from CSV files  
✅ Generate professional-looking card fronts and backs  
✅ Dynamic text fitting for varying description lengths  
✅ Table detection and formatting  
✅ Batch processing with error handling  
✅ Optimal vertical space utilization  
✅ PDF grid layout (configurable rows/cols, portrait/landscape)  
✅ PDF single-card mode (A7 pages, one card per page)  
✅ PDF cut-ready mode (fixed dimensions, guidelines, bleed)  
✅ Command-line interface with comprehensive help  
🚧 Custom illustrations support - Coming soon  

## Quick Start

```bash
# Setup
cd v2
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Generate cards with optimal defaults (2×4 landscape cut-ready)
python spell-cards.py --csv ../csv/warlock_spells.csv

# Show all CLI options
python spell-cards.py --help

# Keep PNG files for debugging (default: auto-cleanup)
python spell-cards.py --csv ../csv/warlock_spells.csv --keep-images

# Or use example scripts
python scripts/examples/test_generation.py
python scripts/examples/test_all_pdf_modes.py
```

## Project Structure

```
v2/
├── src/                   # Production code
│   ├── models.py          # Data models
│   ├── data_loader.py     # CSV and asset loading
│   ├── text_renderer.py   # Text fitting and rendering
│   ├── table_formatter.py # Table detection and formatting
│   ├── card_generator.py  # Card image generation
│   ├── batch_processor.py # Batch processing
│   └── pdf_generator.py   # PDF generation with grid layout
│
├── tests/                 # Unit tests (77 tests, all passing)
│   ├── test_data_loader.py
│   ├── test_text_renderer.py
│   ├── test_table_formatter.py
│   ├── test_batch_processor.py
│   └── test_pdf_generator.py  # 29 tests (3 PDF modes)
│
├── scripts/               # Development and analysis scripts
│   ├── examples/          # Usage examples
│   ├── analysis/          # Analysis and optimization tools
│   ├── testing/           # Integration tests
│   └── utils/             # Utility scripts
│
├── docs/                  # Documentation
│   ├── algorithm/         # Algorithm documentation
│   ├── features/          # Feature documentation
│   ├── fixes/             # Historical fixes
│   └── project/           # Project documentation
│
├── test_data/             # Test fixtures
├── output/                # Generated card images
└── requirements.txt       # Python dependencies
```

## Usage

### Command-Line Interface (Recommended)

```bash
# Basic usage - optimal defaults (2×4 landscape cut-ready)
python spell-cards.py --csv spells.csv

# Grid layout mode (flexible scaling)
python spell-cards.py --csv spells.csv --pdf-mode grid --grid 3x3 --orientation portrait

# Single-card A7 pages (no cutting needed)
python spell-cards.py --csv spells.csv --pdf-mode single-card

# Generate cards only (no PDF)
python spell-cards.py --csv spells.csv --no-pdf

# Show all options
python spell-cards.py --help
```

See [CLI_GUIDE.md](docs/CLI_GUIDE.md) for complete documentation.

### Programmatic Usage

```python
from pathlib import Path
from src.data_loader import load_spell_data, load_assets
from src.card_generator import CardGenerator
from src.batch_processor import BatchProcessor
from src.pdf_generator import PDFGenerator, GridConfig

# Load data
spells = load_spell_data(Path("test_data/test_spells.csv"))
assets = load_assets(Path("../assets"))

# Generate cards
generator = CardGenerator(assets)
processor = BatchProcessor(generator, Path("output"))
processor.process_spells(spells)

# Create PDF - choose your mode:

# Mode 1: Grid layout (flexible, scales to fit)
config = GridConfig(rows=3, cols=3, orientation="portrait")
pdf_gen = PDFGenerator(config)
pdf_gen.generate_pdf(
    card_names=[s.name for s in spells],
    output_path=Path("output/cards_grid.pdf"),
    image_dir=Path("output")
)

# Mode 2: Single-card A7 (one per page)
from src.pdf_generator import SingleCardPDFGenerator
pdf_gen = SingleCardPDFGenerator()
pdf_gen.generate_pdf(
    card_names=[s.name for s in spells],
    output_path=Path("output/cards_a7.pdf"),
    image_dir=Path("output")
)

# Mode 3: Cut-ready (professional printing)
from src.pdf_generator import CutReadyPDFGenerator
config = GridConfig(rows=2, cols=2, margin=5, gap_x=5, gap_y=5)
pdf_gen = CutReadyPDFGenerator(config)
pdf_gen.generate_pdf(
    card_names=[s.name for s in spells],
    output_path=Path("output/cards_cut_ready.pdf"),
    image_dir=Path("output")
)
```

See `scripts/examples/` for more examples.

## Development

### Run Tests
```bash
cd v2
source venv/bin/activate
pytest
```

### Run Analysis
```bash
# Analyze space usage
python scripts/analysis/analyze_card_space.py

# Show project status
python scripts/utils/test_summary.py
```

## Documentation

- **Algorithm**: See `docs/algorithm/TEXT_RENDERING_ALGORITHM.md`
- **Features**: See `docs/features/`
- **Status**: See `docs/project/STATUS.md`
- **Full Index**: See `docs/README.md`

## Current Status

**Completed** (Tasks 1-12):
- ✅ Data loading and validation
- ✅ Text rendering with dynamic sizing
- ✅ Card front and back generation
- ✅ Table detection and formatting
- ✅ Batch processing
- ✅ PDF grid layout (flexible scaling)
- ✅ PDF single-card A7 mode
- ✅ PDF cut-ready mode (guidelines, bleed)
- ✅ Command-line interface with comprehensive help
- ✅ Comprehensive testing (99 tests)
- ✅ Final checkpoint and verification

**Next** (Tasks 13-16):
- 📋 Sample assets and documentation
- 🚧 Optional: AI illustration generation
- 🚧 Optional: GUI with preview

## Specification

This implementation follows the specification in `.kiro/specs/dnd-spell-card-generator-v2/`.

## Performance

- **Batch Processing**: ~10 spells/second
- **Space Usage**: 77-92% of available vertical space
- **File Sizes**: 15-20KB (fronts), 40-115KB (backs)
- **Test Coverage**: 99 tests, 100% passing
- **PDF Modes**: 3 (grid, single-card, cut-ready)
- **Double-Sided Alignment**: Perfect for all modes

## License

(Add your license here)

