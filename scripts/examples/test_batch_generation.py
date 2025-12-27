"""Test batch generation with real spell data."""

from pathlib import Path

# Setup path for imports
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).parent.parent.parent))

from src.data_loader import load_spell_data, load_assets
from src.card_generator import CardGenerator
from src.batch_processor import BatchProcessor


def main():
    """Test batch generation with multiple spells."""
    # Paths
    csv_path = Path("test_data/test_spells.csv")
    assets_dir = Path("../assets")
    output_dir = Path("output/batch_test")
    
    print("Loading spell data...")
    spells = load_spell_data(csv_path)
    print(f"Loaded {len(spells)} spells")
    
    print("\nLoading assets...")
    assets = load_assets(assets_dir)
    print("Assets loaded successfully")
    
    print("\nInitializing card generator...")
    card_generator = CardGenerator(assets)
    
    print("\nInitializing batch processor...")
    
    def progress_callback(current, total, spell_name):
        """Print progress updates."""
        print(f"  [{current}/{total}] Processing: {spell_name}")
    
    batch_processor = BatchProcessor(
        card_generator=card_generator,
        output_dir=output_dir,
        progress_callback=progress_callback
    )
    
    print("\nProcessing spells...")
    results = batch_processor.process_spells(spells)
    
    print("\n" + "="*60)
    print("BATCH PROCESSING COMPLETE")
    print("="*60)
    
    # Print summary
    summary = batch_processor.get_summary(results)
    print(f"\nTotal spells:     {summary['total']}")
    print(f"Successful:       {summary['successful']}")
    print(f"Failed:           {summary['failed']}")
    print(f"Success rate:     {summary['success_rate']*100:.1f}%")
    
    if summary['errors']:
        print("\nErrors:")
        for spell_name, error in summary['errors'].items():
            print(f"  - {spell_name}: {error}")
    
    print(f"\nOutput directory: {output_dir.absolute()}")
    
    # List generated files
    if output_dir.exists():
        files = sorted(output_dir.glob("*.png"))
        print(f"\nGenerated {len(files)} files:")
        for file in files:
            size_kb = file.stat().st_size / 1024
            print(f"  - {file.name} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()