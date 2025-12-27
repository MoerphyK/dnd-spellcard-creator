"""Analyze vertical space usage on card backs."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Setup path for imports
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).parent.parent.parent))

from src.data_loader import load_spell_data, load_assets
from src.card_generator import CardGenerator
from src.text_renderer import TextRenderer


def analyze_text_area(spell_name: str, csv_path: Path):
    """Analyze how much vertical space is being used."""
    spells = load_spell_data(csv_path)
    spell = next((s for s in spells if s.name == spell_name), None)
    
    if not spell:
        print(f"Spell '{spell_name}' not found!")
        return
    
    print("="*80)
    print(f"VERTICAL SPACE ANALYSIS: {spell.name}")
    print("="*80)
    
    # Card dimensions
    card_width = 750
    card_height = 1045
    
    # Info box area
    info_top = 229
    info_height = 140
    info_bottom = info_top + info_height
    
    # Description area
    desc_top = info_bottom + 15  # 384
    desc_max_width = 574
    desc_max_height = 588
    desc_bottom = desc_top + desc_max_height  # 972
    
    print(f"\n📏 CARD DIMENSIONS:")
    print(f"  Total card: {card_width}x{card_height}px")
    print(f"  Info box: y={info_top}-{info_bottom} (height={info_height}px)")
    print(f"  Description: y={desc_top}-{desc_bottom} (height={desc_max_height}px)")
    print(f"  Bottom margin: {card_height - desc_bottom}px")
    
    # Analyze text
    from src.table_formatter import TableFormatter
    formatted_desc = TableFormatter.format_description_with_table(spell.description, max_width=80)
    
    if spell.at_higher_levels:
        full_text = f"Description:\n{formatted_desc}\n\n\nAt Higher Levels:\n{spell.at_higher_levels}"
    else:
        full_text = f"Description:\n{formatted_desc}"
    
    print(f"\n📝 TEXT CONTENT:")
    print(f"  Original description: {len(spell.description)} chars")
    print(f"  Formatted description: {len(formatted_desc)} chars")
    print(f"  Full text (with labels): {len(full_text)} chars")
    print(f"  Lines in text: {full_text.count(chr(10)) + 1}")
    
    # Test different font sizes
    assets = load_assets(Path("../assets"))
    renderer = TextRenderer(assets.font_path)
    
    print(f"\n🔍 FONT SIZE ANALYSIS:")
    print(f"  Current range: 10-32pt")
    print(f"  Current spacing: line=3, paragraph=20")
    
    for font_size in [10, 12, 14, 16, 18, 20, 24, 28, 32]:
        # Calculate wrap width
        wrap_width = renderer.calculate_wrap_width(font_size, desc_max_width)
        
        # Wrap text
        wrapped = renderer.wrap_text(full_text, wrap_width)
        
        # Calculate height with NEW spacing
        height = renderer.calculate_text_height(
            wrapped,
            font_size,
            line_spacing=3,
            paragraph_spacing=20
        )
        
        fits = "✅" if height <= desc_max_height else "❌"
        usage = (height / desc_max_height) * 100
        
        print(f"  {font_size:2d}pt: {height:4.0f}px / {desc_max_height}px ({usage:5.1f}% usage) {fits}")
    
    # Find optimal font size with NEW spacing
    optimal = renderer.find_optimal_font_size(
        full_text,
        min_size=10,
        max_size=32,
        max_width=desc_max_width,
        max_height=desc_max_height,
        line_spacing=3,
        paragraph_spacing=20
    )
    
    wrap_width = renderer.calculate_wrap_width(optimal, desc_max_width)
    wrapped = renderer.wrap_text(full_text, wrap_width)
    actual_height = renderer.calculate_text_height(wrapped, optimal, 3, 20)
    
    print(f"\n🎯 OPTIMAL FONT SIZE:")
    print(f"  Selected: {optimal}pt")
    print(f"  Actual height: {actual_height:.0f}px")
    print(f"  Available height: {desc_max_height}px")
    print(f"  Space usage: {(actual_height/desc_max_height)*100:.1f}%")
    print(f"  Unused space: {desc_max_height - actual_height:.0f}px")
    
    # Suggestions
    unused_pct = ((desc_max_height - actual_height) / desc_max_height) * 100
    
    print(f"\n💡 OPTIMIZATION SUGGESTIONS:")
    if unused_pct > 30:
        print(f"  ⚠️  {unused_pct:.0f}% of vertical space is unused!")
        print(f"  Consider:")
        print(f"    - Increasing max_font_size (currently 32pt)")
        print(f"    - Increasing line_spacing (currently 1)")
        print(f"    - Increasing paragraph_spacing (currently 10)")
    elif unused_pct > 15:
        print(f"  ℹ️  {unused_pct:.0f}% of vertical space is unused")
        print(f"  Could slightly increase font size or spacing for better readability")
    else:
        print(f"  ✅ Good space usage ({100-unused_pct:.0f}% filled)")


def main():
    """Analyze multiple spells."""
    test_cases = [
        ("Light", Path("test_data/test_spells.csv")),
        ("Mirror Image", Path("test_data/test_spells.csv")),
        ("Teleport", Path("test_data/teleport_spell.csv")),
    ]
    
    for spell_name, csv_path in test_cases:
        analyze_text_area(spell_name, csv_path)
        print("\n")


if __name__ == "__main__":
    main()