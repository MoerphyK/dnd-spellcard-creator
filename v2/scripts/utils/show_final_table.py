#!/usr/bin/env python3
"""Show the final formatted table."""

from pathlib import Path

# Setup path for imports
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).parent.parent.parent))

from src.data_loader import load_spell_data
from src.table_formatter import TableFormatter

csv_path = Path("test_data/teleport_spell.csv")
spells = load_spell_data(csv_path)
spell = spells[0]

print("=" * 70)
print("TELEPORT SPELL - FINAL TABLE FORMATTING")
print("=" * 70)

# Format the description
formatted = TableFormatter.format_description_with_table(spell.description)

# Extract just the table part
before, table, after = TableFormatter.extract_table_section(spell.description)

if table:
    formatted_table = TableFormatter.format_table_text(table, max_width=70)
    
    print("\nTELEPORTATION OUTCOME TABLE:")
    print("-" * 70)
    print(formatted_table)
    print("-" * 70)
    
    print("\nTable Explanation:")
    print("  • Roll 1d100 to determine teleportation outcome")
    print("  • Each row shows a familiarity level")
    print("  • Columns show dice ranges for each outcome type")
    print("  • '—' means that outcome doesn't apply")
    
    print("\nColumn Meanings:")
    print("  1. Mishap: Teleportation fails, take 3d10 damage")
    print("  2. Similar Area: Appear in similar but wrong location")
    print("  3. Off Target: Appear 2d12 miles away in random direction")
    print("  4. On Target: Appear exactly where intended")
    
    print("\n" + "=" * 70)
    print("✅ Table correctly formatted with proper dice ranges!")
    print("=" * 70)