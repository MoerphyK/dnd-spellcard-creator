"""Debug table column width calculation."""

from pathlib import Path

# Setup path for imports
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).parent.parent.parent))

from src.data_loader import load_spell_data
from src.table_formatter import TableFormatter


def main():
    """Debug table width calculation."""
    csv_path = Path("test_data/teleport_spell.csv")
    spells = load_spell_data(csv_path)
    spell = spells[0]
    
    before, table, after = TableFormatter.extract_table_section(spell.description)
    rows = TableFormatter.parse_teleportation_table(table)
    
    print("="*70)
    print("TABLE WIDTH CALCULATION DEBUG")
    print("="*70)
    
    print("\nParsed rows:")
    for i, row in enumerate(rows):
        print(f"Row {i}: {row}")
    
    print("\nColumn widths needed:")
    num_cols = len(rows[0])
    col_widths = [0] * num_cols
    
    for row in rows:
        for i, cell in enumerate(row):
            if i < num_cols:
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    for i, width in enumerate(col_widths):
        print(f"  Column {i} ({rows[0][i]}): {width} chars")
    
    spacing = 3
    total = sum(col_widths) + (num_cols - 1) * spacing
    print(f"\nTotal width needed: {sum(col_widths)} + {(num_cols-1)*spacing} spacing = {total} chars")
    print(f"Max width available: 70 chars")
    print(f"Fits without scaling: {total <= 70}")
    
    # Test with different widths
    for max_width in [60, 70, 80]:
        print(f"\n{'='*70}")
        print(f"Testing with max_width={max_width}")
        print(f"{'='*70}")
        formatted = TableFormatter.format_table_text(table, max_width=max_width)
        print(formatted)


if __name__ == "__main__":
    main()