"""Tests for command-line interface."""

import pytest
from pathlib import Path
from src.cli import SpellCardCLI


class TestCLI:
    """Tests for SpellCardCLI class."""
    
    def test_parser_creation(self):
        """Test that parser is created successfully."""
        cli = SpellCardCLI()
        assert cli.parser is not None
        assert cli.parser.prog == 'spell-cards'
    
    def test_parse_minimal_args(self):
        """Test parsing minimal required arguments."""
        cli = SpellCardCLI()
        args = cli.parse_args(['--csv', 'test.csv'])
        
        assert args.csv == Path('test.csv')
        assert args.assets == Path('../assets')
        assert args.output == Path('output')
        assert args.pdf_mode == 'cut-ready'  # Updated default
        assert args.grid == '2x4'  # Updated default
        assert args.orientation == 'landscape'  # Updated default
        assert args.no_pdf is False
    
    def test_parse_all_args(self):
        """Test parsing all arguments."""
        cli = SpellCardCLI()
        args = cli.parse_args([
            '--csv', 'spells.csv',
            '--assets', 'my_assets',
            '--output', 'my_output',
            '--pdf-mode', 'cut-ready',
            '--grid', '2x3',
            '--orientation', 'landscape',
            '--margin', '10',
            '--gap', '5',
            '--pdf-name', 'custom.pdf',
            '--verbose'
        ])
        
        assert args.csv == Path('spells.csv')
        assert args.assets == Path('my_assets')
        assert args.output == Path('my_output')
        assert args.pdf_mode == 'cut-ready'
        assert args.grid == '2x3'
        assert args.orientation == 'landscape'
        assert args.margin == 10
        assert args.gap == 5
        assert args.pdf_name == 'custom.pdf'
        assert args.verbose is True
    
    def test_parse_no_pdf(self):
        """Test --no-pdf flag."""
        cli = SpellCardCLI()
        args = cli.parse_args(['--csv', 'test.csv', '--no-pdf'])
        
        assert args.no_pdf is True
    
    def test_parse_quiet(self):
        """Test --quiet flag."""
        cli = SpellCardCLI()
        args = cli.parse_args(['--csv', 'test.csv', '--quiet'])
        
        assert args.quiet is True
    
    def test_parse_grid_formats(self):
        """Test various grid format specifications."""
        cli = SpellCardCLI()
        
        # Default (updated to 2x4)
        args = cli.parse_args(['--csv', 'test.csv'])
        assert args.grid == '2x4'
        
        # Custom
        args = cli.parse_args(['--csv', 'test.csv', '--grid', '3x3'])
        assert args.grid == '3x3'
    
    def test_parse_pdf_modes(self):
        """Test all PDF mode options."""
        cli = SpellCardCLI()
        
        for mode in ['grid', 'single-card', 'cut-ready']:
            args = cli.parse_args(['--csv', 'test.csv', '--pdf-mode', mode])
            assert args.pdf_mode == mode
    
    def test_parse_orientations(self):
        """Test orientation options."""
        cli = SpellCardCLI()
        
        for orient in ['portrait', 'landscape']:
            args = cli.parse_args(['--csv', 'test.csv', '--orientation', orient])
            assert args.orientation == orient
    
    def test_missing_required_arg(self):
        """Test that missing --csv raises error."""
        cli = SpellCardCLI()
        
        with pytest.raises(SystemExit):
            cli.parse_args([])
    
    def test_invalid_pdf_mode(self):
        """Test that invalid PDF mode raises error."""
        cli = SpellCardCLI()
        
        with pytest.raises(SystemExit):
            cli.parse_args(['--csv', 'test.csv', '--pdf-mode', 'invalid'])
    
    def test_invalid_orientation(self):
        """Test that invalid orientation raises error."""
        cli = SpellCardCLI()
        
        with pytest.raises(SystemExit):
            cli.parse_args(['--csv', 'test.csv', '--orientation', 'invalid'])


class TestGridParsing:
    """Tests for grid string parsing."""
    
    def test_parse_valid_grids(self):
        """Test parsing valid grid specifications."""
        assert SpellCardCLI._parse_grid('3x3') == (3, 3)
        assert SpellCardCLI._parse_grid('2x4') == (2, 4)
        assert SpellCardCLI._parse_grid('4x2') == (4, 2)
        assert SpellCardCLI._parse_grid('1x1') == (1, 1)
        assert SpellCardCLI._parse_grid('5x5') == (5, 5)
    
    def test_parse_case_insensitive(self):
        """Test that grid parsing is case-insensitive."""
        assert SpellCardCLI._parse_grid('3X3') == (3, 3)
        assert SpellCardCLI._parse_grid('2X4') == (2, 4)
    
    def test_parse_invalid_format(self):
        """Test that invalid grid format raises error."""
        with pytest.raises(ValueError, match="Grid must be in format"):
            SpellCardCLI._parse_grid('3-3')
        
        with pytest.raises(ValueError):
            SpellCardCLI._parse_grid('3')
        
        with pytest.raises(ValueError):
            SpellCardCLI._parse_grid('abc')
    
    def test_parse_invalid_values(self):
        """Test that invalid grid values raise error."""
        with pytest.raises(ValueError, match="at least 1"):
            SpellCardCLI._parse_grid('0x3')
        
        with pytest.raises(ValueError, match="at least 1"):
            SpellCardCLI._parse_grid('3x0')
        
        with pytest.raises(ValueError, match="at least 1"):
            SpellCardCLI._parse_grid('-1x3')


