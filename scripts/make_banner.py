#!/usr/bin/env python3
"""Generate assets/banner.png and assets/social-preview.png (1280x640). Original artwork.
Usage: python scripts/make_banner.py  (reads data/banner.json)"""
import json, math, pathlib, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
root = pathlib.Path(__file__).resolve().parent.parent
cfg = json.loads((root / "data/banner.json").read_text(encoding="utf-8"))
W, H = 1280, 640
N = "/usr/share/fonts/truetype/noto/"
MONO = ImageFont.truetype(N + "NotoSansMono-Bold.ttf", 15)
def F(name, s): return ImageFont.truetype(N + name, s)
rnd = random.Random(7)
# 1) dense tiled-text texture, colored by a diagonal gradient
words = cfg["tile_words"]
tex = Image.new("RGB", (W, H), (8, 9, 12)); td = ImageDraw.Draw(tex)
c0, c1, c2 = [tuple(c) for c in cfg["gradient"]]   # left, middle, right colours
def grad(x, y):
    t = min(1, max(0, (x / W) * 0.8 + (y / H) * 0.2))
    a, b, u = (c0, c1, t * 2) if t < .5 else (c1, c2, (t - .5) * 2)
    return tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))
y = -6
while y < H:
    x = -rnd.randint(0, 120)
    while x < W:
        w = rnd.choice(words)
        r, g, b = grad(x, y)
        k = 0.22 + 0.78 * (max(0, x) / W) ** 1.4          # stronger on the right
        if rnd.random() < 0.12: k = min(1, k * 1.8)
        td.text((x, y), w, font=MONO, fill=(int(r * k), int(g * k), int(b * k)))
        x += int(td.textlength(w, font=MONO)) + 12
    y += 19
# 2) left vignette so the title reads
shade = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(shade)
for x in range(W):
    sd.line([(x, 0), (x, H)], fill=int(235 * max(0, 1 - x / 880) ** 0.8))
img = Image.composite(Image.new("RGB", (W, H), (7, 8, 11)), tex, shade)
d = ImageDraw.Draw(img, "RGBA")
# 3) glasses mark + "awesome" wordmark (original drawing)
gx, gy = 70, 66
col = (225, 228, 235, 255)
d.rounded_rectangle((gx, gy, gx + 66, gy + 40), 16, fill=col)
d.rounded_rectangle((gx + 80, gy, gx + 146, gy + 40), 16, fill=col)
d.arc((gx + 56, gy - 6, gx + 90, gy + 22), 200, 340, fill=col, width=6)
d.line([(gx, gy + 6), (gx - 12, gy - 6)], fill=col, width=6); d.line([(gx + 146, gy + 6), (gx + 158, gy - 6)], fill=col, width=6)
d.text((gx + 180, gy - 10), "awesome", font=F("NotoSansMono-Bold.ttf", 54), fill=(225, 228, 235, 255))
# 4) title
ser = F("NotoSerif-BoldItalic.ttf", cfg.get("title_size", 96))
for i, line in enumerate(cfg["title"]):
    d.text((66, 150 + i * 108), line, font=ser, fill=(255, 255, 255, 255))
# 5) subtitle lines
cy = 420
d.text((70, cy), cfg["sub1"], font=F("NotoSansMono-Bold.ttf", 33), fill=(255, 255, 255, 255))
d.text((70, cy + 52), cfg["sub2"], font=F("NotoSansMono-Bold.ttf", 33), fill=(255, 255, 255, 255))
d.rounded_rectangle((60, 556, 60 + d.textlength(cfg["foot"], font=F("NotoSansMono-Bold.ttf", 17)) + 24, 596), 10, fill=(8, 9, 12, 200)); d.text((72, 566), cfg["foot"], font=F("NotoSansMono-Bold.ttf", 17), fill=(170, 176, 190, 255))
# 6) film-strip mark (original drawing)
sx, sy = 830, 110
d.rounded_rectangle((sx, sy, sx + 330, sy + 260), 22, fill=(8, 9, 12, 170), outline=(255, 255, 255, 90), width=3)
for i in range(7):
    for yy in (sy + 14, sy + 232):
        d.rounded_rectangle((sx + 18 + i * 44, yy, sx + 18 + i * 44 + 24, yy + 14), 4, fill=(225, 228, 235, 230))
d.rounded_rectangle((sx + 28, sy + 42, sx + 302, sy + 218), 12, fill=(20, 22, 30, 255), outline=(255, 255, 255, 120), width=2)
d.polygon([(sx + 140, sy + 85), (sx + 140, sy + 175), (sx + 215, sy + 130)], fill=(255, 255, 255, 255))
(root / "assets").mkdir(exist_ok=True)
img.save(root / "assets/banner.png", optimize=True); img.save(root / "assets/social-preview.png", optimize=True)
print("ok")
