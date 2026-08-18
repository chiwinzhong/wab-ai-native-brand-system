#!/usr/bin/env python3
"""Create the square Skill icon from the approved full WIN wordmark."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "wab-diagnose-brand" / "assets" / "win-logo-black.png"
OUTPUT = ROOT / "skills" / "wab-diagnose-brand" / "assets" / "win-logo-square.png"
SIZE = 400
BACKGROUND = (245, 245, 243, 255)


def main():
    logo = Image.open(SOURCE).convert("RGBA")
    logo.thumbnail((320, 150), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (SIZE, SIZE), BACKGROUND)
    x = (SIZE - logo.width) // 2
    y = (SIZE - logo.height) // 2
    canvas.alpha_composite(logo, (x, y))
    canvas.convert("RGB").save(OUTPUT, format="PNG", optimize=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
