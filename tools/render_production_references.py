#!/usr/bin/env python3
"""Draw original, explicitly fictional layout references. Requires Pillow; no network."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "skills/wab-diagnose-brand/assets/production"
INK, PAPER, ACCENT, PALE, MUTED = "#24211F", "#F4EFE7", "#8C4C35", "#E7DED1", "#6E655C"


def font(size, bold=False):
    names = ["DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
             "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def words(draw, text, xy, size=22, color=INK, bold=False):
    draw.text(xy, text, fill=color, font=font(size, bold), spacing=10)


def ceramics(draw, x, y, scale=1, cup=ACCENT):
    def b(coords):
        return tuple(int((v * scale) + (x if i % 2 == 0 else y)) for i, v in enumerate(coords))
    draw.ellipse(b((0, 105, 245, 185)), fill="#C6B39A")
    draw.ellipse(b((8, 86, 237, 155)), fill="#F7F1E8", outline="#A5917B", width=max(1, int(3 * scale)))
    draw.ellipse(b((47, 99, 197, 141)), fill="#DED1BF")
    draw.ellipse(b((285, 132, 505, 188)), fill="#B5A18A")
    draw.pieslice(b((280, -10, 512, 185)), 0, 180, fill="#B99B7B")
    draw.ellipse(b((280, 50, 512, 118)), fill="#E8DAC7", outline="#8C6F56", width=max(1, int(3 * scale)))
    draw.ellipse(b((310, 62, 480, 104)), fill="#9B7A5E")
    draw.ellipse(b((633, 58, 737, 153)), outline=cup, width=max(2, int(18 * scale)))
    draw.rounded_rectangle(b((575, 22, 675, 171)), radius=max(1, int(18 * scale)), fill=cup)
    draw.ellipse(b((575, 16, 675, 49)), fill="#BE8A6F")
    draw.ellipse(b((590, 23, 660, 41)), fill="#5F3528")


def save(image, name):
    OUT.mkdir(parents=True, exist_ok=True)
    image.save(OUT / name, optimize=True)
    print(OUT / name)


def desktop():
    im = Image.new("RGB", (1400, 900), PAPER); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1400, 37), fill=INK)
    words(d, "SYNTHETIC LAYOUT ILLUSTRATION / NOT A CLIENT WEBSITE OR SCREENSHOT", (35, 10), 14, PAPER)
    words(d, "Harbor Kiln", (55, 68), 32, bold=True)
    words(d, "COLLECTION     APPROACH     EVIDENCE", (858, 80), 16)
    d.line((55, 134, 1345, 134), fill="#BFB3A3", width=1)
    words(d, "A TABLEWARE STORY", (55, 195), 17, ACCENT, True)
    words(d, "Worth\ninspecting.", (55, 241), 81, bold=True)
    words(d, "Start with a real buyer question,\nthen show what the evidence can carry.", (60, 460), 23, MUTED)
    d.rectangle((60, 565, 360, 624), fill=ACCENT); words(d, "REVIEW THE COLLECTION", (85, 584), 16, PAPER, True)
    d.rectangle((710, 190, 1345, 647), fill=PALE); ceramics(d, 730, 365, .80)
    words(d, "ORIGINAL FICTIONAL CERAMIC FORMS", (741, 600), 14, MUTED)
    d.line((55, 713, 1345, 713), fill="#BFB3A3")
    words(d, "01 / THE QUESTION", (60, 752), 16, ACCENT, True)
    words(d, "What needs to stay consistent?", (60, 788), 34, bold=True)
    words(d, "Draft copy. No performance claims.", (865, 797), 19, MUTED)
    save(im, "website-desktop-reference.png")


def mobile():
    im = Image.new("RGB", (780, 1300), "#DDD3C6"); d = ImageDraw.Draw(im)
    d.rounded_rectangle((165, 40, 615, 1238), radius=40, fill=INK)
    d.rounded_rectangle((180, 55, 600, 1223), radius=28, fill=PAPER)
    d.rounded_rectangle((318, 63, 462, 81), radius=9, fill=INK)
    words(d, "Harbor Kiln", (204, 115), 25, bold=True); words(d, "MENU +", (507, 124), 13)
    d.line((205, 174, 575, 174), fill="#BFB3A3")
    words(d, "FICTIONAL BRAND / REVIEW", (206, 214), 12, ACCENT, True)
    words(d, "Worth\ninspecting.", (203, 258), 54, bold=True)
    words(d, "A clear buyer question.\nA proportionate promise.", (207, 420), 20, MUTED)
    d.rectangle((207, 510, 542, 569), fill=ACCENT); words(d, "REVIEW THE COLLECTION", (225, 530), 14, PAPER, True)
    d.rectangle((204, 625, 576, 920), fill=PALE); ceramics(d, 216, 710, .47)
    words(d, "FICTIONAL CERAMIC STUDY", (226, 870), 12, MUTED)
    words(d, "What the image\ncannot prove.", (207, 964), 33, bold=True)
    words(d, "Add approved product evidence\nbefore making real claims.", (207, 1073), 17, MUTED)
    words(d, "SYNTHETIC LAYOUT / NOT A SCREENSHOT", (180, 1265), 14)
    save(im, "website-mobile-reference.png")


def cover():
    im = Image.new("RGB", (900, 1200), ACCENT); d = ImageDraw.Draw(im)
    words(d, "HARBOR NOTES", (65, 61), 31, PAPER, True)
    words(d, "FICTIONAL EDITORIAL STUDY", (66, 113), 16, "#EBD5C8")
    d.line((65, 160, 835, 160), fill="#BD8B73", width=2)
    words(d, "At the\ntable.", (56, 204), 115, PAPER, True)
    ceramics(d, 83, 612, 1.00, cup="#C6B39A")
    words(d, "A question. A material.\nA visible evidence boundary.", (65, 924), 28, PAPER)
    words(d, "DEMONSTRATION ONLY / NOT A RELEASED MAGAZINE", (65, 1131), 17, "#EBD5C8")
    save(im, "magazine-cover-reference.png")


def spread():
    im = Image.new("RGB", (1600, 1050), "#D5CBBD"); d = ImageDraw.Draw(im)
    d.rectangle((39, 38, 1561, 1007), fill=PAPER); d.line((800, 38, 800, 1007), fill="#C1B4A2", width=3)
    words(d, "HARBOR NOTES / FICTIONAL FEATURE", (87, 80), 16, ACCENT, True)
    words(d, "Begin with\nthe working\ntable.", (84, 155), 66, bold=True)
    words(d, "An editorial angle, not an invented\ninterview or an unsupported result.", (88, 429), 24, MUTED)
    d.rectangle((87, 555, 718, 879), fill=PALE); ceramics(d, 98, 648, .79)
    words(d, "WHAT THE IMAGE CANNOT PROVE", (853, 86), 16, ACCENT, True)
    words(d, "Make room\nfor evidence.", (851, 151), 53, bold=True)
    y = 345
    for title, body in [("01 / SOURCES", "Names, facts, quotes and dates need a source."), ("02 / RIGHTS", "A credit is not a license to reproduce."), ("03 / REVIEW", "Editorial, design and release are separate."), ("04 / PRODUCTION", "Screen proofs are not press-ready files.")]:
        d.line((854, y - 15, 1508, y - 15), fill="#C1B4A2")
        words(d, title, (854, y + 8), 17, ACCENT, True); words(d, body, (854, y + 48), 20, MUTED); y += 130
    words(d, "03 / ORIGINAL LAYOUT ILLUSTRATION", (87, 958), 14, MUTED)
    words(d, "NOT A REAL PUBLICATION OR CUSTOMER CASE / 04", (1079, 958), 14, MUTED)
    save(im, "magazine-spread-reference.png")


if __name__ == "__main__":
    desktop(); mobile(); cover(); spread()
