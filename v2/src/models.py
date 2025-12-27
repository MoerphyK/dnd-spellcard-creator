"""Data models for spell card generator."""

from dataclasses import dataclass
from typing import Optional, List
from pathlib import Path


@dataclass
class SpellData:
    """Represents a D&D spell with all its properties."""
    
    name: str
    level: str
    casting_time: str
    duration: str
    range: str
    components: str
    classes: List[str]
    description: str
    at_higher_levels: Optional[str] = None
    illustration_path: Optional[Path] = None
    
    @property
    def components_short(self) -> str:
        """Return simplified component string (V, S, M only, no materials)."""
        if "(" in self.components and ")" in self.components:
            return self.components.split("(")[0].strip()
        return self.components
    
    @property
    def level_numeric(self) -> str:
        """Return numeric level (0 for Cantrip, strip ordinal suffixes)."""
        if self.level == "Cantrip":
            return "0"
        # Remove ordinal suffixes (st, nd, rd, th)
        for suffix in ["st", "nd", "rd", "th"]:
            if self.level.endswith(suffix):
                return self.level[:-2]
        return self.level


@dataclass
class AssetCollection:
    """Collection of all graphical assets needed for card generation."""
    
    front_background: Path
    back_background: Path
    front_frame: Path
    spell_banner: Path
    class_banners: dict[str, Path]
    font_path: Path
    
    def validate(self) -> List[str]:
        """Validate that all asset files exist. Returns list of missing files."""
        missing = []
        
        # Check single assets
        for attr in ['front_background', 'back_background', 'front_frame', 
                     'spell_banner', 'font_path']:
            path = getattr(self, attr)
            if not path.exists():
                missing.append(str(path))
        
        # Check class banners
        for class_name, path in self.class_banners.items():
            if not path.exists():
                missing.append(f"{class_name}: {path}")
        
        return missing
