# Hero SVG generator. Regenerates ../assets/profile-hero-{dark,light}-v2.svg
# from ascii_portrait.txt. The source photo is NOT in this repo by design;
# regenerate the ASCII with ascii_gen.py <photo> if the portrait must change.
# Emits assets/profile-hero-dark-v2.svg and profile-hero-light-v2.svg from one template.
# Pure SVG + SMIL. No scripts, no external URLs, no raster embeds, no foreignObject.
import html, os

import os
_D = os.path.dirname(os.path.abspath(__file__))
ASCII = [l.rstrip("\n") for l in open(os.path.join(_D, "ascii_portrait.txt"), encoding="ascii")]
CW_A = 5.3          # ascii char advance
FS_A = 9.0          # ascii font-size
LH_A = 9.6          # ascii line-height
ROWS = len(ASCII)
COLS = max((len(r) for r in ASCII), default=72)

W, H, PAD, R = 1180, 610, 24, 24
LX, LY, LW, LH = 24, 24, 430, 562
RX, RY, RW, RH = 470, 24, 686, 562

PHRASES = [
    "AI Security & AgentOps Builder",
    "Securing AI coding agents & MCP",
    "Blocking data leaks with AI DLP",
    "Fine-tuning LLMs for doc security",
]
SKILLS = ["TypeScript", "Python", "Node.js", "Next.js/React", "FastAPI",
          "PyTorch", "Hugging Face", "Docker", "PostgreSQL", "GitHub Actions"]

THEMES = {
    "dark": dict(
        bg="#000000", panel="#020906", panelOp="0.88", border="rgba(0,209,132,0.08)",
        borderHex="#00D184", borderOp="0.10", text="#BFE8D6", muted="#2E5244",
        g0="#00C97A", g1="#00AFC7", g2="#2EA043",
        blobA="#02291F", blobB="#02242C", blobC="#03200F", blobOp="0.22",
        pill="#020D08", pillTx="#4ED9A4", titlebar="#010604", glow="#00D184",
        sheen="#00D184", sheenOp="0.02", noiseOp="0.05", scan="#00D184"),
    "light": dict(
        bg="#010204", panel="#020906", panelOp="0.88", border="rgba(0,175,199,0.08)",
        borderHex="#00AFC7", borderOp="0.10", text="#BFE8D6", muted="#2E5244",
        g0="#00AFC7", g1="#00C97A", g2="#2EA043",
        blobA="#02242C", blobB="#02291F", blobC="#03200F", blobOp="0.22",
        pill="#020D08", pillTx="#4ED9A4", titlebar="#010604", glow="#00AFC7",
        sheen="#00AFC7", sheenOp="0.02", noiseOp="0.05", scan="#00AFC7"),
}


def esc(s):
    return html.escape(s, quote=True)


def clamp01(v):
    return max(0.0, min(1.0, v))


def typing_anims(idx, full_w):
    """clip-rect width + phrase opacity keyTimes/values over a 12s loop."""
    T = 12.0
    s = idx * 3.0
    t = s + 1.5     # typing done
    h = s + 3.0     # phrase window end
    eps = 0.0008
    # width
    kt, vw = [], []

    def add(k, v):
        k = clamp01(k)
        if kt and abs(k - kt[-1]) < 1e-9:
            k = min(1.0, kt[-1] + eps)
        kt.append(k)
        vw.append(v)
    if s <= 0:
        add(0.0, 0); add(t / T, full_w); add(h / T, full_w); add(h / T + eps, 0); add(1.0, 0)
    elif h >= T:
        add(0.0, 0); add(s / T, 0); add(t / T, full_w); add(1.0, full_w)
    else:
        add(0.0, 0); add(s / T, 0); add(t / T, full_w); add(h / T, full_w); add(h / T + eps, 0); add(1.0, 0)
    width_kt = ";".join(f"{k:.4f}" for k in kt)
    width_v = ";".join(f"{v:.1f}" if isinstance(v, float) else str(v) for v in vw)
    # opacity
    ok, ov = [], []

    def addo(k, v):
        k = clamp01(k)
        if ok and abs(k - ok[-1]) < 1e-9:
            k = min(1.0, ok[-1] + eps)
        ok.append(k)
        ov.append(v)
    if s <= 0:
        addo(0.0, 1); addo(h / T, 1); addo(h / T + eps, 0); addo(1.0, 0)
    elif h >= T:
        addo(0.0, 0); addo(s / T - eps, 0); addo(s / T, 1); addo(1.0, 1)
    else:
        addo(0.0, 0); addo(s / T - eps, 0); addo(s / T, 1); addo(h / T, 1); addo(h / T + eps, 0); addo(1.0, 0)
    op_kt = ";".join(f"{k:.4f}" for k in ok)
    op_v = ";".join(str(v) for v in ov)
    return width_kt, width_v, op_kt, op_v


