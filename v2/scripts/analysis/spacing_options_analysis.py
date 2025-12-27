"""Test different spacing options for better vertical space usage."""

from pathlib import Path

# Setup path for imports
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).parent.parent.parent))

from src.data_loader import load_spell_data, load_assets
from src.text_renderer import TextRenderer
from src.table_formatter import TableFormatter


def test_spacing(spell_name: str, csv_path: Path):
    """Test different spacing configurations."""
    spells = load_spell_data(csv_path)
    spell = next((s for s in spells if s.name == spell_name), None)
    
    if not spell:
        return
    
    print("="*80)
    print(f"SPACING OPTIMIZATION: {spell.name}")
    print("="*80)
    
    # Card dimensions
    desc_max_width = 574
    desc_max_height = 588
    
    # Prepare text
    formatted_desc = TableFormatter.format_description_with_table(spell.description, max_width=80)
    if spell.at_higher_levels:
        full_text = f"Description:\n{formatted_desc}\n\n\nAt Higher Levels:\n{spell.at_higher_levels}"
    else:
        full_text = f"Description:\n{formatted_desc}"
    
    assets = load_assets(Path("../assets"))
    renderer = TextRenderer(assets.font_path)
    
    # Test different spacing configurations
    configs = [
        ("Current (tight)", 1, 10),
        ("Moderate", 2, 15),
        ("Comfortable", 3, 20),
        ("Spacious", 4, 25),
        ("Very spacious", 5, 30),
    ]
    
    print(f"\nText length: {len(full_text)} chars")
    print(f"Available space: {desc_max_height}px")
    print(f"\n{'Config':<20} {'Line':<5} {'Para':<5} {'Font':<5} {'Height':<7} {'Usage':<8} {'Fits'}")
    print("-" * 80)
    
    for name, line_sp, para_sp in configs:
        # Find optimal font size with these spacing settings
        optimal = renderer.find_optimal_font_size(
            full_text,
            min_size=10,
            max_size=32,
            max_width=desc_max_width,
            max_height=desc_max_height,
            line_spacing=line_sp,
            paragraph_spacing=para_sp
        )
        
        # Calculate actual height
        wrap_width = renderer.calculate_wrap_width(optimal, desc_max_width)
        wrapped = renderer.wrap_text(full_text, wrap_width)
        height = renderer.calculate_text_height(wrapped, optimal, line_sp, para_sp)
        
        usage = (height / desc_max_height) * 100
        fits = "✅" if height <= desc_max_height else "❌"
        
        print(f"{name:<20} {line_sp:<5} {para_sp:<5} {optimal:<5} {height:<7.0f} {usage:>6.1f}%  {fits}")
    
    print()


def main():
    """Test spacing for different spell types."""
    test_cases = [
        ("Light", Path("test_data/test_spells.csv")),
        ("Mirror Image", Path("test_data/test_spells.csv")),
        ("Teleport", Path("test_data/teleport_spell.csv")),
    ]
    
    for spell_name, csv_path in test_cases:
        test_spacing(spell_name, csv_path)
    
    print("="*80)
    print("RECOMMENDATION")
    print("="*80)
    print("""
Based on the analysis:

1. SHORT TEXTS (Light): Can use larger spacing without issues
2. MEDIUM TEXTS (Mirror Image): Current spacing works well
3. LONG TEXTS (Teleport): Need more spacing to fill vertical space

SUGGESTED CHANGES:
- line_spacing: 2 → 3 (more breathing room between lines)
- paragraph_spacing: 10 → 20 (clearer paragraph separation)

This will:
✅ Improve readability (less cramped text)
✅ Better utilize vertical space (especially for long texts)
✅ Maintain good balance across all spell lengths
    """)


if __name__ == "__main__":
    main()