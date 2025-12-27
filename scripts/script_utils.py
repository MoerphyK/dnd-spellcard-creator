"""Utility functions for scripts - handles path setup."""

import sys
from pathlib import Path


def setup_path():
    """Add v2/ directory to Python path for imports."""
    # Get v2/ directory (parent of scripts/)
    v2_dir = Path(__file__).parent.parent
    
    # Add to path if not already there
    v2_dir_str = str(v2_dir)
    if v2_dir_str not in sys.path:
        sys.path.insert(0, v2_dir_str)


# Auto-setup when imported
setup_path()
