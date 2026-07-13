# Local-only high-res fullface ASCII generator (photo never committed).
# Usage: python gen_fullface.py <source_image> [out.txt]
from PIL import Image, ImageOps, ImageFilter
from collections import deque
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "portrait.png"
OUT = sys.argv[2] if len(sys.argv) > 2 else "ascii_fullface.txt"
COLS, ROWS = 104, 78         # ~2x density; cell 4.3x7.2 -> ~447x562
RAMP = " .,:;i1tfLCG08@"

img = Image.open(SRC).convert("L")
img = ImageOps.exif_transpose(img)
w, h = img.size
# head-first crop: sides trimmed, stop above mid-chest
img = img.crop((int(w * 0.12), int(h * 0.02), int(w * 0.88), int(h * 0.72)))
img = ImageOps.autocontrast(img, cutoff=1)
w, h = img.size

target = (COLS * 4.3) / (ROWS * 7.2)
cur = w / h
if cur > target:
    nw = int(h * target); x0 = (w - nw) // 2
    img = img.crop((x0, 0, x0 + nw, h))
else:
    nh = int(w / target); y0 = max(0, int((h - nh) * 0.20))
    img = img.crop((0, y0, w, y0 + nh))

img = img.filter(ImageFilter.MedianFilter(3))
small = img.resize((COLS, ROWS), Image.LANCZOS)
px = small.load()

bg = [[False] * COLS for _ in range(ROWS)]
q = deque()
for x in range(COLS):
    for y in (0, ROWS - 1):
        if px[x, y] > 175: q.append((x, y))
for y in range(ROWS):
    for x in (0, COLS - 1):
        if px[x, y] > 175: q.append((x, y))
seen = set(q)
while q:
    x, y = q.popleft()
    bg[y][x] = True
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx, ny = x+dx, y+dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and (nx,ny) not in seen and px[nx,ny] > 165:
            seen.add((nx,ny)); q.append((nx,ny))

lines = []
for y in range(ROWS):
    row = []
    for x in range(COLS):
        if bg[y][x]: row.append(" "); continue
        d = (1.0 - px[x, y]/255.0) ** 0.85
        row.append(RAMP[min(len(RAMP)-1, int(d*len(RAMP)))])
    lines.append("".join(row).rstrip())
open(OUT, "w", encoding="ascii").write("\n".join(lines))
print(f"{len(lines)} rows, max width {max(len(l) for l in lines)}")
