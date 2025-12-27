"""Example script demonstrating all PDF generation modes."""

from pathlib import Path
import sys

# Setup path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.data_loader import load_spell_data, load_assets
from src.card_generator import CardGenerator
from src.batch_processor import BatchProcessor
from src.pdf_generator import (
    PDFGenerator,
    SingleCardPDFGenerator,
    CutReadyPDFGenerator,
    GridConfig
)


def main():
    """Generate cards and create PDFs in all three modes."""
    print("="*80)
    print("PDF GENERATION - ALL MODES")
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
    output_dir = Path("output/all_pdf_modes")
    generator = CardGenerator(assets)
    
    def progress_callback(current, total, spell_name):
        print(f"   [{current}/{total}] {spell_name}")
    
    processor = BatchProcessor(generator, output_dir, progress_callback=progress_callback)
    processor.process_spells(spells)
    print(f"   Generated {len(spells) * 2} card images")
    
    card_names = [spell.name for spell in spells]
    
    # MODE 1: Grid Layout (flexible, scales to fit)
    print("\n" + "="*80)
    print("MODE 1: GRID LAYOUT (Flexible Scaling)")
    print("="*80)
    print("Best for: Home printing, maximum cards per page")
    print("Features: Cards scale to fit, configurable grid size")
    
    print("\n  Creating 3×3 portrait grid...")
    config1 = GridConfig(rows=3, cols=3, orientation="portrait")
    pdf_gen1 = PDFGenerator(config1)
    result1 = pdf_gen1.generate_pdf(
        card_names,
        output_dir / "mode1_grid_3x3.pdf",
        output_dir
    )
    print(f"  ✅ mode1_grid_3x3.pdf - {result1['total_pages']} pages")
    
    # MODE 2: Single-Card A7 (one card per page)
    print("\n" + "="*80)
    print("MODE 2: SINGLE-CARD A7 PAGES")
    print("="*80)
    print("Best for: Individual cards, easy assembly")
    print("Features: One card per A7 page, alternating front/back")
    
    print("\n  Creating A7 single-card PDF...")
    pdf_gen2 = SingleCardPDFGenerator()
    result2 = pdf_gen2.generate_pdf(
        card_names,
        output_dir / "mode2_single_a7.pdf",
        output_dir
    )
    print(f"  ✅ mode2_single_a7.pdf - {result2['total_pages']} pages")
    print(f"     (2 pages per card: front, then back)")
    
    # MODE 3: Cut-Ready (fixed dimensions, guidelines, bleed)
    print("\n" + "="*80)
    print("MODE 3: CUT-READY (Professional Printing)")
    print("="*80)
    print("Best for: Professional printing and cutting")
    print("Features: Fixed card size (63.5×88.5mm), cut guidelines, bleed borders")
    print("          Perfect double-sided alignment")
    
    print("\n  Creating 2×2 cut-ready PDF (portrait)...")
    config3 = GridConfig(rows=2, cols=2, orientation="portrait", margin=5, gap_x=5, gap_y=5)
    pdf_gen3 = CutReadyPDFGenerator(config3)
    result3 = pdf_gen3.generate_pdf(
        card_names,
        output_dir / "mode3_cut_ready_2x2.pdf",
        output_dir
    )
    print(f"  ✅ mode3_cut_ready_2x2.pdf - {result3['total_pages']} pages")
    
    print("\n  Creating 2×3 cut-ready PDF (landscape)...")
    config4 = GridConfig(rows=2, cols=3, orientation="landscape", margin=5, gap_x=5, gap_y=5)
    pdf_gen4 = CutReadyPDFGenerator(config4)
    result4 = pdf_gen4.generate_pdf(
        card_names,
        output_dir / "mode3_cut_ready_2x3_landscape.pdf",
        output_dir
    )
    print(f"  ✅ mode3_cut_ready_2x3_landscape.pdf - {result4['total_pages']} pages")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Generated {len(spells)} spell cards")
    print(f"Created 4 PDF files in 3 different modes")
    print(f"Output directory: {output_dir}")
    
    print("\n📄 PDF Files Created:")
    print("\n  MODE 1 - Grid Layout:")
    print("    • mode1_grid_3x3.pdf")
    print("      - 3×3 grid, portrait orientation")
    print("      - Cards scale to fit page")
    print("      - Good for home printing")
    
    print("\n  MODE 2 - Single-Card A7:")
    print("    • mode2_single_a7.pdf")
    print("      - One card per A7 page")
    print("      - Alternates front/back")
    print("      - Easy to assemble")
    
    print("\n  MODE 3 - Cut-Ready:")
    print("    • mode3_cut_ready_2x2.pdf (portrait)")
    print("    • mode3_cut_ready_2x3_landscape.pdf (landscape)")
    print("      - Fixed card dimensions (63.5×88.5mm)")
    print("      - Cut guidelines (dashed lines)")
    print("      - Bleed borders (1.5mm)")
    print("      - Perfect double-sided alignment")
    
    print("\n📋 Printing Instructions:")
    print("\n  Grid & Cut-Ready Modes:")
    print("    1. Print odd pages (fronts)")
    print("    2. Flip paper stack HORIZONTALLY")
    print("    3. Print even pages (backs)")
    print("    4. Cut along guidelines (cut-ready mode only)")
    
    print("\n  Single-Card Mode:")
    print("    1. Print all pages")
    print("    2. Pages alternate: front, back, front, back...")
    print("    3. Pair them up and you're done!")
    
    print("\n✅ All PDFs ready!")


if __name__ == "__main__":
    main()
