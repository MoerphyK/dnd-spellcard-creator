"""Batch processing for generating multiple spell cards."""

from pathlib import Path
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass

from .models import SpellData, AssetCollection
from .card_generator import CardGenerator


@dataclass
class ProcessingResult:
    """Result of processing a single spell."""
    spell_name: str
    success: bool
    front_path: Optional[Path] = None
    back_path: Optional[Path] = None
    error: Optional[str] = None


class BatchProcessor:
    """Process multiple spells and generate card images."""
    
    def __init__(
        self,
        card_generator: CardGenerator,
        output_dir: Path,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ):
        """
        Initialize batch processor.
        
        Args:
            card_generator: CardGenerator instance
            output_dir: Directory for output images
            progress_callback: Optional callback(current, total, spell_name)
        """
        self.card_generator = card_generator
        self.output_dir = Path(output_dir)
        self.progress_callback = progress_callback
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def process_spells(self, spells: List[SpellData]) -> Dict[str, ProcessingResult]:
        """
        Process multiple spells and generate cards.
        
        Args:
            spells: List of spell data to process
            
        Returns:
            Dictionary mapping spell names to processing results
        """
        results = {}
        total = len(spells)
        
        for i, spell in enumerate(spells, 1):
            # Report progress
            if self.progress_callback:
                self.progress_callback(i, total, spell.name)
            
            # Process this spell
            result = self._process_single_spell(spell)
            results[spell.name] = result
        
        return results
    
    def _process_single_spell(self, spell: SpellData) -> ProcessingResult:
        """
        Process a single spell, handling errors gracefully.
        
        Args:
            spell: Spell data to process
            
        Returns:
            ProcessingResult with success/failure information
        """
        try:
            # Generate filenames
            safe_name = self._sanitize_filename(spell.name)
            front_path = self.output_dir / f"{safe_name}_front.png"
            back_path = self.output_dir / f"{safe_name}_back.png"
            
            # Generate front and back (these methods save the images)
            self.card_generator.generate_card_front(spell, front_path)
            self.card_generator.generate_card_back(spell, back_path)
            
            return ProcessingResult(
                spell_name=spell.name,
                success=True,
                front_path=front_path,
                back_path=back_path
            )
            
        except Exception as e:
            return ProcessingResult(
                spell_name=spell.name,
                success=False,
                error=str(e)
            )
    
    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """
        Convert spell name to safe filename.
        
        Args:
            name: Spell name
            
        Returns:
            Safe filename string
        """
        # Replace spaces with underscores
        safe = name.replace(" ", "_")
        
        # Remove or replace unsafe characters (including apostrophes)
        unsafe_chars = '<>:"/\\|?*\''
        for char in unsafe_chars:
            safe = safe.replace(char, "")
        
        # Convert to lowercase
        safe = safe.lower()
        
        return safe
    
    def get_summary(self, results: Dict[str, ProcessingResult]) -> Dict[str, any]:
        """
        Generate summary statistics from processing results.
        
        Args:
            results: Dictionary of processing results
            
        Returns:
            Dictionary with summary statistics
        """
        total = len(results)
        successful = sum(1 for r in results.values() if r.success)
        failed = total - successful
        
        errors = {
            name: result.error
            for name, result in results.items()
            if not result.success
        }
        
        return {
            "total": total,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total if total > 0 else 0,
            "errors": errors
        }
