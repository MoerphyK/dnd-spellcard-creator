#!/usr/bin/env python3
"""Convenience wrapper for running the spell card generator CLI.

Usage:
    python spell-cards.py --csv spells.csv --pdf-mode grid
    
Or make it executable:
    chmod +x spell-cards.py
    ./spell-cards.py --csv spells.csv --pdf-mode grid
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.cli import main

if __name__ == '__main__':
    main()