def build(theme):
    c = THEMES[theme]
    P = []
    P.append('<?xml version="1.0" encoding="UTF-8"?>')
    P.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
             f'width="{W}" height="{H}" font-family="\'Consolas\',\'Menlo\',\'DejaVu Sans Mono\',monospace" '
             f'role="img" aria-label="pk42ac profile hero">')

    # ---------- defs ----------
    P.append("<defs>")
    # accent gradient (flowing color shift)
    P.append('<linearGradient id="acc" x1="0" y1="0" x2="1" y2="1">')
    for off, (a, b, d) in zip(("0", "0.5", "1"),
                              ((c["g0"], c["g1"], c["g2"]),
                               (c["g1"], c["g2"], c["g0"]),
                               (c["g2"], c["g0"], c["g1"]))):
        P.append(f'<stop offset="{off}" stop-color="{a}">'
                 f'<animate attributeName="stop-color" values="{a};{b};{d};{a}" '
                 f'dur="7s" repeatCount="indefinite"/></stop>')
    P.append("</linearGradient>")
    # border shimmer gradient
    P.append('<linearGradient id="shim" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="{c["g0"]}"/>'
             f'<stop offset="0.5" stop-color="{c["g1"]}"/>'
             f'<stop offset="1" stop-color="{c["g2"]}"/>'
             '<animateTransform attributeName="gradientTransform" type="translate" '
             'values="-1 0;1 0;-1 0" dur="8s" repeatCount="indefinite"/>'
             "</linearGradient>")
    # radial blobs
    for n, col in (("blobA", c["blobA"]), ("blobB", c["blobB"]), ("blobC", c["blobC"])):
        P.append(f'<radialGradient id="{n}"><stop offset="0" stop-color="{col}" stop-opacity="{c["blobOp"]}"/>'
                 f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>')
    # panel sheen
    P.append('<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0" stop-color="{c["sheen"]}" stop-opacity="{c["sheenOp"]}"/>'
             f'<stop offset="0.4" stop-color="{c["sheen"]}" stop-opacity="0"/></linearGradient>')
    # scanline gradient
    P.append('<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{c["scan"]}" stop-opacity="0"/>'
             f'<stop offset="0.5" stop-color="{c["scan"]}" stop-opacity="0.16"/>'
             f'<stop offset="1" stop-color="{c["scan"]}" stop-opacity="0"/></linearGradient>')
    # glow filter
    P.append('<filter id="glow" x="-40%" y="-40%" width="180%" height="180%">'
             '<feGaussianBlur stdDeviation="2.2" result="b"/>'
             '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    P.append('<filter id="softglow" x="-60%" y="-60%" width="220%" height="220%">'
             '<feGaussianBlur stdDeviation="6" result="b"/>'
             '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    # noise
    P.append('<filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.9" '
             'numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>')
    # clips
    P.append(f'<clipPath id="cardClip"><rect x="0" y="0" width="{W}" height="{H}" rx="{R}"/></clipPath>')
    P.append(f'<clipPath id="leftClip"><rect x="{LX}" y="{LY}" width="{LW}" height="{LH}" rx="18"/></clipPath>')
    for i, ph in enumerate(PHRASES):
        P.append(f'<clipPath id="type{i}"><rect id="cr{i}" x="{RX+34}" y="150" width="0" height="34"/></clipPath>')
    P.append("</defs>")

    # ---------- background ----------
    P.append(f'<g clip-path="url(#cardClip)">')
    P.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{c["bg"]}"/>')
    # floating blobs
    blobs = [("blobA", 240, 180, 360), ("blobB", 900, 120, 320), ("blobC", 620, 560, 400),
             ("blobA", 1050, 470, 300)]
    for j, (n, cx, cy, r) in enumerate(blobs):
        P.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{n})">'
                 f'<animateTransform attributeName="transform" type="translate" '
                 f'values="0 0;{18 if j%2 else -18} {-14 if j%2 else 16};0 0" '
                 f'dur="{11+j*2}s" repeatCount="indefinite"/></circle>')
    # noise overlay
    P.append(f'<rect x="0" y="0" width="{W}" height="{H}" filter="url(#noise)" opacity="{c["noiseOp"]}"/>')
    # particles
    for k in range(9):
        px = 60 + k * 125
        dur = 9 + (k % 5) * 1.7
        P.append(f'<circle cx="{px}" cy="{H+10}" r="{1.6 + (k%3)*0.7:.1f}" fill="url(#acc)" opacity="0.55">'
                 f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -{H+40}" '
                 f'dur="{dur:.1f}s" repeatCount="indefinite" begin="{k*0.9:.1f}s"/>'
                 f'<animate attributeName="opacity" values="0;0.6;0" dur="{dur:.1f}s" '
                 f'repeatCount="indefinite" begin="{k*0.9:.1f}s"/></circle>')

    # ---------- left panel ----------
    P.append(f'<rect x="{LX}" y="{LY}" width="{LW}" height="{LH}" rx="18" fill="{c["panel"]}" '
             f'fill-opacity="{c["panelOp"]}" stroke="{c["borderHex"]}" stroke-opacity="{c["borderOp"]}"/>')
    P.append(f'<rect x="{LX}" y="{LY}" width="{LW}" height="{LH}" rx="18" fill="url(#sheen)"/>')
    # ascii portrait (clipped, floating group)
    ax = LX + (LW - COLS * CW_A) / 2
    ay = LY + 34
    P.append(f'<g clip-path="url(#leftClip)"><g filter="url(#glow)">'
             f'<animateTransform attributeName="transform" type="translate" '
             f'values="0 0;0 -4;0 0;0 4;0 0" dur="6s" repeatCount="indefinite"/>')
    reveal_total = 2.6
    for i, row in enumerate(ASCII):
        if not row.strip():
            continue
        y = ay + i * LH_A
        beg = i / max(1, ROWS) * reveal_total
        tl = f' textLength="{len(row)*CW_A:.1f}" lengthAdjust="spacingAndGlyphs"' if row else ""
        P.append(f'<text x="{ax:.1f}" y="{y:.1f}" font-size="{FS_A}" fill="url(#acc)" '
                 f'xml:space="preserve"{tl} opacity="0">{esc(row)}'
                 f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" '
                 f'begin="{beg:.2f}s" fill="freeze"/></text>')
    # ascii cursor (blink) after last non-empty row
    last_y = ay + (ROWS - 1) * LH_A
    P.append(f'<rect x="{ax:.1f}" y="{last_y+4:.1f}" width="7" height="9" fill="{c["glow"]}" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;1;1;0" dur="1s" '
             f'begin="{reveal_total:.2f}s" repeatCount="indefinite"/></rect>')
    P.append("</g>")
    # scanline sweep over left panel
    P.append(f'<rect x="{LX}" y="{LY}" width="{LW}" height="70" fill="url(#scanG)">'
             f'<animateTransform attributeName="transform" type="translate" '
             f'values="0 -80;0 {LH+10}" dur="4.5s" repeatCount="indefinite"/></rect>')
    P.append("</g>")  # end leftClip group

    # ---------- right panel (terminal) ----------
    P.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="18" fill="{c["panel"]}" '
             f'fill-opacity="{c["panelOp"]}" stroke="{c["borderHex"]}" stroke-opacity="{c["borderOp"]}"/>')
    P.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="18" fill="url(#sheen)"/>')
    # titlebar
    P.append(f'<path d="M{RX} {RY+40} v-16 a18 18 0 0 1 18 -18 h{RW-36} a18 18 0 0 1 18 18 v16 Z" '
             f'fill="{c["titlebar"]}"/>')
    for di, dc in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        P.append(f'<circle cx="{RX+26+di*20}" cy="{RY+20}" r="6" fill="{dc}"/>')
    P.append(f'<text x="{RX+RW/2}" y="{RY+25}" font-size="13" fill="{c["muted"]}" '
             f'text-anchor="middle">pk42ac@github: ~</text>')

    tx = RX + 34
    # greeting
    P.append(f'<text x="{tx}" y="{RY+92}" font-size="26" fill="{c["text"]}" font-weight="700" '
             f'xml:space="preserve" opacity="0">Hi \U0001F44B  I\u2019m pk42ac \u00b7 \ubc15\uc131\ud638'
             f'<animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="0.2s" fill="freeze"/></text>')
    # prompt line + typing
    P.append(f'<text x="{tx}" y="{RY+150}" font-size="20" fill="{c["g1"]}" xml:space="preserve">'
             f'<tspan fill="{c["muted"]}">$</tspan> role</text>')
    tin_x = tx + 78
    for i, ph in enumerate(PHRASES):
        wkt, wv, okt, ov = typing_anims(i, len(ph) * 11.5 + 6)
        # move clip rect x to typing start
        P.append(f'<g clip-path="url(#type{i})">'
                 f'<text x="{tin_x}" y="{RY+150}" font-size="20" fill="url(#acc)" '
                 f'font-weight="600" xml:space="preserve" opacity="0">{esc(ph)}'
                 f'<animate attributeName="opacity" values="{ov}" keyTimes="{okt}" '
                 f'dur="12s" repeatCount="indefinite"/></text></g>')
        # animate this phrase's clip rect: reposition x + width
        # (set x once via attribute; width animated)
    # fix clip rect x positions + width animation (added after defs referencing)
    # cursor for typing
    P.append(f'<rect x="{tin_x-16}" y="{RY+132}" width="10" height="24" fill="{c["glow"]}">'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" '
             f'dur="1s" repeatCount="indefinite"/></rect>')

    # skill pills (2 rows x 5), sequential reveal
    py0 = RY + 210
    pill_h = 40
    col_w = (RW - 68) / 5
    for i, sk in enumerate(SKILLS):
        r = i // 5
        col = i % 5
        pxp = tx + col * col_w
        pyp = py0 + r * 56
        pw = col_w - 14
        beg = 1.0 + i * 0.14
        P.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" '
                 f'begin="{beg:.2f}s" fill="freeze"/>'
                 f'<rect x="{pxp:.1f}" y="{pyp}" width="{pw:.1f}" height="{pill_h}" rx="12" '
                 f'fill="{c["pill"]}" stroke="url(#acc)" stroke-width="1.3" filter="url(#glow)">'
                 f'<animate attributeName="stroke-opacity" values="0.55;1;0.55" dur="{3+i%3}s" '
                 f'repeatCount="indefinite"/></rect>'
                 f'<text x="{pxp+pw/2:.1f}" y="{pyp+26}" font-size="14" fill="{c["pillTx"]}" '
                 f'text-anchor="middle">{esc(sk)}</text></g>')
    # projects listing (fills dead space between pills and footer)
    lsy = RY + 352
    P.append(f'<text x="{tx}" y="{lsy}" font-size="18" fill="{c["g1"]}" xml:space="preserve" opacity="0">'
             f'<tspan fill="{c["muted"]}">$</tspan> ls ~/projects'
             f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="2.6s" fill="freeze"/></text>')
    PROJECTS = [
        ("agentguard/", "AgentOps security scanner"),
        ("ai-dlp/", "blocks genAI data leakage"),
        ("doc-classification/", "Qwen3 LoRA security labels"),
        ("dacon-bias/", "multimodal VQA bias mitigation"),
    ]
    for i, (name, desc) in enumerate(PROJECTS):
        ly = lsy + 32 + i * 27
        beg = 2.9 + i * 0.22
        P.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" '
                 f'begin="{beg:.2f}s" fill="freeze"/>'
                 f'<text x="{tx}" y="{ly}" font-size="15" fill="url(#acc)" font-weight="600" '
                 f'xml:space="preserve">{esc(name)}</text>'
                 f'<text x="{tx+230}" y="{ly}" font-size="14" fill="{c["muted"]}" '
                 f'xml:space="preserve">{esc(desc)}</text></g>')

    # footer: github mark + label
    fy = RY + RH - 42
    gh_x = tx
    # inline GitHub mark path (from scratch, simplified rounded mark)
    P.append(f'<g transform="translate({gh_x},{fy-14})" fill="{c["text"]}" filter="url(#softglow)">'
             f'<path d="M14 0 C6.3 0 0 6.3 0 14 c0 6.2 4 11.4 9.6 13.3 0.7 0.1 1-0.3 1-0.7 '
             f'0-0.3 0-1.3 0-2.4 -3.9 0.8-4.7-1.9-4.7-1.9 -0.6-1.6-1.5-2-1.5-2 -1.3-0.9 0.1-0.9 0.1-0.9 '
             f'1.4 0.1 2.2 1.5 2.2 1.5 1.3 2.2 3.3 1.6 4.1 1.2 0.1-0.9 0.5-1.6 0.9-1.9 '
             f'-3.1-0.4-6.4-1.6-6.4-7 0-1.5 0.5-2.8 1.4-3.8 -0.1-0.4-0.6-1.8 0.1-3.8 0 0 1.2-0.4 3.9 1.5 '
             f'1.1-0.3 2.3-0.5 3.5-0.5 1.2 0 2.4 0.2 3.5 0.5 2.7-1.8 3.9-1.5 3.9-1.5 0.8 2 0.3 3.4 0.1 3.8 '
             f'0.9 1 1.4 2.3 1.4 3.8 0 5.5-3.3 6.6-6.5 7 0.5 0.4 1 1.3 1 2.6 0 1.9 0 3.4 0 3.9 '
             f'0 0.4 0.3 0.8 1 0.7 5.6-1.9 9.6-7.1 9.6-13.3 C28 6.3 21.7 0 14 0 Z"/></g>')
    P.append(f'<text x="{gh_x+40}" y="{fy+4}" font-size="16" fill="{c["muted"]}">github.com/Sungho-pk42ac</text>')

    # ---------- outer border shimmer ----------
    P.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="{R}" fill="none" '
             f'stroke="url(#shim)" stroke-width="2" opacity="0.55"/>')
    P.append("</g>")  # end cardClip

    # clip-rect x + width animations (placed at end, still valid: reference by id)
    for i, ph in enumerate(PHRASES):
        wkt, wv, okt, ov = typing_anims(i, len(ph) * 11.5 + 6)
        P.append(f'<rect x="{tin_x}" y="132" width="0" height="34" opacity="0"/>')  # noop spacer safety
    P.append("</svg>")
    return "\n".join(P)


