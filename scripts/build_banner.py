"""Builds assets/banner.svg: Matrix rain + typed techfren wordmark. Self-contained (font embedded)."""
import base64, random, subprocess, sys, tempfile, pathlib

FONT = sys.argv[1]
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "banner.svg"
W, H = 1200, 320
WORD = "techfren"
random.seed(47)

with tempfile.TemporaryDirectory() as d:
    sub = f"{d}/f.woff2"
    subprocess.run(["pyftsubset", FONT, f"--text={WORD}_", "--flavor=woff2", f"--output-file={sub}"], check=True)
    font64 = base64.b64encode(open(sub, "rb").read()).decode()

GLYPHS = "01アイウエオカキクケコサシスセソタチツテトナニヌネノ<>/{}[]=+*"
cols = []
step = 20
for i, x in enumerate(range(10, W, step)):
    n = random.randint(8, 18)
    dur = random.uniform(5, 11)
    delay = -random.uniform(0, dur)
    op = random.choice([0.18, 0.25, 0.32, 0.45])
    parts = []
    for j in range(n):
        g = random.choice(GLYPHS).replace("<", "&lt;").replace(">", "&gt;")
        cls = ' class="h"' if j == n - 1 else ""
        parts.append(f'<tspan x="{x}" dy="18"{cls}>{g}</tspan>')
    tspans = "".join(parts)
    cols.append(
        f'<text class="r" opacity="{op}">{tspans}'
        f'<animateTransform attributeName="transform" type="translate" from="0 {-(n*18+20)}" to="0 {H+20}" '
        f'dur="{dur:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/></text>'
    )

size = 84
x0 = (W - size * len(WORD)) / 2
letters = "".join(
    f'<text class="w" x="{x0 + i*size:.0f}" y="178" style="animation-delay:{0.4 + i*0.2:.1f}s">{c}</text>'
    for i, c in enumerate(WORD)
)
cursor_x = x0 + size * len(WORD) + 6

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="techfren: AJ tells computers what to do in plain English">
<style>
@font-face{{font-family:'PS2P';src:url(data:font/woff2;base64,{font64}) format('woff2')}}
.r{{font:16px monospace;fill:#00ff00}}
.r .h{{fill:#d8ffd8}}
.w{{font:{size}px 'PS2P',monospace;fill:#00ff00;opacity:0;animation:in .01s linear forwards;filter:drop-shadow(0 0 10px #00ff00)}}
@keyframes in{{to{{opacity:1}}}}
.c{{fill:#00ff00;animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.t{{font:22px monospace;fill:#8dff8d;opacity:0;animation:in .6s ease 2.2s forwards}}
@media (prefers-reduced-motion:reduce){{.w,.t{{animation:none;opacity:1}}.c{{animation:none}}}}
</style>
<defs>
<clipPath id="k"><rect width="{W}" height="{H}" rx="8"/></clipPath>
<radialGradient id="v" cx="50%" cy="50%" r="60%"><stop offset="0" stop-color="#000" stop-opacity=".92"/><stop offset=".55" stop-color="#000" stop-opacity=".7"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
</defs>
<g clip-path="url(#k)">
<rect width="{W}" height="{H}" fill="#000"/>
{"".join(cols)}
<rect width="{W}" height="{H}" fill="url(#v)"/>
{letters}
<rect class="c" x="{cursor_x:.0f}" y="100" width="14" height="80"/>
<text class="t" x="{W/2}" y="236" text-anchor="middle">I tell computers what to do in plain English</text>
</g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="8" fill="none" stroke="#008000" stroke-width="2"/>
</svg>
'''
OUT.write_text(svg)
print(OUT, len(svg) // 1024, "KB")
