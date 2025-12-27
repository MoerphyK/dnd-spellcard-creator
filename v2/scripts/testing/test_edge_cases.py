#!/usr/bin/env python3
"""Test edge cases: long descriptions, special formatting, etc."""

from pathlib import Path

# Setup path for imports
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).parent.parent.parent))

from src.data_loader import load_spell_data, load_assets
from src.card_generator import CardGenerator


def main():
    # Paths
    csv_path = Path("test_data/edge_case_spells.csv")
    assets_dir = Path("../assets")
    illustrations_dir = Path("../assets/illustrations")
    output_dir = Path("output/edge_cases")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("EDGE CASE TESTING")
    print("=" * 60)
    
    print("\nLoading spell data...")
    spells = load_spell_data(csv_path, illustrations_dir)
    print(f"Loaded {len(spells)} edge case spells\n")
    
    # Print spell info
    for spell in spells:
        desc_len = len(spell.description)
        has_higher = "Yes" if spell.at_higher_levels else "No"
        print(f"  • {spell.name}")
        print(f"    Description length: {desc_len} chars")
        print(f"    Has 'At Higher Levels': {has_higher}")
        print(f"    Components: {spell.components}")
        print()
    
    print("Loading assets...")
    assets = load_assets(assets_dir)
    
    print("\nGenerating cards...")
    print("-" * 60)
    
    generator = CardGenerator(assets)
    
    for i, spell in enumerate(spells, 1):
        print(f"\n[{i}/{len(spells)}] {spell.name}")
        print(f"  Description: {len(spell.description)} chars")
        
        try:
            # Generate front
            front_path = output_dir / f"{spell.name}_front.png"
            generator.generate_card_front(spell, front_path)
            print(f"  ✓ Front generated")
            
            # Generate back
            back_path = output_dir / f"{spell.name}_back.png"
            generator.generate_card_back(spell, back_path)
            print(f"  ✓ Back generated")
            
            if spell.at_higher_levels:
                print(f"  ℹ Includes 'At Higher Levels' section")
            
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"✅ Edge case testing complete!")
    print(f"   Cards saved to: {output_dir}/")
    print("=" * 60)


if __name__ == "__main__":
    main()