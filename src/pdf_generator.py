"""PDF generation with multiple layout modes for double-sided printing.

This module provides functionality to arrange spell card images into PDF pages
with different layout modes:
- Grid layout: Multiple cards per page in a grid
- Single-card layout: One card per A7 page
- Cut-ready layout: Fixed card dimensions with cut guidelines and bleed

All modes handle double-sided alignment to ensure fronts and backs align
correctly when printed.
"""

from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


@dataclass
class GridConfig:
    """Configuration for PDF grid layout."""
    rows: int = 3
    cols: int = 3
    orientation: str = "portrait"  # "portrait" or "landscape"
    margin: float = 20  # Page margin in points
    gap_x: float = 10   # Horizontal gap between cards in points
    gap_y: float = 10   # Vertical gap between cards in points
    
    def __post_init__(self):
        """Validate configuration."""
        if self.rows < 1 or self.cols < 1:
            raise ValueError("Rows and cols must be at least 1")
        if self.orientation not in ["portrait", "landscape"]:
            raise ValueError("Orientation must be 'portrait' or 'landscape'")


class PDFGenerator:
    """Generates PDF files with spell cards in grid layout."""
    
    # Standard A7 card aspect ratio (portrait)
    CARD_ASPECT_RATIO = 210 / 298
    
    def __init__(self, config: GridConfig):
        """Initialize PDF generator with grid configuration.
        
        Args:
            config: Grid layout configuration
        """
        self.config = config
        self.page_size = self._get_page_size()
        self.page_width, self.page_height = self.page_size
        self.card_width, self.card_height = self._calculate_card_dimensions()
        self.positions = self._calculate_positions()
        self.back_order = self._calculate_back_order()
    
    def _get_page_size(self) -> Tuple[float, float]:
        """Get page size based on orientation.
        
        Returns:
            Tuple of (width, height) in points
        """
        if self.config.orientation == "landscape":
            return landscape(A4)
        return A4
    
    def _calculate_card_dimensions(self) -> Tuple[float, float]:
        """Calculate optimal card dimensions to fit the grid on the page.
        
        The algorithm:
        1. Calculate available space after margins and gaps
        2. Determine card width based on available width
        3. Calculate card height from width using aspect ratio
        4. If total height exceeds available space, scale down
        
        Returns:
            Tuple of (card_width, card_height) in points
        """
        # Available space for the grid
        avail_width = (self.page_width - 2 * self.config.margin - 
                      (self.config.cols - 1) * self.config.gap_x)
        avail_height = (self.page_height - 2 * self.config.margin - 
                       (self.config.rows - 1) * self.config.gap_y)
        
        # Calculate card dimensions based on available width
        card_width = avail_width / self.config.cols
        card_height = card_width / self.CARD_ASPECT_RATIO
        
        # Check if height fits, scale down if needed
        total_height = (card_height * self.config.rows + 
                       (self.config.rows - 1) * self.config.gap_y)
        if total_height > avail_height:
            card_height = avail_height / self.config.rows
            card_width = card_height * self.CARD_ASPECT_RATIO
        
        return card_width, card_height
    
    def _calculate_positions(self) -> List[Tuple[float, float]]:
        """Calculate card positions in the grid.
        
        Positions are calculated from bottom-left, row by row, left to right.
        The grid is centered on the page.
        
        Returns:
            List of (x, y) positions in points
        """
        # Calculate total grid size
        grid_width = (self.config.cols * self.card_width + 
                     (self.config.cols - 1) * self.config.gap_x)
        grid_height = (self.config.rows * self.card_height + 
                      (self.config.rows - 1) * self.config.gap_y)
        
        # Center the grid on the page
        offset_x = (self.page_width - grid_width) / 2.0
        offset_y = (self.page_height - grid_height) / 2.0
        
        # Calculate positions for each card
        positions = []
        for row in range(self.config.rows):
            for col in range(self.config.cols):
                x = offset_x + col * (self.card_width + self.config.gap_x)
                y = offset_y + row * (self.card_height + self.config.gap_y)
                positions.append((x, y))
        
        return positions
    
    def _calculate_back_order(self) -> List[int]:
        """Calculate the order of cards on back pages for double-sided alignment.
        
        For double-sided printing, each row must be horizontally mirrored.
        This ensures that when the page is flipped horizontally, the backs
        align with their corresponding fronts.
        
        Example for 3x3 grid:
        Front page positions:  [0, 1, 2, 3, 4, 5, 6, 7, 8]
        Back page order:       [2, 1, 0, 5, 4, 3, 8, 7, 6]
        
        Returns:
            List of indices indicating the order for back pages
        """
        back_order = []
        for row in range(self.config.rows):
            # Get indices for this row
            row_start = row * self.config.cols
            row_indices = list(range(row_start, row_start + self.config.cols))
            # Reverse the row (horizontal mirror)
            back_order.extend(reversed(row_indices))
        
        return back_order
    
    def generate_pdf(
        self,
        card_names: List[str],
        output_path: Path,
        image_dir: Path
    ) -> dict:
        """Generate PDF with cards in grid layout.
        
        Args:
            card_names: List of card base names (without _front.png/_back.png)
            output_path: Path for output PDF file
            image_dir: Directory containing card images
        
        Returns:
            Dictionary with generation statistics:
            - total_cards: Number of cards processed
            - total_pages: Number of pages generated
            - missing_files: List of missing image files
        """
        cards_per_page = self.config.rows * self.config.cols
        missing_files = []
        
        # Group cards into pages
        groups = []
        for i in range(0, len(card_names), cards_per_page):
            group = card_names[i:i + cards_per_page]
            # Pad last group with None if incomplete
            if len(group) < cards_per_page:
                group.extend([None] * (cards_per_page - len(group)))
            groups.append(group)
        
        # Create PDF
        output_path.parent.mkdir(parents=True, exist_ok=True)
        c = canvas.Canvas(str(output_path), pagesize=self.page_size)
        
        # Generate pages for each group
        for group in groups:
            # Front page
            self._draw_page(c, group, image_dir, "front", self.positions, missing_files)
            c.showPage()
            
            # Back page (with mirrored order)
            self._draw_page(c, group, image_dir, "back", self.positions, missing_files, self.back_order)
            c.showPage()
        
        c.save()
        
        return {
            "total_cards": len(card_names),
            "total_pages": len(groups) * 2,
            "missing_files": missing_files
        }
    
    def _draw_page(
        self,
        c: canvas.Canvas,
        group: List[Optional[str]],
        image_dir: Path,
        side: str,
        positions: List[Tuple[float, float]],
        missing_files: List[str],
        order: Optional[List[int]] = None
    ):
        """Draw a single page with cards.
        
        Args:
            c: ReportLab canvas
            group: List of card names (or None for empty slots)
            image_dir: Directory containing card images
            side: "front" or "back"
            positions: List of (x, y) positions
            missing_files: List to append missing file paths
            order: Optional reordering of cards (for back pages)
        """
        if order is None:
            order = list(range(len(group)))
        
        for i, idx in enumerate(order):
            card_name = group[idx]
            if card_name is None:
                continue
            
            # Sanitize filename to match batch processor output
            safe_name = self._sanitize_filename(card_name)
            image_path = image_dir / f"{safe_name}_{side}.png"
            
            if not image_path.exists():
                missing_files.append(str(image_path))
                continue
            
            # Draw image at position
            pos = positions[i]
            c.drawImage(
                str(image_path),
                pos[0], pos[1],
                width=self.card_width,
                height=self.card_height
            )
    
    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Convert spell name to safe filename (matches batch processor logic).
        
        Args:
            name: Spell name
            
        Returns:
            Safe filename string
        """
        # Replace spaces with underscores
        safe = name.replace(" ", "_")
        
        # Remove or replace unsafe characters
        unsafe_chars = '<>:"/\\|?*\''
        for char in unsafe_chars:
            safe = safe.replace(char, "")
        
        # Convert to lowercase
        safe = safe.lower()
        
        return safe


class SingleCardPDFGenerator:
    """Generates PDF with one card per A7 page, alternating front/back.
    
    This mode creates A7-sized pages (74.25mm × 105mm) with one card per page.
    Cards alternate between front and back for each spell, making it easy to
    print and assemble individual cards.
    """
    
    # A7 dimensions in points (portrait orientation)
    A7_WIDTH = 210  # ~74.25mm
    A7_HEIGHT = 298  # ~105mm
    
    def __init__(self):
        """Initialize single-card PDF generator."""
        self.page_size = (self.A7_WIDTH, self.A7_HEIGHT)
    
    def generate_pdf(
        self,
        card_names: List[str],
        output_path: Path,
        image_dir: Path
    ) -> dict:
        """Generate PDF with one card per A7 page.
        
        For each spell, creates two pages:
        - Page 1: Front of card
        - Page 2: Back of card
        
        Args:
            card_names: List of card base names (without _front.png/_back.png)
            output_path: Path for output PDF file
            image_dir: Directory containing card images
        
        Returns:
            Dictionary with generation statistics:
            - total_cards: Number of cards processed
            - total_pages: Number of pages generated (2 per card)
            - missing_files: List of missing image files
        """
        missing_files = []
        
        # Create PDF
        output_path.parent.mkdir(parents=True, exist_ok=True)
        c = canvas.Canvas(str(output_path), pagesize=self.page_size)
        
        # Generate pages for each card (front, then back)
        for card_name in card_names:
            # Sanitize filename to match batch processor output
            safe_name = self._sanitize_filename(card_name)
            
            # Front page
            front_path = image_dir / f"{safe_name}_front.png"
            if front_path.exists():
                c.drawImage(
                    str(front_path),
                    0, 0,
                    width=self.A7_WIDTH,
                    height=self.A7_HEIGHT
                )
            else:
                missing_files.append(str(front_path))
            c.showPage()
            
            # Back page
            back_path = image_dir / f"{safe_name}_back.png"
            if back_path.exists():
                c.drawImage(
                    str(back_path),
                    0, 0,
                    width=self.A7_WIDTH,
                    height=self.A7_HEIGHT
                )
            else:
                missing_files.append(str(back_path))
            c.showPage()
        
        c.save()
        
        return {
            "total_cards": len(card_names),
            "total_pages": len(card_names) * 2,
            "missing_files": missing_files
        }
    
    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Convert spell name to safe filename (matches batch processor logic).
        
        Args:
            name: Spell name
            
        Returns:
            Safe filename string
        """
        # Replace spaces with underscores
        safe = name.replace(" ", "_")
        
        # Remove or replace unsafe characters
        unsafe_chars = '<>:"/\\|?*\''
        for char in unsafe_chars:
            safe = safe.replace(char, "")
        
        # Convert to lowercase
        safe = safe.lower()
        
        return safe


