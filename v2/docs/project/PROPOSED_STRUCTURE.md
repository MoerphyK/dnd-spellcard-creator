# Proposed File Structure Reorganization

## Current Issues

1. **Root directory cluttered**: 20+ files in `v2/` root
2. **Mixed purposes**: Documentation, tests, analysis scripts all mixed
3. **Hard to navigate**: Difficult to find what you need
4. **No clear separation**: Production code vs development tools

## Current Structure

```
v2/
├── src/                           # ✅ Good - source code
├── tests/                         # ✅ Good - unit tests
├── test_data/                     # ✅ Good - test fixtures
├── output/                        # ✅ Good - generated files
├── venv/                          # ✅ Good - virtual environment
│
├── requirements.txt               # ✅ Keep in root
├── README.md                      # ✅ Keep in root
│
├── 15+ documentation files        # ❌ Should organize
├── 10+ test/analysis scripts      # ❌ Should organize
└── Various other files            # ❌ Should organize
```

## Proposed Structure

```
v2/
├── src/                           # Production code
│   ├── __init__.py
│   ├── models.py
│   ├── data_loader.py
│   ├── text_renderer.py
│   ├── table_formatter.py
│   ├── card_generator.py
│   └── batch_processor.py
│
├── tests/                         # Unit tests
│   ├── test_data_loader.py
│   ├── test_text_renderer.py
│   ├── test_table_formatter.py
│   └── test_batch_processor.py
│
├── test_data/                     # Test fixtures
│   ├── test_spells.csv
│   ├── edge_case_spells.csv
│   └── teleport_spell.csv
│
├── scripts/                       # 🆕 Development/analysis scripts
│   ├── examples/                  # Example usage scripts
│   │   ├── test_generation.py
│   │   ├── test_batch_generation.py
│   │   └── test_batch_warlock.py
│   │
│   ├── analysis/                  # Analysis and debugging
│   │   ├── analyze_card_space.py
│   │   ├── test_spacing_options.py
│   │   ├── find_optimal_spacing.py
│   │   ├── inspect_teleport_table.py
│   │   ├── debug_table_width.py
│   │   └── show_table_improvement.py
│   │
│   ├── testing/                   # Integration/manual tests
│   │   ├── test_table_spell.py
│   │   ├── test_edge_cases.py
│   │   ├── test_table_comparison.py
│   │   ├── verify_cards.py
│   │   └── verify_edge_cases.py
│   │
│   └── utils/                     # Utility scripts
│       ├── test_summary.py
│       ├── show_final_table.py
│       └── debug_table.py
│
├── docs/                          # 🆕 All documentation
│   ├── README.md -> ../README.md  # Symlink to main README
│   │
│   ├── algorithm/                 # Algorithm documentation
│   │   ├── TEXT_RENDERING_ALGORITHM.md
│   │   ├── ALGORITHM_QUICK_REFERENCE.md
│   │   └── index.md
│   │
│   ├── features/                  # Feature documentation
│   │   ├── BATCH_PROCESSING.md
│   │   ├── TABLE_FORMATTING_FINAL.md
│   │   ├── SPACING_OPTIMIZATION.md
│   │   └── index.md
│   │
│   ├── fixes/                     # Historical fixes
│   │   ├── TABLE_FIX_SUMMARY.md
│   │   ├── TABLE_FORMAT_FIXED.md
│   │   ├── TABLE_FORMATTING_RESULTS.md
│   │   └── TABLE_HANDLING.md
│   │
│   └── project/                   # Project documentation
│       ├── STATUS.md
│       ├── DOCUMENTATION_INDEX.md
│       ├── DOCUMENTATION_COMPLETE.md
│       └── PROPOSED_STRUCTURE.md (this file)
│
├── output/                        # Generated card images
│   ├── batch_test/
│   ├── table_test/
│   └── warlock_cards/
│
├── venv/                          # Virtual environment (gitignored)
│
├── .pytest_cache/                 # Pytest cache (gitignored)
│
├── requirements.txt               # Python dependencies
└── README.md                      # Main project README
```

## Benefits

### 1. Clear Separation
- **Production code**: `src/`
- **Tests**: `tests/`
- **Documentation**: `docs/`
- **Scripts**: `scripts/`

### 2. Easy Navigation
- Find examples: `scripts/examples/`
- Find docs: `docs/`
- Find analysis tools: `scripts/analysis/`

