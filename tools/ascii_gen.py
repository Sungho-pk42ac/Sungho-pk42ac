# Local-only ASCII portrait generator. The source photo is never committed.
# Usage: python ascii_gen.py <source_image>
# Maps dark features -> dense glyphs (classic portrait mapping), flood-fills
# the light studio background to spaces so the silhouette stays clean.
from PIL import Image, ImageOps, ImageFilter
from collections import deque
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "portrait.png"
COLS, ROWS = 72, 54          # grid; SVG cell ~6x10px -> 432x540 panel
CELL_ASPECT = 6 / 10         # char cell w:h
# XML-safe ramp, light->dark (index by darkness)
RAMP = " .,:;i1tfLCG08@"

img = Image.open(SRC).convert("L")
img = ImageOps.exif_transpose(img)
w, h = img.size

# face-focused pre-crop: trim side margins and lower chest, boost contrast
img = img.crop((int(w * 0.10), int(h * 0.02), int(w * 0.90), int(h * 0.78)))
img = ImageOps.autocontrast(img, cutoff=1)
w, h = img.size
# center-crop to grid pixel aspect (COLS*6 : ROWS*10)
target = (COLS * 6) / (ROWS * 10)
cur = w / h
if cur > target:  # too wide
    nw = int(h * target)
    x0 = (w - nw) // 2
    img = img.crop((x0, 0, x0 + nw, h))
else:             # too tall -> keep top-biased crop (head)
    nh = int(w / target)
    y0 = max(0, int((h - nh) * 0.25))
    img = img.crop((0, y0, w, y0 + nh))

img = img.filter(ImageFilter.MedianFilter(3))
small = img.resize((COLS, ROWS), Image.LANCZOS)
px = small.load()

# flood-fill background from border cells that are bright
bg = [[False] * COLS for _ in range(ROWS)]
q = deque()
for x in range(COLS):
    for y in (0, ROWS - 1):
        if px[x, y] > 175:
            q.append((x, y))
for y in range(ROWS):
    for x in (0, COLS - 1):
        if px[x, y] > 175:
            q.append((x, y))
seen = set(q)
while q:
    x, y = q.popleft()
    bg[y][x] = True
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in seen and px[nx, ny] > 165:
            seen.add((nx, ny))
            q.append((nx, ny))

lines = []
for y in range(ROWS):
    row = []
    for x in range(COLS):
        if bg[y][x]:
            row.append(" ")
            continue
        v = px[x, y] / 255.0
        d = 1.0 - v            # darkness
        d = d ** 0.85          # gamma lift midtones
        idx = min(len(RAMP) - 1, int(d * len(RAMP)))
        row.append(RAMP[idx])
    lines.append("".join(row).rstrip())

out = "\n".join(lines)
import os
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ascii_portrait.txt"), "w", encoding="ascii") as f:
    f.write(out)
print(out)
print(f"\n-- {len(lines)} rows, max width {max(len(l) for l in lines)}", file=sys.stderr)
