# Scripts Directory

Development, testing, and analysis scripts for the D&D Spell Card Generator V2.

## Directory Structure

### 📚 examples/
Example scripts showing how to use the card generator.

- `test_generation.py` - Generate a few test cards
- `test_batch_generation.py` - Batch generation example (3 spells)
- `test_batch_warlock.py` - Large batch example (101 warlock spells)

**Start here** if you want to see the generator in action!

### 🔍 analysis/
Scripts for analyzing and optimizing card generation.

- `analyze_card_space.py` - Analyze vertical space usage
- `test_spacing_options.py` - Test different spacing configurations
- `find_optimal_spacing.py` - Find optimal spacing values
- `inspect_teleport_table.py` - Inspect table formatting details
- `debug_table_width.py` - Debug table width calculations
- `show_table_improvement.py` - Show table formatting improvements

**Use these** for optimization and debugging.

### 🧪 testing/
Integration and manual testing scripts.

- `test_table_spell.py` - Test table formatting with Teleport spell
- `test_edge_cases.py` - Test edge case spells
- `test_table_comparison.py` - Compare table formatting approaches
- `verify_cards.py` - Verify generated cards
- `verify_edge_cases.py` - Verify edge case handling

**Use these** for validation and testing.

### 🛠️ utils/
Utility scripts for development.

- `test_summary.py` - Display test summary and project status
- `show_final_table.py` - Show final table formatting
- `debug_table.py` - Debug table parsing

**Use these** for quick checks and summaries.

## Quick Start

```bash
# Generate example cards
python scripts/examples/test_generation.py

# Batch generate warlock spells
python scripts/examples/test_batch_warlock.py

# Analyze space usage
python scripts/analysis/analyze_card_space.py

# Show project status
python scripts/utils/test_summary.py
```

## Running Scripts

All scripts should be run from the `v2/` directory:

```bash
cd v2
source venv/bin/activate
python scripts/examples/test_generation.py
```

## Adding New Scripts

When adding new scripts:
1. Choose appropriate subdirectory
2. Add descriptive docstring
3. Update this README
4. Test from v2/ directory
