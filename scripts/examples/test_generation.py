#!/usr/bin/env python3
"""Quick test script to generate a few spell cards."""

from pathlib import Path

# Setup path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.data_loader import load_spell_data, load_assets
from src.card_generator import CardGenerator


def main():
    # Paths
    csv_path = Path("test_data/test_spells.csv")
    assets_dir = Path("../assets")  # Use v1 assets
    illustrations_dir = Path("../assets/illustrations")
    output_dir = Path("output")
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    print("Loading spell data...")
    spells = load_spell_data(csv_path, illustrations_dir)
    print(f"Loaded {len(spells)} spells")
    
    print("\nLoading assets...")
    assets = load_assets(assets_dir)
    
    # Validate assets
    missing = assets.validate()
    if missing:
        print(f"Warning: Missing assets:")
        for m in missing[:5]:  # Show first 5
            print(f"  - {m}")
    
    print("\nGenerating cards...")
    generator = CardGenerator(assets)
    
    for spell in spells:
        print(f"  Generating: {spell.name}")
        
        # Generate front
        front_path = output_dir / f"{spell.name}_front.png"
        generator.generate_card_front(spell, front_path)
        print(f"    ✓ Front: {front_path}")
        
        # Generate back
        back_path = output_dir / f"{spell.name}_back.png"
        generator.generate_card_back(spell, back_path)
        print(f"    ✓ Back: {back_path}")
    
    print(f"\n✅ Generated {len(spells)} cards in {output_dir}/")


if __name__ == "__main__":
    main()
