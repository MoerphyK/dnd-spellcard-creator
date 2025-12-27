"""Card generation for spell cards."""

from pathlib import Path
from typing import Tuple
from PIL import Image
from .models import SpellData, AssetCollection
from .text_renderer import TextRenderer
from .table_formatter import TableFormatter


class CardGenerator:
    """Generates spell card images (front and back)."""
    
    def __init__(self, assets: AssetCollection):
        """
        Initialize card generator with assets.
        
        Args:
            assets: Collection of graphical assets
        """
        self.assets = assets
        self.text_renderer = TextRenderer(assets.font_path)
    
    def _load_image(self, path: Path) -> Image.Image:
        """Load and convert image to RGBA."""
        return Image.open(path).convert("RGBA")
    
    def _paste_with_alpha(
        self,
        base: Image.Image,
        overlay: Image.Image,
        position: Tuple[int, int] = (0, 0)
    ) -> None:
        """
        Paste overlay onto base image with alpha blending.
        
        Args:
            base: Base image to paste onto
            overlay: Image to paste
            position: (x, y) position to paste at
        """
        base.paste(overlay, position, overlay)
    
    def generate_card_front(
        self,
        spell: SpellData,
        output_path: Path
    ) -> Image.Image:
        """
        Generate front side of spell card.
        
        Args:
            spell: Spell data
            output_path: Path to save card image
            
        Returns:
            Generated card image
        """
        # Load background
        card = self._load_image(self.assets.front_background)
        
        # Add illustration if available
        if spell.illustration_path and spell.illustration_path.exists():
            illustration = self._load_image(spell.illustration_path)
            # Resize to fit illustration area (477x477 based on v1)
            illustration = illustration.resize((477, 477), Image.Resampling.LANCZOS)
            self._paste_with_alpha(card, illustration, (138, 230))
        
        # Add front frame overlay
        frame = self._load_image(self.assets.front_frame)
        self._paste_with_alpha(card, frame)
        
        # Add class banners
        for class_name in spell.classes:
            if class_name in self.assets.class_banners:
                banner_path = self.assets.class_banners[class_name]
                if banner_path.exists():
                    banner = self._load_image(banner_path)
                    self._paste_with_alpha(card, banner)
        
        # Add spell name banner with text
        spell_banner = self._load_image(self.assets.spell_banner).copy()
        self.text_renderer.render_text_centered(
            spell_banner,
            spell.name,
            center=(spell_banner.width // 2, 145),
            max_width=spell_banner.width - 80,
            max_height=90,
            max_font_size=36,
            color="black"
        )
        self._paste_with_alpha(card, spell_banner)
        
        # Add spell level
        self.text_renderer.render_text_centered(
            card,
            spell.level_numeric,
            center=(130, 880),
            max_width=90,
            max_height=85,
            max_font_size=60,
            color="black"
        )
        
        # Add stat boxes
        # Casting Time (top left)
        self.text_renderer.render_text_centered(
            card,
            spell.casting_time,
            center=(370, 845),
            max_width=133,
            max_height=60,
            max_font_size=24,
            color="black"
        )
        
        # Duration (top right)
        self.text_renderer.render_text_centered(
            card,
            spell.duration,
            center=(604, 845),
            max_width=133,
            max_height=60,
            max_font_size=24,
            color="black"
        )
        
        # Range (bottom left)
        self.text_renderer.render_text_centered(
            card,
            spell.range,
            center=(382, 953),
            max_width=133,
            max_height=60,
            max_font_size=24,
            color="black"
        )
        
        # Components (bottom right) - simplified
        self.text_renderer.render_text_centered(
            card,
            spell.components_short,
            center=(604, 953),
            max_width=133,
            max_height=60,
            max_font_size=24,
            color="black"
        )
        
        # Save card
        card.save(output_path)
        return card
    
    def generate_card_back(
        self,
        spell: SpellData,
        output_path: Path
    ) -> Image.Image:
        """
        Generate back side of spell card.
        
        Args:
            spell: Spell data
            output_path: Path to save card image
            
        Returns:
            Generated card image
        """
        # Load background
        card = self._load_image(self.assets.back_background)
        
        # Add class banners
        for class_name in spell.classes:
            if class_name in self.assets.class_banners:
                banner_path = self.assets.class_banners[class_name]
                if banner_path.exists():
                    banner = self._load_image(banner_path)
                    self._paste_with_alpha(card, banner)
        
        # Add spell name banner with text
        spell_banner = self._load_image(self.assets.spell_banner).copy()
        self.text_renderer.render_text_centered(
            spell_banner,
            spell.name,
            center=(spell_banner.width // 2, 145),
            max_width=spell_banner.width - 80,
            max_height=90,
            max_font_size=36,
            color="black"
        )
        self._paste_with_alpha(card, spell_banner)
        
        # Add info box with structured stats
        # Filter classes to only valid ones
        valid_classes = [c for c in spell.classes if c in self.assets.class_banners]
        class_list = ", ".join(valid_classes)
        
        info_text = (
            f"Level:        {spell.level}\n"
            f"Casting Time: {spell.casting_time}\n"
            f"Duration:     {spell.duration}\n"
            f"Range:        {spell.range}\n"
            f"Components:   {spell.components}\n"
            f"Classes:      {class_list}"
        )
        
        self.text_renderer.render_text_left_aligned(
            card,
            info_text,
            top_left=(120, 229),
            max_width=544,
            max_height=140,
            max_font_size=20,
            min_font_size=12,
            color="black",
            line_spacing=2,
            paragraph_spacing=20
        )
        
        # Add description
        # Format description with table detection
        # Estimate character width: 574 pixels / ~7 pixels per char at small font = ~80 chars
        formatted_description = TableFormatter.format_description_with_table(
            spell.description, 
            max_width=80
        )
        
        if spell.at_higher_levels:
            description_text = (
                f"Description:\n{formatted_description}\n\n\n"
                f"At Higher Levels:\n{spell.at_higher_levels}"
            )
        else:
            description_text = f"Description:\n{formatted_description}"
        
        self.text_renderer.render_text_left_aligned(
            card,
            description_text,
            top_left=(90, 229 + 140 + 15),  # Below info box with gap
            max_width=574,
            max_height=588,
            max_font_size=32,
            min_font_size=10,
            color="black",
            line_spacing=4,  # Increased for better readability and space usage
            paragraph_spacing=25  # Increased for clearer paragraph separation
        )
        
        # Save card
        card.save(output_path)
        return card
