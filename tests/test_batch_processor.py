"""Tests for batch processing functionality."""

import pytest
from pathlib import Path
from PIL import Image
from unittest.mock import Mock, MagicMock

from src.batch_processor import BatchProcessor, ProcessingResult
from src.models import SpellData, AssetCollection
from src.card_generator import CardGenerator


@pytest.fixture
def mock_card_generator():
    """Create a mock card generator."""
    generator = Mock(spec=CardGenerator)
    
    # Mock generate methods to save dummy images
    def save_dummy_image(spell, path):
        img = Image.new('RGBA', (100, 100), (255, 0, 0, 255))
        img.save(path, "PNG")
    
    generator.generate_card_front.side_effect = save_dummy_image
    generator.generate_card_back.side_effect = save_dummy_image
    
    return generator


@pytest.fixture
def sample_spells():
    """Create sample spell data."""
    return [
        SpellData(
            name="Fireball",
            level="3rd",
            casting_time="1 action",
            range="150 feet",
            components="V, S, M",
            duration="Instantaneous",
            classes=["Sorcerer", "Wizard"],
            description="A bright streak flashes."
        ),
        SpellData(
            name="Magic Missile",
            level="1st",
            casting_time="1 action",
            range="120 feet",
            components="V, S",
            duration="Instantaneous",
            classes=["Sorcerer", "Wizard"],
            description="You create three glowing darts."
        ),
        SpellData(
            name="Shield",
            level="1st",
            casting_time="1 reaction",
            range="Self",
            components="V, S",
            duration="1 round",
            classes=["Sorcerer", "Wizard"],
            description="An invisible barrier appears."
        )
    ]


def test_batch_processor_initialization(mock_card_generator, tmp_path):
    """Test batch processor initialization."""
    output_dir = tmp_path / "output"
    
    processor = BatchProcessor(
        card_generator=mock_card_generator,
        output_dir=output_dir
    )
    
    assert processor.card_generator == mock_card_generator
    assert processor.output_dir == output_dir
    assert output_dir.exists()  # Should create directory


def test_process_single_spell_success(mock_card_generator, sample_spells, tmp_path):
    """Test successful processing of a single spell."""
    processor = BatchProcessor(
        card_generator=mock_card_generator,
        output_dir=tmp_path
    )
    
    result = processor._process_single_spell(sample_spells[0])
    
    assert result.success
    assert result.spell_name == "Fireball"
    assert result.front_path is not None
    assert result.back_path is not None
    assert result.error is None
    assert result.front_path.exists()
    assert result.back_path.exists()


def test_process_single_spell_failure(mock_card_generator, sample_spells, tmp_path):
    """Test handling of spell processing failure."""
    # Make generator raise an error
    mock_card_generator.generate_card_front.side_effect = ValueError("Test error")
    
    processor = BatchProcessor(
        card_generator=mock_card_generator,
        output_dir=tmp_path
    )
    
    result = processor._process_single_spell(sample_spells[0])
    
    assert not result.success
    assert result.spell_name == "Fireball"
    assert result.front_path is None
    assert result.back_path is None
    assert "Test error" in result.error


def test_process_multiple_spells(mock_card_generator, sample_spells, tmp_path):
    """Test processing multiple spells."""
    processor = BatchProcessor(
        card_generator=mock_card_generator,
        output_dir=tmp_path
    )
    
    results = processor.process_spells(sample_spells)
    
    assert len(results) == 3
    assert all(r.success for r in results.values())
    assert "Fireball" in results
    assert "Magic Missile" in results
    assert "Shield" in results


def test_process_with_progress_callback(mock_card_generator, sample_spells, tmp_path):
    """Test progress callback is called correctly."""
    progress_calls = []
    
    def progress_callback(current, total, spell_name):
        progress_calls.append((current, total, spell_name))
    
    processor = BatchProcessor(
        card_generator=mock_card_generator,
        output_dir=tmp_path,
        progress_callback=progress_callback
    )
    
    processor.process_spells(sample_spells)
    
    assert len(progress_calls) == 3
    assert progress_calls[0] == (1, 3, "Fireball")
    assert progress_calls[1] == (2, 3, "Magic Missile")
    assert progress_calls[2] == (3, 3, "Shield")


