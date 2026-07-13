# Fullface hero generator (v3). Regenerates ../assets/profile-hero-{dark,light}-v3.svg
# from ascii_fullface.txt. The source photo is NOT in this repo by design;
# regenerate the ASCII with gen_fullface.py <photo> if the portrait must change.
# Pure SVG + SMIL. No scripts, no external URLs, no raster embeds, no foreignObject.
import html, os

_D = os.path.dirname(os.path.abspath(__file__))
ASCII = [l.rstrip("\n") for l in open(os.path.join(_D, "ascii_fullface.txt"), encoding="ascii")]
ROWS = len(ASCII)
COLS = max((len(r) for r in ASCII), default=104)

W, H = 1180, 610
CW, LH_, FS = 4.3, 7.2, 6.8
AW, AH = COLS * CW, ROWS * LH_
AX, AY = (W - AW) / 2, (H - AH) / 2

TYPED = "pk42ac \u00b7 AI Security & AgentOps Builder"

THEMES = {
    "dark": dict(
        bg="#000000", text="#BFE8D6", muted="#2E5244",
        g0="#00C97A", g1="#00AFC7", g2="#2EA043",
        glow="#00D184", scan="#00D184", noiseOp="0.05",
        blobA="#02291F", blobB="#02242C", blobOp="0.20"),
    "light": dict(
        bg="#010204", text="#BFE8D6", muted="#2E5244",
        g0="#00AFC7", g1="#00C97A", g2="#2EA043",
        glow="#00AFC7", scan="#00AFC7", noiseOp="0.05",
        blobA="#02242C", blobB="#02291F", blobOp="0.20"),
}


def esc(s):
    return html.escape(s, quote=True)


