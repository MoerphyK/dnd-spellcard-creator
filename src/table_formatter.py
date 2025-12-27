"""Table detection and formatting for spell descriptions."""

import re
from typing import List, Tuple, Optional


class TableFormatter:
    """Detects and formats tables in spell descriptions."""
    
    @staticmethod
    def detect_table(text: str) -> bool:
        """
        Detect if text contains a table structure.
        
        Common patterns:
        - Multiple lines with consistent column separators
        - Header row followed by data rows
        - Numeric ranges (01-00, 01-05, etc.)
        
        Args:
            text: Text to analyze
            
        Returns:
            True if table detected
        """
        # Look for table indicators
        table_indicators = [
            r'\d{2}-\d{2}',  # Numeric ranges like 01-00, 01-05
            r'[A-Z][a-z]+\s+[A-Z][a-z]+\s+[A-Z][a-z]+',  # Multiple capitalized words (headers)
        ]
        
        for pattern in table_indicators:
            if len(re.findall(pattern, text)) >= 3:
                return True
        
        return False
    
    @staticmethod
    def extract_table_section(text: str) -> Tuple[str, Optional[str], str]:
        """
        Extract table section from text.
        
        Args:
            text: Full text containing table
            
        Returns:
            Tuple of (before_table, table_text, after_table)
        """
        # Look for table start patterns
        # Common: "TableName" followed by column headers
        table_start_patterns = [
            r'([A-Z][a-z]+ ?[A-Z][a-z]+)\s*([A-Z][a-z]+[A-Z][a-z]+[A-Z][a-z]+)',  # "Teleportation OutcomeFamiliarityMishap..."
            r'([A-Z][a-z]+ [A-Z][a-z]+)\n([A-Z][a-z]+)',  # "Table Name\nHeader"
        ]
        
        for pattern in table_start_patterns:
            match = re.search(pattern, text)
            if match:
                start_pos = match.start()
                
                # Find table end (usually before next sentence or section)
                # Look for end patterns: period followed by capital letter, or "Familiarity." section
                end_patterns = [
                    r'\.\s+[A-Z][a-z]+\.',  # ". Familiarity."
                    r'\s+[A-Z][a-z]+\.\s+',  # " Mishap. "
                ]
                
                end_pos = len(text)
                for end_pattern in end_patterns:
                    end_match = re.search(end_pattern, text[start_pos:])
                    if end_match:
                        end_pos = start_pos + end_match.start()
                        break
                
                before = text[:start_pos]
                table = text[start_pos:end_pos]
                after = text[end_pos:]
                
                return before, table, after
        
        return text, None, ""
    
    @staticmethod
    def parse_teleportation_table(table_text: str) -> List[List[str]]:
        """
        Parse the Teleportation Outcome table specifically.
        
        Format in CSV (no spaces):
        Permanent circle———01-00
        Linked object———01-00
        Very familiar01-0506-1314-2425-00
        
        Each row: Familiarity name + 4 columns (Mishap, Similar Area, Off Target, On Target)
        Each column is either "—" (N/A) or "XX-XX" (dice range)
        
        Returns:
            List of rows with proper column separation
        """
        # Define the table structure
        headers = ["Familiarity", "Mishap", "Similar Area", "Off Target", "On Target"]
        
        # Extract rows - look for familiarity types followed by dice ranges
        familiarity_types = [
            ("Permanent circle", "———01-00"),  # Pattern: 3 dashes + range
            ("Linked object", "———01-00"),
            ("Very familiar", "01-0506-1314-2425-00"),  # Pattern: 4 ranges
            ("Seen casually", "01-3334-4344-5354-00"),
            ("Viewed once or described", "01-4344-5354-7374-00"),
            ("False destination", "01-5051-00——")  # Pattern: 2 ranges + 2 dashes
        ]
        
        rows = [headers]
        
        for fam_type, expected_pattern in familiarity_types:
            # Find this familiarity type in the text
            idx = table_text.find(fam_type)
            
            if idx >= 0:
                # Extract the data after the familiarity name
                start = idx + len(fam_type)
                # Get next 20 characters (enough for 4 columns)
                data = table_text[start:start+20]
                
                # Parse the 4 columns
                columns = []
                i = 0
                
                for col_num in range(4):
                    if i >= len(data):
                        columns.append("—")
                        continue
                    
                    # Check for dash (N/A)
                    if data[i] == '—':
                        columns.append("—")
                        i += 1
                    # Check for dice range (XX-XX format)
                    elif i + 4 < len(data) and data[i:i+2].isdigit() and data[i+2] == '-' and data[i+3:i+5].isdigit():
                        columns.append(data[i:i+5])
                        i += 5
                    else:
                        # Skip unknown character
                        i += 1
                        col_num -= 1  # Retry this column
                
                # Ensure we have exactly 4 columns
                while len(columns) < 4:
                    columns.append("—")
                columns = columns[:4]
                
                rows.append([fam_type] + columns)
        
        return rows
    
    @staticmethod
    def format_table_text(table_text: str, max_width: int = 60) -> str:
        """
        Format table as readable text with proper spacing.
        
        Args:
            table_text: Raw table text
            max_width: Maximum character width
            
        Returns:
            Formatted table text
        """
        # Check if this is a Teleportation table
        if "Teleportation Outcome" in table_text or "Familiarity" in table_text:
            rows = TableFormatter.parse_teleportation_table(table_text)
        else:
            # Fallback to simple formatting
            return TableFormatter._format_simple_table(table_text, max_width)
        
        if not rows or len(rows) == 1:
            return TableFormatter._format_simple_table(table_text, max_width)
        
        # Calculate column widths based on content
        num_cols = len(rows[0])
        col_widths = [0] * num_cols
        
        for row in rows:
            for i, cell in enumerate(row):
                if i < num_cols:
                    col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Check if we need to adjust widths
        spacing = 3  # spaces between columns
        total_width = sum(col_widths) + (num_cols - 1) * spacing
        
        if total_width > max_width:
            # Need to scale down - but try to preserve important columns
            # Priority: keep data columns (dice ranges) full width, scale down text columns
            available_width = max_width - (num_cols - 1) * spacing
            
            # Identify which columns have mostly short content (dice ranges)
            short_cols = []
            for i in range(num_cols):
                max_len = max(len(str(row[i])) for row in rows)
                if max_len <= 10:  # Short columns (like "01-00")
                    short_cols.append(i)
            
            # Calculate space needed for short columns
            short_space = sum(col_widths[i] for i in short_cols)
            long_space = sum(col_widths[i] for i in range(num_cols) if i not in short_cols)
            
            # If we have space, keep short columns full width
            if short_space < available_width:
                remaining = available_width - short_space
                if long_space > 0:
                    scale = remaining / long_space
                    for i in range(num_cols):
                        if i not in short_cols:
                            col_widths[i] = max(8, int(col_widths[i] * scale))
            else:
                # Scale everything proportionally
                scale = available_width / sum(col_widths)
                col_widths = [max(5, int(w * scale)) for w in col_widths]
        
        # Format rows
        formatted_lines = []
        for i, row in enumerate(rows):
            line_parts = []
            for j, cell in enumerate(row):
                if j < num_cols:
                    cell_str = str(cell)
                    # Truncate if needed
                    if len(cell_str) > col_widths[j]:
                        cell_str = cell_str[:col_widths[j]-1] + "…"
                    line_parts.append(cell_str.ljust(col_widths[j]))
            
            formatted_lines.append("   ".join(line_parts))
            
            # Add separator after header
            if i == 0 and len(rows) > 1:
                separator = "   ".join(["─" * w for w in col_widths])
                formatted_lines.append(separator)
        
        return "\n".join(formatted_lines)
    
    @staticmethod
    def _format_simple_table(text: str, max_width: int) -> str:
        """
        Format table-like text with simple indentation and spacing.
        
        Args:
            text: Text to format
            max_width: Maximum width
            
        Returns:
            Formatted text
        """
        # Add line breaks before capital letters that start new entries
        text = re.sub(r'([a-z])([A-Z][a-z]+:)', r'\1\n  \2', text)
        
        # Add spacing around numeric ranges
        text = re.sub(r'(\d{2}-\d{2})', r' \1 ', text)
        
        # Clean up multiple spaces
        text = re.sub(r'  +', '  ', text)
        
        return text
    
    @staticmethod
    def format_description_with_table(description: str, max_width: int = 80) -> str:
        """
        Format description, detecting and formatting any tables.
        
        Args:
            description: Full spell description
            max_width: Maximum character width for table (default 80)
            
        Returns:
            Formatted description with table properly formatted
        """
        if not TableFormatter.detect_table(description):
            return description
        
        # Extract table section
        before, table, after = TableFormatter.extract_table_section(description)
        
        if table is None:
            return description
        
        # Format the table with specified width
        formatted_table = TableFormatter.format_table_text(table, max_width=max_width)
        
        # Reconstruct description
        result = before.strip()
        if result:
            result += "\n\n"
        result += formatted_table
        if after.strip():
            result += "\n\n" + after.strip()
        
        return result
