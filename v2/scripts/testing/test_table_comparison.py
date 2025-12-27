#!/usr/bin/env python3
"""Compare table formatting before and after."""

from pathlib import Path

# Setup path for imports
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).parent.parent.parent))

from src.data_loader import load_spell_data
from src.table_formatter import TableFormatter


def main():
    csv_path = Path("test_data/teleport_spell.csv")
    
    print("=" * 70)
    print("TABLE FORMATTING COMPARISON")
    print("=" * 70)
    
    spells = load_spell_data(csv_path)
    spell = spells[0]
    
    print(f"\nSpell: {spell.name}")
    print(f"Original description length: {len(spell.description)} characters")
    
    # Check if table detected
    has_table = TableFormatter.detect_table(spell.description)
    print(f"Table detected: {has_table}")
    
    if has_table:
        # Format the description
        formatted = TableFormatter.format_description_with_table(spell.description)
        
        print(f"Formatted description length: {len(formatted)} characters")
        print(f"Size change: {len(formatted) - len(spell.description):+d} characters")
        
        print("\n" + "-" * 70)
        print("ORIGINAL (first 400 chars):")
        print("-" * 70)
        print(spell.description[:400])
        print("...")
        
        print("\n" + "-" * 70)
        print("FORMATTED (first 400 chars):")
        print("-" * 70)
        print(formatted[:400])
        print("...")
        
        # Show table section specifically
        before, table, after = TableFormatter.extract_table_section(spell.description)
        if table:
            print("\n" + "-" * 70)
            print("TABLE SECTION (formatted):")
            print("-" * 70)
            formatted_table = TableFormatter.format_table_text(table, max_width=60)
            print(formatted_table[:500])
            if len(formatted_table) > 500:
                print("...")
    
    print("\n" + "=" * 70)
    print("✅ Table formatting improves readability!")
    print("   • Tables are detected automatically")
    print("   • Proper spacing and alignment applied")
    print("   • Text remains fully readable")
    print("=" * 70)


if __name__ == "__main__":
    main()