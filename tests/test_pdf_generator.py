"""Tests for PDF generation with multiple layout modes."""

import pytest
from pathlib import Path
from PIL import Image
from src.pdf_generator import (
    PDFGenerator,
    GridConfig,
    SingleCardPDFGenerator,
    CutReadyPDFGenerator
)


class TestGridConfig:
    """Tests for GridConfig dataclass."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = GridConfig()
        assert config.rows == 3
        assert config.cols == 3
        assert config.orientation == "portrait"
        assert config.margin == 20
        assert config.gap_x == 10
        assert config.gap_y == 10
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = GridConfig(rows=2, cols=4, orientation="landscape")
        assert config.rows == 2
        assert config.cols == 4
        assert config.orientation == "landscape"
    
    def test_invalid_rows(self):
        """Test validation of rows parameter."""
        with pytest.raises(ValueError, match="Rows and cols must be at least 1"):
            GridConfig(rows=0)
    
    def test_invalid_cols(self):
        """Test validation of cols parameter."""
        with pytest.raises(ValueError, match="Rows and cols must be at least 1"):
            GridConfig(cols=-1)
    
    def test_invalid_orientation(self):
        """Test validation of orientation parameter."""
        with pytest.raises(ValueError, match="Orientation must be"):
            GridConfig(orientation="vertical")


class TestPDFGenerator:
    """Tests for PDFGenerator class."""
    
    def test_initialization(self):
        """Test PDF generator initialization."""
        config = GridConfig(rows=3, cols=3)
        generator = PDFGenerator(config)
        
        assert generator.config == config
        assert generator.page_width > 0
        assert generator.page_height > 0
        assert generator.card_width > 0
        assert generator.card_height > 0
        assert len(generator.positions) == 9  # 3x3 grid
        assert len(generator.back_order) == 9
    
    def test_page_size_portrait(self):
        """Test page size calculation for portrait orientation."""
        config = GridConfig(orientation="portrait")
        generator = PDFGenerator(config)
        
        # A4 portrait: width < height
        assert generator.page_width < generator.page_height
        assert generator.page_width == pytest.approx(595.27, rel=0.01)  # A4 width
        assert generator.page_height == pytest.approx(841.89, rel=0.01)  # A4 height
    
    def test_page_size_landscape(self):
        """Test page size calculation for landscape orientation."""
        config = GridConfig(orientation="landscape")
        generator = PDFGenerator(config)
        
        # A4 landscape: width > height
        assert generator.page_width > generator.page_height
        assert generator.page_width == pytest.approx(841.89, rel=0.01)
        assert generator.page_height == pytest.approx(595.27, rel=0.01)
    
    def test_card_dimensions_3x3(self):
        """Test card dimension calculation for 3x3 grid."""
        config = GridConfig(rows=3, cols=3)
        generator = PDFGenerator(config)
        
        # Cards should fit within page
        total_width = (3 * generator.card_width + 2 * config.gap_x + 2 * config.margin)
        total_height = (3 * generator.card_height + 2 * config.gap_y + 2 * config.margin)
        
        assert total_width <= generator.page_width
        assert total_height <= generator.page_height
        
        # Aspect ratio should be maintained
        aspect = generator.card_width / generator.card_height
        expected_aspect = PDFGenerator.CARD_ASPECT_RATIO
        assert aspect == pytest.approx(expected_aspect, rel=0.01)
    
    def test_card_dimensions_2x4(self):
        """Test card dimension calculation for 2x4 grid."""
        config = GridConfig(rows=2, cols=4)
        generator = PDFGenerator(config)
        
        # Cards should fit within page
        total_width = (4 * generator.card_width + 3 * config.gap_x + 2 * config.margin)
        total_height = (2 * generator.card_height + 1 * config.gap_y + 2 * config.margin)
        
        assert total_width <= generator.page_width
        assert total_height <= generator.page_height
    
    def test_positions_count(self):
        """Test that correct number of positions are calculated."""
        config = GridConfig(rows=2, cols=3)
        generator = PDFGenerator(config)
        
        assert len(generator.positions) == 6  # 2x3 = 6
    
    def test_positions_ordering(self):
        """Test that positions are ordered correctly (bottom-left, row by row)."""
        config = GridConfig(rows=2, cols=2, margin=0, gap_x=0, gap_y=0)
        generator = PDFGenerator(config)
        
        # With no margins/gaps, positions should be in a simple grid
        # Bottom-left, bottom-right, top-left, top-right
        assert len(generator.positions) == 4
        
        # First row (bottom) should have lower y than second row (top)
        assert generator.positions[0][1] < generator.positions[2][1]
        assert generator.positions[1][1] < generator.positions[3][1]
        
        # Left cards should have lower x than right cards
        assert generator.positions[0][0] < generator.positions[1][0]
        assert generator.positions[2][0] < generator.positions[3][0]
    
    def test_back_order_3x3(self):
        """Test back order calculation for 3x3 grid."""
        config = GridConfig(rows=3, cols=3)
        generator = PDFGenerator(config)
        
        # Expected: each row reversed
        # Row 0: [0,1,2] -> [2,1,0]
        # Row 1: [3,4,5] -> [5,4,3]
        # Row 2: [6,7,8] -> [8,7,6]
        expected = [2, 1, 0, 5, 4, 3, 8, 7, 6]
        assert generator.back_order == expected
    
    def test_back_order_2x4(self):
        """Test back order calculation for 2x4 grid."""
        config = GridConfig(rows=2, cols=4)
        generator = PDFGenerator(config)
        
        # Expected: each row reversed
        # Row 0: [0,1,2,3] -> [3,2,1,0]
        # Row 1: [4,5,6,7] -> [7,6,5,4]
        expected = [3, 2, 1, 0, 7, 6, 5, 4]
        assert generator.back_order == expected
    
    def test_generate_pdf_creates_file(self, tmp_path):
        """Test that PDF file is created."""
        config = GridConfig(rows=2, cols=2)
        generator = PDFGenerator(config)
        
        # Create dummy card images
        image_dir = tmp_path / "images"
        image_dir.mkdir()
        
        for i in range(3):
            for side in ["front", "back"]:
                img = Image.new("RGB", (210, 298), color="white")
                img.save(image_dir / f"card{i}_{side}.png")
        
        # Generate PDF
        output_path = tmp_path / "output.pdf"
        card_names = ["card0", "card1", "card2"]
        
        result = generator.generate_pdf(card_names, output_path, image_dir)
        
        assert output_path.exists()
        assert result["total_cards"] == 3
        assert result["total_pages"] == 2  # 1 group = 2 pages (front + back)
        assert len(result["missing_files"]) == 0
    
    def test_generate_pdf_multiple_pages(self, tmp_path):
        """Test PDF generation with multiple pages."""
        config = GridConfig(rows=2, cols=2)  # 4 cards per page
        generator = PDFGenerator(config)
        
        # Create dummy card images for 6 cards (needs 2 pages)
        image_dir = tmp_path / "images"
        image_dir.mkdir()
        
        for i in range(6):
            for side in ["front", "back"]:
                img = Image.new("RGB", (210, 298), color="white")
                img.save(image_dir / f"card{i}_{side}.png")
        
        # Generate PDF
        output_path = tmp_path / "output.pdf"
        card_names = [f"card{i}" for i in range(6)]
        
        result = generator.generate_pdf(card_names, output_path, image_dir)
        
        assert output_path.exists()
        assert result["total_cards"] == 6
        assert result["total_pages"] == 4  # 2 groups × 2 pages each
    
    def test_generate_pdf_missing_images(self, tmp_path):
        """Test PDF generation with missing images."""
        config = GridConfig(rows=2, cols=2)
        generator = PDFGenerator(config)
        
        # Create only some images
        image_dir = tmp_path / "images"
        image_dir.mkdir()
        
        img = Image.new("RGB", (210, 298), color="white")
        img.save(image_dir / "card0_front.png")
        img.save(image_dir / "card0_back.png")
        # card1 images missing
        
        # Generate PDF
        output_path = tmp_path / "output.pdf"
        card_names = ["card0", "card1"]
        
        result = generator.generate_pdf(card_names, output_path, image_dir)
        
        assert output_path.exists()
        assert result["total_cards"] == 2
        assert len(result["missing_files"]) == 2  # card1_front and card1_back
    
    def test_generate_pdf_creates_output_dir(self, tmp_path):
        """Test that output directory is created if it doesn't exist."""
        config = GridConfig(rows=2, cols=2)
        generator = PDFGenerator(config)
        
        # Create dummy card images
        image_dir = tmp_path / "images"
        image_dir.mkdir()
        
        img = Image.new("RGB", (210, 298), color="white")
        img.save(image_dir / "card0_front.png")
        img.save(image_dir / "card0_back.png")
        
        # Output to non-existent directory
        output_path = tmp_path / "output" / "subdir" / "test.pdf"
        card_names = ["card0"]
        
        result = generator.generate_pdf(card_names, output_path, image_dir)
        
        assert output_path.exists()
        assert output_path.parent.exists()



