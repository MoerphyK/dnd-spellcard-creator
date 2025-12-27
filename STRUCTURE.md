# Project Structure

Clean, organized structure for the D&D Spell Card Generator V2.

## Directory Tree

```
v2/
│
├── 📦 src/                          Production Code
│   ├── __init__.py
│   ├── models.py                    Data models
│   ├── data_loader.py               CSV and asset loading
│   ├── text_renderer.py             Text rendering engine
│   ├── table_formatter.py           Table detection/formatting
│   ├── card_generator.py            Card image generation
│   └── batch_processor.py           Batch processing
│
├── 🧪 tests/                        Unit Tests (48 tests)
│   ├── test_data_loader.py          12 tests
│   ├── test_text_renderer.py        17 tests
│   ├── test_table_formatter.py      7 tests
│   └── test_batch_processor.py      12 tests
│
├── 🎯 scripts/                      Development Scripts
│   │
│   ├── 📚 examples/                 Usage Examples
│   │   ├── test_generation.py      Generate test cards
│   │   ├── test_batch_generation.py Batch example (3 spells)
│   │   └── test_batch_warlock.py   Large batch (101 spells)
│   │
│   ├── 🔍 analysis/                 Analysis Tools
│   │   ├── analyze_card_space.py   Space usage analysis
│   │   ├── test_spacing_options.py Spacing tests
│   │   ├── find_optimal_spacing.py Optimization
│   │   ├── inspect_teleport_table.py Table inspection
│   │   ├── debug_table_width.py    Width debugging
│   │   └── show_table_improvement.py Improvements
│   │
│   ├── 🧪 testing/                  Integration Tests
│   │   ├── test_table_spell.py     Table formatting test
│   │   ├── test_edge_cases.py      Edge case tests
│   │   ├── test_table_comparison.py Comparisons
│   │   ├── verify_cards.py         Card verification
│   │   └── verify_edge_cases.py    Edge case verification
│   │
│   └── 🛠️  utils/                   Utilities
│       ├── test_summary.py         Project status
│       ├── show_final_table.py     Table display
│       └── debug_table.py          Table debugging
│
├── 📖 docs/                         Documentation
│   │
│   ├── 📐 algorithm/                Algorithm Docs
│   │   ├── TEXT_RENDERING_ALGORITHM.md
│   │   └── ALGORITHM_QUICK_REFERENCE.md
│   │
│   ├── ✨ features/                 Feature Docs
│   │   ├── BATCH_PROCESSING.md
│   │   ├── TABLE_FORMATTING_FINAL.md
│   │   └── SPACING_OPTIMIZATION.md
│   │
│   ├── 🔧 fixes/                    Historical Fixes
│   │   ├── TABLE_FIX_SUMMARY.md
│   │   ├── TABLE_FORMAT_FIXED.md
│   │   ├── TABLE_FORMATTING_RESULTS.md
│   │   └── TABLE_HANDLING.md
│   │
│   └── 📋 project/                  Project Docs
│       ├── STATUS.md
│       ├── DOCUMENTATION_INDEX.md
│       ├── DOCUMENTATION_COMPLETE.md
│       ├── PROPOSED_STRUCTURE.md
│       └── REORGANIZATION_COMPLETE.md
│
├── 📁 test_data/                    Test Fixtures
│   ├── test_spells.csv
│   ├── edge_case_spells.csv
│   └── teleport_spell.csv
│
├── 🖼️  output/                      Generated Cards
│   ├── batch_test/
│   ├── table_test/
│   └── warlock_cards/
│
├── 🐍 venv/                         Virtual Environment
│
├── 📄 README.md                     Main Documentation
└── 📋 requirements.txt              Dependencies
```

## Quick Navigation

### I want to...

**Generate cards**
→ `scripts/examples/test_generation.py`

**Understand the algorithm**
→ `docs/algorithm/TEXT_RENDERING_ALGORITHM.md`

**See project status**
→ `docs/project/STATUS.md`

**Run tests**
→ `pytest tests/`

**Analyze performance**
→ `scripts/analysis/analyze_card_space.py`

**Read feature docs**
→ `docs/features/`

**Find source code**
→ `src/`

## File Counts

| Category | Files | Location |
|----------|-------|----------|
| Source code | 7 | `src/` |
| Unit tests | 4 | `tests/` |
| Example scripts | 3 | `scripts/examples/` |
| Analysis scripts | 6 | `scripts/analysis/` |
| Testing scripts | 5 | `scripts/testing/` |
| Utility scripts | 3 | `scripts/utils/` |
| Algorithm docs | 2 | `docs/algorithm/` |
| Feature docs | 3 | `docs/features/` |
| Fix docs | 4 | `docs/fixes/` |
| Project docs | 5 | `docs/project/` |

**Total**: 42 organized files

## Key Features

✅ Clean root directory (2 files only)  
✅ Clear separation of concerns  
✅ Easy to navigate  
✅ Professional structure  
✅ Scalable organization  
✅ Well documented  

## Status

- **Tests**: 48/48 passing ✅
- **Scripts**: 17/17 working ✅
- **Documentation**: Complete ✅
- **Organization**: Professional ✅

---

**Last Updated**: December 27, 2024
