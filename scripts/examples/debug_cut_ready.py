"""Debug script to check what's happening with cut-ready generation."""

from pathlib import Path
import sys

# Setup path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.data_loader import load_spell_data, load_assets
from src.card_generator import CardGenerator
from src.batch_processor import BatchProcessor
from src.pdf_generator import CutReadyPDFGenerator, GridConfig


def main():
    """Debug cut-ready PDF generation."""
    print("="*80)
    print("DEBUG: Cut-Ready PDF Generation")
    print("="*80)
    
    # Load 5 spells to test
    csv_path = Path("../csv/warlock_spells.csv")
    spells = load_spell_data(csv_path)
    spells = spells[:5]  # Only first 5
    
    print(f"\nLoaded {len(spells)} spells:")
    for i, spell in enumerate(spells):
        print(f"  {i}: {spell.name}")
    
    # Load assets and generate cards
    assets = load_assets(Path("../assets"))
    output_dir = Path("output/debug_cut_ready")
    generator = CardGenerator(assets)
    processor = BatchProcessor(generator, output_dir)
    processor.process_spells(spells)
    
    card_names = [spell.name for spell in spells]
    print(f"\nCard names list: {card_names}")
    
    # Create 2×2 cut-ready PDF (4 cards per page)
    print("\n" + "="*80)
    print("Creating 2×2 cut-ready PDF...")
    print("="*80)
    
    config = GridConfig(rows=2, cols=2, orientation="portrait", margin=5, gap_x=5, gap_y=5)
    pdf_gen = CutReadyPDFGenerator(config)
    
    # Manually check grouping logic
    cards_per_page = config.rows * config.cols
    print(f"\nCards per page: {cards_per_page}")
    print(f"Total cards: {len(card_names)}")
    
    groups = []
    for i in range(0, len(card_names), cards_per_page):
        group = card_names[i:i + cards_per_page]
        if len(group) < cards_per_page:
            group.extend([None] * (cards_per_page - len(group)))
        groups.append(group)
    
    print(f"\nNumber of groups: {len(groups)}")
    for i, group in enumerate(groups):
        print(f"\nGroup {i}:")
        for j, card in enumerate(group):
            print(f"  Position {j}: {card if card else 'EMPTY'}")
        
        # Check if group is all None
        all_none = all(card is None for card in group)
        print(f"  All None? {all_none}")
    
    # Generate PDF
    result = pdf_gen.generate_pdf(
        card_names,
        output_dir / "debug_cut_ready.pdf",
        output_dir
    )
    
    print(f"\n" + "="*80)
    print("RESULT")
    print("="*80)
    print(f"Total cards: {result['total_cards']}")
    print(f"Total pages: {result['total_pages']}")
    print(f"Missing files: {len(result['missing_files'])}")
    
    print(f"\nExpected:")
    print(f"  - Group 0: 4 cards (full page)")
    print(f"  - Group 1: 1 card + 3 empty slots")
    print(f"  - Total: 2 groups = 4 pages (2 front + 2 back)")
    
    print(f"\nActual:")
    print(f"  - Total pages: {result['total_pages']}")


if __name__ == "__main__":
    main()