class TestSingleCardPDFGenerator:
    """Tests for SingleCardPDFGenerator class."""
    
    def test_initialization(self):
        """Test single-card PDF generator initialization."""
        generator = SingleCardPDFGenerator()
        
        assert generator.A7_WIDTH == 210
        assert generator.A7_HEIGHT == 298
        assert generator.page_size == (210, 298)
    
    def test_generate_pdf_creates_file(self, tmp_path):
        """Test that PDF file is created with A7 pages."""
        generator = SingleCardPDFGenerator()
        
        # Create dummy card images
        image_dir = tmp_path / "images"
        image_dir.mkdir()
        
        for i in range(2):
            for side in ["front", "back"]:
                img = Image.new("RGB", (210, 298), color="white")
                img.save(image_dir / f"card{i}_{side}.png")
        
        # Generate PDF
        output_path = tmp_path / "output.pdf"
        card_names = ["card0", "card1"]
        
        result = generator.generate_pdf(card_names, output_path, image_dir)
        
        assert output_path.exists()
        assert result["total_cards"] == 2
        assert result["total_pages"] == 4  # 2 cards × 2 pages each
        assert len(result["missing_files"]) == 0
    
    def test_generate_pdf_alternates_front_back(self, tmp_path):
        """Test that pages alternate between front and back."""
        generator = SingleCardPDFGenerator()
        
        # Create dummy card images
        image_dir = tmp_path / "images"
        image_dir.mkdir()
        
        img = Image.new("RGB", (210, 298), color="white")
        img.save(image_dir / "card0_front.png")
        img.save(image_dir / "card0_back.png")
        
        # Generate PDF
        output_path = tmp_path / "output.pdf"
        result = generator.generate_pdf(["card0"], output_path, image_dir)
        
        assert result["total_pages"] == 2  # Front, then back
    
    def test_generate_pdf_missing_images(self, tmp_path):
        """Test handling of missing images."""
        generator = SingleCardPDFGenerator()
        
        # Create only front image
        image_dir = tmp_path / "images"
        image_dir.mkdir()
        
        img = Image.new("RGB", (210, 298), color="white")
        img.save(image_dir / "card0_front.png")
        # card0_back.png missing
        
        # Generate PDF
        output_path = tmp_path / "output.pdf"
        result = generator.generate_pdf(["card0"], output_path, image_dir)
        
        assert output_path.exists()
        assert len(result["missing_files"]) == 1


