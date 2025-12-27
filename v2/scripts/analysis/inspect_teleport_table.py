"""Inspect the Teleportation table formatting in detail."""

from pathlib import Path

# Setup path for imports
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).parent.parent.parent))

from src.data_loader import load_spell_data
from src.table_formatter import TableFormatter


def main():
    """Inspect table formatting for Teleportation spell."""
    # Load the teleportation spell
    csv_path = Path("test_data/teleport_spell.csv")
    spells = load_spell_data(csv_path)
    
    if not spells:
        print("No spells loaded!")
        return
    
    spell = spells[0]
    
    print("="*70)
    print("TELEPORTATION SPELL - TABLE INSPECTION")
    print("="*70)
    
    print("\n1. ORIGINAL DESCRIPTION (first 500 chars):")
    print("-"*70)
    print(spell.description[:500])
    print("...")
    
    print("\n2. TABLE DETECTION:")
    print("-"*70)
    has_table = TableFormatter.detect_table(spell.description)
    print(f"Table detected: {has_table}")
    
    print("\n3. EXTRACT TABLE SECTION:")
    print("-"*70)
    before, table, after = TableFormatter.extract_table_section(spell.description)
    if table:
        print(f"Before text length: {len(before)} chars")
        print(f"Table text length: {len(table)} chars")
        print(f"After text length: {len(after)} chars")
        print("\nTable text:")
        print(table[:300])
    else:
        print("No table extracted!")
    
    print("\n4. PARSE TABLE:")
    print("-"*70)
    if table:
        rows = TableFormatter.parse_teleportation_table(table)
        print(f"Parsed {len(rows)} rows")
        for row in rows:
            print(row)
    
    print("\n5. FORMATTED TABLE (width=70):")
    print("-"*70)
    if table:
        formatted = TableFormatter.format_table_text(table, max_width=70)
        print(formatted)
    
    print("\n6. FULL FORMATTED DESCRIPTION (width=70):")
    print("-"*70)
    formatted_desc = TableFormatter.format_description_with_table(spell.description, max_width=70)
    print(formatted_desc)
    
    print("\n7. CHARACTER COUNTS:")
    print("-"*70)
    print(f"Original: {len(spell.description)} chars")
    print(f"Formatted: {len(formatted_desc)} chars")
    print(f"Reduction: {len(spell.description) - len(formatted_desc)} chars ({(1 - len(formatted_desc)/len(spell.description))*100:.1f}%)")


if __name__ == "__main__":
    main()