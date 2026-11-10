#!/usr/bin/env python3
"""Auto Master Drive — locked thumbnail template (PIL, no paid tools).

Style lock (channel rule, proven by the Nov 2/3/5/6 thumbnail fixes):
  * Canvas 1920x1080 (16:9).
  * Headline rendered by PIL at the BOTTOM (top quarter stays empty),
    white bold with a black outline — never baked into the AI base image.
  * Optional big YELLOW number line above the headline (range / price / hp).
  * Optional small subline above the number (e.g. "CYBERTRUCK vs RIVIAN R1T").
  * Real AMD logo top-right on a white rounded backing (19% width, 2% margin).
  * Subtle dark gradient over the bottom band so text stays readable on any base.

Usage:
  python3 amd_thumbnail.py --base scene.jpg --headline "ENDS IN 2027" \
      --number "420 VS 320" --subline "CYBERTRUCK vs RIVIAN R1T" \
      --out thumbnail.png
  python3 amd_thumbnail.py --base scene.jpg --headline "420 VS 320" \
      --out thumbnail-alt.png

The base image must NOT already contain headline text — the template renders
all text itself. Use a clean scene still as --base.
"""
import argparse
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
LOGO_PATH = "/home/hatch/workspace/ak-autocore/brand/amd-logo-top.png"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
YELLOW = (255, 214, 10)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def load_font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def wrap_text(draw, text, font, max_width):
    """Split text into lines that fit max_width. Returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, text, max_width, start_size, min_size=40):
    """Largest bold font size (<= start_size) whose wrapped text is <= 2 lines."""
    size = start_size
    while size > min_size:
        font = load_font(size)
        if len(wrap_text(draw, text, font, max_width)) <= 2:
            return font
        size -= 6
    return load_font(min_size)


def bottom_gradient(im):
    """Darken the bottom band with a smooth vertical gradient (PIL only)."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    band_top = int(H * 0.58)
    for y in range(band_top, H):
        alpha = int(150 * (y - band_top) / (H - band_top))
        d.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
    im.alpha_composite(overlay)
    return im


def draw_subline_top_left(draw, text):
    """Small subline at the TOP-LEFT (top-right is the logo's corner).

    The bottom text stack (number + headline) must never cross the subject
    cars, so the subline lives up here, clear of the logo.
    """
    font = fit_font(draw, text, W // 2, 54)
    lines = wrap_text(draw, text, font, W // 2)
    y = 28
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=max(2, font.size // 18))
        draw.text((28 - bbox[0], y - bbox[1]), line, font=font, fill=WHITE,
                  stroke_width=max(2, font.size // 18), stroke_fill=BLACK)
        y += (bbox[3] - bbox[1]) + 8


def draw_centered_block(draw, lines, font, fill, bottom_y, line_gap=12):
    """Draw wrapped lines centered, ending at bottom_y (baseline of last line)."""
    total_h = 0
    heights = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=max(2, font.size // 18))
        h = bbox[3] - bbox[1]
        heights.append(h)
        total_h += h
    total_h += line_gap * (len(lines) - 1)
    y = bottom_y - total_h
    for line, h in zip(lines, heights):
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=max(2, font.size // 18))
        lw = bbox[2] - bbox[0]
        x = (W - lw) // 2 - bbox[0]
        draw.text((x, y - bbox[1]), line, font=font, fill=fill,
                  stroke_width=max(2, font.size // 18), stroke_fill=BLACK)
        y += h + line_gap
    return bottom_y - total_h  # top of the block


def paste_logo(im):
    """Real AMD logo, top-right, white rounded backing (proven recipe)."""
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo.thumbnail((300, 300), Image.LANCZOS)
    lw, lh = logo.size
    pad, m = 14, 20
    bg = Image.new("RGBA", (lw + 2 * pad, lh + 2 * pad), (255, 255, 255, 235))
    mask = Image.new("L", bg.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, bg.size[0] - 1, bg.size[1] - 1],
                                           radius=16, fill=255)
    bx, by = W - m - bg.size[0], m
    im.paste(bg, (bx, by), mask)
    im.paste(logo, (bx + pad, by + pad), logo)
    return im


def build(base_path, headline, number=None, subline=None, out_path="thumbnail.png"):
    im = Image.open(base_path).convert("RGB")
    w, h = im.size
    if w / h > 16 / 9:
        nw = int(h * 16 / 9)
        x = (w - nw) // 2
        im = im.crop((x, 0, x + nw, h))
    else:
        nh = int(w / (16 / 9))
        y = (h - nh) // 2
        im = im.crop((0, y, w, y + nh))
    im = im.resize((W, H), Image.LANCZOS).convert("RGBA")
    im = bottom_gradient(im)
    draw = ImageDraw.Draw(im)
    margin = 90
    max_w = W - 2 * margin
    cursor = H - 70  # bottom edge for the headline block

    head_font = fit_font(draw, headline, max_w, 150)
    head_lines = wrap_text(draw, headline, head_font, max_w)
    top = draw_centered_block(draw, head_lines, head_font, WHITE, cursor)

    if number:
        num_font = fit_font(draw, number, max_w, 175)
        num_lines = wrap_text(draw, number, num_font, max_w)
        top = draw_centered_block(draw, num_lines, num_font, YELLOW, top - 24)

    if subline:
        draw_subline_top_left(draw, subline)

    im = paste_logo(im)
    im.convert("RGB").save(out_path)
    print(out_path, im.size)
    return out_path


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="AMD locked thumbnail template")
    p.add_argument("--base", required=True, help="clean scene still (no baked text)")
    p.add_argument("--headline", required=True, help="main line, rendered at bottom")
    p.add_argument("--number", default=None, help="optional yellow big-number line")
    p.add_argument("--subline", default=None, help="optional small line above number")
    p.add_argument("--out", required=True, help="output PNG path")
    a = p.parse_args()
    build(a.base, a.headline, a.number, a.subline, a.out)
