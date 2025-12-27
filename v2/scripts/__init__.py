"""Scripts package - adds parent directory to path for imports."""

import sys
from pathlib import Path

# Add parent directory (v2/) to Python path so we can import from src/
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))
