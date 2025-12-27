# Documentation Index

## Overview

This directory contains comprehensive documentation for the D&D Spell Card Generator V2.

## Quick Start

1. **New to the project?** Start with `README.md`
2. **Want to understand the algorithm?** Read `ALGORITHM_QUICK_REFERENCE.md`
3. **Need implementation details?** See `TEXT_RENDERING_ALGORITHM.md`
4. **Looking for status?** Check `STATUS.md`

## Documentation Files

### Project Documentation

| File | Purpose | Audience |
|------|---------|----------|
| `README.md` | Project overview and setup | Everyone |
| `STATUS.md` | Current project status | Developers |
| `requirements.txt` | Python dependencies | Developers |

### Algorithm Documentation

| File | Purpose | Audience |
|------|---------|----------|
| `TEXT_RENDERING_ALGORITHM.md` | Complete algorithm documentation | Developers |
| `ALGORITHM_QUICK_REFERENCE.md` | Quick reference guide | Developers |

### Feature Documentation

| File | Purpose | Audience |
|------|---------|----------|
| `TABLE_FORMATTING_FINAL.md` | Table formatting implementation | Developers |
| `TABLE_FIX_SUMMARY.md` | Table formatting fix summary | Everyone |
| `SPACING_OPTIMIZATION.md` | Vertical space optimization | Developers |
| `BATCH_PROCESSING.md` | Batch processing implementation | Developers |

### Historical Documentation

| File | Purpose | Audience |
|------|---------|----------|
| `TABLE_FORMAT_FIXED.md` | Original table fix | Reference |
| `TABLE_FORMATTING_RESULTS.md` | Table formatting results | Reference |
| `TABLE_HANDLING.md` | Table handling notes | Reference |

## Code Documentation

### Source Files (`src/`)

All source files contain comprehensive docstrings:

| File | Purpose | Key Classes/Functions |
|------|---------|----------------------|
| `models.py` | Data models | SpellData, AssetCollection |
| `data_loader.py` | CSV and asset loading | load_spell_data, load_assets |
| `text_renderer.py` | Text rendering engine | TextRenderer |
| `table_formatter.py` | Table detection/formatting | TableFormatter |
| `card_generator.py` | Card image generation | CardGenerator |
| `batch_processor.py` | Batch processing | BatchProcessor |

### Test Files (`tests/`)

| File | Purpose | Coverage |
|------|---------|----------|
| `test_data_loader.py` | Data loading tests | 12 tests |
| `test_text_renderer.py` | Text rendering tests | 17 tests |
| `test_table_formatter.py` | Table formatting tests | 7 tests |
| `test_batch_processor.py` | Batch processing tests | 12 tests |

**Total**: 48 tests, 100% passing

## Specification Files (`.kiro/specs/`)

| File | Purpose |
|------|---------|
| `requirements.md` | Functional requirements (EARS format) |
| `design.md` | System architecture and design |
| `tasks.md` | Implementation task breakdown |

## Analysis Scripts

Utility scripts for testing and analysis:

| File | Purpose |
|------|---------|
| `test_generation.py` | Generate test cards |
| `test_batch_generation.py` | Test batch processing |
| `test_batch_warlock.py` | Large batch test (101 spells) |
| `test_table_spell.py` | Test table formatting |
| `test_spacing_options.py` | Test spacing configurations |
| `analyze_card_space.py` | Analyze vertical space usage |
| `find_optimal_spacing.py` | Find optimal spacing values |
| `show_table_improvement.py` | Show table formatting improvement |
| `inspect_teleport_table.py` | Inspect table parsing |
| `debug_table_width.py` | Debug table width calculations |
| `test_summary.py` | Display test summary |

## Documentation by Topic

### Getting Started
1. `README.md` - Project overview
2. `requirements.txt` - Install dependencies
3. `test_generation.py` - Generate first cards

### Understanding the Code
1. `TEXT_RENDERING_ALGORITHM.md` - Core algorithm
2. `ALGORITHM_QUICK_REFERENCE.md` - Quick reference
3. Source code docstrings - Implementation details

### Features
1. `BATCH_PROCESSING.md` - Batch generation
2. `TABLE_FORMATTING_FINAL.md` - Table handling
3. `SPACING_OPTIMIZATION.md` - Space optimization

### Troubleshooting
1. `STATUS.md` - Current state
2. Test files - Expected behavior
3. Analysis scripts - Debug tools

## Reading Order

### For New Developers
1. `README.md` - Understand the project
2. `STATUS.md` - See what's done
3. `.kiro/specs/requirements.md` - Understand requirements
4. `ALGORITHM_QUICK_REFERENCE.md` - Learn core algorithm
5. Source code - Study implementation

### For Contributors
1. `STATUS.md` - Current state
2. `.kiro/specs/tasks.md` - Remaining work
3. `TEXT_RENDERING_ALGORITHM.md` - Deep dive
4. Test files - Understand expected behavior
5. Source code - Make changes

### For Users
1. `README.md` - How to use
2. `test_generation.py` - Generate cards
3. `test_batch_warlock.py` - Batch generation example

## Documentation Standards

### Code Documentation
- ✅ Module-level docstrings
- ✅ Class-level docstrings
- ✅ Method-level docstrings with examples
- ✅ Inline comments for complex logic
- ✅ Type hints for all functions

### Markdown Documentation
- ✅ Clear headings and structure
- ✅ Code examples
- ✅ Visual examples where helpful
- ✅ Tables for comparisons
- ✅ Status indicators (✅ ❌ ⚠️)

## Maintenance

### When Adding Features
1. Update relevant `.md` files
2. Add docstrings to new code
3. Create tests
4. Update `STATUS.md`
5. Update this index if needed

### When Fixing Bugs
1. Document the fix in a `*_FIX.md` file
2. Update relevant documentation
3. Add regression tests
4. Update `STATUS.md`

## External Resources

### Specifications
- EARS Requirements Format: Industry standard for requirements
- D&D 5E SRD: Spell data source

### Technologies
- Python 3.14: Programming language
- Pillow (PIL): Image manipulation
- pytest: Testing framework

## Contact

For questions about documentation:
- Check existing `.md` files first
- Review code docstrings
- Run analysis scripts for insights

---

**Last Updated**: December 27, 2024  
**Documentation Status**: ✅ Complete and up-to-date
