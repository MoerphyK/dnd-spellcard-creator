"""Example script demonstrating PDF generation with grid layout."""

from pathlib import Path
import sys

# Setup path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.data_loader import load_spell_data, load_assets
from src.card_generator import CardGenerator
from src.batch_processor import BatchProcessor
from src.pdf_generator import PDFGenerator, GridConfig


def main():
    """Generate cards and create PDF with grid layout."""
    print("="*80)
    print("PDF GENERATION EXAMPLE")
    print("="*80)
    
    # Load data
    print("\n1. Loading spell data...")
    csv_path = Path("test_data/test_spells.csv")
    spells = load_spell_data(csv_path)
    print(f"   Loaded {len(spells)} spells")
    
    # Load assets
    print("\n2. Loading assets...")
    assets = load_assets(Path("../assets"))
    print("   Assets loaded successfully")
    
    # Generate card images
    print("\n3. Generating card images...")
    output_dir = Path("output/pdf_test")
    generator = CardGenerator(assets)
    
    def progress_callback(current, total, spell_name):
        print(f"   [{current}/{total}] {spell_name}")
    
    processor = BatchProcessor(generator, output_dir, progress_callback=progress_callback)
    processor.process_spells(spells)
    print(f"   Generated {len(spells) * 2} card images")
    
    # Create PDF with different grid configurations
    card_names = [spell.name for spell in spells]
    
    # Configuration 1: 3x3 portrait (default)
    print("\n4. Creating PDF: 3x3 portrait grid...")
    config1 = GridConfig(rows=3, cols=3, orientation="portrait")
    pdf_gen1 = PDFGenerator(config1)
    result1 = pdf_gen1.generate_pdf(
        card_names,
        Path("output/pdf_test/cards_3x3_portrait.pdf"),
        output_dir
    )
    print(f"   ✅ Created: cards_3x3_portrait.pdf")
    print(f"      Cards: {result1['total_cards']}, Pages: {result1['total_pages']}")
    
    # Configuration 2: 2x4 landscape
    print("\n5. Creating PDF: 2x4 landscape grid...")
    config2 = GridConfig(rows=2, cols=4, orientation="landscape")
    pdf_gen2 = PDFGenerator(config2)
    result2 = pdf_gen2.generate_pdf(
        card_names,
        Path("output/pdf_test/cards_2x4_landscape.pdf"),
        output_dir
    )
    print(f"   ✅ Created: cards_2x4_landscape.pdf")
    print(f"      Cards: {result2['total_cards']}, Pages: {result2['total_pages']}")
    
    # Configuration 3: 4x2 portrait (more cards per page)
    print("\n6. Creating PDF: 4x2 portrait grid...")
    config3 = GridConfig(rows=4, cols=2, orientation="portrait")
    pdf_gen3 = PDFGenerator(config3)
    result3 = pdf_gen3.generate_pdf(
        card_names,
        Path("output/pdf_test/cards_4x2_portrait.pdf"),
        output_dir
    )
    print(f"   ✅ Created: cards_4x2_portrait.pdf")
    print(f"      Cards: {result3['total_cards']}, Pages: {result3['total_pages']}")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Generated {len(spells)} spell cards")
    print(f"Created 3 PDF files with different grid layouts")
    print(f"Output directory: {output_dir}")
    print("\nPDF files:")
    print("  - cards_3x3_portrait.pdf   (3 rows × 3 cols, portrait)")
    print("  - cards_2x4_landscape.pdf  (2 rows × 4 cols, landscape)")
    print("  - cards_4x2_portrait.pdf   (4 rows × 2 cols, portrait)")
    print("\n✅ All PDFs ready for double-sided printing!")
    print("   (Print front page, flip horizontally, print back page)")


if __name__ == "__main__":
    main()
