"""Globus email link cards (Lesson Follow-up 0.38.0): Globus logo + pictogram + crimson label bar. 480x600, shown at 130x163."""
import os
from PIL import Image, ImageDraw, ImageFont
F = os.environ.get('FONTS', '/home/claude/work/lesson-follow-up/skills/study-notes/assets/fonts/')
LOGO = os.path.join(os.path.dirname(__file__), '..', 'flashcards', 'atotal', 'img', 'globus-logo.png')
CR = (185, 5, 65); CR_D = (143, 4, 51); TINT = (251, 234, 240); INK = (39, 39, 42)
W, H, R, S = 480, 600, 36, 3
def pict(d, kind, cx, cy, s):
    lw = 9 * S
    if kind == 'notes':   # document with folded corner and text lines
        x0, y0, x1, y1 = cx - 78*s, cy - 100*s, cx + 78*s, cy + 100*s
        f = 40*s
        d.polygon([(x0, y0), (x1 - f, y0), (x1, y0 + f), (x1, y1), (x0, y1)], fill=TINT, outline=CR, width=lw)
        d.line([(x1 - f, y0), (x1 - f, y0 + f), (x1, y0 + f)], fill=CR, width=lw, joint='curve')
        for i, ln in enumerate([0.75, 0.9, 0.6, 0.85, 0.5]):
            y = y0 + 70*s + i * 26*s
            d.line([(x0 + 26*s, y), (x0 + 26*s + (x1 - x0 - 52*s) * ln, y)], fill=CR, width=7*S)
    elif kind == 'flashcards':   # 0.40.0: two stacked cards, the front one with "Aa"
        bx0, by0 = cx - 66*s, cy - 112*s
        d.rounded_rectangle([bx0, by0, bx0 + 168*s, by0 + 124*s], 14*S, fill=(255, 255, 255), outline=CR, width=lw)
        x0, y0, x1, y1 = cx - 96*s, cy - 64*s, cx + 76*s, cy + 92*s
        d.rounded_rectangle([x0, y0, x1, y1], 14*S, fill=TINT, outline=CR, width=lw)
        fa = ImageFont.truetype(F + 'Montserrat-Bold.ttf', int(72*s))
        d.text(((x0 + x1) // 2, (y0 + y1) // 2 + 2*s), 'Aa', font=fa, fill=CR, anchor='mm')
    else:                 # clipboard with three ticks
        x0, y0, x1, y1 = cx - 82*s, cy - 96*s, cx + 82*s, cy + 104*s
        d.rounded_rectangle([x0, y0, x1, y1], 14*S, fill=TINT, outline=CR, width=lw)
        d.rounded_rectangle([cx - 38*s, y0 - 20*s, cx + 38*s, y0 + 18*s], 10*S, fill=CR)
        for i in range(3):
            y = y0 + 58*s + i * 46*s
            d.line([(x0 + 24*s, y), (x0 + 36*s, y + 12*s), (x0 + 58*s, y - 12*s)], fill=CR, width=8*S, joint='curve')
            d.line([(x0 + 76*s, y), (x1 - 24*s, y)], fill=CR, width=7*S)
def card(slug, label):
    w, h = W*S, H*S
    base = Image.new('RGBA', (w, h), (255, 255, 255, 255)); d = ImageDraw.Draw(base)
    lg = Image.open(LOGO).convert('RGBA'); lg = lg.crop(lg.getbbox())
    lw_ = int(w * 0.78); lg = lg.resize((lw_, int(lg.height * lw_ / lg.width)), Image.LANCZOS)
    base.alpha_composite(lg, ((w - lw_) // 2, 44*S))
    bar_y = 462*S
    pict(d, slug, w // 2, (44*S + lg.height + bar_y) // 2 + 6*S, S * 0.92)
    d.rectangle([0, bar_y, w, h], fill=CR); d.rectangle([0, bar_y, w, bar_y + 7*S], fill=CR_D)
    size = 40*S; fb = ImageFont.truetype(F + 'Montserrat-Bold.ttf', size)
    while d.textlength(label, font=fb) > w - 60*S: size -= 2*S; fb = ImageFont.truetype(F + 'Montserrat-Bold.ttf', size)
    fr = ImageFont.truetype(F + 'Montserrat-Bold.ttf', 22*S)
    cy = bar_y + 7*S + (h - bar_y - 7*S) // 2
    d.text((w // 2, cy - 16*S), label, font=fb, fill='white', anchor='mm')
    d.text((w // 2, cy + 30*S), 'OPEN  ›', font=fr, fill=(255, 205, 220), anchor='mm')
    mask = Image.new('L', (w, h), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], R*S, fill=255)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); im.paste(base, (0, 0), mask)
    ImageDraw.Draw(im).rounded_rectangle([S, S, w - 1 - S, h - 1 - S], R*S, outline=CR + (255,), width=4*S)
    im = im.resize((W, H), Image.LANCZOS)
    out = os.path.join(os.path.dirname(__file__), '..', 'cards', 'globus-card-%s.png' % slug)
    im.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG).save(out, optimize=True)
    return out
import sys
ALL = [('notes', 'Study Notes'), ('test', 'Practice Test'), ('flashcards', 'Flashcards')]
only = sys.argv[1:]   # e.g. python3 make_globus_cards.py flashcards -> build just that card
outs = [card(k, l) for k, l in ALL if not only or k in only]
ims = [Image.open(o).convert('RGBA') for o in outs]
sheet = Image.new('RGBA', (W*len(ims) + 12*(len(ims) + 1), H + 40), (240, 240, 240, 255))
for i, x in enumerate(ims): sheet.alpha_composite(x, (12 + i*(W + 12), 20))
sheet.convert('RGB').save('/tmp/globus-cards-preview.jpg', quality=88)
print(outs)