class TestCutReadyPDFGenerator:
    """Tests for CutReadyPDFGenerator class."""
    
    def test_initialization(self):
        """Test cut-ready PDF generator initialization."""
        # Use 2×2 grid with smaller margins for cut-ready mode
        config = GridConfig(rows=2, cols=2, margin=5, gap_x=5, gap_y=5)
        generator = CutReadyPDFGenerator(config)
        
        assert generator.config == config
        assert generator.card_width > 0
        assert generator.card_height > 0
        assert generator.bleed > 0
        assert len(generator.positions) == 4
        assert len(generator.back_order) == 4
    
    def test_fixed_card_dimensions(self):
        """Test that card dimensions are fixed (not scaled)."""
        config = GridConfig(rows=2, cols=2, margin=5, gap_x=5, gap_y=5)
        generator = CutReadyPDFGenerator(config)
        
        # Card dimensions should match standard poker card size
        expected_width = 63.5 * 2.834645669  # mm to points
        expected_height = 88.5 * 2.834645669
        
        assert generator.card_width == pytest.approx(expected_width, rel=0.01)
        assert generator.card_height == pytest.approx(expected_height, rel=0.01)
    
    def test_grid_too_large_raises_error(self):
        """Test that oversized grid raises validation error."""
        # 10×10 grid won't fit on A4 with fixed card dimensions
        config = GridConfig(rows=10, cols=10)
        
        with pytest.raises(ValueError, match="doesn't fit on"):
            CutReadyPDFGenerator(config)
    
    def test_back_order_calculation(self):
        """Test back order calculation for cut-ready mode."""
        config = GridConfig(rows=2, cols=3, margin=5, gap_x=5, gap_y=5, orientation="landscape")
        generator = CutReadyPDFGenerator(config)
        
        # Expected: each row reversed
        # Row 0: [0,1,2] -> [2,1,0]
        # Row 1: [3,4,5] -> [5,4,3]
        expected = [2, 1, 0, 5, 4, 3]
        assert generator.back_order == expected
    
    def test_generate_pdf_creates_file(self, tmp_path):
        """Test that cut-ready PDF file is created."""
        config = GridConfig(rows=2, cols=2, margin=5, gap_x=5, gap_y=5)
        generator = CutReadyPDFGenerator(config)
        
        # Create dummy card images
        image_dir = tmp_path / "images"
        image_dir.mkdir()
        
        for i in range(3):
            for side in ["front", "back"]:
                img = Image.new("RGB", (210, 298), color="white")
                img.save(image_dir / f"card{i}_{side}.png")
        
        # Generate PDF
        output_path = tmp_path / "output.pdf"
        card_names = ["card0", "card1", "card2"]
        
        result = generator.generate_pdf(card_names, output_path, image_dir)
        
        assert output_path.exists()
        assert result["total_cards"] == 3
        assert result["total_pages"] == 2  # 1 group = 2 pages
        assert len(result["missing_files"]) == 0
    
    def test_portrait_vs_landscape(self):
        """Test that portrait and landscape orientations work."""
        # Portrait should fit 2×2
        config_portrait = GridConfig(rows=2, cols=2, orientation="portrait", margin=5, gap_x=5, gap_y=5)
        gen_portrait = CutReadyPDFGenerator(config_portrait)
        assert gen_portrait.page_width < gen_portrait.page_height
        
        # Landscape should fit more columns
        config_landscape = GridConfig(rows=2, cols=3, orientation="landscape", margin=5, gap_x=5, gap_y=5)
        gen_landscape = CutReadyPDFGenerator(config_landscape)
        assert gen_landscape.page_width > gen_landscape.page_height
    
    def test_bleed_dimensions(self):
        """Test that bleed is correctly calculated."""
        config = GridConfig(rows=2, cols=2, margin=5, gap_x=5, gap_y=5)
        generator = CutReadyPDFGenerator(config)
        
        # Bleed should be 1.5mm in points
        expected_bleed = 1.5 * 2.834645669
        assert generator.bleed == pytest.approx(expected_bleed, rel=0.01)
