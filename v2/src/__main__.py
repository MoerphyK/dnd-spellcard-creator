"""Allow running the spell card generator as a module.

Usage:
    python -m src --csv spells.csv --pdf-mode grid
"""

from .cli import main

if __name__ == '__main__':
    main()
