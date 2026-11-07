#!/usr/bin/env python3
"""Builds assets/banner.svg (animated, photo embedded). Edit PROFILE, run: python scripts/build_banner.py"""
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILE = dict(
    name="Waqas Ahmad",
    title="Building Ideas into Reality",
    roles=["Flutter & Dart applications", "C++ and logical problem solving",
           "Web development", "Python, learning in public"],
    chips=["Flutter", "Dart", "C++", "Web", "Python"],
    status="Open to collaboration  |  Pakistan",
)
NAVY, NAVY2, GOLD, IVORY, MUTED = "#07101f", "#0f2444", "#d4af37", "#f4efe3", "#9aa9c2"
SERIF, SANS = "Georgia, 'Times New Roman', serif", "'Segoe UI', Inter, Arial, sans-serif"
CYCLE = 3 * len(PROFILE["roles"])

img = base64.b64encode((ROOT / "assets/profile.jpg").read_bytes()).decode()
roles = "".join(
    f'<text class="role" x="92" y="318" style="animation-delay:{i*3}s">{r.replace("&", "&amp;")}</text>'
    for i, r in enumerate(PROFILE["roles"]))
chips, x = "", 92
for i, c in enumerate(PROFILE["chips"]):
    w = 28 + len(c) * 10
    chips += (f'<g class="up" style="animation-delay:{1.3+i*.12}s"><rect x="{x}" y="372" width="{w}" height="34" rx="17" '
              f'fill="none" stroke="{GOLD}" stroke-opacity=".6"/><text x="{x+w/2}" y="394" text-anchor="middle" '
              f'font-size="15" fill="{IVORY}">{c}</text></g>')
    x += w + 12

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 520" width="1280" height="520" role="img" aria-label="{PROFILE['name']}, {PROFILE['title']}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY2}"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f3d98b"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="#8f7116"/></linearGradient>
<radialGradient id="halo"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
<clipPath id="c"><circle cx="1020" cy="260" r="168"/></clipPath>
<pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#fff" stroke-opacity=".035"/></pattern>
</defs>
<style>
text{{font-family:{SANS}}} .serif{{font-family:{SERIF}}}
.up{{opacity:0;animation:up .9s cubic-bezier(.2,.7,.2,1) forwards}}
@keyframes up{{from{{opacity:0;transform:translateY(24px)}}to{{opacity:1;transform:none}}}}
.role{{opacity:0;font-size:30px;fill:{GOLD};animation:cyc {CYCLE}s infinite}}
@keyframes cyc{{0%{{opacity:0;transform:translateY(14px)}}3%,17%{{opacity:1;transform:none}}20%,100%{{opacity:0;transform:translateY(-10px)}}}}
.photo{{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop 1.2s .3s cubic-bezier(.2,.9,.3,1.2) forwards}}
@keyframes pop{{from{{opacity:0;transform:scale(.8)}}to{{opacity:1;transform:scale(1)}}}}
.ring{{transform-box:fill-box;transform-origin:center;animation:spin 50s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.halo{{animation:breathe 5s ease-in-out infinite}}
@keyframes breathe{{50%{{opacity:.55}}}}
.dot{{animation:blink 1.8s infinite}} @keyframes blink{{50%{{opacity:.3}}}}
.line{{stroke-dasharray:560;stroke-dashoffset:560;animation:draw 1.6s .2s ease-out forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
</style>
<rect width="1280" height="520" fill="url(#bg)"/><rect width="1280" height="520" fill="url(#g)"/>
<circle class="halo" cx="1020" cy="260" r="300" fill="url(#halo)"/>
<circle class="ring" cx="1020" cy="260" r="206" fill="none" stroke="{GOLD}" stroke-opacity=".45" stroke-dasharray="3 12" stroke-width="2"/>
<g class="photo"><circle cx="1020" cy="260" r="180" fill="url(#gold)"/><circle cx="1020" cy="260" r="173" fill="{NAVY}"/>
<image href="data:image/jpeg;base64,{img}" x="852" y="92" width="336" height="336" clip-path="url(#c)" preserveAspectRatio="xMidYMid slice"/></g>
<path class="line" d="M92 120H650" stroke="url(#gold)" stroke-width="2"/>
<text class="up" x="92" y="156" font-size="19" fill="{MUTED}" style="animation-delay:.2s;letter-spacing:.5px">{PROFILE['title']}</text>
<text class="up serif" x="90" y="244" font-size="88" fill="{IVORY}" style="animation-delay:.45s">{PROFILE['name']}</text>
{roles}{chips}
<g class="up" style="animation-delay:1.9s"><circle class="dot" cx="100" cy="452" r="5" fill="#3ddc97"/><text x="116" y="458" font-size="16" fill="{MUTED}">{PROFILE['status']}</text></g>
</svg>'''
(ROOT / "assets/banner.svg").write_text(svg, encoding="utf-8")
print("assets/banner.svg written,", len(svg)//1024, "KB")
