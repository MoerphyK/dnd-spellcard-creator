"""Generate all PDF modes for warlock spells."""

from pathlib import Path
import sys
import time

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
    """Generate warlock spell cards and create PDFs in all three modes."""
    print("="*80)
    print("WARLOCK SPELL CARDS - ALL PDF MODES")
    print("="*80)
    
    start_time = time.time()
    
    # Load data
    print("\n1. Loading warlock spell data...")
    csv_path = Path("../csv/warlock_spells.csv")
    spells = load_spell_data(csv_path)
    print(f"   ✅ Loaded {len(spells)} warlock spells")
    
    # Load assets
    print("\n2. Loading assets...")
    assets = load_assets(Path("../assets"))
    print("   ✅ Assets loaded successfully")
    
    # Generate card images
    print("\n3. Generating card images...")
    output_dir = Path("output/warlock_pdfs")
    generator = CardGenerator(assets)
    
    # Progress tracking
    progress_count = [0]
    def progress_callback(current, total, spell_name):
        progress_count[0] = current
        if current % 10 == 0 or current == total:
            print(f"   [{current}/{total}] {spell_name}")
    
    processor = BatchProcessor(generator, output_dir, progress_callback=progress_callback)
    results = processor.process_spells(spells)
    
    # Check for errors
    failed = [name for name, result in results.items() if not result.success]
    if failed:
        print(f"\n   ⚠️  {len(failed)} cards failed to generate:")
        for name in failed[:5]:  # Show first 5
            print(f"      - {name}")
        if len(failed) > 5:
            print(f"      ... and {len(failed) - 5} more")
    else:
        print(f"   ✅ Generated {len(spells) * 2} card images (100% success)")
    
    card_names = [spell.name for spell in spells]
    gen_time = time.time() - start_time
    
    # MODE 1: Grid Layout
    print("\n" + "="*80)
    print("MODE 1: GRID LAYOUT PDFs")
    print("="*80)
    
    print("\n  Creating 3×3 portrait grid...")
    pdf_start = time.time()
    config1 = GridConfig(rows=3, cols=3, orientation="portrait")
    pdf_gen1 = PDFGenerator(config1)
    result1 = pdf_gen1.generate_pdf(
        card_names,
        output_dir / "warlock_grid_3x3_portrait.pdf",
        output_dir
    )
    print(f"  ✅ warlock_grid_3x3_portrait.pdf")
    print(f"     {result1['total_cards']} cards, {result1['total_pages']} pages")
    print(f"     ({time.time() - pdf_start:.1f}s)")
    
    print("\n  Creating 2×4 landscape grid...")
    pdf_start = time.time()
    config2 = GridConfig(rows=2, cols=4, orientation="landscape")
    pdf_gen2 = PDFGenerator(config2)
    result2 = pdf_gen2.generate_pdf(
        card_names,
        output_dir / "warlock_grid_2x4_landscape.pdf",
        output_dir
    )
    print(f"  ✅ warlock_grid_2x4_landscape.pdf")
    print(f"     {result2['total_cards']} cards, {result2['total_pages']} pages")
    print(f"     ({time.time() - pdf_start:.1f}s)")
    
    # MODE 2: Single-Card A7
    print("\n" + "="*80)
    print("MODE 2: SINGLE-CARD A7 PDF")
    print("="*80)
    
    print("\n  Creating A7 single-card PDF...")
    pdf_start = time.time()
    pdf_gen3 = SingleCardPDFGenerator()
    result3 = pdf_gen3.generate_pdf(
        card_names,
        output_dir / "warlock_single_a7.pdf",
        output_dir
    )
    print(f"  ✅ warlock_single_a7.pdf")
    print(f"     {result3['total_cards']} cards, {result3['total_pages']} pages")
    print(f"     (2 pages per card: front, back)")
    print(f"     ({time.time() - pdf_start:.1f}s)")
    
    # MODE 3: Cut-Ready
    print("\n" + "="*80)
    print("MODE 3: CUT-READY PDFs")
    print("="*80)
    
    print("\n  Creating 2×2 cut-ready portrait...")
    pdf_start = time.time()
    config4 = GridConfig(rows=2, cols=2, orientation="portrait", margin=5, gap_x=5, gap_y=5)
    pdf_gen4 = CutReadyPDFGenerator(config4)
    result4 = pdf_gen4.generate_pdf(
        card_names,
        output_dir / "warlock_cut_ready_2x2_portrait.pdf",
        output_dir
    )
    print(f"  ✅ warlock_cut_ready_2x2_portrait.pdf")
    print(f"     {result4['total_cards']} cards, {result4['total_pages']} pages")
    print(f"     (Fixed 63.5×88.5mm, guidelines, bleed)")
    print(f"     ({time.time() - pdf_start:.1f}s)")
    
    print("\n  Creating 2×3 cut-ready landscape...")
    pdf_start = time.time()
    config5 = GridConfig(rows=2, cols=3, orientation="landscape", margin=5, gap_x=5, gap_y=5)
    pdf_gen5 = CutReadyPDFGenerator(config5)
    result5 = pdf_gen5.generate_pdf(
        card_names,
        output_dir / "warlock_cut_ready_2x3_landscape.pdf",
        output_dir
    )
    print(f"  ✅ warlock_cut_ready_2x3_landscape.pdf")
    print(f"     {result5['total_cards']} cards, {result5['total_pages']} pages")
    print(f"     (Fixed 63.5×88.5mm, guidelines, bleed)")
    print(f"     ({time.time() - pdf_start:.1f}s)")
    
    # Summary
    total_time = time.time() - start_time
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\n📊 Statistics:")
    print(f"   • Spells processed: {len(spells)}")
    print(f"   • Card images: {len(spells) * 2} (front + back)")
    print(f"   • PDF files created: 5")
    print(f"   • Total time: {total_time:.1f}s")
    print(f"   • Cards/second: {len(spells) / gen_time:.1f}")
    
    print(f"\n📄 PDF Files Created:")
    print(f"\n   Grid Layout (flexible scaling):")
    print(f"   • warlock_grid_3x3_portrait.pdf ({result1['total_pages']} pages)")
    print(f"   • warlock_grid_2x4_landscape.pdf ({result2['total_pages']} pages)")
    
    print(f"\n   Single-Card A7 (one per page):")
    print(f"   • warlock_single_a7.pdf ({result3['total_pages']} pages)")
    
    print(f"\n   Cut-Ready (professional printing):")
    print(f"   • warlock_cut_ready_2x2_portrait.pdf ({result4['total_pages']} pages)")
    print(f"   • warlock_cut_ready_2x3_landscape.pdf ({result5['total_pages']} pages)")
    
    print(f"\n📁 Output directory: {output_dir.absolute()}")
    
    print("\n💡 Printing Tips:")
    print("\n   Grid & Cut-Ready modes:")
    print("   1. Print odd pages (fronts)")
    print("   2. Flip paper stack HORIZONTALLY")
    print("   3. Print even pages (backs)")
    print("   4. Cut along guidelines (cut-ready only)")
    
    print("\n   Single-Card mode:")
    print("   1. Print all pages")
    print("   2. Pages alternate: front, back, front, back...")
    print("   3. Pair them up - done!")
    
    print("\n✅ All warlock spell PDFs ready for printing!")


if __name__ == "__main__":
    main()