def build(theme):
    c = THEMES[theme]
    P = []
    P.append('<?xml version="1.0" encoding="UTF-8"?>')
    P.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
             f'font-family="\'Consolas\',\'Menlo\',\'DejaVu Sans Mono\',monospace" role="img" '
             f'aria-label="pk42ac \u2014 AI Security &amp; AgentOps Builder">')
    # defs
    P.append("<defs>")
    P.append('<linearGradient id="acc" x1="0" y1="0" x2="1" y2="1">')
    for off, (a, b, d) in zip(("0", "0.5", "1"),
                              ((c["g0"], c["g1"], c["g2"]),
                               (c["g1"], c["g2"], c["g0"]),
                               (c["g2"], c["g0"], c["g1"]))):
        P.append(f'<stop offset="{off}" stop-color="{a}">'
                 f'<animate attributeName="stop-color" values="{a};{b};{d};{a}" dur="9s" repeatCount="indefinite"/></stop>')
    P.append("</linearGradient>")
    P.append('<linearGradient id="shim" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="{c["g0"]}"/><stop offset="0.5" stop-color="{c["g1"]}"/>'
             f'<stop offset="1" stop-color="{c["g2"]}"/>'
             '<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;-1 0" dur="10s" repeatCount="indefinite"/></linearGradient>')
    for n, col in (("blobA", c["blobA"]), ("blobB", c["blobB"])):
        P.append(f'<radialGradient id="{n}"><stop offset="0" stop-color="{col}" stop-opacity="{c["blobOp"]}"/>'
                 f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>')
    P.append('<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{c["scan"]}" stop-opacity="0"/>'
             f'<stop offset="0.5" stop-color="{c["scan"]}" stop-opacity="0.10"/>'
             f'<stop offset="1" stop-color="{c["scan"]}" stop-opacity="0"/></linearGradient>')
    P.append('<linearGradient id="scrim" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{c["bg"]}" stop-opacity="0"/>'
             f'<stop offset="1" stop-color="{c["bg"]}" stop-opacity="0.92"/></linearGradient>')
    P.append('<filter id="glow" x="-40%" y="-40%" width="180%" height="180%">'
             '<feGaussianBlur stdDeviation="1.6" result="b"/>'
             '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    P.append('<filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" '
             'stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>')
    P.append(f'<clipPath id="card"><rect x="0" y="0" width="{W}" height="{H}" rx="24"/></clipPath>')
    tw = len(TYPED) * 12.2
    P.append(f'<clipPath id="typeC"><rect x="152" y="{H-52}" width="0" height="30">'
             f'<animate attributeName="width" from="0" to="{tw:.0f}" dur="2.2s" begin="3.2s" '
             f'calcMode="discrete" fill="freeze" '
             f'values="{";".join(f"{tw*k/len(TYPED):.1f}" for k in range(len(TYPED)+1))}" '
             f'keyTimes="{";".join(f"{k/len(TYPED):.4f}" for k in range(len(TYPED)+1))}"/></rect></clipPath>')
    P.append("</defs>")

    P.append('<g clip-path="url(#card)">')
    P.append(f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>')
    # ambient blobs
    P.append(f'<circle cx="260" cy="180" r="420" fill="url(#blobA)">'
             f'<animateTransform attributeName="transform" type="translate" values="0 0;-16 12;0 0" dur="13s" repeatCount="indefinite"/></circle>')
    P.append(f'<circle cx="950" cy="440" r="380" fill="url(#blobB)">'
             f'<animateTransform attributeName="transform" type="translate" values="0 0;14 -10;0 0" dur="15s" repeatCount="indefinite"/></circle>')
    # watermark
    P.append(f'<text x="150" y="330" font-size="150" font-weight="800" fill="url(#acc)" opacity="0.07" '
             f'transform="rotate(-90 150 330)" text-anchor="middle" letter-spacing="6">pk42ac</text>')
    P.append(f'<text x="{W-40}" y="70" font-size="15" fill="{c["muted"]}" text-anchor="end" opacity="0.9" '
             f'letter-spacing="3">AI SECURITY \u00b7 AGENTOPS</text>')
    # ascii face (floating, glowing, row reveal)
    P.append(f'<g filter="url(#glow)"><animateTransform attributeName="transform" type="translate" '
             f'values="0 0;0 -3;0 0;0 3;0 0" dur="7s" repeatCount="indefinite"/>')
    reveal = 3.0
    for i, row in enumerate(ASCII):
        if not row.strip():
            continue
        y = AY + 8 + i * LH_
        P.append(f'<text x="{AX:.1f}" y="{y:.1f}" font-size="{FS}" fill="url(#acc)" xml:space="preserve" '
                 f'textLength="{len(row)*CW:.1f}" lengthAdjust="spacingAndGlyphs" opacity="0">{esc(row)}'
                 f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" '
                 f'begin="{i/max(1,ROWS)*reveal:.2f}s" fill="freeze"/></text>')
    P.append("</g>")
    # particles
    for k in range(6):
        dur = 11 + (k % 4) * 1.9
        P.append(f'<circle cx="{90+k*195}" cy="{H+8}" r="{1.4+(k%3)*0.6:.1f}" fill="url(#acc)" opacity="0.4">'
                 f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -{H+30}" '
                 f'dur="{dur:.1f}s" repeatCount="indefinite" begin="{k*1.3:.1f}s"/>'
                 f'<animate attributeName="opacity" values="0;0.45;0" dur="{dur:.1f}s" repeatCount="indefinite" begin="{k*1.3:.1f}s"/></circle>')
    # scanline
    P.append(f'<rect x="0" y="0" width="{W}" height="90" fill="url(#scanG)">'
             f'<animateTransform attributeName="transform" type="translate" values="0 -100;0 {H+20}" '
             f'dur="6s" repeatCount="indefinite"/></rect>')
    # noise
    P.append(f'<rect width="{W}" height="{H}" filter="url(#noise)" opacity="{c["noiseOp"]}"/>')
    # bottom scrim + whoami
    P.append(f'<rect x="0" y="{H-130}" width="{W}" height="130" fill="url(#scrim)"/>')
    P.append(f'<text x="48" y="{H-30}" font-size="20" fill="{c["muted"]}" xml:space="preserve" opacity="0">'
             f'$ whoami<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="2.8s" fill="freeze"/></text>')
    P.append(f'<g clip-path="url(#typeC)"><text x="152" y="{H-30}" font-size="20" font-weight="700" '
             f'fill="url(#acc)" xml:space="preserve">{esc(TYPED)}</text></g>')
    P.append(f'<rect x="136" y="{H-48}" width="9" height="22" fill="{c["glow"]}" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.01;0.02;0.5;0.51;1" '
             f'dur="1s" begin="2.8s" repeatCount="indefinite"/></rect>')
    # border shimmer
    P.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="24" fill="none" '
             f'stroke="url(#shim)" stroke-width="2" opacity="0.35"/>')
    P.append("</g></svg>")
    return "\n".join(P)


os.makedirs(os.path.join(_D, "..", "assets"), exist_ok=True)
for th in ("dark", "light"):
    out = build(th)
    p = os.path.join(_D, "..", "assets", f"profile-hero-{th}-v3.svg")
    with open(p, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"profile-hero-{th}-v3.svg", len(out.encode("utf-8")), "bytes")
