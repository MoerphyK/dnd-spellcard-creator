"""Show the table formatting improvement."""

from pathlib import Path

# Setup path for imports
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).parent.parent.parent))

from src.data_loader import load_spell_data
from src.table_formatter import TableFormatter


def main():
    """Show table formatting at different widths."""
    csv_path = Path("test_data/teleport_spell.csv")
    spells = load_spell_data(csv_path)
    spell = spells[0]
    
    before, table, after = TableFormatter.extract_table_section(spell.description)
    
    print("="*80)
    print("TABLE FORMATTING IMPROVEMENT")
    print("="*80)
    
    print("\n📊 ORIGINAL TABLE DATA (from CSV):")
    print("-"*80)
    print("Raw format (no spaces between columns):")
    print(table[:200] + "...")
    
    print("\n\n🔧 FORMATTED AT DIFFERENT WIDTHS:")
    print("="*80)
    
    widths = [60, 70, 80]
    for width in widths:
        print(f"\n{'='*80}")
        print(f"Width = {width} characters")
        print(f"{'='*80}")
        formatted = TableFormatter.format_table_text(table, max_width=width)
        print(formatted)
        
        # Check for truncation
        if "…" in formatted:
            print("\n⚠️  Contains truncated text (…)")
        else:
            print("\n✅ All text fully visible!")
    
    print("\n\n" + "="*80)
    print("RECOMMENDATION")
    print("="*80)
    print("""
✅ Use max_width=80 for card generation
   - All column headers fully visible
   - All data fully visible  
   - No truncation needed
   - Fits comfortably in 574px card width
    """)
    
    print("\n" + "="*80)
    print("COLUMN REQUIREMENTS")
    print("="*80)
    rows = TableFormatter.parse_teleportation_table(table)
    num_cols = len(rows[0])
    col_widths = [0] * num_cols
    
    for row in rows:
        for i, cell in enumerate(row):
            if i < num_cols:
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    print("\nColumn widths needed:")
    for i, width in enumerate(col_widths):
        print(f"  {rows[0][i]:20s}: {width:2d} chars")
    
    total = sum(col_widths) + (num_cols - 1) * 3
    print(f"\nTotal: {sum(col_widths)} + {(num_cols-1)*3} spacing = {total} chars")
    print(f"Minimum width needed: {total} chars")


if __name__ == "__main__":
    main()