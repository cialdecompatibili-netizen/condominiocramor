# -*- coding: utf-8 -*-
# GUIDA-SVILUPPO: logo + favicon "palazzo" (torre centrale + due palazzi laterali) coi colori di _data/tema.json.
# Disegnato su griglia 64x64 con finestre GRANDI, cosi' si legge anche a 16px. Uso: python automation/genera_logo_palazzo.py ["#accent" "#dark"]
# Scrive in assets/images: favicon.svg, favicon-32/192/512.png, apple-touch-icon.png, logo-72.png, favicon.ico (e copia favicon.ico/svg nella radice se esistono).
import json, os, shutil, sys
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); IMG = os.path.join(ROOT, 'assets', 'images')
def hx(s): s = s.lstrip('#'); return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))
def mix(a, b, t): return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
def h(c): return '#%02x%02x%02x' % c
tema = json.load(open(os.path.join(ROOT, '_data', 'tema.json'), encoding='utf-8'))
acc = sys.argv[1] if len(sys.argv) > 1 else tema.get('accent', '#1f4e79'); dark = sys.argv[2] if len(sys.argv) > 2 else tema.get('accent_dark', '#14304d')
TOP = mix(hx(acc), (255, 255, 255), .12); BOT = mix(hx(dark), hx(acc), .25)
# forme: (x0, y0, x1, y1) sulla griglia 64
TOWER = [(19, 11, 45, 56), (17, 8.5, 47, 12)]            # corpo + cornicione
SIDES = [(8, 28, 19, 56), (45, 22, 56, 56)]              # palazzi laterali (piu' chiari)
WIN_T = [(24, y, 30, y + 5) for y in (17, 26, 35)] + [(34, y, 40, y + 5) for y in (17, 26, 35)] + [(28, 46, 36, 56)]   # finestre torre + portone
WIN_S = [(11, y, 16, y + 5) for y in (32, 41)] + [(48, y, 53, y + 5) for y in (27, 36, 45)]
SIDE_A = .62   # opacita' dei palazzi laterali
svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (h(TOP), h(BOT)), '<mask id="m"><rect width="64" height="64" fill="#000"/>']
svg += ['<rect x="%s" y="%s" width="%s" height="%s" fill="#fff"/>' % (a, b, c - a, d - b) for a, b, c, d in TOWER]
svg += ['<rect x="%s" y="%s" width="%s" height="%s" fill="#fff" fill-opacity="%s"/>' % (a, b, c - a, d - b, SIDE_A) for a, b, c, d in SIDES]
svg += ['<rect x="%s" y="%s" width="%s" height="%s" fill="#000"/>' % (a, b, c - a, d - b) for a, b, c, d in WIN_T + WIN_S]
svg += ['</mask></defs><rect width="64" height="64" rx="14" fill="url(#s)"/><rect width="64" height="64" fill="#f4f7fb" mask="url(#m)"/></svg>\n']
open(os.path.join(IMG, 'favicon.svg'), 'w', encoding='utf-8', newline='\n').write(''.join(svg))
def render(px):
    K = 1024; k = K / 64
    bg = Image.new('RGB', (K, K)); d = ImageDraw.Draw(bg)
    for y in range(K): d.line([(0, y), (K, y)], fill=mix(TOP, BOT, y / (K - 1)))
    m = Image.new('L', (K, K), 0); md = ImageDraw.Draw(m)
    for a, b, c, e in TOWER: md.rectangle([a * k, b * k, c * k - 1, e * k - 1], fill=255)
    for a, b, c, e in SIDES: md.rectangle([a * k, b * k, c * k - 1, e * k - 1], fill=round(255 * SIDE_A))
    for a, b, c, e in WIN_T + WIN_S: md.rectangle([a * k, b * k, c * k - 1, e * k - 1], fill=0)
    bg.paste(Image.new('RGB', (K, K), (244, 247, 251)), (0, 0), m)
    rr = Image.new('L', (K, K), 0); ImageDraw.Draw(rr).rounded_rectangle([0, 0, K - 1, K - 1], radius=int(14 * k), fill=255)
    out = Image.new('RGBA', (K, K), (0, 0, 0, 0)); out.paste(bg, (0, 0), rr)
    return out.resize((px, px), Image.LANCZOS)
for name, px in (('favicon-32.png', 32), ('favicon-192.png', 192), ('favicon-512.png', 512), ('logo-72.png', 72)): render(px).save(os.path.join(IMG, name))
ap = Image.new('RGB', (180, 180), mix(TOP, BOT, .5)); ap.paste(render(180), (0, 0), render(180)); ap.save(os.path.join(IMG, 'apple-touch-icon.png'))
render(256).save(os.path.join(IMG, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
for f in ('favicon.ico', 'favicon.svg'):
    if os.path.exists(os.path.join(ROOT, f)): shutil.copy(os.path.join(IMG, f), os.path.join(ROOT, f))
print('logo palazzo scritto')