# We need the clip rects to actually sit at tin_x and animate width.
# Simplest: regenerate defs clip rects with correct x + inline width animation.
def build_final(theme):
    svg = build(theme)
    c = THEMES[theme]
    tx = RX + 34
    tin_x = tx + 78
    # replace each <rect id="typeR{i}" ...width="0".../> with positioned + animated rect
    for i, ph in enumerate(PHRASES):
        wkt, wv, okt, ov = typing_anims(i, len(ph) * 11.5 + 6)
        old = f'<rect id="cr{i}" x="{RX+34}" y="150" width="0" height="34"/>'
        new = (f'<rect x="{tin_x}" y="{RY+132}" width="0" height="34">'
               f'<animate attributeName="width" values="{wv}" keyTimes="{wkt}" '
               f'dur="12s" repeatCount="indefinite"/></rect>')
        svg = svg.replace(old, new)
    # drop the noop spacer rects
    svg = svg.replace(f'<rect x="{tin_x}" y="132" width="0" height="34" opacity="0"/>', "")
    return svg


os.makedirs(os.path.join(_D, "..", "assets"), exist_ok=True)
for th, fn in (("dark", "profile-hero-dark-v2.svg"), ("light", "profile-hero-light-v2.svg")):
    out = build_final(th)
    p = os.path.join(_D, "..", "assets", fn)
    with open(p, "w", encoding="utf-8") as f:
        f.write(out)
    print(fn, len(out.encode("utf-8")), "bytes")
