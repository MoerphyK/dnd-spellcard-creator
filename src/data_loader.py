"""Data loading and validation for spell card generator."""

import csv
from pathlib import Path
from typing import List, Optional
from .models import SpellData, AssetCollection


# Known D&D 5e classes
VALID_CLASSES = {
    "Artificer", "Barbarian", "Bard", "Cleric", "Druid", "Fighter",
    "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"
}


class DataLoadError(Exception):
    """Raised when data loading fails."""
    pass


def load_spell_data(csv_path: Path, illustration_dir: Optional[Path] = None) -> List[SpellData]:
    """
    Load spell data from CSV file.
    
    Args:
        csv_path: Path to CSV file with spell data
        illustration_dir: Optional directory containing illustration images
        
    Returns:
        List of SpellData objects
        
    Raises:
        DataLoadError: If CSV is invalid or required fields are missing
    """
    if not csv_path.exists():
        raise DataLoadError(f"CSV file not found: {csv_path}")
    
    spells = []
    required_fields = {
        "Name", "Level", "Casting Time", "Duration", "Range", 
        "Components", "Classes", "Text"
    }
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Validate headers
            if not reader.fieldnames:
                raise DataLoadError("CSV file is empty or has no headers")
            
            missing_fields = required_fields - set(reader.fieldnames)
            if missing_fields:
                raise DataLoadError(
                    f"Missing required CSV columns: {', '.join(missing_fields)}"
                )
            
            # Parse each spell
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                try:
                    # Parse classes
                    classes_str = row["Classes"].strip()
                    if not classes_str:
                        raise ValueError("Classes field is empty")
                    
                    classes = [c.strip() for c in classes_str.split(",")]
                    
                    # Validate class names
                    invalid_classes = [c for c in classes if c not in VALID_CLASSES]
                    if invalid_classes:
                        print(f"Warning: Row {row_num} - Unknown classes: {', '.join(invalid_classes)}")
                    
                    # Find illustration if directory provided
                    illustration_path = None
                    if illustration_dir:
                        illustration_path = find_illustration(row["Name"], illustration_dir)
                    
                    # Create spell data
                    spell = SpellData(
                        name=row["Name"].strip(),
                        level=row["Level"].strip(),
                        casting_time=row["Casting Time"].strip(),
                        duration=row["Duration"].strip(),
                        range=row["Range"].strip(),
                        components=row["Components"].strip(),
                        classes=classes,
                        description=row["Text"].strip(),
                        at_higher_levels=row.get("At Higher Levels", "").strip() or None,
                        illustration_path=illustration_path
                    )
                    
                    spells.append(spell)
                    
                except Exception as e:
                    raise DataLoadError(f"Error parsing row {row_num}: {e}")
    
    except csv.Error as e:
        raise DataLoadError(f"CSV parsing error: {e}")
    except UnicodeDecodeError as e:
        raise DataLoadError(f"File encoding error: {e}")
    
    if not spells:
        raise DataLoadError("No valid spells found in CSV")
    
    return spells


def find_illustration(spell_name: str, illustration_dir: Path) -> Optional[Path]:
    """
    Find illustration file for a spell.
    
    Looks for files matching the spell name (lowercase, spaces replaced with underscores)
    with common image extensions.
    
    Args:
        spell_name: Name of the spell
        illustration_dir: Directory to search for illustrations
        
    Returns:
        Path to illustration file if found, None otherwise
    """
    if not illustration_dir.exists():
        return None
    
    # Convert spell name to filename format
    filename_base = spell_name.lower().replace(" ", "_")
    
    # Try common image extensions
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        illustration_path = illustration_dir / f"{filename_base}{ext}"
        if illustration_path.exists():
            return illustration_path
    
    return None


def load_assets(asset_dir: Path) -> AssetCollection:
    """
    Load all graphical assets from asset directory.
    
    Args:
        asset_dir: Directory containing asset files
        
    Returns:
        AssetCollection with paths to all assets
        
    Raises:
        DataLoadError: If asset directory structure is invalid
    """
    if not asset_dir.exists():
        raise DataLoadError(f"Asset directory not found: {asset_dir}")
    
    # Load class banners
    class_banners = {}
    banner_dir = asset_dir / "class_banners"
    
    if banner_dir.exists():
        for class_name in VALID_CLASSES:
            banner_path = banner_dir / f"{class_name.lower()}.png"
            class_banners[class_name] = banner_path
    
    # Find font file
    font_dir = asset_dir / "fonts"
    font_path = None
    if font_dir.exists():
        # Look for any .ttf file
        ttf_files = list(font_dir.glob("*.ttf")) + list(font_dir.glob("*.TTF"))
        if ttf_files:
            font_path = ttf_files[0]
    
    if not font_path:
        # Default fallback
        font_path = font_dir / "font.ttf" if font_dir.exists() else asset_dir / "font.ttf"
    
    assets = AssetCollection(
        front_background=asset_dir / "front_background.png",
        back_background=asset_dir / "back_background.png",
        front_frame=asset_dir / "front_frame.png",
        spell_banner=asset_dir / "spellname_banner.png",
        class_banners=class_banners,
        font_path=font_path
    )
    
    return assets
