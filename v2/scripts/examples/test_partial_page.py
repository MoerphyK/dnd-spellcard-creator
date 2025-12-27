"""Test cut-ready mode with partial pages to verify empty slots are handled correctly."""

from pathlib import Path
import sys

# Setup path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.data_loader import load_spell_data, load_assets
from src.card_generator import CardGenerator
from src.batch_processor import BatchProcessor
from src.pdf_generator import CutReadyPDFGenerator, GridConfig


def main():
    """Generate cut-ready PDF with partial page to test empty slot handling."""
    print("="*80)
    print("PARTIAL PAGE TEST - Cut-Ready Mode")
    print("="*80)
    
    # Load data - only 5 spells
    print("\n1. Loading test spell data...")
    csv_path = Path("test_data/test_spells.csv")
    spells = load_spell_data(csv_path)
    # Take only first 5 spells to create partial pages
    spells = spells[:3] if len(spells) >= 3 else spells
    print(f"   Loaded {len(spells)} spells (for partial page testing)")
    
    # Load assets
    print("\n2. Loading assets...")
    assets = load_assets(Path("../assets"))
    print("   Assets loaded successfully")
    
    # Generate card images
    print("\n3. Generating card images...")
    output_dir = Path("output/partial_page_test")
    generator = CardGenerator(assets)
    processor = BatchProcessor(generator, output_dir)
    processor.process_spells(spells)
    print(f"   Generated {len(spells) * 2} card images")
    
    card_names = [spell.name for spell in spells]
    
    # Test cut-ready with 2×2 grid (4 cards per page)
    # With 3 cards, we'll have:
    # - Page 1 (front): 3 cards + 1 empty slot
    # - Page 2 (back): 3 cards + 1 empty slot
    print("\n4. Creating cut-ready PDF with partial page...")
    print("   Grid: 2×2 (4 cards per page)")
    print(f"   Cards: {len(spells)} (will have 1 empty slot)")
    
    config = GridConfig(rows=2, cols=2, orientation="portrait", margin=5, gap_x=5, gap_y=5)
    pdf_gen = CutReadyPDFGenerator(config)
    result = pdf_gen.generate_pdf(
        card_names,
        output_dir / "partial_page_cut_ready.pdf",
        output_dir
    )
    
    print(f"\n   ✅ partial_page_cut_ready.pdf created")
    print(f"      Cards: {result['total_cards']}")
    print(f"      Pages: {result['total_pages']}")
    print(f"      Expected: 2 pages (1 front + 1 back)")
    
    print("\n" + "="*80)
    print("VERIFICATION")
    print("="*80)
    print("\nPlease check the PDF:")
    print("  ✓ Page 1 (front): Should have 3 cards + 1 empty white slot")
    print("  ✓ Page 2 (back): Should have 3 cards + 1 empty white slot")
    print("  ✓ Black bleed borders only around filled cards")
    print("  ✓ Cut guidelines only at edges of filled cards")
    print("  ✓ Empty slots should be completely white (no black fill)")
    
    print(f"\n📁 Output: {output_dir.absolute()}/partial_page_cut_ready.pdf")
    print("\n✅ Test complete!")


if __name__ == "__main__":
    main()
