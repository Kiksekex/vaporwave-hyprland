#!/usr/bin/env python3
"""
Vaporwave / Synthwave wallpaper generator for Hyprland rice.
Generates a 2560x1440 wallpaper with full synthwave scene.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random
import os

W, H = 2560, 1440

# ── Palette ───────────────────────────────────────────────────────────────────
BG          = (13,   2,  33)        # near-black indigo
HORIZON     = (45,   0,  80)        # deep purple horizon
SUN_OUTER   = (255,  42, 109)       # hot pink
SUN_INNER   = (255, 113, 206)       # soft pink
SUN_MID     = (255, 200,  80)       # gold band
GRID_COLOR  = (5,   217, 232)       # cyan grid
GRID_DIM    = (2,    80, 100)       # dim cyan
MOUNTAIN_L  = (123,  47, 255)       # violet mountain
MOUNTAIN_R  = (255,  42, 109)       # pink mountain
STAR_COLOR  = (255, 255, 255)
GLOW_CYAN   = (5,   217, 232)
GLOW_PINK   = (255,  42, 109)
GLOW_PURPLE = (180,  60, 255)


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def draw_gradient_sky(img):
    draw = ImageDraw.Draw(img)
    HORIZON_Y = int(H * 0.52)
    for y in range(HORIZON_Y):
        t = y / HORIZON_Y
        # top → deep indigo, bottom → dark purple near horizon
        c = lerp_color((8, 0, 22), (55, 0, 88), t)
        draw.line([(0, y), (W, y)], fill=c)


def draw_stars(img):
    draw = ImageDraw.Draw(img)
    rng = random.Random(42)
    HORIZON_Y = int(H * 0.50)
    for _ in range(420):
        x = rng.randint(0, W)
        y = rng.randint(0, HORIZON_Y - 20)
        size = rng.choice([1, 1, 1, 2, 2, 3])
        alpha = rng.randint(140, 255)
        hue = rng.choice([STAR_COLOR, GLOW_CYAN, SUN_INNER, (200, 180, 255)])
        draw.ellipse([x - size, y - size, x + size, y + size],
                     fill=(*hue, alpha))


def draw_sun(img):
    """Retro segmented sun."""
    cx = W // 2
    HORIZON_Y = int(H * 0.52)
    sun_r = int(H * 0.22)
    cy = HORIZON_Y

    sun_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sun_layer)

    # outer glow
    for g in range(60, 0, -1):
        alpha = int(18 * (1 - g / 60))
        gr = sun_r + g * 3
        sd.ellipse([cx - gr, cy - gr, cx + gr, cy + gr],
                   fill=(*SUN_OUTER, alpha))

    # gradient sun body – horizontal stripes
    num_stripes = 18
    stripe_colors = []
    for i in range(num_stripes):
        t = i / (num_stripes - 1)
        if t < 0.5:
            c = lerp_color(SUN_INNER, SUN_MID, t * 2)
        else:
            c = lerp_color(SUN_MID, SUN_OUTER, (t - 0.5) * 2)
        stripe_colors.append(c)

    for i, color in enumerate(stripe_colors):
        sy = cy - sun_r + i * (sun_r * 2 // num_stripes)
        ey = sy + (sun_r * 2 // num_stripes)
        # clip to circle
        for y in range(sy, ey):
            dy = y - cy
            if abs(dy) > sun_r:
                continue
            half_w = int(math.sqrt(max(0, sun_r * sun_r - dy * dy)))
            sd.line([(cx - half_w, y), (cx + half_w, y)], fill=(*color, 255))

    # horizontal gap lines (retro sun bands) – lower half only
    gap_thickness = max(2, sun_r // 30)
    num_gaps = 8
    for i in range(num_gaps):
        frac = i / num_gaps
        y = cy + int(frac * sun_r)
        if y + gap_thickness <= cy + sun_r:
            dy = y - cy
            half_w = int(math.sqrt(max(0, sun_r * sun_r - dy * dy)))
            sd.rectangle([cx - half_w, y, cx + half_w, y + gap_thickness],
                         fill=(13, 2, 33, 255))

    # horizon clip – mask bottom half below horizon
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([cx - sun_r, cy - sun_r, cx + sun_r, cy + sun_r], fill=255)
    md.rectangle([0, HORIZON_Y, W, H], fill=0)
    sun_layer.putalpha(mask)

    img.paste(sun_layer, mask=sun_layer.split()[3])


def draw_mountains(img):
    draw = ImageDraw.Draw(img)
    HORIZON_Y = int(H * 0.52)

    def mountain_range(peaks, color, glow_color, offset_y=0):
        pts = [(0, HORIZON_Y + offset_y)]
        for px, py in peaks:
            pts.append((px, py + offset_y))
        pts.append((W, HORIZON_Y + offset_y))
        pts.append((W, HORIZON_Y))
        pts.append((0, HORIZON_Y))
        draw.polygon(pts, fill=color)

        # ridge glow
        edge_pts = [(0, HORIZON_Y + offset_y)] + [(px, py + offset_y) for px, py in peaks] + [(W, HORIZON_Y + offset_y)]
        for t in range(6, 0, -1):
            alpha = 60 - t * 8
            shifted = [(x, y - t) for x, y in edge_pts]
            draw.line(shifted, fill=(*glow_color, alpha), width=2)

    peaks_left = [
        (0, HORIZON_Y - 10),
        (120, HORIZON_Y - 120),
        (300, HORIZON_Y - 260),
        (480, HORIZON_Y - 180),
        (600, HORIZON_Y - 310),
        (750, HORIZON_Y - 200),
        (850, HORIZON_Y - 80),
        (W // 2 - 320, HORIZON_Y),
    ]

    peaks_right = [
        (W // 2 + 320, HORIZON_Y),
        (W - 850, HORIZON_Y - 80),
        (W - 750, HORIZON_Y - 200),
        (W - 600, HORIZON_Y - 310),
        (W - 480, HORIZON_Y - 180),
        (W - 300, HORIZON_Y - 260),
        (W - 120, HORIZON_Y - 120),
        (W, HORIZON_Y - 10),
    ]

    mountain_range(peaks_left,  (20, 0, 45), MOUNTAIN_L)
    mountain_range(peaks_right, (20, 0, 45), MOUNTAIN_R)
    mountain_range(peaks_left,  (35, 0, 65), MOUNTAIN_L, offset_y=30)
    mountain_range(peaks_right, (35, 0, 65), MOUNTAIN_R, offset_y=30)


def draw_grid_floor(img):
    HORIZON_Y = int(H * 0.52)
    floor_h = H - HORIZON_Y

    grid_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid_layer)

    # floor background gradient
    for y in range(HORIZON_Y, H):
        t = (y - HORIZON_Y) / floor_h
        c = lerp_color((30, 0, 60), (8, 0, 20), t)
        gd.line([(0, y), (W, y)], fill=(*c, 255))

    # perspective grid – vertical lines converge to vanishing point
    vp_x = W // 2
    vp_y = HORIZON_Y
    num_v = 28
    for i in range(-num_v // 2, num_v // 2 + 1):
        floor_x = W // 2 + i * (W // num_v)
        t_dist = abs(i) / (num_v / 2)
        alpha = int(200 - t_dist * 140)
        gd.line([(vp_x, vp_y), (floor_x, H)],
                fill=(*GRID_COLOR, alpha), width=1)

    # horizontal lines with perspective spacing
    num_h = 20
    for i in range(1, num_h + 1):
        t = (i / num_h) ** 1.8          # perspective curve
        y = int(HORIZON_Y + t * floor_h)
        t_fade = i / num_h
        alpha = int(180 * t_fade)
        gd.line([(0, y), (W, y)], fill=(*GRID_COLOR, alpha), width=1)

    # horizon glow line
    for g in range(12, 0, -1):
        a = int(80 * (1 - g / 12))
        gd.line([(0, HORIZON_Y + g), (W, HORIZON_Y + g)],
                fill=(*GLOW_PINK, a), width=1)
        gd.line([(0, HORIZON_Y - g), (W, HORIZON_Y - g)],
                fill=(*GLOW_CYAN, a), width=1)

    img.paste(grid_layer, mask=grid_layer.split()[3])


def draw_scanlines(img):
    """Subtle CRT scanlines overlay."""
    ol = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ol)
    for y in range(0, H, 3):
        od.line([(0, y), (W, y)], fill=(0, 0, 0, 18))
    img.paste(ol, mask=ol.split()[3])


def draw_vignette(img):
    vl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vl)
    steps = 80
    for i in range(steps, 0, -1):
        t = i / steps
        alpha = int(160 * (t ** 2.2))
        margin = int(i * 12)
        if margin * 2 < W and margin * 2 < H:
            vd.rectangle([margin, margin, W - margin, H - margin],
                         outline=(0, 0, 0, alpha), width=1)
    img.paste(vl, mask=vl.split()[3])


def draw_neon_text(img):
    """VAPOR WAVE title text with glow."""
    draw = ImageDraw.Draw(img)
    HORIZON_Y = int(H * 0.52)

    # Try to load a font, fall back to default
    font_size_title = 110
    font_size_sub = 38
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size_title)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size_sub)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = font_title

    title = "V A P O R W A V E"
    subtitle = "─── s y n t h w a v e  e d i t i o n ───"

    # measure
    try:
        bb = font_title.getbbox(title)
        tw = bb[2] - bb[0]
    except Exception:
        tw = len(title) * 60
    tx = (W - tw) // 2
    ty = int(HORIZON_Y * 0.28)

    # glow layers
    for g in range(20, 0, -1):
        a = int(22 * (1 - g / 20))
        draw.text((tx - g, ty), title, font=font_title, fill=(*GLOW_CYAN, a))
        draw.text((tx + g, ty), title, font=font_title, fill=(*GLOW_PINK, a))

    # main text – gradient simulation (pink → cyan)
    steps = font_size_title
    for line_y in range(ty, ty + steps):
        t = (line_y - ty) / steps
        c = lerp_color(SUN_INNER, GLOW_CYAN, t)
        draw.text((tx, line_y), title, font=font_title, fill=(*c, 255))

    # subtitle
    try:
        bb2 = font_sub.getbbox(subtitle)
        sw = bb2[2] - bb2[0]
    except Exception:
        sw = len(subtitle) * 22
    sx = (W - sw) // 2
    sy = ty + font_size_title + 18
    for g in range(8, 0, -1):
        a = int(30 * (1 - g / 8))
        draw.text((sx, sy - g), subtitle, font=font_sub,
                  fill=(*GLOW_PURPLE, a))
    draw.text((sx, sy), subtitle, font=font_sub, fill=(*GLOW_PURPLE, 220))


def main():
    print("Generating vaporwave wallpaper (2560×1440)…")
    img = Image.new("RGB", (W, H), BG)

    draw_gradient_sky(img)
    draw_stars(img)
    draw_sun(img)
    draw_mountains(img)
    draw_grid_floor(img)
    draw_neon_text(img)
    draw_scanlines(img)
    draw_vignette(img)

    # slight glow bloom via blur overlay
    bloom = img.copy().filter(ImageFilter.GaussianBlur(radius=4))
    bloom = bloom.point(lambda p: int(p * 0.18))
    img = Image.blend(img, bloom, 0.35)

    out = os.path.join(os.path.dirname(__file__), "vaporwave.png")
    img.save(out, "PNG")
    print(f"Saved → {out}")


if __name__ == "__main__":
    main()