class CutReadyPDFGenerator:
    """Generates PDF with fixed card dimensions, cut guidelines, and bleed.
    
    This mode is designed for professional printing and cutting:
    - Fixed card dimensions (63.5mm × 88.5mm - standard poker card size)
    - Cut guidelines showing where to cut
    - Bleed borders extending content beyond cut lines
    - Perfect double-sided alignment for front/back
    
    The double-sided alignment is critical: when you print the front page,
    flip it horizontally, and print the back page, the cards must align
    perfectly for cutting.
    """
    
    # Standard poker card dimensions in mm
    CARD_WIDTH_MM = 63.5
    CARD_HEIGHT_MM = 88.5
    
    # Bleed border in mm (content extends beyond cut line)
    BLEED_MM = 1.5
    
    def __init__(self, config: GridConfig):
        """Initialize cut-ready PDF generator.
        
        Args:
            config: Grid configuration (rows, cols, orientation)
        """
        self.config = config
        self.page_size = self._get_page_size()
        self.page_width, self.page_height = self.page_size
        
        # Convert dimensions to points
        self.card_width = self.CARD_WIDTH_MM * mm
        self.card_height = self.CARD_HEIGHT_MM * mm
        self.bleed = self.BLEED_MM * mm
        
        # Calculate positions and validate fit
        self.positions = self._calculate_positions()
        self.back_order = self._calculate_back_order()
        
        # Validate that grid fits on page
        self._validate_grid_fits()
    
    def _get_page_size(self) -> Tuple[float, float]:
        """Get page size based on orientation."""
        if self.config.orientation == "landscape":
            return landscape(A4)
        return A4
    
    def _calculate_positions(self) -> List[Tuple[float, float]]:
        """Calculate card positions with fixed dimensions.
        
        Unlike the grid layout which scales cards to fit, this uses fixed
        card dimensions and calculates positions to center the grid.
        """
        # Calculate total grid size with fixed card dimensions
        grid_width = (self.config.cols * self.card_width + 
                     (self.config.cols - 1) * self.config.gap_x)
        grid_height = (self.config.rows * self.card_height + 
                      (self.config.rows - 1) * self.config.gap_y)
        
        # Center the grid on the page
        offset_x = (self.page_width - grid_width) / 2.0
        offset_y = (self.page_height - grid_height) / 2.0
        
        # Calculate positions for each card
        positions = []
        for row in range(self.config.rows):
            for col in range(self.config.cols):
                x = offset_x + col * (self.card_width + self.config.gap_x)
                y = offset_y + row * (self.card_height + self.config.gap_y)
                positions.append((x, y))
        
        return positions
    
    def _calculate_back_order(self) -> List[int]:
        """Calculate the order of cards on back pages for double-sided alignment.
        
        Same as grid layout: each row is horizontally mirrored.
        """
        back_order = []
        for row in range(self.config.rows):
            row_start = row * self.config.cols
            row_indices = list(range(row_start, row_start + self.config.cols))
            back_order.extend(reversed(row_indices))
        
        return back_order
    
    def _validate_grid_fits(self):
        """Validate that the grid with fixed card dimensions fits on the page.
        
        Raises:
            ValueError: If grid doesn't fit on page
        """
        grid_width = (self.config.cols * self.card_width + 
                     (self.config.cols - 1) * self.config.gap_x)
        grid_height = (self.config.rows * self.card_height + 
                      (self.config.rows - 1) * self.config.gap_y)
        
        # Add margins
        total_width = grid_width + 2 * self.config.margin
        total_height = grid_height + 2 * self.config.margin
        
        if total_width > self.page_width or total_height > self.page_height:
            raise ValueError(
                f"Grid with fixed card dimensions ({self.config.rows}×{self.config.cols}) "
                f"doesn't fit on {self.config.orientation} page. "
                f"Required: {total_width:.1f}×{total_height:.1f}pt, "
                f"Available: {self.page_width:.1f}×{self.page_height:.1f}pt"
            )
    
    def generate_pdf(
        self,
        card_names: List[str],
        output_path: Path,
        image_dir: Path
    ) -> dict:
        """Generate cut-ready PDF with guidelines and bleed.
        
        Args:
            card_names: List of card base names
            output_path: Path for output PDF file
            image_dir: Directory containing card images
        
        Returns:
            Dictionary with generation statistics
        """
        cards_per_page = self.config.rows * self.config.cols
        missing_files = []
        
        # Group cards into pages
        groups = []
        for i in range(0, len(card_names), cards_per_page):
            group = card_names[i:i + cards_per_page]
            if len(group) < cards_per_page:
                group.extend([None] * (cards_per_page - len(group)))
            groups.append(group)
        
        # Create PDF
        output_path.parent.mkdir(parents=True, exist_ok=True)
        c = canvas.Canvas(str(output_path), pagesize=self.page_size)
        
        # Generate pages for each group
        for group in groups:
            # Skip completely empty groups (all None)
            if all(card is None for card in group):
                continue
            
            # Front page
            self._draw_cut_ready_page(c, group, image_dir, "front", missing_files)
            c.showPage()
            
            # Back page (with mirrored order)
            self._draw_cut_ready_page(c, group, image_dir, "back", missing_files, use_back_order=True)
            c.showPage()
        
        c.save()
        
        return {
            "total_cards": len(card_names),
            "total_pages": len(groups) * 2,
            "missing_files": missing_files
        }
    
    def _draw_cut_ready_page(
        self,
        c: canvas.Canvas,
        group: List[Optional[str]],
        image_dir: Path,
        side: str,
        missing_files: List[str],
        use_back_order: bool = False
    ):
        """Draw a cut-ready page with cards, bleed, and guidelines.
        
        The rendering order:
        1. Draw cut guidelines (on white background)
        2. Fill bleed area for each filled card position with black
        3. Draw card images
        4. Draw card borders
        
        This ensures guidelines are behind the black bleed, so they won't
        be visible if cutting is slightly inaccurate.
        
        Args:
            c: ReportLab canvas
            group: List of card names (or None for empty slots)
            image_dir: Directory containing card images
            side: "front" or "back"
            missing_files: List to append missing file paths
            use_back_order: Whether to use mirrored order for back pages
        """
        order = self.back_order if use_back_order else list(range(len(group)))
        
        # Step 1: Draw cut guidelines FIRST (on white background)
        # This way they'll be hidden under the black bleed if cut is accurate
        self._draw_cut_guidelines(c, group, order)
        
        # Step 2: Fill bleed background only for filled positions
        # This covers the guidelines in the bleed area
        self._draw_bleed_background(c, group, order)
        
        # Step 3: Draw card images
        for i, idx in enumerate(order):
            card_name = group[idx]
            if card_name is None:
                continue
            
            # Sanitize filename to match batch processor output
            safe_name = self._sanitize_filename(card_name)
            image_path = image_dir / f"{safe_name}_{side}.png"
            
            if not image_path.exists():
                missing_files.append(str(image_path))
                continue
            
            pos = self.positions[i]
            c.drawImage(
                str(image_path),
                pos[0], pos[1],
                width=self.card_width,
                height=self.card_height
            )
        
        # Step 4: Draw borders around each card
        self._draw_card_borders(c, group, order)
    
    def _draw_bleed_background(
        self,
        c: canvas.Canvas,
        group: List[Optional[str]],
        order: List[int]
    ):
        """Draw black background only for filled card positions.
        
        This creates bleed borders around each card that has content,
        leaving empty slots white.
        
        Args:
            c: ReportLab canvas
            group: List of card names (or None for empty slots)
            order: Order to draw cards (for back page mirroring)
        """
        c.setFillColorRGB(0, 0, 0)
        
        # Draw black rectangle with bleed for each filled position
        for i, idx in enumerate(order):
            if group[idx] is not None:
                pos = self.positions[i]
                c.rect(
                    pos[0] - self.bleed,
                    pos[1] - self.bleed,
                    self.card_width + 2 * self.bleed,
                    self.card_height + 2 * self.bleed,
                    fill=1,
                    stroke=0
                )
    
    def _draw_cut_guidelines(
        self,
        c: canvas.Canvas,
        group: List[Optional[str]],
        order: List[int]
    ):
        """Draw dashed cut guidelines only at boundaries of filled cards.
        
        Guidelines extend across the entire page to make cutting easier.
        They show exactly where to cut to separate the cards.
        
        Args:
            c: ReportLab canvas
            group: List of card names (or None for empty slots)
            order: Order to draw cards (for back page mirroring)
        """
        # Collect edges only for filled positions
        verticals = set()
        horizontals = set()
        
        for i, idx in enumerate(order):
            if group[idx] is not None:
                x, y = self.positions[i]
                verticals.add(x)
                verticals.add(x + self.card_width)
                horizontals.add(y)
                horizontals.add(y + self.card_height)
        
        # Draw dashed lines
        c.setDash(3, 3)
        c.setStrokeColorRGB(0.5, 0.5, 0.5)  # Gray
        c.setLineWidth(0.5)
        
        # Vertical guidelines
        for x in verticals:
            c.line(x, 0, x, self.page_height)
        
        # Horizontal guidelines
        for y in horizontals:
            c.line(0, y, self.page_width, y)
        
        c.setDash([])  # Reset to solid lines
    
    def _draw_card_borders(
        self,
        c: canvas.Canvas,
        group: List[Optional[str]],
        order: List[int]
    ):
        """Draw borders around each card for visual separation.
        
        Args:
            c: ReportLab canvas
            group: List of card names
            order: Order to draw cards (for back page mirroring)
        """
        c.setLineWidth(self.bleed)
        c.setStrokeColorRGB(0, 0, 0)
        
        for i, idx in enumerate(order):
            if group[idx] is not None:
                pos = self.positions[i]
                c.rect(
                    pos[0] - self.bleed,
                    pos[1] - self.bleed,
                    self.card_width + 2 * self.bleed,
                    self.card_height + 2 * self.bleed,
                    stroke=1,
                    fill=0
                )
    
    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Convert spell name to safe filename (matches batch processor logic).
        
        Args:
            name: Spell name
            
        Returns:
            Safe filename string
        """
        # Replace spaces with underscores
        safe = name.replace(" ", "_")
        
        # Remove or replace unsafe characters
        unsafe_chars = '<>:"/\\|?*\''
        for char in unsafe_chars:
            safe = safe.replace(char, "")
        
        # Convert to lowercase
        safe = safe.lower()
        
        return safe