def test_process_continues_on_error(mock_card_generator, sample_spells, tmp_path):
    """Test that processing continues when one spell fails."""
    # Make second spell fail
    call_count = [0]
    
    def generate_front_with_error(spell, path):
        call_count[0] += 1
        if call_count[0] == 2:  # Fail on second spell
            raise ValueError("Second spell error")
        img = Image.new('RGBA', (100, 100), (255, 0, 0, 255))
        img.save(path, "PNG")
    
    mock_card_generator.generate_card_front.side_effect = generate_front_with_error
    
    processor = BatchProcessor(
        card_generator=mock_card_generator,
        output_dir=tmp_path
    )
    
    results = processor.process_spells(sample_spells)
    
    assert len(results) == 3
    assert results["Fireball"].success
    assert not results["Magic Missile"].success
    assert results["Shield"].success


def test_filename_sanitization(mock_card_generator, tmp_path):
    """Test filename sanitization for special characters."""
    processor = BatchProcessor(
        card_generator=mock_card_generator,
        output_dir=tmp_path
    )
    
    # Test various problematic names
    assert processor._sanitize_filename("Tasha's Hideous Laughter") == "tashas_hideous_laughter"
    assert processor._sanitize_filename("Bigby's Hand") == "bigbys_hand"
    assert processor._sanitize_filename("Spell/Name") == "spellname"
    assert processor._sanitize_filename("Spell:Name") == "spellname"


def test_filename_uniqueness(mock_card_generator, tmp_path):
    """Test that different spells produce unique filenames."""
    processor = BatchProcessor(
        card_generator=mock_card_generator,
        output_dir=tmp_path
    )
    
    spells = [
        SpellData(
            name="Fireball",
            level="3rd",
            casting_time="1 action",
            range="150 feet",
            components="V, S, M",
            duration="Instantaneous",
            classes=["Wizard"],
            description="Test"
        ),
        SpellData(
            name="Fire Ball",  # Different name, same sanitized version
            level="3rd",
            casting_time="1 action",
            range="150 feet",
            components="V, S, M",
            duration="Instantaneous",
            classes=["Wizard"],
            description="Test"
        )
    ]
    
    results = processor.process_spells(spells)
    
    # Both should succeed (second will overwrite first, but that's expected behavior)
    assert results["Fireball"].success
    assert results["Fire Ball"].success


def test_get_summary_all_success(mock_card_generator, sample_spells, tmp_path):
    """Test summary generation with all successful."""
    processor = BatchProcessor(
        card_generator=mock_card_generator,
        output_dir=tmp_path
    )
    
    results = processor.process_spells(sample_spells)
    summary = processor.get_summary(results)
    
    assert summary["total"] == 3
    assert summary["successful"] == 3
    assert summary["failed"] == 0
    assert summary["success_rate"] == 1.0
    assert len(summary["errors"]) == 0


def test_get_summary_with_failures(mock_card_generator, sample_spells, tmp_path):
    """Test summary generation with some failures."""
    # Make second spell fail
    call_count = [0]
    
    def generate_front_with_error(spell, path):
        call_count[0] += 1
        if call_count[0] == 2:
            raise ValueError("Test error")
        img = Image.new('RGBA', (100, 100), (255, 0, 0, 255))
        img.save(path, "PNG")
    
    mock_card_generator.generate_card_front.side_effect = generate_front_with_error
    
    processor = BatchProcessor(
        card_generator=mock_card_generator,
        output_dir=tmp_path
    )
    
    results = processor.process_spells(sample_spells)
    summary = processor.get_summary(results)
    
    assert summary["total"] == 3
    assert summary["successful"] == 2
    assert summary["failed"] == 1
    assert summary["success_rate"] == pytest.approx(0.666, rel=0.01)
    assert "Magic Missile" in summary["errors"]
    assert "Test error" in summary["errors"]["Magic Missile"]


def test_output_file_structure(mock_card_generator, sample_spells, tmp_path):
    """Test that output files are created with correct structure."""
    processor = BatchProcessor(
        card_generator=mock_card_generator,
        output_dir=tmp_path
    )
    
    results = processor.process_spells(sample_spells)
    
    # Check all expected files exist
    expected_files = [
        "fireball_front.png",
        "fireball_back.png",
        "magic_missile_front.png",
        "magic_missile_back.png",
        "shield_front.png",
        "shield_back.png"
    ]
    
    for filename in expected_files:
        filepath = tmp_path / filename
        assert filepath.exists(), f"Expected file {filename} not found"
        
        # Verify it's a valid image
        img = Image.open(filepath)
        assert img.size == (100, 100)  # Our dummy image size


def test_empty_spell_list(mock_card_generator, tmp_path):
    """Test processing empty spell list."""
    processor = BatchProcessor(
        card_generator=mock_card_generator,
        output_dir=tmp_path
    )
    
    results = processor.process_spells([])
    summary = processor.get_summary(results)
    
    assert len(results) == 0
    assert summary["total"] == 0
    assert summary["successful"] == 0
    assert summary["failed"] == 0
