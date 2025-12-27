"""Command-line interface for D&D Spell Card Generator V2.

This module provides a user-friendly CLI for generating spell cards and PDFs
from CSV data.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .data_loader import load_spell_data, load_assets
from .card_generator import CardGenerator
from .batch_processor import BatchProcessor
from .pdf_generator import (
    PDFGenerator,
    SingleCardPDFGenerator,
    CutReadyPDFGenerator,
    GridConfig
)


class SpellCardCLI:
    """Command-line interface for spell card generation."""
    
    def __init__(self):
        """Initialize CLI with argument parser."""
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure argument parser with comprehensive help.
        
        Returns:
            Configured ArgumentParser instance
        """
        parser = argparse.ArgumentParser(
            prog='spell-cards',
            description='''
D&D Spell Card Generator V2
============================

Generate professional-quality spell cards and PDFs from CSV data.
Supports three PDF modes: grid layout, single-card A7, and cut-ready.
            ''',
            epilog='''
Examples:
  # Generate cut-ready PDF with optimal settings (default: 2×4 landscape)
  %(prog)s --csv spells.csv
  
  # Generate grid PDF with custom layout
  %(prog)s --csv spells.csv --pdf-mode grid --grid 3x3 --orientation portrait
  
  # Generate single-card A7 pages (no cutting needed)
  %(prog)s --csv my_spells.csv --pdf-mode single-card
  
  # Generate cards only (no PDF)
  %(prog)s --csv spells.csv --no-pdf
  
For more information, visit: https://github.com/yourusername/dnd-spell-cards
            ''',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        # Required arguments
        required = parser.add_argument_group('required arguments')
        required.add_argument(
            '--csv',
            type=Path,
            required=True,
            metavar='FILE',
            help='Path to CSV file containing spell data (required)'
        )
        
        # Input/Output arguments
        io_group = parser.add_argument_group('input/output options')
        io_group.add_argument(
            '--assets',
            type=Path,
            default=Path('../assets'),
            metavar='DIR',
            help='Path to assets directory (default: ../assets)'
        )
        io_group.add_argument(
            '--output',
            type=Path,
            default=Path('output'),
            metavar='DIR',
            help='Output directory for generated files (default: output)'
        )
        
        # PDF generation arguments
        pdf_group = parser.add_argument_group('PDF generation options')
        pdf_group.add_argument(
            '--pdf-mode',
            choices=['grid', 'single-card', 'cut-ready'],
            default='cut-ready',
            metavar='MODE',
            help='''PDF generation mode (default: cut-ready)
  grid        - Multiple cards per page, scales to fit
  single-card - One card per A7 page, alternating front/back
  cut-ready   - Fixed dimensions with cut guidelines and bleed'''
        )
        pdf_group.add_argument(
            '--no-pdf',
            action='store_true',
            help='Generate card images only, skip PDF generation'
        )
        pdf_group.add_argument(
            '--pdf-name',
            type=str,
            metavar='NAME',
            help='Custom PDF filename (default: cards_<mode>.pdf)'
        )
        pdf_group.add_argument(
            '--keep-images',
            action='store_true',
            help='Keep PNG card images after PDF generation (default: auto-cleanup)'
        )
        
        # Grid configuration arguments
        grid_group = parser.add_argument_group('grid layout options (for grid and cut-ready modes)')
        grid_group.add_argument(
            '--grid',
            type=str,
            default='2x4',
            metavar='RxC',
            help='''Grid size as ROWSxCOLS (default: 2x4)
  Examples: 2x2, 3x3, 2x4, 4x2
  Note: cut-ready mode has size limits due to fixed card dimensions'''
        )
        grid_group.add_argument(
            '--orientation',
            choices=['portrait', 'landscape'],
            default='landscape',
            metavar='ORIENT',
            help='Page orientation (default: landscape)'
        )
        grid_group.add_argument(
            '--margin',
            type=float,
            metavar='POINTS',
            help='Page margin in points (default: 20 for grid, 5 for cut-ready)'
        )
        grid_group.add_argument(
            '--gap',
            type=float,
            metavar='POINTS',
            help='Gap between cards in points (default: 10 for grid, 5 for cut-ready)'
        )
        
        # Display options
        display_group = parser.add_argument_group('display options')
        display_group.add_argument(
            '--verbose',
            '-v',
            action='store_true',
            help='Show detailed progress information'
        )
        display_group.add_argument(
            '--quiet',
            '-q',
            action='store_true',
            help='Suppress all output except errors'
        )
        
        # Version
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s 2.0.0'
        )
        
        return parser
    
    def parse_args(self, args=None):
        """Parse command-line arguments.
        
        Args:
            args: List of arguments (default: sys.argv)
            
        Returns:
            Parsed arguments namespace
        """
        return self.parser.parse_args(args)
    
    def run(self, args=None) -> int:
        """Run the CLI application.
        
        Args:
            args: List of arguments (default: sys.argv)
            
        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            parsed_args = self.parse_args(args)
            return self._execute(parsed_args)
        except KeyboardInterrupt:
            if not parsed_args.quiet:
                print("\n\nOperation cancelled by user.")
            return 130
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            if parsed_args.verbose:
                import traceback
                traceback.print_exc()
            return 1
    
    def _execute(self, args) -> int:
        """Execute the main application logic.
        
        Args:
            args: Parsed arguments
            
        Returns:
            Exit code
        """
        # Validate inputs
        if not args.csv.exists():
            print(f"Error: CSV file not found: {args.csv}", file=sys.stderr)
            return 1
        
        if not args.assets.exists():
            print(f"Error: Assets directory not found: {args.assets}", file=sys.stderr)
            return 1
        
        # Print header
        if not args.quiet:
            print("="*80)
            print("D&D Spell Card Generator V2")
            print("="*80)
        
        # Load data
        if not args.quiet:
            print(f"\n📖 Loading spell data from {args.csv}...")
        
        try:
            spells = load_spell_data(args.csv)
        except Exception as e:
            print(f"Error loading CSV: {e}", file=sys.stderr)
            return 1
        
        if not args.quiet:
            print(f"   ✅ Loaded {len(spells)} spells")
        
        # Load assets
        if not args.quiet:
            print(f"\n🎨 Loading assets from {args.assets}...")
        
        try:
            assets = load_assets(args.assets)
        except Exception as e:
            print(f"Error loading assets: {e}", file=sys.stderr)
            return 1
        
        if not args.quiet:
            print("   ✅ Assets loaded successfully")
        
        # Generate card images
        if not args.quiet:
            print(f"\n🃏 Generating card images...")
        
        generator = CardGenerator(assets)
        
        # Setup progress callback
        progress_callback = None
        if args.verbose:
            def progress_callback(current, total, spell_name):
                print(f"   [{current}/{total}] {spell_name}")
        elif not args.quiet:
            def progress_callback(current, total, spell_name):
                if current % 10 == 0 or current == total:
                    print(f"   Progress: {current}/{total} ({current*100//total}%)")
        
        processor = BatchProcessor(generator, args.output, progress_callback=progress_callback)
        results = processor.process_spells(spells)
        
        # Report results
        summary = processor.get_summary(results)
        if not args.quiet:
            print(f"   ✅ Generated {summary['successful']} cards")
            if summary['failed'] > 0:
                print(f"   ⚠️  {summary['failed']} cards failed")
        
        # Generate PDF if requested
        if not args.no_pdf:
            if not args.quiet:
                print(f"\n📄 Generating PDF ({args.pdf_mode} mode)...")
            
            try:
                pdf_path = self._generate_pdf(args, spells, args.output)
                if not args.quiet:
                    print(f"   ✅ PDF created: {pdf_path}")
                
                # Cleanup PNG files unless --keep-images is specified
                if not args.keep_images:
                    if not args.quiet:
                        print(f"\n🧹 Cleaning up intermediate PNG files...")
                    
                    try:
                        cleanup_count = self._cleanup_png_files(args.output, spells)
                        if not args.quiet:
                            print(f"   ✅ Removed {cleanup_count} PNG files")
                    except Exception as e:
                        # Don't fail the operation if cleanup fails
                        if not args.quiet:
                            print(f"   ⚠️  Cleanup warning: {e}")
                        if args.verbose:
                            import traceback
                            traceback.print_exc()
                
            except Exception as e:
                print(f"Error generating PDF: {e}", file=sys.stderr)
                if args.verbose:
                    import traceback
                    traceback.print_exc()
                return 1
        
        # Final summary
        if not args.quiet:
            print("\n" + "="*80)
            print("✅ COMPLETE")
            print("="*80)
            print(f"📁 Output directory: {args.output.absolute()}")
            if not args.no_pdf:
                print(f"📄 PDF file: {pdf_path.name}")
                if args.keep_images:
                    print(f"🃏 Card images: {summary['successful'] * 2} files (preserved)")
                else:
                    print(f"🃏 Card images: Cleaned up (use --keep-images to preserve)")
            else:
                print(f"🃏 Card images: {summary['successful'] * 2} files")
        
        return 0
    
    def _generate_pdf(self, args, spells, output_dir: Path) -> Path:
        """Generate PDF based on selected mode.
        
        Args:
            args: Parsed arguments
            spells: List of spell data
            output_dir: Output directory
            
        Returns:
            Path to generated PDF file
        """
        card_names = [spell.name for spell in spells]
        
        # Determine PDF filename
        if args.pdf_name:
            pdf_name = args.pdf_name if args.pdf_name.endswith('.pdf') else f"{args.pdf_name}.pdf"
        else:
            pdf_name = f"cards_{args.pdf_mode.replace('-', '_')}.pdf"
        
        pdf_path = output_dir / pdf_name
        
        if args.pdf_mode == 'single-card':
            # Single-card A7 mode
            generator = SingleCardPDFGenerator()
            result = generator.generate_pdf(card_names, pdf_path, output_dir)
            
            if args.verbose:
                print(f"   Pages: {result['total_pages']}")
                if result['missing_files']:
                    print(f"   Missing files: {len(result['missing_files'])}")
        
        else:
            # Grid or cut-ready mode - need grid configuration
            rows, cols = self._parse_grid(args.grid)
            
            # Determine margins and gaps
            if args.pdf_mode == 'cut-ready':
                margin = args.margin if args.margin is not None else 5
                gap = args.gap if args.gap is not None else 5
            else:
                margin = args.margin if args.margin is not None else 20
                gap = args.gap if args.gap is not None else 10
            
            config = GridConfig(
                rows=rows,
                cols=cols,
                orientation=args.orientation,
                margin=margin,
                gap_x=gap,
                gap_y=gap
            )
            
            if args.pdf_mode == 'cut-ready':
                generator = CutReadyPDFGenerator(config)
            else:
                generator = PDFGenerator(config)
            
            result = generator.generate_pdf(card_names, pdf_path, output_dir)
            
            if args.verbose:
                print(f"   Grid: {rows}×{cols} {args.orientation}")
                print(f"   Pages: {result['total_pages']}")
                if result['missing_files']:
                    print(f"   Missing files: {len(result['missing_files'])}")
        
        return pdf_path
    
    @staticmethod
    def _parse_grid(grid_str: str) -> tuple:
        """Parse grid string like '3x3' into (rows, cols).
        
        Args:
            grid_str: Grid specification like '3x3', '2x4', etc.
            
        Returns:
            Tuple of (rows, cols)
            
        Raises:
            ValueError: If grid string is invalid
        """
        try:
            parts = grid_str.lower().split('x')
            if len(parts) != 2:
                raise ValueError("Grid must be in format ROWSxCOLS (e.g., 3x3)")
            
            rows = int(parts[0])
            cols = int(parts[1])
            
            if rows < 1 or cols < 1:
                raise ValueError("Rows and columns must be at least 1")
            
            return rows, cols
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid grid format '{grid_str}': {e}")
    
    @staticmethod
    def _cleanup_png_files(output_dir: Path, spells) -> int:
        """Clean up intermediate PNG files after PDF generation.
        
        Args:
            output_dir: Directory containing PNG files
            spells: List of spell data
            
        Returns:
            Number of files deleted
            
        Raises:
            Exception: If cleanup fails
        """
        import os
        
        deleted_count = 0
        
        for spell in spells:
            # Sanitize filename (same logic as batch processor)
            sanitized_name = spell.name.lower().replace("'", "").replace(" ", "_")
            sanitized_name = "".join(c for c in sanitized_name if c.isalnum() or c == "_")
            
            # Delete front and back PNG files
            front_file = output_dir / f"{sanitized_name}_front.png"
            back_file = output_dir / f"{sanitized_name}_back.png"
            
            for file_path in [front_file, back_file]:
                if file_path.exists():
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                    except Exception as e:
                        # Log but continue with other files
                        raise Exception(f"Failed to delete {file_path}: {e}")
        
        return deleted_count


def main():
    """Main entry point for CLI."""
    cli = SpellCardCLI()
    sys.exit(cli.run())


if __name__ == '__main__':
    main()
