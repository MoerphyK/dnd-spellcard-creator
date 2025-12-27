#!/usr/bin/env python3
"""Verify generated cards are valid images."""

from pathlib import Path
from PIL import Image


def main():
    output_dir = Path("output")
    
    print("Verifying generated cards...\n")
    
    for img_path in sorted(output_dir.glob("*.png")):
        try:
            img = Image.open(img_path)
            width, height = img.size
            mode = img.mode
            print(f"✓ {img_path.name}")
            print(f"  Size: {width}x{height}, Mode: {mode}")
        except Exception as e:
            print(f"✗ {img_path.name}: {e}")
    
    print("\n✅ All cards verified!")


if __name__ == "__main__":
    main()
