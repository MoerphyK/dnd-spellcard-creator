#!/usr/bin/env python3
"""Test spell with table formatting (Teleport)."""

from pathlib import Path

# Setup path for imports
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).parent.parent.parent))

from src.data_loader import load_spell_data, load_assets
from src.card_generator import CardGenerator


def main():
    csv_path = Path("test_data/teleport_spell.csv")
    assets_dir = Path("../assets")
    illustrations_dir = Path("../assets/illustrations")
    output_dir = Path("output/table_test")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("TABLE FORMATTING TEST - Teleport Spell")
    print("=" * 70)
    
    print("\nLoading spell data...")
    spells = load_spell_data(csv_path, illustrations_dir)
    spell = spells[0]
    
    print(f"\nSpell: {spell.name}")
    print(f"Description length: {len(spell.description)} characters")
    print("\nDescription preview (first 500 chars):")
    print("-" * 70)
    print(spell.description[:500] + "...")
    print("-" * 70)
    
    # Check if it contains table-like content
    if "Familiarity" in spell.description and "Mishap" in spell.description:
        print("\n⚠️  DETECTED: Table content in description")
        print("   Contains: Teleportation Outcome table")
    
    print("\nLoading assets...")
    assets = load_assets(assets_dir)
    
    print("\nGenerating cards...")
    generator = CardGenerator(assets)
    
    try:
        # Generate front
        front_path = output_dir / f"{spell.name}_front.png"
        generator.generate_card_front(spell, front_path)
        print(f"✓ Front generated: {front_path}")
        
        # Generate back
        back_path = output_dir / f"{spell.name}_back.png"
        generator.generate_card_back(spell, back_path)
        print(f"✓ Back generated: {back_path}")
        
        # Check file sizes
        front_size = front_path.stat().st_size / 1024
        back_size = back_path.stat().st_size / 1024
        
        print(f"\nFile sizes:")
        print(f"  Front: {front_size:.1f}KB")
        print(f"  Back: {back_size:.1f}KB")
        
        print("\n" + "=" * 70)
        print("✅ Table spell generated successfully!")
        print("\nNOTE: The table is rendered as plain text with the current")
        print("      implementation. The text fitting algorithm will adjust")
        print("      font size to fit all content on the card.")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()