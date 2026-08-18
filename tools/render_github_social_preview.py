#!/usr/bin/env python3
"""Render the WAB GitHub social-preview asset from approved brand files."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "github-social-preview.png"
SQUARE_LOGO = ROOT / "skills" / "wab-diagnose-brand" / "assets" / "win-logo-square.png"
LOGO = ROOT / "skills" / "wab-diagnose-brand" / "assets" / "win-logo-black.png"

WIDTH, HEIGHT = 1280, 640
BLACK = "#0A0A0A"
WHITE = "#FFFFFF"
FOG = "#F5F5F3"
TITANIUM = "#E7E2DC"
GRAY = "#6E6E73"
REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size=size)


def fit_contain(image, box):
    target_width, target_height = box
    source = image.copy()
    source.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
    return source


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas = Image.new("RGB", (WIDTH, HEIGHT), FOG)
    draw = ImageDraw.Draw(canvas)

    draw.rounded_rectangle((24, 24, WIDTH - 24, HEIGHT - 24), radius=28, outline=BLACK, width=2)

    pill = (72, 58, 420, 96)
    draw.rounded_rectangle(pill, radius=19, fill=BLACK)
    draw.text((91, 69), "OPEN AGENT SKILL  /  PUBLIC PREVIEW", font=font(BOLD, 15), fill=WHITE)

    draw.text((68, 126), "WAB", font=font(BOLD, 108), fill=BLACK, stroke_width=1)
    draw.text((74, 248), "AI-NATIVE BRAND SYSTEM", font=font(BOLD, 38), fill=BLACK)
    draw.line((74, 310, 716, 310), fill=BLACK, width=3)
    draw.text((74, 338), "Make brand judgment", font=font(REGULAR, 37), fill=BLACK)
    draw.text((74, 381), "executable.", font=font(BOLD, 37), fill=BLACK)

    draw.text((74, 476), "EVIDENCE-AWARE", font=font(BOLD, 16), fill=GRAY)
    draw.text((274, 476), "DECISION-FIRST", font=font(BOLD, 16), fill=GRAY)
    draw.text((455, 476), "HUMAN-GOVERNED", font=font(BOLD, 16), fill=GRAY)

    panel = (790, 52, 1204, 588)
    draw.rounded_rectangle(panel, radius=24, fill=TITANIUM)

    square_logo = Image.open(SQUARE_LOGO).convert("RGBA")
    square_logo = fit_contain(square_logo, (182, 182))
    canvas.paste(square_logo.convert("RGB"), (906, 88))

    steps = [
        ("01", "EVIDENCE"),
        ("02", "JUDGMENT"),
        ("03", "GOVERNED ACTION"),
    ]
    y_values = [318, 396, 474]
    draw.line((856, y_values[0] + 18, 856, y_values[-1] + 18), fill=BLACK, width=2)
    for (number, label), y in zip(steps, y_values):
        draw.ellipse((846, y + 8, 866, y + 28), fill=BLACK)
        draw.text((887, y), number, font=font(BOLD, 18), fill=GRAY)
        draw.text((927, y - 1), label, font=font(BOLD, 21), fill=BLACK)

    logo = Image.open(LOGO).convert("RGBA")
    logo = fit_contain(logo, (112, 43))
    canvas.paste(logo, (74, 539), logo)
    draw.text((210, 549), "W AI BRANDING", font=font(BOLD, 17), fill=BLACK)
    draw.text((613, 552), "github.com", font=font(REGULAR, 15), fill=GRAY)

    canvas.save(OUTPUT, format="PNG", optimize=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
