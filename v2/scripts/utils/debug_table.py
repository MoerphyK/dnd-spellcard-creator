#!/usr/bin/env python3
"""Debug table parsing."""

from pathlib import Path

# Setup path for imports
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).parent.parent.parent))

from src.data_loader import load_spell_data

csv_path = Path("test_data/teleport_spell.csv")
spells = load_spell_data(csv_path)
spell = spells[0]

# Find the table section
table_start = spell.description.find("Teleportation Outcome")
table_section = spell.description[table_start:table_start+500]

print("RAW TABLE SECTION:")
print("=" * 70)
print(table_section)
print("=" * 70)

# Show character by character for the first row
print("\nFIRST DATA ROW (Permanent circle):")
perm_start = spell.description.find("Permanent circle")
perm_section = spell.description[perm_start:perm_start+50]
print(repr(perm_section))

print("\nSECOND DATA ROW (Linked object):")
link_start = spell.description.find("Linked object")
link_section = spell.description[link_start:link_start+50]
print(repr(link_section))

print("\nTHIRD DATA ROW (Very familiar):")
very_start = spell.description.find("Very familiar")
very_section = spell.description[very_start:very_start+50]
print(repr(very_section))