class TestCLIExecution:
    """Tests for CLI execution."""
    
    def test_run_with_nonexistent_csv(self, capsys):
        """Test that nonexistent CSV file returns error."""
        cli = SpellCardCLI()
        exit_code = cli.run(['--csv', 'nonexistent.csv'])
        
        assert exit_code == 1
        captured = capsys.readouterr()
        assert 'CSV file not found' in captured.err
    
    def test_run_with_nonexistent_assets(self, capsys):
        """Test that nonexistent assets directory returns error."""
        cli = SpellCardCLI()
        exit_code = cli.run([
            '--csv', 'test_data/test_spells.csv',
            '--assets', 'nonexistent_assets'
        ])
        
        assert exit_code == 1
        captured = capsys.readouterr()
        assert 'Assets directory not found' in captured.err
    
    def test_run_success(self, tmp_path):
        """Test successful execution."""
        cli = SpellCardCLI()
        
        # Use test data
        exit_code = cli.run([
            '--csv', 'test_data/test_spells.csv',
            '--output', str(tmp_path),
            '--pdf-mode', 'grid',
            '--grid', '2x2',
            '--quiet'
        ])
        
        assert exit_code == 0
        
        # Check output files exist
        assert (tmp_path / 'cards_grid.pdf').exists()
        
        # Check card images were cleaned up (default behavior)
        png_files = list(tmp_path.glob('*.png'))
        assert len(png_files) == 0  # Cleaned up by default
    
    def test_run_no_pdf(self, tmp_path):
        """Test execution with --no-pdf flag."""
        cli = SpellCardCLI()
        
        exit_code = cli.run([
            '--csv', 'test_data/test_spells.csv',
            '--output', str(tmp_path),
            '--no-pdf',
            '--quiet'
        ])
        
        assert exit_code == 0
        
        # Check no PDF created
        pdf_files = list(tmp_path.glob('*.pdf'))
        assert len(pdf_files) == 0
        
        # Check card images exist
        png_files = list(tmp_path.glob('*.png'))
        assert len(png_files) == 6
    
    def test_run_custom_pdf_name(self, tmp_path):
        """Test execution with custom PDF name."""
        cli = SpellCardCLI()
        
        exit_code = cli.run([
            '--csv', 'test_data/test_spells.csv',
            '--output', str(tmp_path),
            '--pdf-name', 'my_custom_cards',
            '--quiet'
        ])
        
        assert exit_code == 0
        assert (tmp_path / 'my_custom_cards.pdf').exists()
    
    def test_run_single_card_mode(self, tmp_path):
        """Test execution with single-card mode."""
        cli = SpellCardCLI()
        
        exit_code = cli.run([
            '--csv', 'test_data/test_spells.csv',
            '--output', str(tmp_path),
            '--pdf-mode', 'single-card',
            '--quiet'
        ])
        
        assert exit_code == 0
        assert (tmp_path / 'cards_single_card.pdf').exists()
    
    def test_run_cut_ready_mode(self, tmp_path):
        """Test execution with cut-ready mode."""
        cli = SpellCardCLI()
        
        exit_code = cli.run([
            '--csv', 'test_data/test_spells.csv',
            '--output', str(tmp_path),
            '--pdf-mode', 'cut-ready',
            '--grid', '2x2',
            '--quiet'
        ])
        
        assert exit_code == 0
        assert (tmp_path / 'cards_cut_ready.pdf').exists()
    
    def test_run_with_cleanup(self, tmp_path):
        """Test execution with automatic PNG cleanup (default behavior)."""
        cli = SpellCardCLI()
        
        exit_code = cli.run([
            '--csv', 'test_data/test_spells.csv',
            '--output', str(tmp_path),
            '--pdf-mode', 'grid',
            '--quiet'
        ])
        
        assert exit_code == 0
        
        # Check PDF exists
        assert (tmp_path / 'cards_grid.pdf').exists()
        
        # Check PNG files were cleaned up
        png_files = list(tmp_path.glob('*.png'))
        assert len(png_files) == 0
    
    def test_run_with_keep_images(self, tmp_path):
        """Test execution with --keep-images flag."""
        cli = SpellCardCLI()
        
        exit_code = cli.run([
            '--csv', 'test_data/test_spells.csv',
            '--output', str(tmp_path),
            '--pdf-mode', 'grid',
            '--keep-images',
            '--quiet'
        ])
        
        assert exit_code == 0
        
        # Check PDF exists
        assert (tmp_path / 'cards_grid.pdf').exists()
        
        # Check PNG files were preserved
        png_files = list(tmp_path.glob('*.png'))
        assert len(png_files) == 6  # 3 spells × 2 sides
    
    def test_run_no_pdf_keeps_images(self, tmp_path):
        """Test that --no-pdf preserves PNG files (no cleanup)."""
        cli = SpellCardCLI()
        
        exit_code = cli.run([
            '--csv', 'test_data/test_spells.csv',
            '--output', str(tmp_path),
            '--no-pdf',
            '--quiet'
        ])
        
        assert exit_code == 0
        
        # Check no PDF created
        pdf_files = list(tmp_path.glob('*.pdf'))
        assert len(pdf_files) == 0
        
        # Check PNG files exist (not cleaned up)
        png_files = list(tmp_path.glob('*.png'))
        assert len(png_files) == 6
