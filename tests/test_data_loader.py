"""Unit tests for data loading functionality."""

import pytest
import csv
from pathlib import Path
from src.data_loader import load_spell_data, load_assets, find_illustration, DataLoadError
from src.models import SpellData


def test_load_spell_data_valid(tmp_path):
    """Test loading valid spell data from CSV."""
    csv_file = tmp_path / "spells.csv"
    csv_file.write_text(
        'Name,Level,Casting Time,Duration,Range,Components,Classes,Text,At Higher Levels\n'
        'Fireball,3rd,Action,Instantaneous,150 feet,"V, S, M (a tiny ball of bat guano)","Sorcerer, Wizard",A bright streak...,When you cast this spell...\n'
        'Light,Cantrip,Action,1 hour,Touch,"V, M (a firefly)","Bard, Cleric",You touch one object...,\n'
    )
    
    spells = load_spell_data(csv_file)
    
    assert len(spells) == 2
    assert spells[0].name == "Fireball"
    assert spells[0].level == "3rd"
    assert spells[0].classes == ["Sorcerer", "Wizard"]
    assert spells[0].at_higher_levels == "When you cast this spell..."
    assert spells[1].name == "Light"
    assert spells[1].at_higher_levels is None


def test_load_spell_data_missing_file():
    """Test error when CSV file doesn't exist."""
    with pytest.raises(DataLoadError, match="CSV file not found"):
        load_spell_data(Path("nonexistent.csv"))


def test_load_spell_data_missing_columns(tmp_path):
    """Test error when required columns are missing."""
    csv_file = tmp_path / "spells.csv"
    csv_file.write_text('Name,Level\nFireball,3rd\n')
    
    with pytest.raises(DataLoadError, match="Missing required CSV columns"):
        load_spell_data(csv_file)


def test_load_spell_data_empty_file(tmp_path):
    """Test error when CSV file is empty."""
    csv_file = tmp_path / "spells.csv"
    csv_file.write_text('')
    
    with pytest.raises(DataLoadError, match="empty or has no headers"):
        load_spell_data(csv_file)


def test_spell_data_components_short():
    """Test component simplification."""
    spell = SpellData(
        name="Test",
        level="1st",
        casting_time="Action",
        duration="1 hour",
        range="Touch",
        components="V, S, M (a drop of honey)",
        classes=["Bard"],
        description="Test spell"
    )
    
    assert spell.components_short == "V, S, M"
    
    spell2 = SpellData(
        name="Test2",
        level="1st",
        casting_time="Action",
        duration="1 hour",
        range="Touch",
        components="V, S",
        classes=["Bard"],
        description="Test spell"
    )
    
    assert spell2.components_short == "V, S"


def test_spell_data_level_numeric():
    """Test level numeric conversion."""
    cantrip = SpellData(
        name="Light",
        level="Cantrip",
        casting_time="Action",
        duration="1 hour",
        range="Touch",
        components="V",
        classes=["Bard"],
        description="Test"
    )
    assert cantrip.level_numeric == "0"
    
    first = SpellData(
        name="Cure Wounds",
        level="1st",
        casting_time="Action",
        duration="Instantaneous",
        range="Touch",
        components="V, S",
        classes=["Cleric"],
        description="Test"
    )
    assert first.level_numeric == "1"
    
    third = SpellData(
        name="Fireball",
        level="3rd",
        casting_time="Action",
        duration="Instantaneous",
        range="150 feet",
        components="V, S, M",
        classes=["Wizard"],
        description="Test"
    )
    assert third.level_numeric == "3"


def test_find_illustration_found(tmp_path):
    """Test finding illustration file."""
    illus_dir = tmp_path / "illustrations"
    illus_dir.mkdir()
    
    # Create test illustration
    illus_file = illus_dir / "fireball.jpg"
    illus_file.write_text("fake image")
    
    result = find_illustration("Fireball", illus_dir)
    assert result == illus_file


def test_find_illustration_not_found(tmp_path):
    """Test when illustration doesn't exist."""
    illus_dir = tmp_path / "illustrations"
    illus_dir.mkdir()
    
    result = find_illustration("Nonexistent Spell", illus_dir)
    assert result is None


def test_find_illustration_dir_not_exists(tmp_path):
    """Test when illustration directory doesn't exist."""
    result = find_illustration("Fireball", tmp_path / "nonexistent")
    assert result is None


def test_load_assets_structure(tmp_path):
    """Test loading asset collection."""
    asset_dir = tmp_path / "assets"
    asset_dir.mkdir()
    
    # Create minimal asset structure
    (asset_dir / "front_background.png").write_text("fake")
    (asset_dir / "back_background.png").write_text("fake")
    (asset_dir / "front_frame.png").write_text("fake")
    (asset_dir / "spellname_banner.png").write_text("fake")
    
    font_dir = asset_dir / "fonts"
    font_dir.mkdir()
    (font_dir / "test.ttf").write_text("fake")
    
    banner_dir = asset_dir / "class_banners"
    banner_dir.mkdir()
    (banner_dir / "wizard.png").write_text("fake")
    
    assets = load_assets(asset_dir)
    
    assert assets.front_background == asset_dir / "front_background.png"
    assert assets.font_path == font_dir / "test.ttf"
    assert "Wizard" in assets.class_banners


def test_load_assets_missing_dir():
    """Test error when asset directory doesn't exist."""
    with pytest.raises(DataLoadError, match="Asset directory not found"):
        load_assets(Path("nonexistent"))


def test_asset_validation(tmp_path):
    """Test asset validation."""
    asset_dir = tmp_path / "assets"
    asset_dir.mkdir()
    
    # Create only some assets
    (asset_dir / "front_background.png").write_text("fake")
    
    assets = load_assets(asset_dir)
    missing = assets.validate()
    
    # Should report missing files
    assert len(missing) > 0
    assert any("back_background" in m for m in missing)