### 3. Scalability
- Easy to add new scripts
- Easy to add new docs
- Clear where things belong

### 4. Professional Structure
- Industry standard layout
- Easy for contributors
- Clear purpose for each directory

## Migration Plan

### Phase 1: Create New Directories
```bash
mkdir -p scripts/{examples,analysis,testing,utils}
mkdir -p docs/{algorithm,features,fixes,project}
```

### Phase 2: Move Scripts
```bash
# Examples
mv test_generation.py scripts/examples/
mv test_batch_generation.py scripts/examples/
mv test_batch_warlock.py scripts/examples/

# Analysis
mv analyze_card_space.py scripts/analysis/
mv test_spacing_options.py scripts/analysis/
mv find_optimal_spacing.py scripts/analysis/
mv inspect_teleport_table.py scripts/analysis/
mv debug_table_width.py scripts/analysis/
mv show_table_improvement.py scripts/analysis/
mv show_final_table.py scripts/utils/

# Testing
mv test_table_spell.py scripts/testing/
mv test_edge_cases.py scripts/testing/
mv test_table_comparison.py scripts/testing/
mv verify_cards.py scripts/testing/
mv verify_edge_cases.py scripts/testing/

# Utils
mv test_summary.py scripts/utils/
mv debug_table.py scripts/utils/
```

### Phase 3: Move Documentation
```bash
# Algorithm docs
mv TEXT_RENDERING_ALGORITHM.md docs/algorithm/
mv ALGORITHM_QUICK_REFERENCE.md docs/algorithm/

# Feature docs
mv BATCH_PROCESSING.md docs/features/
mv TABLE_FORMATTING_FINAL.md docs/features/
mv SPACING_OPTIMIZATION.md docs/features/

# Fix docs
mv TABLE_FIX_SUMMARY.md docs/fixes/
mv TABLE_FORMAT_FIXED.md docs/fixes/
mv TABLE_FORMATTING_RESULTS.md docs/fixes/
mv TABLE_HANDLING.md docs/fixes/

# Project docs
mv STATUS.md docs/project/
mv DOCUMENTATION_INDEX.md docs/project/
mv DOCUMENTATION_COMPLETE.md docs/project/
mv PROPOSED_STRUCTURE.md docs/project/
```

### Phase 4: Update Imports
Update any scripts that import from relative paths to use correct paths.

### Phase 5: Update Documentation
Update `DOCUMENTATION_INDEX.md` with new paths.

### Phase 6: Create Index Files
Create `index.md` files in each docs subdirectory for easy navigation.

## Files to Keep in Root

```
v2/
├── requirements.txt    # Dependencies
├── README.md          # Main documentation
├── .gitignore         # Git ignore rules
└── pytest.ini         # Pytest configuration (if needed)
```

## Alternative: Simpler Structure

If the above is too complex, a simpler alternative:

```
v2/
├── src/               # Production code
├── tests/             # Unit tests
├── test_data/         # Test fixtures
├── scripts/           # All scripts (examples, analysis, testing)
├── docs/              # All documentation
├── output/            # Generated files
├── venv/              # Virtual environment
├── requirements.txt
└── README.md
```

## Recommendation

I recommend the **full proposed structure** because:
1. We have enough files to warrant organization
2. Clear separation helps maintainability
3. Easy for new contributors to navigate
4. Professional and scalable

However, we can start with the **simpler structure** and refine later if preferred.

## Questions to Consider

1. **Do you want the full structure or simpler version?**
2. **Should we keep any scripts in root for convenience?**
3. **Any specific organization preferences?**
4. **Should we do this now or after more features are complete?**

## Impact

### Low Risk
- ✅ No code changes needed (just file moves)
- ✅ Tests will still work (pytest finds tests automatically)
- ✅ Can be done incrementally
- ✅ Easy to revert if needed

### Benefits
- ✅ Much cleaner structure
- ✅ Easier to find files
- ✅ Better for collaboration
- ✅ More professional appearance

## Next Steps

If approved:
1. Create new directory structure
2. Move files systematically
3. Update any hardcoded paths
4. Update documentation
5. Test that everything still works
6. Commit changes

---

**Status**: Proposal - Awaiting approval  
**Effort**: ~30 minutes  
**Risk**: Low  
**Benefit**: High
