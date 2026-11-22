#!/usr/bin/env python3
"""News Image - Saturday 21 November 2026.

Draws ONE newspaper-poster PNG (1024x1024, deterministic) summing up the
world news of Saturday 21 November 2026: the date dominant at the top and
eight verified stories, each with a headline, a supporting line and a small
drawn pictogram.

Pure Python standard library only: the bitmap font below and the PNG
encoder are written from scratch in this file. No network, no external
fonts, no image libraries.

Running `python3 main.py` from any directory writes entry.png
(1024x1024, under 1 MiB) to $MAKEFUN_OUTPUT_DIR/entry.png when that
variable is set, otherwise to /output/entry.png. Two runs produce
byte-identical output.
"""

import os
import struct
import zlib

# ---------------------------------------------------------------- font ----
# 5 wide x 8 tall bitmap glyphs, drawn by hand for this poster.
# Rows 0-1 are the cap/ascender zone, rows 2-6 the x-height zone,
# row 7 the descender zone. Descenders are what make the risky letters
# unmistakable: 'y' ends in a left-hooking tail on row 7 (never a plain
# 'u'), 'g' is a closed loop with a left-curving tail on row 7 (never a
# '9', whose loop sits on rows 0-3), 'j' has its dot on row 1 and a hook
# on row 7, 'q' tails down-right, 'p' stems down-left.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001", "00000"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110", "00000"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110", "00000"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110", "00000"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111", "00000"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000", "00000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111", "00000"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001", "00000"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110", "00000"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100", "00000"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001", "00000"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111", "00000"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001", "00000"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001", "00000"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110", "00000"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000", "00000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101", "00000"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001", "00000"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110", "00000"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100", "00000"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110", "00000"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100", "00000"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010", "00000"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001", "00000"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100", "00000"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111", "00000"),
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111", "00000"),
    "b": ("10000", "10000", "11110", "10001", "10001", "10001", "11110", "00000"),
    "c": ("00000", "00000", "01110", "10001", "10000", "10001", "01110", "00000"),
    "d": ("00001", "00001", "01111", "10001", "10001", "10001", "01111", "00000"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110", "00000"),
    "f": ("00110", "01001", "01000", "11110", "01000", "01000", "01000", "00000"),
    "g": ("00000", "00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    "h": ("10000", "10000", "11110", "10001", "10001", "10001", "10001", "00000"),
    "i": ("00000", "00100", "00000", "01100", "00100", "00100", "01110", "00000"),
    "j": ("00000", "00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010", "00000"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110", "00000"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101", "00000"),
    "n": ("00000", "00000", "11110", "10001", "10001", "10001", "10001", "00000"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110", "00000"),
    "p": ("00000", "00000", "11110", "10001", "10001", "11110", "10000", "10000"),
    "q": ("00000", "00000", "01111", "10001", "10001", "01111", "00001", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000", "00000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110", "00000"),
    "t": ("00100", "00100", "11110", "00100", "00100", "00100", "00010", "00000"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10001", "01111", "00000"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100", "00000"),
    "w": ("00000", "00000", "10001", "10001", "10101", "10101", "01010", "00000"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001", "00000"),
    "y": ("00000", "00000", "10001", "10001", "10001", "01111", "00001", "01110"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111", "00000"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110", "00000"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110", "00000"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111", "00000"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110", "00000"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010", "00000"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110", "00000"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110", "00000"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000", "00000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110", "00000"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110", "00000"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100", "00000"),
    ",": ("00000", "00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "00000", "01100", "00000", "00000", "01100", "00000", "00000"),
    ";": ("00000", "00000", "01100", "00000", "01100", "00100", "01000", "00000"),
    "'": ("00000", "00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("00000", "01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000", "00000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000", "00000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010", "00000"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000", "00000"),
    "+": ("00000", "00000", "00100", "01110", "00100", "00000", "00000", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100", "00000"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100", "00000"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "*": ("00000", "00100", "10101", "01110", "10101", "00100", "00000", "00000"),
}

# ---------------------------------------------------------------- canvas --
W, H = 1024, 1024
PAPER = (251, 246, 233)   # warm newsprint
INK = (27, 27, 27)       # near-black
RED = (178, 38, 30)      # masthead accent
BLUE = (31, 58, 95)      # number blocks
GREY = (74, 74, 74)      # supporting lines
LIGHT_GREY = (190, 182, 168)  # dividers


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def fill_rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def hline(self, x, y, w, color, thick=1):
        self.fill_rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.fill_rect(x, y, thick, h, color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.fill_rect(x0, y0, thick, thick, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def polyline(self, points, color, thick=1):
        for (x0, y0), (x1, y1) in zip(points, points[1:]):
            self.line(x0, y0, x1, y1, color, thick)

    def circle(self, cx, cy, r, color, thick=2, fill=False):
        import math
        if fill:
            for yy in range(-r, r + 1):
                half = int(math.sqrt(max(0, r * r - yy * yy)))
                self.fill_rect(cx - half, cy + yy, 2 * half + 1, 1, color)
            return
        steps = max(24, 8 * r)
        pts = []
        for k in range(steps + 1):
            a = 2 * math.pi * k / steps
            pts.append((int(cx + r * math.cos(a)), int(cy + r * math.sin(a))))
        self.polyline(pts, color, thick)

    def ellipse(self, cx, cy, rx, ry, color, thick=2):
        import math
        steps = max(24, 8 * max(rx, ry))
        pts = []
        for k in range(steps + 1):
            a = 2 * math.pi * k / steps
            pts.append((int(cx + rx * math.cos(a)), int(cy + ry * math.sin(a))))
        self.polyline(pts, color, thick)


# ------------------------------------------------------------------ text --
def text_width(text, scale):
    return len(text) * 6 * scale


def draw_text(cv, text, x, y, scale, color):
    for ci, ch in enumerate(text):
        glyph = FONT.get(ch)
        if glyph is None:
            continue
        ox = x + ci * 6 * scale
        for gy, row in enumerate(glyph):
            for gx, bit in enumerate(row):
                if bit == "1":
                    cv.fill_rect(ox + gx * scale, y + gy * scale,
                                 scale, scale, color)


def draw_text_centered(cv, text, cx, y, scale, color):
    draw_text(cv, text, cx - text_width(text, scale) // 2, y, scale, color)


def wrap_text(text, max_width, scale):
    """Greedy word wrap; returns a list of lines that fit max_width px."""
    words = text.split(" ")
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# -------------------------------------------------------------- pictograms -
def pictogram(cv, idx, px, py):
    """One small drawn motif per story, inside a 56x56 box at (px, py)."""
    cx, cy = px + 28, py + 28
    if idx == 0:  # jail bars: cartel boss captured
        cv.fill_rect(px + 4, py + 6, 48, 44, INK)
        for bx in (px + 12, px + 26, px + 40):
            cv.vline(bx, py + 6, 44, PAPER, 4)
    elif idx == 1:  # globe: climate talks
        cv.circle(cx, cy, 22, BLUE, 3)
        cv.hline(px + 8, cy, 40, BLUE, 2)
        cv.ellipse(cx, cy, 10, 22, BLUE, 2)
    elif idx == 2:  # blast burst: missile strike
        for ang in range(0, 360, 30):
            import math
            a = math.radians(ang)
            r0, r1 = 8, 26
            cv.line(int(cx + r0 * math.cos(a)), int(cy + r0 * math.sin(a)),
                    int(cx + r1 * math.cos(a)), int(cy + r1 * math.sin(a)),
                    RED, 3)
        cv.circle(cx, cy, 6, RED, 2, fill=True)
    elif idx == 3:  # falling chart: market sell-off
        cv.polyline([(px + 6, py + 12), (px + 20, py + 18), (px + 30, py + 30),
                     (px + 44, py + 44)], RED, 4)
        cv.line(px + 44, py + 44, px + 34, py + 44, RED, 4)
        cv.line(px + 44, py + 44, px + 44, py + 34, RED, 4)
    elif idx == 4:  # seismic zigzag: earthquake
        cv.polyline([(px + 4, cy), (px + 12, cy - 8), (px + 18, cy + 10),
                     (px + 24, cy - 16), (px + 30, cy + 14), (px + 38, cy - 6),
                     (px + 52, cy)], INK, 3)
    elif idx == 5:  # mosquito: wings + body
        cv.ellipse(cx - 12, cy - 10, 12, 5, BLUE, 2)
        cv.ellipse(cx + 12, cy - 10, 12, 5, BLUE, 2)
        cv.line(cx, cy - 8, cx, cy + 18, INK, 4)
        cv.line(cx - 10, cy + 4, cx - 20, cy + 14, INK, 2)
        cv.line(cx + 10, cy + 4, cx + 20, cy + 14, INK, 2)
    elif idx == 6:  # ringed planet: Mercury orbit
        cv.circle(cx, cy, 14, BLUE, 3, fill=True)
        cv.ellipse(cx, cy, 26, 9, RED, 3)
    else:  # tanker on waves: Strait of Hormuz
        cv.fill_rect(px + 6, py + 16, 44, 12, INK)
        cv.fill_rect(px + 14, py + 6, 12, 10, INK)
        cv.fill_rect(px + 32, py + 10, 8, 6, INK)
        cv.polyline([(px + 4, py + 40), (px + 14, py + 34), (px + 24, py + 40),
                     (px + 34, py + 34), (px + 44, py + 40), (px + 52, py + 34)],
                    BLUE, 3)


# --------------------------------------------------------------- content ---
STORIES = [
    ("Mexico captures 'El Chapo Isidro'",
     "FBI top-10 fugitive Fausto Isidro Meza Flores seized in Sinaloa with US help."),
    ("COP31 talks run into overtime",
     "No deal yet in Antalya as fossil fuels and climate finance divide nations."),
    ("Russian 'double-tap' strike hits Kryvyi Rih",
     "2 killed, 60 wounded and 25 apartment blocks damaged in Zelenskyy's hometown."),
    ("Wall Street plunges in AI sell-off",
     "S&P 500 down 3.7% into correction; Nasdaq erases all 2026 gains; Nvidia -14%."),
    ("Magnitude 6.9 quake shakes Peru",
     "Andean tremor near Junin felt in Lima; no casualties or damage reported at first."),
    ("Mosquito trial cuts dengue by 69%",
     "Wolbachia mosquitoes protect schoolchildren in Belo Horizonte, Brazil, over four years."),
    ("BepiColombo enters orbit at Mercury",
     "ESA/JAXA probe arrives after an eight-year journey; two orbiters split in December."),
    ("Two tankers hit near Strait of Hormuz",
     "Projectiles strike off Khasab, Oman; Iran says one tanker hit a mine and caught fire."),
]


def build():
    cv = Canvas(W, H, PAPER)

    # Masthead.
    draw_text_centered(cv, "THE WORLD IN ONE IMAGE", W // 2, 26, 2, RED)
    draw_text_centered(cv, "Saturday 21 November 2026", W // 2, 58, 6, INK)
    cv.hline(44, 122, W - 88, RED, 4)
    cv.hline(44, 130, W - 88, RED, 2)
    draw_text_centered(cv, "EIGHT STORIES FROM AROUND THE GLOBE",
                       W // 2, 142, 2, INK)

    # Story blocks.
    top = 168
    block_h, gap = 98, 4
    text_x = 116
    text_w = 812  # text ends at x=928; pictograms live at x=936..996
    for i, (headline, support) in enumerate(STORIES):
        y = top + i * (block_h + gap)
        # Number block.
        cv.fill_rect(44, y + 8, 56, 56, BLUE)
        draw_text_centered(cv, str(i + 1), 44 + 28, y + 16, 4, PAPER)
        # Headline (one line) + supporting lines (wrapped, up to two).
        draw_text(cv, headline, text_x, y + 10, 3, INK)
        lines = wrap_text(support, text_w, 2)
        for li, line in enumerate(lines[:2]):
            draw_text(cv, line, text_x, y + 44 + li * 18, 2, GREY)
        # Pictogram at the right.
        pictogram(cv, i, 940, y + 21)
        # Divider (except after the last block).
        if i < len(STORIES) - 1:
            cv.hline(44, y + block_h, W - 88, LIGHT_GREY, 2)

    # Footer.
    draw_text_centered(cv, "Every story verified in at least two news sources.",
                       W // 2, 988, 2, GREY)
    return cv


# -------------------------------------------------------------- PNG write --
def chunk(ctype, data):
    out = struct.pack(">I", len(data)) + ctype + data
    out += struct.pack(">I", zlib.crc32(ctype + data) & 0xFFFFFFFF)
    return out


def encode_png(cv):
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    for yy in range(cv.h):
        raw.append(0)  # filter: none
        i = (yy * cv.w) * 3
        raw += cv.px[i:i + cv.w * 3]
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    return png


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.png")


def main():
    png = encode_png(build())
    path = output_path()
    with open(path, "wb") as f:
        f.write(png)
    print("wrote %s (%d bytes)" % (path, len(png)))


if __name__ == "__main__":
    main()
